import numpy as np


def find_duplicate_item_type(items: str) -> str:
    left_comp = items[:len(items)//2]
    right_comp = items[len(items)//2:]

    duplicates = set(left_comp) & set(right_comp)
    if len(duplicates) != 1:
        raise ValueError

    return list(duplicates)[0]


def test_find_duplicate_item_type():
    assert find_duplicate_item_type("vJrwpWtwJgWrhcsFMMfFFhFp") == "p"
    assert find_duplicate_item_type("jqHRNqRjqzjGDLGLrsFMfFZSrLrFZsSL") == "L"
    assert find_duplicate_item_type("PmmdzqPrVvPwwTWBwg") == "P"
    assert find_duplicate_item_type("wMqvLMZHhHMvwLHjbvcjnnSBnvTQFn") == "v"
    assert find_duplicate_item_type("ttgJtRGJQctTZtZT") == "t"
    assert find_duplicate_item_type("CrZsJsPPZsGzwwsLwLmpwMDw") == "s"


def calc_priority(letter: str) -> int:
    lut = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
    return lut.index(letter)+1


def test_calc_priority():
    assert calc_priority("p") == 16
    assert calc_priority("L") == 38
    assert calc_priority("P") == 42
    assert calc_priority("v") == 22
    assert calc_priority("t") == 20
    assert calc_priority("s") == 19


def read_input(file_name: str) -> list:
    with open(file_name, "r") as f:
        lines = f.read().splitlines()
    return lines


# Part 1
input_list = read_input("input.txt")
priorities = [calc_priority(find_duplicate_item_type(items)) for items in input_list]
total_priority = np.sum(priorities)
print(f"Total priority: {total_priority}")


# Part 2
def find_badge(items_list: list) -> str:
    if len(items_list) != 3:
        raise ValueError

    duplicates = set(items_list[0]) & set(items_list[1]) & set(items_list[2])
    if len(duplicates) != 1:
        raise ValueError

    return list(duplicates)[0]


def test_find_badge():
    assert find_badge(["vJrwpWtwJgWrhcsFMMfFFhFp",
                       "jqHRNqRjqzjGDLGLrsFMfFZSrLrFZsSL",
                       "PmmdzqPrVvPwwTWBwg"]) == "r"
    assert find_badge(["wMqvLMZHhHMvwLHjbvcjnnSBnvTQFn",
                       "ttgJtRGJQctTZtZT",
                       "CrZsJsPPZsGzwwsLwLmpwMDw"]) == "Z"


def groups(lst, n):
    for i in range(0, len(lst), n):
        yield lst[i:i + n]


badge_priorities = [calc_priority(find_badge(group_items)) for group_items in groups(input_list, 3)]
print(f"Total badges priority: {np.sum(badge_priorities)}")
