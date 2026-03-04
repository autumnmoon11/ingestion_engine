import os
from openai import AzureOpenAI
from dotenv import load_dotenv

# Load variables from a .env file for security
load_dotenv()

class AzureEmbeddingClient:
    def __init__(self):
        # Initialize the client using environment variables
        self.client = AzureOpenAI(
            api_key=os.getenv("AZURE_OPENAI_API_KEY"),  
            api_version="2024-02-01", # Standard stable version
            azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT")
        )
        self.deployment_name = os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME")

    def get_embedding(self, text: str):
        """
        Converts a string of text into a list of floats (vector).
        """
        # Clean the text (AI models don't like newlines in embeddings)
        text = text.replace("\n", " ")
        
        response = self.client.embeddings.create(
            input=[text],
            model=self.deployment_name
        )
        
        # The actual vector is hidden inside the response object
        return response.data[0].embedding

if __name__ == "__main__":
    # Quick Test
    client = AzureEmbeddingClient()
    sample_vector = client.get_embedding("This is a test for the ingestion engine.")
    print(f"Vector Length: {len(sample_vector)}")
    print(f"First 5 values: {sample_vector[:5]}")