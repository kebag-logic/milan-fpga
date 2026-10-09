#!/usr/bin/env python3
"""Copy publishable receipts from scratch into receipts/ with host paths redacted; write MANIFEST.sha256."""
import hashlib, pathlib, shutil, sys
packet = pathlib.Path(sys.argv[1]).resolve(); clone = sys.argv[2]
home = str(pathlib.Path.home())
subs = [(str(packet), '$PACKET'), (clone, '$HEAD_CLONE'), (home, '$HOME')]
def redact(src, dst):
    dst.parent.mkdir(parents=True, exist_ok=True)
    data = src.read_bytes()
    try:
        text = data.decode()
    except UnicodeDecodeError:
        return
    for old, new in subs:
        text = text.replace(old, new)
    dst.write_text(text)
s = packet / 'scratch'; r = packet / 'receipts'
pairs = []
v = s / 'validate'
for name in ['gates.json', 'mutations/results.json', 'mutations/message-markers.json']:
    pairs.append((v / name, r / 'validate' / name))
for log in sorted(v.glob('*.log')) + sorted(v.glob('*.rc')):
    pairs.append((log, r / 'validate' / log.name))
for log in sorted((v / 'assertion-templates').glob('*.log')):
    pairs.append((log, r / 'validate/assertion-templates' / log.name))
for log in sorted((v / 'dependency-controls').glob('*.log')):
    pairs.append((log, r / 'validate/dependency-controls' / log.name))
pairs.append((s / 'rv32/results.json', r / 'rv32/results.json'))
for cfg in ('debug', 'release'):
    for name in ('build.log', 'smoke.log', 'CMakeFiles/rv32_smoke.dir/link.txt'):
        pairs.append((s / 'rv32' / cfg / name, r / 'rv32' / cfg / name.replace('CMakeFiles/rv32_smoke.dir/', '')))
p8 = s / 'r556-8-probes'
for f in sorted(p8.glob('*.json')) + sorted(p8.glob('*.log')):
    pairs.append((f, r / 'r556-8-probes' / f.name))
rp = s / 'replays'
for f in sorted(rp.glob('*.log')) + sorted(rp.glob('*.rc')) + [rp / 'results.json', rp / 'r5566/probes.json']:
    pairs.append((f, r / 'public-replay' / f.relative_to(rp)))
for f in sorted((s / 'package-prefix-probe').glob('*.log')) + sorted((s / 'package-prefix-probe').glob('*.rc')) + \
        [s / 'package-prefix-probe/results.json', s / 'package-prefix-probe/flags.txt']:
    pairs.append((f, r / 'r557-7-package-prefix' / f.name))
for f in ['hosted-checks.txt', 'hosted-runs.json', 'environment.json', 'setup_sdk.log']:
    pairs.append((s / f, r / f))
for run in ('37925745383', '37925739153'):
    q = s / 'hosted' / run
    for name in ['quality-evidence/gates.json', 'quality-evidence/mutations/results.json',
                 'quality-evidence/assertion-templates.log', 'quality-evidence/dependencies.log', 'rv32-evidence/results.json']:
        pairs.append((q / name, r / 'hosted' / run / name))
for src, dst in pairs:
    if src.is_file():
        redact(src, dst)
    else:
        print('missing', src)
for f in sorted(r.rglob('*')):
    if f.is_file():
        redact(f, f)
rows = []
for f in sorted(list(r.rglob('*')) + list((packet / 'scripts').rglob('*')) + list((packet / 'prior-probes').rglob('*'))):
    if f.is_file():
        rows.append(hashlib.sha256(f.read_bytes()).hexdigest() + '  ' + str(f.relative_to(packet)))
(packet / 'MANIFEST.sha256').write_text('\n'.join(rows) + '\n')
print(len(rows), 'files listed')
