#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""Materialize workflow matrices so one scheduler limit bounds all job containers.

The source matrix remains the inventory. Its Cartesian product becomes concrete
jobs with identical commands and bindings. The original job ID becomes a strict
status carrier, retaining dependencies used by the protected aggregate.
"""

from __future__ import annotations

import copy
import itertools
import json
import re


def literal(value: object) -> str:
    """Render a scalar as a workflow expression literal, with no expression injection."""
    if type(value) is int:
        return str(value)
    if type(value) is bool:
        return str(value).lower()
    if isinstance(value, str) and "${{" not in value:
        return "'" + value.replace("'", "''") + "'"
    raise ValueError("matrix values must be literal strings, integers or booleans")


def substitute(value: object, coordinates: dict) -> object:
    """Resolve matrix references while preserving every other expression and command byte."""
    if isinstance(value, list):
        return [substitute(child, coordinates) for child in value]
    if isinstance(value, dict):
        return {key: substitute(child, coordinates) for key, child in value.items()}
    if not isinstance(value, str):
        return value
    result = value
    for key, coordinate in coordinates.items():
        direct = r"\$\{\{\s*matrix\." + re.escape(key) + r"\s*\}\}"
        text = str(coordinate).lower() if type(coordinate) is bool else str(coordinate)
        result = re.sub(direct, lambda _match: text, result)
    def expression(match: re.Match[str]) -> str:
        """Only replace a matrix token inside an expression, never ordinary shell text."""
        body = match.group()
        for key, coordinate in coordinates.items():
            body = re.sub(r"\bmatrix\." + re.escape(key) + r"\b",
                          lambda _token: literal(coordinate), body)
        if re.search(r"\bmatrix\b", body):
            raise ValueError("unresolved or unsupported matrix expression: " + body)
        return body
    return re.sub(r"\$\{\{.*?\}\}", expression, result, flags=re.DOTALL)


def coordinates(strategy: dict) -> list[dict]:
    """Expand the finite source axes; ambiguous exclusions and empty legs are refused."""
    if set(strategy) - {"matrix", "fail-fast", "max-parallel"}:
        raise ValueError("unsupported strategy field")
    axes = strategy.get("matrix")
    if not isinstance(axes, dict) or not axes or {"include", "exclude"}.intersection(axes):
        raise ValueError("matrix must have literal axes without include or exclude")
    count = 1
    for key, values in axes.items():
        if not re.fullmatch(r"[A-Za-z_][A-Za-z0-9_]*", key):
            raise ValueError("invalid matrix axis")
        if not isinstance(values, list) or not values:
            raise ValueError("matrix axes must be nonempty lists")
        rendered = [literal(value) for value in values]
        if len(set(rendered)) != len(rendered):
            raise ValueError("duplicate matrix coordinate")
        count *= len(values)
    if count > 256:
        raise ValueError("matrix exceeds the bounded job inventory")
    return [dict(zip(axes, values)) for values in itertools.product(*axes.values())]


def carrier(job_id: str, source: dict, children: list[str]) -> dict:
    """Require every concrete job successful, including missing and skipped job refusals."""
    original_needs = source.get("needs", [])
    if isinstance(original_needs, str):
        original_needs = [original_needs]
    needs = original_needs + children
    condition = source.get("if", "success()")
    condition = condition.removeprefix("${{").removesuffix("}}").strip()
    return {"name": job_id, "runs-on": "ubuntu-latest", "timeout-minutes": 1,
            "needs": needs, "if": "${{ always() && (" + condition + ") }}",
            "steps": [{"name": "Require every matrix leg successful",
                       "env": {"CI_MATRIX_NEEDS": "${{ toJSON(needs) }}",
                               "CI_MATRIX_EXPECTED": json.dumps(needs, separators=(",", ":"))},
                       "run": "\n".join((
                           "python3 - <<'PY'", "import json, os",
                           "actual = json.loads(os.environ['CI_MATRIX_NEEDS'])",
                           "expected = json.loads(os.environ['CI_MATRIX_EXPECTED'])",
                           "if set(actual) != set(expected):",
                           "    raise SystemExit('missing or extra matrix dependency')",
                           "for job in expected:",
                           "    if actual[job].get('result') != 'success':",
                           "        raise SystemExit(job + ': failed, cancelled or skipped')",
                           "print('every matrix leg succeeded')", "PY", ""))}]}


def expand(source: dict) -> dict:
    """Generate concrete jobs and carriers without dropping or duplicating a source leg."""
    result = copy.deepcopy(source)
    jobs = {}
    for job_id, job in source["jobs"].items():
        if "strategy" not in job:
            if job_id in jobs:
                raise ValueError("generated job ID collision")
            jobs[job_id] = copy.deepcopy(job)
            continue
        if job["strategy"].get("fail-fast") is not True:
            raise ValueError(job_id + ": every source matrix must fail fast")
        if "outputs" in job:
            raise ValueError("matrix outputs need an explicit aggregation contract")
        children = []
        for index, values in enumerate(coordinates(job["strategy"])):
            child_id = job_id + "-" + str(index)
            if child_id in source["jobs"] or child_id in jobs:
                raise ValueError("generated job ID collision")
            child = substitute(copy.deepcopy(job), values)
            del child["strategy"]
            child["name"] = substitute(job.get("name", job_id + " " + str(index)), values)
            jobs[child_id] = child
            children.append(child_id)
        jobs[job_id] = carrier(job_id, job, children)
    result["jobs"] = jobs
    return result
