""" mode control between test and interactive user interface
"""
# dependencies ---------------------------------------------------------------
import sys
from .ui import InteractiveApp
import subprocess


# constants ------------------------------------------------------------------
VALID_MODES = ['test', 'ui']
MESSAGES = {
    'test': f"Running tests to verify that the program is installed correctly and works as expected ...",
}


# main -----------------------------------------------------------------------
def ui_mode():
    args = sys.argv[1:]
    mode = args[0] if args else 'ui'
    if mode in VALID_MODES:
        prompt_msg = MESSAGES.get(mode, {})
        if prompt_msg:
            print(prompt_msg)
        if mode == 'test':
            subprocess.run(["pytest", "test.py"])
        elif mode == 'ui':
            app_start()
    else:
        print(f'ERROR. Unknown command: {mode}')


def app_start():
    app = InteractiveApp()
    app.boot()


def main():
    ui_mode()
