#!/usr/bin/env python3
"""R394-4: run a subset of the committed mutation arm through its OWN scheduler.

Imports the suite's mutants.py unchanged, makes the ROM images with its rom_images_result(),
builds the committed unit list with arm_units(), keeps the units whose list indices are given,
and runs them with the committed run_units() on N workers, so the verdicts, the sharing, the
datapath-first start and the fixed print order are the committed code's. `--list` prints the
committed unit list (index, datapath flag, what it grades) and exits.

  python3 r394_arm_units.py <suite-dir> --jobs N --units 0,1,5-9
  python3 r394_arm_units.py <suite-dir> --list
"""
import argparse
import importlib.util
import sys
import tempfile
import time
from pathlib import Path


def indices(spec: str) -> list[int]:
    out = []
    for part in spec.split(","):
        a, _, b = part.partition("-")
        out += list(range(int(a), int(b or a) + 1))
    return out


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("suite")
    ap.add_argument("--jobs", type=int, default=4)
    ap.add_argument("--units", default="")
    ap.add_argument("--list", action="store_true")
    a = ap.parse_args()
    suite = Path(a.suite).resolve()
    spec = importlib.util.spec_from_file_location("cc_mutants", suite / "mutants.py")
    m = importlib.util.module_from_spec(spec)
    sys.argv = [str(suite / "mutants.py")]
    spec.loader.exec_module(m)
    labels = ["build check: makeflags", "build check: planted break"]
    labels += [f"control {'+'.join(g)}" for g in m.control_groups()]
    labels += [f"mutant ({leg}) {name}" for leg, name, _, _ in m.MUTATIONS]
    with tempfile.TemporaryDirectory(prefix="r394-arm-") as td:
        work = Path(td)
        units = m.arm_units(work)
        assert len(units) == len(labels), (len(units), len(labels))
        if a.list:
            for i, (u, lab) in enumerate(zip(units, labels)):
                print(f"{i:2d} datapath={u.datapath!s:5} {lab}")
            return 0
        made, lines = m.rom_images_result(work)
        if not made:
            print("\n".join(lines))
            return 1
        pick = indices(a.units)
        print(f"[r394] units {pick} on {a.jobs} worker(s)", flush=True)
        t0 = time.monotonic()
        verdicts = m.run_units([units[i] for i in pick], a.jobs)
        print(f"[r394] {len(verdicts)} checks: {sum(verdicts)} PASS, {len(verdicts) - sum(verdicts)} FAIL; "
              f"{time.monotonic() - t0:.1f} s", flush=True)
    return 0 if all(verdicts) else 1


if __name__ == "__main__":
    sys.exit(main())
