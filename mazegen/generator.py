"""Maze generation algorithms."""

from __future__ import annotations

import random

from .config import MazeConfig
from .model import Coordinate, Maze


class MazeGenerator:
    """Generate a maze using a seeded recursive-backtracking strategy."""

    def __init__(self, config: MazeConfig) -> None:
        """Store generator settings and initialize deterministic randomness."""

        self.config = config
        self._random = random.Random(config.seed)

    def generate(self) -> Maze:
        """Generate a maze that satisfies the mandatory perfect-maze rules."""

        if not self.config.perfect:
            raise ValueError(
                "Only PERFECT=True is implemented for the mandatory version."
            )
        return self._generate_perfect_maze()

    def _generate_perfect_maze(self) -> Maze:
        """Build a perfect maze with iterative recursive backtracking."""

        maze = Maze(self.config.width, self.config.height)
        start = Coordinate(
            x=self._random.randrange(self.config.width),
            y=self._random.randrange(self.config.height),
        )
        stack = [start]
        visited = {start}

        while stack:
            current = stack[-1]
            candidates = [
                (direction, neighbor)
                for direction, neighbor in maze.neighbors(current)
                if neighbor not in visited
            ]
            if not candidates:
                stack.pop()
                continue

            direction, neighbor = self._random.choice(candidates)
            maze.carve_passage(current, direction)
            visited.add(neighbor)
            stack.append(neighbor)

        return maze
