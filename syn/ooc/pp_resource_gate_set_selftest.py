#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
"""Plant the resource gate's route-set rule (#818, the #814 ruling) end to end.

A route endpoint is judged on the recipe's three placement directives, or on one route marked as the shipping
selection. The timing arms judge one route at its signoff corners: each plant keeps the timing summary the worst of
its corners, as one run's reports are, unless it plants that disagreement. The set arms build the recipe's two
comparison routes beside the self-test's shipping route, as the recipe's snippet writes them, and run main(): the
selected route below a floor at one corner, a shipping route below the floor beside a comparison above it, a large
fall from the record, a resource over its tolerance, ties, and every binding of a comparison to its shipping route.
"""

import json
from pathlib import Path
import shutil


#: The signoff reports of the self-test's timing grade, {Slow Fast} at 0 and 85 C, as sw/litex/timing_grade.tcl names
#: them, in the order the gate names them. The worst setup slack is at Slow and the worst hold slack at Fast.
CORNERS = {f"{model}_{temp}C": f"alinx_ax7101_signoff_{model}_{temp}C_timing.rpt"
           for model in ("Slow", "Fast") for temp in (0, 85)}
TIMING = "baseline_timing.rpt"
COMPARISON = "baseline_implementation.tcl"
#: The recipe's comparison directives, each with its worst-corner WNS in the set fixture: below the shipping 0.500.
OTHERS = {"AltSpreadLogic_high": "0.400", "ExtraTimingOpt": "0.300"}
ASLH, ETO = "{AltSpreadLogic_high}/", "{ExtraTimingOpt}/"
SET = ("--comparison", "{AltSpreadLogic_high}", "--comparison", "{ExtraTimingOpt}")
REVERSED = ("--comparison", "{ExtraTimingOpt}", "--comparison", "{AltSpreadLogic_high}")
FAMILY = "ExtraPostPlacementOpt, AltSpreadLogic_high, ExtraTimingOpt"


def summary(wns: str, whs: str) -> str:
    """A Design Timing Summary as the vendor report lays it out, ten endpoints timed."""
    return ("| Design Timing Summary\n| ---\n\n"
            "    WNS(ns)      TNS(ns)  TNS Failing Endpoints  TNS Total Endpoints      WHS(ns)      THS(ns)\n"
            "    -------      -------  ---------------------  -------------------      -------      -------\n"
            f"      {wns}        0.000                      0                   10        {whs}        0.000\n")


def corner_reports(folder: Path, header: str, wns: str = "0.500") -> None:
    """Write a route's signoff corners: the worst setup slack wns at Slow, 1 ns more at Fast, the worst hold at Fast."""
    for name, report in CORNERS.items():
        setup, hold = (wns, "0.200") if name.startswith("Slow") else (f"{float(wns) + 1:.3f}", "0.100")
        (folder / report).write_text(header + summary(setup, hold))


def slack(figure: str, old: str, new: str, route: str = "", at: tuple[str, ...] = ()) -> tuple:
    """Plant one slack in a route's timing summary and in the corners holding its worst value, keeping them one run's.

    WNS is worst at the Slow corners and WHS at the Fast ones; at names fewer, and route leads a comparison's files.
    """
    names = at or tuple(name for name in CORNERS if name.startswith("Slow" if figure == "WNS" else "Fast"))
    return tuple((route + name, old, new) for name in (TIMING, *(CORNERS[corner] for corner in names)))


def on(route: str, plant: tuple) -> tuple:
    """The same plant in a comparison route's file."""
    return (route + plant[0], *plant[1:])


