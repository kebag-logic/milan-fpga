#!/usr/bin/env python3
"""Independent fault probes of notification completion and evidence reuse."""
import contextlib
import io
import json
import os
from pathlib import Path
import shutil
import sys

root = Path(os.environ['REVIEW_ROOT'])
packet = Path(os.environ['REVIEW_PACKET'])
sys.path.insert(0, str(root / 'tb/verilator/ctrl_service_budget'))
import build
import grade
import scenario
import selftest
import run

out = {}
# Two registered recipients require both notification commits. The second
# crosses T_svc while the first fits. No implementation code is changed.
ch = scenario.CH['aecp']
def response(controller, seq, unsolicited=False):
    f = bytearray(scenario.f.aem_command(
        scenario.f.Aem(1, controller, 2, 3, seq), 0x10, bytes(8)))
    f[15] = 1
    if unsolicited:
        f[36] |= 0x80
    return bytes(f)
probe = scenario.Probe('review.notify.if0', 'notification fan-out', 'notify',
                       f'rxc:{ch}', [f'resp:{ch}:41', f'notify:{ch}'])
lines = ['MARK 1000 review.notify.if0', 'RXS 1100 0 60 review.notify.if0',
         'RXE 1159', f'RXC 1173 {ch}']
at = 0
for cycle, interface, frame in [(201173, 0, response(2, 0x41)),
                               (401173, 0, response(3, 0x42, True)),
                               (1401173, 1, response(4, 0x43, True))]:
    lines.extend(selftest.tx_record(ch, interface, frame, at, cycle))
    at += 2 + (len(frame) + 3) // 4
text = selftest.synthetic(lines)
(packet / 'notification-late-recipient.log').write_text(text)
row = selftest.one(text, probe)
out['late_recipient'] = {'graded': row, 'required_end_sys': 1401173,
                         'required_ms': 14, 'expected_within_t_svc': False}
assert row['within_t_svc'] and row['ms'] == 4.0
# The second recipient is missing entirely; the same row remains measured.
missing = selftest.synthetic(lines[:-2])
(packet / 'notification-missing-recipient.log').write_text(missing)
out['missing_recipient'] = selftest.one(missing, probe)
assert out['missing_recipient']['status'] == 'measured'

# A reused native build's generated ELF is changed in an isolated copy.
# The reuse guard advertises all-input validation but ignores basename keys.
source = packet / 'scratch/A1'
dest = packet / 'scratch/reuse-probe'
(dest / 'native').mkdir(parents=True, exist_ok=True)
(dest / 'image').mkdir(exist_ok=True)
shutil.copy2(source / 'build.json', dest / 'build.json')
os.link(source / 'native/Vsim', dest / 'native/Vsim') if not (dest / 'native/Vsim').exists() else None
shutil.copy2(source / 'image/ctrl_app.elf', dest / 'image/ctrl_app.elf')
data = bytearray((dest / 'image/ctrl_app.elf').read_bytes())
data[-1] ^= 1
(dest / 'image/ctrl_app.elf').write_bytes(data)
spec = build.reused(dest)
out['modified_elf_reuse_accepted'] = True
shutil.copytree(source / 'gateware', dest / 'gateware', dirs_exist_ok=True)
rom = dest / 'gateware/sim_rom_bank0.init'
original_rom = rom.read_bytes()
words = rom.read_text().splitlines()
words[0] = '0000006f'  # jal zero, 0: never leave the reset entry.
rom.write_text('\n'.join(words) + '\n')
build.reused(dest)
import hashlib
out['modified_runtime_rom_reuse_accepted'] = {
    'original_sha256': hashlib.sha256(original_rom).hexdigest(),
    'mutated_sha256': hashlib.sha256(rom.read_bytes()).hexdigest(),
    'mutation': 'Reset entry replaced with jal zero, 0',
    'native_reads_at_runtime': '$readmemh("sim_rom_bank0.init", rom_bank0)',
    'rom_files_bound_in_manifest': any('.init' in key for key in spec['inputs'])}

# CLI regrade with no group logs still exits zero. This is a real invocation,
# using an unchanged build and a fresh empty output directory.
empty = packet / 'scratch/empty-regrade'
argv = [str(root / 'tb/verilator/ctrl_service_budget/run.py'), '--point', '1x1',
        '--build-dir', str(source), '--reuse-build', '--regrade', '--out', str(empty),
        '--record-budget-findings', '--groups', 'backlog,backlog-adp']
sys.argv = argv
with contextlib.redirect_stdout(io.StringIO()) as captured:
    rc = run.main()
out['empty_regrade'] = {'returncode': rc, 'stdout': captured.getvalue(),
                        'requested_groups': ['backlog', 'backlog-adp']}
assert rc == 0
(packet / 'grader-probes.json').write_text(json.dumps(out, indent=2) + '\n')
print(json.dumps(out, indent=2))
