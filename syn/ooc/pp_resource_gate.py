#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
"""Reject a material resource or timing regression of the protocol processor.

Issue #234. The baseline recipe (docs/testing/PP_SHADOW_BASELINE_RECIPE.md)
leaves one Vivado measurement directory per endpoint: the integrated shipping
route, or the standalone wrapper synthesis. This gate reads one directory into
a record and compares it with the endpoint recorded in
syn/ooc/pp_resource_baseline.json, whose policy fields (tolerance, floor,
ceiling) docs/design/AREA_BUDGET.md documents.

A record has three parts. The identity is the tool build, device, design,
design state and flow commands: a different identity is a tool or recipe
change, so the gate refuses to compare instead of calling the delta a
regression. The input digest covers every source, include header, constraint,
sourced Tcl file, generic and memory image the script reads: equal digests
with different figures are refused too, because nothing in the design moved.
Only a measurement with the baseline's identity and different inputs is
judged against the tolerances. A route is also judged on its route status
report: an unrouted net or a routing error means the image does not fit.

Exit status: 0 within tolerance; 1 a material regression, an incomplete route
included; 2 not comparable, an unreadable measurement or an unusable baseline,
each with its reason and never through a traceback. A gated figure that
improved by more than its tolerance still exits 0 and prints "re-baseline
recommended". check and check-baseline both read the baseline through one
validator first: strict JSON, then every field of the recorded shape and every
number finite. check-baseline then exits 2 when an endpoint's policy is
incomplete, its own record breaks it, or it differs from the policy table of
the budget page. Every count read from a report is ASCII digits.

    pp_resource_gate.py check <directory> --endpoint route-1x1
    pp_resource_gate.py record <directory> --endpoint route-1x1 [--write]
    pp_resource_gate.py check-baseline
    pp_resource_gate.py --selftest
"""

import argparse
import hashlib
import json
import math
from pathlib import Path
import re
import sys

from pp_baseline_rank import hierarchy


BASELINE = Path(__file__).with_name("pp_resource_baseline.json")
#: The page whose policy table every baseline endpoint must equal.
BUDGET = Path(__file__).resolve().parents[2] / "docs/design/AREA_BUDGET.md"
#: Utilization row label -> record figure; every label must appear, with one value.
ROWS = {"route": {"Slice LUTs": "LUT", "Slice Registers": "FF", "Slice": "SLICE",
                  "Block RAM Tile": "BRAM_TILE", "RAMB36/FIFO": "RAMB36",
                  "RAMB18": "RAMB18", "DSPs": "DSP"},
        "ooc": {"Slice LUTs": "LUT", "Slice Registers": "FF", "Block RAM Tile": "BRAM_TILE",
                "RAMB36/FIFO": "RAMB36", "RAMB18": "RAMB18", "DSPs": "DSP"}}
#: Figures judged against a tolerance. A timing figure regresses when it falls.
GATED = {"route": ("LUT", "FF", "SLICE", "RAMB36", "RAMB18", "DSP", "WNS_ns", "WHS_ns"),
         "ooc": ("LUT", "FF", "RAMB36", "RAMB18", "DSP")}
TIMING = ("WNS_ns", "WHS_ns")
#: Ceilings an endpoint of each kind must carry.
CEILINGS = {"route": ("BRAM_TILE",), "ooc": ()}
#: The budget's policy table: column -> the policy field and the figures it sets.
COLUMNS = {"LUT": ("tolerance", ("LUT",)), "FF": ("tolerance", ("FF",)), "Slice": ("tolerance", ("SLICE",)),
           "RAMB36": ("tolerance", ("RAMB36",)), "RAMB18": ("tolerance", ("RAMB18",)),
           "DSP": ("tolerance", ("DSP",)), "WNS floor": ("floor", ("WNS_ns",)),
           "WHS floor": ("floor", ("WHS_ns",)), "Timing fall": ("tolerance", TIMING),
           "BRAM tile ceiling": ("ceiling", ("BRAM_TILE",))}
