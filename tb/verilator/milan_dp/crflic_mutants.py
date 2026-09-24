#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""Mutation arm for the #530/#551 streaming licence in milan_dp: prove the checks can fail.

sim_crf_licence.cpp (the obj_crflic leg) asserts on the shipping AX 1x1 TDM8
shape that nothing is emitted while the processor declares and admits a
Stream Output that no Listener Ready has reached, and that the CRF licence
and the AAF gate require ACTIVE AND the real grant on every cycle. Before #530
all three consumers read the processor's raw admission verdict, which rises
at DECLARE_TALKER. So the real milan_datapath is mutated back, one consumer
at a time, and the SAME leg is rebuilt through the Makefile's own recipe
(`make crflic-build` with DP_SRC and CRFLIC_MDIR overridden) and run. Each
mutant must make the leg FAIL by its OWN verdict (a `[FAIL]` line or a tally
with failures, read by scripts/suite_tally.py), and the named check must be
among the failures; a crash or an abort is not a catch. The positive control
is the clean leg (obj_crflic, which `make crflic-mutants` builds and runs
first), re-run here.

The other half of #530's failing arms, the protocol processor at its previous
pin 424c688f, needs a second processor checkout and is not run here; the
leg's README records how it was run and what it reported.

What bounds a run. This driver sets no host-time deadline (rule 8's
wall-clock ratchet, scripts/test_evidence.budget item 4). The leg is
cycle-bounded by construction: every phase runs to a fixed cycle target, the
AXI4-Lite BFM gives up after 2048 cycles per handshake, and no loop waits on
a DUT output without a cycle bound, so a mutant ends at the same cycle as
the clean leg. This is an explicit campaign outside the sweep
(docs/testing/TESTING.md), so run by hand nothing but the cycle bound limits
a run; the SIGTERM handler turns a kill into an exit that removes the
temporary directory.

Usage: make -C tb/verilator/milan_dp crflic-mutants
       (or python3 crflic_mutants.py from tb/verilator/milan_dp)
Exit 0 = every mutant was caught and the clean leg still passes.
"""

import signal
import subprocess
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
DP_RTL = HERE / "../../../hdl/milan/milan_datapath.sv"
CLEAN_MDIR = HERE / "obj_crflic"
EXE_NAME = "Vmilan_dp_crflic"
sys.path.insert(0, str(HERE / "../../../scripts"))
from suite_tally import log_reports_failure  # noqa: E402

# (name, the exact source fragment, its replacement, the check it must fail)
MUTATIONS = [
    ("every gate reads the raw verdict",
     "  assign lwsrp_stream_gate = pp_cd_srp_active_w[SRP_TALKERS_C-1:0] &\n"
     "                             pp_cd_srp_sr_admitted_w[SRP_TALKERS_C-1:0];",
     "  assign lwsrp_stream_gate = pp_cd_srp_sr_admitted_w[SRP_TALKERS_C-1:0];",
     "the CRF licence never opened (every cycle sampled)"),
    ("the CRF licence alone reads the raw verdict",
     "                           lwsrp_stream_gate[SRP_TALKERS_C-1];",
     "                           pp_cd_srp_sr_admitted_w[SRP_TALKERS_C-1];",
     "the CRF licence equals ACTIVE[CRF] AND real grant"),
    ("the AAF source 0 gate alone reads the raw verdict",
     "                   (~cfg_lwsrp_enable | lwsrp_stream_gate[0])));",
     "                   (~cfg_lwsrp_enable | pp_cd_srp_sr_admitted_w[0])));",
     "the AAF gate never opened"),
    ("every gate drops the real grant",
     "  assign lwsrp_stream_gate = pp_cd_srp_active_w[SRP_TALKERS_C-1:0] &\n"
     "                             pp_cd_srp_sr_admitted_w[SRP_TALKERS_C-1:0];",
     "  assign lwsrp_stream_gate = pp_cd_srp_active_w[SRP_TALKERS_C-1:0];",
     "refused CRF licence never opened"),
    ("the CRF licence alone drops the real grant",
     "                           lwsrp_stream_gate[SRP_TALKERS_C-1];",
     "                           pp_cd_srp_active_w[SRP_TALKERS_C-1];",
     "refused CRF licence never opened"),
    ("the AAF source 0 gate alone drops the real grant",
     "                   (~cfg_lwsrp_enable | lwsrp_stream_gate[0])));",
     "                   (~cfg_lwsrp_enable | pp_cd_srp_active_w[0])));",
     "refused AAF gate never opened"),
]


def build(rtl_path: Path, mdir: Path) -> Path | None:
    """Build the leg against `rtl_path` through the suite's own recipe; the
    executable, or None when the recipe failed or left none."""
    out = subprocess.run(
        ["make", "-s", "-C", str(HERE), "crflic-build", f"DP_SRC={rtl_path}",
         f"CRFLIC_MDIR={mdir}"],
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


def run_mutant(src: str, mutation: tuple[str, str, str, str], work: Path) -> bool:
    """Plant one mutation, build and run the leg; True when it was caught."""
    name, pattern, replacement, breaks = mutation
    if src.count(pattern) != 1:
        print(f"[FAIL] mutation {name!r}: its pattern appears {src.count(pattern)} "
              f"time(s) in {DP_RTL.name}, expected exactly 1. The RTL moved and this "
              f"mutant is no longer mutating anything - fix the pattern, do not delete the arm.")
        return False
    tag = name.replace(" ", "_")
    mpath = work / f"milan_datapath_{tag}.sv"
    mpath.write_text(src.replace(pattern, replacement))
    exe = build(mpath, work / f"obj_{tag}")
    if exe is None:
        print(f"[FAIL] mutation {name!r} did not compile; a mutant that cannot build "
              f"proves nothing about the leg")
        return False
    answer = verdict(*run_leg(exe), breaks)
    if answer == "caught":
        print(f"[PASS] mutant caught: {name} - breaks \"{breaks}\"")
        return True
    if answer == "pass":
        print(f"[FAIL] mutant SURVIVED: {name}. The leg does not prove \"{breaks}\".")
    else:
        print(f"[FAIL] mutant {name!r} {answer}")
    return False


def main() -> int:
    """Run the positive control and every mutant; 1 if any mutant survived."""
    def on_sigterm(*_: object) -> None:
        """Exit on a kill so the temporary directory is removed."""
        sys.exit(143)

    signal.signal(signal.SIGTERM, on_sigterm)
    src = DP_RTL.read_text()
    passes = 0
    fails = 0
    with tempfile.TemporaryDirectory(prefix="crflic-mutants-") as td:
        work = Path(td)
        clean = CLEAN_MDIR / EXE_NAME
        exe = clean if clean.is_file() else build(DP_RTL, work / "obj_clean")
        answer = verdict(*run_leg(exe), None) if exe else "did not compile"
        if answer == "pass":
            passes += 1
            print("[PASS] the unmutated gateware still passes the obj_crflic leg")
        else:
            fails += 1
            print(f"[FAIL] the unmutated gateware does NOT pass ({answer}) - every "
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
