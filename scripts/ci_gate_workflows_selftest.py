#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""Exercise generated gate scheduling and fail-closed aggregate evidence."""

import copy
import hashlib
import importlib.util
import os
from pathlib import Path
import re
import subprocess
import shlex
import tempfile
from unittest.mock import patch

import ast
from collections.abc import Callable

import ci_builder_legs
from ci_builder_legs import LEGS, REQUIRED, compare, partition, requirements, union
from ci_gate_receipts import Collected, StepContext, record, verify
from ci_gate_workflows import CARRIERS, ROOT, case_inventory, generate, load_template, setup, worker_id, worker_legs
from ci_runtime_workflows import CENSUS_WORKER_BYTES, census_budget_step, cpu_budget_step
from ci_gate_workflows import BUILDER_SPLIT, BUILDER_WORKERS, DRIVER_COMMAND, builder_command, builder_leg_step
from ci_gate_workflows import gate_graph
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
    leg = "End-station builder gates, leg {} of " + str(LEGS)
    assert [case["name"] for case in cases if case["leg"] == 1] == [leg.format(0)]
    assert {case["name"] for case in cases if case["leg"] == 2} == {
        leg.format(1), "CI event and SHA contract gate", "Local act runner contract gate"}
    assert worker_legs("docs", docs) == [0, 1, 2]
    assert builder_command("docs", docs)[2:] == ["--require-rv32"]
    assert builder_command("elaborate", load_template(ROOT, "elaborate"))[2:] == [
        "--require-elaboration", "--require-rv32"]
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
    print("Scheduling: docs builder legs beside the contract worker; dependency-bound Yosys build PASS")


def builder_split_controls() -> None:
    """A divided builder step must end in its one driver command and run it nowhere else."""
    for name in BUILDER_SPLIT:
        source = load_template(ROOT, name)
        step, = (step for step in source["jobs"][CARRIERS[name]]["steps"] if step.get("name") == BUILDER_SPLIT[name])
        *preparation, driver = step["run"].strip().split("\n")
        for label, run in (
                ("driver in a preparation line", "\n".join([*preparation, driver + " --list", driver]) + "\n"),
                ("last line not the driver", "\n".join([*preparation, "true"]) + "\n")):
            changed = copy.deepcopy(source)
            planted, = (item for item in changed["jobs"][CARRIERS[name]]["steps"]
                        if item.get("name") == BUILDER_SPLIT[name])
            planted["run"] = run
            # Each plant breaks one condition alone: two driver lines, or none.
            assert run.count(DRIVER_COMMAND) == (2 if "preparation" in label else 0), (name, label)
            try:
                generate(name, changed)
            except ValueError as exc:
                assert "one driver command" in str(exc), (name, label, str(exc))
                print("Builder split refused the " + name + " template with its " + label)
            else:
                raise AssertionError("builder split accepted the " + name + " template with its " + label)


def suite_generator_controls() -> None:
    """The generated Verilator graph keeps no dedicated milan_dp arm and expects its own
    workers; a template whose arm or expectation disagrees with its own total is refused."""
    source = load_template(ROOT, "rtl")
    jobs = generate("rtl", source)["jobs"]
    matrix = jobs["verilator-shards"]["strategy"]["matrix"]
    workers = len(matrix["shard"])
    assert matrix == {"shard": list(range(workers)), "total": [workers]}, matrix
    ownership, = (step["run"] for step in jobs["verilator-shards"]["steps"]
                  if step.get("name") == "Prove specialized suite ownership")
    assert "= milan_dp ;;" not in ownership, ownership
    verifier, = (step["run"] for step in jobs["verilator-suites"]["steps"]
                 if step.get("name") == "Require every shard to have validated this run's SHA")
    assert re.findall(r"--expect (\d+)", verifier) == [str(workers)], verifier
    total = source["jobs"]["verilator-shards"]["strategy"]["matrix"]["total"][0]
    arm = str(total - 1) + ') test "$(cat "$RUNNER_TEMP/owned-suites")" = milan_dp ;;'

    def planted(job: str, step_name: str, old: str, new: str) -> dict:
        """One template step's text replaced, every other byte of the template kept."""
        changed = copy.deepcopy(source)
        step, = (step for step in changed["jobs"][job]["steps"] if step.get("name") == step_name)
        assert step["run"].count(old) == 1, (step_name, old)
        step["run"] = step["run"].replace(old, new)
        return changed

    recount = copy.deepcopy(source)
    recount["jobs"]["verilator-shards"]["strategy"]["matrix"] = {
        "shard": list(range(total + 1)), "total": [total + 1]}
    for label, template in (
            ("arm index other than its total", planted(
                "verilator-shards", "Prove specialized suite ownership", arm, str(total - 2) + arm[1:])),
            ("--expect other than its total", planted(
                "verilator-suites", "Require every shard to have validated this run's SHA",
                "--expect " + str(total) + " ", "--expect " + str(total + 1) + " ")),
            ("total without its arm and --expect", recount)):
        try:
            generate("rtl", template)
        except ValueError as exc:
            print("Suite generator refused a template " + label + ": " + str(exc))
        else:
            raise AssertionError("suite generator accepted a template " + label)
    print(f"Suite generator: {workers} workers, no dedicated milan_dp arm, --expect {workers} PASS")


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


