#!/usr/bin/env python3
"""Exercise the actual link guard after reset with retained PHY clocks.
This measures link qualification, not Ethernet transmission.
"""
from pathlib import Path
import subprocess
import sys

root = Path(sys.argv[1]).resolve()
packet = Path(__file__).resolve().parent
out = packet / 'scratch' / 'guard'
out.mkdir(parents=True, exist_ok=True)
v = '$VALIDATION_TOOLS/pinned-verilator-5.050/verilator'
print(subprocess.check_output([v, '--version'], text=True), end='', flush=True)
cpp = out / 'probe.cpp'
cpp.write_text(r'''
#include "VKL_link_guard.h"
#include <cstdio>
int main() {
    VKL_link_guard t;
    t.dis_i = t.freeze_i = t.man_reinit_i = t.act_tgl_i = 0;
    t.rx_tgl_i = t.tx_tgl_i = 0;
    auto tick = [&]() {
        t.clk_i = 0; t.eval();
        t.clk_i = 1; t.eval();
    };
    t.rst_n = 0;
    for (int k=0; k<8; ++k) tick();
    t.rst_n = 1;
    unsigned qualified=0, reset=0;
    for (unsigned k=0; k<221700; ++k) {
        t.rx_tgl_i ^= 1; t.tx_tgl_i ^= 1; tick();
        qualified += t.link_est_o != 0;
        reset += t.reinit_o || t.eth_rst_o;
    }
    std::printf("retained clocks: %u/221700 cycles link_est=1; %u cycles MAC reset\n", qualified, reset);
    std::puts("221700 axis cycles at 50 MHz = 4.434 ms, the published 8x8 arm time.");
    std::puts("With the unchanged link_status=up and LINK_CTRL[0]=1 resets, eff_link is qualified before the arm.");
    std::puts("This isolated probe does not instantiate an Ethernet transmitter or prove a wire frame.");
    return (qualified == 221700 && reset == 0) ? 0 : 1;
}
''')
cmd = [v, '--cc', '--exe', '--build', '-j', '16', '--top-module', 'KL_link_guard',
       '--Mdir', str(out / 'obj'), str(root / 'hdl/common/KL_link_guard.sv'), str(cpp)]
with (packet / 'receipts/guard-build.log').open('w') as log:
    r = subprocess.run(cmd, stdout=log, stderr=subprocess.STDOUT)
if r.returncode:
    raise SystemExit(r.returncode)
raise SystemExit(subprocess.run([str(out / 'obj/VKL_link_guard')]).returncode)
