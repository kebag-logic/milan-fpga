#!/usr/bin/env python3
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""Regenerate the recursive CPU source closure from public, pinned Git trees."""

from __future__ import annotations

import argparse
import configparser
import hashlib
import json
from pathlib import Path
import tarfile
import urllib.request


def fetch(url: str) -> bytes:
    """Fetch public metadata without a credential or user configuration."""
    with urllib.request.urlopen(url, timeout=120) as response:
        return response.read()


def closure(row: dict[str, object], cache: Path) -> list[dict[str, object]]:
    """Match each declared submodule to its parent's exact gitlink."""
    url = str(row["url"])
    repository = url.split("github.com/", 1)[1].split("/tar.gz/", 1)[0]
    archive = cache / str(row["filename"])
    if not archive.exists():
        archive.parent.mkdir(parents=True, exist_ok=True)
        archive.write_bytes(fetch(url))
    data = archive.read_bytes()
    if hashlib.sha256(data).hexdigest() != row["sha256"] or len(data) != row["size"]:
        raise ValueError("CPU archive does not match its pin")
    with tarfile.open(archive) as stream:
        members = [m for m in stream if m.name.split("/", 1)[-1] == ".gitmodules"]
        if not members:
            return []
        config = configparser.ConfigParser()
        config.read_string(stream.extractfile(members[0]).read().decode())
    tree = json.loads(fetch(f"https://api.github.com/repos/{repository}/git/trees/{row['version']}?recursive=1"))
    if tree.get("truncated"):
        raise ValueError("truncated CPU Git tree")
    links = {item["path"]: item["sha"] for item in tree["tree"] if item["mode"] == "160000"}
    results = []
    for section in config.sections():
        path, origin = config[section]["path"], config[section]["url"]
        if not origin.startswith("https://github.com/"):
            raise ValueError("CPU submodule must use a public HTTPS origin")
        pin = links.pop(path)
        repository = origin.removeprefix("https://github.com/").removesuffix(".git")
        name = repository.split("/")[-1]
        url = f"https://codeload.github.com/{repository}/tar.gz/{pin}"
        payload = fetch(url)
        child = {"tool": name, "version": pin, "url": url, "filename": f"sources/{name}.tar.gz",
                 "sha256": hashlib.sha256(payload).hexdigest(), "size": len(payload),
                 "kind": "git", "parent": row["tool"], "path": path}
        target = cache / child["filename"]
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(payload)
        results.append(child)
        results.extend(closure(child, cache))
    if links:
        raise ValueError("undeclared CPU gitlinks")
    return results


def main() -> int:
    """Write only the generated recursive source rows, retaining other pins."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--cache", type=Path, required=True)
    args = parser.parse_args()
    path = Path(__file__).with_name("sources.lock.json")
    pins = json.loads(path.read_text())
    cpu = next(row for row in pins["sources"] if row["tool"] == "VexiiRiscv")
    rows = closure(cpu, args.cache)
    names = {row["tool"] for row in rows}
    pins["sources"] = [row for row in pins["sources"] if row["tool"] not in names] + rows
    pins["sources"].sort(key=lambda row: row["tool"])
    path.write_text(json.dumps(pins, sort_keys=True, indent=2) + "\n")
    print(f"Resolved {len(rows)} recursive CPU repositories")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
