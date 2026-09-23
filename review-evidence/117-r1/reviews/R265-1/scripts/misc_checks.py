#!/usr/bin/env python3
"""Spot checks: Run B peer counters, final-2 capture and console, identity 2
console, grader verdicts, power-strip status reads.
Usage: misc_checks.py <review-evidence/117-r1 dir>
"""
import json, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import condec, tapdec

E = sys.argv[1]
L = [json.loads(l) for l in open(f"{E}/bench-a200/bench/runB/pw1-bind.jsonl")]
cn = [x for x in L if x.get("cmd") == "GET_COUNTERS" and x.get("payload", "").startswith("0005")]
c = lambda x, i: int.from_bytes(bytes.fromhex(x["payload"])[8 + 4 * i:12 + 4 * i], "big")
for x in cn:
    print("RunB peer STREAM_INPUT poll t=%.3f LOCKED %d UNLOCKED %d TSU %d TS_VALID %d FRAMES_RX %d"
          % (x["t"], c(x, 0), c(x, 1), c(x, 5), c(x, 6), c(x, 11)))
unb = [x["t"] for x in L if x.get("type") == "unbind"]
print("RunB unbind at", unb)
recs, st = tapdec.load(f"{E}/bench-a202/bench/final/tap-final.pcap")
print("final-2 tap: tapped", st["tapped"], "host-only", st["host_only"], "AVTP stream PDUs",
      sum(1 for r in recs if r["kind"] in ("crf", "aaf")))
for f in ("bench-a202/bench/final/console-final.txt", "bench-a202/identity/console-identity.txt"):
    for r in condec.parse(f"{E}/{f}"):
        if r["cmd"] == "milan_status":
            print(f, r["iso"], {k: r["fields"].get(k) for k in ("VERSION", "GPTP_GM", "CLKV_STAT", "PDELAY_NS")})
        elif "crc" in r:
            print(f, r["cmd"], r["crc"])
        elif "addr" in r:
            print(f, hex(r["addr"]), hex(r["word"]))
for f in ("bench-a200/identity/uart-smoke-identity.log", "bench-a200/bench/final/uart-smoke-final.log",
          "bench-a202/identity/uart-smoke-identity.log", "bench-a202/bench/final/uart-smoke-final.log"):
    print(f, [l.strip() for l in open(f"{E}/{f}") if "UART SMOKE" in l])
for f in ("status-start.txt", "status-end.txt"):
    print(f, " ".join(l.strip() for l in open(f"{E}/bench-a202/bench/powerstrip/{f}") if l.strip().startswith("OUT")))
# Step 5: counters-probe parity (entity IDs masked) and enumeration verdict lines.
import re
rc = f"{E}/bench-a200/bench/runC"
mask = lambda s: re.sub(r"(0x)?(020000fffe000001|3cc0c60102030000)", "ENTITY", s)
a = [mask(l) for l in open(f"{rc}/counters-probe-020000fffe000001.log")]
b = [mask(l) for l in open(f"{rc}/counters-probe-3cc0c60102030000.log")]
print("counters probe DUT vs peer identical modulo entity id:", a == b, "lines", len(a))
print([l.strip() for l in a if "verdict" in l])
for l in open(f"{rc}/a200-enum.log"):
    if l.startswith(("COMPLAINT", "SUMMARY")) or " flags=" in l or "milanInfo" in l or "compat-change" in l:
        print(l.strip())
