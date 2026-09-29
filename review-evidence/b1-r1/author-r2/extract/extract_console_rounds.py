#!/usr/bin/env python3
"""Reproduce the #599 page's console-round claim from the raw consoles.

Claim (docs/findings/599_394_E1_LINK_CYCLES.md, method): console `mem_read`
sampled MAC_STATUS (0x90000110) and the `link_status` CSR (0xf000181c) every
250 ms, and both agreed in all 7,520 console rounds of the session.

A round is one `milan_status` answer and the reads that follow it up to the
next `milan_status`. Each round must hold exactly one read of each word; the
two 32-bit values are compared. The session is the lane's nineteen measured
actions, each with its own hash-checked console capture.

usage: extract_console_rounds.py <raw-root> <repo-at-head>
"""
import re
import sys

from b1r2_common import Inputs, jsonl

ACTIONS = (["dryrun", "bmsr-proof", "baseline-bound"] + [f"cycle{n:02d}" for n in range(1, 11)]
           + [f"gm{n:02d}" for n in range(1, 6)] + ["final"])
MAC = "mem_read 0x90000110 4"
LINK = "mem_read 0xf000181c 4"


def word(raw, addr):
    m = re.search(r"^0x%s\s+((?:[0-9a-f]{2} ){4})" % addr, raw, re.M)
    b = m.group(1).split()
    return int("".join(reversed(b)), 16)  # little-endian dump


def main():
    inp = Inputs(sys.argv[1], sys.argv[2])
    total = agree = 0
    bad = []
    for action in ACTIONS:
        rows = jsonl(inp.path(f"{action}/console.jsonl"))
        rounds, cur = [], None
        for r in rows:
            if r["cmd"] == "milan_status":
                cur = {"t": r["t"], MAC: [], LINK: []}
                rounds.append(cur)
            elif cur is not None and r["cmd"] in (MAC, LINK):
                cur[r["cmd"]].append(word(r["raw"], r["cmd"].split()[1][2:]))
        n_ok = 0
        values = set()
        for rd in rounds:
            if len(rd[MAC]) == 1 and len(rd[LINK]) == 1 and rd[MAC][0] == rd[LINK][0]:
                n_ok += 1
                values.add(rd[MAC][0])
            else:
                bad.append((action, rd["t"], rd[MAC], rd[LINK]))
        total += len(rounds)
        agree += n_ok
        print(f"{action:15s} rounds {len(rounds):4d}  agree {n_ok:4d}  values {sorted('0x%02x' % v for v in values)}")
    print()
    print(f"TOTAL rounds {total}, both words read once and equal in {agree}")
    for b in bad[:20]:
        print("DISAGREE", b)
    ok = total == 7520 and agree == total
    print("CLAIM all 7,520 rounds agree:", "REPRODUCED" if ok else "NOT REPRODUCED")
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
