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

from utils import get_install_command, get_test_command

def generate_format_licenses_js(author, license_type):
    if license_type != "MIT":
        return f"""#!/usr/bin/env node
const fs = require('fs');
const path = require('path');
const CURRENT_YEAR = new Date().getFullYear();
const AUTHOR = '{author}';
const HEADER = `/* Copyright (c) ${{CURRENT_YEAR}} ${{AUTHOR}} */`;
const SKIP_FILES = ['bundle.js'];
const SKIP_DIRS = ['.git', 'node_modules', '.vscode'];
function findFiles(dir, exts) {{
  let files = [];
  try {{
    for (const e of fs.readdirSync(dir, {{ withFileTypes: true }})) {{
      const p = path.join(dir, e.name);
      if (e.isDirectory() && !SKIP_DIRS.includes(e.name)) files.push(...findFiles(p, exts));
      else if (exts.some(x => e.name.endsWith(x)) && !SKIP_FILES.includes(e.name)) files.push(p);
    }}
  }} catch {{}}
  return files;
}}
const root = path.join(__dirname, '..');
const files = findFiles(path.join(root, 'src'), ['.js']);
let added = 0;
for (const f of files) {{
  const c = fs.readFileSync(f, 'utf-8');
  if (!c.includes('Copyright')) {{
    fs.writeFileSync(f, HEADER + '\\n\\n' + c.trimStart(), 'utf-8');
    added++;
    console.log('Added header:', path.relative(root, f));
  }}
}}
console.log(`\\nDone: ${{added}} file(s) updated.`);
"""
    return f"""#!/usr/bin/env node
/*
 * MIT License — Copyright (c) {author}
 * Add/update MIT license headers in all source files.
 * Usage: node scripts/format-with-licenses.js
 */
const fs = require('fs');
const path = require('path');

const CURRENT_YEAR = new Date().getFullYear();
const AUTHOR = '{author}';

const MIT_LICENSE_JS = `/*
MIT License

Copyright (c) ${{CURRENT_YEAR}} ${{AUTHOR}}

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
*/`;

const SKIP_FILES = ['bundle.js'];
const SKIP_DIRS = ['.git', 'node_modules', '.vscode'];
const stats = {{ total: 0, added: 0, updated: 0, skipped: 0, errors: 0 }};

function findFiles(dir, exts) {{
  const files = [];
  try {{
    for (const e of fs.readdirSync(dir, {{ withFileTypes: true }})) {{
      const p = path.join(dir, e.name);
      if (e.isDirectory() && !SKIP_DIRS.includes(e.name)) files.push(...findFiles(p, exts));
      else if (exts.some(x => e.name.endsWith(x)) && !SKIP_FILES.includes(e.name)) files.push(p);
    }}
  }} catch {{}}
  return files;
}}

function hasLicense(content) {{
  return content.replace(/^#!.*\\n/, '').trim().startsWith('/*') && content.includes('MIT License');
}}

function processFile(filePath) {{
  if (filePath.endsWith('format-with-licenses.js')) {{ stats.skipped++; return; }}
  stats.total++;
  try {{
    const content = fs.readFileSync(filePath, 'utf-8');
    const hasShebang = content.startsWith('#!');
    const shebang = hasShebang ? content.split('\\n')[0] + '\\n' : '';
    const body = hasShebang ? content.replace(/^#!.*\\n/, '') : content;
    if (!hasLicense(content)) {{
      fs.writeFileSync(filePath, shebang + MIT_LICENSE_JS + '\\n\\n' + body.trimStart(), 'utf-8');
      stats.added++;
      console.log('  [added]  ', path.relative(path.join(__dirname, '..'), filePath));
    }} else {{
      const m = body.match(/Copyright \\(c\\) (\\d{{4}}) /);
      if (m && m[1] !== String(CURRENT_YEAR)) {{
        fs.writeFileSync(filePath, shebang + body.replace(/Copyright \\(c\\) \\d{{4}} /, `Copyright (c) ${{CURRENT_YEAR}} `), 'utf-8');
        stats.updated++;
        console.log('  [updated]', path.relative(path.join(__dirname, '..'), filePath));
      }} else {{ stats.skipped++; }}
    }}
  }} catch (err) {{ console.error('Error:', filePath, err.message); stats.errors++; }}
}}

const root = path.join(__dirname, '..');
const files = findFiles(path.join(root, 'src'), ['.js']);
console.log('Formatting files and managing license headers...\\n');
console.log(`Found ${{files.length}} file(s)\\n`);
files.forEach(processFile);
console.log(`\\nDone — added: ${{stats.added}}, updated: ${{stats.updated}}, skipped: ${{stats.skipped}}, errors: ${{stats.errors}}`);
"""

