
# `how-much` Project Structure

This project is structured as a standard installable Python package using Poetry for dependency management. The core design principle is modularity, especially for the statistics gathering, to make it easy to add new types of analysis in the future.

```
how-much/
├── pyproject.toml         # Defines the project, dependencies (rich, typer), and CLI command.
├── README.md              # Instructions and description for the project.
│
└── how_much/              # This is the main source code package for the application.
    ├── __init__.py        # Makes `how_much` a Python package and holds the version number.
    ├── cli.py             # Handles the command-line interface using Typer and Rich.
    ├── main.py            # The application's core logic: orchestrates file scanning and analysis.
    ├── ignore.py          # Logic for parsing `.gitignore` and `.howmuchignore` files.
    │
    └── stats/             # A sub-package for all the statistic calculators (the extensible part).
        ├── __init__.py    # Makes `stats` a Python package.
        ├── base_stat.py   # Defines the abstract base class that all statistic calculators must inherit.
        ├── core_stats.py  # Implements the core statistics: line and character counts.
        └── file_counter.py# A simple stat calculator for counting files. (New stats go in new files here).
```