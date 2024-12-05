import re
from loguru import logger


def part1(puzzle: str):
    q = re.compile(r"mul\((\d+),(\d+)\)")
    total = sum([int(a) * int(b) for (a, b) in q.findall(puzzle)])
    logger.success(f"Total sum is {total}")


def part2(puzzle: str):
    q = re.compile(r"mul\((\d+),(\d+)\)")
    q_sections = re.compile(r"(do\(\)|don't\(\))")
    enabled = True
    total = 0
    for section in re.split(q_sections, puzzle):
        if section == "do()":
            enabled = True
        elif section == "don't()":
            enabled = False
        else:
            if enabled:
                total += sum([int(a) * int(b) for (a, b) in q.findall(section)])
    logger.success(f"Total sum is {total}")
