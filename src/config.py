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
import json
import subprocess
from pathlib import Path
from datetime import datetime

CONFIG_FILE = Path.home() / ".scaffoldrc"
HISTORY_FILE = Path.home() / ".scaffold_history"
DEFAULT_SOURCE_SCRIPTS = None
DEFAULT_OUTPUT_DIR = "output"

def get_version(default="0.1.0"):
    """Interactively build a version string in the format MAJOR.MINOR.PATCH."""
    os.system("cls" if os.name == "nt" else "clear")
    print("Set project version (format: MAJOR.MINOR.PATCH)")
    print("  Template: 0.0.0\n")

    def _prompt_part(label, placeholder):
        while True:
            raw = input(f"  {label} [{placeholder}]: ").strip()
            if raw == "":
                return placeholder
            if raw.isdigit():
                return raw
            print("    Invalid input – please enter a number.")

    major = _prompt_part("MAJOR", "0")
    minor = _prompt_part("MINOR", "0")
    patch = _prompt_part("PATCH", "0")

    version = f"{major}.{minor}.{patch}"
    print(f"\n  Version set to: {version}")
    return version

def try_get_git_user():
    """Try to get default author from git config or environment variable."""
    author = os.getenv("SCAFFOLD_DEFAULT_AUTHOR")
    if author:
        return author
    try:
        result = subprocess.run(
            ["git", "config", "--get", "user.name"],
            capture_output=True,
            text=True,
            check=True,
        )
        git_name = result.stdout.strip()
        if git_name:
            return git_name
    except Exception:
        pass
    return "Your Author Name"

def set_default_author():
    """Determine default author name for config."""
    return try_get_git_user() or input("Enter your Author Name: ")

def load_config():
    """Load default settings from ~/.scaffoldrc"""
    defaults = {
        "author": set_default_author(),
        "lang": "javascript",
        "template": "basic",
        "git": False,
        "install": False,
        "output_dir": DEFAULT_OUTPUT_DIR,
        "version": "0.1.0",
        "license": "MIT",
        "description": "",
        "lang_version": None,
        "package_manager": "npm",
        "test_framework": None,
        "linter": None,
        "docker": False,
        "ci": "github",
        "tasks_md": True,
        "changelog_md": True,
        "contributing_md": True,
        "prettier": False,
        "indent_size": 2,
    }
    if CONFIG_FILE.exists():
        try:
            with open(CONFIG_FILE, "r", encoding="utf-8") as f:
                user_config = json.load(f)
                defaults.update(user_config)
        except Exception as e:
            print(f"Warning: Could not load config: {e}")
    return defaults

def load_history():
    """Load project history from ~/.scaffold_history"""
    if HISTORY_FILE.exists():
        try:
            with open(HISTORY_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
                return data.get("projects", [])
        except Exception as e:
            print(f"Warning: Could not load history: {e}")
    return []

def save_to_history(project_config):
    """Save a project configuration to history."""
    try:
        history_data = {"projects": []}
        if HISTORY_FILE.exists():
            try:
                with open(HISTORY_FILE, "r", encoding="utf-8") as f:
                    history_data = json.load(f)
            except Exception:
                pass

        entry = {
            "id": str(int(datetime.now().timestamp() * 1000)),
            "name": project_config.get("name"),
            "lang": project_config.get("lang"),
            "template": project_config.get("template"),
            "author": project_config.get("author"),
            "version": project_config.get("version"),
            "license": project_config.get("license"),
            "description": project_config.get("description"),
            "lang_version": project_config.get("lang_version"),
            "package_manager": project_config.get("package_manager"),
            "test_framework": project_config.get("test_framework"),
            "linter": project_config.get("linter"),
            "docker": project_config.get("docker"),
            "ci": project_config.get("ci"),
            "server": project_config.get("server"),
            "server_port": project_config.get("server_port"),
            "prettier": project_config.get("prettier"),
            "indent_size": project_config.get("indent_size"),
            "timestamp": datetime.now().isoformat(),
            "path": project_config.get("path"),
        }

        history_data["projects"].insert(0, entry)

        history_data["projects"] = history_data["projects"][:50]

        with open(HISTORY_FILE, "w", encoding="utf-8") as f:
            json.dump(history_data, f, indent=2)
    except Exception as e:
        print(f"Warning: Could not save to history: {e}")

def get_recent_projects(limit=10):
    """Get the most recent projects from history."""
    history = load_history()
    return history[:limit]
