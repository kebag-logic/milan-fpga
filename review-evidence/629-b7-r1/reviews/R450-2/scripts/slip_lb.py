#!/usr/bin/env python3
"""Tabulate SLIP_LB (0x8D4) and SLIP_TDM (0x8D8) from every runs/<case>/dut-*.txt console read."""
import glob, os, re, sys
root = sys.argv[1]
for case in sys.argv[2:]:
    fs = sorted(glob.glob(f'{root}/runs/{case}/dut-*.txt'), key=lambda p: [int(t) if t.isdigit() else t for t in re.split(r'(\d+)', p)])
    for p in fs:
        s = open(p).read()
        t = re.search(r'^### (\S+)', s, re.M)
        m = re.search(r'^0x900008d4((?:\s+[0-9a-f]{2}){8})', s, re.M)
        if not m:
            print(case, os.path.basename(p), 'no 0x8d4 read'); continue
        b = m.group(1).split()
        lb = int(b[1] + b[0], 16); lbs = int(b[3] + b[2], 16)
        tdm = int(b[5] + b[4], 16); tdms = int(b[7] + b[6], 16)
        print(f'{case:10s} {os.path.basename(p):22s} {t.group(1) if t else "?"} SLIP_LB dups={lb} skips={lbs} SLIP_TDM dups={tdm} skips={tdms}')
