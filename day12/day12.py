import numpy as np

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



class Graph:
    def __init__(self, grid: str):
        self.grid = np.asarray([[char for char in line] for line in grid.splitlines()])
        self.n_rows, self.n_cols = self.grid.shape

    def get_end(self) -> Point:
        indices = np.argwhere(self.grid == "E")[0]
        return Point(indices[0], indices[1])

    def get_start(self) -> Point:
        indices = np.argwhere(self.grid == "S")[0]
        return Point(indices[0], indices[1])

    def is_end(self, coordinates: Point) -> bool:
        return self.grid[coordinates.x, coordinates.y] == "E"

    def get_elevation(self, coordinates: Point) -> int:
        alphabet = "abcdefghijklmnopqrstuvwxyz"
        char = self.grid[coordinates.x, coordinates.y]
        if char == "S":
            return 0  # same as a
        if char == "E":
            return 25  # same as z

        return alphabet.find(char)

    def is_in_grid(self, coordinates: Point) -> bool:
        if coordinates.x < 0 or coordinates.x >= self.n_rows:
            return False
        if coordinates.y < 0 or coordinates.y >= self.n_cols:
            return False
        return True

    def get_neighbours(self, coordinates: Point) -> list[Point]:
        neighbours = []
        for direction in [Point(1, 0), Point(0, 1), Point(-1, 0), Point(0, -1)]:
            neighbour = coordinates+direction
            if self.is_in_grid(neighbour):
                neighbours.append(neighbour)

        return neighbours

    def get_reachable_neighbours(self, coordinates: Point) -> list[Point]:
        reachable_neighbours = []
        neighbours = self.get_neighbours(coordinates)
        elevation = self.get_elevation(coordinates)
        for neighbour in neighbours:
            if self.get_elevation(neighbour) <= elevation+1:
                reachable_neighbours.append(neighbour)

        return reachable_neighbours

    def get_reachable_neighbours_reverse(self, coordinates: Point) -> list[Point]:
        reachable_neighbours = []
        neighbours = self.get_neighbours(coordinates)
        elevation = self.get_elevation(coordinates)
        for neighbour in neighbours:
            if self.get_elevation(neighbour) >= elevation-1:
                reachable_neighbours.append(neighbour)

        return reachable_neighbours


test_grid = """Sabqponm
abcryxxl
accszExk
acctuvwj
abdefghi"""


def count_path_len(path: dict, end: Point) -> int:
    path_len = 0
    last = end
    while path[last] is not None:
        last = path[last]
        path_len += 1

    return path_len


def test_get_elevation():
    graph = Graph(test_grid)
    assert graph.get_elevation(Point(0, 0)) == 0  # S
    assert graph.get_elevation(Point(0, 1)) == 0  # a
    assert graph.get_elevation(Point(2, 5)) == 25  # E
    assert graph.get_elevation(Point(3, 3)) == 19  # t


def test_get_reachable_neighbours():
    graph = Graph(test_grid)
    assert graph.get_reachable_neighbours(Point(1, 2)) == [Point(2, 2), Point(0, 2), Point(1, 1)]


def test_get_end():
    graph = Graph(test_grid)
    assert graph.get_end() == Point(2, 5)


def test_path_finding():
    graph = Graph(test_grid)
    start = Point(0, 0)

    frontier = [start]
    came_from = {start: None}

    while len(frontier) > 0:
        current = frontier.pop(0)

        if graph.is_end(current):
            break

        for neighbour in graph.get_reachable_neighbours(current):
            if neighbour not in came_from:
                frontier.append(neighbour)
                came_from[neighbour] = current

    end = graph.get_end()
    assert count_path_len(came_from, end) == 31


def main():
    with open("input.txt", "r") as f:
        graph = Graph(f.read())

    start = graph.get_start()
    end = graph.get_end()

    frontier = [start]
    came_from = {start: None}

    while len(frontier) > 0:
        current = frontier.pop(0)

        if graph.is_end(current):
            break

        for neighbour in graph.get_reachable_neighbours(current):
            if neighbour not in came_from:
                frontier.append(neighbour)
                came_from[neighbour] = current

    end = graph.get_end()
    print(f"Path len: {count_path_len(came_from, end)}")

    # Path 2
    frontier = [end]
    came_from = {end: None}

    while len(frontier) > 0:
        current = frontier.pop(0)

        if graph.get_elevation(current) == 0:  # a
            start = current
            break

        for neighbour in graph.get_reachable_neighbours_reverse(current):
            if neighbour not in came_from:
                frontier.append(neighbour)
                came_from[neighbour] = current

    print(f"Path len part 2: {count_path_len(came_from, start)}")



if __name__ == "__main__":
    main()