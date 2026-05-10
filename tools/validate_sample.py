"""Small validation script for local manual checks."""

from __future__ import annotations

from pathlib import Path
import sys

ROOT_DIR = Path(__file__).resolve().parents[1]
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))


def main() -> int:
    """Generate the sample maze and print a short validation summary."""

    from mazegen import (
        MazeGenerator,
        load_config,
        solve_shortest_path,
        validate_maze,
    )

    config = load_config("config.txt")
    maze = MazeGenerator(config).generate()
    validate_maze(maze, config.entry, config.exit, config.perfect)
    coordinates, directions = solve_shortest_path(
        maze,
        config.entry,
        config.exit,
    )
    print(f"Validated maze {config.width}x{config.height}")
    print(f"Output file: {Path(config.output_file)}")
    print(f"Shortest path length: {max(len(coordinates) - 1, 0)}")
    print(f"Shortest path directions: {directions}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
