from typing import List, Optional, Dict, Any
from langchain_google_vertexai import VertexAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from .llm import LLMProvider

class CodeyProvider(LLMProvider):
    def __init__(self, config: Dict[str, Any]):
        """
        Initialize Codey provider with configuration
        
        Args:
            config: Configuration dictionary containing:
                - project_id: GCP project ID
                - location: GCP region (default: us-central1)
                - max_output_tokens: Maximum tokens in response (default: 1024)
                - temperature: Temperature for generation (default: 0.2)
        """
        self.project_id = config["project_id"]
        self.location = config.get("location", "us-central1")
        self.max_output_tokens = config.get("max_output_tokens", 1024)
        self.temperature = config.get("temperature", 0.2)
        
        self.llm = VertexAI(
            model_name="code-bison",
            project=self.project_id,
            location=self.location,
            max_output_tokens=self.max_output_tokens,
            temperature=self.temperature
        )

    def generate_completion(self, prompt: str, **kwargs) -> str:
        """Generate completion using Codey"""
        try:
            # Create prompt template with system prompt
            template = """You are a test automation expert specializing in Playwright with TypeScript and Cucumber.

{user_input}"""
            
            prompt_template = PromptTemplate(
                template=template,
                input_variables=["user_input"]
            )
            
            # Create chain
            chain = LLMChain(llm=self.llm, prompt=prompt_template)
            
            # Get prediction
            return chain.predict(user_input=prompt)
            
        except Exception as e:
            raise Exception(f"Error calling Codey API: {str(e)}")

    def generate_completions(self, prompts: List[str], **kwargs) -> List[str]:
        """Generate multiple completions"""
        return [self.generate_completion(prompt, **kwargs) for prompt in prompts] 