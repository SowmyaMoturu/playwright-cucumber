from pathlib import Path
from typing import Dict, List, Optional, Any
import os
import json
import re

class RepoContext:
    def __init__(self, repo_path: str):
        self.repo_path = Path(repo_path)
        self.base_page = self._load_base_page()
        self.page_objects = self._load_page_objects()
        self.step_definitions = self._load_step_definitions()
        self.features = self._load_features()
        self.patterns = self._extract_patterns()

    def _load_base_page(self) -> str:
        """Load BasePage implementation"""
        base_page_path = self.repo_path / 'src' / 'pages' / 'basepage.ts'
        if base_page_path.exists():
            return base_page_path.read_text()
        return ""

    def _load_page_objects(self) -> Dict[str, str]:
        """Load all page objects"""
        page_objects = {}
        page_dir = self.repo_path / 'src' / 'pages'
        if page_dir.exists():
            for file in page_dir.glob('*.ts'):
                if file.name != 'basepage.ts':
                    page_objects[file.stem] = file.read_text()
        return page_objects

    def _load_step_definitions(self) -> Dict[str, str]:
        """Load all step definitions"""
        steps = {}
        steps_dir = self.repo_path / 'src' / 'step-definitions'
        if steps_dir.exists():
            for file in steps_dir.glob('*.ts'):
                steps[file.stem] = file.read_text()
        return steps

    def _load_features(self) -> Dict[str, str]:
        """Load all feature files"""
        features = {}
        feature_dir = self.repo_path / 'src' / 'features'
        if feature_dir.exists():
            for file in feature_dir.glob('*.feature'):
                features[file.stem] = file.read_text()
        return features

    def _extract_patterns(self) -> Dict[str, List[Dict[str, Any]]]:
        """Extract common patterns from codebase"""
        patterns = {
            'response_handling': [],
            'page_objects': [],
            'step_definitions': [],
            'error_handling': []
        }

        # Extract response handling patterns
        for _, content in self.step_definitions.items():
            response_patterns = re.finditer(
                r'(waitForResponse|getResponsePromise).*?\{.*?\}',
                content,
                re.DOTALL
            )
            for match in response_patterns:
                patterns['response_handling'].append({
                    'type': 'response',
                    'pattern': match.group(0).strip()
                })

        # Extract page object patterns
        for name, content in self.page_objects.items():
            locator_patterns = re.finditer(
                r'private\s+readonly\s+locators\s*=\s*\{.*?\};',
                content,
                re.DOTALL
            )
            for match in locator_patterns:
                patterns['page_objects'].append({
                    'type': 'locators',
                    'name': name,
                    'pattern': match.group(0).strip()
                })

        # Extract error handling patterns
        error_patterns = re.finditer(
            r'try\s*\{.*?catch\s*\(.*?\)\s*\{.*?\}',
            self.base_page,
            re.DOTALL
        )
        for match in error_patterns:
            patterns['error_handling'].append({
                'type': 'error',
                'pattern': match.group(0).strip()
            })

        return patterns

    def get_context(self) -> Dict[str, any]:
        """Get structured context from the repo"""
        return {
            "base_page": self.base_page,
            "page_objects": self.page_objects,
            "step_definitions": self.step_definitions,
            "features": self.features,
            "patterns": self.patterns
        }

    def find_similar_examples(self, pattern: str, pattern_type: Optional[str] = None) -> List[Dict[str, str]]:
        """Find similar examples in existing code"""
        examples = []
        
        # If pattern type specified, only search in those patterns
        if pattern_type and pattern_type in self.patterns:
            for p in self.patterns[pattern_type]:
                if pattern.lower() in p['pattern'].lower():
                    examples.append({
                        "type": pattern_type,
                        "pattern": p['pattern']
                    })
            return examples

        # Search in all patterns
        for pattern_type, patterns in self.patterns.items():
            for p in patterns:
                if pattern.lower() in p['pattern'].lower():
                    examples.append({
                        "type": pattern_type,
                        "pattern": p['pattern']
                    })
        
        # Search in step definitions
        for name, content in self.step_definitions.items():
            if pattern.lower() in content.lower():
                examples.append({
                    "type": "step_definition",
                    "file": name,
                    "content": content
                })
        
        # Search in page objects
        for name, content in self.page_objects.items():
            if pattern.lower() in content.lower():
                examples.append({
                    "type": "page_object",
                    "file": name,
                    "content": content
                })
        
        return examples

def load_repo_context(repo_path: str) -> RepoContext:
    """Load repository context"""
    return RepoContext(repo_path)

def find_examples(context: RepoContext, pattern: str, pattern_type: Optional[str] = None) -> List[Dict[str, str]]:
    """Find examples matching a pattern"""
    return context.find_similar_examples(pattern, pattern_type)