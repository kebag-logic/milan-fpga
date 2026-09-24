#!/usr/bin/env python3
"""For each <a>__<b>-<leg>.log written by swap_matrix.sh, report whether the
event arm's "events, all ten" check is red on BOTH exchanged quadlets.
usage: analyze_swaps.py LEG LOG...   (prints a table and a verdict line)"""
import re, subprocess, sys, os
here = os.path.dirname(os.path.abspath(__file__))
Q = {}
for l in subprocess.run([sys.executable, os.path.join(here, "mk_swap.py"), "--list"],
                        capture_output=True, text=True, check=True).stdout.split("\n"):
    if l.strip():
        k, q = l.split(); Q[k] = int(q)
leg = sys.argv[1]
ok = 0; rows = []
for p in sorted(sys.argv[2:]):
    name = os.path.basename(p)[: -len("-%s.log" % leg)]
    a, b = name.split("__")
    t = open(p).read()
    body = t.split("---- full output ----", 1)[1]
    fails = [l for l in body.splitlines() if "[FAIL]" in l]
    tal = re.search(r"^checks: (\d+)\s+failures: (\d+)", body, re.M)
    def red(q):
        return any(re.search(r"\[CTRS-CRF\] events, all ten: @%d " % (q * 4), f) for f in fails)
    both = red(Q[a]) and red(Q[b])
    ok += both
    rows.append("| %s | %s | @%d %s | @%d %s | %s | %s |" % (
        a, b, Q[a] * 4, "red" if red(Q[a]) else "GREEN", Q[b] * 4,
        "red" if red(Q[b]) else "GREEN", "%s/%s" % tal.groups() if tal else "none",
        "KILLED both" if both else "NOT BOTH"))
print("| port A | port B | quadlet A | | quadlet B | | tally | verdict |")
print("|---|---|---|---|---|---|---|---|")
print("\n".join(rows))
print("\n%d of %d exchanges red on both exchanged quadlets (%s)" % (ok, len(rows), leg))
