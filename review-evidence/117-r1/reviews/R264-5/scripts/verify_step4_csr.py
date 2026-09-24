#!/usr/bin/env python3
"""Steady-state CSR words read over the console in the A200 runs.

Usage: verify_step4_csr.py <a200-packet-dir>
"""
import collections
import re
import statistics
import sys

pk = sys.argv[1]
names = {"0x9000077c": "CLKV_STAT", "0x90000780": "CLKV_TUCNT", "0x90000764": "CRFT_COUNT", "0x90000750": "CRFT_CTRL",
         "0x900007e8": "GPTP_DROPW", "0x900007ec": "GPTP_DROPE", "0x900006f4": "CTLR_DIAG", "0x900007f0": "GPTP_LAT",
         "0x90000720": "RST_EPOCH", "0x90000774": "LINKG_STAT", "0x9000062c": "ADP_GPTP_DOMAIN", "0x900007e4": "ASP_CMD"}
vals, pd = collections.defaultdict(list), []
for rel in ["bench/runA/console.txt", "bench/runB/console.txt", "bench/final/console-final.txt", "identity/console-identity.txt"]:
    t = open(f"{pk}/{rel}", errors="replace").read()
    for m in re.finditer(r"mem_read (0x9000[0-9a-f]{4}) 4\nMemory dump:\n0x9000[0-9a-f]{4}\s+(\S\S) (\S\S) (\S\S) (\S\S)", t):
        vals[(rel.split("/")[-2], m.group(1))].append("".join(reversed(m.groups()[1:])))
    pd += [int(x) for x in re.findall(r"PDELAY_NS=(\d+)", t)]
for (run, a), v in sorted(vals.items()):
    c = collections.Counter(v)
    print(f"{run:10s} {names.get(a, a):16s} reads {len(v):3d} values {dict(c) if len(c) <= 6 else (min(v), max(v), len(c))}")
print("milan_status PDELAY_NS: min", min(pd), "max", max(pd), "median", statistics.median(pd), "n", len(pd))
