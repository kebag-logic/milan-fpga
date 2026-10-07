from pathlib import Path
import hashlib
import json
import os
import subprocess

w = Path(__file__).resolve().parents[1]
repo = Path('$LANES/645-ring-slip')
out = w/'resume/final-source-k'
out.mkdir(exist_ok=True)
head = subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=repo, text=True).strip()
previous = '132d79e7f38212cedf0e344a39d0f811566a1d1b'
delta = subprocess.check_output(['git', 'diff', '--name-status', previous, head], cwd=repo, text=True)
assert delta == 'M\tdocs/design/MEDIA_CLOCK_FOLLOWING.md\nA\tdocs/findings/667_TALKER_START_BENCH.md\n', delta
admission = []
for name in ['protocol-processor', 'gptp-processor', 'third_party/verilog-axis']:
    path = repo/name
    root = subprocess.check_output(['git', '-C', str(path), 'rev-parse', '--show-toplevel'], text=True).strip()
    assert Path(root).resolve() == path.resolve(), (name, root)
    revision = subprocess.check_output(['git', '-C', str(path), 'rev-parse', 'HEAD'], text=True).strip()
    admission.append(dict(path=name, root_verified=True, head=revision))
proof = dict(head=head, measurement_head=previous,
    diff=delta, note='Only the merged findings document and the design-document '
    'measurement statement differ. All other tracked files, submodule entries and executable inputs are byte-identical. '
    'Running regressions remain at the recorded measurement head; their '
    'claims carry forward through this explicit input-identity proof.',
    tree_diff_sha256=hashlib.sha256(subprocess.check_output(
        ['git', 'diff', previous, head], cwd=repo)).hexdigest(),
    dependencies=admission)
(w/'resume/final-doc-identity-k.json').write_text(json.dumps(proof, indent=2)+'\n')
e=os.environ.copy()
e.update(PYTHONDONTWRITEBYTECODE='1', TMPDIR=str(w/'tmp'))
e['PATH']='$VALIDATION_TOOLS/pinned-verilator-5.050:'+e['PATH']
rows=[]
for row in json.loads((w/'resume/merge-final-source/commands.json').read_text())['commands']:
    name, argv = row['name'], row['argv']
    with (out/(name+'.log')).open('w') as stream:
        rc = subprocess.run(argv, cwd=repo, env=e, stdout=stream, stderr=subprocess.STDOUT).returncode
    (out/(name+'.rc')).write_text(str(rc)+'\n')
    rows.append(dict(name=name, argv=argv, rc=rc))
    (out/'commands.json').write_text(json.dumps(dict(head=head, commands=rows), indent=2)+'\n')
    print(name, rc, flush=True)
rc=int(any(row['rc'] for row in rows))
(out/'all.rc').write_text(str(rc)+'\n')
raise SystemExit(rc)
