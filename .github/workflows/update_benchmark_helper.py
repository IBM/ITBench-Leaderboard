import argparse
import json
import logging
import os
import re
import textwrap
import urllib.request
from dataclasses import asdict, dataclass, field
from datetime import datetime, timedelta, timezone
from typing import Any, Dict, List, Optional
from urllib.parse import urlparse

ITBENCH_API = os.getenv("ITBENCH_API")
ITBENCH_API_TOKEN = os.getenv("ITBENCH_API_TOKEN")
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")

logger = logging.getLogger(__name__)
loglevel = logging.getLevelNamesMapping().get(LOG_LEVEL, logging.INFO)
logging.basicConfig(level=loglevel, format="%(asctime)s - %(levelname)s - %(message)s")
logger.setLevel(loglevel)


@dataclass
class UpdatedIssue:
    number: int
    github_username: str
    benchmark_id: str
    comments: List[Dict[str, Any]] = field(default_factory=list)


@dataclass
class BenchmarkStatus:
    number: int
    github_username: str
    benchmark_id: str
    agent_type: str
    status: str
    error_message: Optional[str] = None
    results: List[Dict[str, Any]] = field(default_factory=list)
    status_comment_id: Optional[str] = None


@dataclass
class BenchmarkStatusComment:
    number: int
    comment: str
    closed: bool
    status_comment_id: Optional[str] = None


def output(args, data):
    if args.output:
        with open(args.output, "w") as f:
            f.write(data)
    else:
        print(data)


class ParseCommand:

    def exec(self, args):
        with open(args.input, "r") as f:
            issues = json.load(f)

        updated_issues: List[UpdatedIssue] = []
        for issue in issues:
            number = issue.get("number")
            author = issue.get("author", {})
            comments = issue.get("comments", [])
            benchmark_id_comments = [{"comment": x, "benchmark_id": self.extract_benchmark_id(x)} for x in comments]
            benchmark_id_comment = [x for x in benchmark_id_comments if x.get("benchmark_id")]
            if len(benchmark_id_comment) == 0:
                logger.warning(f"No Benchmark ID comment found for issue {number}, skipping.")
                continue
            benchmark_id_comment = benchmark_id_comment[0]
            updated_issue = UpdatedIssue(
                number=number,
                github_username=author.get("login"),
                benchmark_id=benchmark_id_comment["benchmark_id"],
                comments=comments,
            )
            updated_issues.append(updated_issue)

        data = json.dumps([asdict(x) for x in updated_issues], indent=2)
        output(args, data)

    def extract_benchmark_id(self, issue):
        pattern = r"<!--hidden-benchmark-id>(?P<id>[0-9a-fA-F-]+)</hidden-benchmark-id-->"
        match = re.search(pattern, issue.get("body", ""))
        if match:
            return match.group("id")
        else:
            return None


class StatusCommand:

    def exec(self, args):
        with open(args.input, "r") as f:
            updated_issues = json.load(f)

        updated_issues = [UpdatedIssue(**x) for x in updated_issues]
        benchmark_statuses: List[BenchmarkStatus] = []
        for upd in updated_issues:
            github_username = upd.github_username
            benchmark_id = upd.benchmark_id

            # find existing status comment
            status_comment = [x for x in upd.comments if re.match(r"^### Status", x.get("body", ""))]
            if len(status_comment) == 0:
                status_comment_id = None
            else:
                # Example GitHub issue comment URL:
                # e.g., https://github.com/yana1205/gitops-bench-0310/issues/10#issuecomment-2726194238
                url = status_comment[0].get("url")  # Retrieve the comment URL from the status data

                # Parse the URL and extract the fragment part (everything after "#")
                # The fragment contains the comment ID, formatted as "issuecomment-<numeric_id>"
                parsed_url = urlparse(url)
                status_comment_id = parsed_url.fragment.replace("issuecomment-", "")  # Extract only the numeric comment ID

            # get results of finished scenarios
            bench_results, error = self.request(
                f"{ITBENCH_API}/gitops/retrieve-results?benchmark_id={benchmark_id}&github_username={github_username}"
            )
            if error:
                bs = self.to_benchmark_status(
                    upd, error_message="Failed to get benchmark progress.", status="Unkown", status_comment_id=status_comment_id
                )
                benchmark_statuses.append(bs)
                continue
            bench_result = bench_results[0]  # benchmark_id is specified in query param so the response should contain only 1 item.
            benchmark = bench_result.get("benchmark", {})
            spec = benchmark.get("spec", {})
            agent_type = spec.get("agent_type", None)
            status = benchmark.get("status", {})
            phase = status.get("phase", "Errored")
            results = bench_result.get("results", {})
            bs = self.to_benchmark_status(upd, agent_type=agent_type, status=phase, status_comment_id=status_comment_id, results=results)
            benchmark_statuses.append(bs)

        data = json.dumps([asdict(x) for x in benchmark_statuses], indent=2)
        output(args, data)

    def request(self, url):
        headers = {"Authorization": f"Bearer {ITBENCH_API_TOKEN}"}
        req = urllib.request.Request(url=url, headers=headers, method="GET")
        res = urllib.request.urlopen(req, timeout=10)
        if res.getcode() != 200:
            logger.error(f"Error requesting benchmark JSON: {res.status_code}. {res.content}")
            return None, True
        res_body = res.read()
        res_dict = json.loads(res_body.decode("utf-8"))
        return res_dict, False

    def to_benchmark_status(
        self, upd: UpdatedIssue, agent_type: str, status: str, status_comment_id, error_message: Optional[str] = None, results: List[Dict[str, Any]] = []
    ):
        return BenchmarkStatus(
            number=upd.number,
            github_username=upd.github_username,
            benchmark_id=upd.benchmark_id,
            agent_type=agent_type,
            error_message=error_message,
            status=status,
            status_comment_id=status_comment_id,
            results=results,
        )


