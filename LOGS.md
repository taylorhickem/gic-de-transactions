# LOGS
session logs are timestamped to Singapore timezone in reverse chronological order, with latest entries at the top, and earlier entries at the bottom.

---
## Issue: Interest accrual [Data Engineer] review 2025-08-18 11:05
resolved the interest accrual issue
 - resolved bug `ledger.Ledger._accrue_interest` modify the state variable `acc`
 - added state save to JSON file checkpoints

## Issue: Interest accrual [Data Engineer] review 2025-08-17 20:10
failed, did not implement correctly
zipping and submitting as-is

## Issues [Codex] 2025-08-17 19:53:03

__Summary__

- Implemented month-to-month interest accrual with a 209912 horizon and separated interest computation from statement rendering
- Expanded test suite to ten cases covering negative inputs and validation scenarios
- Updated documentation and closed outstanding issues

__Testing__

- `pytest tests.py`

## Issues [Data Engineer] Codex prompt 2025-08-17 19:49

__Situation__
the first version of the program works _mostly_ as expected, with the exception of some issues identified. In particular, the interest is only calculated for a single month with no interest accrual balance carry-forward to future months. 

__Review__
- documentation `docs/*`
    - with special focus on issues `issues.md`
- source code as-implemented
- test coverage `tests.py`

__Scope__
- issues `issues.md`

__Task__
- resolve the open issues
- ensure backwards compatibility, don't break any prior functionality.
- prioritize widening the test coverage (5-10 tests) with negative tests and input validation tests
    - the test should also cover the open issues: such as the interest accrual issue
- for the interest accrual issue, break-up the interest and ledger balance calculation modeling from the statement print-out. Currently it's lumped together in a single function `ledger.Ledger.statement`. 
    - Consider alternatives such as inherited class(s)
        - `InterestLedger` inherits from a base `Ledger` OR
        - `InterestAccount` that inherits from the base `Account`  OR
        - `InterestTransaction` inherited from base `Transaction` etc.. 
     or don't and just add some extra logic within the existing `Ledger` class. whichever makes sense.
    - Also add a horizon window limit (ex: 209912) to avoid ridiculous scenarios like showing statements for the month `242007`

__Guidelines__
- **DONT BREAK ANYTHING** The current version of the program  _mostly_ works! so first priority is to ensure preservation of current functionality. 
- no matter what you do, TEST TEST TEST and TEST. test at the beginning to ensure program works as expected prior to making any changes, and then prior to wrapping up your session and submitting your PR, test to validate your solution both preserves existing functionality AND resolves the issues addressed in your session.

## Review [Data Engineer] 2025-08-17 <HH>:<MM>

__issues__

| id | status | issue | description |
| - | - | - | - |
| 01 | open | thin test coverage | only 3x tests, good functional coverage, although all tests are mostly positive, only one negative tests and no input validation tests |
| 02 | closed | convenient entry-point `gicbank` | use `gicbank` as entry point instead of `python -m bank.ui` |
| 03 | closed | beg balance | statement doesn't show beginning balance |
| 04 | open | month-to-month interest accrual | interest is only calculated for single month but interest on balances is not accrrued to future months. |

__Unit tests__

 - passed 3x tests
 - 3x positive functional tests
    - deposit_and_withdraw
    - withdrawal_insufficient_balance
    - interest_calculation

__Walkthrough__

 - **(OK) Welcome prompt**: "Welcome to AwesomeGIC Bank! ..."
 - **(OK) Quit**: exits correctly
 - **(OK) Statement print - No interest**: statement print-out with no interest rules, show alternate months with no transactions, add display for beginning balance
 - **(FLAGS) Interest calculation**: tested interest rate, calculates interest on balance for isolated month, but no balance accruals from cumulated interest txns from prior months

 __updates__
01. **entry-point**: created more convenient entry-point `gicbank` using `setup.py` and extra setup step `pip install -e .`
02. **beginning balance**: add beginning balance to statement print-out

## Implementation [Codex] 2025-08-17 17:14
Implemented ledger, CLI, docs and tests.

__Summary__

- Added an object-oriented ledger that validates deposits and withdrawals and assigns unique transaction IDs, preventing negative balances for withdrawals
- Implemented monthly statement generation with end-of-day interest calculation and interest crediting on the final day of the month
- Documented installation and usage steps for end users and architectural details for developers in dedicated guides

__Testing__
✅ pytest tests.py

__Notes__
The interest calculation assumes all dates and rates are valid and does not handle leap years separately.

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