"""srptx_sum.py LOG: each scenario's finding kinds by protocol (first occurrence of each scenario only)."""
import collections, gzip, re, sys
p = sys.argv[1]; text = (gzip.open(p, "rt") if p.endswith(".gz") else open(p)).read()
seen, cur, counts = set(), [], collections.Counter()
for line in text.splitlines():
    m = re.match(r"^srptx (\w+): (\d+) finding\(s\), (\d+) MRPDUs", line)
    if m:
        if m.group(1) not in seen:
            seen.add(m.group(1))
            c = collections.Counter(cur)
            print(f"{m.group(1)}: {m.group(2)} findings, {m.group(3)} MRPDUs; " + ", ".join(f"{k} {v}" for k, v in sorted(c.items())))
        cur = []
        continue
    k = re.match(r"^\[([A-Z]+)\] ?(MSRP|MVRP)?", line)
    if k:
        cur.append(f"[{k.group(1)}]{' ' + k.group(2) if k.group(2) else ''}")
