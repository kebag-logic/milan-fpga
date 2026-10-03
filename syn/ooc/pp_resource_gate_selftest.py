#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
"""Plant every regression and refusal the resource gate claims, end to end.

Each arm copies a synthetic recipe measurement directory, edits the report or
input text a real regression would change, reads it back through the gate's
own parser and judges it against a baseline recorded from the pristine copy.
No arm hands the comparator a hand-built record, so a parser that stops seeing
a row fails here exactly as it would on a real report.
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
          "floor": {"WNS_ns": 0.0, "WHS_ns": 0.0}, "ceiling": {"BRAM_TILE": 5.0}}
LABELS = {"LUT": "Slice LUTs", "FF": "Slice Registers", "SLICE": "Slice", "BRAM_TILE": "Block RAM Tile",
          "RAMB36": "RAMB36/FIFO*", "RAMB18": "RAMB18", "DSP": "DSPs"}
#: The distribution table repeats the register row, as the vendor report does.
REPEATED = "| Slice Registers                            | 2000 |     0 |\n"


def report_header(design: str, state: str) -> str:
    """The vendor header block every report starts with."""
    return ("| Tool Version : Vivado v.2026.1 (lin64) Build 6511674 Tue Jun 16 11:01:26 MDT 2026\n"
            f"| Design       : {design}\n| Device       : xc7a100tfgg484-2\n"
            f"| Design State : {state}\n")


def write_reports(folder: Path, kind: str) -> None:
    """Write utilization, timing, hierarchy and cell census as Vivado lays them out."""
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
                   "place_design -directive ExtraPostPlacementOpt\nroute_design -directive AggressiveExplore\n")
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
    ("WNS below the floor", (SOURCE, (TIMING, "  0.500  ", " -0.010  ")), 1, "below the floor"),
    ("WNS fell more than the tolerance", (SOURCE, (TIMING, "  0.500  ", "  0.200  ")), 1, "fell by"),
    ("WNS fell within the tolerance", (SOURCE, (TIMING, "  0.500  ", "  0.300  ")), 0, "RESULT: PASS"),
    ("WHS below the floor", (SOURCE, (TIMING, "0.100", "-0.001")), 1, "WHS_ns"),
    ("LUT improvement", (SOURCE, row("LUT", 1000, 950)), 0, "ratchet down"),
    ("tool build changed", (("baseline_utilization.rpt", "Build 6511674", "Build 6511675"),), 2, "tool"),
    ("device changed", (("baseline_utilization.rpt", "xc7a100tfgg484-2", "xc7a200tfbg484-2"),), 2, "device"),
    ("placement directive changed", (("baseline_integrated.tcl", "ExtraPostPlacementOpt", "ExtraTimingOpt"),),
     2, "flow"),
    ("thread count changed", (("baseline_integrated.tcl", "maxThreads 32", "maxThreads 16"),), 2, "flow"),
    ("identical inputs, different figures", (row("LUT", 1000, 1001),), 2, "identical inputs"),
    ("export date only", (row("LUT", 1000, 1001), ("alinx_ax7101.v", "morning", "evening")), 2, "identical inputs"),
    ("generated logic changed", (row("LUT", 1000, 1011), ("alinx_ax7101.v", "endmodule", "wire g; endmodule")),
     1, "LUT"),
    ("include header changed", (row("LUT", 1000, 1011), ("{repo}/hdl/common/shape.svh", "2", "9")), 1, "LUT"),
    ("sourced constraint changed", (row("LUT", 1000, 1011), ("{repo}/sw/constraints.tcl", "proc kl", "proc kx")), 1, "LUT"),
    ("memory image changed", (row("LUT", 1000, 1011), ("baseline_images.json", '"ab"', '"cd"')), 1, "LUT"),
    ("duplicate conflicting row", (("baseline_utilization.rpt", "| DSPs", "| DSPs | 9 |\n| DSPs"),), 2, "DSPs"),
    ("malformed count", (row("SLICE", 400, "x"),), 2, "not a count"),
    ("missing Slice row", (("baseline_utilization.rpt", f"| {'Slice':<20} | 400 | 0 | 0 | 9 | 1.0 |\n", ""),),
     2, "'Slice' has values []"),
    ("timing columns changed", ((TIMING, "WHS(ns)", "WXS(ns)"),), 2, "columns"),
    ("missing timing report", ((TIMING, None, None),), 2, "baseline_timing.rpt"),
    ("cell census header changed", (("baseline_cells.tsv", "cell\tprimitive", "cell\tref"),), 2, "header changed"),
    ("second recipe script", (("baseline_ooc.tcl", None, "quit\n"),), 2, "recipe scripts"),
)
OOC_ARMS = (
    ("standalone control", (), 0, "RESULT: PASS"),
    ("standalone clock changed", (("clock.xdc", "20.000", "10.000"),), 2, "standalone_clock_ns"),
    ("generic changed", (row("LUT", 1000, 1011), ("baseline_ooc.tcl", "N_STREAM_IN_P=2", "N_STREAM_IN_P=9")),
     1, "LUT"),
    ("image path moved, same image", (row("LUT", 1000, 1001), ("baseline_ooc.tcl", "/ucode.hex", "/x/ucode.hex")),
     2, "identical inputs"),
    ("standalone RAMB18", (SOURCE, row("RAMB18", 1, 2)), 1, "RAMB18"),
    ("standalone FF", (SOURCE, row("FF", 2000, 2011),
                       ("baseline_utilization.rpt", REPEATED, REPEATED.replace("2000", "2011"))), 1, "FF"),
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


def run_arm(root: Path, kind: str, arm: tuple, entry: dict) -> None:
    """Plant one arm on a fresh copy and require its exact verdict and reason."""
    label, plants, expected, needle = arm
    folder = fresh(root, kind)
    for name, old, new in plants:
        plant(folder, name.replace("{repo}", str(root / "arm/repo")), old, new)
    try:
        status, lines = gate.judge(entry, gate.record(folder, gate.kind_of(folder)))
    except gate.Refusal as error:
        status, lines = 2, [str(error)]
    if status != expected or needle not in "\n".join(lines):
        raise AssertionError(f"{kind} arm {label!r}: exit {status}, wanted {expected} naming {needle!r}\n"
                             + "\n".join(lines))
    print(f"resource gate {kind} arm: {label}: exit {status} PASS")


def recorded(root: Path, kind: str) -> dict:
    """Build the fixture where arms are planted, record it, then keep it pristine."""
    folder = fixture(root / "arm", kind)
    entry = copy.deepcopy(POLICY)
    entry["record"] = gate.record(folder, kind)
    (root / "arm").rename(root / "pristine")
    return entry


def scope_and_baseline_arms(root: Path, entry: dict) -> int:
    """Check sub-block CARRY4 attribution, baseline self-consistency and the command line."""
    if entry["record"]["scopes"]["u_pp/u_srp"]["CARRY4"] != 3 or entry["record"]["figures"]["CARRY4"] != 4:
        raise AssertionError(f"CARRY4 attribution wrong: {entry['record']}")
    baseline = {"endpoints": {"route": entry}}
    if gate.check_baseline(baseline):
        raise AssertionError("a consistent baseline was refused")
    broken = (("tolerance", "LUT", None, "LUT has no non-negative tolerance"),
              ("tolerance", "DSP", -1, "DSP has no non-negative tolerance"),
              ("floor", "WNS_ns", None, "WNS_ns has no floor"),
              ("floor", "WHS_ns", 1.0, "WHS_ns is below its floor"),
              ("ceiling", "BRAM_TILE", 1.0, "BRAM_TILE exceeds its ceiling"))
    for field, figure, value, message in broken:
        changed = copy.deepcopy(baseline)
        if value is None:
            del changed["endpoints"]["route"][field][figure]
        else:
            changed["endpoints"]["route"][field][figure] = value
        if not any(message in problem for problem in gate.check_baseline(changed)):
            raise AssertionError(f"baseline defect accepted: {message}")
    path = root / "baseline.json"
    path.write_text(json.dumps(baseline))
    folder = str(fresh(root, "route"))
    with contextlib.redirect_stdout(io.StringIO()):
        statuses = [gate.main(["check", folder, "--endpoint", "route", "--baseline", str(path)]),
                    gate.main(["check-baseline", "--baseline", str(path)]),
                    gate.main(["record", folder, "--endpoint", "copy", "--baseline", str(path), "--write"])]
        written = json.loads(path.read_text())["endpoints"]["copy"]["record"]
        plant(Path(folder), *row("LUT", 1000, 1011))
        plant(Path(folder), "baseline_images.json", '"ab"', '"cd"')
        statuses.append(gate.main(["check", folder, "--endpoint", "route", "--baseline", str(path)]))
        statuses.append(gate.main(["check-baseline", "--baseline", str(path)]))
    if statuses != [0, 0, 0, 1, 2] or written != entry["record"]:
        raise AssertionError(f"command line verdicts or recording wrong: {statuses}")
    print(f"resource gate CARRY4, {len(broken)} baseline refusals and 5 command-line verdicts PASS")
    return len(broken) + 6


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
        count += scope_and_baseline_arms(Path(tmp) / "route", entries["route"])
        status, lines = gate.judge(entries["route"], entries["ooc"]["record"])
        if status != 2 or "endpoint kind" not in lines[0]:
            raise AssertionError("a standalone record was compared with an integrated baseline")
        count += 1
    print(f"resource gate selftest: {count} arms PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(selftest())
