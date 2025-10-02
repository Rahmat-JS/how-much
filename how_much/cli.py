from pathlib import Path
import typer
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.tree import Tree
from rich import box
from typing import List, Dict, Any

from .main import run_analysis, get_files_to_process
from . import __version__

# Initialize Typer app for the command-line interface
app = typer.Typer(
    name="how-much",
    help="A simple, extensible tool to get statistics from your code repositories.",
    add_completion=False,
)
# Initialize Rich console for beautiful output
console = Console()

def version_callback(value: bool):
    """Callback function to display the version and exit."""
    if value:
        console.print(f"how-much version: {__version__}")
        raise typer.Exit()

def _add_parts_to_tree_dict(tree_dict: Dict[str, Any], parts: List[str]):
    """Recursively builds a nested dictionary from a list of path parts."""
    head, *tail = parts
    if not tail:
        tree_dict[head] = None  # Mark as a file
        return
    if head not in tree_dict or tree_dict[head] is None:
        tree_dict[head] = {}
    _add_parts_to_tree_dict(tree_dict[head], tail)

def _build_rich_tree_from_dict(tree_dict: Dict[str, Any], branch: Tree):
    """Recursively populates a Rich Tree from a nested dictionary."""
    for name, children in sorted(tree_dict.items()):
        if children is None:  # It's a file
            branch.add(f":page_facing_up: [green]{name}[/green]")
        else:  # It's a directory
            new_branch = branch.add(f":open_file_folder: [bold blue]{name}[/bold blue]")
            _build_rich_tree_from_dict(children, new_branch)


@app.command()
def main(
    path: Path = typer.Argument(
        ".",
        exists=True,
        file_okay=True,
        dir_okay=True,
        writable=False,
        readable=True,
        resolve_path=True,
        help="The path to the file or directory to analyze.",
    ),
    list_files: bool = typer.Option(
        False,
        "--list-files",
        "-l",
        help="List all processed files in a tree view instead of showing statistics.",
    ),
    version: bool = typer.Option(
        None,
        "--version",
        "-v",
        callback=version_callback,
        is_eager=True,
        help="Show the version and exit.",
    ),
):
    """
    Analyzes a directory or file and displays statistics or a file tree about it.
    """
    try:
        if list_files:
            # If the flag is set, get the files and display the tree
            console.print(f"Scanning [bold cyan]'{path.name}'[/bold cyan] for processable files...")
            files = get_files_to_process(path)
            
            tree = Tree(
                f":file_folder: [bold magenta]{path.name}[/bold magenta]",
                guide_style="bold bright_blue",
            )
            
            # Build an intermediate dictionary representation of the file tree
            tree_dict = {}
            root_for_rel_path = path if path.is_dir() else path.parent
            for file_path in files:
                relative_parts = file_path.relative_to(root_for_rel_path).parts
                _add_parts_to_tree_dict(tree_dict, list(relative_parts))

            # Build the Rich Tree from the dictionary
            _build_rich_tree_from_dict(tree_dict, tree)
            
            console.print(tree)
            return # Use return for a normal exit

        # The main logic is in run_analysis. This function just handles CLI interaction.
        results = run_analysis(path)

        # Create a Rich table to display the results
        table = Table(box=box.ROUNDED, show_header=True, header_style="bold magenta")
        table.add_column("Statistic", style="dim", width=25)
        table.add_column("Value", justify="right")

        # Populate the table with results, formatting numbers with commas
        for key, value in sorted(results.items()):
            table.add_row(key, f"{value:,}")
            
        # Display the table inside a panel for a polished look
        console.print(Panel(
            table,
            title=f"[bold cyan]Statistics for '{path.name}'[/bold cyan]",
            expand=False
        ))

    except FileNotFoundError as e:
        console.print(f"[bold red]Error: {e}[/bold red]")
        raise typer.Exit(code=1)
    except Exception as e:
        console.print(f"[bold red]An unexpected error occurred: {e}[/bold red]")
        raise typer.Exit(code=1)

