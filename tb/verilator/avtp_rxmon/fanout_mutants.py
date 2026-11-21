#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""Mutation arm for #948's fan-out: sim_fanout.cpp's [FO] checks can fail.

sim_fanout.cpp holds, at the 8x8 shape's eight contexts, that one talker
stream bound to several Stream Inputs is received by each of them (IEEE
1722.1-2021 8.2): the parser reports every matching table entry, the monitor
judges and counts the one PDU for each context, and the depacketizer reads
the one stored frame out once for each input that accepted it. Each defect
below breaks one link of that chain; the parser, the engine or the
depacketizer is mutated one defect at a time and the SAME harness is rebuilt
through the Makefile's own recipe (`make fanout-build` with PARSER_SRC,
RXMON_SRC or DEPKT_SRC and FO_MDIR overridden). Each mutant must make the
harness FAIL by its own verdict, with the named check among the failures; a
crash or an abort is not a catch. The positive control is the unmutated
stack, rebuilt here.

What bounds a run: the harness is cycle-bounded by construction, and the
host-time bound is the sweep's per-suite guard in scripts/run_all_suites.sh.

Usage: make -C tb/verilator/avtp_rxmon   (or python3 fanout_mutants.py from there)
Exit 0 = every mutant was caught and the clean harness still passes.
"""

import signal
import subprocess
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from lockstep_mutants import failed_checks, plant, verdict  # noqa: E402

RTL = HERE / "../../../hdl"
SOURCES = {
    "PARSER_SRC": RTL / "ieee1722/avtp/avtp_stream_parser.sv",
    "RXMON_SRC": RTL / "ieee1722/avtp/KL_avtp_rx_monitor_ctx.sv",
    "DEPKT_SRC": RTL / "ieee1722/aaf/KL_aaf_rx_depacketizer.sv",
}
EXE_NAME = "Vavtp_rxmon_fanout"

# (name, the source it mutates, [(the ONE text it replaces, its replacement)], the check it must fail)
MUTATIONS = [
    ("the parser's one index: each PDU goes to the highest matching entry alone (the defect #948 found)",
     "PARSER_SRC",
     [("          match_vec_o      <= match_vec;\n",
       "          match_vec_o      <= N_STREAMS'(1) << match_idx;\n")],
     "[FO1] accept verdicts: input 0"),
    ("the engine serves a bundle to its first context alone",
     "RXMON_SRC",
     [("            rem_r  <= disp_v_w & ~onehot(disp_s_w);\n",
       "            rem_r  <= '0;\n")],
     "[FO1] accept verdicts: input 1"),
    ("the done pulse leaves out the last context's own accept",
     "RXMON_SRC",
     [("              pdu_done_mask_o <= acc_r | onehot(ev_s_r);\n",
       "              pdu_done_mask_o <= acc_r;\n")],
     "[FO1] payloads reach the depacketizer's output under the input's index: input 1"),
    ("a new bundle inherits the previous bundle's accepts",
     "RXMON_SRC",
     [("            if (!pcont_w) acc_r <= '0;\n", "")],
     "[FO4] the 2-channel input: no payload: input 5"),
    ("the depacketizer reads a frame once: no pass for a second input",
     "DEPKT_SRC",
     [("  assign rewind_w   = fend_w && (rnext_w != '0);\n"
       "  assign release_w  = fend_w && (rnext_w == '0);\n",
       "  assign rewind_w   = 1'b0;\n"
       "  assign release_w  = fend_w;\n")],
     "[FO1] payloads reach the depacketizer's output under the input's index: input 1"),
    ("a second pass keeps the first pass's input",
     "DEPKT_SRC",
     [("      rs_r    <= lowest(rnext_w);\n", "      rs_r    <= rs_r;\n")],
     "[FO1] payloads reach the depacketizer's output under the input's index: input 0"),
    ("a second pass goes on from where the first ended, not from the frame's start",
     "DEPKT_SRC",
     [("      rp_r <= fs_r;\n", "      rp_r <= rp_r;\n")],
     "[FO1] payloads equal the sent ones, byte for byte, in order: input 1"),
    ("a frame no input accepted is read out to input 0",
     "DEPKT_SRC",
     [("            if (first_w && (sq_head_w == '0)) rstate_r <= R_FLUSH_S;\n", "")],
     "[FO7] the 8-channel PDU: payloads reach the depacketizer's output under the input's index: input 0"),
    ("the read side takes a frame before its verdicts are known",
     "DEPKT_SRC",
     [("  assign ff_ready = (rstate_r == R_HDR_S && (pass_r || sq_ne_w)) ||\n",
       "  assign ff_ready = (rstate_r == R_HDR_S) ||\n")],
     "[FO6] payloads equal the sent ones, byte for byte, in order"),
    ("a PDU queued after its frame ended waits for that frame's fate",
     "DEPKT_SRC",
     [("        rq_res_r[rq_a_w] <= !p7_r;\n", "        rq_res_r[rq_a_w] <= 1'b0;\n"),
      ("        if (p7_r) ifl_e_r <= rq_ap_r;\n", "        ifl_e_r <= rq_ap_r;\n")],
     "[FO8] only the full PDU reaches the depacketizer's output: input 0"),
    ("the verdict queue holds two entries, not the four a full ring and a lost PDU need",
     "DEPKT_SRC",
     [("  localparam int RQ_LOG2_C = 2;\n", "  localparam int RQ_LOG2_C = 1;\n")],
     "[FO9] only the three full PDUs reach the depacketizer's output"),
    ("a frame the full store dropped counts in no input's DEPKT drops",
     "DEPKT_SRC",
     [("          drop_p_o    <= 1'b1;\n", "          drop_p_o    <= 1'b0;\n")],
     "[FO10] every accepted PDU is delivered to the input or one of its DEPKT drops"),
]


def build(overrides: dict[str, Path], mdir: Path) -> Path | None:
    """Build the N=8 harness against the given sources through the suite's own recipe; the executable, or None."""
    args = [f"{k}={v}" for k, v in overrides.items()]
    out = subprocess.run(["make", "-s", "-C", str(HERE), "fanout-build", *args, f"FO_MDIR={mdir}"],
                         capture_output=True, text=True, check=False)
    exe = mdir / EXE_NAME
    if out.returncode != 0 or not exe.is_file():
        sys.stdout.write(out.stdout[-2000:])
        sys.stdout.write(out.stderr[-2000:])
        return None
    return exe


