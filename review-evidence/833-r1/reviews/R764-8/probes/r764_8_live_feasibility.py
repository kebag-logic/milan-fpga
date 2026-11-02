#!/usr/bin/env python3
"""Feasibility for #833: owner_stated_seconds with a LIVE new descendant pins the liveness probes.

Usage: python3 -I r764_8_live_feasibility.py <repo-root> <scratch-dir>
Copies scripts/ per case, adds two listings to owner_stated_seconds whose new descendant is a real
sleeping process (so the product's liveness check sees it live), applies the case's mutant (if any)
from r764_8_live_probes.PROBES, and runs `--control owner_stated_seconds`.
"""
import shutil
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from r764_8_live_probes import PROBES  # noqa: E402

ANCHOR = '                kept(f"a {when} resume and its trap command", cell(resume, command), window(resume), shell)\n'
ADDED = '''        sleeper = __import__("subprocess").Popen(["sleep", "60"])
        live_new = sleeper.pid
        names[live_new] = "trap command"
        try:
            kept("a live new descendant beside a stopped shell",
                 lambda clock: {shell: (owner_pid, "2"), child: (shell, "4"),
                                **({live_new: (shell, "9")} if clock else {})},
                 [(0, "SIGTERM", "child"), (2, "SIGKILL", "child"), (2, "SIGKILL", "trap command"),
                  (14, "SIGKILL", "shell"), (14, "SIGKILL", "child"), (14, "SIGKILL", "trap command"),
                  (14, "verdict")], shell)
            kept("a second-pass resume and its live trap command",
                 lambda clock: {shell: (owner_pid, "2"), **({child: (shell, "4")} if clock < TICK else
                                                           {live_new: (shell, "9")} if clock > TICK else {})},
                 window(TICK), shell)
        finally:
            sleeper.kill()
            sleeper.wait()
'''


def main() -> int:
    root, scratch = Path(sys.argv[1]).resolve(), Path(sys.argv[2]).resolve()
    for name in ("none", "sigterm-to-live-new", "live-trap-command-unspared-after-in-grace-resume"):
        tree = scratch / name
        shutil.rmtree(tree, ignore_errors=True)
        shutil.copytree(root / "scripts", tree / "scripts", ignore=shutil.ignore_patterns("__pycache__"))
        test = tree / "scripts/test_suite_cancellation.py"
        text = test.read_text()
        assert text.count(ANCHOR) == 1
        test.write_text(text.replace(ANCHOR, ANCHOR + ADDED))
        product = tree / "scripts/owned_process.py"
        text = product.read_text()
        for old, new in PROBES.get(name, ()):
            assert text.count(old) == 1
            text = text.replace(old, new)
        product.write_text(text)
        run = subprocess.run([sys.executable, "-B", str(test), "--control", "owner_stated_seconds"], cwd=tree,
                             stdin=subprocess.DEVNULL, capture_output=True, text=True, timeout=300)
        lines = [line for line in (run.stdout + run.stderr).splitlines() if line.strip()]
        print(f"{name} + live listings: {'red' if run.returncode else 'green'} rc {run.returncode}: "
              f"{lines[-1][:300] if lines else ''}", flush=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
