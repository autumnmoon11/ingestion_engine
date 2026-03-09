import json
import numpy as np
from pathlib import Path
from utils.ai_utils import AzureEmbeddingClient

class SemanticSearcher:
    def __init__(self, data_path: Path):
        self.data_path = data_path
        self.ai_client = AzureEmbeddingClient()

    def _cosine_similarity(self, v1, v2):
        """Calculates the mathematical closeness of two vectors."""
        return np.dot(v1, v2) / (np.linalg.norm(v1) * np.linalg.norm(v2))

    def search(self, query: str, top_n: int = 3):
        # Convert the user's question into a vector
        print(f"🔍 Searching for: '{query}'...")
        query_vector = self.ai_client.get_embedding(query)
        
        results = []
        
        # Stream through the JSONL data, maintaining memory efficiency
        with open(self.data_path, "r", encoding="utf-8") as f:
            for line in f:
                row = json.loads(line)
                if "embedding" in row:
                    # Explicitly convert the stored list to a float array
                    item_vector = np.array(row["embedding"], dtype=float)
                    # Compare query vector to row vector
                    score = self._cosine_similarity(query_vector, item_vector)
                    results.append((score, row))
        
        # Sort by highest similarity score
        results.sort(key=lambda x: x[0], reverse=True)
        return results[:top_n]

if __name__ == "__main__":
    output_file = Path("data/output.jsonl")
    
    if not output_file.exists():
        print(f"❌ Error: {output_file} not found. Run main.py first!")
    else:
        searcher = SemanticSearcher(output_file)
        
        # Example test question
        user_query = "Are there any reports of battery issues?"
        matches = searcher.search(user_query)
        
        print("\n--- Top Semantic Matches ---")
        for score, row in matches:
            print(f"[Score: {score:.4f}] Product: {row['Product']}")
            print(f"Review: {row['Review_Text']}\n")