import requests
import json

# The URL of your locally running Flask controller
AGENT_URL = "http://127.0.0.1:5001/generate-plan"

# The endpoint info we want to generate a plan for
ENDPOINT_INFO = {
    "method": "GET",
    "path": "/users/{id}",
    "description": "Get a user by their unique ID."
}


def generate_low_quality_plan():
    """
    Calls the running controller to generate a test plan using the
    original, less-specific prompt.txt.
    """
    print("--------------------------------------------------")
    print(f"Calling the agent for: {ENDPOINT_INFO['method']} {ENDPOINT_INFO['path']}")
    print("--------------------------------------------------")

    try:
        response = requests.post(AGENT_URL, json=ENDPOINT_INFO, timeout=30)

        # Check if the request was successful
        response.raise_for_status()

        # Parse the JSON and print just the test plan
        data = response.json()
        if "plan" in data:
            print(data["plan"])
        else:
            print("Error: 'plan' key not found in the response.")
            print("Full response:", data)

    except requests.exceptions.RequestException as e:
        print(f"\n--- ERROR ---")
        print(f"Could not connect to the controller at {AGENT_URL}")
        print("Please make sure the controller.py server is running in a separate terminal.")
        print(f"Details: {e}")
    except json.JSONDecodeError:
        print("\n--- ERROR ---")
        print("Failed to decode the JSON response from the server.")
        print("Raw response:", response.text)


if __name__ == "__main__":
    generate_low_quality_plan()
