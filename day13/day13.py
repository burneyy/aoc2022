from functools import cmp_to_key


test_input = """[1,1,3,1,1]
[1,1,5,1,1]

[[1],[2,3,4]]
[[1],4]

[9]
[[8,7,6]]

[[4,4],4,4]
[[4,4],4,4,4]

[7,7,7,7]
[7,7,7]

[]
[3]

[[[]]]
[[]]

[1,[2,[3,[4,[5,6,7]]]],8,9]
[1,[2,[3,[4,[5,6,0]]]],8,9]"""


def parse_input(input_str):
    list_pairs = []
    for pairs in input_str.split("\n\n"):
        left, right = pairs.splitlines()
        list_pairs.append((eval(left), eval(right)))

    return list_pairs


def parse_input_part2(input_str):
    lists = []
    for pairs in input_str.split("\n\n"):
        left, right = pairs.splitlines()
        lists.append(eval(left))
        lists.append(eval(right))

    # Divider keys
    lists.append([[2]])
    lists.append([[6]])
    return lists


def test_parse_input():
    pairs = parse_input(test_input)
    assert len(pairs) == 8
    for left, right in pairs:
        assert isinstance(left, list)
        assert isinstance(right, list)


def test_parse_input_part2():
    lists = parse_input_part2(test_input)
    assert len(lists) == 18


def pairs_are_in_correct_order(left, right):
    if isinstance(left, int) and isinstance(right, int):
        if left < right:
            return True
        elif left > right:
            return False
        else:
            return None  # not decided yet

    elif isinstance(left, list) and isinstance(right, list):
        pass
    elif isinstance(left, int):
        left = [left]
    elif isinstance(right, int):
        right = [right]

    # Both are lists now
    min_len = min((len(left), len(right)))
    for idx in range(min_len):
        correct_order = pairs_are_in_correct_order(left[idx], right[idx])
        if correct_order is not None:
            return correct_order

    # ran out of items
    if len(left) == len(right):
        return None  # not decided yet
    elif len(left) < len(right):
        return True
    else:
        return False


def test_pairs_are_in_correct_order():
    pairs = parse_input(test_input)
    assert pairs_are_in_correct_order(pairs[0][0], pairs[0][1])
    assert pairs_are_in_correct_order(pairs[1][0], pairs[1][1])
    assert not pairs_are_in_correct_order(pairs[2][0], pairs[2][1])
    assert pairs_are_in_correct_order(pairs[3][0], pairs[3][1])
    assert not pairs_are_in_correct_order(pairs[4][0], pairs[4][1])
    assert pairs_are_in_correct_order(pairs[5][0], pairs[5][1])
    assert not pairs_are_in_correct_order(pairs[6][0], pairs[6][1])
    assert not pairs_are_in_correct_order(pairs[7][0], pairs[7][1])


def test_index_sum():
    pairs = parse_input(test_input)
    idx_sum = 0
    for idx, (left, right) in enumerate(pairs):
        if pairs_are_in_correct_order(left, right):
            idx_sum += idx+1

    assert idx_sum == 13


# needed for sorting
def compare_pairs(left, right):
    correct_order = pairs_are_in_correct_order(left, right)
    if correct_order is None:
        return 0  # equal
    elif pairs_are_in_correct_order(left, right):
        return -1
    else:
        return 1


def test_sorts_lists():
    lists = parse_input_part2(test_input)
    sorted_lists = sorted(lists, key=cmp_to_key(compare_pairs))

    idx_2 = None
    idx_6 = None
    for idx, l in enumerate(sorted_lists):
        if l == [[2]]:
            idx_2 = idx+1
        if l == [[6]]:
            idx_6 = idx+1

    assert idx_2*idx_6 == 140


def main():
    with open("input.txt", "r") as f:
        pairs = parse_input(f.read())

    idx_sum = 0
    for idx, (left, right) in enumerate(pairs):
        if pairs_are_in_correct_order(left, right):
            idx_sum += idx+1

    print(f"Total index: {idx_sum}")

    # part 2
    with open("input.txt", "r") as f:
        lists = parse_input_part2(f.read())

    sorted_lists = sorted(lists, key=cmp_to_key(compare_pairs))

    idx_2 = None
    idx_6 = None
    for idx, l in enumerate(sorted_lists):
        if l == [[2]]:
            idx_2 = idx+1
        if l == [[6]]:
            idx_6 = idx+1

    print(f"Decoder key: {idx_2*idx_6}")


if __name__ == "__main__":
    main()
