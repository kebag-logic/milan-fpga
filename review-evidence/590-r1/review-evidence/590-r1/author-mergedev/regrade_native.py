"""Restore this round's retained service evidence, then regrade all 15 runs at the head.

The raw log and receipt of each run are rebuilt from `native-evidence/`
(checked against their stored and raw SHA-256 and size) and written back into
the run's build directory, so the regrade grades the retained bytes.
"""
from pathlib import Path
import gzip
import hashlib
import json
import subprocess
import time

out = Path(__file__).parent
root = Path('$LANES/590-592-599-firmware')
scratch = Path('$VALIDATION_STORAGE/590-a422/native')
assert Path.cwd() == root
head = subprocess.check_output(['git', 'rev-parse', 'HEAD'], text=True).strip()
assert not subprocess.check_output(['git', 'status', '--porcelain'], text=True).strip()
artifacts = json.loads((out / 'native-artifacts.json').read_text())
commands = json.loads((out / 'native-commands.json').read_text())
results = []


def restore(name, destination):
    matches = [item for item in artifacts if item['name'] in (name, name + '.gz')]
    assert len(matches) == 1, (name, len(matches))
    item = matches[0]
    parts = []
    for part in item['stored']:
        raw = (out / part['path']).read_bytes()
        assert len(raw) == part['size'] and hashlib.sha256(raw).hexdigest() == part['sha256']
        parts.append(raw)
    raw = b''.join(parts)
    if item['name'].endswith('.gz'):
        raw = gzip.decompress(raw)
    assert len(raw) == item['raw_size'] and hashlib.sha256(raw).hexdigest() == item['raw_sha256']
    matched = destination.read_bytes() == raw
    destination.write_bytes(raw)
    return matched


runs = [entry for entry in commands if entry['name'].startswith('service-')
        and not entry['name'].startswith('service-no-publish')]
assert len(runs) == 15 and all(entry['rc'] == 0 and entry['head'] == head for entry in runs)
for entry in sorted(runs, key=lambda item: item['name']):
    name = entry['name']
    args = entry['command']
    directory = Path(args[args.index('--build-dir') + 1])
    plan = args[args.index('--plan') + 1]
    waits = '3000000-5000' if plan == 'device-wait' else '0-0'
    stem = 'service-' + plan + '-1-' + waits
    matched = [restore(name + '-raw.log', directory / (stem + '.log')),
               restore(name + '-receipt.json', directory / (stem + '.json'))]
    log = scratch / ('final-regrade-' + name + '.log')
    command = args + ['--regrade']
    started = time.monotonic()
    with log.open('w') as stream:
        result = subprocess.run(command, cwd=root, stdout=stream, stderr=subprocess.STDOUT, timeout=3600)
    raw = log.read_bytes()
    body = gzip.compress(raw, mtime=0) if len(raw) > 200000 else raw
    assert len(body) <= 200000, log
    stored = out / 'logs' / (log.name + ('.gz' if len(raw) > 200000 else ''))
    stored.write_bytes(body)
    results.append(dict(name=name, head=head, command=command, rc=result.returncode,
                        build_copy_matched_retained=dict(raw_log=matched[0], receipt=matched[1]),
                        seconds=round(time.monotonic() - started, 3), path=str(stored.relative_to(out)),
                        stored_size=len(body), stored_sha256=hashlib.sha256(body).hexdigest(),
                        size=len(raw), sha256=hashlib.sha256(raw).hexdigest()))
    (out / 'native-regrades.json').write_text(json.dumps(results, indent=2) + '\n')
    print(name, 'rc', result.returncode, flush=True)
assert subprocess.check_output(['git', 'rev-parse', 'HEAD'], text=True).strip() == head
assert not subprocess.check_output(['git', 'status', '--porcelain'], text=True).strip()
failed = [r['name'] for r in results if r['rc'] != 0]
print('FAILED: ' + ', '.join(failed) if failed else 'PASS: all 15 retained service runs regraded at ' + head)
