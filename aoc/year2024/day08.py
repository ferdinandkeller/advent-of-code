from loguru import logger
from collections import defaultdict
from itertools import combinations


def parse_puzzle(puzzle: str) -> list[list[str]]:
    return [[*line] for line in puzzle.splitlines()]


def build_puzzle_map(puzzle: list[list[str]]) -> dict[str, list[tuple[int, int]]]:
    puzzle_map = defaultdict(list)
    for y, line in enumerate(puzzle):
        for x, node in enumerate(line):
            if node != ".":
                puzzle_map[node].append((x, y))
    return puzzle_map


def within_bounds(puzzle: list[list[str]], node: tuple[int, int]) -> bool:
    return 0 <= node[0] < len(puzzle[0]) and 0 <= node[1] < len(puzzle)


def get_antinodes_delta(
    node_1: tuple[int, int], node_2: tuple[int, int]
) -> tuple[int, int]:
    (x1, y1), (x2, y2) = node_1, node_2
    return (x2 - x1, y2 - y1)


def get_antinodes(
    puzzle: list[list[int]],
    node_1: tuple[int, int],
    node_2: tuple[int, int],
    line: bool = False,
) -> list[tuple[int, int]]:
    antinodes = []
    dx, dy = get_antinodes_delta(node_1, node_2)
    while True:
        node_2 = (node_2[0] + dx, node_2[1] + dy)
        if not within_bounds(puzzle, node_2):
            break
        antinodes.append(node_2)
        if not line:
            break
    while True:
        node_1 = (node_1[0] - dx, node_1[1] - dy)
        if not within_bounds(puzzle, node_1):
            break
        antinodes.append(node_1)
        if not line:
            break
    return antinodes


def part1(puzzle: str):
    puzzle = parse_puzzle(puzzle)
    puzzle_map = build_puzzle_map(puzzle)
    antinodes = set()
    for node in puzzle_map.keys():
        for node_1, node_2 in combinations(puzzle_map[node], 2):
            antinodes.update(
                get_antinodes(
                    puzzle,
                    node_1,
                    node_2,
                    line=False,
                )
            )
    logger.success(f"Antinodes: {len(antinodes)}")


def part2(puzzle: str):
    puzzle = parse_puzzle(puzzle)
    puzzle_map = build_puzzle_map(puzzle)
    antinodes = set()
    for node in puzzle_map.keys():
        antinodes.update(puzzle_map[node])
        for node_1, node_2 in combinations(puzzle_map[node], 2):
            antinodes.update(
                get_antinodes(
                    puzzle,
                    node_1,
                    node_2,
                    line=True,
                )
            )
    logger.success(f"Antinodes: {len(antinodes)}")
