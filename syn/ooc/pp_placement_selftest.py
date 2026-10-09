#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
"""Selected-placement controls: execute Tcl and judge complete measurement fixtures."""

import contextlib
import copy
import io
import json
from pathlib import Path
import subprocess
import sys
import tempfile

import pp_placement as placement


# Independent oracle: the expected one-interface population, not limits().
COUNTS = {
    "all-fabric": (1, 1, 1, 1, 1, 1, 0, 1, 1, 0, 1),
    "f0-f4": (1, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1),
    "full-split": (0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1),
}
ROLES = ("wrapper", "adp", "acmp-listener", "acmp-talker", "srp", "maap",
         "processor-maap", "aecp", "notify", "mailbox", "gptp")
MODULES = ("KL_pp_shadow", "KL_adp_engine", "KL_pp_acmp_listener", "KL_acmp_talker", "KL_srp_top",
           "KL_maap", "KL_pp_maap", "KL_aecp_engine", "KL_aecp_notify", "KL_mbx", "KL_gptp_shadow")


def hierarchy_fixture(kind: str, prefix: list[str]) -> list[str]:
    """Complete the route's control population while retaining legacy resource rows."""
    lines = [f"| {'  ' * depth}{name} | m{depth} | {900 - depth} | {900 - depth} | 0 | 0 | 50 | 1 | 0 | 0 |"
             for depth, name in enumerate(prefix + ["u_pp", "u_srp"])]
    if kind == "route":
        lines[2] = lines[2].replace("| m2 |", "| KL_pp_shadow |")
        lines[4] = lines[4].replace("| m4 |", "| KL_srp_top |")
        for depth, name, module in (
                (4, "u_adp", "KL_adp_engine"), (4, "u_listener", "KL_pp_acmp_listener"),
                (4, "u_talker", "KL_acmp_talker"), (4, "u_aecp", "KL_aecp_engine"),
                (4, "u_notify", "KL_aecp_notify"), (2, "g_maap.maap_engine", "KL_maap"),
                (2, "g_gptp_plane.u_gptp_shadow", "KL_gptp_shadow")):
            lines.append(f"| {'  ' * depth}{name} | {module} | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |")
    return lines


def census_text(selected: str, counts: tuple[int, ...]) -> str:
    """Write a synthetic observed population using the independently specified roles."""
    return "placement\trole\tcount\n" + "".join(
        f"{selected}\t{role}\t{count}\n" for role, count in zip(ROLES, counts))


def run_tcl(root: Path, selected: str, counts: tuple[int, ...], report: bool) -> subprocess.CompletedProcess:
    """Execute the real census Tcl against a controlled retained-module query."""
    observed = " ".join(f"{module} {count}" for module, count in zip(MODULES, counts))
    script = f"set observed {{{observed}}}\n" + '''
proc get_cells {args} {
  global observed
  set filter [lindex $args end]
  if {![regexp {^ORIG_REF_NAME == (\\w+) \\|\\| REF_NAME == (\\w+)$} $filter -> original reference]
      || $original ne $reference || ![dict exists $observed $original]} {
    error "unexpected module identity query: $filter"
  }
  return [lrepeat [dict get $observed $original] instance]
}
'''
    script += placement.census_tcl(selected, report)
    path = root / "placement.tcl"
    path.write_text(script)
    return subprocess.run(["tclsh", str(path)], cwd=root, capture_output=True, text=True, timeout=10)


def tcl_selftest(root: Path) -> None:
    """Kill every retained/removed-role reversal in both census execution stages."""
    for selected, counts in COUNTS.items():
        for report in (False, True):
            result = run_tcl(root, selected, counts, report)
            if result.returncode != 0:
                raise AssertionError(f"{selected} census control: {result.stderr}")
            if report and (root / placement.REPORT).read_text() != census_text(selected, counts):
                raise AssertionError("emitted placement census differs from the independent oracle")
            for index, role in enumerate(ROLES):
                changed = list(counts)
                changed[index] = 2 if selected == "f0-f4" and role == "wrapper" else 1 - changed[index]
                result = run_tcl(root, selected, tuple(changed), report)
                if result.returncode == 0 or f"wrong placement {selected}: {role} (" not in result.stderr:
                    raise AssertionError(f"{selected} {role}: missing named Tcl refusal: {result.stderr}")
        print(f"placement Tcl {selected}: control and every role reversal at synthesis/route PASS")


