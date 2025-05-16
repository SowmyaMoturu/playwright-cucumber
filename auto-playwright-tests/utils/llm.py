import time
from typing import Dict, Any, Optional
from abc import ABC, abstractmethod
from tenacity import retry, stop_after_attempt, wait_fixed

class LLMProvider(ABC):
    @abstractmethod
    def generate_completion(self, prompt: str, **kwargs) -> str:
        """Generate completion from the LLM provider"""
        pass

class LLMHandler:
    def __init__(self, config: Dict[str, Any]):
        """Initialize LLM handler with configuration"""
        self.config = config
        self.provider = self._initialize_provider()
        
    def _initialize_provider(self) -> LLMProvider:
        """Initialize the appropriate LLM provider based on config"""
        provider_name = self.config.get("provider", "openai").lower()
        
        if provider_name == "openai":
            from .openai_provider import OpenAIProvider
            return OpenAIProvider(self.config["openai"])
        elif provider_name == "anthropic":
            from .claude_client import ClaudeProvider
            return ClaudeProvider(self.config["anthropic"])
        elif provider_name == "codey":
            from .codey_client import CodeyProvider
            return CodeyProvider(self.config["codey"])
        else:
            raise ValueError(f"Unsupported LLM provider: {provider_name}")
    
    @retry(
        stop=stop_after_attempt(3),
        wait=wait_fixed(5),
        retry_error_callback=lambda retry_state: retry_state.outcome.result()
    )
    def generate_test(self, prompt: str, **kwargs) -> str:
        """Generate test code using configured LLM provider"""
        try:
            return self.provider.generate_completion(prompt, **kwargs)
        except Exception as e:
            print(f"Error during test generation: {str(e)}")
            raise

    def parse_response(self, response: str) -> Dict[str, str]:
        """Parse the LLM response into separate files"""
        # TODO: Implement smarter response parsing
        files = {}
        current_file = None
        current_content = []
        
        for line in response.split('\n'):
            if line.startswith('```') and len(line) > 3:
                # New file block
                file_info = line[3:].strip()
                if ':' in file_info:
                    current_file = file_info.split(':')[1].strip()
                    current_content = []
            elif line.startswith('```') and current_file:
                # End of file block
                files[current_file] = '\n'.join(current_content)
                current_file = None
            elif current_file:
                current_content.append(line)
        
        return files if files else {"test.spec.ts": response} 