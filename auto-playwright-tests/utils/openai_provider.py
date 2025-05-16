import time
from typing import Dict, List, Any
from openai import OpenAI
from .llm import LLMProvider

class OpenAIProvider(LLMProvider):
    def __init__(self, config: Dict[str, Any]):
        """Initialize OpenAI provider with configuration"""
        self.config = config
        self.client = OpenAI(api_key=config["api_key"])
        self.model = config.get("model", "gpt-4-turbo-preview")
        self.max_tokens = config.get("max_tokens", 4000)
        self.temperature = config.get("temperature", 0.2)
        self.timeout = config.get("request_timeout", 300)
        self.retry_delay = config.get("retry_delay", 5)

    def generate_completion(self, prompt: str, **kwargs) -> str:
        """Generate completion using OpenAI API"""
        try:
            response = self.client.chat.completions.create(
                model=kwargs.get("model", self.model),
                messages=[
                    {"role": "system", "content": "You are a test automation expert specializing in Playwright with TypeScript and Cucumber."},
                    {"role": "user", "content": prompt}
                ],
                temperature=kwargs.get("temperature", self.temperature),
                max_tokens=kwargs.get("max_tokens", self.max_tokens),
                timeout=kwargs.get("timeout", self.timeout)
            )
            
            return response.choices[0].message.content
            
        except Exception as e:
            if "rate_limit" in str(e).lower():
                print("Rate limit reached, waiting before retry...")
                time.sleep(self.retry_delay)
            raise Exception(f"Error calling OpenAI API: {str(e)}")

    def generate_completions(self, prompts: List[str], **kwargs) -> List[str]:
        """Generate multiple completions"""
        return [self.generate_completion(prompt, **kwargs) for prompt in prompts] 