#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""Generate parallel gate jobs from the original, contract-checked step inventory.

Templates retain the ordered commands and setup. The generator schedules existing
steps, assigns receipt identifiers and adds a fail-closed public aggregate.
"""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
from pathlib import Path
import re
import shlex

import yaml


ROOT = Path(__file__).resolve().parents[1]
CARRIERS = {"docs": "docs-check", "elaborate": "elaborate"}
TEMPLATES = {name: ".github/ci-templates/" + name + ".yml"
             for name in (*CARRIERS, "rtl", "rtl-fast")}
LONG_GATE = {"elaborate": "Standalone LiteX simulation aggregate"}
CONTRACT_GATES = {"CI event and SHA contract gate", "Local act runner contract gate"}
#: The one template step per workflow whose driver command is divided by its
#: measured gate legs (scripts/ci_builder_legs.py), and the worker each leg
#: runs on: the docs legs beside the contract gates, the elaboration legs
#: beside the LiteX aggregate.
BUILDER_SPLIT = {"docs": "End-station builder gates", "elaborate": "Elaboration gates"}
BUILDER_WORKERS = {"docs": (1, 2), "elaborate": (0, 1)}
DRIVER_COMMAND = "python3 sw/builder/test_builder.py"
VERILATOR_SETUP = {"Cache the pinned Verilator build", "Build Verilator from source on cache miss",
                   "Put Verilator on PATH and prove the version"}
SETUP_PREFIXES = ("Install ", "Cache ", "Fetch ", "Apply ", "Place ", "Put ", "Keep ")
#: rtl-fast builds its pinned Yosys once, in a job of its own (#789). The
#: template keeps the build in yosys-elaboration; the generator moves it, and
#: the moved key binds the pinned version, the build recipe and the runner
#: image instead of every workflow file. A workflow edit then rebuilds nothing,
#: and a recipe change rebuilds in a job whose only work is the build.
FAST_TOOL_JOB = "yosys-tool"
FAST_TOOL_CONSUMER = "yosys-elaboration"
FAST_AGGREGATE = "rtl-fast"
#: The owner's 30-minute hosted budget (#789); no job's timeout is raised.
FAST_TOOL_TIMEOUT = 30
YOSYS_BUILD_STEPS = ("Cache the pinned Yosys build", "Build Yosys from source on cache miss")
FAST_TOOL_RESTORE = "Restore the pinned Yosys build"
WORKFLOW_FILES_DIGEST = "${{ hashFiles('.github/workflows/*.yml') }}"
#: The derivation's stand-in for the tool key's recipe digest. generate() replaces it once the tool job is
#: emitted as it runs, so the digest also covers what the transforms after the derivation add to the build:
#: the job budget step's exports, the package-index steps and the rewritten install line (#789).
FAST_TOOL_RECIPE = "recipe-{build-inputs}"
#: Tool job keys that only schedule it; every other job key is build environment and is digested.
FAST_TOOL_SCHEDULING = ("name", "needs", "if", "timeout-minutes")
#: yosys-elaboration's job keys the moved build ran under, so the tool job carries them. Any other job key
#: is refused rather than dropped from the build.
FAST_TOOL_CARRIED = ("runs-on", "env", "defaults")
#: The runtime evidence pair, the only steps the tool job runs after its build. They write only under
#: $RUNNER_TEMP, so nothing outside the digest runs between the build and the cache save.
FAST_TOOL_EVIDENCE = ("ci_record", "ci_upload")
#: A repository file a run body names, such as `scripts/ci_install_cache.py`, which prepares the package
#: index the build installs from. Absolute and `$VAR/` paths are the runner's, not the repository's.
REPOSITORY_READ = re.compile(r"(?<![\w.$/~-])(?:\./)?((?:[\w-]+/)+[\w.-]+\.(?:py|sh|txt|json|ya?ml|toml|cfg|patch|mk))"
                             r"(?![\w/])")


class Dumper(yaml.SafeDumper):
    """Each generated step owns its mapping; never emit YAML reference aliases."""

    def increase_indent(self, flow: bool = False, indentless: bool = False) -> None:
        """Keep source-like nested step indentation for dependency readers."""
        return super().increase_indent(flow, False)

    def ignore_aliases(self, _data: object) -> bool:
        """Keep generated workflow identities explicit."""
        return True


def represent_text(dumper: Dumper, value: str) -> yaml.ScalarNode:
    """Keep full shell scripts as literal blocks, preserving their exact text."""
    return dumper.represent_scalar("tag:yaml.org,2002:str", value,
                                   style="|" if "\n" in value else None)


Dumper.add_representer(str, represent_text)


def setup(step: dict) -> bool:
    """Identify the existing setup steps; all other template steps belong to the union."""
    uses = step.get("uses", "")
    return (uses.startswith(("actions/checkout@", "actions/setup-", "actions/cache@"))
            or step.get("id") == "scope"
            or step.get("name", "").startswith(SETUP_PREFIXES)
            or step.get("name") == "Build Verilator from source on cache miss")


def case_inventory(name: str, template: dict) -> list[dict]:
    """Derive gate identities and leg membership from the original ordered steps."""
    from ci_builder_legs import LEGS
    original = template["jobs"][CARRIERS[name]]["steps"]
    workers = BUILDER_WORKERS[name]
    if len(workers) != LEGS:
        raise ValueError(name + ": builder legs and their workers differ in number")
    cases = []
    for index, step in enumerate(original):
        if setup(step):
            continue
        case = {"id": "gate_" + str(index), "index": index,
                "name": step.get("name", "Run " + step.get("uses", "")),
                "condition": step.get("if", "success()"),
                "leg": (2 if name == "docs" and step.get("name") in CONTRACT_GATES
                        else int(name in LONG_GATE and step.get("name") == LONG_GATE[name]))}
        if step.get("name") != BUILDER_SPLIT[name]:
            cases.append(case)
            continue
        cases.extend({**case, "id": case["id"] + "_" + str(leg), "leg": workers[leg], "builder": leg,
                      "name": case["name"] + ", leg " + str(leg) + " of " + str(LEGS)}
                     for leg in range(LEGS))
    if (sum(case["name"] == LONG_GATE.get(name) for case in cases) != int(name in LONG_GATE)
            or not any(case["leg"] == 0 for case in cases)):
        raise ValueError(name + ": missing or ambiguous measured long gate")
    if sum("builder" in case for case in cases) != LEGS:
        raise ValueError(name + ": missing or ambiguous builder gate command")
    if len({case["name"] for case in cases}) != len(cases):
        raise ValueError(name + ": duplicate gate names")
    return cases


def worker_legs(name: str, template: dict) -> list[int]:
    """Derive every required worker from the original gate inventory."""
    return sorted({case["leg"] for case in case_inventory(name, template)})


def worker_id(name: str, leg: int) -> str:
    """A concrete job the public carrier must require."""
    return name + "-gates-" + str(leg)


def split_builder_run(step: dict) -> tuple[list[str], str]:
    """A divided step's preparation lines and its one driver command, which ends it."""
    *preparation, command = step["run"].strip().split("\n")
    if (not command.startswith(DRIVER_COMMAND + " ")
            or any("sw/builder/test_builder.py" in line for line in preparation)):
        raise ValueError("the divided builder step must end in its one driver command")
    return preparation, command


