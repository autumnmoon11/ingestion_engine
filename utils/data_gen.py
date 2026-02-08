import csv
from pathlib import Path

def generate_mock_data(filename: str, num_rows: int):
    # Find the root directory (up one level from 'utils/')
    project_root = Path(__file__).resolve().parent.parent
    # define the path
    data_dir = project_root / "data"
    data_dir.mkdir(parents=True, exist_ok=True) # Ensures /data exists
    file_path = data_dir / filename

    header = ["id", "name", "status"]
    try:
        with open(file_path, "w", newline='') as file:
            writer = csv.writer(file)
            writer.writerow(header)
            for i in range(1, num_rows + 1):
                writer.writerow([str(100 + i), f"User_{i}", "active"])
        print(f"Successfully generated {num_rows} rows in {file_path}")
    except Exception as e:
        print(f"Generation failed: {e}")

if __name__ == "__main__":
    generate_mock_data("raw_data.csv", 1000000)