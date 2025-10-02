
# How Much

`how-much` is a command-line tool to get statistics from your code repositories or directories. It's built to be fast, simple, and easily extensible.

## Features

-   Calculates statistics like total lines (including and excluding empty lines), characters, and file counts.
-   Correctly ignores files specified in `.gitignore` files at any directory level.
-   Supports a custom `.howmuchignore` file for project-specific ignores.
-   Can display a tree view of all processed (non-ignored) files.
-   Extensible plugin system for adding new statistics.
-   Beautiful and clear output powered by the `rich` library.
    

## Installation

Assuming you have [Poetry](https://python-poetry.org/ "null") installed:
```
# Clone the repository (or navigate to your project directory)
git clone <your-repo-url>
cd how-much

# Install dependencies
poetry install

# Run the tool
poetry run how-much .
```

To install it as a global command via `pip` from source:
```
pip install .
```

## Usage

Run it against the current directory to see statistics:
```
how-much .
```

Or specify a path to a directory or a single file:
```
how-much path/to/your/project
```

### Listing Files

To see a tree view of all the files that will be included in the calculations (i.e., not ignored), use the `--list-files` or `-l` flag:
```
how-much . --list-files
```