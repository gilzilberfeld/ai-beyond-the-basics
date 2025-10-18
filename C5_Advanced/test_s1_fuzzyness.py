import google.generativeai as genai
from Agent.agent import APITestPlanAgent
from config import GEMINI_API_KEY, GEMINI_MODEL_NAME

def test_fuzzy_quality_difference():
    agent = APITestPlanAgent(api_key=GEMINI_API_KEY, model_name=GEMINI_MODEL_NAME)
    endpoint = {"method": "GET", "path": "/users/{id}"}

    # Generate a plan with low "temperature" (more predictable)
    config_a = genai.types.GenerationConfig(temperature=0.2)
    plan_a = agent.generate_plan_for_endpoint(endpoint, generation_config=config_a).lower()

    # Generate a plan with high "temperature" (more "creative"/random)
    config_b = genai.types.GenerationConfig(temperature=0.9)
    plan_b = agent.generate_plan_for_endpoint(endpoint, generation_config=config_b).lower()


    print("\n--- PLAN A (Low Temperature) ---")
    print(plan_a)
    print("\n--- PLAN B (High Temperature) ---")
    print(plan_b)

    # Both plans are structurally valid, so these checks will pass
    assert "happy path" in plan_a and "happy path" in plan_b
    assert "unhappy path" in plan_a and "unhappy path" in plan_b