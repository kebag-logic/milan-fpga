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
#: Each member's hosted wall clock, in seconds, run in a LiteX leg on a worker
#: of its own: the verdict rows of the three leg receipts of run 41583428850,
#: the first run after the legs split. The legs are derived from these figures
#: and kept while each fits LEG_BUDGET at LARGEST. Measured inside the old whole
#: aggregate, after a builder leg in the same job, members cost otherwise
#: (test_ctrl_memory 113 there, 280 alone), so those figures are not used
#: (#737). A member the inventory holds and this table lacks is refused, so a
#: new simulation cannot join a leg unmeasured.
SECONDS = {
    "test_cpu_memory_port_cdc": 70,
    "test_ctrl_memory": 280,
    "test_gmii_rx_capture": 0,
    "test_gptp_tx_timestamp": 461,
    "test_pp_boot_bus_freeze": 25,
    "test_pp_mem_bridge": 14,
    "test_retained_cdc_storage": 331,
    "test_soc_timing_cuts": 240,
}
#: Each member's largest verdict-row seconds over every hosted run with the
#: legs apart, runs 41583428850, 41678609075 (attempts 1 and 3) and
#: 41705989293 (attempts 1 and 2). Every
#: bound and projection uses these; docs/testing/CI_WORKFLOWS.md states the
#: rule a later hosted measurement follows (#737).
LARGEST = {
    "test_cpu_memory_port_cdc": 72,
    "test_ctrl_memory": 284,
    "test_gmii_rx_capture": 0,
    "test_gptp_tx_timestamp": 477,
    "test_pp_boot_bus_freeze": 25,
    "test_pp_mem_bridge": 15,
    "test_retained_cdc_storage": 336,
    "test_soc_timing_cuts": 510,
}
LEGS = 3
#: A LiteX worker's own limit: its job's 45 minutes. The bound is this limit,
#: not the workflow's 30 minutes, which #737 acceptance 1 keeps open (#737).
JOB_LIMIT = 2700
#: Stated headroom a LiteX worker keeps under JOB_LIMIT for hosted variance (#737).
HEADROOM = 600
#: The largest elaborate worker span outside its gate steps and Verilator
#: build over the cited hosted runs: worker 1, run 41705989293 attempt 2 (#737).
SETUP = 739
#: The largest cold Verilator source build over the cited hosted runs: worker
#: 3, run 41678609075 attempt 1 (#737).
COLD_VERILATOR = 431
#: The largest LiteX runner self-test over the cited hosted runs, its leg step
#: less its verdict rows: worker 2, run 41705989293 attempt 2 (#737).
SELFTEST = 4
#: The simulation seconds one leg may hold at LARGEST, so that a cold LiteX
#: worker at every component's largest stays HEADROOM inside JOB_LIMIT. Runner
#: queueing is not in it (#737).
LEG_BUDGET = JOB_LIMIT - HEADROOM - SETUP - COLD_VERILATOR - SELFTEST
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


def partition(names: list[str], seconds: dict[str, int] | None = None, legs: int = LEGS,
              largest: dict[str, int] | None = None) -> list[list[str]]:
    """Longest measured member first onto the least-loaded leg; each leg then in inventory order.

    The legs come from `seconds`; each must hold at most LEG_BUDGET at `largest`."""
    seconds = SECONDS if seconds is None else seconds
    largest = LARGEST if largest is None else largest
    validate_inventory(names)
    unmeasured = [name for name in names if name not in seconds or name not in largest]
    if unmeasured:
        raise ValueError("no measured seconds for " + ", ".join(unmeasured)
                         + "; measure it hosted and add it to SECONDS and LARGEST in scripts/ci_litex_legs.py")
    stale = sorted((set(seconds) | set(largest)) - set(names))
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
    held = max(sum(largest[name] for name in names if owner[name] == leg) for leg in range(legs))
    if held > LEG_BUDGET:
        raise ValueError(f"a LiteX leg holds {held} measured seconds at its largest, above its {LEG_BUDGET}; "
                         "re-derive the legs or add a leg")
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
        if type(receipt["exit"]) is not int or receipt["exit"] != 0:
            raise ValueError(f"LiteX leg {leg}: the runner exited {receipt['exit']}")
    absent = [name for name, owners in ran.items() if not owners]
    repeated = [name for name, owners in ran.items() if len(owners) > 1]
    if absent:
        raise ValueError("LiteX simulations ran in no leg: " + ", ".join(absent))
    # Defence in depth: the per-leg selection check above already refuses a simulation run twice, so this
    # branch is reached only if that check is weakened (#737).
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
                print(f"{leg}/{LEGS} {sum(SECONDS[name] for name in members)}s, at its largest "
                      f"{sum(LARGEST[name] for name in members)}s " + shlex.join(members))
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
