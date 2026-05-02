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

import argparse
import sys

from config import DEFAULT_OUTPUT_DIR, load_config, get_version, get_recent_projects
from scaffolder import scaffold_project, browse_history, edit_project_config

if __name__ == "__main__":
    defaults = load_config()

    parser = argparse.ArgumentParser(description="Project Scaffolder")
    parser.add_argument("name", nargs="?", help="Name of the project")
    parser.add_argument(
        "--author",
        default=defaults["author"],
        help=f"Author name (default: {defaults['author']})",
    )
    parser.add_argument(
        "--lang",
        default=defaults["lang"],
        help=f"Language: python|javascript|html (default: {defaults['lang']})",
    )
    parser.add_argument(
        "--template",
        default=defaults["template"],
        help=f"Template: basic|cli|api (default: {defaults['template']})",
    )
    parser.add_argument(
        "--version",
        nargs="?",
        const="__interactive__",
        default=defaults.get("version", "0.1.0"),
        help="Project version. Use --version or --version 1.2.3 to set directly.",
    )
    parser.add_argument(
        "--license",
        default=defaults.get("license", "MIT"),
        help="License: MIT|Apache-2.0|GPL-3.0 (default: MIT)",
    )
    parser.add_argument(
        "--description",
        default=defaults.get("description", ""),
        help="Short project description",
    )
    parser.add_argument(
        "--entry",
        default=None,
        help="Main entry file name (default: index.js / main.py)",
    )
    parser.add_argument(
        "--lang-version",
        dest="lang_version",
        default=defaults.get("lang_version"),
        help="Language version, e.g. 3.11 or 18",
    )
    parser.add_argument(
        "--package-manager",
        dest="package_manager",
        default=defaults.get("package_manager", "npm"),
        help="Package manager: npm|yarn|pnpm (JS only, default: npm)",
    )
    parser.add_argument(
        "--test-framework",
        dest="test_framework",
        default=defaults.get("test_framework"),
        help="Test framework: jest|vitest (JS) / pytest|unittest (Python)",
    )
    parser.add_argument(
        "--linter",
        default=defaults.get("linter"),
        help="Linter: eslint (JS) / flake8|pylint (Python)",
    )
    parser.add_argument(
        "--docker",
        action="store_true",
        default=defaults.get("docker", False),
        help="Add Dockerfile and .dockerignore",
    )
    parser.add_argument(
        "--ci",
        default=defaults.get("ci", "github"),
        help="CI platform: github|gitlab|none (default: github)",
    )
    parser.add_argument(
        "--server",
        action="store_true",
        default=defaults.get("server", False),
        help="Add a local multi-user Express/Socket.io server (JS only)",
    )
    parser.add_argument(
        "--server-port",
        dest="server_port",
        type=int,
        default=defaults.get("server_port", 3001),
        help="Port for the server (default: 3001)",
    )
    parser.add_argument(
        "--output-dir",
        dest="output_dir",
        default=defaults.get("output_dir", DEFAULT_OUTPUT_DIR),
        help=f"Output directory (default: {DEFAULT_OUTPUT_DIR}). Use 'browse' for interactive folder picker",
    )
    parser.add_argument(
        "--browse",
        action="store_true",
        default=False,
        help="Browse & pick output directory interactively (shortcut for --output-dir browse)",
    )
    parser.add_argument(
        "--no-git", dest="git", action="store_false", help="Skip git initialization"
    )
    parser.add_argument(
        "--no-install",
        dest="install",
        action="store_false",
        help="Skip dependency installation",
    )
    parser.add_argument(
        "--tasks-md",
        dest="tasks_md",
        action="store_true",
        default=defaults.get("tasks_md", True),
        help="Creates a tasks.md file (default: True).",
    )
    parser.add_argument(
        "--changelog-md",
        dest="changelog_md",
        action="store_true",
        default=defaults.get("changelog_md", True),
        help="Creates a changelog.md file (default: True).",
    )
    parser.add_argument(
        "--contributing-md",
        dest="contributing_md",
        action="store_true",
        default=defaults.get("contributing_md", True),
        help="Creates a contributing.md file (default: True).",
    )
    parser.add_argument(
        "--prettier",
        action="store_true",
        default=defaults.get("prettier", False),
        help="Add a .prettierrc configuration file to the project (JS/HTML only)",
    )
    parser.add_argument(
        "--indent-size",
        dest="indent_size",
        type=int,
        default=defaults.get("indent_size", 2),
        help="Indentation width in spaces for .prettierrc (default: 2, requires --prettier)",
    )
    parser.add_argument(
        "--recent",
        action="store_true",
        default=False,
        help="Browse & pick from recently created projects",
    )
    parser.add_argument(
        "--history-limit",
        dest="history_limit",
        type=int,
        default=10,
        help="Number of recent projects to display (default: 10)",
    )
    parser.add_argument(
        "--edit-config",
        dest="edit_config",
        action="store_true",
        default=False,
        help="Edit selected project configuration before creating",
    )
    parser.set_defaults(git=defaults["git"], install=defaults["install"])

    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(0)

    args = parser.parse_args()

    if args.recent:
        recent_projects = get_recent_projects(args.history_limit)
        selected = browse_history(recent_projects)
        if selected is None:
            print("❌ Cancelled.")
            sys.exit(1)

        args.name = selected["name"]
        args.lang = selected["lang"]
        args.template = selected["template"]
        args.author = selected["author"]
        args.version = selected["version"]
        args.license = selected["license"]
        args.description = selected["description"]
        args.lang_version = selected.get("lang_version")
        args.package_manager = selected.get("package_manager", "npm")
        args.test_framework = selected.get("test_framework")
        args.linter = selected.get("linter")
        args.docker = selected.get("docker", False)
        args.ci = selected.get("ci", "github")
        args.server = selected.get("server", False)
        args.server_port = selected.get("server_port", 3001)
        args.prettier = selected.get("prettier", False)
        args.indent_size = selected.get("indent_size", 2)

        if args.edit_config:
            print()
            config_dict = {
                "name": args.name,
                "lang": args.lang,
                "template": args.template,
                "version": args.version,
                "description": args.description,
            }
            edited = edit_project_config(config_dict)
            args.name = edited["name"]
            args.lang = edited["lang"]
            args.template = edited["template"]
            args.version = edited["version"]
            args.description = edited["description"]

    if not args.name:
        parser.print_help()
        sys.exit(0)

    if args.version == "__interactive__":
        args.version = get_version(defaults.get("version", "0.1.0"))

    if args.browse:
        args.output_dir = "browse"

    scaffold_project(args)
