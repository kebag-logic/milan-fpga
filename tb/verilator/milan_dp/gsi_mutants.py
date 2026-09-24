#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""Mutation arm for the #508 GET_STREAM_INFO seam in milan_dp: prove the checks can fail.

sim_nxn.cpp's [GSI] section (the timed obj_notify leg) asserts on the shipping
AX 1x1 shape that a Stream Input's probing_status, acmp_status,
msrp_failure_code and msrp_failure_bridge_id follow the processor's own
listener record and SRP registrar, per sink, through every transition #508
names. Since processor pin a8f8ce81 those fields are the processor's: its top
serves selectors 5 and 7 and the failure-code byte of selector 4 for a
STREAM_INPUT, and milan_datapath answers none of them. So each defect #508
names is planted where it would now live - in a COPY of the processor's hdl/
tree, in a copy of milan_datapath, or in both - and the SAME leg is rebuilt
through the Makefile's own recipe (`make notify-build` with PP_DIR, DP_SRC and
NOTIFY_MDIR overridden) and run. Each mutant must make the leg FAIL by its OWN
verdict (a `[FAIL]` line or a tally with failures, read by
scripts/suite_tally.py), and the named check must be among the failures; a
crash or an abort is not a catch. The positive control is the clean leg
(obj_notify, which `make gsi-mutants` builds and runs first), re-run here.

The submodule checkout is never edited: the processor half of a mutant is
written into a copy of its hdl/ tree under a temporary directory, and the
copy is what the recipe's derived source list points at.

What bounds a run. This driver sets no host-time deadline (rule 8's
wall-clock ratchet, scripts/test_evidence.budget item 4). The leg is
cycle-bounded by construction: every phase runs to a fixed cycle target, an
AEM command waits at most 200,000 cycles for its answer, and the AXI4-Lite
BFM gives up after 4096 cycles per handshake, so a mutant ends at the same
cycle as the clean leg. This is an explicit campaign outside the sweep
(docs/testing/TESTING.md), so run by hand nothing but the cycle bound limits
a run; the SIGTERM handler turns a kill into an exit that removes the
temporary directory.

Usage: make -C tb/verilator/milan_dp gsi-mutants
       (or python3 gsi_mutants.py [N ...] from tb/verilator/milan_dp, where
       each N selects one mutant by its 1-based place in MUTATIONS; the
       clean control runs every time)
