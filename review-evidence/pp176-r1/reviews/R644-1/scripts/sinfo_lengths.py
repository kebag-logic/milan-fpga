#!/usr/bin/env python3
"""Print every observed outcome of AEM 0x000E (SET_STREAM_INFO) at the
lengths a reviewer probe added, from an aecp_cmds observed.json.
Usage: sinfo_lengths.py <observed.json>"""
import json
import sys
d = json.load(open(sys.argv[1]))["decode"]
for k, outcomes in d.items():
    if not k.startswith("AEM ") or not k.endswith("000E"):
        continue
    for upc, by_cdl in outcomes.items():
        for cdl, ans in sorted(by_cdl.items(), key=lambda t: int(t[0])):
            if int(cdl) in (59, 60, 61, 95, 96, 97, 100, 140):
                print(f"{k} upc={upc} cdl={cdl} answers={sorted(ans)}")
