#!/usr/bin/env python3
"""Misc packet checks: AAF_FRAMES rate over the window, DUT console writes, initial-bind gap.
usage: misc_checks.py <packet author dir>"""
import re, sys, json, glob, datetime
A = sys.argv[1]
def reads(files, addr):
    out = []
    for f in files:
        for b in re.split(r"^### ", open(f, errors="replace").read(), flags=re.M):
            m = re.match(r"(\S+) cmd='mem_read 0x%08x" % addr, b)
            if m:
                d = re.search(r"0x%08x\s+((?:[0-9a-f]{2} ){4})" % addr, b)
                t = datetime.datetime.fromisoformat(m.group(1).replace("Z", "+00:00")).timestamp()
                out.append((t, int.from_bytes(bytes.fromhex(d.group(1).replace(" ", "")), "little")))
    return sorted(out)
R = A + "/runs/a-long/"
fr = reads([R + x for x in ("dut-cont-0.txt", "dut-cont-1.txt", "dut-cont-2.txt")], 0x90000660)
for a, b in zip(fr, fr[1:]):
    print(f"AAF_FRAMES +{(b[1]-a[1]) & 0xffffffff} over {b[0]-a[0]:.2f} s = {((b[1]-a[1]) & 0xffffffff)/(b[0]-a[0]):.2f}/s")
w = 0
for f in glob.glob(A + "/**/*.txt", recursive=True) + glob.glob(A + "/**/*.log", recursive=True):
    for line in open(f, errors="replace"):
        if re.search(r"cmd='(mem_write|mem_copy|flash|reboot|reset)", line):
            w += 1; print("WRITE-LIKE", f, line.strip()[:120])
print("DUT console write-like commands in packet:", w)
ev = [json.loads(l) for l in open(A + "/runs/diag1/events.jsonl")]
ub = [e for e in ev if e["kind"] == "unbind"]
evl = [json.loads(l) for l in open(R + "events.jsonl")]
b0 = [e for e in evl if e["kind"] == "bind"][0]
print("diag1 unbinds", len(ub), "gap to a-long initial bind response (local clock) s:",
      round(b0["t"] - ub[-1]["t"], 1) if ub else None)
