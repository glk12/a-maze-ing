"""Command-line entrypoint for the A-Maze-ing project."""

from __future__ import annotations

from dataclasses import replace
import sys

from mazegen import (
    Coordinate,
    Maze,
    MazeConfig,
    MazeConfigError,
    MazeGenerator,
    MazeValidationError,
    load_config,
    solve_shortest_path,
    validate_maze,
)
from mazegen.output import build_output_text, write_output_file
from mazegen.render import render_ascii

ANSI_CLEAR_SCREEN = "\033[2J\033[H"
WALL_COLORS = (
    ("Default", ""),
    ("Blue", "\033[34m"),
    ("Green", "\033[1;32m"),
    ("Yellow", "\033[33m"),
    ("Cyan", "\033[36m"),
    ("Magenta", "\033[35m"),
)


def main(argv: list[str] | None = None) -> int:
    """Run the maze generator from the command line."""

    args = argv if argv is not None else sys.argv[1:]
    if len(args) != 1:
        print("Usage: python3 a_maze_ing.py config.txt", file=sys.stderr)
        return 1

    try:
        config = load_config(args[0])
        _run_interactive_session(config)
        return 0
    except (MazeConfigError, MazeValidationError, ValueError, OSError) as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1
    except Exception as exc:  # pragma: no cover - last-resort guard for the CLI
        print(f"Unexpected error: {exc}", file=sys.stderr)
        return 1

def _run_interactive_session(config: MazeConfig) -> None:
    """Run an interactive ASCII session for viewing and regenerating mazes."""

    show_path = True
    color_index = 0
    generation_index = 0
    status_message = ""
    maze, solution_cells, directions = _generate_and_export(config, generation_index)

    while True:
        color_name, wall_color = WALL_COLORS[color_index]
        print(ANSI_CLEAR_SCREEN, end="")
        visible_solution = solution_cells if show_path else []
        print(render_ascii(maze, config.entry, config.exit, visible_solution, wall_color))
        print(f"\nOutput written to {config.output_file}")
        print(f"Shortest path: {directions if show_path else '[hidden]'}")
        print(
            "Controls: [r] regenerate  [p] show/hide path  "
            f"[c] wall color ({color_name})  [q] quit"
        )
        if status_message:
            print(status_message)
        try:
            command = input("Command: ").strip().lower()
        except EOFError:
            print()
            return

        status_message = ""
        if command in {"q", "quit"}:
            return
        if command in {"p", "path"}:
            show_path = not show_path
            status_message = (
                "Shortest path is now visible."
                if show_path
                else "Shortest path is now hidden."
            )
            continue
        if command in {"c", "color", "colour"}:
            color_index = (color_index + 1) % len(WALL_COLORS)
            status_message = f"Wall color changed to {WALL_COLORS[color_index][0]}."
            continue
        if command in {"r", "regen", "regenerate"}:
            generation_index += 1
            maze, solution_cells, directions = _generate_and_export(
                config,
                generation_index,
            )
            status_message = "Generated a new maze."
            continue

        status_message = "Unknown command. Use r, p, c, or q."


def _generate_and_export(
    config: MazeConfig,
    generation_index: int,
) -> tuple[Maze, list[Coordinate], str]:
    """Generate, validate, solve, and export a maze state."""

    generation_config = _config_for_generation(config, generation_index)
    generator = MazeGenerator(generation_config)
    maze = generator.generate()
    validate_maze(
        maze,
        generation_config.entry,
        generation_config.exit,
        generation_config.perfect,
    )
    solution_cells, directions = solve_shortest_path(
        maze,
        generation_config.entry,
        generation_config.exit,
    )
    output_text = build_output_text(
        maze,
        generation_config.entry,
        generation_config.exit,
        directions,
    )
    write_output_file(generation_config.output_file, output_text)
    return maze, solution_cells, directions


def _config_for_generation(config: MazeConfig, generation_index: int) -> MazeConfig:
    """Return the config to use for the requested generation cycle."""

    if generation_index == 0:
        return config
    base_seed = config.seed if config.seed is not None else "interactive"
    return replace(config, seed=f"{base_seed}:regen:{generation_index}")


if __name__ == "__main__":
    raise SystemExit(main())
