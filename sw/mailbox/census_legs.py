#!/usr/bin/env python3
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""Execute publication census legs and judge the complete rule-removal verdict.

Issue #1008; REQ-VER-01 and REQ-VER-04. Leg zero checks every shape together,
so cross-shape comparisons stay whole. The other legs divide the self-test's
execution inventory, keeping netlist riders beside their hosts. The union
runs the original mutation judgement over every executed arm, exactly once.
"""

from __future__ import annotations

import argparse
from concurrent.futures import ProcessPoolExecutor
import json
import multiprocessing
from pathlib import Path
import sys

import publication_census as pc
import census_selftest as checks
from census_elab import REPO, WORK, toolchain

sys.path.insert(0, str(REPO / "scripts"))
from ci_case_receipts import source_identity  # noqa: E402

LEGS = 5


def inventory() -> list:
    """Discover the serial driver's actual host/rider execution groups."""
    return checks.jobs_for(pc.load(pc.DATAPATH, pc.WRAPPER_SV), pc.fields(pc.mailbox_model.load()))


def selection(every: list, leg: int) -> list:
    """Interleave complete execution groups; leg zero owns the whole shape comparison."""
    if type(leg) is not int or not 0 <= leg < LEGS:
        raise ValueError("unknown census leg")
    return [] if leg == 0 else every[leg - 1::LEGS - 1]


def names(groups: list) -> list[str]:
    """An independent identity for each arm, including the riders."""
    return [arm.what for host, _, riders in groups for arm in (host, *riders)]


def run(leg: int, receipt: Path, jobs: int) -> int:
    """Run real arms and retain their actual verdicts even when one fails."""
    every = inventory()
    selected = selection(every, leg)
    identity = source_identity(REPO)
    rows = []
    print(f"publication census: {toolchain()}", flush=True)
    if leg == 0:
        rc = pc.main(["--check", "--jobs", str(jobs)])
    else:
        WORK.roms()
        with ProcessPoolExecutor(max_workers=jobs, mp_context=multiprocessing.get_context("fork")) as pool:
            for results in pool.map(checks.run_arm, selected):
                for arm, ok, line, through in results:
                    print(line, flush=True)
                    rows.append({"arm": arm.what, "ok": ok, "line": line, "through": through})
        rc = int(any(not row["ok"] or row["through"] is False for row in rows))
    if identity != source_identity(REPO):
        raise ValueError("census source changed during execution")
    document = {"schema": 1, "head": identity[0], "tree": identity[1], "leg": leg, "legs": LEGS,
                "inventory": names(every), "selected": names(selected), "rows": rows, "exit": rc}
    receipt.parent.mkdir(parents=True, exist_ok=True)
    with receipt.open("x") as stream:
        json.dump(document, stream, sort_keys=True)
        stream.write("\n")
    return rc


def union(receipts: list[dict], every: list, identity: tuple[str, str]) -> int:
    """Validate source, inventory, selection and execution, then use the unchanged rule judge."""
    expected = names(every)
    if not expected or len(set(expected)) != len(expected):
        raise ValueError("empty or ambiguous census inventory")
    seen = set()
    executed = {}
    for record in receipts:
        if (set(record) != {"schema", "head", "tree", "leg", "legs", "inventory", "selected", "rows", "exit"}
                or type(record["schema"]) is not int or record["schema"] != 1
                or type(record["legs"]) is not int or record["legs"] != LEGS):
            raise ValueError("census receipt schema differs")
        if (record["head"], record["tree"]) != identity or record["inventory"] != expected:
            raise ValueError("census receipt source or inventory differs")
        leg = record["leg"]
        chosen = names(selection(every, leg))
        if leg in seen or record["selected"] != chosen:
            raise ValueError("duplicate census leg or changed selection")
        seen.add(leg)
        rows = record["rows"]
        if not isinstance(rows, list) or any(
                not isinstance(row, dict) or set(row) != {"arm", "ok", "line", "through"}
                or type(row["ok"]) is not bool or not isinstance(row["line"], str)
                or (row["through"] is not None and type(row["through"]) is not bool) for row in rows):
            raise ValueError("malformed census verdict row")
        if [row["arm"] for row in rows] != chosen:
            raise ValueError("missing, duplicated or extra executed census arm")
        if type(record["exit"]) is not int or record["exit"] != 0:
            raise ValueError("census leg failed")
        executed.update((row["arm"], row) for row in rows)
    if seen != set(range(LEGS)) or set(executed) != set(expected):
        raise ValueError("incomplete census union")
    judged = [arm for host, _, riders in every for arm in (host, *riders)]
    for arm in judged:
        row = executed[arm.what]
        if not row["ok"] or (row["through"] is None) != (arm.rule is None):
            raise ValueError("failed arm or missing rule-removal judgement: " + arm.what)
        print(row["line"])
    print(f"selftest: 0 of {len(judged)} arm(s) failed; {len(judged)} arm(s) and their rules' removals "
          f"across {LEGS - 1} legs")
    return int(bool(checks.mutations(judged, [executed[arm.what]["through"] for arm in judged])))


def main() -> int:
    """The worker writes evidence; the judge refuses incomplete or failed evidence."""
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    commands = parser.add_subparsers(dest="command", required=True)
    worker = commands.add_parser("run")
    worker.add_argument("--leg", type=int, required=True)
    worker.add_argument("--receipt", type=Path, required=True)
    worker.add_argument("--jobs", type=int, default=1)
    judge = commands.add_parser("union")
    judge.add_argument("--root", type=Path, required=True)
    args = parser.parse_args()
    try:
        if args.command == "run":
            if args.jobs < 1:
                raise ValueError("jobs must be positive")
            return run(args.leg, args.receipt, args.jobs)
        records = [json.loads(path.read_text()) for path in sorted(args.root.rglob("census-leg-*.json"))]
        return union(records, inventory(), source_identity(REPO))
    except (OSError, ValueError, KeyError, TypeError, pc.CensusError) as exc:
        print(f"census legs refused: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
