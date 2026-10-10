#!/usr/bin/env python3
"""For every mutant name in the dev and head tables, plant it into that side's own source and compare the
mutated files' C token streams (comments dropped). Same tokens = the same code defect.
usage: compare_mutants.py DEV_JSON HEAD_JSON DEV_TREE HEAD_TREE STACK"""
import json, sys, subprocess, tempfile, re
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
dev = {m["name"]: m for m in json.load(open(sys.argv[1]))}
head = {m["name"]: m for m in json.load(open(sys.argv[2]))}
dev_tree, head_tree, stack = map(Path, sys.argv[3:6])
def toks(text, suffix):
    with tempfile.NamedTemporaryFile("w", suffix=suffix, delete=False) as f:
        f.write(text)
    out = subprocess.run(["clang", "-cc1", "-x", "c", "-std=c11", "-dump-raw-tokens", f.name],
                         capture_output=True, text=True).stderr
    res = []
    for line in out.splitlines():
        kind = line.split(" ", 1)[0]
        i = line.find("'"); mm = list(re.finditer(r"'\s+Loc=<", line))
        spell = line[i + 1:mm[-1].start()]
        if kind in ("comment", "eof", "eod"):
            continue
        if kind == "unknown" and spell.replace("\\n", "").replace("\\t", "").strip() == "":
            continue
        res.append((kind, spell))
    Path(f.name).unlink()
    return res
def src(tree, path):
    if path.startswith("tsn-c-stack/"):
        return stack / path.removeprefix("tsn-c-stack/")
    return tree / "sw/firmware/ctrl" / path
stats = {"same-plant": 0, "same-tokens": 0, "DIFFERENT": 0, "missing": 0}
kills_changed = []
for name in sorted(set(dev) | set(head)):
    d, h = dev.get(name), head.get(name)
    if d is None or h is None:
        print(f"MISSING {name}: dev {d is not None} head {h is not None}"); stats["missing"] += 1; continue
    if d["kills"] != h["kills"]:
        kills_changed.append((name, d["kills"], h["kills"]))
    if d["path"] == h["path"] and d["old"] == h["old"] and d["new"] == h["new"]:
        stats["same-plant"] += 1; continue
    dt = src(dev_tree, d["path"]).read_text(); ht = src(head_tree, h["path"]).read_text()
    assert dt.count(d["old"]) == 1 and ht.count(h["old"]) == 1, name
    suffix = ".h" if d["path"].endswith(".h") else ".c"
    a = toks(dt.replace(d["old"], d["new"]), suffix); b = toks(ht.replace(h["old"], h["new"]), suffix)
    ua = toks(dt, suffix); ub = toks(ht, suffix)
    if a == b and ua == ub and a != ua:
        stats["same-tokens"] += 1
        print(f"same-tokens {name}: {d['path']} -> {h['path']}")
    else:
        stats["DIFFERENT"] += 1
        print(f"DIFFERENT {name}: {d['path']} -> {h['path']} mutated-equal={a == b} base-equal={ua == ub} effective={a != ua}")
for name, a, b in kills_changed:
    print(f"KILLS-CHANGED {name}:\n  dev  {a}\n  head {b}")
print(stats, "kills changed:", len(kills_changed))
