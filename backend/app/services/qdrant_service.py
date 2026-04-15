import os
from qdrant_client import QdrantClient
import google.generativeai as genai

class QdrantService:
    def __init__(self):
        self.qdrant = QdrantClient(url=os.getenv("QDRANT_URL", "http://localhost:6333"))
        
        # Configure the Gemini API client
        genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

    def get_embedding(self, text):
        # Generate the embedding using Gemini
        result = genai.embed_content(
            model="models/text-embedding-004",
            content=text,
            task_type="RETRIEVAL_QUERY"  # Optimizes the embedding specifically for search
        )
        return result['embedding']

    def search_knowledge_base(self, query: str, category: str = "gov_documents"):
        try:
            query_vector = self.get_embedding(query)
            
            search_result = self.qdrant.search(
                collection_name=category,
                query_vector=query_vector,
                limit=1  # Return the single best match for voice output
            )

            if not search_result:
                return "I couldn't find any specific rules regarding that in the database."

            return search_result[0].payload.get('content', "No content available.")
            
        except Exception as e:
            print(f"Qdrant Search Error: {e}")
            return "I am currently unable to access the government records."