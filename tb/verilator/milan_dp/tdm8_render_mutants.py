#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""Mutation arm for the #447 TDM8 render lane: prove the checks can fail.

sim_tdm8_render.cpp asserts, on the elaborated shipping shape, that a dynamic
AUDIO_MAP command reaches the right physical render key, that the pins carry
the routed samples in the right slots at the right phase, that the render
epoch silences the lane over a reset and a bind loss, that the surplus policy
keeps the delay bounded, and - under the CRF clock source selected live
through the real command path - that the commit-to-pin walk stops. On the
MULTI-STREAM elaboration it asserts the other two halves: the epoch's
bind-fall mask is stream qualified in both directions, and a legal cluster key
with no physical projection is suppressed at the crossbar while still
mirroring into the AECP protocol store.

Issue #447 acceptance 5 asks for the negative controls by name, so the real
gateware - the render master, the datapath, or the GENERATED SHAPE HEADER - is
mutated one defect at a time, the SAME leg is rebuilt through the Makefile's
own recipe (`make tdm8render-build` or `make tdm8render-multi-build`, with
TDMRM_SRC, DP_SRC, TDM8R_SHAPE and the object-directory variable overridden)
and run in the short mode that holds the check.

Each mutant must make the leg FAIL by its OWN verdict, with the named check
among the failures; a crash or an abort is not a catch, and neither is a
failure somewhere else. Two arms are CLEAN controls that must still PASS: the
unmutated leg, and the modelled-skew arm below.

WHAT THE CDC CONTROL DOES AND DOES NOT CLAIM. An ordinary zero-delay Verilator
run models neither metastability nor independent bit propagation: the source
word updates coherently and the destination samples a complete old or new
value, so replacing the gray transport with raw binary ALONE changes nothing
observable. The control is therefore a MODEL, stated here rather than implied:
the destination's first synchroniser stage takes the odd bits of the source
word immediately and the even bits one destination clock later, which is a
concrete, bounded statement of bit-arrival difference. Under that model a gray
transport is still safe - consecutive gray codes differ in one bit, so the
skewed sample is the old value or the new one - while a binary transport
splits a multi-bit increment and the destination latches a count the counter
never held. Both arms are run: `modelled bit-arrival skew, gray retained` must
PASS, and `modelled bit-arrival skew, raw binary transport` must FAIL the
named counter check. This demonstrates the DISCRIMINATION the crossing buys
under an explicitly defined fault. It is not a timing analysis and it is not
silicon evidence.

What bounds a livelocking mutant. This driver sets no host-time deadline on a
run. Every mode of sim_tdm8_render.cpp is cycle bounded by construction: it
steps fixed counts, every AXI4-Lite handshake gives up after a guard, every
frame injection is bounded, every AECP wait has a cycle limit, and no loop
waits on a DUT output without one. A leg therefore ends at the same cycle
whatever the mutated gateware does. The host-time bound is the sweep's:
scripts/run_all_suites.sh runs this suite's `make` under its per-suite guard
and reports a kill as TIMEOUT, never as a pass or a fail.

