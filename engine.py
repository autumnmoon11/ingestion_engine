from typing import Generator, Set


def ingest_data(file_path: str="raw_data.csv", row_frequency: int=100000) -> Generator[dict, None, None]:
    """
    Extractor: A memory-efficient stream processor for large-scale CSV ingestion.
    
    This generator maintains O(1) space complexity by yielding rows lazily,
    ensuring stability regardless of the input file size.
    """
    try:
        with open(file_path, "r") as file:
            # Consuming the first line (the header) to move the pointer forward and retrieve keys for the dict
            keys = next(file, None).strip().split(",")
            for row_count, line in enumerate(file, 1):
                if row_count % row_frequency == 0:
                    values = line.strip().split(",")
                    yield dict(zip(keys, values))
    except FileNotFoundError:
        raise FileNotFoundError(f"File {file_path} not found")
    except Exception as e:
        # 'from e' implements Exception Chaining, preserving the original 
        # traceback for root-cause analysis.
        raise RuntimeError(f"Error ingesting data: {e}") from e

def filter_data(data: Generator[dict, None, None], block_list: Set[str]) -> Generator[str, None, None]:
    try:
        for row in data:
            if row["id"] not in block_list:
                yield row
    except Exception as e:
        raise RuntimeError(f"Error filtering data: {e}") from e

if __name__ == "__main__":
    try:
        csv_lines = ingest_data()
        for line in csv_lines:
            print(line)
    except Exception as e:
        print(f"Ingestion failed: {e}")