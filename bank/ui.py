#!/usr/bin/env python3
"""Simple banking CLI using ledger module."""
# dependencies ----------------------------------------------------------------------
from . import drive

DEFAULT_STATE = {
  "accounts": {
    "AC007": [
      {
        "date": "20230601",
        "txn_id": "20230601-01",
        "type": "D",
        "amount": 10.0
      }
    ]
  },
  "rules": [
    {
      "date": "20230601",
      "rule_id": "RULE01",
      "rate": 1.9
    },
    {
      "date": "20230610",
      "rule_id": "RULE02",
      "rate": 5.0
    },
    {
      "date": "20230801",
      "rule_id": "RULE03",
      "rate": 0.5
    }
  ]
}


# classes ----------------------------------------------------------------------------
class BankApp:
    def __init__(self, input_fn=input, output_fn=print):
        self.input_fn = input_fn
        self.output_fn = output_fn
        drive.state_refresh(state_override=DEFAULT_STATE)

    def run(self):
        drive.state_refresh(state_override=DEFAULT_STATE)
        self.output_fn("Welcome to AwesomeGIC Bank! What would you like to do?")
        while True:
            self.output_fn("[T] Input transactions\n[I] Define interest rules\n[P] Print statement\n[Q] Quit")
            choice = self.input_fn("> ").strip().lower()
            if choice == 't':
                self._input_transactions()
            elif choice == 'i':
                self._define_interest_rules()
            elif choice == 'p':
                self._print_statement()
            elif choice == 'q':
                self.output_fn("Thank you for banking with AwesomeGIC Bank.\nHave a nice day!")
                break
            else:
                self.output_fn("Invalid option. Please try again.")

    def _input_transactions(self):
        self.output_fn("Please enter transaction details in <Date> <Account> <Type> <Amount> format\n(or enter blank to go back to main menu):")
        while True:
            line = self.input_fn("> ").strip()
            if not line:
                return
            parts = line.split()
            if len(parts) != 4:
                self.output_fn("Invalid input. Expected 4 fields.")
                continue
            date, account, ttype, amount = parts
            response = drive.transaction_add(date, account, ttype, amount)
            if response['success'] == 1:
                self.output_fn(f"Transaction recorded with id {response['txn_id']}")
            else:
                self.output_fn(response['error'])

    def _define_interest_rules(self):
        self.output_fn("Please enter interest rules details in <Date> <RuleId> <Rate in %> format\n(or enter blank to go back to main menu):")
        while True:
            line = self.input_fn("> ").strip()
            if not line:
                return
            parts = line.split()
            if len(parts) != 3:
                self.output_fn("Invalid input. Expected 3 fields.")
                continue
            date, rule_id, rate = parts
            response = drive.rule_add(date, rule_id, rate)
            if response['success'] == 1:
                self.output_fn("Rule recorded")
            else:
                self.output_fn(response['error'])

    def _print_statement(self):
        self.output_fn("Please enter account and month to generate the statement <Account> <Year><Month>\n(or enter blank to go back to main menu):")
        while True:
            line = self.input_fn("> ").strip()
            if not line:
                return
            parts = line.split()
            if len(parts) != 2:
                self.output_fn("Invalid input. Expected 2 fields.")
                continue
            account, ym = parts
            response = drive.statement(account, ym)
            if response['success'] == 1:
                self.output_fn(response['statement'])
                break
            else:
                self.output_fn(response['error'])


# entry point ----------------------------------------------------------------------------
def main():
    BankApp().run()


if __name__ == '__main__':
    main()
