import yaml


class Monkey:
    def __init__(self, properties: dict, all_monkeys: list):
        self.items = [int(item) for item in str(properties["Starting items"]).split(", ")]
        self.operation = eval(properties["Operation"].replace("new = ", "lambda old: "))
        self.divisible_by = int(properties["Test"]["Condition"].replace("divisible by ", ""))
        self.target_monkey_true = int(properties["Test"]["If true"].replace("throw to monkey ", ""))
        self.target_monkey_false = int(properties["Test"]["If false"].replace("throw to monkey ", ""))
        self.monkey_list = all_monkeys
        self.n_inspected_items = 0
        self.common_divisor = None

    def set_common_divisor(self, divisor: int):
        self.common_divisor = divisor

    def add_item(self, item: int):
        self.items.append(item)

    def get_n_inspected_items(self):
        return self.n_inspected_items

    def throw_items(self, worried=False):
        for item in self.items:
            worry_level = self.operation(item)
            if not worried:
                worry_level //= 3
            if self.common_divisor is not None:
                worry_level %= self.common_divisor

            if worry_level % self.divisible_by == 0:
                self.monkey_list[self.target_monkey_true].add_item(worry_level)
            else:
                self.monkey_list[self.target_monkey_false].add_item(worry_level)
            self.n_inspected_items += 1

        self.items.clear()  # all items thrown


def calc_monkey_business(monkeys: list) -> int:
    n_inspected_items_list = sorted([m.get_n_inspected_items() for m in monkeys])
    return n_inspected_items_list[-1]*n_inspected_items_list[-2]


def calc_common_divisor(monkeys: list) -> int:
    common_divisor = 1
    for m in monkeys:
        common_divisor *= m.divisible_by

    return common_divisor

item_distribution_test = """Monkey 0:
  Starting items: 79, 98
  Operation: new = old * 19
  Test: 
    Condition: divisible by 23
    If true: throw to monkey 2
    If false: throw to monkey 3

Monkey 1:
  Starting items: 54, 65, 75, 74
  Operation: new = old + 6
  Test: 
    Condition: divisible by 19
    If true: throw to monkey 2
    If false: throw to monkey 0

Monkey 2:
  Starting items: 79, 60, 97
  Operation: new = old * old
  Test: 
    Condition: divisible by 13
    If true: throw to monkey 1
    If false: throw to monkey 3

Monkey 3:
  Starting items: 74
  Operation: new = old + 3
  Test: 
    Condition: divisible by 17
    If true: throw to monkey 0
    If false: throw to monkey 1"""


def test_item_distribution():
    monkey_list = []
    item_distribution_yaml = yaml.safe_load(item_distribution_test)
    n_monkeys = len(item_distribution_yaml)
    # Create monkeys
    for m in range(n_monkeys):
        monkey_list.append(Monkey(item_distribution_yaml[f"Monkey {m}"], monkey_list))

    # First round
    for throw_round in range(1, 21):
        for m in range(n_monkeys):
            monkey_list[m].throw_items()

        if throw_round == 1:
            assert monkey_list[0].items == [20, 23, 27, 26]
            assert monkey_list[1].items == [2080, 25, 167, 207, 401, 1046]
            assert monkey_list[2].items == []
            assert monkey_list[3].items == []

        if throw_round == 5:
            assert monkey_list[0].items == [15, 17, 16, 88, 1037]
            assert monkey_list[1].items == [20, 110, 205, 524, 72]
            assert monkey_list[2].items == []
            assert monkey_list[3].items == []

        if throw_round == 10:
            assert monkey_list[0].items == [91, 16, 20, 98]
            assert monkey_list[1].items == [481, 245, 22, 26, 1092, 30]
            assert monkey_list[2].items == []
            assert monkey_list[3].items == []

        if throw_round == 15:
            assert monkey_list[0].items == [83, 44, 8, 184, 9, 20, 26, 102]
            assert monkey_list[1].items == [110, 36]
            assert monkey_list[2].items == []
            assert monkey_list[3].items == []

        if throw_round == 20:
            assert monkey_list[0].items == [10, 12, 14, 26, 34]
            assert monkey_list[1].items == [245, 93, 53, 199, 115]
            assert monkey_list[2].items == []
            assert monkey_list[3].items == []


def test_inspected_items():
    monkey_list = []
    item_distribution_yaml = yaml.safe_load(item_distribution_test)
    n_monkeys = len(item_distribution_yaml)
    # Create monkeys
    for m in range(n_monkeys):
        monkey_list.append(Monkey(item_distribution_yaml[f"Monkey {m}"], monkey_list))

    for throw_round in range(1, 21):
        for m in range(n_monkeys):
            monkey_list[m].throw_items()

    assert monkey_list[0].get_n_inspected_items() == 101
    assert monkey_list[1].get_n_inspected_items() == 95
    assert monkey_list[2].get_n_inspected_items() == 7
    assert monkey_list[3].get_n_inspected_items() == 105

    assert calc_monkey_business(monkey_list) == 101*105


def test_inspected_items_worried():
    monkey_list = []
    item_distribution_yaml = yaml.safe_load(item_distribution_test)
    n_monkeys = len(item_distribution_yaml)
    # Create monkeys
    for m in range(n_monkeys):
        monkey_list.append(Monkey(item_distribution_yaml[f"Monkey {m}"], monkey_list))

    common_divisor = calc_common_divisor(monkey_list)
    for m in range(n_monkeys):
        monkey_list[m].set_common_divisor(common_divisor)

    for throw_round in range(10000):
        for m in range(n_monkeys):
            monkey_list[m].throw_items(worried=True)

    assert monkey_list[0].get_n_inspected_items() == 52166
    assert monkey_list[1].get_n_inspected_items() == 47830
    assert monkey_list[2].get_n_inspected_items() == 1938
    assert monkey_list[3].get_n_inspected_items() == 52013

    assert calc_monkey_business(monkey_list) == 52166*52013

def main():
    with open("input.txt", "r") as f:
        item_distribution_yaml = yaml.safe_load(f)

    monkey_list = []
    n_monkeys = len(item_distribution_yaml)
    # Create monkeys
    for m in range(n_monkeys):
        monkey_list.append(Monkey(item_distribution_yaml[f"Monkey {m}"], monkey_list))

    for throw_round in range(20):
        for m in range(n_monkeys):
            monkey_list[m].throw_items(worried=False)

    print(f"Monkey business (not worried): {calc_monkey_business(monkey_list)}")

    # Part 2
    monkey_list = []
    n_monkeys = len(item_distribution_yaml)
    # Create monkeys
    for m in range(n_monkeys):
        monkey_list.append(Monkey(item_distribution_yaml[f"Monkey {m}"], monkey_list))

    common_divisor = calc_common_divisor(monkey_list)
    for m in range(n_monkeys):
        monkey_list[m].set_common_divisor(common_divisor)

    for throw_round in range(10000):
        for m in range(n_monkeys):
            monkey_list[m].throw_items(worried=True)

    print(f"Monkey business (worried): {calc_monkey_business(monkey_list)}")


if __name__ == "__main__":
    main()