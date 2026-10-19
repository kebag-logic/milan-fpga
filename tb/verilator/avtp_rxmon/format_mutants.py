#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""Mutation arm for the #765 current-format compare: prove the [UF] checks can fail.

sim_main_nx.cpp's [UF] phase grades KL_avtp_rx_monitor_ctx's format compare
against the Stream Input's CURRENT format (Milan v1.2 Table 5.6 and 4.4.2.2;
the channel count is part of the format, Table 6.2): a matching PDU is
accepted, a PDU with another channel count counts UNSUPPORTED_FORMAT and is
discarded, the full 10-bit channels_per_frame is compared, the compare follows
the format a controller sets, and stream 0 reads its format from fmt0_i. Each
defect below is the one its check exists for. The real engine is mutated one
defect at a time and the SAME harness is rebuilt through the Makefile's own
recipe (`make nx-build` with RXMON_SRC and NX_MDIR overridden). Each mutant
must make the harness FAIL by its own verdict, with the named check among the
failures; a crash or an abort is not a catch. The positive control is the
unmutated engine, rebuilt here.

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


def run_mutant(src: str, mutation: tuple[str, str, str, str], work: Path) -> bool:
    """Plant one mutation, build and run the harness; True when it was caught."""
    name, pattern, replacement, breaks = mutation
    if src.count(pattern) != 1:
        print(f"[FAIL] mutation {name!r}: its pattern appears {src.count(pattern)} "
              f"time(s) in {RTL.name}, expected exactly 1. The RTL moved and this "
              f"mutant is no longer mutating anything - fix the pattern, do not delete the arm.")
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
        print(f"[PASS] mutant caught: {name} - breaks \"{breaks}\"")
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
    print(f"\n{passes + fails} checks: {passes} PASS, {fails} FAIL")
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main())
