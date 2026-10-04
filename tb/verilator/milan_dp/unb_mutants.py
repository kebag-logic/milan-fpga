#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""Mutation arm for the #653 unbind order and Table 5.6 pair in milan_dp: prove the checks can fail.

sim_nxn.cpp's [UNB] section (the timed obj_notify leg) unbinds a locked AAF
input and the locked CRF Media Clock Input on the shipping AX 1x1 shape and
asserts that the UNBIND_RX response leaves before any GET_COUNTERS push
reporting the unlock (U2), that MEDIA_LOCKED = MEDIA_UNLOCKED from the
response on with STREAM_INTERRUPTED unmoved (U3), and that the 100 ms silence
timeout after the unbind does not count the unlock again (U4). Each defect
those checks exist for is planted where it would live - in a copy of the
processor's hdl/ tree or in a copy of KL_crf_rx - and the SAME leg is rebuilt
through the Makefile's own recipe (`make notify-build` with PP_DIR, CRFRX_SRC
and NOTIFY_MDIR overridden) and run. Each mutant must make the leg FAIL by
its OWN verdict (a `[FAIL]` line or a tally with failures, read by
scripts/suite_tally.py), every named check it breaks must be among the
failures, and every named check it holds must still pass, so a catch is
attributable to the planted defect and not to a run that went wrong
elsewhere; a crash or an abort is not a catch. The positive control is the
clean leg (obj_notify, which `make unb-mutants` builds and runs first),
re-run here.

The submodule checkout is never edited: the processor half of a mutant is
written into a copy of its hdl/ tree under a temporary directory, and the
copy is what the recipe's derived source list points at.

What bounds a run. This driver sets no host-time deadline (rule 8's
wall-clock ratchet, scripts/test_evidence.budget item 4). The leg is
cycle-bounded by construction: every phase runs to a fixed cycle target, an
AEM command waits at most 200,000 cycles for its answer, [UNB]'s wait ends
one processor-keepalive past the silence window whatever arrives, and the
AXI4-Lite BFM gives up after 4096 cycles per handshake. This is an explicit
campaign outside the sweep (docs/testing/TESTING.md), so run by hand nothing
but the cycle bound limits a run; the SIGTERM handler turns a kill into an
exit that removes the temporary directory.

Usage: make -C tb/verilator/milan_dp unb-mutants
       (or python3 unb_mutants.py [N ...] from tb/verilator/milan_dp, where
       each N selects one mutant by its 1-based place in MUTATIONS; the
       clean control runs every time)
