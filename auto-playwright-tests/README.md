# Playwright-Cucumber Test Generator

An intelligent test automation framework that generates Playwright-Cucumber tests using LLM integration. The framework supports multiple LLM providers (OpenAI, Claude, Codey) and provides flexible test instruction formats.

## Features

- 🤖 **Multi-LLM Support**:
  - OpenAI (GPT-4)
  - Anthropic (Claude)
  - Google Vertex AI (Codey)
  
- 📝 **Flexible Test Instructions**:
  - CSV format for easy maintenance
  - YAML format for complex scenarios
  - Markdown format for detailed instructions
  
- 🔄 **API Mocking & Response Handling**:
  - Automatic API interception
  - Response template support
  - Dynamic response generation
  - State management via World object
  
- 🧪 **Test Data Management**:
  - JSON-based test data
  - Environment-specific overrides
  - Variable resolution in templates
  
- 📊 **Page Object Pattern**:
  - Base page with common utilities
  - Typed interfaces
  - Reusable components
  - Best practice selectors

## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
npm install
```

2. Configure environment variables:
Create a `.env` file with your preferred LLM provider settings:

```env
# OpenAI Configuration
OPENAI_API_KEY=your_api_key_here
OPENAI_MODEL=gpt-4-turbo-preview
OPENAI_TEMPERATURE=0.2

# Claude Configuration (Optional)
CLAUDE_API_KEY=your_claude_key_here
CLAUDE_MODEL=claude-3-sonnet-20240229

# Codey Configuration (Optional)
GOOGLE_APPLICATION_CREDENTIALS=path/to/credentials.json
CODEY_PROJECT_ID=your_project_id
```

## Usage

### 1. Using CSV Instructions

Create a CSV file with test steps:
```csv
step_description,api_endpoint,api_method,api_status,response_key,validation_type,validation_value
"Given I am on the login page",,,,,,url,/login
"When I enter my email",,,,,,element,input[data-testid='email']
```

Generate tests:
```bash
python main.py --instructions path/to/steps.csv --output generated_tests
```

### 2. Using YAML Instructions

For more complex scenarios, use YAML format:
```bash
python main.py --instructions path/to/instructions.yaml --output generated_tests
```

### 3. With Test Data

```bash
python main.py --instructions path/to/steps.csv --test-data path/to/test_data.json --output generated_tests
```

## Directory Structure

```
auto-playwright-tests/
├── config/                 # Configuration files
│   ├── config.yaml        # Main configuration
│   └── instruction_schema.yaml
├── examples/              # Example files
│   ├── login.feature
│   ├── step_instructions_template.csv
│   └── testdata/
├── prompts/              # LLM prompts
│   └── base_prompt.md
├── src/                  # Generated test files
│   ├── features/
│   ├── pages/
│   └── step-definitions/
└── utils/               # Framework utilities
    ├── instruction_processor.py
    ├── llm.py
    └── repo_loader.py
```

## Test Generation Process

1. **Instruction Processing**:
   - Parse CSV/YAML instructions
   - Load test data if provided
   - Process templates and variables

2. **LLM Integration**:
   - Combine base prompt with instructions
   - Generate test code using configured LLM
   - Parse and validate response

3. **Test File Generation**:
   - Create necessary directories
   - Generate feature files
   - Generate step definitions
   - Generate page objects

## Best Practices

1. **API Mocking**:
   - Use `world.saveResponse()` for storing responses
   - Set up interceptors before actions
   - Use typed interfaces for responses

2. **Page Objects**:
   - Use data-testid attributes
   - Implement reusable actions
   - Extend BasePage for common utilities

3. **Test Data**:
   - Use environment-specific data
   - Maintain type safety
   - Follow naming conventions

4. **Error Handling**:
   - Implement proper retries
   - Add descriptive messages
   - Take failure screenshots

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

MIT License - see LICENSE file for details