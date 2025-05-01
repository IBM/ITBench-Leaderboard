# ITBench-Leaderboard

> 🔗 Looking for the public leaderboard? [Click here to view it](https://github.com/IBM/ITBench-Leaderboard/LEADERBOARD.md)

Measure the performance of your AI agent(s) across a wide variety of complex and real-life IT automation tasks targetting three key use cases:
- Site Reliability Engineering (SRE) - focusing on availability and resiliency
- Financial Operations (FinOps) - focusing on enforcing cost efficiencies and optimizing return on investment
- Compliance and Security Operations (CISO) - focusing on ensuring compliance and security of IT implementations

This is a public leaderboard. ITBench handles the deployment of the environments, scenarios and evaluates the submissions made by the agent.

## Key Terminologies
- **Scenario**: ITBench incorporates a collection of problems that we call scenarios. For example, one of the SRE scenarios in ITBench is to resolve a “High error rate on service checkout” in a Kubernetes environment. Another scenario that is relevant for the CISO use case involves assessing the compliance posture for a “new control rule detected for RHEL 9.”
- **Environment**: Each of the ITBench scenarios are deployed in an operational sandboxed Kubernetes environment.
- **Benchmark**: Collection of scenarios that are excuted parallel or in sequence but independent of each other. An agent makes a submission to address or diagnose or remediate the scenario at hand.

## Getting Started
### Prerequisites
- **A private GitHub repository**
  - A file facilitating the agent and leaderboard handshake is committed to this private repository.
  - File(s) may be created or deleted automatically during the benchmark lifecycle.
- **A Kubernetes sandbox cluster (KinD recommended)** -- Only needed for CISO 
  - Do not use a production cluster as the benchmark process will create and delete resources dynamically.
  - Please refer to [prepare-kubeconfig-kind.md](https://github.com/IBM/ITBench-Scenarios/blob/main/ciso/prepare-kubeconfig-kind.md)
- **An agent to benchmark**
  - A base agent is available from IBM for immediate use. The base agent for the CISO use-case can be found [here](https://github.com/IBM/itbench-ciso-caa-agent) and one for SRE and FinOps use cases can be found [here]. This allows you to leverage your methodologies / improvements without having to worry about the agent and leaderboard setvice interactions

### Setup
1. Install the ITBench GitHub App to the private GitHub repository
    - Click [here](https://github.com/apps/ibm-itbench-github-app) and install the ITBench GitHub app to the private repository
    
        👉 [Detailed instructions](docs/instruction-for-agent-submitter-ciso.md#step-0-install-the-itbench-github-app)

2. Register your agent
    - Create a registration issue with your agent info
    
        👉 [Detailed instructions](docs/instruction-for-agent-submitter-ciso.md#step-1-register-your-agent)

3. Create a benchmark request 
    - Submit a benchmark issue linked to your agent config repo

        👉 [Detailed instructions](docs/instruction-for-agent-submitter-ciso.md#step-2-register-your-benchmark)

### Running your agent or our base agent against the benchmark
- A guide to evaluate our CISO base agent against the ITBench Leaderboard can be found [here](docs/instruction-for-agent-submitter-ciso.md#step-3-launch-benchmark).
- A guide to evaluate our SRE base agent against the ITBench Leaderboard can be found [here](https://github.com/IBM/ITBench-SRE-Agent/blob/leaderboard_updates/Leaderboard.md).

## ITBench Ecosystem and Related Repositories

- [ITBench](https://github.com/IBM/ITBench): Central repository providing an overview of the ITBench ecosystem, related announcements, and publications.
- [CAA-CISO Agent](https://github.com/IBM/ITBench-CAA-CISO-Agent): CISO (Chief Information Security Officer) agents that automate compliance assessments by generating policies from natural language, collecting evidence, integrating with GitOps workflows, and deploying policies for assessment.
- [SRE Agent](https://github.com/IBM/ITBench-SRE-Agent): SRE (Site Reliability Engineering) agents designed to diagnose and remediate problems in Kubernetes-based environments. Leverage logs, metrics, traces, and Kubernetes states/events from the IT enviroment.
- [ITBench Scenarios](https://github.com/IBM/ITBench-Scenarios): Environment setup and mechanism to trigger scenarios Service that handles scenario deployment, agent evaluation, and maintains a public leaderboard for comparing agent performance on ITOps use cases.
- [ITBench Utilities](https://github.com/IBM/ITBench-Utilities): Collection of supporting tools and utilities for participants in the ITBench ecosystem and leaderboard challenges.
- [ITBench Tutorials](https://github.com/IBM/ITBench-Tutorials): Repository containing the latest tutorials, workshops, and educational content for getting started with ITBench.

## Maintainers
- Takumi Yanagawa  - [@yana1205](https://github.com/yana1205)
- Yuji Watanabe    - [@yuji-watanabe-jp](https://github.com/yuji-watanabe-jp)