POLICY = ("tolerance", "floor", "ceiling")
RECORD = ("kind", "identity", "inputs_sha256", "figures", "scopes")
#: The identity fields a record holds, each with the type it is recorded as.
IDENTITY = {"tool": str, "device": str, "design": str, "state": str, "flow": list, "standalone_clock_ns": list}
#: The counts every sub-block scope of a record holds.
SCOPE = ("LUT", "FF", "RAMB36", "RAMB18", "DSP", "CARRY4")
#: Notes a baseline file and each endpoint may carry beside the fields the gate reads.
NOTES = {"file": ("schema", "description"), "endpoint": ("measured",)}
#: A count as a report prints it: ASCII digits only, never another script's digit that int() would take.
COUNT = re.compile(r"[0-9]+")
#: A slack as the timing summary prints it: a finite decimal in ASCII digits.
SLACK = re.compile(r"-?[0-9]+\.[0-9]+")
SCRIPTS = {"route": "baseline_integrated.tcl", "ooc": "baseline_ooc.tcl"}
ROOTS = {"route": "alinx_ax7101/milan_datapath/pp_shadow", "ooc": "KL_pp_shadow"}
FLOW = re.compile(r"^(create_project|set_param|synth_design|opt_design|place_design"
                  r"|phys_opt_design|route_design|kl_timing_grade_configure)\b.*$", re.M)
READS = re.compile(r"^(?:read_verilog(?: -v)?|read_xdc|source) \{?([^{}\s]+)\}?[ \t]*$", re.M)
INCLUDES = re.compile(r" -include_dirs \{([^}]*)\}")
GENERICS = re.compile(r" -generic \{([^}]*)\}")
#: One route status row, `# of <label>....... :  <count> :`.
STATUS_ROW = re.compile(r"^[ \t]*#[ \t]*(?:of[ \t]+)?(\S.*?)\.*[ \t]*:[ \t]*(\S+)[ \t]*:[ \t]*$", re.M)


class Refusal(Exception):
    """A measurement that cannot be compared; exit status 2."""


def header(text: str, name: str) -> str:
    """Return one ``| Name : value`` report header field, refusing absence."""
    hits = re.findall(r"^\| " + re.escape(name) + r"\s*: (.+?)\s*$", text, re.M)
    if len(hits) != 1:
        raise Refusal(f"report header {name!r} appears {len(hits)} times")
    return hits[0]


def utilization(text: str, kind: str) -> dict[str, float]:
    """Read the used column of every required utilization row, with one value each."""
    seen: dict[str, set[str]] = {}
    for line in text.splitlines():
        cells = [cell.strip() for cell in line.split("|")[1:-1]]
        if len(cells) >= 2:
            seen.setdefault(cells[0].rstrip("*").strip(), set()).add(cells[1])
    figures = {}
    for label, figure in ROWS[kind].items():
        values = seen.get(label, set())
        if len(values) != 1:
            raise Refusal(f"utilization row {label!r} has values {sorted(values)}")
        value = values.pop()
        if not re.fullmatch(r"[0-9]+(\.5)?", value):
            raise Refusal(f"utilization row {label!r} is not a count: {value!r}")
        figures[figure] = float(value) if "." in value else int(value)
    return figures


def timing(text: str) -> dict[str, float]:
    """Read WNS and WHS from the one Design Timing Summary table."""
    blocks = text.split("| Design Timing Summary")
    if len(blocks) != 2:
        raise Refusal(f"expected one Design Timing Summary, found {len(blocks) - 1}")
    lines = [line for line in blocks[1].splitlines() if line.strip()]
    heads = next((index for index, line in enumerate(lines) if "WNS(ns)" in line), None)
    if heads is None or heads + 2 >= len(lines):
        raise Refusal("Design Timing Summary has no WNS row")
    names = re.split(r"\s{2,}", lines[heads].strip())
    values = lines[heads + 2].split()
    if len(names) != len(values) or len(names) < 5 or names[0] != "WNS(ns)" or names[4] != "WHS(ns)":
        raise Refusal("Design Timing Summary columns changed")
    if not SLACK.fullmatch(values[0]) or not SLACK.fullmatch(values[4]):
        raise Refusal(f"slack is not a finite decimal: WNS {values[0]!r}, WHS {values[4]!r}")
    paths = [value for name, value in zip(names, values) if name in ("TNS Total Endpoints", "THS Total Endpoints")]
    if not paths or not all(COUNT.fullmatch(value) and int(value) > 0 for value in paths):
        raise Refusal(f"Design Timing Summary times no endpoint: total endpoints {paths}")
    return {"WNS_ns": float(values[0]), "WHS_ns": float(values[4])}


