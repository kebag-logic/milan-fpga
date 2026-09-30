"""Re-record tb/verilator/nvm_capture_cpu/measurements.json from the six capture
arms run_native.py measured at one head.

Every graded field is the arm's own measurement.json, re-graded here from its
raw capture.log with the harness's grader; every identity is derived from the
arm's build as PR #609's compare_previous.py derives it. The census, clocks and
harness digests are recomputed and must equal the committed receipt's, or this
refuses. Only the fields that name the measured tree (date, base, tree,
processor pins, firmware and BIOS-patch digests, assignment, provenance), the
six arms and the maxima are rewritten; every other field is kept as committed.

Usage, from the lane root: python3 record_capture_receipt.py <scratch> <head>
"""
from pathlib import Path
import hashlib
import json
import re
import subprocess
import sys

ROOT = Path('$LANES/70-lane2-pin')
HARNESS = ROOT / 'tb/verilator/nvm_capture_cpu'
RECEIPT = HARNESS / 'measurements.json'
sys.path.insert(0, str(HARNESS))
sys.path.insert(0, str(ROOT / 'scripts'))
import run as capture  # noqa: E402
import check_nvm_capture  # noqa: E402
import recipe  # noqa: E402

SCRATCH, HEAD = Path(sys.argv[1]), sys.argv[2]
ASSIGNMENT = 'https://github.com/kebag-logic/milan-fpga/issues/70#issuecomment-5894183475'
PROVENANCE = ('All six arms measure the #70 lane 2 firmware, which loads the AEM image before '
              'nvm_boot() and starts the restore walk on every boot path, at processor pin '
              'b2db3a97. The capture SoC has no Milan MAC MDIO CSR, so the PHY path is '
              'compiled out. ARM through ATTEST contains no heartbeat or PHY call.')


def git(*args):
    return subprocess.check_output(['git', *args], cwd=ROOT, text=True).strip()


def digest(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def rows_of(raw):
    return [dict((key, int(value)) for key, value in re.findall(r'(\w+)=(\d+)', line))
            for line in raw.splitlines() if line.startswith('CAPTURE index=')]


assert git('rev-parse', 'HEAD') == HEAD, 'the lane is not at the measured head'
assert not git('status', '--porcelain', '--untracked-files=no'), 'dirty worktree'
old = json.loads(RECEIPT.read_text())
actual = check_nvm_capture.current_inputs()
assert actual == old['measured_for'], 'capture census or clocks changed'
harness = {path.name: digest(path) for path in HARNESS.iterdir() if path.suffix in ('.py', '.cpp')}
assert harness == old['harness_sha256'], 'measurement harness changed'
short = {recipe.SHAPES[0]: '8x8', recipe.SHAPES[1]: '1x1'}
arms = []
for entry in old['measurements']:
    build = SCRATCH / f"capture-{short[entry['shape']]}-{entry['cpu_hz'] // 1000000}-{entry['traffic']}"
    spec = json.loads((build / 'sources.json').read_text())
    measured = json.loads((build / 'measurement.json').read_text())
    assert capture.grade_rows(rows_of((build / 'capture.log').read_text()), spec) == measured, build
    assert (measured['shape'], measured['cpu_hz'], measured['traffic']) == \
        (entry['shape'], entry['cpu_hz'], entry['traffic']), build
    cpu = [Path(path) for path in spec['sources'] if Path(path).name.startswith('VexiiRiscvLitex_')]
    assert len(cpu) == 1, build
    identities = dict(cpu_netlist_sha256=digest(cpu[0]),
                      instrumented_firmware_sha256=digest(build / 'measurement_firmware/milan_baremetal.c'),
                      bios_sha256=digest(build / 'software/bios/bios.bin'),
                      gptp_ucode_sha256=digest(build / 'generated' / spec['shape'] / 'gptp_ucode.hex'),
                      config_sha256=digest(ROOT / 'configs' / (spec['shape'] + '.yaml')))
    kept = dict(clock_role=entry['clock_role'], command=entry['command'])
    new = {**measured, **kept, **identities}
    assert list(new) == list(entry), (list(new), list(entry))
    arms.append(new)
maxima = []
for shape, clock in sorted({(arm['shape'], arm['cpu_hz']) for arm in arms}):
    group = [arm for arm in arms if (arm['shape'], arm['cpu_hz']) == (shape, clock)]
    worst = capture.maximum_ms(group)
    maxima.append(dict(shape=shape, cpu_hz=clock, maximum_ms=worst, margin=recipe.HOLD_FLOOR_MS / worst))
receipt = dict(old)
receipt.update(
    date='2026-09-29', base=HEAD, tree=git('rev-parse', 'HEAD^{tree}'),
    product_firmware_sha256=digest(ROOT / 'sw/firmware/milan_baremetal/milan_baremetal.c'),
    measurements=arms, maxima=maxima, remeasurement_assignment=ASSIGNMENT,
    processor_pins={name: git('ls-tree', 'HEAD', name).split()[2]
                    for name in old['processor_pins']},
    provenance=PROVENANCE,
    bios_dispatch_patch_sha256=digest(ROOT / 'sw/litex/patches/0006-bios-dispatch-hook.patch'))
assert list(receipt) == list(old)
RECEIPT.write_text(json.dumps(receipt, indent=2) + '\n')
for arm in arms:
    print(arm['shape'], arm['cpu_hz'], arm['traffic'], arm['minimum_ms'], arm['maximum_ms'],
          round(recipe.HOLD_FLOOR_MS / arm['maximum_ms'], 4))
print('maxima', [(m['shape'], m['cpu_hz'], m['maximum_ms'], round(m['margin'], 4)) for m in maxima])
