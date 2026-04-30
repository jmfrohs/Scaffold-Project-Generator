#!/usr/bin/env python3
"""
Add/update license headers in all Python source files.
Usage: python scripts/format_with_licenses.py

Scans src/ and tests/ — skips __pycache__, venv, .git.
"""
import os
import re
from datetime import datetime
from pathlib import Path

CURRENT_YEAR = str(datetime.now().year)
AUTHOR = "jmfrohs"

HEADER = """\
# MIT License
#
# Copyright (c) " + CURRENT_YEAR + " jmfrohs
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
""".replace("chr(10)", "\n")

SKIP_DIRS = {".git", "__pycache__", "venv", ".venv", "node_modules", ".vscode"}
SKIP_FILES = {"format_with_licenses.py"}
DIRS_TO_SCAN = ["src", "tests"]

stats = {"total": 0, "added": 0, "updated": 0, "skipped": 0, "errors": 0}

def build_header():
    return "# MIT License\n#\n# Copyright (c) " + CURRENT_YEAR + " " + AUTHOR + """\n#\n# Permission is hereby granted, free of charge, to any person obtaining a copy\n# of this software and associated documentation files (the \"Software\"), to deal\n# in the Software without restriction, including without limitation the rights\n# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell\n# copies of the Software, and to permit persons to whom the Software is\n# furnished to do so, subject to the following conditions:\n#\n# The above copyright notice and this permission notice shall be included in all\n# copies or substantial portions of the Software.\n#\n# THE SOFTWARE IS PROVIDED \"AS IS\", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR\n# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,\n# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE\n# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER\n# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,\n# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE\n# SOFTWARE."""

def has_license(content):
    stripped = re.sub(r"^#!.*\n", "", content).lstrip()
    return stripped.startswith("# MIT License") or stripped.startswith("# Copyright")

def process_file(filepath):
    if filepath.name in SKIP_FILES:
        stats["skipped"] += 1
        return
    stats["total"] += 1
    try:
        content = filepath.read_text(encoding="utf-8")
        shebang = ""
        body = content
        if content.startswith("#!"):
            first_nl = content.index("\n")
            shebang = content[:first_nl + 1]
            body = content[first_nl + 1:]
        if not has_license(content):
            header = build_header()
            filepath.write_text(shebang + header + "\n\n" + body.lstrip(), encoding="utf-8")
            stats["added"] += 1
            print(f"  [added]   {filepath}")
        else:
            m = re.search(r"Copyright \(c\) (\d{4}) ", body)
            if m and m.group(1) != CURRENT_YEAR:
                new_body = re.sub(r"Copyright \(c\) \d{4} ", f"Copyright (c) {CURRENT_YEAR} ", body)
                filepath.write_text(shebang + new_body, encoding="utf-8")
                stats["updated"] += 1
                print(f"  [updated] {filepath}")
            else:
                stats["skipped"] += 1
    except Exception as e:
        print(f"  [error]   {filepath}: {e}")
        stats["errors"] += 1

def main():
    root = Path(__file__).parent.parent
    print("Formatting Python files and managing license headers...\n")
    files = []
    for d in DIRS_TO_SCAN:
        scan_dir = root / d
        if scan_dir.exists():
            for f in scan_dir.rglob("*.py"):
                if not any(part in SKIP_DIRS for part in f.parts):
                    files.append(f)
    print(f"Found {len(files)} file(s)\n")
    for f in files:
        process_file(f)
    print(f"\nDone — added: {stats['added']}, updated: {stats['updated']}, skipped: {stats['skipped']}, errors: {stats['errors']}")

if __name__ == "__main__":
    main()
