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
from argparse import Namespace

import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from scaffolder import scaffold_project

def _make_args(tmp_path, **overrides):
    defaults = dict(
        name="TestProj",
        author="TestUser",
        lang="python",
        template="basic",
        version="0.1.0",
        license="MIT",
        description="",
        lang_version=None,
        package_manager="npm",
        test_framework="pytest",
        linter=None,
        docker=False,
        ci="github",
        server=False,
        server_port=3001,
        git=False,
        install=False,
        tasks_md=False,
        changelog_md=False,
        contributing_md=False,
        output_dir=str(tmp_path),
        entry=None,
        prettier=False,
        indent_size=2,
    )
    defaults.update(overrides)
    return Namespace(**defaults)

class TestScaffoldProject:
    def test_python_project_structure(self, tmp_path):
        scaffold_project(_make_args(tmp_path))
        base = tmp_path / "TestProj"
        assert (base / "src" / "main.py").exists()
        assert (base / "tests" / "test_main.py").exists()
        assert (base / "requirements.txt").exists()
        assert (base / "README.md").exists()
        assert (base / "LICENSE").exists()
        assert (base / "Makefile").exists()

    def test_python_ci_file_created(self, tmp_path):
        scaffold_project(_make_args(tmp_path, ci="github"))
        ci_file = tmp_path / "TestProj" / ".github" / "workflows" / "ci.yml"
        assert ci_file.exists()

    def test_python_gitlab_ci_file_created(self, tmp_path):
        scaffold_project(_make_args(tmp_path, ci="gitlab"))
        ci_file = tmp_path / "TestProj" / ".gitlab-ci.yml"
        assert ci_file.exists()

    def test_python_docker_files_created(self, tmp_path):
        scaffold_project(_make_args(tmp_path, docker=True))
        base = tmp_path / "TestProj"
        assert (base / "Dockerfile").exists()
        assert (base / ".dockerignore").exists()

    def test_python_tasks_md_created(self, tmp_path):
        scaffold_project(_make_args(tmp_path, tasks_md=True))
        assert (tmp_path / "TestProj" / "tasks.md").exists()

    def test_python_changelog_md_created(self, tmp_path):
        scaffold_project(_make_args(tmp_path, changelog_md=True))
        assert (tmp_path / "TestProj" / "changelog.md").exists()

    def test_python_contributing_md_created(self, tmp_path):
        scaffold_project(_make_args(tmp_path, contributing_md=True))
        assert (tmp_path / "TestProj" / "contributing.md").exists()

    def test_javascript_project_structure(self, tmp_path):
        scaffold_project(_make_args(tmp_path, lang="javascript", test_framework="jest"))
        base = tmp_path / "TestProj"
        assert (base / "src" / "js" / "index.js").exists()
        assert (base / "package.json").exists()
        assert (base / "scripts" / "menu.js").exists()

    def test_html_project_structure(self, tmp_path):
        scaffold_project(_make_args(tmp_path, lang="html", test_framework=None))
        base = tmp_path / "TestProj"
        assert (base / "src" / "index.html").exists()
        assert (base / "src" / "css" / "styles.css").exists()
        assert (base / "src" / "js" / "index.js").exists()
        assert (base / "package.json").exists()

    def test_license_content(self, tmp_path):
        scaffold_project(_make_args(tmp_path))
        license_text = (tmp_path / "TestProj" / "LICENSE").read_text(encoding="utf-8")
        assert "MIT License" in license_text
        assert "TestUser" in license_text

    def test_requirements_contains_pytest(self, tmp_path):
        scaffold_project(_make_args(tmp_path, test_framework="pytest"))
        reqs = (tmp_path / "TestProj" / "requirements.txt").read_text(encoding="utf-8")
        assert "pytest" in reqs

    def test_flake8_config_created_with_linter(self, tmp_path):
        scaffold_project(_make_args(tmp_path, linter="flake8"))
        assert (tmp_path / "TestProj" / ".flake8").exists()

    def test_pylint_config_created_with_linter(self, tmp_path):
        scaffold_project(_make_args(tmp_path, linter="pylint"))
        assert (tmp_path / "TestProj" / ".pylintrc").exists()

    def test_prettierrc_created_when_flag_set_js(self, tmp_path):
        scaffold_project(
            _make_args(
                tmp_path,
                lang="javascript",
                test_framework="jest",
                prettier=True,
                indent_size=4,
            )
        )
        prettierrc = tmp_path / "TestProj" / ".prettierrc"
        assert prettierrc.exists()
        import json

        data = json.loads(prettierrc.read_text(encoding="utf-8"))
        assert data["tabWidth"] == 4

    def test_prettierrc_not_created_without_flag_js(self, tmp_path):
        scaffold_project(
            _make_args(
                tmp_path, lang="javascript", test_framework="jest", prettier=False
            )
        )
        assert not (tmp_path / "TestProj" / ".prettierrc").exists()

    def test_prettierrc_created_when_flag_set_html(self, tmp_path):
        scaffold_project(
            _make_args(
                tmp_path, lang="html", test_framework=None, prettier=True, indent_size=2
            )
        )
        assert (tmp_path / "TestProj" / ".prettierrc").exists()

    def test_prettierrc_not_created_for_python(self, tmp_path):
        scaffold_project(_make_args(tmp_path, lang="python", prettier=True))
        assert not (tmp_path / "TestProj" / ".prettierrc").exists()