Exit 0 = every selected mutant was caught and the clean leg still passes.
"""

import shutil
import signal
import subprocess
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
DP_RTL = HERE / "../../../hdl/milan/milan_datapath.sv"
PP_HDL = HERE / "../../../protocol-processor/hdl"
#: the processor top, relative to its hdl/ tree
PP_TOP = Path("top") / "protocol_processor_top.sv"
CLEAN_MDIR = HERE / "obj_notify"
EXE_NAME = "Vmilan_dp_notify"
sys.path.insert(0, str(HERE / "../../../scripts"))
from suite_tally import log_reports_failure  # noqa: E402

#: the processor's STREAM_INPUT answer arms, verbatim at the pin
PP_SEL4 = "        4'd4: aecp_gsi_data_w = {gsi_data_i[63:16], gsi_fail_code_w, 8'd0};"
PP_SEL5 = "        4'd5: aecp_gsi_data_w = gsi_fail_bridge_w;"
PP_SEL7 = "        4'd7: aecp_gsi_data_w = {32'd0, gsi_status_w, 24'd0};"
PP_INTERNAL = "                           && ((gsi_sel_o == 4'd5) || (gsi_sel_o == 4'd7));"
PP_SINK = "  assign gsi_sink_w = SINK_IDX_W_C'(gsi_desc_index_o);"
#: where the parent's deleted selector-7 arm stood
DP_SEL15 = ("          //! SET_STREAM_FORMAT's verdict on the proposed format (issue #67)\n"
            "          4'd15: gsi_ans_raw_w = sfv_verdict_w;")
#: the parent's pre-#508 selector-7 approximation, verbatim from dev 573f0052
DP_OLD_SEL7 = ("          4'd7: gsi_ans_raw_w = {32'd0,\n"
               "                                 gsi_in_w\n"
               "                                 ? {(!gsi_bnd_w ? 3'd0\n"
               "                                     : gsi_setl_w ? 3'd3 : 3'd1), 5'd0}\n"
               "                                 : 8'd0,\n"
               "                                 24'd0};\n")

# (name, [(file, the text it replaces, its replacement)], the check it must fail).
# `file` is "pp" for the processor top or "dp" for milan_datapath.
MUTATIONS = [
    ("the processor ties a sink's failure bridge id to zero",
     [("pp", PP_SEL5, "        4'd5: aecp_gsi_data_w = 64'd0;")],
     "[GSI] G5 sink 0 Talker Failed: msrp_failure_bridge_id"),
    ("selector 5 goes back to the parent, whose input answer is zero",
     [("pp", PP_INTERNAL, "                           && (gsi_sel_o == 4'd7);"),
      ("pp", PP_SEL5, "        4'd5: aecp_gsi_data_w = gsi_data_i;")],
     "[GSI] G5 sink 0 Talker Failed: msrp_failure_bridge_id"),
    ("the processor ties a sink's failure code to zero",
     [("pp", PP_SEL4, "        4'd4: aecp_gsi_data_w = {gsi_data_i[63:16], 8'd0, 8'd0};")],
     "[GSI] G5 sink 0 Talker Failed: msrp_failure_code"),
    ("the failure-code byte is left to the parent, which no longer supplies it",
     [("pp", PP_SEL4, "        4'd4: aecp_gsi_data_w = gsi_data_i;")],
     "[GSI] G5 sink 1 Talker Failed: msrp_failure_code"),
    ("the processor ties probing/ACMP status to zero",
     [("pp", PP_SEL7, "        4'd7: aecp_gsi_data_w = {32'd0, 8'd0, 24'd0};")],
     "[GSI] G2 sink 0 two probes unanswered: acmp_status"),
    ("the processor reads the other sink's owners",
     [("pp", PP_SINK, "  assign gsi_sink_w = SINK_IDX_W_C'(gsi_desc_index_o ^ 16'd1);")],
     "[GSI] G5 sink 0 beside the other sink's failure: msrp_failure_bridge_id"),
    ("the parent's bound/settled approximation answers selector 7 again",
     [("pp", PP_INTERNAL, "                           && (gsi_sel_o == 4'd5);"),
      ("pp", PP_SEL7, "        4'd7: aecp_gsi_data_w = gsi_data_i;"),
      ("dp", DP_SEL15, DP_OLD_SEL7 + DP_SEL15)],
     "[GSI] G1 sink 0 bound: probing_status"),
]


def build(dp_path: Path, pp_dir: Path, mdir: Path) -> Path | None:
    """Build the leg against `dp_path` and the processor tree `pp_dir`
    through the suite's own recipe; the executable, or None when the recipe
    failed or left none. The ROM images the leg reads are the clean build's:
    `-o` keeps a copied generator's newer timestamp from rewriting them."""
    out = subprocess.run(
        ["make", "-s", "-C", str(HERE), "-o", "ltn_rom.hex", "-o", "ucode.hex",
         "notify-build", f"DP_SRC={dp_path}", f"PP_DIR={pp_dir}",
         f"NOTIFY_MDIR={mdir}"],
        capture_output=True, text=True, check=False)
    exe = mdir / EXE_NAME
    if out.returncode != 0 or not exe.is_file():
        sys.stdout.write(out.stdout[-2000:])
        sys.stdout.write(out.stderr[-2000:])
        return None
    return exe


def run_leg(exe: Path) -> tuple[int, str]:
    """(rc, stdout) of one run of the leg, with no host deadline: the leg is
    cycle-bounded (module docstring)."""
    out = subprocess.run([str(exe)], cwd=str(HERE), capture_output=True,
                         text=True, check=False)
    return out.returncode, out.stdout + out.stderr


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


