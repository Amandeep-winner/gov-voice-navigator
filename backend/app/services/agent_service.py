import os
import google.generativeai as genai
from qdrant_client import QdrantClient
from qdrant_client.http import models

# Configure the Gemini API using the environment variable
# Make sure to run: export GEMINI_API_KEY="your-api-key"
genai.configure(api_key=os.environ.get("GEMINI_API_KEY"))

# Initialize Qdrant Client pointing to the local instance
# Adjust host/port if necessary
try:
    qdrant_client = QdrantClient(host="localhost", port=6333)
except Exception as e:
    print(f"Warning: Failed to initialize Qdrant client: {e}")
    qdrant_client = None

class AgentService:
    """
    Agent service layer handling the core logic for the Vapi custom tools.
    Integrates Qdrant for RAG and Google Gemini API for synthesis.
    """
    
    # Collection names for Qdrant - adjust if your actual names differ
    GOV_DOCS_COLLECTION = "gov_documents"
    LEGAL_RIGHTS_COLLECTION = "legal_rights"
    SCHEMES_COLLECTION = "schemes"

    @classmethod
    def generate_embedding(cls, text: str) -> list[float]:
        """
        Generates an embedding for a specific query text using text-embedding-004.
        """
        try:
            # We use task_type="RETRIEVAL_QUERY" for optimal vector search performance
            response = genai.embed_content(
                model="models/text-embedding-004",
                content=text,
                task_type="RETRIEVAL_QUERY"
            )
            return response['embedding']
        except Exception as e:
            print(f"Error generating embedding: {e}")
            raise

    @classmethod
    def search_gov_documents(cls, query: str) -> str:
        """
        Feature 1: Search Qdrant for document requirements and synthesize an answer.
        """
        try:
            if not qdrant_client:
                return "The database is currently disconnected."

            # Generate query embedding
            query_vector = cls.generate_embedding(query)
            
            # Retrieve from Vector DB using limit parameter
            search_results = qdrant_client.search(
                collection_name=cls.GOV_DOCS_COLLECTION,
                query_vector=query_vector,
                limit=3
            )
            
            if not search_results:
                return "I couldn't find any documents matching your request."
            
            # Combine the retrieved payloads (assuming the document text is stored in 'content')
            context = " ".join([hit.payload.get("content", "") for hit in search_results])
            
            # Synthesize answer using gemini-flash-latest
            model = genai.GenerativeModel('gemini-flash-latest')
            prompt = (
                f"Based on the following document context, explain the requirements for "
                f"the user's query '{query}'. Keep your answer concise, spoken-friendly, "
                f"and easy to understand over voice. Do not output markdown.\n\nContext: {context}"
            )
            response = model.generate_content(prompt)
            
            return response.text
        except Exception as e:
            print(f"Error in search_gov_documents: {e}")
            return "I'm having trouble fetching that document information right now."

    @classmethod
    def search_legal_rights(cls, situation: str) -> str:
        """
        Feature 2: Search Qdrant for emergency legal rights and synthesize an answer.
        """
        try:
            if not qdrant_client:
                return "The database is currently disconnected."

            # Generate query embedding
            query_vector = cls.generate_embedding(situation)
            
            # Retrieve from Vector DB using limit parameter
            search_results = qdrant_client.search(
                collection_name=cls.LEGAL_RIGHTS_COLLECTION,
                query_vector=query_vector,
                limit=3
            )
            
            if not search_results:
                return "I couldn't find any specific legal rights for this situation."
                
            # Combine the retrieved payloads
            context = " ".join([hit.payload.get("content", "") for hit in search_results])
            
            # Synthesize answer using gemini-flash-latest
            model = genai.GenerativeModel('gemini-flash-latest')
            prompt = (
                f"The user is in the following emergency situation: '{situation}'. "
                f"Based on the provided legal context, clearly and concisely state their "
                f"emergency legal rights in a conversational, reassuring tone suitable for voice output. "
                f"Do not output markdown.\n\nContext: {context}"
            )
            response = model.generate_content(prompt)
            
            return response.text
        except Exception as e:
            print(f"Error in search_legal_rights: {e}")
            return "There was an issue retrieving the legal rights for this situation at the moment."

    @classmethod
    def match_schemes(cls, age: int, income: float, occupation: str) -> str:
        """
        Feature 3: Accept a user profile, search Qdrant for matching schemes, 
        and generate a dynamic comparison of the top 3.
        """
        try:
            if not qdrant_client:
                return "The database is currently disconnected."

            # Create a synthetic description of the profile to query the semantic database
            query = f"Government schemes and financial benefits for a {age} year old {occupation} with an annual income of {income}."
            query_vector = cls.generate_embedding(query)
            
            # Fetch a pool of schemes
            search_results = qdrant_client.search(
                collection_name=cls.SCHEMES_COLLECTION,
                query_vector=query_vector,
                limit=5
            )
            
            if not search_results:
                return "I couldn't find any schemes that immediately match your profile."
            
            # Provide the top 3 items to Gemini to compare
            top_results = search_results[:3]
            context = " ".join([hit.payload.get("content", "") for hit in top_results])
            
            # Synthesize comparison using gemini-flash-latest
            model = genai.GenerativeModel('gemini-flash-latest')
            prompt = (
                f"You are a helpful government AI assistant speaking over a phone call. "
                f"The user profile is: Age: {age}, Income: {income}, Occupation: {occupation}. "
                f"Based on the context retrieved from the database, identify the top 3 most relevant "
                f"schemes for their specific profile. Present a spoken-friendly comparison of these top 3 schemes. "
                f"Highlight the benefits simply and clearly so they can choose the best one. Do not output markdown.\n\n"
                f"Context: {context}"
            )
            
            response = model.generate_content(prompt)
            return response.text
        except Exception as e:
            print(f"Error in match_schemes: {e}")
            return "I apologize, but I encountered an error while trying to find matching schemes for you."

    @classmethod
    def compare_schemes(cls, scheme_names: list[str]) -> str:
        """
        Feature 8: Compare specific schemes.
        """
        try:
            if not qdrant_client:
                return "The database is currently disconnected."
            
            contexts = []
            for name in scheme_names:
                query_vector = cls.generate_embedding(name)
                results = qdrant_client.search(
                    collection_name=cls.SCHEMES_COLLECTION,
                    query_vector=query_vector,
                    limit=1
                )
                if results:
                    contexts.append(results[0].payload.get("content", ""))
            
            if not contexts:
                return "I couldn't find information on those specific schemes."
                
            model = genai.GenerativeModel('gemini-flash-latest')
            prompt = (
                f"Compare the following schemes based on efficiency, convenience, and benefits. "
                f"Keep it conversational and easy to understand over voice. No markdown.\n\n"
                f"Context: {' '.join(contexts)}"
            )
            return model.generate_content(prompt).text
        except Exception as e:
            print(f"Error in compare_schemes: {e}")
            return "I couldn't compare those schemes right now."

    @classmethod
    def resolve_rejection(cls, application_type: str, rejection_reason: str = "") -> str:
        """
        Feature 11: Help if application rejected.
        """
        try:
            query = f"Rejected application for {application_type}. Reason: {rejection_reason}"
            query_vector = cls.generate_embedding(query)
            
            if not qdrant_client:
                return "Database disconnected."

            # Search in gov docs or legal rights
            results = qdrant_client.search(
                collection_name=cls.GOV_DOCS_COLLECTION,
                query_vector=query_vector,
                limit=2
            )
            context = " ".join([hit.payload.get("content", "") for hit in results])
            
            model = genai.GenerativeModel('gemini-flash-latest')
            prompt = (
                f"The user's application for {application_type} was rejected. "
                f"Reason: {rejection_reason}. Based on the context, provide steps to correct "
                f"their application, helplines to call, or how to resolve it. Conversational, no markdown.\n\n"
                f"Context: {context}"
            )
            return model.generate_content(prompt).text
        except Exception as e:
            print(f"Error in resolve_rejection: {e}")
            return "I'm having trouble fetching resolution steps at the moment."

    @classmethod
    def renew_document(cls, document_type: str, action: str) -> str:
        """
        Feature 9: Renew/Remake lost documents.
        """
        try:
            query = f"How to {action} my {document_type}"
            query_vector = cls.generate_embedding(query)
            
            if not qdrant_client:
                return "Database disconnected."

            results = qdrant_client.search(
                collection_name=cls.GOV_DOCS_COLLECTION,
                query_vector=query_vector,
                limit=2
            )
            context = " ".join([hit.payload.get("content", "") for hit in results])
            
            model = genai.GenerativeModel('gemini-flash-latest')
            prompt = (
                f"The user wants to {action} their {document_type}. "
                f"Based on the context, explain the required steps and documents. "
                f"Speak naturally, no markdown.\n\nContext: {context}"
            )
            return model.generate_content(prompt).text
        except Exception as e:
            print(f"Error in renew_document: {e}")
            return "I couldn't find the information to update that document."

    @classmethod
    def process_ai_assistant_query(cls, query: str) -> str:
        """
        Process a query for the standalone AI Assistant and return structured JSON.
        """
        try:
            model = genai.GenerativeModel('gemini-flash-latest')
            prompt = (
                "You are an assistant that provides accurate information about Indian government documents.\n"
                "Always respond in structured JSON format with the following fields:\n"
                "- document_name\n"
                "- required_documents (array)\n"
                "- application_process (array of steps)\n"
                "- office_to_visit\n"
                "- additional_notes\n"
                "- related_documents (array of strings: suggest 2-3 other related documents the user might need)\n\n"
                "Ensure the answer is clear, concise, and relevant to India.\n"
                "Do not include any extra text outside JSON, no markdown formatting (like ```json), just the raw JSON string.\n\n"
                f"User Query: {query}"
            )
            response = model.generate_content(prompt)
            # Remove markdown backticks if Gemini includes them
            text = response.text.strip()
            if text.startswith("```json"):
                text = text[7:]
            if text.startswith("```"):
                text = text[3:]
            if text.endswith("```"):
                text = text[:-3]
            return text.strip()
        except Exception as e:
            print(f"Error in process_ai_assistant_query: {e}")
            return '{"error": "Failed to process query"}'

