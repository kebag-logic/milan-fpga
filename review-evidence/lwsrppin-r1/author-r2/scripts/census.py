#!/usr/bin/env python3
"""The twin grade self-test's census, counted from outside: the printed total must equal the checks executed.

Usage: census.py <parent-root>
Counts every call of selftest()'s nested `check` with a profile hook (the way an outside reviewer counted it),
independently of the `ran` list the grade keeps, then runs `twin_mrp.py --selftest` as `make twin` does and reads
the total it prints. Exit 0 only when the two agree, every name is distinct and the run passed.
"""
import re
import subprocess
import sys
from pathlib import Path

root = Path(sys.argv[1]).resolve()
here = root / "tb/verilator/milan_dp"
sys.path.insert(0, str(here))
import twin_mrp as m  # noqa: E402

calls: list[str] = []


def record(frame, event, arg):
    if event == "call" and frame.f_code.co_name == "check" and frame.f_code.co_filename == m.__file__:
        calls.append(frame.f_locals["name"])


sys.setprofile(record)
failed = m.selftest()
sys.setprofile(None)
res = subprocess.run([sys.executable, "-B", "twin_mrp.py", "--selftest"], cwd=here, capture_output=True,
                     text=True, check=False)
line = res.stdout.strip()
printed = re.search(r"\((\d+) checks\)", line)
literal = [n for n in re.findall(r"OK \((\d+) checks\)", (here / "twin_mrp.py").read_text(encoding="utf-8"))]
print("executed named checks:", len(calls), calls)
print("distinct names:", len(set(calls)))
print("selftest() failures:", failed)
print("printed:", repr(line), "rc", res.returncode)
print("hard-coded totals in the source:", literal or "none")
ok = (printed is not None and int(printed.group(1)) == len(calls) == len(set(calls)) and not failed
      and res.returncode == 0 and not literal)
print("census", "AGREES" if ok else "DISAGREES")
sys.exit(0 if ok else 1)
