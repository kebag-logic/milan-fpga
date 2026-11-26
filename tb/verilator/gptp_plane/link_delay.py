#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""Run the link delay verdict phase against isolated microcode defects.

FPGA-gPTP #109: a negative computed link delay of any magnitude is a good
exchange, the Sync path and the engine's publication use it signed and
floored at -800 ns, and +801 ns clears asCapable. The anchors are the pinned
generator's own. Each defect must fail the named checks of phase 6; the
unplanted image must pass all of them, so a defect cannot be caught by a
broken phase.
"""

import argparse
from pathlib import Path
import tempfile

from phc_step import GENERATOR, HERE, invoke, plant

#: the floor of the delay, D = max(D, -NPD_HI_C), and the two writes of it
FLOOR = ('    p.emit("ALU", rd=RT, ra=RD_, rb=0, cnd=ALU_ADD, imm=NPD_HI_C)\n'
         '    p.emit("ALU", rd=RU, ra=RT, rb=0, cnd=ALU_SAR, imm=63)\n'
         '    p.emit("ALU", rd=RT, ra=RT, rb=RU, cnd=ALU_AND)\n'
         '    p.emit("ALU", rd=RD_, ra=RD_, rb=RT, cnd=ALU_SUB)\n')
USED = '    p.emit("WRST", ra=RD_, imm=RG_SCR | S_PDELAY, fmt=FMT_Q)\n'
PUB = '    p.emit("WRST", ra=RD_, imm=RG_PUB | 3, fmt=FMT_Q)\n'
#: the verdict: bad iff D - (NPD_HI_C + 1) is not negative
VERDICT = ('    p.emit("ALU", rd=RT, ra=RD_, rb=0, cnd=ALU_SUB, imm=NPD_HI_C + 1)\n'
           '    p.emit("ALU", rd=RT, ra=RT, rb=0, cnd=ALU_SHR, imm=63)\n'
           '    p.emit("CMP", ra=RT, rb=0, fmt=FMT_D, imm=0)\n'
           '    p.emit("BRS", cnd=BRS_Z, label="bad")            # D - 801 >= 0\n')
#: what the pins before 3ce71b76 judged: good iff -80 <= D <= 800
OLD_WINDOW = ('    p.emit("ALU", rd=RT, ra=RD_, rb=0, cnd=ALU_ADD, imm=80)\n'
              '    p.emit("CMP", ra=RT, rb=0, fmt=FMT_D, imm=NPD_HI_C + 80 + 1)\n'
              '    p.emit("BRS", cnd=BRS_LT, label="good")\n'
              '    p.emit("BR", label="bad")\n')
#: the Sync path's value clamped to 0, the publication left signed
USED_CLAMPED = ('    p.emit("ALU", rd=RT, ra=RD_, rb=0, cnd=ALU_SAR, imm=63)\n'
                '    p.emit("ALU", rd=RT, ra=RD_, rb=RT, cnd=ALU_AND)\n'
                '    p.emit("ALU", rd=RT, ra=RD_, rb=RT, cnd=ALU_SUB)\n'
                '    p.emit("WRST", ra=RT, imm=RG_SCR | S_PDELAY, fmt=FMT_Q)\n')
EXACT = "its offset uses the delay exactly"
PUBLISHED = "the engine publishes the used delay"


def checks(what: str, *delays: str) -> tuple[str, ...]:
    """The named phase 6 checks of the trials `delays`."""
    return tuple(f"link delay {delay}: {what}" for delay in delays)


#: (name, pattern, replacement, every check it must fail)
DEFECTS = (
    ("delay-below-80-refused", VERDICT, OLD_WINDOW,
     checks("asCapable kept", "-81", "-263", "-800", "-801", "-5000000")),
    ("no-floor", FLOOR, "",
     checks(EXACT, "-801") + checks(PUBLISHED, "-801") + checks("no PHC step", "-5000000")),
    ("used-delay-clamped-to-zero", USED, USED_CLAMPED, checks(EXACT, "-3", "-80", "-81", "-263")),
    ("floor-at-zero", FLOOR, FLOOR.replace("imm=NPD_HI_C)", "imm=0)"),
     checks(EXACT, "-263") + checks(PUBLISHED, "-263")),
    ("floor-at-799", FLOOR, FLOOR.replace("imm=NPD_HI_C)", "imm=NPD_HI_C - 1)"),
     checks(EXACT, "-800") + checks(PUBLISHED, "-800")),
    ("published-before-the-floor", FLOOR + USED + PUB, PUB + FLOOR + USED, checks(PUBLISHED, "-801", "-5000000")),
    ("801-is-good", VERDICT, VERDICT.replace("NPD_HI_C + 1)", "NPD_HI_C + 2)"),
     checks("asCapable clears", "801") + checks("the next Follow_Up is not used", "801")),
    ("800-is-bad", VERDICT, VERDICT.replace("NPD_HI_C + 1)", "NPD_HI_C)"), checks("asCapable kept", "800")),
)


def run(work: Path, binary: Path) -> None:
    """Generate and run the unplanted image, then every defect's."""
    source = GENERATOR.read_text()
    arms: list[tuple[str, str, tuple[str, ...]]] = [("clean", source, ())]
    arms.extend((name, plant(source, name, None, old, new), named) for name, old, new, named in DEFECTS)
    for name, program, named in arms:
        directory = work / name
        directory.mkdir(parents=True, exist_ok=True)
        (directory / "generate.py").write_text(program)
        if invoke(["python3", "generate.py", "--clk-hz", "2000000", "-o", "gptp_ucode.hex"],
                  directory, directory / "generate.log"):
            raise RuntimeError(f"{name}: generation failed")
        status = invoke([str(binary), "+link-delay-only"], directory, directory / "run.log")
        log = (directory / "run.log").read_text()
        failed = [line for line in log.splitlines() if line.startswith("FAIL ")]
        if not named:
            if status != 0 or failed or " 0 FAIL" not in log:
                raise RuntimeError(f"{name}: the link delay phase failed")
            print(f"PASS control {name}: every check passes", flush=True)
            continue
        missing = [check for check in named if not any(line.startswith(f"FAIL {check} ") for line in failed)]
        if status != 1 or missing:
            raise RuntimeError(f"{name}: not rejected by {missing or 'a completed tally'}")
        print(f"PASS planted defect {name}: {' | '.join(named)}", flush=True)
    print(f"link_delay campaign: {len(arms)} checks: {len(arms)} PASS, 0 FAIL", flush=True)


def main() -> None:
    """Use a retained external directory when requested, otherwise clean up."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--binary", type=Path, default=HERE / "obj_dir" / "Vgptp_plane_sim")
    parser.add_argument("--work", type=Path)
    args = parser.parse_args()
    if not args.binary.is_file():
        raise SystemExit(f"{args.binary}: build it first (make run)")
    if args.work:
        run(args.work.resolve(), args.binary.resolve())
    else:
        with tempfile.TemporaryDirectory(prefix="gptp-link-delay-") as directory:
            run(Path(directory), args.binary.resolve())


if __name__ == "__main__":
    main()
