#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""Verify documented submodule pins and diagram relationships."""

from __future__ import annotations

import configparser
import re
import subprocess
import sys
import xml.etree.ElementTree as ET
from collections import Counter
from dataclasses import dataclass
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
REFERENCE = ROOT / "docs" / "reference" / "SUBMODULES.md"
DRAWIO = ROOT / "docs" / "diagrams" / "submodule_boundaries.drawio"
GENERATOR = ROOT / "docs" / "diagrams" / "submodule_boundaries.gen.py"
START = "<!-- submodule-pins:start -->"
END = "<!-- submodule-pins:end -->"
SHA = re.compile(r"[0-9a-f]{40}")
EDGE_LABELS = {
    "protocol-processor": "wrapper",
    "gptp-processor": "wrapper",
    "third_party/verilog-axis": "RTL",
    "external": "legacy",
}


@dataclass(frozen=True)
class Row:
    path: str
    pin: str
    purpose: str
    boundary: str


def run_git(*args: str) -> str:
    result = subprocess.run(
        ["git", "-C", str(ROOT), *args],
        check=True,
        capture_output=True,
        text=True,
    )
    return result.stdout.strip()


def configured_paths() -> list[str]:
    config = configparser.ConfigParser()
    config.read(ROOT / ".gitmodules")
    return sorted(config.get(section, "path") for section in config.sections())


def gitlink_pins(paths: list[str]) -> dict[str, str]:
    pins: dict[str, str] = {}
    for path in paths:
        fields = run_git("ls-files", "--stage", "--", path).split()
        if len(fields) < 4 or fields[0] != "160000" or fields[2] != "0":
            raise ValueError(f"{path}: expected one stage-0 gitlink")
        pins[path] = fields[1]
    return pins


def parse_rows(text: str) -> list[Row]:
    if text.count(START) != 1 or text.count(END) != 1:
        raise ValueError("pin table markers must appear exactly once")
    section = text.split(START, 1)[1].split(END, 1)[0]
    rows: list[Row] = []
    for line in section.splitlines():
        stripped = line.strip()
        if not stripped.startswith("|"):
            continue
        fields = [field.strip() for field in stripped.strip("|").split("|")]
        if not fields or fields[0] == "Path" or set(fields[0]) == {"-"}:
            continue
        if len(fields) != 4:
            raise ValueError(f"malformed pin row: {line}")
        rows.append(Row(*(field.strip("`") for field in fields)))
    return rows


def validate_rows(rows: list[Row], pins: dict[str, str]) -> list[str]:
    errors: list[str] = []
    counts = Counter(row.path for row in rows)
    duplicates = sorted(path for path, count in counts.items() if count != 1)
    if duplicates:
        errors.append("duplicate paths: " + ", ".join(duplicates))
    expected = set(pins)
    actual = set(counts)
    if expected - actual:
        errors.append("missing paths: " + ", ".join(sorted(expected - actual)))
    if actual - expected:
        errors.append("unknown paths: " + ", ".join(sorted(actual - expected)))
    for row in rows:
        if not SHA.fullmatch(row.pin):
            errors.append(f"{row.path}: pin is not a full lowercase SHA")
        elif row.path in pins and row.pin != pins[row.path]:
            errors.append(f"{row.path}: documented pin differs from Git")
        if not row.purpose:
            errors.append(f"{row.path}: missing purpose")
        if not row.boundary:
            errors.append(f"{row.path}: missing root boundary")
    return errors


def validate_drawio(paths: list[str]) -> list[str]:
    root = ET.parse(DRAWIO).getroot()
    cells = {cell.get("id"): cell for cell in root.iter("mxCell")}
    errors: list[str] = []
    expected_sources = {"sub-" + path.replace("/", "-") for path in paths}
    edges = [cell for cell in cells.values() if cell.get("edge") == "1"]
    sources = [edge.get("source", "") for edge in edges]
    if Counter(sources) != Counter(expected_sources):
        errors.append("Draw.io edges do not cover every submodule exactly once")
    for path in paths:
        source = "sub-" + path.replace("/", "-")
        cell = cells.get(source)
        if cell is None or path not in cell.get("value", ""):
            errors.append(f"{path}: Draw.io node is missing or mislabeled")
        matching = [edge for edge in edges if edge.get("source") == source]
        if len(matching) != 1:
            continue
        edge = matching[0]
        if edge.get("target") != "root":
            errors.append(f"{path}: Draw.io edge misses root")
        expected_label = EDGE_LABELS.get(path)
        if expected_label is None:
            errors.append(f"{path}: Draw.io role needs checker coverage")
        elif edge.get("value") != expected_label:
            errors.append(f"{path}: Draw.io edge has incorrect role")
        dashed = "dashed=1;" in edge.get("style", "")
        if dashed != (path == "external"):
            errors.append(f"{path}: Draw.io legacy styling is incorrect")
    return errors


def selftest() -> int:
    pins = {"alpha": "a" * 40, "beta": "b" * 40}
    table = f"""{START}
| Path | Pin | Purpose | Root integration |
|---|---|---|---|
| `alpha` | `{'a' * 40}` | One | A |
| `beta` | `{'b' * 40}` | Two | B |
{END}
"""
    rows = parse_rows(table)
    if validate_rows(rows, pins):
        print("selftest: valid table failed")
        return 1
    stale = table.replace("`" + "b" * 40 + "`", "`" + "c" * 40 + "`")
    if not validate_rows(parse_rows(stale), pins):
        print("selftest: stale pin escaped")
        return 1
    duplicate = table.replace(END, f"| `alpha` | `{'a' * 40}` | One | A |\n{END}")
    if not validate_rows(parse_rows(duplicate), pins):
        print("selftest: duplicate path escaped")
        return 1
    try:
        parse_rows(table.replace(END, ""))
    except ValueError:
        pass
    else:
        print("selftest: missing marker escaped")
        return 1
    print("submodule documentation selftest: OK")
    return 0


def main() -> int:
    if sys.argv[1:] == ["--selftest"]:
        return selftest()
    if sys.argv[1:]:
        print(__doc__)
        return 2
    try:
        paths = configured_paths()
        pins = gitlink_pins(paths)
        rows = parse_rows(REFERENCE.read_text(encoding="utf-8"))
        errors = validate_rows(rows, pins)
        diagram = subprocess.run(
            [sys.executable, str(GENERATOR), "--check"],
            cwd=ROOT,
            capture_output=True,
            text=True,
        )
        if diagram.returncode:
            errors.append(diagram.stdout.strip() or diagram.stderr.strip())
        errors.extend(validate_drawio(paths))
    except (OSError, ValueError, subprocess.CalledProcessError, ET.ParseError) as error:
        print(f"submodule documentation: FAIL: {error}")
        return 1
    if errors:
        for error in errors:
            print(error)
        print(f"submodule documentation: FAIL ({len(errors)} findings)")
        return 1
    print(f"submodule documentation: OK ({len(paths)} exact gitlinks)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
