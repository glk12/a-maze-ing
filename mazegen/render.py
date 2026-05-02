"""ASCII rendering helpers for terminal output."""

from __future__ import annotations

from .model import Coordinate, Direction, Maze
from .pattern import get_42_pattern_cells


def render_ascii(
    maze: Maze,
    entry: Coordinate,
    exit_coord: Coordinate,
    solution: list[Coordinate],
) -> str:
    """Render the maze with walls, entry, exit, and solution path."""

    solution_cells = set(solution[1:-1])
    pattern_cells = get_42_pattern_cells(maze.width, maze.height, entry, exit_coord)
    lines: list[str] = []

    top = "+"
    for x in range(maze.width):
        top += "---+" if maze.cell_at(Coordinate(x, 0)).has_wall(Direction.NORTH) else "   +"
    lines.append(top)

    for y in range(maze.height):
        middle = ""
        bottom = "+"
        for x in range(maze.width):
            coord = Coordinate(x, y)
            cell = maze.cell_at(coord)
            middle += "|" if cell.has_wall(Direction.WEST) else " "
            middle += (
                f" {_cell_marker(coord, entry, exit_coord, solution_cells, pattern_cells)} "
            )
            bottom += "---+" if cell.has_wall(Direction.SOUTH) else "   +"
        middle += "|" if maze.cell_at(Coordinate(maze.width - 1, y)).has_wall(Direction.EAST) else " "
        lines.append(middle)
        lines.append(bottom)

    return "\n".join(lines)


def _cell_marker(
    coord: Coordinate,
    entry: Coordinate,
    exit_coord: Coordinate,
    solution_cells: set[Coordinate],
    pattern_cells: set[Coordinate],
) -> str:
    """Return the character used to display a cell."""

    if coord == entry:
        return "E"
    if coord == exit_coord:
        return "X"
    if coord in pattern_cells:
        return "#"
    if coord in solution_cells:
        return "*"
    return " "
