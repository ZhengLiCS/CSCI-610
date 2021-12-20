from datetime import datetime

import numpy as np
from sklearn import tree
from sklearn.ensemble import RandomForestRegressor
import tensorflow as tf


# DFA that can recognize regular language
def generator(num_states, num_alphabet, string_length):
    string_set = []
    for i in range(num_alphabet ** string_length):
        string = np.base_repr(i, num_alphabet)
        string_set.append([0] * (string_length - string.__len__()) + [int(s) for s in string])
    string_set = np.array(string_set)
    print(string_set)

    try:
        with open("src/DFA.npy", 'rb') as file:
            features = np.load(file)
            targets = np.load(file)
        return features, targets, string_set
    except FileNotFoundError:
        features, targets = [], []
        for i in range(num_states ** (num_states * num_alphabet)):
            delta = np.base_repr(i, num_states)
            delta = [0] * (num_states * num_alphabet - delta.__len__()) + [int(d) for d in delta]
            transition_function = np.reshape(delta, [num_states, num_alphabet])

            feature = []
            for string in string_set:
                state = 0
                for item in string:
                    state = transition_function[state, item]
                feature.append(state == num_states - 1)
            features.append(np.array(feature))

            targets.append(transition_function.flatten())

        features = np.array(features)
        targets = np.array(targets)

        random_indices = np.arange(features.__len__())
        np.random.shuffle(random_indices)

        with open("src/DFA.npy", "wb") as file:
            np.save(file, features[random_indices, :])
            np.save(file, targets[random_indices, :])
        return features[random_indices, :], targets[random_indices, :], string_set


if __name__ == "__main__":
    x_train, y_train, strings = generator(num_states=3, num_alphabet=2, string_length=4)
    print(x_train.shape, y_train.shape)

    print(x_train[0, :])

    for string, result in zip(strings, x_train[0, :]):
        print(string, result)

    # model = tree.DecisionTreeClassifier(max_depth=16, max_leaf_nodes=300)
    # model.fit(x_train, y_train[:, 0])
    # r2_score = model.score(x_train, y_train[:, 0])
    # print(r2_score)

    # model = RandomForestRegressor()
    # model.fit(x_train, y_train[:, 0])
    # r2_score = model.score(x_train, y_train[:, 0])
    # print(r2_score)

    model = tf.keras.models.Sequential([
        tf.keras.layers.Dense(512, activation='relu'),
        tf.keras.layers.BatchNormalization(),
        tf.keras.layers.Dense(256, activation='relu'),
        tf.keras.layers.BatchNormalization(),
        tf.keras.layers.Dense(128, activation='relu'),
        tf.keras.layers.BatchNormalization(),
        tf.keras.layers.Dense(y_train.shape[-1])
    ])
    model.compile(
        optimizer=tf.keras.optimizers.Adam(0.01),
        loss=tf.keras.losses.MeanSquaredError(),
        metrics=['accuracy'])
    model.fit(
        x_train, y_train, batch_size=32, epochs=120,
        # validation_data=(x_test, y_test),
        callbacks=[
            tf.keras.callbacks.LearningRateScheduler(lambda epoch, lr: 0.01 * 0.75 ** (epoch // 10), verbose=1),
            tf.keras.callbacks.TensorBoard(log_dir="logs/" + datetime.now().strftime("%Y%m%d-%H%M%S"),
                                           histogram_freq=1)
        ],
    )

