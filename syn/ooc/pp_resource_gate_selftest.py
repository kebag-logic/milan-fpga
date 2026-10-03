#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
"""Plant every regression and refusal the resource gate claims, end to end.

Each arm copies a synthetic recipe measurement directory, edits the report or input text a real regression would change,
reads it back through the gate's own parser and judges it against a baseline recorded from the pristine copy. No arm
hands the comparator a hand-built record, so a parser that stops seeing a row fails here exactly as it would on a real
report. The command-line arms drive the exit-code contract through main() into a stream that takes ASCII only: every
unreadable measurement and unusable baseline exits 2 with its reason, only a regression exits 1, and an exception
planted inside the gate exits 2. Each malformed baseline goes through both check and check-baseline. mutate_json() and
mutate_report() generate the cases the gate's fuzz() runs: random changes to a baseline and to a measurement's reports,
each knowing whether it breaks a shape the gate documents.
"""

from collections.abc import Callable
import contextlib
import copy
import io
import json
import locale
from pathlib import Path
import random
import re
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
#: The image manifest's (name, sha256) entries: three, so that a key can sit in an entry past the first.
IMAGES = (("rom", "ab"), ("ram", "e0"), ("table", "ef"))
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
            f"| Design       : {design}\n| Device       : xc7a100tfgg484-2\n| Design State : {state}\n")


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
    script = ("create_project -force -name alinx_ax7101 -part xc7a100t-fgg484-2\nset_param general.maxThreads 32\n"
              f"read_verilog -v {{{repo}/hdl/milan/KL_pp_shadow.sv}}\nread_verilog {{{gateware}/alinx_ax7101.v}}\n")
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
    (folder / "baseline_images.json").write_text(json.dumps([{"path": f"{repo}/{name}.hex", "sha256": digest}
                                                             for name, digest in IMAGES]))
    write_reports(folder, kind)
    return folder


def row(name: str, before: object, after: object) -> tuple[str, str, str]:
    """Plant one utilization row's used column."""
    return ("baseline_utilization.rpt", f"| {LABELS[name]:<20} | {before} |", f"| {LABELS[name]:<20} | {after} |")


def at(tree: object, path: tuple) -> object:
    """The value at a path of a JSON tree."""
    for key in path:
        tree = tree[key]
    return tree


#: The value edit() is given to remove a key rather than put one.
REMOVE = object()


def edit(*keys: str, value: object = REMOVE) -> Callable[[dict], None]:
    """An edit of the recorded endpoints: put the value at the keys, or remove the last key when none is given."""
    def apply(ends: dict) -> None:
        """Make the edit."""
        held = at(ends, keys[:-1])
        if value is REMOVE:
            del held[keys[-1]]
        else:
            held[keys[-1]] = value
    return apply


