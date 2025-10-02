from pathlib import Path
from typing import Any, Dict
from .base_stat import BaseStat

class LineCounterStat(BaseStat):
    """
    Calculates the total number of lines and non-empty lines
    across all processed files.
    """
    def __init__(self) -> None:
        super().__init__()
        self.total_lines = 0
        self.non_empty_lines = 0

    def process_file(self, file_path: Path) -> None:
        """Counts the lines in a given file and adds it to the total."""
        try:
            with file_path.open("r", encoding="utf-8", errors="ignore") as f:
                for line in f:
                    self.total_lines += 1
                    # This condition checks if the line is not empty after stripping whitespace
                    if line.strip():
                        self.non_empty_lines += 1
        except (IOError, UnicodeDecodeError):
            # Ignore files that can't be opened or read (e.g., binary files)
            pass

    def get_results(self) -> Dict[str, Any]:
        return {
            "Total Lines": self.total_lines,
            "Non-empty Lines": self.non_empty_lines,
        }


class CharCounterStat(BaseStat):
    """Calculates the total number of characters across all processed files."""
    def __init__(self) -> None:
        super().__init__()
        self.total_chars = 0

    def process_file(self, file_path: Path) -> None:
        """Counts the characters in a given file and adds it to the total."""
        try:
            with file_path.open("r", encoding="utf-8", errors="ignore") as f:
                self.total_chars += len(f.read())
        except (IOError, UnicodeDecodeError):
            pass

    def get_results(self) -> Dict[str, Any]:
        return {"Total Characters": self.total_chars}
