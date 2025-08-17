# Developer Guide

## Architecture

The application is a small command line program implemented using an object-oriented design.

- `bank/ledger.py` – domain models and the `Ledger` class that manages accounts, transactions and interest rules. Interest accrual is computed via `Ledger.accrue_interest` and statements are rendered separately.
- `bank/state.py` – persistence helper that saves and loads ledger data from `state.json`.
- `bank/drive.py` – thin wrapper exposing functions used by the UI. All functions return dictionaries with a `success` flag and optional data or error message.
- `bank/ui.py` – interactive command line interface.

## Data model

- **Account** holds a list of `Transaction` objects.
- **Transaction** records `date`, `txn_id`, `type` (`D`, `W`, `I`) and `amount`.
- **InterestRule** defines the interest rate that applies from a given date forward.

State is persisted as JSON in `state.json` at the project root. `Ledger.to_dict()` and `Ledger.from_dict()` serialize and restore the state.

## Coding conventions

- Only the Python standard library is used.
- Functions in `drive.py` return dictionaries of the form `{'success': 1, ...}` or `{'success': -1, 'error': 'message'}`.
- Tests in `tests.py` use `unittest`.

## Running tests

```bash
pytest tests.py
```

Statements are limited to dates up to `209912` by design to avoid unrealistic future periods.

## Logging

The project is small and relies on return values for error reporting. Additional logging can be added by instrumenting the `drive` and `ledger` modules.
