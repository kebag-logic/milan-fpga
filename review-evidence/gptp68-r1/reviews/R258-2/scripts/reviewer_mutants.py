#!/usr/bin/env python3
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""Reviewer-owned generator mutants for the #68 policy, run against ONE
already-built head harness binary (a generator change moves only the ROM
image the simulation reads at start-up, as the suite's own arm does).

Each mutant is one exact textual replacement in a COPY of the head
generator; its pattern must occur exactly once. A mutant is CAUGHT when the
harness tally reports at least one failed check.

Usage: reviewer_mutants.py <head generator> <harness binary> <workdir> [jobs]
"""

import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

GENARGS = ["--clk-hz", "2000000", "--cease-ms", "3000"]

MUTANTS = [
    ("RM1 every good Pdelay verdict re-arms the link-up (rise test removed)",
     '    p.emit("BRS", cnd=BRS_Z, label="done")           # already capable\n',
     ""),
    ("RM2 the clamp saturates every excursion to +lim (sign pick removed)",
     '    p.emit("ALU", rd=reg, ra=reg, rb=RU, cnd=ALU_XOR)\n'
     '    p.emit("ALU", rd=reg, ra=reg, rb=RU, cnd=ALU_SUB)\n',
     ""),
    ("RM3 the locked threshold is one ns wider (100 001 ns)",
     '    p.emit("MOVE", rd=RT, ra=0, imm=STEP_LOCKED_NS_C - STEP_LINKUP_NS_C)\n',
     '    p.emit("MOVE", rd=RT, ra=0,'
     ' imm=STEP_LOCKED_NS_C - STEP_LINKUP_NS_C + 1)\n'),
    ("RM4 the link-up threshold is one ns wider (20 001 ns)",
     '    p.emit("ALU", rd=RB, ra=RB, rb=0, cnd=ALU_ADD, imm=STEP_LINKUP_NS_C)\n',
     '    p.emit("ALU", rd=RB, ra=RB, rb=0, cnd=ALU_ADD,'
     ' imm=STEP_LINKUP_NS_C + 1)\n'),
    ("RM5 the integrator clamp is one unit wider than the envelope",
     '    e_sat(p, RC, RUNTIME["ilim"], "sv_i")',
     '    e_sat(p, RC, RUNTIME["ilim"] + 1, "sv_i")'),
    ("RM6 the step writes +offset instead of -offset",
     '    p.emit("ALU", rd=RB, ra=R0, rb=RA, cnd=ALU_SUB)          # -offset\n',
     '    p.emit("ALU", rd=RB, ra=RA, rb=0, cnd=ALU_ADD, imm=0)\n'),
    ("RM7 the step arm writes the PI trim instead of the bare integrator",
     '    p.emit("RDST", rd=RT, imm=RG_SCR | S_INTG, fmt=FMT_Q)\n'
     '    p.emit("BR", label="sv_rate")\n',
     '    p.emit("BR", label="sv_slew")\n'
     '    p.emit("NOP")\n'),
]


def run_one(args):
    gen_text, binary, work, (name, pat, rep) = args
    tag = name.split()[0]
    d = work / tag
    d.mkdir(parents=True, exist_ok=True)
    n = gen_text.count(pat)
    if n != 1:
        return name, f"PATTERN COUNT {n} (not applied)", ""
    (d / "gen.py").write_text(gen_text.replace(pat, rep), encoding="utf-8")
    g = subprocess.run([sys.executable, "-B", str(d / "gen.py"), *GENARGS,
                        "-o", str(d / "gptp_ucode.hex")],
                       capture_output=True, text=True)
    if g.returncode != 0:
        return name, "GENERATOR REFUSED", g.stderr[-300:]
    r = subprocess.run([str(binary)], cwd=str(d), capture_output=True,
                       text=True)
    out = r.stdout + r.stderr
    (d / "run.log").write_text(out, encoding="utf-8")
    tally = [ln for ln in out.splitlines() if " checks: " in ln]
    fails = [ln for ln in out.splitlines() if ln.startswith("FAIL")]
    verdict = ("CAUGHT" if fails else "SURVIVED") if tally else \
        f"NO TALLY (rc {r.returncode})"
    return name, f"{verdict}: {tally[-1] if tally else ''}", \
        "\n".join("      " + f for f in fails[:4])


def main():
    gen, binary, work = Path(sys.argv[1]), Path(sys.argv[2]), Path(sys.argv[3])
    jobs = int(sys.argv[4]) if len(sys.argv) > 4 else 4
    text = gen.read_text(encoding="utf-8")
    with ThreadPoolExecutor(max_workers=jobs) as ex:
        for name, verdict, detail in ex.map(
                run_one, [(text, binary, work, m) for m in MUTANTS]):
            print(f"{name}: {verdict}")
            if detail:
                print(detail)


if __name__ == "__main__":
    main()
