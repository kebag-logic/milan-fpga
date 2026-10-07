#!/usr/bin/env python3
"""Copy-only probe: declared holds expire and genuine starvation resumes."""
import argparse
import json
from pathlib import Path
import subprocess

p = argparse.ArgumentParser()
p.add_argument('--root', type=Path, default=Path.cwd())
p.add_argument('--sim', required=True)
a = p.parse_args()
root = a.root.resolve()
packet = Path(__file__).resolve().parents[1]
work = packet / 'scratch/hold-expiry'
work.mkdir(parents=True, exist_ok=True)
suite = root / 'tb/verilator/chmap_capture'
source = (suite / 'sim_main.cpp').read_text()
anchor = '  pin_starved_pair_pegs_and_holds();'
assert source.count(anchor) == 1
probe = r'''
  // Independent expiry boundary: keep pair 1 empty through all five holds.
  // The sixth walk must count one genuine dup; the seventh counts two.
  {
    const int stream = 5;
    lrc_wipe();
    lrc_align();
    drv_lb_pdu(stream, 4, 6, 1);
    for (int i = 0; i < 6; ++i) a_tick();
    lrc_pulse();
    dut->lb_tuser_i = stream;
    dut->lb_tdata_i = lb_beat(LBV(stream, 0, 7), LBV(stream, 1, 7));
    dut->lb_tvalid_i = 1;
    dut->lb_tlast_i = 0;
    cyc();
    dut->lb_tvalid_i = 0;
    dut->lb_tdata_i = 0;
    cyc(2);
    const long dup = dut->a_dup_cnt_o;
    const long skip = dut->a_skip_cnt_o;
    for (int walk = 1; walk <= 7; ++walk) {
      a_tick();
      const long expected = walk <= 5 ? 0 : walk == 6 ? 1 : 3;
      char label[96];
      std::snprintf(label, sizeof label, "EXPIRY: walk %d cumulative duplicate delta", walk);
      ck(label, static_cast<long>(dut->a_dup_cnt_o) - dup, expected);
    }
    ck("EXPIRY: skip counter unchanged", static_cast<long>(dut->a_skip_cnt_o) - skip, 0);
    lrc_wipe();
    const long after = dut->a_dup_cnt_o;
    for (int i = 0; i < 6; ++i) a_tick();
    ck("EXPIRY: flush stops subsequent starvation accounting",
       static_cast<long>(dut->a_dup_cnt_o) - after, 0);
  }
'''
source = source.replace(anchor, probe)
source = source.replace('"../../common/verilator_harness.hpp"',
                        json.dumps(str(root / 'tb/common/verilator_harness.hpp')))
cpp = work / 'sim_expiry.cpp'
cpp.write_text(source)
recipe = (suite / 'Makefile').read_text().replace('sim_main.cpp', str(cpp))
mk = work / 'Makefile'
mk.write_text(recipe)
commands = [('build', ['make', '-j16', '-f', str(mk), '-C', str(suite), 'build',
                       'VERILATOR_JOBS=16', f'VERILATOR={a.sim}', f'MDIR={work}/obj']),
            ('run', [str(work / 'obj/Vchmap_wrap')])]
for name, argv in commands:
    target = packet / 'receipts' / ('hold-expiry-' + name)
    target.with_suffix('.command.json').write_text(json.dumps(argv, indent=2) + '\n')
    with target.with_suffix('.log').open('wb') as log:
        rc = subprocess.run(argv, stdout=log, stderr=subprocess.STDOUT, check=False).returncode
    target.with_suffix('.rc').write_text(str(rc) + '\n')
    print(name, 'rc', rc, flush=True)
    if rc:
        raise SystemExit(rc)
