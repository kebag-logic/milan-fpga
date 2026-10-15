#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""Exercise generated gate scheduling and fail-closed aggregate evidence."""

import copy
import hashlib
import importlib.util
import os
from pathlib import Path
import subprocess
import shlex
import tempfile
from unittest.mock import patch

import ast

import ci_builder_legs
from ci_builder_legs import LEGS, REQUIRED, compare, partition, union
from ci_gate_receipts import Collected, StepContext, record, verify
from ci_gate_workflows import CARRIERS, ROOT, case_inventory, generate, load_template, setup, worker_id, worker_legs
from ci_runtime_workflows import cpu_budget_step
from ci_gate_workflows import BUILDER_SPLIT, builder_leg_step, gate_graph
import ci_suite_pieces
from ci_suite_workflows import check_inventory_dependencies, inventory_dependencies


def inventory_controls() -> None:
    """Every current consumer loses its preparation independently and must be refused."""
    preparation = inventory_dependencies()["run"].strip()
    for name in ("docs", "elaborate", "rtl", "rtl-fast"):
        generated = generate(name, load_template(ROOT, name))
        check_inventory_dependencies(generated)
        for job_id, job in generated["jobs"].items():
            if not any(step.get("run", "").strip() == preparation for step in job["steps"]):
                continue
            changed = copy.deepcopy(generated)
            changed["jobs"][job_id]["steps"] = [step for step in job["steps"]
                                                  if step.get("run", "").strip() != preparation]
            refuse_preparation(changed, job_id, name + ": missing inventory preparation in ")
            # A preparation that may not run, or may fail unseen, prepares nothing.
            for planted in ({"if": "${{ false }}"}, {"continue-on-error": True}):
                changed = copy.deepcopy(generated)
                changed["jobs"][job_id]["steps"] = [
                    {**step, **planted} if step.get("run", "").strip() == preparation else step
                    for step in job["steps"]]
                refuse_preparation(changed, job_id, name + ": " + next(iter(planted)) + " preparation in ")


def refuse_preparation(changed: dict, job_id: str, label: str) -> None:
    """The generator's own construction check must name the unprepared reader."""
    try:
        check_inventory_dependencies(changed)
    except ValueError as exc:
        assert job_id in str(exc)
        print("refused " + label + job_id)
    else:
        raise AssertionError("accepted unprepared inventory reader: " + label + job_id)


def scheduling_controls() -> None:
    """Contract gates have their own worker; synthesis workers consume the shared tool."""
    docs = load_template(ROOT, "docs")
    cases = case_inventory("docs", docs)
    assert {case["name"] for case in cases if case["leg"] == 2} == {
        "CI event and SHA contract gate", "Local act runner contract gate"}
    assert worker_legs("docs", docs) == [0, 1, 2]
    source = load_template(ROOT, "rtl")
    generated = gate_graph("rtl", source)["jobs"]
    tool = generated["yosys-tool"]
    worker = generated["yosys-shards"]
    assert tool["needs"] == "full-ci-gate" and tool["if"] == worker["if"]
    assert worker["needs"] == ["full-ci-gate", "yosys-tool"]
    for name in ("Cache the pinned Yosys build", "Build Yosys from source on cache miss"):
        original = next(step for step in source["jobs"]["yosys-shards"]["steps"] if step.get("name") == name)
        moved = next(step for step in tool["steps"] if step.get("name") == name)
        assert {key: value for key, value in moved.items() if key != "id" or "id" in original} == original
        assert not any(step.get("name") == name for step in worker["steps"])
    upload = next(step for step in tool["steps"] if step.get("name") == "Upload the pinned Yosys build")
    download = next(step for step in worker["steps"] if step.get("name") == "Download the pinned Yosys build")
    assert upload["with"]["name"] == download["with"]["name"] == "pinned-yosys-${{ github.sha }}"
    print("Scheduling: separate contract worker and dependency-bound Yosys build PASS")


