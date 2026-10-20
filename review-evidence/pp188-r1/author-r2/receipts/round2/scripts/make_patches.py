#!/usr/bin/env python3
"""Write the round-2 srp_top control patches: usage make_patches.py <repo>."""
import difflib, sys
from pathlib import Path
repo = Path(sys.argv[1])
T = 'hdl/srp/KL_srp_listener_fsm.sv'
ARMS = {
 'listener-csid-ram-ignores-park': (
  "    assign csid_w = lvp_r[ctl_sink_i] ? lsid_r[ctl_sink_i]\n"
  "                                      : wsid_r[ctl_sink_i];\n",
  "    assign csid_w = wsid_r[ctl_sink_i];\n"),
 'listener-csid-flops-ignores-park': (
  "    assign csid_w = lvp_r[ctl_sink_i] ? lsid_r[ctl_sink_i]\n"
  "                                      : sid_r[ctl_sink_i];\n",
  "    assign csid_w = sid_r[ctl_sink_i];\n"),
 'listener-rebind-back-keeps-park': (
  "          lvp_r[ctl_sink_i]       <= set_owes_w && !set_same_w;\n",
  "          lvp_r[ctl_sink_i]       <= (set_owes_w && !set_same_w) || lvp_r[ctl_sink_i];\n"),
 'listener-lo-not-owed': (
  "    set_owes_w = set_lv_w inside {A_LA_C, A_LO_C};\n",
  "    set_owes_w = (set_lv_w == A_LA_C);\n"),
 'listener-park-retires-on-txla': (
  "          if (walk_grant_w && lvp_r[wsrc_r]\n"
  "              && !(wnext_w inside {A_LA_C, A_LO_C})) begin\n",
  "          if (walk_grant_w && lvp_r[wsrc_r]) begin\n"),
 'listener-unrecorded-applicant-owes': (
  "    set_lv_w   = rec_valid_r[ctl_sink_i]\n"
  "               ? app_next_f(app_r[ctl_sink_i], AE_LV_C, 1'b0, p2p_i) : A_VO_C;\n",
  "    set_lv_w   = app_next_f(app_r[ctl_sink_i], AE_LV_C, 1'b0, p2p_i);\n"),
 'listener-aa-tx-stays-aa': (
  "          A_AN_C:  nx = reg_in_i ? A_QA_C : A_AA_C;   // note 8\n"
  "          A_AA_C:  nx = A_QA_C;\n",
  "          A_AN_C:  nx = reg_in_i ? A_QA_C : A_AA_C;   // note 8\n"
  "          A_AA_C:  nx = A_AA_C;\n"),
 'listener-parked-applies-rx': (
  "                     && !lvp_r[s]   // neither stream's values while parked\n", ""),
}
src = (repo / T).read_text()
for name, (old, new) in ARMS.items():
    assert src.count(old) == 1, (name, src.count(old))
    dst = src.replace(old, new)
    text = ''.join(difflib.unified_diff(src.splitlines(keepends=True), dst.splitlines(keepends=True),
                                        'a/' + T, 'b/' + T, n=3))
    text = '\n'.join(l.rstrip(' \t') if l.startswith(('---', '+++')) else l for l in text.split('\n'))
    (repo / 'tb/srp_top/mutations' / (name + '.patch')).write_text(text)
    print(name)
