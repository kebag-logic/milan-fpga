#!/usr/bin/env python3
"""Recount the author's round-2 per-sv2v peaks against the figures in docs/testing/CI_WORKFLOWS.md.

Usage: python3 sv2v_recount.py <sv2v-rss-selftest.log>
The log is review-evidence/744-r1/author-r2/evidence/r2/sv2v-rss-selftest.log at evidence commit
67e05179f28bc777a18f136cfdb759e2adf9750c (published sha256 d91554a6...4f43, unredacted).
"""
import hashlib
import re
import sys

raw = open(sys.argv[1], "rb").read()
print("sha256", hashlib.sha256(raw).hexdigest())
peaks = [int(m.group(1)) for m in re.finditer(rb"^(\d+) KiB [\d.]+ s sv2v$", raw, re.M)]
failed = raw.count(b"Command exited with non-zero status")
print("sv2v runs:", len(peaks), "| exited nonzero:", failed)
print("largest:", max(peaks), "KiB")
print("above 1205884 KiB (round-1 constant):", sum(p > 1205884 for p in peaks))
print("at or above 1000000 KiB:", sum(p >= 1000000 for p in peaks))
print("at or above 1100000 KiB:", sum(p >= 1100000 for p in peaks))
print("below 1000000 KiB:", sorted(p for p in peaks if p < 1000000))
print("documented: 25 elaborated the full datapath, 23 of them above 1205884 KiB, largest 1212036 KiB")
