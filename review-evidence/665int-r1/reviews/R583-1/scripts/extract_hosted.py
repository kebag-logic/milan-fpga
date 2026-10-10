#!/usr/bin/env python3
"""Extract the tally lines of a hosted job log (gh run view --log) into a receipt."""
import re, sys
pat = re.compile(r"(HEAD is now at|mutants: |of \d+ caught|test_ctrl_firmware: |firmware coverage|ESCAPED|"
                 r"\[ok\] (mutant )?(pub-|model-pub|cancelled-link)|PASS|FAIL|tests? passed|refused)")
for line in open(sys.argv[1], encoding="utf-8", errors="replace"):
    body = line.rstrip("\n").split("\t", 2)[-1]
    body = re.sub(r"\x1b\[[0-9;]*m", "", body)
    if pat.search(body):
        print(body[:300])