SOURCE = ("{repo}/hdl/milan/KL_pp_shadow.sv", "endmodule", "wire w; endmodule")
TIMING = "baseline_timing.rpt"
VALUES = "      0.500        0.000                      0                   10        0.100        0.000\n"
FLOW = "baseline_integrated.tcl"
ERRORS = (STATUS, "errors.......... :           0", "errors.......... :           3")
ERROR_ROW = "       # of nets with routing errors.......... :           0 :\n"
ROUTABLE = "       # of routable nets..................... :         100 :\n"
ROUTED = "           # of fully routed nets............. :         100 :\n"
GROWN_FF = (row("FF", 2000, 2011), ("baseline_utilization.rpt", REPEATED, REPEATED.replace("2000", "2011")))
MANIFEST = ("baseline_images.json", None, '["a"]')
HIERARCHY = "baseline_hierarchy.rpt"
TOP_ROW = "| m0 | 900 | 900 | 0 | 0 | 50 | 1 | 0 | 0 |"
#: A number too long to be finite as a float, and one past the integer bound.
LONG, BOUND = "1" + "0" * 400, "1" * 16
#: (label, plants, exit status, text the report must hold or (must hold, must not hold), policy edits)
ROUTE_ARMS = (
    ("unchanged control", (), 0, "RESULT: PASS"),
    ("changed source, unchanged figures", (SOURCE,), 0, "RESULT: PASS"),
    ("LUT growth at the tolerance", (SOURCE, row("LUT", 1000, 1010)), 0, "RESULT: PASS"),
    ("LUT growth over the tolerance", (SOURCE, row("LUT", 1000, 1011)), 1, "LUT"),
    ("FF growth over the tolerance", (SOURCE, *GROWN_FF), 1, "FF"),
    ("register rows disagree", (SOURCE, row("FF", 2000, 2011)), 2, "Slice Registers"),
    ("Slice growth over the tolerance", (SOURCE, row("SLICE", 400, 406)), 1, "SLICE"),
    ("one more RAMB36", (SOURCE, row("RAMB36", 4, 5)), 1, "RAMB36"),
    ("one more RAMB18", (SOURCE, row("RAMB18", 1, 2)), 1, "RAMB18"),
    ("one more DSP", (SOURCE, row("DSP", 2, 3)), 1, "DSP"),
    ("BRAM tiles over the ceiling", (SOURCE, row("BRAM_TILE", 4.5, 5.5)), 1, "ceiling"),
    ("BRAM tiles at the ceiling", (SOURCE, row("BRAM_TILE", 4.5, 5)), 0, "RESULT: PASS"),
    ("WNS below the floor", (SOURCE, (TIMING, "  0.500  ", " -0.010  ")), 1, "below the floor"),
    ("WNS at the floor", (SOURCE, (TIMING, "  0.500  ", "  0.300  ")), 0, "RESULT: PASS", {"floor": {"WNS_ns": 0.3}}),
    ("WNS fell more than the tolerance", (SOURCE, (TIMING, "  0.500  ", "  0.200  ")), 1, "fell by"),
    ("WNS fell by exactly the tolerance", (SOURCE, (TIMING, "  0.500  ", "  0.250  ")), 0, "RESULT: PASS"),
    ("WNS fell within the tolerance", (SOURCE, (TIMING, "  0.500  ", "  0.300  ")), 0, ("RESULT: PASS", "re-baseline")),
    ("WHS below the floor", (SOURCE, (TIMING, "0.100", "-0.001")), 1, "WHS_ns"),
    ("WHS at the floor", (SOURCE, (TIMING, "0.100", "0.000")), 0, "RESULT: PASS"),
    ("WNS not a number", (SOURCE, (TIMING, "  0.500  ", "  nan  ")), 2, "not a finite decimal"),
    ("WHS not a number", (SOURCE, (TIMING, "0.100", "nan")), 2, "not a finite decimal"),
    ("WNS and WHS infinite", (SOURCE, (TIMING, "  0.500  ", "  inf  "), (TIMING, "0.100", "inf")),
     2, "not a finite decimal"),
    ("WNS in other digits", ((TIMING, "  0.500  ", "  \uff10.\uff15\uff10\uff10  "),), 2, "not a finite decimal"),
    ("WNS too long to be finite", (SOURCE, (TIMING, "  0.500  ", f"  {LONG}.063  ")), 2, "WNS is not finite"),
    ("WHS too long to be finite", (SOURCE, (TIMING, "0.100", f"{LONG}.036")), 2, "WHS is not finite"),
    ("no timed endpoint", (SOURCE, (TIMING, " 10 ", "  0 ")), 2, "times no endpoint"),
    ("no hold-timed endpoint", (SOURCE, (TIMING, "THS(ns)\n", "THS(ns)  THS Total Endpoints\n"),
                                (TIMING, "        0.000\n", "        0.000                    0\n")),
     2, "times no endpoint"),
    ("timed endpoints in other digits", ((TIMING, " 10 ", " \uff11\uff10 "),), 2,
     "TNS Total Endpoints is not a whole number of 1 to 15 ASCII digits: '\\uff11\\uff10'"),
    ("timed endpoints past the bound", (SOURCE, (TIMING, " 10 ", f" {BOUND} ")), 2,
     "TNS Total Endpoints is not a whole number of 1 to 15 ASCII digits"),
    ("timing summary without its endpoint columns", (SOURCE, (TIMING, "TNS Total Endpoints", "TNS Other Endpoints")),
     2, "total endpoints []"),
    ("WNS without a fraction", (SOURCE, (TIMING, "  0.500  ", "  1  ")), 2, "not a finite decimal"),
    ("LUT improvement within the tolerance", (SOURCE, row("LUT", 1000, 990)), 0, ("below the baseline", "re-baseline")),
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
    ("route status without its error row", (SOURCE, (STATUS, ERROR_ROW, "")), 2, "'nets with routing errors' row"),
    ("route status with a second error row", (SOURCE, (STATUS, ERROR_ROW, ERROR_ROW * 2)), 2,
     "no single 'nets with routing errors' row"),
    ("route status count unreadable", (SOURCE, (STATUS, ":         120 :", ":        lots :")), 2,
     "'logical nets' is not a whole number of 1 to 15 ASCII digits: 'lots'"),
    ("route status count a superscript", (SOURCE, ERRORS[:2] + ("errors.......... :           \u00b2",)),
     2, "is not a whole number of 1 to 15 ASCII digits: '\\xb2'"),
    ("route status count in other digits", (SOURCE, ERRORS[:2] + ("errors.......... :           \uff10",)),
     2, "is not a whole number of 1 to 15 ASCII digits: '\\uff10'"),
    ("route status count negative", (SOURCE, ERRORS[:2] + ("errors.......... :          -1",)),
     2, "is not a whole number of 1 to 15 ASCII digits: '-1'"),
    ("route status count past the bound", (SOURCE, ERRORS[:2] + (f"errors.......... :           {BOUND}",)),
     2, "is not a whole number of 1 to 15 ASCII digits"),
    ("route status not UTF-8", (SOURCE, (STATUS, None, COMPLETE.encode() + b"\xff\n")), 2,
     "unreadable route status alinx_ax7101_route_status.rpt: 'utf-8' codec can't decode"),
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
    ("image manifest with a repeated key", ((MANIFEST[0], '"ab"', '"ab", "sha256": "cd"'),), 2,
     "the key 'sha256' appears twice in one object"),
    ("image manifest with a bracketed key", ((MANIFEST[0], '"ab"', '"ab", "x[1]": 1'),), 2,
     "the key 'x[1]' is not a name of 1 to 128 of A-Z a-z 0-9 _ . : / -, in /0"),
    ("image manifest with another named key", ((MANIFEST[0], '"ab"', '"ab", "bytes": 1'),), 0, "RESULT: PASS"),
    ("duplicate conflicting row", (("baseline_utilization.rpt", "| DSPs", "| DSPs | 9 |\n| DSPs"),), 2, "DSPs"),
    ("duplicate conflicting header", (("baseline_utilization.rpt", "| Device       : xc7a100tfgg484-2\n",
                                       "| Device       : xc7a100tfgg484-2\n| Device       : xc7a200tfbg484-2\n"),),
     2, "'Device' appears 2 times"),
    ("malformed count", (row("SLICE", 400, "x"),), 2, "not a count"),
    ("count in other digits", (row("LUT", 1000, "\uff11\uff10\uff10\uff10"),), 2, "not a count"),
    ("fractional count", (row("SLICE", 400, "400.25"),), 2, "not a count"),
    ("count past the bound", (SOURCE, row("LUT", 1000, BOUND)), 2,
     "'Slice LUTs' is not a whole number of 1 to 15 ASCII digits"),
    ("BRAM tiles too long to be finite", (SOURCE, row("BRAM_TILE", 4.5, f"{LONG}.5")), 2,
     "'Block RAM Tile' is not finite"),
    ("missing Slice row", (("baseline_utilization.rpt", f"| {'Slice':<20} | 400 | 0 | 0 | 9 | 1.0 |\n", ""),),
     2, "'Slice' has values []"),
    ("timing columns changed", ((TIMING, "WHS(ns)", "WXS(ns)"),), 2, "columns"),
    ("second timing summary", ((TIMING, "| Design Timing Summary\n", "| Design Timing Summary\n" * 2),), 2, "found 2"),
    ("timing value row missing", ((TIMING, VALUES, ""),), 2, "has no WNS row"),
    ("missing timing report", ((TIMING, None, None),), 2, "baseline_timing.rpt"),
    ("second generated top", ((FLOW, "read_xdc alinx_ax7101.xdc\n", "read_xdc alinx_ax7101.xdc\n"
                               "read_verilog alinx_ax7101.v\n"),), 2, "exactly one generated top"),
    ("read source missing", (("{repo}/sw/constraints.tcl", None, None),), 2, "read source is missing"),
    ("include directory missing", ((FLOW, "/hdl/common}", "/hdl/absent}"),), 2, "include directory is missing"),
    ("cell census header changed", (("baseline_cells.tsv", "cell\tprimitive", "cell\tref"),), 2, "header changed"),
    ("hierarchy count in other digits", ((HIERARCHY, "| m0 | 900 |", "| m0 | \uff19\uff10\uff10 |"),),
     2, "not a row of counts"),
    ("hierarchy count in other digits in a middle cell",
     ((HIERARCHY, TOP_ROW, TOP_ROW.replace("| 50 |", "| \uff15\uff10 |")),), 2, "not a row of counts"),
    ("hierarchy count in other digits in the last cell",
     ((HIERARCHY, TOP_ROW, TOP_ROW[:-3] + "\uff10 |"),), 2, "not a row of counts"),
    ("hierarchy count past the bound", ((HIERARCHY, "| m0 | 900 |", f"| m0 | {BOUND} |"),), 2,
     "hierarchy count of 'alinx_ax7101' is not a whole number of 1 to 15 ASCII digits"),
    ("hierarchy row without counts", ((HIERARCHY, "| m4 | 896 |", "| m4 | n/a |"),), 2, "not a row of counts"),
    ("wrapper source read from too near the root",
     ((FLOW, "/hdl/milan/KL_pp_shadow.sv}\n", "/hdl/milan/KL_pp_shadow.sv}\nread_verilog {/milan/KL_pp_shadow.sv}\n"),),
     2, "read source is missing: /milan/KL_pp_shadow.sv"),
    ("second recipe script", (("baseline_ooc.tcl", None, "quit\n"),), 2, "recipe scripts"),
)
OOC_ARMS = (
    ("standalone control", (), 0, ("RESULT: PASS", "route status")),
    ("standalone clock changed", (("clock.xdc", "20.000", "10.000"),), 2, "standalone_clock_ns"),
    ("generic changed", (row("LUT", 1000, 1011), ("baseline_ooc.tcl", "N_STREAM_IN_P=2", "N_STREAM_IN_P=9")), 1, "LUT"),
    ("image path moved, same image", (row("LUT", 1000, 1001), ("baseline_ooc.tcl", "/ucode.hex", "/x/ucode.hex")),
     2, "identical inputs"),
    ("standalone RAMB36", (SOURCE, row("RAMB36", 4, 5)), 1, "RAMB36"),
    ("standalone RAMB18", (SOURCE, row("RAMB18", 1, 2)), 1, "RAMB18"),
    ("standalone DSP", (SOURCE, row("DSP", 2, 3)), 1, "DSP"),
    ("standalone FF", (SOURCE, *GROWN_FF), 1, "FF"),
)


