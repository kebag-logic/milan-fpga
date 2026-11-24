"""Copy text evidence into bounded plain-text parts and index their original hashes."""
from pathlib import Path
import hashlib
import json
import subprocess

scratch = Path('/data-2/milan/tmp/opt-a837')
output = Path('$MANAGEMENT/2026-09-23/opt-a837/round1/receipts')
output.mkdir(parents=True, exist_ok=True)
LIMIT = 190000

def digest(data):
    return hashlib.sha256(data).hexdigest()

def copy(source, relative):
    data = source.read_bytes()
    data.decode('utf-8')
    dest = output / relative
    dest.parent.mkdir(parents=True, exist_ok=True)
    # Replace this source's generated snapshot, including a former unsplit copy or longer part series.
    for old in dest.parent.glob(dest.name + '.part*.txt'):
        old.unlink()
    if dest.exists():
        dest.unlink()
    parts = []
    if len(data) <= LIMIT:
        dest.write_bytes(data)
        parts.append(dest)
    else:
        # Split at whole lines so every part remains independently readable UTF-8.
        block = bytearray()
        for line in data.splitlines(keepends=True):
            if len(line) > LIMIT:
                raise ValueError(f'oversize single line: {source}')
            if len(block) + len(line) > LIMIT:
                part = dest.with_name(dest.name + f'.part{len(parts):03d}.txt')
                part.write_bytes(block)
                parts.append(part)
                block.clear()
            block.extend(line)
        if block:
            part = dest.with_name(dest.name + f'.part{len(parts):03d}.txt')
            part.write_bytes(block)
            parts.append(part)
    return {'source': str(source), 'bytes': len(data), 'sha256': digest(data),
            'parts': [str(p.relative_to(output)) for p in parts]}

sources = sorted(scratch.glob('*.log')) + sorted(scratch.glob('*.log.json'))
sources += sorted((scratch/'jobs').glob('*/results.json'))
sources += sorted((scratch/'jobs').glob('*/*.log')) + sorted((scratch/'jobs').glob('*/*.sh'))
sources += [p for p in (scratch/'builder-receipt.json', scratch/'litex-sim-logs/verdicts.tsv', scratch/'litex-timing-logs/verdicts.tsv', scratch/'input-equivalence.json', scratch/'gptp-placement-ruling.txt', scratch/'integration-overlap.json') if p.exists()]
scale_prefixes = ('scale-', 'scale32-', 'scale64-', 'onehart', 'twoharts')
manifest = [copy(p, Path('scale' if p.name.startswith(scale_prefixes) or p.name == 'gptp-placement-ruling.txt' else '966')/p.relative_to(scratch)) for p in sources]
for pattern in ('scale-model-conflicts.txt', 'scale/trace-controls.json', 'scale/elf-identities.json', 'scale/resource-check.json', 'scale/publication.json', 'scale/*/strict-grades.json', 'scale-input-equivalence.json', 'scale/*/maap-diagnostic.json', 'scale/*/group-grades/*-verdict.json', 'scale/*/early-srp/grade.json', 'scale/*/identity.json', 'scale/*/build.json', 'scale/64-preflight/*.log', 'scale/64-build-verdict.json',
                'scale/*-analysis.json', 'scale/*-memory.json', 'scale/cost-controls/test.cpp', 'scale/cost-controls/harts_cost.hpp',
                'scale-ports/sources.json'):
    for p in sorted(scratch.glob(pattern)):
        manifest.append(copy(p, Path('scale')/p.relative_to(scratch)))
for name in ('run.py','env.sh','workflow_steps.py','act-offline-step.sh','collect_receipts.py','review_evidence.py','docs_head.py','onehart_image.py','scale_analysis.py','cost_controls.py','scale_identity.py','first_group.py','live_grades.py','progress.py','scale_trace_controls.py','scale_strict_grades.py','write_scale_report.py','scale64-preflight.sh'):
    manifest.append(copy(scratch/name, Path('reproduce')/name))
(output/'SOURCES.json').write_text(json.dumps(manifest, indent=2)+'\n')
files = sorted(p for p in output.rglob('*') if p.is_file() and p.name != 'INDEX.md')
lines = ['# Receipts', '', 'Each file is plain text and smaller than 200 KB.',
         'SOURCES.json records whole-log hashes and the ordered parts needed to reconstruct large logs.', '',
         '| File | Bytes | SHA-256 |', '|---|---:|---|']
for p in files:
    data = p.read_bytes()
    assert len(data) < 200000, p
    assert p.suffix != '.gz', p
    relative = p.relative_to(output).as_posix()
    lines.append(f'| [{relative}]({relative}) | {len(data)} | `{digest(data)}` |')
(output/'INDEX.md').write_text('\n'.join(lines)+'\n')
print('indexed',len(files),'text receipts')