def builder_command(name: str, template: dict) -> list[str]:
    """The template's divided driver command; its requirement flags are the union's."""
    steps = [step for step in template["jobs"][CARRIERS[name]]["steps"]
             if step.get("name") == BUILDER_SPLIT[name]]
    if len(steps) != 1:
        raise ValueError(name + ": missing or ambiguous builder gate command")
    return shlex.split(split_builder_run(steps[0])[1])


def builder_leg_step(step: dict, case: dict) -> dict:
    """The template's own builder step, its driver command run for one measured leg with its receipt."""
    preparation, command = split_builder_run(step)
    kept = {key: copy.deepcopy(value) for key, value in step.items() if key != "run"}
    kept["name"] = case["name"]
    kept["run"] = ("".join(line + "\n" for line in preparation)
                   + "python3 scripts/ci_builder_legs.py run " + str(case["builder"])
                   + ' --receipt "$RUNNER_TEMP/gate-results/builder-leg-' + str(case["builder"])
                   + '.json" -- ' + command + "\n")
    return kept


def collection_steps(name: str, leg: int) -> list[dict]:
    """Observe completed source steps even on failure, then retain the actual evidence."""
    destination = "$RUNNER_TEMP/gate-results/receipt.json"
    retained = "${{ runner.temp }}/gate-results/receipt.json"
    if leg in BUILDER_WORKERS[name]:
        retained += "\n${{ runner.temp }}/gate-results/builder-leg-*.json\n"
    return [
        {"name": "Record executed gate outcomes", "if": "${{ always() }}",
         "env": {"CI_GATE_STEPS": "${{ toJSON(steps) }}",
                 "CI_GATE_SCOPE": "${{ steps.scope.outputs.rtl }}"},
         "run": ("python3 scripts/ci_gate_receipts.py record --workflow " + name
                 + " --leg " + str(leg) + ' --output "' + destination + '"\n')},
        {"name": "Upload executed gate outcomes", "if": "${{ always() }}",
         "uses": "actions/upload-artifact@v4",
         "with": {"name": "gate-" + name + "-" + str(leg) + "-${{ github.sha }}",
                  "path": retained, "if-no-files-found": "error"}},
    ]


