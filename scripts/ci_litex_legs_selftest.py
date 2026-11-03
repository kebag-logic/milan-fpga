#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""The standalone LiteX simulations in measured legs (#737): a partition that refuses an unmeasured
member, a stale measurement and an over-budget leg; a union that refuses a dropped, duplicated,
failed, skipped or moved simulation by name; and generated legs that run the template's own step.

ci_gate_workflows_selftest.py runs these controls in the hosted "CI scheduling and evidence controls" step.
"""

import copy
import shlex
from collections.abc import Callable
from unittest.mock import patch

import ci_litex_legs
from ci_litex_legs import LARGEST, LEG_BUDGET, LEGS, SECONDS, partition, union
import ci_builder_legs
from ci_gate_workflows import (BUILDER_CACHES, BUILDER_WORKERS, CARRIERS, LITEX_COMMAND, LITEX_SPLIT, LITEX_WORKERS,
                               METADATA_STEPS, ROOT, VERILATOR_SETUP, builder_caches, gate_graph, generate,
                               litex_leg_step, load_template, metadata_worker, worker_id)


#: The builders' shared caches, the CPU metadata steps and the worker that carries them, named here rather than
#: read from the generator's constants, so that a step dropped from those constants is caught (#737).
SHARED_CACHES = {"elaborate": ("Cache verified sv2v archive", "Cache the pinned pip downloads",
                               "Cache the Scala toolchain")}
METADATA = {"elaborate": ("Cache the generated CPU metadata",
                          "Keep the generated CPU netlist arguments for the next run")}
METADATA_WORKER = {"elaborate": 1}


def litex_receipts(identity: tuple[str, str], names: list[str] | None = None) -> list[dict]:
    """Passing leg receipts in the shape the leg runner binds around the runner's verdict rows."""
    names = ci_litex_legs.inventory() if names is None else names
    legs = partition(names)
    return [{"schema": 1, "head": identity[0], "tree": identity[1], "leg": leg, "legs": len(legs),
             "inventory": list(names), "selected": members, "exit": 0,
             "results": [{"simulation": name, "verdict": "PASS", "seconds": SECONDS[name]} for name in members]}
            for leg, members in enumerate(legs)]


def refused(call: Callable[[], object], label: str, expected: str) -> None:
    """The production check must refuse, naming the planted member or obligation."""
    try:
        call()
    except ValueError as exc:
        assert expected in str(exc), (label, str(exc))
        print("LiteX legs refused " + label + ": " + str(exc)[:160])
    else:
        raise AssertionError("LiteX legs accepted " + label)


def partition_controls(names: list[str]) -> None:
    """Every member in exactly one leg; a gap in the measurements or an over-full leg is refused."""
    legs = partition(names)
    assert len(legs) == LEGS and sorted(name for leg in legs for name in leg) == sorted(names), legs
    assert all(leg == [name for name in names if name in leg] for leg in legs), legs
    assert set(SECONDS) == set(LARGEST) == set(names), sorted((set(SECONDS) | set(LARGEST)) ^ set(names))
    # The largest figures include the run the legs were derived from, so none is below its partition figure.
    assert all(LARGEST[name] >= SECONDS[name] for name in names), (SECONDS, LARGEST)
    assert max(sum(LARGEST[name] for name in leg) for leg in legs) <= LEG_BUDGET
    refused(lambda: partition([*names, "test_new_member"]), "an inventory member with no measured seconds",
            "no measured seconds for test_new_member")
    refused(lambda: partition(names, largest={name: LARGEST[name] for name in names[1:]}),
            "a member with no largest seconds", "no measured seconds for " + names[0])
    refused(lambda: partition(names[1:]), "a measured member gone from the inventory", names[0])
    heavy = {**SECONDS, names[0]: LEG_BUDGET + 1}
    refused(lambda: partition(names, heavy, largest=heavy), "a leg over its measured budget", "add a leg")
    # The legs stay as derived, but a later, larger measurement that overfills one is refused (#737).
    grown = {**LARGEST, names[0]: LEG_BUDGET + 1}
    refused(lambda: partition(names, largest=grown), "a leg over its budget at its largest seconds",
            "at its largest")
    print(f"LiteX partition: {len(names)} members in {LEGS} legs of "
          + ", ".join(str(sum(SECONDS[name] for name in leg)) for leg in legs) + " measured seconds, at their largest "
          + ", ".join(str(sum(LARGEST[name] for name in leg)) for leg in legs))


