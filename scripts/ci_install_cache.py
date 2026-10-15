#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""Bind a package-download cache to the exact solver result and install recipe.

Distribution packages retain their original resolution policy. The prepared
index is used by both the cache planner and the following installation. APT
still verifies each downloaded archive before installing it.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import re
import shlex
import subprocess


def archive_inventory(text: str) -> list[dict]:
    """Require exact source hashes for every archive the solver will download."""
    rows = []
    for line in text.splitlines():
        if not line.startswith("'"):
            continue
        words = shlex.split(line)
        if (len(words) != 4 or not words[2].isdecimal()
                or not re.fullmatch(r"SHA256:[0-9a-f]{64}", words[3])):
            raise ValueError("APT archive inventory lacks an exact SHA-256")
        rows.append({"url": words[0], "filename": words[1], "bytes": int(words[2]),
                     "sha256": words[3].split(":", 1)[1]})
    if len({row["filename"] for row in rows}) != len(rows):
        raise ValueError("duplicate APT archive")
    return rows


def cache_identity(packages: list[str], versions: str, archives: list[dict], recipe: str) -> str:
    """Version, source and recipe changes independently invalidate the key."""
    if not packages or any(not re.fullmatch(r"[a-zA-Z0-9.+:=~-]+", name) for name in packages):
        raise ValueError("package inventory is not literal")
    if not versions.strip() or not re.fullmatch(r"[0-9a-f]{64}", recipe):
        raise ValueError("missing package version or recipe identity")
    version = hashlib.sha256(json.dumps([packages, versions], sort_keys=True).encode()).hexdigest()
    source = hashlib.sha256(json.dumps(archives, sort_keys=True, separators=(",", ":")).encode()).hexdigest()
    return "apt-" + version + "-" + source + "-" + recipe


def main() -> int:
    """Prepare a download-only cache; the existing setup step performs installation."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--packages", nargs="+", required=True)
    parser.add_argument("--recipe", required=True)
    parser.add_argument("--directory", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args()
    args.directory.mkdir(parents=True, exist_ok=True)
    subprocess.run(["sudo", "apt-get", "update", "-qq"], check=True)
    versions = subprocess.check_output(["apt-cache", "policy", *args.packages], text=True)
    command = ["sudo", "apt-get", "-o", "Acquire::ForceHash=sha256", "--print-uris",
               "--download-only", "install", "-y", "--no-install-recommends", *args.packages]
    archives = archive_inventory(subprocess.check_output(command, text=True))
    key = cache_identity(args.packages, versions, archives, args.recipe)
    with args.output.open("a", encoding="utf-8") as stream:
        stream.write("key=" + key + "\n")
    print(json.dumps({"packages": args.packages, "versions": versions, "archives": archives, "key": key},
                     sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
