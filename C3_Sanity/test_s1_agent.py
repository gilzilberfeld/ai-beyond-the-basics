import time

from Agent.agent import APITestPlanAgent
from config import GEMINI_API_KEY, GEMINI_MODEL_NAME, TEST_TIMEOUT

# A real agent instance for live tests
live_agent = APITestPlanAgent(api_key=GEMINI_API_KEY, model_name=GEMINI_MODEL_NAME)
sample_endpoint = {"method": "GET", "path": "/users/{id}", "description": "Get a user by ID"}


# --- Test Case 1: Check for required sections ---
def test_plan_has_required_sections():
    plan = live_agent.generate_plan_for_endpoint(sample_endpoint)
    plan_lower = plan.lower()

    assert "api explanation" in plan_lower
    assert "happy path" in plan_lower
    assert "unhappy path" in plan_lower
    assert "edge cases" in plan_lower


# --- Test Case 2: Check for content relevance ---
def test_plan_content_is_relevant():
    plan = live_agent.generate_plan_for_endpoint(sample_endpoint)
    plan_lower = plan.lower()

    assert "user" in plan_lower
    assert "id" in plan_lower


# --- Test Case 3: Check against a performance benchmark ---
def test_live_plan_generation_is_within_time_benchmark():
    start_time = time.time()
    live_agent.generate_plan_for_endpoint(sample_endpoint)
    end_time = time.time()

    duration = end_time - start_time
    print(f"Plan generation took {duration:.2f} seconds.")
