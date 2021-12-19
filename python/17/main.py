import re


def get_target_ranges(input):
    """
    for a given input, which looks like
    "target area: x=(x_min)..(x_max), y=(y_min)..(y_max)",
    parse the x and y ranges.
    >>> get_target_ranges("target area: x=20..30, y=-10..-5")
    (20, 30, -10, -5)
    """

    ranges_pattern = r"x=(?P<x_min>[\d-]+)\.\.(?P<x_max>[\d-]+), y=(?P<y_min>[\d-]+)\.\.(?P<y_max>[\d-]+)"
    ranges_re = re.compile(ranges_pattern)
    match_dict = ranges_re.search(input).groupdict()
    x_min, x_max = int(match_dict.get('x_min')), int(match_dict.get('x_max'))
    y_min, y_max = int(match_dict.get('y_min')), int(match_dict.get('y_max'))
    return x_min, x_max, y_min, y_max


def check_velocity(v_x, v_y, x_min, x_max, y_min, y_max):
    """
    Check that a given velocity will cause the probe to reach the target,
    if it does, return the maximum height, otherwise None.
    >>> check_velocity(7, 2, 20, 30, -10, -5)
    3
    >>> check_velocity(6, 3, 20, 30, -10, -5)
    6
    >>> check_velocity(9, 0, 20, 30, -10, -5)
    0
    >>> check_velocity(17, -4, 20, 30, -10, -5)
    >>> check_velocity(6, 9, 20, 30, -10, -5)
    45
    """
    # print(f"checking {v_x=}, {v_y=}")
    if v_x < 0:
        return None
    x, y = 0, 0
    max_height = 0
    has_been_above_y_min = y >= y_min
    while x <= x_max:
        if x_min <= x <= x_max and y_min <= y <= y_max:
            return max_height
        if has_been_above_y_min and y < y_min:
            return None
        elif y >= y_max:
            has_been_above_y_min = True
        x += v_x
        y += v_y
        v_x = max(0, v_x - 1)
        v_y -= 1
        max_height = max(max_height, y)
        # print(f" -> {x=}, {y=}")
    return None


def main(input):
    """"""
    x_min, x_max, y_min, y_max = get_target_ranges(input)
    print(f"{x_min=}, {x_max=}, {y_min=}, {y_max=}")

    # check all possible velocities
    max_max_height = 0
    hit_count = 0
    for v_x in range(0, x_max + 1):
        for v_y in range(y_min, max(x_max, y_max) * 2 + 1):
            max_height = check_velocity(v_x, v_y, x_min, x_max, y_min, y_max)
            if max_height is not None:
                hit_count += 1
                max_max_height = max(max_max_height, max_height)
                print(f"{v_x=}, {v_y=}, {max_height=}")
    return max_max_height, hit_count

if __name__ == "__main__":
    EXAMPLE = """target area: x=20..30, y=-10..-5"""
    INPUT = """target area: x=79..137, y=-176..-117"""
    # check_velocity(6, 9, 20, 30, -10, -5)
    # print(main(EXAMPLE))
    print(main(INPUT))
    # main(INPUT)