Exit 0 = every selected mutant was caught and the clean leg still passes.
"""

import shutil
import signal
import subprocess
import sys
import tempfile
from pathlib import Path
from typing import NamedTuple

HERE = Path(__file__).resolve().parent
CRF_RTL = HERE / "../../../hdl/ieee1722/crf/KL_crf_rx.sv"
PP_HDL = HERE / "../../../protocol-processor/hdl"
#: the processor top, relative to its hdl/ tree
PP_TOP = Path("top") / "protocol_processor_top.sv"
CLEAN_MDIR = HERE / "obj_notify"
EXE_NAME = "Vmilan_dp_notify"
sys.path.insert(0, str(HERE / "../../../scripts"))
from suite_tally import log_reports_failure  # noqa: E402

#: the ACMP lane's request to the processor's TX arbiter, verbatim at the pin
PP_ACMP_REQ = "  assign arb_req_w[LANE_ACMP_C]     = laneq_acmp_cnt_r != 4'd0;"
#: ...held 6,000 cycles after the lane fills. The listener has queued its
#: response and gone idle, so the bind level falls, the unlock is counted and
#: its push (about +2,300 and +3,060 cycles) is requested on the AECP lane
#: while the response (+277 unmutated) still waits.
PP_ACMP_HELD = """  logic [12:0] acmp_hold_cyc_r;
  always_ff @(posedge clk_i) begin : acmp_hold
    if (!rst_n || (laneq_acmp_cnt_r == 4'd0)) acmp_hold_cyc_r <= 13'd6000;
    else if (acmp_hold_cyc_r != 13'd0)        acmp_hold_cyc_r <= acmp_hold_cyc_r - 13'd1;
  end
  assign arb_req_w[LANE_ACMP_C]     = (laneq_acmp_cnt_r != 4'd0)
                                    && (acmp_hold_cyc_r == 13'd0);"""
#: KL_crf_rx's unbind arm, verbatim
CRF_FALL = "      if (w_bind_fall_w && locked_o) begin\n"
CRF_FALL_DROP = CRF_FALL + "        locked_o       <= 1'b0;\n"
CRF_FALL_PUSH = ("        cnt_unlocked_o <= cnt_unlocked_o + 32'd1;\n"
                 "        dirty_p_o      <= 1'b1;\n")


class Mutation(NamedTuple):
    """One planted defect and what the leg must say about it."""
    name: str
    #: (file, the text it replaces, its replacement); file is "pp" for the
    #: processor top or "crf" for KL_crf_rx
    edits: list[tuple[str, str, str]]
    #: checks that must be among the failures
    breaks: list[str]
    #: checks that must still pass, so the catch is the planted defect's
    holds: list[str]


MUTATIONS = [
    Mutation("the processor holds every ACMP frame 6000 cycles, so the push overtakes the response",
             [("pp", PP_ACMP_REQ, PP_ACMP_HELD)],
             ["[UNB] AAF sink 0 U2 every push reporting the unlock to A left after the "
              "UNBIND_RX response",
              "[UNB] CRF sink 1 U2 every push reporting the unlock to A left after the "
              "UNBIND_RX response"],
             ["[UNB] AAF sink 0 U1 UNBIND_RX: the ACMP response is SUCCESS",
              "[UNB] AAF sink 0 U2 a push reporting the unlock reached A",
              "[UNB] CRF sink 1 U1 UNBIND_RX: the ACMP response is SUCCESS",
              "[UNB] CRF sink 1 U2 a push reporting the unlock reached A"]),
    Mutation("the CRF unbind does not count its unlock (the engine before #653)",
             [("crf", CRF_FALL, "      if (1'b0) begin\n")],
             ["[UNB] CRF sink 1 U3 as the response left: the source's MEDIA_LOCKED, "
              "MEDIA_UNLOCKED",
              "[UNB] CRF sink 1 U3 right after the response: MEDIA_UNLOCKED = MEDIA_LOCKED"],
             ["[UNB] CRF sink 1 U1 UNBIND_RX: the ACMP response is SUCCESS",
              "[UNB] AAF sink 0 U3 right after the response: MEDIA_UNLOCKED = MEDIA_LOCKED"]),
    Mutation("the CRF unbind keeps the lock, so the silence timeout counts the unlock again",
             [("crf", CRF_FALL_DROP, CRF_FALL)],
             ["[UNB] CRF sink 1 U4 past the silence timeouts: MEDIA_LOCKED, MEDIA_UNLOCKED, "
              "STREAM_INTERRUPTED",
              "[UNB] CRF sink 1 U3 every push after the response reads MEDIA_LOCKED = "
              "MEDIA_UNLOCKED"],
             ["[UNB] CRF sink 1 U3 right after the response: MEDIA_UNLOCKED = MEDIA_LOCKED",
              "[UNB] CRF sink 1 U4 the wait outlasted both 100 ms silence timeouts"]),
    Mutation("the CRF unbind also counts a STREAM_INTERRUPTED",
             [("crf", CRF_FALL, CRF_FALL + "        cnt_intr_o     <= cnt_intr_o + 32'd1;\n")],
             ["[UNB] CRF sink 1 U3 right after the response: STREAM_INTERRUPTED",
              "[UNB] CRF sink 1 U4 past the silence timeouts: MEDIA_LOCKED, MEDIA_UNLOCKED, "
              "STREAM_INTERRUPTED"],
             ["[UNB] CRF sink 1 U3 right after the response: MEDIA_UNLOCKED = MEDIA_LOCKED"]),
    Mutation("the CRF unbind counts its unlock but arms no push",
             [("crf", CRF_FALL_PUSH, "        cnt_unlocked_o <= cnt_unlocked_o + 32'd1;\n")],
             ["[UNB] CRF sink 1 U2 a push reporting the unlock reached A"],
             ["[UNB] CRF sink 1 U3 right after the response: MEDIA_UNLOCKED = MEDIA_LOCKED"]),
]


def build(crf_path: Path, pp_dir: Path, mdir: Path) -> Path | None:
    """Build the leg against `crf_path` and the processor tree `pp_dir`
    through the suite's own recipe; the executable, or None when the recipe
    failed or left none. The ROM images the leg reads are the clean build's:
    `-o` keeps a copied generator's newer timestamp from rewriting them."""
    out = subprocess.run(
        ["make", "-s", "-C", str(HERE), "-o", "ltn_rom.hex", "-o", "ucode.hex",
         "notify-build", f"CRFRX_SRC={crf_path}", f"PP_DIR={pp_dir}",
         f"NOTIFY_MDIR={mdir}"],
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


def marked(out: str, mark: str, check: str) -> bool:
    """Does a line of `out` led by `mark` name `check`?"""
    return any(line.strip().startswith(mark) and check in line
               for line in out.splitlines())


def verdict(rc: int, out: str, mutation: Mutation | None) -> str:
    """'pass', 'caught', or why the run is not evidence."""
    reason, failed = log_reports_failure(out)
    if rc == 0 and not failed:
        return "pass"
    if rc == 0 and failed:
        return f"exited 0 but {reason} - a masked verdict is not evidence"
    if failed:
        if mutation is None:
            return f"failed ({reason})"
        missed = [c for c in mutation.breaks if not marked(out, "[FAIL]", c)]
        if missed:
            return f"failed, but not the named check(s) {missed!r}"
        broken = [c for c in mutation.holds if not marked(out, "[ok]", c)]
        if broken:
            return (f"failed the named checks, but also {broken!r}, which must hold for "
                    f"the catch to be this defect's")
        return "caught"
    if rc < 0:
        return f"died by signal {-rc} with no harness verdict - a crash is not a catch"
    return f"exited {rc} with no harness verdict - a DUT abort is not a catch"


def plant(mutation: Mutation, work: Path, tag: str) -> tuple[Path, Path] | None:
    """Write the mutant's CRF engine and processor tree; None when a pattern
    no longer matches exactly once, so the mutant would mutate nothing."""
    files = {"crf": CRF_RTL, "pp": PP_HDL / PP_TOP}
    texts = {where: path.read_text() for where, path in files.items()}
    for where, pattern, replacement in mutation.edits:
        count = texts[where].count(pattern)
        if count != 1:
            print(f"[FAIL] mutation {mutation.name!r}: a pattern appears {count} time(s) in "
                  f"{files[where].name}, expected exactly 1. The RTL moved and this "
                  f"mutant is no longer mutating anything - fix the pattern, do not "
                  f"delete the arm.")
            return None
        texts[where] = texts[where].replace(pattern, replacement)
    crf_path = work / f"KL_crf_rx_{tag}.sv"
    crf_path.write_text(texts["crf"])
    pp_dir = work / f"pp_hdl_{tag}"
    shutil.copytree(PP_HDL, pp_dir)
    (pp_dir / PP_TOP).write_text(texts["pp"])
    return crf_path, pp_dir


def run_mutant(mutation: Mutation, work: Path) -> bool:
    """Plant one mutation, build and run the leg; True when it was caught."""
    tag = "".join(c if c.isalnum() else "_" for c in mutation.name)
    planted = plant(mutation, work, tag)
    if planted is None:
        return False
    exe = build(planted[0], planted[1], work / f"obj_{tag}")
    if exe is None:
        print(f"[FAIL] mutation {mutation.name!r} did not compile; a mutant that cannot "
              f"build proves nothing about the leg")
        return False
    rc, out = run_leg(exe)
    answer = verdict(rc, out, mutation)
    if answer == "caught":
        print(f"[PASS] mutant caught: {mutation.name} - breaks "
              f"{'; '.join(mutation.breaks)} ({log_reports_failure(out)[0]})")
        return True
    if answer == "pass":
        print(f"[FAIL] mutant SURVIVED: {mutation.name}. The leg does not prove "
              f"{'; '.join(mutation.breaks)}.")
    else:
        print(f"[FAIL] mutant {mutation.name!r} {answer}")
    return False


def selected(argv: list[str]) -> list[Mutation] | None:
    """The mutants `argv` names by 1-based place, every one when it names
    none; None when an argument names no mutant."""
    if not argv:
        return MUTATIONS
    picks = []
    for arg in argv:
        if not arg.isdigit() or not 1 <= int(arg) <= len(MUTATIONS):
            print(f"[FAIL] {arg!r} names no mutant: use 1..{len(MUTATIONS)}")
            return None
        picks.append(MUTATIONS[int(arg) - 1])
    return picks


def main() -> int:
    """Run the positive control and the selected mutants; 1 if any survived."""
    mutations = selected(sys.argv[1:])
    if mutations is None:
        return 2

    def on_sigterm(*_: object) -> None:
        """Exit on a kill so the temporary directory is removed."""
        sys.exit(143)

    signal.signal(signal.SIGTERM, on_sigterm)
    passes = 0
    fails = 0
    with tempfile.TemporaryDirectory(prefix="unb-mutants-") as td:
        work = Path(td)
        clean = CLEAN_MDIR / EXE_NAME
        exe = clean if clean.is_file() else build(CRF_RTL, PP_HDL, work / "obj_clean")
        answer = verdict(*run_leg(exe), None) if exe else "did not compile"
        if answer == "pass":
            passes += 1
            print("[PASS] the unmutated gateware still passes the obj_notify leg")
        else:
            fails += 1
            print(f"[FAIL] the unmutated gateware does NOT pass ({answer}) - every "
                  f"mutant result is meaningless")
        for mutation in mutations:
            if run_mutant(mutation, work):
                passes += 1
            else:
                fails += 1
    print(f"\n{passes + fails} checks: {passes} PASS, {fails} FAIL")
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main())
