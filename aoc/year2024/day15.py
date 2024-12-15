from loguru import logger


def find_start_pos(puzzle_map: list[list[str]]) -> tuple[int, int]:
    for y, line in enumerate(puzzle_map):
        for x, char in enumerate(line):
            if char == "@":
                return x, y


def parse_move(puzzle_move: str) -> tuple[int, int]:
    match puzzle_move:
        case "<":
            return -1, 0
        case ">":
            return 1, 0
        case "^":
            return 0, -1
        case "v":
            return 0, 1
        case _:
            raise ValueError(f"Unknown move: {puzzle_move}")


def parse_moves(puzzle_moves: str) -> list[tuple[int, int]]:
    return [parse_move(move) for move in puzzle_moves]


def parse_puzzle(puzzle: str):
    puzzle_map, puzzle_moves = puzzle.split("\n\n")
    puzzle_moves = parse_moves(puzzle_moves.replace("\n", ""))
    puzzle_map = [list(line) for line in puzzle_map.split("\n")]
    start_pos = find_start_pos(puzzle_map)
    puzzle_map[start_pos[1]][start_pos[0]] = "."
    return puzzle_map, puzzle_moves, start_pos


def parse_char_wide(puzzle_char: str) -> str:
    match puzzle_char:
        case "#":
            return "##"
        case "O":
            return "[]"
        case ".":
            return ".."
        case "@":
            return "@."
        case _:
            raise ValueError(f"Unknown char: {puzzle_char}")


def parse_puzzle_wide(puzzle: str):
    puzzle_map, puzzle_moves = puzzle.split("\n\n")
    puzzle_moves = parse_moves(puzzle_moves.replace("\n", ""))
    puzzle_map = [
        list("".join([parse_char_wide(c) for c in line]))
        for line in puzzle_map.split("\n")
    ]
    start_pos = find_start_pos(puzzle_map)
    puzzle_map[start_pos[1]][start_pos[0]] = "."
    return puzzle_map, puzzle_moves, start_pos


def is_free(
    puzzle_map: list[list[str]], robot_pos: tuple[int, int], direction: tuple[int, int]
) -> bool:
    x, y = robot_pos
    new_x, new_y = x + direction[0], y + direction[1]
    match puzzle_map[new_y][new_x]:
        case "#":
            return False
        case ".":
            return True
        case "O":
            return is_free(puzzle_map, (new_x, new_y), direction)
        case "[":
            if direction[0] == 0:
                return (
                    is_free(puzzle_map, (new_x, new_y), direction)  #
                    and is_free(puzzle_map, (new_x + 1, new_y), direction)  #
                )
            elif direction[1] == 0:
                return is_free(puzzle_map, (new_x, new_y), direction)
        case "]":
            if direction[0] == 0:
                return (
                    is_free(puzzle_map, (new_x, new_y), direction)  #
                    and is_free(puzzle_map, (new_x - 1, new_y), direction)  #
                )
            elif direction[1] == 0:
                return is_free(puzzle_map, (new_x, new_y), direction)


def move_boxes(
    puzzle_map: list[list[str]], robot_pos: tuple[int, int], direction: tuple[int, int]
) -> tuple[int, int]:
    x, y = robot_pos
    new_x, new_y = x + direction[0], y + direction[1]
    match puzzle_map[new_y][new_x]:
        case "O":
            move_boxes(puzzle_map, (new_x, new_y), direction)
        case "[":
            if direction[0] == 0:
                move_boxes(puzzle_map, (new_x, new_y), direction)
                move_boxes(puzzle_map, (new_x + 1, new_y), direction)
                puzzle_map[new_y][new_x + 1] = "."
            elif direction[1] == 0:
                move_boxes(puzzle_map, (new_x, new_y), direction)
        case "]":
            if direction[0] == 0:
                move_boxes(puzzle_map, (new_x, new_y), direction)
                move_boxes(puzzle_map, (new_x - 1, new_y), direction)
                puzzle_map[new_y][new_x - 1] = "."
            elif direction[1] == 0:
                move_boxes(puzzle_map, (new_x, new_y), direction)
    puzzle_map[new_y][new_x] = puzzle_map[y][x]
    return new_x, new_y


def move_robot(
    puzzle_map: list[list[str]], robot_pos: tuple[int, int], direction: tuple[int, int]
) -> tuple[int, int]:
    if is_free(puzzle_map, robot_pos, direction):
        return move_boxes(puzzle_map, robot_pos, direction)
    return robot_pos


def sum_of_gps_coords(puzzle_map: list[list[str]]) -> int:
    gps_coords = 0
    for y, line in enumerate(puzzle_map):
        for x, c in enumerate(line):
            if c == "O" or c == "[":
                gps_coords += 100 * y + x
    return gps_coords


def part1(puzzle: str):
    puzzle_map, puzzle_moves, robot_pos = parse_puzzle(puzzle)
    for direction in puzzle_moves:
        robot_pos = move_robot(puzzle_map, robot_pos, direction)
    gps_coords = sum_of_gps_coords(puzzle_map)
    logger.success(f"Sum of GPS coords: {gps_coords}")


def part2(puzzle: str):
    puzzle_map, puzzle_moves, robot_pos = parse_puzzle_wide(puzzle)
    for direction in puzzle_moves:
        robot_pos = move_robot(puzzle_map, robot_pos, direction)
    gps_coords = sum_of_gps_coords(puzzle_map)
    logger.success(f"Sum of GPS coords: {gps_coords}")
