#!/usr/bin/env python3
"""Reviewer probe (R500-4): a slot whose three boot reads all differ (XOR 8,
16, 32 at its first header byte) at 1x1 and 8x8, slot A and slot B. Prints
the faulted boot's summary after a change and 10 s of service plus a console
commit: HELD must be reported (phase, unread bit), AECP released, the loop
still stepping, nothing erased or programmed, the console refused.
Usage: probe_held_report.py <clone> <workdir>"""
import sys
from pathlib import Path

clone, work = Path(sys.argv[1]).resolve(), Path(sys.argv[2]).resolve()
sys.path.insert(0, str(clone / "sw/firmware/ctrl_nvm/test"))
import nvm_bench as nb                       # noqa: E402
import nvm_checks_write as w                 # noqa: E402
import test_ctrl_nvm as t                    # noqa: E402

KEYS = ("phase", "unread", "terminal", "releases", "read_faults", "dirty", "stale", "erases",
        "programs", "commit_refused", "ok", "steps", "vd_a", "vd_b")
rc = 0
for stem in ("endstation_ax7101_1x1_tdm8", "endstation_ax7101_8x8"):
    b = t.bench_for(nb.shape_inputs(clone / "configs" / f"{stem}.yaml", work / stem), work / stem)
    rid, new = w._one_change(b, 32)
    for x in (0, 1):
        f: list[str] = []
        img = b.assemble(b.frames, 5)
        at = f"{(w.SLOT_A, w.SLOT_B)[x]:#x}"
        r = w.go(b, "", f, "--slot-a" if x == 0 else "--slot-b", b.file("x.bin", img),
                 "--boot-fault", f"read-vary-at:3:0:{at}", "--boot", "--set", f"{rid}:{new.hex()}",
                 "--run-ms", "10000", "--commit-try", "--run-ms", "1000")
        s = r.s
        good = (s["phase"] == w.P_HELD and s["unread"] == 1 << x and s["releases"] >= 1
                and s["erases"] == 0 and s["programs"] == 0 and s["commit_refused"] == 1
                and s["dirty"] == 1 and s["read_faults"] == 2 and not f)
        rc |= 0 if good else 1
        print(f"{stem} slot {'AB'[x]}: {'OK' if good else 'BAD'} "
              + " ".join(f"{k}={s.get(k)}" for k in KEYS) + (f" findings={f}" if f else ""))
sys.exit(rc)
