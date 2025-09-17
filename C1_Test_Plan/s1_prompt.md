You are an expert QA Strategist. Your task is to create a comprehensive test plan for a new AI-powered service.

The service has two main components:
1.  **A Python `APITestPlanAgent` class:**
    * It takes an API endpoint's information (method, path, description).
    * It uses a text file (`prompt.txt`) as a template.
    * It calls a Large Language Model (LLM) to generate a test plan.
    * It formats the raw text from the LLM into a clean, readable string.
2.  **A Flask `controller`:**
    * It exposes a single `/generate-plan` API endpoint.
    * It expects a JSON payload with the API endpoint info.
    * It handles requests, calls the `APITestPlanAgent`, and returns the plan.
    * It includes error handling for bad requests, missing data, and agent failures.

Based on this, generate a list of test cases. Organize them into the following categories:
-   **Controller & API Tests (Black Box):** Testing the service from the outside.
-   **Agent Unit Tests (White Box):** Testing the internal logic of the agent's code.
-   **AI Quality & Content Tests:** Testing the actual output from the LLM.
-   **Performance & Reliability Tests:** Testing the non-functional aspects of the service.

