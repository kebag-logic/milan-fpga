#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
"""Plant every regression and refusal the resource gate claims, end to end.

Each arm copies a synthetic recipe measurement directory, edits the report or
input text a real regression would change, reads it back through the gate's
own parser and judges it against a baseline recorded from the pristine copy.
No arm hands the comparator a hand-built record, so a parser that stops seeing
a row fails here exactly as it would on a real report. The command-line arms
drive the exit-code contract through main(): every unreadable measurement and
unusable baseline exits 2 with its reason, and only a regression exits 1. Each
malformed baseline goes through both check and check-baseline.
"""

import contextlib
import copy
import io
import json
from pathlib import Path
import shutil
import tempfile

import pp_resource_gate as gate


FIGURES = {"LUT": 1000, "FF": 2000, "SLICE": 400, "BRAM_TILE": 4.5, "RAMB36": 4, "RAMB18": 1, "DSP": 2}
POLICY = {"tolerance": {"LUT": 10, "FF": 10, "SLICE": 5, "RAMB36": 0, "RAMB18": 0, "DSP": 0,
                        "WNS_ns": 0.25, "WHS_ns": 0.25},
          "floor": {"WNS_ns": 0.03, "WHS_ns": 0.0}, "ceiling": {"BRAM_TILE": 5.0}}
OOC_POLICY = {"tolerance": {"LUT": 10, "FF": 10, "RAMB36": 0, "RAMB18": 0, "DSP": 0}}
#: The budget page's policy table for the two fixture endpoints, written by hand as the budget writes it.
#: The WNS floor is not zero, so a reader that drops floor cells reads a different policy.
BUDGET = ("# Area budget\n\nThe gate holds each endpoint to this table.\n\n"
          "| Endpoint | LUT | FF | Slice | RAMB36 | RAMB18 | DSP | WNS floor | WHS floor | Timing fall"
          " | BRAM tile ceiling |\n|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|\n"
          "| `route` | +10 | +10 | +5 | +0 | +0 | +0 | +0.030 ns | 0 ns | 0.25 ns | 5.0 |\n"
          "| `ooc` | +10 | +10 | - | +0 | +0 | +0 | - | - | - | - |\n\nProse after the table.\n")
LABELS = {"LUT": "Slice LUTs", "FF": "Slice Registers", "SLICE": "Slice", "BRAM_TILE": "Block RAM Tile",
          "RAMB36": "RAMB36/FIFO*", "RAMB18": "RAMB18", "DSP": "DSPs"}
#: The distribution table repeats the register row, as the vendor report does.
REPEATED = "| Slice Registers                            | 2000 |     0 |\n"
STATUS = "alinx_ax7101_route_status.rpt"
#: A complete route, laid out as report_route_status writes it.
COMPLETE = ("Design Route Status\n"
            "                                               :      # nets :\n"
            "   ------------------------------------------- : ----------- :\n"
            "   # of logical nets.......................... :         120 :\n"
            "       # of nets not needing routing.......... :          20 :\n"
            "           # of internally routed nets........ :          18 :\n"
            "           # of nets with no loads............ :           2 :\n"
            "       # of routable nets..................... :         100 :\n"
            "           # of fully routed nets............. :         100 :\n"
            "       # of nets with routing errors.......... :           0 :\n"
            "   ------------------------------------------- : ----------- :\n")


def report_header(design: str, state: str) -> str:
    """The vendor header block every report starts with."""
    return ("| Tool Version : Vivado v.2026.1 (lin64) Build 6511674 Tue Jun 16 11:01:26 MDT 2026\n"
            f"| Design       : {design}\n| Device       : xc7a100tfgg484-2\n"
            f"| Design State : {state}\n")


def write_reports(folder: Path, kind: str) -> None:
    """Write utilization, timing, hierarchy, cell census and route status as Vivado lays them out."""
    design = "alinx_ax7101" if kind == "route" else "KL_pp_shadow"
    rows = "".join(f"| {LABELS[name]:<20} | {value} | 0 | 0 | 9 | 1.0 |\n" for name, value in FIGURES.items()
                   if kind == "route" or name != "SLICE")
    (folder / "baseline_utilization.rpt").write_text(
        report_header(design, "Physopt postRoute" if kind == "route" else "Synthesized") + rows + REPEATED)
    (folder / "baseline_timing.rpt").write_text(
        report_header(design, "Synthesized") + "| Design Timing Summary\n| ---\n\n"
        "    WNS(ns)      TNS(ns)  TNS Failing Endpoints  TNS Total Endpoints      WHS(ns)      THS(ns)\n"
        "    -------      -------  ---------------------  -------------------      -------      -------\n"
        "      0.500        0.000                      0                   10        0.100        0.000\n")
    prefix = ["alinx_ax7101", "milan_datapath", "pp_shadow"] if kind == "route" else ["KL_pp_shadow"]
    lines = [f"| {'  ' * depth}{name} | m{depth} | {900 - depth} | {900 - depth} | 0 | 0 | 50 | 1 | 0 | 0 |"
             for depth, name in enumerate(prefix + ["u_pp", "u_srp"])]
    (folder / "baseline_hierarchy.rpt").write_text("\n".join(lines) + "\n")
    cells = "/".join(prefix[1:] + ["u_pp", "u_srp"])
    (folder / "baseline_cells.tsv").write_text(
        "cell\tprimitive\n" + "".join(f"{cells}/c{index}\tCARRY4\n" for index in range(3))
        + "top_carry\tCARRY4\ntop_lut\tLUT6\n")
    if kind == "route":
        (folder / STATUS).write_text(COMPLETE)


