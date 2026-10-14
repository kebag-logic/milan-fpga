#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""Recompute a CI job and step inventory from committed workflow bytes.

Only literal matrix axes are supported. Dynamic matrices, aliases, duplicate
keys and unknown dependencies refuse planning instead of losing execution.
This module reads data; it never runs a repository step on the collecting host.
"""

from __future__ import annotations

import argparse
import hashlib
import itertools
from pathlib import Path
import re
import subprocess

import yaml

from ci_manifest import canonical, read

SHA = re.compile(r"[0-9a-f]{40}\Z")
MATRIX_REFERENCE = re.compile(r"\$\{\{\s*matrix\.([A-Za-z_][A-Za-z0-9_-]*)\s*\}\}")


class WorkflowLoader(yaml.SafeLoader):
    """Reject duplicate mapping keys; YAML aliases are rejected before loading."""

    def construct_mapping(self, node: yaml.MappingNode, deep: bool = False) -> dict:
        """Retain each mapping entry once, without last-writer ambiguity."""
        result = {}
        for key_node, value_node in node.value:
            key = self.construct_object(key_node, deep=deep)
            if not isinstance(key, str) or key in result:
                raise ValueError("workflow mapping keys must be unique strings")
            result[key] = self.construct_object(value_node, deep=deep)
        return result


# YAML 1.1 calls the workflow's `on` key a boolean. Keep booleans as text;
# matrix coordinates then retain their declared spelling on both collectors.
WorkflowLoader.yaml_implicit_resolvers = {
    first: [(tag, regex) for tag, regex in resolvers if tag != "tag:yaml.org,2002:bool"]
    for first, resolvers in yaml.SafeLoader.yaml_implicit_resolvers.items()
}


def workflow(text: str) -> dict:
    """Parse bounded workflow data without aliases or executable tags."""
    if len(text.encode()) > 1024 * 1024:
        raise ValueError("workflow exceeds one MiB")
    for token in yaml.scan(text):
        if isinstance(token, (yaml.tokens.AnchorToken, yaml.tokens.AliasToken)):
            raise ValueError("workflow anchors and aliases are unsupported")
    value = yaml.load(text, Loader=WorkflowLoader)
    if not isinstance(value, dict) or not isinstance(value.get("jobs"), dict) or not value["jobs"]:
        raise ValueError("workflow needs a nonempty jobs mapping")
    return value


def matrix_rows(job: dict) -> list[dict]:
    """Expand literal axes in source order, rejecting unmodelled matrix forms."""
    strategy = job.get("strategy", {})
    if not isinstance(strategy, dict):
        raise ValueError("strategy must be a mapping")
    matrix = strategy.get("matrix", {})
    if not isinstance(matrix, dict) or any(key in matrix for key in ("include", "exclude")):
        raise ValueError("only literal matrix axes are supported")
    for key, values in matrix.items():
        if (not isinstance(values, list) or not values
                or any(type(value) not in (str, int) for value in values)
                or any(isinstance(value, str) and "${{" in value for value in values)
                or len({canonical(value) for value in values}) != len(values)):
            raise ValueError(f"matrix.{key}: expected unique literal coordinates")
    size = 1
    for values in matrix.values():
        size *= len(values)
    if size > 256:
        raise ValueError("matrix expands beyond 256 legs")
    return [dict(zip(matrix, values)) for values in itertools.product(*matrix.values())]


def rendered_name(job_id: str, job: dict, matrix: dict) -> str:
    """Match the hosted display name using only declared matrix substitutions."""
    name = job.get("name")
    if name is None:
        suffix = " (" + ", ".join(map(str, matrix.values())) + ")" if matrix else ""
        return job_id + suffix
    if not isinstance(name, str) or not name:
        raise ValueError("job name must be nonempty text")
    def replace(match: re.Match[str]) -> str:
        """A missing matrix name is an invalid display identity."""
        key = match.group(1)
        if key not in matrix:
            raise ValueError(f"job name references absent matrix.{key}")
        return str(matrix[key])
    rendered = MATRIX_REFERENCE.sub(replace, name)
    if "${{" in rendered:
        raise ValueError("job name has an unsupported expression")
    return rendered


def step_plan(step: dict) -> dict:
    """Bind the exact body or action reference, with its execution condition."""
    if not isinstance(step, dict) or ("run" in step) == ("uses" in step):
        raise ValueError("step must have exactly one run or uses body")
    kind = "run" if "run" in step else "uses"
    body = step[kind]
    if not isinstance(body, str) or not body.strip():
        raise ValueError("step body must be nonempty text")
    name = step.get("name", "Run " + body.splitlines()[0])
    condition = step.get("if", "success()")
    if not isinstance(name, str) or not name or not isinstance(condition, str):
        raise ValueError("step name and condition must be text")
    return {"name": name, "kind": kind, "sha256": hashlib.sha256(body.encode()).hexdigest(),
            "condition": condition}


def needs(job: dict) -> list[str]:
    """Read dependency identifiers without silently accepting expressions."""
    value = job.get("needs", [])
    values = [value] if isinstance(value, str) else value
    if (not isinstance(values, list)
            or any(not isinstance(item, str) or not item or "${{" in item for item in values)
            or len(set(values)) != len(values)):
        raise ValueError("needs must name distinct literal jobs")
    return values


def expand_workflow(path: str, text: str) -> tuple[dict, dict]:
    """Return expanded plan entries and independently reproducible API names."""
    jobs = workflow(text)["jobs"]
    plan, labels, coordinates = {}, {}, {}
    for job_id, job in jobs.items():
        if not isinstance(job, dict) or not isinstance(job.get("steps"), list) or not job["steps"]:
            raise ValueError(f"{job_id}: expected executable steps")
        if set(needs(job)) - set(jobs):
            raise ValueError(f"{job_id}: missing dependency")
        coordinates[job_id] = []
        for matrix in matrix_rows(job):
            suffix = "[" + canonical(matrix).decode() + "]" if matrix else ""
            key = path + ":" + job_id + suffix
            label = rendered_name(job_id, job, matrix)
            if label in labels.values():
                raise ValueError(f"{path}: duplicate job display name {label}")
            labels[key] = label
            coordinates[job_id].append(key)
            condition = job.get("if", "success()")
            if not isinstance(condition, str):
                raise ValueError(f"{job_id}: condition must be text")
            plan[key] = {"workflow": path, "job": job_id, "matrix": matrix,
                         "needs": needs(job), "condition": condition,
                         "steps": [step_plan(step) for step in job["steps"]]}
    for key, entry in plan.items():
        entry["needs"] = [leg for job in entry["needs"] for leg in coordinates[job]]
    visited, visiting = set(), set()
    def visit(key: str) -> None:
        """A cyclic plan has no valid execution ordering."""
        if key in visiting:
            raise ValueError("cyclic workflow dependencies")
        if key in visited:
            return
        visiting.add(key)
        for dependency in plan[key]["needs"]:
            visit(dependency)
        visiting.remove(key)
        visited.add(key)
    for key in plan:
        visit(key)
    return plan, labels


def committed_plan(root: Path, head: str) -> dict:
    """Read exact Git blobs, so dirty working files cannot redefine the plan."""
    if not SHA.fullmatch(head):
        raise ValueError("head must be a full commit object ID")
    def git(*args: str) -> bytes:
        """Read source objects without replacement refs or repository hooks."""
        return subprocess.check_output(["git", "--no-replace-objects", "-C", str(root), *args])
    if git("rev-parse", head + "^{commit}").decode().strip() != head:
        raise ValueError("head does not name a commit")
    names = git("ls-tree", "-r", "--name-only", "-z", head, ".github/workflows").split(b"\0")
    paths = sorted(name.decode() for name in names if name.endswith((b".yml", b".yaml")))
    if not paths:
        raise ValueError("head has no workflow definitions")
    definitions, plan, labels = {}, {}, {}
    for path in paths:
        raw = git("show", head + ":" + path)
        definitions[path] = hashlib.sha256(raw).hexdigest()
        entries, names = expand_workflow(path, raw.decode("utf-8"))
        plan.update(entries)
        labels.update(names)
    return {"head": head, "tree": git("rev-parse", head + "^{tree}").decode().strip(),
            "definitions": definitions, "plan": plan, "labels": labels}


def verify_bound_plan(root: Path, payload: dict) -> dict:
    """Refuse self-consistent evidence whose source plan was omitted or edited."""
    source = committed_plan(root, payload["subject"]["head"])
    if payload["subject"]["tree"] != source["tree"]:
        raise ValueError("subject tree differs from committed head")
    for key in ("definitions", "plan"):
        if canonical(payload[key]) != canonical(source[key]):
            raise ValueError(key + " differs from committed workflow inputs")
    return source


def main() -> int:
    """Print the source-derived planning artifact; no runtime success is implied."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path.cwd())
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--head")
    mode.add_argument("--manifest", type=Path)
    args = parser.parse_args()
    try:
        if args.manifest:
            verify_bound_plan(args.root, read(args.manifest)["payload"])
            print("manifest plan matches committed workflow inputs")
        else:
            print(canonical(committed_plan(args.root, args.head)).decode())
    except (OSError, ValueError, KeyError, TypeError, yaml.YAMLError, subprocess.CalledProcessError) as exc:
        print(f"workflow plan refused: {exc}")
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
