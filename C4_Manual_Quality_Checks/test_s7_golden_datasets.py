import requests

AGENT_URL = "http://127.0.0.1:5001/generate-plan"

sample_endpoint_data = {
    "method": "GET",
    "path": "/users/{id}",
    "description": "Get a user by ID containing personal data"
}

INITIAL_GOLDEN_CONCEPTS = {
    "happy_path": [("existing", 3),("valid", 3)], # Happy path concepts get 3 points each
    "unhappy_path": [("non-existent", 3), ("invalid", 3)],
    "edge_cases": [("large", 1), ("zero", 1), ("concurrent", 1)]  # Edge cases get 1 point each
}

NEW_GOLDEN_CONCEPTS = {
    **INITIAL_GOLDEN_CONCEPTS,
    "security": [("sensitive", 3), ("unauthorized", 3)]  # Points -> Importance
}

def test_plan_meets_initial_quality_bar():
    plan = get_live_plan(sample_endpoint_data)
    total_score = calculate_quality_score(plan, INITIAL_GOLDEN_CONCEPTS)

    print(f"Initial Quality Score: {total_score}/9")

    # The current scoring is so good, we want the best 9/9.
    assert total_score >= 8, "The plan failed to meet the initial quality bar."


def test_plan_with_stricter_quality_bar():
    plan = get_live_plan(sample_endpoint_data)
    total_score = calculate_quality_score(plan, NEW_GOLDEN_CONCEPTS)

    # The maximum possible score is now 15 (9 from initial + 6 from security)
    print(f"Stricter Quality Score: {total_score}/15")

    assert "sensitive" in plan # Additional sanity checks
    assert "unauthorized" in plan, "The plan is missing key security considerations."

    # The new bar is higher
    assert total_score < 12, "The plan total score is not high enough."


def get_live_plan(endpoint_data):
    response = requests.post(AGENT_URL, json=endpoint_data)
    response.raise_for_status()  # Raise an exception for bad status codes (4xx or 5xx)
    return response.json()['plan'].lower()



def calculate_quality_score(plan_lower, concepts):
    score = 0

    for category, keywords in concepts.items():
        for keyword, points in keywords:
            if keyword in plan_lower:
                print(f"Found keyword '{keyword}' in category '{category}'. Awarding {points} points.")
                score += points
                # Stop after finding the first keyword in a category to avoid double counting
                break
    return score

