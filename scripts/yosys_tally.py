#!/usr/bin/env python3
"""Validate exhaustive, disjoint Yosys shard evidence."""

from __future__ import annotations

import argparse
import sys
import tempfile
from collections import Counter
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, Sequence

EXPECTED_GATES = {
    "tied-input": True,
    "tap-purity": False,
}
REQUIRED_KEYS = {"kind", "name", "status", "blocking"}


@dataclass(frozen=True)
class Result:
    path: Path
    kind: str
    name: str
    status: str
    blocking: bool


def parse_result(path: Path) -> Result:
    values: dict[str, str] = {}
    try:
        lines = path.read_text(encoding="utf-8").splitlines()
    except OSError as exc:
        raise ValueError(f"{path}: unreadable: {exc}") from exc
    for number, line in enumerate(lines, 1):
        if not line or line.startswith("#"):
            continue
        if "=" not in line:
            raise ValueError(f"{path}:{number}: expected key=value")
        key, value = line.split("=", 1)
        if key in values:
            raise ValueError(f"{path}:{number}: duplicate key {key}")
        values[key] = value
    missing = REQUIRED_KEYS - values.keys()
    extra = values.keys() - REQUIRED_KEYS - {"mode", "cells"}
    if missing:
        raise ValueError(f"{path}: missing key(s): {', '.join(sorted(missing))}")
    if extra:
        raise ValueError(f"{path}: unknown key(s): {', '.join(sorted(extra))}")
    if values["kind"] not in {"top", "gate"}:
        raise ValueError(f"{path}: kind must be top or gate")
    if values["status"] not in {"PASS", "FAIL"}:
        raise ValueError(f"{path}: status must be PASS or FAIL")
    if values["blocking"] not in {"0", "1"}:
        raise ValueError(f"{path}: blocking must be 0 or 1")
    return Result(
        path=path,
        kind=values["kind"],
        name=values["name"],
        status=values["status"],
        blocking=values["blocking"] == "1",
    )


def read_expected(path: Path) -> list[str]:
    try:
        names = [line.strip() for line in path.read_text(encoding="utf-8").splitlines()
                 if line.strip()]
    except OSError as exc:
        raise ValueError(f"expected inventory unreadable: {exc}") from exc
    if not names:
        raise ValueError("expected top inventory is empty")
    duplicates = sorted(name for name, count in Counter(names).items() if count > 1)
    if duplicates:
        raise ValueError(f"expected inventory contains duplicates: {', '.join(duplicates)}")
    return names


def validate(
    roots: Iterable[Path],
    expected: Sequence[str],
    require_structural: bool,
) -> tuple[list[str], list[str], list[Result]]:
    errors: list[str] = []
    notes: list[str] = []
    results: list[Result] = []
    paths: list[Path] = []
    for root in roots:
        if not root.exists():
            errors.append(f"evidence root does not exist: {root}")
            continue
        paths.extend(sorted(root.rglob("*.result")))
    if not paths:
        errors.append("no Yosys result files found")
        return errors, notes, results

    for path in paths:
        try:
            results.append(parse_result(path))
        except ValueError as exc:
            errors.append(str(exc))

    expected_set = set(expected)
    top_results = [result for result in results if result.kind == "top"]
    top_counts = Counter(result.name for result in top_results)
    missing = sorted(expected_set - top_counts.keys())
    unexpected = sorted(top_counts.keys() - expected_set)
    duplicates = sorted(name for name, count in top_counts.items() if count > 1)
    if missing:
        errors.append("missing top evidence: " + ", ".join(missing))
    if unexpected:
        errors.append("unexpected top evidence: " + ", ".join(unexpected))
    if duplicates:
        errors.append("duplicate top evidence: " + ", ".join(duplicates))
    for result in top_results:
        if not result.blocking:
            errors.append(f"top evidence is non-blocking: {result.path}")
        if result.status != "PASS":
            errors.append(f"top failed: {result.name} ({result.path})")

    gate_results = [result for result in results if result.kind == "gate"]
    if require_structural:
        gate_counts = Counter(result.name for result in gate_results)
        for name, blocking in EXPECTED_GATES.items():
            count = gate_counts.get(name, 0)
            if count == 0:
                errors.append(f"missing structural evidence: {name}")
                continue
            if count > 1:
                errors.append(f"duplicate structural evidence: {name}")
            matches = [result for result in gate_results if result.name == name]
            for result in matches:
                if result.blocking != blocking:
                    errors.append(
                        f"structural blocking policy mismatch for {name}: {result.path}"
                    )
                if result.status != "PASS":
                    message = f"structural check failed: {name} ({result.path})"
                    if blocking:
                        errors.append(message)
                    else:
                        notes.append(message + " [informational by existing policy]")
        unexpected_gates = sorted(gate_counts.keys() - EXPECTED_GATES.keys())
        if unexpected_gates:
            errors.append("unexpected structural evidence: " + ", ".join(unexpected_gates))
    elif gate_results:
        errors.append("structural evidence supplied when it was not requested")

    return errors, notes, results