def fixture(root: Path, kind: str) -> Path:
    """Build a repository, a generated export and one measurement directory."""
    repo, gateware = root / "repo", root / "gateware"
    for folder in (repo / "hdl/milan", repo / "hdl/common", repo / "sw", gateware):
        folder.mkdir(parents=True)
    (repo / "hdl/milan/KL_pp_shadow.sv").write_text("module KL_pp_shadow; endmodule\n")
    (repo / "hdl/common/shape.svh").write_text("`define STREAMS 2\n")
    (repo / "sw/constraints.tcl").write_text("proc kl {} {}\n")
    (gateware / "alinx_ax7101.v").write_text(f"// Date : morning\nmodule alinx_ax7101; // {gateware}\n"
                                             f'localparam R = "{repo}/rom.hex";\nendmodule\n')
    (gateware / "alinx_ax7101.xdc").write_text("create_clock -period 20.000 [get_ports clk]\n")
    folder = gateware if kind == "route" else root / "ooc"
    folder.mkdir(exist_ok=True)
    script = ("create_project -force -name alinx_ax7101 -part xc7a100t-fgg484-2\n"
              "set_param general.maxThreads 32\n"
              f"read_verilog -v {{{repo}/hdl/milan/KL_pp_shadow.sv}}\n"
              f"read_verilog {{{gateware}/alinx_ax7101.v}}\n")
    if kind == "route":
        script += ("read_xdc alinx_ax7101.xdc\nsynth_design -directive AreaOptimized_high -top alinx_ax7101 "
                   f"-part xc7a100t-fgg484-2 -include_dirs {{{repo}/hdl/common}}\n"
                   f"source {{{repo}/sw/constraints.tcl}}\nopt_design -directive ExploreArea\n"
                   "kl_timing_grade_configure {xc7a100t-fgg484-2} {commercial} {0} {85} {Slow Fast}\n"
                   "place_design -directive ExtraPostPlacementOpt\nphys_opt_design -directive Explore\n"
                   "route_design -directive AggressiveExplore\n")
    else:
        (folder / "clock.xdc").write_text("create_clock -period 20.000 -name clk [get_ports clk_i]\n")
        script += ("read_xdc clock.xdc\nsynth_design -directive AreaOptimized_high -top KL_pp_shadow "
                   f"-part xc7a100t-fgg484-2 -include_dirs {{{repo}/hdl/common}} -mode out_of_context "
                   f'-generic {{N_STREAM_IN_P=2}} -generic {{UCODE_HEX_P="{repo}/ucode.hex"}}\n')
    (folder / gate.SCRIPTS[kind]).write_text(script)
    (folder / "baseline_images.json").write_text(json.dumps([{"path": f"{repo}/rom.hex", "sha256": "ab"}]))
    write_reports(folder, kind)
    return folder


def row(name: str, before: object, after: object) -> tuple[str, str, str]:
    """Plant one utilization row's used column."""
    return ("baseline_utilization.rpt", f"| {LABELS[name]:<20} | {before} |", f"| {LABELS[name]:<20} | {after} |")