def census_budget(root: Path, cpus: int, kib: int | None, cgroup: str, limits: dict[str, str]) -> str | None:
    """CI_CENSUS_JOBS as the emitted shell sets it over proc and cgroup files planted in the new directory root;
    None if it refused."""
    (root / "bin").mkdir()
    (root / "bin" / "nproc").write_text("#!/bin/sh\nprintf '%s\\n' " + str(cpus) + "\n")
    (root / "bin" / "nproc").chmod(0o755)
    (root / "meminfo").write_text("MemFree:         1024 kB\n"
                                  + ("" if kib is None else f"MemTotal:       {kib} kB\n"))
    (root / "self-cgroup").write_text("0::" + cgroup + "\n")
    for directory, limit in limits.items():
        (root / "sys" / directory).mkdir(parents=True, exist_ok=True)
        (root / "sys" / directory / "memory.max").write_text(limit + "\n")
    (root / "sys").mkdir(exist_ok=True)
    script = census_budget_step()["run"]
    for real, planted, count in (("/proc/meminfo", root / "meminfo", 1),
                                 ("/proc/self/cgroup", root / "self-cgroup", 1),
                                 ("/sys/fs/cgroup", root / "sys", 2)):
        assert script.count(real) == count, real
        script = script.replace(real, str(planted))
    output = root / "census.env"
    ran = subprocess.run(["bash", "-c", script], check=False, capture_output=True, text=True,
                         env={**os.environ, "PATH": str(root / "bin") + ":" + os.environ["PATH"],
                              "GITHUB_ENV": str(output)})
    if ran.returncode:
        assert not output.exists(), ran
        return None
    lines = output.read_text().splitlines()
    assert len(lines) == 1 and lines[0].startswith("CI_CENSUS_JOBS="), lines
    return lines[0].removeprefix("CI_CENSUS_JOBS=")


