#!/usr/bin/env python3
"""A disposable receiver-side fault: replay stale slot zero before recovery collection starts.

Run against a disposable checkout that already has ship8 built. It changes only
the simulated pin receiver's input, not expected samples, checkers or DUT state.
Restores the C++ source in finally; the disposable executable remains a probe.
"""
import os, subprocess, sys
from pathlib import Path
repo=Path(sys.argv[1]).resolve()
out=Path(sys.argv[2]).resolve()
suite=repo/'tb/verilator/milan_dp_render'
src=suite/'sim_ship8_render.cpp'
old=src.read_text()
new=old.replace('    int p_bclk = 0;', '    bool replay_stale_pin = false;\n    long replayed_frames = 0;\n    int p_bclk = 0;',1)
new=new.replace('        const int d = dut->tdm_dout_o;', '''        int d = dut->tdm_dout_o;
        // Fault at the receiver input: a pre-loss event on slot zero.
        // It is active through the entire ungraded recovery interval.
        if (replay_stale_pin && framed && q < kSlotBits) {
            const uint32_t stale = sample_word(0, 1, 0) << 8;
            d = static_cast<int>((stale >> (31 - q)) & 1u);
            if (b && !p_bclk && q == 0) ++replayed_frames;
        }''',1)
for start,end in [('    bind(0, "B3 REBIND");','    const Window w = decode_a_window(kWindowPdus, 0, 1);'),('    for (int l = 0; l < kStreams; l++) bind(l, "Z3 BIND");','    const Window w = decode_a_window(kWindowPdus, 0, 0);')]:
    assert new.count(start)==1
    begin=new.index(start)
    finish=new.index(end,begin)
    new=new[:finish]+'    replay_stale_pin = false;\n    std::printf("[PROBE] stale slot-zero frames before collection: %ld\\n", replayed_frames);\n'+new[finish:]
    new=new[:begin]+'    replay_stale_pin = true;\n'+new[begin:]
assert new!=old
src.write_text(new)
try:
    env=os.environ.copy()
    cmd=['make','-j16','-C',str(suite),'ship8','VERILATOR='+env.get('REVIEW_VERILATOR','$VALIDATION_TOOLS/pinned-verilator-5.050/verilator'),'VERILATOR_JOBS=16']
    with (out/'scratch/freshness.raw').open('w') as f:
        p=subprocess.run(cmd,stdout=f,stderr=subprocess.STDOUT,env=env)
    (out/'freshness.rc').write_text(str(p.returncode)+'\n')
    print('fault-probe rc',p.returncode)
    for line in (out/'scratch/freshness.raw').read_text().splitlines():
        if any(s in line for s in ('[PROBE]','FRESHNESS','checks:','failures:','RESULT:')): print(line)
finally:
    src.write_text(old)
