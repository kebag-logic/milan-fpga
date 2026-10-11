#!/usr/bin/env python3
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""Prove sharded dispatch preserves the live default suite and mutant inventory."""

from __future__ import annotations

import argparse
from collections import Counter
from collections.abc import Callable
from contextlib import ExitStack, redirect_stderr, redirect_stdout
from io import StringIO
import json
from pathlib import Path
from types import ModuleType, SimpleNamespace
from unittest.mock import patch

import test_ctrl_firmware as driver
from ctrl_build import Outcome, Tree


def argument(value: object) -> object:
    """Stable call identity without temporary checkout paths."""
    if isinstance(value, Tree):
        return "firmware tree"
    if isinstance(value, Path):
        return value.name
    return value


def inventory(module: ModuleType, shard: tuple[int, int] | None = None,
              extra_suite: bool = False) -> list[str]:
    """Discover dispatch through the real driver, intercepting expensive entry points.

    Composite arm builders still enumerate their live shapes and suites.
    Campaign entries come from their current tables, including interface variants.
    This checks scheduling; the unchanged real arms judge firmware behavior.
    """
    calls = []
    args = SimpleNamespace(shard=shard, self_test=True, jobs=4, slice=(1, 1),
                           mutation_shard=None, require_rv32=True,
                           lwsrp=module.CTRL.parents[2] / "third_party/lwSRP")
    tree = Tree(module.CTRL, Path("dispatch-build"), Path("dispatch-reuse"),
                module.fw_gtest.Build(jobs=4))

    def arm(name: str) -> Callable[..., Outcome]:
        """Record the live entry point and every argument that selects its suite."""
        def record(*positional: object, **keywords: object) -> Outcome:
            """Return a passing stand-in without compiling or running firmware."""
            call = [name, [argument(v) for v in positional],
                    {k: argument(v) for k, v in keywords.items()}]
            calls.append("suite:" + json.dumps(call, sort_keys=True))
            return Outcome(name, 0, "")
        return record

    def control_campaign(root: Path, reuse: Path, jobs: int, part: tuple[int, int] = (1, 1),
                         shard: tuple[int, int] | None = None) -> bool:
        """Read the same complete or legacy-partitioned control table."""
        table = (module.ctrl_mutants.sliced(part) if shard is None
                 else module.ctrl_mutants.MUTANTS[shard[0]::shard[1]])
        calls.append("control:unnamed-tests")
        calls.extend("control:" + mutant.name for mutant in table)
        return False

    def aecp_campaign(root: Path, jobs: int = 4, shard: tuple[int, int] = (0, 1)) -> bool:
        """Keep the campaign's controls and each live AECP defect visible."""
        calls.append("aecp:controls")
        calls.extend("aecp:" + defect.name for defect in module.aecp_mutants.DEFECTS[shard[0]::shard[1]])
        return False

    def srp_campaign(root: Path, lwsrp: Path, jobs: int = 4, interfaces: int = 2) -> bool:
        """Distinguish both interface variants of the live SRP table."""
        calls.extend(f"srp-if{interfaces}:" + defect.name for defect in module.srp_mutants.DEFECTS)
        return False

    def pin_controls(root: Path, lwsrp: Path) -> int:
        """Retain the unchanged pin-control invocation."""
        calls.append("lwsrp:pin-controls")
        return 0

    with ExitStack() as context, redirect_stdout(StringIO()):
        if extra_suite:
            original = module.run_suites

            def with_future_suite(*args: object) -> list[Outcome]:
                """A new suite needs no entry in an ownership list."""
                results = original(*args)
                results.append(arm("future-suite")())
                return results

            context.enter_context(patch.object(module, "run_suites", with_future_suite))
        for owner in (module.ctrl_arms, module.srp_arms, module.aecp_arms):
            for name, value in vars(owner).copy().items():
                if callable(value) and (name.startswith("arm_") or name in ("core_arm", "image_arm")):
                    context.enter_context(patch.object(owner, name, arm(owner.__name__ + "." + name)))
        context.enter_context(patch.object(module.ctrl_arms, "report", return_value=False))
        context.enter_context(patch.object(module.ctrl_mutants, "campaign", control_campaign))
        context.enter_context(patch.object(module.aecp_mutants, "campaign", aecp_campaign))
        context.enter_context(patch.object(module.srp_mutants, "campaign", srp_campaign))
        context.enter_context(patch.object(module.ctrl_mutants, "lwsrp_pin_arms", pin_controls))
        assert not module.run_selected(args, tree, Path("dispatch-build"))
    return calls


