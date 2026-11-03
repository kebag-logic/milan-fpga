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
from ci_gate_workflows import (BUILDER_CACHES, BUILDER_WORKERS, CARRIERS, LITEX_COMMAND, LITEX_SPLIT, LITEX_WORKERS,
                               ROOT, VERILATOR_SETUP, builder_caches, gate_graph, generate, litex_leg_step,
                               load_template, worker_id)


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
            setup = {step.get("name") for step in steps} & VERILATOR_SETUP
            assert setup == (VERILATOR_SETUP if leg in owners else set()), (name, leg, setup)
            # Only the builders restore and save their shared caches; a LiteX worker carries none (#737).
            shared = [step.get("name") for step in steps if step.get("name") in BUILDER_CACHES[name]]
            assert sorted(shared) == ([] if leg in owners else sorted(BUILDER_CACHES[name])), (name, leg, shared)
    if name in BUILDER_CACHES:
        cache_controls(name)
    if name in LITEX_WORKERS:
        shared = (*LITEX_WORKERS[name][:-1], BUILDER_WORKERS[name][-1])
        with patch.dict(LITEX_WORKERS, {name: shared}):
            refused(lambda: generate(name, load_template(ROOT, name)), "a LiteX leg on a builder worker",
                    "a LiteX leg shares a worker with a builder leg")


def cache_controls(name: str) -> None:
    """A builder that lost a shared cache step, or a LiteX worker that repeats one, is refused by name."""
    from ci_install_workflows import generate as install_workflows
    source = install_workflows(gate_graph(name, load_template(ROOT, name)))
    for leg, label in ((BUILDER_WORKERS[name][0], "a builder without its CPU metadata cache"),
                       (LITEX_WORKERS[name][0], "a LiteX worker repeating the CPU metadata cache")):
        planted = copy.deepcopy(source)
        steps = planted["jobs"][worker_id(name, leg)]["steps"]
        at = next(index for index, step in enumerate(steps) if step.get("name") == BUILDER_CACHES[name][-1])
        if leg in BUILDER_WORKERS[name]:
            del steps[at]
        else:
            steps.insert(at, copy.deepcopy(steps[at]))
        refused(lambda: builder_caches(name, planted), label, worker_id(name, leg) + ": the builders' shared cache")


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
