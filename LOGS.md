# LOGS

session logs are timestamped to Singapore timezone in reverse chronological order, with latest entries at the top, and earlier entries at the bottom.

## UI program [Data Engineer] Codex prompt 2025-08-17 17:12
This UI program is very similar to the UI implemented for the UI of the reference program `crash`, with a much simpler program logic model of a very simple ledger. 

Review
- the instructions in `docs/*`
- context for this project,
- the reference program `crash` with particular emphasis on the CLI UI implementation

Task
- implement the bank interest transaction program using the UI patterns from the reference program

Guidelines
- you should not need to add any additional python dependencies, most of this can be implemented using built-in packages [os, sys, json] 
- given the limits on python dependencies, you also should not need any internet access to perform this task
- create meaningful documentation in `docs/user_guide.md` for **End User** that explains how to install, setup and use the program, common errors
- meaningful documentation in `docs/developer.md` for the **Developer** for how the program is implemented, app architecture, tech stack, modular design, common coding patterns and conventions
- organize your workflow into a TDD pattern. Per the instuctions, create robust test converage in `tests.py` and as you implement, test and validate your work `pytest tests.py`. If you run into errors, debug and resolve them before you create your final submission.
- user-friendly error and exception handling with helpful input validation clues and meaningful error messages
- helpful logging for developer to easily diagnose issues once pushed to PROD
- use OOP class architecture over functional architecture.

## Requirements [Data Engineer] 2025-08-17 16:51
- add requirements `guidelines.md` and `bank_account_interest.md`

## Setup [Data Engineer] 2025-08-17 16:36

- create github repository [gic-de-transactions](https://github.com/taylorhickem/gic-de-transactions)
- create virtual env 
    - from `requirements.txt`
    - install mkdocs dependency
- setup repository outline and files
    - mkdocs `docs/*`  `mydocs.yml`; README.md points to `docs/*`
    - logs `LOGS.md`
    - agent instruction `AGENTS.md`
    - standard git: .gitignore, VERSION, LICENSE