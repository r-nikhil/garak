import json
import requests
import logging
from typing import List, Union
from garak.generators.base import Generator

class CustomPolicyGenerator(Generator):
    def __init__(self, api_url: str, api_key: str, policy_id: str, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.api_url = api_url
        self.api_key = api_key
        self.policy_id = policy_id

    def _call_model(self, prompt: str, generations_this_call: int = 1) -> List[Union[str, None]]:
        headers = {
            "Content-Type": "application/json",
            "Authorization": "Bearer " + self.api_key,
        }

        data = {
            "messages": [
                {
                    "role": "user",
                    "content": prompt,
                }
            ],
            "textType": "MODEL_INPUT",
            "policyIds": [self.policy_id],
        }

        try:
            response = requests.post(self.api_url, headers=headers, json=data, timeout=100)
            response.raise_for_status()
            response_content = response.json()
            violated = response_content['appliedPolicies'][0]['violated']
            return [str(violated)]
        except requests.exceptions.RequestException as e:
            logging.error(f"Request failed: {e}")
            return [None]
        except json.JSONDecodeError as e:
            logging.error(f"Failed to decode JSON from response: {response.text}, error: {e}")
            return [None]
        except Exception as e:
            logging.error(f"Unexpected error processing response: {e}")
            return [None]