def timing_arms() -> tuple:
    """One route's floor, fall, corner and directive arms, in the self-test's route arm form."""
    from pp_resource_gate_selftest import FLOW, LONG, SOURCE, report_header
    header, renamed = report_header("alinx_ax7101", "Physopt postRoute"), []
    for model, slacks in (("Slow", ("0.500", "0.200")), ("Fast", ("1.500", "0.100"))):
        renamed += [(CORNERS[f"{model}_85C"], None, None),
                    (CORNERS[f"{model}_85C"].replace("85C", "100C"), None, header + summary(*slacks))]
    return (
        ("WNS below the floor", (SOURCE, *slack("WNS", "  0.500  ", " -0.010  ")), 1,
         "below the floor 0.03 at Slow_0C, Slow_85C"),
        ("WNS below the floor at one corner", (SOURCE, *slack("WNS", "  0.500  ", "  0.020  ", at=("Slow_85C",))), 1,
         ("below the floor 0.03 at Slow_85C", "at Slow_0C")),
        ("WNS below the floor and fell more than the timing fall: both reported",
         (SOURCE, *slack("WNS", "  0.500  ", "  0.020  ")), 1,
         (("REGRESSION: below the floor 0.03 at Slow_0C, Slow_85C; WARNING: fell by more than 0.25 from the record",
           "WARNING: WNS_ns fell from the record", "RESULT: MATERIAL REGRESSION"), None)),
        ("WNS below the floor within the timing fall: no warning", (SOURCE, *slack("WNS", "  0.500  ", "  0.290  ")),
         1, (("below the floor 0.3 at Slow_0C, Slow_85C", "RESULT: MATERIAL REGRESSION"), "WARNING"),
         {"floor": {"WNS_ns": 0.3}}),
        ("WNS at the floor", (SOURCE, *slack("WNS", "  0.500  ", "  0.300  ")), 0, "RESULT: PASS",
         {"floor": {"WNS_ns": 0.3}}),
        ("WNS fell more than the timing fall: a warning, never a failure",
         (SOURCE, *slack("WNS", "  0.500  ", "  0.200  ")), 0,
         (("WARNING: fell by more than 0.25 from the record", "WARNING: WNS_ns fell from the record", "RESULT: PASS"),
          "REGRESSION")),
        ("WNS fell by exactly the timing fall", (SOURCE, *slack("WNS", "  0.500  ", "  0.250  ")), 0,
         ("RESULT: PASS", "WARNING")),
        ("WNS fell within the timing fall", (SOURCE, *slack("WNS", "  0.500  ", "  0.300  ")), 0,
         ("RESULT: PASS", "re-baseline")),
        ("WNS rise beyond the tolerance", (SOURCE, *slack("WNS", "  0.500  ", "  0.800  ")), 0,
         "re-baseline recommended: WNS_ns"),
        ("WHS below the floor", (SOURCE, *slack("WHS", "0.100", "-0.001")), 1, "WHS_ns"),
        ("WHS below the floor at one corner", (SOURCE, *slack("WHS", "0.100", "-0.001", at=("Fast_85C",))), 1,
         ("below the floor 0.0 at Fast_85C", "at Fast_0C")),
        ("WHS below the floor and fell more than the timing fall: both reported",
         (SOURCE, *slack("WHS", "0.100", "-0.200")), 1,
         (("REGRESSION: below the floor 0.0 at Fast_0C, Fast_85C; WARNING: fell by more than 0.25 from the record",
           "WARNING: WHS_ns fell from the record", "RESULT: MATERIAL REGRESSION"), None)),
        ("WHS below the floor within the timing fall: no warning", (SOURCE, *slack("WHS", "0.100", "-0.001")), 1,
         (("below the floor 0.0 at Fast_0C, Fast_85C", "RESULT: MATERIAL REGRESSION"), "WARNING")),
        ("WHS at the floor", (SOURCE, *slack("WHS", "0.100", "0.000")), 0, "RESULT: PASS"),
        ("identical inputs, different WNS", slack("WNS", "  0.500  ", "  0.400  "), 2, "identical inputs"),
        ("a corner's WNS below the summary's", ((CORNERS["Slow_0C"], "  0.500  ", "  0.450  "),), 2,
         "the signoff corners' worst WNS_ns is 0.45 and the timing summary's 0.5: the reports are not of one run"),
        ("a corner's WHS below the summary's", ((CORNERS["Fast_85C"], "0.100", "0.090"),), 2, "worst WHS_ns is 0.09"),
        ("the summary's WNS below every corner's, under the floor", (SOURCE, (TIMING, "  0.500  ", "  0.010  ")), 2,
         "the signoff corners' worst WNS_ns is 0.5 and the timing summary's 0.01: the reports are not of one run"),
        ("the summary's WHS below every corner's, under the floor", (SOURCE, (TIMING, "0.100", "-0.050")), 2,
         "the signoff corners' worst WHS_ns is 0.1 and the timing summary's -0.05: the reports are not of one run"),
        ("a corner report missing", ((CORNERS["Fast_85C"], None, None),), 2,
         (("FileNotFoundError", "alinx_ax7101_signoff_Fast_85C_timing.rpt"), None)),
        ("a corner report without its summary", ((CORNERS["Slow_0C"], "| Design Timing Summary\n", ""),), 2,
         "alinx_ax7101_signoff_Slow_0C_timing.rpt: expected one Design Timing Summary, found 0"),
        ("a corner slack too long to be finite", ((CORNERS["Fast_0C"], "0.100", f"{LONG}.1"),), 2,
         "alinx_ax7101_signoff_Fast_0C_timing.rpt: WHS is not finite"),
        ("timing grade changed, its corners reported", ((FLOW, "{85}", "{100}"), *renamed), 2, "change in flow"),
        ("signoff reports not written", ((FLOW, "kl_timing_grade_reports alinx_ax7101_signoff\n", ""),), 2,
         "configures 1 timing grades and writes 0 signoff report sets"),
        ("a second timing grade", ((FLOW, "{Slow Fast}\n", "{Slow Fast}\nkl_timing_grade_configure {a} {b} {0} {85} "
                                    "{Slow}\n"),), 2, "configures 2 timing grades"),
        ("placement directive another of the recipe's", ((FLOW, "ExtraPostPlacementOpt", "ExtraTimingOpt"),), 0,
         "RESULT: PASS"),
        ("placement directive outside the recipe", ((FLOW, "ExtraPostPlacementOpt", "Default"),), 2,
         "change in flow"),
    )