def write_result(root: Path, kind: str, name: str, status: str = "PASS",
                 blocking: bool = True, malformed: bool = False) -> None:
    path = root / f"{kind}-{name}.result"
    if malformed:
        path.write_text("not key value\n", encoding="utf-8")
        return
    path.write_text(
        f"kind={kind}\nname={name}\nstatus={status}\n"
        f"blocking={1 if blocking else 0}\n",
        encoding="utf-8",
    )


def selftest() -> int:
    expected = ["a", "b", "c"]
    failures = 0

    def run_case(name: str, mutate, want_error: bool) -> None:
        nonlocal failures
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            for top in expected:
                write_result(root, "top", top)
            write_result(root, "gate", "tied-input", blocking=True)
            write_result(root, "gate", "tap-purity", blocking=False)
            mutate(root)
            errors, _, _ = validate([root], expected, True)
            ok = bool(errors) == want_error
            print(f"  {'ok  ' if ok else 'FAIL'} {name}: errors={len(errors)}")
            failures += 0 if ok else 1

    run_case("complete evidence", lambda _: None, False)
    run_case("missing top", lambda root: (root / "top-b.result").unlink(), True)
    # Duplicate needs a second directory because one filename cannot coexist.
    with tempfile.TemporaryDirectory() as temp:
        root = Path(temp)
        left = root / "left"; right = root / "right"
        left.mkdir(); right.mkdir()
        for top in expected:
            write_result(left, "top", top)
        write_result(right, "top", "a")
        write_result(left, "gate", "tied-input", blocking=True)
        write_result(left, "gate", "tap-purity", blocking=False)
        errors, _, _ = validate([left, right], expected, True)
        ok = any("duplicate top" in error for error in errors)
        print(f"  {'ok  ' if ok else 'FAIL'} duplicate top across roots")
        failures += 0 if ok else 1

    run_case("unexpected top", lambda root: write_result(root, "top", "z"), True)
    run_case("failed top", lambda root: write_result(root, "top", "b", "FAIL"), True)
    run_case("malformed evidence", lambda root: write_result(root, "top", "b", malformed=True), True)
    run_case("missing tied gate", lambda root: (root / "gate-tied-input.result").unlink(), True)
    run_case("failed tied gate", lambda root: write_result(root, "gate", "tied-input", "FAIL", True), True)
    run_case("failed informational gate", lambda root: write_result(root, "gate", "tap-purity", "FAIL", False), False)

    print("selftest:", "PASS" if failures == 0 else f"{failures} FAILURE(S)")
    return 1 if failures else 0


def main(argv: Sequence[str]) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("roots", nargs="*", type=Path)
    parser.add_argument("--expected", required=False, type=Path)
    parser.add_argument("--require-structural", action="store_true")
    parser.add_argument("--selftest", action="store_true")
    args = parser.parse_args(argv[1:])

    if args.selftest:
        return selftest()
    if not args.roots:
        parser.error("at least one evidence root is required unless --selftest is used")
    if args.expected is None:
        parser.error("--expected is required unless --selftest is used")

    try:
        expected = read_expected(args.expected)
    except ValueError as exc:
        parser.error(str(exc))
    errors, notes, results = validate(args.roots, expected, args.require_structural)
    for note in notes:
        print("NOTE:", note)
    for error in errors:
        print("ERROR:", error, file=sys.stderr)
    top_results = [result for result in results if result.kind == "top"]
    print(
        f"Yosys evidence: expected={len(expected)} observed={len(top_results)} "
        f"errors={len(errors)}"
    )
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
