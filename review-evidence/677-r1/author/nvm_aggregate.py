# Standalone validation helper; run from a candidate checkout.
import os
import json
from pathlib import Path
import sys

repo = Path.cwd()
work = Path(os.environ["VALIDATION_WORK"]).resolve()
sys.path.insert(0, str(repo / "sw/firmware/ctrl_nvm/test"))
import nvm_mutants

names = [m.name for m in nvm_mutants.MUTANTS]
records = {}
for directory in sorted(work.glob("nvm-batch-*")):
    for path in sorted(directory.glob("*.json")):
        record = json.loads(path.read_text())
        assert record["name"] not in records, record["name"]
        records[record["name"]] = record
assert len(names) == len(set(names)) == 109, len(names)
assert sorted(records) == sorted(names), set(records) ^ set(names)
findings = [r for r in records.values() if r["finding"]]
assert not findings, findings
(work / "nvm-campaign.json").write_text(json.dumps(dict(
    head=sys.argv[1], mutants=len(names), caught=len(names) - len(findings),
    records=[records[n] for n in names]), indent=1) + "\n")
print(f"NVM campaign at {sys.argv[1]}: {len(names)} repository mutants, each graded once, {len(findings)} findings")
