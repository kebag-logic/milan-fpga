#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""Negative controls for the #387/#602 gmstep and option-off checks.

The #602 ruling excludes PHC-only causes from outgoing mr and MEDIA_RESET.
The clean gmstep leg must still grade tu holdover, continuous transport and,
since #632, a render presentation stage that takes no re-base: the PDUs
stamped across the two steps are refused and counted, and every other PDU
keeps its offset. Real source changes and selected-CRF received mr must
still propagate. Each control rebuilds the same harness against a
disposable source copy through the Makefile and must fail its named check.
A compile error, crash or missing harness verdict is not a catch. The clean
leg is rebuilt if older than its inputs and must pass first.

The default inventory restores the PHC restart term, removes the source
change or CRF propagation, or empties the render stage on the grandmaster's
identity or on the step: #632 retired #387's counted render re-base, so what
the two render controls now plant is that re-base's effect on the queue, and
each must lose PDUs the clean leg presents, uncounted. The explicit --all campaign also
grades the existing holdover, continuity, render-refusal and slew controls,
and restores either PHC cause separately on the INTERNAL option-off leg.
It also restores both PHC causes together and vetoes a genuine CRF request
on the very cycle a software settime re-bases the PHC.
Delayed adjtime causes at 16 and 256 cycles must fail only the adjtime check.

The recipe, the harness and the generated images the legs read belong to
tb/verilator/milan_dp; this driver builds and runs them there. With
--no-small-steps every gmstep run, the positive control's included, leaves
out the #621 small-step phase and nothing else. The sweep runs its controls
that way: none of their named checks is in that phase, and the suite runs
the clean leg once with it. The explicit campaigns run the whole leg.

What bounds a run. This driver sets no host-time deadline (rule 8's
wall-clock ratchet, scripts/test_evidence.budget item 4). The leg is
cycle-bounded by construction: every phase runs a fixed cycle count, every
AXI4-Lite and AECP wait gives up after a fixed cycle count, and no loop waits
on a DUT output without a cycle bound, so a control ends at the same cycle as
the clean leg. The host-time bound of the default run is the sweep's
per-suite guard in scripts/run_all_suites.sh; the SIGTERM handler turns that
kill into an exit that removes the temporary directory.

