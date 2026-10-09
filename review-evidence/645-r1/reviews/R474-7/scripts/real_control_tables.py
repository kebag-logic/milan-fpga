#!/usr/bin/env python3
"""Grade trace_table.py on real harness traces against the harness's own prints.

    python3 -I -B real_control_tables.py <source-tree> <controls-dir> <name>...

For every printed window "[a, e) s: ring slips D+S" with a < e, the table is
run as one bin [a, e) (origin 0) and must report slips D+S and skips S.
It also bins the whole run [0, end) in 0.25 s steps and requires the column
totals to equal the RING-EVENT record counts (dup+skip, skip, recentre),
with no slip in any bin whose only event is a recentre.
"""
import csv
import re
import subprocess
import sys
from pathlib import Path


def table(src, d, n, a, e, step):
    out = d / f"{n}.table-{a}-{e}-{step}.csv"
    argv = [sys.executable, "-I", "-B", str(src / "tb/verilator/follow_ring/trace_table.py"),
            str(d / f"{n}.log"), str(d / f"{n}.pdu.csv"), str(d / f"{n}.servo.csv"),
            "--origin-s", "0", "--from-s", a, "--to-s", e, "--step-s", step, "--csv", str(out)]
    r = subprocess.run(argv, capture_output=True, text=True)
    if r.returncode:
        raise SystemExit(f"{n}: trace_table rc {r.returncode}: {r.stderr}")
    return list(csv.DictReader(out.open()))


def main():
    src, d = Path(sys.argv[1]), Path(sys.argv[2])
    ok = True
    for n in sys.argv[3:]:
        log = (d / f"{n}.log").read_text()
        ev = re.findall(r"^RING-EVENT: (dup|skip|recentre) ([0-9.]+)$", log, re.M)
        end = re.search(r"^RING-EVENTS: complete through ([0-9.]+) s$", log, re.M).group(1)
        for m in re.finditer(r"\[\s*([-0-9.]+),\s*([-0-9.]+)\) s: ring slips (\d+)\+(\d+)", log):
            a, e, dn, sn = m.group(1), m.group(2), int(m.group(3)), int(m.group(4))
            if float(e) <= float(a) or float(a) < 0:
                continue
            step = f"{float(e) - float(a):.3f}"
            rows = table(src, d, n, a, e, step)
            got = (sum(int(r["slips"]) for r in rows), sum(int(r["skips"]) for r in rows))
            good = got == (dn + sn, sn)
            ok &= good
            print(f"{n} window [{a}, {e}): harness {dn}+{sn} table slips/skips {got} "
                  f"{'AGREE' if good else 'DISAGREE'}")
        rows = table(src, d, n, "0", end, "0.25")
        tot = tuple(sum(int(r[k]) for r in rows) for k in ("slips", "skips", "recentres"))
        exp = (sum(k != "recentre" for k, _ in ev), sum(k == "skip" for k, _ in ev),
               sum(k == "recentre" for k, _ in ev))
        good = tot == exp
        ok &= good
        nonzero = [(r["t_s"], r["slips"], r["skips"], r["recentres"]) for r in rows
                   if r["slips"] != "0" or r["recentres"] != "0"]
        print(f"{n} whole run [0, {end}) by 0.25 s: totals (slips, skips, recentres) {tot} "
              f"records {exp} {'AGREE' if good else 'DISAGREE'}; nonzero bins {nonzero}")
    print("real control tables:", "PASS" if ok else "FAIL")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
