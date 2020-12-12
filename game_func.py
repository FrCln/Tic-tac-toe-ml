from field import Field


def print_state(field, player):
    print(field)
    print(dict(enumerate(player.weights[field.state])))


def game(player_x, player_o, log=False):
    f = Field()
    players = [player_o, player_x]
    x = 1
    if log:
        print_state(f, players[x])
    for _ in range(9):
        sign = x + 1
        step = int(players[x].choice(f.state))
        f[step] = sign
        if log:
            print_state(f, players[x])
        if f.check_win(sign):
            players[x].correct(1)
            players[not x].correct(-1)
            return sign
        x = not x
    else:
        for player in players:
            player.correct(0)
    return 0