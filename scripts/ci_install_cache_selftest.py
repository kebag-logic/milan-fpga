#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""Prove installation caches bind sources and recipes without changing gates."""

import copy
import hashlib
import re

from ci_gate_workflows import ROOT, TEMPLATES, gate_graph, load_template, setup
from ci_install_cache import archive_inventory, cache_identity
from ci_install_workflows import generate


def refused(text: str) -> None:
    """Malformed, duplicated or weak source identities cannot make a cache key."""
    try:
        archive_inventory(text)
    except ValueError:
        return
    raise AssertionError("accepted an unbound archive inventory")


def main() -> int:
    """Exercise actual parsing, identity changes and every installation transformation."""
    line = "'https://packages.invalid/p_1.deb' p_1.deb 123 SHA256:" + "a" * 64
    rows = archive_inventory(line)
    key = cache_identity(["p"], "p: Installed: 0 Candidate: 1", rows, "b" * 64)
    for field in ("version", "source", "recipe"):
        changed = copy.deepcopy(rows)
        if field == "source":
            changed[0]["sha256"] = "c" * 64
        altered = cache_identity(["p"], "p: Installed: 0 Candidate: " + ("2" if field == "version" else "1"),
                                 changed, ("c" if field == "recipe" else "b") * 64)
        assert altered != key, field
    for broken in (line.replace("SHA256:", "MD5Sum:"), line.replace("123", "unknown"), line + "\n" + line):
        refused(broken)
    constraints = ROOT.joinpath("ci/constraints-ci.txt").read_text()
    packages = [line for line in constraints.splitlines() if line and not line.startswith("#")]
    assert len(packages) == 28 and len({line.split(" @ ")[0].lower() for line in packages}) == 28
    assert all(re.fullmatch(r"[^ ]+ @ https://files.pythonhosted.org/[^ ]+#sha256=[0-9a-f]{64}", line)
               for line in packages)
    transformed = 0
    for name in TEMPLATES:
        source = gate_graph(name, load_template(ROOT, name))
        result = generate(source)
        for job_id, before in source["jobs"].items():
            after = result["jobs"][job_id]
            for original in before["steps"]:
                matches = [step for step in after["steps"] if step.get("name") == original.get("name")]
                # An unnamed action is unchanged; names are unique for all commands.
                if "run" not in original:
                    assert original in after["steps"]
                    continue
                assert len(matches) == 1
                if not original.get("name", "").startswith(("Install ", "Build ")):
                    assert matches[0] == original, original["name"]
                elif matches[0] != original:
                    transformed += 1
                    assert matches[0].get("if") == original.get("if")
            for step in after["steps"]:
                if step.get("uses") == "actions/cache@v4" and step.get("name", "").startswith("Cache exact"):
                    assert "restore-keys" not in step["with"]
                    assert "scripts/ci_install*.py" in step["with"]["key"]
    assert transformed > 10
    print("install caches: version/source/recipe controls and unchanged test commands PASS")
    print("constraint source:", hashlib.sha256(constraints.encode()).hexdigest())
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
