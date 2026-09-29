#!/usr/bin/env python3
"""P4: compare the archived native service/capture evidence of the two merge-dev
packets (previous merge head 1f039cfe vs this head 4c2a30de), file by file.
Usage: p4_compare_native.py <author-mergedev dir> <author-mergedev2 dir>"""
import hashlib, json, sys
from pathlib import Path

old_root, new_root = map(Path, sys.argv[1:3])

def index(root, subdirs):
    out = {}
    for sub in subdirs:
        d = root / sub
        if not d.is_dir():
            continue
        for p in sorted(d.rglob("*")):
            if p.is_file():
                out.setdefault(p.name, p)
    return out

old = index(old_root, ["native-evidence", "raw/native-evidence", "raw/logs"])
new = index(new_root, ["native-evidence", "uncompressed/native-evidence", "uncompressed/logs"])

def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()

def diffs(a, b, path=""):
    if type(a) != type(b):
        yield path; return
    if isinstance(a, dict):
        for k in sorted(set(a) | set(b)):
            if k not in a or k not in b: yield f"{path}/{k}(missing)"
            else: yield from diffs(a[k], b[k], f"{path}/{k}")
    elif isinstance(a, list):
        if len(a) != len(b): yield f"{path}[len {len(a)}!={len(b)}]"; return
        for i, (x, y) in enumerate(zip(a, b)): yield from diffs(x, y, f"{path}[{i}]")
    elif a != b:
        yield path

same = differ = only_new = 0
for name in sorted(new):
    if name not in old:
        print(f"ONLY-NEW  {name}"); only_new += 1; continue
    if sha(old[name]) == sha(new[name]):
        print(f"IDENTICAL {name}"); same += 1; continue
    differ += 1
    if name.endswith(".json"):
        try:
            d = sorted(set(diffs(json.loads(old[name].read_text()), json.loads(new[name].read_text()))))
        except Exception as e:
            d = [f"unparsable: {e}"]
        print(f"DIFFERS   {name}: {len(d)} JSON paths")
        for x in d: print(f"            {x}")
    else:
        import difflib
        dl = [l for l in difflib.unified_diff(old[name].read_text(errors="replace").splitlines(),
              new[name].read_text(errors="replace").splitlines(), lineterm="", n=0)
              if l[:1] in "+-" and not l.startswith(("+++", "---"))]
        print(f"DIFFERS   {name}: {len(dl)} changed lines")
        for x in dl[:8]: print(f"            {x[:200]}")
for name in sorted(set(old) - set(new)):
    print(f"ONLY-OLD  {name}")
print(f"SUMMARY identical={same} differ={differ} only_new={only_new} only_old={len(set(old)-set(new))}")
