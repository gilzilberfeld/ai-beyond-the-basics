from unittest.mock import patch

from Agent.agent import APITestPlanAgent
from C2_Unit_Tests.common import VALID_FAKE_KEY
from config import GEMINI_MODEL_NAME


# --- Test Case 1: Validate the prompt creation logic ---
def test_full_prompt_formats_correctly():
    agent = APITestPlanAgent(api_key=VALID_FAKE_KEY, model_name=GEMINI_MODEL_NAME)
    endpoint_info = {
        "method": "GET",
        "path": "/users",
        "description": "Get a list of users"
    }
    prompt_template = "Test for {method} at {path}: {description}"
    full_prompt = agent._create_full_prompt(endpoint_info, prompt_template)
    assert full_prompt == "Test for GET at /users: Get a list of users"

# --- Test Cases 2 & 3: Validate the plan formatting logic ---
def test_format_plan_with_valid_markdown_formats_correctly():
    agent = APITestPlanAgent(api_key=VALID_FAKE_KEY, model_name=GEMINI_MODEL_NAME)
    raw_response = (
        "### API Explanation\nThis is a test.\n"
        "### Happy Path\n- Test case 1\n"
    )
    formatted_plan = agent._format_plan(raw_response)
    assert "API EXPLANATION" in formatted_plan
    assert "---------------" in formatted_plan
    assert "This is a test." in formatted_plan
    assert "HAPPY PATH" in formatted_plan
    assert "- Test case 1" in formatted_plan


def test_format_plan_with_messy_markdown_formats_correctly():
    agent = APITestPlanAgent(api_key=VALID_FAKE_KEY, model_name=GEMINI_MODEL_NAME)
    raw_response = (
        "### API Explanation### Happy Path- Test case 1"
    )
    formatted_plan = agent._format_plan(raw_response)

    assert "API EXPLANATION" in formatted_plan
    assert "HAPPY PATH" in formatted_plan
    assert "- TEST CASE 1" in formatted_plan


# --- Test Case 4: Unit test of the public method ---
@patch('Agent.agent.genai.GenerativeModel.generate_content')  # Mocks the actual call to the AI model
def test_generate_plan_for_endpoint_with_mock_model(mock_generate_content):
    # Configure the mock to return a fake AI response object
    class MockResponse:
        def __init__(self, text):
            self.text = text

    mock_generate_content.return_value = MockResponse("### API Explanation\nMocked explanation.")

    agent = APITestPlanAgent(api_key=VALID_FAKE_KEY, model_name=GEMINI_MODEL_NAME)
    endpoint_info = {"method": "POST", "path": "/login"}
    final_plan = agent.generate_plan_for_endpoint(endpoint_info)
    print (final_plan)
    assert "API EXPLANATION" in final_plan
    assert "Mocked explanation." in final_plan