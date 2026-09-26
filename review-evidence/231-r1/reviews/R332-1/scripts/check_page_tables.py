"""Cross-check the baseline page's hierarchical tables against report files.

usage: check_page_tables.py <page.md> <reports-dir>
Compares LUT, FF, RAMB36, RAMB18, DSP from baseline_hierarchy.rpt and the
internal WNS from baseline_scope_timing.tsv. CARRY4 needs the primitive census
(omitted from the public packet) and is reported as not checked here.
"""
import re
import sys
from pathlib import Path

page, reports = Path(sys.argv[1]).read_text(), Path(sys.argv[2])
TABLES = {
    "Vivado OOC, product 1x1": ("ax7101-ooc", ""),
    "Vivado OOC, product 8x8": ("ax8x8-ooc", ""),
    "Vivado integrated synthesis, product 8x8": ("ax8x8-synth-reports", "milan_datapath/pp_shadow/"),
    "Vivado integrated route, shipping product 1x1": ("ax7101-route-reports", "milan_datapath/pp_shadow/"),
}


def hierarchy(path: Path) -> dict[str, list[int]]:
    """Instance path -> [LUT, FF, RAMB36, RAMB18, DSP] from an indented report."""
    rows, stack = {}, []
    for line in path.read_text().splitlines():
        m = re.match(r"^\|( *)(\S[^|]*?)\s*\|[^|]*\|\s*(\d+)\s*\|\s*\d+\s*\|\s*\d+\s*\|\s*\d+\s*\|\s*(\d+)\s*\|\s*([\d.]+)\s*\|\s*(\d+)\s*\|\s*(\d+)\s*\|", line)
        if not m:
            continue
        depth = (len(m[1]) - 1) // 2
        name = m[2]
        if name.startswith("("):
            continue
        stack[depth:] = [name]
        rows["/".join(stack[1:])] = [int(m[3]), int(m[4]), float(m[5]), int(m[6]), int(m[7])]
    return rows


bad = checked = 0
for title, (folder, prefix) in TABLES.items():
    block = page.split(f"**{title}**", 1)[1].split("\n\n", 2)[1]
    hier = hierarchy(reports / folder / "baseline_hierarchy.rpt")
    scope = {}
    for line in (reports / folder / "baseline_scope_timing.tsv").read_text().splitlines()[1:]:
        inst, _, wns = line.split("\t")
        scope[inst] = float(wns)
    for line in block.splitlines()[2:]:
        cells = [c.strip() for c in line.strip("|").split("|")]
        inst = cells[0].strip("`")
        lut, ff, r36, r18, dsp = (float(c.replace(",", "")) for c in cells[1:6])
        wns = float(cells[7])
        rep = hier.get(prefix + inst)
        sc = scope.get(prefix + inst)
        ok = rep is not None and [lut, ff, r36, r18, dsp] == rep and sc is not None and abs(sc - wns) < 1e-9
        checked += 1
        bad += not ok
        print(f"{'ok' if ok else 'MISMATCH':8} {title} | {inst} page={[lut, ff, r36, r18, dsp, wns]} report={rep} scope={sc}")
print(f"rows checked: {checked}; mismatches: {bad}; CARRY4 column not checked (census omitted)")
sys.exit(1 if bad else 0)
