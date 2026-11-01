#!/usr/bin/env python3
"""Bit and offset coverage of the stream-engine register tables.

Usage: python3 -I regmap_check.py <MARK_II_STREAM_ENGINES.md>
For each of the three tables under "Register maps": every register's fields
must cover bits 31:0 exactly once, and offsets must run contiguously from 0
to the block end (ranges such as 0x018-0x01C count as one row).
"""
import re, sys
text = open(sys.argv[1], encoding="utf-8").read()
sec = text[text.index("## Register maps"):text.index("## Block RAM ledger")]
ends = {"Engine registers": 0x2000, "Talker context": 0x40, "Listener context": 0x80}
rc = 0
for title, end in ends.items():
    body = sec[sec.index("### " + title) + 4:]
    body = body[:body.index("\n### ")] if "\n### " in body else body
    rows = [l for l in body.splitlines()
            if l.startswith("| ") and not l.startswith("| Offset") ]
    regs, cur = [], None
    for l in rows:
        c = [x.strip() for x in l.strip().strip("|").split("|")]
        if c[0]:
            cur = [c[0], c[1], []]; regs.append(cur)
        cur[2].append(c[2])
    expect = 0
    for off, name, bits in regs:
        m = re.match(r"0x([0-9A-F]+)(?:-0x([0-9A-F]+))?$", off)
        lo = int(m.group(1), 16); hi = int(m.group(2), 16) if m.group(2) else lo
        if lo != expect:
            print(f"{title}: gap or overlap before {off} (expected 0x{expect:X})"); rc = 1
        expect = hi + 4
        if bits == ["-"]:
            continue
        cov = [0] * 32
        for b in bits:
            m2 = re.match(r"(\d+)(?::(\d+))?$", b)
            h = int(m2.group(1)); l = int(m2.group(2)) if m2.group(2) else h
            for i in range(l, h + 1): cov[i] += 1
        bad = [i for i, v in enumerate(cov) if v != 1]
        if bad:
            print(f"{title}: {name} bits not covered exactly once: {bad}"); rc = 1
    if expect != end:
        print(f"{title}: ends at 0x{expect:X}, expected 0x{end:X}"); rc = 1
    print(f"{title}: {len(regs)} rows, offsets 0x0 to 0x{expect:X}, fields checked")
print("regmap_check:", "PASS" if rc == 0 else "FAIL"); sys.exit(rc)
