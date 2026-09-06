#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""Content-addressed result cache for syn/yosys/run.sh (#350).

A portability-gate top whose inputs cannot have changed is skipped: the key
is a digest over everything the verdict depends on, and the stored value is
the record the gate would have produced, never anything executable.

THE KEY. sha256 over a canonical text naming the top, the mode, the sha256 of
the staged sv2v output, the exact Yosys program with the run's scratch
directory replaced by a placeholder, the Yosys version string, the sha256 of
the Yosys binary and the sv2v version string. Any of those moving is a miss.

THE HIT RULE. A key hit is not a pass. The entry must carry a PASS record
whose recorded inputs equal the current ones field by field, and the cell
count it publishes is RE-DERIVED from the stored `stat -json` with the same
extractor `run.sh` uses on a live run; an entry whose stored JSON disagrees
with its own `cells=` line, whose JSON is missing or unreadable, whose status
is not PASS, or whose record is malformed is REFUSED (exit 2) and the top runs
as if there were no cache. So a stale or forged entry can cost a synthesis,
never make a wrong number green.

THE TRUST BOUNDARY (#270). Two directories: `--dir` is this run's writable
per-head state, `--seed` an optional read-only trusted seed published from
`dev`. Lookups read the per-head directory first and the seed second; stores
write the per-head directory only and never a FAIL. This module never deletes
or rewrites an existing entry.

usage:
  result_cache.py lookup --dir D [--seed S] <inputs>      exit 0 hit (prints cells=N), 1 miss, 2 refused
  result_cache.py store  --dir D <inputs> --cells N --stat-json F
  result_cache.py key    <inputs>                          prints the key
  result_cache.py --selftest
<inputs> = --top T --mode M --sv2v-file F --program P --yosys-version V --yosys-bin B --sv2v-version W
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import sys
import tempfile
from dataclasses import dataclass
from pathlib import Path

SCHEMA = "milan-yosys-result-cache/1"
RECORD = "record"
STAT_JSON = "stat.json"
INPUT_FIELDS = ("top", "mode", "sv2v_sha256", "program", "yosys_version",
                "yosys_sha256", "sv2v_version")
EXIT_HIT, EXIT_MISS, EXIT_REFUSED = 0, 1, 2


@dataclass(frozen=True)
class Inputs:
    """Everything a verdict depends on, as the gate names it."""
    top: str
    mode: str
    sv2v_sha256: str
    program: str
    yosys_version: str
    yosys_sha256: str
    sv2v_version: str

    def canonical(self) -> str:
        """The text the key digests: one `name=value` line per field, with
        the multi-line program flattened so a newline cannot forge a field."""
        lines = [SCHEMA]
        for name in INPUT_FIELDS:
            lines.append(f"{name}={getattr(self, name).replace(chr(10), ' ')}")
        return "\n".join(lines) + "\n"

    def key(self) -> str:
        """The content address."""
        return hashlib.sha256(self.canonical().encode("utf-8")).hexdigest()


def sha256_file(path: Path) -> str:
    """The digest of a file's bytes, streamed."""
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1 << 20), b""):
            digest.update(chunk)
    return digest.hexdigest()


def inputs_from_args(args: argparse.Namespace) -> Inputs:
    """The current run's inputs, digesting the staged sv2v output."""
    return Inputs(top=args.top, mode=args.mode,
                  sv2v_sha256=sha256_file(Path(args.sv2v_file)),
                  program=args.program, yosys_version=args.yosys_version,
                  yosys_sha256=args.yosys_bin_sha256, sv2v_version=args.sv2v_version)


def num_cells(stat_json: Path) -> int | None:
    """`design.num_cells` from a `stat -json` file, exactly as run.sh reads a
    live run's: a non-negative int, or None for anything else."""
    try:
        with stat_json.open(encoding="utf-8") as handle:
            value = json.load(handle)["design"]["num_cells"]
    except (OSError, ValueError, KeyError, TypeError):
        return None
    if isinstance(value, bool) or not isinstance(value, int) or value < 0:
        return None
    return value


def parse_record(text: str) -> dict[str, str] | None:
    """`name=value` lines into a mapping; None for a malformed record."""
    fields: dict[str, str] = {}
    for line in text.splitlines():
        if "=" not in line:
            return None
        name, value = line.split("=", 1)
        if not name or name in fields:
            return None
        fields[name] = value
    return fields