class CommentCommand:

    def exec(self, args):
        with open(args.input, "r") as f:
            benchmark_statuses = json.load(f)
        benchmark_statuses = [BenchmarkStatus(**x) for x in benchmark_statuses]

        benchmark_status_comments: List[BenchmarkStatusComment] = []
        for benchmark_status in benchmark_statuses:
            if benchmark_status.error_message:
                comment = self.to_error_comment(benchmark_status)
            else:
                comment = self.to_comment(benchmark_status)
            closed = benchmark_status.status in ["Finished", "Errored"]
            bsc = BenchmarkStatusComment(
                number=benchmark_status.number,
                status_comment_id=benchmark_status.status_comment_id,
                comment=comment,
                closed=closed,
            )
            benchmark_status_comments.append(bsc)

        data = "\n".join([json.dumps(asdict(x)) for x in benchmark_status_comments])
        data += "\n"
        output(args, data)

    def to_comment(self, benchmark_status: BenchmarkStatus):
        if benchmark_status.agent_type == "CISO":
            table = self.to_table(benchmark_status)
        elif benchmark_status.agent_type == "SRE":
            table = "TBD"
        else:
            table = "TBD"
        timestamp = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
        return f"""\
### Status

#### Benchmark Status
- **Benchmark ID**: {benchmark_status.benchmark_id}
- **Status**: {benchmark_status.status}

#### Results of Finished Scenarios
{table}

#### Last Updated: {timestamp}
"""

    def to_error_comment(self, benchmark_status: BenchmarkStatus):
        return f"""
### Status

#### Benchmark Status
- **Benchmark ID**: {benchmark_status.benchmark_id}
- **Status**: {benchmark_status.status}
- **Message**: {benchmark_status.message}
"""

    def parse_ttr(self, ttr):
        if not ttr:
            return "N/A"

        match = re.match(r"PT(?:(\d+)H)?(?:(\d+)M)?(?:(\d+(?:\.\d+)?)S)?", ttr)
        if not match:
            return "Invalid"

        hours = int(match.group(1)) if match.group(1) else 0
        minutes = int(match.group(2)) if match.group(2) else 0
        seconds = float(match.group(3)) if match.group(3) else 0.0
        return str(int(timedelta(hours=hours, minutes=minutes, seconds=seconds).total_seconds())) + "s"

    def to_table(self, benchmark_status: BenchmarkStatus):
        results = benchmark_status.results
        table = []

        table.append("| Scenario Name | Description | Passed | Time To Resolve | Error | Message | Date |")
        table.append("|---------------|-------------|--------|-----------------|-------|---------|------|")

        for result in results:
            spec = result["spec"]
            name = spec["name"]
            description = spec["description"]
            passed = "✅" if spec["passed"] else "❌"
            errored = "Error" if spec["errored"] else "No error"
            ttr = self.parse_ttr(spec["ttr"])
            date = spec["date"]
            message_text = textwrap.shorten(spec["message"], width=50, placeholder="...")
            table.append(f"| {name} | {description} | {passed} | {ttr} | {errored} | {message_text} | {date} |")

        return "\n".join(table)


def main():
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest="command", required=True)

    parser_parse = subparsers.add_parser("parse", help="Parse issues.json, filter by track flag, extract benchmark id")
    parser_parse.add_argument("-i", "--input", required=True, help="Input file (issues.json)")
    parser_parse.add_argument("-o", "--output", help="Output file (Default. stdout)")
    parser_parse.set_defaults(func=ParseCommand().exec)

    parser_status = subparsers.add_parser("status", help="Get progress and current results of the benchmark")
    parser_status.add_argument("-i", "--input", required=True, help="Input file (parsed issues)")
    parser_status.add_argument("-o", "--output", help="Output file (Default. stdout)")
    parser_status.set_defaults(func=StatusCommand().exec)

    parser_status = subparsers.add_parser("comment", help="Create comment from benchmark statuses")
    parser_status.add_argument("-i", "--input", required=True, help="Input file (benchmark_statuses.json)")
    parser_status.add_argument("-o", "--output", help="Output file (Default. stdout)")
    parser_status.set_defaults(func=CommentCommand().exec)

    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
