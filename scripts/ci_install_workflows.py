#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""Add exact download caches around existing installation commands only."""

import copy
import hashlib
import re
import shlex

RECIPE = "${{ hashFiles('scripts/ci_install*.py', '.github/workflows/*.yml') }}"
SV2V_SHA = "ff8c9eea5bc029b372fb4953427625cddb7cf7e58c1240623ac9f260818d5a00"


def cache(name: str, path: str, key: str, condition: str | None = None) -> dict:
    """Never restore an installation from a broader fallback key."""
    step = {"name": name, "uses": "actions/cache@v4", "with": {"path": path, "key": key}}
    if condition is not None:
        step["if"] = condition
    return step


def apt_packages(body: str) -> list[str]:
    """Read literal package arguments without evaluating any shell expression."""
    joined = body.replace("\\\n", " ")
    rows = re.findall(r"sudo apt-get install ([^\n]+)", joined)
    return sorted({word for row in rows for word in shlex.split(row) if not word.startswith("-")})


def package_steps(step: dict, index: int) -> list[dict]:
    """Prepare a version/source key before each existing distribution install."""
    body = step.get("run", "")
    packages = apt_packages(body)
    if not packages:
        return [step]
    # A guarded fallback inside a test remains byte-for-byte part of that test.
    if not step.get("name", "").startswith(("Install ", "Build ")):
        return [step]
    token = "ci_packages_" + str(index)
    directory = "$RUNNER_TEMP/" + token
    recipe = hashlib.sha256(body.encode()).hexdigest()
    prepare = {"name": "Resolve exact package downloads " + str(index), "id": token,
               "run": "python3 scripts/ci_install_cache.py --packages " + " ".join(packages)
                      + " --recipe " + recipe + ' --directory "' + directory + '" --output "$GITHUB_OUTPUT"\n'}
    condition = step.get("if")
    if condition is not None:
        prepare["if"] = condition
    retained = copy.deepcopy(step)
    retained["run"] = body.replace("sudo apt-get update -qq", ": # package index prepared above").replace(
        "sudo apt-get install", 'sudo apt-get -o Dir::Cache::archives="' + directory + '" install')
    return [prepare, cache("Cache exact package downloads " + str(index),
                           "${{ runner.temp }}/" + token,
                           "${{ runner.os }}-${{ steps." + token + ".outputs.key }}-" + RECIPE, condition), retained]


def archive_steps(step: dict) -> list[dict]:
    """Cache verified release archives and the pinned oracle's incremental build."""
    body = step.get("run", "")
    condition = step.get("if")
    if "curl -fsSL \"$url\" -o /tmp/sv2v.zip" in body:
        retained = copy.deepcopy(step)
        retained["run"] = body.replace(
            'curl -fsSL "$url" -o /tmp/sv2v.zip',
            'mkdir -p "$RUNNER_TEMP/ci-sv2v-cache"\n'
            'archive="$RUNNER_TEMP/ci-sv2v-cache/sv2v.zip"\n'
            'if [ ! -f "$archive" ]; then curl -fsSL "$url" -o "$archive"; fi').replace(
                '/tmp/sv2v.zip', '$archive').replace('unzip -q -o $archive', 'unzip -q -o "$archive"')
        return [cache("Cache verified sv2v archive", "${{ runner.temp }}/ci-sv2v-cache",
                      "sv2v-v0.0.12-" + SV2V_SHA + "-" + RECIPE + "-${{ runner.os }}", condition), retained]
    if step.get("name") == "Build the pinned tsn-gen field oracle on its suite owner":
        retained = copy.deepcopy(step)
        old = ('git clone --filter=blob:none \\\n'
               '  https://github.com/kebag-logic/tsn-gen.git "$RUNNER_TEMP/tsn-gen"')
        if old not in body:
            raise ValueError("oracle clone recipe changed")
        retained["run"] = body.replace(old, 'if [ ! -d "$RUNNER_TEMP/tsn-gen/.git" ]; then\n' + old + '\nfi')
        return [cache("Cache pinned field oracle build", "${{ runner.temp }}/tsn-gen",
                      "tsn-gen-${{ env.TSN_GEN_REV }}-" + RECIPE + "-${{ runner.os }}", condition), retained]
    return [step]


def generate(source: dict) -> dict:
    """Keep test steps intact while binding every added cache to installation inputs."""
    source = copy.deepcopy(source)
    for job in source["jobs"].values():
        original = job["steps"]
        pip = any("pip install" in step.get("run", "") for step in original)
        result = []
        for index, step in enumerate(original):
            for prepared in package_steps(step, index):
                result.extend(archive_steps(prepared))
            if index == 0 and pip:
                result.append(cache("Cache exact Python downloads", "~/.cache/pip",
                                    "python-cpython3.12.3-${{ hashFiles('ci/constraints-ci.txt', "
                                    "'tools/*/requirements.txt', 'sw/litex/litex_pins.txt') }}-"
                                    + RECIPE + "-${{ runner.os }}"))
        if pip:
            job.setdefault("env", {})["PIP_CONSTRAINT"] = "${{ github.workspace }}/ci/constraints-ci.txt"
        job["steps"] = result
    return source
