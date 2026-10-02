#!/usr/bin/env python3
"""Plant each gen_ucode.py patch in a copy of a tree's hdl/ and record the ROM words it changes.

usage: plant_words.py OUT.json TREE PATCH...
Writes {patch_name: {"rc": git-apply rc, "sha256": mutated ucode.hex sha,
"words": {index: [base, mutated]}}}; base is TREE's unmutated ROM.
"""
import hashlib, json, shutil, subprocess, sys, tempfile
from pathlib import Path
out, tree, patches = Path(sys.argv[1]), Path(sys.argv[2]), [Path(p).resolve() for p in sys.argv[3:]]
def rom(root):
    hexf = root / "u.hex"
    subprocess.run([sys.executable, "-B", str(root / "hdl/aecp/ucode/gen_ucode.py"), "-o", str(hexf)],
                   check=True, capture_output=True)
    t = hexf.read_text(); return t, t.split()
res = {}
with tempfile.TemporaryDirectory() as tmp:
    base_root = Path(tmp) / "base"; shutil.copytree(tree / "hdl", base_root / "hdl")
    _, base = rom(base_root)
    for p in patches:
        r = Path(tmp) / p.stem; shutil.copytree(tree / "hdl", r / "hdl")
        a = subprocess.run(["git", "apply", str(p)], cwd=r, capture_output=True, text=True)
        if a.returncode:
            res[p.stem] = {"rc": a.returncode, "err": a.stderr}; continue
        t, w = rom(r)
        res[p.stem] = {"rc": 0, "sha256": hashlib.sha256(t.encode()).hexdigest(),
                       "words": {i: [base[i], w[i]] for i in range(len(w)) if w[i] != base[i]}}
out.write_text(json.dumps(res, indent=1, sort_keys=True) + "\n")
print(out.name, len(res), "patches;", sum(1 for v in res.values() if v["rc"]), "refused")
