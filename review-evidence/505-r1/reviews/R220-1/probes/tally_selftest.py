import re, sys, collections
log = open(sys.argv[1]).read().splitlines()
arms = [l for l in log if "carrier-script-407" in l]
print("lines mentioning carrier-script-407:", len(arms))
c = collections.Counter()
jobs = collections.Counter()
other = []
for l in arms:
    m = re.match(r"\s+ok\s+caught: carrier-script-407 (\S+) step (\d+) (\S+(?: \S+)*)$", l)
    if m:
        c[(m.group(1), m.group(3))] += 1
        jobs[m.group(1)] += 1
        continue
    other.append(l)
for k in sorted(c):
    print(k, c[k])
print("per job:", dict(jobs), "total caught arms", sum(jobs.values()))
print("other lines:")
for l in other:
    print("  ", l[:200])