def recipe_selftest(gateware: Path, standalone: Path, log: Path, source: str, verilog: str) -> None:
    """Preserve legacy recipes; allow only the selected population's removed ROMs."""
    import pp_baseline as recipe
    code = ("import importlib.util, sys; "
            "spec = importlib.util.spec_from_file_location('baseline', sys.argv[1]); "
            "module = importlib.util.module_from_spec(spec); spec.loader.exec_module(module)")
    subprocess.run([sys.executable, "-I", "-B", "-c", code, str(Path(recipe.__file__).resolve())],
                   cwd=gateware, check=True, capture_output=True, text=True, timeout=10)
    recipe.prepare(gateware, gateware, None, False)
    control = (gateware / "baseline_integrated.tcl").read_bytes()
    recipe.main([str(gateware), "--placement", "all-fabric"])
    if (gateware / "baseline_integrated.tcl").read_bytes() != control:
        raise AssertionError("explicit all-fabric changed the original recipe")
    generated = gateware / "alinx_ax7101.v"
    try:
        for selected, absent in (("f0-f4", ("PP_TROM_HEX_P",)),
                                 ("full-split", ("PP_TROM_HEX_P", "PP_UCODE_HEX_P"))):
            text = "\n".join(line for line in verilog.splitlines() if not any(key in line for key in absent))
            generated.write_text(text)
            recipe.main([str(gateware), "--placement", selected, "--single-thread-synthesis"])
            script = (gateware / "baseline_integrated.tcl").read_text()
            before = script.index("synth_design ")
            after = script.index("# Add pre-optimize commands")
            if not script.startswith("set_param synth.maxThreads 1\n"):
                raise AssertionError("split recipe lost synthesis worker identity")
            promotion = "set_msg_config -id {Synth 8-4445} -new_severity ERROR\n"
            if script.count(promotion) != 1 or script.index(promotion) > before:
                raise AssertionError("split recipe lost pre-synthesis ROM enforcement")
            if not before < script.index("wrong placement") < after:
                raise AssertionError("placement check must execute after synthesis, before implementation")
            if script.count("wrong placement") != 22 or "baseline_pp_utilization.rpt" in script:
                raise AssertionError("split recipe lacks both censuses or still assumes a wrapper")
            if "No internal timing path for selected image" not in script:
                raise AssertionError("selected image timing absent")
            images = json.loads((gateware / "baseline_images.json").read_text())
            if len(images) != 5 - len(absent):
                raise AssertionError("removed protocol ROM still required or retained ROM missing")
            with recipe.expect_refusal("ambiguous image or geometry source: GPTP_UCODE_HEX_P"):
                generated.write_text(text.replace("GPTP_UCODE_HEX_P", "MISSING_P"))
                recipe.inventory(gateware, source, selected)
            generated.write_text(text)
            for options in (["--integrated-log", str(log), "--output", str(standalone)],
                            ["--attribution-only"], ["--output", str(standalone)]):
                stderr = io.StringIO()
                with contextlib.redirect_stderr(stderr), recipe.expect_refusal("2", SystemExit):
                    recipe.main([str(gateware), "--placement", selected, *options])
                if "selected split placement requires" not in stderr.getvalue():
                    raise AssertionError("wrong split endpoint refusal")
        generated.write_text(verilog.replace("PP_UCODE_HEX_P", "MISSING_P"))
        with recipe.expect_refusal("ambiguous image or geometry source: PP_UCODE_HEX_P"):
            recipe.inventory(gateware, source, "f0-f4")
        tcl_selftest(gateware)
    finally:
        generated.write_text(verilog)
    print("placement recipe: legacy parity, split preparation, ROM and endpoint refusals PASS")


def selected_fixture(root: Path, selected: str) -> Path:
    """Build a split fixture with no wrapper source or wrapper hierarchy."""
    from pp_resource_gate_selftest import fixture
    folder = fixture(root, "route")
    wrapper = root / "repo/hdl/milan/KL_pp_shadow.sv"
    datapath = wrapper.with_name("milan_datapath.sv")
    wrapper.rename(datapath)
    datapath.write_text("module milan_datapath; endmodule\n")
    script = folder / "baseline_integrated.tcl"
    script.write_text(placement.MARKER + selected + "\n" + script.read_text().replace(str(wrapper), str(datapath)))
    hierarchy = folder / "baseline_hierarchy.rpt"
    hierarchy.write_text("\n".join(hierarchy.read_text().splitlines()[:2]) + "\n")
    counts = list(COUNTS[selected])
    counts[0] = 0
    (folder / placement.REPORT).write_text(census_text(selected, tuple(counts)))
    return folder


