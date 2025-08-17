import json
from pathlib import Path
from .ledger import Ledger

STATE_FILE = Path(__file__).resolve().parent.parent / 'state.json'


def load() -> Ledger:
    if STATE_FILE.exists():
        data = json.loads(STATE_FILE.read_text())
        return Ledger.from_dict(data)
    return Ledger()


def save(ledger: Ledger) -> None:
    STATE_FILE.write_text(json.dumps(ledger.to_dict(), indent=2))
