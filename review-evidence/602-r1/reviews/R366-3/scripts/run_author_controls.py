#!/usr/bin/env python3
"""R366-3: run selected controls of the head's own gmstep_mutants.py inventory
through its own run_control() (anchor count, named check, stays_clean rule),
one at a time, against the scratch clone of the exact head.

Usage: run_author_controls.py VERILATOR_WRAPPER
Environment: VERILATOR and VERILATOR_JOBS=8 are exported for the suite recipe.
"""
import os
import sys
import tempfile
from pathlib import Path

PKT = Path(__file__).resolve().parent.parent
SUITE = PKT / "scratch" / "tree" / "tb/verilator/milan_dp"

WANTED = (
    "PHC adjtime becomes an mr cause 16 cycles later",
    "PHC adjtime becomes an mr cause 256 cycles later",
    "a PHC step suppresses a coincident CRF restart",
)


def main() -> int:
    os.environ["VERILATOR"] = sys.argv[1]
    os.environ["VERILATOR_JOBS"] = "8"
    sys.path.insert(0, str(SUITE))
    import gmstep_mutants as gm  # noqa: E402  (the head's own runner)

    option_off = [c for c in gm.CONTROLS if c.leg == "option-off"]
    selected = option_off + [c for c in gm.CONTROLS if c.name in WANTED and c not in option_off]
    print(f"inventory: {len(gm.CONTROLS)} controls, "
          f"{sum(c.leg == 'gmstep' for c in gm.CONTROLS)} gmstep, {len(option_off)} option-off, "
          f"{sum(c.acceptance for c in gm.CONTROLS)} acceptance")
    caught = 0
    with tempfile.TemporaryDirectory(prefix="r366-3-", dir=PKT / "scratch") as td:
        for tag, control in enumerate(selected):
            print(f"--- {control.name} (leg {control.leg}, stays_clean {list(control.stays_clean)})",
                  flush=True)
            ok = gm.run_control(control, Path(td), tag)
            caught += ok
            sys.stdout.flush()
    print(f"\n{caught}/{len(selected)} selected controls caught by the head's runner")
    return 0 if caught == len(selected) else 1


if __name__ == "__main__":
    sys.exit(main())
