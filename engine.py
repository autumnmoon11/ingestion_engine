from typing import Generator, Set
from collections.abc import Iterable
from pathlib import Path
import csv


def ingest_data(file_path: Path, row_frequency: int=1) -> Generator[dict, None, None]:
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

def filter_data(data_stream: Iterable[dict], block_list: Set[str]) -> Generator[dict, None, None]:
    """
    Filters a stream of dictionaries based on a set of blocked IDs.

    This function acts as a lazy transformer in the pipeline. It processes
    data one row at a time to maintain O(1) space complexity. By utilizing
    a set for blocked_ids, it ensures O(1) average-time complexity for 
    membership lookups.

    Args:
        data_stream (Iterable[dict]): A generator or iterable yielding 
            dictionaries (rows) from the ingestion source.
        blocked_ids (set): A set of strings representing IDs that should 
            be excluded from the output.

    Yields:
        Generator[dict, None, None]: The next row in the stream that does 
            not have a blocked ID.
    """
    try:
        for row in data_stream:
            if row.get("id") not in block_list:
                yield row
    except Exception as e:
        raise RuntimeError(f"Error filtering data: {e}") from e