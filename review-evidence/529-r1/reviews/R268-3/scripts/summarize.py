#!/usr/bin/env python3
"""Tabulate leg logs written by leg.py: per case, the exit, the tally, which
of the four CRF bind-edge checks failed, and how many other [FAIL] lines.
usage: summarize.py LOG...   (prints a markdown table)"""
import re, sys
EDGE = [
    ("sin", "[CTRS-CRF] the bind edge reached the arbiter as STREAM_INPUT N only"),
    ("sout", "[CTRS-CRF] ...and as no STREAM_OUTPUT row"),
    ("avbckd", "[CTRS-CRF] ...nor AVB_INTERFACE 0 or CLOCK_DOMAIN 0"),
    ("other", "[CTRS-CRF] ...nor any tuple of another type or index"),
]
print("| case | leg | args | exit | tally | bind-edge checks red | other [FAIL] lines |")
print("|---|---|---|---|---|---|---|")
for p in sys.argv[1:]:
    t = open(p).read()
    leg = re.search(r"^leg (\S+) args ?(.*)$", t, re.M)
    ex = re.search(r"^exit (\d+)", t, re.M).group(1)
    tal = re.search(r"^checks: (\d+)\s+failures: (\d+)", t, re.M)
    body = t.split("---- full output ----", 1)[1]
    fails = [l.strip() for l in body.splitlines() if "[FAIL]" in l]
    red = [k for k, s in EDGE if any(s[:46] in f for f in fails)]
    others = [f for f in fails if not any(s[:46] in f for _, s in EDGE)]
    case = p.rsplit("/", 1)[-1].rsplit("-" + leg.group(1)[4:] + ".log", 1)[0]
    print("| %s | %s | `%s` | %s | %s | %s | %d |" % (
        case, leg.group(1), leg.group(2).strip(), ex,
        ("%s/%s" % tal.groups()) if tal else "none",
        ",".join(red) if red else "-", len(others)))
