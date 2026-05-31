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

import os
import sys

import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from generators.scripts import (
    generate_format_licenses_java,
    generate_format_licenses_py,
    generate_makefile,
    generate_start_test_server_py,
)

class TestGenerateMakefile:
    def test_pytest_command(self):
        result = generate_makefile("MyProject", "main.py", "pytest", None)
        assert "python -m pytest" in result

    def test_unittest_command(self):
        result = generate_makefile("MyProject", "main.py", "unittest", None)
        assert "python -m unittest discover" in result

    def test_lint_target_included(self):
        result = generate_makefile("MyProject", "main.py", "pytest", "flake8")
        assert "lint" in result
        assert "flake8" in result

    def test_no_lint_target_when_none(self):
        result = generate_makefile("MyProject", "main.py", "pytest", None)
        assert "\nlint:" not in result

    def test_phony_targets(self):
        result = generate_makefile("MyProject", "main.py", "pytest", None)
        assert ".PHONY" in result

class TestGenerateJavaScripts:
    def test_java_makefile_includes_maven_targets(self):
        result = generate_makefile("MyProject", None, None, None, lang="java")
        assert "mvn test" in result
        assert "jacoco:report" in result
        assert "spotless-maven-plugin" in result

    def test_java_makefile_includes_test_server_target(self):
        result = generate_makefile(
            "MyProject",
            None,
            None,
            None,
            lang="java",
            minecraft_server=True,
            minecraft_server_name="TestServer_MyProject",
        )
        assert "test-server-start" in result
        assert "start_test_server.py" in result

    def test_java_format_license_script_targets_java_sources(self):
        result = generate_format_licenses_java("Alice", "MIT")
        assert "src/main/java" in result
        assert "src/test/java" in result
        assert "MIT License" in result

    def test_java_test_server_launcher_targets_server_dir(self):
        result = generate_start_test_server_py("TestServer_MyProject")
        assert "TestServer_MyProject" in result
        assert "start.bat" in result or "start.sh" in result