def set_arms_table() -> tuple:
    """(label, route options, plants, exit status, text the output holds or (holds, lacks)) for main() on a route set.

    An option {directive} names that comparison route, and a plant's file under {directive}/ is that route's.
    """
    from pp_resource_gate_selftest import ERRORS, FLOW, SOURCE, row
    lowered = (*slack("WNS", "  0.400  ", "  0.090  ", ASLH), *slack("WNS", "  0.300  ", "  0.080  ", ETO))
    raised = slack("WNS", "  0.400  ", "  0.600  ", ASLH)
    return (
        ("route set control", SET, (), 0, (("directive ExtraPostPlacementOpt selected", "RESULT: PASS"), "REGRESSION")),
        ("comparisons named in either order", REVERSED, (), 0, "directive ExtraPostPlacementOpt selected"),
        ("a set whose best directive misses the floor at one corner fails", SET,
         (SOURCE, *slack("WNS", "  0.500  ", "  0.020  ", at=("Slow_85C",)),
          *slack("WNS", "  0.400  ", "  0.010  ", ASLH), *slack("WNS", "  0.300  ", "  0.005  ", ETO)), 1,
         (("directive ExtraPostPlacementOpt selected", "below the floor 0.03 at Slow_85C"), "at Slow_0C")),
        ("a set whose shipping directive misses the floor and whose best meets it passes, naming the best", SET,
         (SOURCE, *slack("WNS", "  0.500  ", "  0.020  ")), 0,
         (("directive AltSpreadLogic_high selected", "RESULT: PASS"), "REGRESSION")),
        ("a large fall passes with a WARNING", SET, (SOURCE, *slack("WNS", "  0.500  ", "  0.100  "), *lowered), 0,
         (("directive ExtraPostPlacementOpt selected", "WARNING: WNS_ns fell from the record", "RESULT: PASS"),
          "REGRESSION")),
        ("a resource over its tolerance still fails", SET, (SOURCE, row("LUT", 1000, 1011)), 1,
         (("REGRESSION: grew by more than 10", "RESULT: MATERIAL REGRESSION"), None)),
        ("a selected comparison is judged on its own resources", SET,
         (SOURCE, *raised, on(ASLH, row("SLICE", 400, 406))), 1,
         (("directive AltSpreadLogic_high selected", "REGRESSION: grew by more than 5"), None)),
        ("a route not selected is not judged on its resources", SET, (SOURCE, on(ETO, row("SLICE", 400, 406))), 0,
         "RESULT: PASS"),
        ("a selected comparison is judged on the BRAM tile ceiling", SET,
         (SOURCE, *raised, on(ASLH, row("BRAM_TILE", 4.5, 5.5))), 1,
         (("directive AltSpreadLogic_high selected", "REGRESSION: 5.5 exceeds the ceiling 5.0"), None)),
        ("a route not selected is not judged on the BRAM tile ceiling", SET,
         (SOURCE, on(ETO, row("BRAM_TILE", 4.5, 5.5))), 0, (("RESULT: PASS",), "ceiling")),
        ("a tie between the comparisons goes to the directive the recipe lists first", REVERSED,
         (*raised, *slack("WNS", "  0.300  ", "  0.600  ", ETO)), 0, "directive AltSpreadLogic_high selected"),
        ("a tie with the shipping route goes to the shipping route", REVERSED,
         slack("WNS", "  0.400  ", "  0.500  ", ASLH), 0, "directive ExtraPostPlacementOpt selected"),
        ("a route neither in a set nor marked", (), (), 2, "or alone with --shipping-selection"),
        ("a route both in a set and marked", (*SET, "--shipping-selection"), (), 2,
         "or alone with --shipping-selection"),
        ("a set of one comparison", SET[:2], (), 2,
         f"a route set holds each of {FAMILY} once, not AltSpreadLogic_high, ExtraPostPlacementOpt"),
        ("a set naming one comparison twice", SET[:2] * 2, (), 2,
         "once, not AltSpreadLogic_high, AltSpreadLogic_high, ExtraPostPlacementOpt"),
        ("a set of a selected split placement", (*SET, "--placement", "f0-f4"), (), 2,
         "a selected split placement is judged alone"),
        ("a marked route names its directive", ("--shipping-selection",), (), 0,
         (("directive ExtraPostPlacementOpt: the one route, marked as the shipping selection", "RESULT: PASS"),
          "route set")),
        ("a comparison opening another checkpoint", SET,
         ((ASLH + COMPARISON, "/gateware/alinx_ax7101_synth.dcp", "/other/alinx_ax7101_synth.dcp"),), 2,
         "does not open the shipping checkpoint"),
        ("a comparison of another thread setting", SET, ((ASLH + COMPARISON, "maxThreads 32", "maxThreads 16"),), 2,
         "sets 'set_param general.maxThreads 16', not the shipping route's 'set_param general.maxThreads 32'"),
        ("a comparison running another command", SET,
         ((ETO + COMPARISON, "route_design -directive AggressiveExplore", "route_design -directive Explore"),), 2,
         "is not the script the recipe writes"),
        ("a comparison at the shipping directive", SET,
         ((ASLH + COMPARISON, "-directive AltSpreadLogic_high", "-directive ExtraPostPlacementOpt"),), 2,
         "is not the script the recipe writes"),
        ("a comparison at a directive outside the recipe", SET,
         ((ASLH + COMPARISON, "-directive AltSpreadLogic_high", "-directive Default"),), 2,
         "is not the script the recipe writes"),
        ("a comparison without its script", SET, ((ASLH + COMPARISON, None, None),), 2, COMPARISON),
        ("a set whose shipping route is not at the shipping directive", SET,
         ((FLOW, "ExtraPostPlacementOpt", "ExtraTimingOpt"),), 2, "is not a shipping route the recipe compares"),
        ("a comparison of another tool build, not selected", SET,
         ((ETO + "baseline_utilization.rpt", "Build 6511674", "Build 6511675"),), 2, "tool or recipe change in tool"),
        ("an incomplete comparison route, not selected", SET, (on(ETO, ERRORS),), 1,
         "ROUTE INCOMPLETE: ExtraTimingOpt: 3 nets with routing errors"),
        ("a comparison's corners of another run", SET, ((ETO + CORNERS["Slow_0C"], "  0.300  ", "  0.250  "),), 2,
         "worst WNS_ns is 0.25 and the timing summary's 0.3"),
        ("a comparison without a corner report", SET, ((ETO + CORNERS["Fast_85C"], None, None),), 2,
         "alinx_ax7101_signoff_Fast_85C_timing.rpt"),
        ("a comparison with a wrong population", SET,
         ((ETO + "baseline_hierarchy.rpt", "| KL_adp_engine |", "| KL_adp_other |"),), 2,
         "ExtraTimingOpt: wrong placement all-fabric: adp (KL_adp_engine)"),
        ("the shipping route not selected, measured differently from the record's inputs", SET,
         (*raised, row("LUT", 1000, 1001)), 2, "identical inputs"),
    )


