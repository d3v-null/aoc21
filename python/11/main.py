"""
--- Day 11: Dumbo Octopus ---
You enter a large cavern full of rare bioluminescent dumbo octopuses! They seem to not like the Christmas lights on your submarine, so you turn them off for now.

There are 100 octopuses arranged neatly in a 10 by 10 grid. Each octopus slowly gains energy over time and flashes brightly for a moment when its energy is full. Although your lights are off, maybe you could navigate through the cave without disturbing the octopuses if you could predict when the flashes of light will happen.

Each octopus has an energy level - your submarine can remotely measure the energy level of each octopus (your puzzle input). For example:

5483143223
2745854711
5264556173
6141336146
6357385478
4167524645
2176841721
6882881134
4846848554
5283751526
The energy level of each octopus is a value between 0 and 9. Here, the top-left octopus has an energy level of 5, the bottom-right one has an energy level of 6, and so on.

You can model the energy levels and flashes of light in steps. During a single step, the following occurs:

First, the energy level of each octopus increases by 1.
Then, any octopus with an energy level greater than 9 flashes. This increases the energy level of all adjacent octopuses by 1, including octopuses that are diagonally adjacent. If this causes an octopus to have an energy level greater than 9, it also flashes. This process continues as long as new octopuses keep having their energy level increased beyond 9. (An octopus can only flash at most once per step.)
Finally, any octopus that flashed during this step has its energy level set to 0, as it used all of its energy to flash.
Adjacent flashes can cause an octopus to flash on a step even if it begins that step with very little energy. Consider the middle octopus with 1 energy in this situation:

Before any steps:
11111
19991
19191
19991
11111

After step 1:
34543
40004
50005
40004
34543

After step 2:
45654
51115
61116
51115
45654
An octopus is highlighted when it flashed during the given step.
"""

import numpy as np
from itertools import count, product


def flash(levels, x, y):
    """
    increment every neighbor of (x, y), then increment those neighbors who were
    previously less than 9, but are now greater than 9.
    >>> input = "11111\\n19991\\n19191\\n19991\\n11111"
    >>> levels = np.array([[int(c) for c in line] for line in input.splitlines()])
    >>> levels += 1
    >>> sum(flash(levels, *indices) for indices in product(*map(range, levels.shape)) if levels[indices] > 9)
    9
    >>> levels[(levels > 9)] = 0
    >>> levels
    array([[3, 4, 5, 4, 3],
           [4, 0, 0, 0, 4],
           [5, 0, 0, 0, 5],
           [4, 0, 0, 0, 4],
           [3, 4, 5, 4, 3]])
    >>> levels[(levels > 9)] = 0
    >>> levels += 1
    >>> sum(flash(levels, *indices) for indices in product(*map(range, levels.shape)) if levels[indices] > 9)
    0
    >>> levels
    array([[4, 5, 6, 5, 4],
           [5, 1, 1, 1, 5],
           [6, 1, 1, 1, 6],
           [5, 1, 1, 1, 5],
           [4, 5, 6, 5, 4]])
    """
    flashes = 1
    for i, j in product(range(x-1, x+2), range(y-1, y+2)):
        # if the neighbor (x,y) is out of bounds, or (i,j) skip it
        if (i == x and j == y) or not (0 <= i < levels.shape[0]) or not (0 <= j < levels.shape[1]):
            continue
        # if it hasn't exploded yet, increment it
        if levels[i, j] <= 9:
            levels[i, j] += 1
            # if it ends up exploding, recursively flash its neighbors
            if levels[i, j] > 9:
                flashes += flash(levels, i, j)
    return flashes


def main(input):
    """
    Given the starting energy levels of the dumbo octopuses in your cavern, simulate 100 steps. 
    How many total flashes are there after 100 steps?
    >>> EXAMPLE = "5483143223\\n2745854711\\n5264556173\\n6141336146\\n6357385478\\n4167524645\\n2176841721\\n6882881134\\n4846848554\\n5283751526"
    >>> main(EXAMPLE)
    flashcount=1656
    synchronised at i+1=195
    """
    levels = np.array([[int(c) for c in line] for line in input.splitlines()])
    flashcount = 0
    for i in count():
        # increment all levels by 1
        levels += 1
        # determine flashes
        flashes = [indices for indices in product(
            *map(range, levels.shape)) if levels[indices] > 9]
        # recursively increment flash neighbors and count the flashes
        flashcount += sum(flash(levels, *indices) for indices in flashes)
        # reset flashed levels to 0
        levels[(levels > 9)] = 0
        # after 100 iterations, print the flash count
        if i == 99:
            print(f"{flashcount=}")
        # when everything synchronizes, print the number of iterations.
        if (levels == 0).all():
            print(f"synchronised at {i+1=}")
            break


if __name__ == "__main__":
    EXAMPLE = """5483143223
2745854711
5264556173
6141336146
6357385478
4167524645
2176841721
6882881134
4846848554
5283751526"""
    INPUT = """2138862165
2726378448
3235172758
6281242643
4256223158
1112268142
1162836182
1543525861
1882656326
8844263151"""
    main(EXAMPLE)
    # main(INPUT)
