#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""rtl-fast's pinned Yosys (#789): one cached build under a key bound to every build input, an exact restore,
both derived jobs held whole against the template, the emitted workflow held whole against what the shared
transforms make of the derivation, and a verdict that reads the tool job.

ci_gate_workflows_selftest.py runs fast_tool_controls() in the hosted "CI scheduling and evidence controls" step.
"""

import copy
import fnmatch
import os
import re
import subprocess
from unittest.mock import patch

from collections.abc import Callable

import ci_gate_workflows
import ci_install_workflows
import ci_runtime_workflows
from ci_gate_workflows import ROOT, generate, gate_graph, load_template
from ci_gate_workflows import FAST_AGGREGATE, FAST_TOOL_CONSUMER, FAST_TOOL_JOB, FAST_TOOL_RECIPE, YOSYS_BUILD_STEPS


#: The owner's hosted budget for every job (#789), held here rather than read
#: from the generator, whose constant is what this control judges.
HOSTED_BUDGET_MINUTES = 30
FAST_VERDICT_STEP = "Require every applicable fast gate to pass"
GENERATED_FAST = ".github/workflows/rtl-fast.yml"
VERSION_PROOF = "Install the pinned Yosys and prove the version"
TOOL_RESTORE = "Restore the pinned Yosys build"
SELF_TEST = "Prove the result cache refuses a planted entry"
#: The bound recipe in place of the stand-in: its digest and the optional `hashFiles` of the scripts it reads.
BOUND_RECIPE = r"(recipe-[0-9a-f]{64}(?:-\$\{\{ hashFiles\('[^']+'(?:, '[^']+')*\) \}\})?)"


def named_step(job: dict, name: str) -> dict | None:
    """The one step of `job` called `name`, or None."""
    found = [step for step in job["steps"] if step.get("name") == name]
    return found[0] if len(found) == 1 else None


def key_reads(key: str) -> list[str]:
    """Every path a cache key's `hashFiles` calls name."""
    return [path for call in re.findall(r"hashFiles\(([^)]*)\)", key) for path in re.findall(r"'([^']*)'", call)]


def scripts_run(run: str) -> set[str]:
    """The repository scripts a run body executes with `python3`, `bash` or `sh`, read here independently of
    the generator's own scan."""
    return {path.removeprefix("./") for path in re.findall(
        r"\b(?:python3|bash|sh)\s+(?:-\S+\s+)*([\w./-]+\.(?:py|sh))\b", run) if not path.startswith("/")}


def verdict_exit(job: dict, results: dict[str, str]) -> int:
    """Run the fast verdict's own script with every needed job's result."""
    step = named_step(job, FAST_VERDICT_STEP)
    env = {name: results.get(value.removeprefix("${{ needs.").removesuffix(".result }}"), "success")
           for name, value in step["env"].items()}
    return subprocess.run(["bash", "-c", step["run"]], env={**os.environ, **env}, check=False,
                          capture_output=True, text=True).returncode