def differences(expected: list[str], shards: list[list[str]]) -> dict[str, list[str]]:
    """Each live default invocation must occur exactly once across the shards."""
    want = Counter(expected)
    have = Counter(call for shard in shards for call in shard)
    return {"missing": sorted((want - have).elements()),
            "duplicate_or_unexpected": sorted((have - want).elements())}


def refusal_cases(module: ModuleType) -> None:
    """Invalid or narrowing shard combinations must refuse before any build."""
    flags = (["--shard", value, "--self-test"] for value in ("0/0", "0/3", "4/4", "-1/4", "x/4"))
    incompatible = (["--shard", "0/4"],
                    ["--shard", "0/4", "--self-test", "--coverage", "unused"],
                    ["--shard", "0/4", "--self-test", "--slice", "1/2"],
                    ["--shard", "0/4", "--self-test", "--mutation-shard", "0", "2"])
    for argv in (*flags, *incompatible):
        with redirect_stderr(StringIO()):
            try:
                module.main(argv)
            except SystemExit as exc:
                assert exc.code == 2, (argv, exc.code)
            else:
                raise AssertionError(f"accepted invalid shard arguments: {argv}")
    args = SimpleNamespace(shard=None, self_test=True)
    with patch.object(module, "run_suites", return_value=[]), \
            patch.object(module.ctrl_arms, "report", return_value=True), \
            patch.object(module.ctrl_mutants, "campaign") as campaign:
        assert module.run_selected(args, None, Path("unused"))
        campaign.assert_not_called()
    print("PASS: nine invalid shard combinations refuse; failed normal suites still stop mutations")


def run_cases(module: ModuleType = driver) -> list[list[str]]:
    """Compare live dispatch, then require dropped and duplicated work to fail."""
    expected = inventory(module)
    shards = [inventory(module, (index, module.SHARD_COUNT)) for index in range(module.SHARD_COUNT)]
    assert expected and not any(differences(expected, shards).values())
    assert len(expected) == len(set(expected)), "default inventory has duplicate identities"
    original = module.selected_phases
    for label, replacement in (
            ("missing suite", lambda shard: [p for p in original(shard) if p != "suites"]),
            ("duplicate suite", lambda shard: list(original(shard)) + (["suites"] if shard[0] == 1 else []))):
        with patch.object(module, "selected_phases", replacement):
            bad = [inventory(module, (index, module.SHARD_COUNT)) for index in range(module.SHARD_COUNT)]
        assert any(differences(expected, bad).values()), f"escaped planted {label}"
        print(f"PASS: shard inventory rejects planted {label}")
    future = inventory(module, extra_suite=True)
    future_shards = [inventory(module, (index, module.SHARD_COUNT), extra_suite=True)
                     for index in range(module.SHARD_COUNT)]
    assert len(future) == len(expected) + 1
    assert not any(differences(future, future_shards).values())
    print("PASS: a newly discovered suite is assigned without an ownership list")
    print(f"PASS: {len(expected)} live invocations in exactly one shard; "
          f"shard sizes {[len(shard) for shard in shards]}")
    refusal_cases(module)
    return shards


def main() -> int:
    """Standalone proof and optional generated ownership census."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--census", type=Path)
    args = parser.parse_args()
    shards = run_cases()
    if args.census:
        args.census.write_text(json.dumps(shards, indent=2) + "\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
