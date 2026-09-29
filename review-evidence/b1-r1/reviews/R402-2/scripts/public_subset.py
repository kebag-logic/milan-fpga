#!/usr/bin/env python3
"""Re-derive what the public packet alone carries: the dry-run and final raw consoles.

For each action whose raw console.jsonl is in author-r2/r1/bench/, check it against the
packet's raw index (size, SHA-256), then count its console rounds, the rounds whose
MAC_STATUS and link_status reads are single and equal, and the PP_STAT nvm_pend and
nvm_dirty values. These are the per-action lines the author's extractions print.

usage: public_subset.py <author-r2-packet-dir>
"""
import hashlib
import json
import re
import sys
from pathlib import Path

pk = Path(sys.argv[1])
index = {f["path"]: (f["bytes"], f["sha256"]) for f in json.loads((pk / "r1" / "RAW-ARTIFACTS.json").read_text())["files"]}
fails = 0
for p in sorted((pk / "r1" / "bench").glob("*/console.jsonl")):
    rel = f"{p.parent.name}/console.jsonl"
    got = (p.stat().st_size, hashlib.sha256(p.read_bytes()).hexdigest())
    ok_hash = index.get(rel) == got
    rounds, cur = [], None
    for r in (json.loads(x) for x in p.read_text().splitlines() if x.strip()):
        if r["cmd"] == "milan_status":
            cur = {"pp": int(re.search(r"PP_STAT=([0-9a-f]{8})", r["raw"]).group(1), 16), "w": {}}
            rounds.append(cur)
        elif cur is not None and r["cmd"] in ("mem_read 0x90000110 4", "mem_read 0xf000181c 4"):
            m = re.search(r"^0x[0-9a-f]{8}\s+((?:[0-9a-f]{2} ){4})", r["raw"], re.M)
            cur["w"].setdefault(r["cmd"], []).append(int("".join(reversed(m.group(1).split())), 16))
    agree = sum(1 for x in rounds if len(x["w"]) == 2 and all(len(v) == 1 for v in x["w"].values())
                and len({v[0] for v in x["w"].values()}) == 1)
    pend = sorted({x["pp"] >> 11 & 1 for x in rounds})
    dirty = sorted({x["pp"] >> 8 & 1 for x in rounds})
    print(f"{rel}: raw index {'ok' if ok_hash else 'MISMATCH'}; rounds {len(rounds)}, agree {agree}, pend {pend}, dirty {dirty}")
    fails += not ok_hash or agree != len(rounds)
sys.exit(1 if fails else 0)
