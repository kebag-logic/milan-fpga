# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""The memory test's CPU decode arm (#791): the region pieces the split CPU's generator is handed, and the hookup.

test_ctrl_memory.py runs `arms` and `export_check`, which print and record each graded fact as its own `check`
does, and its mutants include MUTANTS, whose targets are PROPERTIES. The arm grades:

  - ctrl_memory.decode_pieces gives rom and sram as 128, 64 and 32 KiB at their origins. It gives every
    region of up to SWEEP units at every origin below SWEEP as aligned power-of-two pieces that are exactly
    the region, as few as a search over every aligned split finds (`fewest`);
  - cpu_regions hands the split SoC's list over as those pieces, each in its row's mode and on its bus;
  - milan_soc.exact_cpu_decode, on a stand-in VexiiRiscv that finalizes as LiteX's does, hands the CPU's
    naming step the pieces, before the name. It refuses one whose finalize never names its netlist, and
    leaves a CPU that is not a VexiiRiscv as it is;
  - `export_check`: the split export through milan_soc.main() hands the generator rom and sram as their
    pieces, and every row it hands it is an aligned power of two.

Every call looks `ctrl_memory` and `milan_soc` up when it runs, so a mutant rebinding one is graded.
"""

from __future__ import annotations

import types
from typing import Any
from unittest.mock import patch

import ctrl_memory
import milan_soc

#: rom and sram as the CPU generator is handed them: 128, 64 and 32 KiB at each origin.
PIECES = {"rom": ((0x0000_0000, 0x2_0000), (0x0002_0000, 0x1_0000), (0x0003_0000, 0x8000)),
          "sram": ((0x1000_0000, 0x2_0000), (0x1002_0000, 0x1_0000), (0x1003_0000, 0x8000))}
#: The split SoC's region list as LiteX collects it (#878's image), and as the generator must be handed it.
SPLIT_ROWS = [(0x0000_0000, 0x3_8000, "rxc", "p"), (0x1000_0000, 0x3_8000, "rwxc", "p"),
              (0x0100_0000, 0x100_0000, "rxc", "p"), (0x9000_0000, 0x1_0000, "rw", "p"),
              (0x9010_0000, 0x8000, "rw", "p"), (0xF000_0000, 0x1_0000, "rw", "p")]
SPLIT_PIECES = [*[(o, s, "rxc", "p") for o, s in PIECES["rom"]], *[(o, s, "rwxc", "p") for o, s in PIECES["sram"]],
                *SPLIT_ROWS[2:]]
#: The units the sweep runs over: every origin below it, every size up to it.
SWEEP = 64
#: What the mutants below target, beside test_ctrl_memory.py's own properties.
PROPERTIES = {
    "decode pieces": "decode_pieces gives a region as aligned power-of-two pieces, exactly the region (#791)",
    "exact decode": "the split CPU's generator is handed each region's pieces before it names its netlist (#791)",
    "decode guard": "a split CPU whose finalize never names its netlist is refused (#791)",
}
_HANDED = ("VexiiRiscv.memory_regions = ctrl_memory.cpu_regions(VexiiRiscv.memory_regions)\n"
           "        named.append(VexiiRiscv.memory_regions)\n        VexiiRiscv.generate_netlist_name()")
#: test_ctrl_memory.Mutant rows: name, target, owner, attribute, old, new, arm.
MUTANTS = (
    ("pieces unaligned", "decode pieces", "ctrl_memory", "decode_pieces",
     "piece = min(fits, origin & -origin) if origin else fits", "piece = fits", "decode"),
    ("the last piece dropped", "decode pieces", "ctrl_memory", "decode_pieces", "return tuple(pieces)",
     "return tuple(pieces[:-1])", "decode"),
    ("regions handed whole", "exact decode", "ctrl_memory", "cpu_regions",
     "for start, piece in decode_pieces(origin, size)]", "for start, piece in ((origin, size),)]", "decode"),
    ("pieces handed after the name", "exact decode", "milan_soc", "exact_cpu_decode", _HANDED,
     "VexiiRiscv.generate_netlist_name()\n        VexiiRiscv.memory_regions = "
     "ctrl_memory.cpu_regions(VexiiRiscv.memory_regions)\n        named.append(VexiiRiscv.memory_regions)", "decode"),
    ("naming guard off", "decode guard", "milan_soc", "exact_cpu_decode", "if not named:", "if False:", "decode"),
    ("decode hookup removed", "exact decode", "milan_soc", "add_ctrl_memory", "exact_cpu_decode(soc.cpu)", "None",
     "soc"),
)


def check(problems: list[str], ok: bool, what: str) -> None:
    """Record one graded fact, as test_ctrl_memory.check does."""
    print(f"  [{'ok  ' if ok else 'FAIL'}] {what}")
    if not ok:
        problems.append(what)


def fewest(origin: int, size: int) -> int:
    """The fewest aligned power-of-two pieces [origin, origin + size) splits into, by searching every split."""
    best = [0] + [size + 1] * size          # best[n]: the fewest for the first n units
    for at in range(size):
        piece = 1
        while at + piece <= size:
            if (origin + at) % piece == 0:
                best[at + piece] = min(best[at + piece], best[at] + 1)
            piece *= 2
    return best[size]


def exact(origin: int, size: int, pieces: tuple[tuple[int, int], ...]) -> str | None:
    """Why `pieces` is not [origin, origin + size) as aligned power-of-two pieces, in order; None when it is."""
    at = origin
    for start, piece in pieces:
        if start != at or piece <= 0 or piece & (piece - 1) or start % piece:
            return f"(0x{start:x}, 0x{piece:x}) is not an aligned power of two at 0x{at:x}"
        at += piece
    return None if at == origin + size else f"the pieces end at 0x{at:x}, the region at 0x{origin + size:x}"


def standin(names: bool) -> Any:
    """A VexiiRiscv that finalizes as LiteX's does: collect the split SoC's rows, then name the netlist from
    them through its own naming step, or, when `names` is false, never name it."""
    from litex.soc.cores.cpu.vexiiriscv import VexiiRiscv

    class StandIn(VexiiRiscv):
        """No LiteX construction: only the finalize that the decode hookup wraps."""

        def __init__(self) -> None:
            """Skip LiteX's construction: nothing the hookup wraps reads a platform."""

        def do_finalize(self) -> None:
            """LiteX's order: the region list, then the naming step."""
            VexiiRiscv.memory_regions = list(SPLIT_ROWS)
            if names:
                self.generate_netlist_name()
    return StandIn()


