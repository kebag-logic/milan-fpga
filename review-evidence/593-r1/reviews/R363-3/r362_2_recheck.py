#!/usr/bin/env python3
"""R363-3: my own equivalents of the other reviewer's round-2 probes and mutants,
rebuilt from the public R362-2 comment (5859529549) only.

Usage: r362_2_recheck.py <repo>
Part 1 grades I3e-I3h on both tu oracles. Part 2 applies one mutant per counted
R362-2 survivor to a private copy of tb/tools/torture_campaign.py and runs the
unchanged --self-test (KILLED = rc 1 with a named FAIL/ERROR). Up to 8 jobs.
"""
from __future__ import annotations

import concurrent.futures as cf
import importlib.util
import re
import subprocess
import sys
import tempfile
from pathlib import Path

sys.dont_write_bytecode = True
repo = Path(sys.argv[1])
path = repo / "tb/tools/torture_campaign.py"
src = path.read_text(encoding="utf-8")
spec = importlib.util.spec_from_file_location("tc", path)
tc = importlib.util.module_from_spec(spec)
sys.modules["tc"] = tc
spec.loader.exec_module(tc)

print("## Part 1: I3e-I3h (GM at 0, interval [0, clear), resolution R)")
for pid, clear, r, ok in (("I3e", 0.002, 0.249, {"FAIL", "NOT RUN"}), ("I3f", 0.06, 0.2, {"FAIL", "NOT RUN"}),
                          ("I3g", 0.13, 0.125, {"FAIL", "NOT RUN"}), ("I3h", 0.124, 0.124, {"FAIL"})):
    h = tc.check_release_tu_history([(0, clear)], [], gm_changes_s=[0], observation_resolution_s=r,
                                    capture_complete=True)[0]
    s = tc.check_release_tu((0, clear), [], gm_changes_s=[0], holdover_bound_s=0.5,
                            observation_resolution_s=r, capture_complete=True)[0]
    print(f"{pid} R={r} clear={clear}: history={h} single={s} required={sorted(ok)} "
          f"{'MET' if h in ok and s in ok else 'UNMET'}")

MUT = (
    ("C06 covered GM drops start allowance",
     "if start_s - resolution_s <= Decimal(str(event)) < clear_s]", "if start_s <= Decimal(str(event)) < clear_s]"),
    ("C07 covered GM includes clear",
     "if start_s - resolution_s <= Decimal(str(event)) < clear_s]",
     "if start_s - resolution_s <= Decimal(str(event)) <= clear_s]"),
    ("C09 touching intervals accepted",
     "(intervals and start_s <= intervals[-1][1])", "(intervals and start_s < intervals[-1][1])"),
    ("C10 history negative resolution accepted",
     "or not 0 <= observation_resolution_s < RELEASE_TU_RESOLUTION_LIMIT_S):",
     "or not observation_resolution_s < RELEASE_TU_RESOLUTION_LIMIT_S):"),
    ("C19 history resolution_limit_s removed",
     '              "resolution_limit_s": RELEASE_TU_RESOLUTION_LIMIT_S}', "              }"),
    ("C34 empty stream_id accepted",
     'or not record["stream_id"] or not _release_finite', "or not _release_finite"),
    ("C35 negative pdu_index accepted", ' or pdu["pdu_index"] < 0\n', "\n"),
    ("T05 mr cause-window text deleted",
     '"match causes within +/- observation_resolution_s of the toggle; "', '""'),
    ("T21 mr cause-window text made one-sided",
     '"match causes within +/- observation_resolution_s of the toggle; "',
     '"match causes within + observation_resolution_s of the toggle; "'),
    ("T13 tu PHC/fabric examples text deleted",
     '"(including PHC settime/adjtime and fabric discontinuity); "', '""'),
    ("T25 tu PHC/fabric examples text negated",
     '"(including PHC settime/adjtime and fabric discontinuity); "',
     '"(excluding PHC settime/adjtime and fabric discontinuity); "'),
    ("C38 mr verdict cause_window string altered",
     '"cause_window": "toggle timestamp +/- observation_resolution_s",', '"cause_window": "toggle timestamp",'),
)


def run(m):
    name, old, new = m
    if src.count(old) != 1:
        return f"ANCHOR-ERROR {name}: count={src.count(old)}"
    with tempfile.TemporaryDirectory(prefix="r363x-") as d:
        p = Path(d) / "torture_campaign.py"
        p.write_text(src.replace(old, new), encoding="utf-8")
        r = subprocess.run([sys.executable, "-B", str(p), "--self-test"], capture_output=True, text=True,
                           timeout=600)
        failed = sorted(set(re.findall(r"^(?:FAIL|ERROR): (test_\w+)", r.stderr, re.M)))
        state = "KILLED" if r.returncode == 1 and failed else "SURVIVED" if r.returncode == 0 else f"CRASH rc={r.returncode}"
        return f"{state} {name}: {failed}"


print("## Part 2: R362-2 counted survivors, my equivalent mutants")
with cf.ThreadPoolExecutor(max_workers=8) as ex:
    for line in ex.map(run, MUT):
        print(line)