def comparisons(gateware: Path) -> list[Path]:
    """Write the recipe's comparison routes beside the shipping route, as its snippet writes them; return them.

    Each holds the shipping route's other reports and its own worst-corner WNS in its timing summary and corners.
    """
    from pp_resource_gate_selftest import report_header
    tail = (gateware / "baseline_integrated.tcl").read_text().partition("# Add pre-optimize commands")[2]
    header, folders = report_header("alinx_ax7101", "Physopt postRoute"), []
    for directive, wns in OTHERS.items():
        folder = gateware.parent / f"ax7101-{directive}"
        folder.mkdir()
        for name in ("baseline_utilization.rpt", "baseline_hierarchy.rpt", "baseline_cells.tsv",
                     "alinx_ax7101_route_status.rpt"):
            shutil.copy2(gateware / name, folder / name)
        (folder / COMPARISON).write_text(
            f"set_param general.maxThreads 32\nopen_checkpoint {{{gateware}/alinx_ax7101_synth.dcp}}\n"
            + tail.replace("place_design -directive ExtraPostPlacementOpt", f"place_design -directive {directive}"))
        (folder / TIMING).write_text(header + summary(wns, "0.100"))
        corner_reports(folder, header, wns)
        folders.append(folder)
    return folders


def prepared(tmp: Path, plants: tuple) -> tuple[Path, dict[str, str]]:
    """A fresh shipping route and its comparison routes with the plants made; return it and each {name}'s path."""
    import pp_resource_gate_selftest as base
    folder = base.fresh(tmp / "route", "route")
    where = {"{repo}": str(tmp / "route/arm/repo"),
             **{f"{{{directive}}}": str(path) for directive, path in zip(OTHERS, comparisons(folder))}}
    for name, old, new in plants:
        for key, value in where.items():
            name = name.replace(key, value)
        base.plant(folder, name, old, new)
    return folder, where


