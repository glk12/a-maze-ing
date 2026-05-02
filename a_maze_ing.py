"""Command-line entrypoint for the A-Maze-ing project."""

from __future__ import annotations

import sys

from mazegen import (
    MazeConfigError,
    MazeGenerator,
    MazeValidationError,
    load_config,
    solve_shortest_path,
    validate_maze,
)
from mazegen.output import build_output_text, write_output_file
from mazegen.render import render_ascii


def main(argv: list[str] | None = None) -> int:
    """Run the maze generator from the command line."""

    args = argv if argv is not None else sys.argv[1:]
    if len(args) != 1:
        print("Usage: python3 a_maze_ing.py config.txt", file=sys.stderr)
        return 1

    try:
        config = load_config(args[0])
        generator = MazeGenerator(config)
        maze = generator.generate()
        validate_maze(maze, config.entry, config.exit, config.perfect)
        solution_cells, directions = solve_shortest_path(
            maze,
            config.entry,
            config.exit,
        )
        output_text = build_output_text(
            maze,
            config.entry,
            config.exit,
            directions,
        )
        write_output_file(config.output_file, output_text)
        print(render_ascii(maze, config.entry, config.exit, solution_cells))
        print(f"\nOutput written to {config.output_file}")
        return 0
    except (MazeConfigError, MazeValidationError, ValueError, OSError) as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1
    except Exception as exc:  # pragma: no cover - last-resort guard for the CLI
        print(f"Unexpected error: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
