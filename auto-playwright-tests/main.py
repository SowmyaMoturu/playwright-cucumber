from pathlib import Path
import argparse
import yaml
from typing import Dict, Any
from utils.llm import LLMHandler
from utils.instruction_processor import process_instructions

class TestGenerator:
    """Prompt-based test generator"""
    
    def __init__(self, config_path: Path):
        self.config_path = config_path
        self.config = self._load_config()
        self.llm_handler = LLMHandler(self.config)
    
    def _load_config(self) -> Dict[str, Any]:
        """Load configuration from config file"""
        with open(self.config_path / 'config.yaml') as f:
            return yaml.safe_load(f)
    
    def _load_base_prompt(self) -> str:
        """Load and validate base prompt"""
        base_prompt_path = Path(self.config["base_prompt_file"])
        if not base_prompt_path.exists():
            raise FileNotFoundError(f"Base prompt file not found: {base_prompt_path}")
        return base_prompt_path.read_text()
    
    def generate_tests(self, instructions_file: Path, output_dir: Path):
        """Generate tests based on instructions"""
        # Load test instructions
        with open(instructions_file) as f:
            instructions = yaml.safe_load(f)
        
        # Load base prompt
        base_prompt = self._load_base_prompt()
        
        # Process instructions into a format matching base prompt
        processed_instructions = process_instructions(instructions_file)
        
        # Build complete prompt
        prompt = f"{base_prompt}\n\nTest Instructions:\n{processed_instructions}"
        
        # Generate test code using LLM
        print("Generating tests using LLM...")
        response = self.llm_handler.generate_test(prompt)
        
        # Parse and save generated files
        output_dir.mkdir(parents=True, exist_ok=True)
        for filename, content in self.llm_handler.parse_response(response).items():
            output_file = output_dir / filename
            output_file.write_text(content)
            print(f"✓ Generated test file: {output_file}")

def main():
    parser = argparse.ArgumentParser(description="Generate tests using LLM")
    parser.add_argument(
        "--instructions",
        type=str,
        required=True,
        help="Path to test instructions file (YAML format)"
    )
    parser.add_argument(
        "--output",
        type=str,
        default="generated_tests",
        help="Output directory for generated tests"
    )
    parser.add_argument(
        "--config",
        type=str,
        default="config",
        help="Path to configuration directory"
    )
    
    args = parser.parse_args()
    
    try:
        generator = TestGenerator(Path(args.config))
        generator.generate_tests(
            Path(args.instructions),
            Path(args.output)
        )
        print("\n✓ Test generation completed successfully")
        
    except Exception as e:
        print(f"\n❌ Error during test generation: {str(e)}")
        raise

if __name__ == "__main__":
    main()


    