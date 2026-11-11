#!/usr/bin/env python3
"""gate_probe.py - reviewer probe for PR #874 at its head: does the head's attribution leave a frame that
lwSRP sent with its Join timer running ungraded, and does any check still refuse it?

Uses the tracked mutant driver's own build and run helpers (srptx_mutants.build/run), so the planted line
is compiled through the same recipe (twin_fw.py --replace), into a work directory outside the tree.

  python3 -B gate_probe.py <checkout>/tb/verilator/milan_dp WORK ARM [SCENARIO MS]

ARM is one of: clean, join-gate-off.  Prints the findings, the per-frame classification (after_join,
idle_us, neither) and the binary rc; exit 0 when it ran (the verdict is read from the output).
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

ARMS = {
    # lwSRP stops holding transmits behind its Join timer; the timer still runs (mrp_mad.c, mrp_transmit)
    "join-gate-off": ("    ps->join_wait = ps->join_cs;", "    ps->join_wait = 0;"),
}


def main() -> int:
    here, work, arm = Path(sys.argv[1]).resolve(), Path(sys.argv[2]).resolve(), sys.argv[3]
    scenario = sys.argv[4] if len(sys.argv) > 4 else "wire"
    ms = int(sys.argv[5]) if len(sys.argv) > 5 else 3000
    sys.path.insert(0, str(here))
    import srptx_mutants as m  # noqa: E402
    work.mkdir(parents=True, exist_ok=True)
    if arm == "clean":
        ok, out = m.build(work, None, None)
    else:
        old, new = ARMS[arm]
        text = m.MRP.read_text()
        assert text.count(old) == 1, "anchor not unique"
        copy = work / m.MRP.name
        copy.write_text(text.replace(old, new))
        ok, out = m.build(work, m.MRP, copy)
    print(f"build {arm}: {'ok' if ok else 'FAILED'}")
    if not ok:
        print(out)
        return 1
    rc, found, out = m.run(work, scenario, ms)
    print(f"run {arm} {scenario} {ms} ms: binary rc {rc}; findings {len(found)}")
    for f in found[:12]:
        print("   ", f[:300])
    cap = work / f"{scenario}-{ms}.json"
    if cap.exists():
        doc = json.loads(cap.read_text())
        lib = [r for r in doc["lib"] if r["rc"] == 0]
        for proto in ("MSRP", "MVRP"):
            rs = [r for r in lib if r["proto"] == proto] if "proto" in lib[0] else []
            aj = sum(1 for r in rs if r["after_join"])
            idle = sum(1 for r in rs if not r["after_join"] and r["idle_us"] >= 0)
            print(f"   {proto}: records {len(rs)}, after_join {aj}, requested {idle}, neither {len(rs) - aj - idle}")
        print("   record keys:", sorted(lib[0].keys()) if lib else None)
    return 0


if __name__ == "__main__":
    sys.exit(main())
