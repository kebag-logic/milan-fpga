"""Write the round-nine reviewed lists into ci/image/exec-audit.json (scratch).

The self-test's own entries leave the production lists (the self-test carries them); the population's
new entries from the given pin files are added; every other reviewed entry is kept.
Usage: apply_pins9.py PINS.json...
"""
import json, sys
from pathlib import Path
target = Path('$LANES/737-image/ci/image/exec-audit.json')
d = json.loads(target.read_text())
d['checkout_writes'].pop('zz_reviewed_write.txt', None)
d['inline_programs'] = {k: v for k, v in d['inline_programs'].items() if v['source'] != 'ci/image/exec_audit.py'}
d['generated_programs'] = {k: v for k, v in d['generated_programs'].items()
                           if v['generator'] != 'ci/image/exec_audit_selftest.py'}
added = {'inline_programs': 0, 'generated_programs': 0}
for path in sys.argv[1:]:
    pins = json.loads(Path(path).read_text())
    for key in added:
        for digest, entry in pins[key].items():
            if digest in d[key] and d[key][digest] != entry:
                raise SystemExit(f'REFUSED: {key} {digest} differs from its reviewed entry')
            added[key] += digest not in d[key]
            d[key][digest] = entry
target.write_text(json.dumps(d, indent=2, sort_keys=True) + '\n')
print(added, len(d['checkout_writes']), len(d['inline_programs']), len(d['generated_programs']), target.stat().st_size)
