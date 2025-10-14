import pytest

from Agent.agent import APITestPlanAgent
from config import GEMINI_MODEL_NAME


# --- Test Case 1: Test for invalid API key type ---
def test_agent_initialization_with_invalid_key_type():
    with pytest.raises(TypeError, match="API Key must be a string."):
        APITestPlanAgent(api_key=12345, model_name=GEMINI_MODEL_NAME)


# --- Test Case 2: Test for invalid API key length ---
def test_agent_initialization_with_invalid_key_length():
    with pytest.raises(ValueError, match="Invalid API Key"):
        APITestPlanAgent(api_key="short_key", model_name=GEMINI_MODEL_NAME)
