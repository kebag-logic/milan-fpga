"""Independent recount of a `/usr/bin/time` sv2v per-run log: '<KiB> KiB <s> s sv2v' lines,
each optionally preceded by 'Command exited with non-zero status N'. Usage: python3 -I sv2v_recount3.py <log>"""
import hashlib, re, sys
data = open(sys.argv[1], "rb").read()
print("log sha256", hashlib.sha256(data).hexdigest())
runs, pending, bad = [], False, []
for n, line in enumerate(data.decode().splitlines(), 1):
    if re.fullmatch(r"Command exited with non-zero status \d+", line):
        pending = True
    elif m := re.fullmatch(r"(\d+) KiB [0-9.]+ s sv2v", line):
        runs.append((int(m[1]), pending)); pending = False
    else:
        bad.append(n)
assert not bad and not pending, bad
kib = [k for k, _ in runs]
big = [k for k in kib if k >= 1_000_000]
print("runs", len(runs), "| nonzero", sum(z for _, z in runs))
print("at or above 1000000 KiB", len(big), "| span", min(big), "to", max(big))
print("above 1205884 KiB", sum(k > 1205884 for k in kib), "| max", max(kib))
print("nonzero runs' peaks", sorted(k for k, z in runs if z))
print("big runs that exited nonzero", sum(z for k, z in runs if k >= 1_000_000))
print("runs below 1000000 KiB", sorted(k for k in kib if k < 1_000_000))
