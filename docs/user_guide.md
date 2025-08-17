# User Guide

## Installation

This project requires Python 3.8+ and has no external dependencies.

1. Clone the repository and change into the project directory.
2. (Optional) Create a virtual environment.
3. install the program

add the flag `-e` for interactive development mode

```bash
pip install .
```

4. Run the interactive program:

```bash
gicbank
```

## Usage

When launched the program displays a menu:

```
Welcome to AwesomeGIC Bank! What would you like to do?
[T] Input transactions
[I] Define interest rules
[P] Print statement
[Q] Quit
>
```

### T: Input transactions
Enter a line with `Date Account Type Amount`.
Example:
```
20230626 AC001 W 100.00
```
Type `Enter` on an empty line to return to the main menu.

### I: Define interest rules
Enter `Date RuleId Rate`.
Example:
```
20230615 RULE03 2.20
```
The latest rule on a given date replaces earlier rules.
Default account setup is no interest rules is cash account with no interest payments.

### P: Print statement
Enter `Account YearMonth` to generate a monthly statement including interest.
Statements can only be generated up to December 2099 (`209912`).
Example:
```
AC001 202306
```
Example statement:
```
| Date     | Txn Id      | Type | Amount | Balance |
| 20230601 |             | BAL    |    0.00 |     0.00 |
| 20230601 | 20230601-01 | D    |   50.00 |    50.00 |
| 20230630 |             | I    |    0.00 |    50.00 |
```

Interest is automatically accrued at the end of each month and carried forward to future statements.

### Q: Quit
Enter `Q` from the main menu.

## Common errors

- **Invalid date format** – Dates must be in `YYYYMMDD` or `YYYYMM` format.
- **Insufficient balance** – Withdrawals cannot result in a negative balance.
- **Invalid interest rate** – Rates must be between 0 and 100.
