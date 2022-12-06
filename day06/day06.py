
def contains_duplicate(list_like_obj) -> bool:
    if len(list_like_obj) != len(set(list_like_obj)):
        return True
    return False


def find_lock_marker(buffer: str) -> int:
    for i in range(len(buffer)):
        if not contains_duplicate(buffer[i:i+4]):
            return i+4

    return -1


def find_message_marker(buffer: str) -> int:
    for i in range(len(buffer)):
        if not contains_duplicate(buffer[i:i+14]):
            return i+14

    return -1


def test_find_lock_marker():
    assert find_lock_marker("mjqjpqmgbljsphdztnvjfqwrcgsmlb") == 7
    assert find_lock_marker("bvwbjplbgvbhsrlpgdmjqwftvncz") == 5
    assert find_lock_marker("nppdvjthqldpwncqszvftbrmjlhg") == 6
    assert find_lock_marker("nznrnfrfntjfmvfwmzdfjlvtqnbhcprsg") == 10
    assert find_lock_marker("zcfzfwzzqfrljwzlrfnpqdbhtmscgvjw") == 11


def test_find_message_marker():
    assert find_message_marker("mjqjpqmgbljsphdztnvjfqwrcgsmlb") == 19
    assert find_message_marker("bvwbjplbgvbhsrlpgdmjqwftvncz") == 23
    assert find_message_marker("nppdvjthqldpwncqszvftbrmjlhg") == 23
    assert find_message_marker("nznrnfrfntjfmvfwmzdfjlvtqnbhcprsg") == 29
    assert find_message_marker("zcfzfwzzqfrljwzlrfnpqdbhtmscgvjw") == 26


# Part 1
with open("input.txt", "r") as f:
    buffer = f.read()

print(f"Lock marker at {find_lock_marker(buffer)}th character")
# Part 2
print(f"Message marker at {find_message_marker(buffer)}th character")