def aggregate(name: str, template: dict) -> dict:
    """Retain the protected name, requiring both successful jobs and the actual union."""
    from ci_runtime_workflows import reader_setup
    checkout = copy.deepcopy(template["jobs"][CARRIERS[name]]["steps"][0])
    if not str(checkout.get("uses", "")).startswith("actions/checkout@"):
        raise ValueError(name + ": original checkout must stay first")
    return {"runs-on": "ubuntu-24.04", "timeout-minutes": 3,
            "needs": [worker_id(name, leg) for leg in worker_legs(name, template)], "if": "${{ always() }}",
            "steps": [checkout, *reader_setup(),
                      {"name": "Download executed gate outcomes", "uses": "actions/download-artifact@v4",
                       "continue-on-error": True,
                       "with": {"pattern": "gate-" + name + "-*-${{ github.sha }}",
                                "path": "${{ runner.temp }}/gate-results"}},
                      {"name": "Require every gate exactly once",
                       "env": {"CI_GATE_NEEDS": "${{ toJSON(needs) }}"},
                       "run": ("python3 scripts/ci_gate_receipts.py verify --workflow " + name
                               + ' --root "$RUNNER_TEMP/gate-results" --head "$GITHUB_SHA"'
                               + ' --output "$RUNNER_TEMP/gate-union.json"\n')},
                      {"name": "Upload verified gate union", "uses": "actions/upload-artifact@v4",
                       "with": {"name": "gate-union-" + name + "-${{ github.sha }}",
                                "path": "${{ runner.temp }}/gate-union.json", "if-no-files-found": "error"}}]
            }


def recipe_digest(inputs: dict) -> str:
    """The build inputs, every key included, as one digest."""
    return hashlib.sha256(json.dumps(inputs, sort_keys=True, separators=(",", ":")).encode()).hexdigest()


def fast_tool_key(cache: dict, image: str) -> str:
    """The template key, its workflow-file digest replaced by the recipe stand-in and the runner image."""
    key = cache["with"]["key"]
    if key.count(WORKFLOW_FILES_DIGEST) != 1:
        raise ValueError(FAST_TOOL_CONSUMER + ": Yosys cache key lacks its one workflow-file digest")
    return key.replace(WORKFLOW_FILES_DIGEST, FAST_TOOL_RECIPE + "-" + image)


def fast_tool_inputs(workflow: dict) -> tuple[dict, list[str]]:
    """What the emitted tool job feeds its build, and the repository files those steps name.

    The inputs are the workflow's `env` and `defaults`, the tool job's keys other than its scheduling ones,
    and every step up to and including the build as it runs, the moved cache step's own key aside. Make
    reads every environment variable as a variable of the same name, so no `env` entry is left out as
    unrelated (#789)."""
    tool = workflow["jobs"][FAST_TOOL_JOB]
    names = [step.get("name") for step in tool["steps"]]
    if [name for name in names if name in YOSYS_BUILD_STEPS] != list(YOSYS_BUILD_STEPS):
        raise ValueError(FAST_TOOL_JOB + ": missing or reordered Yosys build recipe")
    end = names.index(YOSYS_BUILD_STEPS[1]) + 1
    after = tool["steps"][end:]
    if [step.get("id") for step in after] != list(FAST_TOOL_EVIDENCE):
        raise ValueError(FAST_TOOL_JOB + ": steps after the build that its key does not bind: " + ", ".join(
            str(step.get("name", step.get("id"))) for step in after if step.get("id") not in FAST_TOOL_EVIDENCE))
    steps = copy.deepcopy(tool["steps"][:end])
    del steps[names.index(YOSYS_BUILD_STEPS[0])]["with"]["key"]
    inputs = {"workflow": {key: workflow.get(key) for key in ("env", "defaults")},
              "job": {**{key: value for key, value in tool.items() if key not in (*FAST_TOOL_SCHEDULING, "steps")},
                      "steps": steps}}
    return inputs, sorted({path for step in steps for path in REPOSITORY_READ.findall(step.get("run", ""))})


