#!/usr/bin/env python3
"""Scratch-only trace instrumentation of sim_ax1x1gptp.cpp (never committed)."""
import sys, pathlib
p = pathlib.Path(sys.argv[1]) / "tb/verilator/milan_dp/sim_ax1x1gptp.cpp"
s = p.read_text()
helper = '''
#define R(n) (dut->rootp->milan_datapath__DOT__##n)
#define TRACE_STATE() \\
    "lb_dup=%u lb_skip=%u tdm_dup=%u tdm_skip=%u mga_eng=%u mga_err=%d trim=%d nco_en=%u", \\
    unsigned(R(lb_dup_cnt_w)), unsigned(R(lb_skip_cnt_w)), unsigned(R(tdm_dup_cnt_w)), \\
    unsigned(R(tdm_skip_cnt_w)), unsigned(R(mga_engaged_w)), int(int16_t(R(mga_err_w))), \\
    int(int16_t(R(mnco_servo_trim_w))), unsigned(R(mnco_servo_en_w))
'''
anchor = "namespace {\nconstexpr uint64_t kHz"
assert anchor in s
s = s.replace(anchor, helper + anchor, 1)
old = "            if (index != last_sample + 1) ++order_bad;\n"
assert old in s
new = ('            if (index != last_sample + 1) {\n'
       '                ++order_bad;\n'
       '                printf("TRACE ORDER t=%.6f cyc=%llu last=%u index=%u step=%d ", double(cyc) / kHz,\n'
       '                       static_cast<unsigned long long>(cyc), last_sample, index, int(index - last_sample));\n'
       '                printf(TRACE_STATE()); printf("\\n");\n'
       '            }\n')
s = s.replace(old, new, 1)
old2 = '    if (cyc % (kHz / 4) == 0) printf("PROGRESS'
assert old2 in s
new2 = ('    if (cyc % (kHz / 20) == 0) { printf("TRACE STATE t=%.2f ", double(cyc) / kHz); printf(TRACE_STATE()); printf("\\n"); }\n'
        + old2)
s = s.replace(old2, new2, 1)
p.write_text(s)
print("instrumented", p)
