import pickle

import numpy as np

from field import Field


class AI:
    def __init__(self, init_data_file=None, size=3, learning_coef=None, **kwargs):
        self.learning_coef = learning_coef or 0.5
        data_length = 3 ** (size * size)
        if init_data_file:
            with open(init_data_file, 'br') as f:
                self.weights = pickle.load(f)
            assert isinstance(self.weights, np.ndarray)
            assert self.weights.shape == (data_length, size * size)
            np.around(self.weights, 3, out=self.weights)
            self._correct_all_sums()
        elif 'without_weights' not in kwargs:
            self.generate_weights(data_length, size)
        self.size = size
        self.path = []

    def save_data(self, filename):
        with open(filename, 'bw') as f:
            pickle.dump(self.weights, f)

    def choice(self, state):
        step = np.random.choice(np.arange(self.weights.shape[1]), p=self.weights[state])
        self.path.append((state, step))
        return step

    def generate_weights(self, data_length, size):
        self.weights = np.ones((data_length, size * size), dtype=float)
        for i in range(data_length):
            f = Field(state=i)
            self.weights[i, f.busy_cells()] = 0
        s = self.weights.sum(axis=1)
        s[s == 0] = 1
        self.weights /= np.tile(s[:, np.newaxis], size * size)
        np.around(self.weights, 3, out=self.weights)
        self._correct_all_sums()

    def _correct_all_sums(self):
        s = self.weights.sum(axis=1)
        n = self.weights.shape[0]
        for i in np.arange(n)[(s != 1.0) & (s != 0)]:
            self._correct_sum(i)

    def _correct_sum(self, state):
        n = self.weights.shape[1]
        cor = self.weights[state].argmax()
        self.weights[state, cor] += 1 - self.weights[state].sum()

    def correct(self, result):
        delta = result * self.learning_coef + (1 + 0.1 * self.learning_coef)
        for state, step in reversed(self.path):
            if result == -1 and self.weights[state, step] == 1:
                # Произошло переобучение
                self.weights[state] = np.ones(self.weights.shape[1])
                self.weights[state, Field(state).busy_cells()] = 0
            self.weights[state, step] *= delta
            self.weights[state] = np.around(self.weights[state] / self.weights[state].sum(), 3)
            if self.weights[state, step] < 0:
                self.weights[state, step] = 0
            self._correct_sum(state)
            delta **= 0.7
        self.path = []

    def normalize(self):
        self.weights[self.weights < 0.01] = 0
        self._correct_all_sums()

    def copy(self):
        res = self.__class__(
            size = self.size,
            learning_coef=self.learning_coef,
            without_weights=True
        )
        res.weights = self.weights.copy()
        return res


class FakeAI:
    def __init__(self, init_data_file=None, size=3, learning_coef=None, **kwargs):
        self.size = size

    def save_data(self, filename):
        pass

    def choice(self, state):
        step = np.random.choice(Field(state=state, size=self.size).empty_cells())
        return step

    def generate_weights(self, data_length, size):
        pass

    def correct(self, result):
        pass

    def normalize(self):
        pass


class AI2(AI):
    def __init__(self, init_data_file=None, size=3, learning_coef=None, **kwargs):
        learning_coef = learning_coef or 0.02
        super().__init__(init_data_file, size, learning_coef, **kwargs)

    def choice(self, state):
        if np.all(self.weights[state] == 0):
            # Заведомо проигрышное состояние.
            # Выбираем что угодно, в историю ходов не добавляем.
            step = np.random.choice(Field(state=state, size=self.size).empty_cells())
        else:
            step = np.random.choice(np.arange(self.weights.shape[1]), p=self.weights[state])
            self.path.append((state, step))
        return step

    def correct(self, result):
        delta = result * self.learning_coef + (1 + 0.1 * self.learning_coef)
        state, step = self.path.pop()
        if result == 1:
            # Победа, фикисруем последний ход как единственно правильный
            self.weights[state, :] = 0
            self.weights[state, step] = 1
        elif result == -1:
            # Поражение, фиксируем последний ход как однозначно неправильный
            self.weights[state, step] = 0
            if not np.all(self.weights[state] == 0):
                self._correct_sum(state)
        for state, step in reversed(self.path):
            # Для всех остальных ходов из истории слегка меняем веса
            if result == -1 and self.weights[state, step] == 1:
                # Произошло переобучение
                self.weights[state] = np.ones(self.weights.shape[1])
                self.weights[state, Field(state).busy_cells()] = 0
            elif self.weights[state, step] == 1:
                continue
            self.weights[state, step] *= delta
            self.weights[state] = np.around(self.weights[state] / self.weights[state].sum(), 3)
            if self.weights[state, step] < 0:
                self.weights[state, step] = 0
            self._correct_sum(state)
            delta **= 0.7
        self.path = []


def generate_data():
    ai = AI()
    ai.save_data('init_weights.bin')


if __name__ == '__main__':
    generate_data()
    ai = AI(init_data_file='init_weights.bin')
