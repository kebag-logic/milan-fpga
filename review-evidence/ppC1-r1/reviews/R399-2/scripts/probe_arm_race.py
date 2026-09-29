#!/usr/bin/env python3
"""Disposable probe (R399-1): peer MSRP LeaveAll swept around the own MSRP
leavealltimer expiry, with the timer arm path either direct (as tb/srp_top) or
delayed two clocks (as protocol_processor_top's per-face arm queue: one push
edge plus one pop edge). Builds two copies of tb/srp_top from a pristine tree.
Usage: probe_arm_race.py <pristine tree> <work dir>"""
import pathlib, re, shutil, subprocess, sys

src, work = pathlib.Path(sys.argv[1]), pathlib.Path(sys.argv[2])

PROBE = r'''
  // R399 probe: peer LeaveAll swept across the MSRP expiry; count own actions
  void probe_arm_race() {
    uint32_t deadline=leaveall_setup(DECL_READY);
    until_ms(deadline-3); uint64_t mark=h.t;
    int guard=400;
    while(h.expiry_cycles.empty() && guard--) h.cycle();
    int phase=h.expiry_cycles.empty()?120:int(h.expiry_cycles[0]-mark);
    int bad=0;
    for(int delta=-80; delta<=2; delta++) {
      deadline=leaveall_setup(DECL_READY); until_ms(deadline-3);
      h.idle(phase-7+delta); size_t base=h.archive.size();
      h.feed(mrpdu_body(true,{la_only(4,4,false)}),true);
      h.run_ms(600);
      int rel=(h.expiry_cycles.empty()||h.peer_la_cycles.empty())?9999
              :int(h.peer_la_cycles[0])-int(h.expiry_cycles[0]);
      int own=leaveall_frames(h,base);
      bool rs=!h.peer_la_times.empty() && restarted(d->dbg_la_deadline_o,h.peer_la_times[0]);
      printf("ARMRACE delta=%d peer_minus_first_expiry=%d expiries=%zu actions=%zu own_la_frames=%d restarted=%d\n",
             delta,rel,h.expiry_cycles.size(),h.la_cycles.size(),own,int(rs));
      if(own||!h.la_cycles.empty()) bad++;
    }
    CHECK(bad==0,"PROBE: no own MSRP LeaveAll after a peer LeaveAll near the own expiry (%d offsets send one)",bad);
  }
'''

def make(variant, delay):
    t = work / variant
    if t.exists(): shutil.rmtree(t)
    (t / "tb").mkdir(parents=True)
    shutil.copytree(src / "hdl", t / "hdl")
    shutil.copytree(src / "tb" / "common", t / "tb" / "common")
    shutil.copytree(src / "tb" / "srp_top", t / "tb" / "srp_top",
                    ignore=shutil.ignore_patterns("obj_*"))
    cpp = t / "tb/srp_top/sim_main.cpp"
    s = cpp.read_text()
    s = s.replace("  // P: issue #108.", PROBE + "\n  // P: issue #108.", 1)
    s = s.replace('if (!*group || !strcmp(group,"join")) check_mvrp_join_before_the_stream();',
                  'if (!*group || !strcmp(group,"join")) check_mvrp_join_before_the_stream();\n'
                  '    if (!strcmp(group,"armrace")) probe_arm_race();', 1)
    s = s.replace('&& strcmp(group,"timers") && strcmp(group,"join")) return 2;',
                  '&& strcmp(group,"timers") && strcmp(group,"join") && strcmp(group,"armrace")) return 2;', 1)
    assert "probe_arm_race();" in s and '"armrace")) return 2' in s
    cpp.write_text(s)
    if delay:
        w = t / "tb/srp_top/srp_top_wrap.sv"
        v = w.read_text()
        for sig in ("valid", "cancel", "slot", "owner", "deadline"):
            v, n = re.subn(r"(\.arm_%s(?:_ms)?_o\s*\()arm_%s_w\)" % (sig, sig), r"\1arm_%s_p)" % sig, v)
            assert n == 1, sig
        stage = f'''
  // R399 probe: arm path delayed {delay} clocks (the top-level arm queue is 2 when idle)
  logic                    arm_valid_p, arm_cancel_p;
  logic [TB_SLOT_AW_C-1:0] arm_slot_p;
  logic [7:0]              arm_owner_p;
  logic [31:0]             arm_deadline_p;
  logic [{delay}-1:0]            dv_r;
  logic [{delay}-1:0][TB_SLOT_AW_C+40:0] dd_r;
  always_ff @(posedge clk_i) begin
    if (!rst_n) dv_r <= '0;
    else        dv_r <= {{dv_r, arm_valid_p}};
    dd_r <= {{dd_r, {{arm_cancel_p, arm_slot_p, arm_owner_p, arm_deadline_p}}}};
  end
  assign arm_valid_w = dv_r[{delay}-1];
  assign {{arm_cancel_w, arm_slot_w, arm_owner_w, arm_deadline_w}} = dd_r[{delay}-1];
'''
        v = v.replace("  KL_pp_timer_service #(", stage + "\n  KL_pp_timer_service #(", 1)
        w.write_text(v)
    return t

import os
DELAYS=[int(x) for x in os.environ.get("DELAYS","0,2").split(",")]
for variant, delay in [("direct" if d==0 else f"delay{d}", d) for d in DELAYS]:
    t = make(variant, delay)
    log = work / f"armrace-{variant}.log"
    with log.open("w") as f:
        rc = subprocess.run(["make", "-C", str(t / "tb/srp_top"), "RUN_ARGS=armrace"],
                            stdout=f, stderr=subprocess.STDOUT).returncode
    print(variant, "rc", rc)
