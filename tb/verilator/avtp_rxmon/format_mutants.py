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
else (no mr reference, no lock or settle, no timestamp word). Each defect below
is the one its check exists for. The real engine is mutated one defect at a
time and the SAME harness is rebuilt through the Makefile's own recipe (`make
nx-build` with RXMON_SRC and NX_MDIR overridden). Each mutant must make the
harness FAIL by its own verdict, with the named check among the failures; a
crash or an abort is not a catch. The positive control is the unmutated
engine, rebuilt here.

Two #775 defects move the lock or settle state on a reject: a reject that sets
media_locked, which [SQ4] grades on an unlocked stream first in its era, and a
reject that steps the settle count, which [SQ5] grades inside the settle
window. Each is the defect written into the engine AND into the same line of
the lockstep reference (reference/KL_avtp_rx_monitor_ctx_ref.sv). The lockstep
compare cannot see a defect in both copies, so the [SQ] count check is the one
that must fail. The N=4 stack does not compile the reference, so its verdict
on the engine copy is its verdict on the pair; the arm checks that the
reference still carries the same line, and fails when it does not, because
the arm would then no longer be that defect.

What bounds a run: the harness is cycle-bounded by construction, as the
lockstep arm's docstring states, and the host-time bound is the sweep's
per-suite guard in scripts/run_all_suites.sh.

Usage: make -C tb/verilator/avtp_rxmon   (or python3 format_mutants.py from there)
Exit 0 = every mutant was caught and the clean harness still passes.
"""

import signal
import subprocess
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from lockstep_mutants import failed_checks, verdict  # noqa: E402

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

# (name, the ONE engine line it replaces, its replacement, the reference's ONE
# line, the check it must fail): the defect in both copies
BOTH_COPIES = [
    ("lock set: a discarded PDU sets media_locked",
     "            monst_r <= {ram_q_r[31:8], cur_w.seq};",
     "            monst_r <= {ram_q_r[31:13], 1'b1, ram_q_r[11:8], cur_w.seq};",
     "            monst_r <= {ram_q_r[31:8], cur_r.seq};",
     "[SQ4f] MEDIA_LOCKED +1 at the first accepted PDU"),
    ("settle step: a discarded PDU steps the settle count",
     "            monst_r <= {ram_q_r[31:8], cur_w.seq};",
     "            monst_r <= {ram_q_r[31:12], (ram_q_r[11:8] == 4'd0) ? 4'd0 : "
     "(ram_q_r[11:8] - 4'd1), cur_w.seq};",
     "            monst_r <= {ram_q_r[31:8], cur_r.seq};",
     "[SQ5c] a gap at the window's last PDU counts no SEQ_NUM_MISMATCH"),
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


def run_mutant(src: str, mutation: tuple[str, str, str, str], work: Path,
               ref: tuple[str, str] | None = None) -> bool:
    """Plant one mutation, build and run the harness; True when it was caught.
    Given `ref` = (reference text, its line), the reference must carry that
    line once, so the mutant is the same defect in both copies."""
    name, pattern, replacement, breaks = mutation
    if not anchored(src, pattern, name, RTL.name):
        return False
    if ref is not None and not anchored(ref[0], ref[1], name, REF.name):
        return False
    tag = name.split(":")[0].replace(" ", "_")
    mpath = work / f"KL_avtp_rx_monitor_ctx_{tag}.sv"
    mpath.write_text(src.replace(pattern, replacement))
    exe = build(mpath, work / f"obj_{tag}")
    if exe is None:
        print(f"[FAIL] mutation {name!r} did not compile; a mutant that cannot build "
              f"proves nothing about the harness")
        return False
    rc, out = run_harness(exe)
    answer = verdict(rc, out, breaks)
    if answer == "caught":
        broke = failed_checks(out)
        where = " (the defect in the engine and the reference)" if ref is not None else ""
        print(f"[PASS] mutant caught{where}: {name} - breaks \"{breaks}\"")
        print(f"    it broke {len(broke)} check(s): {'; '.join(broke)}")
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
        for name, pattern, replacement, ref_line, breaks in BOTH_COPIES:
            if run_mutant(src, (name, pattern, replacement, breaks), work,
                          (ref_src, ref_line)):
                passes += 1
            else:
                fails += 1
    print(f"\n{passes + fails} checks: {passes} PASS, {fails} FAIL")
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main())
