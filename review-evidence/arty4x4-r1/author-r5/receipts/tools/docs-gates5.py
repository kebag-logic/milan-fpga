"""The docs workflow's checks that need no runner state, each logged, run in the checkout at its head.
usage: docs-gates4.py (cwd = checkout root)"""
import json, os, re, shlex, subprocess, sys
from pathlib import Path
R = Path('$VALIDATION_STORAGE/arty4x4-a863/gates5/docs'); R.mkdir(parents=True, exist_ok=True)
SKIP = re.compile(r'\\$|gen_hdl_reference|RUNNER_TEMP|install_dir|ci_fail_fast\.py (watch|cancel|tail)|test_builder\.py|--with-submodule')
cmds = [c for c in Path('$VALIDATION_STORAGE/arty4x4-a863/tools/docs-cmds.txt').read_text().splitlines()
        if c and not SKIP.search(c)]
env = dict(os.environ, PYTHONDONTWRITEBYTECODE='1', TMPDIR='$VALIDATION_STORAGE/arty4x4-a863/work-tmp')
head = subprocess.check_output(['git', 'rev-parse', 'HEAD'], text=True).strip()
rows = []
for k, c in enumerate(cmds):
    argv = shlex.split(c)
    with (R / f'{k:03d}.log').open('w') as log:
        rc = subprocess.run(['nice', '-n', '19', *argv], env=env, stdout=log, stderr=subprocess.STDOUT).returncode
    rows.append(dict(n=k, command=c, returncode=rc))
    print(rc, c, flush=True)
(R / 'results.json').write_text(json.dumps(dict(head=head, rows=rows), indent=2) + '\n')
bad = [r for r in rows if r['returncode']]
print('DOCS', 'PASS' if not bad else 'FAIL', head, len(rows), 'commands', len(bad), 'failed', flush=True)
raise SystemExit(1 if bad else 0)