def located(directory: Path, script: str) -> tuple[list[Path], tuple[str, ...]]:
    """Resolve every read or sourced file and the roots a generated file may name."""
    sources = [Path(name) if Path(name).is_absolute() else directory / name
               for name in READS.findall(script)]
    generated = [path.parent for path in sources if path.name == "alinx_ax7101.v"]
    repository = [path.parents[2] for path in sources
                  if path.name == "KL_pp_shadow.sv" and path.parent.name == "milan" and len(path.parents) > 2]
    if len(generated) != 1 or len(repository) != 1:
        raise Refusal("the script must read exactly one generated top and one KL_pp_shadow.sv")
    headers = []
    for group in INCLUDES.findall(script):
        for folder in (Path(name) for name in group.split()):
            if not folder.is_dir():
                raise Refusal(f"include directory is missing: {folder}")
            headers += sorted(path for path in folder.iterdir() if path.suffix in (".svh", ".vh"))
    return sources + headers, (str(generated[0]), str(repository[0]), str(directory))


def inputs(directory: Path, script: str) -> str:
    """Digest every design input in script order, independent of where it was built."""
    files, roots = located(directory, script)
    digest = hashlib.sha256()
    for path in files:
        if not path.is_file():
            raise Refusal(f"read source is missing: {path}")
        data = path.read_bytes()
        if str(path).startswith(roots[0] + "/"):
            # The exporter stamps dates in comments and absolute roots in paths.
            text = re.sub(r"//[^\n]*", "", data.decode(errors="replace"))
            for index, root in enumerate(roots):
                text = text.replace(root, f"$ROOT{index}")
            data = text.encode()
        digest.update(path.name.encode() + b"\0" + hashlib.sha256(data).digest())
    for generic in GENERICS.findall(script):
        digest.update(re.sub(r'"[^"]*/([^/"]+)"', r'"\1"', generic).encode() + b"\0")
    images = json.loads((directory / "baseline_images.json").read_text())
    if not isinstance(images, list) or not all(isinstance(image, dict) and isinstance(image.get("path"), str)
                                               and isinstance(image.get("sha256"), str) for image in images):
        raise Refusal("baseline_images.json is not a list of path and sha256 entries")
    for image in sorted(images, key=lambda row: Path(row["path"]).name):
        digest.update(f"{Path(image['path']).name}\0{image['sha256']}\0".encode())
    return digest.hexdigest()


def identity(directory: Path, script: str, report: str) -> dict:
    """Bind tool, device, design and flow; paths and generics belong to the inputs."""
    tool = re.match(r"(.+? Build \d+)", header(report, "Tool Version"))
    if tool is None:
        raise Refusal("report header 'Tool Version' carries no build")
    flow = [GENERICS.sub("", INCLUDES.sub("", match.group(0))).strip()
            for match in FLOW.finditer(script)]
    clock = directory / "clock.xdc"
    return {"tool": tool[1], "device": header(report, "Device"),
            "design": header(report, "Design"), "state": header(report, "Design State"),
            "flow": flow,
            "standalone_clock_ns": re.findall(r"-period (\S+)", clock.read_text()) if clock.is_file() else []}


def census(directory: Path) -> dict[str, int]:
    """Count CARRY4 cells under every hierarchical prefix of the primitive census."""
    lines = (directory / "baseline_cells.tsv").read_text().splitlines()
    if not lines or lines[0] != "cell\tprimitive":
        raise Refusal("baseline_cells.tsv header changed")
    carry = {"": 0}
    for line in lines[1:]:
        cell, _, primitive = line.partition("\t")
        if primitive == "CARRY4":
            carry[""] += 1
            parts = cell.split("/")
            for depth in range(1, len(parts)):
                key = "/".join(parts[:depth])
                carry[key] = carry.get(key, 0) + 1
    return carry


