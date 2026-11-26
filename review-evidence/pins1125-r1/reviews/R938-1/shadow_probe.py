#!/usr/bin/env python3
"""Exercise the public clamp and test whether the last offset check requires a new pair."""
import os
import pathlib
import subprocess
import sys

packet = pathlib.Path(__file__).resolve().parent
root = packet / 'scratch/probe'
suite = root / 'tb/verilator/gptp_shadow'
bank = root / 'hdl/ieee8021as/gptp_plane/KL_gptp_shadow.sv'
harness = suite / 'sim_main.cpp'
sim = pathlib.Path(sys.argv[1]).resolve()
env = os.environ.copy()
env['TMPDIR'] = str(packet / 'scratch')
env['CCACHE_DISABLE'] = '1'
def run(name):
    logpath = packet / 'receipts' / (name + '.log')
    with logpath.open('w') as log:
        command = ['make', '-j16', 'run', 'VERILATOR_JOBS=8', 'VERILATOR=' + str(sim)]
        print('COMMAND', repr(command), file=log, flush=True)
        p = subprocess.run(command, cwd=suite, env=env, stdout=log, stderr=subprocess.STDOUT)
        print('EXIT', p.returncode, file=log)
    (packet / 'receipts' / (name + '.rc')).write_text(str(p.returncode) + '\n')
    return p.returncode, logpath.read_text()

original_bank = bank.read_bytes()
original_harness = harness.read_bytes()
try:
    rc, text = run('shadow-clean')
    assert rc == 0 and '483 checks: 483 PASS, 0 FAIL' in text
    old = b"        pub_pdelay_ns_o <= pub_pdelay_raw_w[31] ? 32'd0\n                                                : pub_pdelay_raw_w;\n"
    assert original_bank.count(old) == 1
    bank.write_bytes(original_bank.replace(old, b'        pub_pdelay_ns_o <= pub_pdelay_raw_w;\n'))
    rc, text = run('shadow-clamp-removed')
    assert rc != 0 and 'FAIL #109 -263 ns: the public bank reads 0' in text
    bank.write_bytes(original_bank)
    old = b'    gm_pair_on_link(m, used_delay(d));\n'
    assert original_harness.count(old) == 1
    harness.write_bytes(original_harness.replace(old, b'    // Probe: omit the graded pair; preserve all assertions.\n'))
    rc, text = run('shadow-graded-pair-omitted')
    print('Omitted-pair probe rc', rc)
    print('\n'.join(line for line in text.splitlines() if line.startswith('FAIL ') or 'checks:' in line))
finally:
    bank.write_bytes(original_bank)
    harness.write_bytes(original_harness)
assert bank.read_bytes() == original_bank and harness.read_bytes() == original_harness
print('Public clamp defect detected; source bytes restored.')