def fast_tool_findings(template: dict, generated: dict) -> list[str]:
    """Every property #789 asks of rtl-fast's Yosys, each refused in its own words; empty is a pass."""
    source, jobs = template["jobs"], generated["jobs"]
    findings = []
    tool, consumer, aggregate = jobs.get(FAST_TOOL_JOB), jobs[FAST_TOOL_CONSUMER], jobs[FAST_AGGREGATE]
    original = source[FAST_TOOL_CONSUMER]
    cache, build = (named_step(original, name) for name in YOSYS_BUILD_STEPS)
    if tool is None or tool.get("name") != "Prepare pinned Yosys":
        return ["no Prepare pinned Yosys job"]
    # The moved build ran under the consumer's job environment, so the tool job runs it under the same one.
    for key in ("needs", "if", "runs-on", "env", "defaults"):
        if tool.get(key) != original.get(key):
            findings.append("tool job " + key + " differs from yosys-elaboration's")
    raised = [job_id for job_id, job in source.items() if jobs[job_id].get("timeout-minutes") != job["timeout-minutes"]]
    if raised or not 0 < tool["timeout-minutes"] <= HOSTED_BUDGET_MINUTES:
        findings.append("timeout changed or above the hosted budget: " + ", ".join(raised or [FAST_TOOL_JOB]))
    moved = named_step(tool, YOSYS_BUILD_STEPS[0])
    if (moved is None or named_step(tool, YOSYS_BUILD_STEPS[1]) is None
            or {k: v for k, v in moved.items() if k != "with"} != {k: v for k, v in cache.items() if k != "with"}
            or moved["with"].get("path") != cache["with"]["path"]):
        findings.append("tool job does not carry the template cache and build steps")
        return findings
    if set(moved["with"]) != {"path", "key"}:
        findings.append("tool cache restores more than its exact key")
    key = moved["with"]["key"]
    source_commit = re.search(r'rev-parse HEAD\)" = "([0-9a-f]{40})"', build["run"]).group(1)
    reads = key_reads(key)
    built = tool["steps"][:[step.get("name") for step in tool["steps"]].index(YOSYS_BUILD_STEPS[1]) + 1]
    unbound = sorted(set().union(*(scripts_run(step.get("run", "")) for step in built)) - set(reads))
    for words, held in (("tool key binds the workflow files",
                         not any(fnmatch.fnmatch(GENERATED_FAST, path) or path.startswith(".github/")
                                 for path in reads)),
                        ("tool key does not bind the scripts its build steps run: " + ", ".join(unbound),
                         not unbound),
                        ("tool key lacks the pinned version", key.startswith("yosys-${{ env.YOSYS_VERSION }}-")
                         and '--branch "$YOSYS_VERSION"' in build["run"]),
                        ("tool key lacks the source commit", "-" + source_commit + "-" in key),
                        ("tool key lacks the build recipe", re.search(r"-recipe-[0-9a-f]{64}-", key) is not None),
                        ("tool key lacks the runner image",
                         key.endswith("-" + original["runs-on"] + "-${{ runner.os }}"))):
        if not held:
            findings.append(words)
    if any(step.get("name") in YOSYS_BUILD_STEPS or "/tmp/yosys-src" in step.get("run", "")
           for step in consumer["steps"]):
        findings.append("yosys-elaboration builds Yosys")
    needs = original["needs"]
    if consumer["needs"] != [*([needs] if isinstance(needs, str) else needs), FAST_TOOL_JOB]:
        findings.append("yosys-elaboration does not need the tool job")
    restores = [step for step in consumer["steps"] if step.get("with", {}).get("path") == cache["with"]["path"]]
    names = [step.get("name") for step in consumer["steps"]]
    install = names.index(VERSION_PROOF) if VERSION_PROOF in names else -1
    if (len(restores) != 1 or restores[0].get("uses") != cache["uses"]
            or restores[0]["with"] != {"path": cache["with"]["path"], "key": key, "fail-on-cache-miss": True}
            or consumer["steps"].index(restores[0]) > install):
        findings.append("yosys-elaboration does not restore exactly the tool tree before its version proof")
    if FAST_TOOL_JOB not in aggregate["needs"] or verdict_exit(aggregate, {FAST_TOOL_JOB: "failure",
                                                                         FAST_TOOL_CONSUMER: "skipped"}) == 0:
        findings.append("rtl-fast verdict accepts a failed tool job")
    if verdict_exit(aggregate, {}) != 0:
        findings.append("rtl-fast verdict refuses an all-green run")
    return findings


def tool_cache(jobs: dict) -> dict:
    """The moved cache step's `with`."""
    return named_step(jobs[FAST_TOOL_JOB], YOSYS_BUILD_STEPS[0])["with"]


def tool_restore(jobs: dict) -> dict:
    """yosys-elaboration's restore step's `with`."""
    return named_step(jobs[FAST_TOOL_CONSUMER], TOOL_RESTORE)["with"]


def verdict_step(jobs: dict) -> dict:
    """The fast verdict step."""
    return named_step(jobs[FAST_AGGREGATE], FAST_VERDICT_STEP)


