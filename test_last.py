from ai import AI
from log import game

ai_o = AI('data\\23-04-18-41-ai_o.bin')
ai_x = AI('data\\23-04-18-41-ai_x.bin')

game(ai_x, ai_o)