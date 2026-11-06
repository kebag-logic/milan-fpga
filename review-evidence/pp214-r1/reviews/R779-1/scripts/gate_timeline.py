#!/usr/bin/env python3
"""Print the parent gates' start, end, rc and interpreter record. usage: gate_timeline.py <parent-chain dir>"""
import glob, os, sys, time
root = sys.argv[1]
def rd(p):
    return open(p).read().strip() if os.path.exists(p) else ""
def ts(s):
    return time.strftime("%H:%M:%S", time.gmtime(int(s))) if s else "--:--:--"
for name, sub in (("cited gates (UTC)", "gates"), ("first attempt, not cited (UTC)", "first-attempt-system-python")):
    print("==", name)
    rows = []
    for f in glob.glob(f"{root}/{sub}/*.cmd"):
        b = f[:-4]
        rows.append((rd(b + ".start"), os.path.basename(b), rd(b + ".rc") or "none", rd(b + ".end"), rd(b + ".python").replace("\n", " | ")))
    for s, g, rc, e, py in sorted(rows):
        print(ts(s), ts(e), "rc=" + rc, g, py)