def fast_tool_planted(template: dict, generated: dict) -> None:
    """One planted defect per property of the generated graph; each must be refused in its own words."""
    key = tool_cache(generated["jobs"])["key"]
    source_commit = re.search(r"-([0-9a-f]{40})-", key).group(1)
    recipe = re.search(r"-recipe-[0-9a-f]{64}", key).group(0)
    binding = re.search(r"-\$\{\{ hashFiles\([^)]*\) \}\}", key).group(0)
    unpinned = key.replace(recipe, "-${{ hashFiles('.github/workflows/*.yml') }}")
    template_build = named_step(template["jobs"][FAST_TOOL_CONSUMER], YOSYS_BUILD_STEPS[1])
    for label, edit, words in (
            ("tool key bound to the workflow files", lambda jobs: tool_cache(jobs).update(key=unpinned),
             "tool key binds the workflow files"),
            ("tool key without its script binding", lambda jobs: tool_cache(jobs).update(
                key=key.replace(binding, "")), "tool key does not bind the scripts its build steps run"),
            ("tool job under another environment", lambda jobs: jobs[FAST_TOOL_JOB].update(
                {"env": {"CXXFLAGS": "-O0"}}), "tool job env differs from yosys-elaboration's"),
            ("tool key without the version", lambda jobs: tool_cache(jobs).update(
                key=key.replace("${{ env.YOSYS_VERSION }}", "v0")), "tool key lacks the pinned version"),
            ("tool key without the source", lambda jobs: tool_cache(jobs).update(
                key=key.replace(source_commit, "head")), "tool key lacks the source commit"),
            ("tool key without the recipe", lambda jobs: tool_cache(jobs).update(
                key=key.replace(recipe, "")), "tool key lacks the build recipe"),
            ("tool key without the image", lambda jobs: tool_cache(jobs).update(
                key=key.replace("-ubuntu-24.04", "")), "tool key lacks the runner image"),
            ("tool cache with a fallback", lambda jobs: tool_cache(jobs).update({"restore-keys": "yosys-"}),
             "tool cache restores more than its exact key"),
            ("tool job without its build", lambda jobs: jobs[FAST_TOOL_JOB]["steps"].remove(
                named_step(jobs[FAST_TOOL_JOB], YOSYS_BUILD_STEPS[1])),
             "tool job does not carry the template cache and build steps"),
            ("tool timeout above the budget", lambda jobs: jobs[FAST_TOOL_JOB].update({"timeout-minutes": 45}),
             "timeout changed or above the hosted budget: yosys-tool"),
            ("consumer timeout raised", lambda jobs: jobs[FAST_TOOL_CONSUMER].update({"timeout-minutes": 45}),
             "timeout changed or above the hosted budget: yosys-elaboration"),
            ("tool job on another condition", lambda jobs: jobs[FAST_TOOL_JOB].update({"if": "${{ true }}"}),
             "tool job if differs from yosys-elaboration's"),
            ("consumer builds again", lambda jobs: jobs[FAST_TOOL_CONSUMER]["steps"].insert(
                4, copy.deepcopy(template_build)), "yosys-elaboration builds Yosys"),
            ("consumer without the tool need", lambda jobs: jobs[FAST_TOOL_CONSUMER].update({"needs": "changes"}),
             "yosys-elaboration does not need the tool job"),
            ("restore accepts a miss", lambda jobs: tool_restore(jobs).pop("fail-on-cache-miss"),
             "yosys-elaboration does not restore exactly the tool tree"),
            ("restore with a fallback", lambda jobs: tool_restore(jobs).update({"restore-keys": "yosys-"}),
             "yosys-elaboration does not restore exactly the tool tree"),
            ("restore of another key", lambda jobs: tool_restore(jobs).update(key=unpinned),
             "yosys-elaboration does not restore exactly the tool tree"),
            ("verdict without the tool need", lambda jobs: jobs[FAST_AGGREGATE]["needs"].remove(FAST_TOOL_JOB),
             "rtl-fast verdict accepts a failed tool job"),
            ("verdict without the tool pair", lambda jobs: verdict_step(jobs).update(
                run=verdict_step(jobs)["run"].replace('"yosys-tool:$YOSYS_TOOL_RESULT" \\\n', "")),
             "rtl-fast verdict accepts a failed tool job")):
        changed = copy.deepcopy(generated)
        edit(changed["jobs"])
        found = fast_tool_findings(template, changed)
        assert any(words in finding for finding in found), (label, found)
        print("Fast Yosys tool refused " + label + ": " + "; ".join(found))


def step_label(step: dict) -> str:
    """A template step's name, or the action an unnamed step uses."""
    return step.get("name", step.get("uses"))


def step_findings(owner: str, expected: list[dict], actual: list[dict], steps: str) -> list[str]:
    """Each step of `expected` that `actual` drops or changes and each step it adds, else any reordering or
    repeat, in `owner`'s words; empty when the two lists are equal."""
    labels, expected_labels = [step_label(step) for step in actual], [step_label(step) for step in expected]
    findings = []
    for step in expected:
        if step_label(step) not in labels:
            findings.append(owner + " drops " + step_label(step))
        elif step not in actual:
            findings.append(owner + " changes " + step_label(step))
    findings.extend(owner + " adds " + label for label in labels if label not in expected_labels)
    if not findings and actual != expected:
        findings.append(owner + " reorders or repeats its " + steps)
    return findings


