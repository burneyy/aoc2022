import numpy as np


def read_input(file_name: str) -> list:
    with open(file_name, "r") as f:
        lines = f.read().splitlines()
    return lines


def is_overlapping(input: str, completely: bool = True) -> bool:
    ranges_raw = input.split(",")
    ranges = [range(int(r.split("-")[0]), int(r.split("-")[1])+1) for r in ranges_raw]
    sets = [ set(r) for r in ranges ]
    intersect = sets[0] & sets[1]
    if not completely:
        return len(intersect) > 0
    else:
        for s in sets:
            if s == intersect:
                return True

        return False


def test_is_overlapping():
    assert not is_overlapping("2-4,6-8")
    assert not is_overlapping("2-3,4-5")
    assert not is_overlapping("5-7,7-9")
    assert is_overlapping("2-8,3-7")
    assert is_overlapping("6-6,4-6")
    assert not is_overlapping("2-6,4-8")


def test_is_overlapping_party():
    assert not is_overlapping("2-4,6-8", False)
    assert not is_overlapping("2-3,4-5", False)
    assert is_overlapping("5-7,7-9", False)
    assert is_overlapping("2-8,3-7", False)
    assert is_overlapping("6-6,4-6", False)
    assert is_overlapping("2-6,4-8", False)


# Part 1
input_list = read_input("input.txt")
overlap_list = [is_overlapping(i, True) for i in input_list]
print(f"Overlapping completely: {np.sum(overlap_list)}")

# Part 2
overlap_list_partly = [is_overlapping(i, False) for i in input_list]
print(f"Overlapping partly: {np.sum(overlap_list_partly)}")
