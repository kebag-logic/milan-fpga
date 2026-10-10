#!/usr/bin/env python3
"""Decode the item-6 console reads: 0x110 (MAC_STATUS), 0x200..0x233 (STATS window).

Usage: item6_console.py <packet-author-dir>
"""
import re, sys
from pathlib import Path

A = Path(sys.argv[1])
files = [A / "soak/console-prebind.txt"] + [A / f"soak/console-soak-{n:03d}.txt" for n in range(0, 121, 5)] + [A / "restore/console-final.txt"]
rows = []
for f in files:
    words, cur = {}, None
    for line in open(f, errors="replace"):
        m = re.match(r"0x9000(0[0-9a-f]{3})\s+((?:[0-9a-f]{2} )+)", line)
        if m:
            base = int(m.group(1), 16)
            b = bytes.fromhex(m.group(2).replace(" ", ""))
            for i in range(0, len(b) - 3, 4):
                words[base + i] = int.from_bytes(b[i:i + 4], "little")
    rows.append((f.name, words.get(0x110), words.get(0x204), [words.get(a) for a in range(0x210, 0x234, 4)], words.get(0x200)))
for r in rows:
    print(r[0], "MAC_STATUS=%s" % (hex(r[1]) if r[1] is not None else None),
          "STATS_CAP=%s" % (hex(r[2]) if r[2] is not None else None), "lanes0x210..0x230=", r[3])
cap = {r[2] for r in rows}
print("reads:", len(rows), "STATS_CAP values:", [hex(c) for c in cap if c is not None])
c = 0x1B8
print("0x1B8 bits set:", [n for n in range(9) if c >> n & 1], "bit6:", c >> 6 & 1)
print("all lanes zero at every read:", all(all(v == 0 for v in r[3] if v is not None) and None not in r[3] for r in rows))
print("MAC_STATUS all 0xd:", all(r[1] == 0xd for r in rows))
