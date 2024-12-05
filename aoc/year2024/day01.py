import re
from loguru import logger


def part1(puzzle: str):
    q = re.compile(r"(\d+) +(\d+)")

    left_list = []
    right_list = []

    for left, right in q.findall(puzzle):
        left_list.append(int(left))
        right_list.append(int(right))

    left_list.sort()
    right_list.sort()

    dist = 0
    for left, right in zip(left_list, right_list):
        dist += abs(right - left)

    logger.success(f"Distance: {dist}")


def part2(puzzle: str):
    q = re.compile(r"(\d+) +(\d+)")

    left_map = {}
    right_map = {}

    for left, right in q.findall(puzzle):
        left = int(left)
        if left not in left_map:
            left_map[left] = 0
        left_map[left] += 1

        right = int(right)
        if right not in right_map:
            right_map[right] = 0
        right_map[right] += 1

    left_keys = set(left_map.keys())
    right_keys = set(right_map.keys())

    similarity = 0
    for key in left_keys.intersection(right_keys):
        similarity += key * left_map[key] * right_map[key]

    logger.success(f"Similarity: {similarity}")
