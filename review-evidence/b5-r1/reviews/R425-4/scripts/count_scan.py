#!/usr/bin/env python3
"""List every line where a number word or numeral sits within four words of a
stream / cluster / port / census / entry noun, for manual review of the
stream-count ruling. usage: count_scan.py FILE..."""
import re, sys
NUM = r"(?:\d[\d,]*|one|two|three|four|five|six|seven|eight|nine|ten|eleven|twelve|both|all|every|each)"
NOUN = r"(?:streams?|stream states?|stream ports?|clusters?|ports?|census|entries|entry|STREAM_\w+)"
rx = re.compile(rf"\b{NUM}\b(?:\W+\w+){{0,4}}?\W+{NOUN}\b|\b{NOUN}\b(?:\W+\w+){{0,2}}?\W+{NUM}\b", re.I)
for f in sys.argv[1:]:
    for n, line in enumerate(open(f), 1):
        for m in rx.finditer(line):
            print(f"{f.split('/')[-1]}:{n}: {m.group(0)}")
