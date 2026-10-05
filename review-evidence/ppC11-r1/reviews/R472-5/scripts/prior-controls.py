#!/usr/bin/env python3
"""Recheck the prior parser and figure self-test defects in disposable scripts."""
import concurrent.futures
import json
import os
from pathlib import Path
import sys

from review import PACKET, RECEIPTS, SCRATCH, run

repo = Path(sys.argv[1] if len(sys.argv) > 1 else '.').resolve()
env = os.environ.copy()
env.update(TMPDIR=str(SCRATCH), PYTHONDONTWRITEBYTECODE='1')
ids = (repo/'scripts/check-ids.py').read_text()
fig = (repo/'scripts/check-figures.py').read_text()
cases = [
    ('minus-one', ids, '(token.endswith("-1") and token[:-2] in rows)', 'token.endswith("-1")', ['case 7']),
    ('optional-newline', ids, 'if optional:\n', 'if optional and "\\n" not in optional.group(0):\n', ['case 8', 'case 10']),
    ('foreign-object', fig, '("image", "feImage", "foreignObject")', '("image", "feImage")', ['case 8']),
    ('svg-root', fig, 'if svg.tag != f"{SVG_NS}svg":', 'if False:', ['case 9', 'case 10']),
    ('empty-inventory', fig, 'if not names:', 'if False:', ['case 12']),
    ('missing-inventory', fig, 'if at < 0:', 'if False:', ['case 13']),
]


def probe(case):
    name, source, old, new, diagnostics = case
    assert source.count(old) == 1, name
    script = SCRATCH/('prior-'+name+'.py')
    script.write_text(source.replace(old, new))
    out = run(repo, 'prior-'+name, [sys.executable, script, '--selftest'], env, 1)
    assert all(d in out for d in diagnostics), name
    return {'control': name, 'expected_rc': 1, 'observed_rc': 1,
            'diagnostics': diagnostics, 'verdict': 'KILLED'}


with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:
    results = list(pool.map(probe, cases))
(RECEIPTS/'prior-controls.json').write_text(json.dumps(results, indent=2)+'\n')