#: The policy table rows of BUDGET: its head, separator, route row and standalone row.
TABLE = BUDGET.split("\n")[4:8]
#: A scope's counts, for arms that add a sub-block.
COUNTS = {name: 1 for name in gate.SCOPE}
#: An edit adding a sub-block named with a generate index, as Vivado names one: the one key that may hold brackets.
INDEXED = edit("route", "record", "scopes", "u_pp/g_rx[5].u_x", value=COUNTS)
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
    ("check of a route without its status", "route", ((STATUS, None, None),), None, 2, "NOT COMPARABLE: expected one"),
    ("check of a route status count past the integer text limit", "route",
     (SOURCE, ERRORS[:2] + ("errors.......... :  " + "9" * 4401,)), None, 2, "(4401 characters)"),
    ("check of a WNS too long to be finite", "route", (SOURCE, (TIMING, "  0.500  ", f"  {LONG}.063  ")), None,
     2, "NOT COMPARABLE: unreadable measurement"),
    ("check of a wrong-shape image manifest", "route", (MANIFEST,), None, 2, "not a list of path and sha256"),
    ("check against a baseline that is not JSON", "route", (SOURCE,), "{not json", 2, "is unreadable"),
    ("check against a missing baseline", "route", (SOURCE,), Path("absent.json"), 2, "is unreadable"),
    ("check against a baseline without endpoints", "route", (SOURCE,), "[]", 2, "holds no endpoints table"),
    ("check against a scope name with a generate index", "route", (SOURCE,), INDEXED, 0, "RESULT: PASS"),
    ("check of a bracketed key in the last image manifest entry", "route", ((MANIFEST[0], '"ef"', '"ef", "x[1]": 1'),),
     None, 2, "the key 'x[1]' is not a name of 1 to 128 of A-Z a-z 0-9 _ . : / -, in /2"),
    ("check of an endpoint the baseline does not hold", "route", (SOURCE,), edit("route"), 2,
     "holds no endpoint route, only ooc"),
    ("check of an endpoint without a record", "route", (SOURCE,), edit("route", "record"), 2, "route: has no record"),
    ("check of a gated figure without a tolerance", "route", (SOURCE,),
     edit("route", "tolerance", "LUT"), 2, "LUT has no non-negative tolerance"),
    ("check of a ceiling naming no figure", "route", (SOURCE,),
     edit("route", "ceiling", "BRAM_TILES", value=5.0), 2, "not a recorded figure"),
)
#: check-baseline through main(): (label, edit of the recorded endpoints or None, budget page: BUDGET (None),
#: a rewrite of it, or an absent path, exit status, text the output holds).
AUDIT_ARMS = (
    ("a consistent baseline", None, None, 0, "baseline PASS: 2 endpoints"),
    ("a scope name with a generate index", INDEXED, None, 0, "baseline PASS: 2 endpoints"),
    ("a missing record", edit("route", "record"), None, 2, "route: has no record"),
    ("an incomplete record", edit("route", "record", "scopes"), None, 2, "the record lacks scopes"),
    ("a missing tolerance", edit("route", "tolerance", "LUT"), None, 2, "LUT has no non-negative tolerance"),
    ("a negative tolerance", edit("route", "tolerance", "DSP", value=-1), None, 2, "DSP has no non-negative tolerance"),
    ("a missing floor", edit("route", "floor", "WNS_ns"), None, 2, "WNS_ns has no floor"),
    ("a record below its floor", edit("route", "floor", "WHS_ns", value=1.0), None, 2, "WHS_ns is below its floor"),
    ("a record over its ceiling", edit("route", "ceiling", "BRAM_TILE", value=1.0), None,
     2, "BRAM_TILE exceeds its ceiling"),
    ("a missing route ceiling", edit("route", "ceiling"), None, 2, "BRAM_TILE has no ceiling"),
    ("a ceiling naming no figure", edit("route", "ceiling", "BRAM_TILES", value=5.0), None, 2, "not a recorded figure"),
    ("a malformed policy", edit("route", "tolerance", value=[10]), None,
     2, "route: tolerance is not a table of figures"),
    ("a tolerance the budget does not hold", edit("route", "tolerance", "LUT", value=10 ** 9), None,
     2, "tolerance LUT is 1000000000 in the baseline and 10.0 in the budget table"),
    ("a budget value the baseline does not hold", None, lambda page: page.replace("+5 |", "+6 |"),
     2, "tolerance SLICE is 5 in the baseline and 6.0 in the budget table"),
    ("a budget floor the baseline does not hold", None, lambda page: page.replace("+0.030 ns", "+0.040 ns"),
     2, "floor WNS_ns is 0.03 in the baseline and 0.04 in the budget table"),
    ("a budget ceiling the baseline does not hold", None, lambda page: page.replace("| 5.0 |", "| 6.0 |"),
     2, "ceiling BRAM_TILE is 5.0 in the baseline and 6.0 in the budget table"),
    ("a baseline policy figure the budget table lacks", edit("route", "ceiling", "LUT", value=2000),
     None, 2, "ceiling LUT is 2000 in the baseline and None in the budget table"),
    ("a budget cell in other digits", None, lambda page: page.replace("| +5 |", "| +\uff15 |"), 2, "neither a value"),
    ("a budget cell too long to be finite", None, lambda page: page.replace("| +5 |", f"| +{LONG} |"), 2,
     "budget budget.md: budget policy cell '+100"),
    ("an endpoint the budget lacks", None, lambda page: page.replace("| `ooc` |", "Not a row: `ooc` |"),
     2, "ooc: only the baseline names it"),
    ("a budget row the baseline lacks", lambda ends: ends.pop("ooc"), None, 2, "ooc: only the budget table names it"),
    ("no budget table", None, lambda page: page.replace(TABLE[0], "Prose."), 2, "holds 0 resource-gate policy tables"),
    ("two budget tables", None, lambda page: page + "\n" + "\n".join(TABLE), 2, "holds 2 resource-gate policy tables"),
    ("a repeated budget row", None, lambda page: page.replace("| `ooc` |", TABLE[2] + "\n| `ooc` |"),
     2, "malformed or repeated"),
    ("a budget cell that is no value", None, lambda page: page.replace("| +5 |", "| five |"), 2, "neither a value"),
    ("a budget page that is not UTF-8", None, lambda page: page.encode() + b"\xff\n", 2,
     "budget budget.md: 'utf-8' codec can't decode"),
    ("no budget page", None, Path("absent.md"), 2, "budget absent.md"),
)
#: Baselines not of the recorded shape: (label, baseline file as in CHECK_ARMS, text the refusal holds). check and
#: check-baseline both refuse each one with exit 2 before reading any field of it.
MALFORMED = (
    ("a NaN floor", edit("route", "floor", "WNS_ns", value=float("nan")), "the number NaN is not finite"),
    ("an infinite tolerance", edit("route", "tolerance", "LUT", value=float("inf")),
     "the number Infinity is not finite"),
    ("a ceiling too large to be finite", ('"BRAM_TILE": 5.0}', '"BRAM_TILE": 5e999}'),
     "the JSON number is not finite: '5e999'"),
    ("a timing figure recorded as a long whole number", edit("route", "record", "figures", "WNS_ns", value=10 ** 400),
     "the JSON integer is not a whole number of 1 to 15 ASCII digits: '1000000000"),
    ("a scope count past the bound", edit("route", "record", "scopes", "u_pp/u_srp", "LUT", value=10 ** 15),
     "the JSON integer is not a whole number of 1 to 15 ASCII digits: '1000000000000000'"),
    ("a whole number past the integer text limit", ('"BRAM_TILE": 5.0}', '"BRAM_TILE": 5.0, "X": ' + "9" * 4401 + "}"),
     "(4401 characters)"),
    ("a file nested too deep to read", "[" * 100000 + "]" * 100000, "is unreadable"),
    ("a repeated key", ('"BRAM_TILE": 5.0}', '"BRAM_TILE": 9.0, "BRAM_TILE": 5.0}'),
     "the key 'BRAM_TILE' appears twice in one object"),
    ("an endpoint field named by a lone surrogate", lambda ends: ends["route"].update({"\ud800": {}}),
     "the key '\\ud800' is not a name"),
    ("a scope named by a lone surrogate", edit("route", "record", "scopes", "\ud800", value=COUNTS),
     "the key '\\ud800' is not a name"),
    ("a key of 129 characters", lambda ends: ends["route"]["record"]["scopes"].update({"x" * 129: COUNTS}),
     "(129 characters) is not a name"),
    ("an endpoint name with a generate index", lambda ends: ends.update({"route[1]": ends["ooc"]}),
     "the key 'route[1]' is not a name of 1 to 128 of A-Z a-z 0-9 _ . : / -, in /endpoints"),
    ("a policy figure with a generate index", edit("route", "tolerance", "LUT[0]", value=1),
     "the key 'LUT[0]' is not a name of 1 to 128 of A-Z a-z 0-9 _ . : / -, in /endpoints/route/tolerance"),
    ("a note of the file holding a bracketed key", ('{"endpoints": ', '{"description": [{"x[1]": 1}], "endpoints": '),
     "the key 'x[1]' is not a name of 1 to 128 of A-Z a-z 0-9 _ . : / -, in /description/0"),
    ("a note holding a bracketed key under scopes", edit("route", "measured", value={"scopes": {"g_rx[5]": 1}}),
     "the key 'g_rx[5]' is not a name of 1 to 128 of A-Z a-z 0-9 _ . : / -, in /endpoints/route/measured/scopes"),
    ("a bracketed key in a note list past its first item", edit("route", "measured", value=[{"a": 1}, [], {"x[1]": 1}]),
     "the key 'x[1]' is not a name of 1 to 128 of A-Z a-z 0-9 _ . : / -, in /endpoints/route/measured/2"),
    ("an unknown field in the file", ('{"endpoints": ', '{"note": "x", "endpoints": '), "unknown fields note"),
    ("an unknown field in an endpoint", lambda ends: ends["route"].update({"ceilings": {}}), "unknown fields ceilings"),
    ("an unknown field in a record", edit("route", "record", "note", value="x"),
     "route: the record holds unknown fields note"),
    ("a record kind that is a list", edit("route", "record", "kind", value=["route"]), "kind ['route'] is not one of"),
    ("an unknown record kind", edit("route", "record", "kind", value="tile"), "kind 'tile' is not one of"),
    ("an identity that is text", edit("route", "record", "identity", value="Vivado"), "identity does not hold exactly"),
    ("an identity without its device", edit("route", "record", "identity", "device"), "identity does not hold exactly"),
    ("an identity with an extra key", edit("route", "record", "identity", "host", value="x"),
     "identity does not hold exactly"),
    ("an identity field of another type", edit("route", "record", "identity", "tool", value=7),
     "not of its recorded type"),
    ("a flow that is not text", edit("route", "record", "identity", "flow", value=[1]), "not a list of text"),
    ("a standalone clock that is not text", edit("ooc", "record", "identity", "standalone_clock_ns", value=[5]),
     "ooc: the record identity's flow or standalone clock is not a list of text"),
    ("an input digest that is no digest", edit("route", "record", "inputs_sha256", value="ab"),
     "not a sha256 hex digest"),
    ("an input digest that is a number", edit("route", "record", "inputs_sha256", value=5), "not a sha256 hex digest"),
    ("an input digest in upper case", edit("route", "record", "inputs_sha256", value="AB" * 32),
     "not a sha256 hex digest"),
    ("figures that are a list", edit("route", "record", "figures", value=[]), "figures are not exactly"),
    ("figures without LUT", edit("route", "record", "figures", "LUT"), "figures are not exactly"),
    ("figures with an extra figure", edit("route", "record", "figures", "URAM", value=0), "figures are not exactly"),
    ("a gated figure that is text", edit("route", "record", "figures", "LUT", value="1000"),
     "recorded figure is not a finite number"),
    ("a gated figure that is null", edit("route", "record", "figures", "WNS_ns", value=None),
     "recorded figure is not a finite number"),
    ("a gated figure that is a bool", edit("route", "record", "figures", "DSP", value=True),
     "recorded figure is not a finite number"),
    ("a malformed endpoint after the first", edit("ooc", "record", "figures", "LUT", value="1000"),
     "ooc: a recorded figure is not a finite number"),
    ("scopes that are a list", edit("route", "record", "scopes", value=[]), "scopes are not a table"),
    ("a scope without its CARRY4 count", edit("route", "record", "scopes", "wrapper", "CARRY4"),
     "scopes are not a table"),
    ("a scope with an extra count", edit("route", "record", "scopes", "wrapper", "URAM", value=0),
     "scopes are not a table"),
    ("a fractional scope count", edit("route", "record", "scopes", "u_pp/u_srp", "LUT", value=1.5),
     "sub-block count is not a non-negative whole number"),
    ("a negative scope count", edit("route", "record", "scopes", "u_pp/u_srp", "FF", value=-1),
     "sub-block count is not a non-negative whole number"),
    ("a scope count that is a bool", edit("route", "record", "scopes", "u_pp/u_srp", "LUT", value=True),
     "sub-block count is not a non-negative whole number"),
    ("a tolerance that is text", edit("route", "tolerance", "LUT", value="10"),
     "a tolerance value is not a finite number"),
    ("a ceiling that is a bool", edit("route", "ceiling", "BRAM_TILE", value=True),
     "a ceiling value is not a finite number"),
    ("a floor table that is a list", edit("route", "floor", value=[0]), "floor is not a table"),
)
#: Gate functions an exception is planted in, each reached by the command that follows it.
PLANTED = (("load", "check"), ("census", "check"), ("routing", "check"), ("judge", "check"),
           ("entry_problems", "check"), ("load", "check-baseline"), ("check_baseline", "check-baseline"))


