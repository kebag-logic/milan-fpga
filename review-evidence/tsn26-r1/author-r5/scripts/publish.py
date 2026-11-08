# SPDX-License-Identifier: MIT
# usage: publish.py OUT_DIR
# Copies the round 5 receipts, map and scripts from scratch into OUT_DIR. Host paths are replaced by
# <clone>, <scratch>, <reviews>, <tools> and <lane>. Files over 200 KB are not copied; their sha256 and size are
# recorded instead. Refuses to write a file that still names a host path.
import hashlib, json, shutil, sys
from pathlib import Path
S = Path('<scratch>')
OUT = Path(sys.argv[1])
SUBS = [('<clone>', '<clone>'), ('<scratch>', '<scratch>'),
        ('<reviews>', '<reviews>'), ('<tools>', '<tools>'),
        ('<lane>', '<lane>')]
LIMIT = 200 * 1024
skipped = []


def put(src, dst):
    src, dst = Path(src), OUT / dst
    data = src.read_bytes()
    if len(data) > LIMIT:
        skipped.append(f'{hashlib.sha256(data).hexdigest()}  {len(data)}  {dst.relative_to(OUT)}')
        return
    text = data.decode()
    for a, b in SUBS:
        text = text.replace(a, b)
    for bad in ('/ho' + 'me/', '/da' + 'ta/', 'al' + 'ex'):
        assert bad not in text, (str(src), bad)
    dst.parent.mkdir(parents=True, exist_ok=True)
    dst.write_text(text)


V = S / 'val-final'
for log in sorted(V.glob('*.log')):
    put(log, 'receipts/final/' + log.name)
for rc in sorted(V.glob('*.rc')):
    put(rc, 'receipts/final/' + rc.name)
put(V / 'gates.json', 'receipts/final/gates.json')
put(S / 'val-final.log', 'receipts/final/validate.log')
put(S / 'val-final.rc', 'receipts/final/validate.rc')
put(S / 'rv32-final.log', 'receipts/final/baremetal.log')
put(S / 'rv32-final.rc', 'receipts/final/baremetal.rc')
put(S / 'rv32-final/results.json', 'receipts/final/rv32-results.json')
put(S / 'gates-final.head', 'receipts/final/head.txt')
for n in ('status', 'status-after', 'diffsha', 'diffsha-after'):
    put(S / f'gates-final.{n}', f'receipts/final/clone-{n}.txt')
res = json.loads((V / 'mutations/results.json').read_text())
summary = [{'name': r['name'], 'status': r['status'], 'failing_tests': sorted(r.get('failures') or {})} for r in res]
(OUT / 'receipts/final/campaign-summary.json').write_text(json.dumps(summary, indent=1) + '\n')
put(V / 'mutations/results.json', 'receipts/final/campaign-results.json')
for step in ('s1', 's2', 's3', 's4'):
    put(S / f'val-{step}.log', f'receipts/steps/{step}-validate.log')
    put(S / f'val-{step}.rc', f'receipts/steps/{step}-validate.rc')
    put(S / f'rv32-{step}.log', f'receipts/steps/{step}-baremetal.log')
    put(S / f'rv32-{step}.rc', f'receipts/steps/{step}-baremetal.rc')
    if (S / f'val-{step}/gates.json').exists():
        put(S / f'val-{step}/gates.json', f'receipts/steps/{step}-gates.json')
        put(S / f'val-{step}/mutation.log', f'receipts/steps/{step}-mutation.log')
    for n in ('head', 'status', 'status-after', 'diffsha', 'diffsha-after'):
        put(S / f'gates-{step}.{n}', f'receipts/steps/{step}-{n}.txt')
put(S / 'escape-final.json', 'receipts/escape-final.json')
put(S / 'escape-final.txt', 'receipts/escape-final.txt')
put(S / 'per-test-escape.json', 'receipts/per-test-escape.json')
put(S / 'sizes-and-images.txt', 'receipts/sizes-and-images.txt')
for f in ('probe-r4-r4b.txt', 'probe-r4c.txt', 'probe-owed6.txt', 'inputs.sha256'):
    put(S / 'probes' / f, 'receipts/probes/' + f)
for f in ('r793-reviewer-plants.txt', 'r794-escape-check4.txt', 'r794-escape-check4.log'):
    put(S / 'rev' / f, 'receipts/reviewer-scripts/' + f)
for f in ('sentence_map.py', 'check_map.py', 'check-final.txt', 'map-final.md'):
    put(S / 'map' / f, 'map/' + f)
for f in ('run_step.sh', 'run_final.sh', 'cand_plants.py', 'escape5.py', 'per_test_escape5.py', 'imgx.sh', 'imgsize.sh',
          'pr_body5.py', 'publish.py'):
    put(S / 'scripts' / f, 'scripts/' + f)
put(S / 'cand2.json', 'scripts/candidate-plant-seven-owed.json')
put(S / 'cand3.json', 'scripts/candidate-plant-answer.json')
(OUT / 'receipts/not-copied.sha256.txt').write_text('# sha256  bytes  path (over 200 KB, not copied)\n' +
                                                   '\n'.join(skipped) + '\n')
print('\n'.join(skipped))