def set_arms(tmp: Path, entries: dict) -> int:
    """Run every route-set arm, the standalone refusals and the set's re-record through main(); return the count."""
    import pp_resource_gate_selftest as base
    path, table = base.baseline_file(tmp, entries, None), set_arms_table()
    for label, options, plants, wanted, needle in table:
        folder, where = prepared(tmp, plants)
        status, lines = base.cli("check", folder, "--endpoint", "route", *(where.get(item, item) for item in options),
                                 "--baseline", path)
        base.expect(f"route-set arm {label!r}", status, lines, wanted, needle)
        print(f"resource gate route-set arm: {label}: exit {status} PASS")
    standalone = base.fresh(tmp / "ooc", "ooc")
    for options in (("--shipping-selection",), ("--comparison", standalone)):
        status, lines = base.cli("check", standalone, "--endpoint", "ooc", *options, "--baseline", path)
        base.expect(f"route-set arm 'a standalone synthesis with {options[0]}'", status, lines, 2,
                    "a standalone synthesis has no placement directive")
        print(f"resource gate route-set arm: a standalone synthesis with {options[0]}: exit 2 PASS")
    re_record(tmp, entries)
    return len(table) + 3


def re_record(tmp: Path, entries: dict) -> None:
    """record --write of a set replaces the route record with the selected route's, its flow naming its directive."""
    import pp_resource_gate_selftest as base
    path = base.baseline_file(tmp, entries, None)
    folder, where = prepared(tmp, slack("WNS", "  0.400  ", "  0.600  ", ASLH))
    options = [where.get(item, item) for item in SET]
    status, lines = base.cli("record", folder, "--endpoint", "route", *options, "--baseline", path, "--write")
    written = json.loads(path.read_text())["endpoints"]["route"]["record"]
    if status != 0 or "directive AltSpreadLogic_high selected: the best worst-corner WNS, 0.6 ns" not in lines \
            or "place_design -directive AltSpreadLogic_high" not in written["identity"]["flow"] \
            or written["figures"]["WNS_ns"] != 0.6 or written["scopes"] != entries["route"]["record"]["scopes"]:
        raise AssertionError(f"record --write of a set exited {status} or wrote another route: {ascii(lines[:8])}")
    status, lines = base.cli("check", folder, "--endpoint", "route", *options, "--baseline", path)
    base.expect("route-set arm 'the re-recorded set against its own record'", status, lines, 0,
                (("directive AltSpreadLogic_high selected", "RESULT: PASS"), "REGRESSION"))
    print("resource gate route-set arm: record --write of a set stores the selected route, then passes: PASS")
