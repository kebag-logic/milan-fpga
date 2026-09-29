#!/usr/bin/env python3
"""Round-4 check of the F6 census sentences against the archived transcripts.

Usage: census_sentence_r4.py <archived author dir> <606 page.md> <pr-body.md>

Recounts from the controller transcripts (byte-duplicate snapshot.jsonl
excluded): the state-changing ACMP commands and their listener, every AECP
command name, and every command addressed to a DUT STREAM_INPUT (descriptor
type 5, IEEE 1722.1 Table 7.1), split by command. Then checks each census
claim in the #606 page's Saved-state layer and in the PR body's Round 2 F2
bullet, printing OK or FAIL per claim. Exit 1 on any FAIL.
"""
import json
import re
import sys
from collections import Counter
from pathlib import Path

A, page, body = Path(sys.argv[1]), Path(sys.argv[2]).read_text(), Path(sys.argv[3]).read_text()

files = [p for p in sorted(A.rglob("*.jsonl"))
         if not (p.name == "snapshot.jsonl" and (p.parent / "snapshot-after.jsonl").read_bytes() == p.read_bytes())]
sc, aecp, dut_si, acmp_all, acmp_dut = Counter(), Counter(), Counter(), 0, 0
for p in files:
    for line in p.read_text().splitlines():
        if not line.strip():
            continue
        r = json.loads(line)
        resp = r.get("response") if isinstance(r.get("response"), dict) else {}
        if r.get("kind") == "transaction":
            sc[(r["mt"], resp.get("listener_uid"))] += 1
            acmp_all += 1
            continue
        w = str(r.get("what", ""))
        cmd = resp.get("cmd")
        if cmd:
            aecp[cmd] += 1
        if w.startswith("state-"):
            acmp_all += 1
            acmp_dut += r.get("role") == "dut"
        parts = w.split("-")
        if r.get("role") == "dut" and len(parts) == 3 and parts[1] == "5":
            dut_si[cmd or "GET_RX_STATE"] += 1

n_sc = sum(sc.values())
peer_only = set(uid for (_, uid) in sc) == {8}
sc_to_dut_si = 0  # no transaction names a DUT listener; checked by peer_only
aecp_ro = all(c.startswith(("GET_", "READ_")) for c in aecp)
print("archive: state-changing ACMP", dict(sc), "total", n_sc, "all to peer listener_uid 8:", peer_only)
print("archive: AECP names", sorted(aecp), "all GET_/READ_:", aecp_ro)
print("archive: commands addressed to a DUT stream input", dict(dut_si), "total", sum(dut_si.values()))
print("archive: all ACMP commands", acmp_all, "of which to the DUT", acmp_dut)

bullet = next((ln for ln in body.splitlines() if ln.startswith("- **F2, the saved-state layer.**")), "")
fails = 0


def check(name, ok):
    global fails
    fails += not ok
    print(("OK   " if ok else "FAIL ") + name)


for label, text in (("page", page), ("PR body F2 bullet", bullet)):
    check(f"{label}: no unqualified 'no command ... addressed' claim",
          not re.search(r"\bno command (in the lane )?addressed", text, re.I))
    check(f"{label}: 'no state-changing command addressed' a DUT stream input, and archive agrees",
          re.search(r"no state-changing command addressed", text, re.I) is not None and peer_only and sc_to_dut_si == 0)
    m = re.search(r"the (\d+) `CONNECT_RX` and `DISCONNECT_RX` went to the reference peer", text, re.I)
    check(f"{label}: '{m.group(1) if m else '?'} CONNECT_RX and DISCONNECT_RX went to the reference peer' == {n_sc}",
          bool(m) and int(m.group(1)) == n_sc and peer_only)
    check(f"{label}: 'every AECP command was a GET_ or READ_'",
          "every AECP command was a GET_ or READ_" in text and aecp_ro)
    m = re.search(r"were reads, which write no record: (\d+) GET_RX_STATE \(the polls above\), (\d+) GET_COUNTERS and (\d+) READ_DESCRIPTOR", text)
    want = (dut_si["GET_RX_STATE"], dut_si["GET_COUNTERS"], dut_si["READ_DESCRIPTOR"])
    got = tuple(int(x) for x in m.groups()) if m else None
    check(f"{label}: reads named {got} == archive {want}, and no other command addressed a DUT input",
          got == want and set(dut_si) == {"GET_RX_STATE", "GET_COUNTERS", "READ_DESCRIPTOR"})
    m = re.search(r"(\d+) ACMP commands all to the peer's input", text)
    if m:
        check(f"{label}: '{m.group(1)} ACMP commands all to the peer's input' == archive ACMP total {acmp_all} with 0 to the DUT ({acmp_dut})",
              int(m.group(1)) == acmp_all and acmp_dut == 0)
print("fails:", fails)
sys.exit(1 if fails else 0)
