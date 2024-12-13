from loguru import logger
import re


def parse_puzzle(puzzle: str, target_delta: int = 0):
    q1 = re.compile(r"Button A: X\+(\d+), Y\+(\d+)")
    q2 = re.compile(r"Button B: X\+(\d+), Y\+(\d+)")
    q3 = re.compile(r"Prize: X=(\d+), Y=(\d+)")

    def parse_machine(
        machine: str,
    ) -> tuple[tuple[int, int], tuple[int, int], tuple[int, int]]:
        line1, line2, line3 = machine.split("\n")

        a_x, a_y = map(float, q1.match(line1).groups())
        b_x, b_y = map(float, q2.match(line2).groups())
        p_x, p_y = map(float, q3.match(line3).groups())

        return (a_x, a_y), (b_x, b_y), (p_x + target_delta, p_y + target_delta)

    return [parse_machine(machine) for machine in puzzle.split("\n\n")]


def token_cost(
    dir_a: tuple[int, int],
    dir_b: tuple[int, int],
    target: tuple[int, int],
) -> int:
    # inverse matrix
    det = dir_a[0] * dir_b[1] - dir_a[1] * dir_b[0]
    a_press_count = (target[0] * dir_b[1] - target[1] * dir_b[0]) / det
    b_press_count = (target[1] * dir_a[0] - target[0] * dir_a[1]) / det
    # check valid
    if a_press_count % 1 != 0 or b_press_count % 1 != 0:
        return 0
    return int(3 * a_press_count + b_press_count)


def part1(puzzle: str):
    puzzle = parse_puzzle(puzzle)
    tokens_cost = sum(token_cost(*machine) for machine in puzzle)
    logger.success(f"Tokens to win all prizes: {tokens_cost}")


def part2(puzzle: str):
    puzzle = parse_puzzle(puzzle, target_delta=10000000000000)
    tokens_cost = sum(token_cost(*machine) for machine in puzzle)
    logger.success(f"Tokens to win all prizes: {tokens_cost}")
