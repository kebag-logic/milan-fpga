#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""Build each named mutant of KL_aaf_clock_meter and require its named check to fail.

The mutants are the ones docs/design/MEDIA_CLOCK_FOLLOWING.md's test plan
names for the meter rows (#629). Each is a set of exact source replacements,
every anchor required to occur exactly once, applied to a scratch copy: no
checkout file is edited. A mutant counts as killed only when its build
succeeds, the harness exits 1 with RESULT: FAIL, and the named check is among
the failures; a compiler error or abnormal exit never counts. A clean build
of the same recipe runs first, as the positive control.
"""

import os
import signal
import subprocess
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
RTL = HERE / "../../../hdl/ieee1722/crf/KL_aaf_clock_meter.sv"

#: (name, ((anchor, replacement), ...), harness case, the check it must fail)
MUTANTS = (
    ("decimation_by_1",
     (("        if (s2_tu_edge_w) pdu_restart_r <= 1'b1;\n      end",
       "        if (s2_tu_edge_w) pdu_restart_r <= 1'b1;\n"
       "        pc_v_r <= 1'b1; pc_ts0_r <= s2_ts_r; pc_sum_r <= '0;"
       " pc_id_r <= s2_gid_w;\n      end"),),
     "rates", "[M1 +0.00 ppm] rate_valid rises within 4.2 s and holds"),
    ("rate_over_512ms_E1",
     (("g_snap_old_r <= ring_r[ring_idx_r];",
       "g_snap_old_r <= ring_r[ring_idx_r - 1'b1];"),
      ("g_snap_old_r - NOM_SPAN_NS_C);", "g_snap_old_r - NOM_SNAP_NS_C);"),
      ("rate_ns_o    <= g_rdiff_r >>> RING_LOG2_C;", "rate_ns_o    <= g_rdiff_r;")),
     "shapes", "[M2 rsign] every rate within 360 ns of the planted rate"),
    ("bound_2048_B1",
     (("1 << $clog2(2 * TS_ERR_NS_C + DRIFT_NS_C);", "2048;"),),
     "shapes", "[M2 indep] no history restart"),
    ("first_pdu_pick_P1",
     (("g_pick_r <= pc_ts0_r + 32'(pc_sum_r >>> GRP_LOG2_C);", "g_pick_r <= pc_ts0_r;"),),
     "shapes", "[M2 indep] every rate within 256 ns of the planted rate"),
    ("spacing_bound_16384_B3",
     (("? 32'(GAP_NS_C) : 32'(JUMP_NS_C);", "? 32'(GAP_NS_C) : 32'd16384;"),),
     "beyond", "[M3 rsign1800] the error restarts the history"),
    ("within_group_void_removed",
     (("wire        s2_in_bound_w = (s2_dev_r <= $signed(32'(JUMP_NS_C)))\n"
       "                           && (s2_dev_r >= -$signed(32'(JUMP_NS_C)));",
       "wire        s2_in_bound_w = 1'b1;"),),
     "beyond", "[M3 indep2100] the error restarts the history"),
    ("stream_data_length_unchecked",
     (("\n               && (f_sdl_w == 16'(32'(f_cpf_w) * PDU_OCTETS_PER_CH_C));", ";"),),
     "format", "[M4 12-sample] does not lock"),
    ("continuity_without_wrap",
     (("g_k_r     <= g_id_r - last_id_r;",
       "g_k_r     <= (g_id_r < last_id_r) ? 4'd0 : g_id_r - last_id_r;"),),
     "wrap", "[M5] zero restarts across the sequence wraps"),
    ("timeout_disabled",
     (("wire tout_fire_w = en_w && (tout_r == TOUTW_C'(TOUT_CYC_C));",
       "wire tout_fire_w = 1'b0;"),),
     "lock", "[M6] unlocks 100 ms after the last PDU"),
    ("no_restart_on_tu_edge",
     (("wire        s2_tu_edge_w = tu_seeded_r && (s2_tu_r != prev_tu_r);",
       "wire        s2_tu_edge_w = 1'b0;"),),
     "restarts", "[M7 tu edge] rate_valid falls at the event"),
    ("restart_on_any_loss",
     (("if (s2_tu_edge_w) pdu_restart_r <= 1'b1;",
       "if (s2_tu_edge_w || s2_gap_r) pdu_restart_r <= 1'b1;"),),
     "loss_periodic", "[M8 indep 1 s] rate_valid from 4.1 s on and never falls"),
    ("snapshot_next_pick_less_2ms",
     (("g_mid_r <= last_pick_r + {g_diff_r[31], g_diff_r[31:1]};",
       "g_mid_r <= last_pick_r + g_diff_r - 32'(GRP_NS_C);"),),
     "loss_snapshot", "[M9] every rate equals the no-loss run within 1 LSB"),
    ("voided_snapshot_restarts",
     (("      if (g_first_r || !g3_sp_ok_w) begin\n        ring_we_w = 1'b1;",
       "      if (g_first_r || !g3_sp_ok_w || g3_snap_mid_w) begin\n        ring_we_w = 1'b1;"),
      ("        if (g_first_r || !g3_sp_ok_w) begin\n          //! a new history",
       "        if (g_first_r || !g3_sp_ok_w || g3_snap_mid_w) begin\n"
       "          //! a new history")),
     "loss_snapshot", "[M9] no history restart"),
    ("multi_group_gap_accepted",
     (("wire        g3_k_ok_w    = (g_k_r == 4'd1) || (g_k_r == 4'd2);",
       "wire        g3_k_ok_w    = (g_k_r != 4'd0);"),
      ("- ((g_k_r == 4'd2) ? 32'(2 * GRP_NS_C) : 32'(GRP_NS_C)));",
       "- 32'(32'(g_k_r) * GRP_NS_C));"),
      ("wire [31:0] g3_bound_w   = (g_k_r == 4'd2) ?",
       "wire [31:0] g3_bound_w   = (g_k_r >= 4'd2) ?")),
     "bound", "[M10 two losses in adjacent groups] restarts once"),
    ("gap_bound_4096",
     (("localparam int unsigned GAP_NS_C    = 5120;",
       "localparam int unsigned GAP_NS_C    = 4096;"),),
     "gap_value", "[M11 a] +3,900 ns at +300 ppm, 5,100 ns from 4 ms: no restart"),
    ("gap_bound_scaled_with_k",
     (("? 32'(GAP_NS_C) : 32'(JUMP_NS_C);", "? 32'(2 * JUMP_NS_C) : 32'(JUMP_NS_C);"),),
     "gap_value", "[M11 b] half sample at -300 ppm against +/-J, 6,365 ns off: one restart"),
    ("no_check_across_a_gap",
     (("wire        g3_sp_ok_w   = g3_k_ok_w && ($signed(g_sp_r) <= $signed(g3_bound_w))\n"
       "                                       && ($signed(g_sp_r) >= -$signed(g3_bound_w));",
       "wire        g3_sp_ok_w   = g3_k_ok_w && ((g_k_r == 4'd2) ||\n"
       "    (($signed(g_sp_r) <= $signed(g3_bound_w)) && ($signed(g_sp_r) >= -$signed(g3_bound_w))));"),),
     "step_in_gap", "[M12 PDU 0 lost, step +20833 @1] restarts the history once"),
    ("listener_compare_ignored",
     (("(match_idx_i == follow_idx_i) && !stopped_w", "1'b1 && !stopped_w"),),
     "selection", "[M13 another listener] not measured"),
    ("no_reseed_at_era_start",
     (("        mr_seeded_r  <= 1'b0;\n        tu_seeded_r  <= 1'b0;\n",
       "        tu_seeded_r  <= 1'b0;\n"),),
     "pulses", "[M14 listener change to the opposite mr level] mr_toggle_p pulses"),
    ("era_lock_clear_on_disrupt",
     (("      if (tout_fire_w && locked_o) begin",
       "      if ((tout_fire_w || lock_clr_w) && locked_o) begin"),),
     "pulses", "[M14 listener change to the opposite mr level] disrupt_p pulses"),
    ("disrupt_tied_low",
     (("disrupt_p_o <= 1'b1;               //! the ONE disruption pulse",
       "disrupt_p_o <= 1'b0;"),),
     "pulses", "[M14 100 ms of silence] disrupt_p pulses"),
    ("enable_tied_high",
     (("  wire               en_w = en_i;", "  wire               en_w = 1'b1;"),),
     "pulses", "[M14 enable low, talker 0 toggling its mr] mr_toggle_p pulses"),
)


def build(work: Path, name: str, source: str) -> Path | None:
    """Build the harness against `source`; None when the build fails."""
    rtl = work / f"{name}.sv"
    rtl.write_text(source)
    mdir = work / f"obj_{name}"
    result = subprocess.run(
        ["make", "-s", "-C", str(HERE), "build", f"METER_RTL={rtl}", f"MDIR={mdir}",
         f"VERILATOR={os.environ.get('VERILATOR', 'verilator')}",
         f"VERILATOR_JOBS={os.environ.get('VERILATOR_JOBS', '0')}"],
        capture_output=True, text=True, check=False)
    if result.returncode:
        print(result.stdout[-2000:] + result.stderr[-2000:])
        print(f"FAIL {name}: compilation failed")
        return None
    return mdir / "Vmeter_sim"


def run_case(exe: Path, name: str, case: str, failure: str | None) -> bool:
    """A clean control passes; a mutant must fail by its named check."""
    result = subprocess.run([str(exe), case], capture_output=True, text=True, check=False)
    output = result.stdout + result.stderr
    if failure is None:
        passed = result.returncode == 0 and "RESULT: PASS" in output
    else:
        passed = (result.returncode == 1 and "RESULT: FAIL" in output and
                  f"[FAIL] {failure}" in output)
    print(f"[{'PASS' if passed else 'FAIL'}] {name} ({case}): rc={result.returncode}")
    if passed and failure is not None:
        # The sweep judges this campaign's verdict, not the expected DUT failure.
        print(f"  named rejection: {failure}")
    elif not passed:
        print(output[-4000:])
    return passed


def mutate(source: str, edits: tuple[tuple[str, str], ...]) -> str | None:
    """Apply every edit, each anchor exactly once; None when one is not."""
    for anchor, replacement in edits:
        if source.count(anchor) != 1:
            return None
        source = source.replace(anchor, replacement)
    return source


def main() -> int:
    """Run the clean control and every mutant; fail if any defect escapes."""
    def interrupted(_signum: int, _frame: object) -> None:
        """Unwind temporary storage when the caller stops the campaign."""
        raise SystemExit(143)

    signal.signal(signal.SIGTERM, interrupted)
    source = RTL.read_text()
    results = []
    with tempfile.TemporaryDirectory(prefix="aaf-meter-mutants-") as directory:
        work = Path(directory)
        clean = build(work, "clean", source)
        results.append(clean is not None and run_case(clean, "clean", "selection", None))
        for name, edits, case, failure in MUTANTS:
            mutated = mutate(source, edits)
            if mutated is None:
                print(f"FAIL {name}: expected exactly one occurrence of every mutation anchor")
                results.append(False)
                continue
            exe = build(work, name, mutated)
            results.append(exe is not None and run_case(exe, name, case, failure))
    failures = sum(not passed for passed in results)
    print(f"aaf_clock_meter mutants: {len(results) - failures}/{len(results)} as required")
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