def fresh(root: Path, kind: str) -> Path:
    """Recreate the arm tree from the pristine copy and name its measurement directory."""
    shutil.rmtree(root / "arm", ignore_errors=True)
    shutil.copytree(root / "pristine", root / "arm", symlinks=True)
    return root / "arm" / ("gateware" if kind == "route" else "ooc")


def plant(folder: Path, name: str, old: str | None, new: str | bytes | None) -> None:
    """Edit exactly one occurrence, delete a file (both None) or create one (old None) of text or bytes."""
    path = Path(name) if name.startswith("/") else folder / name
    if old is None:
        if new is None:
            path.unlink()
        else:
            (path.write_bytes if isinstance(new, bytes) else path.write_text)(new)
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
                             + (f" and not {absent!r}" if absent else "") + "\n" + ascii(report))


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
    """Run the gate's command line in process into a stream that takes ASCII only.

    An escaped exception, a character printing cannot encode included, is a traceback, never an exit status.
    """
    raw = io.BytesIO()
    out = io.TextIOWrapper(raw, encoding="ascii", errors="strict", newline="\n")
    try:
        with contextlib.redirect_stdout(out):
            status = gate.main([str(arg) for arg in argv])
        out.flush()
    except SystemExit as error:  # argparse's usage exit: its status, with no reason on standard output
        return error.code, [*raw.getvalue().decode("ascii", "replace").splitlines(), "exited through argparse"]
    except Exception as error:  # the contract is an exit status with a reason, so this fails the arm
        return -1, [*raw.getvalue().decode("ascii", "replace").splitlines(),
                    f"escaped {type(error).__name__}: {ascii(str(error))}"]
    return status, raw.getvalue().decode("ascii").splitlines()


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
    """Write the budget page an arm's check-baseline reads, as text or bytes, or name an absent one."""
    if isinstance(page, Path):
        return tmp / page
    path = tmp / "budget.md"
    data = BUDGET if page is None else page(BUDGET)
    (path.write_bytes if isinstance(data, bytes) else path.write_text)(data)
    return path


