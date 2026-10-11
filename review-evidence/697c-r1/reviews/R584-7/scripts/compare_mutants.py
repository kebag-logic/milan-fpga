#!/usr/bin/env python3
"""usage: compare_mutants.py <base.json> <head.json> <base tree> <head tree>
For every control-campaign plant, by name: applies base's (old,new) to the base tree's file and head's to the
head tree's file (a tsn-c-stack/ path is the head's submodule), strips comments with the C preprocessor
(-fpreprocessed) and compares the two mutated programs token by token; compares the kills (arm, test, words).
Also compares the AECP campaign's defects field by field."""
import json, subprocess, sys
from pathlib import Path
b, h = (json.load(open(p)) for p in sys.argv[1:3])
bt, ht = Path(sys.argv[3]), Path(sys.argv[4])
def toks(text):
    r = subprocess.run(["gcc", "-fpreprocessed", "-dD", "-E", "-P", "-x", "c", "-"], input=text, text=True,
                       capture_output=True)
    return r.stdout.split()
def where(tree, path, stack):
    if path.startswith("tsn-c-stack/"):
        return tree / "third_party/tsn-c-stack" / path.removeprefix("tsn-c-stack/")
    return tree / "sw/firmware/ctrl" / path
LEGACY = {"src/adp.c": "adp/adp.c", "src/acmp.c": "acmp/acmp.c", "src/maap.c": "maap/maap.c",
          "include/adp.h": "adp/adp.h", "include/acmp.h": "acmp/acmp.h", "include/maap.h": "maap/maap.h"}
bm = {m["name"]: m for m in b["ctrl"]}; hm = {m["name"]: m for m in h["ctrl"]}
print(f"control plants: base {len(b['ctrl'])} head {len(h['ctrl'])}; names only in base {sorted(bm.keys()-hm.keys())}; only in head {sorted(hm.keys()-bm.keys())}")
same = differ = textsame = 0; kills_differ = []
for name in sorted(bm.keys() & hm.keys()):
    x, y = bm[name], hm[name]
    fx = where(bt, x["path"], False).read_text(); fy = where(ht, y["path"], True).read_text()
    if y["path"].startswith("tsn-c-stack/") and LEGACY.get(y["path"].removeprefix("tsn-c-stack/")) != x["path"]:
        print(f"PATH MAP {name}: {x['path']} -> {y['path']}"); differ += 1; continue
    if fx.count(x["old"]) != 1 or fy.count(y["old"]) != 1:
        print(f"ANCHOR {name}: base {fx.count(x['old'])} head {fy.count(y['old'])}"); differ += 1; continue
    textsame += (x["old"], x["new"]) == (y["old"], y["new"])
    if toks(fx.replace(x["old"], x["new"])) == toks(fy.replace(y["old"], y["new"])) and toks(fx) == toks(fy):
        same += 1
    else:
        differ += 1; print(f"PROGRAM DIFFERS {name}")
    if x["kills"] != y["kills"]:
        kills_differ.append((name, x["kills"], y["kills"]))
print(f"mutated programs token-identical: {same}; differing: {differ}; plants with unchanged (old,new) text: {textsame}")
print(f"plants whose kills (arm, test, words) differ: {len(kills_differ)}")
for k in kills_differ:
    print("  KILLS", k[0]); print("    base:", k[1]); print("    head:", k[2])
if "aecp" in b and "aecp" in h:
    print(f"AECP defects: base {len(b['aecp'])} head {len(h['aecp'])}; identical: {b['aecp'] == h['aecp']}")
else:
    print("AECP:", b.get("aecp_error"), h.get("aecp_error"))
