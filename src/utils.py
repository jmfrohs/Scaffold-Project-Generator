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
import subprocess

def create_directory(directory_path):
    if not os.path.exists(directory_path):
        os.makedirs(directory_path)
        print(f"Created directory: {directory_path}")

def write_file(file_path, content):
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"Created file: {file_path}")

def create_tasks_md(output_dir):
    tasks_md_content = "# Project Tasks\n\n"
    tasks_md_path = os.path.join(output_dir, "tasks.md")
    write_file(tasks_md_path, content=tasks_md_content)

def create_changelog_md(output_dir):
    changelog_md_content = "# Changelog\n\nAll notable changes to this project will be documented in this file.\n"
    changelog_md_path = os.path.join(output_dir, "changelog.md")
    write_file(changelog_md_path, content=changelog_md_content)

def create_contributing_md(output_dir):
    contributing_md_content = "# Contributing\n\nThank you for considering contributing to this project! Please read the following guidelines before submitting a pull request.\n"
    contributing_md_path = os.path.join(output_dir, "contributing.md")
    write_file(contributing_md_path, content=contributing_md_content)

def run_command(command, cwd):
    """Run a shell command and return its success."""
    try:
        si = subprocess.STARTUPINFO()
        si.dwFlags |= subprocess.STARTF_USESHOWWINDOW
        si.wShowWindow = subprocess.SW_HIDE
        subprocess.run(
            command,
            shell=True,
            check=True,
            cwd=cwd,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            startupinfo=si,
        )
        return True
    except subprocess.CalledProcessError:
        print(f"Error running command '{command}'")
        return False

def get_install_command(package_manager):
    return {"npm": "npm install", "yarn": "yarn", "pnpm": "pnpm install"}.get(
        package_manager, "npm install"
    )

def get_test_command(lang, test_framework, package_manager):
    if lang == "javascript":
        if test_framework == "vitest":
            pm = package_manager or "npm"
            return f"{pm} run test"
        return {"npm": "npm test", "yarn": "yarn test", "pnpm": "pnpm test"}.get(
            package_manager, "npm test"
        )
    elif lang == "python":
        if test_framework == "unittest":
            return "python -m unittest discover"
        return "pytest"
