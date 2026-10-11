#!/usr/bin/env python3
"""Round 3 scratch probe: run check 13's writer-restart cases one by one on a
shape and print, per case, whether the restart held, its read count and its
findings; with --plant LABEL, on a copy of the firmware carrying that #671
control. Usage: restart_cases.py ROOT WORK SHAPE [--plant LABEL]"""
from __future__ import annotations

import argparse
import sys
from dataclasses import replace
from pathlib import Path


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("root")
    ap.add_argument("work")
    ap.add_argument("shape")
    ap.add_argument("--plant", default="")
    a = ap.parse_args()
    root = Path(a.root).resolve()
    sys.path.insert(0, str(root / "sw/firmware/nvm_hosttest"))
    import test_nvm_firmware as t
    import read_fault_cases as rfc

    text = t.FIRMWARE.read_text()
    if a.plant:
        for old, new in rfc.READ_FAULT_MUTATIONS[a.plant][0]:
            assert text.count(old) == 1, a.plant
            text = text.replace(old, new)
    work = Path(a.work).resolve()
    work.mkdir(parents=True, exist_ok=True)
    bench = replace(t.make_bench(root / "configs" / f"{a.shape}.yaml", work / "bench", text), jobs=1)
    fr = t.fault_run(bench)
    body = t.KLJ2_HDR + (bench.img_len - t.KLJ2_HDR - t.KLJ2_TRAILER) // 2
    cases = [c for c in rfc.fault_cases(body) if c.restart]
    total = 0
    for n, case in enumerate(cases):
        w = work / f"c{n}"
        w.mkdir(exist_ok=True)
        got = t.grade_fault_case(bench, fr, case, w)
        _, s, _ = t.run(bench, "--slot-a", str(w / "rf_a.bin"), "--slot-b", str(w / "rf_b.bin"), "--boot",
                        "--idle-ms", "100", *case.fault, "--restart", "--change",
                        f"{fr.off}:{fr.changes[0].hex()}", "--idle-ms", "3000")
        total += len(got)
        print(f"{case.name}: restart_reads={s.get('restart_reads')} acks={s.get('acks')} "
              f"backed={s.get('backed')} stale={s.get('stale')} dirty={s.get('dirty')} "
              f"findings={len(got)}" + (f"; first: {got[0]}" if got else ""), flush=True)
    print(f"{len(cases)} restart case(s), {total} finding(s)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
