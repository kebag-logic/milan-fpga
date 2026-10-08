#!/usr/bin/env python3
"""Audit public source-head receipts without re-running a full validation bank.

Arguments: repository, extracted author-r2e directory, public Git tree JSON.
The extraction must come from evidence commit 00f489b18c63d9cf7e617ddb9e0437902062d416.
"""
import hashlib
import importlib.util
import json
from pathlib import Path
import re
import subprocess
import sys

repo, packet, treefile = map(lambda x: Path(x).resolve(), sys.argv[1:4])
root = packet / "round2e"
HEAD = "85db353400c6bf3965d279a9f5b5d47e08a0d1ed"
evidence = "00f489b18c63d9cf7e617ddb9e0437902062d416"
receipt = {"source_head": HEAD, "evidence_commit": evidence}
seen = []
def read(relative):
    path = root / relative
    data = path.read_bytes()
    seen.append({"path": relative, "sha256": hashlib.sha256(data).hexdigest()})
    return data.decode()
def js(relative):
    return json.loads(read(relative))
def good(name):
    assert read(f"logs/{name}.rc").strip() == "0", name
    record = js(f"logs/{name}.receipt.json")
    assert record["rc"] == 0
    return record

count = 0
for item in json.loads(treefile.read_text())["tree"]:
    prefix = "review-evidence/645-r1/author-r2e/"
    if item["type"] != "blob" or not item["path"].startswith(prefix):
        continue
    data = (packet / item["path"][len(prefix):]).read_bytes()
    assert hashlib.sha1(b"blob " + str(len(data)).encode() + b"\0" + data).hexdigest() == item["sha"]
    count += 1
receipt["public_packet_git_blobs_verified"] = count
exports = js("functional/exports-85db3534.json")
assert exports["commit"] == HEAD
assert all(not value["status"] for value in exports["exports"].values())

inventory = subprocess.check_output(["bash", "scripts/run_all_suites.sh", "--list"], cwd=repo, text=True).splitlines()
suite_rows, totals = [], []
for shard in (0, 1):
    good(f"sweep-{shard}-rerun")
    text = read(f"logs/sweep-{shard}-rerun.log")
    names = re.findall(r"^PASS\s+(\S+)$", text, re.M)
    suite_rows.extend(names)
    n, passed, failed, timeout = map(int, re.search(r"suites: (\d+)\s+passed: (\d+)\s+failed: (\d+)\s+timed out: (\d+)", text).groups())
    checks, failures = map(int, re.search(r"checks: (\d+)\s+in-suite failures: (\d+)", text).groups())
    assert n == passed == len(names) and failed == timeout == failures == 0
    totals.append(checks)
    for name in names:
        choices = [root / f"sweep-rerun/{shard}/{name}{suffix}" for suffix in (".log", ".tail.txt")]
        assert sum(path.exists() for path in choices) == 1
assert sorted(suite_rows) == sorted(inventory) and len(suite_rows) == len(set(suite_rows)) == 61
assert sum(totals) == 2185760
receipt["suite_sweep"] = {"suites": 61, "checks": sum(totals), "failures": 0, "exact_inventory_once": True, "raw_log_limit": "Some large logs are published as tails plus hashes; full aggregate totals are author execution evidence."}

arrival_rows, margins = [], []
for sign in ("slow", "fast"):
    for envelope in ("none", "uniform5", "tail24", "uniform60"):
        directory = root / "arrival" / f"{sign}-{envelope}"
        logs = sorted(directory.glob("b8*_p*.log"))
        assert [int(f.stem.rsplit("_p", 1)[1]) for f in logs] == list(range(16))
        group_margins = []
        for f in logs:
            rel = f.relative_to(root).as_posix()
            text = read(rel)
            assert read(str(Path(rel).with_suffix(".rc"))).strip() == "0"
            assert "RESULT: PASS" in text and "[FAIL]" not in text
            steps = re.findall(r"settle recentre fired \((\d+) pulse\(s\), render recentre executed (\d+)\); slips before it (\d+), after it (\d+)", text)
            assert len(steps) == 3 and all(a == b == "1" and post == "0" for a,b,pre,post in steps)
            assert int(steps[0][2]) <= 3 and all(pre == "0" for a,b,pre,post in steps[1:])
            times = re.findall(r"settle recentre [\d.]+ s after the start, ([\d.]+) s after LOCKED", text)
            assert len(times) == 3 and all(abs(float(t)-4.096) <= .002 for t in times)
            ms = [(float(a),float(b)) for a,b in re.findall(r"^MARGINS: .+ empty ([\d.]+) full ([\d.]+) ticks$", text,re.M)]
            assert len(ms) == 3 and all(a >= 1 and b >= 1 for a,b in ms)
            group_margins.extend(ms)
        margins.extend(group_margins)
        arrival_rows.append({"group": f"{sign}-{envelope}", "phases": 16, "post_settle_windows": len(group_margins), "minimum_empty_ticks": min(a for a,b in group_margins), "minimum_full_ticks": min(b for a,b in group_margins)})
