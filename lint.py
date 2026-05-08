#!/usr/bin/env python3
"""Linting script to enforce layer architecture and file rules."""

import ast
import sys
from pathlib import Path


# Layer order for dependency checking
LAYERS = ['types', 'config', 'repo', 'service', 'runtime', 'ui', 'providers', 'utils']
LAYER_INDEX = {layer: idx for idx, layer in enumerate(LAYERS)}

# Valid imports for each layer
VALID_IMPORTS = {
    'types': ['types'],
    'config': ['types', 'config'],
    'repo': ['types', 'config', 'repo'],
    'service': ['types', 'config', 'repo', 'providers', 'service'],
    'runtime': ['types', 'config', 'repo', 'service', 'providers', 'runtime'],
    'ui': ['types', 'config', 'service', 'runtime', 'providers', 'ui'],
    'providers': ['types', 'config', 'utils', 'providers'],
    'utils': ['utils'],
}

MAX_LINES = 300
SRC_DIR = Path(__file__).resolve() / 'src'


def get_layer(filepath: Path) -> str | None:
    """Get the layer name for a source file."""
    try:
        rel_path = filepath.relative_to(SRC_DIR)
        parts = rel_path.parts
        if parts:
            return parts[0]
    except ValueError:
        pass
    return None


def get_imports(filepath: Path) -> list[str]:
    """Parse imports from a Python file."""
    imports = []
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        tree = ast.parse(content)
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    imports.append(alias.name.split('.')[0])
            elif isinstance(node, ast.ImportFrom):
                if node.module:
                    imports.append(node.module.split('.')[0])
    except SyntaxError:
        pass
    return imports


def check_file(filepath: Path) -> list[str]:
    """Check a single file for violations."""
    errors = []

    # Check file exists in src/
    try:
        filepath.relative_to(Path(__file__).resolve() / 'src')
    except ValueError:
        return errors  # Not a src file

    layer = get_layer(filepath)
    if layer is None:
        errors.append(f"{filepath}: file not in a layer directory")
        return errors

    # Check line count
    with open(filepath, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    if len(lines) > MAX_LINES:
        errors.append(f"{filepath}:{len(lines)}: file exceeds {MAX_LINES} lines ({len(lines)})")

    # Check imports
    imports = get_imports(filepath)
    valid = VALID_IMPORTS.get(layer, [])
    for imp in imports:
        if imp not in valid:
            errors.append(f"{filepath}: import '{imp}' not allowed in layer '{layer}' (valid: {valid})")

    return errors


def main() -> int:
    """Run all checks."""
    errors = []
    src_dir = Path(__file__).resolve() / 'src'

    # Find all Python files in src/
    for py_file in src_dir.rglob('*.py'):
        file_errors = check_file(py_file)
        errors.extend(file_errors)

    if errors:
        print("Lint violations found:", file=sys.stderr)
        for error in errors:
            print(f"  {error}", file=sys.stderr)
        return 1

    print("All checks passed.")
    return 0


if __name__ == '__main__':
    sys.exit(main())
