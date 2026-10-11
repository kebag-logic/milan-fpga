#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""Reviewer cross-check for PR #715 / issue #671 (round R602-4).

Re-derives, with a reviewer-written model of the firmware's boot reads
(nvm_judge_slot / nvm_restage / nvm_boot as written at the head), the read
count, the UNREAD set and the re-stage cause of EVERY generated check-13
case, including the ones `fault_cases` drops, and compares them with the
lane's reference model `read_fault_cases.expect`. Also classifies every
dropped case against the stated detection limit, and counts the cases.

Usage: crosscheck_model.py REPO OUT.json
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

TRIES = 3
MASK = 0xFFFF_FFFF


def model(case, rfc):
    """Reviewer model: returns (reads, unread, unstaged, final verdicts)."""
    newer = case.valid.upper()
    other = "B" if newer == "A" else "A"
    content = {newer: ("OK", case.seq, newer),
               other: ("OK", (case.seq - 1) & MASK, other) if case.older else ("BLANK", None, other)}
    option, arg = case.fault
    faulted = arg[0].upper()
    n = 0 if case.restart else 1   # a cold boot first reads the AEM image

    def read(slot):
        nonlocal n
        k = n
        n += 1
        if slot == faulted and case.skip <= k < case.skip + case.count:
            if option == "--read-fault":
                return ("BAD", k)           # a different wrong byte on every faulty read
            if option == "--read-ff":
                return ("BLANK", None, "ff")
            return content["B" if slot == "A" else "A"]   # the other slot's bytes
        return content[slot]

    def same(x, y):
        # two refusals agree when their bytes agree; an all-0xFF read and a
        # blank slot are the same bytes
        norm = lambda r: ("BLANK",) if r[0] == "BLANK" else r
        return norm(x) == norm(y)

    def judge(slot):
        first = second = None
        for t in range(TRIES):
            r = read(slot)
            if r[0] == "OK" or (t >= 1 and same(first, r)) or (t >= 2 and same(second, r)):
                return r
            if t == 0:
                first = r
            else:
                second = r
        return ("UNREAD",)

    v = {"A": judge("A")}
    v["B"] = judge("B")
    unread = {s for s in "AB" if v[s] == ("UNREAD",)}
    unstaged = set()

    def pick():
        oks = [s for s in "AB" if v[s][0] == "OK"]
        if len(oks) == 2:
            d = (v["A"][1] - v["B"][1]) & MASK
            return "A" if d < 0x8000_0000 else "B"
        return oks[0] if oks else None

    chosen = pick()
    while chosen is not None:
        good = False
        for _ in range(TRIES):
            r = read(chosen)
            if r[0] == "OK" and r[1] == v[chosen][1]:
                good = True
                break
        if good:
            break
        unstaged.add(chosen)
        unread.add(chosen)
        v[chosen] = ("UNREAD",)
        chosen = pick()
    # a slot's final view is "as its bytes are" if it equals its own content
    # (OK at its own sequence, or BLANK for a blank slot), or UNREAD
    def truthful(s):
        if v[s] == ("UNREAD",):
            return True
        c = content[s]
        return v[s][0] == c[0] and (c[0] == "BLANK" or v[s][1] == c[1])
    return n, "".join(sorted(unread)), "".join(sorted(unstaged)), all(truthful(s) for s in "AB")


def main() -> int:
    repo, out = Path(sys.argv[1]), Path(sys.argv[2])
    sys.path.insert(0, str(repo / "sw/firmware/nvm_hosttest"))
    import read_fault_cases as rfc

    body = 1000
    generated = []
    for restart in (True, False):
        for older, faulted, manners, seqs in rfc.GROUPS:
            for turn, valid in enumerate("ab"):
                slot = valid if faulted == "valid" else ("b" if valid == "a" else "a")
                bound = rfc.BOOT_READ_BOUND - int(restart)
                for w, (skip, count) in enumerate(rfc.windows(bound)):
                    for m, manner in enumerate(manners):
                        generated.append(rfc.FaultCase(valid, older, seqs[(w + m + turn) % len(seqs)],
                                                       rfc.fault(manner, slot, skip, count, body),
                                                       skip, count, restart))
    kept = rfc.fault_cases(body)
    mism, dropped = [], []
    for c in generated:
        e = rfc.expect(c)
        reads, unread, unstaged, within = model(c, rfc)
        if (e.reads, e.unread, e.unstaged, e.within) != (reads, unread, unstaged, within):
            mism.append({"case": c.name, "skip": c.skip, "count": c.count,
                         "lane": [e.reads, e.unread, e.unstaged, e.within],
                         "reviewer": [reads, unread, unstaged, within]})
        if not e.within:
            dropped.append(c)
    byte_dropped = [c.name for c in dropped if c.fault[0] == "--read-fault"]
    kinds = {}
    for c in dropped:
        kinds[c.fault[0]] = kinds.get(c.fault[0], 0) + 1
    # windows per bound: every start in the bound, lengths 1..TRIES+1, plus WHOLE
    win_ok = all(set(rfc.windows(b)) == {rfc.WHOLE} | {(s, n) for s in range(b) for n in range(1, TRIES + 2)}
                 for b in (12, 13))
    # each (restart, group, orientation, window) meets every sequence of its group across manners?
    seq_cover = {}
    for c in kept:
        key = (c.restart, c.older, c.fault[0], c.valid)
        seq_cover.setdefault(key, set()).add(c.seq)
    res = {"generated": len(generated), "kept": len(kept), "dropped": len(dropped),
           "kept_cold": sum(1 for c in kept if not c.restart),
           "kept_restart": sum(1 for c in kept if c.restart),
           "model_mismatches": len(mism), "mismatch_examples": mism[:10],
           "dropped_by_option": kinds, "byte_fault_cases_dropped": byte_dropped,
           "windows_complete": win_ok,
           "max_reads_cold": max(rfc.expect(c).reads for c in generated if not c.restart),
           "max_reads_restart": max(rfc.expect(c).reads for c in generated if c.restart),
           "seq_coverage": {str(k): sorted(hex(s) for s in v) for k, v in sorted(seq_cover.items(), key=str)}}
    out.write_text(json.dumps(res, indent=1) + "\n")
    print(json.dumps({k: v for k, v in res.items() if k != "seq_coverage"}, indent=1))
    return 1 if mism or byte_dropped or not win_ok else 0


if __name__ == "__main__":
    raise SystemExit(main())
