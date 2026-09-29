"""Re-run the unchanged reviewer probes and the product link guard at the current head."""
from pathlib import Path
import hashlib
import json
import subprocess
import time

out = Path(__file__).parent
root = Path('$LANES/590-592-599-firmware')
assert Path.cwd() == root
head = subprocess.check_output(['git', 'rev-parse', 'HEAD'], text=True).strip()
assert not subprocess.check_output(['git', 'status', '--porcelain'], text=True).strip()
tmp = Path('$VALIDATION_STORAGE/590-a430/probes')
r368 = Path('$REVIEWS/590-r368-2-packet/probes')
r369 = Path('$REVIEWS/590-r369-2-packet/scripts')
# name, argv, expected raw rc, text every passing log must contain (as in round 3)
probes = [
    ('phase-probe', ['python3', '-B', str(r369 / 'probe_mdio_phase.py'), str(root), str(tmp / 'phase')], 0,
     'PHASE=1 published link_status=13'),
    ('disabled-writer-probe', ['python3', '-B', str(r368 / 'disabled_writer_probe.py'), str(root), str(tmp / 'disabled')], 0,
     'fw=head             plant=csr-id-mismatch line=empty-line   disabled_msg=1 hb=0 backed=0 stale=0'),
    ('dispatch-oracle-probe', ['python3', '-B', str(r369 / 'builtin_oracle_probe.py'), str(root)], 0,
     "plan=queued-builtins tick_calls=0 findings=['console line lacks a dispatch opportunity: ']"),
    ('edge-cross', ['python3', '-B', str(r368 / 'host_mutant2.py'), str(root), 'edge-cross'], 1,
     'MUTANT edge-cross: KILLED'),
    ('product-link-guard', ['python3', '-B', str(out / 'product_link_guard.py')], 0,
     'PASS: actual RV32 BIOS links with marker; missing marker fails by name'),
]
results = []
for name, argv, expected, marker in probes:
    log = out / 'logs' / ('probe-' + name + '.log')
    start = time.monotonic()
    with log.open('w') as stream:
        result = subprocess.run(['timeout', '1800', *argv], stdout=stream, stderr=subprocess.STDOUT, cwd=root)
    raw = log.read_bytes()
    graded = 0 if result.returncode == expected and marker in raw.decode() else 1
    results.append(dict(name=name, head=head, command=argv, raw_rc=result.returncode,
                        expected_rc=expected, rc=graded, seconds=round(time.monotonic() - start, 3),
                        path=str(log.relative_to(out)), size=len(raw), sha256=hashlib.sha256(raw).hexdigest()))
    (out / 'probes.json').write_text(json.dumps(results, indent=2) + '\n')
    print(name, 'raw rc', result.returncode, 'graded rc', graded, flush=True)
assert subprocess.check_output(['git', 'rev-parse', 'HEAD'], text=True).strip() == head
assert not subprocess.check_output(['git', 'status', '--porcelain'], text=True).strip()
failed = [r['name'] for r in results if r['rc'] != 0]
print('FAILED: ' + ', '.join(failed) if failed else 'PASS: current-head probes')
