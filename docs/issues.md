# Issues
issues: bugs, enhancements for the program development

## open
open issues

| id | status | issue | description |
| - | - | - | - |

## closed
closed issues

| id | status | issue | description |
| 02 | closed | convenient entry-point `gicbank` | use `gicbank` as entry point instead of `python -m bank.ui` |
| 03 | closed | beg balance | statement doesn't show beginning balance |
| 01 | closed | thin test coverage | expanded to ten tests including negative and validation cases |
| 04 | closed | month-to-month interest accrual | interest is accrued across months with horizon limit |

## issue details

### (closed) 04 month to month iterest accrual
interest is only calculated for single month but interest on balances is not accrrued to future months.
if the statement print-out is in a future month, say `202503` and meanwhile transactions go as far back as `202306` Then to accurately reflect the balance as-of `202503`, when the statement print function is executed from the UI, interest accruals need to be calculated for all balances from `202306` until `202503` to accurately reflect the current balance.

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
| 20230701 |             | BAL  |   50.08 |    50.08 |
| 20230731 |             | I    |    0.09 |    50.17 |
```
