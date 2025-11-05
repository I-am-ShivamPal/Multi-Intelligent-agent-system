import os
import csv
import datetime
import pandas as pd
from abc import ABC, abstractmethod

class BaseAgent(ABC):
    """Base class for all agents with common functionality."""
    
    def __init__(self, log_file_path: str):
        self.log_file = log_file_path
        self._initialize_log_file()
    
    def _initialize_log_file(self):
        """Initialize log file with headers if it doesn't exist."""
        os.makedirs(os.path.dirname(self.log_file), exist_ok=True)
        if not os.path.exists(self.log_file):
            headers = self.get_log_headers()
            with open(self.log_file, 'w', newline='') as f:
                csv.writer(f).writerow(headers)
    
    def _log_entry(self, data: dict):
        """Log an entry with automatic timestamp."""
        data['timestamp'] = datetime.datetime.now().isoformat()
        with open(self.log_file, 'a', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=self.get_log_headers())
            writer.writerow(data)
    
    def _safe_read_csv(self, file_path: str) -> pd.DataFrame:
        """Safely read CSV with comprehensive error handling."""
        try:
            if not os.path.exists(file_path):
                return pd.DataFrame()
            return pd.read_csv(file_path)
        except (pd.errors.EmptyDataError, pd.errors.ParserError, UnicodeDecodeError, PermissionError):
            return pd.DataFrame()
    
    @abstractmethod
    def get_log_headers(self) -> list:
        """Return list of log file headers."""
        pass
    
    @abstractmethod
    def run(self):
        """Main agent execution method."""
        pass