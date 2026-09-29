#!/usr/bin/env python3
"""Independent round-2 re-derivation of the saved-state layer (F2).

Usage: saved_state_r2.py <archived author dir>

From the archived console captures: the two milan_nvm reads (slots, image
sequence, records, writer, PP_NVM_STAT, commit counts) and the PP_STAT word
of every milan_status sample, decoded per docs/reference/REGISTER_MAP.md
0x924 / 0x93C. From the controller transcripts: every ACMP state-changing
transaction (message types 6 and 8), every AECP command name, and every
GET_RX_STATE poll of a DUT stream input, counted per input and with
byte-duplicate transcript files (snapshot.jsonl vs snapshot-after.jsonl)
separated from distinct records. Prints no identifier other than the DUT's.
"""
import json
import re
import sys
from collections import Counter
from pathlib import Path

A = Path(sys.argv[1])


def nvm(rel):
    t = (A / rel).read_text(errors="replace")
    m = re.search(r"^### (\S+) cmd='milan_nvm'.*\nmilan_nvm\n(NVM: slot.*)\n(NVM: PP_NVM_STAT.*)\n", t, re.M)
    s, st = m.group(2), m.group(3)
    return {
        "at": m.group(1),
        "slots": "%s / %s" % re.search(r"slot A \S+ seq (\d+), slot B \S+ seq (\d+)", s).groups(),
        "image": re.search(r"image seq (\d+)", s).group(1),
        "records": "%s records, %s B" % re.search(r"(\d+) records, (\d+) B", s).groups(),
        "writer": re.search(r"writer (\w+)", s).group(1),
        "PP_NVM_STAT": re.search(r"PP_NVM_STAT=([0-9a-f]{8})", st).group(1),
        "pend": re.search(r" pend=(\d)", st).group(1),
        "commits": "%s / %s" % re.search(r"commits ok=(\d+) failed=(\d+)", st).groups(),
        "PP_STAT": re.search(r"PP_STAT=([0-9a-f]{8})", t).group(1),
    }


start, end = nvm("identity/console-identity.txt"), nvm("restore/console-final.txt")
for k in start:
    print(f"{k:12s} start={start[k]!s:32s} end={end[k]}")
print("start == end apart from time:", all(start[k] == end[k] for k in start if k != "at"))
ns = int(start["PP_NVM_STAT"], 16)
print("PP_NVM_STAT decode: tag %02x unres %d pend %d commit_busy %d stale %d dirty %d img_valid %d backed %d"
      % (ns >> 24, ns >> 23 & 1, ns >> 22 & 1, ns >> 10 & 1, ns >> 9 & 1, ns >> 8 & 1, ns >> 7 & 1, ns >> 6 & 1))

# PP_STAT in every console sample
consoles = sorted(p for p in A.rglob("console*.txt"))
vals, nvm_files, times = Counter(), [], []
for p in consoles:
    t = p.read_text(errors="replace")
    for m in re.finditer(r"^### (\S+) cmd='milan_status'.*\nmilan_status\n.*PP_STAT=([0-9a-f]{8})", t, re.M):
        vals[m.group(2)] += 1
        times.append((m.group(1), p.relative_to(A).as_posix()))
    if "cmd='milan_nvm'" in t:
        nvm_files.append(p.relative_to(A).as_posix())
times.sort()
print("console .txt files:", len(consoles), "milan_status samples:", sum(vals.values()), "distinct PP_STAT:", dict(vals))
for v in vals:
    x = int(v, 16)
    print(f"  {v}: alarm {x>>4&1} backed {x>>6&1} dirty {x>>8&1} stale {x>>9&1} img_valid {x>>10&1} pend {x>>11&1} verdict {x>>12&15}")
print("files carrying a milan_nvm read:", nvm_files)
acts = [t for t in times if not t[1].startswith(("identity/", "restore/"))]
print("action samples:", len(acts), "first", acts[0], "last", acts[-1])

# transcripts
dups = 0
distinct_files = []
for p in sorted(A.rglob("*.jsonl")):
    if p.name == "snapshot.jsonl" and (p.parent / "snapshot-after.jsonl").read_bytes() == p.read_bytes():
        dups += 1
        continue
    distinct_files.append(p)
print("snapshot.jsonl files byte-identical to snapshot-after.jsonl (excluded as duplicates):", dups)
acmp, aecp, polls_all, polls_distinct = Counter(), Counter(), Counter(), Counter()
bad = []
for p in sorted(A.rglob("*.jsonl")):
    dup = p not in distinct_files
    for line in p.read_text().splitlines():
        if not line.strip():
            continue
        r = json.loads(line)
        resp = r.get("response") if isinstance(r.get("response"), dict) else {}
        if r.get("kind") == "transaction" and not dup:
            acmp[(r["mt"], resp.get("listener_uid"), resp.get("status"))] += 1
        cmd = resp.get("cmd") or (r.get("cmd") if isinstance(r.get("cmd"), str) else None)
        if cmd and not dup:
            aecp[cmd] += 1
        w = r.get("what", "")
        if r.get("role") == "dut" and isinstance(w, str) and w.startswith("state-5-"):
            polls_all[w] += 1
            if not dup:
                polls_distinct[w] += 1
            if resp.get("conn_count") != 0:
                bad.append((p.relative_to(A).as_posix(), w))
print("ACMP transactions (mt, listener_uid, status):", dict(acmp))
print("AECP command names (distinct records):", dict(aecp))
print("non-GET/READ AECP commands:", [c for c in aecp if not c.startswith(("GET_", "READ_"))])
print("DUT stream-input GET_RX_STATE records, all files:", dict(polls_all), "total", sum(polls_all.values()))
print("DUT stream-input GET_RX_STATE records, duplicates excluded:", dict(polls_distinct), "total", sum(polls_distinct.values()))
print("DUT stream-input records with conn_count != 0:", bad or "none")
