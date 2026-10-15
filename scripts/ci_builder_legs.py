#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""Run the end-station builder gates in measured legs and judge their union.

The driver owns the ordered gate inventory (``--list``), runs a named subset
(``--gates``) and records each gate's verdict and NOT RUN rows
(``--receipt``). Only the measured leg boundary and the union proof live here.
``--require-elaboration`` and ``--require-rv32`` are judged on the union,
never per leg: a leg holding no elaboration gate passes them vacuously.
"""

from __future__ import annotations

import argparse
import hashlib
import importlib
import json
from pathlib import Path
import subprocess
import sys
import tempfile

from ci_case_receipts import canonical, source_identity, validate_inventory

ROOT = Path(__file__).resolve().parents[1]
DRIVER = "sw/builder/test_builder.py"
#: Gates measured to need a leg of their own: 945.182 of the 1292.671 seconds
#: the unsharded command took in the shipping image at 16 CPUs. Every other
#: gate runs in the last leg, in inventory order.
ISOLATED = ("test_baremetal_profile_contract",)
LEGS = len(ISOLATED) + 1
#: The gates each requirement judges, named here rather than read from the
#: inventory, so that one deleted from the inventory or run in a leg without
#: the flag is refused by name. The bare-metal profile gate reads
#: --require-rv32; the gates that consult the LiteX interpreter, and the
#: recipe gate's toolchain classifier, record the skip kinds
#: --require-elaboration refuses.
REQUIRED = {
    "--require-elaboration": (
        "test_soc_option_refusals", "test_commercial_timing_grade",
        "test_clock_crossing_constraints", "test_gptp_plane_reaches_the_instance",
        "test_gptp_plane_instance_gate_bites", "test_optional_blocks_reach_the_instance",
        "test_optional_block_instance_gate_bites", "test_clock_plan_reaches_the_instance",
        "test_clock_plan_instance_gate_bites", "test_datapath_params_match_the_instance",
        "test_datapath_params_gate_bites", "test_every_recipe_elaborates",
        "test_recipe_smoke_gate_bites", "test_toolchain_patches_are_applied",
        "test_toolchain_patch_gate_bites"),
    "--require-rv32": ("test_baremetal_profile_contract",),
}
SCHEMA = 1


def inventory(root: Path = ROOT) -> list[str]:
    """Read the driver anew; receipts cannot define their own universe."""
    result = subprocess.run([sys.executable, DRIVER, "--list"], cwd=root, check=True,
                            capture_output=True, text=True)
    names = json.loads(result.stdout)
    validate_inventory(names)
    return names


def partition(names: list[str]) -> list[list[str]]:
    """Each measured gate alone, then every other gate in inventory order."""
    absent = [name for name in ISOLATED if name not in names]
    if absent:
        raise ValueError("measured leg gate absent from the driver inventory: " + ", ".join(absent))
    return [[name] for name in ISOLATED] + [[name for name in names if name not in ISOLATED]]


def run(leg: int | None, receipt: Path, command: list[str]) -> int:
    """Run one leg, or with None the unsharded reference, binding the driver's receipt."""
    if command[:2] != ["python3", DRIVER]:
        raise ValueError("a builder leg runs " + DRIVER + " as its template step does")
    legs = partition(inventory())
    if leg is not None and not 0 <= leg < len(legs):
        raise ValueError("unknown builder leg")
    selection = [] if leg is None else ["--gates", ",".join(legs[leg])]
    head, tree = source_identity(ROOT)
    with tempfile.TemporaryDirectory(prefix="builder-leg-") as temporary:
        record = Path(temporary) / "driver.json"
        rc = subprocess.run([*command, *selection, "--receipt", str(record)], cwd=ROOT,
                            check=False).returncode
        if not record.exists():
            return rc or 1
        driver = json.loads(record.read_text())
    if source_identity(ROOT) != (head, tree):
        raise ValueError("source identity changed during the builder leg")
    receipt.parent.mkdir(parents=True, exist_ok=True)
    with receipt.open("xb") as stream:
        stream.write(canonical({"schema": SCHEMA, "head": head, "tree": tree, "leg": leg,
                                "legs": len(legs), "driver": driver}) + b"\n")
    return rc


def elaboration_verdict(ledger: list[tuple[str, str, str]]) -> int:
    """The driver's own --require-elaboration judgement, applied to the union ledger."""
    sys.path.insert(0, str(ROOT / "sw/builder"))
    return importlib.import_module("test_builder")._require_elaboration_verdict(ledger)


def driver_rows(leg: int | None, driver: dict, expected: list[str], names: list[str]) -> list[dict]:
    """One driver receipt's executed gates, refused unless they are exactly its selection."""
    if set(driver) != {"inventory", "selected", "requirements", "gates", "require_elaboration"}:
        raise ValueError(f"builder leg {leg}: driver receipt fields differ")
    if driver["inventory"] != names:
        raise ValueError(f"builder leg {leg}: driver inventory differs from the driver")
    if driver["selected"] != expected:
        raise ValueError(f"builder leg {leg}: selection differs from its measured leg")
    flags = driver["requirements"]
    if not isinstance(flags, list) or not set(flags) <= set(REQUIRED) or len(set(flags)) != len(flags):
        raise ValueError(f"builder leg {leg}: unknown requirement flags")
    if driver["require_elaboration"] != (0 if "--require-elaboration" in flags else None):
        raise ValueError(f"builder leg {leg}: its own --require-elaboration verdict did not pass")
    rows = driver["gates"]
    if not isinstance(rows, list) or any(
            not isinstance(row, dict) or set(row) != {"gate", "verdict", "not_run"}
            or row["verdict"] != "pass" or not isinstance(row["not_run"], list)
            or any(not isinstance(item, list) or len(item) != 3
                   or not all(isinstance(part, str) for part in item) for item in row["not_run"])
            for row in rows):
        raise ValueError(f"builder leg {leg}: gate verdict rows differ from schema or did not pass")
    ran = [row["gate"] for row in rows]
    if ran != expected:
        missing = [name for name in expected if name not in ran]
        raise ValueError(f"builder leg {leg} did not run its selection exactly once: "
                         + (", ".join(missing) or "order or extra gates"))
    return rows


