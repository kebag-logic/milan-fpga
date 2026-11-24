"""srptx_lines.py LOG: each scenario's finding lines, first run of each scenario, sorted by scenario name."""
import gzip, re, sys
p = sys.argv[1]; text = (gzip.open(p, "rt") if p.endswith(".gz") else open(p)).read()
seen, cur, out = set(), [], {}
for line in text.splitlines():
    m = re.match(r"^srptx (\w+): \d+ finding\(s\)", line)
    if m:
        if m.group(1) not in seen:
            seen.add(m.group(1)); out[m.group(1)] = cur
        cur = []
    elif re.match(r"^\[[A-Z]+\]", line):
        cur.append(line)
for k in sorted(out):
    for l in out[k]:
        print(f"{k}\t{l}")
