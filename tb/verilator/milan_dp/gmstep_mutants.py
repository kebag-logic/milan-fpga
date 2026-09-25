#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""Negative controls for the #387 gmstep leg and its option-off checks: prove they can fail.

sim_gmstep.cpp grades a grandmaster change that steps the PHC by 1.5 s while
an AAF stream is bound and locked under CRF selection, against the #387
decision: tu on the commit edge and a holdover after the step, the stream kept
streaming, one counted render re-base, one mr toggle and one MEDIA_RESET, all
of them the step's. Each control plants one defect into a private copy of the
source that carries the property - the datapath, the clock-validity block or
the render setpoint stage - and rebuilds the SAME leg through the Makefile's
own recipe (`make gmstep-build` with DP_SRC, CLKV_SRC or RSP_SRC, and
GMSTEP_MDIR, overridden) and runs it. Each control must make the leg FAIL by
its OWN verdict (a `[FAIL]` line or a tally with failures, read by
scripts/suite_tally.py), and the named check must be among the failures; a
crash or an abort is not a catch. The positive control is the clean leg the
sweep just built (obj_gmstep), re-run here; a binary older than any input of
its recipe is stale (a direct run after a source edit) and is rebuilt instead
of graded.

Two controls plant into the datapath but grade the option-off leg
(sim_main.cpp, `make option-off-build` with DP_SRC and OPTOFF_MDIR
overridden), where the harness itself commands a CLKV adjtime and a software
settime on an INTERNAL media clock: a settime that no longer toggles mr, and
a step toggle gated by the CRF clock-source selection. Their positive
control is that leg's clean build (obj_dir), under the same freshness rule.

Two inventories. The default run, which `make run` ends with, plants the
three controls issue #387's acceptance names: the step not toggling mr, the
render stage re-basing twice (the grandmaster identity as well as the step),
and the step not re-centring the render stage at all (ruling 5802264260
item 1: disabling the re-centre must fail the one-counted-event check). Each
costs one elaboration of the datapath, which is why the rest of the inventory
is the explicit `make gmstep-mutants` target (`--all`), per
docs/testing/TESTING.md's explicit-campaign rule; the option-off controls
are in that explicit inventory too. The third arm the
acceptance names, a pending restart that a step cancels, is in
tb/verilator/tkdiag (T17, T18 and mcr_mutants.py), where the restart engine's
holds can be driven PDU by PDU.

What bounds a run. This driver sets no host-time deadline (rule 8's
wall-clock ratchet, scripts/test_evidence.budget item 4). The leg is
cycle-bounded by construction: every phase runs a fixed cycle count, every
AXI4-Lite and AECP wait gives up after a fixed cycle count, and no loop waits
on a DUT output without a cycle bound, so a control ends at the same cycle as
the clean leg. The host-time bound of the default run is the sweep's
per-suite guard in scripts/run_all_suites.sh; the SIGTERM handler turns that
kill into an exit that removes the temporary directory.

Usage: python3 gmstep_mutants.py [--all]   (run from tb/verilator/milan_dp)
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
SOURCES = {
    "datapath": HERE / "../../../hdl/milan/milan_datapath.sv",
    "clkv": HERE / "../../../hdl/ieee8021as/ptp_timestamp/KL_ptp_clock_validity.sv",
    "stage": HERE / "../../../hdl/ieee1722/aaf/KL_render_setpoint.sv",
}
#: the make variable that points the recipe at each source
MAKE_VAR = {"datapath": "DP_SRC", "clkv": "CLKV_SRC", "stage": "RSP_SRC"}
sys.path.insert(0, str(HERE / "../../../scripts"))
from suite_tally import log_reports_failure  # noqa: E402

#: the render stage's re-base trigger; its second line is also the anchor the
#: #386 and #447 render runners plant their clock-source control on
RENDER_TRIGGER = "       media_rebase_p_w\n       | src_recentre_p_r;"
TALKER_GATE = "  assign aaf_stream_en_w = aaf_stream_en_raw_w & ~amap_edit_out_resv_r;"


class Leg(NamedTuple):
    """One elaboration a control can be graded on, built by its own recipe."""

    target: str                 #: the make target that builds it alone
    mdir_var: str               #: the make variable naming its build directory
    clean_mdir: Path            #: where the sweep builds the clean leg
    exe_name: str
    harness: str                #: its C++ harness, an input of the recipe
    takes_aem: bool             #: it reads the AEM image beside its binary


LEGS = {
    "gmstep": Leg("gmstep-build", "GMSTEP_MDIR", HERE / "obj_gmstep",
                  "Vmilan_dp_gmstep", "sim_gmstep.cpp", True),
    "option-off": Leg("option-off-build", "OPTOFF_MDIR", HERE / "obj_dir",
                      "Vmilan_dp_sim", "sim_main.cpp", False),
}


