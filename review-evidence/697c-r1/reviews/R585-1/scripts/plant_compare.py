#!/usr/bin/env python3
"""Compare the planted programs of the base and head campaigns token for token.

For each plant name in both dumps, the base plant is written into the base file text and the head plant into
the head file text; both results (and both unplanted files) are reduced to C tokens with comments removed by
the preprocessor (token_identity.tokens). A plant is EQUIVALENT when the planted programs are token-identical
whenever the unplanted programs are. Kills (arm, test, words) are compared too.
usage: plant_compare.py <base.json> <head.json>"""
import json, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from token_identity import tokens  # noqa: E402

base = {r["name"]: r for r in json.load(open(sys.argv[1]))}
head = {r["name"]: r for r in json.load(open(sys.argv[2]))}
print(f"plants: base {len(base)}, head {len(head)}; only base {sorted(set(base)-set(head))}; "
      f"only head {sorted(set(head)-set(base))}")
cache = {}
def toks(text):
    if text not in cache:
        cache[text] = tokens(text.encode())
    return cache[text]
bad = same_path = moved = killdiff = 0
for name in sorted(set(base) & set(head)):
    b, h = base[name], head[name]
    bt, ht = Path(b["file"]).read_text(), Path(h["file"]).read_text()
    if bt.count(b["old"]) != 1 or ht.count(h["old"]) != 1:
        print(f"ANCHOR {name}: base {bt.count(b['old'])} head {ht.count(h['old'])}"); bad += 1; continue
    try:
        orig_eq = toks(bt) == toks(ht)
        plant_eq = toks(bt.replace(b["old"], b["new"])) == toks(ht.replace(h["old"], h["new"]))
    except SystemExit as exc:
        print(f"LEX {name}: {exc}"); bad += 1; continue
    if b["path"] == h["path"]:
        same_path += 1
    else:
        moved += 1
    if not orig_eq:
        print(f"NOTE {name}: unplanted files differ in tokens ({b['path']} vs {h['path']})")
    if orig_eq and not plant_eq:
        print(f"DIFFERENT {name}: planted programs differ ({b['path']} vs {h['path']})"); bad += 1
    if b["kills"] != h["kills"]:
        killdiff += 1
        for kb, kh in zip(b["kills"], h["kills"]):
            if kb != kh:
                print(f"KILL {name}: base {kb} head {kh}")
        if len(b["kills"]) != len(h["kills"]):
            print(f"KILL {name}: base {len(b['kills'])} kills, head {len(h['kills'])}")
print(f"compared {len(set(base) & set(head))}: {moved} moved into the stack, {same_path} same path; "
      f"{bad} not equivalent; {killdiff} with changed kills")
sys.exit(1 if bad or set(base) ^ set(head) else 0)
