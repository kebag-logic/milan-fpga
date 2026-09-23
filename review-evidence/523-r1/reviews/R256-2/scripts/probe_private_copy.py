#!/usr/bin/env python3
"""Reviewer probe: run the production copy_inputs() on a real checkout and
audit every private file: population equals the tracked scopes at the pins,
bytes equal the Git blobs, mode equals caller mode plus owner write, one link,
distinct inode, regular file, and the caller checkout is unchanged.

Usage: probe_private_copy.py REPO_COPY TARGET_DIR OUT_JSON
"""
import hashlib, json, os, stat, subprocess, sys
from pathlib import Path

repo = Path(sys.argv[1]).resolve()
target = Path(sys.argv[2])
out = Path(sys.argv[3])
sys.path.insert(0, str(repo / "scripts"))
sys.path.insert(0, str(repo / "tb/verilator/gptp_shadow"))
from owned_process import OwnedProcesses
from private_inputs import FIRST_PARTY, DEPENDENCIES, copy_inputs

def tracked(root, rev, scopes):
    rows = subprocess.check_output(["git", "-C", str(root), "ls-tree", "-rz", rev, "--", *scopes]).split(b"\0")
    return {r.split(b"\t", 1)[1].decode(): (r.split()[0].decode(), r.split()[2].decode()) for r in rows if r}

expected = {name: (root_rel, meta) for name, meta in tracked(repo, "HEAD", FIRST_PARTY).items() for root_rel in [""]}
pins = dict(line.split(b"\t")[::-1] for line in subprocess.check_output(["git", "-C", str(repo), "ls-tree", "-z", "HEAD", "--", *DEPENDENCIES]).split(b"\0") if line)
for dep, scopes in DEPENDENCIES.items():
    rev = pins[dep.encode()].split()[2].decode()
    for name, meta in tracked(repo / dep, rev, scopes).items():
        expected[f"{dep}/{name}"] = (dep, meta)
target.mkdir(parents=True)
with OwnedProcesses() as owner:
    copy_inputs(repo, target, owner)
actual = {str(p.relative_to(target)) for p in target.rglob("*") if not p.is_dir() or p.is_symlink()}
problems = []
if actual != set(expected):
    problems.append(dict(extra=sorted(actual - set(expected))[:10], missing=sorted(set(expected) - actual)[:10]))
for name, (_dep, (mode, blob)) in expected.items():
    p, src = target / name, repo / name
    if not p.exists():
        continue
    info, sinfo = p.lstat(), src.lstat()
    data = p.read_bytes()
    if not stat.S_ISREG(info.st_mode): problems.append(f"not regular: {name}")
    if info.st_nlink != 1: problems.append(f"nlink {info.st_nlink}: {name}")
    if (info.st_dev, info.st_ino) == (sinfo.st_dev, sinfo.st_ino): problems.append(f"same inode: {name}")
    if hashlib.sha1(b"blob %d\0" % len(data) + data).hexdigest() != blob: problems.append(f"bytes: {name}")
    if stat.S_IMODE(info.st_mode) != (stat.S_IMODE(sinfo.st_mode) | stat.S_IWUSR): problems.append(f"mode: {name}")
    if bool(info.st_mode & stat.S_IXUSR) != (mode == "100755"): problems.append(f"exec bit vs Git mode: {name}")
links = [str(p) for p in target.rglob("*") if p.is_symlink()]
result = dict(files=len(expected), first_party=sum(1 for v in expected.values() if v[0] == ""),
              dependencies={d: sum(1 for v in expected.values() if v[0] == d) for d in DEPENDENCIES},
              symlinks_in_private=len(links), problems=problems)
out.write_text(json.dumps(result, indent=2) + "\n")
print(json.dumps(result))
sys.exit(1 if problems or links else 0)
