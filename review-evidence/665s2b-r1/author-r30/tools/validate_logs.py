"""Parse every finished group log of the given result dirs with the harness's own parser (grade.parse) and its grade
(grade.grade), reporting each that raises: a log a full disk cut. usage: python3 -I validate_logs.py HARNESS N_IF DIR..."""
import json, sys
from pathlib import Path
sys.path.insert(0, sys.argv[1])
import grade, scenario
n_if = int(sys.argv[2])
bad = ok = 0
for d in sys.argv[3:]:
    for f in sorted(Path(d).glob('*.log')):
        t = f.read_text(errors='replace')
        if 'SUMMARY' not in t[-4000:]:
            continue
        try:
            grade.parse(t, 100_000_000, 100_000_000)
            ok += 1
        except Exception as e:
            bad += 1
            print(f'BAD {f.parent.name}/{f.name}: {type(e).__name__} {e}')
print(f'{ok} parse, {bad} bad')
