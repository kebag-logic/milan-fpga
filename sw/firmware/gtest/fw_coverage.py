#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""fw_coverage.py - line and branch coverage of the bare-metal firmware, and the ratchet that refuses a drop.

WHAT IT MEASURES. The firmware's sources under sw/firmware/ctrl and
sw/firmware/ctrl_nvm (not the tests, not the host models and stubs), as both
host gates run them: each gate's --coverage mode builds the firmware at -O0
with gcc's --coverage instrumentation, the tests and the host models without
it, and runs every arm that executes the firmware, every shipped shape of the
saved-state store included. A failing run refuses the measurement.

HOW. gcc's own gcov, in its JSON intermediate format (gcov --json-format
--branch-probabilities, gcc 9 and later), is read by the small reader here;
no other coverage tool is involved. A source compiled into several objects
(each arm, each shape) is merged by line: a line is covered when any run
executed it, and an arc when any run took it. Where builds of one line differ
in their arcs (a shape constant that folds a condition), the build with the
most arcs is the line's measure. Exception edges (`throw`) are not counted;
the firmware is C.

THE EXCLUSIONS are the table under "Coverage exclusions" in
sw/firmware/gtest/README.md, one row per function: the file, the function,
a fragment of the statement left uncovered (which must occur once in the
function, so the row names its code), what is left uncovered there ("N arcs",
"N lines", or both) and why it cannot be reached. A row is matched against
the whole function, as gcov's own function ranges bound it, because gcc at
-O0 files the arcs of a condition that spans lines under one of them, and
not the same one in every version: the function's uncovered arcs and
unexecuted lines must be exactly what its rows say. A row that does not
match the measurement, names no reason, or whose fragment is missing or
repeated in the function is refused.

THE RATCHET is sw/firmware/gtest/coverage.ratchet: per file, covered over
total for lines and for branches after the exclusions. A file whose line or
branch coverage falls below its recorded fraction is refused, and so is a
measured file the ratchet does not record and a recorded one nothing
measured. --write records the measurement, and refuses to record a drop.

Usage:
    python3 sw/firmware/gtest/fw_coverage.py --check [--lwsrp DIR] [--jobs N]
    python3 sw/firmware/gtest/fw_coverage.py --write [--lwsrp DIR] [--jobs N]
    python3 sw/firmware/gtest/fw_coverage.py --selftest

Exit 0 = at or over the ratchet; 1 = a drop, a stale or malformed exclusion,
or a file in one place and not the other; 2 = the measurement could not be
taken (a gate failed, no gcov, no data).
"""

from __future__ import annotations

import argparse
import gzip
import json
import os
import re
import subprocess
import sys
import tempfile
from dataclasses import dataclass, field
from fractions import Fraction
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
#: The page holding the exclusion table: this directory's README. It is under
#: sw/, so every change to it runs firmware-unit already. Its name is joined
#: from stem and suffix because scripts/ci_scope.py's scan reads a bare
#: README-dot-md literal as the top-level README, a documentation page this
#: gate never reads.
README = HERE / ("README" + ".md")
RATCHET = HERE / "coverage.ratchet"
#: The firmware this gate measures; under them, these are not firmware.
MEASURED_ROOTS = ("sw/firmware/ctrl/", "sw/firmware/ctrl_nvm/")
NOT_FIRMWARE = ("/test/", "/host/")
GATES = (("ctrl", ROOT / "sw/firmware/ctrl/test/test_ctrl_firmware.py"),
         ("ctrl_nvm", ROOT / "sw/firmware/ctrl_nvm/test/test_ctrl_nvm.py"))
EXCLUSIONS_HEADING = "Coverage exclusions"


class Unmeasured(Exception):
    """The measurement could not be taken: exit 2, never a pass."""


@dataclass
class Line:
    """One source line as the runs saw it: executed or not, and its arcs."""

    count: int = 0
    arcs: list[int] = field(default_factory=list)


@dataclass(frozen=True)
class Exclusion:
    """One row of the README's exclusion table."""

    file: str
    function: str
    statement: str
    uncovered: str
    reason: str


@dataclass
class Source:
    """One firmware source as every run saw it: its lines, and the line range
    of each of its functions."""

    lines: dict[int, Line] = field(default_factory=dict)
    functions: dict[str, tuple[int, int]] = field(default_factory=dict)


