import os
import importlib
import inspect
from pathlib import Path
from typing import List, Dict, Any

from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn, TimeElapsedColumn

from .stats.base_stat import BaseStat
from .ignore import build_ignore_spec

def discover_stats() -> List[BaseStat]:
    """
    Dynamically discovers and instantiates all statistic calculator classes
    from all modules inside the 'stats' package. This makes the tool extensible.
    To add a new stat, simply add a new file in the 'stats' directory with a
    class that inherits from BaseStat.
    """
    stats_instances = []
    stats_package_path = Path(__file__).parent / "stats"
    
    # Iterate over all python files in the stats directory
    for module_file in stats_package_path.glob("*.py"):
        if module_file.name.startswith("__"):
            continue
            
        module_name = f"how_much.stats.{module_file.stem}"
        try:
            # Import the module
            module = importlib.import_module(module_name)
            # Find all classes in the module that are subclasses of BaseStat
            for _, obj in inspect.getmembers(module, inspect.isclass):
                if issubclass(obj, BaseStat) and obj is not BaseStat:
                    stats_instances.append(obj())
        except ImportError:
            # Handle potential import errors gracefully
            continue
            
    return stats_instances

def get_files_to_process(target_path: Path) -> List[Path]:
    """
    Finds all files in a given path that are not ignored by .gitignore
    or .howmuchignore rules.

    Args:
        target_path: The directory or file to scan.

    Returns:
        A list of Path objects for all files to be processed.
    """
    if not target_path.exists():
        raise FileNotFoundError(f"The path '{target_path}' does not exist.")

    # If target is a file, the root for ignore searching is its parent directory
    root_for_ignore = target_path if target_path.is_dir() else target_path.parent
    ignore_spec = build_ignore_spec(root_for_ignore)

    files_to_process = []
    if target_path.is_dir():
        for root, _, files in os.walk(target_path):
            for file in files:
                file_path = Path(root) / file
                # The path must be relative to the ignore root for correct matching
                relative_path = file_path.relative_to(root_for_ignore)
                if not ignore_spec.match_file(str(relative_path)):
                    files_to_process.append(file_path)
    elif target_path.is_file(): # Handle case where a single file is passed
        relative_path = target_path.relative_to(root_for_ignore)
        if not ignore_spec.match_file(str(relative_path)):
             files_to_process.append(target_path)
    
    return files_to_process

def run_analysis(target_path: Path) -> Dict[str, Any]:
    """
    Runs the full analysis on a given path.

    1. Discovers all available statistic calculators.
    2. Finds all non-ignored files.
    3. Processes each file with the calculators.
    4. Collects and returns the results.
    """
    stat_calculators = discover_stats()
    files_to_process = get_files_to_process(target_path)

    # Use Rich's Progress bar to show processing status
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        BarColumn(),
        TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
        TimeElapsedColumn(),
    ) as progress:
        task = progress.add_task("[green]Analyzing files...", total=len(files_to_process))
        for file_path in files_to_process:
            for calculator in stat_calculators:
                calculator.process_file(file_path)
            progress.update(task, advance=1)

    # Collect results from all calculators into a single dictionary
    all_results = {}
    for calculator in stat_calculators:
        all_results.update(calculator.get_results())
        
    return all_results

