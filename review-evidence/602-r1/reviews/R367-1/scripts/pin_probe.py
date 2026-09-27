#!/usr/bin/env python3
"""Apply test_builder.py's direct_initializer regex and exact-RHS rule for
mcr_restart_p_w (sw/builder/test_builder.py:10572-10586, 10774-10780) to the
head datapath and to planted copies. usage: pin_probe.py HEAD_DATAPATH [PLANTED...]"""
import re, sys
EXPECT = re.sub(r"\s+", "", "crf_clk_selected_r & ((tkd_crflk_q_r & ~crf_locked_w) | crf_mr_toggle_p_w)")
rc = 0
for i, path in enumerate(sys.argv[1:]):
    src = open(path).read()
    m = list(re.finditer(r"(?m)^[ \t]*wire[ \t]+mcr_restart_p_w[ \t]*=[ \t]*(?P<value>[^;]+);", src))
    ok = len(m) == 1 and re.sub(r"\s+", "", m[0].group("value")) == EXPECT
    want = (i == 0)
    print(f"{path}: pin {'ACCEPTS' if ok else 'REJECTS'} (expected {'ACCEPTS' if want else 'REJECTS'})")
    rc |= ok != want
sys.exit(rc)
