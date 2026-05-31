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
import datetime as date
from config import try_get_user_country

current_year = str(date.datetime.now().year)
country = try_get_user_country()

def create_htmlcov_directory(output_dir):
    htmlcov_dir = os.path.join(output_dir, "htmlcov")
    create_directory(htmlcov_dir)

def create_coverage_html(
    output_dir,
    coverage_percent=58,
    coverage_version="7.13.5",
    creation_date=None,
    files_rows="",
    total_statements=604,
    total_missing=252,
    total_excluded=0,
    total_coverage_ratio="352 604",
):
    if creation_date is None:
        from datetime import datetime

        creation_date = datetime.now().strftime("%Y-%m-%d %H:%M %z")

    coverage_html_path = os.path.join(output_dir, "htmlcov", "index.html")
    html_content = html_coverage_template.format(
        coverage_percent=coverage_percent,
        coverage_version=coverage_version,
        creation_date=creation_date,
        files_rows=files_rows,
        total_statements=total_statements,
        total_missing=total_missing,
        total_excluded=total_excluded,
        total_coverage_ratio=total_coverage_ratio,
        total_coverage_percent=coverage_percent,
    )
    write_file(coverage_html_path, content=html_content)

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

html_coverage_template = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta http-equiv="Content-Type" content="text/html; charset=utf-8">
    <title>HTML Coverage report</title>
    <link rel="icon" sizes="32x32" href="favicon_32_cb_c827f16f.png">
    <link rel="stylesheet" href="style_cb_5c747636.css" type="text/css">
    <script src="coverage_html_cb_188fc9a4.js" defer></script>
</head>
<body class="indexfile">
<header>
    <div class="content">
        <h1>HTML Coverage report:
            <span class="pc_cov" id="total-coverage">{coverage_percent}%</span>
        </h1>
        <aside id="help_panel_wrapper">
            <input id="help_panel_state" type="checkbox">
            <label for="help_panel_state">
                <img id="keyboard_icon" src="keybd_closed_cb_900cfef5.png" alt="Show/hide keyboard shortcuts">
            </label>
            <div id="help_panel">
                <p class="legend">Shortcuts on this page</p>
                <div class="keyhelp">
                    <p>
                        <kbd>f</kbd>
                        <kbd>s</kbd>
                        <kbd>m</kbd>
                        <kbd>x</kbd>
                        <kbd>c</kbd>
                        &nbsp; change column sorting
                    </p>
                    <p>
                        <kbd>[</kbd>
                        <kbd>]</kbd>
                        &nbsp; prev/next file
                    </p>
                    <p>
                        <kbd>?</kbd> &nbsp; show/hide this help
                    </p>
                </div>
            </div>
        </aside>
        <form id="filter_container">
            <input id="filter" type="text" value="" placeholder="filter...">
            <div>
                <input id="hide100" type="checkbox" >
                <label for="hide100">hide covered</label>
            </div>
        </form>
        <h2>
                <a class="button current">Files</a>
                <a class="button" href="function_index.html">Functions</a>
                <a class="button" href="class_index.html">Classes</a>
        </h2>
        <p class="text">
            <a class="nav" href="https://coverage.readthedocs.io/en/{coverage_version}">coverage.py v{coverage_version}</a>,
            created at {creation_date}
        </p>
    </div>
</header>
<main id="index">
    <table class="index" data-sortable>
        <thead>
            <tr class="tablehead" title="Click to sort">
                <th id="file" class="name" aria-sort="none" data-shortcut="f">File<span class="arrows"></span></th>
                <th class="spacer">&nbsp;</th>
                <th id="statements" aria-sort="none" data-default-sort-order="descending" data-shortcut="s">statements<span class="arrows"></span></th>
                <th id="missing" aria-sort="none" data-default-sort-order="descending" data-shortcut="m">missing<span class="arrows"></span></th>
                <th id="excluded" aria-sort="none" data-default-sort-order="descending" data-shortcut="x">excluded<span class="arrows"></span></th>
                <th class="spacer">&nbsp;</th>
                <th id="coverage" aria-sort="none" data-shortcut="c">coverage<span class="arrows"></span></th>
            </tr>
        </thead>
        <tbody>
            {files_rows}
        </tbody>
        <tfoot>
            <tr class="total">
                <td class="name">Total</td>
                <td class="spacer">&nbsp;</td>
                <td class="statements" data-value="{total_statements}"></td>
                <td class="missing" data-value="{total_missing}"></td>
                <td class="excluded" data-value="{total_excluded}"></td>
                <td class="spacer">&nbsp;</td>
                <td data-ratio="{total_coverage_ratio}"><span class="coverage-percent">{total_coverage_percent}%</span></td>
            </tr>
        </tfoot>
    </table>
    <p id="no_rows">
        No items found using the specified filter.
    </p>
</main>
<footer>
    <div class="content">
        <p>
            <a class="nav" href="https://coverage.readthedocs.io/en/{coverage_version}">coverage.py v{coverage_version}</a>,
            created at {creation_date}
        </p>
    </div>
    <aside class="hidden">
        <a id="prevFileLink" class="nav" href="z_145eef247bfb46b6_utils_py.html"></a>
        <a id="nextFileLink" class="nav" href="z_145eef247bfb46b6_config_py.html"></a>
        <button type="button" class="button_prev_file" data-shortcut="["></button>
        <button type="button" class="button_next_file" data-shortcut="]"></button>
        <button type="button" class="button_show_hide_help" data-shortcut="?"></button>
    </aside>
</footer>

<script>
// Dynamisch alle Coverage-Daten basierend auf Attributen berechnen
function calculateCoverageData() {{
    // Statements, Missing, Excluded aktualisieren
    const dataCells = {{
        statements: document.querySelectorAll('td.statements[data-value]'),
        missing: document.querySelectorAll('td.missing[data-value]'),
        excluded: document.querySelectorAll('td.excluded[data-value]')
    }};
    
    // Alle Zellen mit Werten befüllen
    ['statements', 'missing', 'excluded'].forEach(type => {{
        dataCells[type].forEach(cell => {{
            const value = cell.getAttribute('data-value');
            cell.textContent = value;
        }});
    }});
    
    // Coverage-Prozentsätze berechnen
    const coverageCells = document.querySelectorAll('.coverage-percent');
    
    coverageCells.forEach(cell => {{
        const parentTd = cell.parentElement;
        const ratio = parentTd.getAttribute('data-ratio');
        
        if (ratio) {{
            const [covered, total] = ratio.split(' ').map(Number);
            if (total > 0) {{
                const percentage = Math.round((covered / total) * 100);
                cell.textContent = percentage + '%';
            }} else {{
                cell.textContent = '100%';
            }}
        }}
    }});
    
    // Total-Coverage in der Kopfzeile berechnen
    const totalRow = document.querySelector('tr.total');
    if (totalRow) {{
        const totalCell = totalRow.querySelector('[data-ratio]');
        if (totalCell) {{
            const ratio = totalCell.getAttribute('data-ratio');
            const [covered, total] = ratio.split(' ').map(Number);
            const percentage = Math.round((covered / total) * 100);
            const totalCoverageSpan = document.getElementById('total-coverage');
            if (totalCoverageSpan) {{
                totalCoverageSpan.textContent = percentage + '%';
            }}
        }}
    }}
}}

// Bei Seitenladung ausführen
document.addEventListener('DOMContentLoaded', calculateCoverageData);
</script>
</body>
</html>
"""
