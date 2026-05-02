"""Serialize mazes to the project output format."""

from __future__ import annotations

from pathlib import Path

from .model import Coordinate, Maze


def build_output_text(
    maze: Maze,
    entry: Coordinate,
    exit_coord: Coordinate,
    path_directions: str,
) -> str:
    """Return the output file contents for a generated maze."""

    lines = []
    for y in range(maze.height):
        line = "".join(
            format(maze.cell_at(Coordinate(x, y)).walls, "X")
            for x in range(maze.width)
        )
        lines.append(line)
    lines.extend(
        [
            "",
            f"ENTRY={entry.x},{entry.y}",
            f"EXIT={exit_coord.x},{exit_coord.y}",
            f"PATH={path_directions}",
        ]
    )
    return "\n".join(lines) + "\n"


def write_output_file(path: Path, contents: str) -> None:
    """Write the maze output file to disk."""

    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(contents, encoding="utf-8")