def generate_format_licenses_py(author, license_type):
    if license_type == "MIT":
        header_template = f'# MIT License\\n#\\n# Copyright (c) {{year}} {author}\\n#\\n# Permission is hereby granted, free of charge, to any person obtaining a copy\\n# of this software and associated documentation files (the "Software"), to deal\\n# in the Software without restriction, including without limitation the rights\\n# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell\\n# copies of the Software, and to permit persons to whom the Software is\\n# furnished to do so, subject to the following conditions:\\n#\\n# The above copyright notice and this permission notice shall be included in all\\n# copies or substantial portions of the Software.\\n#\\n# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR\\n# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,\\n# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE\\n# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER\\n# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,\\n# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE\\n# SOFTWARE.'
    else:
        header_template = f"# Copyright (c) {{year}} {author}"
    return f'''#!/usr/bin/env python3
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
AUTHOR = "{author}"

HEADER = """\\
{header_template.replace("{year}", '" + CURRENT_YEAR + "').replace("\\n", chr(10))}
""".replace("chr(10)", "\\n")

SKIP_DIRS = {{".git", "__pycache__", "venv", ".venv", "node_modules", ".vscode"}}
SKIP_FILES = {{"format_with_licenses.py"}}
DIRS_TO_SCAN = ["src", "tests"]

stats = {{"total": 0, "added": 0, "updated": 0, "skipped": 0, "errors": 0}}

def build_header():
    return "# MIT License\\n#\\n# Copyright (c) " + CURRENT_YEAR + " " + AUTHOR + """\\n#\\n# Permission is hereby granted, free of charge, to any person obtaining a copy\\n# of this software and associated documentation files (the \\"Software\\"), to deal\\n# in the Software without restriction, including without limitation the rights\\n# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell\\n# copies of the Software, and to permit persons to whom the Software is\\n# furnished to do so, subject to the following conditions:\\n#\\n# The above copyright notice and this permission notice shall be included in all\\n# copies or substantial portions of the Software.\\n#\\n# THE SOFTWARE IS PROVIDED \\"AS IS\\", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR\\n# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,\\n# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE\\n# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER\\n# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,\\n# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE\\n# SOFTWARE."""

def has_license(content):
    stripped = re.sub(r"^#!.*\\n", "", content).lstrip()
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
            first_nl = content.index("\\n")
            shebang = content[:first_nl + 1]
            body = content[first_nl + 1:]
        if not has_license(content):
            header = build_header()
            filepath.write_text(shebang + header + "\\n\\n" + body.lstrip(), encoding="utf-8")
            stats["added"] += 1
            print(f"  [added]   {{filepath}}")
        else:
            m = re.search(r"Copyright \\(c\\) (\\d{{4}}) ", body)
            if m and m.group(1) != CURRENT_YEAR:
                new_body = re.sub(r"Copyright \\(c\\) \\d{{4}} ", f"Copyright (c) {{CURRENT_YEAR}} ", body)
                filepath.write_text(shebang + new_body, encoding="utf-8")
                stats["updated"] += 1
                print(f"  [updated] {{filepath}}")
            else:
                stats["skipped"] += 1
    except Exception as e:
        print(f"  [error]   {{filepath}}: {{e}}")
        stats["errors"] += 1

def main():
    root = Path(__file__).parent.parent
    print("Formatting Python files and managing license headers...\\n")
    files = []
    for d in DIRS_TO_SCAN:
        scan_dir = root / d
        if scan_dir.exists():
            for f in scan_dir.rglob("*.py"):
                if not any(part in SKIP_DIRS for part in f.parts):
                    files.append(f)
    print(f"Found {{len(files)}} file(s)\\n")
    for f in files:
        process_file(f)
    print(f"\\nDone — added: {{stats[\'added\']}}, updated: {{stats[\'updated\']}}, skipped: {{stats[\'skipped\']}}, errors: {{stats[\'errors\']}}")

if __name__ == "__main__":
    main()
'''

