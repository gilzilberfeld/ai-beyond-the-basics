import requests

AGENT_URL = "http://127.0.0.1:5001/generate-plan"

sample_endpoint_data = {
    "method": "GET",
    "path": "/users/{id}",
    "description": "Get a user by ID"
}

# --- Test Case 1: Check for Factual Correctness (Anti-Hallucination) ---
def test_plan_does_not_hallucinate_actions():
    plan = get_live_plan(sample_endpoint_data)
    assert "delete" not in plan
    assert "post" not in plan
    assert "update" not in plan

# --- Test Case 2: Check for Correct Categorization ---
def test_plan_categorizes_tests_correctly():
    plan = get_live_plan(sample_endpoint_data)

    happy_path_index = plan.find("happy path")
    unhappy_path_index = plan.find("unhappy path")
    invalid_keyword_index = plan.find("invalid")

    if invalid_keyword_index != -1 and happy_path_index != -1 and unhappy_path_index != -1:
        # Unhappy "includes" invalid
        assert invalid_keyword_index > unhappy_path_index
        # Happy before unhappy
        assert unhappy_path_index > happy_path_index

def get_live_plan(endpoint_data):
    response = requests.post(AGENT_URL, json=endpoint_data)
    response.raise_for_status()  # Raise an exception for bad status codes (4xx or 5xx)
    return response.json()['plan'].lower()
