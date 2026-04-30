#!/usr/bin/env python3
"""
Project menu for TESTREFACTOR
Usage: python scripts/menu.py
"""
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).parent.parent

COMMANDS = [
    ("1", "install       → pip install -r requirements.txt", "pip install -r requirements.txt"),
    ("2", "run           → python src/main.py", "python src/main.py"),
    ("3", "test          → pytest", "pytest"),
    ("4", "coverage      → pytest --cov=src --cov-report=term", "pytest --cov=src --cov-report=term"),
    ("5", "format        → black src/ tests/", "black src/ tests/"),
    ("6", "format:lic    → python scripts/format_with_licenses.py", "python scripts/format_with_licenses.py"),

    ("8", "pre-commit    → format + format:lic", "black src/ tests/ && python scripts/format_with_licenses.py"),
    ("0", "exit", None),
]

def run(cmd):
    print(f"\n> {cmd}\n")
    try:
        subprocess.run(cmd, shell=True, check=True, cwd=ROOT)
    except subprocess.CalledProcessError as e:
        print(f"Command failed with exit code {e.returncode}")

def show_menu():
    print("\n========================================")
    print(f"  TESTREFACTOR — Project Menu")
    print("========================================")
    for key, label, _ in COMMANDS:
        if key != "0":
            print(f"  [{key}] {label}")
    print("  [0] exit")
    print("----------------------------------------")

def main():
    while True:
        show_menu()
        choice = input("  Select: ").strip()
        match = next((c for c in COMMANDS if c[0] == choice), None)
        if not match:
            print("  Invalid choice.")
        elif match[2] is None:
            print("  Goodbye!")
            sys.exit(0)
        else:
            run(match[2])

if __name__ == "__main__":
    main()
