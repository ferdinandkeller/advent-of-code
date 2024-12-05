import re
from loguru import logger
from functools import cmp_to_key


def parse_rules(rules: str) -> list[tuple[int, int]]:
    q = re.compile(r"(\d+)\|(\d+)")
    return [(int(a), int(b)) for a, b in q.findall(rules)]


def parse_update(update: str) -> list[int]:
    return [int(p) for p in update.split(",")]


def parse_updates(updates: str) -> list[list[int]]:
    return [parse_update(u) for u in updates.split("\n")]


def verify_update(update: list[int], rules: list[tuple[int, int]]) -> bool:
    pages_map = {p: i for i, p in enumerate(update)}
    for p1, p2 in rules:
        if p1 in pages_map and p2 in pages_map:
            p1_pos = pages_map[p1]
            p2_pos = pages_map[p2]
            if p2_pos < p1_pos:
                return False
    return True


def verify_updates(updates: list[list[int]], rules: list[tuple[int, int]]) -> int:
    total = 0
    for update in updates:
        if verify_update(update, rules):
            total += update[len(update) // 2]
    return total


def part1(puzzle: str):
    rules, updates = puzzle.split("\n\n")
    rules = parse_rules(rules)
    updates = parse_updates(updates)
    middle_pages_total = verify_updates(updates, rules)
    logger.success(f"Middle pages total: {middle_pages_total}")


def get_rules_map(rules: list[tuple[int, int]]) -> dict[int, set[int]]:
    # for each page, we create a set of the rules they are part of
    # that way we can intersect those sets to find the rules that
    # apply to two pages
    rules_map = {}
    for i, (p1, p2) in enumerate(rules):
        if p1 not in rules_map:
            rules_map[p1] = set()
        rules_map[p1].add(i)
        if p2 not in rules_map:
            rules_map[p2] = set()
        rules_map[p2].add(i)
    return rules_map


def get_rules_sorting_key(rules: list[tuple[int, int]]):
    rules_map = get_rules_map(rules)

    def get_key(p1: int, p2: int) -> int:
        p1_rules = rules_map[p1]
        p2_rules = rules_map[p2]
        intersection_rules = p1_rules.intersection(p2_rules)
        if len(intersection_rules) == 0:
            # no rule applies to both pages
            # we don't care about the order
            return 0
        elif len(intersection_rules) == 1:
            # one rule applies to both pages, we retrieve it
            (first_page, _) = rules[intersection_rules.pop()]
            if first_page == p1:
                return -1  # keep p1 first
            else:
                return 1  # switch p2 first
        else:
            # should not happen
            raise Exception("Multiple rules found")

    return cmp_to_key(get_key)


def verify_updates_and_fix(
    updates: list[list[int]], rules: list[tuple[int, int]]
) -> int:
    total = 0
    for update in updates:
        if not verify_update(update, rules):
            update_sorted = sorted(update, key=get_rules_sorting_key(rules))
            total += update_sorted[len(update_sorted) // 2]
    return total


def part2(puzzle: str):
    rules, updates = puzzle.split("\n\n")
    rules = parse_rules(rules)
    updates = parse_updates(updates)
    middle_pages_total = verify_updates_and_fix(updates, rules)
    logger.success(f"Middle pages total: {middle_pages_total}")