def fast_tool_retention(template: dict, derived: dict) -> list[str]:
    """yosys-elaboration after the derivation runs every template step but the moved pair, in order and
    unchanged, with the one exact restore in the pair's place; the tool job runs exactly the checkout and the
    two moved steps. Each deviation is refused by name; empty is a pass (#789)."""
    original = template["jobs"][FAST_TOOL_CONSUMER]
    consumer, tool = derived[FAST_TOOL_CONSUMER], derived.get(FAST_TOOL_JOB, {"steps": []})
    at = [step.get("name") for step in original["steps"]].index(YOSYS_BUILD_STEPS[0])
    cache, build = original["steps"][at:at + 2]
    kept = [*original["steps"][:at], *original["steps"][at + 2:]]
    live = [step for step in consumer["steps"] if step.get("name") != TOOL_RESTORE]
    labels, kept_labels = [step_label(step) for step in live], [step_label(step) for step in kept]
    findings = step_findings(FAST_TOOL_CONSUMER, kept, live, "retained steps")
    key = (named_step(tool, YOSYS_BUILD_STEPS[0]) or {"with": {}})["with"].get("key")
    restore = {"name": TOOL_RESTORE, "uses": cache["uses"],
               "with": {"path": cache["with"]["path"], "key": key, "fail-on-cache-miss": True}}
    places = [index for index, step in enumerate(consumer["steps"]) if step.get("name") == TOOL_RESTORE]
    if (len(places) != 1 or consumer["steps"][places[0]] != restore
            or [step_label(step) for step in consumer["steps"][:places[0]]]
            != [label for label in kept_labels[:at] if label in labels]):
        findings.append("yosys-elaboration's one exact restore is not in its build's place")
    if ({name: value for name, value in consumer.items() if name not in ("steps", "needs")}
            != {name: value for name, value in original.items() if name not in ("steps", "needs")}):
        findings.append("yosys-elaboration's job keys differ from the template's")
    moved = copy.deepcopy(cache)
    moved["with"]["key"] = key
    if tool["steps"] != [original["steps"][0], moved, build]:
        findings.append("tool job steps are not the checkout and the two moved steps")
    return findings


def fast_tool_retention_planted(template: dict, derived: dict) -> None:
    """Each retained step dropped, and each other deviation of the two derived jobs, refused by name."""
    kept = [step_label(step) for step in template["jobs"][FAST_TOOL_CONSUMER]["steps"]
            if step.get("name") not in YOSYS_BUILD_STEPS]

    def consumer(jobs: dict) -> list[dict]:
        """yosys-elaboration's derived steps."""
        return jobs[FAST_TOOL_CONSUMER]["steps"]

    def drop(label: str) -> Callable[[dict], None]:
        """Remove the one derived step labelled `label`."""
        return lambda jobs: consumer(jobs).remove(next(step for step in consumer(jobs) if step_label(step) == label))

    def swap(jobs: dict) -> None:
        """Exchange the two retained steps after the elaboration."""
        steps = consumer(jobs)
        first = [step_label(step) for step in steps].index("Prove ooc.sh generates the ROMs and fails on a failed top")
        steps[first], steps[first + 1] = steps[first + 1], steps[first]

    def edited(jobs: dict) -> None:
        """One retained body rewritten."""
        step = named_step(jobs[FAST_TOOL_CONSUMER], "Elaborate the integration-heavy tops")
        assert step["run"].count(" \\\n  --top KL_gptp_shadow") == 1
        step["run"] = step["run"].replace(" \\\n  --top KL_gptp_shadow", "")

    def restore_last(jobs: dict) -> None:
        """The restore moved behind every retained step."""
        steps = consumer(jobs)
        steps.append(steps.pop([step.get("name") for step in steps].index(TOOL_RESTORE)))

    for label, edit, words in (
            *((label + " dropped", drop(label), "yosys-elaboration drops " + label) for label in kept),
            ("a retained body rewritten", edited, "yosys-elaboration changes Elaborate the integration-heavy tops"),
            ("a step added", lambda jobs: consumer(jobs).append({"name": "Planted step", "run": "true\n"}),
             "yosys-elaboration adds Planted step"),
            ("two retained steps swapped", swap, "yosys-elaboration reorders or repeats its retained steps"),
            ("a retained step repeated", lambda jobs: consumer(jobs).append(
                copy.deepcopy(named_step(jobs[FAST_TOOL_CONSUMER], SELF_TEST))),
             "yosys-elaboration reorders or repeats its retained steps"),
            ("the restore moved last", restore_last,
             "yosys-elaboration's one exact restore is not in its build's place"),
            ("the restore accepting a miss", lambda jobs: tool_restore(jobs).pop("fail-on-cache-miss"),
             "yosys-elaboration's one exact restore is not in its build's place"),
            ("a consumer job key added", lambda jobs: jobs[FAST_TOOL_CONSUMER].update({"env": {"X": "1"}}),
             "yosys-elaboration's job keys differ from the template's"),
            ("a tool job step added", lambda jobs: jobs[FAST_TOOL_JOB]["steps"].append(
                {"name": "Planted step", "run": "true\n"}), "tool job steps are not the checkout and the two moved"),
            ("the tool build rewritten", lambda jobs: named_step(jobs[FAST_TOOL_JOB], YOSYS_BUILD_STEPS[1]).update(
                run="true\n"), "tool job steps are not the checkout and the two moved")):
        changed = copy.deepcopy(derived)
        edit(changed)
        found = fast_tool_retention(template, changed)
        assert any(words in finding for finding in found), (label, found)
        print("Fast Yosys tool retention refused " + label + ": " + "; ".join(found))
    # The same judge on the generator itself: a derivation that drops a self-test is named.
    derive = ci_gate_workflows.fast_yosys_tool

    def dropping(source: dict) -> dict:
        """The real derivation, then one retained self-test removed from its output."""
        result = derive(source)
        drop(SELF_TEST)(result["jobs"])
        return result

    with patch.object(ci_gate_workflows, "fast_yosys_tool", dropping):
        found = fast_tool_retention(template, gate_graph("rtl-fast", template)["jobs"])
    assert found == ["yosys-elaboration drops " + SELF_TEST], found
    print("Fast Yosys tool retention refused a derivation that drops a self-test: " + found[0])


