#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""Mutation arm for the render_setpoint suite: prove its assertions can fail.

Why this exists. `sim_main.cpp` asserts the setpoint law per PDU, the beat
format for four channel counts, the rails, the observer, the one-shot
recentre, the event-atomic pop and the crossbar walker's channel view - and
nothing proved any of those checks could fail. A harness whose assertions
never fail is indistinguishable from a harness that asserts nothing, and
this stage is the latency law of the shipping render path.

So the real RTL is mutated, one defect at a time, and the SAME harness is run
against each mutant through the suite's own Makefile recipe (`make build`
with SRCS and MDIR overridden, plus the shape overrides a mutant names), so
the flag set is stated once. Every mutant must make the harness FAIL by its
OWN verdict (a `[FAIL]` line or a tally with failures, read by
scripts/suite_tally.py); the unmutated build must still PASS on every shape a
mutant uses. A crash or an abort is not a catch. Each pattern is REQUIRED to
appear exactly once, so a refactor that moves the code fails here instead of
silently skipping a mutant.

The round-5 mutants are the review's own probes, kept as the failing
controls of the fixes: the pop re-reading the prefill flag every beat (a
flush or a prefill entry inside the pop window truncates the event), the
pop re-reading the head pointer every beat (a recentre snap inside the window
tears the event), the push ignoring a concurrent pop, the overrun drop
re-judged at every lane, the crossbar told N_CH_P lanes on a 7-lane build
(the pad lane wraps onto channel 0), and a wire channel count change ignored.

What bounds a livelocking mutant. This driver sets no host-time deadline
on a run (rule 8's wall-clock ratchet, scripts/test_evidence.budget item
4). The harness is cycle-bounded by construction, not by a cap constant:
sim_main.cpp advances the stage only through idle(n), a fixed cycle count,
run_to(target), a fixed cycle target, and push_pdu, a fixed beat count, and
no loop in it waits on a DUT output, so every run ends at the same cycle
whatever the mutated stage does. The host-time bound is the sweep's:
scripts/run_all_suites.sh runs this suite's `make` (the `run` target, then
`odd`, then `mutants`) under its per-suite guard, suite_timeout = 1800 s,
and reports a kill as TIMEOUT, an UNKNOWN result (exit 92), never a pass or
a fail. The SIGTERM handler in main() turns that kill into an exit that
removes the temporary directory and the harness's own process group. Run by
hand, outside the sweep, nothing but the cycle bound limits a run.