def expect_case(label: str, result: tuple[int, list[str]], status: int, reason: str) -> None:
    """Require the precise verdict and named evidence for every planted case."""
    code, lines = result
    if code != status or reason not in "\n".join(lines):
        raise AssertionError(f"{label}: wanted {status} / {reason}, got {result}")
    print(f"placement gate {label}: expected exit {status}, {reason}: PASS")


def all_fabric_selftest(root: Path, baseline: Path) -> None:
    """Refuse unmarked wrong populations in both comparisons and acceptance writes."""
    from pp_resource_gate_selftest import cli, fixture
    folder = fixture(root / "all-fabric", "route")
    arguments = (folder, "--endpoint", "route-1x1", "--baseline", baseline)
    report = folder / "baseline_hierarchy.rpt"
    original = report.read_text()
    baseline_bytes = baseline.read_bytes()
    expect_case("all-fabric unmarked control", cli("check", *arguments), 0, "RESULT: PASS")
    plants = []
    for role, module, count in zip(ROLES, MODULES, COUNTS["all-fabric"]):
        matching = next((line for line in original.splitlines(keepends=True) if f"| {module} |" in line), None)
        if count:
            plants.append((role + " absent", original.replace(matching, ""), (role,)))
            duplicate = matching.replace(matching.split("|")[1], "  duplicate_" + role + " ", 1)
        else:
            duplicate = f"|   unexpected_{role} | {module} | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |\n"
        plants.append((role + " excess", original + duplicate, (role,)))
    removed = ("adp", "acmp-listener", "acmp-talker", "srp", "maap")
    removed_modules = {MODULES[ROLES.index(role)] for role in removed}
    split = "".join(line for line in original.splitlines(keepends=True)
                    if line.split("|")[2].strip() not in removed_modules)
    plants.append(("wrapper-retaining f0-f4 without marker", split, removed))
    try:
        for label, changed, roles in plants:
            report.write_text(changed)
            for command in (("check",), ("record", "--write")):
                result = cli(*command, *arguments)
                for role in roles:
                    expect_case(label + " " + command[0], result, 2, f"{role} ({MODULES[ROLES.index(role)]})")
                if baseline.read_bytes() != baseline_bytes:
                    raise AssertionError("wrong all-fabric population changed acceptance baseline")
        # Own-logic rows repeat module names; specializations retain their identity.
        valid = original
        for module in MODULES:
            valid = valid.replace(f"| {module} |", f"| {module}__parameterized12 |")
        valid += "|   (own) | KL_pp_shadow | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |\n"
        valid += "|   shim | KL_pp_maap_shim | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |\n"
        report.write_text(valid)
        expect_case("all-fabric own rows and specialized modules", cli("check", *arguments), 0, "RESULT: PASS")
        report.write_text(valid.replace("KL_adp_engine__parameterized12", "KL_adp_engine_impostor"))
        expect_case("all-fabric module prefix is insufficient", cli("check", *arguments), 2, "adp (KL_adp_engine)")
    finally:
        report.write_text(original)


