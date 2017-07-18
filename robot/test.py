import sys

def max_repeat(str1, str2):
    l1 = len(str1)
    l2 = len(str2)
    if l1 >= l2:
        long = str1
        short = str2
        len_long = l1
        len_short = l2
    else:
        long = str2
        short = str1
        len_long = l2
        len_short = l1

    MAX = 0
    for i in range(len_long):
        j = i + 1
        while j <= len_long:
            sub = long[i:j]
            if short.find(sub) < 0:
                break
            elif j - i > MAX:
                MAX = j - i
                if MAX == len_short:
                    return (MAX, len_short)
            j += 1
    return (MAX, len_short)

print(max_repeat('不用那就不做，您可以做点其他的去。', '不用那就不做，您可以做点其他的去。'))
