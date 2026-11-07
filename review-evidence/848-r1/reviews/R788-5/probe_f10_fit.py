#!/usr/bin/env python3
"""Does one arm, with no added line and within the 120-column limit, kill the D0-before-archive mutant?

Usage: probe_f10_fit.py REPO SHA WORKDIR
"""
import shutil
import subprocess
import sys
from pathlib import Path

REPO, SHA, WORK = sys.argv[1], sys.argv[2], Path(sys.argv[3])
SCRIPT = "scripts/docs_inventory.py"
OLD = '("archive page is obsolete with its successor", lambda root: None, 0,'
NEW = '("a listed archive page", edit_data(lambda d: d["verified_pages"].append("docs/history/v1/OLD.md")), 0,'
BRANCH = 'verified = "archive" if path.startswith(ARCHIVE_PREFIX) else "D0" if path in checked else "area lane"'
SWAP = 'verified = "D0" if path in checked else "archive" if path.startswith(ARCHIVE_PREFIX) else "area lane"'


def tree(name, swap):
    root = WORK / name
    if root.exists():
        shutil.rmtree(root)
    subprocess.run(["git", "clone", "-q", "--no-hardlinks", "--no-checkout", REPO, str(root)], check=True)
    subprocess.run(["git", "-C", str(root), "checkout", "-q", "--detach", SHA], check=True)
    path = root / SCRIPT
    text = path.read_text(encoding="utf-8")
    assert OLD in text and BRANCH in text
    text = text.replace(OLD, NEW)
    if swap:
        text = text.replace(BRANCH, SWAP)
    path.write_text(text, encoding="utf-8")
    lines = text.splitlines()
    done = subprocess.run([sys.executable, "-I", SCRIPT, "--selftest"], cwd=root, capture_output=True, text=True,
                          check=False)
    first = (done.stdout + done.stderr).splitlines()[0][:170]
    print(f"{name}: module lines {len(lines)}; longest line {max(map(len, lines))}; --selftest rc {done.returncode} [{first}]")


WORK.mkdir(parents=True, exist_ok=True)
tree("fit_control", False)
tree("fit_mutant", True)
