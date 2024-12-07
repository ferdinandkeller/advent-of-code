from loguru import logger
from typing import Literal
from dataclasses import dataclass


@dataclass
class Vec:
    x: int
    y: int

    def turn_cw(self) -> "Vec":
        return Vec(self.y, -self.x)

    def turn_counter_cw(self) -> "Vec":
        return Vec(-self.y, self.x)

    def __add__(self, other: "Vec") -> "Vec":
        return Vec(self.x + other.x, self.y + other.y)

    def __sub__(self, other: "Vec") -> "Vec":
        return Vec(self.x - other.x, self.y - other.y)

    def __neg__(self) -> "Vec":
        return Vec(-self.x, -self.y)


def parse_puzzle(
    puzzle: str,
) -> list[list[str]]:
    return [[*line] for line in puzzle.splitlines()][::-1]


# def parse_puzzle(
#     puzzle: str,
# ) -> list[list[str]]:
#     return [[*line] for line in puzzle.splitlines()]


# def find_start(puzzle: list[list[str]]) -> tuple[int, int]:
#     for y, line in enumerate(puzzle):
#         for x, c in enumerate(line):
#             if c == "^":
#                 puzzle[y][x] = "0"
#                 return y, x
#     raise ValueError("No start found")


# def next_pos(y: int, x: int, dir: int) -> tuple[int, int]:
#     # in order: up, right, down, left
#     match dir:
#         case 0:
#             return y - 1, x
#         case 1:
#             return y, x + 1
#         case 2:
#             return y + 1, x
#         case 3:
#             return y, x - 1
#         case _:
#             raise ValueError(f"Invalid direction: {dir}")


# def can_go_forward(
#     puzzle: list[list[str]], y: int, x: int, dir: int
# ) -> bool | Literal["leaves", "loop"]:
#     if not (0 <= y < len(puzzle) and 0 <= x < len(puzzle[0])):
#         return "leaves"
#     if puzzle[y][x] == str(dir):
#         return "loop"
#     return puzzle[y][x] != "#"


# def simulate(
#     puzzle: list[list[str]], y: int, x: int, dir: int
# ) -> Literal["leaves", "loop"]:
#     while True:
#         next_y, next_x = next_pos(y, x, dir)
#         match cgf := can_go_forward(puzzle, next_y, next_x, dir):
#             case "leaves" | "loop":
#                 return cgf
#             case True:
#                 y, x = next_y, next_x
#                 puzzle[y][x] = str(dir)
#             case False:
#                 dir = (dir + 1) % 4
#             case _:
#                 raise ValueError("Invalid return")


# def display_puzzle(puzzle: list[list[str]]):
#     for line in puzzle:
#         print("".join(line))


def display_puzzle(puzzle: list[list[str]]):
    for line in puzzle[::-1]:
        print("".join(line))


# def count_crosses(puzzle: list[list[str]]) -> int:
#     return sum(1 for line in puzzle for c in line if c != "." and c != "#")


# def clone_puzzle(puzzle: list[list[str]]) -> list[list[str]]:
#     return [line.copy() for line in puzzle]


# def part1(puzzle: str):
#     puzzle = parse_puzzle(puzzle)
#     y, x = find_start(puzzle)
#     simulate(puzzle, y, x, 0)
#     total_crosses = count_crosses(puzzle)
#     logger.success(f"Total crosses: {total_crosses}")


# def part2(puzzle: str):
#     puzzle = parse_puzzle(puzzle)
#     y, x = find_start(puzzle)
#     total_loops = 0
#     for r_y in range(len(puzzle)):
#         for r_x in range(len(puzzle[0])):
#             if puzzle[r_y][r_x] == "#" or puzzle[r_y][r_x] == "0":
#                 continue
#             puzzle_clone = clone_puzzle(puzzle)
#             puzzle_clone[r_y][r_x] = "#"
#             if "loop" == simulate(puzzle_clone, y, x, 0):
#                 total_loops += 1
#                 logger.debug(f"Loop at {r_y}, {r_x}")

#     logger.success(f"Total loops: {total_loops}")


# ========================================================================================================================
def find_start(puzzle: list[list[str]]) -> Vec:
    for y, line in enumerate(puzzle):
        for x, c in enumerate(line):
            if c == "^":
                puzzle[y][x] = "."
                return Vec(x, y)
    raise ValueError("No start found")


def part2(puzzle: str):
    puzzle = parse_puzzle(puzzle)
    pos = find_start(puzzle)
    dir = Vec(0, 1)
    dist = 0
    paths = [[set() for _ in range(len(puzzle[0]))] for _ in range(len(puzzle))]
    move(puzzle, paths, pos, dir, dist)
    display_paths(paths)


def display_paths(paths: list[list[set[int]]]):
    logger.info("start display path")
    for line in paths[::-1]:
        logger.debug(line)


def move(
    puzzle: list[list[str]],
    paths: list[list[set[int]]],
    pos: Vec,
    dir: Vec,
    dist: int,
    forward: bool = True,
) -> Literal["done", "colliding"]:
    if not is_valid_pos(puzzle, pos):
        return "done"
    if is_colliding(puzzle, pos):
        return "colliding"
    paths[pos.y][pos.x].add(dist)
    dist += 1 if forward else -1
    pos += dir if forward else -dir
    move(puzzle, paths, pos, dir, dist, forward)


def is_valid_pos(puzzle: list[list[str]], pos: Vec) -> bool:
    return 0 <= pos.y < len(puzzle) and 0 <= pos.x < len(puzzle[0])


def is_colliding(puzzle: list[list[str]], pos: Vec) -> bool:
    return puzzle[pos.y][pos.x] == "#"
