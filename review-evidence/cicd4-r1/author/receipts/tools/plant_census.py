"""Plant failures into copies of the real census leg receipts and require the judge to refuse each."""
import copy, json, shutil, subprocess, sys
from pathlib import Path
snap, results, scratch = Path(sys.argv[1]), Path(sys.argv[2]), Path(sys.argv[3])
real = {p.parent.name: json.loads(p.read_text()) for p in results.rglob("census-leg-*.json")}
def judge(records):
    if scratch.exists():
        shutil.rmtree(scratch)
    for name, record in records:
        (scratch / name).mkdir(parents=True, exist_ok=True)
        (scratch / name / (name + ".json")).write_text(json.dumps(record))
    run = subprocess.run([sys.executable, "sw/mailbox/census_legs.py", "union", "--root", str(scratch)],
                         cwd=snap, capture_output=True, text=True)
    return run.returncode, (run.stderr.strip().splitlines() or run.stdout.strip().splitlines() or [""])[-1]
base = sorted(real.items())
rc, last = judge(base)
print(f"unplanted: rc={rc} {last}")
assert rc == 0
def edited(leg, edit):
    records = copy.deepcopy(base)
    edit(records[leg][1])
    return records
plants = [
    ("leg 2 failed its arm", edited(2, lambda r: r["rows"][0].update(ok=False))),
    ("leg 3 exit 1", edited(3, lambda r: r.update(exit=1))),
    ("leg 1 rule removal held", edited(1, lambda r: next(x for x in r["rows"] if x["through"] is not None).update(through=False))),
    ("leg 4 lost an arm", edited(4, lambda r: r["rows"].pop())),
    ("leg 0 missing", base[1:]),
    ("leg 1 twice", base + [("census-leg-1b", base[1][1])]),
    ("leg 2 another head", edited(2, lambda r: r.update(head="0" * 40))),
]
for label, records in plants:
    rc, last = judge(records)
    print(f"planted {label}: rc={rc} {last}")
    assert rc != 0, label
print("every planted census failure refused")
