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
import shutil
import sys
from pathlib import Path

try:
    import questionary

    HAS_QUESTIONARY = True
except ImportError:
    HAS_QUESTIONARY = False

from config import DEFAULT_SOURCE_SCRIPTS
from generators.common import (
    generate_dockerfile,
    generate_dockerignore,
    generate_eslint_config,
    generate_flake8_config,
    generate_github_ci,
    generate_gitignore,
    generate_gitlab_ci,
    generate_license,
    generate_prettier_config,
    generate_pylint_config,
    generate_readme,
)
from generators.html import generate_html_css, generate_html_index, generate_html_js
from generators.scripts import (
    generate_format_licenses_js,
    generate_format_licenses_py,
    generate_makefile,
    generate_menu_html,
    generate_menu_js,
    generate_menu_py,
)
from generators.server import scaffold_server
from utils import (
    create_directory,
    create_tasks_md,
    get_install_command,
    run_command,
    write_file,
)

HIDDEN_DIRS = {
    ".git",
    "node_modules",
    "__pycache__",
    ".venv",
    "venv",
    ".idea",
    ".vscode",
    ".cache",
}

def browse_directory(start=None):
    """Interactive arrow-key directory browser using questionary."""
    if not HAS_QUESTIONARY:
        print("⚠️  questionary not installed. Run: pip install questionary")
        return None

    current = Path(start or Path.home()).resolve()

    while True:
        try:
            subdirs = sorted(
                [
                    d.name
                    for d in current.iterdir()
                    if d.is_dir()
                    and d.name not in HIDDEN_DIRS
                    and not d.name.startswith(".")
                ],
                key=str.lower,
            )
        except PermissionError:
            print(f"⚠️  No permission to read {current}")
            current = current.parent
            continue

        choices = []
        choices.append(
            questionary.Choice(
                title=f"✅ Use this folder ({current})", value="__select__"
            )
        )
        choices.append(
            questionary.Choice(title="📝 Type path manually", value="__manual__")
        )
        choices.append(questionary.Separator("─" * 40))
        for name in subdirs:
            choices.append(questionary.Choice(title=f"📁 {name}", value=name))

        answer = questionary.select(
            f"📂 {current}",
            choices=choices,
            use_shortcuts=False,
            use_arrow_keys=True,
        ).ask()

        if answer is None:  # Ctrl+C
            return None
        elif answer == "__select__":
            return str(current)
        elif answer == "__up__":
            current = current.parent
        elif answer == "__manual__":
            typed = questionary.text("Enter path:", default=str(current)).ask()
            if typed:
                p = Path(typed).expanduser().resolve()
                if p.is_dir():
                    current = p
                else:
                    print(f"⚠️  Not a valid directory: {typed}")
        else:
            current = current / answer

    return str(current)

