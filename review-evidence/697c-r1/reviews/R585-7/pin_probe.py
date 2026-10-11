#!/usr/bin/env python3
"""Reproduce pin checks in a disposable clone; creates no commits."""
import argparse
import hashlib
import os
from pathlib import Path
import shutil
import subprocess
import sys

ap = argparse.ArgumentParser()
ap.add_argument("checkout", type=Path)
ap.add_argument("scratch", type=Path)
a = ap.parse_args()
root = a.checkout.resolve()
work = a.scratch.resolve() / "pin-probe"
work.mkdir(parents=True, exist_ok=True)
sys.path.insert(0, str(root / "sw/firmware/ctrl/test"))
from ctrl_build import Refusal, stack_pin, stack_gitlink

def git(*args, data=None, env=None):
    return subprocess.run(["git", "-C", str(clone), *args], input=data,
                          stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                          check=True, env=env).stdout

clone = work / "stack"
if clone.exists():
    shutil.rmtree(clone)
subprocess.run(["git", "clone", "--quiet", "--no-hardlinks",
                str(root / "third_party/tsn-c-stack"), str(clone)], check=True)
pin = stack_gitlink()
git("checkout", "--quiet", "--detach", pin)
print("pin:", pin)
print("unmodified:", stack_pin(clone, pin))
header = clone / "include/adp.h"
original = header.read_bytes()
assert original.count(b"#define ADP_ADVERTISE_MS 5000u") == 1
header.write_bytes(original.replace(b"#define ADP_ADVERTISE_MS 5000u",
                                    b"#define ADP_ADVERTISE_MS 9000u"))
try:
    stack_pin(clone, pin)
    raise AssertionError("ordinary changed source was accepted")
except Refusal as exc:
    print("ordinary edit: REFUSED", exc)
old_tree = git("rev-parse", pin + ":include").decode().strip()
new_blob = git("hash-object", "-w", "include/adp.h").decode().strip()
entries = git("ls-tree", "-z", old_tree).split(b"\0")
changed = []
for entry in filter(None, entries):
    meta, name = entry.split(b"\t", 1)
    if name == b"adp.h":
        mode, kind, _ = meta.split()
        entry = mode + b" " + kind + b" " + new_blob.encode() + b"\t" + name
    changed.append(entry)
new_tree = git("mktree", "-z", data=b"\0".join(changed) + b"\0").decode().strip()
git("replace", old_tree, new_tree)
print("replaced tree:", old_tree, "->", new_tree)
print("HEAD still:", git("rev-parse", "HEAD").decode().strip())
canonical = git("show", pin + ":include/adp.h",
                env={**os.environ, "GIT_NO_REPLACE_OBJECTS": "1"})
assert canonical == original and header.read_bytes() != canonical
print("canonical header sha256:", hashlib.sha256(canonical).hexdigest())
print("worktree header sha256:", hashlib.sha256(header.read_bytes()).hexdigest())
macros = subprocess.check_output(['cc', '-dM', '-E', '-I', str(clone / 'include'),
                                  '-include', 'adp.h', '-x', 'c', '/dev/null'], text=True)
advertise = next(line for line in macros.splitlines() if line.startswith('#define ADP_ADVERTISE_MS '))
print('compiler reads:', advertise)
assert advertise == '#define ADP_ADVERTISE_MS 9000u'
try:
    accepted = stack_pin(clone, pin)
except Refusal as exc:
    print("replacement control: REFUSED", exc)
else:
    print("replacement control: ESCAPED; pin check accepted", accepted)
git("replace", "-d", old_tree)
header.write_bytes(original)
print("restored clone:", stack_pin(clone, pin))
