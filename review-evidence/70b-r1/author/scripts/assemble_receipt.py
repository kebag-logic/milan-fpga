#!/usr/bin/env python3
"""Assemble tb/verilator/nvm_capture_cpu/measurements.json from the six arms (#70).

Usage: assemble_receipt.py <repo> <arms-root> <base-commit> <assignment-url> <date>

An earlier lane's assembler with this lane's provenance. Each arm directory
<arms-root>/<arm>/capture-<arm>/ holds the harness's own measurement.json and
build products, and <arms-root>/run-<arm>.log its run log. The summaries are
taken verbatim; the per-arm identities are hashed from the build products (the
same five fields the previous receipt carried); the census, harness hashes and
maxima are recomputed through scripts/check_nvm_capture.py's own functions,
and the result is checked with that gate's check_receipt before it is written.
The measured commit must be the checked-out HEAD, with a clean tree, and every
run log must name the simulator the receipt records.
"""
import hashlib
import json
import subprocess
import sys
from pathlib import Path

repo, arms_root, base, assignment, date = (Path(sys.argv[1]), Path(sys.argv[2]), sys.argv[3],
                                           sys.argv[4], sys.argv[5])
sys.path[:0] = [str(repo / 'scripts')]
import check_nvm_capture as gate  # noqa: E402

ORDER = [('endstation_ax7101_1x1_tdm8', '1x1', 50), ('endstation_ax7101_8x8', '8x8', 50),
         ('endstation_ax7101_8x8', '8x8', 100)]


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def git(*args: str) -> str:
    return subprocess.run(['git', '-C', str(repo), *args], check=True,
                          capture_output=True, text=True).stdout.strip()


base_full = git('rev-parse', base)
assert git('rev-parse', 'HEAD') == base_full, 'the measured commit must be the checked-out HEAD'
assert git('status', '--porcelain') == '', 'the measured tree must be clean'
old = json.loads((repo / 'tb/verilator/nvm_capture_cpu/measurements.json').read_text())
measurements = []
for shape, tag, mhz in ORDER:
    for traffic in ('on', 'off'):
        arm = f'{tag}-{mhz}-{traffic}'
        d = arms_root / arm / f'capture-{arm}'
        log = (arms_root / f'run-{arm}.log').read_text()
        assert f"Verilation Report: {old['simulator']} " in log.replace('V e r i l a t i o n   R e p o r t', 'Verilation Report'), arm
        summary = json.loads((d / 'measurement.json').read_text())
        src = json.loads((d / 'sources.json').read_text())
        netlists = [Path(s) for s in src['sources'] if Path(s).name.startswith('VexiiRiscvLitex_')]
        assert len(netlists) == 1, netlists
        assert (summary['shape'], summary['cpu_hz'], summary['traffic']) == (shape, mhz * 1_000_000, traffic)
        rows = summary.pop('rows')
        entry = dict(summary)
        entry['clock_role'] = 'contract' if mhz == 50 else 'non-contract comparison'
        entry['command'] = ('unshare -Urn "$PRODUCT_PYTHON" -B tb/verilator/nvm_capture_cpu/run.py '
                            f'--shape {shape} --cpu-hz {mhz}000000 --captures 16 --traffic {traffic} '
                            f'--build-dir "$SCRATCH/capture-{arm}"')
        entry['cpu_netlist_sha256'] = sha(netlists[0])
        entry['instrumented_firmware_sha256'] = sha(d / 'measurement_firmware/milan_baremetal.c')
        entry['bios_sha256'] = sha(d / 'software/bios/bios.bin')
        entry['gptp_ucode_sha256'] = sha(d / 'generated' / shape / 'gptp_ucode.hex')
        entry['config_sha256'] = sha(repo / 'configs' / f'{shape}.yaml')
        entry['rows'] = rows
        order = list(old['measurements'][0].keys())
        assert set(order) == set(entry), (set(order) ^ set(entry))
        measurements.append({k: entry[k] for k in order})

