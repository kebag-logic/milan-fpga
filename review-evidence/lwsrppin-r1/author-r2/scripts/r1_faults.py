#!/usr/bin/env python3
"""Replay round 1's five planted grade faults on the current twin_mrp.py; each must fail `--selftest`.

Usage: r1_faults.py <parent-root> <scratch-dir>
Round 1 planted each fault as a whole-file copy of the grade at 402834ac; each differs from that file (and from
dbba60e6's) in exactly one code substitution, given here. Each is applied to a copy of tb/verilator/milan_dp's
Python files under <scratch-dir>/<name>/tb/verilator/x (sw symlinked, as twin_decode.py needs), and the copy's
`twin_mrp.py --selftest` must exit non-zero. The control is the unmodified copy, which must pass.
"""
import shutil
import subprocess
import sys
from pathlib import Path

FAULTS = {
    "old-rla-before-after": ("    outcomes = transmit(leave_all, config, part)\n",
                             "    outcomes = transmit(leave_all, config, part) if not leave_all else \\\n"
                             "        [(x, step(\"rLA!\", y, part)) for x, y in transmit(True, config, part)] + \\\n"
                             "        transmit(True, step(\"rLA!\", config, part), part)\n"),
    "no-txlaf": ("    if leave_all and full:\n", "    if False:\n"),
    "no-fourpacked": ('    return 2 + WIDTH[application][kind] + 1 + (1 if application == "MSRP" and kind == 3 else 0)\n',
                      "    return 2 + WIDTH[application][kind] + 1 + 0\n"),
    "room-1499": ("MRPDU_ROOM = 1500\n", "MRPDU_ROOM = 1499\n"),
    "mvrp-walk-off": ("    return offset + 2 - s.at\n", "    return offset - s.at\n"),
}


def main(root: Path, scratch: Path) -> int:
    bad = 0
    for name, (old, new) in [("control", ("", "")), *FAULTS.items()]:
        top = scratch / name
        where = top / "tb/verilator/x"
        where.mkdir(parents=True, exist_ok=True)
        if not (top / "sw").exists():
            (top / "sw").symlink_to(root / "sw")
        for py in (root / "tb/verilator/milan_dp").glob("*.py"):
            shutil.copy2(py, where / py.name)
        target = where / "twin_mrp.py"
        text = target.read_text(encoding="utf-8")
        if old:
            if text.count(old) != 1:
                print(f"{name}: SUBSTITUTION NOT UNIQUE ({text.count(old)})")
                bad += 1
                continue
            target.write_text(text.replace(old, new), encoding="utf-8")
        res = subprocess.run([sys.executable, "-B", "-E", "-s", "twin_mrp.py", "--selftest"], cwd=where,
                             capture_output=True, text=True, check=False)
        last = (res.stdout + res.stderr).strip().splitlines()[-1:] or [""]
        ok = res.returncode == 0 if name == "control" else res.returncode != 0
        verdict = ("PASS" if ok else "CONTROL FAILED") if name == "control" else ("CAUGHT" if ok else "ESCAPED")
        bad += not ok
        print(f"{name}: {verdict} rc={res.returncode}: {last[0]}")
    print(f"r1_faults: {len(FAULTS)} faults, {bad} escaped or failed")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main(Path(sys.argv[1]).resolve(), Path(sys.argv[2]).resolve()))
