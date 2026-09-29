#!/usr/bin/env python3
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""Disposable probes of the KL_srp_top LeaveAll stale-expiry guard (R398-2).

Every probe works on a scratch export of a processor tree; nothing in the
source tree is written.

  wrap  : the timer service's ms timebase resets to BASE (near 2**32), so
          the DUT sees absolute time wrap during the srp_top scenarios. The
          wrapper hands the bench time relative to reset (now - BASE, and the
          two LeaveAll deadlines likewise), so the bench's own unsigned
          arithmetic stays valid. With --unsigned the guard's modular compare
          is replaced by a plain unsigned `now < deadline` (a non-wrap-safe
          control that the probe must be able to tell apart).
  drop  : the wrapper drops the second non-cancel arm of each LeaveAll slot
          after reset (the first is the startup arm), i.e. the re-arm that
          follows a received LeaveAll, as the processor top's arm queue does
          on overrun. A bench group 'dropprobe' feeds one peer MVRP and one
          peer MSRP LeaveAll before the own deadlines, then runs 60 s with no
          further peer LeaveAll and counts own LeaveAlls.

Usage:
  probe_guard.py wrap  --src TREE --work DIR --base HEX [--unsigned] GROUP...
  probe_guard.py drop  --src TREE --work DIR [--patch HDL.patch]
