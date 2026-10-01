#!/usr/bin/env python3
"""Page tool hashes vs packet tools; controller-side tool snapshots; DUT AAF_FRAMES and
SLIP_TDM rates from the console reads. usage: provenance_checks.py <author dir> <page>"""
import hashlib, re, sys
from datetime import datetime
from pathlib import Path
A, page = Path(sys.argv[1]), open(sys.argv[2]).read()
for name, h in re.findall(r"\| `([a-z_0-9]+\.py)` \| [^|]+\| `([0-9a-f]{64})` \|", page):
    got = hashlib.sha256((A / "tools" / name).read_bytes()).hexdigest()
    print(f"page {name} {h[:12]} packet {got[:12]} {'EQUAL' if got == h else 'DIFFERENT'}")
for snap in ("controller-start.txt", "controller-end.txt"):
    for l in open(A / "restore" / snap):
        if l.rstrip().endswith(".py") and len(l.split()[0]) == 64:
            print(f"{snap}: {l.split()[1]} {l.split()[0][:12]}")
def reads(f, addr):
    out = []; ts = None
    for l in open(f):
        m = re.match(r"### (\S+)Z cmd='mem_read (0x[0-9a-f]+)", l)
        if m: ts = (datetime.fromisoformat(m.group(1)), m.group(2)); continue
        if ts and ts[1] == addr and l.startswith(addr):
            toks = []
            for tok in l.split()[1:17]:
                if len(tok) != 2 or any(ch not in "0123456789abcdef" for ch in tok): break
                toks.append(tok)
            b = bytes.fromhex("".join(toks))
            out.append((ts[0], b)); ts = None
    return out
r = [reads(A / "runs/a-long" / f"dut-cont-{i}.txt", "0x90000660")[0] for i in range(3)]
for (t0, b0), (t1, b1) in zip(r, r[1:]):
    dt = (t1 - t0).total_seconds(); print(f"AAF_FRAMES rate {(int.from_bytes(b1[0:4],'little')-int.from_bytes(b0[0:4],'little'))/dt:.3f}/s over {dt:.3f} s")
s = [reads(A / "runs/a-long" / f"dut-cont-{i}.txt", "0x900008d4")[0] for i in (0, 2)]
d0, d1 = (int.from_bytes(b[4:6], "little") for _, b in s); k0, k1 = (int.from_bytes(b[6:8], "little") for _, b in s)
dt = (s[1][0] - s[0][0]).total_seconds()
print(f"SLIP_TDM dups {d0} -> {d1} (+{d1-d0}) skips {k0} -> {k1} over {dt:.3f} s = {(d1-d0)/dt:.4f}/s")
for f in ("restore/dut-start.txt", "restore/dut-end.txt"):
    t, b = reads(A / f, "0x900008d4")[0]
    print(f"{f}: SLIP_TDM dups {int.from_bytes(b[4:6],'little')} skips {int.from_bytes(b[6:8],'little')} at {t}")
plan = 100e6 * 23 / (2 * 37) * 34 / 43
off = (plan / (48000 * 512) - 1) * 1e6
print(f"divider plan A audio clock {plan:.3f} Hz, offset {off:.4f} ppm, beat {1/(-off*1e-6):.1f} frames = {1/(-off*1e-6)/48000:.4f} s")
