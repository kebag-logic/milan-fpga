"""cmp_counts.py <mutants.py of the run> <campaign log> <README>...: pair each campaign arm line with its MUTANTS
entry in order, then report every README table row `| `arm` ... | group | N | ... |` whose N differs from the
measured failures of that (arm, group)."""
import ast, re, sys
from pathlib import Path
src = Path(sys.argv[1]).read_text()
tree = ast.parse(src)
muts = None
for node in tree.body:
    if isinstance(node, ast.Assign) and getattr(node.targets[0], 'id', '') == 'MUTANTS':
        muts = ast.literal_eval(node.value)
lines = [m.group(0) for l in Path(sys.argv[2]).read_text().splitlines()
         for m in [re.search(r'(?<![A-Za-z0-9-])[A-Za-z0-9-]+: rc=\d+ failures=\d+ (KILLED|UNPROVEN).*$', l)] if m]
assert len(lines) == len(muts), (len(lines), len(muts))
meas = {}
for (arm, suite, group, _), l in zip(muts, lines):
    assert l.startswith(arm + ':'), (arm, l)
    n = int(re.search(r'failures=(\d+)', l).group(1))
    meas.setdefault((arm, suite, group), n)
    meas[(arm, suite, group)] = n
print(f"{len(lines)} arm runs paired")
for readme in sys.argv[3:]:
    suite = Path(readme).parent.name
    for i, row in enumerate(Path(readme).read_text().splitlines(), 1):
        m = re.match(r'^\| `([A-Za-z0-9-]+)`[^|]*\| ([a-z0-9]+) \| (\d+) \|', row)
        if not m:
            continue
        arm, group, n = m.group(1), m.group(2), int(m.group(3))
        key = (arm, suite, group)
        if key not in meas:
            print(f"{readme}:{i}: {arm} {group}: recorded {n}, NOT GRADED in this campaign")
        elif meas[key] != n:
            print(f"{readme}:{i}: {arm} {group}: recorded {n}, measured {meas[key]}")
