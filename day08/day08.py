import numpy as np

def parse_grid(grid: str):
    return np.asarray([ [char for char in line] for line in grid.splitlines()])


test_grid = parse_grid("""30373
25512
65332
33549
35390""")

def is_visible(grid, idx_row, idx_col):
    row = grid[idx_row,:]
    col = grid[:,idx_col]


    # Trees at the border are always visible!
    if idx_row == 0 or idx_row == len(row)-1:
        return True
    if idx_col == 0 or idx_col == len(col)-1:
        return True

    tree_height = grid[idx_row, idx_col]
    # Visible horizontally?
    for idx in range(idx_col+1, len(row)):  # to the right
        if row[idx] >= tree_height:
            break  # not visible
    else:
        return True
    for idx in range(idx_col-1, -1, -1):  # to the left
        if row[idx] >= tree_height:
            break  # not visible
    else:
        return True
    # Visible vertically?
    for idx in range(idx_row+1, len(col)):  # to the  bottom
        if col[idx] >= tree_height:
            break  # not visible
    else:
        return True
    for idx in range(idx_row-1, -1, -1):  # to the right
        if col[idx] >= tree_height:
            break  # not visible
    else:
        return True

    return False


def test_is_visible():
    assert is_visible(test_grid, 1, 1)  # top-left 5
    assert is_visible(test_grid, 1, 2)  # top-middle 5
    assert not is_visible(test_grid, 1, 3)  # top-right 1
    assert is_visible(test_grid, 2, 1)  # left-middle 5
    assert not is_visible(test_grid, 2, 2)  # center 3
    assert is_visible(test_grid, 2, 3)  # right-middle 3
    assert is_visible(test_grid, 3, 2)  # bottom-middle 5
    assert not is_visible(test_grid, 3, 1)  # bottom-left 3
    assert not is_visible(test_grid, 3, 3)  # bottom-right 4


def calc_scenic_score(grid, idx_row, idx_col):
    row = grid[idx_row,:]
    col = grid[:,idx_col]


    if idx_row == 0 or idx_row == len(row)-1:
        return 0
    if idx_col == 0 or idx_col == len(col)-1:
        return 0

    tree_height = grid[idx_row, idx_col]
    # Visible horizontally?
    scenic_score = 1
    steps = 0
    for idx in range(idx_col+1, len(row)):  # to the right
        steps += 1
        if row[idx] >= tree_height:
            break  # not visible
    scenic_score *= steps

    steps = 0
    for idx in range(idx_col-1, -1, -1):  # to the left
        steps += 1
        if row[idx] >= tree_height:
            break  # not visible

    scenic_score *= steps

    steps = 0
    for idx in range(idx_row+1, len(col)):  # to the  bottom
        steps += 1
        if col[idx] >= tree_height:
            break  # not visible

    scenic_score *= steps

    steps = 0
    for idx in range(idx_row-1, -1, -1):  # to the right
        steps += 1
        if col[idx] >= tree_height:
            break  # not visible
    scenic_score *= steps

    return scenic_score


def test_scenic_score():
    assert calc_scenic_score(test_grid, 1, 2) == 4  # top-middle 5
    assert calc_scenic_score(test_grid, 3, 2) == 8  # bottom-middle 5


if __name__ == "__main__":
    with open("input.txt", "r") as f:
        grid = parse_grid(f.read())

    n_rows, n_cols = grid.shape

    n_visible = 0
    for idx_row in range(n_rows):
        for idx_col in range(n_cols):
            if is_visible(grid, idx_row, idx_col):
                n_visible += 1

    print(f"Visible tree: {n_visible}")

    # Part 2
    max_score = 0
    for idx_row in range(n_rows):
        for idx_col in range(n_cols):
            score = calc_scenic_score(grid, idx_row, idx_col)
            if score > max_score:
                max_score = score

    print(f"Max scenic score: {max_score}")