def census_controls() -> None:
    """Execute the emitted census budget shell: bounded by the job's memory, never above nproc,
    refusing the unreadable."""
    gib = 1024 * 1024
    container = {"": str(8 * 2**30)}
    hosted = {"": "max", "system.slice": "max", "system.slice/runner.service": "max"}
    with tempfile.TemporaryDirectory(prefix="census-budgets-") as temporary:
        root = Path(temporary)
        for described, cpus, kib, cgroup, limits, want in (
            # #742: sixteen CPUs in an eight-GiB act job container on a 61 GiB host.
            ("act job container", 16, 61 * gib, "/", container, "4"),
            ("hosted runner without a cgroup limit", 4, 16 * gib, "/system.slice/runner.service", hosted, "4"),
            ("host memory below its cgroup's", 16, 4 * gib, "/", container, "2"),
            ("a lower ancestor limit", 16, 61 * gib, "/a/b", {"": "max", "a": str(4 * 2**30), "a/b": "max"}, "2"),
            ("fewer CPUs than memory allows", 2, 61 * gib, "/", container, "2"),
            ("memory for less than one worker", 16, 61 * gib, "/", {"": str(2**30)}, "1"),
            ("a cgroup without a memory controller", 16, 61 * gib, "/", {}, "16"),
            ("an unreadable limit", 16, 61 * gib, "/", {"": "garbage"}, None),
            ("an empty limit", 16, 61 * gib, "/", {"": ""}, None),
            ("no MemTotal", 16, None, "/", container, None),
            ("zero CPUs", 0, 61 * gib, "/", container, None),
        ):
            got = census_budget(Path(tempfile.mkdtemp(dir=root)), cpus, kib, cgroup, limits)
            assert got == want, (described, got, want)
            print(f"Census budget: {described}: {'refused' if got is None else got + ' worker(s)'}")
    assert 4 * CENSUS_WORKER_BYTES * 3 <= 2 * 8 * 2**30 < 5 * CENSUS_WORKER_BYTES * 3
    owners = [(name, job_id) for name in ("docs", "elaborate", "rtl", "rtl-fast")
              for job_id, job in generate(name, load_template(ROOT, name))["jobs"].items()
              if any(step.get("name") == census_budget_step()["name"] for step in job["steps"])]
    assert owners == [("rtl-fast", "publication-census")], owners
    steps = generate("rtl-fast", load_template(ROOT, "rtl-fast"))["jobs"]["publication-census"]["steps"]
    names = [step.get("name") for step in steps]
    census = next(i for i, step in enumerate(steps) if "publication_census.py" in step.get("run", ""))
    assert names.index(census_budget_step()["name"]) < census
    assert '--jobs "$CI_CENSUS_JOBS"' in steps[census]["run"] and "CI_CAMPAIGN_JOBS" not in steps[census]["run"]
    print("Census budget: only publication-census sets CI_CENSUS_JOBS, before its census")


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
    both = list(REQUIRED)
    good = builder_receipts(identity, names)
    assert union(good, *identity, both, names)["union"] == "pass"
    assert [len(cases) for cases in partition(names)] == [1, len(names) - 1]
    elaboration = "test_every_recipe_elaborates"
    rv32 = REQUIRED["--require-rv32"][0]

    def refused(label: str, receipts: list, expected: str, inventory: list[str] = names,
                flags: list[str] = both) -> None:
        """The union must refuse naming the planted gate or obligation."""
        try:
            union(receipts, *identity, flags, inventory)
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
    compare(reference, good, *identity, both, names)
    differs = copy.deepcopy(reference)
    differs["driver"]["gates"][-1]["not_run"] = [["gate 11", "no report", "row"]]
    try:
        compare(differs, good, *identity, both, names)
    except ValueError as exc:
        assert names[-1] in str(exc)
        print("Builder comparison refused a NOT RUN row the legs lack")
    else:
        raise AssertionError("comparison accepted an unequal NOT RUN ledger")
    docs_builder_controls(identity, names, reference, refused)
    print("Builder legs: union-level requirements and per-gate equality PASS")


def docs_builder_controls(identity: tuple[str, str], names: list[str], reference: dict,
                          refused: Callable[..., None]) -> None:
    """The docs command carries --require-rv32 alone; its union judges exactly that."""
    flags = requirements(builder_command("docs", load_template(ROOT, "docs")))
    assert flags == ["--require-rv32"]
    rv32 = REQUIRED["--require-rv32"][0]
    docs = builder_receipts(identity, names, tuple(flags))
    assert union(docs, *identity, flags, names)["requirements"] == {"--require-rv32": [rv32]}
    # Without --require-elaboration a LiteX or toolchain skip is a recorded
    # NOT RUN row, as in the unsharded docs run; with it, the union refuses.
    skip = copy.deepcopy(docs)
    skip[1]["driver"]["gates"][0]["not_run"] = [["gate 23g", "no LiteX here", "toolchain"]]
    assert union(skip, *identity, flags, names)["not_run"] == [["gate 23g", "no LiteX here", "toolchain"]]
    elaborate = copy.deepcopy(skip)
    for receipt in elaborate:
        receipt["driver"].update(requirements=list(REQUIRED), require_elaboration=0)
    refused("toolchain skip under the elaboration command", elaborate, "toolchain skip")
    unjudged = builder_receipts(identity, names, ())
    refused("docs RV32 gate in a leg without --require-rv32", [unjudged[0], docs[1]], rv32, flags=flags)
    refused("docs leg without its command's --require-rv32", [docs[0], unjudged[1]], "leg 1: requirement flags",
            flags=flags)
    extra = builder_receipts(identity, names, tuple(REQUIRED))
    refused("docs leg with a requirement its command lacks", [docs[0], extra[1]], "leg 1: requirement flags",
            flags=flags)
    for command, label in ((["python3", "x", "--require-rv32", "--require-rv32"], "repeated"),
                           (["python3", "x", "--require-anything"], "unknown")):
        try:
            requirements(command)
        except ValueError as exc:
            print("Builder requirements refused a " + label + " flag: " + str(exc))
        else:
            raise AssertionError("builder requirements accepted a " + label + " flag")
    docs_reference = copy.deepcopy(reference)
    docs_reference["driver"].update(requirements=flags, require_elaboration=None)
    compare(docs_reference, docs, *identity, flags, names)
    try:
        compare(reference, docs, *identity, flags, names)
    except ValueError as exc:
        assert "requirements" in str(exc)
        print("Builder comparison refused a reference run with another command's requirements")
    else:
        raise AssertionError("comparison accepted a reference with other requirements")
    print("Builder legs: the docs union judges --require-rv32 alone")


