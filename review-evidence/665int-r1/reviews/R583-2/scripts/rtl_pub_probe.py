#!/usr/bin/env python3
"""Reviewer RTL probes, not in the author's table: plant one defect into a copy
of hdl/milan/mailbox and build the mailbox suite against it through the
Wishbone adapter with the suite's own recipe (tb/verilator/mbx/mutants.py's
build_and_run). Usage: VERILATOR=... python3 -B rtl_pub_probe.py <repo> <scratch>"""
import shutil, sys
from pathlib import Path
repo, scratch = Path(sys.argv[1]), Path(sys.argv[2])
sys.path.insert(0, str(repo / "tb/verilator/mbx"))
import mutants  # noqa: E402
PROBES = [
    ("talker-decl-output-from-licence",
     "pub_talker_decl_o[MBX_N_PUB_SOURCES_C*i +: MBX_N_PUB_SOURCES_C] = MBX_N_PUB_SOURCES_C'(mbx_field_f(32'(pub_talker_decl_r[i])",
     "pub_talker_decl_o[MBX_N_PUB_SOURCES_C*i +: MBX_N_PUB_SOURCES_C] = MBX_N_PUB_SOURCES_C'(mbx_field_f(32'(pub_licence_r[i])"),
    ("started-gated-by-bound",
     "pub_started_o[MBX_N_PUB_SINKS_C*i + k] = mbx_field_f(32'(pub_binding_r[i][k]), MBX_BINDING_STARTED_LSB_C, MBX_BINDING_STARTED_WIDTH_C) != 0;",
     "pub_started_o[MBX_N_PUB_SINKS_C*i + k] = mbx_field_f(32'(pub_binding_r[i][k]), MBX_BINDING_STARTED_LSB_C, MBX_BINDING_STARTED_WIDTH_C) != 0 && pub_binding_r[i][k][0];"),
    ("idle-slope-written-from-sid-lo-offset",
     "if (!pub_sink_w && pub_reg_w == AW2_C'(MBX_PUB_REG_IDLE_SLOPE_C))",
     "if (pub_reg_w == AW2_C'(MBX_PUB_REG_IDLE_SLOPE_C))"),
]
for name, old, new in PROBES:
    work = scratch / name
    shutil.rmtree(work, ignore_errors=True)
    rtl = work / "rtl"
    shutil.copytree(repo / "hdl/milan/mailbox", rtl)
    top = rtl / "KL_mbx.sv"
    text = top.read_text()
    assert text.count(old) == 1, name
    top.write_text(text.replace(old, new))
    rc, out = mutants.build_and_run(rtl, work, 0)
    fails = [l for l in out.splitlines() if "[FAIL]" in l]
    print(f"{name:40} rc={rc} {'CAUGHT' if rc else 'ESCAPED'} {len(fails)} failed; first: {fails[0][:120] if fails else ''}")