def child_budget(directory: Path, target: str, budget: int, makefile: Path | None = None) -> None:
    """Read the actual child recipe, including its expanded compiler arguments."""
    command = ["make", "--no-print-directory", "-n", "-B", "-C", str(directory)]
    if makefile is not None:
        command += ["-f", str(makefile)]
    result = subprocess.run([*command, target, "VERILATOR=ci-budget-compiler", "MAKEFLAGS="], check=True,
                            capture_output=True, text=True,
                            env={**os.environ, "VERILATOR_JOBS": str(budget), "MAKEFLAGS": ""})
    recipes = [shlex.split(line) for line in result.stdout.replace("\\\n", " ").splitlines()
               if line.startswith("ci-budget-compiler ")]
    assert recipes, (directory, target, result.stdout)
    for recipe in recipes:
        assert recipe[recipe.index("-j") + 1] == str(budget), (directory, target, recipe)


def child_controls(work: Path) -> None:
    """Every capture child consumes its budget; a literal unlimited child is refused."""
    spec = importlib.util.spec_from_file_location("capture_budget", ROOT / "tb/verilator/capture_coherence/mutants.py")
    driver = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(driver)
    recipes = {(row[0], row[1]) for row in driver.LEGS.values()}
    recipes.add((driver.HERE, "dp-build"))
    for width in (4, 12, 16):
        for directory, target in sorted(recipes):
            child_budget(directory, target, width // 4)
        print(f"Capture child recipes: {width} CPUs, {len(recipes)} recipes consume {width // 4} each")
    makefile = work / "unbounded.mk"
    text = (driver.MEDIA_NCO / "Makefile").read_text()
    assert "-j $(VERILATOR_JOBS)" in text
    makefile.write_text(text.replace("-j $(VERILATOR_JOBS)", "-j 0"))
    try:
        child_budget(driver.MEDIA_NCO, "build", 4, makefile)
    except AssertionError:
        print("Capture child control: unlimited compiler budget refused")
    else:
        raise AssertionError("budget-ignoring child accepted")


def cpu_controls() -> None:
    """Execute the emitted shell at hosted, fallback and normal local widths."""
    with tempfile.TemporaryDirectory(prefix="cpu-budgets-") as temporary:
        root = Path(temporary)
        child_controls(root)
        for cpus, campaign in ((1, 1), (4, 4), (12, 4), (16, 4)):
            (root / "nproc").write_text("#!/bin/sh\nprintf '%s\\n' " + str(cpus) + "\n")
            (root / "nproc").chmod(0o755)
            output = root / (str(cpus) + ".env")
            subprocess.run(["bash", "-c", cpu_budget_step()["run"]], check=True,
                           env={**os.environ, "PATH": str(root) + ":" + os.environ["PATH"],
                                "GITHUB_ENV": str(output)})
            assert output.read_text().splitlines() == [
                f"CI_BUILD_JOBS={cpus}", f"CI_TOOL_BUILD_JOBS={min(cpus, 8)}", f"CI_CAMPAIGN_JOBS={campaign}",
                f"VERILATOR_JOBS={cpus}", f"SIM_JOBS={campaign}",
                "MAKEFLAGS=-j1 --no-print-directory"]
            with patch.object(os, "sched_getaffinity", return_value=set(range(cpus))), \
                    patch.object(subprocess, "run", return_value=subprocess.CompletedProcess([], 0)) as ran:
                assert ci_suite_pieces.run("capture_coherence__0", root) == 0
                command = ran.call_args.args[0]
                jobs = int(command[command.index("--jobs") + 1])
                compiler = int(ran.call_args.kwargs["env"]["VERILATOR_JOBS"])
                assert jobs == campaign and jobs * compiler <= cpus
                assert compiler == cpus // campaign
            print(f"CPU budgets: {cpus} cores; {campaign} campaigns; nested builds bounded")
        (root / "nproc").write_text("#!/bin/sh\necho 0\n")
        refused = subprocess.run(["bash", "-c", cpu_budget_step()["run"]], check=False,
                                 env={**os.environ, "PATH": str(root) + ":" + os.environ["PATH"],
                                      "GITHUB_ENV": str(root / "zero.env")})
        assert refused.returncode != 0 and not (root / "zero.env").exists()
    for name in ("docs", "elaborate", "rtl", "rtl-fast"):
        workflow = generate(name, load_template(ROOT, name))
        for job in workflow["jobs"].values():
            assert sum(step.get("name") == cpu_budget_step()["name"] for step in job["steps"]) == 1


def builder_receipts(identity: tuple[str, str], names: list[str] | None = None,
                     flags: tuple[str, ...] = tuple(REQUIRED)) -> list[dict]:
    """Passing leg receipts in the shape the leg runner binds around the driver's own."""
    names = ci_builder_legs.inventory() if names is None else names
    legs = partition(names)
    return [{"schema": 1, "head": identity[0], "tree": identity[1], "leg": leg, "legs": len(legs),
             "driver": {"inventory": names, "selected": cases, "requirements": list(flags),
                        "gates": [{"gate": gate, "verdict": "pass", "not_run": []} for gate in cases],
                        "require_elaboration": 0 if "--require-elaboration" in flags else None}}
            for leg, cases in enumerate(legs)]


def builder_owner_controls() -> None:
    """The named requirement owners are exactly the driver gates that read each requirement."""
    tree = ast.parse((ROOT / ci_builder_legs.DRIVER).read_text())
    gates = {node.name: node for node in tree.body
             if isinstance(node, ast.FunctionDef) and node.name.startswith("test_")}
    litex = {name for name, node in gates.items()
             if any(isinstance(item, ast.Name) and item.id == "_litex_or_skip" for item in ast.walk(node))}
    rv32 = {name for name, node in gates.items()
            if any(isinstance(item, ast.Constant) and item.value == "--require-rv32" for item in ast.walk(node))}
    assert litex == set(REQUIRED["--require-elaboration"]), sorted(litex ^ set(REQUIRED["--require-elaboration"]))
    assert rv32 == set(REQUIRED["--require-rv32"]), sorted(rv32)
    print(f"Builder owners: {len(litex)} LiteX-consulting gates and {len(rv32)} RV32 gate named")


def builder_controls() -> None:
    """Judge the requirements on the union; each planted loss is refused by name."""
    builder_owner_controls()
    identity = ("a" * 40, "b" * 40)
    names = ci_builder_legs.inventory()
    good = builder_receipts(identity, names)
    assert union(good, *identity, names)["union"] == "pass"
    assert [len(cases) for cases in partition(names)] == [1, len(names) - 1]
    elaboration = "test_every_recipe_elaborates"
    rv32 = REQUIRED["--require-rv32"][0]

    def refused(label: str, receipts: list, expected: str, inventory: list[str] = names) -> None:
        """The union must refuse naming the planted gate or obligation."""
        try:
            union(receipts, *identity, inventory)
        except ValueError as exc:
            assert expected in str(exc), (label, str(exc))
            print("Builder union refused " + label + ": " + str(exc)[:160])
        else:
            raise AssertionError("builder union accepted " + label)

    deleted = [name for name in names if name != elaboration]
    refused("elaboration gate deleted from the inventory",
            builder_receipts(identity, deleted), elaboration + " absent", deleted)
    refused("elaboration leg lost", good[:1], elaboration)
    skipped = copy.deepcopy(good)
    skipped[1]["driver"]["gates"] = [row for row in skipped[1]["driver"]["gates"] if row["gate"] != elaboration]
    refused("elaboration gate skipped inside its leg", skipped, elaboration)
    with patch.object(ci_builder_legs, "ISOLATED", (rv32, elaboration)), \
            patch.object(ci_builder_legs, "LEGS", 3):
        moved = builder_receipts(identity, names)
        refused("elaboration gate moved to a leg that never ran", [moved[0], moved[2]], elaboration)
    vacuous = builder_receipts(identity, names, ("--require-rv32",))
    refused("elaboration gates in a leg without --require-elaboration", [good[0], vacuous[1]], elaboration)
    unjudged = builder_receipts(identity, names, ("--require-elaboration",))
    refused("RV32 gate in a leg without --require-rv32", [unjudged[0], good[1]], rv32)
    forged = copy.deepcopy(good)
    forged[0]["driver"]["gates"][0]["not_run"] = [["gate 23g", "stock VexiiRiscv", "toolchain"]]
    refused("toolchain skip under a passing leg verdict", forged, "toolchain skip")
    own = copy.deepcopy(good)
    own[1]["driver"]["require_elaboration"] = 1
    refused("leg whose own elaboration verdict failed", own, "did not pass")
    for label, edit, expected in (
            ("failed gate verdict",
             lambda value: value[1]["driver"]["gates"][0].update(verdict="fail"), "did not pass"),
            ("changed selection", lambda value: value[0]["driver"]["selected"].append(names[0]), "selection"),
            ("duplicated leg", lambda value: value.append(copy.deepcopy(value[0])), "duplicated"),
            ("changed head", lambda value: value[0].update(head="c" * 40), "source identity"),
            ("changed driver inventory", lambda value: value[1]["driver"]["inventory"].pop(), "inventory"),
            ("unknown requirement", lambda value: value[0]["driver"]["requirements"].append("--x"), "flags")):
        changed = copy.deepcopy(good)
        edit(changed)
        refused(label, changed, expected)
    try:
        partition([name for name in names if name != rv32])
    except ValueError as exc:
        assert rv32 in str(exc)
        print("Builder partition refused a measured gate absent from the inventory")
    else:
        raise AssertionError("partition accepted a lost measured gate")
    reference = {"schema": 1, "head": identity[0], "tree": identity[1], "leg": None, "legs": LEGS,
                 "driver": {"inventory": names, "selected": names, "requirements": list(REQUIRED),
                            "gates": [row for receipt in good for row in receipt["driver"]["gates"]],
                            "require_elaboration": 0}}
    reference["driver"]["gates"].sort(key=lambda row: names.index(row["gate"]))
    compare(reference, good, *identity, names)
    differs = copy.deepcopy(reference)
    differs["driver"]["gates"][-1]["not_run"] = [["gate 11", "no report", "row"]]
    try:
        compare(differs, good, *identity, names)
    except ValueError as exc:
        assert names[-1] in str(exc)
        print("Builder comparison refused a NOT RUN row the legs lack")
    else:
        raise AssertionError("comparison accepted an unequal NOT RUN ledger")
    print("Builder legs: union-level requirements and per-gate equality PASS")


def main() -> int:
    """Drive the production generator and verifier with independent planted losses."""
    inventory_controls()
    scheduling_controls()
    cpu_controls()
    for name, carrier in CARRIERS.items():
        source = load_template(ROOT, name)
        generated = generate(name, source)
        cases = case_inventory(name, source)
        legs = worker_legs(name, source)
        identity = ("a" * 40, "b" * 40)
        digest = hashlib.sha256(name.encode()).hexdigest()
        scope = "true" if name == "elaborate" else ""
        actual = {case["id"]: {"outcome": "success", "conclusion": "success"} for case in cases}
        receipts = [record(name, leg, source, identity, digest, StepContext(actual, scope)) for leg in legs]
        needs = {worker_id(name, leg): {"result": "success"} for leg in legs}
        builder = builder_receipts(identity) if name in BUILDER_SPLIT else None
        assert len(verify(name, source, identity, digest, Collected(receipts, builder), needs)) == len(cases)
        assert set(generated["jobs"][carrier]["needs"]) == set(needs)
        original = source["jobs"][carrier]["steps"]
        for case in cases:
            owned = [step for step in generated["jobs"][worker_id(name, case["leg"])]["steps"]
                     if step.get("id") == case["id"]]
            assert len(owned) == 1
            body = copy.deepcopy(owned[0])
            del body["id"]
            if "builder" in case:
                # The leg runs the template's own command, only adding its selection.
                assert body == builder_leg_step(original[case["index"]], case)
                assert body["run"].endswith(" -- " + original[case["index"]]["run"].strip() + "\n")
                assert {key: value for key, value in body.items() if key not in ("name", "run")} == {
                    key: value for key, value in original[case["index"]].items() if key not in ("name", "run")}
            else:
                assert body == original[case["index"]]
        for leg in legs:
            steps = generated["jobs"][worker_id(name, leg)]["steps"]
            index = {case["id"]: case["index"] for case in cases}
            source_order = [index[step["id"]] for step in steps if step.get("id") in index]
            assert source_order == sorted(source_order)
            assert len(source_order) == sum(case["leg"] == leg for case in cases)
        def refuse(label: str, records: list, jobs: dict, legs_builder: list | None = builder) -> None:
            """Every damaged collection must reach the production refusal path."""
            try:
                verify(name, source, identity, digest, Collected(records, legs_builder), jobs)
            except (ValueError, KeyError, TypeError):
                print(name + ": refused " + label)
            else:
                raise AssertionError(name + ": accepted " + label)
        for status in ("failure", "cancelled", "skipped", None):
            changed = copy.deepcopy(needs)
            changed[worker_id(name, 0)]["result"] = status
            refuse("dependent job " + str(status), receipts, changed)
        missing = copy.deepcopy(needs)
        missing.pop(worker_id(name, 0))
        refuse("missing dependent job", receipts, missing)
        refuse("missing receipt", receipts[:1], needs)
        refuse("duplicated leg", [receipts[0], receipts[0]], needs)
        for field in ("head", "tree", "template_sha256", "inventory"):
            changed = copy.deepcopy(receipts)
            changed[0][field] = [] if field == "inventory" else "c" * len(changed[0][field])
            refuse("changed " + field, changed, needs)
        for status in ("failure", "cancelled", "skipped", None):
            changed = copy.deepcopy(receipts)
            changed[0]["results"][0]["outcome"] = status
            changed[0]["results"][0]["conclusion"] = status
            refuse("gate outcome " + str(status), changed, needs)
        dropped = cases[-1]["id"]
        changed = copy.deepcopy(receipts)
        for receipt in changed:
            receipt["inventory"].remove(dropped)
            receipt["results"] = [row for row in receipt["results"] if row["case"] != dropped]
        refuse("gate dropped from every leg and claimed inventory", changed, needs)
        if name == "elaborate":
            mixed = copy.deepcopy(receipts)
            mixed[1]["scope"] = "false"
            for row in mixed[1]["results"]:
                row.update(outcome="skipped", conclusion="skipped")
            refuse("individually valid mixed execution scopes", mixed, needs)
            refuse("executed builder division without builder receipts", receipts, needs, None)
            refuse("executed builder division missing a leg receipt", receipts, needs, builder[:1])
            skipped = {case["id"]: {"outcome": "skipped", "conclusion": "skipped"} for case in cases}
            receipts = [record(name, leg, source, identity, digest, StepContext(skipped, "false")) for leg in legs]
            assert len(verify(name, source, identity, digest, Collected(receipts), needs)) == len(cases)
            refuse("builder receipts from a skipped builder division", receipts, needs, builder)
            receipts[0]["scope"] = "true"
            refuse("contradictory skip scope", receipts, needs, None)
        assert len({case["index"] for case in cases}) == sum(not setup(step) for step in original)
        assert sum("builder" in case for case in cases) == (LEGS if name in BUILDER_SPLIT else 0)
        print(f"{name}: {len(cases)} source gates retain their complete original steps")
    builder_controls()
    print("gate workflow and union controls: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
