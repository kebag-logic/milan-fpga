#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""Canonical CI evidence and strict comparison, independent of transport.

Collectors supply observations; this module never invents a successful step.
The compared payload has the seven sections specified in CI_SIGNATURE.md.
An incomplete collection remains useful evidence, but cannot compare equal.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import re
import sys
from typing import Any

SECTIONS = ("subject", "definitions", "environment", "plan", "execution",
            "inventories", "results")
OBSERVATIONS = {"wall_clock", "runner", "cpu_count", "logs", "cache"}
SHA256 = re.compile(r"[0-9a-f]{64}\Z")
SHA1 = re.compile(r"[0-9a-f]{40}\Z")


def canonical(value: Any) -> bytes:
    """Encode UTF-8, sorted keys and integers, refusing ambiguous JSON values."""
    def inspect(item: Any) -> None:
        """Reject floats, non-string keys and non-JSON Python values recursively."""
        if type(item) in (str, int, bool) or item is None:
            return
        if isinstance(item, list):
            for child in item:
                inspect(child)
            return
        if isinstance(item, dict) and all(isinstance(key, str) for key in item):
            for child in item.values():
                inspect(child)
            return
        raise ValueError("canonical JSON permits no floats or non-JSON values")

    inspect(value)
    return json.dumps(value, sort_keys=True, ensure_ascii=False,
                      separators=(",", ":"), allow_nan=False).encode("utf-8")


