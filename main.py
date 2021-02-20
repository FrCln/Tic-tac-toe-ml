import argparse
import csv
from datetime import datetime
import os
import sys

from ai import AI, FakeAI, AI2, AIMinimax
from field import Field


GAMES = 10000


def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-x', '--aix', default='prog')
    parser.add_argument('-o', '--aio', default='prog')
    parser.add_argument('-c', '--coef')
    parser.add_argument('-g', '--games')
    args = parser.parse_args()


    if args.coef:
        if not args.coef.isdigit():
            print('Coefficient must be fractional part of a real number')
            sys.exit(1)
        coef = int(args.coef) / 10 ** len(args.coef)
    else:
        coef = None

    if args.games:
        if not args.games.isdigit():
            print('Number of games must be a number')
            sys.exit(1)
        games = int(args.games)
    else:
        games = GAMES

    return args.aix, args.aio, coef, games


def game(ai_x, ai_o):
    f = Field()
    players = [ai_o, ai_x]
    x = 1
    for _ in range(9):
        sign = x + 1
        step = int(players[x].choice(f.state))
        f[step] = sign
        if f.check_win(sign):
            players[x].correct(1)
            players[not x].correct(-1)
            return sign
        x = not x
    for ai in players:
        ai.correct(0)
    return 0


ai_types = {
    'fake': FakeAI,
    'simple': AI,
    'prog': AI2,
    'minimax': AIMinimax
}

aix_type, aio_type, coef, games = get_args()

ai_x = ai_types[aix_type](learning_coef=coef)
ai_o = ai_types[aio_type](learning_coef=coef)
ai_x.normalize()
ai_o.normalize()
score = [0] * 3
log = [[0] * 4]
print('n:     draws: x_win: o_win:\n')

for i in range(games):
    score[game(ai_x, ai_o)] += 1
    log.append([i+1] + score)
    print(f'\033[1A{i:<6} {score[0]:<6} {score[2]:<6} {score[1]:<6}')

save_file = os.path.join('data', 'out')
ai_x.save_data(save_file + '-ai_x.bin')
ai_o.save_data(save_file + '-ai_o.bin')
with open(save_file + '-results.txt', 'w') as f:
    f.write('n:     draws: x_win: o_win:\n'
            f'{i:<6} {score[0]:<6} {score[2]:<6} {score[1]:<6}\n')

with open(save_file + '-results.csv', 'w') as f:
    csv_writer = csv.writer(f)
    csv_writer.writerows(log)