from loguru import logger


def parse_puzzle(puzzle: str) -> list[tuple[int, list[int]]]:
    out = []
    for line in puzzle.splitlines():
        total, numbers = line.split(": ")
        out.append((int(total), [int(n) for n in numbers.split(" ")]))
    return out


def adds_up_correctly(total: int, numbers: list[int]) -> bool:
    if len(numbers) == 0:
        return total == 0
    latest = numbers.pop()
    if total % latest == 0:
        if adds_up_correctly(total // latest, numbers.copy()):
            return True
    if total - latest >= 0:
        if adds_up_correctly(total - latest, numbers.copy()):
            return True
    return False


def solve_equations(puzzle: list[tuple[int, list[int]]]) -> int:
    total_calibration = 0
    for total, numbers in puzzle:
        if adds_up_correctly(total, numbers):
            total_calibration += total
    return total_calibration


def part1(puzzle: str):
    puzzle = parse_puzzle(puzzle)
    total_calibration = solve_equations(puzzle)
    logger.success(f"Total calibration: {total_calibration}")


def adds_up_correctly2(total: int, numbers: list[int]) -> bool:
    if len(numbers) == 0:
        return total == 0
    latest = numbers.pop()
    if total % latest == 0:
        if adds_up_correctly2(total // latest, numbers.copy()):
            return True
    if total - latest >= 0:
        if adds_up_correctly2(total - latest, numbers.copy()):
            return True
    if (total - latest) % 10 ** len(str(latest)) == 0:
        if adds_up_correctly2(
            (total - latest) // 10 ** len(str(latest)), numbers.copy()
        ):
            return True
    return False


def solve_equations2(puzzle: list[tuple[int, list[int]]]) -> int:
    total_calibration = 0
    for total, numbers in puzzle:
        if adds_up_correctly2(total, numbers):
            total_calibration += total
    return total_calibration


def part2(puzzle: str):
    puzzle = parse_puzzle(puzzle)
    total_calibration = solve_equations2(puzzle)
    logger.success(f"Total calibration: {total_calibration}")