def fast_tool_emission(template: dict, generated: dict) -> list[str]:
    """The emitted rtl-fast workflow is exactly what the shared install and runtime transforms make of the
    derivation, except that the tool cache and its one restore carry one bound recipe where the stand-in was.
    No rtl-fast stage after the derivation, the key binding among them, can then drop, add, reorder or rewrite
    a step or a key of any job. Each deviation is refused by name; empty is a pass (#789)."""
    staged = ci_runtime_workflows.generate("rtl-fast", ci_install_workflows.generate(gate_graph("rtl-fast", template)))
    emitted = copy.deepcopy(generated)
    findings, recipes = [], set()
    for job_id, name in ((FAST_TOOL_JOB, YOSYS_BUILD_STEPS[0]), (FAST_TOOL_CONSUMER, TOOL_RESTORE)):
        expected = named_step(staged["jobs"].get(job_id, {"steps": []}), name)
        step = named_step(emitted["jobs"].get(job_id, {"steps": []}), name)
        if expected is None or step is None:
            continue
        stand_in = str(expected.get("with", {}).get("key", ""))
        prefix, _, suffix = stand_in.partition(FAST_TOOL_RECIPE)
        bound = re.fullmatch(re.escape(prefix) + BOUND_RECIPE + re.escape(suffix), str(step.get("with", {}).get("key")))
        if FAST_TOOL_RECIPE not in stand_in or bound is None:
            findings.append("emitted " + job_id + "'s " + name + " key is not its stand-in with one recipe bound")
            continue
        recipes.add(bound.group(1))
        step["with"]["key"] = stand_in
    if len(recipes) > 1:
        findings.append("emitted tool cache and its restore bind different recipes")
    tops = sorted(key for key in {*staged, *emitted} if key != "jobs" and staged.get(key) != emitted.get(key))
    if tops:
        findings.append("emitted workflow keys differ from the transformed derivation's: " + ", ".join(tops))
    if list(emitted["jobs"]) != list(staged["jobs"]):
        findings.append("emitted jobs differ from the transformed derivation's: " + (", ".join(
            [*("adds " + job_id for job_id in emitted["jobs"] if job_id not in staged["jobs"]),
             *("drops " + job_id for job_id in staged["jobs"] if job_id not in emitted["jobs"])]) or "reordered"))
    for job_id, job in staged["jobs"].items():
        if job_id not in emitted["jobs"]:
            continue
        actual = emitted["jobs"][job_id]
        if {key: value for key, value in actual.items() if key != "steps"} != {
                key: value for key, value in job.items() if key != "steps"}:
            findings.append("emitted " + job_id + "'s job keys differ from the transformed derivation's")
        findings.extend(step_findings("emitted " + job_id, job["steps"], actual["steps"], "steps"))
    return findings


