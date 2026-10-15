#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""Read source objects and scheduler telemetry using independently pinned code.

The trusted runner validates this file and its two helpers before starting it
with an isolated interpreter and a private bytecode-cache directory. No candidate
Python module is imported and no candidate command is executed on the host.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import zipfile

import yaml


def artifact_rows(root: Path, filename: str, cancelled: bool = False) -> list[dict]:
    """Read bounded JSON members without extracting candidate archives to the host."""
    rows = []
    paths = sorted(root.rglob("*.zip"))
    if len(paths) > 256:
        raise ValueError("artifact archive count exceeds its bound")
    for path in paths:
        if path.is_symlink() or not path.is_file() or path.stat().st_size > 1024**3:
            raise ValueError("artifact archive is not a regular file")
        try:
            archive = zipfile.ZipFile(path)
        except zipfile.BadZipFile:
            if not cancelled:
                raise
            print("Interrupted upload has no completed evidence:", path.name)
            continue
        with archive:
            if len(archive.infolist()) > 4096:
                raise ValueError("artifact member inventory exceeds its bound")
            for member in archive.infolist():
                if Path(member.filename).name != filename:
                    continue
                if member.file_size > 2 * 1024 * 1024:
                    raise ValueError("runtime JSON artifact exceeds its bound")
                rows.append(json.loads(archive.read(member)))
    return rows


def observations(source: dict, definitions: dict, events: list[dict], failed: bool) -> tuple[dict, dict]:
    """Map only actual top-level Main events; never infer a successful missing step."""
    execution, results, seen = {}, {}, set()
    for key, entry in source["plan"].items():
        execution[key] = [{"name": step["name"], "outcome": "unknown", "skip_reason": None}
                          for step in entry["steps"]]
    for event in events:
        candidates = [key for key, entry in source["plan"].items()
                      if entry["job"] == event.get("jobID") and entry["matrix"] == (event.get("matrix") or {})
                      and event.get("job", "").startswith(definitions[entry["workflow"]]["name"] + "/")]
        if len(candidates) != 1:
            raise ValueError("scheduler event has ambiguous or unplanned job identity")
        key = candidates[0]
        seen.add(key)
        if "jobResult" in event:
            if key in results:
                raise ValueError("duplicate scheduler job conclusion")
            results[key] = event["jobResult"]
        if "stepResult" not in event or event.get("stage") != "Main":
            continue
        step_ids = event.get("stepID", [])
        if not isinstance(step_ids, list) or len(step_ids) != 1:
            continue
        entry = source["plan"][key]
        steps = definitions[entry["workflow"]]["jobs"][entry["job"]]["steps"]
        matches = [index for index, step in enumerate(steps)
                   if str(step.get("id", index)) == step_ids[0]]
        if len(matches) != 1:
            raise ValueError("scheduler event has an unplanned step ID")
        index = matches[0]
        observed = execution[key][index]
        if observed["outcome"] != "unknown":
            raise ValueError("duplicate scheduler step conclusion")
        outcome = event["stepResult"]
        observed.update(outcome=outcome, skip_reason=entry["steps"][index]["condition"]
                        if outcome == "skipped" else None)
    for key in source["plan"]:
        if key not in results:
            results[key] = "cancelled" if failed and key in seen else "not_run"
    return execution, results


def collect(root: Path, subject: dict, events: Path, artifacts: Path, failed: bool) -> dict:
    """Build the same canonical envelope from source data and scheduler observations."""
    from ci_manifest import canonical, envelope
    from ci_workflow_plan import committed_plan, workflow
    source = committed_plan(root, subject["head"])
    if subject["tree"] != source["tree"]:
        raise ValueError("local subject tree differs from source commit")
    definitions = {path: workflow(subprocess.check_output(
        ["git", "--no-replace-objects", "-C", str(root), "show", subject["head"] + ":" + path], text=True))
        for path in source["definitions"]}
    rows = [json.loads(line) for line in events.read_text().splitlines()] if events.exists() else []
    execution, results = observations(source, definitions, rows, failed)
    tools, inventories = {}, {}
    for receipt in artifact_rows(artifacts, "job-evidence.json", failed):
        if (receipt["head"], receipt["tree"]) != (subject["head"], subject["tree"]):
            raise ValueError("local tool receipt source differs")
        matrix = receipt["matrix"]
        key = receipt["workflow"] + ":" + receipt["job"]
        if matrix:
            key += "[" + canonical(matrix).decode() + "]"
        if key not in source["plan"]:
            raise ValueError("tool receipt names an unplanned job")
        for name, value in receipt["tools"].items():
            if key + "/" + name in tools:
                raise ValueError("duplicate measured tool receipt")
            tools[key + "/" + name] = value
    for receipt in [*artifact_rows(artifacts, "union.json", failed),
                    *artifact_rows(artifacts, "gate-union.json", failed)]:
        suite = receipt["suite"]
        if suite in inventories or (receipt["head"], receipt["tree"]) != (subject["head"], subject["tree"]):
            raise ValueError("duplicate or different-source executed union")
        inventories[suite] = {"expected": receipt["inventory"],
                              "legs": {row["shard"]: row["cases"] for row in receipt["legs"]},
                              "union": "success" if receipt["union"] == "pass" else "failure",
                              "verdicts_sha256": receipt["verdicts_sha256"]}
    actions = sorted({step["uses"] for document in definitions.values()
                      for job in document["jobs"].values() for step in job["steps"] if "uses" in step})
    payload = {"subject": subject, "definitions": source["definitions"], "plan": source["plan"],
               "environment": {"image": None, "tools": tools, "actions": actions},
               "execution": execution, "results": results, "inventories": inventories}
    first = next((row["job"] for row in rows if row.get("jobResult") == "failure"), None)
    return envelope(payload, {"logs": {"first_failure": first}})


def main() -> int:
    """Load only pinned helper bytes, then read candidate objects as data."""
    parser = argparse.ArgumentParser(description=__doc__)
    for name in ("root", "subject", "events", "artifacts", "output", "pins"):
        parser.add_argument("--" + name, type=Path, required=True)
    parser.add_argument("--failed", action="store_true")
    args = parser.parse_args()
    directory = Path(__file__).resolve().parent
    pins = json.loads(args.pins.read_text())
    if set(pins) != {"ci_manifest.py", "ci_workflow_plan.py", "ci_local_manifest.py"}:
        raise ValueError("collector helper pin inventory differs")
    for name, digest in pins.items():
        path = directory / name
        if path.is_symlink() or hashlib.sha256(path.read_bytes()).hexdigest() != digest:
            raise ValueError("collector helper digest differs: " + name)
    # Standard library and YAML imports above have already resolved under -I.
    # The caller supplies a fresh -X pycache_prefix, so imports read these bytes.
    sys.path.insert(0, str(directory))
    from ci_manifest import canonical
    result = collect(args.root, json.loads(args.subject.read_text()), args.events, args.artifacts, args.failed)
    args.output.write_bytes(canonical(result) + b"\n")
    print("manifest collection complete; valid build:", result["complete"])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
