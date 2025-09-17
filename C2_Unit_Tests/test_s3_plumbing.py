from unittest.mock import patch

import pytest
from google.api_core import exceptions

from Agent.agent import APITestPlanAgent
from C2_Unit_Tests.common import VALID_FAKE_KEY
from config import GEMINI_MODEL_NAME


# --- Test Case 1: Test for invalid API key type ---
def test_agent_initialization_with_invalid_key_type():
    with pytest.raises(TypeError, match="API Key must be a string."):
        APITestPlanAgent(api_key=12345, model_name=GEMINI_MODEL_NAME)


# --- Test Case 2: Test for invalid API key length ---
def test_agent_initialization_with_invalid_key_length():
    with pytest.raises(ValueError, match="Invalid API Key"):
        APITestPlanAgent(api_key="short_key", model_name=GEMINI_MODEL_NAME)


# --- Test Case 3: Test for invalid API key length ---
@patch('Agent.agent.genai.GenerativeModel.generate_content',
       side_effect=exceptions.GoogleAPICallError("Model is unavailable"))
def test_agent_handles_model_api_error_gracefully(mock_generate_content):
    # Use a valid key to ensure the agent initializes correctly
    agent = APITestPlanAgent(api_key=VALID_FAKE_KEY,
                             model_name=GEMINI_MODEL_NAME)
    endpoint_info = {"method": "GET", "path": "/test"}
    result = agent.generate_plan_for_endpoint(endpoint_info)
    assert "API error" in result
