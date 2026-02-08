from engine import ingest_data, filter_data
from destinations import Destination, FileDestination
from utils.time_execution import time_execution_decorator
from pathlib import Path

@time_execution_decorator
def run_ingestion(destination: Destination, blocked_ids: set, input_csv: Path):
    """Orchestrates the data stream from extraction to loading."""
    with destination as dest:
        raw_stream = ingest_data(input_csv, row_frequency=1)
        filtered_stream = filter_data(raw_stream, blocked_ids)
        for row in filtered_stream:
            dest.write(row)

def load_blocked_ids(file_path: str) -> set:
    try:
        with open(file_path, "r") as f:
            # Using a set comprehension for O(1) lookup efficiency
            return {line.strip() for line in f if line.strip()}
    except FileNotFoundError:
        return set() # Fail gracefully with an empty set

def main():
    # 1. Load configuration/dependencies
    data_path = Path("data") 
    input_csv = data_path / "raw_data.csv"
    blocked_txt = data_path / "blocked_ids.txt"
    output_csv = data_path / "output.csv"

    blocked = load_blocked_ids(blocked_txt)
    
    # 2. Strategy Selection (Change to ConsoleDestination() to test)
    dest = FileDestination(output_csv)

    # 3. Execution
    print("--- Pipeline Started ---")
    run_ingestion(dest, blocked, input_csv)
    
    # 4. Telemetry Report
    if hasattr(run_ingestion, "last_execution_time"):
        print(f"Pipeline finished in: {run_ingestion.last_execution_time}s")

if __name__ == "__main__":
    main()