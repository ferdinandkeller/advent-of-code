from loguru import logger
from functools import cache


def parse_puzzle(puzzle: str):
    return [int(n) for n in puzzle.split(" ")]


def update_number(number: int) -> list[int]:
    if number == 0:
        return [1]
    number_length = len(str(number))
    if number_length % 2 == 0:
        pow_10 = 10 ** (number_length // 2)
        return [number // pow_10, number % pow_10]
    return [number * 2024]


@cache  # use memoization to accelerate the process
def get_stones_count(value: int, N: int) -> int:
    if N == 0:
        return 1
    return sum(get_stones_count(v, N - 1) for v in update_number(value))


def get_sequence_stones_count(values: list[int], N: int) -> int:
    return sum(get_stones_count(v, N) for v in values)


def part1(puzzle: str):
    puzzle = parse_puzzle(puzzle)
    stones_count = get_sequence_stones_count(puzzle, 25)
    logger.success(f"Number of stones after 25 blinks is {stones_count}")


def part2(puzzle: str):
    puzzle = parse_puzzle(puzzle)
    stones_count = get_sequence_stones_count(puzzle, 75)
    logger.success(f"Number of stones after 75 blinks is {stones_count}")
