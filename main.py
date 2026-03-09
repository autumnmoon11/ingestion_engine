from engine import ingest_data, filter_data, AITransformer
from destinations import Destination, JSONLDestination
from utils.time_execution import time_execution_decorator
from pathlib import Path

@time_execution_decorator
def run_ingestion(destination: Destination, blocked_ids: set, input_csv: Path):
    """Orchestrates the data stream from extraction to loading."""

    ai_transformer = AITransformer()

    with destination as dest:
        raw_stream = ingest_data(input_csv, row_frequency=1)
        filtered_stream = filter_data(raw_stream, blocked_ids)
        for row in filtered_stream:
            enriched_row = ai_transformer.transform_row(row)
            dest.write(enriched_row)

def load_blocked_ids(file_path: str) -> set:
    try:
        with open(file_path, "r") as f:
            # Using a set comprehension for O(1) lookup efficiency
            return {line.strip() for line in f if line.strip()}
    except FileNotFoundError:
        return set() # Fail gracefully with an empty set

def main():
    data_path = Path("data") 
    input_csv = data_path / "semantic_data.csv"
    blocked_txt = data_path / "blocked_ids.txt"
    output_jsonl = data_path / "output.jsonl"

    blocked = load_blocked_ids(blocked_txt)
    
    dest = JSONLDestination(output_jsonl)

    print("--- AI-Enriched JSONLPipeline Started ---")
    run_ingestion(dest, blocked, input_csv)
    
    # Telemetry Report
    if hasattr(run_ingestion, "last_execution_time"):
        print(f"Pipeline finished in: {run_ingestion.last_execution_time}s")

if __name__ == "__main__":
    main()