def gate_selftest() -> None:
    """Compare split routes against unchanged policy and refuse mislabelled populations."""
    import pp_resource_gate as gate
    from pp_resource_gate_selftest import POLICY, cli, fixture, row
    with tempfile.TemporaryDirectory(prefix="pp-placement-gate-") as tmp:
        root = Path(tmp)
        original = fixture(root / "base", "route")
        entry = {"record": gate.record(original, "route"), **copy.deepcopy(POLICY)}
        baseline = root / "baseline.json"
        baseline.write_text(json.dumps({"endpoints": {"route-1x1": entry}}))
        baseline_bytes = baseline.read_bytes()
        all_fabric_selftest(root, baseline)
        for selected in ("f0-f4", "full-split"):
            folder = selected_fixture(root / selected, selected)
            arguments = (folder, "--endpoint", "route-1x1", "--baseline", baseline,
                         "--placement", selected)
            expect_case(selected, cli("check", *arguments), 0, f"placement {selected}")
            recipe = folder / "baseline_integrated.tcl"
            original_script = recipe.read_text()
            marker = placement.MARKER + selected + "\n"
            for label, changed in (("absent selection", original_script.replace(marker, "")),
                                   ("duplicate selection", marker + original_script),
                                   ("wrong selection", original_script.replace(marker,
                                                                              placement.MARKER + "all-fabric\n"))):
                recipe.write_text(changed)
                expect_case(selected + " " + label, cli("check", *arguments), 2, "recipe names")
            recipe.write_text(original_script)
            candidate = gate.record(folder, "route", selected)
            if gate.shape_problems(selected, {"record": candidate, **POLICY}):
                raise AssertionError("split measurement departed from the existing acceptance record shape")
            script = recipe.read_text()
            if gate.inputs(folder, script, "f0-f4") == gate.inputs(folder, script, "full-split"):
                raise AssertionError("input identity omits selected placement")
            if candidate["identity"] != entry["record"]["identity"] or "image" not in candidate["scopes"]:
                raise AssertionError("split measurement changed flow identity or omitted whole-image scopes")
            if "no scope deltas claimed" not in "\n".join(gate.scope_deltas(entry["record"]["scopes"],
                                                                                          candidate["scopes"])):
                raise AssertionError("changed attribution roots reported as engine-removal savings")
            expect_case(selected + " unselected", cli("check", folder, "--endpoint", "route-1x1",
                                                       "--baseline", baseline), 2, "wrong placement")
            expect_case(selected + " re-record", cli("record", *arguments, "--write"), 2, "M9")
            gate_refusals(folder, selected, arguments)
            for figure, before, after, reason in (("RAMB36", 4, 5, "RAMB36"),
                                                  ("BRAM_TILE", 4.5, 5.5, "ceiling"),
                                                  ("LUT", 1000, 1011, "LUT")):
                filename, old, new = row(figure, before, after)
                report = folder / filename
                pristine = report.read_text()
                report.write_text(pristine.replace(old, new))
                expect_case(selected + " " + reason, cli("check", *arguments), 1, reason)
                report.write_text(pristine)
            for filename, old, new, reason in (
                    ("baseline_timing.rpt", "0.100", "-0.001", "WHS_ns"),
                    ("alinx_ax7101_route_status.rpt", "fully routed nets............. :         100",
                     "fully routed nets............. :          99", "ROUTE INCOMPLETE"),
                    ("baseline_utilization.rpt", "Build 6511674", "Build 6511675", "tool or recipe change")):
                report = folder / filename
                pristine = report.read_text()
                report.write_text(pristine.replace(old, new))
                expect_case(selected + " " + reason, cli("check", *arguments),
                            2 if "recipe" in reason else 1, reason)
                report.write_text(pristine)
        if baseline.read_bytes() != baseline_bytes:
            raise AssertionError("selected measurements changed acceptance baseline")
        print("placement gate: unchanged acceptance schema, record and policy PASS")


def gate_refusals(folder: Path, selected: str, arguments: tuple) -> None:
    """Plant wrong ownership, missing evidence and malformed role counts independently."""
    from pp_resource_gate_selftest import cli
    report = folder / placement.REPORT
    original = report.read_text()
    counts = list(COUNTS[selected])
    counts[0] = 0
    plants = [("missing census", None, placement.REPORT),
              ("wrong header", original.replace("placement\trole", "placement\towner"), "header"),
              ("wrong placement", original.replace(selected, "all-fabric"), "wrong placement"),
              ("missing wrapper row", "\n".join(line for line in original.splitlines()
                                                 if "\twrapper\t" not in line), "missing roles"),
              ("duplicate row", original + original.splitlines()[1] + "\n", "duplicate"),
              ("invalid count", original.replace("\t0\n", "\t-1\n", 1), "invalid")]
    for index, role in enumerate(ROLES):
        changed = counts.copy()
        changed[index] = 2 if selected == "f0-f4" and role == "wrapper" else 1 - changed[index]
        plants.append((role, census_text(selected, tuple(changed)), f"{role} ({MODULES[index]})"))
    for label, text, reason in plants:
        if text is None:
            report.unlink()
        else:
            report.write_text(text)
        expect_case(selected + " " + label, cli("check", *arguments), 2, reason)
        report.write_text(original)
