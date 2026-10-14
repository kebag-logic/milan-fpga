#!/usr/bin/env python3
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""Derive distribution roots and resolve their dependency closure from checked debs."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import re
import subprocess


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]


def roots(root: Path = ROOT) -> list[str]:
    """Require an installing workflow or a concrete consumer for every root."""
    inventory = json.loads((root / "ci/image/tool-inventory.json").read_text())
    names = {row["tool"] for row in inventory["tools"] if row["kind"] == "apt"}
    declared = json.loads((root / "ci/image/package_roots.json").read_text())
    for row in declared["runtime"] + declared["recipe"]:
        if not row["reason"] or not row["literal"] or row["literal"] not in (root / row["path"]).read_text():
            raise ValueError(f"distribution root has no consumer: {row['package']}")
        if row["package"] in names:
            raise ValueError(f"duplicate distribution root: {row['package']}")
        names.add(row["package"])
    return sorted(names)


def metadata(path: Path, row: dict[str, object]) -> dict[str, str]:
    """Read dependency fields only after verifying the exact locked archive."""
    with path.open("rb") as stream:
        actual = hashlib.file_digest(stream, "sha256").hexdigest()
    if actual != row["sha256"] or path.stat().st_size != row["size"]:
        raise ValueError("distribution archive differs from its source pin")
    data = subprocess.check_output(["dpkg-deb", "--field", str(path)], text=True)
    fields = {}
    for line in data.splitlines():
        if line and not line[0].isspace() and ": " in line:
            key, value = line.split(": ", 1)
            fields[key] = value
    if fields["Package"] != row["tool"] or fields["Version"] != row["version"]:
        raise ValueError("distribution archive identity differs from its declaration")
    return fields


def satisfies(version: str, relation: str | None, wanted: str | None) -> bool:
    """Let the distribution version comparator judge dependency constraints."""
    if not relation:
        return True
    return subprocess.run(["dpkg", "--compare-versions", version, relation, wanted], check=False).returncode == 0


def selected_packages(pins: dict[str, object], cache: Path, base: list[dict[str, str]]) -> list[dict[str, object]]:
    """Resolve required dependencies, preferring the base where it already suffices."""
    rows = {row["tool"]: row for row in pins["packages"]}
    fields = {name: metadata(cache / row["filename"], row) for name, row in rows.items()}
    installed = {row["Package"]: row for row in base}
    providers = {}
    for name, row in {**fields, **installed}.items():
        for part in row.get("Provides", "").split(","):
            token = part.strip().split(" ", 1)[0]
            if token:
                providers.setdefault(token, []).append(name)
    selected = set()
    pending = roots()
    while pending:
        name = pending.pop()
        if name in selected:
            continue
        if name not in fields:
            if name in installed:
                continue
            raise ValueError(f"unresolved distribution root: {name}")
        selected.add(name)
        for group in (fields[name].get("Pre-Depends", "") + "," + fields[name].get("Depends", "")).split(","):
            if not group.strip():
                continue
            found = False
            for alternative in group.split("|"):
                match = re.fullmatch(r"\s*([\w+.-]+)(?::\w+)?(?:\s*\(([<>=]+)\s*([^\)]+)\))?\s*", alternative)
                if match is None:
                    raise ValueError(f"unsupported dependency: {alternative}")
                dependency, relation, version = match.groups()
                choices = [dependency, *sorted(providers.get(dependency, []))]
                for choice in choices:
                    if choice in installed and satisfies(installed[choice]["Version"], relation, version):
                        found = True
                        break
                    if choice in fields and satisfies(fields[choice]["Version"], relation, version):
                        pending.append(choice)
                        found = True
                        break
                if found:
                    break
            if not found:
                raise ValueError(f"unresolved package dependency: {name}: {group}")
    return [rows[name] for name in sorted(selected)]


def main() -> int:
    """Regenerate or check the resolved package set without consulting moving indexes."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--cache", type=Path, required=True)
    parser.add_argument("--candidates", type=Path, help="source lock containing additional checked archive candidates")
    parser.add_argument("--write", action="store_true")
    args = parser.parse_args()
    path = HERE / "sources.lock.json"
    pins = json.loads(path.read_text())
    if args.candidates:
        candidates = json.loads(args.candidates.read_text())["packages"]
        current = {row["tool"]: row for row in pins["packages"]}
        for row in candidates:
            if row["tool"] in current and current[row["tool"]] != row:
                raise ValueError("candidate conflicts with an existing package pin")
            current[row["tool"]] = row
        pins["packages"] = list(current.values())
    base = pins["base_packages"]
    packages = selected_packages(pins, args.cache, base)
    if args.write:
        pins["packages"] = packages
        path.write_text(json.dumps(pins, sort_keys=True, indent=2) + "\n")
    elif pins["packages"] != packages:
        raise ValueError("distribution lock contains missing or unused packages")
    print(f"PASS: {len(roots())} used roots resolve to {len(packages)} locked packages")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
