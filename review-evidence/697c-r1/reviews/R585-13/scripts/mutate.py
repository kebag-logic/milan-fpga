#!/usr/bin/env python3
"""Mutation probes of the pin proof's round-14 delta: each mutant replaces one exact fragment of a file of a
disposable milan-fpga checkout, runs run_pin_controls.py on it, reports which controls escaped, and restores
the file's bytes (checked against their sha256 before and after).

usage: mutate.py <disposable checkout> <work root>
"""
import hashlib
import subprocess
import sys
from pathlib import Path

repo, root = Path(sys.argv[1]).resolve(), Path(sys.argv[2]).resolve()
runner = Path(__file__).resolve().parent / "run_pin_controls.py"
B = "sw/firmware/ctrl/test/ctrl_build.py"
STORED_TREE = ('data = stored(stack, "tree", oid, algorithm, f"the pinned {prefix} tree" if prefix else '
               '"the pinned root tree")')
MUTANTS = [
    ("M1 no hash compared", B, "    if held != oid:\n", "    if False:\n"),
    ("M2 core.fsmonitor=false removed", B, '["git", "-c", "core.fsmonitor=false", "-C",', '["git", "-C",'),
    ("M3 trees read unhashed", B, STORED_TREE, 'data = git(stack, "cat-file", "tree", oid).raw'),
    ("M4 root tree read unhashed", B, STORED_TREE,
     'data = git(stack, "cat-file", "tree", oid).raw if not prefix else ' + STORED_TREE[7:]),
    ("M5 commit read unhashed", B, 'head, _, _ = stored(stack, "commit", pin, algorithm, "the pinned commit")',
     'head, _, _ = git(stack, "cat-file", "commit", pin).raw'),
    ("M6 no subtree walked", B, '                trees.append((f"{prefix}{name}/", child))\n',
     '                pass\n'),
]
root.mkdir(parents=True, exist_ok=True)
for label, rel, old, new in MUTANTS:
    path = repo / rel
    original = path.read_bytes()
    digest = hashlib.sha256(original).hexdigest()
    text = original.decode()
    if text.count(old) != 1:
        print(f"{label}: fragment found {text.count(old)} times, not applied")
        continue
    path.write_text(text.replace(old, new), encoding="utf-8")
    work = root / label.split()[0]
    try:
        res = subprocess.run([sys.executable, "-I", str(runner), str(repo), str(work)], capture_output=True,
                             text=True, timeout=900)
    finally:
        path.write_bytes(original)
    assert hashlib.sha256(path.read_bytes()).hexdigest() == digest
    out = res.stdout + res.stderr
    (root / f"{label.split()[0]}.log").write_text(out, encoding="utf-8")
    escaped = [ln[:220] for ln in out.splitlines() if ln.startswith("[ESCAPED]") or ln.startswith("  [CENSUS]")]
    summary = [ln for ln in out.splitlines() if ln.startswith("SUMMARY")]
    print(f"{label}: exit {res.returncode}; {summary[0] if summary else 'no summary: ' + out.strip()[-300:]}")
    for ln in escaped:
        print(f"    {ln}")
print("file bytes restored:", subprocess.run(["git", "-C", str(repo), "status", "--porcelain"], capture_output=True,
                                              text=True).stdout.strip() or "clean")
