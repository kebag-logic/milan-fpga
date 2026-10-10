"""Compare differing exported objects, archives and ELFs with debug sections stripped (scratch tool).

Usage: python3 strip_compare.py SIDE_A SIDE_B COMPARE_JSON
"""
import json, subprocess, sys, tempfile
from pathlib import Path
ROOT = Path('$SCRATCH')
SDK = Path('$SDK/bin')
a, b, report = sys.argv[1], sys.argv[2], json.loads(Path(sys.argv[3]).read_text())

def stripped(side, path, work):
    out = work / (side + '-' + path.name)
    subprocess.run([str(SDK / 'riscv32-linux-objcopy'), '--strip-debug', str(path), str(out)], check=True)
    if path.suffix == '.a':
        # Archive member headers carry mtimes; compare members, not the container.
        members = work / (side + '-members-' + path.name)
        members.mkdir()
        subprocess.run([str(SDK / 'riscv32-linux-ar'), 'x', str(out)], cwd=members, check=True)
        return {m.name: m.read_bytes() for m in sorted(members.iterdir())}
    return out.read_bytes()

def norm(side, data):
    if isinstance(data, dict):
        return {norm(side, k.encode()).decode(): norm(side, v) for k, v in data.items()}
    for old in (f'{ROOT}/exp-{side}', f'{ROOT}/res/{side}', f'{ROOT}/res/{side}'.replace('/', '_')):
        data = data.replace(old.encode(), old.replace(side, 'SIDE').encode())
    return data

summary = {}
for shape, v in report['shapes'].items():
    for rel in v['different']:
        if Path(rel).suffix not in ('.o', '.a', '.elf'):
            summary.setdefault('text', []).append(f'{shape}/{rel}')
            continue
        with tempfile.TemporaryDirectory(dir=ROOT / 'tmp') as tmp:
            work = Path(tmp)
            x = stripped(a, ROOT / 'res' / a / shape / rel, work)
            y = stripped(b, ROOT / 'res' / b / shape / rel, work)
            key = 'equal_without_debug' if norm(a, x) == norm(b, y) else 'DIFFERENT_without_debug'
            summary.setdefault(key, []).append(f'{shape}/{rel}')
for key, items in sorted(summary.items()):
    print(key, len(items))
    if key != 'equal_without_debug':
        for item in items:
            print('  ', item)
