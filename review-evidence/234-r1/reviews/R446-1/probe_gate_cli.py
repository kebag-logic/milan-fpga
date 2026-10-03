#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
"""Reviewer probe: plant regressions through pp_resource_gate.py's own CLI.

Builds a measurement directory with the gate self-test's fixture (inputs side),
replaces its reports with Vivado-layout reports carrying the RECORDED route /
standalone figures of syn/ooc/pp_resource_baseline.json, records it with the
gate's own `record --write` into a temporary baseline that keeps the REAL
policy (tolerance, floor, ceiling) of that file, then plants one regression
per case and runs `pp_resource_gate.py check` as a subprocess.

Usage: probe_gate_cli.py <checkout>   (prints one line per case; exit 0 when
every case has the expected rc, 1 otherwise; expectations marked GAP are the
reviewer's view of what the documented contract requires).
"""

import copy
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile

ROOT = Path(sys.argv[1]).resolve()
OOC = ROOT / "syn/ooc"
sys.path.insert(0, str(OOC))
import pp_resource_gate_selftest as fx  # noqa: E402

REAL = json.loads((OOC / "pp_resource_baseline.json").read_text())

HEADER = ("Copyright 1986-2026 Xilinx, Inc. All Rights Reserved.\n"
          "---------------------------------------------------------------------------\n"
          "| Tool Version : Vivado v.2026.1 (lin64) Build 6511674 Tue Jun 16 11:01:26 MDT 2026\n"
          "| Date         : Sat Oct  3 09:00:00 2026\n"
          "| Host         : host running 64-bit Linux\n"
          "| Command      : report_utilization -file baseline_utilization.rpt\n"
          "| Design       : {design}\n"
          "| Device       : xc7a100tfgg484-2\n"
          "| Speed File   : -2\n"
          "| Design State : {state}\n"
          "---------------------------------------------------------------------------\n\n")


def row(label, value, avail, pct):
    return f"| {label:<42} | {value:>6} |     0 |          0 | {avail:>9} | {pct:>6} |\n"


def util_report(kind, f):
    design, state = ("alinx_ax7101", "Physopt postRoute") if kind == "route" else ("KL_pp_shadow", "Synthesized")
    star = "" if kind == "route" else "*"
    text = HEADER.format(design=design, state=state)
    text += "1. Slice Logic\n--------------\n\n+------+\n|  Site Type | Used | Fixed | Prohibited | Available | Util% |\n"
    text += row("Slice LUTs" + star, f["LUT"], 63400, "79.07")
    text += row("  LUT as Logic", f["LUT"] - 1242, 63400, "77.11")
    text += row("Slice Registers", f["FF"], 126800, "46.53")
    text += row("  Register as Flip Flop", f["FF"], 126800, "46.53")
    if kind == "route":
        text += "\n2. Slice Logic Distribution\n---------------------------\n\n"
        text += row("Slice", f["SLICE"], 15850, "99.78")
        text += row("  SLICEL", 10000, "", "")
        text += row("  LUT as Logic", f["LUT"] - 1242, 63400, "77.11")
        text += row("Slice Registers", f["FF"], 126800, "46.53")
    text += "\n3. Memory\n---------\n\n"
    text += row("Block RAM Tile", f["BRAM_TILE"], 135, "68.52")
    text += row("  RAMB36/FIFO*", f["RAMB36"], 135, "58.52")
    text += row("  RAMB18", f["RAMB18"], 270, "10.00")
    text += "\n4. DSP\n------\n\n"
    text += row("DSPs", f["DSP"], 240, "5.83")
    text += "\n7. Primitives\n-------------\n\n| FDRE | 58000 | Flop & Latch |\n| RAMB36E1 | 79 | Block Memory |\n"
    return text


