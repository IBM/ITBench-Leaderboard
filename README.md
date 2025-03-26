# ITBench leaderboard
 
This repository powers the community leaderboard for [ITBench](https://github.com/IBM/ITBench), an open benchmark for evaluating AI agents on real-world IT automation tasks.
 
The leaderboard showcases how different agents perform across officially defined scenarios spanning Site Reliability Engineering (SRE), Financial Operations (FinOps), and Compliance/Security (CISO) domains.
 
## 🏆 About the leaderboard
 
The leaderboard is automatically updated from submitted results and displays performance metrics for each agent, such as:
 
- Percentage of scenarios successfully completed
- Scenario-specific scores
- Runtime or efficiency metrics (if applicable)
 
Submissions are verified and merged via pull request. For details on the benchmark and environment setup, refer to the [ITBench main repo](https://github.com/IBM/ITBench).
 
## 📊 Sample leaderboard (placeholder)
 
| Rank | Agent Name            | Overall Score | SRE | FinOps | CISO | Notes                     |
|------|------------------------|---------------|-----|--------|------|---------------------------|
| 1    | Baseline SRE Agent     | 85%           | ✅✅✅✅✅✅ | N/A    | N/A  | Solved all SRE scenarios  |
| 2    | Baseline CISO Agent    | 80%           | N/A | N/A    | ✅✅✅  | High compliance coverage  |
| 3    | Your Agent Here        | TBD           | TBD | TBD    | TBD  | Submit to find out        |
 
> This is placeholder data. Actual results will be posted after public submissions open.
 
---
 
## 📤 Submitting your results
 
Ready to submit your agent? Follow these steps:
 
1. **Run the official ITBench scenarios**  
   Use [ITBench-Scenarios](https://github.com/IBM/ITBench-Scenarios) and run your agent (e.g., [SRE agent](https://github.com/IBM/itbench-sre-agent) or [CISO agent](https://github.com/IBM/itbench-ciso-caa-agent)) on each task.
 
2. **Collect your results**  
   Capture outcome data (e.g., scenario success/failure, logs, scores). You can use the utilities provided in [ITBench-Utilities](https://github.com/IBM/ITBench-Utilities) to format and summarize results.
 
3. **Fork this repository and submit a pull request**  
   Include:
   - Your agent name and affiliation (if applicable)
   - A link to your agent’s source repo
   - A structured summary of your results (in `data/` or `leaderboard.md`)
   - Any logs or metadata that aid verification
 
4. **Verification**  
   The ITBench team may re-run your agent on selected scenarios. Verified submissions will be added to the public leaderboard.
 
---
 
## 📁 Repository structure
 
```
.
├── data/               # Submitted results and metadata
├── leaderboard.md      # Markdown version of the public leaderboard
├── scripts/            # (Optional) Helper scripts for formatting or validation
└── README.md
```
 
## 📄 License
 
This project is licensed under the [Apache License 2.0](LICENSE).
 
## 🙋 Contributing
 
To improve the leaderboard infrastructure or submission process:
 
- Open an issue to propose enhancements
- Submit a pull request for code, formatting improvements, or submission guidelines
- Follow the [contribution guidelines in the main ITBench repo](https://github.com/IBM/ITBench)
 
By contributing, you agree to license your work under Apache 2.0 and follow the ITBench project’s code of conduct.