@dataclass(frozen=True)
class Tally:
    """One file's coverage: covered and total lines and branch arcs."""

    lines: tuple[int, int]
    branches: tuple[int, int]


def merge_line(into: Line, count: int, arcs: list[int]) -> None:
    """Fold one build's view of a line into the merged one."""
    into.count = max(into.count, count)
    if len(arcs) > len(into.arcs):
        into.arcs = [max(a, b) for a, b in zip(arcs, into.arcs + [0] * (len(arcs) - len(into.arcs)))]
    elif len(arcs) == len(into.arcs):
        into.arcs = [max(a, b) for a, b in zip(arcs, into.arcs)]


def relative(path: str) -> str | None:
    """The firmware source a gcov file entry names, repository-relative, or None."""
    p = Path(path)
    try:
        rel = p.resolve().relative_to(ROOT).as_posix()
    except ValueError:
        return None
    if not rel.startswith(MEASURED_ROOTS) or any(part in f"/{rel}" for part in NOT_FIRMWARE):
        return None
    return rel


def read_gcov_json(doc: dict, merged: dict[str, Source]) -> None:
    """Fold one gcov JSON document (one object's data) into `merged`."""
    for entry in doc.get("files", []):
        rel = relative(entry.get("file", ""))
        if rel is None:
            continue
        source = merged.setdefault(rel, Source())
        for fn in entry.get("functions", []):
            source.functions[fn["name"]] = (int(fn["start_line"]), int(fn["end_line"]))
        per_line: dict[int, Line] = {}
        for ln in entry.get("lines", []):
            seen = per_line.setdefault(int(ln["line_number"]), Line())
            seen.count += int(ln.get("count", 0))
            seen.arcs += [int(b.get("count", 0)) for b in ln.get("branches", []) if not b.get("throw", False)]
        for number, seen in per_line.items():
            merge_line(source.lines.setdefault(number, Line()), seen.count, seen.arcs)


def collect(build_dirs: list[Path]) -> dict[str, Source]:
    """Run gcov over every .gcda under the build directories and merge."""
    merged: dict[str, Source] = {}
    gcdas = sorted(p for d in build_dirs for p in d.rglob("*.gcda"))
    if not gcdas:
        raise Unmeasured("no .gcda under the coverage build: nothing ran instrumented")
    with tempfile.TemporaryDirectory(prefix="fw-gcov.") as tmp:
        for k, gcda in enumerate(gcdas):
            out = Path(tmp) / str(k)
            out.mkdir()
            res = subprocess.run(["gcov", "--json-format", "--branch-probabilities", "-o", str(gcda.parent), str(gcda)],
                                 cwd=out, capture_output=True, text=True, check=False)
            docs = sorted(out.glob("*.gcov.json.gz"))
            if res.returncode != 0 or not docs:
                raise Unmeasured(f"gcov on {gcda.name} failed: {res.stderr.strip()[:200]}")
            for doc in docs:
                with gzip.open(doc, "rt", encoding="utf-8") as fh:
                    read_gcov_json(json.load(fh), merged)
    return merged


def exclusions(readme: str) -> list[Exclusion]:
    """The rows of the table under the exclusions heading of the README."""
    rows: list[Exclusion] = []
    inside = False
    for line in readme.splitlines():
        if line.startswith("#"):
            inside = line.lstrip("#").strip() == EXCLUSIONS_HEADING
            continue
        if not inside or not line.startswith("|") or set(line) <= set("|-: "):
            continue
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if len(cells) != 5 or cells[0] == "File":
            continue
        rows.append(Exclusion(*[c[1:-1] if c.startswith("`") and c.endswith("`") else c for c in cells]))
    return rows


def parse_uncovered(text: str) -> tuple[int, int] | None:
    """(arcs, lines) a row's Uncovered cell states: "1 arc", "2 arcs, 1 line"."""
    arcs = lines = 0
    for part in (p.strip() for p in text.split(",")):
        m = re.fullmatch(r"(\d+) (arcs?|lines?)", part)
        if m is None:
            return None
        if m.group(2).startswith("arc"):
            arcs += int(m.group(1))
        else:
            lines += int(m.group(1))
    return arcs, lines