SOURCE = ("{repo}/hdl/milan/KL_pp_shadow.sv", "endmodule", "wire w; endmodule")
TIMING = "baseline_timing.rpt"
VALUES = "      0.500        0.000                      0                   10        0.100        0.000\n"
FLOW = "baseline_integrated.tcl"
ERRORS = (STATUS, "errors.......... :           0", "errors.......... :           3")
ROUTABLE = "       # of routable nets..................... :         100 :\n"
ROUTED = "           # of fully routed nets............. :         100 :\n"
MANIFEST = ("baseline_images.json", None, '["a"]')
#: (label, plants, exit status, text the report must hold or (must hold, must not hold), policy edits)
ROUTE_ARMS = (
    ("unchanged control", (), 0, "RESULT: PASS"),
    ("changed source, unchanged figures", (SOURCE,), 0, "RESULT: PASS"),
    ("LUT growth at the tolerance", (SOURCE, row("LUT", 1000, 1010)), 0, "RESULT: PASS"),
    ("LUT growth over the tolerance", (SOURCE, row("LUT", 1000, 1011)), 1, "LUT"),
    ("FF growth over the tolerance", (SOURCE, row("FF", 2000, 2011),
                                      ("baseline_utilization.rpt", REPEATED, REPEATED.replace("2000", "2011"))),
     1, "FF"),
    ("register rows disagree", (SOURCE, row("FF", 2000, 2011)), 2, "Slice Registers"),
    ("Slice growth over the tolerance", (SOURCE, row("SLICE", 400, 406)), 1, "SLICE"),
    ("one more RAMB36", (SOURCE, row("RAMB36", 4, 5)), 1, "RAMB36"),
    ("one more RAMB18", (SOURCE, row("RAMB18", 1, 2)), 1, "RAMB18"),
    ("one more DSP", (SOURCE, row("DSP", 2, 3)), 1, "DSP"),
    ("BRAM tiles over the ceiling", (SOURCE, row("BRAM_TILE", 4.5, 5.5)), 1, "ceiling"),
    ("BRAM tiles at the ceiling", (SOURCE, row("BRAM_TILE", 4.5, 5)), 0, "RESULT: PASS"),
    ("WNS below the floor", (SOURCE, (TIMING, "  0.500  ", " -0.010  ")), 1, "below the floor"),
    ("WNS at the floor", (SOURCE, (TIMING, "  0.500  ", "  0.300  ")), 0, "RESULT: PASS",
     {"floor": {"WNS_ns": 0.3}}),
    ("WNS fell more than the tolerance", (SOURCE, (TIMING, "  0.500  ", "  0.200  ")), 1, "fell by"),
    ("WNS fell by exactly the tolerance", (SOURCE, (TIMING, "  0.500  ", "  0.250  ")), 0, "RESULT: PASS"),
    ("WNS fell within the tolerance", (SOURCE, (TIMING, "  0.500  ", "  0.300  ")), 0,
     ("RESULT: PASS", "re-baseline")),
    ("WHS below the floor", (SOURCE, (TIMING, "0.100", "-0.001")), 1, "WHS_ns"),
    ("WHS at the floor", (SOURCE, (TIMING, "0.100", "0.000")), 0, "RESULT: PASS"),
    ("WNS not a number", (SOURCE, (TIMING, "  0.500  ", "  nan  ")), 2, "not a finite decimal"),
    ("WHS not a number", (SOURCE, (TIMING, "0.100", "nan")), 2, "not a finite decimal"),
    ("WNS and WHS infinite", (SOURCE, (TIMING, "  0.500  ", "  inf  "), (TIMING, "0.100", "inf")),
     2, "not a finite decimal"),
    ("WNS in other digits", ((TIMING, "  0.500  ", "  \uff10.\uff15\uff10\uff10  "),), 2, "not a finite decimal"),
    ("no timed endpoint", (SOURCE, (TIMING, " 10 ", "  0 ")), 2, "times no endpoint"),
    ("timed endpoints in other digits", ((TIMING, " 10 ", " \uff11\uff10 "),), 2, "times no endpoint"),
    ("timing summary without its endpoint columns", (SOURCE, (TIMING, "TNS Total Endpoints", "TNS Other Endpoints")),
     2, "total endpoints []"),
    ("LUT improvement within the tolerance", (SOURCE, row("LUT", 1000, 990)), 0,
     ("below the baseline", "re-baseline")),
    ("LUT improvement beyond the tolerance", (SOURCE, row("LUT", 1000, 950)), 0, "re-baseline recommended: LUT"),
    ("WNS rise beyond the tolerance", (SOURCE, (TIMING, "  0.500  ", "  0.800  ")), 0,
     "re-baseline recommended: WNS_ns"),
    ("route status complete", (SOURCE,), 0, "route status: complete"),
    ("nets with routing errors", (SOURCE, ERRORS), 1, "ROUTE INCOMPLETE: 3 nets with routing errors"),
    ("unrouted nets", (SOURCE, (STATUS, "       # of nets with routing errors",
                                "           # of unrouted nets.............. :          37 :\n"
                                "       # of nets with routing errors")), 1, "37 unrouted nets"),
    ("routable nets not fully routed", (SOURCE, (STATUS, "routed nets............. :         100",
                                                 "routed nets............. :          99")),
     1, "99 of 100 routable nets fully routed"),
    ("route status report missing", (SOURCE, (STATUS, None, None)), 2, "route status report, found 0"),
    ("second route status report", (SOURCE, ("other_route_status.rpt", None, COMPLETE)), 2, "found 2"),
    ("route status without its error row", (SOURCE, (STATUS, "       # of nets with routing errors.......... :"
                                                     "           0 :\n", "")), 2, "'nets with routing errors' row"),
    ("route status count unreadable", (SOURCE, (STATUS, ":         120 :", ":        lots :")), 2, "not a count"),
    ("route status count a superscript", (SOURCE, ERRORS[:2] + ("errors.......... :           \u00b2",)),
     2, "not a count: '\u00b2'"),
    ("route status count in other digits", (SOURCE, ERRORS[:2] + ("errors.......... :           \uff10",)),
     2, "not a count: '\uff10'"),
    ("route status without its routable row", (SOURCE, (STATUS, ROUTABLE, "")), 2, "0 'routable nets' rows"),
    ("route status without its fully routed row", (SOURCE, (STATUS, ROUTED, "")), 2, "0 'fully routed nets' rows"),
    ("route status without both net rows", (SOURCE, (STATUS, ROUTABLE + ROUTED, "")), 2, "0 'routable nets' rows"),
    ("route status with a second routable row", (SOURCE, (STATUS, ROUTABLE, ROUTABLE * 2)),
     2, "2 'routable nets' rows"),
    ("tool build changed", (("baseline_utilization.rpt", "Build 6511674", "Build 6511675"),), 2, "tool"),
    ("device changed", (("baseline_utilization.rpt", "xc7a100tfgg484-2", "xc7a200tfbg484-2"),), 2, "device"),
    ("design changed", (("baseline_utilization.rpt", "| Design       : alinx_ax7101", "| Design       : other"),),
     2, "change in design"),
    ("design state changed", (("baseline_utilization.rpt", "Physopt postRoute", "Routed"),), 2, "change in state"),
    ("project creation changed", ((FLOW, "-name alinx_ax7101", "-name other"),), 2, "change in flow"),
    ("thread count changed", ((FLOW, "maxThreads 32", "maxThreads 16"),), 2, "change in flow"),
    ("synthesis directive changed", ((FLOW, "AreaOptimized_high", "Default"),), 2, "change in flow"),
    ("optimization directive changed", ((FLOW, "opt_design -directive ExploreArea", "opt_design -directive Default"),),
     2, "change in flow"),
    ("timing grade changed", ((FLOW, "{85}", "{100}"),), 2, "change in flow"),
    ("placement directive changed", ((FLOW, "ExtraPostPlacementOpt", "ExtraTimingOpt"),), 2, "change in flow"),
    ("physical optimization directive changed",
     ((FLOW, "phys_opt_design -directive Explore\n", "phys_opt_design -directive AggressiveFanoutOpt\n"),),
     2, "change in flow"),
    ("routing directive changed", ((FLOW, "AggressiveExplore", "NoTimingRelaxation"),), 2, "change in flow"),
    ("identical inputs, different figures", (row("LUT", 1000, 1001),), 2, "identical inputs"),
    ("identical inputs, different WNS", ((TIMING, "  0.500  ", "  0.400  "),), 2, "identical inputs"),
    ("export date only", (row("LUT", 1000, 1001), ("alinx_ax7101.v", "morning", "evening")), 2, "identical inputs"),
    ("generated logic changed", (row("LUT", 1000, 1011), ("alinx_ax7101.v", "endmodule", "wire g; endmodule")),
     1, "LUT"),
    ("include header changed", (row("LUT", 1000, 1011), ("{repo}/hdl/common/shape.svh", "2", "9")), 1, "LUT"),
    ("sourced constraint changed",
     (row("LUT", 1000, 1011), ("{repo}/sw/constraints.tcl", "proc kl", "proc kx")), 1, "LUT"),
    ("memory image changed", (row("LUT", 1000, 1011), ("baseline_images.json", '"ab"', '"cd"')), 1, "LUT"),
    ("image manifest of the wrong shape", (MANIFEST,), 2, "not a list of path and sha256"),
    ("image manifest nested too deep", ((MANIFEST[0], None, "[" * 100000 + "]" * 100000),), 2, "RecursionError"),
    ("duplicate conflicting row", (("baseline_utilization.rpt", "| DSPs", "| DSPs | 9 |\n| DSPs"),), 2, "DSPs"),
    ("duplicate conflicting header", (("baseline_utilization.rpt", "| Device       : xc7a100tfgg484-2\n",
                                       "| Device       : xc7a100tfgg484-2\n| Device       : xc7a200tfbg484-2\n"),),
     2, "'Device' appears 2 times"),
    ("malformed count", (row("SLICE", 400, "x"),), 2, "not a count"),
    ("count in other digits", (row("LUT", 1000, "\uff11\uff10\uff10\uff10"),), 2, "not a count"),
    ("fractional count", (row("SLICE", 400, "400.25"),), 2, "not a count"),
    ("missing Slice row", (("baseline_utilization.rpt", f"| {'Slice':<20} | 400 | 0 | 0 | 9 | 1.0 |\n", ""),),
     2, "'Slice' has values []"),
    ("timing columns changed", ((TIMING, "WHS(ns)", "WXS(ns)"),), 2, "columns"),
    ("second timing summary", ((TIMING, "| Design Timing Summary\n", "| Design Timing Summary\n" * 2),), 2,
     "found 2"),
    ("timing value row missing", ((TIMING, VALUES, ""),), 2, "has no WNS row"),
    ("missing timing report", ((TIMING, None, None),), 2, "baseline_timing.rpt"),
    ("second generated top", ((FLOW, "read_xdc alinx_ax7101.xdc\n", "read_xdc alinx_ax7101.xdc\n"
                               "read_verilog alinx_ax7101.v\n"),), 2, "exactly one generated top"),
    ("read source missing", (("{repo}/sw/constraints.tcl", None, None),), 2, "read source is missing"),
    ("include directory missing", ((FLOW, "/hdl/common}", "/hdl/absent}"),), 2, "include directory is missing"),
    ("cell census header changed", (("baseline_cells.tsv", "cell\tprimitive", "cell\tref"),), 2, "header changed"),
    ("hierarchy count in other digits", (("baseline_hierarchy.rpt", "| m0 | 900 |", "| m0 | \uff19\uff10\uff10 |"),),
     2, "not a row of counts"),
    ("hierarchy row without counts", (("baseline_hierarchy.rpt", "| m4 | 896 |", "| m4 | n/a |"),),
     2, "not a row of counts"),
    ("wrapper source read from too near the root",
     ((FLOW, "/hdl/milan/KL_pp_shadow.sv}\n", "/hdl/milan/KL_pp_shadow.sv}\nread_verilog {/milan/KL_pp_shadow.sv}\n"),),
     2, "read source is missing: /milan/KL_pp_shadow.sv"),
    ("second recipe script", (("baseline_ooc.tcl", None, "quit\n"),), 2, "recipe scripts"),
)
OOC_ARMS = (
    ("standalone control", (), 0, ("RESULT: PASS", "route status")),
    ("standalone clock changed", (("clock.xdc", "20.000", "10.000"),), 2, "standalone_clock_ns"),
    ("generic changed", (row("LUT", 1000, 1011), ("baseline_ooc.tcl", "N_STREAM_IN_P=2", "N_STREAM_IN_P=9")),
     1, "LUT"),
    ("image path moved, same image", (row("LUT", 1000, 1001), ("baseline_ooc.tcl", "/ucode.hex", "/x/ucode.hex")),
     2, "identical inputs"),
    ("standalone RAMB36", (SOURCE, row("RAMB36", 4, 5)), 1, "RAMB36"),
    ("standalone RAMB18", (SOURCE, row("RAMB18", 1, 2)), 1, "RAMB18"),
    ("standalone DSP", (SOURCE, row("DSP", 2, 3)), 1, "DSP"),
    ("standalone FF", (SOURCE, row("FF", 2000, 2011),
                       ("baseline_utilization.rpt", REPEATED, REPEATED.replace("2000", "2011"))), 1, "FF"),
)


