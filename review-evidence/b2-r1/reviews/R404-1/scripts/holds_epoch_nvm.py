#!/usr/bin/env python3
"""Long-hold gaps, reset epoch and saved-state reads from the lane B2 packet.

Usage: holds_epoch_nvm.py <packet author dir>

1. Unbound time before binds 2-5: the CONNECT_RX transaction start of bind N
   minus the DISCONNECT_RX transaction end of unbind N-1, both on the
   controller host clock, from bind.jsonl / unbind.jsonl.
2. Reset epoch (console word 0x90000720) before/after every action, from each
   analysis.json, plus the identity and final console reads.
3. Every PP_STAT value and every milan_nvm line in every console sample, with
   PP_STAT bit 11 (nvm_pend) decoded.
Exit 0 only when bind gaps exceed 30 s, every epoch reads 1, and the NVM slot
line and nvm_pend are identical at the first and last read.
"""
import json
import re
import sys
from collections import Counter
from pathlib import Path


def txn(path, mt, field):
    """Host time of the first ACMP transaction of message type mt."""
    for line in open(path):
        r = json.loads(line)
        if r.get("kind") == "transaction" and r.get("mt") == mt:
            return r[field]
    raise SystemExit(f"{path}: no transaction {mt}")


def main():
    pkt = Path(sys.argv[1])
    ok = True
    print("unbound before bind (s, controller host clock):")
    for n in range(2, 6):
        gap = txn(pkt / f"bind/bind-{n}/bind.jsonl", 6, "start") - \
            txn(pkt / f"bind/unbind-{n-1}/unbind.jsonl", 8, "end")
        print(f"  bind-{n}: {gap:.1f}")
        ok &= gap > 30.0

    ep = Counter()
    for f in sorted(pkt.glob("*/*/analysis.json")):
        ep[str(json.load(open(f)).get("rst_epoch_before_after"))] += 1
    print("rst_epoch_before_after over analysis.json:", dict(ep))
    ok &= set(ep) == {"[1, 1]"}

    stat = Counter()
    nvm = []
    consoles = sorted(pkt.rglob("console*.txt"))
    for f in consoles:
        text = f.read_text(errors="replace")
        for m in re.finditer(r"PP_STAT=([0-9a-f]{8})", text):
            stat[m.group(1)] += 1
        for m in re.finditer(r"### (\S+) cmd='milan_nvm'.*?\n(.*?)\n(NVM: slot[^\n]*)\n(NVM: PP_NVM_STAT[^\n]*)",
                             text, re.S):
            nvm.append((m.group(1), f.relative_to(pkt).as_posix(), m.group(3), m.group(4)))
    print("console files", len(consoles))
    for v, c in sorted(stat.items()):
        print(f"  PP_STAT={v} x{c} nvm_pend(bit 11)={(int(v, 16) >> 11) & 1}")
    nvm.sort()
    for t, f, slots, st in nvm:
        pend = re.search(r" pend=(\d)", st).group(1)
        commits = re.search(r"commits ok=(\d+) failed=(\d+)", st).groups()
        print(f"  {t} {f}: {slots[5:]} | pend={pend} commits ok={commits[0]} failed={commits[1]}")
    ok &= len(nvm) >= 2 and nvm[0][2:] == nvm[-1][2:] and len(stat) == 1
    print("RESULT", "PASS" if ok else "FAIL")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