def verify_entry(entry: Path, inputs: Inputs) -> tuple[int | None, str]:
    """The hit rule over one entry directory: (cells, "") on a verified hit,
    (None, reason) on a refusal."""
    try:
        record = parse_record((entry / RECORD).read_text(encoding="utf-8"))
    except OSError as error:
        return None, f"record unreadable: {error}"
    if record is None:
        return None, "record malformed"
    if record.get("schema") != SCHEMA:
        return None, f"schema {record.get('schema')!r} is not {SCHEMA}"
    if record.get("status") != "PASS":
        return None, f"status {record.get('status')!r} is not PASS"
    for name in INPUT_FIELDS:
        want = getattr(inputs, name).replace("\n", " ")
        if record.get(name) != want:
            return None, f"recorded {name} differs from the current one"
    derived = num_cells(entry / STAT_JSON)
    if derived is None:
        return None, "stored stat.json carries no design.num_cells"
    if record.get("cells") != str(derived):
        return None, (f"recorded cells={record.get('cells')} but the stored "
                      f"stat.json derives {derived}")
    return derived, ""


def lookup(dirs: list[Path], inputs: Inputs) -> tuple[int, str]:
    """(exit status, message). Per-head state first, then the seed; the first
    directory holding the key decides, hit or refusal."""
    key = inputs.key()
    for base in dirs:
        entry = base / key
        if not entry.is_dir():
            continue
        cells, reason = verify_entry(entry, inputs)
        if cells is None:
            return EXIT_REFUSED, f"refused {key[:12]} in {base}: {reason}"
        return EXIT_HIT, f"cells={cells}"
    return EXIT_MISS, f"miss {key[:12]}"


def store(base: Path, inputs: Inputs, cells: str, stat_json: Path) -> str:
    """Write one PASS entry atomically into the per-head directory, or raise
    ValueError on anything that must not be cached."""
    derived = num_cells(stat_json)
    if derived is None:
        raise ValueError("stat.json carries no design.num_cells; nothing to store")
    if str(derived) != cells:
        raise ValueError(f"cells={cells} disagrees with stat.json ({derived})")
    key = inputs.key()
    entry = base / key
    if entry.exists():
        return f"kept {key[:12]}"
    base.mkdir(parents=True, exist_ok=True)
    staging = Path(tempfile.mkdtemp(prefix=f".{key[:12]}.", dir=base))
    lines = [f"schema={SCHEMA}", "status=PASS", f"cells={derived}"]
    lines += [f"{n}={getattr(inputs, n).replace(chr(10), ' ')}" for n in INPUT_FIELDS]
    (staging / RECORD).write_text("\n".join(lines) + "\n", encoding="utf-8")
    (staging / STAT_JSON).write_bytes(stat_json.read_bytes())
    try:
        os.rename(staging, entry)
    except OSError:
        # a concurrent writer of the same key won; its bytes are ours
        for leftover in staging.iterdir():
            leftover.unlink()
        staging.rmdir()
    return f"stored {key[:12]}"


def add_input_args(parser: argparse.ArgumentParser) -> None:
    """The seven inputs every sub-command names."""
    for flag in ("--top", "--mode", "--sv2v-file", "--program", "--yosys-version",
                 "--yosys-bin-sha256", "--sv2v-version"):
        parser.add_argument(flag, required=True)


def build_parser() -> argparse.ArgumentParser:
    """The command line."""
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--selftest", action="store_true")
    sub = parser.add_subparsers(dest="command")
    for name in ("lookup", "store", "key"):
        p = sub.add_parser(name)
        add_input_args(p)
        if name != "key":
            p.add_argument("--dir", required=True)
        if name == "lookup":
            p.add_argument("--seed")
        if name == "store":
            p.add_argument("--cells", required=True)
            p.add_argument("--stat-json", required=True)
    return parser


def main(argv: list[str]) -> int:
    """Dispatch; the exit status is the answer run.sh reads."""
    parser = build_parser()
    args = parser.parse_args(argv)
    if args.selftest:
        return selftest()
    if args.command is None:
        parser.print_usage(sys.stderr)
        return 2
    inputs = inputs_from_args(args)
    if args.command == "key":
        print(inputs.key())
        return 0
    if args.command == "lookup":
        dirs = [Path(args.dir)] + ([Path(args.seed)] if args.seed else [])
        status, message = lookup(dirs, inputs)
        print(message, file=sys.stdout if status == EXIT_HIT else sys.stderr)
        return status
    try:
        print(store(Path(args.dir), inputs, args.cells, Path(args.stat_json)))
    except (ValueError, OSError) as error:
        print(f"result_cache: not stored: {error}", file=sys.stderr)
        return 2
    return 0


# --- self-test ---------------------------------------------------------------

def _inputs(sv2v: Path, **overrides: str) -> Inputs:
    fields = dict(top="T", mode="full", sv2v_sha256=sha256_file(sv2v),
                  program="read_verilog @TMP@/T.v; synth -top T; hierarchy -check; stat -top T",
                  yosys_version="Yosys 0.66", yosys_sha256="ab" * 32, sv2v_version="v0.0.12")
    fields.update(overrides)
    return Inputs(**fields)


def _stat(path: Path, cells: int) -> Path:
    path.write_text(json.dumps({"design": {"num_cells": cells}}), encoding="utf-8")
    return path


