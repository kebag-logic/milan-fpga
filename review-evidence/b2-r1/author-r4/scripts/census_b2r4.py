#!/usr/bin/env python3
"""[A449] Round 4 of PR #622 (F6): the lane's command census as recorded.

Reads every controller transcript of the lane B2 author packet and classifies
each command by protocol, command, target entity and descriptor. Each action's
snapshot.jsonl is checked to be a byte copy of its snapshot-after.jsonl and is
left out. Checks the four statements the round-4 assignment asks the #606 page
to make:
  1. no state-changing command addressed a DUT stream input;
  2. the state-changing commands were 105 CONNECT_RX and 105 DISCONNECT_RX, all
     to the reference peer (listener is not the DUT, listener unique id 8);
  3. every AECP command, to either entity, was a GET_ or READ_ command;
  4. the commands that did address a DUT stream input (descriptor type 5) were
     reads: 228 GET_RX_STATE, 228 GET_COUNTERS and 4 READ_DESCRIPTOR.

Usage: census_b2r4.py <round-1 author dir> [<archive MANIFEST.json>]
With the manifest, every transcript read is checked against its
original_sha256 under author/. Prints counts, labels and relative paths only;
no entity identifier is printed.
"""
import hashlib
import json
import struct
import sys
from collections import Counter
from pathlib import Path

A = Path(sys.argv[1])
FAILURES = []

# IEEE 1722.1 ACMP message types and AEM descriptor types used below.
ACMP = {0: "CONNECT_TX", 2: "DISCONNECT_TX", 4: "GET_TX_STATE", 6: "CONNECT_RX",
        8: "DISCONNECT_RX", 10: "GET_RX_STATE", 12: "GET_TX_CONNECTION"}
ACMP_READS = {"GET_TX_STATE", "GET_RX_STATE", "GET_TX_CONNECTION"}
DESC = {0: "ENTITY", 1: "CONFIGURATION", 5: "STREAM_INPUT", 6: "STREAM_OUTPUT",
        9: "AVB_INTERFACE", 10: "CLOCK_SOURCE", 36: "CLOCK_DOMAIN"}


def check(ok, what):
    print(("PASS " if ok else "FAIL ") + what)
    if not ok:
        FAILURES.append(what)


def recs(p):
    for line in p.read_text().splitlines():
        if line.strip():
            yield json.loads(line)


files = sorted(A.rglob("*.jsonl"))
copies = {p for p in A.rglob("snapshot.jsonl")
          if p.read_bytes() == (p.parent / "snapshot-after.jsonl").read_bytes()}
events = [p for p in files if p.name == "events.jsonl"]
transcripts = [p for p in files if p not in copies and p not in events]
print(f"jsonl files: {len(files)}; snapshot.jsonl byte copies of snapshot-after.jsonl: {len(copies)} "
      f"of {sum(1 for p in files if p.name == 'snapshot.jsonl')}; events.jsonl (no commands): {len(events)}")
print(f"controller transcripts counted: {len(transcripts)}", dict(Counter(p.name for p in transcripts)))
check(len(copies) == 112 and sum(1 for p in files if p.name == "snapshot.jsonl") == 112,
      "all 112 snapshot.jsonl are byte copies and are left out")

if len(sys.argv) > 2:
    # the original packet matches original_sha256; the public redacted copy matches published_sha256
    man = {e["file"]: e for e in json.loads(Path(sys.argv[2]).read_text())}
    orig = pub = 0
    for p in files:
        e = man.get("author/" + p.relative_to(A).as_posix()) or {}
        h = hashlib.sha256(p.read_bytes()).hexdigest()
        orig += h == e.get("original_sha256")
        pub += h == e.get("published_sha256")
    print(f"against the archive manifest: {orig} equal original_sha256, {pub} equal published_sha256")
    check(orig == len(files) or pub == len(files),
          f"all {len(files)} jsonl files equal the archive manifest (original or published copy)")

# The DUT entity id, taken from the DUT's own GET_RX_STATE responses; compared, never printed.
dut_ids = {r["response"].get("listener") for p in transcripts for r in recs(p)
           if r.get("role") == "dut" and str(r.get("what", "")).startswith("state-5-")}
check(len(dut_ids) == 1, "the DUT's GET_RX_STATE responses name one listener entity (the DUT)")
DUT = next(iter(dut_ids))