def fast_tool_emission_planted(template: dict, generated: dict) -> None:
    """Each step of both emitted jobs dropped in turn, and each other deviation after the derivation, refused
    by name, as is a key binding stage that drops a self-test."""
    def job_steps(jobs: dict, job_id: str) -> list[dict]:
        """One emitted job's steps."""
        return jobs[job_id]["steps"]

    def drop(job_id: str, label: str) -> Callable[[dict], None]:
        """Remove the one emitted step of `job_id` called `label`."""
        return lambda jobs: job_steps(jobs, job_id).remove(named_step(jobs[job_id], label))

    def swap(jobs: dict) -> None:
        """Exchange the two ooc self-tests."""
        steps = job_steps(jobs, FAST_TOOL_CONSUMER)
        first = [step.get("name") for step in steps].index("Prove ooc.sh generates the ROMs and fails on a failed top")
        steps[first], steps[first + 1] = steps[first + 1], steps[first]

    def rebound(jobs: dict) -> None:
        """The restore bound to another recipe digest than the tool cache."""
        key = tool_restore(jobs)["key"]
        tool_restore(jobs)["key"] = re.sub(r"recipe-[0-9a-f]{64}", "recipe-" + "0" * 64, key)

    planted = {"name": "Planted step", "run": "true\n"}
    for label, edit, words in (
            *((job_id + " without " + step["name"], drop(job_id, step["name"]),
               "emitted " + job_id + " drops " + step["name"])
              for job_id in (FAST_TOOL_CONSUMER, FAST_TOOL_JOB) for step in generated["jobs"][job_id]["steps"]),
            ("a self-test body rewritten", lambda jobs: named_step(jobs[FAST_TOOL_CONSUMER], SELF_TEST).update(
                run="true\n"), "emitted yosys-elaboration changes " + SELF_TEST),
            ("the tool build rewritten", lambda jobs: named_step(jobs[FAST_TOOL_JOB], YOSYS_BUILD_STEPS[1]).update(
                run="true\n"), "emitted yosys-tool changes " + YOSYS_BUILD_STEPS[1]),
            ("the tool evidence record rewritten", lambda jobs: named_step(
                jobs[FAST_TOOL_JOB], "Record actual job execution").update(run="touch /opt/yosys/planted\n"),
             "emitted yosys-tool changes Record actual job execution"),
            ("a consumer step added", lambda jobs: job_steps(jobs, FAST_TOOL_CONSUMER).append(copy.deepcopy(planted)),
             "emitted yosys-elaboration adds Planted step"),
            ("a tool step added before the cache save", lambda jobs: job_steps(jobs, FAST_TOOL_JOB).insert(
                -2, copy.deepcopy(planted)), "emitted yosys-tool adds Planted step"),
            ("two self-tests swapped", swap, "emitted yosys-elaboration reorders or repeats its steps"),
            ("a consumer job key added", lambda jobs: jobs[FAST_TOOL_CONSUMER].update({"env": {"X": "1"}}),
             "emitted yosys-elaboration's job keys differ"),
            ("a tool job key added", lambda jobs: jobs[FAST_TOOL_JOB].update({"env": {"CXXFLAGS": "-O0"}}),
             "emitted yosys-tool's job keys differ"),
            ("another job's step dropped", drop("verilator-lint", "Fetch RTL dependencies"),
             "emitted verilator-lint drops Fetch RTL dependencies"),
            ("a job added", lambda jobs: jobs.update({"planted": {"runs-on": "ubuntu-24.04", "steps": [planted]}}),
             "emitted jobs differ from the transformed derivation's: adds planted"),
            ("the stand-in left in the restore", lambda jobs: tool_restore(jobs).update(
                key=re.sub(r"recipe-[0-9a-f]{64}", FAST_TOOL_RECIPE, tool_restore(jobs)["key"])),
             "emitted yosys-elaboration's Restore the pinned Yosys build key is not its stand-in with one recipe"),
            ("the restore bound to another recipe", rebound,
             "emitted tool cache and its restore bind different recipes")):
        changed = copy.deepcopy(generated)
        edit(changed["jobs"])
        found = fast_tool_emission(template, changed)
        assert any(words in finding for finding in found), (label, found)
        print("Fast Yosys tool emission refused " + label + ": " + "; ".join(found))
    flagged = copy.deepcopy(generated)
    flagged["env"]["CXXFLAGS"] = "-O0"
    found = fast_tool_emission(template, flagged)
    assert found == ["emitted workflow keys differ from the transformed derivation's: env"], found
    print("Fast Yosys tool emission refused a workflow env set after the digest: " + found[0])
    # The same judge on the generator itself: a key binding stage that drops a self-test is named.
    bind = ci_gate_workflows.bind_fast_tool_key

    def dropping(workflow: dict) -> None:
        """The real key binding, then one retained self-test removed from yosys-elaboration."""
        bind(workflow)
        drop(FAST_TOOL_CONSUMER, SELF_TEST)(workflow["jobs"])

    with patch.object(ci_gate_workflows, "bind_fast_tool_key", dropping):
        found = fast_tool_emission(template, generate("rtl-fast", template))
    assert found == ["emitted yosys-elaboration drops " + SELF_TEST], found
    print("Fast Yosys tool emission refused a key binding that drops a self-test: " + found[0])


