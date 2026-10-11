import re, sys, collections
arm = kind = None; legs = collections.defaultdict(collections.Counter); count = collections.Counter()
for line in open(sys.argv[1]):
    m = re.match(r"^(\S+): rc=\d+ (KILLED|UNPROVEN)", line)
    if m:
        arm = m.group(1); kind = arm if arm.startswith("bench:") else arm.split(":")[-1]
        count[kind] += 1; continue
    m = re.match(r"^    FAIL: (GUARD|ELAB |inventory)\s*(\w+)?", line)
    if m and arm:
        leg = m.group(2) if m.group(1) != "inventory" else "-"
        legs[kind][(m.group(1).strip(), leg)] += 1
for kind in count:
    print(kind, count[kind], dict(legs[kind]))
