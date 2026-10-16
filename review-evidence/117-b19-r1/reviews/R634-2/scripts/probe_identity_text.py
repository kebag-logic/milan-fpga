#!/usr/bin/env python3
"""Count, without printing it, the takeover Announce's clock identity (priority1 240,
from the gm01..gm05 tap captures) in five spellings across given text files.
Usage: probe_identity_text.py RAW_ROOT FILE..."""
import struct, sys
from pathlib import Path
raw = Path(sys.argv[1]); ids = set()
for run in ("gm01", "gm02", "gm03", "gm04", "gm05"):
    b = open(raw / run / "tap.pcap", "rb").read(); off = 24
    while off + 16 <= len(b):
        _, _, incl, _ = struct.unpack("<IIII", b[off:off + 16]); off += 16
        pkt = b[off:off + incl]; off += incl
        if len(pkt) < 42 or struct.unpack("<I", pkt[:4])[0] != 6: continue
        fr = pkt[28:]; et = struct.unpack(">H", fr[12:14])[0]; p = fr[14:]
        if et == 0x8100: et = struct.unpack(">H", fr[16:18])[0]; p = fr[18:]
        if et == 0x88F7 and len(p) >= 61 and (p[0] & 0xF) == 0xB and p[47] == 240: ids.add(p[53:61].hex())
print("identities:", len(ids))
for f in sys.argv[2:]:
    t = open(f, encoding="utf-8", errors="replace").read().lower(); n = 0
    for v in ids:
        for form in (v, ":".join(v[i:i+2] for i in range(0, 16, 2)), v[:6] + "." + v[6:10] + "." + v[10:],
                     ":".join((v[:6] + v[10:])[i:i+2] for i in range(0, 12, 2)), "-".join(v[i:i+2] for i in range(0, 16, 2))):
            n += t.count(form)
    print(f"{Path(f).name}: {n} hits")
