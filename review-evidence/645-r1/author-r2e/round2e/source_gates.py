"""The 28 source and docs gates of round 2c, rerun at this lane's tree.

  python3 -B source_gates.py OUT_NAME
Each command keeps its own log and rc under round2d/OUT_NAME; all.rc is 0 only
when every command exits 0. Runs in the lane checkout (cwd), never piped.
"""
from pathlib import Path
import json
import os
import subprocess
import sys

w = Path(__file__).resolve().parent
repo = Path('$REPO')
out = w / sys.argv[1]
out.mkdir(exist_ok=True)
head = subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=repo, text=True).strip()
dirty = subprocess.check_output(['git', 'status', '--porcelain'], cwd=repo, text=True)
admission = []
for name in ['protocol-processor', 'gptp-processor', 'third_party/verilog-axis']:
    path = repo / name
    root = subprocess.check_output(['git', '-C', str(path), 'rev-parse', '--show-toplevel'], text=True).strip()
    assert Path(root).resolve() == path.resolve(), (name, root)
    admission.append(dict(path=name, root_verified=True,
                          head=subprocess.check_output(['git', '-C', str(path), 'rev-parse', 'HEAD'], text=True).strip()))
e = os.environ.copy()
e.update(PYTHONDONTWRITEBYTECODE='1', TMPDIR=str(w / 'tmp'))
e['PATH'] = '$VALIDATION_TOOLS/pinned-verilator-5.050:' + e['PATH']
spec = json.loads((w.parent / 'round2c/resume/merge-final-source/commands.json').read_text())['commands']
rows = []
for row in spec:
    name, argv = row['name'], row['argv']
    with (out / (name + '.log')).open('w') as stream:
        rc = subprocess.run(argv, cwd=repo, env=e, stdout=stream, stderr=subprocess.STDOUT).returncode
    (out / (name + '.rc')).write_text(str(rc) + '\n')
    rows.append(dict(name=name, argv=argv, rc=rc))
    (out / 'commands.json').write_text(json.dumps(dict(head=head, worktree_dirty=dirty, dependencies=admission,
                                                       commands=rows), indent=2) + '\n')
    print(name, rc, flush=True)
rc = int(any(row['rc'] for row in rows))
(out / 'all.rc').write_text(str(rc) + '\n')
raise SystemExit(rc)
