import numpy as np
import automata as auto


def gen_graph(automata):
    if isinstance(automata["transition function"][0][0], set):  # NFA
        states = automata["states"]
        alphabet = automata["alphabet"] + [r"$\varepsilon$"]

        graph = np.zeros([automata["states"].__len__()] * 2 + [alphabet.__len__()])
        for r in range(automata["states"].__len__()):
            for c in range(alphabet.__len__()):
                for state in automata["transition function"][r][c]:
                    graph[r, states.index(state), c] = 1
    else:  # DFA
        states = automata["states"]
        alphabet = automata["alphabet"]

        graph = np.zeros([automata["states"].__len__()] * 2 + [alphabet.__len__()])
        for r in range(automata["states"].__len__()):
            for c in range(alphabet.__len__()):
                graph[r, states.index(automata["transition function"][r][c]), c] = 1

    start_state = automata["states"].index(automata["start state"])
    accept_state = np.array([automata["states"].index(state) for state in automata["accept states"]])

    return graph, start_state, accept_state


# DFA Minimization using Myphill-Nerode Theorem
def enumerate_nfa(num_states=2, num_alphabet=2):
    nfa_collection, dfa_collection = [], []
    for i in range((num_alphabet ** num_states) ** ((num_alphabet + 1) * num_states)):
        transition_function = [[] for _ in range(num_states)]
        codes = np.base_repr(i, num_states)
        codes = "0" * (num_states ** 2 * (num_alphabet + 1) - codes.__len__()) + codes
        for r in range(num_states):
            for c in range(num_alphabet + 1):
                k = r * (num_alphabet + 1) + c
                code = codes[k * num_states:(k + 1) * num_states]
                if code == "00":  # TODO: rewrite this condition
                    item = set()
                elif code == "10":
                    item = {"q0"}
                elif code == "01":
                    item = {"q1"}
                else:
                    item = {"q0", "q1"}
                transition_function[r].append(item)

        for accept_states in [{"q0"}, {"q1"}, {"q0", "q1"}]:  # TODO: rewrite this list
            nfa = {
                "states": ["q{}".format(i) for i in range(num_states)],
                "alphabet": [str(i) for i in range(num_alphabet)],
                "start state": "q0",
                "accept states": accept_states,
                "transition function": transition_function
            }
            dfa = auto.nfa2dfa(nfa, simplify=True)

            if dfa["accept states"].__len__() != 0:
                nfa_collection.append(nfa)
                dfa_collection.append(dfa)
    return nfa_collection, dfa_collection


def enumerate_string(num_alphabet=2, string_length=3):
    string_set = []
    for i in range(num_alphabet ** string_length):
        string = np.base_repr(i, num_alphabet)
        string_set.append([0] * (string_length - string.__len__()) + [int(s) for s in string])
    return np.array(string_set)


def generate_dataset(num_states=2, num_alphabet=2, string_length=3):
    nfa_collection, dfa_collection = enumerate_nfa(num_states, num_alphabet)
    string_set = enumerate_string(num_alphabet, string_length)

    features, targets = [], []
    for nfa, dfa in zip(nfa_collection, dfa_collection):
        feature = []
        for string in string_set:
            state = dfa["start state"]  # TODO: the DFA start from the first state
            for letter in string:
                state = dfa["transition function"][dfa["states"].index(state)][dfa["alphabet"].index(str(letter))]
            feature.append(state in dfa["accept states"])
        features.append(feature)
        targets.append(nfa)
    features = np.array(features)

    features, indices = np.unique(features, axis=0, return_index=True)
    targets = [targets[index] for index in indices]

    return features, targets, string_set


if __name__ == "__main__":
    _features, _targets, _string_set = generate_dataset(num_states=2, num_alphabet=2, string_length=3)
    print(_features.shape, _string_set.shape)
    print(_string_set)

    concat = []
    for i in range(5):
        nfa = _targets[i]
        concat.append(_features[i])
        auto.print_automata(nfa)
    concat = np.concatenate([_string_set, np.array(concat).T], axis=1)
    print(concat)