receipt["arrival"] = {"phases":128,"post_settle_windows":len(margins),"minimum_empty_ticks":min(a for a,b in margins),"minimum_full_ticks":min(b for a,b in margins),"groups":arrival_rows}

sys.path.insert(0, str(repo / "tb/verilator/follow_ring"))
import quiet_distributions
quiet = quiet_distributions.grade(root / "arrival", 2)
receipt["quiet"] = quiet
pulls = []
for f in sorted((root / "follow-pullin").glob("pullin*.log")):
    rel = f.relative_to(root).as_posix()
    text = read(rel)
    assert read(str(Path(rel).with_suffix(".rc"))).strip() == "0"
    assert "RESULT: PASS" in text and "[FAIL]" not in text
    row = re.search(r"settle recentre fired \((\d+) pulse\(s\), render recentre executed (\d+)\); slips before it (\d+), after it (\d+)",text)
    assert row and row[1] == row[2] == "1" and row[4] == "0"
    classification=re.search(r"^RESULT-647:.*: (ON THE LAW|BEFORE NOT GRADABLE|AFTER NOT GRADABLE)$",text,re.M)
    assert classification
    pulls.append({"case": f.stem,"pre_slips":int(row[3]),"classification":classification[1]})
assert len(pulls) == 32
receipt["pullin"] = {"cases":32,"pre_slip_cases":sum(x["pre_slips"]>0 for x in pulls),"post_slips":0,"classifications":{c:sum(x["classification"]==c for x in pulls) for c in ("ON THE LAW","BEFORE NOT GRADABLE","AFTER NOT GRADABLE")}}
assert receipt["pullin"]["classifications"]=={"ON THE LAW":28,"BEFORE NOT GRADABLE":2,"AFTER NOT GRADABLE":2}

good("render-pullin")
render = []
for f in sorted((root / "render-pullin-pullin").glob("pullin*.log")):
    text = read(f.relative_to(root).as_posix())
    assert "RESULT: PASS" in text and "[FAIL]" not in text and "NOT GRADABLE" not in text
    checks, failures = map(int,re.search(r"== tdm8_render: checks: (\d+)\s+failures: (\d+) ==",text).groups())
    assert failures == 0
    render.append(checks)
assert len(render) == 18 and sum(render) == 558
good("render-boundary")
boundary = read("logs/render-boundary.log")
assert "81 checks: 81 PASS, 0 FAIL" in boundary
assert "largest walk over 564 windows is 3 cycles" in boundary
receipt["render"] = {"pullin_phases":18,"checks":558,"all_gradable":True,"boundary_checks":81,"boundary_windows":564,"max_walk_cycles":3}

comparison = []
for name in ("dev-render-mutants", "render-mutants"):
    text = read("logs/"+name+".log")
    assert read("logs/"+name+".rc").strip() == "2"
    fails = re.findall(r"^\[FAIL\].*$",text,re.M)
    passes = re.findall(r"^\[PASS\].*$",text,re.M)
    comparison.append((fails,passes))
assert len(comparison[0][0]) == 4 and comparison[0][0] == comparison[1][0]
assert len(comparison[0][1]) == 28 and len(comparison[1][1]) == 30
assert set(comparison[0][1]) <= set(comparison[1][1])
receipt["issue_657"] = {"dev":"28/32, rc 2","head":"30/34, rc 2","identical_failures":comparison[0][0],"new_passing_rows":sorted(set(comparison[1][1])-set(comparison[0][1]))}
follow = read("sweep-rerun/0/follow_ring.log")
assert "follow_ring mutants: 12/12 caught" in follow and "small pulls: 10/10 passed" in follow
receipt["follow_default"] = {"mutants": "12/12 caught", "small_pulls":"10/10", "controller_rates":re.findall(r"settle control (\d+) Hz: PASS",follow)}
assert len(receipt["follow_default"]["controller_rates"])==4
good("physical")
physical = read("physical/milan_dp_gptp.log")
assert "checks: 197   in-suite failures: 0" in read("logs/physical.log")
wire = re.findall(r"^RECENTRE WIRE .*$", physical,re.M)
assert len(wire) == 2 and all("declared_step=-5 observed_step=-5" in row and "dup=0 skip=0" in row for row in wire)
receipt["physical_model"] = {"checks":197,"wire_rows":wire,"hardware_proof":False}

sys.path.insert(0,str(repo / "syn/ooc"))
import pp_resource_gate as gate
baseline = (repo / "syn/ooc/pp_resource_baseline.json").read_bytes()
resources = js("resource-summary.json")
assert hashlib.sha256(baseline).hexdigest() == resources["baseline_sha256"]
assert not gate.check_baseline(gate.load(repo / "syn/ooc/pp_resource_baseline.json"),repo / "docs/design/AREA_BUDGET.md")
resource_rows=[]
for endpoint, folder, kind in [("route-1x1","ax7101/gateware","route"),("ooc-1x1","ooc-1x1","ooc"),("ooc-8x8","ooc-8x8","ooc")]:
    good("resource-"+endpoint)
    log=read("logs/resource-"+endpoint+".log")
    assert "RESULT: PASS" in log
    figures=gate.utilization(read(f"timing/{folder}/baseline_utilization.rpt"),kind)
    summary=next(r for r in resources["rows"] if r["endpoint"]==endpoint)
    assert all(summary["candidate"][k]==v for k,v in figures.items())
    assert summary["identity_matches"] and summary["rc"]==0
    resource_rows.append({"endpoint":endpoint,"raw_figures":figures,"baseline":summary["baseline"],"gate_exit":0})
