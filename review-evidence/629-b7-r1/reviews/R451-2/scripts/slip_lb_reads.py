#!/usr/bin/env python3
"""Print SLIP_LB (0x8D4 word: [15:0] dups, [31:16] skips) from every DUT read file of one run,
in time order.  usage: slip_lb_reads.py <run dir>"""
import re, sys, pathlib
rows = []
for f in pathlib.Path(sys.argv[1]).glob("dut-*.txt"):
    txt = f.read_text(errors="replace")
    stamp = re.search(r"^### (\S+)", txt, re.M).group(1)
    m = re.search(r"^0x([0-9a-f]+)\s+((?:[0-9a-f]{2} ){4,16})", txt, re.M)
    for blk in re.finditer(r"cmd='mem_read 0x([0-9a-f]+) (\d+)'.*?\n0x[0-9a-f]+\s+((?:[0-9a-f]{2} ?)+)", txt, re.S):
        base, n, hexb = int(blk.group(1), 16), int(blk.group(2)), blk.group(3).split()
        for off in range(0, len(hexb) - 3, 4):
            if (base + off) & 0xFFF == 0x8D4:
                w = int.from_bytes(bytes(int(h, 16) for h in hexb[off:off + 4]), "little")
                rows.append((stamp, f.name, w & 0xFFFF, w >> 16))
for r in sorted(rows): print(*r)