def union(receipts: list[dict], head: str, tree: str, names: list[str] | None = None) -> dict:
    """Every gate exactly once, each a pass, with both requirements judged on the union."""
    names = inventory() if names is None else names
    validate_inventory(names)
    legs = partition(names)
    executed: dict[str, tuple[dict, list[str]]] = {}
    seen = []
    for receipt in receipts:
        if (set(receipt) != {"schema", "head", "tree", "leg", "legs", "driver"}
                or receipt["schema"] != SCHEMA or receipt["legs"] != len(legs)):
            raise ValueError("builder leg receipt schema differs")
        if (receipt["head"], receipt["tree"]) != (head, tree):
            raise ValueError("builder leg source identity differs from the run")
        leg = receipt["leg"]
        if type(leg) is not int or not 0 <= leg < len(legs) or leg in seen:
            raise ValueError("unknown or duplicated builder leg")
        seen.append(leg)
        for row in driver_rows(leg, receipt["driver"], legs[leg], names):
            executed[row["gate"]] = (row, receipt["driver"]["requirements"])
    # Owners first: a lost leg, a deleted gate or a leg without the flag is
    # refused naming the gates the requirement no longer judges.
    for flag, owners in REQUIRED.items():
        absent = [gate for gate in owners if gate not in names]
        unrun = [gate for gate in owners if gate in names and gate not in executed]
        unjudged = [gate for gate in owners if gate in executed and flag not in executed[gate][1]]
        for gates, why in ((absent, "absent from the driver inventory"), (unrun, "ran in no leg"),
                           (unjudged, "ran only in a leg without the flag")):
            if gates:
                raise ValueError(f"{flag} on the union: {', '.join(gates)} {why}")
    if sorted(seen) != list(range(len(legs))):
        raise ValueError("missing builder leg")
    ledger = [tuple(item) for name in names for item in executed[name][0]["not_run"]]
    if elaboration_verdict(ledger):
        raise ValueError("--require-elaboration on the union: the ledger holds a toolchain skip")
    observed = [executed[name][0] for name in names]
    return {"suite": "builder", "head": head, "tree": tree, "inventory": names,
            "legs": [{"shard": f"{leg}/{len(legs)}", "cases": cases} for leg, cases in enumerate(legs)],
            "requirements": {flag: list(owners) for flag, owners in REQUIRED.items()},
            "not_run": [list(item) for item in ledger], "union": "pass",
            "verdicts_sha256": hashlib.sha256(canonical(observed)).hexdigest()}


def compare(reference: dict, receipts: list[dict], head: str, tree: str,
            names: list[str] | None = None) -> dict:
    """Require per-gate verdicts and the NOT RUN ledger to equal one unsharded run."""
    names = inventory() if names is None else names
    result = union(receipts, head, tree, names)
    if (set(reference) != {"schema", "head", "tree", "leg", "legs", "driver"}
            or reference["leg"] is not None or (reference["head"], reference["tree"]) != (head, tree)):
        raise ValueError("reference must be an unsharded run of the same source")
    if sorted(reference["driver"]["requirements"]) != sorted(REQUIRED):
        raise ValueError("reference must carry both requirements")
    rows = driver_rows(None, reference["driver"], names, names)
    sharded = {row["gate"]: row for receipt in receipts for row in receipt["driver"]["gates"]}
    for row in rows:
        if sharded[row["gate"]] != row:
            raise ValueError(row["gate"] + ": sharded verdict or NOT RUN rows differ")
    if [item for row in rows for item in row["not_run"]] != result["not_run"]:
        raise ValueError("sharded NOT RUN ledger differs from the unsharded run")
    return result


def main() -> int:
    """Run one leg, or verify a union, optionally against an unsharded reference."""
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="operation", required=True)
    execute = sub.add_parser("run")
    execute.add_argument("leg", choices=[*map(str, range(LEGS)), "all"])
    execute.add_argument("--receipt", required=True, type=Path)
    execute.add_argument("command", nargs=argparse.REMAINDER)
    check = sub.add_parser("union")
    check.add_argument("--head", required=True)
    check.add_argument("--tree", required=True)
    check.add_argument("--reference", type=Path)
    check.add_argument("--output", type=Path)
    check.add_argument("receipts", nargs="+", type=Path)
    args = parser.parse_args()
    try:
        if args.operation == "run":
            command = args.command[1:] if args.command[:1] == ["--"] else args.command
            return run(None if args.leg == "all" else int(args.leg), args.receipt, command)
        receipts = [json.loads(path.read_text()) for path in args.receipts]
        if args.reference:
            result = compare(json.loads(args.reference.read_text()), receipts, args.head, args.tree)
        else:
            result = union(receipts, args.head, args.tree)
        if args.output:
            args.output.write_bytes(canonical(result) + b"\n")
        print(f"builder: {len(result['inventory'])} gates exactly once; requirements judged on the union"
              + ("; equal to the unsharded run" if args.reference else ""))
    except (OSError, ValueError, KeyError, TypeError, subprocess.CalledProcessError) as exc:
        print(f"builder legs refused: {exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
