import os
import unittest
from bank import drive, state


class BankTests(unittest.TestCase):
    def setUp(self):
        # ensure fresh state
        if state.STATE_FILE.exists():
            state.STATE_FILE.unlink()
        drive.state_refresh()

    def test_deposit_and_withdraw(self):
        r1 = drive.transaction_add('20230601', 'AC001', 'D', 100)
        self.assertEqual(1, r1['success'])
        r2 = drive.transaction_add('20230602', 'AC001', 'W', 50)
        self.assertEqual(1, r2['success'])
        stmt = drive.statement('AC001', '202306')
        self.assertEqual(1, stmt['success'])
        self.assertIn('20230601-01', stmt['statement'])
        self.assertIn('20230602-01', stmt['statement'])

    def test_withdrawal_insufficient_balance(self):
        drive.transaction_add('20230601', 'AC002', 'D', 50)
        resp = drive.transaction_add('20230602', 'AC002', 'W', 60)
        self.assertEqual(-1, resp['success'])

    def test_interest_calculation(self):
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


if __name__ == '__main__':
    unittest.main()
