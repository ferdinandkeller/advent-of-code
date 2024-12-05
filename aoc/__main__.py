from pathlib import Path
import sys
import requests
import importlib
from loguru import logger


def get_puzzle(year: int, day: int) -> str | None:
    puzzle_cache = Path(__file__).parent / "inputs" / f"year{year}" / f"day{day:02}.txt"

    # check if cached
    if puzzle_cache.exists():
        with puzzle_cache.open("r") as f:
            logger.info(f"Using cached input for year {year} day {day}.")
            return f.read().strip()

    # else pull & cache
    with open(Path("session_cookie.txt")) as f:
        session_cookie = f.read().strip()
    puzzle_cache.parent.mkdir(parents=True, exist_ok=True)
    url = f"https://adventofcode.com/{year}/day/{day}/input"
    response = requests.get(url, headers={"Cookie": f"session={session_cookie}"})

    if response.status_code == 200:
        input_data = response.text.strip()
        with puzzle_cache.open("w") as f:
            f.write(input_data)
        logger.success(f"Input for year {year} day {day} downloaded.")
        return input_data
    elif response.status_code == 400:
        logger.error("Bad request: Did you provide a valid session cookie?")
        return None
    elif response.status_code == 404:
        logger.error("Input not found: Is the challenge unlocked yet?")
        return None
    else:
        logger.error(f"Error: Received status code {response.status_code}")
        return None


def get_solution(year: int, day: int, challenge: int) -> any:
    solution_path = Path(__file__).parent / f"year{year}" / f"day{day:02}.py"
    module_name = f"year{year}.day{day:02}"

    if not solution_path.exists():
        logger.error(f"Solution for year {year} day {day} not found.")
        return None

    try:
        module = importlib.import_module(module_name)
        part = getattr(module, f"part{challenge}", None)
        if part is None:
            logger.error(
                f"Solution not found for year {year} day {day} challenge {challenge}."
            )
            return None
    except Exception as e:
        logger.error(f"Failed to load module {module_name}")
        logger.exception(e)
        return None

    return part


if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: python __main__.py <year> <day> <challenge>")
        sys.exit(1)

    try:
        year = int(sys.argv[1])
        day = int(sys.argv[2])
        challenge = int(sys.argv[3])
    except ValueError:
        print("Year, day, and challenge must be integers.")
        sys.exit(1)

    try:
        if (puzzle := get_puzzle(year, day)) is None:
            sys.exit(1)
        if (part := get_solution(year, day, challenge)) is None:
            sys.exit(1)
        part(puzzle)
    except Exception as e:
        logger.exception(e)
        sys.exit(1)