class Control(NamedTuple):
    """One planted defect and the check it must break."""

    name: str
    source: str                 #: a key of SOURCES
    anchor: str                 #: the text it replaces, exactly once
    replacement: str
    breaks: str                 #: the named check that must fail
    acceptance: bool            #: named by #387's acceptance: runs by default
    leg: str = "gmstep"         #: a key of LEGS


CONTROLS = [
    Control("the policy level is tied low at the servo", "datapath",
            ".phc_slew_active_i (gptp_slew_eff_w)",
            ".phc_slew_active_i (1'b0)",
            "slew path: the actual servo receives the level", False),
    Control("the policy level omits the applied-rate tail", "datapath",
            "gptp_slew_active_w || (|gptp_slew_tail_r)",
            "gptp_slew_active_w",
            "slew path: every staged sample covers the PHC tail", False),
    Control("the step does not toggle mr", "datapath",
            "                       | media_rebase_p_w;",
            "                       ;",
            "restart: the outgoing mr toggles exactly once", True),
    Control("the grandmaster identity re-bases the render stage as well as the step",
            "datapath", RENDER_TRIGGER,
            "       gm_recentre_p_r | media_rebase_p_w\n       | src_recentre_p_r;",
            "render: the GM change is one counted re-base event", True),
    Control("the step does not re-centre the render stage", "datapath",
            RENDER_TRIGGER,
            "       1'b0\n       | src_recentre_p_r;",
            "render: the GM change is one counted re-base event", True),
    Control("the render re-base is keyed to the identity, not the step", "datapath",
            RENDER_TRIGGER,
            "       gm_recentre_p_r\n       | src_recentre_p_r;",
            "render: every counted re-base lands at a PDU end right after the step", False),
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
    Control("the step's re-centre snaps one event off the setpoint", "stage",
            "                rptr_r[s]    <= snap_rptr_w;\n"
            "                prefill_r[s] <= 1'b0;",
            "                rptr_r[s]    <= prefill_r[s] ? snap_rptr_w : snap_rptr_w - 1'b1;\n"
            "                prefill_r[s] <= 1'b0;",
            "render: every PDU push leaves the target fill across the event", False),
    Control("a software settime does not toggle mr", "datapath",
            "                       | media_rebase_p_w;",
            "                       | eff_ptp_adjust_w;",
            "CLKV: the settime toggled mr once more (#387)", False, "option-off"),
    Control("the step's mr toggle is gated by the CRF clock-source selection", "datapath",
            "                       | media_rebase_p_w;",
            "                       | (crf_clk_selected_r & media_rebase_p_w);",
            "CLKV: its mr toggled once per PHC step issued so far (#387)", False,
            "option-off"),
]


def build(leg: Leg, sources: dict[str, Path], mdir: Path) -> Path | None:
    """Build `leg` against `sources` through the suite's own recipe; the
    executable, or None when the recipe failed or left none."""
    command = ["make", "-s", "-C", str(HERE), leg.target, f"{leg.mdir_var}={mdir}"]
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
    out = subprocess.run(["make", "--no-print-directory", "-s", "-C", str(HERE), "print-srcs"],
                         capture_output=True, text=True, check=False)
    if out.returncode != 0 or not exe.is_file():
        return False
    inputs = [HERE / name for name in out.stdout.split()]
    inputs += [HERE / leg.harness, HERE / "Makefile"]
    built = exe.stat().st_mtime
    return all(src.is_file() and src.stat().st_mtime <= built for src in inputs)


def run_leg(leg: Leg, exe: Path) -> tuple[int, str]:
    """(rc, stdout) of one run of the leg, with no host deadline: it is
    cycle-bounded (module docstring). The AEM image sits beside the binary."""
    command = [str(exe)] + ([str(exe.parent / "aemi.bin")] if leg.takes_aem else [])
    out = subprocess.run(command, cwd=str(HERE), capture_output=True, text=True,
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


def run_control(control: Control, work: Path, tag: int) -> bool:
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
    rc, out = run_leg(leg, exe)
    answer = verdict(rc, out, control.breaks)
    if answer == "caught":
        broke = failed_checks(out)
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
                print(f"[INFO] {exe.relative_to(HERE)} is missing or older than its "
                      f"sources: the positive control is rebuilt")
                exe = build(leg, {}, work / f"obj_clean_{leg.target}")
            answer = verdict(*run_leg(leg, exe), None) if exe else "did not compile"
            if answer == "pass":
                passes += 1
                print(f"[PASS] the unmutated gateware still passes the {key} leg")
            else:
                fails += 1
                print(f"[FAIL] the unmutated gateware does NOT pass the {key} leg "
                      f"({answer}) - every control result on it is meaningless")
        for tag, control in enumerate(selected):
            if run_control(control, work, tag):
                passes += 1
            else:
                fails += 1
    print(f"\n{passes + fails} checks: {passes} PASS, {fails} FAIL")
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main())