def case_step_controls(name: str, case: dict, generated: dict, original: dict) -> None:
    """Each gate is its worker's original step; a builder leg adds only its selection."""
    owned = [step for step in generated["jobs"][worker_id(name, case["leg"])]["steps"]
             if step.get("id") == case["id"]]
    assert len(owned) == 1
    body = copy.deepcopy(owned[0])
    del body["id"]
    if "builder" not in case:
        assert body == original
        return
    # The leg runs the template's own step, only adding its selection to the
    # driver command that ends it.
    assert body == builder_leg_step(original, case)
    assert case["leg"] == BUILDER_WORKERS[name][case["builder"]]
    *preparation, driver = original["run"].strip().split("\n")
    *kept, line = body["run"].strip().split("\n")
    assert kept == preparation and line.endswith(" -- " + driver), body["run"]
    words = shlex.split(line)
    assert words[:2] == ["python3", "scripts/ci_builder_legs.py"], words
    parsed, command = ci_builder_legs.parse(words[2:])
    assert (parsed.operation, parsed.leg, command) == ("run", str(case["builder"]), shlex.split(driver)), words
    assert parsed.receipt.name == "builder-leg-" + str(case["builder"]) + ".json"
    assert {key: value for key, value in body.items() if key not in ("name", "run")} == {
        key: value for key, value in original.items() if key not in ("name", "run")}


def main() -> int:
    """Drive the production generator and verifier with independent planted losses."""
    inventory_controls()
    scheduling_controls()
    builder_split_controls()
    suite_generator_controls()
    cpu_controls()
    census_controls()
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
        flags = requirements(builder_command(name, source))
        builder = builder_receipts(identity, flags=tuple(flags))
        assert len(verify(name, source, identity, digest, Collected(receipts, builder), needs)) == len(cases)
        assert set(generated["jobs"][carrier]["needs"]) == set(needs)
        original = source["jobs"][carrier]["steps"]
        for case in cases:
            case_step_controls(name, case, generated, original[case["index"]])
        for leg in legs:
            steps = generated["jobs"][worker_id(name, leg)]["steps"]
            index = {case["id"]: case["index"] for case in cases}
            source_order = [index[step["id"]] for step in steps if step.get("id") in index]
            assert source_order == sorted(source_order)
            assert len(source_order) == sum(case["leg"] == leg for case in cases)
        # Exactly the workers that run a builder leg retain its receipt.
        owners = {case["leg"] for case in cases if "builder" in case}
        assert owners == set(BUILDER_WORKERS[name]), (name, owners)
        for leg in legs:
            upload, = (step for step in generated["jobs"][worker_id(name, leg)]["steps"]
                       if step.get("name") == "Upload executed gate outcomes")
            retained = "builder-leg-*.json" in upload["with"]["path"]
            assert retained == (leg in owners), (name, leg, upload["with"]["path"])
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
        refuse("executed builder division without builder receipts", receipts, needs, None)
        refuse("executed builder division missing a leg receipt", receipts, needs, builder[:1])
        other = builder_receipts(identity, flags=tuple(sorted(set(REQUIRED) ^ set(flags))))
        refuse("builder legs run with the other workflow's requirement flags", receipts, needs, other)
        if name == "elaborate":
            mixed = copy.deepcopy(receipts)
            mixed[1]["scope"] = "false"
            for row in mixed[1]["results"]:
                row.update(outcome="skipped", conclusion="skipped")
            refuse("individually valid mixed execution scopes", mixed, needs)
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
