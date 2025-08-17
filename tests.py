#!/usr/bin/env python3
"""Unit tests"""
# dependencies ---------------------------------------------------------------------------------------
import unittest
from bank import drive, state


# unit tests ---------------------------------------------------------------------------------------
class BankTests(unittest.TestCase):
    def setUp(self):
        # ensure fresh state
        if state.STATE_FILE.exists():
            state.STATE_FILE.unlink()
        drive.state_refresh()

    def test_01_deposit_and_withdraw(self):
        r1 = drive.transaction_add('20230601', 'AC001', 'D', 100)
        self.assertEqual(1, r1['success'])
        r2 = drive.transaction_add('20230602', 'AC001', 'W', 50)
        self.assertEqual(1, r2['success'])
        stmt = drive.statement('AC001', '202306')
        self.assertEqual(1, stmt['success'])
        self.assertIn('20230601-01', stmt['statement'])
        self.assertIn('20230602-01', stmt['statement'])

    def test_02_withdrawal_insufficient_balance(self):
        drive.transaction_add('20230601', 'AC002', 'D', 50)
        resp = drive.transaction_add('20230602', 'AC002', 'W', 60)
        self.assertEqual(-1, resp['success'])

    def test_03_interest_calculation(self):
        # setup transactions
        drive.transaction_add('20230505', 'AC001', 'D', 100)
        drive.transaction_add('20230601', 'AC001', 'D', 150)
        drive.transaction_add('20230626', 'AC001', 'W', 20)
        drive.transaction_add('20230626', 'AC001', 'W', 100)
        # rules
        drive.rule_add('20230101', 'RULE01', 1.95)
        drive.rule_add('20230520', 'RULE02', 1.90)
        drive.rule_add('20230615', 'RULE03', 2.20)
        stmt = drive.statement('AC001', '202306')
        self.assertEqual(1, stmt['success'])
        self.assertAlmostEqual(0.39, stmt['interest'], places=2)
        self.assertIn('| 20230630 |             | I    |', stmt['statement'])

    def test_04_interest_accrual_across_months(self):
        drive.transaction_add('20230601', 'AC003', 'D', 50)
        drive.rule_add('20230101', 'R1', 2.0)
        stmt = drive.statement('AC003', '202307')
        self.assertEqual(1, stmt['success'])
        self.assertIn('| 20230701 |             | BAL  |   50.08 |    50.08 |', stmt['statement'])
        self.assertIn('| 20230731 |             | I    |    0.09 |    50.17 |', stmt['statement'])

    def test_05_invalid_transaction_type(self):
        resp = drive.transaction_add('20230601', 'AC004', 'X', 10)
        self.assertEqual(-1, resp['success'])

    def test_06_invalid_amount(self):
        resp = drive.transaction_add('20230601', 'AC005', 'D', 0)
        self.assertEqual(-1, resp['success'])
        resp2 = drive.transaction_add('20230601', 'AC005', 'D', -5)
        self.assertEqual(-1, resp2['success'])

    def test_07_rule_rate_invalid(self):
        resp = drive.rule_add('20230101', 'R2', 0)
        self.assertEqual(-1, resp['success'])
        resp2 = drive.rule_add('20230101', 'R3', 100)
        self.assertEqual(-1, resp2['success'])

    def test_08_statement_invalid_account(self):
        resp = drive.statement('NOACC', '202306')
        self.assertEqual(-1, resp['success'])

    def test_09_statement_invalid_year_month_format(self):
        drive.transaction_add('20230601', 'AC006', 'D', 10)
        resp = drive.statement('AC006', '2023')
        self.assertEqual(-1, resp['success'])

    def test_10_statement_horizon_limit(self):
        drive.transaction_add('20230601', 'AC007', 'D', 10)
        resp = drive.statement('AC007', '242007')
        self.assertEqual(-1, resp['success'])


if __name__ == '__main__':
    unittest.main()
