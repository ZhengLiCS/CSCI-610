import numpy as np


def print_automata(automata):
    states = automata["states"]
    alphabet = automata["alphabet"] + [r"$\varepsilon$"] * (automata["alphabet"].__len__() != automata["transition function"][0].__len__())
    transition_function = automata["transition function"]

    column_lengths = []
    for c in range(alphabet.__len__()):
        set_list = [str(transition_function[r][c]) for r in range(states.__len__())]
        set_list = [r"$\varnothing$" if item == "set()" else item for item in set_list]
        column_lengths.append(max([item.__len__() for item in set_list]))

    # columns
    index_length = 0
    for r in range(states.__len__()):
        item = str(states[r]).replace("'", "")
        item = r"$\varnothing$" if item == "set()" else item
        index_length = max(index_length, str(item).__len__())
    message = " " * index_length + " | "
    for c in range(alphabet.__len__()):
        message += ("{:<" + str(column_lengths[c]) + "}").format(alphabet[c]) + "\t"
    message += "\n"

    # hline
    message += "-" * index_length + " + "
    for c in range(alphabet.__len__()):
        message += "-" * column_lengths[c] + "\t"
    message += "\n"

    # body
    for r in range(states.__len__()):
        item = str(states[r]).replace("'", "")
        item = r"$\varnothing$" if item == "set()" else item
        message += ("{:<" + str(index_length) + "}").format(item) + " | "
        for c in range(alphabet.__len__()):
            item = str(transition_function[r][c]).replace("'", "")
            item = r"$\varnothing$" if item == "set()" else item
            message += ("{:<" + str(column_lengths[c]) + "}").format(item) + "\t"
        message += "\n"

    # print

    print("states: " + str(automata["states"]).replace("'", ""))
    print("alphabet: " + str(automata["alphabet"]).replace("'", ""))
    print("start state: " + str(automata["start state"]).replace("'", ""))
    print("accept states: " + str(automata["accept states"]).replace("'", ""))
    print("transition function: ")
    print(message)


def gen_closure(automata, state):
    _closure = set()
    closure = {state} | automata["transition function"][automata["states"].index(state)][-1]
    while closure != _closure:
        _closure = closure.copy()
        for state in _closure:
            closure |= automata["transition function"][automata["states"].index(state)][-1]
    return closure


def nfa2dfa(nfa, simplify=False):
    start_closure = gen_closure(nfa, nfa["start state"])

    dfa = {
        "states": [start_closure],
        "alphabet": nfa["alphabet"],
        "start state": start_closure,
        "accept states": [],
        "transition function": [],
    }
    for states in dfa["states"]:
        row = []
        for letter in dfa["alphabet"]:
            item = set()
            for state in states:
                item |= nfa["transition function"][nfa["states"].index(state)][nfa["alphabet"].index(letter)]

            closure = set()
            for state in item:
                closure |= gen_closure(nfa, state)

            if closure not in dfa["states"]:
                dfa["states"].append(closure)
            for state in nfa["accept states"]:
                if state in closure and closure not in dfa["accept states"]:
                    dfa["accept states"].append(closure)
                    break
            row.append(closure)
        dfa["transition function"].append(row)

    if simplify:
        dfa["start state"] = "Q{}".format(dfa["states"].index(dfa["start state"]))
        dfa["accept states"] = ["Q{}".format(dfa["states"].index(state)) for state in dfa["accept states"]]
        for r in range(dfa["states"].__len__()):
            for c in range(dfa["alphabet"].__len__()):
                dfa["transition function"][r][c] = "Q{}".format(dfa["states"].index(dfa["transition function"][r][c]))
        dfa["states"] = ["Q{}".format(i) for i in range(dfa["states"].__len__())]

    return dfa


if __name__ == "__main__":
    # ================ demo 1 ================
    nfa_obj = {
        "states": ["q0", "q1", "q2"],
        "alphabet": ["a", "b"],
        "start state": "q0",
        "accept states": {"q2"},
        "transition function": [
            [set(), {"q0"}, {"q1"}],
            [{"q1"}, set(), {"q2"}],
            [{"q1"}, {"q0"}, set()],
        ],
    }
    print_automata(nfa_obj)

    dfa_obj = nfa2dfa(nfa_obj)
    print_automata(dfa_obj)

    dfa_obj = nfa2dfa(nfa_obj, simplify=True)
    print_automata(dfa_obj)

    # ================ demo 2 ================
    nfa_obj = {
        "states": ["q1", "q2", "q3"],
        "alphabet": ["a", "b"],
        "start state": "q1",
        "accept states": ["q2"],
        "transition function": [
            [{"q3"}, set(), {"q2"}],
            [{"q1"}, set(), set()],
            [{"q2"}, {"q2", "q3"}, set()],
        ],
    }
    print_automata(nfa_obj)

    dfa_obj = nfa2dfa(nfa_obj)
    print_automata(dfa_obj)

    dfa_obj = nfa2dfa(nfa_obj, simplify=True)
    print_automata(dfa_obj)

