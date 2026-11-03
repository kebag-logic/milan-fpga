#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""Run the standalone LiteX simulations in measured legs and judge their union (#737).

``scripts/run_litex_sims.sh`` owns the pinned inventory (``--list``), runs a
named subset (``--only``) and writes one verdict row per member it ran
(``verdicts.tsv``). Only the measured seconds, the leg partition derived from
them and the union proof live here. Run one after another the members took
18 to 25 minutes hosted after the setup and a builder leg in the same job,
which sat within a minute of that job's 45-minute limit (#737).
"""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import shlex
import subprocess
import sys

from ci_case_receipts import canonical, source_identity, validate_inventory

ROOT = Path(__file__).resolve().parents[1]
RUNNER = "scripts/run_litex_sims.sh"
VERDICTS = "verdicts.tsv"
#: Each member's largest hosted wall clock, in seconds, over the
#: elaborate-gates-1 logs of runs 41470524727, 41526004847 and 41554508699 and
#: of run 41476923392's first three attempts, read from the gaps between the
#: runner's consecutive result lines. A member the inventory holds and this
#: table lacks is refused, so a new simulation cannot join a leg unmeasured.
SECONDS = {
    "test_cpu_memory_port_cdc": 72,
    "test_ctrl_memory": 113,
    "test_gmii_rx_capture": 1,
    "test_gptp_tx_timestamp": 477,
    "test_pp_boot_bus_freeze": 26,
    "test_pp_mem_bridge": 14,
    "test_retained_cdc_storage": 348,
    "test_soc_timing_cuts": 534,
}
LEGS = 3
#: The simulation seconds one leg may hold. A hosted job's 30 minutes (#737),
#: less its measured 112 seconds of setup, a 300-second cold Verilator build
#: and 60 seconds of evidence upload, leaves 1328; this keeps the rest as margin.
LEG_BUDGET = 1200
SCHEMA = 1


def inventory(root: Path = ROOT) -> list[str]:
    """Read the runner anew; receipts cannot define their own universe."""
    result = subprocess.run(["bash", RUNNER, "--list"], cwd=root, check=True, capture_output=True, text=True)
    paths = result.stdout.split()
    if any(not path.startswith("sw/litex/") or not path.endswith(".py") for path in paths):
        raise ValueError("unexpected LiteX runner inventory line")
    names = [path.removeprefix("sw/litex/").removesuffix(".py") for path in paths]
    validate_inventory(names)
    return names


def partition(names: list[str], seconds: dict[str, int] | None = None, legs: int = LEGS) -> list[list[str]]:
    """Longest measured member first onto the least-loaded leg; each leg then in inventory order."""
    seconds = SECONDS if seconds is None else seconds
    validate_inventory(names)
    unmeasured = [name for name in names if name not in seconds]
    if unmeasured:
        raise ValueError("no measured seconds for " + ", ".join(unmeasured)
                         + "; measure it hosted and add it to SECONDS in scripts/ci_litex_legs.py")
    stale = sorted(set(seconds) - set(names))
    if stale:
        raise ValueError("measured seconds for a member outside the inventory: " + ", ".join(stale))
    if legs < 1 or legs > len(names):
        raise ValueError("leg count must be between one and the inventory size")
    loads = [0] * legs
    owner = {}
    for name in sorted(names, key=lambda name: (-seconds[name], names.index(name))):
        leg = loads.index(min(loads))
        owner[name] = leg
        loads[leg] += seconds[name]
    if max(loads) > LEG_BUDGET:
        raise ValueError(f"a LiteX leg holds {max(loads)} measured seconds, above its {LEG_BUDGET}; add a leg")
    return [[name for name in names if owner[name] == leg] for leg in range(legs)]


def outdir(command: list[str]) -> Path:
    """The template's undivided aggregate command, and the log directory it names."""
    if len(command) != 2 or command[0] != RUNNER or command[1].startswith("-"):
        raise ValueError("a LiteX leg runs `" + RUNNER + " <logdir>` as its template step does")
    return Path(command[1])


def run(leg: int, receipt: Path, command: list[str]) -> int:
    """Run one leg's selection through the runner and bind its verdict rows to the source."""
    logs = outdir(command)
    names = inventory()
    legs = partition(names)
    if not 0 <= leg < len(legs):
        raise ValueError("unknown LiteX leg")
    head, tree = source_identity(ROOT)
    # A table left by an earlier run is not this leg's evidence.
    table = ROOT / logs / VERDICTS
    table.unlink(missing_ok=True)
    rc = subprocess.run([*command, "--only", ",".join(legs[leg])], cwd=ROOT, check=False).returncode
    if source_identity(ROOT) != (head, tree):
        raise ValueError("source identity changed during the LiteX leg")
    rows = []
    if table.exists():
        for line in table.read_text().splitlines():
            simulation, verdict, seconds = line.split("\t")
            rows.append({"simulation": simulation, "verdict": verdict, "seconds": int(seconds)})
    receipt.parent.mkdir(parents=True, exist_ok=True)
    with receipt.open("xb") as stream:
        stream.write(canonical({"schema": SCHEMA, "head": head, "tree": tree, "leg": leg, "legs": len(legs),
                                "inventory": names, "selected": legs[leg], "exit": rc,
                                "results": rows}) + b"\n")
    return rc