#: The policy table rows of BUDGET: its head, separator, route row and standalone row.
TABLE = BUDGET.split("\n")[4:8]
#: Commands through main(): (label, measurement kind, plants, baseline file, exit status, text the output holds).
#: The baseline file is the recorded one (None), raw text, an edit of its endpoints, an (old, new) edit of the
#: recorded file's text, or an absent path.
CHECK_ARMS = (
    ("check within tolerance", "route", (SOURCE,), None, 0, "RESULT: PASS"),
    ("check reads the kind from a standalone directory", "ooc", (), None, 0, "RESULT: PASS"),
    ("check of a regression", "route", (row("LUT", 1000, 1011), ("baseline_images.json", '"ab"', '"cd"')), None,
     1, "MATERIAL REGRESSION"),
    ("check of an unrouted route", "route", (SOURCE, ERRORS), None, 1, "ROUTE INCOMPLETE"),
    ("check of an unreadable measurement", "route", ((TIMING, None, None),), None,
     2, "NOT COMPARABLE: unreadable measurement"),
    ("check of a route without its status", "route", ((STATUS, None, None),), None,
     2, "NOT COMPARABLE: expected one"),
    ("check of a wrong-shape image manifest", "route", (MANIFEST,), None, 2, "not a list of path and sha256"),
    ("check against a baseline that is not JSON", "route", (SOURCE,), "{not json", 2, "is unreadable"),
    ("check against a missing baseline", "route", (SOURCE,), Path("absent.json"), 2, "is unreadable"),
    ("check against a baseline without endpoints", "route", (SOURCE,), "[]", 2, "holds no endpoints table"),
    ("check of an endpoint without a record", "route", (SOURCE,), lambda ends: ends["route"].pop("record"),
     2, "route: has no record"),
    ("check of a gated figure without a tolerance", "route", (SOURCE,),
     lambda ends: ends["route"]["tolerance"].pop("LUT"), 2, "LUT has no non-negative tolerance"),
    ("check of a ceiling naming no figure", "route", (SOURCE,),
     lambda ends: ends["route"]["ceiling"].update({"BRAM_TILES": 5.0}), 2, "not a recorded figure"),
)
#: check-baseline through main(): (label, edit of the recorded endpoints or None, budget page: BUDGET (None),
#: a rewrite of it, or an absent path, exit status, text the output holds).
AUDIT_ARMS = (
    ("a consistent baseline", None, None, 0, "baseline PASS: 2 endpoints"),
    ("a missing record", lambda ends: ends["route"].pop("record"), None, 2, "route: has no record"),
    ("an incomplete record", lambda ends: ends["route"]["record"].pop("scopes"), None, 2, "the record lacks scopes"),
    ("a missing tolerance", lambda ends: ends["route"]["tolerance"].pop("LUT"), None,
     2, "LUT has no non-negative tolerance"),
    ("a negative tolerance", lambda ends: ends["route"]["tolerance"].update({"DSP": -1}), None,
     2, "DSP has no non-negative tolerance"),
    ("a missing floor", lambda ends: ends["route"]["floor"].pop("WNS_ns"), None, 2, "WNS_ns has no floor"),
    ("a record below its floor", lambda ends: ends["route"]["floor"].update({"WHS_ns": 1.0}), None,
     2, "WHS_ns is below its floor"),
    ("a record over its ceiling", lambda ends: ends["route"]["ceiling"].update({"BRAM_TILE": 1.0}), None,
     2, "BRAM_TILE exceeds its ceiling"),
    ("a missing route ceiling", lambda ends: ends["route"].pop("ceiling"), None, 2, "BRAM_TILE has no ceiling"),
    ("a ceiling naming no figure", lambda ends: ends["route"]["ceiling"].update({"BRAM_TILES": 5.0}), None,
     2, "not a recorded figure"),
    ("a malformed policy", lambda ends: ends["route"].update({"tolerance": [10]}), None,
     2, "route: tolerance is not a table of figures"),
    ("a tolerance the budget does not hold", lambda ends: ends["route"]["tolerance"].update({"LUT": 10 ** 9}), None,
     2, "tolerance LUT is 1000000000 in the baseline and 10.0 in the budget table"),
    ("a budget value the baseline does not hold", None, lambda page: page.replace("+5 |", "+6 |"),
     2, "tolerance SLICE is 5 in the baseline and 6.0 in the budget table"),
    ("a budget floor the baseline does not hold", None, lambda page: page.replace("+0.030 ns", "+0.040 ns"),
     2, "floor WNS_ns is 0.03 in the baseline and 0.04 in the budget table"),
    ("a budget ceiling the baseline does not hold", None, lambda page: page.replace("| 5.0 |", "| 6.0 |"),
     2, "ceiling BRAM_TILE is 5.0 in the baseline and 6.0 in the budget table"),
    ("a baseline policy figure the budget table lacks", lambda ends: ends["route"]["ceiling"].update({"LUT": 2000}),
     None, 2, "ceiling LUT is 2000 in the baseline and None in the budget table"),
    ("a budget cell in other digits", None, lambda page: page.replace("| +5 |", "| +\uff15 |"), 2, "neither a value"),
    ("an endpoint the budget lacks", None, lambda page: page.replace("| `ooc` |", "Not a row: `ooc` |"),
     2, "ooc: only the baseline names it"),
    ("a budget row the baseline lacks", lambda ends: ends.pop("ooc"), None, 2, "ooc: only the budget table names it"),
    ("no budget table", None, lambda page: page.replace(TABLE[0], "Prose."), 2, "holds 0 resource-gate policy tables"),
    ("two budget tables", None, lambda page: page + "\n" + "\n".join(TABLE), 2, "holds 2 resource-gate policy tables"),
    ("a repeated budget row", None, lambda page: page.replace("| `ooc` |", TABLE[2] + "\n| `ooc` |"),
     2, "malformed or repeated"),
    ("a budget cell that is no value", None, lambda page: page.replace("| +5 |", "| five |"), 2, "neither a value"),
    ("no budget page", None, Path("absent.md"), 2, "budget absent.md"),
)
#: Baselines not of the recorded shape: (label, baseline file as in CHECK_ARMS, text the refusal holds). check and
#: check-baseline both refuse each one with exit 2 before reading any field of it.
MALFORMED = (
    ("a NaN floor", lambda ends: ends["route"]["floor"].update({"WNS_ns": float("nan")}),
     "the number NaN is not finite"),
    ("an infinite tolerance", lambda ends: ends["route"]["tolerance"].update({"LUT": float("inf")}),
     "the number Infinity is not finite"),
    ("a ceiling too large to be finite", ('"BRAM_TILE": 5.0}', '"BRAM_TILE": 5e999}'),
     "the number 5e999 is not finite"),
    ("a file nested too deep to read", "[" * 100000 + "]" * 100000, "is unreadable"),
    ("an unknown field in the file", ('{"endpoints": ', '{"note": "x", "endpoints": '), "unknown fields note"),
    ("an unknown field in an endpoint", lambda ends: ends["route"].update({"ceilings": {}}), "unknown fields ceilings"),
    ("a record kind that is a list", lambda ends: ends["route"]["record"].update({"kind": ["route"]}),
     "kind ['route'] is not one of"),
    ("an unknown record kind", lambda ends: ends["route"]["record"].update({"kind": "tile"}),
     "kind 'tile' is not one of"),
    ("an identity that is text", lambda ends: ends["route"]["record"].update({"identity": "Vivado"}),
     "identity does not hold exactly"),
    ("an identity without its device", lambda ends: ends["route"]["record"]["identity"].pop("device"),
     "identity does not hold exactly"),
    ("an identity field of another type", lambda ends: ends["route"]["record"]["identity"].update({"tool": 7}),
     "not of its recorded type"),
    ("a flow that is not text", lambda ends: ends["route"]["record"]["identity"].update({"flow": [1]}),
     "not a list of text"),
    ("an input digest that is no digest", lambda ends: ends["route"]["record"].update({"inputs_sha256": "ab"}),
     "not a sha256 hex digest"),
    ("figures that are a list", lambda ends: ends["route"]["record"].update({"figures": []}),
     "figures are not exactly"),
    ("figures without LUT", lambda ends: ends["route"]["record"]["figures"].pop("LUT"), "figures are not exactly"),
    ("a gated figure that is text", lambda ends: ends["route"]["record"]["figures"].update({"LUT": "1000"}),
     "recorded figure is not a finite number"),
    ("a gated figure that is null", lambda ends: ends["route"]["record"]["figures"].update({"WNS_ns": None}),
     "recorded figure is not a finite number"),
    ("a gated figure that is a bool", lambda ends: ends["route"]["record"]["figures"].update({"DSP": True}),
     "recorded figure is not a finite number"),
    ("scopes that are a list", lambda ends: ends["route"]["record"].update({"scopes": []}),
     "scopes are not a table"),
    ("a scope without its CARRY4 count", lambda ends: ends["route"]["record"]["scopes"]["wrapper"].pop("CARRY4"),
     "scopes are not a table"),
    ("a fractional scope count", lambda ends: ends["route"]["record"]["scopes"]["u_pp/u_srp"].update({"LUT": 1.5}),
     "sub-block count is not a non-negative whole number"),
    ("a negative scope count", lambda ends: ends["route"]["record"]["scopes"]["u_pp/u_srp"].update({"FF": -1}),
     "sub-block count is not a non-negative whole number"),
    ("a tolerance that is text", lambda ends: ends["route"]["tolerance"].update({"LUT": "10"}),
     "a tolerance value is not a finite number"),
    ("a ceiling that is a bool", lambda ends: ends["route"]["ceiling"].update({"BRAM_TILE": True}),
     "a ceiling value is not a finite number"),
    ("a floor table that is a list", lambda ends: ends["route"].update({"floor": [0]}), "floor is not a table"),
)


