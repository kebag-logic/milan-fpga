#!/usr/bin/env python3
"""R500-2 reviewer demonstrations for PR #669 (#665 F1): what the two
planted defects that survive the suite do, on the head and on the plant.

Run from the root of a checkout of the head under review:

    python3 /path/to/r500_2_demos.py <scratch-dir>

Read-only on the checkout; copies and builds go under <scratch-dir>.
"""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path.cwd()
sys.path.insert(0, str(ROOT / "sw/firmware/ctrl_nvm/test"))

import nvm_mutants                                       # noqa: E402
import test_ctrl_nvm as gate                             # noqa: E402
from nvm_bench import shape_inputs                       # noqa: E402
from nvm_checks import _two_slots, state_matches, rid_payloads   # noqa: E402
from nvm_mutants import Mutant                           # noqa: E402

SHAPE = ROOT / "configs/endstation_ax7101_1x1_tdm8.yaml"
STORE = nvm_mutants.STORE
FALLBACK = (STORE, "\t\tif (chosen != NVM_NONE && !nvm_stage_slot(chosen))\n\t\t\tchosen = NVM_NONE;",
            "\t\tif (chosen != NVM_NONE)\n\t\t\t(void)nvm_stage_slot(chosen);")
TAKEN = (STORE, "r.id >= nvm.cursor.id;", "r.id > nvm.cursor.id;")


def bench(inputs, work: Path, name: str, seam):
    if seam is None:
        return gate.bench_for(inputs, work / name)
    tree = work / name / "tree"
    nvm_mutants.plant(Mutant(name, (seam,), ()), tree)
    return gate.bench_for(inputs, work / name, tree)


def fallback_demo(b, label: str) -> None:
    """Slot A newer (6), B older (5). The re-stage of A (read 4) and of B
    (read 5) both return one flipped bit: no clean copy of either is read."""
    imgs = _two_slots(b, 6, 5)
    r = b.run("--slot-a", b.file("a.bin", imgs[0]), "--slot-b", b.file("b.bin", imgs[1]),
              "--boot-fault", "read-flip:2:4", "--boot", "--dump-state", "st.txt")
    bad = state_matches(b, b.work / "st.txt", rid_payloads(b, imgs[r.s["auth"]])) \
        if r.s["auth"] in (0, 1) else []
    print(f"DEMO fallback_restage [{label}]: terminal={r.s['terminal']} auth={r.s['auth']} "
          f"cause={r.s['cause']} vd_a={r.s['vd_a']} vd_b={r.s['vd_b']} applied={r.s['applied']} "
          f"state-vs-slot: {bad[0] if bad else 'matches the slot named (or none named)'}",
          flush=True)


def taken_demo(b, label: str) -> None:
    """A change to the record the running capture examines NEXT (the first
    record, before any capture step), then a commit, then 5 s, then a
    second change: DR2a wants its erase 1,000 to 1,050 ms after it."""
    g = b.file("g.bin", b.assemble(b.frames, 5))
    first = min(b.frames)
    plen = len(b.frames[first]) - 8
    v1 = bytes((first * 13 + j * 11 + 91) & 0xFF for j in range(plen)).hex()
    v2 = bytes((first * 13 + j * 11 + 92) & 0xFF for j in range(plen)).hex()
    r = b.run("--slot-b", g, "--boot", "--set-pattern", "1", "--until-phase", "2",
              "--set", f"{first}:{v1}", "--until-idle", "--run-ms", "5000", "--mark",
              "--set", f"{first}:{v2}", "--until-idle")
    after = r.erases[1] - r.marks[-1] if len(r.erases) > 1 and r.marks else None
    print(f"DEMO dr2a_boundary [{label}]: ok={r.s['ok']} second erase {after} us after the "
          f"second change (DR2a wants 1,000,000 to 1,050,000)", flush=True)


def main() -> int:
    work = Path(sys.argv[1]).resolve()
    work.mkdir(parents=True, exist_ok=True)
    inputs = shape_inputs(SHAPE, work / "inputs")
    head = bench(inputs, work, "head", None)
    fb = bench(inputs, work, "fallback_restage_unchecked", FALLBACK)
    tk = bench(inputs, work, "taken_off_by_one", TAKEN)
    fallback_demo(head, "head")
    fallback_demo(fb, "plant fallback_restage_unchecked")
    taken_demo(head, "head")
    taken_demo(tk, "plant taken_off_by_one")
    return 0


if __name__ == "__main__":
    sys.exit(main())
