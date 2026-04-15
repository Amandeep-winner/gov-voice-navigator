import os
from dotenv import load_dotenv
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct
import google.generativeai as genai

load_dotenv()

# Initialize Qdrant Client
qdrant = QdrantClient(url=os.getenv("QDRANT_URL", "http://localhost:6333"))

# Configure Gemini API
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# Define Collections based on categories
COLLECTIONS = ["gov_documents", "legal_rights", "schemes"]
VECTOR_SIZE = 768  # Gemini text-embedding-004 uses 768 dimensions

def setup_collections():
    for collection in COLLECTIONS:
        qdrant.recreate_collection(
            collection_name=collection,
            vectors_config=VectorParams(size=VECTOR_SIZE, distance=Distance.COSINE),
        )
        print(f"Recreated collection: {collection} with dimension {VECTOR_SIZE}")

def get_embedding(text):
    result = genai.embed_content(
        model="models/text-embedding-004",
        content=text,
        task_type="RETRIEVAL_DOCUMENT" 
    )
    return result['embedding']

def seed_database():
    mock_data = [
        # Gov Documents
        {
            "collection": "gov_documents",
            "id": 1,
            "payload": {
                "title": "Aadhaar Card Address Update",
                "category": "update",
                "content": "To update your Aadhaar card address or phone number, you need an Address Proof like a passport, bank statement, or utility bill. You can apply online via the UIDAI portal."
            }
        },
        {
            "collection": "gov_documents",
            "id": 2,
            "payload": {
                "title": "Applying for a New Passport",
                "category": "new",
                "content": "For a new passport, visit the Passport Seva Kendra. Required documents: Address proof (Aadhaar/Utility bill), Date of Birth proof (Birth certificate/10th mark sheet)."
            }
        },
        {
            "collection": "gov_documents",
            "id": 3,
            "payload": {
                "title": "Lost PAN Card Remake",
                "category": "lost",
                "content": "If you lost your PAN card, you must apply for a reprint on the NSDL or UTIITSL website. Provide your PAN number and an Aadhaar copy. A nominal fee is required. File an FIR if it was stolen."
            }
        },
        {
            "collection": "gov_documents",
            "id": 4,
            "payload": {
                "title": "Passport Application Rejected",
                "category": "rejection",
                "content": "If your passport application is rejected due to address mismatch, submit an updated utility bill or bank statement. You can book another appointment without paying the fee again within a year. Call helpline 1800-258-1800."
            }
        },
        # Legal Rights
        {
            "collection": "legal_rights",
            "id": 5,
            "payload": {
                "title": "Police Demanding Bribe",
                "category": "extortion",
                "content": "If a police officer demands a bribe, refuse it. It is illegal under the Prevention of Corruption Act. Immediately call the Anti-Corruption Bureau (ACB) helpline (1064) or the state vigilance commission."
            }
        },
        {
            "collection": "legal_rights",
            "id": 6,
            "payload": {
                "title": "Arbitrary Police Stop and Search",
                "category": "emergency",
                "content": "You have the right to know why you are being stopped. Police cannot search your vehicle or person without a warrant or reasonable suspicion of a crime. Ask for their ID if they are not in uniform."
            }
        },
        # Schemes
        {
            "collection": "schemes",
            "id": 7,
            "payload": {
                "title": "PM Kisan Samman Nidhi",
                "category": "agriculture",
                "occupation": "farmer",
                "efficiency": 8,
                "chances": 9,
                "content": "Income support of 6000 rupees/year to farmer families. Best for immediate financial aid. Documents needed: Aadhaar, Bank Details, Land records. Very efficient payout via Direct Benefit Transfer."
            }
        },
        {
            "collection": "schemes",
            "id": 8,
            "payload": {
                "title": "Startup India Seed Fund",
                "category": "business",
                "occupation": "businessman",
                "efficiency": 7,
                "chances": 5,
                "content": "Provides financial assistance to startups for proof of concept and prototype development. High benefit but strict selection. Requires a DPIIT recognized startup certificate."
            }
        },
        {
            "collection": "schemes",
            "id": 9,
            "payload": {
                "title": "PMMY (Mudra Yojana)",
                "category": "business",
                "occupation": "businessman",
                "efficiency": 9,
                "chances": 8,
                "content": "Loans up to 10 Lakhs for non-corporate micro-enterprises. Great for new businessmen. Easier to get than Seed Fund. Needs project report, ID proof, address proof."
            }
        },
        {
            "collection": "schemes",
            "id": 10,
            "payload": {
                "title": "National Means Cum Merit Scholarship",
                "category": "education",
                "occupation": "student",
                "efficiency": 8,
                "chances": 7,
                "content": "Scholarship for economically weaker students passing 8th grade. Requires income certificate showing income < 3.5 Lakhs. Documents: caste certificate, disability certificate (if applicable)."
            }
        }
    ]

    for item in mock_data:
        # We embed the content, but keep payload intact for metadata filtering and details
        vector = get_embedding(item["payload"]["content"])
        qdrant.upsert(
            collection_name=item["collection"],
            points=[
                PointStruct(
                    id=item["id"],
                    vector=vector,
                    payload=item["payload"]
                )
            ]
        )
    print("Database seeded successfully with richer mock data!")

if __name__ == "__main__":
    setup_collections()
    seed_database()