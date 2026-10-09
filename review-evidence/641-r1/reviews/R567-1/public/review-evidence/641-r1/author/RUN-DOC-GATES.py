#!/usr/bin/env python3
"""Replay the assigned documentation and script gates from the repository root."""
import json
import os
from pathlib import Path
import subprocess

here = Path(__file__).resolve().parent
out = Path(os.environ['WORK']) / 'docs-replay'
out.mkdir(parents=True, exist_ok=True)
rows = []
for name, argv, options in json.loads((here / 'DOC-GATES.json').read_text()):
    argv = [os.environ['MD_PYTHON'] if value == '$MD_PYTHON' else value for value in argv]
    env = dict(os.environ, **options.get('env', {}))
    with (out / (name + '.log')).open('w') as log:
        result = subprocess.run(argv, env=env, stdout=log, stderr=subprocess.STDOUT, check=False)
    rows.append(dict(name=name, rc=result.returncode))
    print(name, result.returncode, flush=True)
    (out / 'results.json').write_text(json.dumps(rows, indent=2) + '\n')
raise SystemExit(int(any(row['rc'] for row in rows)))
