from math import sqrt


class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __repr__(self):
        return f'Point({self.x}, {self.y})'

    def __eq__(self, other):
        if isinstance(other, Point):
            return self.x == other.x and self.y == other.y
        return False

    def __hash__(self):
        return hash((self.x, self.y))

    def __sub__(self, other):
        return Point(self.x - other.x, self.y - other.y)

    def __add__(self, other):
        return Point(self.x + other.x, self.y + other.y)

    def __abs__(self):
        return sqrt(self.x**2 + self.y**2)


class Knot:
    def __init__(self, start_point: Point):
        self.location = start_point
        self.visited_locations = {start_point}

    def move(self, direction: str, distance: int):
        if direction == 'U':
            self.location += Point(0, distance)
        elif direction == 'D':
            self.location += Point(0, -distance)
        elif direction == 'L':
            self.location += Point(-distance, 0)
        elif direction == 'R':
            self.location += Point(distance, 0)
        else:
            raise ValueError(f'Unknown direction {direction}')

        self.visited_locations.add(self.location)

    def follow(self, other):
        diff = other.location - self.location
        if abs(diff) < 2:
            return
        else:
            if diff.x > 1:
                diff.x = 1
            elif diff.x < -1:
                diff.x = -1
            if diff.y > 1:
                diff.y = 1
            elif diff.y < -1:
                diff.y = -1

            self.location += diff

            self.visited_locations.add(self.location)


def parse_instructions(instructions):
    for instruction in instructions:
        direction, distance = instruction.split(" ")
        for _ in range(int(distance)):
            yield direction


test_instructions = """R 4
U 4
L 3
D 1
R 4
D 1
L 5
R 2"""


def test_follow():
    head = Knot(Point(0, 0))
    tail = Knot(Point(0, 0))
    for direction in parse_instructions(test_instructions.splitlines()):
        head.move(direction, 1)
        tail.follow(head)

    assert head.location == Point(2, 2)
    assert tail.location == Point(1, 2)
    assert len(tail.visited_locations) == 13


def test_follow_multiple():
    knots = [Knot(Point(0, 0)) for _ in range(10)]
    for direction in parse_instructions(test_instructions.splitlines()):
        knots[0].move(direction, 1)
        for i in range(1, len(knots)):
            knots[i].follow(knots[i-1])

    assert len(knots[9].visited_locations) == 1


test_instructions_part2 = """R 5
U 8
L 8
D 3
R 17
D 10
L 25
U 20"""


def test_follow_multiple_part2():
    knots = [Knot(Point(0, 0)) for _ in range(10)]
    for direction in parse_instructions(test_instructions_part2.splitlines()):
        knots[0].move(direction, 1)
        for i in range(1, len(knots)):
            knots[i].follow(knots[i-1])

    assert len(knots[9].visited_locations) == 36


def main():
    head = Knot(Point(0, 0))
    tail = Knot(Point(0, 0))

    with open("input.txt") as f:
        for line in f:
            for direction in parse_instructions(line.splitlines()):
                head.move(direction, 1)
                tail.follow(head)

    print(f"Part 1: {len(tail.visited_locations)} visited tail locations")

    knots = [Knot(Point(0, 0)) for _ in range(10)]
    with open("input.txt") as f:
        for line in f:
            for direction in parse_instructions(line.splitlines()):
                knots[0].move(direction, 1)
                for i in range(1, 10):
                    knots[i].follow(knots[i-1])

    print(f"Part 2: {len(knots[9].visited_locations)} visited tail locations")


if __name__ == "__main__":
    main()
