#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""Mutation arm for #765's format compare and #775's sequence advance: [UF], [SQ] can fail.

sim_main_nx.cpp's [UF] phase grades KL_avtp_rx_monitor_ctx's format compare
against the Stream Input's CURRENT format (Milan v1.2 Table 5.6 and 4.4.2.2;
the channel count is part of the format, Table 6.2): a matching PDU is
accepted, a PDU with another channel count counts UNSUPPORTED_FORMAT and is
discarded, the full 10-bit channels_per_frame is compared, the compare follows
the format a controller sets, and stream 0 reads its format from fmt0_i. The
[SQ] phase grades #775: a discarded off-format PDU was still received (Milan
v1.2 Table 5.6), so its sequence_num advances prev_seq, and it changes nothing
else (no mr reference or seed, no lock or settle, no timestamp word). Each
defect below is the one its check exists for. The real engine is mutated one
defect at a time and the SAME harness is rebuilt through the Makefile's own
recipe (`make nx-build` with RXMON_SRC and NX_MDIR overridden). Each mutant
must make the harness FAIL by its own verdict, with the named check among the
failures; a crash or an abort is not a catch. The positive control is the
unmutated engine, rebuilt here.

Four #775 defects move other state on a reject, each planted as the same
defect in the engine AND in the same line of the lockstep reference
(reference/KL_avtp_rx_monitor_ctx_ref.sv): a reject that sets media_locked,
which [SQ4] grades on an unlocked stream first in its era; one that steps
the settle count, which [SQ5] grades inside the settle window; one that sets
the mr seed, which [SQ6] grades before the era's first accepted PDU; and one
that clears it, which [SQ7] grades on a seeded stream. Both planted copies
are written, and the arm builds both: the N=4 stack from the planted engine
(it compiles no reference), and the lockstep leg at N=1 and N=8 from the
planted engine beside the planted reference (`make lockstep-build` with
RXMON_SRC, REF_SRC and LS_MDIR overridden). The arm is caught when the N=4
stack fails its named [SQ] check. The lockstep compare cannot see a defect
in both copies, so its result on the pair is printed as measured and does
not decide the arm; it is printed as checks/failures pairs, which the sweep's
tally does not count as checks of the shipping tree.

What bounds a run: the harness is cycle-bounded by construction, as the
lockstep arm's docstring states, and the host-time bound is the sweep's
per-suite guard in scripts/run_all_suites.sh.

