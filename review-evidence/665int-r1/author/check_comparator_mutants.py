#!/usr/bin/env python3
"""Plant three comparator defects in scratch copies and require each caught.

Usage: check_comparator_mutants.py ROOT WORK
Each mutant must make `--self-test` exit nonzero; the unmodified file must
exit zero. Prints one JSON report; exits 0 only when all four hold.
"""

import json
from pathlib import Path
import subprocess
import sys

SOURCE = "sw/firmware/ctrl/test/srp_wire_compare.py"
SORT = ('"events": sorted(events, key=lambda event: (event[0], event[1], event[2],\n'
        '                                                   -1 if event[3] is None else event[3], event[4])),')
ORDERED = ("return ([canonical_opportunity(frames) for frames in fabric] ==\n"
           "            [canonical_opportunity(frames) for frames in split])")
MUTANTS = {
    "dedupe": ('"events": sorted(events,', '"events": sorted(set(events),'),
    "unordered-opportunities": (ORDERED, "key = repr\n    return (sorted([canonical_opportunity(frames) for frames in fabric], key=key) ==\n"
                                "            sorted([canonical_opportunity(frames) for frames in split], key=key))"),
    "no-canonical-sort": (SORT, '"events": events,'),
}


def run(path: Path) -> subprocess.CompletedProcess:
    """Run one comparator copy's self-test in isolated mode."""
    return subprocess.run([sys.executable, "-B", "-I", str(path), "--self-test"],
                          capture_output=True, text=True, check=False)


def main() -> int:
    """Write mutants, run them, and report each outcome."""
    root, work = Path(sys.argv[1]), Path(sys.argv[2])
    work.mkdir(parents=True, exist_ok=True)
    text = (root / SOURCE).read_text()
    report = {"unmodified_rc": run(root / SOURCE).returncode, "mutants": {}}
    for name, (old, new) in MUTANTS.items():
        if text.count(old) != 1:
            report["mutants"][name] = {"error": "anchor not unique"}
            continue
        path = work / f"{name}.py"
        path.write_text(text.replace(old, new))
        result = run(path)
        last = (result.stderr.strip().splitlines() or [""])[-1]
        report["mutants"][name] = {"rc": result.returncode, "last_line": last}
    print(json.dumps(report, indent=2))
    caught = all(item.get("rc", 0) != 0 for item in report["mutants"].values())
    return 0 if report["unmodified_rc"] == 0 and caught else 1


if __name__ == "__main__":
    sys.exit(main())
