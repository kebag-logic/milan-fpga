#!/usr/bin/env python3
"""Every SLIP_TDM (0x8D8) read in a run's DUT console transcript: dups [15:0], skips [31:16].
usage: slip_tdm_reads.py <dut-read.txt>..."""
import re, sys, datetime
txt = "".join(open(f, errors="replace").read() for f in sys.argv[1:])
blocks = re.split(r"^### ", txt, flags=re.M)
rows = []
for b in blocks:
    m = re.match(r"(\S+) cmd='mem_read 0x900008d4 12'", b)
    if not m:
        continue
    d = re.search(r"0x900008d4\s+((?:[0-9a-f]{2} ){12})", b)
    by = bytes.fromhex(d.group(1).replace(" ", ""))
    w = int.from_bytes(by[4:8], "little")
    t = datetime.datetime.fromisoformat(m.group(1).replace("Z", "+00:00")).timestamp()
    rows.append((m.group(1), t, w & 0xFFFF, w >> 16, by[0:4].hex()))
rows.sort(key=lambda r: r[1])
for r in rows:
    print(r[0], "dups", r[2], "skips", r[3], "SLIP_LB", r[4])
for a, b in zip(rows, rows[1:]):
    print(f"{a[0]} -> {b[0]}: {b[1]-a[1]:.2f} s, dups +{b[2]-a[2]} ({(b[2]-a[2])/(b[1]-a[1]):.4f}/s), skips +{b[3]-a[3]}")
