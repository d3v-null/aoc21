import numpy as np


def cycle(histogram):
    """
    >>> cycle({1: 1, 2: 1, 3: 2, 4: 1})
    {0: 1, 1: 1, 2: 2, 3: 1}
    >>> cycle({0: 1, 1: 1, 2: 2, 3: 1})
    {0: 1, 1: 2, 1: 2, 6: 1, 8: 1}
    """

    next_histogram = {}
    for k, v in histogram.items():
        if k == 0:
            next_histogram[6] = v + next_histogram.get(6, 0)
            next_histogram[8] = v + next_histogram.get(8, 0)
        else:
            next_histogram[k - 1] = v + next_histogram.get(k - 1, 0)
    return next_histogram

def main(input):
    histogram = {}
    for v in map(int, input.split(',')):
        histogram[v] = histogram.get(v, 0) + 1
    for i in range(256):
        print(f"{i=} {sum(histogram.values())}, {sorted(histogram.items())=}")
        histogram = cycle(histogram)
    return sum(histogram.values())
    

if __name__ == "__main__":
    print(cycle({1: 1, 2: 1, 3: 2, 4: 1}))
    print(cycle({0: 1, 1: 1, 2: 2, 3: 1}))
    print(main("3,4,3,1,2"))
    print(main("5,1,1,3,1,1,5,1,2,1,5,2,5,1,1,1,4,1,1,5,1,1,4,1,1,1,3,5,1,1,1,1,1,1,1,1,1,4,4,4,1,1,1,1,1,4,1,1,1,1,1,5,1,1,1,4,1,1,1,1,1,3,1,1,4,1,4,1,1,2,3,1,1,1,1,4,1,2,2,1,1,1,1,1,1,3,1,1,1,1,1,2,1,1,1,1,1,1,1,4,4,1,4,2,1,1,1,1,1,4,3,1,1,1,1,2,1,1,1,2,1,1,3,1,1,1,2,1,1,1,3,1,3,1,1,1,1,1,1,1,1,1,3,1,1,1,1,3,1,1,1,1,1,1,2,1,1,2,3,1,2,1,1,4,1,1,5,3,1,1,1,2,4,1,1,2,4,2,1,1,1,1,1,1,1,2,1,1,1,1,1,1,1,1,4,3,1,2,1,2,1,5,1,2,1,1,5,1,1,1,1,1,1,2,2,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,4,1,1,1,1,1,3,1,1,5,1,1,1,1,5,1,4,1,1,1,4,1,3,4,1,4,1,1,1,1,1,1,1,1,1,3,5,1,3,1,1,1,1,4,1,5,3,1,1,1,1,1,5,1,1,1,2,2"))