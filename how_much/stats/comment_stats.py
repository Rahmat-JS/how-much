import re
from pathlib import Path
from typing import Any, Dict
from .base_stat import BaseStat

# Mapping of file extensions (without dot) to their single-line comment markers.
# This can be extended to support more languages. We will ignore block comments
# for simplicity, as they are harder to parse reliably line-by-line.
SINGLE_LINE_COMMENT_MARKERS = {
    "py": "#", "rb": "#", "sh": "#", "pl": "#", "r": "#", "yml": "#", "yaml": "#",
    "js": "//", "ts": "//", "java": "//", "c": "//", "cpp": "//", "h": "//", "hpp": "//",
    "cs": "//", "go": "//", "rs": "//", "swift": "//", "kt": "//", "scala": "//",
    "php": "//", "sql": "--", "lua": "--",
}

# Regex to find 'TODO' as a whole word. \b is a word boundary, which ensures
# we don't match words like "TODOS" or "MYTODO". It requires TODO to be uppercase.
TODO_PATTERN = re.compile(r'\bTODO\b')


class TodoCounterStat(BaseStat):
    """
    Counts the occurrences of 'TODO' inside single-line comments
    for supported file types.
    """
    def __init__(self) -> None:
        super().__init__()
        self.todo_count = 0

    def process_file(self, file_path: Path) -> None:
        """
        Reads a file, identifies comment lines based on the file extension,
        and counts occurrences of 'TODO'.
        """
        # Get file extension, removing the leading dot
        extension = file_path.suffix[1:]
        
        # Check if we have a comment marker for this file type
        comment_marker = SINGLE_LINE_COMMENT_MARKERS.get(extension)
        if not comment_marker:
            return # Skip files we don't know how to parse for comments

        try:
            with file_path.open("r", encoding="utf-8", errors="ignore") as f:
                for line in f:
                    # Find the position of the comment marker
                    comment_start_index = line.find(comment_marker)

                    # If the marker is found in the line
                    if comment_start_index != -1:
                        # Extract the substring from the comment marker to the end
                        comment_text = line[comment_start_index:]
                        
                        # Use the regex to find all non-overlapping matches of 'TODO'
                        matches = TODO_PATTERN.findall(comment_text)
                        self.todo_count += len(matches)

        except (IOError, UnicodeDecodeError):
            # Silently ignore files that cannot be read as text (e.g., binary files)
            pass

    def get_results(self) -> Dict[str, Any]:
        return {"TODO Comments": self.todo_count}

