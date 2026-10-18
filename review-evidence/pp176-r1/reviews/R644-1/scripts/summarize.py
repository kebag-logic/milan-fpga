#!/usr/bin/env python3
"""Summarize the reviewer's suite runs: per run, the rc, the default-build
tally (pp_top) or sweep tally (aecp_cmds), and the failing check IDs or
decode lines. aecp_cmds lines naming the engine's sweep-input digest or the
trial count are dropped for the mux tree, whose engine is the planted copy.
Usage: summarize.py <runs-dir>"""
import pathlib
import re
import sys

runs = pathlib.Path(sys.argv[1])
order = lambda p: [int(t) if t.isdigit() else t for t in re.split(r"(\d+)", p.name)]
for rc in sorted(runs.glob("*.rc"), key=order):
    name = rc.stem
    log = rc.with_suffix(".log").read_text(errors="replace").splitlines()
    tally = [l for l in log if l.startswith("[build default") or l.startswith("aecp_cmds:")]
    fails = []
    for l in log:
        if "pp_top" in name and l.startswith("FAIL: "):
            fails.append(l[6:].split(":", 1)[0])
        if "aecp_cmds" in name and l.startswith("FAIL:"):
            if name.startswith("mux-") and ("sweep inputs" in l or "sweep trials" in l):
                continue
            m = re.search(r"decode AEM 0x000E (\w+): observed (\{.*?\}\}?)", l)
            fails.append(f"0x000E {m.group(1)} observed {m.group(2)}" if m else l[5:].strip()[:160])
    print(f"{name}: rc={rc.read_text().strip()} | {' / '.join(tally)}")
    print(f"    fails: {', '.join(fails) if fails else '(none)'}")
