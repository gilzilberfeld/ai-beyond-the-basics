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

# --- Test Case 3: Test end-to-end performance benchmark ---
def test_controller_e2e_performance_benchmark(client):
    import time
    from config import TEST_TIMEOUT

    start_time = time.time()
    client.post('/generate-plan', json={
        "method": "GET",
        "path": "/posts",
        "description": "Get all posts"
    })
    end_time = time.time()

    duration = end_time - start_time
    print(f"End-to-end request took {duration:.2f} seconds.")

    assert duration < TEST_TIMEOUT