def fresh(root: Path, kind: str) -> Path:
    """Recreate the arm tree from the pristine copy and name its measurement directory."""
    shutil.rmtree(root / "arm", ignore_errors=True)
    shutil.copytree(root / "pristine", root / "arm", symlinks=True)
    return root / "arm" / ("gateware" if kind == "route" else "ooc")


def plant(folder: Path, name: str, old: str | None, new: str | None) -> None:
    """Edit exactly one occurrence, delete a file (both None) or create one (old None)."""
    path = Path(name) if name.startswith("/") else folder / name
    if old is None:
        if new is None:
            path.unlink()
        else:
            path.write_text(new)
        return
    text = path.read_text()
    if text.count(old) != 1:
        raise AssertionError(f"plant {old!r} is not unique in {path}")
    path.write_text(text.replace(old, new))


def expect(where: str, status: int, lines: list[str], wanted: int, needle: str | tuple[str, str]) -> None:
    """Require an exit status and a report holding one text and, when given, lacking another."""
    held, absent = (needle, None) if isinstance(needle, str) else needle
    report = "\n".join(lines)
    if status != wanted or held not in report or (absent is not None and absent in report):
        raise AssertionError(f"{where}: exit {status}, wanted {wanted} naming {held!r}"
                             + (f" and not {absent!r}" if absent else "") + "\n" + report)


