#!/usr/bin/env python3
"""Run a slice of the clone's gmstep_mutants.py --all inventory, unmodified.

Usage: gmstep_chunk.py CLONE (clean | FIRST LAST)
  clean       grade both unmutated legs (gmstep, option-off) as positive controls
  FIRST LAST  plant CONTROLS[FIRST..LAST] inclusive through the clone's own
              run_control(), exactly as `gmstep_mutants.py --all` does

The slice exists only so each foreground call stays under a host time limit.
Exit 0 only when every graded item passed (clean) or was caught (controls).
"""
import sys
import tempfile
from pathlib import Path


def main() -> int:
    clone = Path(sys.argv[1]).resolve()
    here = clone / "tb/verilator/milan_dp"
    sys.path.insert(0, str(here))
    import gmstep_mutants as gm  # noqa: E402  (the clone's own driver)

    fails = passes = 0
    with tempfile.TemporaryDirectory(prefix="gmstep-chunk-",
                                     dir=str(Path(__file__).resolve().parent / "scratch")) as td:
        work = Path(td)
        if sys.argv[2] == "clean":
            for key, leg in gm.LEGS.items():
                exe = leg.clean_mdir / leg.exe_name
                if not gm.is_fresh(leg, exe):
                    print(f"[INFO] {key}: clean leg rebuilt in scratch")
                    exe = gm.build(leg, {}, work / f"obj_clean_{leg.target}")
                answer = gm.verdict(*gm.run_leg(leg, exe), None) if exe else "did not compile"
                ok = answer == "pass"
                print(f"[{'PASS' if ok else 'FAIL'}] unmutated {key} leg: {answer}")
                passes, fails = passes + ok, fails + (not ok)
        else:
            first, last = int(sys.argv[2]), int(sys.argv[3])
            for tag in range(first, last + 1):
                control = gm.CONTROLS[tag]
                print(f"[INFO] control {tag}: {control.name} (leg {control.leg})")
                if gm.run_control(control, work, tag):
                    passes += 1
                else:
                    fails += 1
    print(f"\nchunk {sys.argv[2:]}: {passes + fails} items: {passes} PASS, {fails} FAIL"
          f" (inventory size {len(gm.CONTROLS)})")
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main())
