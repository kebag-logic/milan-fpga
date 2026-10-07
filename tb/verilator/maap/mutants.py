#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""Build each planted KL_maap defect of #686; require its named Annex B check to fail.

Every #686 item has at least one mutant: item 1 is B.2.1 (DEFEND destination,
control_data_length), item 2 B.3.4 (probe and announce timer draws, random
for every station MAC), item 3 B.3.2 Table B.7 notes b and d (ANNOUNCE
conflict detection), item 4 Table B.7 (four PROBEs, the first at once, the
ANNOUNCE at once). Each mutant is
an exact source replacement whose anchor must occur exactly once, applied to
a scratch copy: no checkout file is edited. A mutant counts as killed only
when its build succeeds, the harness exits 1, and the named check is among
its failures; a compiler error or abnormal exit never counts. A clean build
runs first as the positive control.
"""

import os
import signal
import subprocess
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
RTL = HERE / "../../../hdl/ieee1722/maap/KL_maap.sv"

BEGIN_TIMER = ("            timer_ms_r   <= '0;                 //! sProbe at once\n"
               "            state_r      <= PROBE_S;\n          end")
RESTART_TIMER = ("            timer_ms_r   <= '0;                 //! sProbe at once\n"
                 "            state_r      <= PROBE_S;\n            conflicts_o")
CELL = "((state_r == PROBE_S) || !mac_lower_w)"
SEED = "(mac_seed_w == 16'h0) ? 16'hACE1 : mac_seed_w"

#: (name, #686 item, anchor, replacement, the check that must fail)
MUTANTS = (
    ("cdl_28", 1, "CDL_C          = 8'd16;", "CDL_C          = 8'd28;",
     "B.2.1 cdl 16 (Begin! PROBE 1)"),
    ("defend_to_multicast", 1, "(tx_msg_r == MSG_DEFEND_C) ? tx_dst_r",
     "1'b0 ? tx_dst_r", "B.2.1 DEFEND DA = PROBE source (above)"),
    ("defend_destination_not_latched", 1, "? tx_dst_r\n", "? rx_src_r\n",
     "B.2.1 DEFEND DA latched at send"),
    ("every_frame_to_the_prober", 1, "(tx_msg_r == MSG_DEFEND_C) ? tx_dst_r",
     "1'b1 ? tx_dst_r", "B.2.1 PROBE DA multicast (Begin! 1)"),
    ("probe_draw_7_bits", 2, "{10'd0, lfsr_r[5:0]}", "{9'd0, lfsr_r[6:0]}",
     "B.3.4.2 probe T < 600 ms (campaign)"),
    ("probe_base_500", 2, "PROBE_MIN_MS_C    = 518;", "PROBE_MIN_MS_C    = 500;",
     "B.3.4.2 probe T > 500 ms (campaign)"),
    ("announce_base_3s", 2, "ANNOUNCE_MIN_MS_C = 30488;", "ANNOUNCE_MIN_MS_C = 3000;",
     "B.3.4.1 announce T > 30 s"),
    ("announce_draw_11_bits", 2, "{6'd0, lfsr_r[9:0]}", "{5'd0, lfsr_r[10:0]}",
     "B.3.4.1 announce T < 32 s"),
    ("announce_not_randomized", 2, "{6'd0, lfsr_r[9:0]}", "16'd512",
     "B.3.4.1 announce T randomized"),
    ("zero_seed_freezes_the_probe_draw", 2, SEED, "mac_seed_w",
     "B.3.4.2 probe T randomized (zero-seed MAC)"),
    ("zero_seed_freezes_the_announce_draw", 2, SEED, "mac_seed_w",
     "B.3.4.1 announce T randomized (zero-seed MAC)"),
    ("announce_judged_on_conflict_fields", 3,
     "rx_defend_w = (rx_msg_r == {2'b00, MSG_DEFEND_C});",
     "rx_defend_w = (rx_msg_r != {2'b00, MSG_PROBE_C});",
     "B.2.7 ANNOUNCE conflict_* is not its range"),
    ("inclusive_range_end", 3, "({1'b0, rx_start_r} < our_end_w)",
     "({1'b0, rx_start_r} <= our_end_w)", "note b adjacent above: no conflict"),
    ("inclusive_range_start", 3, "({1'b0, offset_r} < req_end_w);",
     "({1'b0, offset_r} <= req_end_w);", "note b adjacent below: no conflict"),
    ("empty_range_conflicts", 3, "rx_pool_r && (rx_cnt_r != 16'd0) && ", "rx_pool_r && ",
     "note b empty range: no conflict"),
    ("no_compare_mac", 3, CELL, "1'b1", "T.B7 note d: lower MAC keeps range"),
    ("compare_mac_while_probing", 3, CELL, "!mac_lower_w",
     "T.B7 rAnnounce!/PROBE: no compare_MAC"),
    ("compare_mac_unreversed", 3,
     "octet_rev = {m[7:0], m[15:8], m[23:16], m[31:24], m[39:32], m[47:40]};",
     "octet_rev = m;", "T.B7 rAnnounce!/DEFEND: re-address"),
    ("three_probes", 4, "PROBE_SENDS_C  = 4;", "PROBE_SENDS_C  = 3;",
     "T.B7 Begin!: four PROBEs before ANNOUNCE"),
    ("first_probe_after_a_timer", 4, BEGIN_TIMER,
     BEGIN_TIMER.replace("<= '0;", "<= probe_iv_w;"), "T.B7 Begin!: first PROBE at once"),
    ("restart_probe_after_a_timer", 4, RESTART_TIMER,
     RESTART_TIMER.replace("<= '0;", "<= probe_iv_w;"), "T.B7 Restart!: first PROBE at once"),
    ("announce_after_a_timer", 4, "                timer_ms_r <= '0;\n",
     "                timer_ms_r <= announce_iv_w;\n",
     "T.B7 probeCount!: ANNOUNCE at once (Begin!)"),
    ("restart_rewrites_the_frame_on_the_wire", 3,
     "f[30] = tx_off_r[15:8]; f[31] = tx_off_r[7:0];",
     "f[30] = offset_r[15:8]; f[31] = offset_r[7:0];", "frame on the wire keeps its offset"),
    ("overlap_count_to_our_end", 1, "16'(conf_end_w - {1'b0, conf_start_w})",
     "16'(our_end_w - {1'b0, conf_start_w})", "B.2.8 conflict_count = overlap (below)"),
)


def run_case(work: Path, name: str, source: str, failure: str | None) -> bool:
    """A compiler error or abnormal termination never counts as a kill."""
    rtl = work / f"{name}.sv"
    rtl.write_text(source)
    mdir = work / f"obj_{name}"
    result = subprocess.run(
        ["make", "-s", "-C", str(HERE), "build", f"MAAP_RTL={rtl}", f"MDIR={mdir}",
         f"VERILATOR={os.environ.get('VERILATOR', 'verilator')}",
         f"VERILATOR_JOBS={os.environ.get('VERILATOR_JOBS', '0')}"],
        capture_output=True, text=True, check=False)
    if result.returncode:
        print(result.stdout[-2000:] + result.stderr[-2000:])
        print(f"[ESCAPED] {name}: compilation failed")
        return False
    result = subprocess.run([str(mdir / "VKL_maap_sim")],
                            capture_output=True, text=True, check=False)
    output = result.stdout + result.stderr
    if failure is None:
        passed = result.returncode == 0 and " 0 failures" in output
    else:
        passed = result.returncode == 1 and f"[FAIL] {failure}" in output
    print(f"[{'ok' if passed else 'ESCAPED'}] {name}: rc={result.returncode}", flush=True)
    if passed and failure is not None:
        # The sweep judges this campaign's verdict, not expected DUT failures.
        print(f"  named rejection: {failure}")
    elif not passed:
        print(output)
    return passed


def main() -> int:
    """Run the clean control and every mutant; fail if any defect escapes."""
    def interrupted(_signum: int, _frame: object) -> None:
        """Unwind temporary storage when the caller stops the campaign."""
        raise SystemExit(143)

    signal.signal(signal.SIGTERM, interrupted)
    source = RTL.read_text()
    items = {item for _, item, _, _, _ in MUTANTS}
    if items != {1, 2, 3, 4}:
        print(f"[ESCAPED] campaign: #686 items without a mutant: {sorted({1, 2, 3, 4} - items)}")
        return 1
    with tempfile.TemporaryDirectory(prefix="maap-mutants-") as directory:
        work = Path(directory)
        results = [run_case(work, "clean", source, None)]
        if not results[0]:
            return 1
        for name, _, anchor, replacement, failure in MUTANTS:
            if source.count(anchor) != 1:
                print(f"[ESCAPED] {name}: expected exactly one mutation anchor")
                results.append(False)
                continue
            results.append(run_case(work, name, source.replace(anchor, replacement), failure))
    failures = sum(not passed for passed in results)
    print(f"== maap mutants: checks: {len(results)}   failures: {failures} ==")
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
