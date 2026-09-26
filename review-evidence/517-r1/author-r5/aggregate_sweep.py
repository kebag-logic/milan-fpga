import json
import subprocess
import sys
from run_gate import ENV, OUT, ROOT, run

sys.path.insert(0, str(ROOT / 'scripts'))
from suite_tally import scan

inventory = json.loads((OUT / 'sweep-inventory.json').read_text())
all_names = []
rows = []
for index in range(5):
    directory = OUT / f'sweep-{index}'
    paths = sorted(directory.glob('*.log'))
    names = [path.stem for path in paths]
    assert names == sorted(inventory[str(index)]), (index, names)
    all_names.extend(names)
    gate = json.loads((OUT / f'sweep-{index}.json').read_text())
    assert gate['exit'] == 0, gate
    suites = []
    for path in paths:
        checks, failures, matched, unparsed, skipped = scan(path.read_text(errors='replace'))
        assert checks > 0 and failures == 0 and not unparsed, path
        suites.append(dict(suite=path.stem, checks=checks, failures=failures,
                           tallies=len(matched), unparsed=unparsed, skips=skipped))
    rows.append(dict(chunk=f'{index}/5', suites=len(suites),
                     checks=sum(row['checks'] for row in suites),
                     failures=sum(row['failures'] for row in suites),
                     declared_skips=sum(len(row['skips']) for row in suites),
                     seconds=gate['seconds'], exit=gate['exit'], details=suites))
assert len(all_names) == len(set(all_names)) == 55
result = dict(head=subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=ROOT, text=True).strip(),
              suites=len(all_names), checks=sum(row['checks'] for row in rows),
              failures=sum(row['failures'] for row in rows),
              declared_skips=sum(row['declared_skips'] for row in rows), chunks=rows)
(OUT / 'sweep-summary.json').write_text(json.dumps(result, indent=2)+'\n')
argv = ['python3', 'scripts/suite_tally.py', '--expect-suite-root', str(ROOT / 'tb/verilator')]
argv.extend(str(OUT / f'sweep-{index}') for index in range(5))
assert run('sweep-accounting', argv) == 0
print(json.dumps({key: value for key, value in result.items() if key != 'chunks'}), flush=True)
