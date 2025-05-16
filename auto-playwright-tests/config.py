from pathlib import Path
from typing import Dict, Any
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

DEFAULT_CONFIG = {
    "base_prompt_file": "prompts/base_prompt.md",
    "output_dir": "src/tests",
    "page_objects_dir": "src/pages",
    "step_definitions_dir": "src/step-definitions",
    "features_dir": "src/features",
    "openai": {
        "api_key": os.getenv("OPENAI_API_KEY"),
        "model": os.getenv("OPENAI_MODEL", "gpt-4-turbo-preview"),
        "temperature": float(os.getenv("OPENAI_TEMPERATURE", "0.7")),
        "max_tokens": int(os.getenv("OPENAI_MAX_TOKENS", "4000")),
        "request_timeout": int(os.getenv("OPENAI_TIMEOUT", "300")),
        "retry_attempts": int(os.getenv("OPENAI_RETRY_ATTEMPTS", "3")),
        "retry_delay": int(os.getenv("OPENAI_RETRY_DELAY", "5"))
    }
}

def load_config(config_path: str | Path | None = None) -> Dict[str, Any]:
    """Load configuration with defaults"""
    config = DEFAULT_CONFIG.copy()
    
    if config_path:
        # Here you could add custom config loading if needed
        pass
    
    # Validate required settings
    if not config["openai"]["api_key"]:
        raise ValueError("OpenAI API key not found. Please set OPENAI_API_KEY environment variable.")
        
    return config 