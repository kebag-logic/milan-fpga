# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
#
#! THE entry point. `harness/run.sh` is a thin wrapper around this.
#!
#! Unattended means unattended: nothing here reads stdin, nothing prompts, and
#! with no arguments at all the runner picks up the last run's cursor and
#! continues where it stopped.

from __future__ import annotations

import argparse
import os
import secrets
import sys
from pathlib import Path

from . import log as logmod
from . import registry as regmod
from .config import ConfigError, load
from .runner import PHASES, Runner


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        prog="milanharness",
        description="Milan validation + torture harness (unattended).")
    p.add_argument("--config", default="", help="bench config TOML")
    p.add_argument("--run-id", default="",
                   help="resume/append to this run id (default: continue the "
                        "newest run, or start a new one)")
    p.add_argument("--new", action="store_true",
                   help="force a NEW run id instead of continuing the newest")
    p.add_argument("--from", dest="from_phase", default="", metavar="PHASE",
                   choices=("",) + PHASES, help="start at this phase")
    p.add_argument("--only", default="", metavar="ITEM",
                   help="run only this item id / step name")
    p.add_argument("--phases", default="", metavar="A,B",
                   help="comma-separated subset of phases, in order")
    p.add_argument("--seed", type=int, default=0,
                   help="matrix RNG seed (0 = draw one and record it)")
    p.add_argument("--dry-run", action="store_true",
                   help="run every phase against the mock bench - no board is "
                        "touched")
    p.add_argument("--dry-run-fault", default="", metavar="KIND[:VALUE]",
                   help="inject a fault into the mock: item:<id>, outage:<n>, "
                        "known_good:<check>")
    p.add_argument("--report-only", default="", metavar="RUN_ID",
                   help="regenerate the report from an existing run and exit")
    p.add_argument("--check-registry", action="store_true",
                   help="load and validate the item registry, then exit")
    p.add_argument("--list-phases", action="store_true")
    return p


def main(argv=None) -> int:
    args = build_parser().parse_args(argv)

    if args.list_phases:
        print("\n".join(PHASES))
        return 0

    try:
        cfg = load(args.config or None, allow_placeholders=args.dry_run)
    except ConfigError as exc:
        print(f"config error: {exc}", file=sys.stderr)
        return 2

    if args.check_registry:
        try:
            reg = regmod.load(cfg.items_path, cfg.items_overlay or None)
        except regmod.RegistryMissing as exc:
            print(f"registry unavailable (BLOCKED, not an error): {exc}")
            return 0
        except regmod.RegistryError as exc:
            print(f"registry unusable: {exc}", file=sys.stderr)
            return 1
        t = reg.tally()
        print(f"registry OK: {t['total']} rows "
              f"({t['implemented']} implemented, {t['not_implemented']} "
              f"not-implemented) from {reg.source}")
        for g, n in sorted(t["by_group"].items(),
                           key=lambda kv: int(kv[0].split("-")[1])):
            print(f"  {g}: {n}")
        return 0

    root = cfg.run_root
    root.mkdir(parents=True, exist_ok=True)

    if args.report_only:
        from .report import report_only
        print(report_only(root, args.report_only))
        return 0

    rid = args.run_id or ("" if args.new else (logmod.latest_run(root) or ""))
    if not rid:
        rid = logmod.run_id(root=root)
    limits = logmod.Limits(
        human_log_max_bytes=int(cfg.get("run", "human_log_max_bytes", 8 << 20)),
        human_log_keep=int(cfg.get("run", "human_log_keep", 40)),
        max_item_output_bytes=int(cfg.get("run", "max_item_output_bytes", 256 << 10)),
        min_free_disk_mb=int(cfg.get("run", "min_free_disk_mb", 512)),
    )
    run = logmod.RunDir(root, rid, limits)

    seed = args.seed or int(cfg.get("matrix", "seed", 0) or 0)
    if not seed:
        seed = secrets.randbelow(2 ** 31)

    transport_runner = None
    if args.dry_run:
        from .mock import MockBench
        faults = _parse_fault(args.dry_run_fault)
        board0 = cfg.boards[0]
        transport_runner = MockBench(version=board0.version_expect, faults=faults)

    phases = PHASES
    if args.phases:
        want = tuple(p.strip() for p in args.phases.split(",") if p.strip())
        bad = [p for p in want if p not in PHASES]
        if bad:
            print(f"--phases: unknown {bad}", file=sys.stderr)
            return 2
        phases = want

    runner = Runner(cfg, run_dir=run, dry_run=args.dry_run, seed=seed,
                    transport_runner=transport_runner,
                    from_phase=args.from_phase, only=args.only, phases=phases)
    rc = runner.execute()
    state, reason = run.status()
    print(f"{state} {reason}")
    print(f"run dir: {run.dir}")
    return rc


def _parse_fault(spec: str) -> dict:
    if not spec:
        return {}
    kind, _, value = spec.partition(":")
    if kind == "outage":
        return {"outage": int(value or 1)}
    if kind == "item":
        return {"item": value}
    if kind == "known_good":
        return {"known_good_fail": value or "media-plane"}
    raise SystemExit(f"--dry-run-fault: unknown kind {kind!r}")


if __name__ == "__main__":
    sys.exit(main())
