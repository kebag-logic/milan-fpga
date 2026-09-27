#!/usr/bin/env python3
"""Regenerate every configs/endstation_*.yaml with each tree's own builder and
compare all artifacts byte for byte (and against the head's tracked
configs/generated/). usage: artifact_identity.py BASE_TREE HEAD_TREE OUTDIR"""
import hashlib, json, subprocess, sys
from pathlib import Path

base, head, out = (Path(p).resolve() for p in sys.argv[1:4])
res = {}
for label, tree in (("base", base), ("head", head)):
    res[label] = {}
    for cfg in sorted((tree / "configs").glob("endstation_*.yaml")):
        tgt = out / label / cfg.stem
        subprocess.run([sys.executable, str(tree / "sw/builder/endstation_builder.py"),
                        str(cfg), "-o", str(tgt)], check=True, cwd=str(tree),
                       stdout=subprocess.DEVNULL)
        res[label][cfg.stem] = {str(p.relative_to(tgt)): hashlib.sha256(p.read_bytes()).hexdigest()
                                for p in sorted(tgt.rglob("*")) if p.is_file()}
tracked = {}
for d in sorted((head / "configs/generated").iterdir()):
    if d.is_dir():
        tracked[d.name] = {p.name: hashlib.sha256(p.read_bytes()).hexdigest()
                           for p in sorted(d.rglob("*")) if p.is_file()}
ok = True
for cfg in res["head"]:
    same = res["base"].get(cfg) == res["head"][cfg]
    ok &= same
    # compare by file name: the tracked tree keeps only gen/adp_shape_defaults.svh
    flat = {k.rsplit("/", 1)[-1]: v for k, v in res["head"][cfg].items()}
    tr = tracked.get(cfg, {})
    common = sorted(set(flat) & set(tr))
    tmatch = all(flat[k] == tr[k] for k in common)
    print(f"{cfg}: {len(res['head'][cfg])} artifacts; base==head {same}; "
          f"vs tracked configs/generated: {len(common)} common files, identical {tmatch}")
(out / "identity.json").write_text(json.dumps(res, indent=1, sort_keys=True) + "\n")
print("PASS" if ok and len(res["head"]) == 5 else "FAIL")
sys.exit(0 if ok else 1)
