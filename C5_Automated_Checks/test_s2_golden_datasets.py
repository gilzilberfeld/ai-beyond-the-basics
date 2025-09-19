import requests

AGENT_URL = "http://127.0.0.1:5001/generate-plan"

sample_endpoint_data = {
    "method": "GET",
    "path": "/users/{id}",
    "description": "Get a user by ID containing personal data"
}

# --- Test Case 1 (PASS): Check against the initial Golden Dataset ---
def test_plan_meets_initial_quality_bar():
    plan = get_live_plan(sample_endpoint_data)

    has_happy_path = "valid" in plan or "existing" in plan
    has_unhappy_path = "invalid" in plan or "non-existent" in plan

    assert has_happy_path and has_unhappy_path, "Plan must cover both happy and unhappy paths."

# --- Test Case 2 (FAIL): Check against the stricter Golden Dataset ---
def test_plan_fails_stricter_quality_bar():
    plan = get_live_plan(sample_endpoint_data)

    # The new, stricter requirement
    mentions_security = "security" in plan or "sensitive" in plan or "password" in plan
    assert mentions_security, "Plan is missing critical security and data privacy test cases."

def get_live_plan(endpoint_data):
    response = requests.post(AGENT_URL, json=endpoint_data)
    response.raise_for_status()  # Raise an exception for bad status codes (4xx or 5xx)
    return response.json()['plan'].lower()