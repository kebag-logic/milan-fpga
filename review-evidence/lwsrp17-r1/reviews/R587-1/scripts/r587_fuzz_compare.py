#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""Compare r587_fuzz outputs from the base and head libraries.

Usage: r587_fuzz_compare.py ETHERTYPE_HEX MODE BASE_OUT HEAD_OUT
MODE roomy: every call must match (result, sends, rc, decoded-event multiset)
            and every head PDU must have the grouped form.
MODE tight: head-only invariants (grouped form, length <= capacity, no write
            past capacity, retried PDUs unchanged); BASE_OUT may be '-'.
Prints one summary line; rc 0 when clean.
"""
import os
import sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from r587_decode import decode, events_of, grade, Bad  # noqa: E402


def parse(path):
    calls, cur, other = [], {"sends": []}, []
    for line in open(path):
        f = line.split()
        if not f:
            continue
        if f[0] == "S":
            cur["sends"].append((int(f[1]), int(f[2]), bytes.fromhex(f[3]) if len(f) > 3 else b""))
        elif f[0] == "C":
            cur.update(step=int(f[1]), cap=int(f[2]), result=int(f[3]))
            calls.append(cur)
            cur = {"sends": []}
        elif f[0] in ("O", "R", "X", "END"):
            other.append(line.strip())
    return calls, other


def main():
    eth, mode, base_path, head_path = int(sys.argv[1], 16), sys.argv[2], sys.argv[3], sys.argv[4]
    head, head_other = parse(head_path)
    problems, pdus, layout_only = [], 0, 0
    if "END" not in head_other:
        problems.append("head run did not finish")
    for o in head_other:
        if o[0] in "OR":
            problems.append("head " + o)
    for c in head:
        for rc, ln, data in c["sends"]:
            pdus += 1
            if ln > c["cap"]:
                problems.append(f"step {c['step']}: {ln} > capacity {c['cap']}")
            try:
                m, e, t = decode(data, eth)
            except Bad as err:
                problems.append(f"step {c['step']}: undecodable {err}")
                continue
            g = grade(m, e, t, eth)
            if g:
                problems.append(f"step {c['step']}: {g}")
    if mode == "roomy":
        base, base_other = parse(base_path)
        if [o for o in base_other if o[0] == "X"] != [o for o in head_other if o[0] == "X"]:
            problems.append("operation results differ")
        if len(base) != len(head):
            problems.append(f"call count {len(base)} vs {len(head)}")
        for b, h in zip(base, head):
            if b["result"] != h["result"] or len(b["sends"]) != len(h["sends"]):
                problems.append(f"step {h['step']}: result {b['result']}->{h['result']}")
                break
            for (rb, _, db), (rh, _, dh) in zip(b["sends"], h["sends"]):
                try:
                    eb, eh = events_of(decode(db, eth)[0]), events_of(decode(dh, eth)[0])
                except Bad as err:
                    problems.append(f"step {h['step']}: {err}")
                    continue
                if rb != rh or eb != eh:
                    problems.append(f"step {h['step']}: decoded events differ")
                elif db != dh:
                    layout_only += 1
    print(f"{os.path.basename(head_path)}: calls={len(head)} pdus={pdus} layout_only={layout_only} "
          f"problems={len(problems)}" + ("".join("\n  FAIL " + p for p in problems[:5])))
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main())
