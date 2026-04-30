# MIT License
#
# Copyright (c) 2026 jmfrohs
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import json
import os
import sys

import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from generators.common import (
    generate_dockerfile,
    generate_dockerignore,
    generate_eslint_config,
    generate_flake8_config,
    generate_gitignore,
    generate_github_ci,
    generate_gitlab_ci,
    generate_license,
    generate_prettier_config,
    generate_pylint_config,
    generate_readme,
)

class TestGenerateGitignore:
    def test_common_entries_present(self):
        result = generate_gitignore("javascript")
        assert "node_modules/" in result
        assert ".DS_Store" in result

    def test_python_entries(self):
        result = generate_gitignore("python")
        assert "__pycache__/" in result
        assert "*.pyc" in result
        assert "venv/" in result

    def test_python_entries_not_in_js(self):
        result = generate_gitignore("javascript")
        assert "__pycache__/" not in result

class TestGenerateLicense:
    def test_mit_contains_author(self):
        result = generate_license("MIT", "Alice")
        assert "Alice" in result
        assert "MIT License" in result

    def test_apache_contains_author(self):
        result = generate_license("Apache-2.0", "Bob")
        assert "Bob" in result
        assert "Apache License" in result

    def test_gpl_contains_author(self):
        result = generate_license("GPL-3.0", "Carol")
        assert "Carol" in result
        assert "GNU General Public License" in result

    def test_unknown_license_fallback(self):
        result = generate_license("WTFPL", "Dave")
        assert "Dave" in result

    def test_year_is_2026(self):
        result = generate_license("MIT", "X")
        assert "2026" in result

class TestGenerateGithubCi:
    def test_js_contains_node_setup(self):
        result = generate_github_ci("javascript", "18", "jest", "npm")
        assert "actions/setup-node" in result
        assert "18" in result
        assert "npm install" in result

    def test_py_contains_python_setup(self):
        result = generate_github_ci("python", "3.11", "pytest", None)
        assert "actions/setup-python" in result
        assert "3.11" in result
        assert "pytest" in result

    def test_js_default_version(self):
        result = generate_github_ci("javascript", None, "jest", "npm")
        assert "18" in result

    def test_py_default_version(self):
        result = generate_github_ci("python", None, "pytest", None)
        assert "3.11" in result

class TestGenerateGitlabCi:
    def test_js_image_node(self):
        result = generate_gitlab_ci("javascript", "18", "jest", "npm")
        assert "image: node:18" in result
        assert "npm install" in result

    def test_py_image_python(self):
        result = generate_gitlab_ci("python", "3.11", "pytest", None)
        assert "image: python:3.11" in result
        assert "pytest" in result

    def test_js_default_version(self):
        result = generate_gitlab_ci("javascript", None, "jest", "npm")
        assert "node:18" in result

    def test_py_default_version(self):
        result = generate_gitlab_ci("python", None, "pytest", None)
        assert "python:3.11" in result

class TestGenerateDockerfile:
    def test_js_dockerfile(self):
        result = generate_dockerfile("javascript", "18", "index.js")
        assert "FROM node:18-alpine" in result
        assert "index.js" in result

    def test_py_dockerfile(self):
        result = generate_dockerfile("python", "3.11", "main.py")
        assert "FROM python:3.11-slim" in result
        assert "main.py" in result

    def test_js_default_version(self):
        result = generate_dockerfile("javascript", None, "index.js")
        assert "node:18" in result

    def test_py_default_version(self):
        result = generate_dockerfile("python", None, "main.py")
        assert "python:3.11" in result

class TestGenerateDockerignore:
    def test_common_entries(self):
        result = generate_dockerignore("javascript")
        assert ".git" in result
        assert "README.md" in result

    def test_js_entries(self):
        result = generate_dockerignore("javascript")
        assert "node_modules/" in result

    def test_py_entries(self):
        result = generate_dockerignore("python")
        assert "__pycache__/" in result
        assert "venv/" in result

    def test_py_entries_not_in_js(self):
        result = generate_dockerignore("javascript")
        assert "venv/" not in result

class TestLinterConfigs:
    def test_eslint_is_valid_json(self):
        result = generate_eslint_config()
        parsed = json.loads(result)
        assert "rules" in parsed

    def test_flake8_max_line_length(self):
        result = generate_flake8_config()
        assert "max-line-length = 88" in result

    def test_pylint_max_line_length(self):
        result = generate_pylint_config()
        assert "max-line-length=88" in result

class TestPrettierConfig:
    def test_is_valid_json(self):
        result = generate_prettier_config()
        parsed = json.loads(result)
        assert "tabWidth" in parsed

    def test_default_indent_size(self):
        result = generate_prettier_config()
        parsed = json.loads(result)
        assert parsed["tabWidth"] == 2

    def test_custom_indent_size(self):
        result = generate_prettier_config(4)
        parsed = json.loads(result)
        assert parsed["tabWidth"] == 4

    def test_contains_expected_keys(self):
        result = generate_prettier_config()
        parsed = json.loads(result)
        assert "semi" in parsed
        assert "singleQuote" in parsed
        assert "printWidth" in parsed

class TestGenerateReadme:
    def test_project_name_in_readme(self):
        result = generate_readme(
            "MyApp",
            "javascript",
            "Alice",
            "A desc",
            "1.0.0",
            "MIT",
            "18",
            "jest",
            "npm",
        )
        assert "MyApp" in result

    def test_author_in_readme(self):
        result = generate_readme(
            "MyApp", "javascript", "Alice", "", "1.0.0", "MIT", "18", "jest", "npm"
        )
        assert "Alice" in result

    def test_description_in_readme(self):
        result = generate_readme(
            "MyApp",
            "python",
            "Alice",
            "My description",
            "1.0.0",
            "MIT",
            "3.11",
            "pytest",
            None,
        )
        assert "My description" in result

    def test_no_empty_description_line(self):
        result = generate_readme(
            "MyApp", "python", "Alice", "", "1.0.0", "MIT", "3.11", "pytest", None
        )
        assert "\n\n\n" not in result
