#!/usr/bin/env python3
"""Read-only focused gates for R219-3; full stdout and status retained."""
from concurrent.futures import ThreadPoolExecutor
import datetime
import json
from pathlib import Path
import subprocess

OUT = Path(__file__).resolve().parent
ROOT = Path('$VALIDATION_STORAGE/reviews/r219-505-r3')
BASE = 'b17580b91deb11f3441dfc5d7f9fafe539d929b8'
commands = {
    'ci-check': ['python3', '-B', 'scripts/ci_events.py', '--check'],
    'ci-selftest': ['python3', '-B', 'scripts/ci_events.py', '--selftest'],
    'docs-check': ['python3', '-B', 'scripts/docs_check.py'],
    'toc-check': ['python3', '-B', 'scripts/gen_toc.py', '--check'],
    'doc-paths': ['python3', '-B', 'scripts/check_doc_paths.py'],
    'em-dash': ['python3', '-B', 'scripts/check_em_dash.py', '--base', BASE],
    'diff-check': ['git', 'diff', '--check', BASE, 'HEAD'],
}

def run(item):
    name, args = item
    argv = ['rtk', 'proxy', *args]
    begin = datetime.datetime.now(datetime.timezone.utc).isoformat()
    p = subprocess.run(argv, cwd=ROOT, text=True, capture_output=True)
    dest = OUT / 'gates'
    dest.mkdir(exist_ok=True)
    (dest / f'{name}.stdout.log').write_text(p.stdout)
    (dest / f'{name}.stderr.log').write_text(p.stderr)
    result = {'name': name, 'argv': argv, 'cwd': str(ROOT),
              'started_utc': begin, 'exit': p.returncode,
              'finished_utc': datetime.datetime.now(datetime.timezone.utc).isoformat()}
    (dest / f'{name}.json').write_text(json.dumps(result, indent=2) + '\n')
    print(f'{name}: exit {p.returncode}; {p.stdout.splitlines()[-1:]!r}', flush=True)
    return result

with ThreadPoolExecutor(max_workers=4) as pool:
    results = list(pool.map(run, commands.items()))
assert all(r['exit'] == 0 for r in results), results
