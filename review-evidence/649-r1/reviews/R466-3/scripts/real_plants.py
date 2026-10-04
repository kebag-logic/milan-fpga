#!/usr/bin/env python3
"""Reviewer probe for #649 (R466-3): plant figure-preserving wrong figures into a copy of the published REAL route
inputs (report rows moved between sibling leaves so every ancestor still sums, census cells re-owned) and require
`resmap_map.py map` to refuse each (exit 1) under the expected tie. Usage: real_plants.py <tree> <inputs/map dir with
map_cells.tsv> <scratch> <out json>"""
import json, re, shutil, subprocess, sys
from pathlib import Path

tree, src, scratch, out = Path(sys.argv[1]), Path(sys.argv[2]), Path(sys.argv[3]), Path(sys.argv[4])

def row_edit(text, name, column, delta):
    """Add delta to one numeric column (0 = Total LUTs .. 7 = DSP) of the one report table row named `name`."""
    lines = text.splitlines(keepends=True)
    hits = [i for i, l in enumerate(lines) if l.count("|") == 11 and l.split("|")[1].strip() == name]
    assert len(hits) == 1, (name, len(hits))
    cells = lines[hits[0]].split("|")
    old = cells[3 + column]
    new = str(int(old) + delta)
    cells[3 + column] = new.rjust(len(old) - 1) + " "
    lines[hits[0]] = "|".join(cells)
    return "".join(lines)


def plant(name, edits, census_edit=None, flat_edit=None):
    d = scratch / name
    if d.exists():
        shutil.rmtree(d)
    shutil.copytree(src, d)
    rpt = d / "map_hierarchy.rpt"
    text = rpt.read_text()
    for row, column, delta in edits:
        text = row_edit(text, row, column, delta)
    rpt.write_text(text)
    if census_edit:
        c = d / "map_cells.tsv"
        t = c.read_text()
        old, new = census_edit
        assert t.count(old) == 1, (name, t.count(old))
        c.write_text(t.replace(old, new))
    if flat_edit:
        f = d / "map_utilization.rpt"
        t = f.read_text(); old, new = flat_edit
        assert t.count(old) == 1
        f.write_text(t.replace(old, new))
    r = subprocess.run([sys.executable, "syn/resmap/resmap_map.py", "map", str(d)], cwd=tree, capture_output=True,
                       text=True)
    shutil.rmtree(d)
    return {"plant": name, "rc": r.returncode, "first_lines": r.stdout.splitlines()[:3]}

# A census cell of csr (an unrecorded scope) holding a flip-flop, re-owned to chan_map_capture.
census = (src / "map_cells.tsv").read_text()
ff = next(l for l in census.splitlines() if l.startswith("milan_datapath/csr/") and "\tFDRE\t" in l)
lut = next(l for l in census.splitlines() if l.startswith("milan_datapath/csr/") and re.search(r"\tLUT6\tLEAF\t", l))
results = [
    plant("clean-control", []),
    # LUT moved between two sibling leaves outside the 51 recorded scopes: ancestry and record still hold.
    plant("lut-moved-csr-to-chanmap", [("csr", 0, -1), ("csr", 1, -1), ("chan_map_capture", 0, 1),
                                       ("chan_map_capture", 1, 1)]),
    # FF moved between two sibling leaves outside the recorded scopes.
    plant("ff-moved-crf-rx-to-talker-diag", [("crf_rx", 4, -1), ("talker_diag", 4, 1)]),
    # The census re-owns one csr flip-flop to chan_map_capture; the report is untouched.
    plant("census-ff-reowned", [], census_edit=(ff, ff.replace("milan_datapath/csr/", "milan_datapath/chan_map_capture/", 1))),
    # The census re-owns one csr LUT to chan_map_capture.
    plant("census-lut-reowned", [], census_edit=(lut, lut.replace("milan_datapath/csr/", "milan_datapath/chan_map_capture/", 1))),
    # A sharing adjustment made one deeper: the datapath and the image each one LUT smaller, all ancestry still legal.
    plant("sharing-adjustment-deepened", [("milan_datapath", 0, -1), ("milan_datapath", 1, -1), ("alinx_ax7101", 0, -1),
                                          ("alinx_ax7101", 1, -1)], flat_edit=("| Slice LUTs                 | 50767 |",
                                                                              "| Slice LUTs                 | 50766 |")),
    # The flat report's slice count planted.
    plant("flat-slices", [], flat_edit=("| Slice                                      | 15832 |",
                                        "| Slice                                      | 15833 |")),
]
out.write_text(json.dumps(results, indent=1) + "\n")
for r in results:
    print(r["rc"], r["plant"], "|", " / ".join(r["first_lines"])[:220])
