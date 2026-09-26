import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import sys
import time

from run_gate import ENV, OUT, ROOT

SUITE = ROOT / 'tb/verilator/milan_dp'
sys.path.insert(0, str(SUITE))
from test_sim_pool import LEGACY_LEGS

AUDIT = OUT / 'write-audit'
AUDIT.mkdir(exist_ok=True)
PRIVATE = Path('/tmp/517-a324-write-audit')
PRIVATE.mkdir(exist_ok=True)

def snapshot(root):
    result = {}
    for directory, dirs, files in os.walk(root):
        dirs[:] = [d for d in dirs if d != '.git']
        for name in files:
            path = Path(directory) / name
            try:
                st = path.stat()
                result[str(path.relative_to(root))] = [st.st_mtime_ns, st.st_ctime_ns, st.st_size]
            except FileNotFoundError:
                pass
    return result

rows = []
for _banner, exe in LEGACY_LEGS:
    name = Path(exe).parent.name
    where = AUDIT / name
    where.mkdir(exist_ok=True)
    private = PRIVATE / name
    private.mkdir(exist_ok=True)
    env = dict(ENV, TMPDIR=str(private))
    env.pop('PYTHONDONTWRITEBYTECODE', None)
    before = snapshot(ROOT)
    (where / 'tree-before.json').write_text(json.dumps(before, indent=1)+'\n')
    observed = {}
    argv = ['strace', '-f', '-qq', '-ttt', '-y', '-s', '4096',
            '-e', 'trace=%file', '-e', 'inject=unlink:delay_enter=100ms',
            '-e', 'inject=unlinkat:delay_enter=100ms', '-e', 'inject=rmdir:delay_enter=100ms',
            '-o', str(where / 'files.trace'), exe]
    start = time.time()
    with (where / 'leg.log').open('wb') as log:
        proc = subprocess.Popen(argv, cwd=SUITE, env=env, stdout=log, stderr=subprocess.STDOUT)
        while proc.poll() is None:
            for path, metadata in snapshot(private).items():
                versions = observed.setdefault(path, [])
                if not versions or versions[-1] != metadata:
                    versions.append(metadata)
            time.sleep(0.025)
        rc = proc.wait()
    after = snapshot(ROOT)
    changed = {p: {'before': before.get(p), 'after': after.get(p)}
               for p in before.keys() | after.keys() if before.get(p) != after.get(p)}
    (where / 'tree-changed.json').write_text(json.dumps(changed, indent=1)+'\n')
    (where / 'private-timestamps.json').write_text(json.dumps(observed, indent=1)+'\n')
    trace = (where / 'files.trace').read_text()
    writes = [line for line in trace.splitlines()
              if re.search(r'O_WRONLY|O_RDWR|creat\(|mkdir|rename|unlink|rmdir', line)]
    (where / 'writes.trace').write_text('\n'.join(writes)+'\n')
    row = dict(leg=name, exit=rc, seconds=round(time.time()-start, 3),
               tree_changes=list(changed), private_files=sorted(observed),
               trace_writes=len(writes))
    rows.append(row)
    (AUDIT / 'summary.json').write_text(json.dumps(rows, indent=1)+'\n')
    print(json.dumps(row), flush=True)
    assert rc == 0, name
# Same-byte write control: the timestamp observer must still report it.
control = PRIVATE / 'positive-control'
control.write_bytes(b'unchanged bytes\n')
before = snapshot(PRIVATE)
time.sleep(0.025)
control.write_bytes(control.read_bytes())
after = snapshot(PRIVATE)
assert before['positive-control'] != after['positive-control']
(AUDIT / 'positive-control.json').write_text(json.dumps(dict(
    before=before['positive-control'], after=after['positive-control'],
    same_bytes=True, detected=True), indent=1)+'\n')
print('Private same-byte timestamp positive control: PASS', flush=True)
