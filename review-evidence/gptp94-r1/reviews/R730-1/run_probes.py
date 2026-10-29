#!/usr/bin/env python3
"""Reproduce focused port-disable probes without changing the reviewed tree."""
import argparse
import io
import os
from pathlib import Path
import subprocess
import tarfile
import time

HEAD = '9d509029de967c50de7527edf2b8869aa9db9074'
p = argparse.ArgumentParser()
p.add_argument('--repo', type=Path, required=True)
p.add_argument('--compiler', type=Path, default=Path('$VALIDATION_TOOLS/pinned-verilator-5.050/verilator'))
p.add_argument('--jobs', type=int, default=16)
p.add_argument('--case', choices=['probe', 'focused'], default='probe')
a = p.parse_args()
assert 1 <= a.jobs <= 16
packet = Path(__file__).resolve().parent
tree = packet / 'scratch' / (a.case + '-tree')
tree.mkdir(parents=True, exist_ok=True)
assert subprocess.check_output(['git', '-C', str(a.repo), 'rev-parse', 'HEAD'], text=True).strip() == HEAD
version = subprocess.check_output([str(a.compiler), '--version'], text=True)
assert '5.050' in version
(packet / 'compiler-identity.txt').write_text(version)
archive = subprocess.check_output(['git', '-C', str(a.repo), 'archive', HEAD])
with tarfile.open(fileobj=io.BytesIO(archive)) as tar:
    tar.extractall(tree, filter='data')
src = tree / 'tb/verilator/engine/sim_main.cpp'
s = src.read_text()
start = s.index('  int run_suite() {')
end = s.index('\n private:', start)
s = s[:start] + '''  int run_suite() {
    independent_port_probes();
    printf("%d checks: %d PASS, %d FAIL\\n", checks, checks - fails, fails);
    return fails ? 1 : 0;
  }
''' + s[end:]
s = s.replace('\n private:', '\n private:\n' + (packet / 'probe.cpp.inc').read_text(), 1)
if a.case == 'focused':
    s = s.replace('    independent_port_probes();', '''    bring_the_engine_out_of_reset();
    settle_as_capable_master("focused setup");
    boot_watch = false;
    end_the_cease_on_a_port_toggle();
    drop_ascapable_at_a_link_loss();
    drop_a_frame_built_across_the_fall();
    keep_the_countdown_exit();''')
src.write_text(s)
work = tree / 'tb/verilator/engine'
rtl = tree / 'hdl'
sources = ['ucpu/gptp_ucpu_pkg.sv', 'ucpu/KL_gptp_ucpu.sv',
           'wire/KL_gptp_rx_parser.sv', 'wire/KL_gptp_tx_slot.sv',
           'common/KL_gptp_timer.sv', 'top/KL_gptp_engine.sv']
cmd = [str(a.compiler), '--cc', '--exe', '--build', '-j', str(a.jobs),
       '--top-module', 'KL_gptp_engine', '-Wall', '-Wno-fatal',
       '-Wno-DECLFILENAME', '-Wno-UNUSEDSIGNAL', '-Wno-WIDTHEXPAND',
       '-Wno-WIDTHTRUNC', '-Wno-UNUSEDPARAM',
       '-GUCODE_HEX_P="gptp_ucode.hex"', '-GCLK_HZ_P=2000000',
       '-CFLAGS', '-std=c++17 -O2 -Wall -Wextra',
       *[str(rtl / x) for x in sources], 'sim_main.cpp', '-o', 'Vprobe']
for name, command in [(a.case + '-build', cmd), (a.case + '-run', ['./obj_dir/Vprobe'])]:
    t = time.monotonic()
    with (packet / (name + '.log')).open('w') as log:
        log.write('command: ' + repr(command) + '\n'); log.flush()
        r = subprocess.run(command, cwd=work, stdout=log, stderr=subprocess.STDOUT, timeout=540)
    (packet / (name + '.rc')).write_text(str(r.returncode) + '\n')
    print(name, 'rc', r.returncode, 'seconds', round(time.monotonic() - t, 2), flush=True)
    if name.endswith('-build') and r.returncode:
        raise SystemExit(r.returncode)
