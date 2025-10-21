from unittest.mock import patch

from google.api_core import exceptions

from Agent.agent import APITestPlanAgent
from C2_Developer_Tests.common import VALID_FAKE_KEY
from config import GEMINI_MODEL_NAME


@patch('Agent.agent.genai.GenerativeModel.generate_content',
       side_effect=exceptions.GoogleAPICallError("Model is unavailable"))
def test_agent_handles_model_api_error_gracefully(mock_generate_content):
    agent = APITestPlanAgent(api_key=VALID_FAKE_KEY,
                             model_name=GEMINI_MODEL_NAME)
    endpoint_info = {"method": "GET", "path": "/test"}
    result = agent.generate_plan_for_endpoint(endpoint_info)
    assert "API error" in result

@patch('Agent.agent.genai.GenerativeModel.generate_content')
def test_agent_handles_empty_model_response(mock_generate_content):
    mock_generate_content.return_value.text = ""
    agent = APITestPlanAgent(api_key=VALID_FAKE_KEY, model_name=GEMINI_MODEL_NAME)
    result = agent.generate_plan_for_endpoint({"method": "GET", "path": "/data"})
    assert "Error: The AI model returned an empty plan" in result