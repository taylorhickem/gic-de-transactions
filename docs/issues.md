# Issues
issues: bugs, enhancements for the program development

## open
open issues

| id | status | issue | description |
| - | - | - | - |
| 01 | open | thin test coverage | only 3x tests, good functional coverage, although all tests are mostly positive, only one negative tests and no input validation tests |
| 04 | open | month-to-month interest accrual | interest is only calculated for single month but interest on balances is not accrrued to future months. |

## closed
closed issues

| id | status | issue | description |
| 02 | closed | convenient entry-point `gicbank` | use `gicbank` as entry point instead of `python -m bank.ui` |
| 03 | closed | beg balance | statement doesn't show beginning balance |

## issue details

### (open) 04 month to month iterest accrual
interest is only calculated for single month but interest on balances is not accrrued to future months.

part of the issue is the conflation of the statement printing with interest accrual in the function `ledger.Ledger.statement`. 
suggestion to separately model the statement ledger balance modeling from the statement printing.

OK statement for month `202306` with interest credited at end of month

```
| Date     | Txn Id      | Type | Amount  | Balance  |
| 20230601 |             | BAL  |    0.00 |     0.00 |
| 20230601 | 20230601-01 | D    |   50.00 |    50.00 |
| 20230630 |             | I    |    0.08 |    50.08 |
```

X wrong, beginning balance should be `50.08`, actual `50.00`
- carry forward ending balance from `202306` with interest accrual

statement for month `202307`

```
| Date     | Txn Id      | Type | Amount  | Balance  |
| 20230701 |             | BAL  |   50.00 |    50.00 |
| 20230731 |             | I    |    0.02 |    50.02 |
```
