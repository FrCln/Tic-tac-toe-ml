import argparse
import csv
from datetime import datetime
import os
import sys

from ai import AI2, FakeAI
from field import Field
from game_func import game


GAMES = 5000
ENEMIES_O = 30
ENEMIES_X = 15

init_data_file=os.path.join('data', 'init_weights.bin')
ai_o = AI2(init_data_file)
log = [[0] * 4]

print('Learning O-s')
for enemy in range(ENEMIES_O):
    score = [0] * 3
    ai_x = FakeAI()
    print(f'Enemy #{enemy + 1}')
    print('n:     draws: x_win: o_win:\n')
    for i in range(GAMES):
        score[game(ai_x, ai_o)] += 1
        log.append([enemy * GAMES + i+1] + score)
        print(f'\033[1A{i:<6} {score[0]:<6} {score[2]:<6} {score[1]:<6}')
    ai_o.normalize()

print('\nLearning X-s')
ai_x = ai_o
for enemy in range(ENEMIES_X):
    score = [0] * 3
    ai_o = FakeAI()
    print(f'Enemy #{enemy + 1}')
    print('n:     draws: x_win: o_win:\n')
    for i in range(GAMES):
        score[game(ai_x, ai_o)] += 1
        log.append([enemy * GAMES + i+1] + score)
        print(f'\033[1A{i:<6} {score[0]:<6} {score[2]:<6} {score[1]:<6}')
    ai_x.normalize()

print('\nTesting both')
ai_o = ai_x.copy()
score = [0] * 3
print('n:     draws: x_win: o_win:\n')
for i in range(GAMES):
    score[game(ai_x, ai_o)] += 1
    log.append([enemy * GAMES + i+1] + score)
    print(f'\033[1A{i:<6} {score[0]:<6} {score[2]:<6} {score[1]:<6}')
ai_x.normalize()
ai_o.normalize()

print('\nOnce again')
ai_o, ai_x = ai_x, ai_o
score = [0] * 3
print('n:     draws: x_win: o_win:\n')
for i in range(GAMES):
    score[game(ai_x, ai_o)] += 1
    log.append([enemy * GAMES + i+1] + score)
    print(f'\033[1A{i:<6} {score[0]:<6} {score[2]:<6} {score[1]:<6}')
ai_x.normalize()
ai_o.normalize()

save_file = os.path.join('data', 'out')
ai_x.save_data(save_file + '-ai_x.bin')
ai_o.save_data(save_file + '-ai_o.bin')

with open(save_file + '-results.csv', 'w') as f:
    csv_writer = csv.writer(f)
    csv_writer.writerows(log)
