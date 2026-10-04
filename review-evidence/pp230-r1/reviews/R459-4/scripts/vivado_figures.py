#!/usr/bin/env python3
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""Re-derive PR #154's area and timing figures from the published Vivado reports.

Inputs: a directory holding review-evidence/pp230-r1/author-r1/vivado/{base,head}/...
as published on the milan-fpga evidence branch (commit 06fe795b), and that
commit's MANIFEST.json. Every report read is first checked against its
published SHA-256. Prints the figures; exit 0 when every figure equals the
value the PR body and docs/architecture/10_srp_engine.md section 5.1 state.

usage: vivado_figures.py <vivado-dir> <MANIFEST.json>
"""
import hashlib
import json
import re
import sys
from pathlib import Path

root, manifest = Path(sys.argv[1]), json.loads(Path(sys.argv[2]).read_text())
pub = {e["file"]: e["published_sha256"] for e in manifest}
bad = 0


def read(rel: str) -> str:
    global bad
    p = root / rel
    h = hashlib.sha256(p.read_bytes()).hexdigest()
    key = "author-r1/vivado/" + rel
    if pub.get(key) != h:
        print(f"DIGEST MISMATCH {key}")
        bad += 1
    return p.read_text()


def hier(rel: str) -> dict[str, tuple[int, int, int]]:
    """Instance -> (total LUT, LUTRAM, FF) for u_srp and its children."""
    out = {}
    for ln in read(rel).splitlines():
        m = re.match(r"^\|\s+(\(u_srp\)|u_srp|u_admission|u_decoder|u_domain|u_encoder|u_listener|u_talker|u_vlan)\s+\|\s+(KL_srp_\w+)\s+\|"
                     r"\s+(\d+)\s+\|\s+\d+\s+\|\s+(\d+)\s+\|\s+\d+\s+\|\s+(\d+)\s+\|", ln)
        if m:
            out[m.group(1) if m.group(1) in ("u_srp", "(u_srp)") else m.group(2)] = (
                int(m.group(3)), int(m.group(4)), int(m.group(5)))
    return out


def wns(rel: str) -> tuple[float, float]:
    t = read(rel)
    m = re.search(r"WNS\(ns\).*?\n\s*-+.*?\n\s*(-?[\d.]+)\s+\S+\s+\S+\s+\S+\s+(-?[\d.]+)", t)
    return float(m.group(1)), float(m.group(2))


def check(name: str, got, want) -> None:
    global bad
    ok = got == want
    bad += not ok
    print(f"{'OK  ' if ok else 'DIFF'} {name}: {got} (stated {want})")


h = {(v, r): hier(f"{v}/{r}/baseline_hierarchy.rpt") for v in ("base", "head") for r in ("ooc-1x1", "ooc-8x8", "route-1x1")}
check("route u_srp LUT (LUTRAM) / FF, base", h["base", "route-1x1"]["u_srp"], (4340, 180, 6263))
check("route u_srp LUT (LUTRAM) / FF, head", h["head", "route-1x1"]["u_srp"], (3711, 298, 3839))
check("1x1 u_srp LUT, base/head", (h["base", "ooc-1x1"]["u_srp"][0], h["head", "ooc-1x1"]["u_srp"][0]), (4558, 3988))
check("1x1 u_srp FF, base/head", (h["base", "ooc-1x1"]["u_srp"][2], h["head", "ooc-1x1"]["u_srp"][2]), (6438, 3979))
check("8x8 u_srp LUT, base/head", (h["base", "ooc-8x8"]["u_srp"][0], h["head", "ooc-8x8"]["u_srp"][0]), (8705, 7313))
check("8x8 u_srp FF, base/head", (h["base", "ooc-8x8"]["u_srp"][2], h["head", "ooc-8x8"]["u_srp"][2]), (11192, 7747))
check("1x1 top glue LUT/FF base", (h["base", "ooc-1x1"]["(u_srp)"][0], h["base", "ooc-1x1"]["(u_srp)"][2]), (907, 2836))
check("1x1 top glue LUT/FF head", (h["head", "ooc-1x1"]["(u_srp)"][0], h["head", "ooc-1x1"]["(u_srp)"][2]), (354, 545))
three = ("KL_srp_talker_fsm", "KL_srp_listener_fsm", "KL_srp_admission")
for shape, want in (("ooc-1x1", (-37, -168)), ("ooc-8x8", (-791, -762))):
    d = tuple(sum(h["head", shape][k][i] for k in three) - sum(h["base", shape][k][i] for k in three) for i in (0, 2))
    check(f"talker+listener+admission delta LUT/FF {shape}", d, want)
per = {}
for v in ("base", "head"):
    for k in three + ("u_srp",):
        per[v, k] = tuple(round((h[v, "ooc-8x8"][k][i] - h[v, "ooc-1x1"][k][i]) / 7) for i in (0, 2))
check("per source talker head", per["head", "KL_srp_talker_fsm"], (129, 168))
check("per source talker base", per["base", "KL_srp_talker_fsm"], (213, 221))
check("per sink listener head", per["head", "KL_srp_listener_fsm"], (208, 278))
check("per sink listener base", per["base", "KL_srp_listener_fsm"], (227, 278))
check("per source admission head", per["head", "KL_srp_admission"], (69, 69))
check("per source admission base", per["base", "KL_srp_admission"], (73, 101))
check("whole engine per pair head", per["head", "u_srp"], (475, 538))
check("whole engine per pair base", per["base", "u_srp"], (592, 679))
check("route WNS/WHS base", wns("base/route-1x1/baseline_timing.rpt"), (0.079, 0.014))
check("route WNS/WHS head", wns("head/route-1x1/baseline_timing.rpt"), (0.354, 0.036))
check("1x1 WNS estimate base/head", (wns("base/ooc-1x1/baseline_timing.rpt")[0], wns("head/ooc-1x1/baseline_timing.rpt")[0]), (-2.059, -1.874))
check("8x8 WNS estimate base/head", (wns("base/ooc-8x8/baseline_timing.rpt")[0], wns("head/ooc-8x8/baseline_timing.rpt")[0]), (-2.161, -1.495))
for v, want in (("base", 0), ("head", 0)):
    m = re.search(r"nets with routing errors\.+ :\s+(\d+)", read(f"{v}/route-1x1/alinx_ax7101_route_status.rpt"))
    check(f"route errors {v}", int(m.group(1)), want)


def util(rel: str, row: str) -> int:
    m = re.search(r"^\| " + re.escape(row) + r"\s+\|\s+([\d.]+)", read(rel), re.M)
    return float(m.group(1)) if "." in m.group(1) else int(m.group(1))


check("route LUT base/head", (util("base/route-1x1/baseline_utilization.rpt", "Slice LUTs"),
                              util("head/route-1x1/baseline_utilization.rpt", "Slice LUTs")), (51434, 51005))
check("route FF base/head", (util("base/route-1x1/baseline_utilization.rpt", "Slice Registers"),
                             util("head/route-1x1/baseline_utilization.rpt", "Slice Registers")), (59691, 57262))
check("route Slice base/head", (util("base/route-1x1/baseline_utilization.rpt", "Slice"),
                                util("head/route-1x1/baseline_utilization.rpt", "Slice")), (15847, 15837))
check("1x1 F7 mux delta", util("base/ooc-1x1/baseline_utilization.rpt", "F7 Muxes")
      - util("head/ooc-1x1/baseline_utilization.rpt", "F7 Muxes"), 296)
log = read("head/ooc-1x1/baseline.log")
fm = log[log.index("Distributed RAM: Final Mapping Report"):]
fm = fm[:fm.index("Finished ROM")]
for obj, want in (("tf_tk_ram_r_reg", "32 x 47 | RAM32M x 8"), ("tf_ls_ram_r_reg", "32 x 47 | RAM32M x 8"),
                  ("wtsp_r_reg", "2 x 68 | RAM32M x 12"), ("slope_q_r_reg", "2 x 32 | RAM32M x 6")):
    m = re.search(re.escape(obj) + r"\s+\|\s+[\w ]+\|\s+(\d+ x \d+)\s+\|\s+(RAM32M x \d+)", fm)
    check(f"1x1 head final mapping {obj}", f"{m.group(1)} | {m.group(2)}" if m else None, want)
print(f"{bad} differing")
sys.exit(1 if bad else 0)
