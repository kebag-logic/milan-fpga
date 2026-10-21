#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""Mutation arm for the render_queue suite: prove its assertions can fail.

Why this exists. `sim_main.cpp` grades every event KL_render_queue presents
to every interface byte-exact against a reference model of the presentation
law (#632), phase by phase, with the late, too-early and untimed counters,
the slips, a frame read a lap later, a flush, the timestamp wrap and the
observability taps. A harness whose assertions never fail is
indistinguishable from a harness that asserts nothing, and this stage is the
presentation law of the shipping render path.

So the real RTL is mutated, one defect at a time, and the SAME harness is run
against each mutant through the suite's own Makefile recipe (`make build`
with SRCS and MDIR overridden, plus the shape overrides a mutant names), so
the flag set is stated once. Every mutant must make the harness FAIL by its
OWN verdict (a `[FAIL]` line or a tally with failures, read by
scripts/suite_tally.py) AND the failure must be the check the mutant names:
a run that fails some other check proves nothing about that one. The
unmutated build must still PASS on every shape a mutant uses. A crash or an
abort is not a catch. Each pattern is REQUIRED to appear exactly once, so a
refactor that moves the code fails here instead of silently skipping a
mutant.

What bounds a livelocking mutant. This driver sets no host-time deadline
on a run (rule 8's wall-clock ratchet, scripts/test_evidence.budget item
4). The harness is cycle-bounded by construction: sim_main.cpp advances the
stage only through frame(), a fixed 100 cycles, and push(), a fixed beat
count inside it, and no loop in it waits on a DUT output, so every run ends
at the same cycle whatever the mutated stage does. The host-time bound is
the sweep's: scripts/run_all_suites.sh runs this suite's `make` (the `run`
target, then `odd`, then `mutants`) under its per-suite guard and reports a
kill as TIMEOUT, an UNKNOWN result (exit 92), never a pass or a fail. The
SIGTERM handler in main() turns that kill into an exit that removes the
temporary directory and the harness's own process group.