def plant_source(tmp: Path) -> Path:
    """A route measurement of a changed source with unchanged figures: within tolerance against the record."""
    folder = fresh(tmp / "route", "route")
    plant(folder, SOURCE[0].replace("{repo}", str(tmp / "route/arm/repo")), *SOURCE[1:])
    return folder


def planted(name: str) -> Callable[..., None]:
    """A stand-in for one gate function that raises an exception none of the gate's handlers names."""
    def boom(*_args: object, **_kwargs: object) -> None:
        """Raise the planted exception."""
        raise ZeroDivisionError(f"planted \ud800\x1b[31m in {name}")
    return boom


def barrier_arms(tmp: Path, entries: dict) -> int:
    """Exceptions planted inside the gate, a non-ASCII path and a refused write, through main(); return the count."""
    for name, command in PLANTED:
        original = getattr(gate, name)
        setattr(gate, name, planted(name))
        try:
            path = baseline_file(tmp, entries, None)
            if command == "check":
                status, lines = cli("check", plant_source(tmp), "--endpoint", "route", "--baseline", path)
            else:
                status, lines = cli("check-baseline", "--baseline", path, "--budget", budget_file(tmp, None))
        finally:
            setattr(gate, name, original)
        expect(f"planted-exception arm {name} through {command}", status, lines, 2,
               f"NOT COMPARABLE: ZeroDivisionError: planted \\ud800\\x1b[31m in {name}")
        print(f"resource gate planted-exception arm: {name} through {command}: exit 2 PASS")
    link = tmp / "mesur\u00e9"
    link.symlink_to(plant_source(tmp))
    status, lines = cli("check", link, "--endpoint", "route", "--baseline", baseline_file(tmp, entries, None))
    expect("command-line arm 'a directory named in another script'", status, lines, 0, "/mesur\\xe9\n")
    print("resource gate command-line arm: a directory named in another script: exit 0 PASS")
    path = baseline_file(tmp, entries, None)
    before = path.read_bytes()
    status, lines = cli("record", fresh(tmp / "route", "route"), "--endpoint", "copy[1]", "--baseline", path, "--write")
    expect("command-line arm 'record --write of an endpoint name the baseline refuses'", status, lines, 2,
           "the key 'copy[1]' is not a name of 1 to 128 of A-Z a-z 0-9 _ . : / -, in /endpoints")
    if path.read_bytes() != before:
        raise AssertionError("record --write wrote a baseline the gate refuses")
    print("resource gate command-line arm: record --write of an endpoint name the baseline refuses: exit 2 PASS")
    return len(PLANTED) + 2


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
    return len(CHECK_ARMS) + len(AUDIT_ARMS) + 2 * len(MALFORMED) + 2 + barrier_arms(tmp, entries)


