from abc import ABC, abstractmethod
from pathlib import Path
import json
import csv

class Destination(ABC):
    @abstractmethod
    def write(self, data: dict) -> None:
        pass

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        pass

class CSVDestination(Destination):
    """
    Strategy for persisting data as a CSV file.
    Updated to use Path objects for cross-platform reliability.
    """
    def __init__(self, file_path: Path):
        self.file_path = file_path
        self.file = None
        self.writer = None

    def __enter__(self):
        # Ensure the parent directory exists before opening
        self.file_path.parent.mkdir(parents=True, exist_ok=True)
        self.file = open(self.file_path, "w", newline="", encoding="utf-8")
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.file:
            self.file.close()

    def write(self, row: dict):
        if not self.writer:
            # Lazy initialization of the DictWriter using the first row's keys
            self.writer = csv.DictWriter(self.file, fieldnames=row.keys())
            self.writer.writeheader()
        self.writer.writerow(row)

class JSONLDestination(Destination):
    """
    Strategy for persisting data as JSON Lines (.jsonl).
    Ideal for AI workloads as it preserves vector arrays as native lists.
    """
    def __init__(self, file_path: Path):
        self.file_path = file_path
        self.file = None

    def __enter__(self):
        self.file_path.parent.mkdir(parents=True, exist_ok=True)
        self.file = open(self.file_path, "w", encoding="utf-8")
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.file:
            self.file.close()

    def write(self, row: dict):
        # json.dumps converts the Python dict (and the vector list) 
        # into a valid JSON string for one line.
        self.file.write(json.dumps(row) + "\n")

class ConsoleDestination(Destination):
    def write(self, data: dict) -> None:
        display_data = data.copy()
        if "embedding" in display_data and isinstance(display_data["embedding"], list):
            vector = display_data["embedding"]
            display_data["embedding"] = f"[{vector[0]:.4f}, {vector[1]:.4f}, ... (len: {len(vector)})]"
        print(display_data)

class CloudDestination(Destination):
    def __init__(self, cloud_provider: str):
        self.cloud_provider = cloud_provider

    def write(self, data: dict) -> None:
        print(f"Writing data to {self.cloud_provider}: {data}")