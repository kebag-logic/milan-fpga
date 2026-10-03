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
judged against the tolerances.

Exit status: 0 within tolerance; 1 a material regression; 2 not comparable
or an unreadable measurement.

    pp_resource_gate.py check <directory> --endpoint route-1x1
    pp_resource_gate.py record <directory> --endpoint route-1x1 [--write]
    pp_resource_gate.py check-baseline
    pp_resource_gate.py --selftest
"""

import argparse
import hashlib
import json
from pathlib import Path
import re
import sys

from pp_baseline_rank import hierarchy


BASELINE = Path(__file__).with_name("pp_resource_baseline.json")
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
SCRIPTS = {"route": "baseline_integrated.tcl", "ooc": "baseline_ooc.tcl"}
ROOTS = {"route": "alinx_ax7101/milan_datapath/pp_shadow", "ooc": "KL_pp_shadow"}
FLOW = re.compile(r"^(create_project|set_param|synth_design|opt_design|place_design"
                  r"|phys_opt_design|route_design|kl_timing_grade_configure)\b.*$", re.M)
READS = re.compile(r"^(?:read_verilog(?: -v)?|read_xdc|source) \{?([^{}\s]+)\}?[ \t]*$", re.M)
INCLUDES = re.compile(r" -include_dirs \{([^}]*)\}")
GENERICS = re.compile(r" -generic \{([^}]*)\}")


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
        if not re.fullmatch(r"\d+(\.5)?", value):
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
    try:
        return {"WNS_ns": float(values[0]), "WHS_ns": float(values[4])}
    except ValueError as error:
        raise Refusal(f"unreadable slack: {error}") from error


def located(directory: Path, script: str) -> tuple[list[Path], tuple[str, ...]]:
    """Resolve every read or sourced file and the roots a generated file may name."""
    sources = [Path(name) if Path(name).is_absolute() else directory / name
               for name in READS.findall(script)]
    generated = [path.parent for path in sources if path.name == "alinx_ax7101.v"]
    repository = [path.parents[2] for path in sources
                  if path.name == "KL_pp_shadow.sv" and path.parent.name == "milan"]
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
    except (OSError, ValueError, KeyError) as error:
        raise Refusal(f"unreadable measurement {directory}: {error}") from error


def judge(entry: dict, candidate: dict) -> tuple[int, list[str]]:
    """Compare one record with its baseline entry; return the exit status and report."""
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
    for figure in GATED[base["kind"]]:
        before, after = base["figures"][figure], candidate["figures"][figure]
        verdict, ok = verdict_for(entry, figure, before, after)
        status = status if ok else 1
        lines.append(f"{figure:<10}{before:>12}{after:>12}{round(after - before, 3):>10}  {verdict}")
    for figure, ceiling in entry.get("ceiling", {}).items():
        if candidate["figures"][figure] > ceiling:
            status = 1
            lines.append(f"{figure:<10} REGRESSION: {candidate['figures'][figure]} exceeds the ceiling {ceiling}")
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
    return ("ok, below the baseline: record it to ratchet down" if after < before else "ok"), True


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


def check_baseline(baseline: dict) -> list[str]:
    """Refuse a baseline whose policy is incomplete or whose record fails its own limits."""
    problems = []
    for name, entry in baseline["endpoints"].items():
        kind, figures = entry["record"]["kind"], entry["record"]["figures"]
        for figure in GATED[kind]:
            if not entry.get("tolerance", {}).get(figure, -1) >= 0:
                problems.append(f"{name}: {figure} has no non-negative tolerance")
            if figure in TIMING and figure not in entry.get("floor", {}):
                problems.append(f"{name}: {figure} has no floor")
            elif figure in TIMING and figures[figure] < entry["floor"][figure]:
                problems.append(f"{name}: the recorded {figure} is below its floor")
        for figure, ceiling in entry.get("ceiling", {}).items():
            if figures[figure] > ceiling:
                problems.append(f"{name}: the recorded {figure} exceeds its ceiling")
    return problems


def main(argv: list[str] | None = None) -> int:
    """Run one command and return its exit status."""
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("command", nargs="?", choices=("check", "record", "check-baseline"))
    parser.add_argument("directory", type=Path, nargs="?")
    parser.add_argument("--endpoint")
    parser.add_argument("--baseline", type=Path, default=BASELINE)
    parser.add_argument("--write", action="store_true", help="record: replace the endpoint's recorded figures")
    parser.add_argument("--selftest", action="store_true")
    args = parser.parse_args(argv)
    if args.selftest:
        from pp_resource_gate_selftest import selftest
        return selftest()
    printing = args.command == "record" and not args.write
    baseline = {"endpoints": {}} if printing else json.loads(args.baseline.read_text())
    if args.command == "check-baseline":
        problems = check_baseline(baseline)
        print("\n".join(problems) or f"baseline PASS: {len(baseline['endpoints'])} endpoints")
        return 2 if problems else 0
    known = args.endpoint in baseline["endpoints"] or (args.command == "record" and args.endpoint)
    if args.command is None or args.directory is None or not known:
        parser.error(f"name a command, a directory and one of {sorted(baseline['endpoints'])}")
    try:
        directory = args.directory.resolve()
        candidate = record(directory, kind_of(directory))
    except Refusal as error:
        print(f"NOT COMPARABLE: {error}")
        return 2
    if args.command == "record":
        print(json.dumps(candidate, indent=1))
        if args.write:
            baseline["endpoints"].setdefault(args.endpoint, {})["record"] = candidate
            args.baseline.write_text(json.dumps(baseline, indent=1) + "\n")
        return 0
    status, lines = judge(baseline["endpoints"][args.endpoint], candidate)
    print("\n".join([f"endpoint {args.endpoint}: {args.directory}", *lines]))
    return status


if __name__ == "__main__":
    sys.exit(main())
