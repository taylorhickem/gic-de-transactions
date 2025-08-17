"""Crash module to represent the memory state of the simulation. interfaces with a json file dictionary in runtime
"""
# dependencies ---------------------------------------------------------------
import json


# constants ------------------------------------------------------------------
STATE_FILE = 'state.json'


# module variables -----------------------------------------------------------
sim_state = {}


# methods ---------------------------------------------------------------------
def refresh():
    global sim_state
    sim_state = {}
    save()


def load():
    global sim_state
    success = 0
    error = ''
    try:
        with open(STATE_FILE, 'r') as f:
            sim_state = json.load(f)
            f.close()
        success = 1
    except Exception as e:
        error = f'ERROR. problem reading grid state file {STATE_FILE}. {str(e)}'
    response = {
        'success': success,
        'error': error
    }
    return response


def save():
    global sim_state
    success = 0
    error = ''
    try:
        with open(STATE_FILE, 'w') as f:
            json.dump(sim_state, f)
            f.close()
        success = 1
    except Exception as e:
        error = f'ERROR. problem writing grid state to file {STATE_FILE}. {str(e)}'
    response = {
        'success': success,
        'error': error
    }
    return response
