"""Remove one production guard at a time; restore source even on failure."""
import json
from pathlib import Path
import subprocess
import sys

ROOT = Path('$LANES/573-builder-refusals')
OUT = Path(__file__).resolve().parent
CASES = json.loads((OUT / 'mutations.json').read_text())
source = ROOT / 'sw/builder/endstation_builder.py'
original = source.read_text()
head = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip()
results = []
try:
    for case in CASES:
        if len(sys.argv) > 1 and case['issue'] != sys.argv[1]:
            continue
        old, new = case['old'], case['new']
        assert original.count(old) == 1, case['name']
        source.write_text(original.replace(old, new))
        result = subprocess.run(['python3', '-B', 'sw/builder/test_declarations.py'],
                                cwd=ROOT, capture_output=True, text=True, timeout=600)
        evidence = result.stdout + result.stderr
        assert result.returncode == 1 and case['failure'] in evidence, evidence
        last = evidence.splitlines()[-1]
        results.append(dict(head=head, issue=case['issue'], mutation=case['name'],
                            returncode=result.returncode, diagnostic=last))
        print(f"KILLED {case['issue']} {case['name']}: {last}")
finally:
    source.write_text(original)
destination = OUT / ('mutations-' + (sys.argv[1] if len(sys.argv) > 1 else 'all') + '.json')
destination.write_text(json.dumps(results, indent=2) + '\n')
if len(sys.argv) == 1:
    for issue in sorted({row['issue'] for row in results}):
        (OUT / f'mutations-{issue}.json').write_text(json.dumps(
            [row for row in results if row['issue'] == issue], indent=2) + '\n')
