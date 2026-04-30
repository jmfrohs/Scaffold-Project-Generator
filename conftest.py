import platform
import sys
import time

import pytest

GREEN  = "\033[32m"
RED    = "\033[31m"
YELLOW = "\033[33m"
BOLD   = "\033[1m"
RESET  = "\033[0m"

_W = 72


def _bar(text, char="=", width=_W):
    inner = f" {text} "
    pad = max(0, width - len(inner))
    return char * (pad // 2) + inner + char * (pad - pad // 2)


class AlignedReporter:
    def __init__(self, config):
        self._config = config
        self._total = 0
        self._current = 0
        self._max_len = 0
        self._failed = []
        self._start = time.time()

    def pytest_sessionstart(self, session):
        self._start = time.time()
        try:
            import pluggy
            pluggy_ver = pluggy.__version__
        except Exception:
            pluggy_ver = "?"
        sys.stdout.write(_bar("test session starts") + "\n")
        sys.stdout.write(
            f"platform {platform.system().lower()} -- "
            f"Python {platform.python_version()}, "
            f"pytest-{pytest.__version__}, pluggy-{pluggy_ver} -- {sys.executable}\n"
        )
        sys.stdout.write(f"rootdir: {self._config.rootdir}\n")
        sys.stdout.flush()

    def pytest_collection_finish(self, session):
        self._total = len(session.items)
        self._max_len = max((len(i.nodeid) for i in session.items), default=0)
        sys.stdout.write(f"collected {self._total} items\n\n")
        sys.stdout.flush()

    def pytest_runtest_logreport(self, report):
        if report.when == "call":
            pass
        elif report.when == "setup" and report.failed:
            pass
        else:
            return

        self._current += 1
        pad = self._max_len - len(report.nodeid) + 1

        if report.passed:
            status = f"{GREEN}PASSED{RESET}"
        elif report.failed:
            status = f"{RED}FAILED{RESET}"
            self._failed.append(report)
        else:
            status = f"{YELLOW}SKIPPED{RESET}"

        sys.stdout.write(f"{report.nodeid}{' ' * pad} {status}\n")
        sys.stdout.flush()

    def pytest_sessionfinish(self, session, exitstatus):
        elapsed = time.time() - self._start
        n_fail = len(self._failed)
        n_pass = self._current - n_fail

        if self._failed:
            sys.stdout.write(f"\n{'=' * _W}\n{BOLD}{RED}FAILURES{RESET}\n")
            for rep in self._failed:
                sys.stdout.write(f"{'_' * _W}\n{BOLD}{RED}{rep.nodeid}{RESET}\n")
                if rep.longrepr:
                    sys.stdout.write(str(rep.longrepr) + "\n")

        cov_str = ""
        try:
            import io
            import coverage as coverage_module
            cov = coverage_module.Coverage()
            cov.load()
            buf = io.StringIO()
            total_pct = cov.report(file=buf)
            cov_str = f" | overall coverage: {GREEN}{int(total_pct)}%{RESET if n_fail == 0 else ''}"
        except Exception:
            pass

        parts = []
        if n_fail:
            parts.append(f"{n_fail} failed")
        if n_pass:
            parts.append(f"{n_pass} passed")
        summary = ", ".join(parts) + f" in {elapsed:.2f}s"
        color = RED if n_fail else GREEN
        sys.stdout.write(f"\n{color}{_bar(summary)}{RESET}{cov_str}\n")
        sys.stdout.flush()


def pytest_configure(config):
    config.pluginmanager.register(AlignedReporter(config), "aligned_reporter")

