#!/usr/bin/env python3
"""Reviewer probes (R458-3): one exact edit each on a copy of hdl/srp.
usage: make_probes.py <hdl/srp at the head> <outdir>; each edit must match exactly once."""
import shutil, sys
from pathlib import Path
SRC, OUT = Path(sys.argv[1]), Path(sys.argv[2])
PROBES = [
    # talker walk record written on an offered (not accepted) gate open
    ("r3-wtsp-write-ignores-ready", "KL_srp_talker_fsm.sv",
     "  assign gate_open_acc_w = rst_n && gate_acc_w && gate_open_i;",
     "  assign gate_open_acc_w = rst_n && gate_valid_i && gate_open_i;"),
    # listener walk stream_id written on an offered (not accepted) settle
    ("r3-wsid-write-ignores-ready", "KL_srp_listener_fsm.sv",
     "      if (rst_n && ctl_acc_w && ctl_settle_i) begin",
     "      if (rst_n && ctl_valid_i && ctl_settle_i) begin"),
    # talker walk TSpec read through a register (block-RAM-style latency)
    ("r3-wtsp-registered-read", "KL_srp_talker_fsm.sv",
     "  assign wtsp_w = wtsp_r[wsrc_r];",
     "  always_ff @(posedge clk_i) wtsp_w <= wtsp_r[wsrc_r];"),
    # listener walk stream_id read through a register, RAM arm only
    ("r3-wsid-registered-read", "KL_srp_listener_fsm.sv",
     "    assign wsid_w = wsid_r[wsrc_r];",
     "    always_ff @(posedge clk_i) wsid_w <= wsid_r[wsrc_r];"),
]
for name, f, old, new in PROBES:
    d = OUT / name
    if d.exists(): shutil.rmtree(d)
    shutil.copytree(SRC, d)
    t = (d / f).read_text()
    assert t.count(old) == 1, (name, t.count(old))
    (d / f).write_text(t.replace(old, new))
    print(name, f)
