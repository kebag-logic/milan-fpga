"""Compare the final fw_coverage --check table in a hosted firmware-unit job log with a coverage.ratchet image.
Usage: python3 -I hosted_rows.py <job log, escape codes stripped> <ratchet image> [timestamp prefix of the final table]"""
import sys
log, rat = sys.argv[1], sys.argv[2]
pfx = sys.argv[3] if len(sys.argv) > 3 else "2026-11-12T03:55:"
rows = {}
for l in open(log):
    f = l.split()
    if len(f) >= 4 and f[0].startswith(pfx) and (f[1].startswith("sw/") or f[1].startswith("third_party/")) and "/" in f[2]:
        rows[f[1]] = (f[2].split("/")[0], f[3].split("/")[0])
r = {l.split()[0]: l.split() for l in open(rat) if l.strip() and not l.startswith("#")}
lbad = [(k, rows[k][0], r[k][2]) for k in rows if r[k][2] != f"{rows[k][0]}/{rows[k][0]}"]
bbad = [(k, rows[k][1], r[k][4]) for k in rows if r[k][4] != f"{rows[k][1]}/{rows[k][1]}"]
print(f"hosted --check rows {len(rows)}; ratchet image rows {len(r)}")
print(f"line-count differences {len(lbad)}: {lbad}")
print(f"branch-count differences {len(bbad)}: {bbad}")
