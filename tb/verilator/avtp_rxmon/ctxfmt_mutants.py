#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""Mutation arm for #946's LCTX format contract: sim_ctxfmt.cpp's [CF] checks can fail.

sim_ctxfmt.cpp holds, at the 8x8 shape's eight contexts, what the split
firmware's sink port relies on: a format written through the window while the
input is unbound survives the bind's walk, each context judges a PDU against
its own words, and an unbind keeps them (Milan v1.2 Table 5.6, 4.4.2.2). Each
defect below is one that would make the firmware's write insufficient; the
real engine is mutated one defect at a time and the SAME harness is rebuilt
through the Makefile's own recipe (`make ctxfmt-build` with RXMON_SRC and
CF_MDIR overridden). Each mutant must make the harness FAIL by its own
verdict, with the named check among the failures; a crash or an abort is not
a catch. The positive control is the unmutated engine, rebuilt here.

What bounds a run: the harness is cycle-bounded by construction, and the
host-time bound is the sweep's per-suite guard in scripts/run_all_suites.sh.

Usage: make -C tb/verilator/avtp_rxmon   (or python3 ctxfmt_mutants.py from there)
Exit 0 = every mutant was caught and the clean harness still passes.
"""

import signal
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[2] / "scripts"))
import mutant_stage  # noqa: E402
sys.path.insert(0, str(HERE))
from lockstep_mutants import failed_checks, verdict  # noqa: E402

RTL = HERE / "../../../hdl/ieee1722/avtp/KL_avtp_rx_monitor_ctx.sv"
EXE_NAME = "Vavtp_rxmon_ctxfmt"

# (name, the ONE text it replaces, its replacement, the check it must fail)
MUTATIONS = [
    ("bind walk provisions every stream: streams above 0 take fmt0_i's words at the bind",
     "            wrph_r <= (ev_s_r == '0) ? 4'd1 : 4'd5;",
     "            wrph_r <= 4'd1;",
     "[CF3] a PDU of the input's own channel count is accepted"),
    ("stream 0's alias: a stream above 0 is judged against fmt0_i's channel count",
     "          fmt_r[31:0] <= ram_q_r;",
     "          fmt_r[31:0] <= fmt0_i[31:0];",
     "[CF3] a PDU of the input's own channel count is accepted"),
    ("another context: the window's write lands in the neighbouring stream's words",
     "  assign ram_waddr_w = eng_we_w ? eng_waddr_w : lctx_wr_addr_i[AW_C-1:0];",
     "  assign ram_waddr_w = eng_we_w ? eng_waddr_w : (lctx_wr_addr_i[AW_C-1:0] ^ AW_C'(32));",
     "[CF2] the first in-format PDU is accepted"),
    ("an unbind's walk writes over the format: the unlock's MON_STATE write lands in FMT_HI",
     "            eng_waddr_w = laddr(ev_s_r, W_MONST_C);\n"
     "            eng_wdata_w = ram_q_r & ~32'h0000_1000;   // clear media_locked",
     "            eng_waddr_w = laddr(ev_s_r, W_FMT_HI_C);\n"
     "            eng_wdata_w = ram_q_r & ~32'h0000_1000;   // clear media_locked",
     "[CF5] the rebound input's first PDU is accepted"),
]


def build(rtl_path: Path, mdir: Path) -> Path | None:
    """Build the N=8 harness against `rtl_path` through the suite's own recipe; the executable, or None."""
    out = subprocess.run(["make", "-s", "-C", str(HERE), "ctxfmt-build", f"RXMON_SRC={rtl_path}",
                          f"CF_MDIR={mdir}"], capture_output=True, text=True, check=False)
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


def run_mutant(src: str, mutation: tuple[str, str, str, str], work: Path, index: int) -> bool:
    """Plant one mutation, build and run the harness; True when it was caught."""
    name, pattern, replacement, breaks = mutation
    if src.count(pattern) != 1:
        print(f"[FAIL] mutation {name!r}: its pattern appears {src.count(pattern)} time(s) in {RTL.name}, "
              f"expected exactly 1. The RTL moved and this mutant is no longer mutating anything - fix the "
              f"pattern, do not delete the arm.")
        return False
    mpath = work / f"KL_avtp_rx_monitor_ctx_m{index}.sv"
    mpath.write_text(src.replace(pattern, replacement))
    exe = build(mpath, work / f"obj_m{index}")
    if exe is None:
        print(f"[FAIL] mutation {name!r} did not compile; a mutant that cannot build proves nothing")
        return False
    answer = verdict(*run_harness(exe), breaks)
    if answer == "caught":
        _, out = run_harness(exe)
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
    src = RTL.read_text()
    passes = 0
    fails = 0
    with mutant_stage.directory("rxmon-ctxfmt-mutants-") as td:
        work = Path(td)
        exe = build(RTL.resolve(), work / "obj_clean")
        answer = verdict(*run_harness(exe), None) if exe else "did not compile"
        if answer == "pass":
            passes += 1
            print("[PASS] the unmutated context engine still passes the N=8 format contract")
        else:
            fails += 1
            print(f"[FAIL] the unmutated context engine does NOT pass ({answer}) - every mutant result is "
                  f"meaningless")
        for index, mutation in enumerate(MUTATIONS):
            if run_mutant(src, mutation, work, index):
                passes += 1
            else:
                fails += 1
    print(f"\n{passes + fails} checks: {passes} PASS, {fails} FAIL")
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main())
