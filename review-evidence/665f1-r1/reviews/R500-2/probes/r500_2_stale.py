#!/usr/bin/env python3
"""R500-2: the store's `stale` after a failed attempt whose retry commits
while a same-value change call is outstanding, and that change is then
suppressed by DR2b. FASTCONNECT section 9.2: nvm_stale clears when backed is
true again AND nothing is dirty. Run from the head's checkout root, on both
ports:

    python3 /path/to/r500_2_stale.py <scratch-dir>
"""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path.cwd()
sys.path.insert(0, str(ROOT / "sw/firmware/ctrl_nvm/test"))

import test_ctrl_nvm as gate                             # noqa: E402
from nvm_bench import shape_inputs                       # noqa: E402

KEYS = ("ok", "failed", "skipped", "stale", "dirty", "pending", "phase", "exhausted")


def main() -> int:
    work = Path(sys.argv[1]).resolve()
    inputs = shape_inputs(ROOT / "configs/endstation_ax7101_1x1_tdm8.yaml", work / "inputs")
    b = gate.bench_for(inputs, work / "head")
    g = b.file("g.bin", b.assemble(b.frames, 5))
    rid = max(b.frames)
    plen = len(b.frames[rid]) - 8
    new = bytes((rid * 13 + j * 11 + 77) & 0xFF for j in range(plen)).hex()
    # attempt 1 fails at its read-back; the retry's capture runs; once it is
    # sealing, the same value is reported changed again (a repeated SET)
    base = ["--slot-b", g, "--boot", "--fault", "program-drop:1", "--set", f"{rid}:{new}",
            "--until-phase", "8", "--run-ms", "500", "--until-phase", "3"]
    for port in ((), ("--litespi",)):
        for label, tail in (("control: no repeated change", ["--until-idle", "--run-ms", "3000"]),
                            ("same value reported again during the retry",
                             ["--touch", str(rid), "--until-idle", "--run-ms", "3000"])):
            r = b.run(*port, *base, *tail)
            print(f"STALE {'litespi' if port else 'model'} [{label}]: "
                  + " ".join(f"{k}={r.s[k]}" for k in KEYS), flush=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
