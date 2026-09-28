"""Regenerate the five builder shapes and compare every artifact to the base."""
import hashlib
import json
from pathlib import Path
import sys

ROOT = Path('$LANES/602-phc-step-mr')
WORK = Path('$VALIDATION_STORAGE/602-a388-work')
OUT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT/'sw/builder'))
import endstation_builder as builder

before = json.loads((OUT/'generated-before.json').read_text())
after = {}
for config in sorted((ROOT/'configs').glob('endstation_*.yaml')):
    target = WORK/'generated-after'/config.stem
    builder.build(str(config), str(target))
    after[config.stem] = {
        str(path.relative_to(target)): {
            'bytes': path.stat().st_size,
            'sha256': hashlib.sha256(path.read_bytes()).hexdigest(),
        }
        for path in sorted(target.rglob('*')) if path.is_file()
    }
    assert after[config.stem] == before[config.stem], config.stem
    print(config.stem, len(after[config.stem]), 'artifacts: byte-identical')
assert len(after) == 5 and after == before
(OUT/'generated-after.json').write_text(json.dumps(after, indent=2)+'\n')
print('PASS: all 50 artifacts across five configurations remain byte-identical')