def uncovered_in(source: Source, span: tuple[int, int]) -> tuple[int, int]:
    """(uncovered arcs, unexecuted lines) of a function's line range."""
    lines = [ln for n, ln in source.lines.items() if span[0] <= n <= span[1]]
    return (sum(1 for ln in lines for a in ln.arcs if a == 0), sum(1 for ln in lines if ln.count == 0))


def apply_exclusions(merged: dict[str, Source], rows: list[Exclusion],
                     root: Path = ROOT) -> tuple[dict[str, Source], list[str]]:
    """Remove what the rows accept, function by function; (what is left, the findings)."""
    found: list[str] = []
    stated: dict[tuple[str, str], list[int]] = {}
    for row in rows:
        what = f"exclusion {row.file} {row.function}(): `{row.statement}`"
        span = merged.get(row.file, Source()).functions.get(row.function)
        counts = parse_uncovered(row.uncovered)
        if not row.reason:
            found.append(f"{what}: no reason given")
        elif counts is None:
            found.append(f"{what}: cannot read {row.uncovered!r}")
        elif span is None:
            found.append(f"{what}: no such function in the measurement")
        else:
            text = (root / row.file).read_text(encoding="utf-8").splitlines()[span[0] - 1:span[1]]
            hits = sum(ln.count(row.statement) for ln in text)
            if hits != 1:
                found.append(f"{what}: the statement occurs {hits} times in the function, not once")
            else:
                total = stated.setdefault((row.file, row.function), [0, 0])
                total[0] += counts[0]
                total[1] += counts[1]
    for (rel, function), (arcs, lines) in stated.items():
        source = merged[rel]
        span = source.functions[function]
        got = uncovered_in(source, span)
        if got != (arcs, lines):
            found.append(f"exclusion {rel} {function}(): the rows say {arcs} arcs and {lines} lines uncovered, "
                         f"the measurement {got[0]} and {got[1]}")
            continue
        for n, ln in list(source.lines.items()):
            if span[0] <= n <= span[1]:
                ln.arcs = [a for a in ln.arcs if a != 0]
                if ln.count == 0:
                    del source.lines[n]
    return merged, found


def tally(merged: dict[str, Source]) -> dict[str, Tally]:
    """Per file: covered and total lines and branch arcs."""
    out = {}
    for rel, source in sorted(merged.items()):
        lines = source.lines
        arcs = [a for ln in lines.values() for a in ln.arcs]
        out[rel] = Tally((sum(1 for ln in lines.values() if ln.count > 0), len(lines)),
                         (sum(1 for a in arcs if a > 0), len(arcs)))
    return out


def fraction(pair: tuple[int, int]) -> Fraction:
    """covered / total, a file with nothing to cover counting whole."""
    return Fraction(pair[0], pair[1]) if pair[1] else Fraction(1)


def read_ratchet(text: str) -> dict[str, Tally]:
    """The ratchet file: `file lines C/T branches C/T` per line, `#` comments."""
    out = {}
    for line in text.splitlines():
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        rel, _l, lines, _b, branches = line.split()
        out[rel] = Tally(tuple(map(int, lines.split("/"))), tuple(map(int, branches.split("/"))))
    return out


def compare(measured: dict[str, Tally], ratchet: dict[str, Tally]) -> list[str]:
    """Every drop, and every file in one table and not the other."""
    found = []
    for rel in sorted(set(measured) | set(ratchet)):
        if rel not in ratchet:
            found.append(f"{rel}: measured, but the ratchet does not record it")
            continue
        if rel not in measured:
            found.append(f"{rel}: recorded in the ratchet, but nothing measured it")
            continue
        for kind in ("lines", "branches"):
            got, floor = getattr(measured[rel], kind), getattr(ratchet[rel], kind)
            if fraction(got) < fraction(floor):
                found.append(f"{rel}: {kind} {got[0]}/{got[1]} fell below the recorded {floor[0]}/{floor[1]}")
    return found


