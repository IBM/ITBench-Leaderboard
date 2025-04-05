#import ssl
import argparse
import json
import os
import urllib.request
from urllib.parse import urlencode

ITBENCH_API = os.getenv("ITBENCH_API")
ITBENCH_API_TOKEN = os.getenv("ITBENCH_API_TOKEN")
#ITBENCH_CERT = os.getenv("ITBENCH_CERT")


def get_leaderboard(benchmark_id: str = None, github_username: str = None):
    # Required as the current IT Bench server is not using a trusted certificate
    #ssl_context = ssl.create_default_context(cafile=ITBENCH_CERT)
    url = f"{ITBENCH_API}/gitops/aggregate-results"
    query_params = {}
    if benchmark_id is not None:
        query_params["benchmark_id"] = benchmark_id
    if github_username is not None:
        query_params["github_username"] = github_username
    if query_params:
        url += "?" + urlencode(query_params)
    headers = {
        "Authorization" : f"Bearer {ITBENCH_API_TOKEN}"
    }
    req = urllib.request.Request(url=url, headers=headers, method="GET")
    #res = urllib.request.urlopen(req, timeout=10, context=ssl_context) # Use this if using internal server
    res = urllib.request.urlopen(req, timeout=10)
    
    if res.getcode() != 200:
        print(f"Error requesting leaderboard JSON: {res.status_code}. {res.content}")
        exit(1)

    res_body = res.read()
    res_dict = json.loads(res_body.decode("utf-8"))
    return res_dict



def print_table(data):
    header_str = ['Rank', 'Agent Name', 'Overall Score', 'SRE', 'FinOps', 'CISO', 'Notes']
    line_fmt = '| {:^4} | {:^20} | {:^13} | {:^13} | {:^13} | {:^13} | {:<30} |'
    headers = line_fmt.format(*header_str)
    header_len = len(headers)
    print('-' * header_len)
    print(headers)
    print(line_fmt.format(*("---" * 7)))
    for bench_line in data:
        print(line_fmt.format(*bench_line))


SAMPLE_DATA = [
    {
        'name': 'Run-2',
        'incident_type': 'SRE',
        'agent': 'Agent-104',
        'results': [{}] * 10,
        'mttr': 'PT0S',
        'num_of_passed': 2,
        'score': 0.2,
        'date': '2025-03-11T13:54:23.576999Z',
        'id': 'f324b0ca-5065-435e-a140-1db3f409926d',
        'agent_type': 'SRE',
        'github_username': 'Rohan-Arora',
    },
    {
        'name': 'My CISO Agent Benchmark 2',
        'incident_type': 'Gen-CIS-b-K8s-Kyverno',
        'agent': 'My CISO Agent (Yana)',
        'results': [{}] * 10,
        'mttr': 'PT1M5.70376S',
        'num_of_passed': 1,
        'score': 0.1,
        'date': '2025-03-17T00:36:52.334468Z',
        'id': 'de1a2838-e3d0-44bc-885f-53b210c73d19',
        'agent_type': 'CISO',
        'github_username': 'yana1205',
    },
    {
        'name': 'Top SRE Benchmark',
        'incident_type': 'SRE',
        'agent': 'Baseline SRE Agent',
        'results': [{}] * 10,
        'mttr': 'PT30S',
        'num_of_passed': 7,
        'score': 0.70,
        'date': '2025-03-20T12:00:00Z',
        'id': 'aaa-bbb',
        'agent_type': 'SRE',
        'github_username': 'sre_star',
    },
    {
        'name': 'Top CISO Benchmark',
        'incident_type': 'Gen-CIS-b-RHEL9-Ansible-OPA',
        'agent': 'Baseline CISO Agentp',
        'results': [{}] * 10,
        'mttr': 'PT1M',
        'num_of_passed': 6,
        'score': 0.6,
        'date': '2025-03-20T12:10:00Z',
        'id': 'ccc-ddd',
        'agent_type': 'CISO',
        'github_username': 'ciso_champ',
    }
]
if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="Print IT Bench leaderboard")
    parser.add_argument("leaderboard")
    parser.add_argument("-u", "--github_username", type=str)
    parser.add_argument("-b", "--benchmark_id", type=str)
    parser.add_argument("--sample", action="store_true", help="Use sample data")
    args = parser.parse_args()
    if args.sample:
        leaderboard = SAMPLE_DATA
    else:
        if args.leaderboard =="global":
            leaderboard = get_leaderboard()
        else:
            leaderboard = get_leaderboard(args.benchmark_id, args.github_username)
   
    bench_summary = []
    leaderboard = sorted(leaderboard, key=lambda x: x['score'], reverse=True)
    
    prev_score = None
    rank = 0
    count = 0
    for benchmark in leaderboard:
        #print(benchmark)
        count += 1
        if benchmark["score"] != prev_score:
            rank = count
        name = benchmark["agent"]
        score = f'{int(benchmark["score"] * 100)}%'
        agent_type = benchmark["agent_type"]
        checkmarks = "✅" * benchmark["num_of_passed"] if benchmark["num_of_passed"] >= 0 else "N/A"
        notes = f'Related to {benchmark["incident_type"]} scenarios'

        sre = finops = ciso = "N/A"
        if agent_type == "SRE":
            sre = checkmarks
        elif agent_type == "FinOps":
            finops = checkmarks
        elif agent_type == "CISO":
            ciso = checkmarks
        bench_line = [
            rank,
            name,
            score,
            sre,
            finops,
            ciso,
            notes,
        ]
        prev_score = benchmark["score"]
        bench_summary.append(bench_line)


    print_table(bench_summary)