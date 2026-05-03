*This project has been created as part of the 42 curriculum by glopes-a, vguerra-.*

# A-Maze-ing

## Description

`A-Maze-ing` is a Python 3.10+ maze generator built for the 42 project of the same name.
Its goal is to generate a valid maze from a configuration file, validate that maze against
the mandatory rules, compute the shortest path between the entry and exit, print a visual
ASCII representation in the terminal, and export the final maze in the hexadecimal format
required by the subject.

The current implementation is organized around a reusable package, [`mazegen/`](/home/glopes-a/a-maze-ing/mazegen),
plus the required CLI entrypoint [`a_maze_ing.py`](/home/glopes-a/a-maze-ing/a_maze_ing.py).
The main flow is:

1. Parse and validate the config file.
2. Generate a maze from the validated settings.
3. Validate the generated structure.
4. Solve the shortest path from `ENTRY` to `EXIT`.
5. Render the maze in ASCII.
6. Write the maze and solution path to the output file.

## Instructions

### Requirements

- Python `3.10` or newer

### Installation

Install the local package in editable mode:

```bash
make install
```

Equivalent command:

```bash
python3 -m pip install -e .
```

### Execution

Run the mandatory entrypoint with a config file:

```bash
python3 a_maze_ing.py config.txt
```

Or use:

```bash
make run
```

The program:

- reads the configuration from `config.txt`;
- prints an ASCII maze in the terminal;
- writes the exported maze to the file configured by `OUTPUT_FILE`.

### Useful commands

- `make debug`: runs the program with `PYTHONFAULTHANDLER=1`
- `make lint`: runs `flake8` and `mypy`
- `python3 tools/validate_sample.py`: generates a maze and prints a short validation summary

## Configuration File

The configuration file uses one `KEY=VALUE` pair per line.

Rules:

- Empty lines are ignored.
- Lines starting with `#` are ignored.
- Duplicate keys are rejected.
- Missing mandatory keys are rejected.

### Complete structure

Mandatory keys:

- `WIDTH`
- `HEIGHT`
- `ENTRY`
- `EXIT`
- `OUTPUT_FILE`
- `PERFECT`

Optional key:

- `SEED`

### Expected format of each field

- `WIDTH=<positive integer>`
- `HEIGHT=<positive integer>`
- `ENTRY=<x,y>`
- `EXIT=<x,y>`
- `OUTPUT_FILE=<path or filename>`
- `PERFECT=True|False`
- `SEED=<integer or string>` optional

Additional constraints enforced by the code:

- `ENTRY` and `EXIT` use zero-based coordinates.
- `ENTRY` must be inside maze bounds.
- `EXIT` must be inside maze bounds.
- `ENTRY` and `EXIT` must be different.
- `OUTPUT_FILE` must not be empty.
- The current generator only implements `PERFECT=True`.

### Example

```text
# Default A-Maze-ing configuration
WIDTH=15
HEIGHT=13
ENTRY=0,0
EXIT=10,5
OUTPUT_FILE=output_maze.txt
PERFECT=True
SEED=42
```

## Generation Algorithm

The project uses a seeded recursive backtracking algorithm implemented iteratively with an
explicit stack in [`mazegen/generator.py`](/home/glopes-a/a-maze-ing/mazegen/generator.py).

Algorithm steps:

1. Create a grid where every cell starts fully closed with the wall mask `0xF`.
2. Reserve the internal `42` pattern cells when the maze is large enough.
3. Choose a random active start cell using the configured `SEED`.
4. Repeatedly choose a random unvisited neighbor.
5. Open the shared wall between the current cell and that neighbor.
6. Push the neighbor onto the stack and continue.
7. If a cell has no valid unvisited neighbors, pop the stack to backtrack.
8. Stop when all active cells have been visited.

### Why this algorithm

We chose recursive backtracking because it matches the mandatory project requirements well:

- it is simple to reason about and implement correctly;
- it naturally produces connected mazes;
- it produces a spanning tree, which directly supports the `PERFECT=True` rule;
- it works well with deterministic randomness through a seed;
- it integrates cleanly with the project's wall-bit model and validation rules.

Using an explicit stack instead of Python recursion also avoids recursion-depth issues on
larger mazes and keeps the control flow easier to inspect while debugging.

## Maze Format And Model

Each maze cell stores its walls as a 4-bit mask in [`mazegen/model.py`](/home/glopes-a/a-maze-ing/mazegen/model.py):

- `1`: North
- `2`: East
- `4`: South
- `8`: West

All cells begin as `0xF`, meaning all four walls are closed. When the generator carves a
passage, it removes the wall from both adjacent cells so the maze remains coherent.

The main reusable types are:

- `Direction`: cardinal directions plus movement helpers
- `Coordinate`: immutable `x, y` positions
- `Cell`: one cell and its wall mask
- `Maze`: the whole grid with neighbor lookup and passage carving helpers

## Output Format