Usage: python3 gmstep_mutants.py [--all | --slew] [--no-small-steps]
(run from tb/verilator/milan_dp_gm_steps)
Exit 0 = every control was caught and the clean leg still passes.
"""

import argparse
import signal
import subprocess
import sys
import tempfile
from pathlib import Path
from typing import NamedTuple

HERE = Path(__file__).resolve().parent
#: the suite that owns both legs' recipes and harnesses, and the run directory
#: of their binaries: they read the generated ROM images there
DP = HERE.parent / "milan_dp"
SOURCES = {
    "datapath": HERE / "../../../hdl/milan/milan_datapath.sv",
    "clkv": HERE / "../../../hdl/ieee8021as/ptp_timestamp/KL_ptp_clock_validity.sv",
    "stage": HERE / "../../../hdl/ieee1722/aaf/KL_render_queue.sv",
    "restart": HERE / "../../../hdl/ieee1722/avtp/KL_media_clock_restart.sv",
}
#: the make variable that points the recipe at each source
MAKE_VAR = {"datapath": "DP_SRC", "clkv": "CLKV_SRC", "stage": "RQ_SRC", "restart": "MCR_SRC"}
sys.path.insert(0, str(HERE / "../../../scripts"))
from suite_tally import log_reports_failure  # noqa: E402

#: the render presentation stage's flush: the bind wipe, and nothing else
#: (#632). The render controls OR a re-base cause into it.
RENDER_FLUSH = "    .flush_i      (strtbl_bind_fall_w),"
#: what #387's re-base pulse read, the PHC's two strobes (#632 retired the
#: wire with the setpoint stage); the restart controls restore it as a term
PHC_REBASE = "(eff_ptp_adjust_w | cfg_ptp_cmd_load)"
#: the restart request's last line: a control that appends " | <cause>" to it
#: ORs the cause into the whole request (#629 added the AAF meter's two terms
#: after the CRF ones, so the request ends here)
RESTART_TRIGGER = "       | aafm_disrupt_p_w | aafm_mr_toggle_p_w;"
#: the selected CRF stream's two terms, the disruption and the received toggle:
#: a control that ANDs a veto into the CRF restart plants it inside this group,
#: since on RESTART_TRIGGER the `&` binds to the AAF toggle alone
CRF_RESTART_TERMS = "        & ((tkd_crflk_q_r & ~crf_locked_w) | crf_mr_toggle_p_w))"
RESTART_DECL = ("  wire mcr_restart_p_w /* verilator public_flat_rd */ =\n"
                "       (crf_clk_selected_r\n" + CRF_RESTART_TERMS + "\n" + RESTART_TRIGGER)
TALKER_GATE = "  assign aaf_stream_en_w = aaf_stream_en_raw_w & ~amap_edit_out_resv_r;"


class Leg(NamedTuple):
    """One elaboration a control can be graded on, built by its own recipe."""

    target: str                 #: the make target that builds it alone
    mdir_var: str               #: the make variable naming its build directory
    clean_mdir: Path            #: where the sweep builds the clean leg
    exe_name: str
    harness: str                #: its C++ harness, an input of the recipe
    takes_aem: bool             #: it reads the AEM image beside its binary
    short_flag: str = ""        #: what --no-small-steps passes it, if anything


LEGS = {
    "gmstep": Leg("gmstep-build", "GMSTEP_MDIR", DP / "obj_gmstep",
                  "Vmilan_dp_gmstep", "sim_gmstep.cpp", True, "--no-small-steps"),
    "option-off": Leg("option-off-build", "OPTOFF_MDIR", DP / "obj_dir",
                      "Vmilan_dp_sim", "sim_main.cpp", False),
}


class Control(NamedTuple):
    """One planted defect and the check it must break."""

    name: str
    source: str                 #: a key of SOURCES
    anchor: str                 #: the text it replaces, exactly once
    replacement: str
    breaks: str                 #: the named check that must fail
    acceptance: bool            #: named by #387/#602 acceptance: runs by default
    leg: str = "gmstep"         #: a key of LEGS
    stays_clean: tuple[str, ...] = ()  #: sibling checks this cause must not break


# The counter input is delayed independently of the slew-level release.
COUNTER_ADDEND_PORT = """  timestamp_counter #(
    .COUNTER_WIDTH (64),
    .INCR_WIDTH    (32),
    .FRAC_WIDTH    (24),
    .PPS_P             (PPS_P),
    .PPS_WIDTH_CYC_P (PPS_WIDTH_CYC_P)
  ) ts_counter (
    .clk                  (gtx_clk),
    .resetn               (gtx_resetn),
    .enable_i             (phc_enable_ts_w),
    .incr_i               (phc_incr_ts_w),
    .adj_i                (phc_adj_ts_w),"""

CONTROLS = [
    Control("the policy level is tied low at the servo", "datapath",
            ".phc_slew_active_i (gptp_slew_eff_w)",
            ".phc_slew_active_i (1'b0)",
            "slew path: the actual servo receives the level", False),
    Control("the policy level omits the applied-rate tail", "datapath",
            "gptp_slew_active_w || (|gptp_slew_tail_r)",
            "gptp_slew_active_w",
            "slew path: every staged sample covers the PHC tail", False),
    Control("the policy level misses an extra addend stage", "datapath",
            COUNTER_ADDEND_PORT,
            "  logic [31:0] probe_adj_r;\n"
            "  always_ff @(posedge gtx_clk) begin : probe_addend_delay\n"
            "    if (!gtx_resetn) probe_adj_r <= '0;\n"
            "    else probe_adj_r <= phc_adj_ts_w;\n"
            "  end : probe_addend_delay\n" +
            COUNTER_ADDEND_PORT.replace("(phc_adj_ts_w)", "(probe_adj_r)"),
            "slew path: every staged sample covers the PHC tail", False),
    Control("the PHC re-base restart term is restored", "datapath",
            RESTART_TRIGGER,
            RESTART_TRIGGER[:-1] + " | " + PHC_REBASE + ";",
            "restart: a PHC-only step leaves outgoing mr unchanged", True),
    Control("the source-change term is removed", "restart",
            "src_change_w = (clk_src_q_r != clk_src_i);",
            "src_change_w = 1'b0;",
            "source control: a real source change toggles mr once", True),
    Control("selected CRF mr propagation is removed", "datapath",
            CRF_RESTART_TERMS,
            "        & (tkd_crflk_q_r & ~crf_locked_w))",
            "CRF control: selected CRF mr propagates exactly once", True),
    Control("the grandmaster identity empties the render stage", "datapath",
            RENDER_FLUSH,
            "    .flush_i      (strtbl_bind_fall_w | {N_STREAMS{gm_recentre_p_r}}),",
            "render: every PDU not presented was refused by the stage and counted once", True),
    Control("the step empties the render stage", "datapath",
            RENDER_FLUSH,
            "    .flush_i      (strtbl_bind_fall_w | {N_STREAMS{eff_ptp_adjust_w}}),",
            "render: every PDU not presented was refused by the stage and counted once", True),
    Control("the refused PDUs are not counted", "stage",
            "      if (c_early_w   && !(&early_o))   early_o   <= early_o + 16'd1;",
            "      if (1'b0        && !(&early_o))   early_o   <= early_o + 16'd1;",
            "render: every PDU not presented was refused by the stage and counted once", False),
    Control("tu reaches the talkers four cycles late", "clkv",
            "  assign ts_uncertain_o = (~sync_ok_w) | hold_w | disc_p_w;",
            "  logic [3:0] tu_late_r;\n"
            "  always_ff @(posedge clk_i) begin : p_tu_late\n"
            "    tu_late_r <= {tu_late_r[2:0], (~sync_ok_w) | hold_w | disc_p_w};\n"
            "  end : p_tu_late\n"
            "  assign ts_uncertain_o = tu_late_r[3];",
            "tu: set in the first cycle the bank names GM B", False),
    Control("the plane's step does not re-arm the holdover", "datapath",
            "                   ? gptp_step_we_w : cfg_ptp_cmd_adjust),",
            "                   ? 1'b0 : cfg_ptp_cmd_adjust),",
            "tu: held at least the 0.25 s holdover after the step", False),
    Control("tu stops the talker", "datapath", TALKER_GATE,
            "  assign aaf_stream_en_w = aaf_stream_en_raw_w & ~amap_edit_out_resv_r"
            " & ~clkv_tu_w;",
            "licence: the talker never pauses beyond four of its intervals", False),
    Control("the grandmaster change stops the talker for good", "datapath", TALKER_GATE,
            "  logic gm_stop_r;\n"
            "  always_ff @(posedge axis_clk) begin : p_gm_stop\n"
            "    if (!axis_resetn) gm_stop_r <= 1'b0;\n"
            "    else if (gm_recentre_p_r) gm_stop_r <= 1'b1;\n"
            "  end : p_gm_stop\n"
            "  assign aaf_stream_en_w = aaf_stream_en_raw_w & ~amap_edit_out_resv_r"
            " & ~gm_stop_r;",
            "licence: the talker never pauses beyond four of its intervals", False),
    Control("a gap in the presented frames leaves no counted slip", "stage",
            "      if (rd0_end_w && !any_w && (32'(rs_r) == s) && live_r[s]) gap_w = 1'b1;",
            "      if (rd0_end_w && !any_w && (32'(rs_r) == s) && live_r[s]) gap_w = 1'b0;",
            "render: the refused PDUs' frames are one counted slip", False),
    Control("software settime is restored as an mr cause", "datapath",
            RESTART_TRIGGER,
            RESTART_TRIGGER[:-1] + " | cfg_ptp_cmd_load;",
            "CLKV: the settime leaves mr unchanged (#602)", False, "option-off",
            ("CLKV: PHC-only steps leave INTERNAL mr unchanged (#602)",)),
    Control("PHC adjtime is restored as an mr cause", "datapath",
            RESTART_TRIGGER,
            RESTART_TRIGGER[:-1] + " | eff_ptp_adjust_w;",
            "CLKV: PHC-only steps leave INTERNAL mr unchanged (#602)", False,
            "option-off", ("CLKV: the settime leaves mr unchanged (#602)",)),
    Control("both PHC restart causes are restored", "datapath",
            RESTART_TRIGGER,
            RESTART_TRIGGER[:-1] + " | " + PHC_REBASE + ";",
            "CLKV: the settime leaves mr unchanged (#602)", False, "option-off"),
    Control("PHC adjtime becomes an mr cause 16 cycles later", "datapath",
            RESTART_DECL,
            "  logic [15:0] probe_adj_sr_r;\n"
            "  always_ff @(posedge axis_clk) begin : probe_adj_delay\n"
            "    if (!axis_resetn) probe_adj_sr_r <= '0;\n"
            "    else probe_adj_sr_r <= {probe_adj_sr_r[14:0], eff_ptp_adjust_w};\n"
            "  end : probe_adj_delay\n" +
            RESTART_DECL[:-1] + " | probe_adj_sr_r[15];",
            "CLKV: PHC-only steps leave INTERNAL mr unchanged (#602)", False,
            "option-off", ("CLKV: the settime leaves mr unchanged (#602)",
                           "CLKV: settime adds no MEDIA_RESET (#602)")),
    Control("PHC adjtime becomes an mr cause 256 cycles later", "datapath",
            RESTART_DECL,
            "  logic [8:0] probe_adj_cnt_r;\n"
            "  always_ff @(posedge axis_clk) begin : probe_adj_count\n"
            "    if (!axis_resetn) probe_adj_cnt_r <= '0;\n"
            "    else if (eff_ptp_adjust_w) probe_adj_cnt_r <= 9'd256;\n"
            "    else if (probe_adj_cnt_r != 9'd0) probe_adj_cnt_r <= probe_adj_cnt_r - 9'd1;\n"
            "  end : probe_adj_count\n" +
            RESTART_DECL[:-1] + " | (probe_adj_cnt_r == 9'd1);",
            "CLKV: PHC-only steps leave INTERNAL mr unchanged (#602)", False,
            "option-off", ("CLKV: the settime leaves mr unchanged (#602)",
                           "CLKV: settime adds no MEDIA_RESET (#602)")),
    Control("a PHC step suppresses a coincident CRF restart", "datapath",
            CRF_RESTART_TERMS,
            CRF_RESTART_TERMS[:-1] + " & ~" + PHC_REBASE + ")",
            "coincident: a PHC step does not suppress the CRF restart", False),
]


def build(leg: Leg, sources: dict[str, Path], mdir: Path) -> Path | None:
    """Build `leg` against `sources` through its own recipe in milan_dp; the
    executable, or None when the recipe failed or left none."""
    command = ["make", "-s", "-C", str(DP), leg.target, f"{leg.mdir_var}={mdir}"]
    command += [f"{MAKE_VAR[key]}={path}" for key, path in sources.items()]
    out = subprocess.run(command, capture_output=True, text=True, check=False)
    exe = mdir / leg.exe_name
    if out.returncode != 0 or not exe.is_file():
        sys.stdout.write(out.stdout[-2000:])
        sys.stdout.write(out.stderr[-2000:])
        return None
    return exe


def is_fresh(leg: Leg, exe: Path) -> bool:
    """True when `exe` exists and is no older than any input of its recipe:
    the Makefile's SRCS (`make print-srcs`), the leg's harness and the
    Makefile itself. A list that cannot be read counts as stale."""
    # GNU make 4.3 can inherit directory printing from a parent recipe even
    # with -s. Keep that chatter out of the source-path inventory for both legs.
    out = subprocess.run(["make", "--no-print-directory", "-s", "-C", str(DP), "print-srcs"],
                         capture_output=True, text=True, check=False)
    if out.returncode != 0 or not exe.is_file():
        return False
    inputs = [DP / name for name in out.stdout.split()]
    inputs += [DP / leg.harness, DP / "Makefile"]
    built = exe.stat().st_mtime
    return all(src.is_file() and src.stat().st_mtime <= built for src in inputs)


def run_leg(leg: Leg, exe: Path, short: bool) -> tuple[int, str]:
    """(rc, stdout) of one run of the leg, with no host deadline: it is
    cycle-bounded (module docstring). The AEM image sits beside the binary.
    `short` passes the leg's --no-small-steps flag, when it has one."""
    command = [str(exe)] + ([str(exe.parent / "aemi.bin")] if leg.takes_aem else [])
    command += [leg.short_flag] if short and leg.short_flag else []
    out = subprocess.run(command, cwd=str(DP), capture_output=True, text=True,
                         check=False)
    return out.returncode, out.stdout + out.stderr


def failed_checks(out: str) -> list[str]:
    """The names of the checks the leg printed as failed, in order."""
    return [line.strip()[len("[FAIL]"):].split(" got=")[0].strip()
            for line in out.splitlines() if line.strip().startswith("[FAIL]")]


def verdict(rc: int, out: str, must_fail: str | None) -> str:
    """'pass', 'caught', or why the run is not evidence."""
    reason, failed = log_reports_failure(out)
    if rc == 0 and not failed:
        return "pass"
    if rc == 0 and failed:
        return f"exited 0 but {reason} - a masked verdict is not evidence"
    if failed:
        if must_fail and not any(line.strip().startswith("[FAIL]") and must_fail in line
                                 for line in out.splitlines()):
            return f"failed, but not the named check ({must_fail!r})"
        return "caught"
    if rc < 0:
        return f"died by signal {-rc} with no harness verdict - a crash is not a catch"
    return f"exited {rc} with no harness verdict - a DUT abort is not a catch"


def run_control(control: Control, work: Path, tag: int, short: bool) -> bool:
    """Plant one control, build and run the leg; True when it was caught."""
    base = SOURCES[control.source].resolve()
    text = base.read_text()
    if text.count(control.anchor) != 1:
        print(f"[FAIL] control {control.name!r}: its anchor appears "
              f"{text.count(control.anchor)} time(s) in {base.name}, expected exactly 1. "
              f"The RTL moved and this control no longer plants anything - fix the "
              f"anchor, do not delete the arm.")
        return False
    planted = work / f"c{tag}_{base.name}"
    planted.write_text(text.replace(control.anchor, control.replacement))
    sources = {key: path.resolve() for key, path in SOURCES.items()}
    sources[control.source] = planted
    leg = LEGS[control.leg]
    exe = build(leg, sources, work / f"obj_c{tag}")
    if exe is None:
        print(f"[FAIL] control {control.name!r} did not compile; a control that cannot "
              f"build proves nothing about the leg")
        return False
    rc, out = run_leg(leg, exe, short)
    answer = verdict(rc, out, control.breaks)
    if answer == "caught":
        broke = failed_checks(out)
        if any(clean in failure for clean in control.stays_clean for failure in broke):
            print(f"[FAIL] control {control.name!r} also broke an unrelated event check: {broke}")
            return False
        print(f"[PASS] control caught: {control.name} - breaks \"{control.breaks}\"")
        print(f"    it broke {len(broke)} check(s): {'; '.join(broke)}")
        return True
    if answer == "pass":
        print(f"[FAIL] control SURVIVED: {control.name}. The leg does not prove "
              f"\"{control.breaks}\".")
    else:
        print(f"[FAIL] control {control.name!r} {answer}")
    return False


def main() -> int:
    """Run the positive control and the selected controls; 1 if any survived."""
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--all", action="store_true",
                        help="plant the whole inventory, not only the acceptance's controls")
    parser.add_argument("--slew", action="store_true", help="plant only the #545 connection controls")
    parser.add_argument("--no-small-steps", action="store_true",
                        help="run every gmstep leg without its #621 small-step phase")
    args = parser.parse_args()

    def on_sigterm(*_: object) -> None:
        """Exit on a kill so the temporary directory is removed."""
        sys.exit(143)

    signal.signal(signal.SIGTERM, on_sigterm)
    selected = [c for c in CONTROLS if
                (c.name.startswith("the policy level") if args.slew else args.all or c.acceptance)]
    passes = 0
    fails = 0
    with tempfile.TemporaryDirectory(prefix="gmstep-mutants-") as td:
        work = Path(td)
        for key in dict.fromkeys(c.leg for c in selected):
            leg = LEGS[key]
            exe = leg.clean_mdir / leg.exe_name
            if not is_fresh(leg, exe):
                print(f"[INFO] {exe.relative_to(DP)} is missing or older than its "
                      f"sources: the positive control is rebuilt")
                exe = build(leg, {}, work / f"obj_clean_{leg.target}")
            answer = (verdict(*run_leg(leg, exe, args.no_small_steps), None) if exe
                      else "did not compile")
            mode = f" ({leg.short_flag})" if args.no_small_steps and leg.short_flag else ""
            if answer == "pass":
                passes += 1
                print(f"[PASS] the unmutated gateware still passes the {key} leg{mode}")
            else:
                fails += 1
                print(f"[FAIL] the unmutated gateware does NOT pass the {key} leg{mode} "
                      f"({answer}) - every control result on it is meaningless")
        for tag, control in enumerate(selected):
            if run_control(control, work, tag, args.no_small_steps):
                passes += 1
            else:
                fails += 1
    print(f"\n{passes + fails} checks: {passes} PASS, {fails} FAIL")
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main())
