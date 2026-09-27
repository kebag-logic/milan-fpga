#!/usr/bin/env python3
"""Generate every configs/endstation_*.yaml with sw/builder/endstation_builder.py
from two trees (the reviewed head clone and an extracted base tree) and compare
every emitted artifact byte for byte.

Usage: artifact_identity.py <head-tree> <base-tree> <out-dir>
"""
import hashlib
import json
import subprocess
import sys
from pathlib import Path

head, base, out = (Path(p).resolve() for p in sys.argv[1:4])
DRIVER = ("import sys; sys.path.insert(0, sys.argv[1] + '/sw/builder'); "
          "import endstation_builder as b; b.build(sys.argv[2], sys.argv[3])")


def generate(tree, tag):
    result = {}
    for cfg in sorted((tree / "configs").glob("endstation_*.yaml")):
        target = out / tag / cfg.stem
        subprocess.run([sys.executable, "-c", DRIVER, str(tree), str(cfg), str(target)],
                       cwd=str(tree), check=True, capture_output=True)
        result[cfg.stem] = {str(p.relative_to(target)): hashlib.sha256(p.read_bytes()).hexdigest()
                            for p in sorted(target.rglob("*")) if p.is_file()}
    return result


h, b = generate(head, "head"), generate(base, "base")
rc = 0
for cfg in sorted(set(h) | set(b)):
    same = h.get(cfg) == b.get(cfg)
    rc |= not same
    print(f"{cfg}: {len(h.get(cfg, {}))} head / {len(b.get(cfg, {}))} base artifacts: "
          f"{'byte-identical' if same else 'DIFFER'}")
print(f"configs={len(h)} artifacts={sum(len(v) for v in h.values())} "
      f"{'ALL IDENTICAL' if rc == 0 else 'DIFFERENCES FOUND'}")
(out / "hashes.json").write_text(json.dumps({"head": h, "base": b}, indent=2) + "\n")
sys.exit(rc)
