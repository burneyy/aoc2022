class Cpu:
    def __init__(self):
        self.register_X = 1
        self.operation_queue = []

    def get_x(self):
        return self.register_X

    def increment_x(self, value: int):
        self.register_X += value

    def is_idle(self):
        return len(self.operation_queue) == 0

    def add_operation(self, operation: str):
        if operation.startswith("addx"):
            self.operation_queue.append("noop")
            self.operation_queue.append(operation)
        elif operation == "noop":
            self.operation_queue.append(operation)
        else:
            raise ValueError(f"Invalid operation {operation}")

    def execute_next_operation(self):
        if self.is_idle():
            return

        operation = self.operation_queue.pop(0)
        if operation == "noop":
            pass
        elif operation.startswith("addx"):
            self.increment_x(int(operation.split(" ")[1]))
        else:
            raise ValueError(f"Invalid operation {operation}")


class Crt:
    def __init__(self, n_rows=6, n_cols=40):
        self.n_cols = n_cols
        self.n_rows = n_rows
        self.drawn_pixels = ["."]*(n_cols*n_rows)

    def draw(self, pixel, sprite):
        if sprite-1 <= pixel%self.n_cols <= sprite+1:
            self.drawn_pixels[pixel] = "#"
        else:
            self.drawn_pixels[pixel] = "."

    def __str__(self):
        s = "".join(self.drawn_pixels)
        return "\n".join(s[i:i+self.n_cols] for i in range(0, len(s), self.n_cols))



test_operations = """noop
addx 3
addx -5"""

def test_x():
    cpu = Cpu()
    for op in test_operations.splitlines():
        cpu.add_operation(op)

    cpu.execute_next_operation()  # cycle 1
    assert cpu.get_x() == 1
    cpu.execute_next_operation()  # cycle 2
    assert cpu.get_x() == 1
    cpu.execute_next_operation()  # cycle 3
    assert cpu.get_x() == 4
    cpu.execute_next_operation()  # cycle 4
    assert cpu.get_x() == 4
    cpu.execute_next_operation()  # cycle 5
    assert cpu.get_x() == -1

test_operations_long = """addx 15
addx -11
addx 6
addx -3
addx 5
addx -1
addx -8
addx 13
addx 4
noop
addx -1
addx 5
addx -1
addx 5
addx -1
addx 5
addx -1
addx 5
addx -1
addx -35
addx 1
addx 24
addx -19
addx 1
addx 16
addx -11
noop
noop
addx 21
addx -15
noop
noop
addx -3
addx 9
addx 1
addx -3
addx 8
addx 1
addx 5
noop
noop
noop
noop
noop
addx -36
noop
addx 1
addx 7
noop
noop
noop
addx 2
addx 6
noop
noop
noop
noop
noop
addx 1
noop
noop
addx 7
addx 1
noop
addx -13
addx 13
addx 7
noop
addx 1
addx -33
noop
noop
noop
addx 2
noop
noop
noop
addx 8
noop
addx -1
addx 2
addx 1
noop
addx 17
addx -9
addx 1
addx 1
addx -3
addx 11
noop
noop
addx 1
noop
addx 1
noop
noop
addx -13
addx -19
addx 1
addx 3
addx 26
addx -30
addx 12
addx -1
addx 3
addx 1
noop
noop
noop
addx -9
addx 18
addx 1
addx 2
noop
noop
addx 9
noop
noop
noop
addx -1
addx 2
addx -37
addx 1
addx 3
noop
addx 15
addx -21
addx 22
addx -6
addx 1
noop
addx 2
addx 1
noop
addx -10
noop
noop
addx 20
addx 1
addx 2
addx 2
addx -6
addx -11
noop
noop
noop"""


def test_signal_strengths():
    cpu = Cpu()
    for op in test_operations_long.splitlines():
        cpu.add_operation(op)

    signal_strength_tot = 0
    for cycle in range(1, 230):
        signal_strength = cycle * cpu.get_x()
        if cycle == 20:
            signal_strength_tot += signal_strength
            assert signal_strength == 420
        if cycle == 60:
            signal_strength_tot += signal_strength
            assert signal_strength == 1140
        if cycle == 100:
            signal_strength_tot += signal_strength
            assert signal_strength == 1800
        if cycle == 140:
            signal_strength_tot += signal_strength
            assert signal_strength == 2940
        if cycle == 180:
            signal_strength_tot += signal_strength
            assert signal_strength == 2880
        if cycle == 220:
            signal_strength_tot += signal_strength
            assert signal_strength == 3960

        cpu.execute_next_operation()

    assert signal_strength_tot == 13140


def test_drawing():
    cpu = Cpu()
    for op in test_operations_long.splitlines():
        cpu.add_operation(op)

    crt = Crt()
    for cycle in range(1, 241):
        crt.draw(cycle-1, cpu.get_x())
        cpu.execute_next_operation()

    assert str(crt) == """##..##..##..##..##..##..##..##..##..##..
###...###...###...###...###...###...###.
####....####....####....####....####....
#####.....#####.....#####.....#####.....
######......######......######......####
#######.......#######.......#######....."""


def main():
    cpu = Cpu()
    for line in open("input.txt", "r"):
        cpu.add_operation(line.rstrip())

    signal_strength_tot = 0
    for cycle in range(1, 230):
        signal_strength = cycle * cpu.get_x()
        if cycle == 20:
            signal_strength_tot += signal_strength
        if cycle == 60:
            signal_strength_tot += signal_strength
        if cycle == 100:
            signal_strength_tot += signal_strength
        if cycle == 140:
            signal_strength_tot += signal_strength
        if cycle == 180:
            signal_strength_tot += signal_strength
        if cycle == 220:
            signal_strength_tot += signal_strength

        cpu.execute_next_operation()

    print(f"Total signal strength: {signal_strength_tot}")


    # Part 2
    cpu = Cpu()
    for line in open("input.txt", "r"):
        cpu.add_operation(line.rstrip())

    crt = Crt()
    for cycle in range(1, 241):
        crt.draw(cycle-1, cpu.get_x())
        cpu.execute_next_operation()

    print("Part 2")
    print(str(crt))

if __name__ == "__main__":
    main()