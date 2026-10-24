"""Prefix raw job-log lines with the two tab columns `gh run view --log` adds, so suite_shards.py --measure can read them.
usage: python3 -I tabify.py <raw-job-log> <job-name> <out>"""
import sys
src, name, out = sys.argv[1:4]
with open(src, encoding="utf-8", errors="replace") as f, open(out, "w", encoding="utf-8") as o:
    for line in f: o.write(f"{name}\tstep\t{line}")