def generate_menu_js(
    project_name,
    entry,
    package_manager,
    test_framework,
    linter,
    server=False,
    server_port=3001,
):
    install_cmd = get_install_command(package_manager)
    test_cmd = get_test_command("javascript", test_framework, package_manager)
    coverage_cmd = (
        f"{test_framework} --coverage"
        if test_framework == "jest"
        else f"{package_manager} run coverage"
    )
    start_cmd = f"node src/js/{entry}"
    format_cmd = 'prettier --write "src/**/*.js"'
    lint_entry = (
        '  { key: "7", label: "lint          → eslint src/", cmd: "eslint src/" }},'
        if linter == "eslint"
        else ""
    )
    pre_commit_cmd = (
        f"{package_manager} run format && node scripts/format-with-licenses.js"
        + (" && eslint src/" if linter == "eslint" else "")
    )
    server_entries = ""
    if server:
        server_entries = f"""  {{ key: "s", label: "server:start  → cd server && node index.js", cmd: "cd server && node index.js" }},
  {{ key: "d", label: "server:dev    → cd server && node --watch index.js", cmd: "cd server && node --watch index.js" }},
  {{ key: "i", label: "server:install → cd server && {get_install_command(package_manager)}", cmd: "cd server && {get_install_command(package_manager)}" }},"""
    return f"""#!/usr/bin/env node
/**
 * Project menu for {project_name}
 * Usage: node scripts/menu.js
 */
const {{ execSync }} = require('child_process');
const readline = require('readline');

const COMMANDS = [
  {{ key: "1", label: "install       → {install_cmd}", cmd: "{install_cmd}" }},
  {{ key: "2", label: "start         → {start_cmd}", cmd: "{start_cmd}" }},
  {{ key: "3", label: "test          → {test_cmd}", cmd: "{test_cmd}" }},
  {{ key: "4", label: "coverage      → {coverage_cmd}", cmd: "{coverage_cmd}" }},
  {{ key: "5", label: "format        → {format_cmd}", cmd: `{format_cmd}` }},
  {{ key: "6", label: "format:lic    → node scripts/format-with-licenses.js", cmd: "node scripts/format-with-licenses.js" }},
{lint_entry}
  {{ key: "8", label: "pre-commit    → format + format:lic{' + lint' if linter == 'eslint' else ''}", cmd: "{pre_commit_cmd}" }},
{server_entries}
  {{ key: "0", label: "exit", cmd: null }},
];

function run(cmd) {{
  console.log(`\\n> ${{cmd}}\\n`);
  try {{
    execSync(cmd, {{ stdio: 'inherit', cwd: require('path').join(__dirname, '..') }});
  }} catch (e) {{
    console.error('Command failed with exit code', e.status);
  }}
}}

function showMenu() {{
  console.log('\\n========================================');
  console.log('  {project_name} — Project Menu');
  console.log('========================================');
  COMMANDS.forEach(c => c.key !== "0" && console.log(`  [${{c.key}}] ${{c.label}}`));
  console.log('  [0] exit');
  console.log('----------------------------------------');
}}

const rl = readline.createInterface({{ input: process.stdin, output: process.stdout }});

function prompt() {{
  showMenu();
  rl.question('  Select: ', (answer) => {{
    const entry = COMMANDS.find(c => c.key === answer.trim());
    if (!entry) {{
      console.log('  Invalid choice.');
    }} else if (entry.cmd === null) {{
      console.log('  Goodbye!');
      rl.close();
      return;
    }} else {{
      run(entry.cmd);
    }}
    prompt();
  }});
}}

prompt();
"""

def generate_menu_py(project_name, entry, test_framework, linter):
    test_cmd = get_test_command("python", test_framework, None)
    coverage_cmd = (
        "pytest --cov=src --cov-report=term"
        if test_framework == "pytest"
        else "python -m unittest discover"
    )
    lint_entry = (
        f'    ("7", "lint          → {linter} src/", "{linter} src/"),'
        if linter
        else ""
    )
    pre_commit_parts = ["black src/ tests/", "python scripts/format_with_licenses.py"]
    if linter:
        pre_commit_parts.append(f"{linter} src/")
    pre_commit_cmd = " && ".join(pre_commit_parts)
    return f"""#!/usr/bin/env python3
\"\"\"
Project menu for {project_name}
Usage: python scripts/menu.py
\"\"\"
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).parent.parent

COMMANDS = [
    ("1", "install       → pip install -r requirements.txt", "pip install -r requirements.txt"),
    ("2", "run           → python src/{entry}", "python src/{entry}"),
    ("3", "test          → {test_cmd}", "{test_cmd}"),
    ("4", "coverage      → {coverage_cmd}", "{coverage_cmd}"),
    ("5", "format        → black src/ tests/", "black src/ tests/"),
    ("6", "format:lic    → python scripts/format_with_licenses.py", "python scripts/format_with_licenses.py"),
{lint_entry}
    ("8", "pre-commit    → format + format:lic{' + lint' if linter else ''}", "{pre_commit_cmd}"),
    ("0", "exit", None),
]

def run(cmd):
    print(f"\\n> {{cmd}}\\n")
    try:
        subprocess.run(cmd, shell=True, check=True, cwd=ROOT)
    except subprocess.CalledProcessError as e:
        print(f"Command failed with exit code {{e.returncode}}")

def show_menu():
    print("\\n========================================")
    print(f"  {project_name} — Project Menu")
    print("========================================")
    for key, label, _ in COMMANDS:
        if key != "0":
            print(f"  [{{key}}] {{label}}")
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
"""

