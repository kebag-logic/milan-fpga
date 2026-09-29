#!/usr/bin/env python3
"""Two receipts from the archived packet, no bench access.

1. DUT saved-state (NVM) layer at the start and end of the session: the
   milan_nvm lines and PP_STAT[11] (nvm_pend) from the identity readback, the
   dry run, the final action and the final console.
2. Raw-retention coverage: for every action, which raw files the per-action
   raw-artifacts.json indexes, whether a byte-identical copy is archived, and
   the directory the index names (only its first component is printed).

usage: restore_and_retention.py <extracted-packet-dir>/author
"""
import hashlib
import json
import re
import sys
from pathlib import Path

author = Path(sys.argv[1])
print("== DUT saved-state layer")
for f in ("identity/console-identity.txt", "restore/console-final.txt"):
    t = (author / f).read_text()
    for m in re.finditer(r"NVM: slot[^\n]*|PP_NVM_STAT=[^\n]*|PP_STAT=([0-9a-f]{8})", t):
        s = m.group(0)
        if s.startswith("PP_STAT="):
            s += f"  (nvm_pend PP_STAT[11]={int(m.group(1), 16) >> 11 & 1})"
        print(f"{f}: {s}")
for f in ("bench/dryrun/console.jsonl", "bench/final/console.jsonl"):
    rows = [json.loads(x) for x in (author / f).read_text().splitlines() if x.strip()]
    ps = [re.search(r"PP_STAT=([0-9a-f]{8})", r["raw"])[1] for r in rows if r["cmd"] == "milan_status"]
    print(f"{f}: {len(ps)} milan_status samples, PP_STAT values {sorted(set(ps))}, "
          f"nvm_pend values {sorted({int(p, 16) >> 11 & 1 for p in ps})}")

print("\n== raw retention")
archived = {hashlib.sha256(p.read_bytes()).hexdigest() for p in author.rglob("*") if p.is_file()}
dirs = set()
for idx in sorted((author / "bench").glob("*/raw-artifacts.json")):
    rows = json.loads(idx.read_text())
    have = [Path(r["path"]).name for r in rows if r["sha256"] in archived]
    miss = [Path(r["path"]).name for r in rows if r["sha256"] not in archived]
    dirs |= {"/" + Path(r["path"]).parts[1] for r in rows if r["path"].startswith("/")}
    print(f"{idx.parent.name:15s} indexed {len(rows):2d}; archived {sorted(have)}; NOT archived {sorted(miss)}")
print("index path roots:", sorted(dirs))