def timing_report(wns, whs, endpoints=12345):
    return (HEADER.format(design="x", state="Routed").replace("report_utilization", "report_timing_summary")
            + "------------------------------------------------------------------------------------------------\n"
            "| Design Timing Summary\n| ---------------------\n"
            "------------------------------------------------------------------------------------------------\n\n"
            "    WNS(ns)      TNS(ns)  TNS Failing Endpoints  TNS Total Endpoints      WHS(ns)      THS(ns)"
            "  THS Failing Endpoints  THS Total Endpoints     WPWS(ns)     TPWS(ns)  TPWS Failing Endpoints"
            "  TPWS Total Endpoints  \n"
            "    -------      -------  ---------------------  -------------------      -------      -------"
            "  ---------------------  -------------------     --------     --------  ----------------------"
            "  --------------------  \n"
            f"    {wns:>7}        0.000                      0  {endpoints:>19}    {whs:>9}        0.000"
            f"                      0  {endpoints:>19}        3.000        0.000                       0"
            "                 50000  \n\n\nAll user specified timing constraints are met.\n")


def build(tmp: Path, kind: str, figures: dict, wns="0.063", whs="0.036"):
    folder = fx.fixture(tmp, kind)
    (folder / "baseline_utilization.rpt").write_text(util_report(kind, figures))
    (folder / "baseline_timing.rpt").write_text(timing_report(wns, whs))
    return folder


def gate(*args):
    r = subprocess.run([sys.executable, "-B", str(OOC / "pp_resource_gate.py"), *map(str, args)],
                       capture_output=True, text=True, timeout=120)
    return r.returncode, (r.stdout + r.stderr).strip().splitlines()


def edit(path: Path, old, new):
    text = path.read_text()
    if text.count(old) < 1:
        raise AssertionError(f"plant {old!r} not in {path}")
    path.write_text(text.replace(old, new))


