# User Guide

## Installation

This project requires Python 3.8+ and has no external dependencies.

1. Clone the repository and change into the project directory.
2. (Optional) Create a virtual environment.
3. Run the interactive program:

```bash
python -m bank.ui
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

### Input transactions
Enter a line with `Date Account Type Amount`.
Example:
```
20230626 AC001 W 100.00
```
Type `Enter` on an empty line to return to the main menu.

### Define interest rules
Enter `Date RuleId Rate`.
Example:
```
20230615 RULE03 2.20
```
The latest rule on a given date replaces earlier rules.

### Print statement
Enter `Account YearMonth` to generate a monthly statement including interest.
Example:
```
AC001 202306
```

### Quit
Enter `Q` from the main menu.

## Common errors

- **Invalid date format** – Dates must be in `YYYYMMDD` or `YYYYMM` format.
- **Insufficient balance** – Withdrawals cannot result in a negative balance.
- **Invalid interest rate** – Rates must be between 0 and 100.
