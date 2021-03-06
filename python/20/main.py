import numpy as np
from itertools import product
from more_itertools import split_at


def enhance(inp, enhancer, pad_value):
    pad = np.pad(inp, (3,3,), constant_values=(pad_value,))
    out = np.zeros((pad.shape[0]-2, pad.shape[1]-2), dtype=np.int8)
    print(f'{pad_value=}')
    display(pad)
    # return np.array([
    #     inp.get((x, y), 0)
    #     for x, y in np.ndindex(inp.shape)
    # ])
    for i, j in np.ndindex(out.shape):
        address = ""
        for di, dj in product(range(3), repeat=2):
            address += str(pad[i+di, j+dj])
        # print(f"{i=}, {j=}, addr={int(address, 2)} ({address}). enh={enhancer[int(address, 2)]}")
        out[i, j] = enhancer[int(address, 2)]
    return out


def display(inp):
    print(f"({inp.shape})=")
    for line in inp:
        print(''.join([['.','#'][int(x)] for x in line]))

def main(input):
    enhance_lines, inp_lines, *_ = split_at(input.splitlines(), lambda x: not x)
    print(f"{enhance_lines=}\n{inp_lines=}")
    enhancer = [['.', '#'].index(x) for x in ''.join(enhance_lines)]
    print(f"{len(enhancer)}, {enhancer=}")
    inp = np.array([
        [['.', '#'].index(x) for x in line]
        for line in inp_lines
    ])
    for i in range(50):
        # dumb hack to deal with enhancer starting with '#'.
        pad_value = (i % 2) * enhancer[0]
        print(f"{i=}, {pad_value=}")
        display(inp)
        inp = enhance(inp, enhancer, pad_value)
    display(inp)
    # count the number of '#'
    print(f"{np.sum(inp)=}")