Usage: python3 mutants.py      (run from tb/verilator/render_queue)
Exit 0 = every mutant was caught and the clean build still passes.
"""

import os
import signal
import subprocess
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
RTL = HERE / "../../../hdl/ieee1722/aaf/KL_render_queue.sv"
sys.path.insert(0, str(HERE / "../../../scripts"))
from suite_tally import log_reports_failure  # noqa: E402

#: the shipping shape (`make odd`): one stream, one interface, 7 lanes
ODD_SHAPE = ("N_STREAMS=1", "N_CH=7", "N_IF=1", "LEAD1=0")

#: (name, ((pattern, replacement), ...), the assertion this defect must
#: break - one check name, or several, spelled as sim_main.cpp prints
#: them, the Makefile shape overrides the mutant runs under)
MUTATIONS = [
    ("a timestamp's frame truncated, not rounded to the nearest",
     (("          rem_r <= NW_C'({rem_r, 1'b0} + rem_r + NW_C'(PS3_C / 2));",
       "          rem_r <= NW_C'({rem_r, 1'b0} + rem_r);"),),
     "[round] every event presented to every interface is the frame the law names", ()),
    ("the divider's last quotient bit dropped",
     (("            f0_r  <= f0_r + FW_C'(q_r) + FW_C'({{(QW_C-1){1'b0}}, dge_w});",
       "            f0_r  <= f0_r + FW_C'(q_r);"),),
     "[place] every event presented to every interface is the frame the law names", ()),
    ("the timestamp difference taken on 31 bits (the 2^32 wrap misread)",
     (("  wire signed [31:0] d_w      = signed'(hdr_ts_ns_i - ev_ns_i);",
       "  wire signed [31:0] d_w      = signed'({1'b0, hdr_ts_ns_i[30:0]} - {1'b0, ev_ns_i[30:0]});"),),
     "[wrap] every event presented to every interface is the frame the law names", ()),
    ("every interface reads the smallest out-lead",
     (("  wire [FW_C-1:0] rd_fr_w = sn_r + FW_C'(lead_rd_w);",
       "  wire [FW_C-1:0] rd_fr_w = sn_r + FW_C'(KMIN_C);"),),
     "[place] every event presented to every interface is the frame the law names", ()),
    ("banked by lane parity alone: a straddling beat's two lanes share a bank",
     (("  wire        b0_w  = ch0_w[0] ^ fr0_w[0];\n  wire        b1_w  = ch1_w[0] ^ fr1_w[0];",
       "  wire        b0_w  = ch0_w[0];\n  wire        b1_w  = ch1_w[0];"),
      ("  wire  [24:0] even_w = rodd_r ? rd1_r : rd0_r;\n  wire  [24:0] odd_w  = rodd_r ? rd0_r : rd1_r;",
       "  wire  [24:0] even_w = rd0_r;\n  wire  [24:0] odd_w  = rd1_r;")),
     "[chans] every event presented to every interface is the frame the law names", ()),
    ("a consumed frame's rows left valid (no invalidation)",
     (("      we0_w = 1'b1; wa0_w = waddr(slot_r, cons_w[RW_C-1:0], beat_r); wd0_w = '0;\n"
       "      we1_w = 1'b1; wa1_w = waddr(slot_r, cons_w[RW_C-1:0], beat_r); wd1_w = '0;",
       "      we0_w = 1'b0; wa0_w = waddr(slot_r, cons_w[RW_C-1:0], beat_r); wd0_w = '0;\n"
       "      we1_w = 1'b0; wa1_w = waddr(slot_r, cons_w[RW_C-1:0], beat_r); wd1_w = '0;"),),
     "[lap] every event presented to every interface is the frame the law names", ()),
    ("a bind wipe ignored",
     (("        if (flush_i[s]) begin\n          flpend_r[s]    <= 1'b1;",
       "        if (flush_i[s]) begin\n          flpend_r[s]    <= 1'b0;"),),
     "[flush] every event presented to every interface is the frame the law names", ()),
    ("tv ignored",
     (("        pst_r  <= !hdr_tv_i ? P_UNTIMED_S",
       "        pst_r  <= 1'b0 ? P_UNTIMED_S"),),
     ("[untimed] every event presented to every interface is the frame the law names",
      "[untimed] untimed PDUs counted once each"), ()),
    ("a payload placed before its frame is known",
     (("  wire        place_w = sof_r ? (pst_r == P_OK_S) : pdu_ok_r;",
       "  wire        place_w = sof_r ? ((pst_r == P_OK_S) || (pst_r == P_DIV_S)) : pdu_ok_r;"),
      ("  wire        b_untimed_w = sof_r ? !((pst_r == P_OK_S) || (pst_r == P_LATE_S)"
       " || (pst_r == P_EARLY_S))",
       "  wire        b_untimed_w = sof_r ? !((pst_r == P_OK_S) || (pst_r == P_DIV_S)"
       " || (pst_r == P_LATE_S) || (pst_r == P_EARLY_S))")),
     "[untimed] untimed PDUs counted once each", ()),
    ("the per-event late rule removed",
     (("  wire        late0_w  = dr0_w[FW_C-1] || (dr0_w == '0);\n"
       "  wire        late1_w  = dr1_w[FW_C-1] || (dr1_w == '0);\n"
       "  wire        early0_w = !late0_w && (32'(dr0_w) >= ROWS_C);\n"
       "  wire        early1_w = !late1_w && (32'(dr1_w) >= ROWS_C);",
       "  wire        late0_w  = 1'b0;\n"
       "  wire        late1_w  = 1'b0;\n"
       "  wire        early0_w = !dr0_w[FW_C-1] && (32'(dr0_w) >= ROWS_C);\n"
       "  wire        early1_w = !dr1_w[FW_C-1] && (32'(dr1_w) >= ROWS_C);"),),
     "[late] every event presented to every interface is the frame the law names", ()),
    ("the per-event early rule removed",
     (("  wire        early0_w = !late0_w && (32'(dr0_w) >= ROWS_C);\n"
       "  wire        early1_w = !late1_w && (32'(dr1_w) >= ROWS_C);",
       "  wire        early0_w = 1'b0;\n"
       "  wire        early1_w = 1'b0;"),),
     "[early] every event presented to every interface is the frame the law names", ()),
    ("a gap in a presenting stream not counted",
     (("      if (rd0_end_w && !any_w && (32'(rs_r) == s) && live_r[s]) gap_w = 1'b1;",
       "      if (1'b0 && rd0_end_w && !any_w && (32'(rs_r) == s) && live_r[s]) gap_w = 1'b1;"),),
     "[slip] gaps and overlaps counted", ()),
    ("a PDU on a frame its stream wrote not counted",
     (("  assign b_slip_w = (!sof_r && pdu_slip_r) || overlap_w;",
       "  assign b_slip_w = 1'b0;"),),
     "[slip] gaps and overlaps counted", ()),
    ("lead_o kept after the stream drains",
     (("        if (lwv_r[s] && (sst_r == S_SCRUB_S) && (lead_s_w[s][FW_C-1] || (lead_s_w[s] == '0)))\n"
       "          lwv_r[s] <= 1'b0;",
       "        if (1'b0)\n          lwv_r[s] <= 1'b0;"),),
     "[place] lead_o and idle_o follow the model at every frame end", ()),
    ("each render tick after the first stream's last beat",
     (("        if (rv_r && rlastif_r && (32'(rif_r) == i)) render_tick_p_o[i] <= 1'b1;",
       "        if (rv_r && rlast_r && (32'(rif_r) == i)) render_tick_p_o[i] <= 1'b1;"),),
     "[if] each interface's render tick comes one cycle after its last beat, once per event", ()),
    ("a pop for an event without a sample",
     (("          if (any_w) pop_p_o[s] <= 1'b1;",
       "          pop_p_o[s] <= 1'b1;"),),
     "[obs] stream 0: one pop per interface-0 read with a sample", ()),
    ("converged kept through a gap",
     (("          if (!any_w) begin\n            conv_ms_r[s]   <= 7'd0;\n"
       "            converged_r[s] <= 1'b0;\n          end",
       "          if (!any_w) begin\n            conv_ms_r[s]   <= 7'd0;\n          end"),),
     "[obs] converged after 110 ms of steady presentation, and cleared by the gap after it", ()),
    ("the pad lane of an odd count read as a channel",
     (("      m_wire_chans_o[s*4 +: 4] = 4'(2 * PAIRS_C);",
       "      m_wire_chans_o[s*4 +: 4] = 4'(N_CH_P);"),),
     "[if] every stream presents 2 x ceil(N_CH / 2)", ODD_SHAPE),
]


def build(rtl_path: Path, workdir: Path, tag: str, shape: tuple[str, ...]) -> Path | None:
    """Build the harness against `rtl_path` through the suite's own recipe."""
    mdir = workdir / f"obj_{tag}"
    out = subprocess.run(
        ["make", "-s", "-C", str(HERE), "build", f"SRCS={rtl_path}", f"MDIR={mdir}", *shape],
        capture_output=True, text=True)
    exe = mdir / "VKL_render_queue_sim"
    if out.returncode != 0 or not exe.is_file():
        return None
    return exe


