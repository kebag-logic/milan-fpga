#!/usr/bin/env python3
"""P1 and boundary probes in a disposable exact-head source extraction."""
from pathlib import Path
import io
import subprocess
import sys
import tarfile

repo = Path(sys.argv[1]).resolve()
scratch = Path(__file__).resolve().parent / 'scratch/margins'
scratch.mkdir(parents=True, exist_ok=True)
data = subprocess.check_output(['git', '-C', str(repo), 'archive', 'HEAD', 'sw/mailbox', 'docs/reference', 'hdl/milan/mailbox', 'sw/firmware/ctrl/mbx'])
with tarfile.open(fileobj=io.BytesIO(data)) as archive:
    archive.extractall(scratch, filter='data')
def run(*args, expected=0):
    proc = subprocess.run([sys.executable, '-B', 'sw/mailbox/gen_mailbox.py', *args], cwd=scratch, text=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    print('COMMAND gen_mailbox.py', *args, 'rc', proc.returncode)
    print(proc.stdout)
    assert proc.returncode == expected
    return proc.stdout
page = scratch / 'docs/reference/FR_NFR.md'
original = page.read_text()
run('--check', '--crosscheck')
yaml = scratch / 'sw/mailbox/mailbox.yaml'
text = yaml.read_text()
start = text.index('name: aecp')
pos = text.index('refill_ms: 5', start)
yaml.write_text(text[:pos] + text[pos:].replace('refill_ms: 5', 'refill_ms: 10', 1))
out = run('--check', expected=1)
assert sum('FR_NFR.md:' in line and "'AECP" in line for line in out.splitlines()) == 3
run('--write')
run('--check', '--crosscheck')
rows = [x for x in page.read_text().splitlines() if '| `aecp` |' in x and x.startswith('| AECP')]
assert len(rows) == 3
for row, margin in zip(rows, (208, 218, 208)):
    cells = [x.strip() for x in row.strip('|').split('|')]
    assert cells[8] == '11 ms' and cells[9] == f'{margin} ms'
    print('P1 REGENERATED', row)
acmp = lambda s: [x for x in s.splitlines() if x.startswith('| ACMP command to its response')]
assert acmp(page.read_text()) == acmp(original)
print('P1 ACMP unchanged: PASS')
for mode in ('hand-edit', 'zero-margin', 'negative-margin'):
    page.write_text(original)
    yaml.write_text(text)
    run('--write')
    if mode == 'hand-edit':
        page.write_text(original.replace('| 213 ms | 223 ms |', '| 214 ms | 223 ms |', 1))
    else:
        page.write_text(original.replace('| `acmp` | 200 ms | 20 ms |', '| `acmp` | ' + ('27' if mode == 'zero-margin' else '26') + ' ms | 20 ms |', 1))
        run('--write')
    out = run('--check', expected=1)
    assert ('reads' if mode == 'hand-edit' else 'leaves no margin') in out
    print(mode, 'PASS')
