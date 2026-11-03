#!/usr/bin/env python3
"""Section 5's fit table at a checkout: the platform image (ctrl_plat_image.py) and the size fixture
(ctrl_srp_image.py, --with-aecp, split layout) at the four points, each planned by ctrl_memory, with the ledgered
point named at 8x8 with two interfaces only, as the harness and the boot simulation name it. Also ctrl_plat's size.

usage: fit.py CHECKOUT RUNTIME_DIR OUT
"""
import json
import subprocess
import sys
from pathlib import Path

checkout, runtime, out = (Path(a).resolve() for a in sys.argv[1:4])
test = checkout / 'sw/firmware/ctrl/test'
points = [('endstation_ax7101_1x1_tdm8', 1), ('endstation_ax7101_1x1_tdm8', 2), ('endstation_ax7101_8x8', 1),
          ('endstation_ax7101_8x8', 2)]
libs = ['--libc', str(runtime / 'libc.a'), '--compiler-runtime', str(runtime / 'libcompiler_rt.a')]
rows = []
for shape, n in points:
    largest = (shape, n) == ('endstation_ax7101_8x8', 2)
    cfg = str(checkout / 'configs' / f'{shape}.yaml')
    plat_out, fix_out = out / f'plat-{shape}-{n}', out / f'fixture-{shape}-{n}'
    plat = [sys.executable, '-B', str(test / 'ctrl_plat_image.py'), '--config', cfg, '--interfaces', str(n),
            '--csr-csv', str(test / 'ctrl_plat_csr.csv'), '--output', str(plat_out), *libs,
            *(['--ledgered-point', 'platform-8x8-two-interfaces'] if largest else [])]
    fix = [sys.executable, '-B', str(test / 'ctrl_srp_image.py'), '--config', cfg, '--interfaces', str(n),
           '--with-aecp', '--layout', 'split', '--output', str(fix_out), *libs,
           *(['--ledgered-point', '8x8-two-interfaces'] if largest else [])]
    for argv, where in ((plat, plat_out), (fix, fix_out)):
        where.mkdir(parents=True, exist_ok=True)
        done = subprocess.run(argv, cwd=checkout, capture_output=True, text=True)
        (where / 'tool.log').write_text(done.stdout + done.stderr)
        if done.returncode:
            raise SystemExit(f'{argv[2]} {shape} {n}: rc {done.returncode}; see {where / "tool.log"}')
    p = json.loads((plat_out / 'size.json').read_text())
    split = p['split']
    nm = (plat_out / 'symbols.txt').read_text().splitlines()
    ctrl_plat = next(int(f.split()[1], 16) for f in nm if f.split()[-1] == 'ctrl_plat')
    fixture = json.loads((fix_out / 'size.json').read_text())['split']
    rows.append(dict(shape=shape, interfaces=n, platform=split, fixture=fixture, ctrl_plat=ctrl_plat))
    print(f"{shape} if{n}: platform {split['rom']['bytes']:,} / {split['sram']['bytes']:,} B, {split['tiles']} tiles; "
          f"fixture {fixture['rom']['bytes']:,} / {fixture['sram']['bytes']:,} B, {fixture['tiles']} tiles; "
          f"ctrl_plat {ctrl_plat:,} B", flush=True)
(out / 'fit.json').write_text(json.dumps(rows, indent=1) + '\n')
