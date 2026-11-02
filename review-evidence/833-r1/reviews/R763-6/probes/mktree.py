#!/usr/bin/env python3
"""Copy a scripts/ tree to DEST/scripts and apply one mutant to owned_process.py.

Usage: python3 -I mktree.py SRC_SCRIPTS DEST NAME
NAME is a key of SRC's MUTANTS, a key of EXTRA below, or "none".
Each edit must match the product exactly once.
"""
import ast
import shutil
import sys
from pathlib import Path

#: Reviewer mutants of scripts/owned_process.py at a987b601 (round R763-6).
EXTRA = {
    # Row 6 / not-pinned item 2: new descendants get SIGTERM during grace, which
    # includes a command the resumed shell's trap starts when the resume is in grace.
    "rv6-sigterm-to-new": [(
        "                    if (pid, start) not in initial:\n                        continue\n                elif",
        "                    pass\n                elif")],
    # Same, narrowed to the trap's commands only: a trap command is SIGTERMed in grace.
    "rv6-sigterm-trap-commands": [(
        "                    if (pid, start) not in initial:\n                        continue\n                elif",
        "                    if (pid, start) not in initial and resumed is None:\n                        continue\n                elif")],
    # Row 2 / row 5: the cancelled shell is sent SIGTERM (and so SIGCONT) by cleanup too.
    "rv6-sigterm-cancelled-shell": [(
        "if pid == root_pid and self.root_notified and (resumed is None or clock < kill_all):",
        "if pid == root_pid and self.root_notified and signum == signal.SIGKILL"
        " and (resumed is None or clock < kill_all):")],
    # Row 1: the signal is sent before the start time is rechecked.
    "rv6-signal-before-recheck": [(
        "            identity = _identity(pid)\n            if identity is None or identity[1] != start:\n"
        "                return False\n            self._signal(fd, signum)\n",
        "            self._signal(fd, signum)\n            identity = _identity(pid)\n"
        "            if identity is None or identity[1] != start:\n                return False\n")],
    # Row 6: the trap window is 9.5 s, not 10 s.
    "rv6-trap-9.5s": [("TRAP_SECONDS = 10.0", "TRAP_SECONDS = 9.5")],
    # Row 9: the pass cap is 0.6 s.
    "rv6-pass-cap-0.6s": [("MAX_PASS_SECONDS = 0.5", "MAX_PASS_SECONDS = 0.6")],
    # Row 16: the report's age is the start tick over 100, not the clock tick rate.
    "rv6-report-age-hz100": [("int(fields[19]) / os.sysconf('SC_CLK_TCK')", "int(fields[19]) / 1000")],
    # Row 12: cleanup returns once the census lists only processes it just collected.
    "rv6-return-before-confirm": [(
        "            owned = {pid: entry for pid, entry in census.items() if pid not in reaped}\n",
        "            owned = {pid: entry for pid, entry in census.items() if pid not in reaped}\n"
        "            if not owned:\n                return\n")],
}


def mutants_of(src: Path) -> dict:
    """MUTANTS from SRC's process_test_support.py, read without importing it."""
    tree = ast.parse((src / "process_test_support.py").read_text())
    for node in tree.body:
        if isinstance(node, ast.AnnAssign) and getattr(node.target, "id", "") == "MUTANTS":
            return {key: list(value[2:]) for key, value in ast.literal_eval(node.value).items()}
    raise SystemExit("no MUTANTS")


def main() -> int:
    src, dest, name = Path(sys.argv[1]), Path(sys.argv[2]), sys.argv[3]
    edits = EXTRA.get(name)
    if edits is None:
        edits = [] if name == "none" else mutants_of(src)[name]
    shutil.copytree(src, dest / "scripts", ignore=shutil.ignore_patterns("__pycache__"))
    product = dest / "scripts/owned_process.py"
    text = product.read_text()
    for old, new in edits:
        assert text.count(old) == 1, f"mutant {name} does not apply: {old!r}"
        text = text.replace(old, new)
    product.write_text(text)
    print(f"{name}: {len(edits)} edit(s) applied in {dest}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
