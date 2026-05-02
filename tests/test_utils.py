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
from pathlib import Path

import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from utils import (
    create_directory,
    create_changelog_md,
    create_contributing_md,
    create_tasks_md,
    get_install_command,
    get_test_command,
    run_command,
    write_file,
)

class TestGetInstallCommand:
    def test_npm(self):
        assert get_install_command("npm") == "npm install"

    def test_yarn(self):
        assert get_install_command("yarn") == "yarn"

    def test_pnpm(self):
        assert get_install_command("pnpm") == "pnpm install"

    def test_unknown_falls_back_to_npm(self):
        assert get_install_command("bun") == "npm install"

class TestGetTestCommand:
    def test_js_jest_npm(self):
        assert get_test_command("javascript", "jest", "npm") == "npm test"

    def test_js_jest_yarn(self):
        assert get_test_command("javascript", "jest", "yarn") == "yarn test"

    def test_js_jest_pnpm(self):
        assert get_test_command("javascript", "jest", "pnpm") == "pnpm test"

    def test_js_vitest_npm(self):
        assert get_test_command("javascript", "vitest", "npm") == "npm run test"

    def test_js_vitest_yarn(self):
        assert get_test_command("javascript", "vitest", "yarn") == "yarn run test"

    def test_python_pytest(self):
        assert get_test_command("python", "pytest", None) == "pytest"

    def test_python_unittest(self):
        assert (
            get_test_command("python", "unittest", None)
            == "python -m unittest discover"
        )

    def test_python_default(self):
        assert get_test_command("python", None, None) == "pytest"

class TestCreateDirectory:
    def test_creates_directory(self, tmp_path):
        new_dir = str(tmp_path / "newdir")
        create_directory(new_dir)
        assert os.path.isdir(new_dir)

    def test_does_not_fail_if_exists(self, tmp_path):
        existing = str(tmp_path / "existing")
        os.makedirs(existing)
        create_directory(existing)  # should not raise
        assert os.path.isdir(existing)

class TestWriteFile:
    def test_creates_file_with_content(self, tmp_path):
        filepath = str(tmp_path / "hello.txt")
        write_file(filepath, "hello world")
        assert Path(filepath).read_text(encoding="utf-8") == "hello world"

    def test_overwrites_existing_file(self, tmp_path):
        filepath = str(tmp_path / "hello.txt")
        write_file(filepath, "first")
        write_file(filepath, "second")
        assert Path(filepath).read_text(encoding="utf-8") == "second"

class TestCreateTasksMd:
    def test_creates_tasks_md(self, tmp_path):
        create_tasks_md(str(tmp_path))
        tasks_file = tmp_path / "tasks.md"
        assert tasks_file.exists()
        assert "# Project Tasks" in tasks_file.read_text(encoding="utf-8")

class TestCreateChangelogMd:
    def test_creates_changelog_md(self, tmp_path):
        create_changelog_md(str(tmp_path))
        changelog_file = tmp_path / "changelog.md"
        assert changelog_file.exists()
        content = changelog_file.read_text(encoding="utf-8")
        assert "# Changelog" in content
        assert "All notable changes" in content

class TestCreateContributingMd:
    def test_creates_contributing_md(self, tmp_path):
        create_contributing_md(str(tmp_path))
        contributing_file = tmp_path / "contributing.md"
        assert contributing_file.exists()
        content = contributing_file.read_text(encoding="utf-8")
        assert "# Contributing" in content
        assert "Thank you for considering contributing" in content

class TestRunCommand:
    def test_successful_command_returns_true(self, tmp_path):
        result = run_command("echo hello", str(tmp_path))
        assert result is True

    def test_failing_command_returns_false(self, tmp_path):
        result = run_command("exit 1", str(tmp_path))
        assert result is False