#: Odd characters a generated case plants: other scripts' digits, lone surrogates, controls, marks, wide ones.
ODD = ("\uff10", "\u0661", "\u00b2", "\U0001d7ce", "\ud800", "\udfff", "\x00", "\x1b", "\u200b", "\u0301",
       "\u202e", "\ufeff", "\u00e9", "\U0001f600", "\t")
#: Digits that int(), float() or str.isdigit() would take and that are not ASCII.
OTHER_DIGITS = ("\uff10", "\uff15", "\u0661", "\u0966", "\u00b2", "\U0001d7ce")
#: Keys outside every name class the baseline documents.
BAD_NAMES = ("", "a b", "x" * 129, "\u00e9", "\ud800", "LUT\n", 'a"b', "\uff2c\uff35\uff34", "a|b", "{x}")
#: Keys a case writes into an open object, a note or an image manifest entry. Only the first two are names there:
#: brackets belong to a sub-block scope name alone.
OPEN_KEYS = ("text", "run.2:a/b-c_d", "x[1]", "g_rx[5].u", "]", *BAD_NAMES)
#: JSON number texts the converters refuse: past 15 digits, too large to be finite, or not JSON numbers at all.
OVERFLOWS = (LONG, "-" + "9" * 16, "9" * 16, "1e400", "-1e400", LONG + ".5", "NaN", "Infinity", "9" * 4401)
#: Values of every JSON type, for a case that puts one where its path does not take it.
SAMPLES = ("x", "", "\ud800", "\uff11", 7, -1, 1.5, 0, True, False, None, [], [1], ["x"], {}, {"a": 1})
#: Report tokens that are not what a gated cell of each kind holds, none holding a space, bar or colon.
GARBLES = {"count": ("n/a", "-", "1,000", "1e3", "0x10", "+5", "1.25", "1.5", "-1", "\uff11"),
           "used": ("n/a", "-", "1,000", "1e3", "0x10", "+5", "1.25", "4.0", "-1", "\uff11"),
           "slack": ("n/a", "-", "1,000", "1e3", "0x10", "+5", "-1", "\uff11", "1.", ".5", "inf", "nan", "1")}
#: The changes to each report's own layout that break it.
STRUCTURAL = {"baseline_utilization.rpt": ("header twice", "header removed"), "baseline_timing.rpt": ("summary twice",),
              "baseline_cells.tsv": ("census header",), "route status": ("row twice", "row removed", "second report"),
              "baseline_images.json": ("entry key",)}
#: Byte sequences no UTF-8 text holds.
UNDECODABLE = (b"\xff", b"\xc3(", b"\xed\xa0\x80", b"\x80", b"\xf8\x88\x80\x80\x80")
#: The files of every measurement directory the gate reads and a generated case changes.
REPORTS = ("baseline_utilization.rpt", "baseline_timing.rpt", "baseline_hierarchy.rpt", "baseline_cells.tsv",
           "baseline_images.json")


def rule(path: tuple) -> str | None:
    """The shape the baseline documents at one path, or None where it documents none (notes, open tables)."""
    match path:
        case (("endpoints",) | ("endpoints", _) | ("endpoints", _, "record" | "tolerance" | "floor" | "ceiling")
              | ("endpoints", _, "record", "identity" | "figures" | "scopes")
              | ("endpoints", _, "record", "scopes", _)):
            return "dict"
        case ("endpoints", _, "record", "identity", "flow" | "standalone_clock_ns"):
            return "texts"
        case ("endpoints", _, "record", "identity", _) | ("endpoints", _, "record", "identity", _, int()):
            return "text"
        case ("endpoints", _, "record", "figures", _) | ("endpoints", _, "tolerance" | "floor" | "ceiling", _):
            return "number"
        case ("endpoints", _, "record", "scopes", _, _):
            return "count"
        case ("endpoints", _, "record", "kind" | "inputs_sha256"):
            return path[-1]
    return None


def breaks(shape: str, value: object) -> bool:
    """Whether a value breaks the shape the baseline documents for its path; any other kind breaks it."""
    number = isinstance(value, (int, float)) and not isinstance(value, bool)
    return {"dict": not isinstance(value, dict), "text": not isinstance(value, str),
            "texts": not (isinstance(value, list) and all(isinstance(item, str) for item in value)),
            "number": not number, "count": not (type(value) is int and value >= 0), "kind": True,
            "inputs_sha256": not (isinstance(value, str) and re.fullmatch("[0-9a-f]{64}", value))}[shape]