def run_harness(exe: Path) -> tuple[int, str]:
    """(rc, stdout) of one run, with no host deadline: the harness is cycle-bounded."""
    out = subprocess.run([str(exe)], cwd=str(HERE), capture_output=True, text=True, check=False)
    return out.returncode, out.stdout + out.stderr


def run_mutant(mutation: tuple[str, str, list[tuple[str, str]], str], work: Path, index: int) -> bool:
    """Plant one mutation, build and run the harness; True when it was caught."""
    name, which, edits, breaks = mutation
    src = SOURCES[which]
    text = plant(src.read_text(), edits, name, src.name)
    if text is None:
        return False
    mpath = work / f"m{index}_{src.name}"
    mpath.write_text(text)
    exe = build({which: mpath}, work / f"obj_m{index}")
    if exe is None:
        print(f"[FAIL] mutation {name!r} did not compile; a mutant that cannot build proves nothing")
        return False
    rc, out = run_harness(exe)
    answer = verdict(rc, out, breaks)
    if answer == "caught":
        broke = failed_checks(out)
        print(f"[PASS] mutant caught: {name} - breaks \"{breaks}\"")
        print(f"    it broke {len(broke)} check(s); first: {broke[0] if broke else '-'}")
        return True
    if answer == "pass":
        print(f"[FAIL] mutant SURVIVED: {name}. The harness does not prove \"{breaks}\".")
    else:
        print(f"[FAIL] mutant {name!r} {answer}")
    return False


def main() -> int:
    """Run the positive control and every mutant; 1 if any mutant survived."""
    def on_sigterm(*_: object) -> None:
        """Exit on a kill so the temporary directory is removed."""
        sys.exit(143)

    signal.signal(signal.SIGTERM, on_sigterm)
    passes = 0
    fails = 0
    with tempfile.TemporaryDirectory(prefix="rxmon-fanout-mutants-") as td:
        work = Path(td)
        exe = build({}, work / "obj_clean")
        answer = verdict(*run_harness(exe), None) if exe else "did not compile"
        if answer == "pass":
            passes += 1
            print("[PASS] the unmutated stack still passes the N=8 fan-out contract")
        else:
            fails += 1
            print(f"[FAIL] the unmutated stack does NOT pass ({answer}) - every mutant result is meaningless")
        for index, mutation in enumerate(MUTATIONS):
            if run_mutant(mutation, work, index):
                passes += 1
            else:
                fails += 1
    print(f"\n{passes + fails} checks: {passes} PASS, {fails} FAIL")
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main())
