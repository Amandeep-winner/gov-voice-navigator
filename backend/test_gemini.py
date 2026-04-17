import os
from dotenv import load_dotenv

# Load env before importing agent_service
basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.env'))

from app.services.agent_service import AgentService

try:
    print("Testing process_ai_assistant_query...")
    result = AgentService.process_ai_assistant_query("What documents are required for Aadhaar card?")
    print("Result:", result)
except Exception as e:
    import traceback
    traceback.print_exc()