def union_controls() -> None:
    """Each planted loss of a simulation, a verdict or a leg is refused by name."""
    identity = ("a" * 40, "b" * 40)
    names = ci_litex_legs.inventory()
    partition_controls(names)
    good = litex_receipts(identity, names)
    assert union(good, *identity, names)["union"] == "pass"
    first, last = good[0]["selected"][0], good[1]["selected"][-1]

    def plant(edit: Callable[[list], object]) -> list:
        """A copy of the passing receipts with one planted change."""
        changed = copy.deepcopy(good)
        edit(changed)
        return changed

    for label, edit, expected in (
            ("a simulation dropped from its leg", lambda value: value[0]["results"].pop(0),
             "did not run its selection exactly once: " + first),
            ("a simulation dropped from its leg's selection and results",
             lambda value: (value[0]["selected"].pop(0), value[0]["results"].pop(0)), "selection differs"),
            ("a simulation run in a second leg",
             lambda value: value[0]["results"].append(copy.deepcopy(value[1]["results"][-1])),
             "order or extra simulations"),
            ("a simulation outside the inventory",
             lambda value: value[1]["results"].append({"simulation": "test_rogue", "verdict": "PASS", "seconds": 1}),
             "test_rogue"),
            ("a failed simulation", lambda value: value[1]["results"][-1].update(verdict="FAIL"), last + ": FAIL"),
            ("a skipped simulation", lambda value: value[1]["results"][-1].update(verdict="SKIP"), last + ": SKIP"),
            ("a timed-out simulation", lambda value: value[1]["results"][-1].update(verdict="TIMEOUT"), "TIMEOUT"),
            ("a red runner exit", lambda value: value[0].update(exit=1), "exited 1"),
            ("a boolean runner exit", lambda value: value[0].update(exit=False), "exited False"),
            ("a lost leg", lambda value: value.pop(), "ran in no leg: " + ", ".join(good[-1]["selected"])),
            ("a duplicated leg", lambda value: value.append(copy.deepcopy(value[0])), "duplicated"),
            ("a changed head", lambda value: value[0].update(head="c" * 40), "source identity"),
            ("a changed inventory", lambda value: value[1]["inventory"].pop(), "inventory differs"),
            ("a changed schema", lambda value: value[0].pop("exit"), "schema")):
        refused(lambda changed=plant(edit): union(changed, *identity, names), label, expected)
    print("LiteX union: every simulation exactly once, each a pass PASS")


def split_controls() -> None:
    """A divided simulation step must end in its one aggregate command and run no simulation elsewhere."""
    for name in LITEX_SPLIT:
        source = load_template(ROOT, name)
        step, = (step for step in source["jobs"][CARRIERS[name]]["steps"] if step.get("name") == LITEX_SPLIT[name])
        *preparation, command = step["run"].strip().split("\n")
        assert preparation == [LITEX_COMMAND + " --selftest"], preparation
        for label, run in (
                ("aggregate in a preparation line", "\n".join([*preparation, command, command]) + "\n"),
                ("last line not the aggregate", "\n".join([*preparation, "true"]) + "\n"),
                ("aggregate with a selection of its own", "\n".join([*preparation, command + " --only x"]) + "\n")):
            changed = copy.deepcopy(source)
            planted, = (item for item in changed["jobs"][CARRIERS[name]]["steps"]
                        if item.get("name") == LITEX_SPLIT[name])
            planted["run"] = run
            refused(lambda changed=changed: generate(name, changed), "the " + name + " template with its " + label,
                    "one aggregate command")


def step_controls(name: str, case: dict, generated: dict, original: dict) -> None:
    """A LiteX leg is its worker's original step, only adding the leg runner around its aggregate command."""
    owned = [step for step in generated["jobs"][worker_id(name, case["leg"])]["steps"] if step.get("id") == case["id"]]
    assert len(owned) == 1
    body = copy.deepcopy(owned[0])
    del body["id"]
    assert body == litex_leg_step(original, case)
    assert case["leg"] == LITEX_WORKERS[name][case["litex"]]
    *preparation, command = original["run"].strip().split("\n")
    *kept, line = body["run"].strip().split("\n")
    assert kept == preparation and line.endswith(" -- " + command), body["run"]
    words = shlex.split(line)
    assert words[:2] == ["python3", "scripts/ci_litex_legs.py"], words
    parsed, runner = ci_litex_legs.parse(words[2:])
    assert (parsed.operation, parsed.leg, runner) == ("run", str(case["litex"]), shlex.split(command)), words
    assert parsed.receipt.name == "litex-leg-" + str(case["litex"]) + ".json"
    assert {key: value for key, value in body.items() if key not in ("name", "run")} == {
        key: value for key, value in original.items() if key not in ("name", "run")}


