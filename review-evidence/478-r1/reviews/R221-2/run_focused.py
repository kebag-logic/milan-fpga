import hashlib
import io
import json
import os
from pathlib import Path
import subprocess
import sys
import tarfile
import tempfile

root, out = Path(sys.argv[1]).resolve(), Path(sys.argv[2]).resolve()
out.mkdir(parents=True, exist_ok=True)
worker = Path(__file__).with_name('focused_worker.py')
head = '1496558d82cf35fc98dda0e781b2a1be643c301a'
original_base = 'b17580b91deb11f3441dfc5d7f9fafe539d929b8'
integrated_base = '88e9276b2a220c716f64a843f7e1eb8f9265e896'
def git(repo, *args):
    return subprocess.check_output(['rtk', 'proxy', 'git', '-C', str(repo), *args],
                                   env={**os.environ, 'GIT_NO_REPLACE_OBJECTS':'1'})
def export(repo, ref, dest):
    dest.mkdir(parents=True, exist_ok=True)
    data = git(repo, 'archive', ref)
    with tarfile.open(fileobj=io.BytesIO(data)) as archive:
        archive.extractall(dest, filter='data')

receipts = []
with tempfile.TemporaryDirectory(prefix='r221-focused-') as scratch:
    for rev, mode in [(head, 'focused'), (original_base, 'images'), (integrated_base, 'images')]:
        dest = Path(scratch) / rev[:8]
        export(root, rev, dest)
        pins = {}
        for sub in ['protocol-processor', 'gptp-processor', 'third_party/verilog-axis']:
            pin = git(root, 'rev-parse', rev + ':' + sub).decode().strip()
            pins[sub] = pin
            export(root / sub, pin, dest / sub)
        rec = out / rev[:8]
        rec.mkdir()
        cmd = ['rtk', 'proxy', 'python3', '-B', str(worker), str(dest), str(rec), mode]
        with (rec / 'focused.log').open('w') as log:
            result = subprocess.run(cmd, cwd=dest, stdout=log, stderr=subprocess.STDOUT,
                                    env={**os.environ, 'PYTHONDONTWRITEBYTECODE':'1', 'MAKEFLAGS':'-j8'})
        receipts.append(dict(head=rev,mode=mode,exit=result.returncode,submodules=pins))
        (out / 'execution.json').write_text(json.dumps(receipts, indent=2) + '\n')
        assert result.returncode == 0, (rev, result.returncode, str(rec / 'focused.log'))
    current = json.loads((out / head[:8] / 'images.json').read_text())
    for rev in [original_base, integrated_base]:
        other = json.loads((out / rev[:8] / 'images.json').read_text())
        assert current == other
        for name in current:
            assert (out / head[:8] / (name + '.bin')).read_bytes() == (out / rev[:8] / (name + '.bin')).read_bytes()
    assert len({json.dumps(x['submodules'],sort_keys=True) for x in receipts}) == 1
    (out / 'comparison.json').write_text(json.dumps(dict(head=head, baselines=[original_base,integrated_base],
        byte_equal=True, pins_unchanged=True, images=current), indent=2) + '\n')
print('PASS: focused controls; five complete images byte-identical to both baselines; pins unchanged')