def run_harness(exe: Path) -> tuple[int, str]:
    """(rc, stdout) of one harness run, waited for with no host deadline: the
    harness is cycle-bounded (module docstring). The harness is its own
    session, so the sweep's kill reaches it only through the SIGTERM handler
    in main(), whose exit runs the kill below."""
    proc = subprocess.Popen([str(exe)], stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                            text=True, start_new_session=True)
    try:
        out, _ = proc.communicate()
        return proc.returncode, out
    finally:
        if proc.poll() is None:
            os.killpg(os.getpgid(proc.pid), signal.SIGKILL)
            proc.wait()


def named_checks(breaks: str | tuple[str, ...]) -> tuple[str, ...]:
    """The check name(s) a mutant must break, as a tuple."""
    return (breaks,) if isinstance(breaks, str) else breaks


def verdict(rc: int, out: str, must_fail: tuple[str, ...] = ()) -> str:
    """How the harness answered: 'pass', 'caught', or why it is not evidence.

    A harness failure is a catch only when the check the mutant NAMES is
    among the reported failures; the datapath driver
    (tb/verilator/milan_dp/render_mutants.py) makes the same demand.
    """
    reason, failed = log_reports_failure(out)
    if rc == 0 and not failed:
        return "pass"
    if rc == 0 and failed:
        return f"exited 0 but {reason} - a masked verdict is not evidence"
    if failed:
        lines = [line.strip() for line in out.splitlines()
                 if line.strip().startswith("[FAIL]")]
        missing = [w for w in must_fail
                   if not any(w in line for line in lines)]
        if missing:
            return ("failed, but not the named check(s) "
                    f"{', '.join(repr(w) for w in missing)}")
        return "caught"
    if rc < 0:
        return f"died by signal {-rc} with no harness verdict - a crash is not a catch"
    return f"exited {rc} with no harness verdict - a DUT abort is not a catch"


