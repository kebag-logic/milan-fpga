"""Compare the milan_dp README campaign table's "N of M" column with a campaign verdict file.
Usage: python3 -I readme_vs_verdicts.py <README.md> <verdicts.txt>"""
import re, sys
rows = {}
for line in open(sys.argv[1]):
    m = re.match(r"\| (\d+) \| [^|]+ \| ([^|]+) \| .* \| (\d+) of (\d+) \|$", line.strip())
    if m:
        rows[int(m.group(1))] = (m.group(2).strip(), int(m.group(3)), int(m.group(4)))
got = []
for line in open(sys.argv[2]):
    m = re.match(r"\[PASS\] mutant caught: (.*?) - breaks .*report (\d+) failure\(s\) across (\d+) checks", line)
    if m:
        got.append((m.group(1), int(m.group(2)), int(m.group(3))))
bad = 0
print(f"README rows {len(rows)}, verdict mutants {len(got)}")
for i, (name, n, t) in enumerate(got, 1):
    r = rows.get(i)
    same = r is not None and r[0] == name and r[1] == n and r[2] == t
    bad += not same
    if not same:
        print(f"DIFF row {i}: README {r} verdict {(name, n, t)}")
print("all rows agree" if not bad and len(rows) == len(got) else f"{bad} differ")
sys.exit(1 if bad or len(rows) != len(got) else 0)