def scaffold_project(args):
    project_name = args.name
    author = args.author
    lang = args.lang.lower()
    template = args.template
    version = args.version
    license_type = args.license
    description = args.description
    lang_version = args.lang_version
    package_manager = args.package_manager
    test_framework = args.test_framework or (
        "jest" if lang == "javascript" else ("pytest" if lang == "python" else None)
    )
    linter = args.linter
    docker = args.docker
    ci = args.ci
    server = args.server
    server_port = args.server_port
    prettier = getattr(args, "prettier", False)
    indent_size = getattr(args, "indent_size", 2)
    if args.output_dir == "browse":
        browsed = browse_directory()
        if browsed is None:
            print("❌ Cancelled.")
            sys.exit(1)
        output_dir = browsed
    else:
        output_dir = (
            os.path.join(os.path.dirname(os.path.abspath(__file__)), args.output_dir)
            if not os.path.isabs(args.output_dir)
            else args.output_dir
        )
    entry = args.entry or (
        "index.js"
        if lang == "javascript"
        else ("index.html" if lang == "html" else "main.py")
    )

    base_dir = os.path.join(output_dir, project_name)
    print(f"\nScaffolding {project_name} ({lang}/{template}) → {base_dir}")

    dirs = ["", "docs", "scripts"]
    if lang == "html":
        dirs += ["src", "src/js", "src/css"]
    else:
        if ci == "github":
            dirs.append(".github/workflows")
        dirs += ["src/js", "tests"] if lang == "javascript" else ["src", "tests"]
    for d in dirs:
        create_directory(os.path.join(base_dir, d))

    gitignore_content = generate_gitignore(lang)
    if server:
        gitignore_content += "\nserver/.env\nserver/node_modules/\n"
    write_file(os.path.join(base_dir, ".gitignore"), gitignore_content)
    write_file(
        os.path.join(base_dir, "LICENSE"), generate_license(license_type, author)
    )
    project_name = project_name.replace("-", " ").upper()
    write_file(
        os.path.join(base_dir, "README.md"),
        generate_readme(
            project_name,
            lang,
            author,
            description,
            version,
            license_type,
            lang_version,
            test_framework,
            package_manager,
        ),
    )

    if lang != "html":
        if ci == "github":
            write_file(
                os.path.join(base_dir, ".github/workflows/ci.yml"),
                generate_github_ci(lang, lang_version, test_framework, package_manager),
            )
        elif ci == "gitlab":
            write_file(
                os.path.join(base_dir, ".gitlab-ci.yml"),
                generate_gitlab_ci(lang, lang_version, test_framework, package_manager),
            )

    if lang == "javascript":
        test_dep = "vitest" if test_framework == "vitest" else "jest"
        test_dep_version = "^1.6.0" if test_framework == "vitest" else "^29.0.0"
        dev_deps = {test_dep: test_dep_version, "prettier": "^3.0.0"}
        coverage_cmd = (
            f"{test_dep} --coverage"
            if test_dep == "jest"
            else f"{package_manager} run coverage"
        )
        pre_commit_cmd = (
            f"{package_manager} run format && {package_manager} run format:lic"
            + (f" && {package_manager} run lint" if linter == "eslint" else "")
        )
        scripts = {
            "start": f"node src/js/{entry}",
            "test": test_dep,
            "coverage": coverage_cmd,
            "format": 'prettier --write "src/**/*.js"',
            "format:lic": "node scripts/format-with-licenses.js",
            "pre-commit": pre_commit_cmd,
            "menu": "node scripts/menu.js",
        }
        if server:
            scripts["server:start"] = "cd server && node index.js"
            scripts["server:dev"] = "cd server && node --watch index.js"
            scripts["server:install"] = (
                f"cd server && {get_install_command(package_manager)}"
            )
            scripts["server:stop"] = (
                "taskkill /F /IM node.exe 2>nul || echo No server running"
            )
        if linter == "eslint":
            dev_deps["eslint"] = "^8.0.0"
            scripts["lint"] = "eslint src/"

        project_name = project_name.lower().replace(" ", "-")

        package_json = {
            "name": project_name,
            "version": version,
            "description": description,
            "author": author,
            "license": license_type,
            "scripts": scripts,
            "devDependencies": dev_deps,
        }
        write_file(
            os.path.join(base_dir, "package.json"), json.dumps(package_json, indent=2)
        )
        write_file(
            os.path.join(base_dir, f"src/js/{entry}"),
            f"console.log('Hello from {project_name}!');\n",
        )
        if linter == "eslint":
            write_file(
                os.path.join(base_dir, ".eslintrc.json"), generate_eslint_config()
            )
        if prettier:
            write_file(
                os.path.join(base_dir, ".prettierrc"),
                generate_prettier_config(indent_size),
            )

    elif lang == "python":
        reqs = ["black"]
        if test_framework == "pytest":
            reqs.insert(0, "pytest")
        if linter == "flake8":
            reqs.append("flake8")
        elif linter == "pylint":
            reqs.append("pylint")
        write_file(os.path.join(base_dir, "requirements.txt"), "\n".join(reqs) + "\n")
        write_file(
            os.path.join(base_dir, f"src/{entry}"),
            f"def main():\n    print('Hello from {project_name}!')\n\nif __name__ == '__main__':\n    main()\n",
        )
        if test_framework == "pytest":
            write_file(
                os.path.join(base_dir, "tests/test_main.py"),
                "def test_example():\n    assert True\n",
            )
        elif test_framework == "unittest":
            write_file(
                os.path.join(base_dir, "tests/test_main.py"),
                "import unittest\n\nclass TestMain(unittest.TestCase):\n    def test_example(self):\n        self.assertTrue(True)\n\nif __name__ == '__main__':\n    unittest.main()\n",
            )
        if linter == "flake8":
            write_file(os.path.join(base_dir, ".flake8"), generate_flake8_config())
        elif linter == "pylint":
            write_file(os.path.join(base_dir, ".pylintrc"), generate_pylint_config())

    elif lang == "html":
        project_name_norm = project_name.lower().replace(" ", "-")
        scripts = {
            "start": "npx http-server src/ -o",
            "format": 'prettier --write "src/**"',
            "format:lic": "node scripts/format-with-licenses.js",
            "pre-commit": f"{package_manager} run format && {package_manager} run format:lic",
            "menu": "node scripts/menu.js",
        }
        if server:
            scripts["server:start"] = "cd server && node index.js"
            scripts["server:dev"] = "cd server && node --watch index.js"
            scripts["server:install"] = (
                f"cd server && {get_install_command(package_manager)}"
            )
            scripts["server:stop"] = (
                "taskkill /F /IM node.exe 2>nul || echo No server running"
            )
        package_json = {
            "name": project_name_norm,
            "version": version,
            "description": description,
            "author": author,
            "license": license_type,
            "scripts": scripts,
            "devDependencies": {"http-server": "^14.0.0", "prettier": "^3.0.0"},
        }
        project_name = project_name_norm
        write_file(
            os.path.join(base_dir, "package.json"), json.dumps(package_json, indent=2)
        )
        write_file(
            os.path.join(base_dir, "src/index.html"), generate_html_index(project_name)
        )
        write_file(
            os.path.join(base_dir, "src/js/index.js"), generate_html_js(project_name)
        )
        write_file(os.path.join(base_dir, "src/css/styles.css"), generate_html_css())
        if prettier:
            write_file(
                os.path.join(base_dir, ".prettierrc"),
                generate_prettier_config(indent_size),
            )

    if docker:
        write_file(
            os.path.join(base_dir, "Dockerfile"),
            generate_dockerfile(lang, lang_version, entry),
        )
        write_file(os.path.join(base_dir, ".dockerignore"), generate_dockerignore(lang))

    if server:
        scaffold_server(base_dir, project_name, package_manager, server_port)

    if lang == "javascript":
        write_file(
            os.path.join(base_dir, "scripts/menu.js"),
            generate_menu_js(
                project_name,
                entry,
                package_manager,
                test_framework,
                linter,
                server,
                server_port,
            ),
        )
        write_file(
            os.path.join(base_dir, "scripts/format-with-licenses.js"),
            generate_format_licenses_js(author, license_type),
        )
    elif lang == "python":
        write_file(
            os.path.join(base_dir, "scripts/menu.py"),
            generate_menu_py(project_name, entry, test_framework, linter),
        )
        write_file(
            os.path.join(base_dir, "scripts/format_with_licenses.py"),
            generate_format_licenses_py(author, license_type),
        )
        write_file(
            os.path.join(base_dir, "Makefile"),
            generate_makefile(project_name, entry, test_framework, linter),
        )
    elif lang == "html":
        write_file(
            os.path.join(base_dir, "scripts/menu.js"),
            generate_menu_html(project_name, package_manager, server, server_port),
        )
        write_file(
            os.path.join(base_dir, "scripts/format-with-licenses.js"),
            generate_format_licenses_js(author, license_type),
        )

    if DEFAULT_SOURCE_SCRIPTS and os.path.exists(DEFAULT_SOURCE_SCRIPTS):
        print("Copying scripts...")
        for item in os.listdir(DEFAULT_SOURCE_SCRIPTS):
            dest = os.path.join(base_dir, "scripts", item)
            if not os.path.exists(dest):
                shutil.copy2(os.path.join(DEFAULT_SOURCE_SCRIPTS, item), dest)

    if args.git:
        print("Initializing Git repository...")
        if run_command("git init", base_dir):
            run_command("git add .", base_dir)
            run_command('git commit -m "Initial scaffold"', base_dir)

    if args.install:
        print("Installing dependencies...")
        if lang in ("javascript", "html"):
            run_command(get_install_command(package_manager), base_dir)
            if server:
                print("Installing server dependencies...")
                run_command(
                    get_install_command(package_manager),
                    os.path.join(base_dir, "server"),
                )
        elif lang == "python":
            run_command("python -m venv venv", base_dir)
            pip_path = (
                os.path.join(base_dir, "venv", "Scripts", "pip")
                if os.name == "nt"
                else os.path.join(base_dir, "venv", "bin", "pip")
            )
            run_command(f"{pip_path} install -r requirements.txt", base_dir)

    if args.tasks_md:
        create_tasks_md(base_dir)

    print(f"\nSuccessfully scaffolded {project_name} in {base_dir}")
