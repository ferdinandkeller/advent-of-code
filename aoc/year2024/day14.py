from loguru import logger
import re

WIDTH = 101
HEIGHT = 103


def parse_puzzle(puzzle: str) -> list[tuple[int, int, int, int]]:
    q = re.compile(r"p=(\d+),(\d+) v=(\-?\d+),(\-?\d+)")
    return [list(map(int, q.match(line).groups())) for line in puzzle.split("\n")]


def move(pos: int, velocity: int, steps: int, size: int) -> int:
    return (pos + velocity * steps) % size


def step_puzzle(
    puzzle: list[tuple[int, int, int, int]],
    width: int,
    height: int,
    steps: int,
) -> list[tuple[int, int, int, int]]:
    new_puzzle = []
    for x, y, vx, vy in puzzle:
        new_x = move(x, vx, steps, width)
        new_y = move(y, vy, steps, height)
        new_puzzle.append((new_x, new_y, vx, vy))
    return new_puzzle


def get_safety_factor(
    puzzle: list[tuple[int, int, int, int]],
    width: int,
    height: int,
    steps: int = 100,
) -> int:
    x_center = width // 2
    y_center = height // 2
    quarters = [0, 0, 0, 0]
    for x, y, _, _ in step_puzzle(puzzle, width, height, steps):
        if x < x_center:
            if y < y_center:
                quarters[0] += 1
            elif y_center < y:
                quarters[1] += 1
        elif x_center < x:
            if y < y_center:
                quarters[2] += 1
            elif y_center < y:
                quarters[3] += 1
    return quarters[0] * quarters[1] * quarters[2] * quarters[3]


def find_tree(
    puzzle: list[tuple[int, int, int, int]],
    width: int,
    height: int,
) -> int | None:
    for steps in range(1, 10_000):
        puzzle = step_puzzle(puzzle, width, height, steps=1)
        pos_x = [x for x, _, _, _ in puzzle]
        pos_y = [y for _, y, _, _ in puzzle]
        average_x = sum(pos_x) // len(pos_x)
        average_y = sum(pos_y) // len(pos_y)
        x_stddev = sum((x - average_x) ** 2 for x in pos_x) // len(pos_x)
        y_stddev = sum((y - average_y) ** 2 for y in pos_y) // len(pos_y)
        if x_stddev < 500 and y_stddev < 500:
            return steps
    return None


def display(
    puzzle: list[tuple[int, int, int, int]],
    width: int,
    height: int,
) -> str:
    panel = [["  " for _ in range(width)] for _ in range(height)]
    for x, y, _, _ in puzzle:
        panel[y][x] = "##"
    out = ""
    for row in panel:
        out += "".join(row) + "\n"
    print(out)


def part1(puzzle: str):
    puzzle = parse_puzzle(puzzle)
    safety_factor = get_safety_factor(puzzle, width=WIDTH, height=HEIGHT)
    logger.success(f"Safety factor value: {safety_factor}")


def part2(puzzle: str):
    puzzle = parse_puzzle(puzzle)
    tree_steps = find_tree(puzzle, width=WIDTH, height=HEIGHT)
    if tree_steps is None:
        logger.error("Tree not found. Maybe adjust the number of steps.")
        return
    else:
        puzzle = step_puzzle(puzzle, width=WIDTH, height=HEIGHT, steps=tree_steps)
        display(puzzle, width=WIDTH, height=HEIGHT)
        logger.success(f"Tree found after {tree_steps} steps")
