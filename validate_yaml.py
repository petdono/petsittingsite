#!/usr/bin/env python3
"""
Simple YAML validation for docker-compose files
"""

import re

def validate_docker_compose(file_path):
    """Basic validation of docker-compose.yml structure"""
    try:
        with open(file_path, 'r') as f:
            content = f.read()

        # Check for basic structure - more flexible
        if 'version:' not in content[:100]:  # Check first 100 chars
            return False, "File must contain 'version:' declaration"

        if 'services:' not in content:
            return False, "File must contain 'services:' section"

        # Check for common YAML issues
        lines = content.split('\n')
        indent_stack = []

        for i, line in enumerate(lines, 1):
            stripped = line.strip()
            if not stripped or stripped.startswith('#'):
                continue

            # Count leading spaces
            indent = len(line) - len(line.lstrip())

            # Check for inconsistent indentation (allow 2 or 4 spaces)
            if indent > 0 and indent % 2 != 0:
                return False, f"Line {i}: Inconsistent indentation (use 2 or 4 spaces)"

            # Check for missing colons in key-value pairs
            if ':' not in line and not line.strip().startswith('-') and not stripped.startswith('version'):
                return False, f"Line {i}: Missing colon or not a list item"

        return True, "YAML structure looks valid"

    except Exception as e:
        return False, f"Error reading file: {e}"

if __name__ == "__main__":
    valid, message = validate_docker_compose('docker-compose.yml')
    if valid:
        print("✅ docker-compose.yml validation passed")
    else:
        print(f"❌ Validation failed: {message}")