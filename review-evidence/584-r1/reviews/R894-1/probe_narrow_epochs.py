#!/usr/bin/env python3
"""Exercise narrow lanes at non-power-of-two widths and across epoch/reset boundaries."""
import os
from pathlib import Path
import shutil
import subprocess
import sys

root = Path(sys.argv[1]).resolve()
packet = Path(__file__).resolve().parent
copy = packet / 'scratch/epochs'
for name in ('tb/verilator/tdm_render', 'tb/common', 'hdl/common', 'hdl/ieee1722/aaf'):
    shutil.copytree(root / name, copy / name, dirs_exist_ok=True)
suite = copy / 'tb/verilator/tdm_render'
make = suite / 'Makefile'
make.write_text(make.read_text().replace('--build -j 0', '--build -j 2') +
                '\n$(eval $(call LANE,lane3of8,3,8,1,8))\n' +
                '$(eval $(call LANE,lane7of32,7,32,1,10))\n')
src = suite / 'sim_master.cpp'
extra = r'''
    // A graceful epoch closes an already active narrow lane. No old stored
    // sample or prefetched frame may survive the flush, including after a
    // reset that the stopped serial clock could not observe directly.
    dut->fresh_i = 0;
    dut->epoch_evt_i = 1;
    tdm_cycle();
    dut->epoch_evt_i = 0;
    for (int f = 0; f < 6; ++f) decode_frame();
    auto silent = decode_frame();
    for (auto word : silent) check.hex("epoch closed: every bus slot is silent", word, 0);
    check.dec("closed epoch blocks commits", dut->commit_en_o, 0);
    commit(std::vector<std::uint32_t>(kSlots, 0xABCDEF));
    decode_frame();
    silent = decode_frame();
    for (auto word : silent) check.hex("closed-epoch commit cannot leak", word, 0);

    // Serial clock stopped during the entire reset pulse.
    dut->rst_n = 0;
    for (int c = 0; c < 12; ++c) {
        dut->clk_i = 0; dut->eval(); dut->clk_i = 1; dut->eval();
    }
    dut->rst_n = 1;
    for (int f = 0; f < 6; ++f) decode_frame();
    silent = decode_frame();
    for (auto word : silent) check.hex("stopped-clock reset: no stale sample", word, 0);
    check.dec("freshness still required after reset", dut->commit_en_o, 0);
    dut->fresh_i = 1;
    for (int f = 0; f < 6; ++f) decode_frame();
    check.that("freshness reopens narrow lane", dut->commit_en_o);
    commit(std::vector<std::uint32_t>(kSlots, 0x765432));
    decode_frame();
    auto resumed = decode_frame();
    for (int s = 0; s < kBusSlots; ++s)
        check.hex("post-reset fresh lane / zero tail", resumed[s], s < kSlots ? 0x76543200u : 0);
'''
anchor = '    check.dec("no commit overrun", dut->overruns_o, 0);'
assert src.read_text().count(anchor) == 1
src.write_text(src.read_text().replace(anchor, extra + '\n' + anchor))
verilator = os.environ.get('REVIEW_VERILATOR', 'verilator')
cmd = ['make', '-j16', 'lane1of32', 'lane3of8', 'lane7of32', f'VERILATOR={verilator}']
env = dict(os.environ, TMPDIR=str(packet / 'scratch'), PYTHONDONTWRITEBYTECODE='1')
with (packet / 'narrow-epochs.log').open('w') as log:
    log.write('command: ' + repr(cmd) + '\n'); log.flush()
    run = subprocess.run(cmd, cwd=suite, env=env, stdout=log, stderr=subprocess.STDOUT)
(packet / 'narrow-epochs.rc').write_text(str(run.returncode) + '\n')
print('narrow-epochs', run.returncode)
sys.exit(run.returncode)
