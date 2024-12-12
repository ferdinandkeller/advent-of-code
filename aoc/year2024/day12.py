from loguru import logger
from collections import defaultdict


def parse_puzzle(puzzle: str) -> list[list[str]]:
    return [[*line] for line in puzzle.split("\n")]


def is_inside(puzzle: list[list[str]], x: int, y: int) -> bool:
    return 0 <= x < len(puzzle[0]) and 0 <= y < len(puzzle)


def get_adjacent(x: int, y: int) -> list[tuple[int, int]]:
    return [(x + dx, y + dy) for dx, dy in [(1, 0), (0, -1), (-1, 0), (0, 1)]]


def explore_zone(
    puzzle: list[list[str]],
    zone_map: list[list[int]],
    explored_cache: set[tuple[int, int]],
    x: int,
    y: int,
    zone_id: int,
):
    if (x, y) in explored_cache:
        return
    explored_cache.add((x, y))
    zone_map[y][x] = zone_id
    for a_x, a_y in get_adjacent(x, y):
        if is_inside(puzzle, a_x, a_y) and puzzle[a_y][a_x] == puzzle[y][x]:
            explore_zone(puzzle, zone_map, explored_cache, a_x, a_y, zone_id)


def build_zone_map(
    puzzle: list[list[str]],
):
    zone_map = [[0 for _ in range(len(puzzle[0]))] for _ in range(len(puzzle))]
    explored_cache = set()
    zone_id = 0
    for y in range(len(puzzle)):
        for x in range(len(puzzle[y])):
            if (x, y) not in explored_cache:
                explore_zone(puzzle, zone_map, explored_cache, x, y, zone_id)
                zone_id += 1
    return zone_map


def get_zone(zone_map: list[list[int]], x: int, y: int) -> int:
    if not is_inside(zone_map, x, y):
        return -1
    return zone_map[y][x]


def get_adjacent_zone(
    zone_map: list[list[int]], x: int, y: int
) -> list[tuple[int, int]]:
    return [get_zone(zone_map, a_x, a_y) for a_x, a_y in get_adjacent(x, y)]


def get_zones_area(zone_map: list[list[int]]) -> dict[int, int]:
    areas = defaultdict(int)
    for y in range(len(zone_map)):
        for x in range(len(zone_map[y])):
            areas[zone_map[y][x]] += 1
    return areas


def get_zone_perimeters(
    zone_map: list[list[int]],
) -> tuple[dict[int, int], dict[int, int]]:
    perimeters = defaultdict(int)
    for y in range(len(zone_map)):
        for x in range(len(zone_map[y])):
            for a_x, a_y in get_adjacent(x, y):
                if get_zone(zone_map, x, y) != get_zone(zone_map, a_x, a_y):
                    perimeters[zone_map[y][x]] += 1
    return perimeters


def get_corner_axis_score(current_zone_id: int, n1: int, n2: int) -> int:
    return not (n1 == current_zone_id) ^ (n2 == current_zone_id)


def is_square(zone_map: list[list[int]], current_zone_id: int, x: int, y: int) -> bool:
    return (
        get_zone(zone_map, x + 1, y) == current_zone_id
        and get_zone(zone_map, x, y + 1) == current_zone_id
        and get_zone(zone_map, x + 1, y + 1) == current_zone_id
    )


def get_corner_score(zone_map: list[list[int]], x: int, y: int) -> int:
    current_zone_id = zone_map[y][x]
    n1, n2, n3, n4 = get_adjacent_zone(zone_map, x, y)
    return (
        get_corner_axis_score(current_zone_id, n1, n2)
        + get_corner_axis_score(current_zone_id, n2, n3)
        + get_corner_axis_score(current_zone_id, n3, n4)
        + get_corner_axis_score(current_zone_id, n4, n1)
        - 4 * is_square(zone_map, current_zone_id, x, y)
    )


def get_zone_perimeters2(
    zone_map: list[list[int]],
) -> tuple[dict[int, int], dict[int, int]]:
    perimeters = defaultdict(int)
    for y in range(len(zone_map)):
        for x in range(len(zone_map[y])):
            perimeters[zone_map[y][x]] += get_corner_score(zone_map, x, y)
    return perimeters


def get_fencing_price(areas: dict[int, int], perimeters: dict[int, int]) -> int:
    fencing_price = 0
    for key in areas.keys():
        fencing_price += areas[key] * perimeters[key]
    return fencing_price


def part1(puzzle: str):
    puzzle = parse_puzzle(puzzle)
    zone_map = build_zone_map(puzzle)
    areas = get_zones_area(zone_map)
    perimeters = get_zone_perimeters(zone_map)
    fencing_price = get_fencing_price(areas, perimeters)
    logger.success(f"Fencing price: {fencing_price}")


def part2(puzzle: str):
    puzzle = parse_puzzle(puzzle)
    zone_map = build_zone_map(puzzle)
    areas = get_zones_area(zone_map)
    perimeters = get_zone_perimeters2(zone_map)
    fencing_price = get_fencing_price(areas, perimeters)
    logger.success(f"Fencing price: {fencing_price}")