Usage: python3 tdm8_render_mutants.py    (run from tb/verilator/milan_dp)
Exit 0 = every mutant was caught, and every clean control still passes.
"""

import os
import signal
import subprocess
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
RENDER_RTL = HERE / "../../../hdl/ieee1722/aaf/KL_tdm_render_master.sv"
DP_RTL = HERE / "../../../hdl/milan/milan_datapath.sv"
SHAPE_SVH = (HERE / "../../../configs/generated/endstation_ax7101_1x1_tdm8"
             / "gen/adp_shape_defaults.svh")
sys.path.insert(0, str(HERE / "../../../scripts"))
from suite_tally import log_reports_failure  # noqa: E402

#: the two ELABORATIONS this leg has, each with the Makefile target that
#: builds it, the object-directory override that target reads, the executable
#: it produces and the clean control the sweep leaves on disk. The
#: multi-stream one exists because the stream-qualified epoch mask and the
#: nonphysical in-range cluster key are not observable on a one-stream shape
#: at all, so a mutant of either has nowhere to fail on the shipping build.
LEGS = {
    "ship": ("tdm8render-build", "TDM8R_MDIR", "Vmilan_dp_tdm8r",
             HERE / "obj_tdm8r/Vmilan_dp_tdm8r"),
    "multi": ("tdm8render-multi-build", "TDM8RM_MDIR", "Vmilan_dp_tdm8rm",
              HERE / "obj_tdm8rm/Vmilan_dp_tdm8rm"),
}

#: the three things a mutant may plant into: (path, the Makefile override).
#: `shape` is a whole DIRECTORY the recipe points +incdir at, because a
#: generated projection table is selected by include path and not by file.
SOURCES = {
    "render": (RENDER_RTL, "TDMRM_SRC"),
    "datapath": (DP_RTL, "DP_SRC"),
    "shape": (SHAPE_SVH, "TDM8R_SHAPE"),
}

#: (name, source, [(pattern, replacement), ...], leg, mode, the check it must
#: break). A mutation is a list of edits because some defects are not
#: expressible as one: the modelled-skew control needs a declaration, a reset
#: and the synchroniser itself, and it is still ONE defect. `leg` names which
#: elaboration holds the check (LEGS above); `mode` is the short argv that
#: reaches it, or None where the leg's one phase is the whole run.
MUTATIONS = [
    ("wrong physical base: the identity projection", "shape",
     [("localparam logic [6:0] ADP_DMAP_IN_RPHYS_C [0:7] = "
       "'{7'h42, 7'h43, 7'h44, 7'h45, 7'h46, 7'h47, 7'h48, 7'h49};",
       "localparam logic [6:0] ADP_DMAP_IN_RPHYS_C [0:7] = "
       "'{7'h40, 7'h41, 7'h42, 7'h43, 7'h44, 7'h45, 7'h46, 7'h47};")],
     "ship", "--serial-only",
     "T4 PROJECTION: physical keys 2..9 hold the routed sources"),
    ("wrong slot order: the bank walk runs backwards", "datapath",
     [("          tdmr_data_r  <= chmap_phys_w[(CHMAP_RPHYS_TDM_BASE_C\n"
       "                                        + 32'(tdmr_slot_r) + 1)*24 +: 24];",
       "          tdmr_data_r  <= chmap_phys_w[(CHMAP_RPHYS_TDM_BASE_C\n"
       "                                        + RLAST_C - 32'(tdmr_slot_r))*24 +: 24];")],
     "ship", "--serial-only",
     "T6 IDENTITY: every decoded frame is a complete 24-bit match against "
     "the injection record"),
    ("shared identity corruption: one pdu bit of EVERY channel", "datapath",
     [("    .s_tdata_i  (rsp_tdata_w),",
       "    .s_tdata_i  (rsp_tdata_w ^ 64'h0000_0001_0000_0001),")],
     "ship", "--serial-only",
     "T6 IDENTITY: every decoded frame is a complete 24-bit match against "
     "the injection record"),
    # A DOUT-ONLY PHASE SLIP MOVES NO CLOCK. BCLK, FSYNC and every value of
    # the decoder's free-running position are unchanged by it, so the framing
    # counter cannot see it and is not asked to: the check named here is the
    # independent full-word and padding grading, which is what a shifted data
    # line really does break.
    ("one-bit phase slip: the bit for position p, not p + 1", "render",
     [("  wire [SW_C-1:0]  bit_slot_w = frame_pos_i[FRAME_POS_W_P-1 -: SW_C];\n"
       "  wire [SBW_C-1:0] bit_idx_w  = frame_pos_i[SBW_C-1 : 0];",
       "  wire [FRAME_POS_W_P-1:0] mut_pos_w = frame_pos_i - 1'b1;\n"
       "  wire [SW_C-1:0]  bit_slot_w = mut_pos_w[FRAME_POS_W_P-1 -: SW_C];\n"
       "  wire [SBW_C-1:0] bit_idx_w  = mut_pos_w[SBW_C-1 : 0];")],
     "ship", "--serial-only",
     "T6 PADDING: the eight pad bits of every slot are zero"),
    ("uncounted repeat: the underrun counter never increments", "render",
     [("          else unders_b_r <= (&unders_b_r) ? unders_b_r : unders_b_r + 16'd1;",
       "          else unders_b_r <= unders_b_r;")],
     "ship", "--serial-only",
     "T6 ORDER: every repeat is a counted underrun"),
    ("drop NEWEST: the prefetch keeps the have-next guard", "render",
     [("      if (!ser_flush_r && !ren_r && !fetch_v_r && !rempty_w) ren_r <= 1'b1;",
       "      if (!ser_flush_r && !have_next_r && !ren_r && !fetch_v_r && !rempty_w) ren_r <= 1'b1;")],
     "ship", "--serial-only",
     "T14 SKIP LAW: the forced surplus was COUNTED as skips"),
    # ONE DEFECT, TWO PLACES. The producer retains an epoch request in two
    # ways - the reset VALUE of the request itself, and the reset value of the
    # synchroniser that reads the serial side's flush level - and either alone
    # re-arms the round trip. The defect being modelled is "the producer does
    # not retain a request across a reset", so the mutant removes both; a
    # single-sided edit would only prove that the other side still works.
    ("the epoch request does not RETAIN across a reset", "render",
     [("      epoch_req_r <= 1'b1;               //! reset IS an epoch event\n"
       "      commit_en_r <= 1'b0;",
       "      epoch_req_r <= 1'b0;               //! MUTANT: no retained request\n"
       "      commit_en_r <= 1'b1;"),
      ("      flush_s_r <= 2'b11;                //! assume flushed until proven otherwise",
       "      flush_s_r <= 2'b00;                //! MUTANT: assume running")],
     "ship", "--epoch-only",
     "T18 RESET: the epoch reopened and was counted"),
    # ONE DEFECT, TWO PLACES again: the epoch gates commits at the adapter
    # (through commit_en_o) and again at the FIFO write itself, and either
    # alone stops a closed epoch admitting a frame. The defect is "a closed
    # epoch does not gate commits".
    ("ungated commit: a closed epoch admits frames anyway", "render",
     [("  assign commit_en_o = commit_en_r;",
       "  assign commit_en_o = 1'b1;"),
      ("  wire fifo_wen_w = tick_i && commit_en_r && !wfull_w;",
       "  wire fifo_wen_w = tick_i && !wfull_w;")],
     "ship", "--epoch-only",
     "T26 MAP WRITE IN A CLOSED EPOCH: the re-seeded crossbar value never "
     "reaches a slot"),
    ("modelled bit-arrival skew, raw binary transport", "render",
     [("  logic [15:0] fr_1_r, fr_2_r, un_1_r, un_2_r;",
       "  logic [15:0] fr_1_r, fr_2_r, un_1_r, un_2_r, fr_d_r;"),
      ("      fr_1_r <= '0; fr_2_r <= '0; un_1_r <= '0; un_2_r <= '0;",
       "      fr_1_r <= '0; fr_2_r <= '0; un_1_r <= '0; un_2_r <= '0;\n"
       "      fr_d_r <= '0;"),
      ("      {fr_2_r, fr_1_r} <= {fr_1_r, fr_g_r};",
       "      fr_d_r <= fr_g_r;\n"
       "      fr_1_r <= (fr_g_r & 16'hAAAA) | (fr_d_r & 16'h5555);\n"
       "      fr_2_r <= fr_1_r;"),
      ("      fr_g_r <= bin2gray16(frames_b_r);",
       "      fr_g_r <= frames_b_r;"),
      ("  assign frames_o    = gray2bin16(fr_2_r);",
       "  assign frames_o    = fr_2_r;")],
     "ship", "--serial-only",
     "T28 COUNTERS: no sampled frame count ran ahead of the frames the pins "
     "delivered"),
    # ---- the #447 continuation's four: CRF, the stream-qualified epoch mask
    #      in both directions, and the nonphysical in-range CSR mirror.
    ("the clock-source trigger dropped from the recentre set", "datapath",
     [("       | src_recentre_p_r;",
       "       | 1'b0;")],
     "ship", "--crf-only",
     "T30 CRF: ...as exactly one render recentre pulse"),
    # The mask exists so that a fall on a stream the lane does not render
    # leaves the lane alone. Take the qualification away and the lane flushes
    # on somebody else's unbind - which is the defect the mask was added for.
    ("the bind-fall mask is not stream qualified", "datapath",
     [("  wire tdmr_epoch_evt_w = |(strtbl_bind_fall_w & tdmr_lane_streams_w);",
       "  wire tdmr_epoch_evt_w = |strtbl_bind_fall_w;")],
     "multi", None,
     "M3 UNRELATED LOSS: the adapter's commit gate never closed, not for one "
     "cycle"),
    # ...and the other direction, which a mask that simply never fires would
    # pass: the lane's stream set must follow the STREAM FIELD of the mapping
    # the crossbar actually holds, not the first stream.
    ("the lane's stream set ignores the mapping's stream field", "datapath",
     [("          if (32'(rword[5:3]) == s) tdmr_lane_streams_w[s] = 1'b1;",
       "          if (s == 0) tdmr_lane_streams_w[s] = 1'b1;")],
     "multi", None,
     "M5 RENDERED LOSS: the adapter's commit gate CLOSED, which the unrelated "
     "loss never did"),
    # [R152] the preserved mirror: suppressing the PHYSICAL projection must
    # not suppress the protocol-store write, and this is the mutation that
    # would.
    ("the CSR protocol-store mirror gated on the physical projection",
     "datapath",
     [("          && cfg_chmap_wr_en && !cfg_chmap_wr_side\n"
       "          && (32'(cfg_chmap_wr_addr) < AMAP_IN_KEYS_C)) begin",
       "          && cfg_chmap_wr_en && !cfg_chmap_wr_side\n"
       "          && cfg_chmap_rphys_w[6]\n"
       "          && (32'(cfg_chmap_wr_addr) < AMAP_IN_KEYS_C)) begin")],
     "multi", None,
     "M6 NONPHYSICAL: ...and the SAME write is still mirrored into the AECP "
     "protocol store, read back through GET_AUDIO_MAP"),
]

#: the CLEAN controls under the same modelled fault: the crossing this design
#: actually uses must survive it, or the discrimination above would only mean
#: that the model itself breaks everything.
CLEAN_CONTROLS = [
    ("modelled bit-arrival skew, gray retained", "render",
     [("  logic [15:0] fr_1_r, fr_2_r, un_1_r, un_2_r;",
       "  logic [15:0] fr_1_r, fr_2_r, un_1_r, un_2_r, fr_d_r;"),
      ("      fr_1_r <= '0; fr_2_r <= '0; un_1_r <= '0; un_2_r <= '0;",
       "      fr_1_r <= '0; fr_2_r <= '0; un_1_r <= '0; un_2_r <= '0;\n"
       "      fr_d_r <= '0;"),
      ("      {fr_2_r, fr_1_r} <= {fr_1_r, fr_g_r};",
       "      fr_d_r <= fr_g_r;\n"
       "      fr_1_r <= (fr_g_r & 16'hAAAA) | (fr_d_r & 16'h5555);\n"
       "      fr_2_r <= fr_1_r;")],
     "ship", "--serial-only"),
]

#: the defect arms the LEG itself carries, because their defect is in the
#: STIMULUS rather than in the gateware: a render clock that never runs, one
#: transmitted sample that differs from the record the oracle keeps, and a
#: clock-source command that runs in full but names INTERNAL. The third is
#: what keeps the aligned-window claims from being a quiet run: everything
#: else about that phase is unchanged, so only the claims that depend on the
#: SELECTION can fail.
LEG_DEFECTS = [
    ("stopped render clock", "ship", "--defect-stopped-clock",
     "T5 FRAMING: the window decoded whole frames"),
    ("a single changed sample", "ship", "--defect-one-sample",
     "T6 IDENTITY: every decoded frame is a complete 24-bit match against "
     "the injection record"),
    ("the clock-source selection names INTERNAL", "ship",
     "--defect-internal-select",
     "T30 CRF ALIGNED: the walk STOPPED once the grids were held together, "
     "which is what the aligner buys the lane"),
]


def build(leg: str, overrides: dict[str, str], mdir: Path) -> Path | None:
    """Build one ELABORATION through the suite's own recipe, `overrides`
    applied. `leg` selects the Makefile target, its object-directory variable
    and the executable name from LEGS, so a mutant is always built by the same
    recipe the positive control was."""
    target, mdir_var, exe_name, _ = LEGS[leg]
    cmd = ["make", "-s", "-C", str(HERE), target, f"{mdir_var}={mdir}"]
    cmd += [f"{k}={v}" for k, v in overrides.items()]
    out = subprocess.run(cmd, capture_output=True, text=True, check=False)
    exe = mdir / exe_name
    if out.returncode != 0 or not exe.is_file():
        sys.stdout.write(out.stdout[-2000:])
        sys.stdout.write(out.stderr[-2000:])
        return None
    return exe


def run_leg(exe: Path, mode: str | None) -> tuple[int, str]:
    """(rc, stdout) of one run, waited for with no host deadline: every mode
    of the leg is cycle bounded (module docstring). `mode` is None where the
    elaboration's one phase is the whole run. The leg is its own session, so
    the sweep's kill reaches it only through the SIGTERM handler in main(),
    whose exit runs the kill below."""
    argv = [str(exe)] + ([mode] if mode else [])
    proc = subprocess.Popen(argv, cwd=str(HERE),
                            stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                            text=True, start_new_session=True)
    try:
        out, _ = proc.communicate()
        return proc.returncode, out
    finally:
        if proc.poll() is None:
            os.killpg(os.getpgid(proc.pid), signal.SIGKILL)
            proc.wait()


def verdict(rc: int, out: str, must_fail: str | None) -> str:
    """'pass', 'caught', or why the run is not evidence."""
    reason, failed = log_reports_failure(out)
    if rc == 0 and not failed:
        return "pass"
    if rc == 0 and failed:
        return f"exited 0 but {reason} - a masked verdict is not evidence"
    if failed:
        if must_fail and not any(line.strip().startswith("[FAIL]")
                                 and must_fail in line
                                 for line in out.splitlines()):
            return f"failed, but not the named check ({must_fail!r})"
        return "caught"
    if rc < 0:
        return (f"died by signal {-rc} with no harness verdict - a crash is "
                "not a catch")
    return f"exited {rc} with no harness verdict - a DUT abort is not a catch"


def plant(source: str, edits: list[tuple[str, str]], work: Path,
          tag: str) -> tuple[str | None, str]:
    """Write the mutated source (or shape directory) and return the override
    value the recipe needs, plus a reason when the pattern no longer fits."""
    path, _ = SOURCES[source]
    text = path.read_text()
    for pattern, replacement in edits:
        if text.count(pattern) != 1:
            return None, (f"its pattern appears {text.count(pattern)} time(s) "
                          f"in {path.name}, expected exactly 1. The source "
                          "moved and this mutant is no longer mutating "
                          "anything - fix the pattern, do not delete the arm")
        text = text.replace(pattern, replacement)
    if source == "shape":
        # a shape is selected by INCLUDE PATH, so the mutant is a directory
        gen = work / f"shape_{tag}" / "gen"
        gen.mkdir(parents=True, exist_ok=True)
        (gen / "adp_shape_defaults.svh").write_text(text)
        return f"+incdir+{gen.parent}", ""
    out = work / f"{path.stem}_{tag}.sv"
    out.write_text(text)
    return str(out), ""


def main() -> int:
    """Run the clean controls and every mutant; 1 if any survived."""
    def on_sigterm(*_: object) -> None:
        """Leave on the sweep's kill with the shape run_all_suites.sh reads as
        a TIMEOUT, so a killed mutation round is never a pass or a fail."""
        sys.exit(143)

    signal.signal(signal.SIGTERM, on_sigterm)
    passes = fails = 0
    with tempfile.TemporaryDirectory(prefix="tdm8-render-mutants-") as td:
        work = Path(td)
        #: the positive controls, one per elaboration: the clean build the
        #: sweep left on disk, or a fresh one when this runner is invoked
        #: alone. Every verdict below comes from the same binary shape.
        clean: dict[str, Path | None] = {}
        for leg, (_, _, _, on_disk) in LEGS.items():
            clean[leg] = (on_disk if on_disk.is_file()
                          else build(leg, {}, work / f"obj_clean_{leg}"))
        for leg, mode in sorted({(m[3], m[4]) for m in MUTATIONS}
                                | {(c[3], c[4]) for c in CLEAN_CONTROLS},
                                key=lambda x: (x[0], x[1] or "")):
            answer = (verdict(*run_leg(clean[leg], mode), None) if clean[leg]
                      else "did not compile")
            if answer == "pass":
                passes += 1
                print(f"[PASS] the unmutated gateware still passes the render "
                      f"lane leg ({leg} {mode or 'whole'})")
            else:
                fails += 1
                print(f"[FAIL] the unmutated gateware does NOT pass ({leg} "
                      f"{mode or 'whole'}: {answer}) - every mutant result in "
                      "that mode is meaningless")
        # the leg's own defect arms: the stimulus is wrong, the gateware is not
        for name, leg, mode, breaks in LEG_DEFECTS:
            if clean[leg] is None:
                fails += 1
                print(f"[FAIL] leg defect arm {name!r}: no clean executable")
                continue
            answer = verdict(*run_leg(clean[leg], mode), breaks)
            if answer == "caught":
                passes += 1
                print(f"[PASS] leg defect caught ({leg} {mode}): {name} - "
                      f"breaks \"{breaks}\"")
            else:
                fails += 1
                print(f"[FAIL] leg defect {name!r} {answer}")
        # the clean controls under an explicitly modelled fault
        for name, source, edits, leg, mode in CLEAN_CONTROLS:
            tag = name.replace(" ", "_").replace(",", "").replace("-", "_")
            value, why = plant(source, edits, work, tag)
            if value is None:
                fails += 1
                print(f"[FAIL] clean control {name!r}: {why}")
                continue
            mexe = build(leg, {SOURCES[source][1]: value}, work / f"obj_{tag}")
            if mexe is None:
                fails += 1
                print(f"[FAIL] clean control {name!r} did not compile")
                continue
            answer = verdict(*run_leg(mexe, mode), None)
            if answer == "pass":
                passes += 1
                print(f"[PASS] clean control still passes ({leg} "
                      f"{mode or 'whole'}): {name}")
            else:
                fails += 1
                print(f"[FAIL] clean control {name!r} did not pass: {answer}. "
                      "The modelled fault breaks the sound crossing too, so "
                      "it discriminates nothing.")
        for name, source, edits, leg, mode, breaks in MUTATIONS:
            tag = name.replace(" ", "_").replace(":", "").replace(",", "")
            tag = tag.replace("-", "_").replace(".", "").replace("'", "")
            value, why = plant(source, edits, work, tag)
            if value is None:
                fails += 1
                print(f"[FAIL] mutation {name!r}: {why}")
                continue
            mexe = build(leg, {SOURCES[source][1]: value}, work / f"obj_{tag}")
            if mexe is None:
                fails += 1
                print(f"[FAIL] mutation {name!r} did not compile; a mutant "
                      "that cannot build proves nothing about the leg")
                continue
            answer = verdict(*run_leg(mexe, mode), breaks)
            if answer == "caught":
                passes += 1
                print(f"[PASS] mutant caught ({leg} {mode or 'whole'}): {name}"
                      f" - breaks \"{breaks}\"")
            elif answer == "pass":
                fails += 1
                print(f"[FAIL] mutant SURVIVED: {name}. The leg does not "
                      f"prove \"{breaks}\".")
            else:
                fails += 1
                print(f"[FAIL] mutant {name!r} {answer}")
    total = passes + fails
    print(f"\n{total} checks: {passes} PASS, {fails} FAIL")
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main())