def scopes(directory: Path, kind: str, carry: dict[str, int]) -> dict[str, dict[str, int]]:
    """Per-instance LUT, FF, RAMB, DSP and CARRY4 for the wrapper and three levels below."""
    rows = hierarchy(directory / "baseline_hierarchy.rpt")
    root = ROOTS[kind]
    if root not in rows:
        raise Refusal(f"hierarchy report has no {root}")
    result = {}
    for key, counts in rows.items():
        inside = key == root or key.startswith(root + "/")
        if inside and not key.endswith("/@own") and key.count("/") <= root.count("/") + 3:
            relative = key.removeprefix(root).lstrip("/") or "wrapper"
            cells = key.split("/", 1)[1] if "/" in key else ""
            result[relative] = {name: counts[name] for name in ("LUT", "FF", "RAMB36", "RAMB18", "DSP")}
            result[relative]["CARRY4"] = carry.get(cells, 0)
    return result


def kind_of(directory: Path) -> str:
    """Name the endpoint kind from the one recipe script the directory holds."""
    kinds = [kind for kind, script in SCRIPTS.items() if (directory / script).is_file()]
    if len(kinds) != 1:
        raise Refusal(f"{directory} holds {len(kinds)} recipe scripts, not one")
    return kinds[0]


def record(directory: Path, kind: str) -> dict:
    """Read one recipe measurement directory into a comparable record."""
    try:
        script = (directory / SCRIPTS[kind]).read_text()
        report = (directory / "baseline_utilization.rpt").read_text()
        figures = utilization(report, kind)
        figures.update(timing((directory / "baseline_timing.rpt").read_text()))
        carry = census(directory)
        figures["CARRY4"] = carry[""]
        return {"kind": kind, "identity": identity(directory, script, report),
                "inputs_sha256": inputs(directory, script), "figures": figures,
                "scopes": scopes(directory, kind, carry)}
    except (OSError, ValueError, KeyError, IndexError, TypeError, RecursionError) as error:
        raise Refusal(f"unreadable measurement {directory}: {type(error).__name__}: {error}") from error


def routing(directory: Path, kind: str) -> list[str]:
    """Name what keeps a route from completing, read from the run's one route status report."""
    if kind != "route":
        return []
    reports = sorted(directory.glob("*_route_status.rpt"))
    if len(reports) != 1:
        raise Refusal(f"expected one *_route_status.rpt route status report, found {len(reports)}")
    try:
        rows = STATUS_ROW.findall(reports[0].read_text())
    except (OSError, ValueError) as error:
        raise Refusal(f"unreadable route status {reports[0].name}: {error}") from error
    counts: dict[str, list[int]] = {}
    for label, value in rows:
        if not COUNT.fullmatch(value):
            raise Refusal(f"route status row {label!r} is not a count: {value!r}")
        counts.setdefault(label, []).append(int(value))
    for label in ("routable nets", "fully routed nets"):
        if len(counts.get(label, [])) != 1:
            raise Refusal(f"{reports[0].name} has {len(counts.get(label, []))} {label!r} rows, not one")
    if len(counts.get("nets with routing errors", [])) != 1:
        raise Refusal(f"{reports[0].name} has no single 'nets with routing errors' row")
    routable, routed = sum(counts.get("routable nets", [])), sum(counts.get("fully routed nets", []))
    problems = [f"{sum(values)} {label}" for label, values in counts.items()
                if sum(values) and ("routing errors" in label or "unrouted" in label)]
    if routed != routable:
        problems.append(f"{routed} of {routable} routable nets fully routed")
    return problems