def union(receipts: list[dict], head: str, tree: str, names: list[str] | None = None) -> dict:
    """Every simulation exactly once, in its measured leg, each a pass."""
    names = inventory() if names is None else names
    legs = partition(names)
    seen: list[int] = []
    ran: dict[str, list[int]] = {name: [] for name in names}
    observed = {}
    for receipt in receipts:
        if (set(receipt) != {"schema", "head", "tree", "leg", "legs", "inventory", "selected", "exit", "results"}
                or receipt["schema"] != SCHEMA or receipt["legs"] != len(legs)):
            raise ValueError("LiteX leg receipt schema differs")
        if (receipt["head"], receipt["tree"]) != (head, tree):
            raise ValueError("LiteX leg source identity differs from the run")
        leg = receipt["leg"]
        if type(leg) is not int or not 0 <= leg < len(legs) or leg in seen:
            raise ValueError("unknown or duplicated LiteX leg")
        seen.append(leg)
        if receipt["inventory"] != names:
            raise ValueError(f"LiteX leg {leg}: inventory differs from the runner")
        if receipt["selected"] != legs[leg]:
            raise ValueError(f"LiteX leg {leg}: selection differs from its measured leg")
        rows = receipt["results"]
        if not isinstance(rows, list) or any(
                not isinstance(row, dict) or set(row) != {"simulation", "verdict", "seconds"}
                or not isinstance(row["simulation"], str) or type(row["seconds"]) is not int for row in rows):
            raise ValueError(f"LiteX leg {leg}: verdict rows differ from schema")
        for row in rows:
            if row["simulation"] not in ran:
                raise ValueError(f"LiteX leg {leg} ran {row['simulation']}, which is not in the inventory")
            ran[row["simulation"]].append(leg)
            if row["verdict"] != "PASS":
                raise ValueError(f"{row['simulation']}: {row['verdict']} in LiteX leg {leg}")
            observed[row["simulation"]] = {"simulation": row["simulation"], "verdict": row["verdict"]}
        executed = [row["simulation"] for row in rows]
        if executed != legs[leg]:
            missing = [name for name in legs[leg] if name not in executed]
            raise ValueError(f"LiteX leg {leg} did not run its selection exactly once: "
                             + (", ".join(missing) or "order or extra simulations"))
        if receipt["exit"] != 0:
            raise ValueError(f"LiteX leg {leg}: the runner exited {receipt['exit']}")
    absent = [name for name, owners in ran.items() if not owners]
    repeated = [name for name, owners in ran.items() if len(owners) > 1]
    if absent:
        raise ValueError("LiteX simulations ran in no leg: " + ", ".join(absent))
    if repeated:
        raise ValueError("LiteX simulations ran in more than one leg: " + ", ".join(repeated))
    if sorted(seen) != list(range(len(legs))):
        raise ValueError("missing LiteX leg")
    return {"suite": "litex", "head": head, "tree": tree, "inventory": names,
            "legs": [{"shard": f"{leg}/{len(legs)}", "cases": cases} for leg, cases in enumerate(legs)],
            "union": "pass",
            "verdicts_sha256": hashlib.sha256(canonical([observed[name] for name in names])).hexdigest()}


def parse(argv: list[str]) -> tuple[argparse.Namespace, list[str]]:
    """Own options before the first `--`; the runner command, unparsed, after it."""
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="operation", required=True)
    execute = sub.add_parser("run")
    execute.add_argument("leg", choices=[*map(str, range(LEGS))])
    execute.add_argument("--receipt", required=True, type=Path)
    check = sub.add_parser("union")
    check.add_argument("--head", required=True)
    check.add_argument("--tree", required=True)
    check.add_argument("--output", type=Path)
    check.add_argument("receipts", nargs="+", type=Path)
    sub.add_parser("legs")
    split = argv.index("--") if "--" in argv else len(argv)
    args = parser.parse_args(argv[:split])
    command = argv[split + 1:]
    if (args.operation == "run") != bool(command):
        parser.error("a leg needs its runner command after `--`, and only a leg takes one")
    return args, command


def main() -> int:
    """Run one leg, print the measured partition, or verify a union."""
    args, command = parse(sys.argv[1:])
    try:
        if args.operation == "run":
            return run(int(args.leg), args.receipt, command)
        if args.operation == "legs":
            for leg, members in enumerate(partition(inventory())):
                print(f"{leg}/{LEGS} {sum(SECONDS[name] for name in members)}s " + shlex.join(members))
            return 0
        result = union([json.loads(path.read_text()) for path in args.receipts], args.head, args.tree)
        if args.output:
            args.output.write_bytes(canonical(result) + b"\n")
        print(f"litex: {len(result['inventory'])} simulations exactly once, each a pass")
    except (OSError, ValueError, KeyError, TypeError, subprocess.CalledProcessError) as exc:
        print(f"LiteX legs refused: {exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