if __name__ == "__main__":
    EXAMPLE = """..#.#..#####.#.#.#.###.##.....###.##.#..###.####..#####..#....#..#..##..##
#..######.###...####..#..#####..##..#.#####...##.#.#..#.##..#.#......#.###
.######.###.####...#.##.##..#..#..#####.....#.#....###..#.##......#.....#.
.#..#..##..#...##.######.####.####.#.#...#.......#..#.#.#...####.##.#.....
.#..#...##.#.##..#...##.#.##..###.#......#.#.......#.#.#.####.###.##...#..
...####.#..#..#.##.#....##..#.####....##...##..#...#......#.#.......#.....
..##..####..#...#.#.#...##..#.#..###..#####........#..####......#..#

#..#.
#....
##..#
..#..
..###"""
    INPUT = """###.#..##.####.....#.#..##.#....##.##.##..#.####.#.#.#.#.#..##.####.####...##.#.###..#..#.##...##..##..#....###########..####..###....#.##...##...#....#########.#..#..##..#..#.#.#.##...###..####.##.#####.####.#....#.#.##..###...#..#...##.##.#..#...#..##..#..#...###........#..##....#.#.##.##.##.######..##.#...#..#######.###.#..#.#....#.###.#....#.....#.#..##.#.......##..#..#..#...#..##.######.#.####.#....#.....#.##.#.#..##.#..##..#.##..#.##...###......##.#####..##.###.#.#.######.#####..#.#..#.....#....#.##..

.##.#######....##...######.##.#.#...#.#..#..#.##...#.#.#.#.#.##..#......#..##..#.#..#.#.##.#.#...#..
.#.#.#.##..########.....####..#..##...##.###...#########....####.##.####..##.##..####.##...#..#....#
##..#######....##.##.#...#.#.#.##.#...#.###########....#.##.#.#...#...#..###..#..#..#.##.#.#.##..###
#.##....##..##....#..#.####.#..##....###.#...#.####.#..#........#..####..##.#####.#..#.#.#..#...##.#
..##.####...#..#.#.####..#.####....#....#.##.##.####...#..#....####..........##.....###.#..#.####.#.
##.#.#.###.##..#..#...#.###.####.#...#.##.#.##...###.#.####.#.##......###.##.###..#..#.....##.###...
#.#.#####.#######.######..##.#.....#.#.##...#..###.##.#.#....#.....#.##..#.##.#######..##..#....#..#
...#.##.##.#...###.#...#....#.#...##..##.###......#.#.####....####.#######....###..###...#...#....##
.##..##.....##.###..#..##..#......##.#.##...##.#.#.#.##...#####.##.....#....#.##.#.#.#....###.##.#..
..####.##..#.###..#....#..####....#.#.###.####.#....##..#.#.##.....##.###.##.###..##......#....#.#..
#.#.##.....#.##.###..##..####.#...#..##.#.#.##..##......#..###.######.#.##..##.###.#####.#.........#
.#.#.#.####.#.####.#.#.#.#########..##.#.#.....#.####.#.#.#..###.#..#..##..#.#.#.##........#..#.####
######.###..##.##.#.##.##...#.......#.#..#..##.#..#....#.#...##.#.###.#..##.##..##..#....###.#.###..
#..#..#####......####.#.#####...#...##..##.#..###.....#..#.#...######.##.######..#.##.###.#...#...##
..#####.#.#...##.###.####...#..##.##..##.##.#.#..####..#.####....#.#..#....##.##.##..#..##..##.#..#.
....#####.##..##.###.##...#.##.#.##....##...###..#...####.#.#..#..###...##..##.###.##.##...###.###..
....##......#....##..##.#.###..###..##.....##.#.#.#.#.###.###..#.##.####..#.#..#...#...##...#.##.##.
##....##....#.#...#......#..#.#.#..#..##.##..#...###....#.#..#.#.###.###..######.##...##..##...##.#.
##.#..###..#..##...##.#..#...###...#..####.#....####..##.###.##...#....#####.##...#............#.#..
..##..#..###.#...##.#.##.#....###.#...#.#.###..#.#..#.##...#.#.###.###.####..#.#####.###..#.#...#..#
..##..##.#..###.#..#.##.##..#.##.##.####......####.###..#.##..#.#....#.##...###...##.##.##.##.#.#.##
#.##.#.#.#.###.#..#.##.#.#.####...#.#.###.##.##..#.#.#.###.#.##.##.#.#.#.###...##.....#......#...###
.##..#########.####.####.#.##....#....#.#.#.#..#.#..##.###.###....###...#..#.##..#..##..#..#...##.##
..###..##.##..#.#....##..##..#.####..#...#.#.####.#####..##....##.....#....#...####...##...###.####.
########.##..##.##...##.##..###...#####.####.#.#.#.#.######...##..####..##..##....#..##.....###.####
.##.....#..#....#.####...#.###..####...##.#...###.##...##..#..###.#..#.#####...##...#..##.##..###...
.###....#.#####....#.#....#.###.......#######.#...##...#..#.#....#..##..###.####.....#.#.##..##.##..
#...#.##.#.##.#.##...###.#..#.####...##...####.#...#.####.#.##...#...##.......#..#......#.##.#..#.#.
..#####..#......#.#..#...#...#..#.....##.#...##..###.......##..##..#.#....###.#######..#...#.#...##.
.......##.###....#.##....####..#..#.####.#.###########.#..#....###.#.###.#.##...#.#...###.#.#.....#.
.###.##...###....###..#........##.......##...#.###...##.##..#....##.....##.##....##..#...#.##.#..##.
####...#..##......###.##..#.#######.#.#..##...#.#.#...#####.####...########.#..#..###.############..
#.#.#..##....#.....##...#.#####.##.#####...#....#.##.#..#.##.##...###..#.##.#.###.###..#.#.....#..#.
.####.#####..#.##.#.###.##..#.#.##...#...#.#.....###..#..#.#...####...#...##.###.###..##..#.....##..
##...#...##..####....#.#.####...#..##.....#.##...###..##.#.#.#.....##.##.#.........##...###..##....#
####.#.##....#.....##.#....##.......#.#.#.#.###..#.###...###..#.##.###...#..###...###...#...##.#.###
.#...#.#######.###########..#..###.##..#.##.##...#..###....#######.##..#.#....####.#..##...#...#....
###..#..##.#.##.##....#..#.#.##...#####.##......#.##....#.##..##...#.##.#.##.##...#.#.#.#....#.##..#
.##....#..#..#...#..#.#....#.#####...#..#.....#....#.#....##...##.##..#..#..........#.#.###...##.#.#
#....#.####...######.#####.#...##..#.#...##..##...#.##.#.##.####.#####.....###..#..#.#.##.##.#..#...
..##..###.####.##.....###.###...#....##.#.#...#.....##....#.#..#..#####..##.#.###.#..##.#.###...#.#.
..##.##...#..#..#.#..#.#..##.#.#.......#.#.#...#.#..#..##..##.###.###...###..##...#####...#..#.###.#
#.#.#.....##........#####.....#...##..###.#.#.##...#.##..#.###...#.######.###..##..###.#.#.#....##..
..#.#.#.##.####.#..#.....#.##.......##...#..##.#####..###..#..#..####..##.##.#.##...####.#.##..#.##.
#######.#..###.....##..#.#.#####.#..#.#.##.###..#.......###......##..#####..#.#..##.##....#..#..#..#
##.##..###.....##..####.##.###.#.#......#.#.######.#..#......#####.....#######.#.#.#.###.#.###.#.###
##.#..##.##...#...#..##..#...#.##.#...#####..##.##..#.#.#..#..##..#..#.#..#........#...#..###..#.##.
#.#.#...#..###.#......#.#..#.########......##.#.##..#..##..#...###.#..#.#..#.#..#####.##...#########
.#..#.##.#######.#####.##.####....#..#.#.#.#########.#.###....#.#....###...##.#.#....##....#.###....
..######.####....#..##...####..#...#..#...#####.##.#.#....#..#.#######..#....#.#.#..#.#....###..##.#
...#.###..#..######.####....##....####.##..#.#.#####...##.#..#..#.###.#.#.#.##....#.###.#..#.#.###..
#..#.#.#.##.###.###.#....##.#####.#.##.....####.....#.....#.#.###...#.##.#...##.###...##....##.#..#.
###..#.##...###..##..#..#.##.#.####...##.#..#.###..#.#..#.#.....#####..#.######..###..#....##..#.##.
##..##.###.###.#####.#..##...####.###..###.###.##..#..##...#....##.###.##..###..#.........##.##..#.#
##...#....#.##.#.#......####.##....##.##....##...#....#.#.....#....##...##....###..###..###.#.....##
.####...#..###...#####.#.##...##.....##...####..#####..##...#..##...####.....#.##...#.###...#.##.###
##.#..##..#..#.#####...#...##....##.#.#.#.########..#..#.#.###..###...##.##.#.##.#..##.#.##.###.#.#.
###.#.###.###......#....#######.#.#..#..##...##.###....###.##.#...##....#...#..#.#...######..##.###.
#.###.####.###.#.#..##.###..#.##..#...#..#.#..#####..#.#.###.#.#.#..#..#...#.#....######.##.....##.#
.#...#.#.#..#.##..##..#.##.#####..#....######...#...#.....#.#..##.#...###.##.#######.#.##.#....#.#..
.#....#...#..#.#.##.#....##....#..#...#..#.##..#.##.##..#..#..#.#.#..##....##.#..#...#..#...##.##...
..#.#..#.#...#.###.#.#######.#...##..#.##...#.#.###.#..#.##..#..#.#######.####.#.####..#.##.#.##..#.
#.#..#######.###..#.####..#.##.#...###.###.#..#.##.#...#...#.#.#.###..#.##.##....#.###...##...#.#..#
.##...#...##.#.##..####.#.#.#..####.##...##..#..#.#.#..#..#....##.##.##...#.#.#.##.#....#.######...#
##.#..#.##.....###.########.##.####...#.####...##.######.###..#######.#..##.#..#..#.#.####..###.#..#
#.#..####.########...##..##..####..#.##.#..#..#..#..###.######..##.....##.##..#...#....#...##....###
#############..##..###..#.###.##..###..##...##.#.......#####.#.#..##..#.....##.#..#....##....#.##...
####.##.#.#...##.#..#..#.##.##.#.###..#.#.#.....#.#.###..#..##.#.#.##..##.#...##..###....##...##.#.#
#...##.#....#..#.....##..#.#...##...##..#.#########.#..#.#.##........###.###...##..#####.###.#....#.
..#..#...#..##...#..##...#.#.....#.#######.####.##..#.#...#......#.#..####.#........#...#.#..#..##.#
#.##..##.#.#..##.#.####.#.#..#..#...#####.######..#.#.######...#..##.##..#####.#.#.##...##.#..##..##
...##.##.#....###.#...#.##...#..###...##.#.#..#.###.....#...##.......##.###.##..##.#.##...#....##.#.
###....##.#.#.#..#....####.#.....##.....#...##.#.....#.###.#####.#..#.##...###.......#...#.....#.#.#
....#.#..#.#..##.####.##...#######.#..#.##.##..####..#.#....##..#.....#...#.##.####.##.#####.#######
#..#..#.###....#.##.#.#.##.###.##.###.............#....##.##.###..#...#.#..#.#.#.#...#..#......#####
...##..##..#....####.#..##.#.#.#.#.....#.#..###...##.##....#####......#####.##..###.##.#..###..#...#
.##..#.#.#.##.###.#.#..##...#.##..#####.######..#.#...#....#...#..##..#.#.....#.#.##..##.#..##.##...
.#.#.#.#.#..####.#.#.##.....##.##.#.##..###.#..##...##..#....##..#..##...##.#..##..####.#..#.#...#..
#.#..##.#.#..#...##.##....#.#...###...###.####.#.####.##.#...##.#..##....###..#..#.##.#.#..#.#.##..#
.###...####.#.###....##..#...#####......##...#...#..#.#..###..#.....##..###.#.###.....#.##..####.#.#
#..###.#....#..###...#..####.####..#.#####.#.....#...##..##..#...#..#...#.##...##..########..#.##.#.
..######..#.####..#..####..#..#...##...#...###.##...#..###.##...#.###.##...#....#....##..##.##.###.#
###.#.##..###..#..#........#.#.........##..##.....###.###.#.......###..#.#....##....#.....#.##...###
..#.....#.#..###.##.####.#.......#.#.##..##.#.##...####..#.###..#.###.#####.####....#.#...#.#..##..#
.....######.###..##.#..####..#..##.####.##..##.##...#.#..##...#.##..####.####...##..#.....#.....####
###.##.#..#.##.#.#.###....#..#.#..##..#.....###.##.##.#.###.####...##.###..#..##.##..##..##.###...##
#....####.####.####.#.######...#########..##..#.#....#.......#.##.#.....#.###..#.##....#.##..##.##.#
...##..#...#..##..#.###.##..#..###.###....###.####.#.####.#.#.#.#.#....#######.##..###.#.######.##..
#...#.#.#...#.#.#..#.###.#.#####.#.###.#..##.#.####...#.#.#.....#..####..#.###....##.##..#.#..##.#.#
...##..##....#.##.###...##.....###....#..###....#.#.##..###..###..#.#....#.###....#.##..######..#.##
...#..#...###...##.###.....#...#.#..#.##..###.#....###.#.#...##.#..##..###.#...#..#..#.##..#...#.#..
#.....#.###.##..##.#..#..#....#..##.###.##.#.#..##...#....##.##.#.#....#.###..#..###....###.#.#.#.##
...##.#..###..##..##.###.#.#..###....#.##..##.#..###...##...#.#.....###.....##.....#.#.##.#.###..#.#
..##.##..#...#..#.#.##.##.########.#.######....######.#.###..##...###..#####.##.#..#.##.#.##..######
.....##.##..#.#.#...###.#.#....##...###.....#.###...#.....###.#......#.#..#.##..#.######.#...####..#
..####....####.#......#.##..###.###...##########..##......#..###.#.#...#####.#.#########..###..#....
#..#..#.#..#..#..##..#.###.#...#.#.####...#.#######...##.##..#..####.#.....#..##.####.##.##.##.#....
#..#....####.#.###.##...##.###.####.##.######....#.#.#.###.##.##.#.#.##...##.#.#.##.#..#..###.#.....
.###.#....##.#.###...##.#.##...##.###.#.####.##.#####..#.##....##..##....#######...#..###.#....##...
.#..#..###.#.##.....##..#.#.###.###..#...#.#.#...#..##..###....#..##........#.#.##..##.####.#.###.#.
"""
    # main(EXAMPLE)
    main(INPUT)
