#!/usr/bin/env python3
"""Recompute fixed-contract gaps directly from captured MAC notification times."""
import json
from pathlib import Path

p = Path(__file__).resolve().parent
summary = []
for shape, name in [(1, "makeflags-1-run.log"), (8, "frames-only-8-run.log")]:
    rows = {}
    for line in (p / name).read_text().splitlines():
        if not line.startswith("NOTE,"):
            continue
        _, ty, ix, recipient, cycle = line.split(",")
        rows.setdefault((int(ty), int(ix), int(recipient)), []).append(int(cycle))
    expected = {(ty, ix, recipient) for ty in (5, 6) for ix in range(shape + 1)
                for recipient in (0, 1)}
    assert set(rows) == expected
    gaps = []
    tails = []
    descriptive = []
    for key, times in sorted(rows.items()):
        assert len(times) >= 2 and times == sorted(times)
        assert all(0 <= t < 5000000 for t in times)
        values = [b - a for a, b in zip(times, times[1:])]
        tail = 5000000 - times[-1]
        assert all(1000000 <= gap <= 1025000 for gap in values)
        assert tail <= 1025000
        gaps.extend(values)
        tails.append(tail)
        bins = [sum(second * 1000000 <= t < (second + 1) * 1000000 for t in times)
                for second in range(5)]
        descriptive.append({"type": key[0], "index": key[1], "recipient": key[2],
                            "bins": bins})
    old_cells = [row["bins"][second] for row in descriptive for second in (2, 3, 4)]
    record = {"shape": shape, "source": name, "rows": len(rows), "graded_gaps": len(gaps),
              "min_ms": min(gaps) / 1000, "max_ms": max(gaps) / 1000,
              "max_tail_ms": max(tails) / 1000, "fixed_bound_ms": 1025,
              "old_three_bin_cell_count": len(old_cells),
              "old_three_bin_cells_all_one": all(c == 1 for c in old_cells),
              "descriptive_bins_not_graded": descriptive}
    summary.append(record)
(p / "independent-notification-audit.json").write_text(json.dumps(summary, indent=2) + "\n")
for row in summary:
    print({k: v for k, v in row.items() if k != "descriptive_bins_not_graded"})
