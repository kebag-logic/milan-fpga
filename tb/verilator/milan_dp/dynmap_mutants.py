#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""Planted controls for the #658 [DYNMAP] leg in milan_dp: prove its checks can fail.

sim_nxn.cpp's [DYNMAP] section (the dynmap leg, shipping AX 1x1 TDM8 shape)
grades the power-on audio maps, a SET_STREAM_FORMAT under Milan v1.2 5.4.2.7
and the maps a restored 4-channel input format leaves. #658's ruling
(comment 5988843004, item 5) names two controls: an empty reset, and no clip
after the restore. Each must fail its check. Two more cover the arms the
ruling's two cannot reach: the output clip, which only the boot-window arm
exercises, and the crossbar RAMs, which only the CSR readback grades.

Seven more remove the boot window's guard arms, one each (review R490-1 F1):
the CSR writer's hold at all four sites, then at each store alone; the
CLOSED terminal; the sweep after the terminal; its drain clock; and the edit
face's wait. Each is caught by the staged arm that places its stimulus on
the clock the guard owns.

Twenty-three more, the #637 controls, plant one defect each in the parent's
channel-map record writer and restore (milan_datapath's amr_* blocks) or in
the device-face arbiter KL_pp_shadow adds in front of the backend, and each
is caught by its named [MAPREC] check: the trigger, the debounce, the empty
list read as an erased record (#763), every framed record refused, the
crc16 ignored, both roll-backs, the faces' waits, the change qualification
(DR2b), the taint, the restore's own writes, the entity enable, the three
DR2c arms, the restore's deadline, and four arbiter and glue arms.

The empty reset is also planted under the two end-to-end checks the ruling
asks for, each in its own suite: the listener (tb/verilator/milan_dp_render,
whose `T18 POWER-ON` decodes stream channel c at TDM8 serial slot c) and the
talker (tb/verilator/capture_coherence's milan_datapath leg, whose columns
carry TDM capture slot c in stream channel c). Neither issues a map command,
so both must fail when the power-on map is empty.

Each defect is planted in a COPY of milan_datapath and the leg is rebuilt
through its suite's own recipe (`make dynmap-build`, `make tdm8render-build`
or `make dp-build`, with DP_SRC and the objdir overridden) and run. A mutant
is caught only when the leg FAILS by its own verdict (a `[FAIL]` line or a
tally with failures, read by scripts/suite_tally.py) AND the named check is
among the failures; a crash or an abort is not a catch. Each leg's positive
control is its clean build, run again here.

What bounds a run: no host-time deadline. The leg is cycle-bounded by
construction (each AEM command waits a fixed number of cycles for its answer,
the restore wait is bounded, the AXI4-Lite BFM gives up after a fixed number
of cycles per handshake), so a mutant ends no later than the clean leg. This
is an explicit campaign outside the sweep (docs/testing/TESTING.md); the
SIGTERM handler turns a kill into an exit that removes the temporary
directory.

Usage: make -C tb/verilator/milan_dp dynmap-mutants
       (or python3 dynmap_mutants.py [N ...] from tb/verilator/milan_dp,
       where each N selects one mutant by its 1-based place in MUTATIONS;
       the clean control runs every time)
Exit 0 = every selected mutant was caught and the clean leg still passes.
"""

import signal
import subprocess
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
DP_RTL = HERE / "../../../hdl/milan/milan_datapath.sv"
#: the #637 arbiter's file, planted through the suite's SHADOW_SRC
SHADOW_RTL = HERE / "../../../hdl/milan/KL_pp_shadow.sv"
#: each leg's suite, build target, objdir variable, clean objdir, executable,
#: the arguments it runs with and the generated inputs its build may not remake
LEGS = {
    "dynmap": (HERE, "dynmap-build", "DYNMAP_MDIR", "obj_dynmap",
               "Vmilan_dp_dynmap", (), ("ltn_rom.hex", "ucode.hex")),
    "listener": (HERE / "../milan_dp_render", "tdm8render-build", "TDM8R_MDIR",
                 "obj_tdm8r", "Vmilan_dp_tdm8r", (),
                 ("ltn_rom.hex", "ucode.hex", "tdm8r_aemi.bin")),
    "talker": (HERE / "../capture_coherence", "dp-build", "DP_MDIR", "obj_dp",
               "Vcoherence_dp", ("--quick",), ("ltn_rom.hex", "ucode.hex")),
}
sys.path.insert(0, str(HERE / "../../../scripts"))
from suite_tally import log_reports_failure  # noqa: E402

#: the two image constants: the stores' reset value and the window's source
IMG_IN = "  localparam logic [AMAP_IN_KEYS_C*8-1:0] AMAP_IN_IMAGE_C = amap_in_image();"
IMG_OUT = "  localparam logic [AMAP_OUT_KEYS_C-1:0] AMAP_OUT_IMAGE_C = amap_out_image();"
#: the clip's reading of the processor's published rows, per direction
ROW_IN = ("      if ((s < ACMP_SINKS_C) && pp_aecp_fmt_in_v_w[s])\n"
          "        amap_in_ch_w[s] = pp_aecp_fmt_in_w[64*s + 22 +: 10];\n")
ROW_OUT = ("      if ((s < ACMP_SRC_C) && pp_aecp_fmt_out_v_w[s])\n"
           "        amap_out_ch_w[s] = pp_aecp_fmt_out_w[64*s + 22 +: 10];\n")
#: the boot writer's enable onto the two crossbar write legs
WRITER = "  wire amap_boot_wr_w   = amap_boot_r || amap_boot_last_r;"

EMPTY = [(IMG_IN, IMG_IN.replace("amap_in_image()", "'0")),
         (IMG_OUT, IMG_OUT.replace("amap_out_image()", "'0"))]

#: the CSR writer's hold at its four sites: the two crossbar write muxes and
#: the two stores (review R490-1 F1). The RAM sites are not planted alone:
#: on this shape the boot writer drives both write legs on every busy clock
#: and each mux gives that leg priority, so neither RAM site can change a
#: write here (README, "The boot window's guard arms").
HOLD = "&& !amap_boot_busy_w && !aecp_locked"
HOLD_CAPTURE_RAM = ("(!aecp_odmap_wr_p_w && !amap_edit_txn_active_r\n"
                    f"                     {HOLD}")
HOLD_RENDER_RAM = ("(!aecp_dmap_wr_p_w && !amap_edit_txn_active_r\n"
                   f"                     {HOLD}")
HOLD_OUT_STORE = (f"          {HOLD}\n"
                  "          && cfg_chmap_wr_en && cfg_chmap_wr_side")
HOLD_IN_STORE = (f"          {HOLD}\n"
                 "          && cfg_chmap_wr_en && !cfg_chmap_wr_side")


def unheld(site: str) -> tuple[str, str]:
    """The edit that removes the hold's term at one site."""
    return (site, site.replace(HOLD, "&& !aecp_locked"))


#: the window's end: its terminal, its sweep and the sweep's drain clock
TERMINAL = "if (amap_boot_r && (pp_restore_done_w || pp_restore_closed_w)) begin"
SWEEP = "        amap_boot_last_r <= 1'b1;\n"
DRAIN = "      amap_boot_drain_r <= amap_boot_last_r && amap_boot_wrap_w;"
WAIT = "  assign pp_amap_edit_wait_w = amap_boot_busy_w;"

# (leg, name, [(the text it replaces, its replacement)], the check it must fail)
MUTATIONS = [
    ("dynmap", "an empty reset: the power-on image holds no mapping", EMPTY,
     "[DYNMAP] power-on SPI 0: number_of_mappings"),
    ("dynmap", "no clip after the restore: the window ignores a restored input format",
     [(ROW_IN, "")],
     "[DYNMAP] restored SPI 0: number_of_mappings"),
    ("dynmap", "no output clip: the window ignores a STREAM_OUTPUT row",
     [(ROW_OUT, "")],
     "[DYNMAP] window, output row staged at 4 ch: capture RAM keys 0..7 hold "
     "the output map"),
    ("dynmap", "the boot writer never fills the crossbar RAMs",
     [(WRITER, "  wire amap_boot_wr_w   = 1'b0;")],
     "[DYNMAP] power-on: render RAM keys 2..9 hold the input map"),
    ("dynmap", "the CSR writer is not held while the boot writer is busy",
     [unheld(HOLD_CAPTURE_RAM), unheld(HOLD_RENDER_RAM), unheld(HOLD_OUT_STORE),
      unheld(HOLD_IN_STORE)],
     "[DYNMAP] CSR hold, input: no CSR write splits the store from the RAM"),
    ("dynmap", "the input store alone takes a CSR write while the writer is busy",
     [unheld(HOLD_IN_STORE)],
     "[DYNMAP] CSR hold, input: no CSR write splits the store from the RAM"),
    ("dynmap", "the output store alone takes a CSR write while the writer is busy",
     [unheld(HOLD_OUT_STORE)],
     "[DYNMAP] CSR hold, output: no CSR write splits the store from the RAM"),
    ("dynmap", "the boot window ignores the CLOSED terminal",
     [(TERMINAL, "if (amap_boot_r && pp_restore_done_w) begin")],
     "[DYNMAP] CSR hold, input: CSR lands in both once the sweep after CLOSED "
     "has ended"),
    ("dynmap", "no sweep after the restore's terminal",
     [(SWEEP, "        amap_boot_last_r <= 1'b0;\n")],
     "[DYNMAP] CLOSED on the roll-back's clock: render RAM keys 2..9 hold the "
     "input map"),
    ("dynmap", "no drain clock: busy ends while the last boot write is in flight",
     [(DRAIN, "      amap_boot_drain_r <= 1'b0;")],
     "[DYNMAP] CSR hold, input: no CSR write splits the store from the RAM"),
    ("dynmap", "the edit face never waits for the boot writer",
     [(WAIT, "  assign pp_amap_edit_wait_w = 1'b0;")],
     "[DYNMAP] edit meets the sweep: the ADD is answered only after the sweep "
     "ends"),
    ("dynmap", "the map writer never marks a record dirty",
     [("      amr_dirty_r <= amr_dirty_r | amr_set_w;\n",
       "      amr_dirty_r <= amr_dirty_r;\n")],
     "[MAPREC] empty: the window holds the codec's records and the pend has fallen"),
    ("dynmap", "an empty saved list reads as an erased record (#763)",
     [("          if ((amr_magic_r != 16'h1722) || (amr_hplen_r != amr_plen_w)) begin",
       "          if ((amr_magic_r != 16'h1722) || (amr_hplen_r != amr_plen_w)\n"
       "              || !((|amr_li_r) || (|amr_lo_r))) begin")],
     "[MAPREC] empty, after the power cycle: SPI 0: number_of_mappings"),
    ("dynmap", "no first-dirty window: the change is written at the next tick",
     [("            if (amr_mscnt_r == 10'd500) begin", "            if (1'b1) begin")],
     "[MAPREC] empty: the write waited out the 500 ms first-dirty window"),
    ("dynmap", "the restore refuses every framed record",
     [("                       || amr_refuse_r) begin", "                       || 1'b1) begin")],
     "[MAPREC] saved, after the power cycle: SPI 0: number_of_mappings"),
    ("dynmap", "the restore ignores the record's crc16",
     [("(amr_hcrc_r != amr_crc_r)", "1'b0")],
     "[MAPREC] torn input record: SPI 0: number_of_mappings"),
    ("dynmap", "a failed walk rolls nothing back",
     [("          amr_rb_r      <= 1'b1;\n", "          amr_rb_r      <= 1'b0;\n")],
     "[MAPREC] roll-back: SPI 0: number_of_mappings"),
    ("dynmap", "the roll-back sweeps the RAMs and leaves the stores",
     [("      if (amap_boot_r || amr_rb_r) begin", "      if (amap_boot_r) begin")],
     "[MAPREC] roll-back: SPI 0: number_of_mappings"),
    ("dynmap", "the roll-back puts the stores back and never sweeps the RAMs",
     [("        amap_boot_last_r <= amr_rb_r;", "        amap_boot_last_r <= 1'b0;")],
     "[MAPREC] roll-back: render RAM keys 2..9 hold the input list"),
    ("dynmap", "the map restore runs over the D3 walk's roll-back",
     [("(pp_restore_rb_w || (pp_rs_cause_w != 3'd0))", "(pp_rs_cause_w != 3'd0)")],
     "[MAPREC] D3 roll-back: SPI 0: number_of_mappings"),
    ("dynmap", "GET_AUDIO_MAP does not wait for the map restore",
     [("                          && (amr_rs_hold_r || !(amap_srv_r && amap_sel_match_w));",
       "                          && !(amap_srv_r && amap_sel_match_w);")],
     "[MAPREC] held GET: answered with the restored list"),
    ("dynmap", "the format judge does not wait for the map restore",
     [("                             || (amr_rs_run_w && (pp_gsi_kind_w == 2'd0)",
       "                             || (1'b0 && (pp_gsi_kind_w == 2'd0)")],
     "[MAPREC] held SET_STREAM_FORMAT: SUCCESS against the restored list"),
    ("dynmap", "the entity enable does not wait for the map restore",
     [("      .enable_i          ((pp_enable_w | cfg_adp_enable) && !amr_rs_hold_r),",
       "      .enable_i          (pp_enable_w | cfg_adp_enable),")],
     "[MAPREC] held GET: the entity enable waits for the map restore"),
    ("dynmap", "every phase-5 beat marks its record, changed or not (DR2b)",
     [("      if (amap_edit_live_wr_p && (amap_edit_type_r == DESC_STREAM_PORT_IN_C)",
       "      if (amap_edit_beat_w && (pp_amap_edit_phase_w == 3'd5) && amap_edit_context_w\n"
       "          && (amap_edit_type_r == DESC_STREAM_PORT_IN_C)")],
     "[MAPREC] unchanged: no record write follows an unchanged edit"),
    ("dynmap", "a restore write counts as a change",
     [("  assign amap_edit_live_wr_p = axis_resetn && amap_edit_beat_w && !amr_own_r",
       "  assign amap_edit_live_wr_p = axis_resetn && amap_edit_beat_w")],
     "[MAPREC] saved: the restore itself writes no record"),
    ("dynmap", "a change after the latch does not taint the write",
     [("      if (amr_set_r_w) amr_taint_r <= 1'b1;\n", "")],
     "[MAPREC] taint: the window ends on the final list"),
    ("dynmap", "a fourth attempt follows the third failure",
     [("          if (amr_fails_r == 2'd2) begin", "          if (amr_fails_r == 2'd3) begin")],
     "[MAPREC] failing writes: three attempts, then no more"),
    ("dynmap", "no backoff between attempts",
     [("            amr_st_r    <= AS_WBWAIT;", "            amr_st_r    <= AS_WLAT;")],
     "[MAPREC] failing writes: the attempts are at least 500 ms apart"),
    ("dynmap", "the last failed attempt raises no alarm",
     [("            amr_alarm_r <= 1'b1;", "            amr_alarm_r <= 1'b0;")],
     "[MAPREC] failing writes: the alarm (PP_STAT[4]) is raised"),
    ("dynmap", "the map restore has no per-wait deadline",
     [("(amr_rs_w ? AMR_RS_TMO_CYC_P : AMR_MEM_TMO_CYC_P)",
       "(amr_rs_w ? 32'h7FFF_FFFF : AMR_MEM_TMO_CYC_P)")],
     "[MAPREC] silent memory: the restore reached its terminal and the map restore ended"),
    ("dynmap", "the arbiter does not drain a read the map writer abandoned",
     [("        da_drain_r <= 1'b1;\n", "        da_drain_r <= 1'b0;\n")],
     "[MAPREC] silent memory, late answer: a later change reaches the window", "shadow"),
    ("dynmap", "the arbiter's selection moves while the backend serves a command",
     [("  assign da_free_w = !nvm_busy_w && !nvm_gnt_w && !nvm_done_w && !nvm_err_w\n",
       "  assign da_free_w = !nvm_gnt_w && !nvm_done_w && !nvm_err_w\n")],
     "[MAPREC] shared face: both writers' records are in the window", "shadow"),
    ("dynmap", "the map writer's pending is not reported",
     [("                    | amap_unflushed_i\n", "")],
     "[MAPREC] empty: PP_STAT pend rises with the accepted change", "shadow"),
    ("dynmap", "the map writer's alarm does not reach nvm_alarm",
     [("      .alarm_i         (nvm_alarm_w | amap_alarm_i),", "      .alarm_i         (nvm_alarm_w),"),
      ("  assign nvm_alarm_o     = nvm_alarm_w | amap_alarm_i;", "  assign nvm_alarm_o     = nvm_alarm_w;")],
     "[MAPREC] failing writes: the alarm (PP_STAT[4]) is raised", "shadow"),
    ("listener", "an empty reset, under the listener's end-to-end check", EMPTY,
     "T18 POWER-ON: with no map command since the reset, the lane renders "
     "injected events"),
    ("talker", "an empty reset, under the talker's end-to-end check", EMPTY,
     "[V] every requested column was decoded"),
]


def build(leg: str, dp_path: Path, mdir: Path,
          shadow_path: Path | None = None) -> Path | None:
    """Build `leg` against `dp_path` (and `shadow_path` for KL_pp_shadow, the
    suite's own copy when None) through its suite's own recipe; the
    executable, or None when the recipe failed or left none. The generated
    inputs the leg reads are the clean build's: `-o` keeps them unmade."""
    suite, target, mvar, _clean, exe_name, _args, keep = LEGS[leg]
    cmd = ["make", "-s", "-C", str(suite)]
    for name in keep:
        cmd += ["-o", name]
    cmd += [target, f"DP_SRC={dp_path}", f"{mvar}={mdir}"]
    if shadow_path is not None:
        cmd += [f"SHADOW_SRC={shadow_path}"]
    out = subprocess.run(cmd, capture_output=True, text=True, check=False)
    exe = mdir / exe_name
    if out.returncode != 0 or not exe.is_file():
        sys.stdout.write(out.stdout[-2000:])
        sys.stdout.write(out.stderr[-2000:])
        return None
    return exe


def run_leg(leg: str, exe: Path) -> tuple[int, str]:
    """(rc, stdout) of one run of `leg`, from its suite directory, with no
    host deadline: every leg is cycle-bounded (module docstring)."""
    suite, _t, _m, _c, _e, args, _k = LEGS[leg]
    out = subprocess.run([str(exe), *args], cwd=str(suite), capture_output=True,
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


def plant(name: str, edits: list[tuple[str, str]], work: Path, tag: str,
          source: Path = DP_RTL) -> Path | None:
    """Write the mutant's copy of `source` (the datapath unless the arm names
    KL_pp_shadow); None when a pattern no longer matches exactly once, so the
    mutant would mutate nothing."""
    text = source.read_text()
    for pattern, replacement in edits:
        count = text.count(pattern)
        if count != 1:
            print(f"[FAIL] mutation {name!r}: a pattern appears {count} time(s) in "
                  f"{source.name}, expected exactly 1. The RTL moved and this "
                  f"mutant is no longer mutating anything - fix the pattern, do not "
                  f"delete the arm.")
            return None
        text = text.replace(pattern, replacement)
    out = work / f"{source.stem}_{tag}.sv"
    out.write_text(text)
    return out


def run_mutant(mutation: tuple, work: Path) -> bool:
    """Plant one mutation, build and run its leg; True when it was caught.
    A fifth element "shadow" plants it in KL_pp_shadow instead of the
    datapath."""
    leg, name, edits, breaks = mutation[:4]
    in_shadow = len(mutation) > 4 and mutation[4] == "shadow"
    tag = "".join(c if c.isalnum() else "_" for c in name)[:48]
    planted = plant(name, edits, work, tag, SHADOW_RTL if in_shadow else DP_RTL)
    if planted is None:
        return False
    if in_shadow:
        exe = build(leg, DP_RTL, work / f"obj_{tag}", planted)
    else:
        exe = build(leg, planted, work / f"obj_{tag}")
    if exe is None:
        print(f"[FAIL] mutation {name!r} did not compile; a mutant that cannot build "
              f"proves nothing about the leg")
        return False
    rc, out = run_leg(leg, exe)
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


def selected(argv: list[str]) -> list[tuple] | None:
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
    with tempfile.TemporaryDirectory(prefix="dynmap-mutants-") as td:
        work = Path(td)
        for leg in dict.fromkeys(m[0] for m in mutations):
            suite, _t, _m, clean_mdir, exe_name, _a, _k = LEGS[leg]
            clean = suite / clean_mdir / exe_name
            exe = clean if clean.is_file() else build(leg, DP_RTL, work / f"obj_clean_{leg}")
            answer = verdict(*run_leg(leg, exe), None) if exe else "did not compile"
            if answer == "pass":
                passes += 1
                print(f"[PASS] the unmutated gateware still passes the {leg} leg")
            else:
                fails += 1
                print(f"[FAIL] the unmutated gateware does NOT pass the {leg} leg "
                      f"({answer}) - its mutant results are meaningless")
        for mutation in mutations:
            if run_mutant(mutation, work):
                passes += 1
            else:
                fails += 1
    print(f"\n{passes + fails} checks: {passes} PASS, {fails} FAIL")
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main())