Usage: python3 mutants.py      (run from tb/verilator/render_setpoint)
Exit 0 = every mutant was caught and the clean build still passes.
"""

import os
import signal
import subprocess
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
RTL = HERE / "../../../hdl/ieee1722/aaf/KL_render_setpoint.sv"
sys.path.insert(0, str(HERE / "../../../scripts"))
from suite_tally import log_reports_failure  # noqa: E402

#: the 7-lane shape (`make odd`): an odd N_CH_P, where the last beat's second
#: lane is the pad the crossbar must never place on channel 0
ODD_SHAPE = ("N_CH=7",)

#: (name, ((pattern, replacement), ...), the assertion this defect should
#: break, the Makefile shape overrides the mutant runs under)
MUTATIONS = [
    ("prefill target three events high",
     (("localparam int unsigned TARGET_C = SETPOINT_EVT_P + PDU_EVENTS_P;",
       "localparam int unsigned TARGET_C = SETPOINT_EVT_P + PDU_EVENTS_P + 3;"),),
     "[L] every PDU's first event inside the law band", ()),
    ("recentre pulse ignored",
     (("if (recentre_p_i && !prefill_r[s]) pend_r[s] <= 1'b1;",
       "if (1'b0 && !prefill_r[s]) pend_r[s] <= 1'b1;"),),
     "[V] the pulse was consumed at the next PDU end", ()),
    ("recentre re-armed after the snap (not one-shot)",
     (("                rptr_r[s]    <= snap_rptr_w;\n"
       "                prefill_r[s] <= 1'b0;\n"
       "                pend_r[s]    <= 1'b0;\n",
       "                rptr_r[s]    <= snap_rptr_w;\n"
       "                prefill_r[s] <= 1'b0;\n"
       "                pend_r[s]    <= pend_r[s];\n"),),
     "[V] counted once, never again", ()),
    ("even-lane channel mask dropped",
     (("wire [23:0] smp_e_w  = (32'(lane_e_w) < 32'(c_pop_w)) ? rd_e_w : 24'd0;",
       "wire [23:0] smp_e_w  = rd_e_w;"),),
     "[C] 3 channels (straddle): lanes >= C read zero", ()),
    ("straddled even lane never written to an odd row",
     (("(st1_w && !ch1_w[0] &&  row1_w[0]);",
       "1'b0;"),),
     "[C] 3 channels (straddle) and mono: lanes < C byte-exact", ()),
    ("underrun leaves prefill off (repeat storm)",
     (("        if (pop_dry_w && (32'(slot_r) == s)) begin\n"
       "          prefill_r[s]   <= 1'b1;\n",
       "        if (pop_dry_w && (32'(slot_r) == s)) begin\n"
       "          prefill_r[s]   <= 1'b0;\n"),),
     "[U] no repeat storm: still one underrun", ()),
    ("high rail never snaps",
     (("              if (high_w) begin",
       "              if (1'b0) begin"),),
     "[R] two PDUs over: the high rail snapped once", ()),
    # ---- round 5: the review's probes as failing controls ----
    ("pop re-reads the prefill flag every beat (a flush or prefill entry inside the window truncates)",
     (("  wire            pop_ok_w   = first_beat_w ? pop_take_w : ev_ok_r;\n",
       "  wire            pop_ok_w   = first_beat_w ? pop_take_w : (ev_ok_r && !prefill_pop_w);\n"),),
     "[X] A: the event in flight reached the crossbar whole", ()),
    ("pop re-reads the head pointer every beat (a snap inside the window tears the event)",
     (("  wire [DEPTH_LOG2_P-1:0] rd_row_w = first_beat_w ? rptr_pop_w[DEPTH_LOG2_P-1:0]\n"
       "                                                  : ev_row_r;\n",
       "  wire [DEPTH_LOG2_P-1:0] rd_row_w = first_beat_w ? rptr_pop_w[DEPTH_LOG2_P-1:0]\n"
       "                                                  : DEPTH_LOG2_P'(rptr_pop_w - PW_C'(1));\n"),),
     "[X] B: the event in flight reached the crossbar whole (no tear)", ()),
    ("push ignores a concurrent pop",
     (("  wire  [PW_C-1:0] rptr_eff_in_w = rptr_in_w\n"
       "                                 + PW_C'(pop_take_w && (slot_r == s_tuser_i));\n",
       "  wire  [PW_C-1:0] rptr_eff_in_w = rptr_in_w\n"
       "                                 + PW_C'(1'b0 && pop_take_w && (slot_r == s_tuser_i));\n"),),
     "[X] D: a PDU end on the pop's own edge: dev +6 exactly trips no rail", ()),
    ("overrun drop re-judged at every lane (a pop inside a dropped event stores its tail)",
     (("  wire             drop0_w    = start0_w ? full0_w : evt_drop_r;\n",
       "  wire             drop0_w    = full0_w;\n"),),
     "[X] E: every rendered row is one event's (no half-stored row)", ()),
    ("crossbar told N_CH_P lanes (the pad lane of an odd count wraps onto channel 0)",
     (("      m_wire_chans_o[s*4 +: 4] = 4'(2 * PAIRS_C);\n",
       "      m_wire_chans_o[s*4 +: 4] = 4'(N_CH_P);\n"),),
     "[X] the crossbar contract held on every beat of the run", ODD_SHAPE),
    ("wire channel count change ignored",
     (("  wire chans_moved_w = s_ok_w && (chans_q_in_w != 4'd0) && (chans_q_in_w != c_in_w);\n",
       "  wire chans_moved_w = 1'b0 && s_ok_w && (chans_q_in_w != 4'd0) && (chans_q_in_w != c_in_w);\n"),),
     "[X] G: the first beat at the new count flushed and re-prefilled the stream", ()),
]


def build(rtl_path: Path, workdir: Path, tag: str, shape: tuple[str, ...]) -> Path | None:
    """Build the harness against `rtl_path` through the suite's own recipe."""
    mdir = workdir / f"obj_{tag}"
    out = subprocess.run(
        ["make", "-s", "-C", str(HERE), "build", f"SRCS={rtl_path}", f"MDIR={mdir}", *shape],
        capture_output=True, text=True)
    exe = mdir / "VKL_render_setpoint_sim"
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


def verdict(rc: int, out: str) -> str:
    """How the harness answered: 'pass', 'caught', or why it is not evidence."""
    reason, failed = log_reports_failure(out)
    if rc == 0 and not failed:
        return "pass"
    if rc == 0 and failed:
        return f"exited 0 but {reason} - a masked verdict is not evidence"
    if failed:
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
    with tempfile.TemporaryDirectory(prefix="render-setpoint-mutants-") as td:
        work = Path(td)
        clean = work / "KL_render_setpoint.sv"
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
            mpath = work / f"KL_render_setpoint_{tag}.sv"
            mpath.write_text(mutated)
            exe = build(mpath, work, tag, shape)
            if exe is None:
                fails += 1
                print(f"[FAIL] mutation {name!r} did not compile; a mutant that "
                      f"cannot build proves nothing about the harness")
                continue
            answer = verdict(*run_harness(exe))
            if answer == "caught":
                passes += 1
                print(f"[PASS] mutant caught: {name} - breaks \"{breaks}\"")
            elif answer == "pass":
                fails += 1
                print(f"[FAIL] mutant SURVIVED: {name}. The harness does not "
                      f"prove \"{breaks}\".")
            else:
                fails += 1
                print(f"[FAIL] mutant {name!r} {answer}")
    total = passes + fails
    print(f"\n{total} checks: {passes} PASS, {fails} FAIL")
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main())