def run_arm(root: Path, kind: str, arm: tuple, entry: dict) -> None:
    """Plant one arm on a fresh copy and require its exact verdict and reason."""
    label, plants, wanted, needle, *edits = arm
    entry = copy.deepcopy(entry)
    for field, values in (edits[0] if edits else {}).items():
        entry[field].update(values)
    folder = fresh(root, kind)
    for name, old, new in plants:
        plant(folder, name.replace("{repo}", str(root / "arm/repo")), old, new)
    try:
        candidate = gate.record(folder, gate.kind_of(folder))
        status, lines = gate.judge(entry, candidate, gate.routing(folder, candidate["kind"]))
    except gate.Refusal as error:
        status, lines = 2, [str(error)]
    except Exception as error:  # an exception the gate lets escape fails the arm by name
        status, lines = -1, [f"escaped {type(error).__name__}: {error}"]
    expect(f"{kind} arm {label!r}", status, lines, wanted, needle)
    print(f"resource gate {kind} arm: {label}: exit {status} PASS")


def recorded(root: Path, kind: str) -> dict:
    """Build the fixture where arms are planted, record it, then keep it pristine."""
    folder = fixture(root / "arm", kind)
    entry = copy.deepcopy(POLICY if kind == "route" else OOC_POLICY)
    entry["record"] = gate.record(folder, kind)
    (root / "arm").rename(root / "pristine")
    return entry


