from abc import ABC, abstractmethod
from pathlib import Path
from typing import Any, Dict

class BaseStat(ABC):
    """
    Abstract base class for all statistic calculators.
    
    This defines the contract for our "plugins". Any new statistic calculator
    must inherit from this class and implement its abstract methods. This allows
    the main application to discover and use them without knowing the specifics
    of each calculation.
    """

    def __init__(self) -> None:
        """Initializes the statistic calculator."""
        # A friendly name for the statistic, derived from the class name.
        self.name = self.__class__.__name__.replace("Stat", "")

    @abstractmethod
    def process_file(self, file_path: Path) -> None:
        """
        Process a single file to update the statistic.
        This method is called for every file that is not ignored.

        Args:
            file_path: The path to the file to process.
        """
        pass

    @abstractmethod
    def get_results(self) -> Dict[str, Any]:
        """
        Return the final calculated statistics after all files are processed.

        Returns:
            A dictionary where keys are statistic names (e.g., "Total Lines")
            and values are the results.
        """
        pass
