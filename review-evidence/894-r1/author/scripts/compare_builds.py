"""Two builds of one leg compared: every image ELF byte for byte and as objcopy -O binary, every recorded build input,
and a sample group's log. usage: compare_builds.py OLD_BUILD NEW_BUILD SAMPLE_LOG_OLD SAMPLE_LOG_NEW"""
import hashlib, json, subprocess, sys, tempfile
from pathlib import Path
old, new, lo, ln = map(Path, sys.argv[1:5])
OC = '$WORKSPACE_HOME/br-milan-rv32/host/bin/riscv32-buildroot-linux-gnu-objcopy'
h = lambda b: hashlib.sha256(b).hexdigest()
bad = 0
elfs = sorted(p.relative_to(old) for p in old.rglob('ctrl_app.elf') if 'results' not in p.parts)
for rel in elfs:
    a, b = old / rel, new / rel
    if not b.exists():
        print(f'{rel}: absent in the new build'); bad += 1; continue
    with tempfile.TemporaryDirectory() as d:
        subprocess.run([OC, '-O', 'binary', str(a), f'{d}/a'], check=True)
        subprocess.run([OC, '-O', 'binary', str(b), f'{d}/b'], check=True)
        x, y = Path(f'{d}/a').read_bytes(), Path(f'{d}/b').read_bytes()
    same = x == y
    bad += not same
    print(f'{rel} objcopy -O binary {"identical" if same else "DIFFERS"}: old {h(x)} new {h(y)}, {len(y)} B')
    print(f'{rel} elf {"identical" if a.read_bytes() == b.read_bytes() else "differs"}')
io, inn = json.loads((old / 'build.json').read_text())['inputs'], json.loads((new / 'build.json').read_text())['inputs']
diff = [k for k in sorted(set(io) | set(inn)) if io.get(k) != inn.get(k)]
for k in diff:
    print(f'input differs: {k}')
print(f'inputs compared: {len(set(io) | set(inn))}, identical: {len(set(io) | set(inn)) - len(diff)}')
x, y = lo.read_bytes(), ln.read_bytes()
same = x == y
bad += not same
print(f'sample {ln.stem} log {"identical" if same else "DIFFERS"}: recorded {h(x)} new {h(y)}, {len(y)} bytes')
sys.exit(1 if bad else 0)
