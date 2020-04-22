def hanoi(n, start, end, by):
    if n == 1:
        print(str(start) + "->" + str(end))
    else:
        hanoi(n - 1, start, by, end)
        hanoi(1, start, end, by)
        hanoi(n - 1, by, end, start)


if __name__ == "__main__":
    hanoi(3, 1, 3, 2)