Usage: make -C tb/verilator/avtp_rxmon   (or python3 format_mutants.py from there)
Exit 0 = every mutant was caught and the clean harness still passes.
"""

import re
import signal
import subprocess
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from lockstep_mutants import build as build_lockstep  # noqa: E402
from lockstep_mutants import failed_checks, verdict  # noqa: E402
from lockstep_mutants import run_harness as run_lockstep  # noqa: E402

RTL = HERE / "../../../hdl/ieee1722/avtp/KL_avtp_rx_monitor_ctx.sv"
REF = HERE / "reference/KL_avtp_rx_monitor_ctx_ref.sv"
EXE_NAME = "Vavtp_rxmon_nx_sim"

# (name, the ONE text it replaces, its replacement, the check it must fail)
MUTATIONS = [
    ("family compare: the channel count is not compared (the reading #765 replaces)",
     "                  (p_cpf_w     == f_cpf_w)     &&\n",
     "",
     "[UF2a] a 2-channel PDU against 8 channels has no accept verdict"),
    ("low byte: only channels_per_frame[7:0] is compared",
     "  wire [9:0] p_cpf_w    = cur_w.fsh[49:40];",
     "  wire [9:0] p_cpf_w    = {2'b00, cur_w.fsh[47:40]};",
     "[UF3a] a 264-channel PDU against 8 channels has no accept verdict"),
    ("inverted: a matching channel count is rejected",
     "                  (p_cpf_w     == f_cpf_w)     &&",
     "                  (p_cpf_w     != f_cpf_w)     &&",
     "[UF1a] a matching 8-channel PDU is accepted"),
    ("fixed count: the compare reads a constant, not the current format",
     "  wire [9:0] f_cpf_w     = fmt_r[31:22];",
     "  wire [9:0] f_cpf_w     = 10'd8;",
     "[UF4a] with a 2-channel current format, a 2-channel PDU is accepted"),
    ("stream 0: the channel word of fmt0_i is not loaded",
     "              fmt_r <= fmt0_i;              //! stream-0 format alias",
     "              fmt_r <= {fmt0_i[63:32], fmt_r[31:0]};",
     "[UF5a] stream 0: a 2-channel PDU against fmt0_i's 8 has no verdict"),
    ("no advance: a discarded PDU leaves prev_seq (the defect #775 fixes)",
     "            monst_r <= {ram_q_r[31:8], cur_w.seq};",
     "            monst_r <= ram_q_r;",
     "[SQ2c] SEQ_NUM_MISMATCH unchanged: the next PDU was in sequence"),
    ("whole state: a discarded PDU writes an accepted PDU's MON_STATE",
     "            monst_r <= {ram_q_r[31:8], cur_w.seq};",
     "            monst_r <= monst_next_w;",
     "[SQ2d] MEDIA_RESET unchanged"),
    ("accepted walk: a discarded PDU also writes the timestamp words",
     "            mst_r   <= M_PSEQ_S;",
     "            mst_r   <= M_PWR_S;",
     "[SQ1d] ...and it writes no timestamp word (LAST_TSD)"),
]

#: the reject's MON_STATE write-back, in the engine and in the reference;
#: BUNDLE stands for each one's PDU bundle (cur_w, cur_r)
REJECT_WB = "            monst_r <= {ram_q_r[31:8], BUNDLE.seq};"
BUNDLES = ("cur_w", "cur_r")
#: the lockstep harness's own tally line, one per shape
LS_TALLY = re.compile(r"lockstep N=(\d+): checks:\s*(\d+)\s+failures:\s*(\d+)")

# (name, the reject write-back's replacement, the check it must fail): the
# defect in both copies
BOTH_COPIES = [
    ("lock set: a discarded PDU sets media_locked",
     "            monst_r <= {ram_q_r[31:13], 1'b1, ram_q_r[11:8], BUNDLE.seq};",
     "[SQ4f] MEDIA_LOCKED +1 at the first accepted PDU"),
    ("settle step: a discarded PDU steps the settle count",
     "            monst_r <= {ram_q_r[31:12], (ram_q_r[11:8] == 4'd0) ? 4'd0 : "
     "(ram_q_r[11:8] - 4'd1), BUNDLE.seq};",
     "[SQ5c] a gap at the window's last PDU counts no SEQ_NUM_MISMATCH"),
    ("mr seed set: a discarded PDU sets the mr seed",
     "            monst_r <= {ram_q_r[31:24], 1'b1, ram_q_r[22:8], BUNDLE.seq};",
     "[SQ6e] ...and counts no MEDIA_RESET: it seeds the reference"),
    ("mr seed clear: a discarded PDU clears the mr seed",
     "            monst_r <= {ram_q_r[31:24], 1'b0, ram_q_r[22:8], BUNDLE.seq};",
     "[SQ7d] MEDIA_RESET +1 at the toggled PDU after the reject"),
]


def build(rtl_path: Path, mdir: Path) -> Path | None:
    """Build the N=4 harness against `rtl_path` through the suite's own recipe;
    the executable, or None when the recipe failed or left none."""
    out = subprocess.run(
        ["make", "-s", "-C", str(HERE), "nx-build", f"RXMON_SRC={rtl_path}",
         f"NX_MDIR={mdir}"],
        capture_output=True, text=True, check=False)
    exe = mdir / EXE_NAME
    if out.returncode != 0 or not exe.is_file():
        sys.stdout.write(out.stdout[-2000:])
        sys.stdout.write(out.stderr[-2000:])
        return None
    return exe


def run_harness(exe: Path) -> tuple[int, str]:
    """(rc, stdout) of one run, with no host deadline: the harness is cycle-bounded."""
    out = subprocess.run([str(exe)], cwd=str(HERE), capture_output=True, text=True,
                         check=False)
    return out.returncode, out.stdout + out.stderr


def anchored(text: str, pattern: str, name: str, where: str) -> bool:
    """True when `pattern` appears exactly once in `text`; reported when not."""
    if text.count(pattern) == 1:
        return True
    print(f"[FAIL] mutation {name!r}: its pattern appears {text.count(pattern)} "
          f"time(s) in {where}, expected exactly 1. The RTL moved and this "
          f"mutant is no longer mutating anything - fix the pattern, do not delete the arm.")
    return False


def run_mutant(src: str, mutation: tuple[str, str, str, str], work: Path) -> bool:
    """Plant one mutation in the engine, build and run the N=4 harness; True
    when it was caught."""
    name, pattern, replacement, breaks = mutation
    if not anchored(src, pattern, name, RTL.name):
        return False
    tag = name.split(":")[0].replace(" ", "_")
    mpath = work / f"KL_avtp_rx_monitor_ctx_{tag}.sv"
    mpath.write_text(src.replace(pattern, replacement))
    return graded(name, breaks, build(mpath, work / f"obj_{tag}"), "")


def graded(name: str, breaks: str, exe: Path | None, where: str) -> bool:
    """Run the N=4 harness `exe` of one mutant; True when it failed `breaks`."""
    if exe is None:
        print(f"[FAIL] mutation {name!r} did not compile; a mutant that cannot build "
              f"proves nothing about the harness")
        return False
    rc, out = run_harness(exe)
    answer = verdict(rc, out, breaks)
    if answer == "caught":
        broke = failed_checks(out)
        print(f"[PASS] mutant caught{where}: {name} - breaks \"{breaks}\"")
        print(f"    it broke {len(broke)} check(s): {'; '.join(broke)}")
        return True
    if answer == "pass":
        print(f"[FAIL] mutant SURVIVED: {name}. The harness does not prove \"{breaks}\".")
    else:
        print(f"[FAIL] mutant {name!r} {answer}")
    return False


def run_pair(src: str, ref: str, mutation: tuple[str, str, str], work: Path) -> bool:
    """Plant one mutation in the engine and in the reference, build the N=4
    harness from the planted engine and the lockstep leg from both planted
    copies; True when the N=4 harness caught it. The lockstep result on the
    pair is printed as measured."""
    name, replacement, breaks = mutation
    tag = name.split(":")[0].replace(" ", "_")
    planted = []
    for text, where, bundle, stem in ((src, RTL.name, BUNDLES[0], "ctx"),
                                      (ref, REF.name, BUNDLES[1], "ctx_ref")):
        pattern = REJECT_WB.replace("BUNDLE", bundle)
        if not anchored(text, pattern, name, where):
            return False
        path = work / f"KL_avtp_rx_monitor_{stem}_{tag}.sv"
        path.write_text(text.replace(pattern, replacement.replace("BUNDLE", bundle)))
        planted.append(path)
    caught = graded(name, breaks, build(planted[0], work / f"obj_{tag}"),
                    " (planted in the engine and the reference; the N=4 stack built "
                    "from the planted engine)")
    print(f"    planted copies: {planted[0].name} (the N=4 stack and the lockstep leg), "
          f"{planted[1].name} (the lockstep leg)")
    exes = build_lockstep(planted[0], work / f"obj_ls_{tag}", planted[1])
    if exes is None:
        print("    lockstep on the planted pair, as measured: did not compile")
        return False
    rc, out = run_lockstep(exes)
    # Restated as checks/failures pairs: the sweep's tally (scripts/suite_tally.py)
    # reads a harness tally on any line of this log, and a mutant pair's run is
    # neither a check of the shipping tree nor a verdict on this arm.
    shapes = ", ".join(f"N={n} {c}/{f}" for n, c, f in LS_TALLY.findall(out)) or "no tally"
    print(f"    lockstep on the planted pair, as measured and not graded: rc {rc}, "
          f"{shapes} (checks/failures)")
    return caught


def main() -> int:
    """Run the positive control and every mutant; 1 if any mutant survived."""
    def on_sigterm(*_: object) -> None:
        """Exit on a kill so the temporary directory is removed."""
        sys.exit(143)

    signal.signal(signal.SIGTERM, on_sigterm)
    src = RTL.read_text()
    ref_src = REF.read_text()
    passes = 0
    fails = 0
    with tempfile.TemporaryDirectory(prefix="rxmon-format-mutants-") as td:
        work = Path(td)
        exe = build(RTL, work / "obj_clean")
        answer = verdict(*run_harness(exe), None) if exe else "did not compile"
        if answer == "pass":
            passes += 1
            print("[PASS] the unmutated context engine still passes the N=4 harness")
        else:
            fails += 1
            print(f"[FAIL] the unmutated context engine does NOT pass ({answer}) - every "
                  f"mutant result is meaningless")
        for mutation in MUTATIONS:
            if run_mutant(src, mutation, work):
                passes += 1
            else:
                fails += 1
        for pair in BOTH_COPIES:
            if run_pair(src, ref_src, pair, work):
                passes += 1
            else:
                fails += 1
    print(f"\n{passes + fails} checks: {passes} PASS, {fails} FAIL")
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main())