def mutate(src: str, edits: tuple[tuple[str, str], ...]) -> str | None:
    """The source with every edit applied, or None if any pattern is not unique."""
    for pattern, replacement in edits:
        if src.count(pattern) != 1:
            return None
        src = src.replace(pattern, replacement)
    return src


def main() -> int:
    """Run the positive controls and every mutant; 1 if any mutant survived."""
    src = RTL.read_text()
    passes = fails = 0
    signal.signal(signal.SIGTERM, lambda *_: sys.exit(143))
    with tempfile.TemporaryDirectory(prefix="render-queue-mutants-") as td:
        work = Path(td)
        clean = work / "KL_render_queue.sv"
        clean.write_text(src)
        shapes = sorted({m[3] for m in MUTATIONS})
        for shape in shapes:
            tag = "clean" + "".join("_" + s.replace("=", "") for s in shape)
            exe = build(clean, work, tag, shape)
            answer = verdict(*run_harness(exe)) if exe else "did not compile"
            label = " ".join(shape) if shape else "the default shape"
            if answer == "pass":
                passes += 1
                print(f"[PASS] the unmutated RTL still passes the harness on {label}")
            else:
                fails += 1
                print(f"[FAIL] the unmutated RTL does NOT pass on {label} ({answer}) - "
                      f"every mutant result on that shape is meaningless")
        for name, edits, breaks, shape in MUTATIONS:
            mutated = mutate(src, edits)
            if mutated is None:
                fails += 1
                counts = [src.count(p) for p, _ in edits]
                print(f"[FAIL] mutation {name!r}: its pattern(s) appear {counts} "
                      f"time(s), expected exactly 1 each. The RTL moved and this "
                      f"mutant is no longer mutating anything - fix the pattern, "
                      f"do not delete the arm.")
                continue
            tag = "".join(c if c.isalnum() else "_" for c in name)[:60]
            mpath = work / f"KL_render_queue_{tag}.sv"
            mpath.write_text(mutated)
            exe = build(mpath, work, tag, shape)
            if exe is None:
                fails += 1
                print(f"[FAIL] mutation {name!r} did not compile; a mutant that "
                      f"cannot build proves nothing about the harness")
                continue
            wanted = named_checks(breaks)
            shown = " and ".join(f'"{w}"' for w in wanted)
            answer = verdict(*run_harness(exe), wanted)
            if answer == "caught":
                passes += 1
                print(f"[PASS] mutant caught: {name} - breaks {shown}")
            elif answer == "pass":
                fails += 1
                print(f"[FAIL] mutant SURVIVED: {name}. The harness does not "
                      f"prove {shown}.")
            else:
                fails += 1
                print(f"[FAIL] mutant {name!r} {answer}")
    total = passes + fails
    print(f"\n{total} checks: {passes} PASS, {fails} FAIL")
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main())
