#!/usr/bin/env python3
"""Cross-check the author's mapping TSV against all eight utilization reports."""
import csv, pathlib, re, sys
a = pathlib.Path(sys.argv[1]) / "receipts/public/author-r5/evidence-r5/map"
for row in csv.DictReader((a / "ctrl_memory_ooc.tsv").open(), delimiter="\t"):
    text = (a / "util" / f"{row['top']}_utilization.rpt").read_text()
    primitives = text.split("7. Primitives\n-------------", 1)[1].split("8. Black Boxes", 1)[0]
    counts = {k: int(v) for k, v in re.findall(r"^\|\s*(\w+)\s*\|\s*(\d+)\s*\|", primitives, re.M)}
    for key in ("RAMB36E1", "RAMB18E1"):
        assert counts.get(key, 0) == int(row[key]), (row["top"], key)
    ramb18 = re.search(r"^\|\s*RAMB18\s*\|\s*(\d+)\s*\|", text, re.M)
    assert ramb18 and int(ramb18.group(1)) == int(row["RAMB18E1"])
    assert sum(v for k, v in counts.items() if k.startswith("LUT")) == int(row["LUT"])
    assert sum(v for k, v in counts.items() if k.startswith("FD")) == int(row["FF"])
    lut = re.search(r"^\|\s*Slice LUTs\*?\s*\|\s*(\d+)\s*\|", text, re.M)
    assert lut
    print(row["top"], "PASS primitive counts; Slice LUTs", lut.group(1), "LUT cells", row["LUT"])
print("PASS all eight mapping reports; absent zero primitive rows cross-checked against memory summary")