def closed(path: tuple, table: dict) -> tuple | None:
    """The keys a closed object of the baseline must hold, or None when the object is open or undocumented."""
    match path:
        case ():
            return ("endpoints",)
        case ("endpoints", _):
            return ("record",)
        case ("endpoints", _, "record"):
            return gate.RECORD
        case ("endpoints", _, "record", "identity" | "figures"):
            return tuple(gate.IDENTITY) if path[-1] == "identity" else tuple(table)
        case ("endpoints", _, "record", "scopes", _):
            return gate.SCOPE
    return None


def nodes(value: object, path: tuple = ()) -> list[tuple[tuple, object]]:
    """Every (path, value) of a JSON tree, the root first."""
    items = value.items() if isinstance(value, dict) else enumerate(value) if isinstance(value, list) else ()
    return [(path, value)] + [found for key, item in items for found in nodes(item, path + (key,))]


def dump(value: object, raw: dict, twice: tuple | None = None, path: tuple = ()) -> str:
    """Write JSON, with raw text at the paths raw names and the pair at path twice written two times."""
    if path in raw:
        return raw[path]
    if isinstance(value, dict):
        pairs = [f"{json.dumps(key)}: {dump(item, raw, twice, path + (key,))}" for key, item in value.items()]
        pairs += [pair for pair, key in zip(pairs, value) if path + (key,) == twice]
        return "{" + ", ".join(pairs) + "}"
    if isinstance(value, list):
        return "[" + ", ".join(dump(item, raw, twice, path + (index,)) for index, item in enumerate(value)) + "]"
    return json.dumps(value)


def spliced(rng: random.Random, data: bytes) -> tuple[bytes, bool]:
    """Insert bytes no UTF-8 text holds; return them and whether read_text(), in the locale's encoding, refuses."""
    index = rng.randint(0, len(data))
    data = data[:index] + rng.choice(UNDECODABLE) + data[index:]
    try:
        data.decode(locale.getpreferredencoding(False))
    except UnicodeDecodeError:
        return data, True
    return data, False


def mutate_json(rng: random.Random, base: dict) -> tuple[str, bytes, bool]:
    """One random change to the baseline: (operator, the file's bytes, whether a documented shape breaks)."""
    tree = copy.deepcopy(base)
    every = nodes(tree)
    keys = [path + (key,) for path, value in every if isinstance(value, dict) for key in value]
    leaves = [path for path, value in every if path and not isinstance(value, (dict, list))]
    numbers = [path for path, value in every if path and type(value) in (int, float)]
    texts = [path for path, value in every if path and isinstance(value, str)]
    operator = rng.choice(("type", "value", "remove", "add", "bad name", "bracket name", "duplicate", "overflow",
                           "digit", "truncate", "unicode", "size", "bytes", "note"))
    raw, twice, broken = {}, None, True
    if operator in ("type", "value", "unicode"):
        path = rng.choice([path for path, _ in every if path and rule(path)] if operator == "type" else
                          numbers if operator == "value" else texts)
        value = at(tree, path)
        if operator == "type":
            value = rng.choice([sample for sample in SAMPLES if breaks(rule(path), sample)])
        elif operator == "value":
            count, broken = rule(path) in ("count", None), False
            value = rng.randint(0, 10 ** 15 - 1) if count else rng.uniform(-9999, 9999)
        else:
            index = rng.randint(0, len(value))
            value, broken = value[:index] + rng.choice(ODD) + value[index:], rule(path) in ("kind", "inputs_sha256")
        at(tree, path[:-1])[path[-1]] = value
    elif operator in ("remove", "bad name", "bracket name"):
        path = rng.choice(keys)
        held = at(tree, path[:-1])
        need = closed(path[:-1], held) or ()
        name = None if operator == "remove" else rng.choice(BAD_NAMES) if operator == "bad name" else path[-1] + "[1]"
        pairs = [(name if key == path[-1] else key, value) for key, value in held.items()]
        held.clear()
        held.update((key, value) for key, value in pairs if key is not None)
        scope = len(path) == 5 and path[2:4] == ("record", "scopes")
        broken = path[-1] in need if operator == "remove" else operator == "bad name" or not scope
    elif operator == "add":
        path = rng.choice([path for path, value in every if isinstance(value, dict)])
        at(tree, path)["fuzz_extra"] = 1
        broken = closed(path, {}) is not None
    elif operator == "duplicate":
        twice = rng.choice(keys)
    elif operator == "overflow":
        raw = {rng.choice(leaves): rng.choice(OVERFLOWS)}
    elif operator == "digit":
        path = rng.choice(numbers)
        number = json.dumps(at(tree, path))
        index = rng.choice([index for index, char in enumerate(number) if char in "0123456789"])
        raw = {path: number[:index] + rng.choice(OTHER_DIGITS) + number[index + 1:]}
    elif operator == "truncate":
        text = dump(tree, {})
        return operator, text[:rng.randrange(len(text))].encode(), True
    elif operator == "size":
        operator = rng.choice(("size: deep nesting", "size: many scopes", "size: long text"))
        if operator == "size: deep nesting":
            raw = {rng.choice(leaves): "[" * 100000 + "]" * 100000}
        elif operator == "size: long text":
            path, broken = rng.choice(texts), False
            at(tree, path[:-1])[path[-1]] = "x" * 200000
        else:
            record, broken = rng.choice(list(tree["endpoints"].values()))["record"], False
            record["scopes"].update({f"fuzz/s{index}": dict(COUNTS) for index in range(2000)})
    elif operator == "bytes":
        return (operator, *spliced(rng, dump(tree, {}).encode()))
    elif operator == "note":
        key, notes = rng.choice(OPEN_KEYS), [(name,) for name in gate.NOTES["file"]] + [
            ("endpoints", end, name) for end in tree["endpoints"] for name in gate.NOTES["endpoint"]]
        value, note, broken = {key: rng.choice(SAMPLES)}, rng.choice(notes), key not in OPEN_KEYS[:2]
        items = [{"run": index} for index in range(3)]
        items.insert(rng.randint(0, 3), value)
        at(tree, note[:-1])[note[-1]] = rng.choice((value, items, {"scopes": value}))
    return operator, dump(tree, raw, twice).encode(), broken


