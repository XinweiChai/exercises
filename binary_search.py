def rec_search(arr, t, start, end):
    if start > end:
        return -1
    pos = (start + end) // 2
    if t == arr[pos]:
        return pos
    elif t < arr[pos]:
        return rec_search(arr, t, start, pos - 1)
    else:
        return rec_search(arr, t, pos + 1, end)


def binary_search(arr, t):
    if not arr:
        return -1
    pos = len(arr) // 2
    if t == arr[pos]:
        return pos
    elif t < arr[pos]:
        return binary_search(arr[0:pos], t)
    else:
        temp = binary_search(arr[pos + 1:], t)
        if temp == -1:
            return -1
        else:
            return temp + pos + 1

if __name__ == "__main__":
    x = [1, 2, 3, 5, 6, 7, 8, 9, 10]
    # print(rec_search(x, 7, 0, len(x) - 1))
    print(binary_search(x, 10))