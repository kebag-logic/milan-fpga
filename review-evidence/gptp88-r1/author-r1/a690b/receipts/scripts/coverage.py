"""Map every check new at head to the mutants whose run fails it.

usage: coverage.py <suite> <base names> <head names> <mutant log dir> <out md>
A check is new when its name occurs more often at head than at base. A
FAIL line names its check as the text after "FAIL " up to " got ".
"""
import collections, re, sys
from pathlib import Path
suite, base_f, head_f, logdir, out = sys.argv[1:6]
base = collections.Counter(Path(base_f).read_text().splitlines())
head = collections.Counter(Path(head_f).read_text().splitlines())
new = [n for n in dict.fromkeys(Path(head_f).read_text().splitlines())
       if head[n] > base.get(n, 0)]
gone = [n for n in base if n not in head]
fails = {}
for log in sorted(Path(logdir).glob("*.log")):
    if log.name in ("run.log",):
        continue
    lines = log.read_text().splitlines()
    if not lines or not lines[0].startswith("mutant: "):
        continue
    mname = lines[0][len("mutant: "):]
    names = set()
    for l in lines:
        if l.startswith("FAIL ") and " got " in l:
            names.add(l[5:l.rindex(" got ")].rstrip())
    fails[mname] = names
rows, uncovered = [], []
for n in new:
    by = sorted(m for m, s in fails.items() if n in s)
    rows.append((n, by))
    if not by:
        uncovered.append(n)
with open(out, "w") as f:
    f.write(f"# {suite}: checks new at head and the mutants that fail them\n\n")
    f.write(f"Base {sum(base.values())} check executions, head "
            f"{sum(head.values())}; {len(new)} new check names; "
            f"{len(gone)} base names no longer run; "
            f"{len(new) - len(uncovered)} of {len(new)} new names fail under "
            f"at least one planted mutant.\n\n")
    if uncovered:
        f.write("## Not failed by any mutant\n\n" +
                "".join(f"- {n}\n" for n in uncovered) + "\n")
    f.write("## New checks\n\n")
    for n, by in rows:
        f.write(f"- {n} <- {'; '.join(by) if by else 'NONE'}\n")
    f.write("\n## Base checks no longer run\n\n" +
            "".join(f"- {n}\n" for n in gone))
print(f"{suite}: {len(new)} new, {len(uncovered)} uncovered, {len(gone)} gone")
for n in uncovered:
    print("UNCOVERED", n)
