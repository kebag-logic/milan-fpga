#!/usr/bin/env python3
"""Undo each round-4 generator change in a disposable copy and run --check.

  m1  register_sv.py      Interpreter.loop: never read a loop as one selection
  m2  register_page.py    named(): return the row's term unchanged
  m3  register_fields.py  the x[i*w +: w] word-index branch disabled

Usage: python3 -I mutants_generator_delta.py REPO WORKDIR PYTHON
PYTHON must have wavedrom==2.0.3.post3. Prints one line per mutant: rc and last line.
"""
import shutil
import subprocess
import sys
from pathlib import Path

repo, work, python = Path(sys.argv[1]).resolve(), Path(sys.argv[2]).resolve(), sys.argv[3]
EDITS = {
    "m1": ("scripts/register_sv.py", "        chosen = selection(st)\n", "        chosen = None\n"),
    "m2": ("scripts/register_page.py",
           "    for wire, phrase in wording.phrases.items():\n        definition",
           "    return term\n    for wire, phrase in wording.phrases.items():\n        definition"),
    "m3": ("scripts/register_fields.py",
           '            if start.unknown and node[2][0] == "bin" and node[2][1] == "*" and \\\n',
           '            if False and start.unknown and node[2][0] == "bin" and node[2][1] == "*" and \\\n'),
}
for name, (path, old, new) in EDITS.items():
    tree = work / f"mut_{name}"
    if tree.exists():
        shutil.rmtree(tree)
    shutil.copytree(repo, tree, ignore=shutil.ignore_patterns(".git"), symlinks=True)
    text = (tree / path).read_text(encoding="utf-8")
    assert text.count(old) == 1, f"{name}: anchor not unique"
    (tree / path).write_text(text.replace(old, new), encoding="utf-8")
    ran = subprocess.run([python, "-I", "scripts/gen_register_reference.py", "--check"], cwd=tree,
                         capture_output=True, text=True, check=False)
    last = (ran.stdout + ran.stderr).strip().splitlines()[-1:]
    print(f"{name} {path} rc={ran.returncode} {last}")