def bind_fast_tool_key(workflow: dict) -> None:
    """Replace the recipe stand-in in the tool cache and its one restore with the digest of the build inputs.

    A repository file the build's steps name is bound by its content through `hashFiles`, which both jobs
    evaluate on the same checkout; the workflow files are never among them."""
    inputs, reads = fast_tool_inputs(workflow)
    recipe = "recipe-" + recipe_digest(inputs)
    if reads:
        recipe += "-${{ hashFiles(" + ", ".join("'" + path + "'" for path in reads) + ") }}"
    keyed = [(job_id, step.get("name")) for job_id, job in workflow["jobs"].items() for step in job["steps"]
             if FAST_TOOL_RECIPE in str(step.get("with", {}).get("key", ""))]
    if keyed != [(FAST_TOOL_JOB, YOSYS_BUILD_STEPS[0]), (FAST_TOOL_CONSUMER, FAST_TOOL_RESTORE)]:
        raise ValueError(FAST_TOOL_JOB + ": the recipe stand-in must key exactly its cache and the one restore")
    for job_id, name in keyed:
        step = next(step for step in workflow["jobs"][job_id]["steps"] if step.get("name") == name)
        step["with"]["key"] = step["with"]["key"].replace(FAST_TOOL_RECIPE, recipe)


def result_binding(job_id: str) -> tuple[str, str]:
    """The fast verdict's environment name and value for one needed job's result."""
    return job_id.upper().replace("-", "_") + "_RESULT", "${{ needs." + job_id + ".result }}"


def require_fast_tool(verdict_job: dict) -> None:
    """A failed tool job skips yosys-elaboration, which the verdict accepts, so it reads the tool's result too."""
    tool, tool_value = result_binding(FAST_TOOL_JOB)
    consumer, _ = result_binding(FAST_TOOL_CONSUMER)
    steps = verdict_job["steps"]
    if FAST_TOOL_CONSUMER not in verdict_job["needs"] or len(steps) != 1 or consumer not in steps[0]["env"]:
        raise ValueError(FAST_AGGREGATE + ": verdict lacks its yosys-elaboration result")
    verdict_job["needs"].insert(verdict_job["needs"].index(FAST_TOOL_CONSUMER), FAST_TOOL_JOB)
    verdict = steps[0]
    env = {}
    for name, value in verdict["env"].items():
        if name == consumer:
            env[tool] = tool_value
        env[name] = value
    verdict["env"] = env
    lines = verdict["run"].split("\n")
    pair = '"' + FAST_TOOL_CONSUMER + ":$" + consumer + '" \\'
    found = [index for index, line in enumerate(lines) if line.strip() == pair]
    if len(found) != 1:
        raise ValueError(FAST_AGGREGATE + ": verdict lacks its one yosys-elaboration result pair")
    line = lines[found[0]]
    lines.insert(found[0], line[:len(line) - len(line.lstrip())] + '"' + FAST_TOOL_JOB + ":$" + tool + '" \\')
    verdict["run"] = "\n".join(lines)


def fast_yosys_tool(source: dict) -> dict:
    """Build Yosys in its own job; yosys-elaboration restores that exact tree or fails (#789)."""
    jobs = source["jobs"]
    consumer = jobs[FAST_TOOL_CONSUMER]
    names = [step.get("name") for step in consumer["steps"]]
    if (FAST_TOOL_JOB in jobs or [name for name in names if name in YOSYS_BUILD_STEPS] != list(YOSYS_BUILD_STEPS)
            or names[names.index(YOSYS_BUILD_STEPS[0]) + 1] != YOSYS_BUILD_STEPS[1]):
        raise ValueError(FAST_TOOL_CONSUMER + ": missing or reordered Yosys build recipe")
    checkout = consumer["steps"][0]
    if not str(checkout.get("uses", "")).startswith("actions/checkout@"):
        raise ValueError(FAST_TOOL_CONSUMER + ": original checkout must stay first")
    unmodelled = sorted(set(consumer) - {"steps", *FAST_TOOL_SCHEDULING, *FAST_TOOL_CARRIED})
    if unmodelled:
        raise ValueError(FAST_TOOL_CONSUMER + ": job keys the tool job does not carry into the build: "
                         + ", ".join(unmodelled))
    at = names.index(YOSYS_BUILD_STEPS[0])
    cache, build = consumer["steps"][at:at + 2]
    key = fast_tool_key(cache, consumer["runs-on"])
    moved = copy.deepcopy(cache)
    moved["with"]["key"] = key
    tool = {"name": "Prepare pinned Yosys", "runs-on": consumer["runs-on"], "timeout-minutes": FAST_TOOL_TIMEOUT,
            "needs": copy.deepcopy(consumer["needs"]), "if": consumer["if"],
            **{carried: copy.deepcopy(consumer[carried]) for carried in FAST_TOOL_CARRIED[1:] if carried in consumer},
            "steps": [copy.deepcopy(checkout), moved, copy.deepcopy(build)]}
    needs = consumer["needs"]
    consumer["needs"] = [*([needs] if isinstance(needs, str) else needs), FAST_TOOL_JOB]
    # The tool job's exact tree or a refusal: no fallback key, and no build here.
    consumer["steps"][at:at + 2] = [{"name": FAST_TOOL_RESTORE, "uses": cache["uses"],
                                     "with": {"path": cache["with"]["path"], "key": key,
                                              "fail-on-cache-miss": True}}]
    require_fast_tool(jobs[FAST_AGGREGATE])
    ordered = {}
    for job_id, job in jobs.items():
        if job_id == FAST_TOOL_CONSUMER:
            ordered[FAST_TOOL_JOB] = tool
        ordered[job_id] = job
    source["jobs"] = ordered
    return source


