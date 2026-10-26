#!/usr/bin/env python3
"""Reuse-attestation probe: plant one stale input at a time in a copy of a finished build and
ask the harness's own build.reused() whether it would reuse it; then run run.py --reuse-build on
one plant to show the refusal and the exit status.

Usage: stale_probe2.py CHECKOUT BUILD_DIR SCRATCH
Every plant must be refused; the unchanged copy must be accepted. The shared CPU netlist is never
modified: its content plant points the recorded key at a modified private copy.
"""
import hashlib
import json
import shutil
import subprocess
import sys
from pathlib import Path

checkout, build, scratch = Path(sys.argv[1]), Path(sys.argv[2]).resolve(), Path(sys.argv[3]).resolve()
sys.path.insert(0, str(checkout / 'tb/verilator/ctrl_service_budget'))
import build as builder  # noqa: E402


def fresh(name: str) -> Path:
    d = scratch / name
    shutil.rmtree(d, ignore_errors=True)
    shutil.copytree(build, d, ignore=shutil.ignore_patterns('results'), symlinks=True)
    spec = json.loads((d / 'build.json').read_text())
    # Build-relative paths recorded in build.json (elf, sources) are rewritten to the copy.
    text = (d / 'build.json').read_text().replace(str(build), str(d))
    (d / 'build.json').write_text(text)
    return d


def spec_edit(d: Path, fn) -> None:
    spec = json.loads((d / 'build.json').read_text())
    fn(spec)
    (d / 'build.json').write_text(json.dumps(spec, indent=2) + '\n')


def flip(p: Path) -> None:
    b = bytearray(p.read_bytes())
    b[len(b) // 2] ^= 0x01
    p.write_bytes(bytes(b))


def netlist_key(spec: dict) -> str:
    return next(k for k in spec['inputs'] if k.startswith('external:') and 'VexiiRiscvLitex_' in k)


def private_netlist(d: Path) -> None:
    def fn(spec):
        key = netlist_key(spec)
        src = Path(key.split(':', 1)[1])
        copy = d / 'private' / src.name
        copy.parent.mkdir(exist_ok=True)
        shutil.copy(src, copy)
        flip(copy)
        new = f'external:{copy}'
        spec['inputs'][new] = spec['inputs'].pop(key)        # the recorded digest, now of a changed file
        spec['sources'] = [str(copy) if s == str(src) else s for s in spec['sources']]
    spec_edit(d, fn)


PLANTS = [
    ('unchanged copy (control: must be accepted)', lambda d: None),
    ('image ELF changed', lambda d: flip(d / 'image/ctrl_app.elf')),
    ('ROM bank 0 .init changed (first word)', lambda d: (d / 'gateware/sim_rom_bank0.init').write_text(
        'deadbeef\n' + ''.join((d / 'gateware/sim_rom_bank0.init').read_text().splitlines(True)[1:]))),
    ('ROM bank 1 .init deleted', lambda d: (d / 'gateware/sim_rom_bank1.init').unlink()),
    ('an unrecorded ROM .init added', lambda d: shutil.copy(d / 'gateware/sim_rom_bank0.init',
                                                            d / 'gateware/sim_rom_bank2.init')),
    ('SoC Verilog sim.v changed', lambda d: flip(d / 'gateware/sim.v')),
    ('CPU netlist content changed (private copy under the recorded digest)', private_netlist),
    ('CPU netlist recorded digest zeroed', lambda d: spec_edit(d, lambda s: s['inputs'].__setitem__(netlist_key(s), '0' * 64))),
    ('runtime libc.a changed', lambda d: flip(d / 'runtime/libc.a')),
    ('budget_config.hpp changed', lambda d: flip(d / 'budget_config.hpp')),
    ('native model Vsim changed', lambda d: flip(d / 'native/Vsim')),
    ('firmware tree digest differs from the checkout', lambda d: spec_edit(d, lambda s: s['inputs'].__setitem__('tree:firmware', '0' * 64))),
    ('a bare-basename key (the round-1 form)', lambda d: spec_edit(d, lambda s: s['inputs'].__setitem__('sim.v', s['inputs'].pop('build:gateware/sim.v')))),
    ('an external key with a relative path', lambda d: spec_edit(d, lambda s: s['inputs'].__setitem__('external:relative/x.v', '0' * 64))),
    ('build.json without inputs', lambda d: spec_edit(d, lambda s: s.pop('inputs'))),
]

bad = 0
for n, (what, plant) in enumerate(PLANTS):
    d = fresh(f'p{n:02d}')
    plant(d)
    try:
        builder.reused(d)
        verdict = 'ACCEPTED'
    except (RuntimeError, OSError, KeyError, ValueError) as e:
        verdict = f'REFUSED ({type(e).__name__}: {str(e)[:150]})'
    ok = verdict == 'ACCEPTED' if n == 0 else verdict.startswith('REFUSED')
    bad += not ok
    print(f'{"ok " if ok else "BAD"} {what}: {verdict}')
r = subprocess.run([sys.executable, '-B', str(checkout / 'tb/verilator/ctrl_service_budget/run.py'), '--point', '1x1',
                    '--build-dir', str(scratch / 'p02'), '--reuse-build', '--groups', 'fixture', '--record-budget-findings'],
                   capture_output=True, text=True)
print(f'run.py --reuse-build on the ROM-bank plant: rc={r.returncode} :: {r.stdout.strip()[:200]}')
bad += r.returncode != 1
print(f'stale probe: {len(PLANTS)} cases, {bad} wrong')
