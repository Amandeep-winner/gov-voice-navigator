from flask import Blueprint, request, jsonify
from app.services.agent_service import AgentService
import json

assistant_bp = Blueprint('assistant_routes', __name__)

@assistant_bp.route('/ai-assistant/query', methods=['POST'])
def handle_assistant_query():
    try:
        data = request.get_json()
        query = data.get('query')
        if not query:
            return jsonify({"error": "Query is required"}), 400
            
        json_string = AgentService.process_ai_assistant_query(query)
        
        try:
            parsed_json = json.loads(json_string)
            return jsonify(parsed_json), 200
        except json.JSONDecodeError:
            print("Failed to parse JSON from Gemini:", json_string)
            return jsonify({"error": "Failed to parse AI response"}), 500
            
    except Exception as e:
        print(f"Error in handle_assistant_query: {e}")
        return jsonify({"error": "Internal server error"}), 500
