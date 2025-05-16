import os
import json
import requests
from typing import Dict, List, Optional, Union
from .llm import LLMProvider

class ClaudeProvider(LLMProvider):
    def __init__(self, config: Dict[str, any]):
        """Initialize Claude provider with configuration"""
        self.api_key = config["api_key"]
        self.base_url = "https://api.anthropic.com/v1/messages"
        self.model = config.get("model", "claude-3-sonnet-20240229")
        self.max_tokens = config.get("max_tokens", 4096)
        self.temperature = config.get("temperature", 0.2)
        self.headers = {
            "x-api-key": self.api_key,
            "anthropic-version": "2023-06-01",
            "content-type": "application/json"
        }

    def generate_completion(self, prompt: str, **kwargs) -> str:
        """Generate completion using Claude API"""
        try:
            data = {
                "model": kwargs.get("model", self.model),
                "max_tokens": kwargs.get("max_tokens", self.max_tokens),
                "temperature": kwargs.get("temperature", self.temperature),
                "messages": [
                    {"role": "system", "content": "You are a test automation expert specializing in Playwright with TypeScript and Cucumber."},
                    {"role": "user", "content": prompt}
                ]
            }
            
            response = requests.post(
                self.base_url,
                headers=self.headers,
                json=data,
                timeout=kwargs.get("timeout", 60)
            )
            response.raise_for_status()
            
            return response.json()["content"][0]["text"]
            
        except requests.exceptions.Timeout:
            raise Exception("Claude API request timed out")
        except requests.exceptions.RequestException as e:
            raise Exception(f"Claude API request failed: {str(e)}")
        except KeyError as e:
            raise Exception(f"Unexpected Claude API response format: {str(e)}")
        except Exception as e:
            raise Exception(f"Error calling Claude API: {str(e)}")

    def generate_completions(self, prompts: List[str], **kwargs) -> List[str]:
        """Generate multiple completions"""
        return [self.generate_completion(prompt, **kwargs) for prompt in prompts] 