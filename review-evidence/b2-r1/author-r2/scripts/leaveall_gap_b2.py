#!/usr/bin/env python3
"""DUT MSRP LeaveAlls that follow a received bridge MSRP LeaveAll, and cycle 22's gap.

usage: leaveall_gap_b2.py <round-1 packet author dir> <archive MANIFEST.json>

802.1Q-2014 Table 10-5 (10.7.9) maps rLA! to "Start leavealltimer", and 10.6
says a received LeaveAll restarts the timer without a message. The own timer
draws 10-15 s (Milan v1.2 Table 4.3, processor F08.1). So a conformant
participant sends no LeaveAll within 10 s of a received one. The processor at
c951a9ff does not restart the timer on receipt (10_srp_engine.md section 6.5,
"Timer on receipt: an open deviation", processor issue #108).

Reads every msrp.tsv (112 captures: 12 bind-series captures and 100 cycles).
A DUT LeaveAll is one MRPDU time at which the DUT sent LeaveAll for any type.
A bridge LeaveAll is one MRPDU time at which the bridge sent LeaveAll for any
type. For every DUT LeaveAll with an earlier bridge LeaveAll in the same
capture, the gap is the DUT LeaveAll minus the latest earlier bridge LeaveAll.

Prints both counts, because the two round-1 receipts count different units:
DUT LeaveAll MRPDUs (R404-1's `leaveall_damping.py` counts these) and captures
holding at least one (R405-1's `leaveall_damping.py` counts these).
No identifier is printed.
"""
import hashlib
import json
import sys
from pathlib import Path

A = Path(sys.argv[1])
MAN = {e["file"]: e for e in json.load(open(sys.argv[2]))}
LIM = 10.0
caps, pdu_hits, cap_hits, unmatched = 0, [], {}, []
for f in sorted(A.rglob("msrp.tsv")):
    b = f.read_bytes()
    rel = f.relative_to(A).as_posix()
    e = MAN.get("author/" + rel)
    if e is None or e["original_sha256"] != hashlib.sha256(b).hexdigest():
        unmatched.append(rel)
    rows = [l.split("\t") for l in b.decode().splitlines()[1:] if l.strip()]
    caps += 1
    br = sorted({float(r[0]) for r in rows if r[1] == "bridge" and r[3] == "LeaveAll"})
    own = sorted({float(r[0]) for r in rows if r[1] == "DUT" and r[3] == "LeaveAll"})
    for o in own:
        prev = [x for x in br if x < o]
        if prev and o - prev[-1] < LIM:
            pdu_hits.append((f.parent.name, o - prev[-1]))
            cap_hits.setdefault(f.parent.name, []).append(o - prev[-1])

gaps = sorted(g for _, g in pdu_hits)
print(f"captures read: {caps}; msrp.tsv not matching the archive original_sha256: {unmatched or 'none'}")
print(f"DUT LeaveAll MRPDUs less than {LIM:.0f} s after a received bridge LeaveAll: {len(pdu_hits)}")
print(f"captures holding at least one: {len(cap_hits)} of {caps}")
print(f"captures holding two: {sorted(k for k, v in cap_hits.items() if len(v) > 1)}")
print(f"gap min / median / max, s: {gaps[0]:.6f} / {gaps[len(gaps) // 2]:.6f} / {gaps[-1]:.6f}")
print(f"gaps under 1 s: {sum(g < 1.0 for g in gaps)}")

d = A / "cycles" / "cycle-022"
an = json.loads((d / "analysis.json").read_text())
rows = [l.split("\t") for l in (d / "msrp.tsv").read_text().splitlines()[1:] if l.strip()]
disc = an["disconnect_response_s"]
lv = disc + an["bridge_lv_after_disconnect_s"]
br = max(float(r[0]) for r in rows if r[1] == "bridge" and r[3] == "LeaveAll" and float(r[0]) < lv)
own = min(float(r[0]) for r in rows if r[1] == "DUT" and r[3] == "LeaveAll" and float(r[0]) > br)
print("\ncycle 22, seconds after the tapped DISCONNECT_RX response:")
print(f"  bridge LeaveAll                  {br - disc:+.6f}  types {sorted({r[2] for r in rows if r[1] == 'bridge' and r[3] == 'LeaveAll' and float(r[0]) == br})}")
print(f"  DUT's own LeaveAll               {own - disc:+.6f}  types {sorted({r[2] for r in rows if r[1] == 'DUT' and r[3] == 'LeaveAll' and float(r[0]) == own})}")
print(f"  bridge Listener Lv               {lv - disc:+.6f}")
print(f"  own LeaveAll minus bridge LeaveAll {own - br:.6f} s; own LeaveAll minus Lv {1e3 * (own - lv):+.6f} ms")
print(f"  cycle 22 in the gap list: {[round(g, 6) for n, g in pdu_hits if n == 'cycle-022']}")
sys.exit(0 if not unmatched and caps == 112 else 1)
