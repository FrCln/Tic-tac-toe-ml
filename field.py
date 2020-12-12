class SignError(ValueError):
    pass


class Field():
    def __init__(self, state=0, size=3):
        self.size = size
        self.state = state
        self._field = []
        for i in range(size * size):
            self._field.append(state % 3)
            state //= 3

    def __repr__(self):
        return f'Field(size={self.size}, state={self.state})'

    def __str__(self):
        signs = {0: '.', 1: '0', 2: 'X'}
        res = 'Field:\n'
        for i in range(self.size):
            for j in range(self.size):
                res += signs[self._field[i * self.size + j]]
            res += '\n'
        res += f'State: {self.state}'
        return res

    def __setitem__(self, index, item):
        assert item in (1, 2)
        if isinstance(index, int):
            n = index
        elif isinstance(index, tuple):
            assert len(index) == 2
            n = index[0] * self.size + index[1]
        else:
            raise TypeError(f'index must be int or tuple, not {index.__class__.__name__}')
        assert self._field[n] == 0, f'{self}, {n}'
        self._field[n] = item
        self.state += item * (3 ** n)

    def __getitem__(self, index):
        if isinstance(index, int):
            n = index
        elif isinstance(index, tuple):
            assert len(index) == 2
            n = index[0] * self.size + index[1]
        else:
            raise TypeError(f'index must be int or tuple, not {index.__class__.__name__}')
        return self._field[n]

    def empty_cells(self):
        return [n for n in range(self.size ** 2) if self._field[n] == 0]

    def busy_cells(self):
        return [n for n in range(self.size ** 2) if self._field[n] != 0]

    def _check_row(self, n, sign):
        assert sign in (1, 2)
        start = n * self.size
        return all(self._field[i] == sign for i in range(start, start + self.size))

    def _check_column(self, n, sign):
        assert sign in (1, 2)
        return all(self._field[i] == sign for i in range(n, self.size**2, self.size))

    def _check_diags(self, sign):
        assert sign in (1, 2)
        return all(self._field[i * (self.size + 1)] == sign for i in range(self.size)) or \
               all(self._field[(i + 1) * self.size - 1 - i] == sign for i in range(self.size))

    def check_win(self, sign):
        assert sign in (1, 2)
        for i in range(self.size):
            if self._check_column(i, sign):
                return True
            if self._check_row(i, sign):
                return True
        if self._check_diags(sign):
            return True

    def check_full(self):
        return not self.empty_cells()    


if __name__ == '__main__':
    field = Field()
    print(field)
    field[0, 2] = 2
    field[1, 1] = 2
    field[2, 0] = 2
    print(field)
    print(field.check_win(2))