def finalized(cpu: Any) -> tuple[list[list[tuple]], str | None]:
    """The lists the class's naming step saw while `cpu` finalized after the hookup, and any refusal."""
    from litex.soc.cores.cpu.vexiiriscv import VexiiRiscv
    seen: list[list[tuple]] = []
    with patch.object(VexiiRiscv, "generate_netlist_name", staticmethod(
            lambda: seen.append(list(VexiiRiscv.memory_regions)))), \
            patch.object(VexiiRiscv, "memory_regions", [], create=True):
        milan_soc.exact_cpu_decode(cpu)
        try:
            cpu.do_finalize()
        except RuntimeError as exc:
            return seen, str(exc)
    return seen, None


def arms(problems: list[str]) -> None:
    """decode_pieces, cpu_regions and the hookup that hands the split CPU's generator the pieces."""
    got = {r.name: ctrl_memory.decode_pieces(r.origin, r.size) for r in (ctrl_memory.ROM, ctrl_memory.RAM)}
    check(problems, got == PIECES, f"decode_pieces gives rom and sram as 128, 64 and 32 KiB at their origins ({got})")
    wrong = []
    for origin in range(SWEEP):
        for size in range(1, SWEEP + 1):
            pieces = ctrl_memory.decode_pieces(origin, size)
            why = exact(origin, size, pieces) or (None if len(pieces) == fewest(origin, size) else
                                                  f"{len(pieces)} pieces, {fewest(origin, size)} suffice")
            if why:
                wrong.append(f"[{origin}, {origin + size}): {why}")
    check(problems, not wrong, f"decode_pieces gives every region of up to {SWEEP} units at every origin below "
                               f"{SWEEP} as aligned power-of-two pieces, exactly the region and as few as any split "
                               f"({len(wrong)} wrong; first: {wrong[:1]})")
    rows = ctrl_memory.cpu_regions(list(SPLIT_ROWS))
    check(problems, rows == SPLIT_PIECES,
          f"cpu_regions hands the split SoC's list over as rom's and sram's pieces, each in its row's mode and on "
          f"its bus, and every aligned power-of-two row as itself ({rows})")
    seen, refusal = finalized(standin(names=True))
    check(problems, seen == [SPLIT_PIECES] and refusal is None,
          f"exact_cpu_decode hands the CPU's naming step the pieces, before it names the netlist ({seen}, {refusal})")
    seen, refusal = finalized(standin(names=False))
    check(problems, seen == [] and refusal is not None and "#791" in refusal,
          f"exact_cpu_decode refuses a CPU whose finalize never names its netlist ({refusal})")
    other = types.SimpleNamespace()
    milan_soc.exact_cpu_decode(other)
    check(problems, vars(other) == {},
          f"exact_cpu_decode leaves a CPU that is not a VexiiRiscv as it is ({vars(other)})")


def generator_rows() -> list[list[object]]:
    """The region list the last finalized VexiiRiscv handed its generator, in a milan_soc.main() child."""
    from litex.soc.cores.cpu.vexiiriscv import VexiiRiscv
    return [list(r) for r in getattr(VexiiRiscv, "memory_regions", [])]


def export_check(problems: list[str], result: dict[str, Any]) -> None:
    """The split export hands the generator rom and sram as their pieces, and only aligned powers of two."""
    rows = [tuple(r) for r in result.get("cpu_regions", [])]
    want = {r.name: [(o, s, mode, "p") for o, s in ctrl_memory.decode_pieces(r.origin, r.size)]
            for r, mode in ((ctrl_memory.ROM, "rxc"), (ctrl_memory.RAM, "rwxc"))}
    got = {r.name: [row for row in rows if r.holds(row[0], row[0] + row[1])]
           for r in (ctrl_memory.ROM, ctrl_memory.RAM)}
    check(problems, got == want and all(s & (s - 1) == 0 and o % s == 0 for o, s, *_ in rows),
          f"the split export hands the CPU generator rom and sram as their decode pieces, and every row it hands "
          f"it is an aligned power of two (#791) ({rows})")
