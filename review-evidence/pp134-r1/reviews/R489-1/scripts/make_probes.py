#!/usr/bin/env python3
"""Build disposable probe trees for the srp_top lvleave group (review R489-1).

Usage: make_probes.py <pristine-head-tree> <scratch-dir> <patch-out-dir>
Each probe is an exact-string edit of a copy of the head tree; the edit must
match exactly once or the script stops. The unified diff of every probe is
written to <patch-out-dir>/<name>.diff as a receipt.
"""
import difflib
import shutil
import sys
from pathlib import Path

TALKER = "hdl/srp/KL_srp_talker_fsm.sv"
TOP = "hdl/srp/KL_srp_top.sv"
SIM = "tb/srp_top/sim_main.cpp"

TRACE = """  // REVIEW PROBE (no behaviour change): registrar trace
  logic [N_SOURCES_P-1:0][1:0] probe_prev_r;
  always_ff @(posedge clk_i) begin : review_probe
    probe_prev_r <= reg_r;
    if (rst_n && arm_valid_o)
      $display("REGTRACE ms=%0d arm slot=%0d cancel=%0d deadline=%0d",
               now_ms_i, arm_slot_o, arm_cancel_o, arm_deadline_ms_o);
    for (int unsigned s = 0; s < N_SOURCES_P; s++) begin
      if (rst_n && reg_rx_hit_w[s] && (evt_mrp_event_i == 3'(SRP_EV_LV)))
        $display("REGTRACE ms=%0d src=%0d rx=Lv reg_at_rx=%0d", now_ms_i, s, reg_r[s]);
      if (rst_n && exp_hit_w && (exp_idx_w == s))
        $display("REGTRACE ms=%0d src=%0d leavetimer_expiry reg=%0d", now_ms_i, s, reg_r[s]);
      if (rst_n && (probe_prev_r[s] != reg_r[s]))
        $display("REGTRACE ms=%0d src=%0d reg %0d->%0d", now_ms_i, s, probe_prev_r[s], reg_r[s]);
    end
  end

  // --------------------------------------------------------- VLAN op plane
"""

LV_COMMENT = "          // LV: table 10-4 rLv on LV is -x- (the LeaveAll aging continues)\n"

PROBES = {
    # trace only; must pass 24/24 and show the registrar state at each Lv
    "trace": [(TALKER, "  // --------------------------------------------------------- VLAN op plane\n",
               TRACE)],
    # an Lv in LV restarts the leave timer (a plausible wrong reading)
    "lv-restarts-timer": [(TALKER, LV_COMMENT,
                           LV_COMMENT + "          if (reg_r[s] == R_LV_C) tpend_r[s] <= T_ARM_C;\n")],
    # an Lv in LV ends the registration at once (strict reading, no -x-)
    "lv-in-lv-ends-now": [(TALKER, LV_COMMENT,
                           LV_COMMENT + "          if (reg_r[s] == R_LV_C) reg_r[s] <= R_MT_C;\n")],
    # leave time 2 ms over the default: S2's window must reject it
    "leave-5002": [(TOP, "parameter int unsigned LEAVE_MS_P    = 5000,",
                    "parameter int unsigned LEAVE_MS_P    = 5002,")],
    # leave time 2 ms under the default: S1 and S2 must reject it
    "leave-4998": [(TOP, "parameter int unsigned LEAVE_MS_P    = 5000,",
                    "parameter int unsigned LEAVE_MS_P    = 4998,")],
    # the own LeaveAll no longer ages the Listener registrar
    "own-la-no-age": [(TALKER,
                       "assign leaveall_any_w = leaveall_rx_i[SRP_LA_LISTENER_C] || leaveall_own_i;",
                       "assign leaveall_any_w = leaveall_rx_i[SRP_LA_LISTENER_C];")],
    # a received Listener LeaveAll no longer ages the Listener registrar
    "peer-la-no-age": [(TALKER,
                        "assign leaveall_any_w = leaveall_rx_i[SRP_LA_LISTENER_C] || leaveall_own_i;",
                        "assign leaveall_any_w = leaveall_own_i;")],
    # harness probe: the bridge never sends either Lv (limit characterisation)
    "harness-no-lv": [
        (SIM, "        lr.vecs.push_back(Vec{false, 1, fv_sid(own_sid(target)), {EV_LV}, {fp}});\n", ""),
        (SIM, "        listener_event(target, EV_LV, fp);\n      }\n", "      }\n"),
        (SIM, "      const int lv2_reg = source_reg(target);\n      listener_event(target, EV_LV, fp);\n",
         "      const int lv2_reg = source_reg(target);\n"),
    ],
}


def main() -> int:
    head, scratch, out = (Path(a) for a in sys.argv[1:4])
    out.mkdir(parents=True, exist_ok=True)
    for name, edits in PROBES.items():
        tree = scratch / f"probe-{name}"
        if tree.exists():
            shutil.rmtree(tree)
        shutil.copytree(head / "hdl", tree / "hdl")
        shutil.copytree(head / "tb", tree / "tb")
        diffs = []
        for rel, old, new in edits:
            path = tree / rel
            text = path.read_text()
            if text.count(old) != 1:
                print(f"{name}: anchor not unique in {rel} ({text.count(old)})")
                return 1
            changed = text.replace(old, new)
            path.write_text(changed)
            diffs.extend(difflib.unified_diff(text.splitlines(True), changed.splitlines(True),
                                              "a/" + rel, "b/" + rel))
        (out / f"{name}.diff").write_text("".join(diffs))
        print(f"{name}: {tree}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