def main():
    results, failures = [], 0
    with tempfile.TemporaryDirectory(prefix="r446-gate-probe-") as tmp:
        tmp = Path(tmp)
        cases = []
        for endpoint, kind in (("route-1x1", "route"), ("ooc-1x1", "ooc"), ("ooc-8x8", "ooc")):
            figs = REAL["endpoints"][endpoint]["record"]["figures"]
            base_dir = tmp / f"{endpoint}-pristine"
            base_dir.mkdir()
            folder = build(base_dir, kind, figs, "0.063" if kind == "route" else "-1.616",
                           "0.036" if kind == "route" else "0.159")
            baseline = tmp / f"{endpoint}.json"
            policy = copy.deepcopy(REAL)
            for name in list(policy["endpoints"]):
                if name != endpoint:
                    del policy["endpoints"][name]
            baseline.write_text(json.dumps(policy))
            rc, out = gate("record", folder, "--endpoint", endpoint, "--baseline", baseline, "--write")
            assert rc == 0, out
            rec = json.loads(baseline.read_text())["endpoints"][endpoint]
            assert rec["tolerance"] == REAL["endpoints"][endpoint]["tolerance"], "policy not preserved"
            assert rec["record"]["figures"]["LUT"] == figs["LUT"], "figures not parsed"
            cases.append((endpoint, kind, base_dir, baseline, figs))

        def probe(endpoint, kind, base_dir, baseline, figs, label, expect, plants, src=True, note=""):
            nonlocal failures
            arm = tmp / "arm"
            shutil.rmtree(arm, ignore_errors=True)
            shutil.copytree(base_dir, arm, symlinks=True)
            # fixture() embeds absolute paths of base_dir; rebase them in every text file
            for p in arm.rglob("*"):
                if p.is_file():
                    try:
                        p.write_text(p.read_text().replace(str(base_dir), str(arm)))
                    except UnicodeDecodeError:
                        pass
            folder = arm / ("gateware" if kind == "route" else "ooc")
            if src:
                edit(arm / "repo/hdl/milan/KL_pp_shadow.sv", "endmodule", "wire probe; endmodule")
            for plant in plants:
                plant(folder)
            rc, out = gate("check", folder, "--endpoint", endpoint, "--baseline", baseline)
            ok = rc == expect
            failures += 0 if ok else 1
            tail = next((l for l in out if "REGRESSION" in l or "NOT COMPARABLE" in l or "RESULT" in l
                         or "Error" in l or "error" in l), out[-1] if out else "")
            results.append(f"{'OK ' if ok else 'BAD'} {endpoint:<9} {label:<52} rc={rc} want={expect} {note}| {tail.strip()[:110]}")

        def util(figs, kind, **delta):
            f = dict(figs)
            f.update(delta)
            return lambda folder: (folder / "baseline_utilization.rpt").write_text(util_report(kind, f))

        def tim(wns, whs, endpoints=12345):
            return lambda folder: (folder / "baseline_timing.rpt").write_text(timing_report(wns, whs, endpoints))

        for endpoint, kind, base_dir, baseline, figs in cases:
            P = lambda label, expect, plants, **kw: probe(endpoint, kind, base_dir, baseline, figs, label, expect, plants, **kw)
            tol = REAL["endpoints"][endpoint]["tolerance"]
            P("control: inputs changed, figures equal", 0, [])
            P("control: inputs unchanged, figures equal", 0, [], src=False)
            for fig in ("LUT", "FF"):
                P(f"{fig} +{tol[fig]} (at tolerance)", 0, [util(figs, kind, **{fig: figs[fig] + tol[fig]})])
                P(f"{fig} +{tol[fig] + 1} (over tolerance)", 1, [util(figs, kind, **{fig: figs[fig] + tol[fig] + 1})])
                P(f"{fig} -5000 (improvement)", 0, [util(figs, kind, **{fig: figs[fig] - 5000})])
            for fig in ("RAMB36", "RAMB18", "DSP"):
                P(f"{fig} +1", 1, [util(figs, kind, **{fig: figs[fig] + 1})])
            P("same figures, identical inputs, LUT +1", 2, [util(figs, kind, LUT=figs["LUT"] + 1)], src=False)
            P("tool build changed", 2, [lambda f: edit(f / "baseline_utilization.rpt", "Build 6511674", "Build 6511999")])
            P("device changed", 2, [lambda f: edit(f / "baseline_utilization.rpt", "xc7a100tfgg484-2", "xc7a200tfbg484-2")])
            P("Design header changed", 2, [lambda f: edit(f / "baseline_utilization.rpt", "| Design       : ", "| Design       : other_")])
            P("Design State header changed", 2, [lambda f: edit(f / "baseline_utilization.rpt", "| Design State : ", "| Design State : Placed ")])
            script = fx.gate.SCRIPTS[kind]
            P("thread count 32 -> 8", 2, [lambda f: edit(f / script, "maxThreads 32", "maxThreads 8")])
            P("synthesis directive changed", 2, [lambda f: edit(f / script, "AreaOptimized_high", "Default")])
            P("missing utilization report", 2, [lambda f: (f / "baseline_utilization.rpt").unlink()])
            P("missing timing report", 2, [lambda f: (f / "baseline_timing.rpt").unlink()])
            P("missing hierarchy report", 2, [lambda f: (f / "baseline_hierarchy.rpt").unlink()])
            P("missing cell census", 2, [lambda f: (f / "baseline_cells.tsv").unlink()])
            P("missing image inventory", 2, [lambda f: (f / "baseline_images.json").unlink()])
            P("missing recipe script", 2, [lambda f: (f / script).unlink()])
            P("missing DSPs row", 2, [lambda f: edit(f / "baseline_utilization.rpt", "| DSPs", "| DSP_gone")])
            P("conflicting duplicate LUT row", 2, [lambda f: edit(f / "baseline_utilization.rpt", "| Slice LUTs", "| Slice LUTs | 1 | 0 |\n| Slice LUTs")])
            P("non-count used value 12.3", 2, [lambda f: edit(f / "baseline_utilization.rpt", f"| {figs['DSP']:>6} |", "|   12.3 |")])
            P("no Design Timing Summary", 2, [lambda f: edit(f / "baseline_timing.rpt", "| Design Timing Summary", "| Other Summary")])
            P("slack 'NA'", 2, [tim("NA", "NA")])
            if kind == "route":
                P(f"SLICE +{tol['SLICE']}", 0, [util(figs, kind, SLICE=figs["SLICE"] + tol["SLICE"])])
                P(f"SLICE +{tol['SLICE'] + 1}", 1, [util(figs, kind, SLICE=figs["SLICE"] + tol["SLICE"] + 1)])
                P("BRAM tiles 121.5 (at ceiling)", 0, [util(figs, kind, BRAM_TILE=121.5)])
                P("BRAM tiles 122 (over ceiling)", 1, [util(figs, kind, BRAM_TILE=122)])
                P("WNS +0.030 (at floor)", 0, [tim("0.030", "0.036")])
                P("WNS +0.029 (below floor)", 1, [tim("0.029", "0.036")])
                P("WHS 0.000 (at floor)", 0, [tim("0.063", "0.000")])
                P("WHS -0.001 (below floor)", 1, [tim("0.063", "-0.001")])
                P("WNS -2.000 (failing route)", 1, [tim("-2.000", "0.036")])
                P("GAP? unconstrained: WNS/WHS 'inf', 0 endpoints", 1, [tim("inf", "inf", 0)],
                  note="(Vivado prints inf when no path is constrained)")
                P("GAP? WNS 'nan'", 2, [tim("nan", "0.036")])
            else:
                P("standalone clock 10 ns", 2, [lambda f: (f / "clock.xdc").write_text(
                    "create_clock -period 10.000 -name clk [get_ports clk_i]\n")])
                P("standalone clock file missing", 2, [lambda f: (f / "clock.xdc").unlink()])
                P("standalone WNS -9.000 (not gated, documented)", 0, [tim("-9.000", "0.159")])
                P("Slice row present in OOC report (ignored)", 0, [])

        # CLI-level baseline handling
        endpoint, kind, base_dir, baseline, figs = cases[0]
        folder = base_dir / "gateware"

        def cli(label, expect, args, note=""):
            nonlocal failures
            rc, out = gate(*args)
            ok = rc == expect
            failures += 0 if ok else 1
            results.append(f"{'OK ' if ok else 'BAD'} cli       {label:<52} rc={rc} want={expect} {note}| {(out[-1] if out else '').strip()[:110]}")

        cli("unknown endpoint", 2, ["check", folder, "--endpoint", "route-9x9", "--baseline", baseline])
        cli("no command", 2, ["--baseline", baseline])
        cli("measurement directory absent", 2, ["check", tmp / "absent", "--endpoint", endpoint, "--baseline", baseline])
        cli("GAP? baseline file absent (doc: 1 = material regression)", 2, ["check", folder, "--endpoint", endpoint,
                                                                       "--baseline", tmp / "absent.json"])
        bad = tmp / "malformed.json"
        bad.write_text("{not json")
        cli("GAP? baseline JSON malformed", 2, ["check", folder, "--endpoint", endpoint, "--baseline", bad])
        broken = json.loads(baseline.read_text())
        del broken["endpoints"][endpoint]["tolerance"]["DSP"]
        bad.write_text(json.dumps(broken))
        cli("GAP? baseline lacks DSP tolerance: check", 2, ["check", folder, "--endpoint", endpoint, "--baseline", bad])
        cli("baseline lacks DSP tolerance: check-baseline", 2, ["check-baseline", "--baseline", bad])
        broken = json.loads(baseline.read_text())
        del broken["endpoints"][endpoint]["ceiling"]
        bad.write_text(json.dumps(broken))
        cli("GAP? route ceiling deleted: check-baseline", 2, ["check-baseline", "--baseline", bad],
            note="(policy says 121.5-tile ceiling)")
        broken = json.loads(baseline.read_text())
        broken["endpoints"][endpoint]["tolerance"]["LUT"] = 10 ** 9
        bad.write_text(json.dumps(broken))
        cli("GAP? LUT tolerance 1e9: check-baseline", 2, ["check-baseline", "--baseline", bad],
            note="(diff review is the documented control)")
        broken = json.loads(baseline.read_text())
        broken["endpoints"][endpoint]["ceiling"] = {"BRAM_TILES": 121.5}
        bad.write_text(json.dumps(broken))
        cli("GAP? ceiling names unknown figure: check-baseline", 2, ["check-baseline", "--baseline", bad])
        cli("real baseline: check-baseline", 0, ["check-baseline"])
    print("\n".join(results))
    print(f"probe_gate_cli: {len(results)} cases, {failures} not as expected (GAP? lines are reviewer expectations)")
    return 0 if failures == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