def gate_graph(name: str, template: dict) -> dict:
    """Preserve ordered bodies, conditions, bindings and source checkout in each leg."""
    source = copy.deepcopy(template)
    if True in source:
        source["on"] = source.pop(True)
    if name not in CARRIERS:
        if name == "rtl":
            from ci_suite_workflows import generate as suite_workflows
            return suite_workflows(source)
        if name == "rtl-fast":
            return fast_yosys_tool(source)
        return source
    original = source["jobs"].pop(CARRIERS[name])
    cases: dict[int, list[dict]] = {}
    for case in case_inventory(name, template):
        cases.setdefault(case["index"], []).append(case)
    for leg in worker_legs(name, template):
        worker = {key: copy.deepcopy(value) for key, value in original.items() if key != "steps"}
        worker["timeout-minutes"] = 45
        worker["steps"] = []
        for index, step in enumerate(original["steps"]):
            owned = [case for case in cases.get(index, []) if case["leg"] == leg]
            if index in cases and not owned:
                continue
            if name == "elaborate" and step.get("name") in VERILATOR_SETUP and leg != 1:
                continue
            case = owned[0] if owned else None
            kept = builder_leg_step(step, case) if case and "builder" in case else copy.deepcopy(step)
            if case:
                if "id" in kept:
                    raise ValueError(name + ": gate already has an output identifier")
                kept["id"] = case["id"]
            if step.get("name") == "CI scheduling and evidence controls":
                from ci_suite_workflows import inventory_dependencies
                worker["steps"].append(inventory_dependencies())
            worker["steps"].append(kept)
        worker["steps"].extend(collection_steps(name, leg))
        source["jobs"][worker_id(name, leg)] = worker
    source["jobs"][CARRIERS[name]] = aggregate(name, template)
    return source



def generate(name: str, template: dict) -> dict:
    """Add runtime collection after deriving the unchanged gate schedule."""
    from ci_runtime_workflows import generate as runtime_workflows
    from ci_install_workflows import generate as install_workflows
    from ci_suite_workflows import check_inventory_dependencies
    result = runtime_workflows(name, install_workflows(gate_graph(name, template)))
    if name == "rtl-fast":
        bind_fast_tool_key(result)
    check_inventory_dependencies(result)
    return result


def load_template(root: Path, name: str) -> dict:
    """Read the source inventory; the workflow contract also validates every original step."""
    value = yaml.safe_load(root.joinpath(TEMPLATES[name]).read_text())
    if not isinstance(value, dict):
        raise ValueError(name + ": template must be a mapping")
    return value


def rendered(name: str, template: dict) -> str:
    """Only this generator writes the derived hosted workflow."""
    value = generate(name, template)
    if True in value:
        value["on"] = value.pop(True)
    return ("# Generated by scripts/ci_gate_workflows.py from " + TEMPLATES[name] + ".\n"
            + "# Edit the template and regenerate; original commands remain contract-checked.\n"
            + yaml.dump(value, Dumper=Dumper, sort_keys=False, width=100))


def main() -> int:
    """Regenerate, or fail when a checked-in generated workflow has drifted."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=ROOT)
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    failed = False
    for name in TEMPLATES:
        target = args.root / ".github/workflows" / (name + ".yml")
        expected = rendered(name, load_template(args.root, name))
        if args.check:
            if target.read_text() != expected:
                print(str(target.relative_to(args.root)) + ": regenerate the gate jobs")
                failed = True
        else:
            target.write_text(expected)
    return int(failed)


if __name__ == "__main__":
    raise SystemExit(main())
