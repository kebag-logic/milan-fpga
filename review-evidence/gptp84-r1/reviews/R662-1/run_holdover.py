#!/usr/bin/env python3
"""Exercise the unchanged public parent holdover for every prescaler phase.

The copied authority is from parent e9cbb676; QTICK=8 scales 250 ms to
eight cycles. The control keeps two quarter ticks; the fault uses one.
"""
import concurrent.futures
import json
import os
from pathlib import Path
import subprocess

p = Path(__file__).resolve().parent
w = p / 'scratch/holdover'
w.mkdir(parents=True, exist_ok=True)
logs = p / 'holdover'
logs.mkdir(exist_ok=True)
src = w / 'KL_ptp_clock_validity.sv'
src.write_bytes((p / 'authority-KL_ptp_clock_validity.sv').read_bytes())
cpp = w / 'probe.cpp'
cpp.write_text(r'''
#include "VKL_ptp_clock_validity.h"
#include <cstdio>
int main() {
  unsigned checks=0, fails=0;
  auto check=[&](bool x, const char *n) {
    ++checks; if(!x) { ++fails; std::printf("FAIL %s\n",n); }
  };
  for(unsigned phase=0; phase<8; ++phase) {
    VKL_ptp_clock_validity d;
    auto tick=[&]() {d.clk_i=0; d.eval(); d.clk_i=1; d.eval();};
    d.rst_n=0; d.fabric_sync_ok_i=1; d.fabric_as_cap_i=1;
    d.fabric_disc_p_i=0; d.phc_load_p_i=0; d.phc_adj_p_i=0;
    d.gm_id_i=1; tick(); tick(); d.rst_n=1;
    for(unsigned t=0;t<32+phase;++t) tick();
    check(!d.ts_uncertain_o,"settled master has tu zero");
    // A changed GM must assert even before the edge retaining the hold.
    d.gm_id_i=2; d.eval();
    check(d.ts_uncertain_o,"GM edge warns immediately");
    unsigned first_clear=0;
    for(unsigned t=1;t<=20;++t) {
      tick(); if(!first_clear && !d.ts_uncertain_o) first_clear=t;
      if(t<=8) check(d.ts_uncertain_o,"GM change holds at least 250 ms");
    }
    std::printf("phase=%u first_clear=%u cycles quarter_tick=8\n",phase,first_clear);
    check(first_clear>=9 && first_clear<=17,"bounded two-quarter-tick clearance");
    check(!d.ts_uncertain_o,"master returns to tu zero");
    d.fabric_sync_ok_i=0; d.eval();
    check(d.ts_uncertain_o,"unsynchronised slave stays uncertain");
  }
  std::printf("%u checks: %u PASS, %u FAIL\n",checks,checks-fails,fails);
  return fails?1:0;
}
''')
def command(tag, args):
    with (logs / (tag+'.log')).open('w') as f:
        r = subprocess.run(args, cwd=w, stdout=f, stderr=subprocess.STDOUT)
    (logs / (tag+'.rc')).write_text(str(r.returncode)+'\n')
    return r.returncode
def run(name, hold):
    obj=w/name
    args=[os.environ.get('REVIEW_SIMULATOR','$VALIDATION_TOOLS/pinned-verilator-5.050/verilator'), '--cc','--exe','--build','-j','8',
          '--top-module','KL_ptp_clock_validity','--Mdir',str(obj),
          '-GQTICK_CYC_P=8','-GHOLD_QTICK_P='+str(hold),'-GFABRIC_GPTP_P=1',
          '-Wno-fatal',str(src),str(cpp),'-o','probe']
    assert command(name+'-build',args)==0
    rc=command(name,[str(obj/'probe')])
    assert rc==(0 if hold==2 else 1)
    return {'case':name,'hold_quarter_ticks':hold,'rc':rc}
with concurrent.futures.ThreadPoolExecutor(max_workers=2) as ex:
    rows=list(ex.map(lambda x:run(*x),[('control',2),('one-tick-fault',1)]))
(logs/'summary.json').write_text(json.dumps(rows,indent=2)+'\n')
print(json.dumps(rows))