def judge(entry: dict, candidate: dict, unrouted: list[str] | None = None) -> tuple[int, list[str]]:
    """Compare one record with its baseline entry; return the exit status and report.

    ``unrouted`` is what routing() found incomplete in the candidate's route,
    or None for a bare record whose route status was never read.
    """
    base = entry["record"]
    if candidate["kind"] != base["kind"]:
        return 2, [f"NOT COMPARABLE: endpoint kind {candidate['kind']} against {base['kind']}"]
    changed = sorted(key for key in base["identity"]
                     if base["identity"][key] != candidate["identity"].get(key))
    if changed:
        return 2, [f"NOT COMPARABLE: tool or recipe change in {', '.join(changed)}; measure the "
                   "baseline again under the new identity instead of comparing across it"]
    if candidate["inputs_sha256"] == base["inputs_sha256"] and candidate["figures"] != base["figures"]:
        return 2, ["NOT COMPARABLE: identical inputs measured differently (non-determinism or "
                   "an unrecorded tool setting), which is not an architectural change"]
    status, lines = 0, [f"{'figure':<10}{'baseline':>12}{'candidate':>12}{'delta':>10}  verdict"]
    improved = []
    for figure in GATED[base["kind"]]:
        before, after = base["figures"][figure], candidate["figures"][figure]
        verdict, ok = verdict_for(entry, figure, before, after)
        status = status if ok else 1
        lines.append(f"{figure:<10}{before:>12}{after:>12}{round(after - before, 3):>10}  {verdict}")
        gain = after - before if figure in TIMING else before - after
        if gain > entry["tolerance"][figure]:
            improved.append(figure)
    for figure, ceiling in entry.get("ceiling", {}).items():
        if candidate["figures"][figure] > ceiling:
            status = 1
            lines.append(f"{figure:<10} REGRESSION: {candidate['figures'][figure]} exceeds the ceiling {ceiling}")
    if unrouted:
        status = 1
        lines.append(f"ROUTE INCOMPLETE: {', '.join(unrouted)}; the image does not fit")
    elif unrouted is not None and candidate["kind"] == "route":
        lines.append("route status: complete, no unrouted net and no routing error")
    if improved:
        lines.append(f"re-baseline recommended: {', '.join(improved)} improved by more than the tolerance; "
                     "record the accepted measurement so later growth is judged from it")
    lines += scope_deltas(base["scopes"], candidate["scopes"])
    lines.append("RESULT: " + ("PASS" if status == 0 else "MATERIAL REGRESSION"))
    return status, lines


def verdict_for(entry: dict, figure: str, before: float, after: float) -> tuple[str, bool]:
    """Apply one figure's tolerance, and a timing figure's floor."""
    tolerance = entry["tolerance"][figure]
    if figure in TIMING:
        floor = entry["floor"][figure]
        if after < floor:
            return f"REGRESSION: below the floor {floor}", False
        if before - after > tolerance:
            return f"REGRESSION: fell by more than {tolerance}", False
        return "ok", True
    if after - before > tolerance:
        return f"REGRESSION: grew by more than {tolerance}", False
    return ("ok, below the baseline" if after < before else "ok"), True


def scope_deltas(before: dict, after: dict) -> list[str]:
    """List the largest sub-block LUT and FF movements; reported, never gated."""
    moves = []
    for key in sorted(set(before) | set(after)):
        old, new = before.get(key, {}), after.get(key, {})
        lut, ff = new.get("LUT", 0) - old.get("LUT", 0), new.get("FF", 0) - old.get("FF", 0)
        if lut or ff or not old or not new:
            note = "" if old and new else " (instance added or removed)"
            moves.append((abs(lut) + abs(ff), f"  {key}: LUT {lut:+d}, FF {ff:+d}{note}"))
    moves.sort(key=lambda move: -move[0])
    return ["sub-block movements, not gated:", *(line for _, line in moves[:12])] if moves else []


def finite(text: str) -> float:
    """Read one JSON decimal, refusing one so large that it reads as infinity."""
    value = float(text)
    if not math.isfinite(value):
        raise ValueError(f"the number {text} is not finite")
    return value


def constant(name: str) -> float:
    """Refuse NaN and Infinity: JSON does not define them, and no figure or policy can be one."""
    raise ValueError(f"the number {name} is not finite")


def number(value: object) -> bool:
    """Tell a JSON number from a bool, a string or null; load() has already refused a non-finite one."""
    return isinstance(value, (int, float)) and not isinstance(value, bool)


