import os
import uuid

import requests
from flask import Blueprint, jsonify, request

from app.services.agent_service import AgentService

vapi_bp = Blueprint('vapi_routes', __name__)

@vapi_bp.route('/api/vapi/agent', methods=['POST'])
def vapi_agent():
    """
    Webhook endpoint for Vapi.ai custom tool calling.
    Vapi automatically sends a POST request here with the tool call payload.
    """
    try:
        # Parse incoming JSON payload from Vapi
        payload = request.json
        if not payload:
            return jsonify({"error": "No JSON payload provided"}), 400

        # Check if this is indeed a tool call event
        message_type = payload.get("message", {}).get("type")
        if message_type != "toolCalls":
            # If it's another kind of message, acknowledge gracefully
            return jsonify({"status": "acknowledged"}), 200

        tool_calls = payload.get("message", {}).get("toolCalls", [])
        if not tool_calls:
            return jsonify({"error": "No tool calls found"}), 400

        # Initialize responses array (Vapi expects an array of results)
        responses = []

        # Process each tool call in the array (often just one)
        for tool_call in tool_calls:
            tool_call_id = tool_call.get("id")
            function_info = tool_call.get("function", {})
            func_name = function_info.get("name")
            arguments = function_info.get("arguments", {})

            result_text = "I'm sorry, I didn't understand the request."

            try:
                # Dynamically route to the correct method based on function.name
                if func_name == "search_gov_documents":
                    query = arguments.get("query", "")
                    result_text = AgentService.search_gov_documents(query)

                elif func_name == "search_legal_rights":
                    situation = arguments.get("situation", "")
                    result_text = AgentService.search_legal_rights(situation)

                elif func_name == "match_schemes":
                    age = arguments.get("age", 0)
                    income = float(arguments.get("income", 0.0))
                    occupation = arguments.get("occupation", "")
                    result_text = AgentService.match_schemes(age, income, occupation)
                    
                elif func_name == "compare_schemes":
                    scheme_names = arguments.get("scheme_names", [])
                    result_text = AgentService.compare_schemes(scheme_names)

                elif func_name == "resolve_rejection":
                    application_type = arguments.get("application_type", "")
                    rejection_reason = arguments.get("rejection_reason", "")
                    result_text = AgentService.resolve_rejection(application_type, rejection_reason)

                elif func_name == "renew_document":
                    document_type = arguments.get("document_type", "")
                    action = arguments.get("action", "")
                    result_text = AgentService.renew_document(document_type, action)

                else:
                    print(f"Unknown function called: {func_name}")
                    result_text = f"I cannot handle the requested operation: {func_name}."

            except Exception as func_err:
                print(f"Error executing {func_name}: {func_err}")
                result_text = "There was an internal error pulling this information."

            # Append formatted dictionary mapping tool call ID to the execution result
            responses.append({
                "toolCallId": tool_call_id,
                "result": result_text
            })

        # Return the exact JSON wrapper expected by Vapi
        return jsonify({"results": responses}), 200

    except Exception as e:
        print(f"Top level exception in vapi_agent webhook: {e}")
        # Provide a safe fallback voice response
        fallback_id = "unknown"
        if request.json and isinstance(request.json, dict):
            calls = request.json.get("message", {}).get("toolCalls", [])
            if calls and len(calls) > 0:
                fallback_id = calls[0].get("id", "unknown")
                
        return jsonify({
             "results": [
                {
                    "toolCallId": fallback_id,
                    "result": "I am experiencing technical difficulties at the moment."
                }
            ]
        }), 500


@vapi_bp.route('/start-call', methods=['POST'])
def start_call():
    """
    Create a NEW Vapi call session every time the user clicks "Start Voice".

    Returns the identifiers required for the Vapi Web SDK to join the new session.
    """
    try:
        data = request.get_json(silent=True) or {}

        # IMPORTANT: do not reuse call ids; always create a fresh server-side call.
        assistant_id = (
            data.get("assistantId")
            or data.get("assistant_id")
            or os.getenv("VAPI_ASSISTANT_ID")
        )
        if not assistant_id:
            return jsonify({"error": "Missing assistantId (request body or VAPI_ASSISTANT_ID)"}), 400

        # Vapi web calls are authenticated with the public web key.
        # Allow the frontend to pass it explicitly, since this is already a public key.
        vapi_public_key = (
            data.get("publicKey")
            or data.get("public_key")
            or os.getenv("VAPI_PUBLIC_KEY")
            or os.getenv("VITE_VAPI_PUBLIC_KEY")
        )
        if not vapi_public_key:
            return jsonify(
                {
                    "error": "Missing Vapi public key for web call creation",
                    "hint": "Provide `publicKey` in the request body or set VAPI_PUBLIC_KEY on backend",
                }
            ), 500

        # Vapi web-call creation.
        # IMPORTANT: browser sessions must use /call/web, not /call (phone calls).
        create_payload = {
            "assistantId": assistant_id,
            # Keep the room alive long enough for the client to connect/reconnect cleanly.
            "roomDeleteOnUserLeaveEnabled": False,
            "metadata": {
                "source": "gov-voice-navigator-web",
                "sessionId": str(uuid.uuid4()),
            },
        }

        headers = {
            "Authorization": f"Bearer {vapi_public_key}",
            "Content-Type": "application/json",
        }

        resp = requests.post(
            "https://api.vapi.ai/call/web",
            json=create_payload,
            headers=headers,
            timeout=30,
        )
        if not resp.ok:
            # Keep response details for debugging without leaking secrets.
            return jsonify(
                {
                    "error": "Vapi call creation failed",
                    "status": resp.status_code,
                    "details": resp.text,
                }
            ), resp.status_code

        payload = resp.json()

        # Response shape can vary; extract defensively.
        call_id = (
            payload.get("id")
            or (payload.get("call") or {}).get("id")
            or (payload.get("data") or {}).get("id")
        )
        web_call_url = (
            payload.get("webCallUrl")
            or (payload.get("webCall") or {}).get("webCallUrl")
            or (payload.get("transport") or {}).get("callUrl")
            or (payload.get("call") or {}).get("webCallUrl")
        )

        if not call_id or not web_call_url:
            return jsonify(
                {
                    "error": "Vapi create call succeeded but response was missing call identifiers",
                    "received": {
                        "call_id": call_id,
                        "web_call_url": web_call_url,
                    },
                    # Avoid returning the full payload; it can be large.
                }
            ), 500

        return jsonify({"call_id": call_id, "webCallUrl": web_call_url}), 200

    except Exception as e:
        return jsonify({"error": "Unexpected error creating Vapi call", "details": str(e)}), 500