def tokens(name: str, text: str, kind: str) -> list[tuple[int, int, str]]:
    """Every number the gate reads in one report, located as (start, end, kind of token)."""
    found, offset = [], 0
    for line in text.splitlines(keepends=True):
        parts = line.split("|")
        cells = range(0)
        if name == "baseline_utilization.rpt" and len(parts) > 3 and parts[1].strip().rstrip("*").strip() \
                in gate.ROWS[kind]:
            cells = range(2, 3)
        elif name == "baseline_hierarchy.rpt" and len(parts) == 12 and parts[3].strip() != "Total LUTs":
            cells = range(3, 11)
        position = offset
        for index, part in enumerate(parts):
            if index in cells and part.strip():
                start = position + len(part) - len(part.lstrip())
                found.append((start, start + len(part.strip()), "used" if len(cells) == 1 else "count"))
            position += len(part) + 1
        offset += len(line)
    if name == "baseline_timing.rpt" and "| Design Timing Summary" in text:
        block = text.index("| Design Timing Summary")
        lines = [match for match in re.finditer(r"[^\n]*\S[^\n]*", text[block:])]
        heads = next((index for index, match in enumerate(lines) if "WNS(ns)" in match[0]), len(lines))
        if heads + 2 < len(lines):
            names = re.split(r"\s{2,}", lines[heads][0].strip())
            for index, value in enumerate(re.finditer(r"\S+", lines[heads + 2][0])):
                if index in (0, 4) or names[index:index + 1] in (["TNS Total Endpoints"], ["THS Total Endpoints"]):
                    start = block + lines[heads + 2].start() + value.start()
                    found.append((start, start + len(value[0]), "slack" if index in (0, 4) else "count"))
    if name.endswith("_route_status.rpt"):
        found = [(match.start(2), match.end(2), "count") for match in gate.STATUS_ROW.finditer(text)]
    return found


def mutate_report(rng: random.Random, name: str, text: str, kind: str) -> tuple[str, dict, bool]:
    """One random change to a report: (operator, {file: bytes, or None to delete it}, whether a shape breaks)."""
    lines, found = text.splitlines(keepends=True), tokens(name, text, kind)
    shaped = STRUCTURAL.get("route status" if name.endswith("_route_status.rpt") else name, ())
    operators = ("missing", "empty", "bytes", "truncate", "lines", "unicode") + ("token",) * 3 * bool(found) + shaped
    operator, broken, extra = rng.choice(operators), kind != "clock", {}
    if operator == "token":
        start, end, token = rng.choice(found)
        value = text[start:end]
        operator = rng.choice(("digit", "huge", "garble", "number"))
        if operator == "digit":
            index = rng.choice([index for index, char in enumerate(value) if char in "0123456789"])
            value = value[:index] + rng.choice(OTHER_DIGITS) + value[index + 1:]
        elif operator == "huge":
            value = rng.choice((LONG + ".5", "-" + LONG + ".25") if token == "slack" else
                               ("9" * rng.randint(16, 40), "9" * 4401) + ((LONG + ".5",) if token == "used" else ()))
        elif operator == "garble":
            value = rng.choice(GARBLES[token])
        else:
            value = f"{rng.uniform(-2, 2):.3f}" if token == "slack" else str(rng.randint(0, 10 ** 6))
        text, broken = text[:start] + value + text[end:], operator != "number"
    elif operator == "missing":
        return operator, {name: None}, broken
    elif operator == "empty":
        text = ""
    elif operator == "bytes":
        data, broken = spliced(rng, text.encode())
        return operator, {name: data}, broken
    elif operator in ("truncate", "lines", "unicode"):
        index, other, broken = rng.randrange(len(lines)), rng.randrange(len(lines)), False
        if operator == "truncate":
            lines = [text[:rng.randrange(len(text) + 1)]]
        elif operator == "unicode":
            lines[index] = lines[index][:other % 40] + rng.choice(ODD) + lines[index][other % 40:]
        else:
            operator = rng.choice(("delete line", "duplicate line", "swap lines", "junk lines"))
            junk = ["".join(rng.choice(ODD + ("a", "|", ":", "#", " ", "9")) for _ in range(40)) + "\n"] * 500
            lines[index:index + 1] = {"delete line": [], "duplicate line": [lines[index]] * 2, "junk lines": junk,
                                      "swap lines": [lines[other]]}[operator]
        text = "".join(lines)
    elif operator in ("header twice", "header removed", "row twice", "row removed"):
        pattern = r"\| (Tool Version|Design|Device|Design State)\s*: " if operator.startswith("header") else \
            r".*# of (routable nets|fully routed nets|nets with routing errors)\."
        index = rng.choice([index for index, line in enumerate(lines) if re.match(pattern, line)])
        lines[index:index + 1] = [lines[index]] * (2 if operator.endswith("twice") else 0)
        text = "".join(lines)
    elif operator == "summary twice":
        index = rng.randint(0, len(lines))
        text = "".join(lines[:index] + ["| Design Timing Summary\n"] + lines[index:])
    elif operator == "census header":
        text = "cell\tref\n" + "".join(lines[1:])
    elif operator == "second report":
        extra = {"fuzz_route_status.rpt": text.encode()}
    elif operator == "entry key":
        entries, key = json.loads(text), rng.choice(OPEN_KEYS)
        rng.choice(entries)[key] = rng.choice(SAMPLES)
        text, broken = json.dumps(entries), key not in OPEN_KEYS[:2]
    return operator, {name: text.encode("utf-8", "surrogatepass"), **extra}, broken


def fixtures(work: Path) -> tuple[list[tuple[Path, str]], dict, str]:
    """The self-test's fuzz targets: the route and standalone fixtures, a baseline of both, and its budget page."""
    runs = [{"seconds": seconds} for seconds in (12, 9, 30)]
    base = {"schema": 1, "description": {"text": "fixture baseline", "runs": runs}, "endpoints": {}}
    for kind in ("route", "ooc"):
        (work / kind).mkdir()
        base["endpoints"][kind] = dict(recorded(work / kind, kind), measured={"run": "fixture"})
    return [(fresh(work / kind, kind), kind) for kind in ("route", "ooc")], base, BUDGET


def selftest() -> int:
    """Run every arm and 500 generated cases; return 0 only when each one produced its expected verdict."""
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
    if gate.fuzz(500, 234) != 0:
        raise AssertionError("a generated case broke the exit-code contract")
    print(f"resource gate selftest: {count} arms and 500 generated cases PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(selftest())
