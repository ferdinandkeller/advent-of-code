import re
from loguru import logger
from itertools import pairwise


def report_valid(report: list[int]) -> bool:
    go_up: bool | None = None
    for a, b in pairwise(report):
        dist = abs(b - a)
        direction = b > a
        if not (1 <= dist <= 3):
            return False
        if go_up is None:
            go_up = direction
        elif go_up != direction:
            return False
    return True


def part1(puzzle: str):
    q = re.compile(r"\d+")

    counter = 0
    for line in puzzle.splitlines():
        numbers = [int(n) for n in q.findall(line)]
        counter += report_valid(numbers)

    logger.success(f"Valid reports counter: {counter}")


def parallel_report_valid(report: list[int]) -> bool:
    for i in range(len(report)):
        new_report = report[:i] + report[i + 1 :]
        if report_valid(new_report):
            return True
    return False


def part2(puzzle: str):
    q = re.compile(r"\d+")

    counter = 0
    for line in puzzle.splitlines():
        numbers = [int(n) for n in q.findall(line)]
        counter += parallel_report_valid(numbers)

    logger.success(f"Valid parallel reports counter: {counter}")
