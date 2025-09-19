from pathlib import Path

import google.generativeai as genai
from google.api_core import exceptions
import re

PROMPT_FILE = PROMPT_FILE_PATH = Path(__file__).parent / "prompt.txt"
GEMINI_KEY_LENGTH = 39


class APITestPlanAgent:
    def __init__(self, api_key, model_name):
        if not isinstance(api_key, str):
            raise TypeError("API Key must be a string.")

        # A common length for Gemini API keys is 39 characters.
        if len(api_key) != GEMINI_KEY_LENGTH:
            raise ValueError(f"Invalid API Key: Must be 39 characters long, but was {len(api_key)}.")

        genai.configure(api_key=api_key)
        self.model_name = model_name
        self.model = genai.GenerativeModel(self.model_name)

    def generate_plan_for_endpoint(self, endpoint_info,generation_config=None):
        prompt_template = self._load_prompt_template()

        try:
            full_prompt = self._create_full_prompt(endpoint_info, prompt_template)
        except KeyError as e:
            return f"Error: The prompt template is missing a key: {e}"
        try:
            response = self.model.generate_content(full_prompt, generation_config=generation_config)
            formatted_plan = self._format_plan(response.text)
            return formatted_plan
        except (exceptions.GoogleAPICallError, exceptions.RetryError, ValueError) as e:
            return f"Model API error: " + str(e)
        except Exception as e:
            return "Model Error: An unexpected error occurred: " + str(e)

    def _load_prompt_template(self, filepath=PROMPT_FILE):
        try:
            with open(filepath, 'r') as f:
                return f.read()
        except FileNotFoundError:
            return "Generate a test plan for the following API endpoint: {method} {path} - {description}"

    def _create_full_prompt(self, endpoint_info, prompt_template):
        # Injects the endpoint details into the prompt template.
        full_prompt = prompt_template.format(
            method=endpoint_info.get('method', 'N/A'),
            path=endpoint_info.get('path', 'N/A'),
            description=endpoint_info.get('description', 'N/A')
        )
        return full_prompt

    def _format_plan(self, raw_response):
        # Normalize headers (e.g., ### Section Name -> SECTION NAME)
        formatted_text = re.sub(r'###\s*(.*)',
                                lambda m: f"\n{m.group(1).upper().strip()}\n" + "-" * len(m.group(1).strip()),
                                raw_response)
        # Clean up extra newlines and leading/trailing whitespace
        return formatted_text.strip()