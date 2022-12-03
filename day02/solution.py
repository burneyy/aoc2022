import numpy as np


class RockPaperScissors:
    def __init__(self, shape: str):
        if shape == "A" or shape == "X":
            self.shape = "rock"
            self.value = 1
        elif shape == "B" or shape == "Y":
            self.shape = "paper"
            self.value = 2
        elif shape == "C" or shape == "Z":
            self.shape = "scissors"
            self.value = 3

    @classmethod
    def create_from_condition(cls, other, condition):
        if condition == "X":  # lose
            result = 2
        elif condition == "Y":  # draw
            result = 0
        elif condition == "Z":  # win
            result = 1
        else:
            raise ValueError()

        value = (other.get_value()-1+result) % 3

        return cls("ABC"[value])

    def get_shape(self):
        return self.shape

    def get_value(self):
        return self.value

    def get_score_against(self, other):
        result = (self.value - other.get_value()) % 3
        if result == 0:
            return 3  # draw
        elif result == 1:
            return 6  # win
        elif result == 2:
            return 0  # lose


# Part 1
def read_strategy_from_file(file_name: str) -> list:
    with open(file_name, "r") as f:
        lines = f.read().splitlines()

    return lines


def calculate_round_score(strategy: str, part_two: bool = False) -> int:
    opp_enc, you_enc = strategy.split(" ")
    opp = RockPaperScissors(opp_enc)
    if part_two:
        you = RockPaperScissors.create_from_condition(opp, you_enc)
    else:
        you = RockPaperScissors(you_enc)

    return you.get_value() + you.get_score_against(opp)


def test_calculate_round_score_part_one():
    assert calculate_round_score("A Y") == 8
    assert calculate_round_score("B X") == 1
    assert calculate_round_score("C Z") == 6


def test_calculate_round_score_part_two():
    assert calculate_round_score("A Y", part_two=True) == 4
    assert calculate_round_score("B X", part_two=True) == 1
    assert calculate_round_score("C Z", part_two=True) == 7


def calculate_total_score(strategy_list, part_two=False):
    scores = [calculate_round_score(strategy, part_two) for strategy in strategy_list]
    return np.sum(scores)


def test_calculate_total_score():
    test_list = ["A Y", "B X", "C Z"]
    assert calculate_total_score(test_list) == 15


def test_calculate_total_score_part_two():
    test_list = ["A Y", "B X", "C Z"]
    assert calculate_total_score(test_list, part_two=True) == 12


input_list = read_strategy_from_file("input.txt")
print(f"Expected total score (part 1): {calculate_total_score(input_list)}")


# Part 2
print(f"Expected total score (part 2): {calculate_total_score(input_list, True)}")
