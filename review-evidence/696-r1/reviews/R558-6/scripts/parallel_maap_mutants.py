#!/usr/bin/env python3
"""Run tb/verilator/maap/mutants.py's own MUTANTS table and run_case() in parallel.

Usage: parallel_maap_mutants.py <repo-root> <work-dir> [jobs]

Same anchors, replacements, named checks and kill rule as the committed driver
(build succeeds, harness exits 1, the named [FAIL] line is present; a clean
control must exit 0 with " 0 failures"). Only the scheduling differs (one worker process per row, so each
row's captured report is its own). The
datapath clean control and the three datapath plants are taken verbatim from
the committed driver's main().
"""
import concurrent.futures as cf
import multiprocessing
import contextlib
import io
import sys
from pathlib import Path

root, work = Path(sys.argv[1]).resolve(), Path(sys.argv[2]).resolve()
jobs = int(sys.argv[3]) if len(sys.argv) > 3 else 8
sys.path.insert(0, str(root / "tb/verilator/maap"))
import mutants as m  # noqa: E402

source = m.RTL.read_text()
cases = [("clean", source, None, False)]
bad = []
for name, _item, anchor, repl, failure in m.MUTANTS:
    if source.count(anchor) != 1:
        bad.append(name)
        continue
    cases.append((name, source.replace(anchor, repl), failure, False))
DATAPATH = (
    ("m4_datapath_clean", None, None),
    ("m4_reset_time_sampling",
     ("      lfsr_r       <= 32'hACE1;\n      rng_seeded_r <= 1'b0;",
      "      lfsr_r       <= enable_seed_w;\n      rng_seeded_r <= 1'b1;"),
     "M4 datapath: programmed MAC changes probe intervals"),
    ("m5_datapath_ignores_link",
     ("else if (restart_w || port_operational_p)", "else if (restart_w)"),
     "M5 datapath: link return starts four fresh PROBEs"),
    ("m3_datapath_ignores_clock",
     ("station_mac_i[31:0] + realtime_ns_i", "station_mac_i[31:0]"),
     "M3 datapath: real-time clock changes probe intervals"),
)
for name, sub, failure in DATAPATH:
    if sub is None:
        cases.append((name, source, None, True))
    elif source.count(sub[0]) != 1:
        bad.append(name)
    else:
        cases.append((name, source.replace(*sub), failure, True))
work.mkdir(parents=True, exist_ok=True)


def one(case):
    """Run one row through the committed run_case and capture its report."""
    name, src, failure, integration = case
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        ok = m.run_case(work, name, src, failure, integration)
    return name, ok, buf.getvalue()


results = {}
with cf.ProcessPoolExecutor(max_workers=jobs,
                            mp_context=multiprocessing.get_context("fork")) as ex:
    for name, ok, out in ex.map(one, cases):
        results[name] = ok
        print(out.rstrip(), flush=True)
        print(f"ROW {name} {'PASS' if ok else 'FAIL'}", flush=True)
for name in bad:
    print(f"[ESCAPED] {name}: expected exactly one mutation anchor")
fails = sum(not v for v in results.values()) + len(bad)
print(f"== parallel maap mutants: rows: {len(results) + len(bad)}   failures: {fails} ==")
sys.exit(1 if fails else 0)