def _key_arms(problems: list[str], work: Path) -> None:
    """Arm 1: every input moves the key; the same inputs give the same key."""
    sv2v = work / "T.v"; sv2v.write_text("module T; endmodule\n")
    base = _inputs(sv2v)
    if base.key() != _inputs(sv2v).key():
        problems.append("the key is not a function of its inputs")
    other = work / "T2.v"; other.write_text("module T; wire x; endmodule\n")
    variants = {
        "sv2v output": _inputs(other), "program": _inputs(sv2v, program="synth -top T"),
        "yosys version": _inputs(sv2v, yosys_version="Yosys 0.33"),
        "yosys binary": _inputs(sv2v, yosys_sha256="cd" * 32),
        "sv2v version": _inputs(sv2v, sv2v_version="v0.0.11"),
        "top": _inputs(sv2v, top="U"), "mode": _inputs(sv2v, mode="elaborate"),
    }
    for what, variant in variants.items():
        if variant.key() == base.key():
            problems.append(f"changing the {what} did not change the key")


def _hit_arms(problems: list[str], work: Path) -> None:
    """Arms 2-9: a stored PASS hits with its re-derived count; every planted
    defect is refused rather than trusted; the seed is read, never written."""
    sv2v = work / "H.v"; sv2v.write_text("module H; endmodule\n")
    inputs = _inputs(sv2v, top="H")
    head, seed = work / "head", work / "seed"
    stat = _stat(work / "stat.json", 42)
    store(head, inputs, "42", stat)
    status, message = lookup([head], inputs)
    if (status, message) != (EXIT_HIT, "cells=42"):
        problems.append(f"a stored PASS did not hit: {status} {message}")
    if lookup([head], _inputs(sv2v, top="H", mode="elaborate"))[0] != EXIT_MISS:
        problems.append("a different mode hit the full-mode entry")
    entry = head / inputs.key()
    record = (entry / RECORD).read_text()
    (entry / RECORD).write_text(record.replace("cells=42", "cells=7"))
    if lookup([head], inputs)[0] != EXIT_REFUSED:
        problems.append("a forged cells= line was trusted")
    (entry / RECORD).write_text(record)
    _stat(entry / STAT_JSON, 43)
    if lookup([head], inputs)[0] != EXIT_REFUSED:
        problems.append("a stored stat.json disagreeing with cells= was trusted")
    (entry / STAT_JSON).unlink()
    if lookup([head], inputs)[0] != EXIT_REFUSED:
        problems.append("a missing stat.json was trusted")
    _stat(entry / STAT_JSON, 42)
    (entry / RECORD).write_text(record.replace("status=PASS", "status=FAIL"))
    if lookup([head], inputs)[0] != EXIT_REFUSED:
        problems.append("a FAIL entry was served as a hit")
    (entry / RECORD).write_text("garbage\n")
    if lookup([head], inputs)[0] != EXIT_REFUSED:
        problems.append("a malformed record was trusted")
    (entry / RECORD).write_text(record.replace("yosys_sha256=" + "ab" * 32,
                                               "yosys_sha256=" + "ef" * 32))
    if lookup([head], inputs)[0] != EXIT_REFUSED:
        problems.append("an entry recording another yosys binary under this key was trusted")
    (entry / RECORD).write_text(record)
    try:
        store(head, inputs, "41", stat)
        problems.append("store accepted a cells= that disagrees with stat.json")
    except ValueError:
        pass
    try:
        store(head, inputs, "42", work / "absent.json")
        problems.append("store accepted a missing stat.json")
    except ValueError:
        pass
    # the seed is read second and never written
    seed_inputs = _inputs(sv2v, top="S")
    store(seed, seed_inputs, "42", stat)
    seed.chmod(0o555)
    try:
        status, message = lookup([work / "empty-head", seed], seed_inputs)
        if (status, message) != (EXIT_HIT, "cells=42"):
            problems.append(f"a seed entry did not hit through an empty head: {status} {message}")
        if any(seed.iterdir()) and len(list(seed.iterdir())) != 1:
            problems.append("lookup wrote into the seed")
        store(work / "empty-head", seed_inputs, "42", stat)
        if not (work / "empty-head" / seed_inputs.key()).is_dir():
            problems.append("store did not write the per-head directory")
        if len(list(seed.iterdir())) != 1:
            problems.append("store wrote into the seed")
    finally:
        seed.chmod(0o755)


def selftest() -> int:
    """Run every arm in a scratch directory; exit 1 naming each failure."""
    problems: list[str] = []
    with tempfile.TemporaryDirectory(prefix="result-cache-selftest.") as tmp:
        work = Path(tmp)
        _key_arms(problems, work)
        _hit_arms(problems, work)
    for problem in problems:
        print(f"SELFTEST FAIL: {problem}", file=sys.stderr)
    print(f"result_cache selftest: {'OK' if not problems else 'FAIL'} "
          f"(7 key arms, 12 hit-rule and trust arms)")
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