def plant(name: str, edits: list[tuple[str, str, str]], work: Path,
          tag: str) -> tuple[Path, Path] | None:
    """Write the mutant's datapath and processor tree; None when a pattern
    no longer matches exactly once, so the mutant would mutate nothing."""
    texts = {"dp": DP_RTL.read_text(), "pp": (PP_HDL / PP_TOP).read_text()}
    for where, pattern, replacement in edits:
        count = texts[where].count(pattern)
        if count != 1:
            print(f"[FAIL] mutation {name!r}: a pattern appears {count} time(s) in "
                  f"{'milan_datapath.sv' if where == 'dp' else PP_TOP.name}, expected "
                  f"exactly 1. The RTL moved and this mutant is no longer mutating "
                  f"anything - fix the pattern, do not delete the arm.")
            return None
        texts[where] = texts[where].replace(pattern, replacement)
    dp_path = work / f"milan_datapath_{tag}.sv"
    dp_path.write_text(texts["dp"])
    pp_dir = work / f"pp_hdl_{tag}"
    shutil.copytree(PP_HDL, pp_dir)
    (pp_dir / PP_TOP).write_text(texts["pp"])
    return dp_path, pp_dir


def run_mutant(mutation: tuple[str, list[tuple[str, str, str]], str], work: Path) -> bool:
    """Plant one mutation, build and run the leg; True when it was caught."""
    name, edits, breaks = mutation
    tag = "".join(c if c.isalnum() else "_" for c in name)
    planted = plant(name, edits, work, tag)
    if planted is None:
        return False
    exe = build(planted[0], planted[1], work / f"obj_{tag}")
    if exe is None:
        print(f"[FAIL] mutation {name!r} did not compile; a mutant that cannot build "
              f"proves nothing about the leg")
        return False
    rc, out = run_leg(exe)
    answer = verdict(rc, out, breaks)
    if answer == "caught":
        print(f"[PASS] mutant caught: {name} - breaks \"{breaks}\" "
              f"({log_reports_failure(out)[0]})")
        return True
    if answer == "pass":
        print(f"[FAIL] mutant SURVIVED: {name}. The leg does not prove \"{breaks}\".")
    else:
        print(f"[FAIL] mutant {name!r} {answer}")
    return False


def selected(argv: list[str]) -> list[tuple[str, list[tuple[str, str, str]], str]] | None:
    """The mutants `argv` names by 1-based place, every one when it names
    none; None when an argument names no mutant."""
    if not argv:
        return MUTATIONS
    picks = []
    for arg in argv:
        if not arg.isdigit() or not 1 <= int(arg) <= len(MUTATIONS):
            print(f"[FAIL] {arg!r} names no mutant: use 1..{len(MUTATIONS)}")
            return None
        picks.append(MUTATIONS[int(arg) - 1])
    return picks


def main() -> int:
    """Run the positive control and the selected mutants; 1 if any survived."""
    mutations = selected(sys.argv[1:])
    if mutations is None:
        return 2

    def on_sigterm(*_: object) -> None:
        """Exit on a kill so the temporary directory is removed."""
        sys.exit(143)

    signal.signal(signal.SIGTERM, on_sigterm)
    passes = 0
    fails = 0
    with tempfile.TemporaryDirectory(prefix="gsi-mutants-") as td:
        work = Path(td)
        clean = CLEAN_MDIR / EXE_NAME
        exe = clean if clean.is_file() else build(DP_RTL, PP_HDL, work / "obj_clean")
        answer = verdict(*run_leg(exe), None) if exe else "did not compile"
        if answer == "pass":
            passes += 1
            print("[PASS] the unmutated gateware still passes the obj_notify leg")
        else:
            fails += 1
            print(f"[FAIL] the unmutated gateware does NOT pass ({answer}) - every "
                  f"mutant result is meaningless")
        for mutation in mutations:
            if run_mutant(mutation, work):
                passes += 1
            else:
                fails += 1
    print(f"\n{passes + fails} checks: {passes} PASS, {fails} FAIL")
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main())
