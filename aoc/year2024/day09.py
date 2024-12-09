from loguru import logger
from collections import deque, defaultdict
from dataclasses import dataclass


@dataclass
class File:
    id: int
    index: int
    size: int

    def is_void(self):
        return self.id == -1

    def __repr__(self):
        if self.is_void():
            return f"[i:{self.index},s:{self.size}]"
        return f"#{self.id}[i:{self.index},s:{self.size}]]"


def parse_puzzle(puzzle: str) -> deque[File]:
    d = deque()
    file_id = 0
    file_index = 0
    for i, file_size in enumerate(puzzle):
        file_size = int(file_size)
        if file_size == 0:
            continue
        if i % 2 == 0:
            d.append(File(file_id, file_index, file_size))
            file_id += 1
        else:
            d.append(File(-1, file_index, file_size))
        file_index += file_size
    return d


def get_file(puzzle: deque[File]) -> File | None:
    if len(puzzle) == 0:
        return None
    if (file := puzzle.pop()).is_void():
        return get_file(puzzle)
    else:
        return file


def get_files(puzzle: deque[File], size: int) -> list[File]:
    out = []
    while True:
        if (file := get_file(puzzle)) is None:
            break
        if file.size >= size:
            out.append(File(file.id, file.index + file.size - size, size))
            if file.size != size:
                puzzle.append(File(file.id, file.index, file.size - size))
            break
        else:
            out.append(file)
            size -= file.size
    return out


def collapse(puzzle: deque[File]):
    out = []
    while True:
        if len(puzzle) == 0:
            break
        file = puzzle.popleft()
        if file.is_void():
            void_index = file.index
            for f in get_files(puzzle, file.size):
                out.append(File(f.id, void_index, f.size))
                void_index += f.size
        else:
            out.append(file)
    return out


def combine(collapsed: list[File]) -> list[File]:
    out = []
    previous = None
    for file in collapsed:
        if file.size == 0:
            continue
        if previous is None:
            previous = file
            continue
        if previous.id == file.id:
            previous.size += file.size
        else:
            out.append(previous)
            previous = file
    if previous is not None:
        out.append(previous)
    return out


def defragment(puzzle: deque[File]) -> list[File]:
    return combine(collapse(puzzle))


def span_sum(index: int, size: int) -> int:
    return index * size + size * (size - 1) // 2


def checksum(collapsed: list[File]) -> int:
    return sum(file.id * span_sum(file.index, file.size) for file in collapsed)


def get_void_map(puzzle: deque[File]) -> dict[int, set[int]]:
    void_map = defaultdict(set)
    for file in puzzle:
        if file.is_void():
            void_map[file.size].add(file.index)
    return void_map


def find_available_void_at_size(
    void_map: dict[int, set[int]], maximum_index: int, size: int
) -> int | None:
    return min(
        (index for index in void_map[size] if index < maximum_index), default=None
    )


def find_available_void(
    void_map: dict[int, set[int]], maximum_index: int, minimum_size: int
) -> tuple[int, int] | None:
    smallest_index = None
    smallest_size = None
    for size in void_map.keys():
        if size < minimum_size:
            continue
        index = find_available_void_at_size(void_map, maximum_index, size)
        if index is not None and (smallest_index is None or index < smallest_index):
            smallest_index = index
            smallest_size = size
    if smallest_index is not None:
        return smallest_index, smallest_size
    return None


def defragment2(puzzle: deque[File], void_map: dict[int, set[int]]) -> list[File]:
    defragmented = []

    while len(puzzle) > 0:
        last = puzzle.pop()
        if last.is_void():
            continue
        void = find_available_void(void_map, last.index, last.size)
        if void is not None:
            void_index, void_size = void
            defragmented.append(File(last.id, void_index, last.size))
            void_map[void_size].remove(void_index)
            if last.size != void_size:
                void_map[void_size - last.size].add(void_index + last.size)
        else:
            defragmented.append(last)

    return defragmented


def part1(puzzle: str):
    puzzle = parse_puzzle(puzzle)
    defragmented = defragment(puzzle)
    checksum_value = checksum(defragmented)
    logger.success(f"Checksum: {checksum_value}")


def part2(puzzle: str):
    puzzle = parse_puzzle(puzzle)
    void_map = get_void_map(puzzle)
    defragmented = defragment2(puzzle, void_map)
    checksum_value = checksum(defragmented)
    logger.success(f"Checksum: {checksum_value}")
