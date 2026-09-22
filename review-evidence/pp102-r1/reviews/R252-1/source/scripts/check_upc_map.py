#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""The µPC map is written down twice; this makes the two copies agree.

WHY THIS EXISTS. `hdl/aecp/ucode/gen_ucode.py` places each microprogram at an
entry point `E_NAME = <addr>`, and `hdl/aecp/KL_aecp_engine.sv` dispatches to
it through a mirrored `localparam logic [10:0] UPC_NAME_C = 11'd<addr>`.
Nothing connected the two, and on 2026-08-16 they drifted twice inside one
change: a ROM re-layout moved `E_SCFG` from 1344 to 1456 while the engine went
on dispatching to 1344, which by then held a different program's first
instruction.

The failure mode is the reason this is a script and not a code review note.
A wrong µPC does NOT fail to elaborate, does not warn, and does not crash: the
µCPU simply starts executing at the wrong address, runs whatever it finds
(including the ROM's deterministic fill, which is full of register writes), and
emits a well-formed AECP response carrying garbage. The bench sees SUCCESS with
a plausible-looking body. It took a hex dump of the response to notice.

So: parse both files, compare the maps, and refuse a mismatch. A name present
in one and absent from the other is reported too — an engine constant with no
program behind it dispatches into fill just as surely as a wrong number.

Exit 0 = they agree. Exit 1 = they do not, and the diff is printed.
"""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
UCODE = ROOT / "hdl" / "aecp" / "ucode" / "gen_ucode.py"
ENGINE = ROOT / "hdl" / "aecp" / "KL_aecp_engine.sv"

#! `E_NAME = 1234` at the start of a line, comment optional. Deliberately NOT
#! matching indented assignments: a local in a function is not an entry point.
RE_UCODE = re.compile(r"^(E_[A-Z0-9_]+)\s*=\s*(\d+)\s*(?:#.*)?$", re.M)
#! `localparam logic [10:0] UPC_NAME_C = 11'd1234;`
RE_ENGINE = re.compile(
    r"localparam\s+logic\s*\[10:0\]\s+UPC_([A-Z0-9_]+)_C\s*=\s*11'd(\d+)\s*;")


RE_PLACED = re.compile(r"place\((E_[A-Z0-9_]+)\s*,")

def main() -> int:
    """The gate: every entry point is its own place() target and every engine
    UPC_ constant names that program's address; 1 prints the disagreement."""
    for path in (UCODE, ENGINE):
        if not path.exists():
            print(f"UPC MAP GATE: cannot read {path}", file=sys.stderr)
            return 1

    usrc = UCODE.read_text(encoding="utf-8")
    ucode = {m.group(1): int(m.group(2))
             for m in RE_UCODE.finditer(usrc)}
    #! An address that is only a NUMBER is an address that can drift: if a name
    #! points INTO another program's instruction list rather than at its own
    #! place() target, inserting one word above it moves the instruction and
    #! leaves the constant behind, and comparing two hand-written numbers still
    #! says PASS. A review demonstrated exactly that. Requiring every name to be
    #! a place() target is what makes the comparison below mean something.
    placed = set(RE_PLACED.findall(usrc))
    esrc = ENGINE.read_text(encoding="utf-8")
    engine = {m.group(1): int(m.group(2))
              for m in RE_ENGINE.finditer(esrc)}

    if not ucode or not engine:
        print("UPC MAP GATE: parsed nothing — the patterns have gone stale, "
              "which is itself a failure", file=sys.stderr)
        return 1

    #! The engine dispatches to a SUBSET: plenty of programs are reached only
    #! by a BRANCH from another program (E_RDSTUB, E_GCTRSNS, the FAIL arms) and
    #! never named by a localparam. So every ENGINE constant must have a
    #! matching program, but not every program needs a constant.
    problems = []
    for name, addr in sorted(ucode.items()):
        if name not in placed:
            problems.append(
                f"  {name} = {addr} is never a place() target. It names an "
                f"address INSIDE some other program, so an instruction added "
                f"above it moves the code and leaves this constant behind; "
                f"and this gate cannot see that. Give it its own place().")

    for name, addr in sorted(engine.items()):
        want = ucode.get("E_" + name)
        if want is None:
            problems.append(
                f"  UPC_{name}_C = {addr} has NO program: gen_ucode.py defines "
                f"no E_{name}. The µCPU would start in whatever lives at "
                f"{addr} — most likely the ROM fill.")
        elif want != addr:
            problems.append(
                f"  UPC_{name}_C = {addr} but E_{name} = {want}. The engine "
                f"dispatches {addr - want:+d} words away from the program.")

    if problems:
        print("UPC MAP GATE: FAIL — the engine and the µcode disagree\n")
        print("\n".join(problems))
        print("\nA wrong µPC does not fail to elaborate and does not warn; it\n"
              "executes the ROM fill and answers with a well-formed response\n"
              "carrying garbage. Fix the constant, do not widen this gate.")
        return 1

    print(f"UPC MAP GATE: PASS ({len(engine)} engine constants, "
          f"{len(ucode)} entry points, all agree)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
