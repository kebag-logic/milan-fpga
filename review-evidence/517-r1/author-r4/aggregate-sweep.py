from pathlib import Path
import hashlib
import json
import shutil
import subprocess
import sys

out = Path(__file__).resolve().parent
sys.path.insert(0,str(Path.cwd()/'scripts'))
from suite_tally import scan
inventory = json.loads((out/'sweep-inventory.json').read_text())
exits = json.loads((out/'sweep-exits.json').read_text())
assert len(exits) == 5 and all(row['exit_code'] == 0 for row in exits)
combined = out/'sweep-combined'
combined.mkdir(exist_ok=False)
owned = {}
total_checks = total_failures = 0
skips = []
for index in range(5):
    expected = next(row['suites'] for row in inventory if row['shard'] == f'{index}/5')
    logs = sorted((out/f'sweep-{index}').glob('*.log'))
    actual = [path.stem for path in logs]
    assert actual == expected, (index, actual, expected)
    for path in logs:
        assert path.stem not in owned, path
        data = path.read_bytes()
        shutil.copyfile(path, combined/path.name)
        checks, failures, matched, unparsed, skipped = scan(data.decode(errors='replace'))
        assert not unparsed and failures == 0, path
        total_checks += checks
        total_failures += failures
        skips.extend(dict(suite=path.stem,reason=reason) for reason in skipped)
        owned[path.stem] = dict(chunk=f'{index}/5',sha256=hashlib.sha256(data).hexdigest(),bytes=len(data),checks=checks,failures=failures,tallies=len(matched))
assert sorted(owned) == inventory[0]['suites']
result = subprocess.run(['python3','scripts/suite_tally.py',str(combined),'--expect-suite-root','tb/verilator'],check=False)
report = dict(exit_code=result.returncode,suites=len(owned),checks=total_checks,failures=total_failures,skips=skips,ownership=owned)
(out/'sweep-aggregate.json').write_text(json.dumps(report,indent=2)+'\n')
print(f'Combined sweep: {len(owned)} unique default suites; exit {result.returncode}',flush=True)
sys.exit(result.returncode)