actual = gate.current_inputs()
keys = [(m['shape'], m['cpu_hz'], m['traffic']) for m in measurements]
maxima = []
for shape, clock in sorted({k[:2] for k in keys}):
    group = [m for m in measurements if (m['shape'], m['cpu_hz']) == (shape, clock)]
    worst = gate.capture.maximum_ms(group)
    maxima.append(dict(shape=shape, cpu_hz=clock, maximum_ms=worst,
                       margin=gate.recipe.HOLD_FLOOR_MS / worst))


def cycles(arms: list) -> dict:
    return {(m['shape'], m['cpu_hz'], m['traffic']): [r['sys_cycles'] for r in m['rows']] for m in arms}


repeats = cycles(measurements) == cycles(old['measurements'])
same = sum(a == b for m, o in zip(measurements, old['measurements'])
           for a, b in zip([r['sys_cycles'] for r in m['rows']], [r['sys_cycles'] for r in o['rows']]))
harness = {p.name: sha(p) for p in gate.HARNESS.iterdir() if p.suffix in ('.py', '.cpp')}
pins = {sub: git('ls-tree', base_full, sub).split()[2] for sub in old['processor_pins']}
dev = git('rev-parse', f'{base_full}^')

new = dict(old)
new['date'] = date
new['base'] = base_full
new['measured_for'] = actual
new['harness_sha256'] = harness
new['measurements'] = measurements
new['maxima'] = maxima
new['remeasurement_assignment'] = assignment
new['processor_pins'] = pins
new['tree'] = git('rev-parse', f'{base_full}^{{tree}}')
new['provenance'] = (
    f"All six arms measure {base_full[:8]}, the #70 firmware on dev {dev[:8]}: entity_advertise() "
    "reports the enable it requested rather than an enabled entity, the restore wait reports at its "
    "timeout that the fabric holds the enable, and the PHY poll runs on every boot path past the CSR "
    "identity check. nvm_capture() and the census are unchanged, and so are dev's capture harness and "
    "RTL. Processor pins "
    f"{pins['protocol-processor'][:8]} (protocol) and {pins['gptp-processor'][:8]} (gPTP). "
    + (f"All 96 captures repeat the previous receipt's system-cycle counts ({old['base'][:8]}). "
       if repeats else f"{same} of 96 captures repeat the previous receipt's system-cycle counts ({old['base'][:8]}). ")
    + "The six "
    "arms ran in two drivers of three, so at most two builds ran at once; independent simulations "
    "overlapped. The capture SoC has no Milan MAC MDIO CSR, so the PHY path is compiled out. ARM "
    "through ATTEST contains no heartbeat or PHY call.")
new['product_firmware_sha256'] = sha(repo / 'sw/firmware/milan_baremetal/milan_baremetal.c')
base_firmware = subprocess.run(['git', '-C', str(repo), 'show',
                               f'{base_full}:sw/firmware/milan_baremetal/milan_baremetal.c'],
                              check=True, capture_output=True).stdout
assert hashlib.sha256(base_firmware).hexdigest() == new['product_firmware_sha256']
new['bios_dispatch_patch_sha256'] = sha(repo / 'sw/litex/patches/0006-bios-dispatch-hook.patch')
assert list(new.keys()) == list(old.keys())
gate.check_receipt(new, actual)
(repo / 'tb/verilator/nvm_capture_cpu/measurements.json').write_text(json.dumps(new, indent=2) + '\n')
for m in maxima:
    print('MAXIMUM', m['shape'], m['cpu_hz'], f"{m['maximum_ms']:.5f} ms", f"{m['margin']:.4f}x")
for m in measurements:
    print('ARM', m['shape'], m['cpu_hz'], m['traffic'], m['minimum_ms'], m['maximum_ms'], f"{m['margin']:.4f}x")
print('REPEATS previous cycle counts:', repeats, f'({same} of 96 equal)')
