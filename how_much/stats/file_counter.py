from pathlib import Path
from typing import Any, Dict
from .base_stat import BaseStat

class FileCounterStat(BaseStat):
    """Counts the total number of files processed."""
    def __init__(self) -> None:
        super().__init__()
        self.file_count = 0

    def process_file(self, file_path: Path) -> None:
        """Increments the file counter for each file processed."""
        self.file_count += 1

    def get_results(self) -> Dict[str, Any]:
        return {"Processed Files": self.file_count}