"""
import argparse
import shutil
import subprocess
import sys
from pathlib import Path

HDL = ["common/pp_pkg.sv", "srp/srp_pkg.sv", "common/KL_pp_prng.sv",
       "common/KL_pp_timer_service.sv", "packet_engine/KL_pp_tx_slots.sv",
       "srp/KL_srp_decoder.sv", "srp/KL_srp_domain.sv", "srp/KL_srp_vlan.sv",
       "srp/KL_srp_talker_fsm.sv", "srp/KL_srp_listener_fsm.sv",
       "srp/KL_srp_admission.sv", "srp/KL_srp_encoder.sv", "srp/KL_srp_top.sv"]


def sub1(text: str, old: str, new: str, what: str) -> str:
    """Replace exactly one occurrence or stop: a drifted anchor is no probe."""
    n = text.count(old)
    if n != 1:
        sys.exit(f"anchor '{what}' found {n} times")
    return text.replace(old, new)


def export(src: Path, work: Path) -> Path:
    if work.exists():
        shutil.rmtree(work)
    shutil.copytree(src / "hdl", work / "hdl")
    for suite in ("common", "srp_top"):
        shutil.copytree(src / "tb" / suite, work / "tb" / suite,
                        ignore=shutil.ignore_patterns("obj_*"))
    return work / "tb" / "srp_top"


def build(tb: Path, verilator: str) -> None:
    cmd = [verilator, "--cc", "--exe", "--build", "-j", "8",
           "--top-module", "srp_top_wrap", "-Wall", "-Wno-fatal",
           "-Wno-DECLFILENAME", "-Wno-UNUSEDSIGNAL", "-Wno-WIDTHEXPAND",
           "-Wno-WIDTHTRUNC", "-Wno-UNUSEDPARAM", "-CFLAGS",
           f"-std=c++17 -O2 -I{tb} -Wall -Wextra"]
    cmd += ["../../hdl/" + h for h in HDL] + ["srp_top_wrap.sv", "sim_main.cpp",
                                              "-o", "Vsrp_top_sim"]
    r = subprocess.run(cmd, cwd=tb, stdout=subprocess.PIPE,
                       stderr=subprocess.STDOUT, text=True)
    (tb / "build.log").write_text(r.stdout)
    if r.returncode:
        sys.exit(f"build failed rc={r.returncode}; see {tb / 'build.log'}")


def plant_wrap(tb: Path, base: int, unsigned: bool) -> None:
    root = tb.parents[1]
    ts = root / "hdl/common/KL_pp_timer_service.sv"
    t = ts.read_text()
    t = sub1(t, "now_ms_r <= 32'd0;", f"now_ms_r <= 32'h{base:08X};", "timer reset")
    ts.write_text(t)
    w = (tb / "srp_top_wrap.sv").read_text()
    # the DUT and the timer run on absolute time; the bench sees reset-relative
    w = sub1(w, "      .now_ms_i            (now_ms_o),",
             "      .now_ms_i            (now_abs_w),", "dut now")
    w = sub1(w, "      .now_ms_o          (now_ms_o),",
             "      .now_ms_o          (now_abs_w),", "timer now")
    w = sub1(w, "  assign dbg_la_deadline_o = u_dut.cad_dl_r[3];",
             f"  logic [31:0] now_abs_w;\n"
             f"  assign now_ms_o = now_abs_w - 32'h{base:08X};\n"
             f"  assign dbg_la_deadline_o = u_dut.cad_dl_r[3] - 32'h{base:08X};",
             "msrp deadline")
    w = sub1(w, "  assign dbg_la_mvrp_deadline_o = u_dut.cad_dl_r[4];",
             f"  assign dbg_la_mvrp_deadline_o = u_dut.cad_dl_r[4] - 32'h{base:08X};",
             "mvrp deadline")
    w = sub1(w, "    output logic [31:0] now_ms_o,", "    output wire [31:0] now_ms_o,",
             "now port kind")
    (tb / "srp_top_wrap.sv").write_text(w)
    if unsigned:
        top = root / "hdl/srp/KL_srp_top.sv"
        s = top.read_text()
        s = sub1(s, "                      || la_msrp_age_w[31];",
                 "                      || (now_ms_i < cad_dl_r[CAD_LA_MSRP_C]);", "msrp guard")
        s = sub1(s, "                      || la_mvrp_age_w[31];",
                 "                      || (now_ms_i < cad_dl_r[CAD_LA_MVRP_C]);", "mvrp guard")
        top.write_text(s)


DROP_SV = """
  // ---- probe: drop the second non-cancel arm of each LeaveAll slot ---------
  logic [1:0] prb_la_arms_r [0:1];
  logic       prb_drop_w;
  always_ff @(posedge clk_i) begin : prb_count
    if (!rst_n) begin
      prb_la_arms_r[0] <= 2'd0;
      prb_la_arms_r[1] <= 2'd0;
    end else if (arm_valid_w && !arm_cancel_w && (arm_slot_w == 5'd3 || arm_slot_w == 5'd4)) begin
      if (prb_la_arms_r[arm_slot_w == 5'd4] != 2'd3)
        prb_la_arms_r[arm_slot_w == 5'd4] <= prb_la_arms_r[arm_slot_w == 5'd4] + 2'd1;
    end
  end
  assign prb_drop_w = arm_valid_w && !arm_cancel_w && (arm_slot_w == 5'd3 || arm_slot_w == 5'd4)
                      && (prb_la_arms_r[arm_slot_w == 5'd4] == 2'd1);
  logic [31:0] prb_drops_r;
  always_ff @(posedge clk_i) begin : prb_drops
    if (!rst_n) prb_drops_r <= 32'd0;
    else if (prb_drop_w) prb_drops_r <= prb_drops_r + 32'd1;
  end
"""

DROP_CPP = r"""
  // probe (R398-2): peer LeaveAlls restart both timers; the wrapper drops
  // the re-arms; then no peer LeaveAll for 60 s.
  void probe_dropped_rearm() {
    leaveall_setup(DECL_READY);
    const uint32_t mdl = d->dbg_la_mvrp_deadline_o;
    const uint32_t sdl = d->dbg_la_deadline_o;
    const uint32_t first = mdl < sdl ? mdl : sdl;
    until_ms(first - 3000);
    const size_t base = h.archive.size();
    const uint32_t peer_at = d->now_ms_o;
    h.feed(peer_mvrp_leaveall(2), false);
    h.feed(mrpdu_body(true, {la_only(4, 4, false)}), true);
    h.run_ms(60000);
    printf("DROPPROBE peer_at=%u old_mvrp_dl=%u old_msrp_dl=%u new_mvrp_dl=%u new_msrp_dl=%u "
           "mvrp_expiries=%zu msrp_expiries=%zu own_mvrp_la_frames=%d own_msrp_la_frames=%d "
           "drops=%u now=%u\n",
           peer_at, mdl, sdl, (unsigned)d->dbg_la_mvrp_deadline_o, (unsigned)d->dbg_la_deadline_o,
           h.mvrp_expiry_cycles.size(), h.expiry_cycles.size(),
           mvrp_leaveall_frames(h, base), leaveall_frames(h, base),
           (unsigned)d->dbg_prb_drops_o, (unsigned)d->now_ms_o);
  }
"""


def plant_drop(tb: Path) -> None:
    w = (tb / "srp_top_wrap.sv").read_text()
    w = sub1(w, "  // ---- prng faces", DROP_SV + "\n  // ---- prng faces", "prng anchor")
    w = sub1(w, "      tmr_arm_valid_w = arm_valid_w;",
             "      tmr_arm_valid_w = arm_valid_w && !prb_drop_w;", "direct arm")
    w = sub1(w, "    output wire        dbg_mvrp_join_o,",
             "    output wire        dbg_mvrp_join_o,\n    output wire [31:0] dbg_prb_drops_o,",
             "port anchor")
    w = sub1(w, "  assign dbg_la_deadline_o = u_dut.cad_dl_r[3];",
             "  assign dbg_prb_drops_o = prb_drops_r;\n  assign dbg_la_deadline_o = u_dut.cad_dl_r[3];",
             "drops out")
    (tb / "srp_top_wrap.sv").write_text(w)
    c = (tb / "sim_main.cpp").read_text()
    c = sub1(c, "  void check_restart_across_arm_latency() {",
             DROP_CPP + "\n  void check_restart_across_arm_latency() {", "cpp anchor")
    c = sub1(c, '    if (!*group || !strcmp(group,"armdelay")) check_restart_across_arm_latency();',
             '    if (!strcmp(group,"dropprobe")) { probe_dropped_rearm(); }\n'
             '    if (!*group || !strcmp(group,"armdelay")) check_restart_across_arm_latency();',
             "dispatch")
    c = sub1(c, 'strcmp(group,"armdelay") && strcmp(group,"phases")',
             'strcmp(group,"armdelay") && strcmp(group,"dropprobe") && strcmp(group,"phases")',
             "group list")
    (tb / "sim_main.cpp").write_text(c)


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("mode", choices=["wrap", "drop"])
    ap.add_argument("--src", type=Path, required=True)
    ap.add_argument("--work", type=Path, required=True)
    ap.add_argument("--base", default="0")
    ap.add_argument("--unsigned", action="store_true")
    ap.add_argument("--verilator", default="verilator")
    ap.add_argument("--patch", type=Path, help="git-apply this HDL patch in the work tree first")
    ap.add_argument("groups", nargs="*")
    a = ap.parse_args()
    a.work = a.work.resolve()
    tb = export(a.src.resolve(), a.work)
    if a.patch:
        subprocess.run(["git", "apply", str(a.patch.resolve())], cwd=a.work, check=True)
    if a.mode == "wrap":
        plant_wrap(tb, int(a.base, 16), a.unsigned)
        groups = a.groups
    else:
        plant_drop(tb)
        groups = ["dropprobe"]
    build(tb, a.verilator)
    rc = 0
    for g in groups:
        r = subprocess.run(["./obj_dir/Vsrp_top_sim", g], cwd=tb, stdout=subprocess.PIPE,
                           stderr=subprocess.STDOUT, text=True)
        print(f"=== group {g} rc={r.returncode}")
        print(r.stdout)
        rc |= r.returncode
    return rc


if __name__ == "__main__":
    raise SystemExit(main())
