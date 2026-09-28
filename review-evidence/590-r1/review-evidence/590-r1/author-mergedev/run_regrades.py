"""Re-run the round-3 kept-log service regrades, unchanged, at the merge head.

The round-3 build directories are only read: the harness compares its bound
build hashes before it writes anything, and the write check below proves that
no file under those directories changed during the run.
"""
from pathlib import Path
import hashlib
import json
import subprocess
import time

root = Path('$LANES/590-592-599-firmware')
out = Path(__file__).parent
round3 = Path('$MANAGEMENT/2026-09-23/590-a411')
builds = Path('$VALIDATION_STORAGE/590-a411')
assert Path.cwd() == root
head = subprocess.check_output(['git', 'rev-parse', 'HEAD'], text=True).strip()
assert not subprocess.check_output(['git', 'status', '--porcelain'], text=True).strip()
kept = json.loads((round3 / 'final-target-gates.json').read_text())
assert len(kept) == 15


def snapshot():
    """Size and modification time of every file in the round-3 service builds."""
    return {str(p): (p.stat().st_size, p.stat().st_mtime_ns)
            for p in sorted(builds.glob('service-*/**/*')) if p.is_file()}


before = snapshot()
results = []
for entry in kept:
    name, command = entry['name'], entry['command']
    assert command[-1] == '--regrade' and entry['rc'] == 0
    log = out / 'logs' / ('regrade-' + name + '.log')
    start = time.monotonic()
    with log.open('w') as stream:
        result = subprocess.run(command, cwd=root, stdout=stream, stderr=subprocess.STDOUT, timeout=3600)
    raw = log.read_bytes()
    results.append(dict(name=name, head=head, command=command, rc=result.returncode,
                        refusal='stale or unbound build; rebuild' in raw.decode(errors='replace'),
                        seconds=round(time.monotonic() - start, 3), path=str(log.relative_to(out)),
                        size=len(raw), sha256=hashlib.sha256(raw).hexdigest()))
    (out / 'regrade-gates.json').write_text(json.dumps(results, indent=2) + '\n')
    print(name, 'rc', result.returncode, 'refusal', results[-1]['refusal'], flush=True)
after = snapshot()
assert before == after, 'a round-3 build file changed'
print('round-3 build files unchanged:', len(after))
assert subprocess.check_output(['git', 'rev-parse', 'HEAD'], text=True).strip() == head
assert not subprocess.check_output(['git', 'status', '--porcelain'], text=True).strip()
failed = [r['name'] for r in results if r['rc'] != 0]
print('FAILED: ' + ', '.join(failed) if failed else 'PASS: all kept service logs regraded at ' + head)
