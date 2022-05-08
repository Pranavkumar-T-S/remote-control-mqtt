import json


def __update_state__():
    global state
    with open("state.json") as file:
        state = json.loads(file.read())
        print(state)


def save_state(state):
    state_json = json.dumps(state)
    with open("state.json", 'w') as file:
        file.write(state_json)
    __update_state__()


def retrieve_state():
    __update_state__()
    global state
    return state


def gpio_pins():
    with open("pins.json") as file:
        pins = json.loads(file.read())
        return pins


state = {}
__update_state__()
