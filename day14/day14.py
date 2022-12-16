import numpy as np


class Grid:
    def __init__(self, n_rows, n_cols, offset_row=0, offset_col=0):
        self.grid = [["." for c in range(n_cols)] for r in range(n_rows)]
        self.shape = (n_rows, n_cols)
        self.offset = (offset_row, offset_col)
        self.source = (0, 500)
        self._add_char(0, 500, "+")
        self.max_rock_row = 0

    def __str__(self):
        out = ""
        for line_no, line in enumerate(self.grid):
            out += f"{self.offset[0]+line_no} {''.join(line)}\n"

        return out.rstrip()

    def _add_char(self, row, col, char):
        row -= self.offset[0]
        col -= self.offset[1]
        self.grid[row][col] = char

    def add_rock(self, row, col):
        self._add_char(row, col, "#")
        if row > self.max_rock_row:
            self.max_rock_row = row

    def add_rock_line(self, line_str):
        coords = line_str.split(" -> ")
        for start, stop in [(coords[i], coords[i+1]) for i in range(len(coords)-1)]:
            start_col, start_row = [int(s) for s in start.split(",")]
            stop_col, stop_row = [int(s) for s in stop.split(",")]
            if start_col == stop_col:
                for row in range(min(start_row, stop_row), max(start_row, stop_row)+1):
                    self.add_rock(row, start_col)
            elif start_row == stop_row:
                for col in range(min(start_col, stop_col), max(start_col, stop_col)+1):
                    self.add_rock(start_row, col)

    def add_rock_line_bottom(self):
        self.grid[self.max_rock_row+2] = ["#" for c in range(self.shape[1])]

    def is_air(self, row, col):
        row -= self.offset[0]
        col -= self.offset[1]
        return self.grid[row][col] == "."

    def is_sand(self, row, col):
        row -= self.offset[0]
        col -= self.offset[1]
        return self.grid[row][col] == "o"

    def pour_sand(self):
        row, col = self.source
        min_row = self.offset[0]
        max_row = self.offset[0]+self.shape[0]-1
        min_col = self.offset[1]
        max_col = self.offset[1]+self.shape[1]-1
        while True:
            if row+1 > max_row:
                return None  # fall into the void

            if self.is_air(row+1, col):
                row += 1
            elif col-1 < min_col:
                return None  # fall into the void
            elif self.is_air(row+1, col-1):
                row += 1
                col -= 1
            elif col+1 > max_col:
                return None  # fall into the void
            elif self.is_air(row+1, col+1):
                row += 1
                col += 1
            else:
                self._add_char(row, col, "o")
                return row, col  # at rest


test_input = """498,4 -> 498,6 -> 496,6
503,4 -> 502,4 -> 502,9 -> 494,9"""


def parse_input(grid, input_str):
    for line in input_str.splitlines():
        grid.add_rock_line(line)

    return grid


def test_parse_input():
    grid = Grid(10, 10, 0, 494)
    grid = parse_input(grid, test_input)
    assert str(grid) == """0 ......+...
1 ..........
2 ..........
3 ..........
4 ....#...##
5 ....#...#.
6 ..###...#.
7 ........#.
8 ........#.
9 #########."""


def test_pour_sand():
    grid = Grid(10, 10, 0, 494)
    grid = parse_input(grid, test_input)
    grid.pour_sand()
    assert str(grid) == """0 ......+...
1 ..........
2 ..........
3 ..........
4 ....#...##
5 ....#...#.
6 ..###...#.
7 ........#.
8 ......o.#.
9 #########."""
    grid.pour_sand()
    grid.pour_sand()
    grid.pour_sand()
    grid.pour_sand()
    assert str(grid) == """0 ......+...
1 ..........
2 ..........
3 ..........
4 ....#...##
5 ....#...#.
6 ..###...#.
7 ......o.#.
8 ....oooo#.
9 #########."""


def test_units_of_sand():
    grid = Grid(10, 10, 0, 494)
    grid = parse_input(grid, test_input)
    n_units = 0
    while True:
        if grid.pour_sand() is not None:
            n_units += 1
        else:
            break

    assert n_units == 24


def test_part_two():
    grid = Grid(40, 40, 0, 480)
    grid = parse_input(grid, test_input)
    grid.add_rock_line_bottom()
    n_units = 0
    while True:
        if grid.pour_sand() is None:
            raise ValueError()
        n_units += 1
        if grid.is_sand(0, 500):
            break

    assert n_units == 93


def main():
    grid = Grid(200, 200, 0, 400)
    with open("input.txt", "r") as f:
        grid = parse_input(grid, f.read())
    n_units = 0
    while True:
        if grid.pour_sand() is not None:
            n_units += 1
        else:
            break

    print(n_units)

    # Part 2
    grid = Grid(200, 400, 0, 300)
    with open("input.txt", "r") as f:
        grid = parse_input(grid, f.read())
    grid.add_rock_line_bottom()
    n_units = 0
    while True:
        if grid.pour_sand() is None:
            raise ValueError()
        n_units += 1
        if grid.is_sand(0, 500):
            break

    print(n_units)

if __name__ == "__main__":
    main()