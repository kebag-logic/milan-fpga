#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""Grade all 128 quiet distributions before selecting a settle arm band.

ROOT contains slow/fast crossed with none/uniform5/tail24/uniform60, named
slow-none, etc. Each directory contains the sixteen sweep.py B8 phase logs.
All four stimulus-selected windows in every log are included, with no
error-based exclusion. Missing phases, failed runs and incomplete histograms
fail, even if the available extrema would fit the proposed band.
"""

import argparse
from collections import Counter
import json
from pathlib import Path
import re

WINDOWS = {"INTERNAL before switch", "AAF after settle",
           "[SW] AAF to CRF:", "[SW] CRF to AAF:"}
LINE = re.compile(r"^ERROR-DISTRIBUTION: (.+) window ([\d.]+) ([\d.]+) "
                  r"samples (\d+) axis_hz (\d+) histogram(.*)$", re.M)


def grade(root: Path, band: int) -> dict:
    """Return the complete signed histograms and the independent band check."""
    groups = {}
    for sign in ("slow", "fast"):
        for envelope in ("none", "uniform5", "tail24", "uniform60"):
            name = f"{sign}-{envelope}"
            files = sorted((root / name).glob("b8_*_p*.log"))
            assert [int(p.stem.rsplit("_p", 1)[1]) for p in files] == list(range(16)), name
            hist = Counter()
            total = 0
            for path in files:
                status = path.with_suffix(".rc")
                if not status.exists():
                    status = path.parent / "driver.rc"
                assert status.read_text().strip() == "0", str(status)
                text = path.read_text()
                assert "RESULT: PASS" in text and "[FAIL]" not in text, str(path)
                phase = re.search(r"^RESULT-645: phase ([\d.]+)", text, re.M)
                expected = int(path.stem.rsplit("_p", 1)[1]) / 16
                assert phase and float(phase[1]) == expected, str(path)
                rows = LINE.findall(text)
                assert len(rows) == 4 and {r[0] for r in rows} == WINDOWS, str(path)
                for _, begin, end, samples, axis, bins in rows:
                    assert float(end) > float(begin) and int(axis) == 6250000, str(path)
                    pairs = [tuple(map(int, item.split(":"))) for item in bins.split()]
                    assert pairs and len({err for err, _ in pairs}) == len(pairs), str(path)
                    assert all(count > 0 for _, count in pairs), str(path)
                    assert sum(count for _, count in pairs) == int(samples), str(path)
                    hist.update(dict(pairs))
                    total += int(samples)
            groups[name] = {"phases": len(files), "samples": total,
                            "min": min(hist), "max": max(hist), "histogram": dict(sorted(hist.items()))}
    excursion = max(max(abs(g["min"]), abs(g["max"])) for g in groups.values())
    assert band >= 2 * excursion, f"band {band} < twice quiet excursion {excursion}"
    assert band < 9, f"band {band} would miss the +9-cycle fine pull"
    return {"axis_hz": 6250000, "phases": 128, "windows": 512, "groups": groups,
            "quiet_excursion": excursion, "band_axis_cycles": band, "result": "PASS"}


def main() -> int:
    """Write a compact, reproducible receipt only after all checks pass."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("root", type=Path)
    parser.add_argument("--band", type=int, required=True)
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args()
    receipt = grade(args.root, args.band)
    args.out.write_text(json.dumps(receipt, indent=2) + "\n")
    print(f"quiet distributions: {receipt['phases']} phases, {receipt['windows']} windows, "
          f"peak {receipt['quiet_excursion']} axis cycles; band {args.band}: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
