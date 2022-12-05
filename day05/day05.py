class Stacks:
    def __init__(self, stack_arrangement: str):
        self.stacks = self.parse_arrangement(stack_arrangement)

    def parse_arrangement(self, stack_arrangement: str):
        rev_arr = stack_arrangement.split("\n")[::-1]
        n_stacks = len(rev_arr[0].split("   "))
        stacks = [[] for i in range(n_stacks)]
        for line in rev_arr[1:]:
            for idx in range(n_stacks):
                if line[1+idx*4] != " ":
                    stacks[idx].append(line[1+idx*4])

        return stacks

    def get_n_stacks(self):
        return len(self.stacks)

    def get_stack(self, no: int):
        return self.stacks[no-1]

    def get_stacks(self):
        return self.stacks

    def append(self, stack_no: int, item: str):
        self.stacks[stack_no-1].append(item)

    def pop(self, stack_no: int, index: int = -1):
        return self.stacks[stack_no-1].pop(index)

    def get_top_items(self):
        top_items = ""
        for stack in self.stacks:
            length = len(stack)
            if length > 0:
                top_items += stack[length-1]

        return top_items

    def perform_move_operation(self, operation: str, keep_order: bool = False):
        op = operation.replace("move ", "").replace(" from ", ",").replace(" to ", ",").split(",")
        amount = int(op[0])
        from_stack = int(op[1])
        to_stack = int(op[2])

        for idx in range(amount*(-1), 0, 1):
            if keep_order:
                self.append(to_stack, self.pop(from_stack, idx))
            else:
                self.append(to_stack, self.pop(from_stack))



test_arrangement = """    [D]    
[N] [C]    
[Z] [M] [P]
 1   2   3 """


def test_stacks_creation():
    stacks = Stacks(test_arrangement)
    assert stacks.get_n_stacks() == 3
    assert stacks.get_stack(1) == ["Z", "N"]
    assert stacks.get_stack(2) == ["M", "C", "D"]
    assert stacks.get_stack(3) == ["P"]


def test_stacks_movement():
    stacks = Stacks(test_arrangement)

    stacks.perform_move_operation("move 1 from 2 to 1")
    assert stacks.get_stack(1) == ["Z", "N", "D"]
    assert stacks.get_stack(2) == ["M", "C"]
    assert stacks.get_stack(3) == ["P"]

    stacks.perform_move_operation("move 3 from 1 to 3")
    assert stacks.get_stack(1) == []
    assert stacks.get_stack(2) == ["M", "C"]
    assert stacks.get_stack(3) == ["P", "D", "N", "Z"]

    stacks.perform_move_operation("move 2 from 2 to 1")
    assert stacks.get_stack(1) == ["C", "M"]
    assert stacks.get_stack(2) == []
    assert stacks.get_stack(3) == ["P", "D", "N", "Z"]

    stacks.perform_move_operation("move 1 from 1 to 2")
    assert stacks.get_stack(1) == ["C"]
    assert stacks.get_stack(2) == ["M"]
    assert stacks.get_stack(3) == ["P", "D", "N", "Z"]

    assert stacks.get_top_items() == "CMZ"


def test_stacks_movement_with_order():
    stacks = Stacks(test_arrangement)

    stacks.perform_move_operation("move 1 from 2 to 1", keep_order=True)
    assert stacks.get_stack(1) == ["Z", "N", "D"]
    assert stacks.get_stack(2) == ["M", "C"]
    assert stacks.get_stack(3) == ["P"]

    stacks.perform_move_operation("move 3 from 1 to 3", keep_order=True)
    assert stacks.get_stack(1) == []
    assert stacks.get_stack(2) == ["M", "C"]
    assert stacks.get_stack(3) == ["P", "Z", "N", "D"]

    stacks.perform_move_operation("move 2 from 2 to 1", keep_order=True)
    assert stacks.get_stack(1) == ["M", "C"]
    assert stacks.get_stack(2) == []
    assert stacks.get_stack(3) == ["P", "Z", "N", "D"]

    stacks.perform_move_operation("move 1 from 1 to 2", keep_order=True)
    assert stacks.get_stack(1) == ["M"]
    assert stacks.get_stack(2) == ["C"]
    assert stacks.get_stack(3) == ["P", "Z", "N", "D"]

    assert stacks.get_top_items() == "MCD"


def read_input(file_name: str):
    with open(file_name, "r") as f:
        sections = f.read().split("\n\n")

    return sections[0], sections[1].splitlines()


# Part 1
stack_arrangement, move_operations = read_input("input.txt")
stacks = Stacks(stack_arrangement)
for operation in move_operations:
    stacks.perform_move_operation(operation)

print(f"Top crates: {stacks.get_top_items()}")

# Part 2
stacks = Stacks(stack_arrangement)
for operation in move_operations:
    stacks.perform_move_operation(operation, True)

print(f"Top crates with order: {stacks.get_top_items()}")
