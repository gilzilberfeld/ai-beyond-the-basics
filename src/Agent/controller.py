from flask import Flask, request, jsonify
from Agent.agent import APITestPlanAgent
from config import GEMINI_API_KEY, GEMINI_MODEL_NAME

app = Flask(__name__)

try:
    agent = APITestPlanAgent(api_key=GEMINI_API_KEY, model_name=GEMINI_MODEL_NAME)
except (TypeError, ValueError) as e:
    print(f"FATAL: Could not initialize agent. Check your config.py and .env file. Error: {e}")
    agent = None


@app.route('/generate-plan', methods=['POST'])
def generate_plan():
    if not agent:
        return jsonify({"error": "Agent is not configured correctly. Check server logs."}), 500

    body_data = request.get_json()
    if not body_data:
        return jsonify({"error": "Invalid request: Missing JSON body."}), 400

    required_fields = ['method', 'path', 'description']
    missing_fields = [field for field in required_fields if field not in body_data]
    if missing_fields:
        return jsonify({"error": f"Missing required field(s): {', '.join(missing_fields)}"}), 400

    plan = agent.generate_plan_for_endpoint(body_data)

    if plan.startswith("Error:"):
        return jsonify({"error": plan}), 500

    return jsonify({"plan": plan}), 200


if __name__ == '__main__':
    app.run(debug=True, port=5001)