def generate_menu_html(project_name, package_manager, server=False, server_port=3001):
    install_cmd = get_install_command(package_manager)
    format_cmd = 'prettier --write "src/**"'
    pre_commit_cmd = f"{package_manager} run format && {package_manager} run format:lic"
    server_entries = ""
    if server:
        server_entries = f"""  {{ key: "s", label: "server:start  → cd server && node index.js", cmd: "cd server && node index.js" }},
  {{ key: "d", label: "server:dev    → cd server && node --watch index.js", cmd: "cd server && node --watch index.js" }},
  {{ key: "i", label: "server:install → cd server && {get_install_command(package_manager)}", cmd: "cd server && {get_install_command(package_manager)}" }},"""
    return f"""#!/usr/bin/env node
/**
 * Project menu for {project_name}
 * Usage: node scripts/menu.js
 */
const {{ execSync }} = require('child_process');
const readline = require('readline');

const COMMANDS = [
  {{ key: "1", label: "install       → {install_cmd}", cmd: "{install_cmd}" }},
  {{ key: "2", label: "start         → npx http-server src/ -o", cmd: "npx http-server src/ -o" }},
  {{ key: "3", label: "format        → {format_cmd}", cmd: `{format_cmd}` }},
  {{ key: "4", label: "format:lic    → node scripts/format-with-licenses.js", cmd: "node scripts/format-with-licenses.js" }},
  {{ key: "5", label: "pre-commit    → format + format:lic", cmd: "{pre_commit_cmd}" }},
{server_entries}
  {{ key: "0", label: "exit", cmd: null }},
];

function run(cmd) {{
  console.log(`\\n> ${{cmd}}\\n`);
  try {{
    execSync(cmd, {{ stdio: 'inherit', cwd: require('path').join(__dirname, '..') }});
  }} catch (e) {{
    console.error('Command failed with exit code', e.status);
  }}
}}

function showMenu() {{
  console.log('\\n========================================');
  console.log('  {project_name} — Project Menu');
  console.log('========================================');
  COMMANDS.forEach(c => c.key !== "0" && console.log(`  [${{c.key}}] ${{c.label}}`));
  console.log('  [0] exit');
  console.log('----------------------------------------');
}}

const rl = readline.createInterface({{ input: process.stdin, output: process.stdout }});

function prompt() {{
  showMenu();
  rl.question('  Select: ', (answer) => {{
    const entry = COMMANDS.find(c => c.key === answer.trim());
    if (!entry) {{
      console.log('  Invalid choice.');
    }} else if (entry.cmd === null) {{
      console.log('  Goodbye!');
      rl.close();
      return;
    }} else {{
      run(entry.cmd);
    }}
    prompt();
  }});
}}

prompt();
"""

def generate_makefile(project_name, entry, test_framework, linter):
    test_cmd = (
        "python -m pytest"
        if test_framework == "pytest"
        else "python -m unittest discover"
    )
    coverage_cmd = (
        "python -m pytest --cov=src --cov-report=term"
        if test_framework == "pytest"
        else "python -m unittest discover"
    )
    lint_cmd = f"python -m {linter} src/" if linter else ""
    lint_target = f"\nlint:\n\t{lint_cmd}\n" if linter else ""
    pre_commit_parts = [
        "python -m black src/ tests/",
        "python scripts/format_with_licenses.py",
    ]
    if linter:
        pre_commit_parts.append(lint_cmd)
    pre_commit_cmds = "\n\t".join(pre_commit_parts)
    return f""".PHONY: install run test coverage format format-lic{' lint' if linter else ''} pre-commit

install:
\tpip install -r requirements.txt

run:
\tpython src/{entry}

test:
\t{test_cmd}

coverage:
\t{coverage_cmd}

format:
\tpython -m black src/ tests/

format-lic:
\tpython scripts/format_with_licenses.py
{lint_target}
pre-commit:
\t{pre_commit_cmds}

menu:
\tpython scripts/menu.py
"""
