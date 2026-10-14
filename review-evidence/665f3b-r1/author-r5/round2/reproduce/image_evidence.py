import os
import hashlib
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path.cwd() / 'sw/firmware/ctrl/test'))
import ctrl_image

work = Path(os.environ['WORK'])
output = Path(os.environ['PACKET']) / 'round2'
output.mkdir(exist_ok=True)
shapes = sorted(p.name for p in (work / 'images/head').iterdir() if p.is_dir())
tool = os.environ['MILAN_RV32_CC'].removesuffix('gcc')
rows = []
for composition, folder in [('ADP-ACMP-MAAP', work / 'images'),
                            ('SRP', work / 'composed-images/srp'),
                            ('SRP-AECP', work / 'composed-images/aecp')]:
    for shape in shapes:
        row = dict(composition=composition, shape=shape)
        for side in ('base', 'head'):
            path = folder / side / shape / 'ctrl_app.elf'
            if composition == 'ADP-ACMP-MAAP':
                sections = ctrl_image.section_sizes(tool, path)
            else:
                report = json.loads((path.parent / 'size.json').read_text())
                sections = {k.lstrip('.'): v for k, v in report['sections'].items()}
            data = path.read_bytes()
            row[side] = dict(sha256=hashlib.sha256(data).hexdigest(), size=len(data),
                             load=sum(sections.get(k, 0) for k in ('text', 'rodata', 'data')),
                             sections=sections)
        row['growth'] = row['head']['load'] - row['base']['load']
        rows.append(row)
assert len(rows) == 15
ceiling = 2048
def within(before, after):
    return after - before <= ceiling
assert all(within(r['base']['load'], r['head']['load']) for r in rows)
controls = dict(ceiling=ceiling, rows=len(rows), maximum_growth=max(r['growth'] for r in rows),
                boundary_2048_accepted=within(1000, 3048), boundary_2049_refused=not within(1000, 3049))
assert controls['boundary_2048_accepted'] and controls['boundary_2049_refused']
(output / 'image-hashes.json').write_text(json.dumps(rows, indent=2) + '\n')
(output / 'image-growth-controls.json').write_text(json.dumps(controls, indent=2) + '\n')
lines = ['| Composition / shape | Load before | Load after | Growth | ELF SHA-256 before | ELF SHA-256 after |',
         '|---|---:|---:|---:|---|---|']
for r in rows:
    lines.append(f"| {r['composition']} / `{r['shape']}` | {r['base']['load']} | {r['head']['load']} | +{r['growth']} | `{r['base']['sha256']}` | `{r['head']['sha256']}` |")
(output / 'image-table.md').write_text('\n'.join(lines) + '\n')
print(json.dumps(controls))
