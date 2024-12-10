from loguru import logger


def parse_height(height: str) -> int:
    if height == ".":
        return -1
    else:
        return int(height)


def parse_puzzle(puzzle: str) -> list[list[int]]:
    return [[parse_height(c) for c in line] for line in puzzle.splitlines()]


def valid_position(puzzle: list[list[int]], x: int, y: int) -> bool:
    return 0 <= x < len(puzzle[0]) and 0 <= y < len(puzzle)


def create_scores(puzzle: list[list[int]]) -> list[list[set[int]]]:
    trailhead_index = 0
    scores = [[set() for _ in range(len(puzzle))] for _ in range(len(puzzle[0]))]
    for y in range(len(puzzle)):
        for x in range(len(puzzle[y])):
            if puzzle[y][x] == 0:
                scores[y][x].add(trailhead_index)
                trailhead_index += 1
    return scores


def propagate_score(
    puzzle: list[list[int]],
    scores: list[list[set[int]]],
    height_value: int,
    x: int,
    y: int,
):
    if puzzle[y][x] != height_value:
        return
    for dy, dx in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
        next_y = y + dy
        next_x = x + dx
        if not valid_position(puzzle, next_x, next_y):
            continue
        if puzzle[next_y][next_x] == height_value - 1:
            scores[y][x].update(scores[next_y][next_x])


def propagate_scores(
    puzzle: list[list[int]], scores: list[list[set[int]]], height_value: int
) -> list[list[int]]:
    for y in range(len(puzzle)):
        for x in range(len(puzzle[y])):
            propagate_score(puzzle, scores, height_value, x, y)


def compute_score(puzzle: list[list[int]], scores: list[list[set[int]]]) -> int:
    score = 0
    for y in range(len(puzzle)):
        for x in range(len(puzzle[y])):
            if puzzle[y][x] == 9:
                score += len(scores[y][x])
    return score


def part1(puzzle: str):
    puzzle = parse_puzzle(puzzle)
    scores = create_scores(puzzle)
    for height_value in range(1, 10):
        propagate_scores(puzzle, scores, height_value)
    score = compute_score(puzzle, scores)
    logger.success(f"Hiking score : {score}")


def create_scores2(puzzle: list[list[int]]) -> list[list[int]]:
    scores = [[0 for _ in range(len(puzzle))] for _ in range(len(puzzle[0]))]
    for y in range(len(puzzle)):
        for x in range(len(puzzle[y])):
            if puzzle[y][x] == 0:
                scores[y][x] = 1
    return scores


def propagate_score2(
    puzzle: list[list[int]],
    scores: list[list[int]],
    score_value: int,
    x: int,
    y: int,
):
    if puzzle[y][x] != score_value:
        return
    for dy, dx in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
        next_y = y + dy
        next_x = x + dx
        if not valid_position(puzzle, next_x, next_y):
            continue
        if puzzle[next_y][next_x] == score_value - 1:
            scores[y][x] += scores[next_y][next_x]


def propagate_scores2(
    puzzle: list[list[int]], scores: list[list[int]], score_value: int
) -> list[list[int]]:
    for y in range(len(puzzle)):
        for x in range(len(puzzle[y])):
            propagate_score2(puzzle, scores, score_value, x, y)


def compute_score2(puzzle: list[list[int]], scores: list[list[int]]) -> int:
    score = 0
    for y in range(len(puzzle)):
        for x in range(len(puzzle[y])):
            if puzzle[y][x] == 9:
                score += scores[y][x]
    return score


def part2(puzzle: str):
    puzzle = parse_puzzle(puzzle)
    scores = create_scores2(puzzle)
    for height_value in range(1, 10):
        propagate_scores2(puzzle, scores, height_value)
    score = compute_score2(puzzle, scores)
    logger.success(f"Hiking score : {score}")
