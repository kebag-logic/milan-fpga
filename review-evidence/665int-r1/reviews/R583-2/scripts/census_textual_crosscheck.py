#!/usr/bin/env python3
"""Reviewer cross-check, independent of the census's parser: every textual
occurrence (comments blanked) of a pp_cd_*_w wire or pp_aecp_strm_started_w in
milan_datapath.sv is either a declaration, the processor wrapper's own output
connection, or on a line the census reports as a read. Prints any occurrence
that is none of these. Usage: python3 -I census_textual_crosscheck.py <repo> <census --list log>"""
import re, sys
from pathlib import Path
repo, listing = Path(sys.argv[1]), Path(sys.argv[2])
text = (repo / "hdl/milan/milan_datapath.sv").read_text()
code = re.sub(r"/\*.*?\*/", lambda m: re.sub(r"[^\n]", " ", m.group()), text, flags=re.S)
code = re.sub(r"//[^\n]*", "", code)
census_lines = set()
for ln in listing.read_text().splitlines():
    m = re.search(r"lines (\S+)", ln)
    if m:
        census_lines |= {int(x) for x in m.group(1).split(",")}
pop = re.compile(r"\b(pp_cd_\w+_w|pp_aecp_strm_started_w)\b")
decl = re.compile(r"^\s*(wire|logic)\b")
outconn = re.compile(r"^\s*\.\w+_o\s*\(\s*(pp_cd_\w+_w|pp_aecp_strm_started_w)\s*\)")
other, counts = [], {"declaration": 0, "wrapper output": 0, "census read": 0}
for no, line in enumerate(code.splitlines(), 1):
    for m in pop.finditer(line):
        if decl.match(line) and line.index(m.group()) < (line.index("=") if "=" in line else 10**9):
            counts["declaration"] += 1
        elif outconn.match(line):
            counts["wrapper output"] += 1
        elif no in census_lines:
            counts["census read"] += 1
        else:
            other.append(f"line {no}: {line.strip()[:120]}")
print(counts, f"census lines {len(census_lines)}")
print("unaccounted occurrences:", len(other)); [print("  " + o) for o in other]
sys.exit(1 if other else 0)
