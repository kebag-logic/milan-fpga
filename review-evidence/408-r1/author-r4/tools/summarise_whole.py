#!/usr/bin/env python3
"""Tabulate the whole-gate reviewer probes at the new head, beside the
round-three external review's receipts at 11b1b86c where one exists.

usage: summarise_whole.py <whole-dir> <R273-5 receipts/probes dir> <out.md>"""
import json
import sys
from pathlib import Path

whole, prior, out = Path(sys.argv[1]), Path(sys.argv[2]), Path(sys.argv[3])
PRIOR = {"bom": "bom", "extra": "extra", "hi": "hi", "md": "md",
         "published": "published", "r2-cases": "r2", "unread": "unread",
         "round1-all_head": "r1"}
PIN_NAMES = [("spells a character outside the allowlist of S", "allowlist"),
             ("spells `$` in its code", "S:$"),
             ("universal character name in its code", "S:UCN"),
             ("__has_include or __has_include_next", "S:__has_include"),
             ("must not spell a token with a digraph", "digraph ban"),
             ("carries a trigraph", "S:trigraph")]
rows, changes = [], []
for path in sorted(whole.glob("*.json")):
    name, mode = path.stem.rsplit("-", 1)
    data = json.loads(path.read_text(encoding="utf-8"))
    results = data["results"]
    verdicts = {r["label"]: r["verdict"] for r in results}
    acc = sum(v == "ACCEPTED" for v in verdicts.values())
    by = {}
    for r in results:
        if r["verdict"] == "REFUSED":
            tag = next((t for s, t in PIN_NAMES if s in r["reason"]), "other rule")
            by[tag] = by.get(tag, 0) + 1
    pins = [r for r in results if "pin_ok" in r]
    pin_bad = [r["label"] for r in pins if not r["pin_ok"]]
    before = ""
    if name in PRIOR and (prior / f"{PRIOR[name]}-head-{mode}.json").is_file():
        old = {r["label"]: r["verdict"] for r in json.loads(
            (prior / f"{PRIOR[name]}-head-{mode}.json").read_text())["results"]}
        acc0 = sum(v == "ACCEPTED" for v in old.values())
        before = f"{len(old) - acc0} refused / {acc0} accepted"
        for label, verdict in verdicts.items():
            if old.get(label) != verdict:
                changes.append((name, mode, label, old.get(label), verdict))
    rows.append((name, mode, len(results), len(results) - acc, acc,
                 ", ".join(f"{t} {n}" for t, n in sorted(by.items())),
                 f"{len(pins) - len(pin_bad)}/{len(pins)}" if pins else "-",
                 before))
lines = ["| case file | mode | cases | refused | accepted | refused by | pins ok | at 11b1b86c (R273-5 receipt) |",
         "|---|---|---|---|---|---|---|---|"]
lines += [f"| {r[0]} | {r[1]} | {r[2]} | {r[3]} | {r[4]} | {r[5]} | {r[6]} | {r[7]} |" for r in rows]
lines += ["", "Verdict changes against 11b1b86c:", ""]
lines += [f"- {n} ({m}): {l[:110]} -- {a} -> {b}" for n, m, l, a, b in changes] or ["- none"]
out.write_text("\n".join(lines) + "\n", encoding="utf-8")
print("\n".join(lines))
