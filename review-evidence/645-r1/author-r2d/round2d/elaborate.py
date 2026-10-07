"""Re-elaborate the shipping AX7101 1x1 TDM8 LiteX project at 3eee12dc
(round2d/route-source export) into round2d/tf/route/ax7101, with round 2c's
argv apart from paths, and compare every generated file with round 2c's
timing project (round2c/tf/route/ax7101) after normalising the export and
output paths, so the reused vendor scripts are known to match."""
import hashlib
import json
import os
import shlex
import subprocess
from pathlib import Path

w = Path('$VALIDATION_STORAGE/645-a531/round2d')
c = Path('$VALIDATION_STORAGE/645-a531/round2c')
root = w / 'route-source'
old = c / 'tf/route/ax7101'
new = w / 'tf/route/ax7101'
out = w / 'tf/elaboration'
out.mkdir(parents=True, exist_ok=True)
env = os.environ.copy()
env.update(PYTHONDONTWRITEBYTECODE='1', PYTHONHASHSEED='0', MAKEFLAGS='-j4', TMPDIR=str(w / 'tmp'),
           LITEX_ENV_CC_TRIPLE='riscv32-linux')
env['PATH'] = str(Path.home() / 'litex-milan/venv/bin') + ':$VALIDATION_STORAGE/231-a337-sdk/bin:' + env['PATH']


def run(name, argv, cwd):
    with (out / (name + '.log')).open('w') as log:
        rc = subprocess.run(argv, cwd=cwd, env=env, stdout=log, stderr=subprocess.STDOUT).returncode
    (out / (name + '.rc')).write_text(f'{rc}\n')
    print(name, rc, flush=True)
    if rc:
        raise SystemExit(rc)


def norm(data: bytes) -> bytes:
    for path, tag in ((str(new), '@OUT@'), (str(old), '@OUT@'), (str(c / 'route-f/ax7101'), '@OUT@'),
                      (str(root), '@SRC@'), (str(c / 'route-source'), '@SRC@')):
        data = data.replace(path.encode(), tag.encode())
    return data


run('ax7101-dry-run', ['bash', 'sw/litex/build.sh', 'ax7101', '--dry-run'], root)
lines = [x for x in (out / 'ax7101-dry-run.log').read_text().splitlines() if 'exec python3 milan_soc.py ' in x]
assert len(lines) == 1
argv = shlex.split(lines[0].split('exec python3 ', 1)[1])
argv.remove('--build')
argv[argv.index('--output-dir') + 1] = str(new)
argv[argv.index('--vivado-max-threads') + 1] = '32'
earlier = json.loads((c / 'timing-f6bd415f/elaboration/ax7101-argv.json').read_text()
                     if (c / 'timing-f6bd415f/elaboration/ax7101-argv.json').exists()
                     else (Path.home() / 'milan-fpga-management/2026-09-23/645-a531/round2c/timing-f6bd415f/elaboration/ax7101-argv.json').read_text())
earlier[earlier.index('--output-dir') + 1] = str(new)
earlier = [a.replace(str(c / 'route-source'), str(root)) for a in earlier]
assert argv == earlier, (argv, earlier)
(out / 'ax7101-argv.json').write_text(json.dumps(argv, indent=2) + '\n')
run('ax7101-elaboration', [str(Path.home() / 'litex-milan/venv/bin/python3'), *argv], root / 'sw/litex')

report = {'argv_equal_to_round2c_apart_from_paths': True, 'files': []}
differ = []
for path in sorted(p for p in new.rglob('*') if p.is_file() and 'software' not in p.relative_to(new).parts[:1]):
    rel = path.relative_to(new)
    twin = old / rel
    a = norm(path.read_bytes())
    b = norm(twin.read_bytes()) if twin.is_file() else None
    same = a == b
    report['files'].append(dict(path=str(rel), bytes=len(a), sha256=hashlib.sha256(a).hexdigest(), equal_to_round2c=same))
    if not same:
        differ.append(str(rel))
report['differing_files'] = differ
(out / 'elaboration-compare.json').write_text(json.dumps(report, indent=2) + '\n')
print('generated files', len(report['files']), 'differing', differ)