def unique_object(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    """A duplicate JSON key is evidence ambiguity, never last-value-wins."""
    result: dict[str, Any] = {}
    for key, value in pairs:
        if key in result:
            raise ValueError(f"duplicate JSON key: {key}")
        result[key] = value
    return result


def read(path: Path) -> dict[str, Any]:
    """Read strict JSON, including duplicate-key and non-finite-value refusal."""
    value = json.loads(path.read_text(encoding="utf-8"), object_pairs_hook=unique_object)
    canonical(value)
    if not isinstance(value, dict):
        raise ValueError("manifest must be an object")
    return value


def exact_keys(value: Any, keys: set[str], where: str) -> None:
    """Refuse both missing fields and undocumented extensions."""
    if not isinstance(value, dict) or set(value) != keys:
        raise ValueError(f"{where}: expected exactly {sorted(keys)}")


def require_digest(value: Any, pattern: re.Pattern[str], where: str) -> None:
    """An absent or malformed digest cannot bind an input."""
    if not isinstance(value, str) or pattern.fullmatch(value) is None:
        raise ValueError(f"{where}: invalid digest")


def subject_errors(subject: dict[str, Any]) -> None:
    """Require exact source identity and the event's own ancestry fields."""
    keys = {"repository", "head", "tree", "event"}
    if subject.get("event") == "pull_request":
        keys |= {"base", "merge_base"}
    elif subject.get("event") != "push":
        raise ValueError("subject.event: expected push or pull_request")
    exact_keys(subject, keys, "subject")
    if not isinstance(subject["repository"], str) or subject["repository"].count("/") != 1:
        raise ValueError("subject.repository: expected owner/repository")
    for key in keys - {"repository", "event"}:
        require_digest(subject[key], SHA1, "subject." + key)


def completion_errors(payload: dict[str, Any]) -> list[str]:
    """Name missing runtime evidence without substituting planned success."""
    errors: list[str] = []
    plan = payload["plan"]
    execution = payload["execution"]
    results = payload["results"]
    if not plan or not isinstance(plan, dict):
        raise ValueError("plan: expected a nonempty resolved job map")
    if not isinstance(execution, dict) or not isinstance(results, dict):
        raise ValueError("execution and results must be job maps")
    if set(execution) != set(plan):
        errors.append("execution: missing or extra job/leg")
    if set(results) != set(plan):
        errors.append("results: missing or extra job/leg")
    for job, definition in plan.items():
        exact_keys(definition, {"workflow", "job", "matrix", "needs", "condition", "steps"},
                   "plan." + job)
        steps = definition["steps"]
        if not isinstance(steps, list) or not steps:
            raise ValueError(f"plan.{job}.steps: expected nonempty list")
        actual = execution.get(job, [])
        if not isinstance(actual, list) or len(actual) != len(steps):
            errors.append(f"execution.{job}: missing or extra step")
            continue
        for index, (step, observed) in enumerate(zip(steps, actual)):
            where = f"{job}.steps[{index}]"
            exact_keys(step, {"name", "kind", "sha256", "condition"}, "plan." + where)
            require_digest(step["sha256"], SHA256, "plan." + where)
            if step["kind"] not in ("run", "uses"):
                raise ValueError(f"plan.{where}: invalid step kind")
            exact_keys(observed, {"name", "outcome", "skip_reason"}, "execution." + where)
            if observed["name"] != step["name"]:
                errors.append(f"execution.{where}: step name differs")
            # Conditional skips need a collector's evaluated condition receipt.
            # Until that receipt is validated, a skip cannot make a valid build.
            if observed["outcome"] != "success" or observed["skip_reason"] is not None:
                errors.append(f"execution.{where}: step did not succeed")
        if results.get(job) != "success":
            errors.append(f"results.{job}: job/leg did not succeed")
    expected_unions = {entry["job"].removeprefix("union-") for entry in plan.values()
                       if entry["job"].startswith("union-")}
    expected_unions.update("gate/" + name for name in ("docs", "elaborate")
                           if any(entry["job"] == name + "-gates-0" for entry in plan.values()))
    for missing in sorted(expected_unions - set(payload["inventories"])):
        errors.append("inventories." + missing + ": missing executed union")
    for suite, inventory in payload["inventories"].items():
        exact_keys(inventory, {"expected", "legs", "union", "verdicts_sha256"},
                   "inventories." + suite)
        expected = inventory["expected"]
        legs = inventory["legs"]
        if (not isinstance(expected, list) or not expected
                or any(not isinstance(case, str) or not case for case in expected)
                or len(expected) != len(set(expected)) or not isinstance(legs, dict)):
            raise ValueError(f"inventories.{suite}: invalid case inventory")
        if any(not isinstance(cases, list) for cases in legs.values()):
            raise ValueError(f"inventories.{suite}: invalid leg inventory")
        executed = [case for cases in legs.values() for case in cases]
        if (inventory["union"] != "success" or sorted(expected) != sorted(executed)
                or len(executed) != len(set(executed))):
            errors.append(f"inventories.{suite}: union does not prove exactly-once execution")
        require_digest(inventory["verdicts_sha256"], SHA256, "inventories." + suite)
    return errors


def envelope(payload: dict[str, Any], observations: dict[str, Any]) -> dict[str, Any]:
    """Produce evidence, explicitly incomplete whenever a required result is absent."""
    exact_keys(payload, set(SECTIONS), "payload")
    canonical(payload)
    subject_errors(payload["subject"])
    for key in ("definitions", "environment", "inventories"):
        if not isinstance(payload[key], dict):
            raise ValueError(key + ": expected object")
    if not payload["definitions"]:
        raise ValueError("definitions: no workflow digests")
    for path, digest in payload["definitions"].items():
        if not path.startswith(".github/workflows/") or not path.endswith(".yml"):
            raise ValueError("definitions: unexpected workflow path")
        require_digest(digest, SHA256, "definitions." + path)
    exact_keys(payload["environment"], {"image", "tools", "actions"}, "environment")
    tools = payload["environment"]["tools"]
    if not isinstance(tools, dict) or not isinstance(payload["environment"]["actions"], list):
        raise ValueError("environment: tools must be a map and actions a list")
    missing_provenance = []
    for name, tool in tools.items():
        exact_keys(tool, {"version", "source_sha256", "recipe_sha256", "binary_sha256"},
                   "environment.tools." + name)
        if not isinstance(tool["version"], str) or not tool["version"]:
            raise ValueError("environment.tools." + name + ": version missing")
        for field in ("source_sha256", "recipe_sha256", "binary_sha256"):
            if tool[field] is None:
                missing_provenance.append("environment.tools." + name + "." + field + ": unmeasured")
            else:
                require_digest(tool[field], SHA256, "environment.tools." + name + "." + field)
    if set(observations) - OBSERVATIONS:
        raise ValueError("observations: unknown excluded field")
    problems = completion_errors(payload) + missing_provenance
    image = payload["environment"]["image"]
    if not isinstance(image, str) or re.fullmatch(r"[^\s]+@sha256:[0-9a-f]{64}", image) is None:
        problems.append("environment.image: no immutable image digest")
    for action in payload["environment"]["actions"]:
        if not isinstance(action, str) or re.fullmatch(r"[^\s]+@[0-9a-f]{40}", action) is None:
            problems.append("environment.actions: action is not pinned by commit")
    if not payload["environment"]["tools"]:
        problems.append("environment.tools: no measured tool inventory")
    return {"schema": 1, "payload": payload, "sha256": hashlib.sha256(canonical(payload)).hexdigest(),
            "complete": not problems, "incomplete_reasons": problems, "observations": observations}


def validate(document: dict[str, Any]) -> None:
    """Recompute the digest and completeness; never trust either recorded claim."""
    exact_keys(document, {"schema", "payload", "sha256", "complete", "incomplete_reasons",
                          "observations"}, "manifest")
    if type(document["schema"]) is not int or document["schema"] != 1:
        raise ValueError("manifest.schema: unsupported version")
    expected = envelope(document["payload"], document["observations"])
    if canonical(expected) != canonical(document):
        raise ValueError("manifest: inconsistent digest, completeness or schema")
    if not document["complete"]:
        raise ValueError("incomplete manifest: " + "; ".join(document["incomplete_reasons"]))


def differences(left: Any, right: Any, path: str = "payload") -> list[str]:
    """Name every differing field, retaining list ordering and JSON type identity."""
    if type(left) is not type(right):
        return [path + ": type differs"]
    if isinstance(left, dict):
        result = [path + "." + key + ": missing or extra field" for key in sorted(set(left) ^ set(right))]
        for key in sorted(set(left) & set(right)):
            result.extend(differences(left[key], right[key], path + "." + key))
        return result
    if isinstance(left, list):
        result = [] if len(left) == len(right) else [path + ": length differs"]
        for index, (a, b) in enumerate(zip(left, right)):
            result.extend(differences(a, b, f"{path}[{index}]"))
        return result
    return [] if left == right else [path + ": value differs"]


def compare(left: dict[str, Any], right: dict[str, Any]) -> list[str]:
    """Compare complete collections; this does not authenticate their collectors."""
    validate(left)
    validate(right)
    return differences(left["payload"], right["payload"])


def main() -> int:
    """Package collector input or compare two independently collected manifests."""
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest="command", required=True)
    emit = commands.add_parser("emit")
    emit.add_argument("payload", type=Path)
    emit.add_argument("output", type=Path)
    emit.add_argument("--observations", type=Path)
    check = commands.add_parser("compare")
    check.add_argument("local", type=Path)
    check.add_argument("github", type=Path)
    check.add_argument("--root", type=Path, default=Path.cwd())
    args = parser.parse_args()
    try:
        if args.command == "emit":
            result = envelope(read(args.payload), read(args.observations) if args.observations else {})
            with args.output.open("xb") as stream:
                stream.write(canonical(result) + b"\n")
            print("complete" if result["complete"] else "incomplete")
            return 0 if result["complete"] else 1
        from ci_workflow_plan import verify_bound_plan
        left, right = read(args.local), read(args.github)
        verify_bound_plan(args.root, left["payload"])
        verify_bound_plan(args.root, right["payload"])
        changed = compare(left, right)
        print("\n".join(changed) if changed else "equal")
        return int(bool(changed))
    except (OSError, ValueError, TypeError, KeyError) as error:
        print(f"manifest refused: {error}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
