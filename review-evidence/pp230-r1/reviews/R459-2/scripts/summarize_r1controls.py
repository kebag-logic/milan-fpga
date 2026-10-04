#!/usr/bin/env python3
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""Tabulate r1_controls_vs_committed.sh: per round-1 control and committed
suite, the exit status, the failing-check count and the failing check names
(the tag before the first colon of each FAIL: line), with the shapes.

usage: summarize_r1controls.py CT_DIR CONTROLS_TSV
"""
import pathlib
import re
import sys


def main():
    ct, tsv = pathlib.Path(sys.argv[1]), pathlib.Path(sys.argv[2])
    print("| control | declared | suite | rc | failing | named failing checks (shapes) | verdict |")
    print("|---|---|---|---:|---:|---|---|")
    bad = 0
    for line in tsv.read_text().splitlines():
        name, expect, _ = line.split("\t")
        rcs = {}
        for rcf in sorted((ct / name).glob("*.rc")):
            suite = rcf.stem
            rc = int(rcf.read_text().strip())
            log = (ct / name / f"{suite}.log").read_text(errors="replace")
            fails = [l for l in log.splitlines() if l.startswith("FAIL:")]
            tags = {}
            for l in fails:
                m = re.match(r"FAIL: ([A-Z]+\d+[a-z]?)\b", l)
                t = m.group(1) if m else l[6:40].strip()
                sh = re.search(r"\[(\d+/\d+)\]\s*$", l)
                tags.setdefault(t, set()).add(sh.group(1) if sh else "suite, no shape tag")
            built = "checks:" in log
            rcs[suite] = (rc, len(fails), built)
            desc = "; ".join(f"{t} ({', '.join(sorted(s))})" for t, s in sorted(tags.items())[:8])
            if len(tags) > 8:
                desc += f"; +{len(tags) - 8} more"
            print(f"| `{name}` | {expect} | {suite} | {rc} | {len(fails)} | {desc} | |")
        killed = any(rc != 0 and n > 0 and b for rc, n, b in rcs.values())
        clean = all(rc == 0 and n == 0 and b for rc, n, b in rcs.values())
        if expect == "equiv":
            ok = clean
            v = "silent in every suite, as declared" if ok else "NOT SILENT"
        else:
            ok = killed
            v = "killed by a named committed check" if ok else "SURVIVES"
        bad += not ok
        print(f"| `{name}` | {expect} | **all** | | | | {v} |")
    print(f"\n{bad} controls not as declared")
    return 1 if bad else 0


if __name__ == "__main__":
    raise SystemExit(main())
