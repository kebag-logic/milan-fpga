#!/usr/bin/env python3
"""Re-derive the merge-head AX7101 1x1 TDM8 3-seed table from the published JSON.

Usage: sweep_crosscheck.py <sweep-results.json> <sweep-summary.json>
Checks, per seed: head, rc, four declared corners (Slow/Fast x 0/85 C),
WNS >= +0.030, WHS >= 0, TNS = THS = 0, four Ethernet pairs at 8 ns with
positive slack, Max Delay Datapath Only in every interaction report, no
'unsafe' row, zero 12-4739/20-1307/12-5201, zero critical warnings, accepted
build gate, unquarantined bitstream, and hook order in the emitted Tcl.
"""
import json, sys
HEAD = "c7ee5cbd4ed6215b988f3811d5e9156e21aa55c5"
res = {r["seed"]: r for r in json.load(open(sys.argv[1]))}
summ = json.load(open(sys.argv[2]))
ok = True
def check(cond, msg):
    global ok
    print(("  PASS " if cond else "  FAIL ") + msg); ok &= bool(cond)
# Claimed table (issue #607 REVIEW READY 5877640842), to compare against JSON.
CLAIM = {"asl": (0.312, 0.036, (6.141, 6.644, 6.465, 6.591)),
         "eto": (0.309, 0.014, (6.279, 6.719, 6.583, 6.591)),
         "eppo": (0.063, 0.036, (6.136, 6.826, 6.443, 6.691))}
PAIRS = (("eth_clocks0_rx", "milansoc_crg_clkout0"), ("milansoc_crg_clkout0", "eth_clocks0_rx"),
         ("eth_clocks0_rx", "milansoc_crg_clkout1"), ("milansoc_crg_clkout1", "eth_clocks0_rx"))
print("rom_check:", {k: v["expected"] == v["actual"] for k, v in summ["rom_check"].items()})
check(all(v["expected"] == v["actual"] for v in summ["rom_check"].values()), "generated ROMs equal the c951a9ff digest rows")
print("| Seed | WNS | TNS | WHS | THS | eth->sys | sys->eth | eth->milan | milan->eth | CW | 12-4739/20-1307/12-5201 |")
for s in summ["seeds"]:
    seed = s["seed"]; r = res[seed]
    print(f"== {seed} {s['directive']}")
    check(s["head"] == HEAD and r["head"] == HEAD, "summary and results name the exact head")
    check(r["rc"] == 0 and r["report_rc"] == 0, "build rc 0 and report rc 0")
    check("--vivado-max-threads" in r["command"] and r["command"][r["command"].index("--vivado-max-threads") + 1] == "16", "16-thread cap in the recorded command")
    check(r["command"][r["command"].index("--place-directive") + 1] == s["directive"], "directive matches command")
    corners = {(t["corner"], int(t["temperature_C"])) for t in s["timing"]}
    check(corners == {("Slow", 0), ("Fast", 0), ("Slow", 85), ("Fast", 85)}, f"four declared corners {sorted(corners)}")
    wns = min(t["WNS"] for t in s["timing"]); whs = min(t["WHS"] for t in s["timing"])
    tns = min(t["TNS"] for t in s["timing"]); ths = min(t["THS"] for t in s["timing"])
    check(all(t["WNS"] >= 0.030 for t in s["timing"]), f"WNS >= +0.030 at every corner (worst {wns:+.3f})")
    check(all(t["WHS"] >= 0 for t in s["timing"]), f"WHS >= 0 at every corner (worst {whs:+.3f})")
    check(tns == 0 and ths == 0 and all(t["negative_paths"] == 0 for t in s["timing"]), "TNS = THS = 0, no negative paths")
    slack = {}
    for p in PAIRS:
        rows = [c for c in s["crossings"] if (c["from"], c["to"]) == p]
        check(len(rows) == 4 and all(c["requirement_ns"] == 8.0 and c["slack_ns"] > 0 for c in rows),
              f"{p[0]}->{p[1]}: 4 corner rows, 8.000 ns requirement, positive slack")
        slack[p] = min(c["slack_ns"] for c in rows)
    for rep in s["interactions"]:
        pairs = rep["pairs"]
        good = len(pairs) == 4 and all(l.rstrip().endswith("Max Delay Datapath Only") and " 8.00 " in l for l in pairs)
        unsafe = [l for l in rep["all_eth_pairs"] if "unsafe" in l.lower()]
        check(good and not unsafe, f"{rep['report'].rsplit('/', 1)[-1]}: 4 pairs Max Delay Datapath Only at 8.00, no unsafe")
    check(len(s["interactions"]) == 7, f"seven interaction reports ({len(s['interactions'])})")
    check(s["emitted_severity_counts"].get("CRITICAL WARNING", -1) == 0 and not s["critical_warnings"], "zero critical warnings")
    check(s["emitted_severity_counts"].get("ERROR", -1) == 0, "zero errors")
    check(all(v == 0 for v in s["diagnostic_counts"].values()) and set(s["diagnostic_counts"]) == {"12-4739", "20-1307", "12-5201"}, "zero 12-4739/20-1307/12-5201")
    check(any("no 12-4739, 20-1307 or 12-5201" in l for l in s["build_gate"]) and s["bitstreams"] == ["alinx_ax7101.bit"], "build gate accepted; unquarantined bitstream")
    check(any("quasi_static cells=112" in a["text"] for a in s["application"]) and any("budget_ns=8.000" in a["text"] for a in s["application"]), "hook applied (112 quasi-static cells, 8 ns budget)")
    o = s["tcl_order"]
    check(o["synth_design"] < o["milan_eth_constraints"] < o["opt_design"] < o["kl_timing_grade_configure"] < o["place_design"]
          < o["route_design"] < o["kl_timing_grade_reports"] < o["report_clock_interaction"] < o["write_bitstream"], f"emitted Tcl order {o}")
    check(s["margin_ok"] and s["bound_ok"], "collector margin_ok and bound_ok")
    cw, cwhs, cs = CLAIM[seed]
    derived = (slack[PAIRS[0]], slack[PAIRS[1]], slack[PAIRS[2]], slack[PAIRS[3]])
    check(abs(wns - cw) < 5e-4 and abs(whs - cwhs) < 5e-4 and all(abs(a - b) < 5e-4 for a, b in zip(derived, cs)),
          f"published prose table row equals JSON-derived row")
    print(f"| {seed} | {wns:+.3f} | {tns:g} | {whs:+.3f} | {ths:g} | " + " | ".join(f"{x:+.3f}" for x in derived)
          + f" | {s['emitted_severity_counts']['CRITICAL WARNING']} | {sum(s['diagnostic_counts'].values())} |")
print("SWEEP", "PASS" if ok else "FAIL")
sys.exit(0 if ok else 1)
