#!/usr/bin/env python3
"""Retain raw focused runtime logs and independently check their result groups."""
import collections
import json
import pathlib
import re
import shutil
import sys

packet = pathlib.Path(sys.argv[1])
summary = {}
groups = {"tx-interval": "TX", "rx-interval": "RX", "tx-reset": "TX_RESET",
          "aaf-reset": "RX_RESET", "crf-reset": "RX_RESET", "rx-saturation": "RX",
          "late": "CADENCE", "rate": "RATE", "tx-nodirty": "OUTPUT_CADENCE", "fixed-grid": "PHASE"}
for label in ("clean-1", "clean-8", "pending-wrap", *groups,
              "f5-1-clean", "f5-8-clean", "f5-1-fixed-grid", "f5-1-late", "f5-1-rate"):
    work = packet / "scratch" / label
    record = {}
    for kind in ("run", "escape"):
        source = work / (kind + ".log")
        if not source.exists():
            assert kind == "escape" and label in ("clean-1", "clean-8", "pending-wrap", "f5-1-clean", "f5-8-clean")
            continue
        destination = packet / "receipts" / (label + "." + kind + ".log")
        shutil.copyfile(source, destination)
        text = source.read_text()
        failures = [line for line in text.splitlines() if "[FAIL]" in line]
        if label in groups and kind == "run":
            assert failures and all("[726 " + groups[label] + "]" in line for line in failures)
            assert "RESULT: FAIL" in text
        elif label.startswith("f5-1-") and label != "f5-1-clean" and kind == "run":
            assert "[  FAILED  ]" in text
        else:
            assert not failures and ("RESULT: PASS" in text or "[  PASSED  ]" in text)
        record[kind] = {"receipt": str(destination.relative_to(packet)), "failures": len(failures),
                        "named_groups": sorted(set(re.findall(r"\[726 ([A-Z_]+)\]", "\n".join(failures))))}
    summary[label] = record

for shape in (1, 8):
    text = (packet / "receipts" / f"clean-{shape}.run.log").read_text()
    notes = collections.defaultdict(list)
    gaps = {}
    for line in text.splitlines():
        fields = line.split(",")
        if fields[0] == "NOTE":
            notes[tuple(map(int, fields[1:4]))].append(int(fields[4]))
        if fields[0] == "GAPS":
            gaps[tuple(map(int, fields[2:5]))] = list(map(float, fields[6:]))
    assert len(notes) == 4 * (shape + 1) == len(gaps)
    all_gaps = []
    for key, times in notes.items():
        differences = [(b - a) / 1000 for a, b in zip(times, times[1:])]
        count, low, high, tail, service = gaps[key]
        assert len(times) == count and min(differences) == low and max(differences) == high
        assert low >= 1000 and high <= 1000 + service and tail <= 1000 + service
        all_gaps += differences
    summary[f"clean-{shape}"]["independent_gap_audit"] = {
        "rows": len(notes), "gaps": len(all_gaps), "min_ms": min(all_gaps),
        "max_ms": max(all_gaps), "maximum_measured_service_ms": max(g[4] for g in gaps.values())}

public = packet / "receipts/public/author-r4/review-round4"
for shape, expected in ((1, 12), (8, 54)):
    text = (public / f"earlier-scratch__standing-before-{shape}__run.log").read_text()
    failures = [line for line in text.splitlines() if "[FAIL]" in line]
    assert len(failures) == expected
    found = set(re.findall(r"\[726 ([A-Z_]+)\]", "\n".join(failures)))
    assert found == {"TX", "RX", "CADENCE"}
    summary[f"public-baseline-{shape}"] = {"failures": len(failures), "groups": sorted(found)}

(packet / "receipts/local-runtime-audit.json").write_text(json.dumps(summary, indent=2) + "\n")
print(json.dumps(summary, indent=2))
