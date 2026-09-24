#!/usr/bin/env python3
"""Compare gate 1b's mutation tables at base and head, label by label.

Reads the connected mutation audits written by probe.py --mutation-audit and
reports, for every base entry pinned on a text rule #408/#409 retired or
narrowed, the head entry of the same label and the sentence(s) it is pinned
on now, plus every label present on one side only.
Usage: compare_tables.py <base.json> <head.json>
"""

import json
import sys

RETIRED = {
    "SPLICE": "firmware must not splice physical source lines with backslash-newline",
    "PASTE": "firmware must not paste tokens",
    "SELECT": "firmware must not select boot code with the preprocessor",
    "REACH": "a conditional group reaching",
    "CAST_SET": "the firmware's casts to a pointer are pinned",
    "STORE_SET": "the firmware's stores through a pointer are pinned",
    "ASM_SET": "the firmware's inline asm is pinned",
    "LISTING": "the firmware's directory is pinned to",
    "MACRO(read)": "inside a macro body: every call to a CSR primitive",
}

base = {r["label"]: r for r in json.load(open(sys.argv[1]))}
head = {r["label"]: r for r in json.load(open(sys.argv[2]))}
for side, rows in (("base", base), ("head", head)):
    bad = [label for label, r in rows.items()
           if r["verdict"] != "REFUSED" or not r["pin_ok"]]
    print(f"{side}: {len(rows)} entries, all refused on their pin: {not bad}"
          + (f" -- NOT: {bad}" if bad else ""))
print()
print("base entries pinned on a retired/narrowed text rule -> head:")
for label, r in base.items():
    hit = [name for name, pin in RETIRED.items()
           if any(pin in p for p in r["pin"])]
    if not hit:
        continue
    now = head.get(label)
    where = ("ABSENT at head" if now is None else
             f"head pin {now['pin']} ({'refused, pin ok' if now['verdict'] == 'REFUSED' and now['pin_ok'] else now['verdict']})")
    print(f"- [{','.join(hit)}] {label}\n    {where}")
print()
print("labels only at base:")
for label in base:
    if label not in head:
        print(f"- {label}  (base pin {base[label]['pin']})")
print("labels only at head:")
for label in head:
    if label not in base:
        print(f"- {label}  (head pin {head[label]['pin']})")