def shape_problems(name: str, entry: object) -> list[str]:
    """List every field of one baseline endpoint that is missing or not of the recorded shape."""
    base = entry.get("record") if isinstance(entry, dict) else None
    if not isinstance(base, dict):
        return [f"{name}: has no record"]
    lacking = [key for key in RECORD if key not in base]
    if lacking:
        return [f"{name}: the record lacks {', '.join(lacking)}"]
    kind, identity, figures, scopes = base["kind"], base["identity"], base["figures"], base["scopes"]
    if not isinstance(kind, str) or kind not in GATED:
        return [f"{name}: the record kind {kind!r} is not one of {', '.join(GATED)}"]
    problems = []
    unknown = sorted(set(entry) - {"record", *POLICY, *NOTES["endpoint"]})
    if unknown:
        problems.append(f"{name}: the endpoint holds unknown fields {', '.join(unknown)}")
    if not isinstance(identity, dict) or sorted(identity) != sorted(IDENTITY):
        problems.append(f"{name}: the record identity does not hold exactly {', '.join(IDENTITY)}")
    elif not all(isinstance(identity[key], recorded) for key, recorded in IDENTITY.items()):
        problems.append(f"{name}: a record identity field is not of its recorded type")
    elif not all(isinstance(item, str) for key in ("flow", "standalone_clock_ns") for item in identity[key]):
        problems.append(f"{name}: the record identity's flow or standalone clock is not a list of text")
    if not isinstance(base["inputs_sha256"], str) or not re.fullmatch(r"[0-9a-f]{64}", base["inputs_sha256"]):
        problems.append(f"{name}: the record input digest is not a sha256 hex digest")
    held = sorted({*ROWS[kind].values(), *TIMING, "CARRY4"})
    if not isinstance(figures, dict) or sorted(figures) != held:
        problems.append(f"{name}: the record figures are not exactly {', '.join(held)}")
    elif not all(number(value) for value in figures.values()):
        problems.append(f"{name}: a recorded figure is not a finite number")
    if not isinstance(scopes, dict) or not all(isinstance(counts, dict) and sorted(counts) == sorted(SCOPE)
                                               for counts in scopes.values()):
        problems.append(f"{name}: the record scopes are not a table of {', '.join(SCOPE)} per sub-block")
    elif not all(type(count) is int and count >= 0 for counts in scopes.values() for count in counts.values()):
        problems.append(f"{name}: a recorded sub-block count is not a non-negative whole number")
    for field in POLICY:
        if not isinstance(entry.get(field, {}), dict):
            problems.append(f"{name}: {field} is not a table of figures")
        elif not all(number(value) for value in entry.get(field, {}).values()):
            problems.append(f"{name}: a {field} value is not a finite number")
    return problems


def load(path: Path) -> dict:
    """Read a baseline file whole: strict JSON, an endpoints table and every endpoint of the recorded shape."""
    try:
        baseline = json.loads(path.read_text(), parse_constant=constant, parse_float=finite)
    except (OSError, ValueError, RecursionError) as error:
        raise Refusal(f"baseline {path} is unreadable: {error}") from error
    if not isinstance(baseline, dict) or not isinstance(baseline.get("endpoints"), dict):
        raise Refusal(f"baseline {path} holds no endpoints table")
    unknown = sorted(set(baseline) - {"endpoints", *NOTES["file"]})
    problems = [f"the file holds unknown fields {', '.join(unknown)}"] if unknown else []
    problems += [problem for name, entry in baseline["endpoints"].items() for problem in shape_problems(name, entry)]
    if problems:
        raise Refusal(f"baseline {path} is malformed: {'; '.join(problems)}")
    return baseline


def entry_problems(name: str, entry: dict) -> list[str]:
    """List what keeps one endpoint load() accepted from being a complete policy its own record meets."""
    kind, figures = entry["record"]["kind"], entry["record"]["figures"]
    problems = []
    for figure in GATED[kind]:
        if not entry.get("tolerance", {}).get(figure, -1) >= 0:
            problems.append(f"{name}: {figure} has no non-negative tolerance")
        if figure in TIMING and figure not in entry.get("floor", {}):
            problems.append(f"{name}: {figure} has no floor")
        elif figure in TIMING and figures[figure] < entry["floor"][figure]:
            problems.append(f"{name}: the recorded {figure} is below its floor")
    for figure in CEILINGS[kind]:
        if figure not in entry.get("ceiling", {}):
            problems.append(f"{name}: {figure} has no ceiling")
    for figure, ceiling in entry.get("ceiling", {}).items():
        if figure not in figures:
            problems.append(f"{name}: the ceiling names {figure}, which is not a recorded figure")
        elif figures[figure] > ceiling:
            problems.append(f"{name}: the recorded {figure} exceeds its ceiling")
    return problems