The output file is written row by row, one hexadecimal digit per cell. After an empty line,
the metadata block is appended:

```text
ENTRY=x,y
EXIT=x,y
PATH=NNEESW
```

Example:

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

## Reusable Parts

The reusable part of the project is the [`mazegen/`](/home/glopes-a/a-maze-ing/mazegen)
package. It is separated from the CLI entrypoint so the generation logic can be imported
and reused in other scripts, tests, or future projects.

Main reusable modules:

- [`mazegen/config.py`](/home/glopes-a/a-maze-ing/mazegen/config.py): config parsing and validation
- [`mazegen/model.py`](/home/glopes-a/a-maze-ing/mazegen/model.py): maze data model
- [`mazegen/generator.py`](/home/glopes-a/a-maze-ing/mazegen/generator.py): maze generation
- [`mazegen/solver.py`](/home/glopes-a/a-maze-ing/mazegen/solver.py): validation and shortest-path solving
- [`mazegen/render.py`](/home/glopes-a/a-maze-ing/mazegen/render.py): terminal rendering
- [`mazegen/output.py`](/home/glopes-a/a-maze-ing/mazegen/output.py): export serialization

In practice, another script can import `load_config`, `MazeGenerator`, `validate_maze`, or
`solve_shortest_path` directly from `mazegen` without depending on the CLI.

## Team And Project Management

### Team roles

- `glopes-a`: implementation, project structure, packaging, CLI integration, documentation
- `vguerra-`: implementation, validation logic, testing, review, documentation

These roles were collaborative rather than rigid; both contributors reviewed architecture,
generation behavior, and output compliance throughout the project.

### Planning and evolution

Initial plan:

1. Define the maze data model and wall encoding.
2. Implement config parsing and input validation.
3. Implement a correct mandatory maze generation algorithm.
4. Add shortest-path solving and structural validation.
5. Add ASCII rendering and file export.
6. Package the reusable code and document the project.

How it evolved:

- The reusable package boundary became more important than originally planned, so core logic
  was grouped under `mazegen/` instead of being kept directly in the entrypoint.
- Validation grew from simple config checks into a separate structural verification step for
  borders, coherence, connectivity, perfect-maze properties, and forbidden open `3x3` areas.
- The internal `42` reserved pattern was integrated into generation, validation, and rendering,
  which forced cleaner separation between active maze cells and blocked cells.

### What worked well

- Separating the reusable package from the CLI kept the code easier to reason about.
- Using a compact wall-bit model made generation, validation, rendering, and export align well.
- Deterministic seeding made debugging and comparison much easier.
- Validating the generated maze after creation gave fast feedback on rule compliance.

### What could be improved

- Only `PERFECT=True` is currently implemented; non-perfect maze generation is not yet supported.
- There are no automated unit tests yet; current checks are based on manual validation and linting.
- Additional output modes or alternative generation algorithms could be added in the future.

### Tools used

- `Python 3.10+`
- `make`
- `flake8`
- `mypy`
- local shell tooling for manual runs and verification

## Validation And Quality Checks

Manual validation flow:

```bash
python3 a_maze_ing.py config.txt
python3 tools/validate_sample.py
make lint
```

Useful manual checks:

- remove one mandatory config key;
- place `ENTRY` or `EXIT` outside bounds;
- set `ENTRY` equal to `EXIT`;
- write an invalid line without `=`;
- change `SEED` and confirm the maze changes;
- run twice with the same `SEED` and confirm the maze stays the same.

## Advanced Features

Beyond the minimal CLI flow, the current implementation also includes:

- deterministic generation through `SEED`;
- reusable Python package organization;
- shortest-path solving with direction export;
- terminal ASCII rendering with path highlighting;
- structural post-generation validation;
- internal reserved `42` pattern rendering when the maze is large enough.

The project does not currently implement multiple generation algorithms or multiple display
backends.

## Resources

Classic references used for the topic:

- The official project subject: [`en.subject.pdf`](/home/glopes-a/a-maze-ing/en.subject.pdf)
- Python documentation: https://docs.python.org/3/
- `dataclasses` documentation: https://docs.python.org/3/library/dataclasses.html
- `enum` documentation: https://docs.python.org/3/library/enum.html
- `pathlib` documentation: https://docs.python.org/3/library/pathlib.html
- Depth-first search and backtracking references for maze generation:
  https://en.wikipedia.org/wiki/Maze_generation_algorithm
- Breadth-first search reference for shortest-path solving:
  https://en.wikipedia.org/wiki/Breadth-first_search

### AI usage

AI was used as an assistant for:

- structuring and refining documentation;
- explaining code behavior and reviewing readability;
- checking alignment between the implementation and the README requirements;
- suggesting wording improvements and organizational cleanup.

AI was not used as a substitute for validating the mandatory project rules. Final design
choices, implementation decisions, debugging, verification, and compliance checks remained
the responsibility of the project authors.
