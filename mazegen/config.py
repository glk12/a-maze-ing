"""Configuration parsing and validation for A-Maze-ing."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from .model import Coordinate


REQUIRED_KEYS = (
    "WIDTH",
    "HEIGHT",
    "ENTRY",
    "EXIT",
    "OUTPUT_FILE",
    "PERFECT",
)


class MazeConfigError(Exception):
    """Raised when the configuration file is invalid."""


@dataclass(frozen=True)
class MazeConfig:
    """Validated configuration used to build a maze."""

    width: int
    height: int
    entry: Coordinate
    exit: Coordinate
    output_file: Path
    perfect: bool
    seed: int | str | None = None


def load_config(path_str: str) -> MazeConfig:
    """Parse and validate a maze configuration file."""

    path = Path(path_str)
    if not path.is_file():
        raise MazeConfigError(f"Config file not found: {path}")

    raw_values: dict[str, str] = {}
    try:
        lines = path.read_text(encoding="utf-8").splitlines()
    except OSError as exc:
        raise MazeConfigError(f"Could not read config file: {path}") from exc

    for line_number, raw_line in enumerate(lines, start=1):
        line = raw_line.strip()
        if not line or line.startswith("#"):
            continue
        if "=" not in line:
            raise MazeConfigError(
                f"Invalid config syntax on line {line_number}: expected KEY=VALUE."
            )
        key, value = line.split("=", maxsplit=1)
        key = key.strip()
        value = value.strip()
        if not key or not value:
            raise MazeConfigError(
                f"Invalid config syntax on line {line_number}: empty key or value."
            )
        if key in raw_values:
            raise MazeConfigError(f"Duplicate config key on line {line_number}: {key}")
        raw_values[key] = value

    missing_keys = [key for key in REQUIRED_KEYS if key not in raw_values]
    if missing_keys:
        missing = ", ".join(missing_keys)
        raise MazeConfigError(f"Missing mandatory config keys: {missing}")

    width = _parse_positive_int(raw_values["WIDTH"], "WIDTH")
    height = _parse_positive_int(raw_values["HEIGHT"], "HEIGHT")
    entry = _parse_coordinate(raw_values["ENTRY"], "ENTRY")
    exit_coord = _parse_coordinate(raw_values["EXIT"], "EXIT")

    if entry == exit_coord:
        raise MazeConfigError("ENTRY and EXIT must be different coordinates.")
    if not _coord_in_bounds(entry, width, height):
        raise MazeConfigError("ENTRY is outside maze bounds.")
    if not _coord_in_bounds(exit_coord, width, height):
        raise MazeConfigError("EXIT is outside maze bounds.")

    output_file = Path(raw_values["OUTPUT_FILE"])
    if not output_file.name:
        raise MazeConfigError("OUTPUT_FILE must not be empty.")

    perfect = _parse_bool(raw_values["PERFECT"], "PERFECT")
    seed = raw_values.get("SEED")
    if seed is not None:
        try:
            seed = int(seed)
        except ValueError:
            seed = seed

    return MazeConfig(
        width=width,
        height=height,
        entry=entry,
        exit=exit_coord,
        output_file=output_file,
        perfect=perfect,
        seed=seed,
    )


def _parse_positive_int(value: str, key: str) -> int:
    """Parse a strictly positive integer."""

    try:
        parsed = int(value)
    except ValueError as exc:
        raise MazeConfigError(f"{key} must be an integer.") from exc
    if parsed <= 0:
        raise MazeConfigError(f"{key} must be greater than zero.")
    return parsed


def _parse_coordinate(value: str, key: str) -> Coordinate:
    """Parse a zero-based `x,y` coordinate pair."""

    parts = [part.strip() for part in value.split(",")]
    if len(parts) != 2:
        raise MazeConfigError(f"{key} must use the format x,y.")
    try:
        x = int(parts[0])
        y = int(parts[1])
    except ValueError as exc:
        raise MazeConfigError(f"{key} must contain integer coordinates.") from exc
    return Coordinate(x=x, y=y)


def _parse_bool(value: str, key: str) -> bool:
    """Parse a boolean value written as True or False."""

    normalized = value.strip().lower()
    if normalized == "true":
        return True
    if normalized == "false":
        return False
    raise MazeConfigError(f"{key} must be either True or False.")


def _coord_in_bounds(coord: Coordinate, width: int, height: int) -> bool:
    """Return whether a coordinate fits inside a width/height rectangle."""

    return 0 <= coord.x < width and 0 <= coord.y < height