def relocated_arm(root: Path, entry: dict) -> None:
    """The same export measured at another build root has the same inputs, so a moved figure is refused."""
    moved = root / "moved"
    shutil.copytree(root / "pristine", moved, symlinks=True)
    for path in moved.rglob("*"):
        if path.is_file():
            path.write_text(path.read_text().replace(str(root / "arm"), str(moved)))
    folder = moved / "gateware"
    plant(folder, *row("LUT", 1000, 1001))
    status, lines = gate.judge(entry, gate.record(folder, "route"), gate.routing(folder, "route"))
    expect("route arm 'export built at another root'", status, lines, 2, "identical inputs")
    print(f"resource gate route arm: export built at another root: exit {status} PASS")


def cli(*argv: object) -> tuple[int, list[str]]:
    """Run the gate's command line in process; an escaped exception is a traceback, never an exit status."""
    out = io.StringIO()
    try:
        with contextlib.redirect_stdout(out):
            status = gate.main([str(arg) for arg in argv])
    except Exception as error:  # the contract is an exit status with a reason, so this fails the arm
        return -1, [*out.getvalue().splitlines(), f"escaped {type(error).__name__}: {error}"]
    return status, out.getvalue().splitlines()


def baseline_file(tmp: Path, entries: dict, data: object) -> Path:
    """Write the baseline an arm's command reads: as recorded, edited or raw text; or name an absent file."""
    if isinstance(data, Path):
        return tmp / data
    path = tmp / "baseline.json"
    if isinstance(data, str):
        path.write_text(data)
        return path
    baseline = copy.deepcopy({"endpoints": entries})
    if callable(data):
        data(baseline["endpoints"])
    text = json.dumps(baseline)
    if isinstance(data, tuple):
        if text.count(data[0]) != 1:
            raise AssertionError(f"baseline edit {data[0]!r} is not unique")
        text = text.replace(*data)
    path.write_text(text)
    return path