def worker_controls(name: str, generated: dict, cases: list[dict], legs: list[int]) -> None:
    """Exactly the workers that run a LiteX leg set up Verilator and retain the leg's receipt."""
    owners = {case["leg"] for case in cases if "litex" in case}
    assert owners == set(LITEX_WORKERS.get(name, ())), (name, owners)
    for leg in legs:
        steps = generated["jobs"][worker_id(name, leg)]["steps"]
        upload, = (step for step in steps if step.get("name") == "Upload executed gate outcomes")
        assert ("litex-leg-*.json" in upload["with"]["path"]) == (leg in owners), (name, leg, upload["with"]["path"])
        if name in LITEX_WORKERS:
            # LEG_BUDGET is derived from the LiteX worker's own limit, so a changed limit is caught here (#737).
            if leg in owners:
                minutes = generated["jobs"][worker_id(name, leg)]["timeout-minutes"]
                assert minutes * 60 == ci_litex_legs.JOB_LIMIT, (name, leg, minutes)
            setup = {step.get("name") for step in steps} & VERILATOR_SETUP
            assert setup == (VERILATOR_SETUP if leg in owners else set()), (name, leg, setup)
            # Only the builders restore and save their shared caches; a LiteX worker carries none, and only the
            # builder that generates the CPU metadata carries its cache and the step that fills it (#737).
            assert (set(BUILDER_CACHES[name]), METADATA_STEPS[name], metadata_worker(name)) == (
                {*SHARED_CACHES[name], METADATA[name][0]}, METADATA[name], METADATA_WORKER[name]), name
            names = [step.get("name") for step in steps]
            common = sorted(SHARED_CACHES[name])
            shared = sorted(found for found in names if found in common)
            assert shared == ([] if leg in owners else common), (name, leg, shared)
            metadata = sorted(found for found in names if found in METADATA[name])
            assert metadata == (sorted(METADATA[name]) if leg == METADATA_WORKER[name] else []), (name, leg, metadata)
    if name in BUILDER_CACHES:
        cache_controls(name)
    aggregate_controls(name, generated)
    if name in LITEX_WORKERS:
        shared = (*LITEX_WORKERS[name][:-1], BUILDER_WORKERS[name][-1])
        with patch.dict(LITEX_WORKERS, {name: shared}):
            refused(lambda: generate(name, load_template(ROOT, name)), "a LiteX leg on a builder worker",
                    "a LiteX leg shares a worker with a builder leg")


def aggregate_controls(name: str, generated: dict) -> None:
    """The elaborate aggregate fetches the head alone, under its 3-minute limit; the docs one keeps its history."""
    job = generated["jobs"][CARRIERS[name]]
    checkout = job["steps"][0]
    assert job["timeout-minutes"] == 3, (name, job["timeout-minutes"])
    assert checkout["uses"] == "actions/checkout@v4", (name, checkout)
    # Its full-history fetch reached the limit in run 41678609075 (#737).
    expected = None if name == "elaborate" else {"fetch-depth": 0}
    assert checkout.get("with") == expected, (name, checkout)


def cache_controls(name: str) -> None:
    """A worker that lost a shared cache or CPU metadata step, or repeats one, is refused by name; so are
    elaboration gates split across builder legs, which leave no one worker generating the metadata."""
    from ci_install_workflows import generate as install_workflows
    source = install_workflows(gate_graph(name, load_template(ROOT, name)))
    generator = metadata_worker(name)
    for leg, step_name, label, expected in (
            (BUILDER_WORKERS[name][0], BUILDER_CACHES[name][-1], "a builder without its CPU metadata cache",
             "the builders' shared cache"),
            (LITEX_WORKERS[name][0], BUILDER_CACHES[name][-1], "a LiteX worker repeating the CPU metadata cache",
             "the builders' shared cache"),
            (generator, METADATA_STEPS[name][-1], "the generating builder without the step that fills its cache",
             "the CPU metadata steps"),
            (LITEX_WORKERS[name][-1], METADATA_STEPS[name][-1], "a LiteX worker repeating that step",
             "the CPU metadata steps")):
        planted = copy.deepcopy(source)
        steps = planted["jobs"][worker_id(name, leg)]["steps"]
        at = next(index for index, step in enumerate(steps) if step.get("name") == step_name)
        if leg in BUILDER_WORKERS[name]:
            del steps[at]
        else:
            steps.insert(at, copy.deepcopy(steps[at]))
        refused(lambda: builder_caches(name, planted), label, worker_id(name, leg) + ": " + expected)
    split = (*ci_builder_legs.ISOLATED, ci_builder_legs.REQUIRED["--require-elaboration"][0])
    with patch.object(ci_builder_legs, "ISOLATED", split), patch.object(ci_builder_legs, "LEGS", len(split) + 1):
        refused(lambda: metadata_worker(name), "elaboration gates split across builder legs",
                "the elaboration gates span builder legs")


def verify_controls(litex: list[dict], refuse: Callable[[str, list | None], None]) -> None:
    """The gate aggregate reaches the LiteX union: a dropped, duplicated or unreceipted simulation is refused."""
    dropped = copy.deepcopy(litex)
    dropped[0]["results"].pop(0)
    refuse("a LiteX simulation dropped from its leg", dropped)
    duplicated = copy.deepcopy(litex)
    duplicated[1]["results"].append(copy.deepcopy(duplicated[0]["results"][0]))
    refuse("a LiteX simulation run in two legs", duplicated)
    refuse("executed LiteX division without LiteX receipts", None)
    refuse("executed LiteX division missing a leg receipt", litex[:1])


def main() -> int:
    """Run the partition, union and split controls alone."""
    union_controls()
    split_controls()
    print("LiteX leg controls: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