def fast_tool_key_inputs(template: dict, generated: dict) -> None:
    """The key follows every input the emitted tool job feeds its build: the template build step, the
    workflow's and the job's environment, what the transforms after the derivation add to or rewrite in the
    build, the scripts those steps run and the runner image. It ignores what only schedules the tool job or
    lies outside the build (#789)."""
    key = tool_cache(generated["jobs"])["key"]

    def template_with(step_name: str, old: str, new: str) -> dict:
        """The rtl-fast template with one yosys-elaboration step's text replaced."""
        changed = copy.deepcopy(template)
        step = named_step(changed["jobs"][FAST_TOOL_CONSUMER], step_name)
        assert step["run"].count(old) == 1, (step_name, old)
        step["run"] = step["run"].replace(old, new)
        return changed

    def tool_key(changed: dict) -> str:
        """The tool key generated from one template."""
        return tool_cache(generate("rtl-fast", changed)["jobs"])["key"]

    def transformed(module: object, attribute: str, edit: Callable[[dict], None]) -> str:
        """The pristine template's tool key, generated with one transform after the derivation rewritten."""
        original = getattr(module, attribute)

        def rewritten(*args: object) -> dict:
            """The transform's own output, then `edit`."""
            result = original(*args)
            edit(result)
            return result

        with patch.object(module, attribute, rewritten):
            return tool_key(template)

    def build_rewrite(workflow: dict) -> None:
        """A generator-side rewrite of the moved build's compile line."""
        build = named_step(workflow["jobs"][FAST_TOOL_JOB], YOSYS_BUILD_STEPS[1])
        line = '-j"$CI_TOOL_BUILD_JOBS" PREFIX='
        assert build["run"].count(line) == 1
        build["run"] = build["run"].replace(line, '-j"$CI_TOOL_BUILD_JOBS" CXXFLAGS=-O0 PREFIX=')

    def budget_export(step: dict) -> None:
        """One more export from the generated job budget step, which the build inherits."""
        step["run"] = step["run"].replace("} >> \"$GITHUB_ENV\"", "  printf 'CXXFLAGS=%s\\n' -O0\n} >> \"$GITHUB_ENV\"")

    flagged = copy.deepcopy(template)
    flagged["env"]["CXXFLAGS"] = "-O0"
    shelled = copy.deepcopy(template)
    shelled["defaults"] = {"run": {"shell": "bash --noprofile --norc -euo pipefail {0}"}}
    standard = copy.deepcopy(template)
    standard["jobs"][FAST_TOOL_CONSUMER]["env"] = {"CXXSTD": "c++23"}
    scripted =template_with(YOSYS_BUILD_STEPS[1], "make -C /tmp/yosys-src config-gcc",
                             "python3 scripts/ci_scope.py --selftest\nmake -C /tmp/yosys-src config-gcc")
    moved = copy.deepcopy(template)
    moved["jobs"][FAST_TOOL_CONSUMER]["runs-on"] = "ubuntu-22.04"
    missed = []
    for label, changed in (
            ("the template build step", tool_key(template_with(YOSYS_BUILD_STEPS[1], "ENABLE_PLUGINS := 0",
                                                               "ENABLE_PLUGINS := 1"))),
            ("the workflow env", tool_key(flagged)),
            ("the workflow defaults", tool_key(shelled)),
            ("yosys-elaboration's job env", tool_key(standard)),
            ("an install-transform rewrite of the build",
             transformed(ci_install_workflows, "generate", build_rewrite)),
            ("an export added to the job budget step",
             transformed(ci_runtime_workflows, "cpu_budget_step", budget_export)),
            ("a script the build runs", tool_key(scripted)),
            ("the runner image", tool_key(moved))):
        if changed == key:
            missed.append(label)
    assert not missed, "tool key unchanged by an edit of its build inputs: " + ", ".join(missed)
    assert fast_tool_findings(standard, generate("rtl-fast", standard)) == [], "tool job lost the consumer env"
    assert "scripts/ci_scope.py" in key_reads(tool_key(scripted)), "tool key does not bind a script its build runs"
    assert "-ubuntu-22.04-" in tool_key(moved), "tool key does not name its runner image"
    print("Fast Yosys tool key follows the build step, the workflow env and defaults, the job env, the generated"
          " build rewrite and budget exports, the scripts the build runs and the runner image")
    other = template_with("Elaborate the integration-heavy tops", "--top KL_gptp_shadow",
                          "--top KL_gptp_shadow --top KL_pp_shadow")
    assert generate("rtl-fast", other) != generated and tool_key(other) == key, \
        "tool key changed by an edit outside the build recipe"
    scheduled = copy.deepcopy(template)
    scheduled["jobs"][FAST_TOOL_CONSUMER]["if"] = "${{ needs.changes.outputs.rtl == 'true' && !cancelled() }}"
    rescheduled = generate("rtl-fast", scheduled)["jobs"][FAST_TOOL_JOB]
    assert rescheduled["if"] == scheduled["jobs"][FAST_TOOL_CONSUMER]["if"] and tool_key(scheduled) == key, \
        "tool key changed by an edit of what only schedules the tool job"
    print("Fast Yosys tool key unchanged by an edit outside the build recipe or of the tool job's schedule")

    def after_build(workflow: dict) -> None:
        """A step between the build and the cache save, which the key would not bind."""
        steps = workflow["jobs"][FAST_TOOL_JOB]["steps"]
        steps.insert([step.get("name") for step in steps].index(YOSYS_BUILD_STEPS[1]) + 1,
                     {"name": "Touch the built tree", "id": "touch", "run": "touch /opt/yosys/planted\n"})

    try:
        transformed(ci_runtime_workflows, "generate", after_build)
    except ValueError as exc:
        assert "steps after the build that its key does not bind: Touch the built tree" in str(exc), str(exc)
        print("Fast Yosys tool generator refused " + str(exc))
    else:
        raise AssertionError("fast Yosys tool generator accepted a step after the build that its key does not bind")