def budget_file(tmp: Path, page: object) -> Path:
    """Write the budget page an arm's check-baseline reads, or name an absent one."""
    if isinstance(page, Path):
        return tmp / page
    path = tmp / "budget.md"
    path.write_text(BUDGET if page is None else page(BUDGET))
    return path


def plant_source(tmp: Path) -> Path:
    """A route measurement of a changed source with unchanged figures: within tolerance against the record."""
    folder = fresh(tmp / "route", "route")
    plant(folder, SOURCE[0].replace("{repo}", str(tmp / "route/arm/repo")), *SOURCE[1:])
    return folder


def command_line_arms(tmp: Path, entries: dict) -> int:
    """Drive the exit-code contract and check-baseline through main(); return the arm count."""
    if entries["route"]["record"]["scopes"]["u_pp/u_srp"]["CARRY4"] != 3 \
            or entries["route"]["record"]["figures"]["CARRY4"] != 4:
        raise AssertionError(f"CARRY4 attribution wrong: {entries['route']['record']}")
    for label, kind, plants, data, wanted, needle in CHECK_ARMS:
        folder = fresh(tmp / kind, kind)
        for name, old, new in plants:
            plant(folder, name.replace("{repo}", str(tmp / kind / "arm/repo")), old, new)
        status, lines = cli("check", folder, "--endpoint", kind, "--baseline", baseline_file(tmp, entries, data))
        expect(f"command-line arm {label!r}", status, lines, wanted, needle)
        print(f"resource gate command-line arm: {label}: exit {status} PASS")
    for label, data, page, wanted, needle in AUDIT_ARMS:
        status, lines = cli("check-baseline", "--baseline", baseline_file(tmp, entries, data),
                            "--budget", budget_file(tmp, page))
        expect(f"check-baseline arm {label!r}", status, lines, wanted, needle)
        print(f"resource gate check-baseline arm: {label}: exit {status} PASS")
    for label, data, needle in MALFORMED:
        path = baseline_file(tmp, entries, data)
        status, lines = cli("check", plant_source(tmp), "--endpoint", "route", "--baseline", path)
        expect(f"malformed-baseline arm {label!r} through check", status, lines, 2, needle)
        status, lines = cli("check-baseline", "--baseline", path, "--budget", budget_file(tmp, None))
        expect(f"malformed-baseline arm {label!r} through check-baseline", status, lines, 2, needle)
        print(f"resource gate malformed-baseline arm: {label}: exit 2 through check and check-baseline PASS")
    path = baseline_file(tmp, entries, None)
    status, _ = cli("record", fresh(tmp / "route", "route"), "--endpoint", "copy", "--baseline", path, "--write")
    if status != 0 or json.loads(path.read_text())["endpoints"]["copy"]["record"] != entries["route"]["record"]:
        raise AssertionError(f"record --write exited {status} or wrote a different record")
    print("resource gate CARRY4 attribution and record --write PASS")
    return len(CHECK_ARMS) + len(AUDIT_ARMS) + 2 * len(MALFORMED) + 2


def selftest() -> int:
    """Run every arm; return 0 only when each one produced its expected verdict."""
    count, entries = 0, {}
    with tempfile.TemporaryDirectory(prefix="pp-resource-gate-") as tmp:
        for kind, arms in (("route", ROUTE_ARMS), ("ooc", OOC_ARMS)):
            root = Path(tmp) / kind
            root.mkdir()
            entries[kind] = recorded(root, kind)
            for arm in arms:
                run_arm(root, kind, arm, entries[kind])
            count += len(arms)
        relocated_arm(Path(tmp) / "route", entries["route"])
        count += 1 + command_line_arms(Path(tmp), entries)
        status, lines = gate.judge(entries["route"], entries["ooc"]["record"], [])
        if status != 2 or "endpoint kind" not in lines[0]:
            raise AssertionError("a standalone record was compared with an integrated baseline")
        count += 1
    print(f"resource gate selftest: {count} arms PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(selftest())
