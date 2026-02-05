from typing import Generator

def ingest_data(file_path: str="raw_data.csv", row_frequency: int=100000) -> Generator[str, None, None]:
    """
    Extractor: A memory-efficient stream processor for large-scale CSV ingestion.
    
    This generator maintains O(1) space complexity by yielding rows lazily,
    ensuring stability regardless of the input file size.
    """
    try:
        with open(file_path, "r") as file:
            for row_count, line in enumerate(file, 1):
                if row_count % row_frequency == 0:
                    yield line.strip()
    except FileNotFoundError:
        raise FileNotFoundError(f"File {file_path} not found")
    except Exception as e:
        # 'from e' implements Exception Chaining, preserving the original 
        # traceback for root-cause analysis.
        raise RuntimeError(f"Error ingesting data: {e}") from e


if __name__ == "__main__":
    try:
        csv_lines = ingest_data()
        for line in csv_lines:
            print(line)
    except Exception as e:
        print(f"Ingestion failed: {e}")