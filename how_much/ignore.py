import os
from pathlib import Path
import pathspec

# File names that contain ignore patterns
IGNORE_FILENAMES = [".gitignore", ".howmuchignore"]
# Default patterns to always ignore
DEFAULT_IGNORE_PATTERNS = [".git/", "__pycache__/", "*.pyc", "*.so", ".idea/", ".vscode/"]

def build_ignore_spec(root: Path) -> pathspec.PathSpec:
    """
    Walks the directory tree starting from `root`, finds all ignore files,
    and compiles them into a single `pathspec.PathSpec` object.
    Patterns from nested ignore files are handled correctly by prepending their
    containing directory.

    Args:
        root (Path): The root directory of the repository/project to scan.

    Returns:
        pathspec.PathSpec: A spec object to match files against.
    """
    all_patterns = list(DEFAULT_IGNORE_PATTERNS)

    for dirpath, _, filenames in os.walk(root):
        current_dir = Path(dirpath)
        for ignore_filename in IGNORE_FILENAMES:
            if ignore_filename in filenames:
                ignore_file_path = current_dir / ignore_filename
                
                # The directory of the ignore file, relative to the scan root.
                relative_dir = ignore_file_path.parent.relative_to(root)

                with ignore_file_path.open("r", encoding="utf-8", errors="ignore") as f:
                    for line in f:
                        pattern = line.strip()
                        if not pattern or pattern.startswith("#"):
                            continue

                        # A pattern in 'subdir/.gitignore' is relative to 'subdir/'.
                        # We must prepend the path to that subdir to make it work correctly
                        # from the root of the scan.
                        if str(relative_dir) != ".":
                            full_pattern = f"{relative_dir.as_posix()}/{pattern}"
                        else:
                            full_pattern = pattern
                        
                        all_patterns.append(full_pattern)

    # 'gitwildmatch' is the style of matching used by .gitignore
    return pathspec.PathSpec.from_lines("gitwildmatch", all_patterns)
