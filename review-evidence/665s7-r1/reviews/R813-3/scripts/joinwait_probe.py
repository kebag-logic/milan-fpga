#!/usr/bin/env python3
"""joinwait_probe.py - does the [TIME] check refuse an lwSRP that transmits while its Join timer runs?

Usage: python3 -I joinwait_probe.py CLONE WORK OLD_GRADE [SCENARIO:MS ...]

CLONE      the reviewed checkout (its tb/verilator/milan_dp is the bench under test)
WORK       an empty scratch directory for the builds and captures
OLD_GRADE  a copy of srptx_grade.py from another head, laid out so its parents[2] has sw/
SCENARIO:MS  scenarios to run (ms 0 = the scenario's own length)

Arms (PROBE_ARMS=a,b selects): the clean tracked sources and two mutants of lwSRP mrp_mad.c.
join_wait_ignored drops join_wait from mrp_transmit's hold, so every request is answered at the next
poll while the Join timer runs. leaveall_skips_join_wait lets only a pending LeaveAll skip that hold.
On a point-to-point port either may be a requested transmit opportunity (docs/reference/FR_NFR.md
3.4.1, Milan v1.2 4.2.7.1.1), limited by the rate rule. Each capture is graded by
the CLONE's srptx_grade.py and by OLD_GRADE; every [TIME] finding is printed with a count. The
bench's own per-frame record (after_join, idle_us) is summarised so the attribution of each frame is
visible. Nothing in CLONE is edited: the planted copy lives in WORK and reaches the build through the
bench's own twin_fw.py --replace recipe (srptx_mutants.build).
"""
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

ANCHOR = "    if (!ps->prepared_pdu && (!ps->tx_pending || ps->join_wait)) {"
PLANT = "    if (!ps->prepared_pdu && !ps->tx_pending) {"
#: the narrower arm: only a LeaveAll skips the Join timer's hold (sent at the next poll while it runs)
PLANT_LA = "    if (!ps->prepared_pdu && (!ps->tx_pending || (ps->join_wait && ps->la != MRP_LA_STATE_ACTIVE))) {"


def main() -> int:
    clone, work, old_grade = Path(sys.argv[1]).resolve(), Path(sys.argv[2]).resolve(), Path(sys.argv[3]).resolve()
    scenarios = [(s.split(":")[0], int(s.split(":")[1])) for s in sys.argv[4:]] or [("wire", 16000)]
    here = clone / "tb/verilator/milan_dp"
    sys.path.insert(0, str(here))
    import srptx_mutants as m  # noqa: E402  (the bench's own build and run recipe)

    mrp = clone / "third_party/lwSRP/src/core/mrp_mad.c"
    text = mrp.read_text()
    assert text.count(ANCHOR) == 1, "anchor not found once"
    arms = {"clean": None, "join_wait_ignored": text.replace(ANCHOR, PLANT),
            "leaveall_skips_join_wait": text.replace(ANCHOR, PLANT_LA)}
    only = [a for a in __import__("os").environ.get("PROBE_ARMS", "").split(",") if a]
    if only:
        arms = {k: v for k, v in arms.items() if k in only}
    rc_all = 0
    for name, planted in arms.items():
        arm = work / name
        arm.mkdir(parents=True, exist_ok=True)
        copy = None
        if planted is not None:
            copy = arm / "mrp_mad.c"
            copy.write_text(planted)
        ok, out = m.build(arm, mrp if copy else None, copy)
        print(f"== arm {name}: build {'ok' if ok else 'FAILED'}")
        if not ok:
            print(out)
            rc_all = 1
            continue
        for scenario, ms in scenarios:
            cap = arm / f"{scenario}-{ms}.json"
            cmd = [str(arm / "sp" / "Vmilan_dp_twin_sp"), "--srptx", scenario, str(cap)]
            if ms:
                cmd += ["--ms", str(ms)]
            ran = subprocess.run(cmd, capture_output=True, text=True, cwd=here)
            print(f"-- {name} {scenario} {ms}: bench rc {ran.returncode}")
            if not cap.exists():
                print(ran.stdout[-2000:] + ran.stderr[-2000:])
                rc_all = 1
                continue
            doc = json.loads(cap.read_text())
            lib = doc.get("lib", doc.get("accepted", []))
            if isinstance(lib, list) and lib and "after_join" in lib[0]:
                kinds = {"after_join": 0, "requested(idle_us>=0)": 0, "neither": 0}
                for r in lib:
                    if r["after_join"]:
                        kinds["after_join"] += 1
                    elif r["idle_us"] >= 0:
                        kinds["requested(idle_us>=0)"] += 1
                    else:
                        kinds["neither"] += 1
                print(f"   bench records: {len(lib)} accepted MRPDUs, {kinds}")
            for label, grade in (("head grade", here / "srptx_grade.py"), ("round-2 grade", old_grade)):
                g = subprocess.run([sys.executable, "-B", str(grade), str(cap)], capture_output=True, text=True,
                                   cwd=grade.parent)
                found = [ln for ln in g.stdout.splitlines() if ln.startswith("[")]
                time = [ln for ln in found if ln.startswith("[TIME]")]
                print(f"   {label}: rc {g.returncode}, {len(found)} findings, {len(time)} [TIME]")
                for ln in found[:6]:
                    print(f"     {ln[:260]}")
    return rc_all


if __name__ == "__main__":
    sys.exit(main())
