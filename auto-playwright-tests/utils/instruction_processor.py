import yaml
import csv
from pathlib import Path
from typing import Dict, List, Any
import json

class InstructionProcessor:
    def __init__(self, instruction_file: str, test_data_path: str | None = None):
        """
        Initialize instruction processor
        
        Args:
            instruction_file: Path to instruction file (YAML or CSV)
            test_data_path: Optional path to test data file
        """
        self.instruction_file = Path(instruction_file)
        self.instructions = self._load_instructions()
        self.test_data = self._load_json(test_data_path) if test_data_path else None

    def _load_instructions(self) -> Dict[str, Any]:
        """Load instructions from file (YAML or CSV)"""
        if self.instruction_file.suffix.lower() == '.csv':
            return self._load_csv(str(self.instruction_file))
        else:
            return self._load_yaml(str(self.instruction_file))

    def _load_csv(self, path: str) -> Dict[str, Any]:
        """Load and process CSV file directly"""
        with open(path, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            rows = list(reader)
            
        instructions = {
            "feature_name": Path(path).stem,
            "steps": []
        }
        
        for row in rows:
            step = {
                "step": row["step_description"],
                "api_interceptions": [],
                "validations": [],
                "test_data": {}
            }
            
            # Process optional API interceptions
            if row.get("api_endpoint") and row.get("api_method"):
                interception = {
                    "endpoint": row["api_endpoint"],
                    "method": row["api_method"],
                    "status": int(row.get("api_status", "200")),
                    "response_key": row.get("response_key", ""),
                }
                if row.get("response_template"):
                    interception["response_template"] = row["response_template"]
                step["api_interceptions"].append(interception)
            
            # Process optional validations
            if row.get("validation_type") and row.get("validation_value"):
                validation = {
                    "type": row["validation_type"],
                    "value": row["validation_value"]
                }
                if row.get("validation_selector"):
                    validation["selector"] = row["validation_selector"]
                if row.get("validation_assertion"):
                    validation["assertion"] = row["validation_assertion"]
                step["validations"].append(validation)
            
            # Process optional test data
            if row.get("test_data_source"):
                step["test_data"]["source"] = row["test_data_source"]
                if row.get("test_data_field"):
                    step["test_data"]["field"] = row["test_data_field"]
            
            instructions["steps"].append(step)
            
        return instructions

    def _load_yaml(self, path: str) -> Dict[str, Any]:
        """Load YAML file"""
        with open(path, 'r') as f:
            return yaml.safe_load(f)

    def _load_json(self, path: str) -> Dict[str, Any]:
        """Load JSON test data file"""
        with open(path, 'r') as f:
            return json.load(f)

    def _resolve_template_variables(self, template: str) -> str:
        """Replace {{variable}} placeholders with actual values"""
        if not self.test_data:
            return template
            
        # TODO: Implement variable resolution from test_data and world object references
        return template

    def _format_api_interception(self, interception: Dict[str, Any]) -> str:
        """Format a single API interception instruction"""
        response = interception.get('response_template', '{}')
        if isinstance(response, str):
            response = self._resolve_template_variables(response)

        return f"""await page.route('{interception['endpoint']}', async (route) => {{
  const response = {response};
  await route.fulfill({{ 
    status: {interception['status']},
    json: response 
  }});
  world.saveResponse('{interception['response_key']}', response);
}});"""

    def _format_validation(self, validation: Dict[str, Any]) -> str:
        """Format a single validation instruction"""
        if validation['type'] == 'url':
            expected = self._resolve_template_variables(validation['value'])
            return f"expect(page.url()).toContain('{expected}');"
        elif validation['type'] == 'element':
            value = self._resolve_template_variables(validation['value'])
            return f"""await expect(page.locator('{validation['selector']}')).{validation['assertion']}('{value}');"""
        return ""

    def generate_instructions(self) -> str:
        """Generate formatted instructions from the template"""
        instructions = [f"# Additional Instructions for: {self.instructions['feature_name']}\n"]

        # Add global interceptions
        if self.instructions.get('global_interceptions'):
            instructions.append("## Global API Interceptions")
            instructions.append("```typescript")
            for interception in self.instructions['global_interceptions']:
                instructions.append(self._format_api_interception(interception))
            instructions.append("```\n")

        # Add step-specific instructions
        instructions.append("## Step-specific Instructions")
        for step in self.instructions['steps']:
            instructions.append(f"\n### Step: {step['step']}")

            # Add API interceptions
            if step.get('api_interceptions'):
                instructions.append("\nAPI Interceptions:")
                instructions.append("```typescript")
                for interception in step['api_interceptions']:
                    instructions.append(self._format_api_interception(interception))
                instructions.append("```")

            # Add test data
            if step.get('test_data') and step['test_data'].get('source'):
                instructions.append("\nTest Data:")
                instructions.append(f"Use value from: {step['test_data']['source']}")

            # Add validations
            if step.get('validations'):
                instructions.append("\nValidations:")
                instructions.append("```typescript")
                for validation in step['validations']:
                    instructions.append(self._format_validation(validation))
                instructions.append("```")

        return "\n".join(instructions)

def process_instructions(instruction_file: str, test_data_path: str | None = None) -> str:
    """Process instruction file (YAML or CSV) and return formatted instructions"""
    processor = InstructionProcessor(instruction_file, test_data_path)
    return processor.generate_instructions() 