cmds = []   # (protocol, command, target role, descriptor type or None, index or None, file)
state_changes = []
txn = Counter()
unpaired = mislabel = 0
for p in transcripts:
    prev = None
    for r in recs(p):
        rel = p.relative_to(A).as_posix()
        if r.get("kind") == "transaction":
            # the wire record of the ACMP command just emitted: paired, not a second command
            txn[r.get("mt")] += 1
            if not (prev and prev.get("what") == f"acmp-{r.get('mt')}" and prev.get("response") == r.get("response")):
                unpaired += 1
            prev = r
            continue
        if r.get("type") == "start":
            prev = r
            continue
        if r.get("type") == "aem":   # identity transcript: raw AEM command records
            req = bytes.fromhex(r.get("req", ""))
            dtype = struct.unpack(">H", req[-4:-2])[0] if r.get("cmd") == "READ_DESCRIPTOR" and len(req) >= 8 else None
            role = "dut" if r.get("target") == DUT else "peer"
            cmds.append(("AECP", r.get("cmd"), role, dtype, None, rel))
            prev = r
            continue
        role, what = r.get("role"), str(r.get("what", ""))
        resp = r.get("response") if isinstance(r.get("response"), dict) else {}
        parts = what.split("-")
        if what.startswith("state-"):
            kind, idx = int(parts[1]), int(parts[2])
            cmds.append(("ACMP", "GET_RX_STATE" if kind == 5 else "GET_TX_STATE", role, kind, idx, rel))
        elif what.startswith("acmp-"):
            mt = int(parts[1])
            target = "dut" if resp.get("listener") == DUT else "peer"
            mislabel += target != role
            cmds.append(("ACMP", ACMP.get(mt, f"mt{mt}"), target, 5, resp.get("listener_uid"), rel))
            state_changes.append((ACMP.get(mt, f"mt{mt}"), target, resp.get("listener_uid"),
                                  resp.get("talker") == DUT, resp.get("talker_uid"), resp.get("status")))
        else:
            dtype = int(parts[1]) if len(parts) == 3 and parts[0] in ("desc", "counter") else None
            idx = int(parts[2]) if dtype is not None else None
            cmds.append(("AECP", resp.get("cmd"), role, dtype, idx, rel))
        prev = r

print(f"\ncommands (paired ACMP wire records not counted twice): {len(cmds)}")
by = Counter((c[0], c[1], c[2], DESC.get(c[3], c[3]) if c[3] is not None else "-") for c in cmds)
for k in sorted(by, key=str):
    print(f"  {k[0]:4s} {k[1]:18s} to {k[2]:4s} descriptor {k[3]!s:14s} {by[k]:5d}")
check(unpaired == 0 and sum(txn.values()) == len(state_changes),
      f"{sum(txn.values())} ACMP wire records {dict(txn)}, each the record of the preceding state-changing command")
check(mislabel == 0, "every ACMP command's role label matches the listener entity its response names")


def is_read(c):
    return (c[0] == "ACMP" and c[1] in ACMP_READS) or (c[0] == "AECP" and str(c[1]).startswith(("GET_", "READ_")))


writes = [c for c in cmds if not is_read(c)]
print("\n== 1. no state-changing command addressed a DUT stream input")
w_dut = [c for c in writes if c[2] == "dut"]
w_dut_si = [c for c in w_dut if c[3] == 5]
print(f"state-changing commands: {len(writes)}; to the DUT: {len(w_dut)}; to a DUT stream input: {len(w_dut_si)}")
check(len(w_dut_si) == 0, "0 state-changing commands addressed a DUT stream input")
check(len(w_dut) == 0, "0 state-changing commands addressed the DUT at all")

print("\n== 2. the state-changing commands: 105 CONNECT_RX and 105 DISCONNECT_RX to the reference peer")
sc = Counter((n, t, uid) for n, t, uid, _tdut, _tuid, _st in state_changes)
print("by (command, target, listener unique id):", {f"{k[0]} to {k[1]} input {k[2]}": v for k, v in sorted(sc.items())})
check(sorted(writes) == sorted(c for c in cmds if c[0] == "ACMP" and c[1] in ("CONNECT_RX", "DISCONNECT_RX")),
      "every state-changing command is an ACMP CONNECT_RX or DISCONNECT_RX")
check(sc == Counter({("CONNECT_RX", "peer", 8): 105, ("DISCONNECT_RX", "peer", 8): 105}),
      "105 CONNECT_RX and 105 DISCONNECT_RX, 210 in all, every one to the peer's Stream Input 8")
conn = [s for s in state_changes if s[0] == "CONNECT_RX"]
check(all(s[3] and s[4] == 1 for s in conn), "every CONNECT_RX names DUT Stream Output 1 as talker")
check(all(s[5] == 0 for s in state_changes), "all 210 responses read status 0 (SUCCESS)")

print("\n== 3. every AECP command, to either entity, was a GET_ or READ_")
aecp = Counter((c[1], c[2]) for c in cmds if c[0] == "AECP")
print("AECP commands by (command, target):", {f"{k[0]} to {k[1]}": v for k, v in sorted(aecp.items())})
check(all(str(n).startswith(("GET_", "READ_")) for n, _t in aecp),
      f"all {sum(aecp.values())} AECP commands are GET_ or READ_")

print("\n== 4. the commands that addressed a DUT stream input were reads")
si = [c for c in cmds if c[2] == "dut" and c[3] == 5]
per = Counter((c[0], c[1], c[4]) for c in si)
print("DUT stream-input commands by (protocol, command, input):",
      {f"{k[0]} {k[1]} input {k[2]}": v for k, v in sorted(per.items(), key=str)})
tot = Counter(c[1] for c in si)
print("totals:", dict(sorted(tot.items())), "all:", len(si))
check(tot == Counter({"GET_RX_STATE": 228, "GET_COUNTERS": 228, "READ_DESCRIPTOR": 4}),
      "228 GET_RX_STATE, 228 GET_COUNTERS and 4 READ_DESCRIPTOR, 460 in all")
check(per[("ACMP", "GET_RX_STATE", 1)] == 226 and per[("ACMP", "GET_RX_STATE", 0)] == 2,
      "GET_RX_STATE: 226 on Stream Input 1, 2 on Stream Input 0 (the polls the page counts)")
check(all(is_read(c) for c in si), "all 460 are reads (0 state-changing)")

print(f"\nFAILURES {len(FAILURES)}")
sys.exit(1 if FAILURES else 0)
