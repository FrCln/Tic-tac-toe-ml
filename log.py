import argparse
import os
import sys

from ai import AI
from field import Field


def get_args():
    signs = {'x': 2, 'X': 2, 'O': 1, 'o': 1, '0': 1, None: None}
    parser = argparse.ArgumentParser()
    parser.add_argument('name')
    parser.add_argument('-s', '--sign')
    args = parser.parse_args()
    if args.sign and args.sign not in 'xoXO':
        print('Sign must be x or o.')
    return args.name, signs[args.sign]


def game(ai_x, ai_o, log_sign=None):
    f = Field()
    history = []
    players = [ai_o, ai_x]
    x = 1
    for _ in range(9):
        sign = x + 1
        step = int(players[x].choice(f.state))
        f[step] = sign
        if f.check_win(sign):
            if log_sign is None or sign == log_sign:
                for st in history:
                    print(Field(st))
                print(f'\033[1;31m{f}\033[0m')
                print()
            players[x].correct(1)
            players[not x].correct(-1)
            return sign
        history.append(f.state)
        x = not x
    for ai in players:
        ai.correct(0)
    return 0


def main():
    name, log_sign = get_args()
    name = os.path.join('data', name)
    ai_x = AI(init_data_file=name + '-ai_x.bin')
    ai_o = AI(init_data_file=name + '-ai_o.bin')
    print()
    for i in range(10000):
        game(ai_x, ai_o, log_sign)
        print(f'\033[1A{i + 1}')


if __name__ == '__main__':
    main()