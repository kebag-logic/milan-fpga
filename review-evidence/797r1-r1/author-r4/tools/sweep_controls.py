#!/usr/bin/env python3
"""Planted controls for scripts/register_read_sweep.py: each plants one defect
into a copy of the head's page and runs the sweep on it. A wrong row must exit
1 (a new table included: the harness reads every table's words), an unreadable clause
must exit 2.
Usage: sweep_controls.py <lane> <work>   (prints a TSV; exit 1 if any control survives)"""
import subprocess
import sys
from pathlib import Path

lane, work = Path(sys.argv[1]), Path(sys.argv[2])
page = (lane / "docs/reference/REGISTER_MAP.md").read_text(encoding="utf-8")
OLD_RENDER = "| `STRM_SEL[8]` selects a listener and the stream index `STRM_SEL[3:0]` is 0 | the fields above |"
NEW_RENDER = "| the selected stream exists and `STRM_SEL[8]` selects a listener | the fields above |"
PLANTS = [
    ("baseline: the head's page", lambda p: p, 0),
    ("RENDER_STAT row as at e90284bd", lambda p: p.replace(NEW_RENDER, OLD_RENDER), 1),
    ("STRMW_SRP index-0 row without STRM_SEL[9]",
     lambda p: p.replace("is 0 and `STRM_SEL[9]` is 0 | `i_lwsrp_status` |", "is 0 | `i_lwsrp_status` |"), 1),
    ("CHMAP_LOOP values swapped",
     lambda p: p.replace("| `CHMAP_SNAP[1]` is 1 | the fields above |", "| `CHMAP_SNAP[1]` is 1 | `0xDEADDEAD` |"), 1),
    ("STRMW_CNTn RAW row reads the poison",
     lambda p: p.replace("is `SK_RAW_C` | the fields above |", "is `SK_RAW_C` | `0xDEADDEAD` |"), 1),
    ("STRMW_SID_LO SRP row without the poll clause",
     lambda p: p.replace(" and the SRP table answered a poll since the last `STRM_SEL`/`STRMW_CTRL` write | `i_srp_ctx_rd_sid[31:0]` |",
                         " | `i_srp_ctx_rd_sid[31:0]` |"), 1),
    ("a clause the sweep cannot read",
     lambda p: p.replace("| `CHMAP_SNAP[1]` is 0 |", "| no channel-map readback has completed |"), 2),
    ("a new read table is swept without a sweep edit",
     lambda p: p.replace("## Build parameters", "### NEWREG register (offset 0x7FC)\n\n| When | A read returns |\n"
                         "|---|---|\n| every case | `0x12345678` |\n\n## Build parameters", 1), 1),
]
print("control\trc\twant\tlast line")
bad = 0
for name, plant, want in PLANTS:
    planted = plant(page)
    if want and planted == page:
        print(f"{name}\t-\t{want}\tTHE PLANT DID NOT APPLY")
        bad += 1
        continue
    target = work / "page.md"
    target.write_text(planted, encoding="utf-8")
    run = subprocess.run([sys.executable, "-I", str(lane / "scripts/register_read_sweep.py"), "--page", str(target),
                          "--work", str(work / "build")], capture_output=True, text=True, check=False)
    last = (run.stdout.strip().splitlines() or [""])[-1]
    bad += run.returncode != want
    print(f"{name}\t{run.returncode}\t{want}\t{last}")
sys.exit(1 if bad else 0)