def policy_table(text: str) -> dict[str, dict[str, dict[str, float]]]:
    """Read the policy each endpoint row of the budget's one resource-gate table sets."""
    head = "| Endpoint | " + " | ".join(COLUMNS) + " |"
    lines = text.splitlines()
    starts = [index for index, line in enumerate(lines) if line.strip() == head]
    if len(starts) != 1:
        raise Refusal(f"the budget holds {len(starts)} resource-gate policy tables, not one")
    table: dict[str, dict[str, dict[str, float]]] = {}
    for line in lines[starts[0] + 2:]:
        if not line.startswith("|"):
            break
        cells = [cell.strip() for cell in line.strip().strip("|").split("|")]
        name = re.fullmatch(r"`([\w-]+)`", cells[0])
        if len(cells) != len(COLUMNS) + 1 or name is None or name[1] in table:
            raise Refusal(f"budget policy row is malformed or repeated: {line.strip()}")
        table[name[1]] = {field: {} for field in POLICY}
        for cell, (field, figures) in zip(cells[1:], COLUMNS.values()):
            value = re.fullmatch(r"([+-]?[0-9]+(?:\.[0-9]+)?)(?: ns)?", cell)
            if value is None and cell != "-":
                raise Refusal(f"budget policy cell {cell!r} is neither a value nor '-'")
            for figure in figures if value else ():
                table[name[1]][field][figure] = float(value[1])
    return table


def check_baseline(baseline: dict, budget: Path) -> list[str]:
    """Refuse a baseline whose policy is incomplete, fails its own record or departs from the budget table."""
    endpoints = baseline["endpoints"]
    problems = [problem for name, entry in endpoints.items() for problem in entry_problems(name, entry)]
    try:
        table = policy_table(budget.read_text())
    except (OSError, ValueError, Refusal) as error:
        return problems + [f"budget {budget.name}: {error}"]
    for name in sorted(set(endpoints) | set(table)):
        if name not in table or name not in endpoints:
            problems.append(f"{name}: only the {'baseline' if name in endpoints else 'budget table'} names it")
            continue
        entry = endpoints[name]
        for field in POLICY:
            held = entry.get(field, {})
            for figure in sorted(set(held) | set(table[name][field])):
                if held.get(figure) != table[name][field].get(figure):
                    problems.append(f"{name}: {field} {figure} is {held.get(figure)} in the baseline and "
                                    f"{table[name][field].get(figure)} in the budget table")
    return problems


def main(argv: list[str] | None = None) -> int:
    """Run one command and return its exit status."""
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("command", nargs="?", choices=("check", "record", "check-baseline"))
    parser.add_argument("directory", type=Path, nargs="?")
    parser.add_argument("--endpoint")
    parser.add_argument("--baseline", type=Path, default=BASELINE)
    parser.add_argument("--budget", type=Path, default=BUDGET, help="check-baseline: the page with the policy table")
    parser.add_argument("--write", action="store_true", help="record: replace the endpoint's recorded figures")
    parser.add_argument("--selftest", action="store_true")
    args = parser.parse_args(argv)
    if args.selftest:
        from pp_resource_gate_selftest import selftest
        return selftest()
    printing = args.command == "record" and not args.write
    try:
        baseline = {"endpoints": {}} if printing else load(args.baseline)
        if args.command == "check-baseline":
            problems = check_baseline(baseline, args.budget)
            print("\n".join(problems) or f"baseline PASS: {len(baseline['endpoints'])} endpoints")
            return 2 if problems else 0
        known = args.endpoint in baseline["endpoints"] or (args.command == "record" and args.endpoint)
        if args.command is None or args.directory is None or not known:
            parser.error(f"name a command, a directory and one of {sorted(baseline['endpoints'])}")
        endpoint = baseline["endpoints"].get(args.endpoint)
        problems = entry_problems(args.endpoint, endpoint) if args.command == "check" else []
        if problems:
            raise Refusal(f"baseline endpoint {args.endpoint} is unusable: {'; '.join(problems)}")
        directory = args.directory.resolve()
        candidate = record(directory, kind_of(directory))
        unrouted = routing(directory, candidate["kind"]) if args.command == "check" else []
    except Refusal as error:
        print(f"NOT COMPARABLE: {error}")
        return 2
    if args.command == "record":
        print(json.dumps(candidate, indent=1))
        if args.write:
            baseline["endpoints"].setdefault(args.endpoint, {})["record"] = candidate
            args.baseline.write_text(json.dumps(baseline, indent=1) + "\n")
        return 0
    status, lines = judge(baseline["endpoints"][args.endpoint], candidate, unrouted)
    print("\n".join([f"endpoint {args.endpoint}: {args.directory}", *lines]))
    return status


if __name__ == "__main__":
    sys.exit(main())
