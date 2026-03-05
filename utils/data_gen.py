import csv
import random
from pathlib import Path

REVIEWS = [
    "The battery life on these headphones is incredible, lasted all week.",
    "Extremely disappointed with the build quality, it broke after two days.",
    "Great value for the price, the sound is crisp and clear.",
    "The connection keeps dropping when I walk into another room.",
    "Best purchase I've made this year, highly recommend to everyone!"
]

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


def generate_semantic_data(file_path: Path, row_count=1000):
    headers = ["ID", "Product", "Review_Text", "Category"]
    
    with open(file_path, mode='w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(headers)
        
        for i in range(row_count):
            writer.writerow([
                f"{i:08}",
                random.choice(["Phone", "Laptop", "Headphones", "Watch"]),
                random.choice(REVIEWS),
                random.choice(["Electronics", "Accessories"])
            ])
    print(f"Generated {row_count} semantic rows at {file_path}")


if __name__ == "__main__":
    project_root = Path(__file__).resolve().parent.parent
    data_path = project_root / "data" / "semantic_data.csv"
    
    # Generate 10 rows for safe, low-cost AI testing
    generate_semantic_data(data_path, row_count=10)