from binarytree import Node
from more_itertools import windowed
from math import ceil, comb
# from functools import reduce
from itertools import combinations

DEBUG = False

def split_only(tree, node, split_type="split"):
    """
    If any regular number is 10 or greater, the leftmost such regular number splits.

    To split a regular number, replace it with a pair; the left element of the
    pair should be the regular number divided by two and rounded down, while the
    right element of the pair should be the regular number divided by two and
    rounded up.

    For example, 10 becomes [5,5], 11 becomes [5,6], 12 becomes [6,6], and so on.
    >>> tree = list_to_tree([0, 0])
    >>> tree_to_list(split_only(tree, list_to_tree(10)))
    [5, 5]
    >>> tree_to_list(split_only(tree, list_to_tree(11)))
    [5, 6]
    >>> tree_to_list(split_only(tree, list_to_tree(12)))
    [6, 6]
    """
    assert node.height == 0
    assert node.value >= 10
    node.left = Node(node.value // 2)
    node.right = Node(ceil(node.value / 2))
    original_value = node.value
    node.value = 0
    if DEBUG: print(split_type, original_value, tree_to_list(tree))
    return node

def explode_specific(tree, parent):
    modified_neighbors = []
    windows = [*windowed(filter(lambda node: node.height == 0, tree.inorder), 4)]
    for i, window in enumerate(windows):
        if window[1] == parent.left and window[2] == parent.right:
            left_neighbor, left_exploding, right_exploding, right_neighbor = window
            # we matched in the middle of the window, add the left and right values to their neighbors
            parent.value, parent.left, parent.right = 0, None, None
            left_neighbor.val += left_exploding.val
            modified_neighbors.append(left_neighbor)
            right_neighbor.val += right_exploding.val
            modified_neighbors.append(right_neighbor)
            break
        elif i == 0 and window[0] == parent.left and window[1] == parent.right:
            # we matched with the left exploding pair at the start, therefore it has no left neighbor
            # so left_exploding is not added to any number,
            # and right_exploding is added to the right neighbor
            left_exploding, right_exploding, right_neighbor, _ = window
            parent.value, parent.left, parent.right = 0, None, None
            right_neighbor.val += right_exploding.val
            modified_neighbors.append(right_neighbor)
            break
        elif i == len(windows) - 1 and window[2] == parent.left and window[3] == parent.right:
            # we matched with the right exploding pair at the end, therefore it has no right neighbor
            _, left_neighbor, left_exploding, right_exploding = window
            parent.value, parent.left, parent.right = 0, None, None
            left_neighbor.val += left_exploding.val
            modified_neighbors.append(left_neighbor)
            break
    if DEBUG and modified_neighbors:
        print("exploded", tree_to_list(tree), modified_neighbors)
    return modified_neighbors

def explode_only(tree):
    """
    Explode a snail number.

    If any pair is nested inside four pairs, the leftmost such pair explodes.

    To explode a pair, the pair's left value is added to the first regular number to the left of
    the exploding pair (if any), and the pair's right value is added to the first regular number
    to the right of the exploding pair (if any). Exploding pairs will always consist of two regular
    numbers. Then, the entire exploding pair is replaced with the regular number 0.

    Here are some examples of a single explode action:

    >>> exp, modified_neighbors = explode_only(list_to_tree([[[[[9,8],1],2],3],4]))
    >>> tree_to_list(exp)
    [[[[0, 9], 2], 3], 4]
    >>> [*map(tree_to_list, modified_neighbors)]
    [9]
    >>> exp, modified_neighbors = explode_only(list_to_tree([7,[6,[5,[4,[3,2]]]]]))
    >>> tree_to_list(exp)
    [7, [6, [5, [7, 0]]]]
    >>> [*map(tree_to_list, modified_neighbors)]
    [7]
    >>> exp, modified_neighbors = explode_only(list_to_tree([[6,[5,[4,[3,2]]]],1]))
    >>> tree_to_list(exp)
    [[6, [5, [7, 0]]], 3]
    >>> [*map(tree_to_list, modified_neighbors)]
    [7, 3]
    >>> exp, modified_neighbors = explode_only(list_to_tree([[3,[2,[1,[7,3]]]],[6,[5,[4,[3,2]]]]]))
    >>> tree_to_list(exp)
    [[3, [2, [8, 0]]], [9, [5, [4, [3, 2]]]]]
    >>> [*map(tree_to_list, modified_neighbors)]
    [8, 9]
    >>> exp, modified_neighbors = explode_only(list_to_tree([[3,[2,[8,0]]],[9,[5,[4,[3,2]]]]]))
    >>> tree_to_list(exp)
    [[3, [2, [8, 0]]], [9, [5, [7, 0]]]]
    >>> [*map(tree_to_list, modified_neighbors)]
    [7]
    """

    modified_neighbors = []
    if tree.height <= 4:
        return tree, modified_neighbors
    # find the parent of any pair that's nested inside four pairs
    exploding_parents = [*filter(lambda node: node.height == 1, tree.levels[4])]
    if len(exploding_parents) == 0:
        return tree, modified_neighbors
    if DEBUG: print(f"explode: there are {len(exploding_parents)} exploding parents", [*map(tree_to_list, exploding_parents)])
    # only the leftmost such pair explodes
    exploding_parent = exploding_parents[0]
    assert exploding_parent.left.height == exploding_parent.right.height == 0
    modified_neighbors = explode_specific(tree, exploding_parent)
    return tree, modified_neighbors


def get_node_depth(tree, node):
    """
    >>> t = list_to_tree([1, [2, 3]])
    >>> get_node_depth(t, t.left)
    1
    >>> get_node_depth(t, t.right.left)
    2
    """
    for level, nodes in enumerate(tree.levels):
        if node in nodes:
            return level
    return None

NO_CLEANUP = True

def split_and_cleanup(tree, node, split_type="split"):
    split_only(tree, node, split_type)
    # Here the probblem says:
    #   if split produces a pair that meets the explode criteria, that pair
    #   explodes before other splits occur.
    # but this is a fucking lie, you can see why if u enable NO_CLEANUP
    if NO_CLEANUP:
        return
    if tree.height < 4:
        return tree
    if get_node_depth(tree, node) > 4:
        explode_specific_and_cleanup(tree, node)


def explode_specific_and_cleanup(tree, node):
    modified_neighbors = explode_specific(tree, node)
    if NO_CLEANUP:
        return
    for neighbor in modified_neighbors:
        if neighbor.value >= 10:
            # split_and_cleanup(tree, neighbor, "nsplt")
            split_only(tree, neighbor, "nsplt")
    for neighbor in modified_neighbors:
        neighbor_depth = get_node_depth(tree, neighbor)
        if neighbor_depth > 4:
            explode_specific_and_cleanup(tree, neighbor)


def reduce(tree):
    while True:
        if DEBUG: print("reduce loop", tree, sum(node.value for node in tree))
        # modifications = False
        # If any pair is nested inside four pairs, the leftmost such pair explodes.
        if tree.height > 4:
            exploding_parents = [*filter(lambda node: node.height == 1, tree.levels[4])]
            if len(exploding_parents) > 0:
                explode_specific_and_cleanup(tree, exploding_parents[0])
                continue
        # If any regular number is 10 or greater, the leftmost such regular number splits.
        big_leaves = [*filter(lambda node: node.height == 0 and node.value >= 10, tree.inorder)]
        if big_leaves:
            split_and_cleanup(tree, big_leaves[0])
            continue
        return tree

def list_to_tree(snail_list):
    """
    >>> tree_to_list(list_to_tree([[[[[9,8],1],2],3],4]))
    [[[[[9, 8], 1], 2], 3], 4]
    >>> list_to_tree(10)
    Node(10)
    """
    if type(snail_list) == int:
        return Node(snail_list)
    left, right = snail_list
    return Node(0, list_to_tree(left), list_to_tree(right))

def tree_to_list(tree):
    """
    >>> tree_to_list(Node(0, Node(1), Node(0, Node(2), Node(3))))
    [1, [2, 3]]
    """
    if tree.left is None and tree.right is None:
        return tree.value
    return [tree_to_list(tree.left), tree_to_list(tree.right)]

def add_trees(left, right):
    result = Node(0, left, right)
    if DEBUG:
        print(f"adding   {tree_to_list(left)}")
        print(f"adding  +{tree_to_list(right)}")
        print(f"adding  ={tree_to_list(result)}")
    return result


def get_magnitude(tree):
    """
    The magnitude of a pair is 3 times the magnitude of its left element plus 2 times the magnitude
    of its right element. The magnitude of a regular number is just that number.

    For example, the magnitude of [9,1] is 3*9 + 2*1 = 29; the magnitude of
    [1,9] is 3*1 + 2*9 = 21. Magnitude calculations are recursive: the magnitude
    of [[9,1],[1,9]] is 3*29 + 2*21 = 129.

    >>> get_magnitude(list_to_tree([9,1]))
    29
    >>> get_magnitude(list_to_tree([1,9]))
    21
    >>> get_magnitude(list_to_tree([[9,1],[1,9]]))
    129
    """
    if tree.left is None and tree.right is None:
        return tree.value
    return 3 * get_magnitude(tree.left) + 2 * get_magnitude(tree.right)

def sum_and_reduce(input):
    """
    add and reduce the list of trees

    >>> tree_to_list(sum_and_reduce([\
            [1, 1], \
            [2, 2], \
            [3, 3], \
            [4, 4] \
        ]))
    [[[[1, 1], [2, 2]], [3, 3]], [4, 4]]
    >>> tree_to_list(sum_and_reduce([\
            [1, 1], \
            [2, 2], \
            [3, 3], \
            [4, 4], \
            [5, 5] \
        ]))
    [[[[3, 0], [5, 3]], [4, 4]], [5, 5]]
    >>> tree_to_list(sum_and_reduce([\
            [1, 1], \
            [2, 2], \
            [3, 3], \
            [4, 4], \
            [5, 5], \
            [6, 6] \
        ]))
    [[[[5, 0], [7, 4]], [5, 5]], [6, 6]]
    >>> tree_to_list(sum_and_reduce([\
            [[[0, [4, 5]], [0, 0]], [[[4, 5], [2, 6]], [9, 5]]], \
            [7, [[[3, 7], [4, 3]], [[6, 3], [8, 8]]]] \
        ]))
    [[[[4, 0], [5, 4]], [[7, 7], [6, 0]]], [[8, [7, 7]], [[7, 9], [5, 0]]]]

    >>> tree_to_list(sum_and_reduce([ \
            [[[[4,3],4],4],[7,[[8,4],9]]], \
            [1,1] \
        ]))
    [[[[0, 7], 4], [[7, 8], [6, 0]]], [8, 1]]
    """
    result = list_to_tree(input[0])
    result = reduce(result)
    for snail_list in input[1:]:
        tree = list_to_tree(snail_list)
        result = add_trees(result, tree)
        result = reduce(result)
    return result

def part1(input):
    result = sum_and_reduce(input)
    magnitude = get_magnitude(result)
    return magnitude

def part2(input):
    """
    What is the largest magnitude of any sum of two different numbers in the list?
    """
    max_magnitude = 0
    biggest_elems = sorted(input, key=(lambda l: get_magnitude(list_to_tree(l))), reverse=True)
    for left, right in combinations(biggest_elems, 2):
        result = sum_and_reduce([left, right])
        magnitude = get_magnitude(result)
        if magnitude > max_magnitude:
            max_magnitude = magnitude
        result = sum_and_reduce([right, left])
        magnitude = get_magnitude(result)
        if magnitude > max_magnitude:
            max_magnitude = magnitude
    return max_magnitude

if __name__ == "__main__":
    # DEBUG = True

    # EXAMPLE = [
    #     [[[0,[4,5]],[0,0]],[[[4,5],[2,6]],[9,5]]],
    #     [7,[[[3,7],[4,3]],[[6,3],[8,8]]]],
    #     [[2,[[0,8],[3,4]]],[[[6,7],1],[7,[1,6]]]],
    #     [[[[2,4],7],[6,[0,5]]],[[[6,8],[2,8]],[[2,1],[4,5]]]],
    #     [7,[5,[[3,8],[1,4]]]],
    #     [[2,[2,2]],[8,[8,1]]],
    #     [2,9],
    #     [1,[[[9,3],9],[[9,0],[0,7]]]],
    #     [[[5,[7,4]],7],1],
    #     [[[[4,2],2],6],[8,7]],
    # ]
    # result = sum_and_reduce(EXAMPLE)
    # print(tree_to_list(result), get_magnitude(result))
    # exit()

    # EXAMPLE = [
    #     [[[0, [5, 8]], [[1, 7], [9, 6]]], [[4, [1, 2]], [[1, 4], 2]]],
    #     [[[5, [2, 8]], 4], [5, [[9, 9], 0]]],
    #     [6, [[[6, 2], [5, 6]], [[7, 6], [4, 7]]]],
    #     [[[6, [0, 7]], [0, 9]], [4, [9, [9, 0]]]],
    #     [[[7, [6, 4]], [3, [1, 3]]], [[[5, 5], 1], 9]],
    #     [[6, [[7, 3], [3, 2]]], [[[3, 8], [5, 7]], 4]],
    #     [[[[5, 4], [7, 7]], 8], [[8, 3], 8]],
    #     [[9, 3], [[9, 9], [6, [4, 9]]]],
    #     [[2, [[7, 7], 7]], [[5, 8], [[9, 3], [0, 2]]]],
    #     [[[[5, 2], 5], [8, [3, 7]]], [[5, [7, 5]], [4, 4]]],
    # ]
    # # result = sum_and_reduce(EXAMPLE)
    # # print(tree_to_list(result), get_magnitude(result))
    # print(part2(EXAMPLE))
    # exit()

    INPUT = [
        [[[3, 9], [7, 2]], [[8, 4], [[5, 6], 0]]],
        [[[1, [4, 9]], [[1, 8], [1, 5]]], [[[2, 6], [6, 7]], [[4, 6], [9, 0]]]],
        [[[[9, 2], 1], [[0, 7], [9, 6]]], [[5, 9], [7, [6, 9]]]],
        [8, 9],
        [[4, [6, 1]], [2, [[6, 7], 2]]],
        [[6, [[4, 1], 5]], [4, 9]],
        [[[0, 6], [8, [8, 5]]], [6, 9]],
        [[0, [1, 0]], [[8, [7, 4]], [[1, 1], [5, 0]]]],
        [[[1, [0, 1]], 6], [1, 9]],
        [[2, [[9, 0], [6, 1]]], [[8, 4], [5, 7]]],
        [[[[5, 3], [0, 9]], [1, [0, 7]]], [[9, 0], [2, [2, 0]]]],
        [[2, [2, [6, 8]]], [[9, [5, 4]], [4, [3, 4]]]],
        [[[[4, 0], [7, 0]], [[4, 8], [5, 8]]], [[[7, 2], [2, 2]], [[3, 3], 3]]],
        [[5, 0], 5],
        [[8, [[5, 0], 2]], [6, [5, 1]]],
        [[[9, [8, 8]], [8, 7]], [[[4, 2], 4], [[5, 1], [4, 8]]]],
        [[[[1, 1], 3], 5], 9],
        [[[[1, 7], [6, 5]], 5], [[0, 6], 0]],
        [[9, 6], 2],
        [[[2, [0, 8]], [8, [2, 1]]], 5],
        [[[9, [3, 7]], 3], [0, [5, 9]]],
        [[[2, [1, 7]], 6], [[7, [8, 2]], [[8, 2], 8]]],
        [[[[1, 2], 1], 5], 2],
        [4, [8, [3, 9]]],
        [[[[8, 9], [6, 0]], [[1, 6], 7]], 8],
        [[2, [8, 1]], 3],
        [[2, 2], [[8, [0, 2]], [[5, 0], 5]]],
        [9, [2, [[6, 1], [8, 9]]]],
        [[4, [[6, 6], 4]], [[[9, 3], [3, 1]], 5]],
        [[[7, 8], 1], 0],
        [[[8, 8], [[1, 0], 7]], [4, 6]],
        [9, 8],
        [[[[4, 2], 9], [[9, 9], 7]], [7, [9, [5, 8]]]],
        [[4, [4, [3, 3]]], 8],
        [0, 2],
        [[4, [5, 5]], [9, [[6, 9], 4]]],
        [[[7, 3], [[1, 2], 6]], [[[2, 4], [6, 7]], [[5, 0], 9]]],
        [[[[2, 0], 5], [4, 5]], [[[6, 5], [6, 0]], [1, [3, 4]]]],
        [[3, [6, 8]], [[[3, 0], 0], [[2, 8], 7]]],
        [[[4, [6, 2]], [9, [4, 1]]], [8, [3, 4]]],
        [[[6, [6, 8]], [7, [2, 0]]], [4, [[8, 7], [1, 6]]]],
        [2, [0, [4, 0]]],
        [[[[0, 5], 1], 8], [[9, [0, 3]], 3]],
        [[[3, [5, 2]], [3, [3, 2]]], [[[7, 3], 1], 7]],
        [1, [[[1, 8], [1, 7]], 0]],
        [[8, 6], [[0, 4], 4]],
        [[[8, 2], [4, 6]], 3],
        [5, [[[7, 5], [4, 5]], [0, 2]]],
        [[3, [3, 6]], 6],
        [[[[6, 8], [5, 7]], [[7, 3], 5]], [[8, [4, 8]], 8]],
        [[[[5, 8], [3, 1]], [[3, 7], [7, 0]]], [[9, 7], 0]],
        [[2, [[5, 3], 8]], 0],
        [0, [2, 8]],
        [[8, 9], [[[2, 2], [4, 7]], [[4, 0], 1]]],
        [[[[3, 0], 8], [[7, 3], [6, 1]]], [[3, 8], [4, 2]]],
        [[[[6, 7], [4, 3]], [[3, 9], 5]], 8],
        [[[7, 7], [[3, 4], 7]], [[[0, 4], 1], 9]],
        [[[7, 5], 5], [[2, [9, 9]], [0, [3, 5]]]],
        [[[[3, 3], [6, 1]], [5, 8]], [[4, 7], [8, 1]]],
        [[[0, [7, 3]], [6, [7, 2]]], [[0, 8], 7]],
        [[[2, 7], [9, 7]], [8, [3, 8]]],
        [[[0, 2], 6], [[9, [6, 5]], [[3, 9], 1]]],
        [[7, [[3, 4], [2, 8]]], [[[4, 1], 4], 7]],
        [[3, [[3, 4], 6]], [[3, 9], [[4, 5], [3, 0]]]],
        [[[5, [5, 1]], [2, 4]], [1, [[1, 6], 6]]],
        [[[5, 6], [[1, 3], [5, 0]]], [[[4, 1], 8], [5, 5]]],
        [[[[2, 0], 7], [[8, 9], 1]], [[[4, 0], [1, 6]], 1]],
        [[[2, 0], [[4, 2], [9, 9]]], [4, 9]],
        [[[[1, 9], 6], 2], [[5, 4], [2, 4]]],
        [[[[4, 1], [4, 5]], [[2, 3], 2]], [3, [[8, 8], 1]]],
        [[[[8, 1], 0], [2, 2]], [[2, [7, 1]], 1]],
        [[[7, 4], [[1, 3], 5]], [[6, 8], [[0, 0], 2]]],
        [[[1, 2], 8], [[[1, 7], [4, 0]], [[8, 2], 8]]],
        [[[0, 8], [3, 6]], [[[5, 3], 7], [9, 7]]],
        [[4, 6], [[[7, 9], [7, 5]], [[4, 6], [8, 4]]]],
        [[[[7, 3], 0], [[6, 2], [7, 2]]], [9, [[8, 0], 3]]],
        [[[3, 0], 1], [[2, 3], 1]],
        [[[5, [8, 6]], [[1, 2], 2]], [[[1, 4], 6], [5, [7, 1]]]],
        [[[[1, 5], 8], [0, 0]], 4],
        [[[7, [6, 8]], 3], [[5, 1], [[2, 8], [4, 6]]]],
        [3, [[[5, 8], [4, 5]], [[7, 7], 8]]],
        [[6, [7, [8, 2]]], [[9, 0], 0]],
        [[[8, [7, 6]], 1], [[2, 4], 6]],
        [[[[0, 4], 2], [0, 7]], [6, 6]],
        [1, [[1, 9], [9, 3]]],
        [[[[5, 2], [5, 3]], [[9, 0], 4]], 2],
        [[[[5, 5], 3], [7, [1, 2]]], [6, [7, 2]]],
        [[[[2, 1], 3], 8], [[2, [8, 2]], [7, 4]]],
        [[8, [9, [1, 8]]], [[[4, 4], [0, 6]], [6, 3]]],
        [[[1, 6], [1, [2, 5]]], 0],
        [[[[0, 1], [7, 2]], [[7, 2], 3]], [2, [[7, 8], [0, 7]]]],
        [[[[1, 8], 8], [[5, 7], [3, 4]]], [[[2, 5], [7, 4]], [[8, 4], 9]]],
        [[[2, 2], [5, [1, 0]]], [[[6, 6], [3, 0]], [[8, 5], 5]]],
        [[[[8, 2], [4, 8]], [9, 4]], [[8, [7, 9]], 0]],
        [[3, [5, [2, 4]]], [[[8, 1], 0], [[0, 4], [4, 5]]]],
        [[5, [9, [3, 8]]], [4, [1, [5, 2]]]],
        [[[3, [0, 6]], [7, [8, 7]]], [[6, 8], [[8, 7], 0]]],
        [[[[0, 2], 5], [4, 6]], 3],
        [[6, 7], [[1, [4, 6]], 9]],
        [7, [3, [[8, 8], 5]]],
    ]
    # print(part1(INPUT))
    print(part2(INPUT))
