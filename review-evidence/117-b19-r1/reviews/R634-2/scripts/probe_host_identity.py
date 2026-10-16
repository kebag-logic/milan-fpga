#!/usr/bin/env python3
"""Find the clock identity the takeover Announce named (priority1 240) in a
run's tap capture, and count its occurrences under docs/ of a checkout in
five spellings. Prints counts only, never the value.
Usage: probe_host_identity.py RAW_ROOT CHECKOUT"""
import subprocess, sys
from pathlib import Path
raw, co = Path(sys.argv[1]), sys.argv[2]
ids = set()
import struct
for run in ("gm01", "gm02", "gm03", "gm04", "gm05"):
    raw_b = open(raw / run / "tap.pcap", "rb").read(); off = 24
    while off + 16 <= len(raw_b):
        _, _, incl, _ = struct.unpack("<IIII", raw_b[off:off + 16]); off += 16
        pkt = raw_b[off:off + incl]; off += incl
        if len(pkt) < 42 or struct.unpack("<I", pkt[:4])[0] != 6: continue
        fr = pkt[28:]; et = struct.unpack(">H", fr[12:14])[0]; p = fr[14:]
        if et == 0x8100: et = struct.unpack(">H", fr[16:18])[0]; p = fr[18:]
        if et == 0x88F7 and len(p) >= 61 and (p[0] & 0xF) == 0xB and p[47] == 240:
            ids.add(p[53:61].hex())
print("distinct priority1-240 grandmaster identities:", len(ids))
for v in ids:
    forms = {"plain": v, "colon": ":".join(v[i:i+2] for i in range(0, 16, 2)), "dotted": v[:6] + "." + v[6:10] + "." + v[10:],
             "mac-derived": ":".join((v[:6] + v[10:])[i:i+2] for i in range(0, 12, 2)), "upper": v.upper()}
    for k, f in forms.items():
        rc = subprocess.run(["git", "-C", co, "grep", "-i", "-c", "-F", f, "HEAD", "--", "docs"], capture_output=True, text=True)
        n = sum(int(l.rsplit(":", 1)[1]) for l in rc.stdout.splitlines()) if rc.stdout.strip() else 0
        print(f"form {k}: {n} hits under docs/ at HEAD")
