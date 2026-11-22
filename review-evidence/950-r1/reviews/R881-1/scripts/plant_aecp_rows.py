"""plant_aecp_rows.py <test-dir> <out> <name>...: plant only the named rows of aecp_mutants.DEFECTS through the AECP
campaign's own planting and grading (aecp_mutants.campaign, which works on a copy), its drift control first."""
import json, sys
from pathlib import Path
sys.path.insert(0, sys.argv[1])
import aecp_mutants as am
out, names = Path(sys.argv[2]), sys.argv[3:]
am.controls()
rows = tuple(d for d in am.DEFECTS if d.name in names)
assert {d.name for d in rows} == set(names), set(names) - {d.name for d in rows}
am.DEFECTS = rows
am.controls = lambda: None
escaped = am.campaign(out, jobs=4)
res = json.loads((out / "results.json").read_text())
for r in res:
    print(json.dumps(r)[:600])
print(f"caught {sum(r['caught'] for r in res)} of {len(res)}")
sys.exit(1 if escaped else 0)
