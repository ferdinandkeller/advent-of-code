from loguru import logger


def detect_xmas_dir(
    table: list[str], w: int, h: int, x: int, y: int, x_dir: int, y_dir: int
) -> bool:
    for dist, letter in [(1, "M"), (2, "A"), (3, "S")]:
        new_y = y + y_dir * dist
        new_x = x + x_dir * dist
        if not (0 <= new_y < h and 0 <= new_x < w):
            return False
        if table[new_y][new_x] != letter:
            return False
    return True


def count_xmas_360(table: list[str], w: int, h: int, x: int, y: int) -> int:
    total = 0
    for y_dir in [-1, 0, 1]:
        for x_dir in [-1, 0, 1]:
            total += detect_xmas_dir(table, w, h, x, y, x_dir, y_dir)
    return total


def count_xmas(table: list[str], w: int, h: int) -> int:
    total = 0
    for y in range(h):
        for x in range(w):
            if table[y][x] == "X":
                total += count_xmas_360(table, w, h, x, y)
    return total


def part1(puzzle: str):
    table = [line for line in puzzle.splitlines()]
    total_xmas = count_xmas(table, len(table[0]), len(table))
    logger.success(f"Total XMAS: {total_xmas}")


def detect_cross_mas(table: list[str], w: int, h: int, x: int, y: int) -> bool:
    tl_br = table[y - 1][x - 1] == "M" and table[y + 1][x + 1] == "S"
    br_tl = table[y + 1][x + 1] == "M" and table[y - 1][x - 1] == "S"
    tr_bl = table[y - 1][x + 1] == "M" and table[y + 1][x - 1] == "S"
    bl_tr = table[y + 1][x - 1] == "M" and table[y - 1][x + 1] == "S"
    return (tl_br or br_tl) and (tr_bl or bl_tr)


def count_cross_mas(table: list[str], w: int, h: int) -> int:
    total = 0
    for y in range(1, h - 1):
        for x in range(1, w - 1):
            if table[y][x] == "A":
                total += detect_cross_mas(table, w, h, x, y)
    return total


def part2(puzzle: str):
    table = [line for line in puzzle.splitlines()]
    total_cross_mas = count_cross_mas(table, len(table[0]), len(table))
    logger.success(f"Total X-MAS: {total_cross_mas}")
