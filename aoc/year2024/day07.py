from loguru import logger


def parse_puzzle(puzzle: str) -> list[tuple[int, list[int]]]:
    out = []
    for line in puzzle.splitlines():
        total, numbers = line.split(": ")
        out.append((int(total), [int(n) for n in numbers.split(" ")]))
    return out


def computable(total: int, numbers: list[int]) -> bool:
    if len(numbers) == 0:
        return total == 0
    latest = numbers.pop()
    if total % latest == 0:
        if computable(total // latest, numbers.copy()):
            return True
    if total - latest >= 0:
        if computable(total - latest, numbers.copy()):
            return True
    return False


def computables(puzzle: list[tuple[int, list[int]]]) -> int:
    total_computable = 0
    for total, numbers in puzzle:
        if computable(total, numbers):
            total_computable += total
    return total_computable


def part1(puzzle: str):
    puzzle = parse_puzzle(puzzle)
    total_computable = computables(puzzle)
    logger.success(f"Total computable: {total_computable}")


def computable2(total: int, numbers: list[int]) -> bool:
    if len(numbers) == 0:
        return total == 0
    latest = numbers.pop()
    if total % latest == 0:
        if computable2(total // latest, numbers.copy()):
            return True
    if total - latest >= 0:
        if computable2(total - latest, numbers.copy()):
            return True
    if (total - latest) % 10 ** len(str(latest)) == 0:
        if computable2((total - latest) // 10 ** len(str(latest)), numbers.copy()):
            return True
    return False


def computables2(puzzle: list[tuple[int, list[int]]]) -> int:
    total_computable = 0
    for total, numbers in puzzle:
        if computable2(total, numbers):
            total_computable += total
    return total_computable


def part2(puzzle: str):
    puzzle = parse_puzzle(puzzle)
    total_computable = computables2(puzzle)
    logger.success(f"Total computable: {total_computable}")
