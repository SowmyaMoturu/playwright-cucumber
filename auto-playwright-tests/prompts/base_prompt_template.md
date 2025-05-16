# Test Generation Instructions

## Framework Configuration
```yaml
framework: {{framework}}  # e.g., 'playwright', 'selenium', 'cypress'
language: {{language}}    # e.g., 'typescript', 'javascript', 'python'
project_structure: |
  {{project_structure}}   # Describe your project's folder structure
```

## Test Requirements

1. Framework-Specific Patterns:
   {{framework_patterns}}  # Add your framework's specific patterns and best practices

2. Response Handling:
   {{response_handling}}   # Describe how to handle API responses in your framework

3. Test Structure:
   {{test_structure}}     # Define how tests should be structured

4. Assertions:
   {{assertions}}         # Specify assertion patterns and best practices

5. Page Objects/Components:
   {{components}}         # Define how to use page objects or components

6. Error Handling:
   {{error_handling}}     # Specify error handling patterns

## Example Patterns

### API Mocking:
```{{language}}
{{api_mock_example}}
```

### Assertions:
```{{language}}
{{assertion_example}}
```

### Page Object Usage:
```{{language}}
{{page_object_example}}
```

## Additional Requirements:
{{additional_requirements}}  # Add any project-specific requirements 