from unittest.mock import patch

import pytest
from Agent.controller import app


@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client


# --- Test Case 1: Test for missing data in request ---
def test_controller_handles_missing_data(client):
    response = client.post('/generate-plan', json={"method": "GET"})  # Missing 'path'

    assert response.status_code == 400
    assert b"Missing required field" in response.data


# --- Test Case 2: Test controller handling of agent/model errors ---
@patch('Agent.controller.agent.generate_plan_for_endpoint')
def test_controller_handles_agent_error(mock_generate_plan, client):
    # Configure the mock to return an error message, simulating an AI failure
    mock_generate_plan.return_value = "Error: Could not generate the plan due to an API error."

    response = client.post('/generate-plan', json={
        "method": "GET",
        "path": "/posts",
        "description": "Get all posts"
    })

    assert response.status_code == 500
    assert b"Error: Could not generate the plan" in response.data


# --- Test Case 3: Test that the controller returns the correct JSON structure on success
@patch('Agent.controller.agent.generate_plan_for_endpoint')
def test_controller_returns_correct_json_structure(mock_generate_plan, client):
    mock_generate_plan.return_value = "This is a valid test plan."
    response = client.post('/generate-plan', json={
        "method": "GET",
        "path": "/posts",
        "description": "A test"
    })

    assert response.status_code == 200
    json_data = response.get_json()
    assert "plan" in json_data
    assert json_data["plan"] == "This is a valid test plan."