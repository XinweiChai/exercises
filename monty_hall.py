import random

turns = 10000
size = 3


def exclude_by_host():
    cnt = 0
    for i in range(turns):
        prize = random.randint(1, size)
        choose = 1
        if choose == prize:
            cnt += 1
    return cnt / turns


def exclude_by_player():
    cnt = 0
    available_turns = 0
    while available_turns <= turns:
        prize = random.randint(1, size)
        guess_of_the_other_player = random.randint(2, size)
        if guess_of_the_other_player != prize:
            available_turns += 1
        choose = 1
        if choose == prize:
            cnt += 1
    return cnt / turns


if __name__ == '__main__':
    print(exclude_by_host())
    print(exclude_by_player())
