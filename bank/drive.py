#!/usr/bin/env python3
"""Main handler for program actions"""
# dependencies ----------------------------------------------------------------------
from . import state


# module variables  -----------------------------------------------------------------
ledger = None


# actions  -------------------------------------------------------------------------
def state_refresh(state_override={}):
    global ledger
    ledger = state.load(state_override=state_override)
    state.save(ledger)    


def transaction_add(date: str, account: str, t_type: str, amount: float):
    try:
        txn = ledger.add_transaction(date, account, t_type, float(amount))
    except Exception as e:
        return {'success': -1, 'error': str(e)}
    else:
        state.save(ledger)
        return {'success': 1, 'txn_id': txn.txn_id}


def rule_add(date: str, rule_id: str, rate: float):
    try:
        ledger.add_rule(date, rule_id, float(rate))
    except Exception as e:
        return {'success': -1, 'error': str(e)}
    else:
        state.save(ledger)
        return {'success': 1}


def statement(account: str, year_month: str):
    try:
        result = ledger.statement(account, year_month)
    except Exception as e:
        return {'success': -1, 'error': str(e)}
    else:
        state.save(ledger)
        return {'success': 1, **result}


# main  -------------------------------------------------------------------------------
ledger = state.load()
