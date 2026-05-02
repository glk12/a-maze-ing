# A-Maze-ing

Python 3.10+ maze generator for the 42 project `A-Maze-ing`.

The project provides:

- the required entrypoint `a_maze_ing.py`;
- a reusable `MazeGenerator` implementation inside the `mazegen` package;
- maze validation, solving, ASCII rendering, and hexadecimal export.

The project subject remains the source of truth. This README documents the current implementation and how to use it.

## Authors

- `glopes-a`
- `vguerra-`

## Subject Summary

The mandatory project requires:

- execution with `python3 a_maze_ing.py config.txt`;
- a config file using `KEY=VALUE`;
- mandatory keys `WIDTH`, `HEIGHT`, `ENTRY`, `EXIT`, `OUTPUT_FILE`, `PERFECT`;
- random maze generation with reproducibility through a seed;
- wall encoding per cell using the `N/E/S/W` bit layout;
- coherent shared walls between neighboring cells;
- valid entry and exit coordinates inside bounds and different from each other;
- external borders closed by walls;
- full connectivity and no isolated cells;
- shortest valid path written with `N`, `E`, `S`, `W`;
- output file encoded row by row in hexadecimal;
- visual maze representation in the terminal;
- robust handling of invalid config, impossible parameters, missing files, and unexpected errors;
- `Makefile`, type hints, docstrings, and project documentation.

## Repository Structure

- [`a_maze_ing.py`](/home/glopes-a/a-maze-ing/a_maze_ing.py): command-line entrypoint.
- [`mazegen/`](/home/glopes-a/a-maze-ing/mazegen): reusable maze package.
- [`config.txt`](/home/glopes-a/a-maze-ing/config.txt): example configuration file.
- [`tools/validate_sample.py`](/home/glopes-a/a-maze-ing/tools/validate_sample.py): small validation script.
- [`Makefile`](/home/glopes-a/a-maze-ing/Makefile): required project commands.
- [`en.subject.pdf`](/home/glopes-a/a-maze-ing/en.subject.pdf): subject PDF in the repository.

## Installation

Use Python 3.10 or newer.

Install the reusable package locally:

```bash
make install
```

This runs:

```bash
python3 -m pip install -e .
```

## Usage

Run the program with:

```bash
python3 a_maze_ing.py config.txt
```

Or use:

```bash
make run
```

The program prints an ASCII representation of the maze and writes the output file configured by `OUTPUT_FILE`.

## Configuration File

The config file format is:

```text
KEY=VALUE
```

Empty lines and lines starting with `#` are ignored.

Mandatory keys:

- `WIDTH`
- `HEIGHT`
- `ENTRY`
- `EXIT`
- `OUTPUT_FILE`
- `PERFECT`

Supported optional keys:

- `SEED`

Example:

```text
WIDTH=8
HEIGHT=6
ENTRY=0,0
EXIT=7,5
OUTPUT_FILE=output_maze.txt
PERFECT=True
SEED=42
```

Current implementation assumptions:

- `ENTRY` and `EXIT` use zero-based coordinates in `x,y` format.
- `PERFECT` must be `True` or `False`.
- the implemented mandatory path currently supports `PERFECT=True`.

## Maze Model

Each cell stores four walls:

- bit `0`: North
- bit `1`: East
- bit `2`: South
- bit `3`: West

In the code, the hexadecimal wall mask is:

- `1` for North
- `2` for East
- `4` for South
- `8` for West

All cells start fully closed as `0xF`. When a passage is carved, the wall is removed from both neighboring cells to keep the maze coherent.

## Generation Algorithm

The current generator uses seeded recursive backtracking with an explicit stack:

1. Create a grid where every cell has all four walls.
2. Choose a random start cell using the configured seed.
3. Pick a random unvisited neighbor.
4. Remove the shared wall between the two cells.
5. Continue until stuck, then backtrack.

This produces a connected spanning tree, which is why `PERFECT=True` yields exactly one path between any two cells.

## Validation Rules Implemented

The current code validates:

- config syntax and missing mandatory keys;
- integer dimensions greater than zero;
- valid `ENTRY` and `EXIT` format;
- entry and exit inside bounds;
- entry and exit being different;
- border walls remaining closed;
- neighboring wall coherence;
- full maze connectivity;
- shortest path existence between entry and exit;
- rejection of open `3x3` areas;
- perfect-maze property through graph validation.

## Output File Format

The output file writes the maze row by row, one hexadecimal digit per cell.

After one empty line, it writes:

```text
ENTRY=x,y
EXIT=x,y
PATH=NNEESW
```

Example generated output:

```text
97953953
C56BC6BA
9552952A
A956C3C6
AC393A93
C7C6C46E

ENTRY=0,0
EXIT=7,5
PATH=SEENEESENEESSSWNWWSESSENES
```

## Terminal Visualization

The project currently uses terminal ASCII rendering, which satisfies the mandatory visual requirement. The rendered maze shows:

- walls;
- the entry cell as `E`;
- the exit cell as `X`;
- the shortest path as `*`.

## Reusable Package

The `MazeGenerator` is implemented inside the standalone package [`mazegen/`](/home/glopes-a/a-maze-ing/mazegen). This keeps the generation logic reusable for future projects and prepares the repository for packaging later.

Main modules:

- [`mazegen/config.py`](/home/glopes-a/a-maze-ing/mazegen/config.py)
- [`mazegen/model.py`](/home/glopes-a/a-maze-ing/mazegen/model.py)
- [`mazegen/generator.py`](/home/glopes-a/a-maze-ing/mazegen/generator.py)
- [`mazegen/solver.py`](/home/glopes-a/a-maze-ing/mazegen/solver.py)
- [`mazegen/output.py`](/home/glopes-a/a-maze-ing/mazegen/output.py)
- [`mazegen/render.py`](/home/glopes-a/a-maze-ing/mazegen/render.py)

## Makefile

Available targets:

- `make install`: install the package in editable mode.
- `make run`: run the project with `config.txt`.
- `make debug`: run with Python fault handler enabled.
- `make clean`: remove cache and build artifacts.
- `make lint`: run `flake8` and `mypy` with the required flags.

## Manual Validation

Main flow:

```bash
python3 a_maze_ing.py config.txt
```

Validation helper:

```bash
python3 tools/validate_sample.py
```

Good manual checks:

- remove one mandatory key from the config file;
- set `ENTRY` or `EXIT` outside bounds;
- set `ENTRY` equal to `EXIT`;
- write an invalid line without `=`;
- change `SEED` and confirm the maze changes;
- run twice with the same `SEED` and confirm the maze stays the same.

## Quality Checks

The subject requires:

```bash
flake8 .
mypy . --warn-return-any --warn-unused-ignores --ignore-missing-imports --disallow-untyped-defs --check-untyped-defs
```

These commands are exposed through:

```bash
make lint
```

## Error Handling

The CLI handles:

- missing config file;
- unreadable config file;
- invalid config syntax;
- missing mandatory keys;
- invalid values and impossible coordinates;
- invalid generated maze state;
- unexpected runtime errors with a fallback message.

## Current Status

Covered in the current implementation:

- config parser;
- maze data model;
- reusable `MazeGenerator`;
- seeded recursive-backtracking generation;
- structural validation and shortest-path solver;
- hexadecimal output encoder;
- terminal ASCII rendering;
- root CLI entrypoint;
- Makefile;
- README and validation helper script.

Still needs subject review:

- exact `42` pattern behavior from the PDF;
- non-perfect generation when `PERFECT=False`;
- final confirmation that every README detail matches the subject wording exactly.