def render_ratchet(measured: dict[str, Tally]) -> str:
    """The ratchet file for a measurement."""
    head = ["# Per-file coverage of the bare-metal firmware's host suites (#665 lane FT), after the",
            "# exclusions in sw/firmware/gtest/README.md. Written by fw_coverage.py --write, which",
            "# refuses to record a drop; read by fw_coverage.py --check, which refuses one.",
            "# file  lines covered/total  branches covered/total"]
    rows = [f"{rel}  lines {t.lines[0]}/{t.lines[1]}  branches {t.branches[0]}/{t.branches[1]}"
            for rel, t in sorted(measured.items())]
    return "\n".join(head + rows) + "\n"


def report(raw: dict[str, Tally], kept: dict[str, Tally]) -> None:
    """The per-file table: before and after the exclusions."""
    print(f"{'file':<46} {'lines':>11} {'branches':>11}   after exclusions")
    for rel in sorted(kept):
        r, k = raw[rel], kept[rel]
        print(f"{rel:<46} {r.lines[0]:>5}/{r.lines[1]:<5} {r.branches[0]:>5}/{r.branches[1]:<5}   "
              f"lines {float(fraction(k.lines)) * 100:6.2f} %  branches {float(fraction(k.branches)) * 100:6.2f} %")


def measure(work: Path, lwsrp: Path | None, jobs: int) -> dict[str, Source]:
    """Run both gates in coverage mode into `work` and read what they left."""
    dirs = []
    for name, gate in GATES:
        out = work / name
        argv = [sys.executable, str(gate), "--coverage", str(out)]
        if name == "ctrl" and lwsrp is not None:
            argv += ["--lwsrp", str(lwsrp)]
        if name == "ctrl_nvm":
            argv += ["--jobs", str(jobs)]
        res = subprocess.run(argv, capture_output=True, text=True, check=False)
        tail = "\n".join((res.stdout + res.stderr).strip().splitlines()[-8:])
        print(f"[{'ok' if res.returncode == 0 else 'FAIL'}] {name} coverage run\n{tail}")
        if res.returncode != 0:
            raise Unmeasured(f"the {name} gate failed in coverage mode (exit {res.returncode})")
        dirs.append(out)
    return collect(dirs)


def main(argv: list[str] | None = None) -> int:
    """Measure, apply the exclusions, and hold the ratchet."""
    ap = argparse.ArgumentParser(description=__doc__.split("\n", 1)[0])
    mode = ap.add_mutually_exclusive_group(required=True)
    mode.add_argument("--check", action="store_true", help="refuse any drop below the ratchet")
    mode.add_argument("--write", action="store_true", help="record the measurement (never a drop)")
    mode.add_argument("--selftest", action="store_true", help="the planted cases")
    ap.add_argument("--lwsrp", type=Path, help="a lwSRP checkout at the pin: also run the lwsrp arm")
    ap.add_argument("--jobs", type=int, default=os.cpu_count() or 4, help="parallel builds")
    ap.add_argument("--keep", type=Path, help="keep the coverage builds here")
    args = ap.parse_args(argv)
    if args.selftest:
        from fw_coverage_selftest import run_cases
        return run_cases()
    try:
        with tempfile.TemporaryDirectory(prefix="fw-coverage.") as tmp:
            merged = measure(args.keep or Path(tmp), args.lwsrp, args.jobs)
    except Unmeasured as exc:
        print(f"UNMEASURED: {exc}")
        return 2
    raw = tally(merged)
    kept_lines, found = apply_exclusions(merged, exclusions(README.read_text(encoding="utf-8")))
    kept = tally(kept_lines)
    report(raw, kept)
    ratchet = read_ratchet(RATCHET.read_text(encoding="utf-8")) if RATCHET.exists() else {}
    drops = compare(kept, ratchet)
    if args.write:
        refused = [d for d in drops if "fell below" in d]
        if refused or found:
            print("\n".join(f"REFUSED: {d}" for d in refused + found))
            return 1
        RATCHET.write_text(render_ratchet(kept), encoding="utf-8")
        print(f"recorded {len(kept)} files in {RATCHET.relative_to(ROOT)}")
        return 0
    for x in found + drops:
        print(f"FINDING: {x}")
    print(f"firmware coverage: {'FAIL' if found or drops else 'PASS'} ({len(kept)} files)")
    return 1 if found or drops else 0


if __name__ == "__main__":
    sys.exit(main())
