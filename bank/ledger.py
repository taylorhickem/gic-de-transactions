#!/usr/bin/env python3
"""Classes for the transaction data model"""
# dependencies ----------------------------------------------------------------------
import datetime as dt
from dataclasses import dataclass, field
from typing import Dict, List, Optional

# constants ------------------------------------------------------------------------------
TXN_DATE_FORMAT = '%Y%m%d'


# helper functions -----------------------------------------------------------------------
def end_of_month(year, month):
    if month == 12:
        end_date = dt.date(year + 1, 1, 1) - dt.timedelta(days=1)
    else:
        end_date = dt.date(year, month + 1, 1) - dt.timedelta(days=1)
    return end_date


# classes ------------------------------------------------------------------------------
@dataclass
class Transaction:
    date: dt.date
    txn_id: str
    type: str  # 'D', 'W'
    amount: float


@dataclass
class InterestRule:
    date: dt.date
    rule_id: str
    rate: float  # percentage


@dataclass
class Account:
    name: str
    transactions: List[Transaction] = field(default_factory=list)

    def add_transaction(self, txn: Transaction) -> None:
        self.transactions.append(txn)
        self.transactions.sort(key=lambda t: (t.date, t.txn_id))

    def balance_before(self, date: dt.date) -> float:
        bal = 0.0
        for t in sorted(self.transactions, key=lambda t: (t.date, t.txn_id)):
            if t.date >= date:
                break
            if t.type.upper() == 'D':
                bal += t.amount
            elif t.type.upper() == 'W':
                bal -= t.amount
            elif t.type.upper() == 'I':
                bal += t.amount
        return bal

    def transactions_in_month(self, year: int, month: int) -> List[Transaction]:
        return [
            t for t in sorted(self.transactions, key=lambda t: (t.date, t.txn_id))
            if t.date.year == year and t.date.month == month
        ]


class Ledger:
    def __init__(self):
        self.accounts: Dict[str, Account] = {}
        self.rules: List[InterestRule] = []

    # --- account and transaction handling ---
    def _get_account(self, name: str) -> Account:
        if name not in self.accounts:
            self.accounts[name] = Account(name)
        return self.accounts[name]

    def add_transaction(self, date_str: str, account_name: str, t_type: str, amount: float) -> Transaction:
        date = dt.datetime.strptime(date_str, TXN_DATE_FORMAT).date()
        t_type = t_type.upper()
        if t_type not in ('D', 'W'):
            raise ValueError('Type must be D or W')
        if amount <= 0:
            raise ValueError('Amount must be greater than 0')
        acc = self._get_account(account_name)
        # check balance for withdrawal
        if t_type == 'W':
            bal_before = acc.balance_before(date)
            # also include earlier transactions same day before this one
            for t in acc.transactions:
                if t.date == date:
                    if t.type.upper() == 'D':
                        bal_before += t.amount
                    elif t.type.upper() in ('W', 'I'):
                        bal_before -= t.amount
            if bal_before - amount < 0:
                raise ValueError('Balance cannot go below 0')
        # generate txn id
        count = len([t for t in acc.transactions if t.date == date]) + 1
        txn_id = f"{date_str}-{count:02d}"
        txn = Transaction(date=date, txn_id=txn_id, type=t_type, amount=round(amount, 2))
        acc.add_transaction(txn)
        return txn

    # --- interest rules ---
    def add_rule(self, date_str: str, rule_id: str, rate: float) -> InterestRule:
        if not (0 < rate < 100):
            raise ValueError('Rate must be between 0 and 100')
        date = dt.datetime.strptime(date_str, TXN_DATE_FORMAT).date()
        # remove existing rule same date
        self.rules = [r for r in self.rules if r.date != date]
        rule = InterestRule(date=date, rule_id=rule_id, rate=rate)
        self.rules.append(rule)
        self.rules.sort(key=lambda r: r.date)
        return rule

    def _rate_for_date(self, date: dt.date) -> float:
        applicable = [r for r in self.rules if r.date <= date]
        if not applicable:
            return 0.0
        return applicable[-1].rate

    @staticmethod
    def _add_txn_line(lines, date, amount, txn_id, txn_type, end_bal, type_pad: str ='    '):
        txn_line = f"| {date.strftime(TXN_DATE_FORMAT)} | {txn_id:<11} | {txn_type}{type_pad}| {amount:7.2f} | {end_bal:8.2f} |"
        lines.append(txn_line)
        return lines

    # --- statement and interest ---
    def statement(self, account_name: str, year_month: str) -> Dict[str, str]:
        year = int(year_month[:4])
        month = int(year_month[4:])
        acc = self.accounts.get(account_name)
        if not acc:
            raise ValueError('Account not found')

        transactions = acc.transactions_in_month(year, month)
        start_date = dt.date(year, month, 1)
        end_date = end_of_month(year, month)
        balance = acc.balance_before(start_date)

        lines = [f"Account: {account_name}", "| Date     | Txn Id      | Type | Amount  | Balance  |"]
        # show beginning balance
        lines = self._add_txn_line(
            lines,
            start_date,
            balance,
            '',
            'BAL',
            balance,
            type_pad='  '
        )

        # map date to transactions
        txns_by_day: Dict[dt.date, List[Transaction]] = {}
        for t in transactions:
            txns_by_day.setdefault(t.date, []).append(t)
        interest_total = 0.0
        day = start_date
        while day <= end_date:
            day_txns = txns_by_day.get(day, [])
            for t in day_txns:
                if t.type == 'D':
                    balance += t.amount
                elif t.type == 'W':
                    balance -= t.amount
                lines = self._add_txn_line(
                    lines,
                    t.date,
                    t.amount,
                    t.txn_id,
                    t.type,
                    balance
                )
            rate = self._rate_for_date(day)
            interest_total += balance * rate
            day += dt.timedelta(days=1)
        interest = round(interest_total / 100 / 365, 2)
        balance += interest
        lines = self._add_txn_line(
            lines,
            end_date,
            interest,
            '',
            'I',
            balance
        )
        statement_text = '\n'.join(lines)
        return {
            'statement': statement_text,
            'interest': interest
        }

    def to_dict(self) -> Dict:
        data = {
            'accounts': {
                name: [
                    {
                        'date': t.date.strftime(TXN_DATE_FORMAT),
                        'txn_id': t.txn_id,
                        'type': t.type,
                        'amount': t.amount,
                    }
                    for t in acc.transactions
                ]
                for name, acc in self.accounts.items()
            },
            'rules': [
                {
                    'date': r.date.strftime(TXN_DATE_FORMAT),
                    'rule_id': r.rule_id,
                    'rate': r.rate,
                }
                for r in self.rules
            ],
        }
        return data

    @classmethod
    def from_dict(cls, data: Dict) -> 'Ledger':
        ledger = cls()
        for name, txns in data.get('accounts', {}).items():
            acc = ledger._get_account(name)
            for t in txns:
                acc.add_transaction(
                    Transaction(
                        date=dt.datetime.strptime(t['date'], TXN_DATE_FORMAT).date(),
                        txn_id=t['txn_id'],
                        type=t['type'],
                        amount=t['amount'],
                    )
                )
        for r in data.get('rules', []):
            ledger.rules.append(
                InterestRule(
                    date=dt.datetime.strptime(r['date'], TXN_DATE_FORMAT).date(),
                    rule_id=r['rule_id'],
                    rate=r['rate'],
                )
            )
        ledger.rules.sort(key=lambda r: r.date)
        return ledger