def fast_tool_template_refusals(template: dict) -> None:
    """A template the derivation cannot read faithfully is refused, never half-derived."""
    def template_steps(changed: dict) -> list[dict]:
        """yosys-elaboration's template steps."""
        return changed["jobs"][FAST_TOOL_CONSUMER]["steps"]

    def unbound_key(changed: dict) -> None:
        """The template key with its workflow-file digest replaced by another."""
        step = named_step(changed["jobs"][FAST_TOOL_CONSUMER], YOSYS_BUILD_STEPS[0])
        step["with"]["key"] = step["with"]["key"].replace(".github/workflows/*.yml", "scripts/*.py")

    def swapped(changed: dict) -> None:
        """The build step ahead of its cache step."""
        steps = template_steps(changed)
        at = [step.get("name") for step in steps].index(YOSYS_BUILD_STEPS[0])
        steps[at], steps[at + 1] = steps[at + 1], steps[at]

    def interposed(changed: dict) -> None:
        """A step between the cache step and its build, which the derivation would move as the build."""
        steps = template_steps(changed)
        at = [step.get("name") for step in steps].index(YOSYS_BUILD_STEPS[0])
        steps.insert(at + 1, {"name": "Interposed step", "run": "true\n"})

    for label, edit, words in (
            ("key without its workflow-file digest", unbound_key, "lacks its one workflow-file digest"),
            ("build step removed", lambda changed: template_steps(changed).remove(
                named_step(changed["jobs"][FAST_TOOL_CONSUMER], YOSYS_BUILD_STEPS[1])),
             "missing or reordered Yosys build recipe"),
            ("build before its cache", swapped, "missing or reordered Yosys build recipe"),
            ("step between the cache and its build", interposed, "missing or reordered Yosys build recipe"),
            ("consumer in a container the tool job would not carry", lambda changed: changed["jobs"][
                FAST_TOOL_CONSUMER].update({"container": {"image": "ubuntu:24.04"}}),
             "job keys the tool job does not carry into the build: container"),
            ("verdict without the elaboration pair", lambda changed: verdict_step(changed["jobs"]).update(
                run=verdict_step(changed["jobs"])["run"].replace(
                    '"yosys-elaboration:$YOSYS_ELABORATION_RESULT" \\\n', "")),
             "verdict lacks its one yosys-elaboration result pair")):
        changed = copy.deepcopy(template)
        edit(changed)
        try:
            generate("rtl-fast", changed)
        except ValueError as exc:
            assert words in str(exc), (label, str(exc))
            print("Fast Yosys tool generator refused a template " + label + ": " + str(exc))
        else:
            raise AssertionError("fast Yosys tool generator accepted a template " + label)


def fast_tool_controls() -> None:
    """rtl-fast's Yosys: built once under a workflow-free key, restored exactly, and judged by the verdict (#789)."""
    template = load_template(ROOT, "rtl-fast")
    generated = generate("rtl-fast", template)
    derived = gate_graph("rtl-fast", template)["jobs"]
    found = (fast_tool_retention(template, derived) + fast_tool_emission(template, generated)
             + fast_tool_findings(template, generated))
    assert found == [], found
    print("Fast Yosys tool: yosys-elaboration keeps every other template step in order, the tool job runs"
          " the checkout and the two moved steps, and the emitted workflow changes only their two keys")
    order = list(template["jobs"])
    at = order.index(FAST_TOOL_CONSUMER)
    assert list(derived) == [*order[:at], FAST_TOOL_JOB, *order[at:]], "tool job not just before its consumer"
    for job_id in order:
        if job_id not in (FAST_TOOL_CONSUMER, FAST_AGGREGATE):
            assert derived[job_id] == template["jobs"][job_id], "the derivation changed " + job_id
    docs_only = {job_id: "skipped" for job_id in order if job_id not in ("changes", FAST_AGGREGATE)}
    assert verdict_exit(generated["jobs"][FAST_AGGREGATE], {**docs_only, FAST_TOOL_JOB: "skipped"}) == 0, \
        "rtl-fast verdict refuses a docs-only run"
    print("Fast Yosys tool: only yosys-elaboration and the verdict change; a docs-only run stays green")
    fast_tool_planted(template, generated)
    fast_tool_retention_planted(template, derived)
    fast_tool_emission_planted(template, generated)
    fast_tool_key_inputs(template, generated)
    fast_tool_template_refusals(template)
    print("Fast Yosys tool: one cached build, an exact restore, a verdict that reads it PASS")