receipt["resources"]={"baseline_sha256":resources["baseline_sha256"],"endpoints":resource_rows,"limit":"Full source-input digest cannot be reconstructed from trimmed public artifacts; exact-source admission and successful check commands are author receipts."}
own={}
for tag in ("cmc_base","cmc_head","settle_base","settle_head"):
    fig=gate.utilization(read(f"area-ooc/util_{tag}.rpt"),"ooc")
    own[tag]={k:fig[k] for k in ("LUT","FF")}
delta={key:sum(own[x+"_head"][key]-own[x+"_base"][key] for x in ("cmc","settle")) for key in ("LUT","FF")}
assert delta=={"LUT":113,"FF":78}
assert all(value<=120 for value in delta.values())
for tag,rev in (("base","99e4eb6c"),("head",HEAD)):
    data=subprocess.check_output(["git","show",rev+":hdl/ieee1722/aaf/KL_chan_map_capture.sv"],cwd=repo)
    assert hashlib.sha256(data).hexdigest()==js("area-ooc/comparison.json")["inputs"]["cmc_"+tag+".sv"]["sha256"]
    dp=subprocess.check_output(["git","show",rev+":hdl/milan/milan_datapath.sv"],cwd=repo,text=True)
    start=dp.index("  localparam int unsigned SRC_SETTLE_ERR_C")
    marker="  end : g_src_recentre" if tag=="base" else "  end : g_settle_recentre"
    fragment=dp[start:dp.index(marker,start)+len(marker)]+"\n"
    if tag=="head":
        fragment=next(line for line in dp.splitlines() if "localparam int unsigned MCSRV_WIN_LOG2_C" in line)+"\n"+fragment
    key="piece_base.svh" if tag=="base" else "piece_new.svh"
    assert hashlib.sha256(fragment.encode()).hexdigest()==js("area-ooc/comparison.json")["inputs"][key]["sha256"]
receipt["own_area"]={"rows":own,"delta":delta,"limit_each":120}

timing=[]
for directive,folder in [("ExtraPostPlacementOpt","ax7101"),("AltSpreadLogic_high","ax7101-AltSpreadLogic_high"),("ExtraTimingOpt","ax7101-ExtraTimingOpt")]:
    good(directive+"-implementation");good(directive+"-manifest")
    assert read("logs/"+directive+"-constraint-check.rc").strip()=="0"
    prefix=f"timing/{folder}/gateware/alinx_ax7101"
    metrics=[]
    for corner in ("Slow","Fast"):
        for temperature in (0,85):
            text=read(f"{prefix}_signoff_{corner}_{temperature}C_timing.head.txt")
            lines=[l for l in text.split("| Design Timing Summary")[1].splitlines() if l.strip()]
            ix=next(i for i,l in enumerate(lines) if "WNS(ns)" in l)
            values=lines[ix+2].split()
            assert all(float(values[i])==0 for i in (1,2,5,6))
            metrics.append({"corner":corner,"temperature_metadata":temperature,**gate.timing(text),"TNS_ns":float(values[1]),"THS_ns":float(values[5]),"setup_failing_endpoints":int(values[2]),"hold_failing_endpoints":int(values[6])})
    pack=read(prefix+"_iob_pack.rpt")
    rows=re.findall(r"^PASS  eth0_rx_(?:data\[\d\]|dv):.*$",pack,re.M)
    assert len(rows)==9 and all("ILOGIC_" in row for row in rows)
    assert len(re.findall(r"^PASS  ",pack,re.M))==21 and not re.search(r"^FAIL  ",pack,re.M)
    wns=min(x["WNS_ns"] for x in metrics);whs=min(x["WHS_ns"] for x in metrics)
    timing.append({"directive":directive,"worst_WNS_ns":wns,"worst_WHS_ns":whs,"corner_metrics":metrics,"IOB":"21 PASS / 1 INERT / 0 FAIL","nine_GMII_in_ILOGIC":True,"meets_margin":wns>=.03 and whs>=0})
assert [(r["worst_WNS_ns"],r["worst_WHS_ns"]) for r in timing]==[(.057,.024),(.066,.024),(.011,.036)]
receipt["timing"]={"rows":timing,"kept":"AltSpreadLogic_high","fresh_synthesis_run_by_reviewer":False}
receipt["examined_public_receipts"] = sorted({row["path"]:row for row in seen}.values(),key=lambda row:row["path"])
receipt["result"]="PASS"
print(json.dumps(receipt,indent=2))
