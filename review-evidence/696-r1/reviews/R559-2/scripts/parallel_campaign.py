#!/usr/bin/env python3
"""Run every row of the tree's tb/verilator/maap/mutants.py campaign concurrently,
reusing its own MUTANTS table, run_case() verdict rule and the four real-datapath
rows of its main(). Usage: VERILATOR=<path> python3 -I parallel_campaign.py <tree> <workdir> [jobs]"""
import importlib.util, sys, pathlib, concurrent.futures as cf
tree, work = pathlib.Path(sys.argv[1]).resolve(), pathlib.Path(sys.argv[2]).resolve()
jobs = int(sys.argv[3]) if len(sys.argv) > 3 else 12
spec = importlib.util.spec_from_file_location("mutants", tree / "tb/verilator/maap/mutants.py")
m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
src = m.RTL.read_text()
rows = [("clean", src, None, False)]
for name, _, anchor, repl, failure in m.MUTANTS:
    assert src.count(anchor) == 1, name
    rows.append((name, src.replace(anchor, repl), failure, False))
rows.append(("m4_datapath_clean", src, None, True))
for name, a, r, f in (
    ("m4_reset_time_sampling", "      lfsr_r       <= 32'hACE1;\n      rng_seeded_r <= 1'b0;",
     "      lfsr_r       <= enable_seed_w;\n      rng_seeded_r <= 1'b1;", "M4 datapath: programmed MAC changes probe intervals"),
    ("m5_datapath_ignores_link", "else if (restart_w || port_operational_p)", "else if (restart_w)",
     "M5 datapath: link return starts four fresh PROBEs"),
    ("m3_datapath_ignores_clock", "station_mac_i[31:0] + realtime_ns_i", "station_mac_i[31:0]",
     "M3 datapath: real-time clock changes probe intervals")):
    assert src.count(a) == 1, name
    rows.append((name, src.replace(a, r), f, True))
work.mkdir(parents=True, exist_ok=True)
with cf.ThreadPoolExecutor(jobs) as ex:
    res = list(ex.map(lambda row: (row[0], m.run_case(work, *row)), rows))
fails = [n for n, ok in res if not ok]
print(f"== parallel maap campaign: rows {len(res)} mutants {len(res)-2} escaped/failed {len(fails)} {fails} ==")
sys.exit(1 if fails else 0)
