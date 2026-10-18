#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""Mutation arm for the parser suite: prove its rx_err_i checks are load-bearing.

Why this exists. FPGA-gPTP #35: `rx_err_i` was read only in the end-of-frame
branch, so a flag on any earlier byte was ignored and the frame dispatched,
and the suite stayed green because it only ever raised the flag with the
last byte. The repair latches the flag on any byte, and `sim_main.cpp` now
raises it at every byte position of four message types, and splits every
bank write of a flagged frame into those before, on and after the flagged
byte, none allowed after it (the ruling in #35). Checks that never
fail are indistinguishable from checks that assert nothing, so each defect
below is planted in the real parser RTL, one at a time, and the SAME harness
must fail on it. The unmutated build must still pass, without which the arm
would be satisfied by a harness that fails on everything.

"Caught" is stricter here than a red tally: every check a mutant names must
appear in a FAIL line, so an unrelated failure cannot stand in for the
evidence. See tb/mutation_verdict.py for why a non-zero exit alone is not a
catch. Everything is staged into a temporary directory, so nothing is
written into the tree.

The first mutant is the planted control the issue asks for: it deletes the
latch and so restores exactly the end-of-frame-only read the base shipped.
The last is the defect the ruling in #35 asks for: a refused frame's words
may stay in the write bank, so a clean frame behind it that skips one field
write would hand its event the refused frame's word.
"""

from __future__ import annotations

import subprocess
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
HDL = (HERE / "../../../hdl").resolve()
sys.path.insert(0, str((HERE / "../../").resolve()))

from mutation_verdict import verdict  # noqa: E402

#: the RTL the suite builds, in the order the Makefile lists it
RTL_SOURCES = ("ucpu/gptp_ucpu_pkg.sv", "wire/KL_gptp_rx_parser.sv")
PARSER = "wire/KL_gptp_rx_parser.sv"

VFLAGS = [
    "--cc", "--exe", "--build", "-j", "0", "--top-module", "KL_gptp_rx_parser",
    "-Wall", "-Wno-fatal", "-Wno-DECLFILENAME", "-Wno-UNUSEDSIGNAL",
    "-Wno-WIDTHEXPAND", "-Wno-WIDTHTRUNC", "-Wno-UNUSEDPARAM",
]

LATCH = "        if (rx_err_i) bad_r <= 1'b1;\n"
EOF_TERM = "fin_ok_r <= !bad_r && !rx_err_i && (cnt_r >= min_end_w) &&"
TYPES = ("sync", "fu", "pdreq", "pdresp")
#: the before/on/after oracle adds an Announce, whose deferred hop-count
#: word is the one write that can land after an eof
ORACLE_TYPES = TYPES + ("ann",)


def each(check: str, types: tuple[str, ...] = TYPES) -> tuple[str, ...]:
    """The named check, once per message type the sweep covers."""
    return tuple(f"{t} {check}" for t in types)


def oracle(check: str) -> tuple[str, ...]:
    """The named first/middle/eof oracle check, once per type it covers."""
    return each(f"rx_err at first, middle, eof: {check}", ORACLE_TYPES)


#: (clean, refused) pairs of the stale-word check
PAIRS = (("sync", "sync"), ("sync", "pdresp"), ("fu", "fu"), ("fu", "pdresp"),
         ("pdreq", "pdreq"), ("pdreq", "sync"), ("pdresp", "pdresp"),
         ("pdresp", "fu"))


def pairs(check: str) -> tuple[str, ...]:
    """The named stale-word check, once per pair it covers."""
    return tuple(f"{c} after a refused {r}: {check}" for c, r in PAIRS)


#: (name, [(pattern, replacement), ...] in the parser, checks that must FAIL)
MUTATIONS = [
    ("rx_err read only at eof (the planted control)",
     [(LATCH, "")],
     each("rx_err at every byte: one drop") +
     each("rx_err at every byte: no event") +
     each("rx_err at every byte: no later write") +
     oracle("one drop") + oracle("no event") + oracle("no write after")),
    ("a first-byte flag lost to the sof clear",
     [(LATCH, ""),
      ("      if (rx_valid_i) begin\n        if (rx_sof_i) begin\n",
       "      if (rx_valid_i) begin\n" + LATCH + "        if (rx_sof_i) begin\n")],
     each("rx_err at every byte: one drop") + oracle("one drop")),
    ("the eof byte's own flag ignored",
     [(EOF_TERM, "fin_ok_r <= !bad_r && (cnt_r >= min_end_w) &&")],
     each("rx_err at every byte: one drop") +
     each("rx_err at every byte: no event") +
     oracle("one drop") + oracle("no event") +
     ("ann rx_err at first, middle, eof: no write after",)),
    ("every flagged byte counts a drop",
     [(LATCH, "        if (rx_err_i) begin\n"
              "          bad_r <= 1'b1;\n"
              "          drop_cnt_r <= drop_cnt_r + 16'd1;\n"
              "        end\n")],
     each("rx_err held from byte 20 to eof: one drop")),
    ("rx_err ignored on every byte",
     [(LATCH, ""),
      (EOF_TERM, "fin_ok_r <= !bad_r && (cnt_r >= min_end_w) &&")],
     each("rx_err held from byte 20 to eof: no event")),
    ("the refusal outlives its frame",
     [("          bad_r    <= 1'b0;\n", "")],
     each("control after the errors: event") +
     each("control after the errors: no drop") +
     pairs("one drop") + pairs("event")),
    ("rx_err sampled between bytes",
     [(LATCH + "      end\n", "      end\n      if (rx_err_i) bad_r <= 1'b1;\n")],
     ("rx_err in every gap between bytes: sync event",
      "rx_err in every gap between bytes: no drop")),
    # the planted defect the ruling in #35 asks for: the clean frame behind
    # a refused one skips its source-identity write, so the refused frame's
    # w2 is what its event would read
    ("a refusal skips the next frame's w2 write",
     [("  logic        bad_r;          //! poisoned: consume to eof, then drop\n",
       "  logic        bad_r;          //! poisoned: consume to eof, then drop\n"
       "  logic        was_bad_r;\n"),
      ("      bad_r       <= 1'b0;\n",
       "      bad_r       <= 1'b0;\n      was_bad_r   <= 1'b0;\n"),
      ("          bad_r    <= 1'b0;\n",
       "          bad_r    <= 1'b0;\n          was_bad_r <= bad_r;\n"),
      ("              bank_we_o    <= !bad_r;\n              bank_addr_o  <= 5'd2;\n",
       "              bank_we_o    <= !bad_r && !was_bad_r;\n"
       "              bank_addr_o  <= 5'd2;\n")],
     pairs("every word is this frame's")),
]


def stage(work: Path, tag: str,
          edits: list[tuple[str, str]] | None = None) -> Path:
    """A directory holding the RTL, with the parser edited by `edits`.
    Nothing outside the returned directory is written."""
    srcdir = work / f"src_{tag}"
    for name in RTL_SOURCES:
        target = srcdir / name
        target.parent.mkdir(parents=True, exist_ok=True)
        text = (HDL / name).read_text(encoding="utf-8")
        if edits and name == PARSER:
            for pattern, replacement in edits:
                text = text.replace(pattern, replacement)
        target.write_text(text, encoding="utf-8")
    return srcdir


def build(srcdir: Path, work: Path, tag: str) -> Path | None:
    """Build the harness against the RTL in `srcdir`; the exe, or None."""
    mdir = work / f"obj_{tag}"
    exe_name = f"Vparser_{tag}"
    out = subprocess.run(
        ["verilator", *VFLAGS, "--Mdir", str(mdir),
         "-CFLAGS", f"-std=c++17 -O2 -I{HERE} -Wall -Wextra",
         *[str(srcdir / s) for s in RTL_SOURCES],
         str(HERE / "sim_main.cpp"), "-o", exe_name],
        capture_output=True, text=True)
    exe = mdir / exe_name
    if out.returncode != 0 or not exe.is_file():
        return None
    return exe


def run_harness(exe: Path) -> tuple[int, str]:
    """(rc, output) of one harness run. The suite is a fixed directed
    sequence with no open-ended wait, so it needs no host deadline."""
    out = subprocess.run([str(exe)], capture_output=True, text=True)
    return out.returncode, out.stdout + out.stderr


def main() -> int:
    """Run the control and every mutant, and report the arm's exit status.

    0 when the unmutated RTL passes and every mutant fails each check it
    names; 1 when any mutant survived, missed a named check, failed to
    build, or no longer matches its pattern.
    """
    passes = fails = 0
    with tempfile.TemporaryDirectory(prefix="parser-mutants-") as td:
        work = Path(td)

        # -- positive control: the real RTL must still pass ------------------
        exe = build(stage(work, "clean"), work, "clean")
        answer = verdict(*run_harness(exe)) if exe else "did not compile"
        if answer == "pass":
            passes += 1
            print("[PASS] the unmutated parser still passes the harness")
        else:
            fails += 1
            print(f"[FAIL] the unmutated parser does NOT pass ({answer}) - "
                  f"every mutant result below is meaningless")

        # -- each mutant must fail every check it names ------------------------
        src = (HDL / PARSER).read_text(encoding="utf-8")
        for name, edits, breaks in MUTATIONS:
            stale = [p for p, _ in edits if src.count(p) != 1]
            if stale:
                fails += 1
                print(f"[FAIL] mutation {name!r}: a pattern no longer appears "
                      f"exactly once in {PARSER}. The RTL moved and this "
                      f"mutant is no longer mutating anything - fix the "
                      f"pattern, do not delete the arm.")
                continue
            tag = "".join(c if c.isalnum() else "_" for c in name)
            exe = build(stage(work, tag, edits), work, tag)
            if exe is None:
                fails += 1
                print(f"[FAIL] mutation {name!r} did not compile; a mutant "
                      f"that cannot build proves nothing about the harness")
                continue
            rc, output = run_harness(exe)
            answer = verdict(rc, output)
            failed = [line for line in output.splitlines()
                      if line.startswith("FAIL ")]
            missed = [check for check in breaks
                      if not any(check in line for line in failed)]
            if answer == "caught" and missed:
                answer = f"missed its named check(s): {', '.join(missed)}"
            if answer == "caught":
                passes += 1
                print(f"[PASS] mutant caught: {name} - fails all "
                      f"{len(breaks)} named check(s), first "
                      f"\"{breaks[0]}\"")
            elif answer == "pass":
                fails += 1
                print(f"[FAIL] mutant SURVIVED: {name}. The harness does not "
                      f"prove \"{breaks[0]}\".")
            else:
                fails += 1
                print(f"[FAIL] mutant {name!r} {answer}")

    total = passes + fails
    print(f"\n{total} checks: {passes} PASS, {fails} FAIL")
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main())
