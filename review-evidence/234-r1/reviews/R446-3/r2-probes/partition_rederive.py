#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
"""Reviewer re-derivation of the round-2 "rest of the wrapper" partition.

Reads the published A and B 1x1 standalone records (review-evidence/234-r1/
author/evidence/{A,B}-record-ooc-1x1.json) and the two pages at the head.
A term is one listed scope's own logic: the scope minus its listed direct
children. The partition is every term outside u_nvm_port (the scope and its
listed descendants). Prints the derived figures and checks each against the
sentences of both pages.

Usage: partition_rederive.py <checkout> <evidence-dir>; exit 0 when all hold.
"""

import json
from pathlib import Path
import sys

REPO, EV = Path(sys.argv[1]), Path(sys.argv[2])
A = json.loads((EV / "A-record-ooc-1x1.json").read_text())["scopes"]
B = json.loads((EV / "B-record-ooc-1x1.json").read_text())["scopes"]


def parent(key: str) -> str:
    return "wrapper" if "/" not in key else key.rsplit("/", 1)[0]


def own(scopes: dict, key: str, figure: str) -> int:
    children = [other for other in scopes if other != "wrapper" and other != key and parent(other) == key]
    return scopes[key][figure] - sum(scopes[child][figure] for child in children)


keys = sorted(set(A) | set(B))
assert set(A) == set(B), f"scope sets differ: {set(A) ^ set(B)}"
nvm = [key for key in keys if key.rsplit("/", 1)[-1] == "u_nvm_port"]
assert len(nvm) == 1, nvm
inside = {key for key in keys if key == nvm[0] or key.startswith(nvm[0] + "/")}
terms = [key for key in keys if key not in inside]
delta = {key: {f: own(B, key, f) - own(A, key, f) for f in ("LUT", "FF")} for key in terms}
net = {f: sum(d[f] for d in delta.values()) for f in ("LUT", "FF")}
absolute = {f: sum(abs(d[f]) for d in delta.values()) for f in ("LUT", "FF")}
nvm_move = {f: B[nvm[0]][f] - A[nvm[0]][f] for f in ("LUT", "FF")}
top = delta["u_pp"]
whole = {f: B["wrapper"][f] - A["wrapper"][f] for f in ("LUT", "FF")}
print(f"u_nvm_port scope: {nvm[0]}, {len(inside)} listed scope(s) inside it, move {nvm_move}")
print(f"terms: {len(terms)}; net {net}; absolute {absolute}; processor top own {top}")
print(f"identity: wrapper move {whole} = u_nvm_port {nvm_move} + partition net {net}: "
      f"{all(whole[f] == nvm_move[f] + net[f] for f in whole)}")
for key in sorted(terms, key=lambda k: -(abs(delta[k]['LUT']) + abs(delta[k]['FF']))):
    if delta[key]["LUT"] or delta[key]["FF"]:
        print(f"  {key}: LUT {delta[key]['LUT']:+d}, FF {delta[key]['FF']:+d}")
budget = (REPO / "docs/design/AREA_BUDGET.md").read_text()
finding = (REPO / "docs/findings/234_PP_SHADOW_AREA_BASELINE.md").read_text()
claims = [
    (budget, f"grows by {nvm_move['LUT']} LUTs and {nvm_move['FF']} FFs"),
    (finding, f"grows `u_nvm_port` by {nvm_move['LUT']} LUTs and {nvm_move['FF']} FFs"),
    (budget, f"net {net['LUT']:+d} LUTs and {net['FF']:+d} FFs"),
    (finding, f"net {net['LUT']:+d} LUTs and {net['FF']:+d} FFs"),
    (budget, f"outside `u_nvm_port`, {len(terms)} terms"),
    (finding, f"outside `u_nvm_port`, {len(terms)} terms"),
    (budget, f"sum to {absolute['LUT']} LUTs and {absolute['FF']} FFs"),
    (finding, f"sum to {absolute['LUT']} LUTs and {absolute['FF']} FFs"),
    (budget, f"{top['LUT']} LUTs and {top['FF']:+d} FFs"),
    (finding, f"{top['LUT']} LUTs and {top['FF']:+d} FFs"),
]
bad = 0
for page, sentence in claims:
    ok = sentence in page
    bad += not ok
    name = "AREA_BUDGET.md" if page is budget else "234_PP_SHADOW_AREA_BASELINE.md"
    print(f"{'OK ' if ok else 'BAD'} {name} holds {sentence!r}")
print(f"partition re-derivation: {bad} mismatch(es)")
sys.exit(1 if bad else 0)
