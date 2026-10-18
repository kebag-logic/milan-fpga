#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""Mutation arm for the gasket suite: prove its 81 checks are load-bearing.

Why this exists. `sim_main.cpp` drives the TX and RX MII gaskets and the two
dual-clock FIFOs around them, and checks delivery, byte counts, the SFD
toggles and back-to-back framing - and nothing proved any of those checks
could fail. A harness whose assertions never fail is indistinguishable from a
harness that asserts nothing, and this suite is the one that pins the defect
the gasket was repaired for: a TX FIFO level truncated below its full width
reads a completely full FIFO as empty and wedges the transmitter in S_IDLE
forever. A silently vacuous suite here would let exactly that defect return.

So the real bench RTL is mutated, one defect at a time, and the SAME harness
is run against each mutant. Every mutant must make it FAIL. The unmutated
build must still PASS - without that control the arm would be satisfied by a
harness that fails on everything.

"Caught" means the harness's own tally says so; see tb/mutation_verdict.py for
why a non-zero exit alone is not a catch. Mutants are built in a temporary
directory, so nothing is written into the tree.

What this arm found the suite does NOT prove, recorded rather than hidden,
because the value of a mutation arm is the map of what it cannot reach. Two
further defects SURVIVED the 81 checks and are therefore not listed above:
removing the start threshold entirely (`f_level_i >= 7'd8` reduced to
`!f_empty_i`, so the transmitter leaves S_IDLE before a startable burst is
buffered), and a read-side level off by one in bench_afifo. Both are real
defects the harness does not detect. Closing them needs new CHECKS, not new
mutants, and that is a change to sim_main.cpp rather than to this file.
"""

from __future__ import annotations

import subprocess
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
BENCH = (HERE / "../../../bench/arty").resolve()
sys.path.insert(0, str((HERE / "../../").resolve()))

from mutation_verdict import verdict  # noqa: E402

#: the four sources the suite builds, mutated copies and all
SOURCES = ("bench_afifo.sv", "bench_mii_tx.sv", "bench_mii_rx.sv")
TOP_SV = "gasket_tb_top.sv"

#: (name, file, pattern, replacement, the assertion this defect should break)
MUTATIONS = [
    ("tx fifo level truncated", "bench_mii_tx.sv",
     "input  wire  [6:0] f_level_i,",
     "input  wire  [5:0] f_level_i,",
     "a FIFO holding exactly 64 words reports a level the gasket can see, "
     "instead of reading 0 and wedging S_IDLE"),
    ("tx sfd toggle frozen", "bench_mii_tx.sv",
     "          sfd_toggle_o <= ~sfd_toggle_o;",
     "          sfd_toggle_o <= sfd_toggle_o;",
     "the egress timestamp point is marked once per frame at the SFD"),
    ("rx sfd toggle frozen", "bench_mii_rx.sv",
     "            sfd_toggle_o <= ~sfd_toggle_o;",
     "            sfd_toggle_o <= sfd_toggle_o;",
     "the ingress timestamp point is marked once per frame at the SFD"),
    ("rx end of frame never raised", "bench_mii_rx.sv",
     "              b_eof_o   <= 1'b1;",
     "              b_eof_o   <= 1'b0;",
     "a delivered frame is terminated, so the receiver can count its bytes"),
]

VFLAGS = [
    "--cc", "--exe", "--build", "-j", "0", "--top-module", "gasket_tb_top",
    "-Wall", "-Wno-fatal", "-Wno-DECLFILENAME", "-Wno-UNUSEDSIGNAL",
    "-Wno-WIDTHEXPAND", "-Wno-WIDTHTRUNC", "-Wno-UNUSEDPARAM",
]


def build(srcdir: Path, workdir: Path, tag: str) -> Path | None:
    """Build the harness against the sources in `srcdir`; the exe, or None."""
    mdir = workdir / f"obj_{tag}"
    exe_name = f"Vgasket_{tag}"
    out = subprocess.run(
        ["verilator", *VFLAGS, "--Mdir", str(mdir),
         "-CFLAGS", f"-std=c++17 -O2 -I{HERE}",
         *[str(srcdir / s) for s in SOURCES], str(srcdir / TOP_SV),
         str(HERE / "sim_main.cpp"), "-o", exe_name],
        capture_output=True, text=True)
    exe = mdir / exe_name
    if out.returncode != 0 or not exe.is_file():
        return None
    return exe


def run_harness(exe: Path) -> tuple[int, str]:
    """(rc, stdout) of one harness run.

    No host deadline: sim_main.cpp bounds its own waits in DUT cycles, so a
    wedged gasket FAILS the suite rather than hanging it - which is the very
    property the first mutant below exercises.
    """
    out = subprocess.run([str(exe)], capture_output=True, text=True)
    return out.returncode, out.stdout + out.stderr



def stage(work: Path, tag: str,
          mutate: tuple[str, str, str] | None = None) -> Path:
    """A directory holding the four sources, with at most one mutated.

    `mutate` is the (source, pattern, replacement) triple of MUTATIONS; the
    replacement is applied to that one source as it is copied, so the staged
    tree differs from bench/arty in exactly one place. Nothing outside the
    returned directory is written.
    """
    srcdir = work / f"src_{tag}"
    srcdir.mkdir()
    for name in SOURCES:
        text = (BENCH / name).read_text()
        if mutate is not None and mutate[0] == name:
            text = text.replace(mutate[1], mutate[2])
        (srcdir / name).write_text(text)
    (srcdir / TOP_SV).write_text((HERE / TOP_SV).read_text())
    return srcdir


def main() -> int:
    """Run the control and every mutant, and report the arm's exit status.

    0 when the unmutated bench RTL passes and all four mutants are caught;
    1 when any mutant survived, failed to build, or no longer matches its
    pattern - each of which is printed with the assertion it was defending.
    """
    passes = fails = 0
    with tempfile.TemporaryDirectory(prefix="gasket-mutants-") as td:
        work = Path(td)

        # -- positive control: the real RTL must still pass -------------------
        exe = build(stage(work, "clean"), work, "clean")
        answer = verdict(*run_harness(exe)) \
            if exe else "did not compile"
        if answer == "pass":
            passes += 1
            print("[PASS] the unmutated bench RTL still passes the harness")
        else:
            fails += 1
            print(f"[FAIL] the unmutated bench RTL does NOT pass ({answer}) - "
                  f"every mutant result below is meaningless")

        # -- each mutant must be caught ---------------------------------------
        for name, fname, pattern, replacement, breaks in MUTATIONS:
            src = (BENCH / fname).read_text()
            if src.count(pattern) != 1:
                fails += 1
                print(f"[FAIL] mutation {name!r}: its pattern appears "
                      f"{src.count(pattern)} time(s) in {fname}, expected "
                      f"exactly 1. The RTL moved and this mutant is no longer "
                      f"mutating anything - fix the pattern, do not delete "
                      f"the arm.")
                continue
            tag = name.replace(" ", "_")
            srcdir = stage(work, tag, (fname, pattern, replacement))
            exe = build(srcdir, work, tag)
            if exe is None:
                fails += 1
                print(f"[FAIL] mutation {name!r} did not compile; a mutant "
                      f"that cannot build proves nothing about the harness")
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
