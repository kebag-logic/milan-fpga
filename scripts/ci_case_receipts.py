#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""Prove executed case coverage against a driver's freshly derived inventory.

A planned list is not execution evidence. Each receipt records each completed
case, its verdict, process status and the digest of its complete diagnostic
output. Verification requires every case exactly once, on its selected leg,
at the requested commit and tree. Comparing a complete unsharded run with a
complete sharded run additionally requires identical per-case observations.
"""

from __future__ import annotations

import argparse
from collections import Counter
import hashlib
import json
import os
import stat
from pathlib import Path
import re
import subprocess

from suite_shards import parse_shard

SCHEMA = 1
HEX256 = re.compile(r"[0-9a-f]{64}")
HEX160 = re.compile(r"[0-9a-f]{40}")


def canonical(value: object) -> bytes:
    """One encoding for inventory and output evidence."""
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=True).encode()


def validate_inventory(names: list[str]) -> None:
    """An empty or ambiguous driver inventory cannot prove coverage."""
    if (not isinstance(names, list) or not names
            or any(not isinstance(name, str) or not name for name in names)
            or len(set(names)) != len(names)):
        raise ValueError("inventory must be a nonempty list of unique case names")


def partition(names: list[str], shard: str | None) -> list[str]:
    """Select cases in driver order; no option retains the complete inventory."""
    validate_inventory(names)
    if shard is None:
        return names[:]
    index, total = parse_shard(shard)
    if total > len(names):
        raise ValueError("more shards than cases would leave empty legs")
    return names[index::total]


def source_identity(root: Path) -> tuple[str, str]:
    """Prove committed bytes directly; index flags cannot hide a source edit."""
    env = dict(os.environ, GIT_NO_REPLACE_OBJECTS="1")

    def git(directory: Path, *args: str) -> bytes:
        """Read repository metadata without replacement objects."""
        return subprocess.check_output(["git", *args], cwd=directory, env=env)

    def check(directory: Path, revision: str) -> None:
        """Compare every tracked entry with its committed mode and bytes."""
        entries = git(directory, "ls-tree", "-rz", revision).split(b"\0")
        for entry in filter(None, entries):
            metadata, name = entry.split(b"\t", 1)
            mode, kind, oid = metadata.split()
            path = directory / os.fsdecode(name)
            if kind == b"commit":
                # Uninitialised, unused dependencies contain no execution inputs.
                if not (path / ".git").exists():
                    if path.exists() and any(path.iterdir()):
                        raise ValueError(f"source dependency is not a checkout: {path}")
                    continue
                top = git(path, "rev-parse", "--show-toplevel").decode().strip()
                if Path(top).resolve() != path.resolve():
                    raise ValueError(f"source dependency root differs: {path}")
                origin = git(path, "remote", "get-url", "origin").decode().strip()
                if not origin:
                    raise ValueError(f"source dependency origin missing: {path}")
                if name == b"third_party/tsn-c-stack" and origin != "https://github.com/kebag-logic/tsn-c-stack.git":
                    raise ValueError("source dependency origin differs: third_party/tsn-c-stack")
                if git(path, "rev-parse", "HEAD").strip() != oid:
                    raise ValueError(f"source dependency revision differs: {path}")
                check(path, oid.decode())
                continue
            try:
                info = path.lstat()
                if mode == b"120000" and stat.S_ISLNK(info.st_mode):
                    data = os.fsencode(os.readlink(path))
                elif mode in (b"100644", b"100755") and stat.S_ISREG(info.st_mode):
                    if bool(info.st_mode & 0o111) != (mode == b"100755"):
                        raise ValueError(f"source mode differs: {path}")
                    data = path.read_bytes()
                else:
                    raise ValueError(f"source kind differs: {path}")
            except OSError as exc:
                raise ValueError(f"source unavailable: {path}") from exc
            digest = hashlib.sha1(b"blob " + str(len(data)).encode() + b"\0" + data).hexdigest()
            if digest != oid.decode():
                raise ValueError(f"source bytes differ: {path}")
        if git(directory, "ls-files", "--others", "--exclude-standard", "-z"):
            raise ValueError(f"untracked source in {directory}")
        if git(directory, "diff", "--cached", "--name-only", revision):
            raise ValueError(f"staged source differs in {directory}")

    root = root.resolve()
    if Path(git(root, "rev-parse", "--show-toplevel").decode().strip()).resolve() != root:
        raise ValueError("source root is not the checkout root")
    head = git(root, "rev-parse", "HEAD").decode().strip()
    tree = git(root, "rev-parse", "HEAD^{tree}").decode().strip()
    check(root, head)
    return head, tree


class Receipt:
    """Record observations only; the driver still owns every case's verdict."""

    def __init__(self, root: Path, suite: str, names: list[str], shard: str | None,
                 path: Path | None) -> None:
        self.path = path
        self.root = root
        self.results: list[dict[str, object]] = []
        self.data: dict[str, object] = {}
        if path is None:
            return
        if path.exists():
            raise ValueError(f"receipt already exists: {path}")
        head, tree = source_identity(root)
        self.data = {"schema": SCHEMA, "suite": suite, "head": head, "tree": tree,
                     "inventory": names, "shard": shard, "results": self.results}

    def record(self, name: str, outcome: str, rc: int, output: str,
               result_line: str | None = None) -> None:
        """Keep the completed case's own status and exact output, including failures."""
        if self.path is None:
            return
        self.results.append({"case": name, "outcome": outcome, "returncode": rc,
                             "output_sha256": hashlib.sha256(output.encode()).hexdigest()})
        if result_line is not None:
            self.results[-1]["result_line"] = result_line
        log_dir = self.path.with_suffix(".logs")
        log_dir.mkdir(parents=True, exist_ok=True)
        # A digest filename cannot escape the log directory through a case name.
        log_dir.joinpath(hashlib.sha256(name.encode()).hexdigest() + ".log").write_text(output)

    def finish(self) -> None:
        """Publish only after the driver has graded every selected result."""
        if self.path is not None:
            if source_identity(self.root) != (self.data["head"], self.data["tree"]):
                raise ValueError("source identity changed during execution")
            self.path.parent.mkdir(parents=True, exist_ok=True)
            with self.path.open("xb") as stream:
                stream.write(canonical(self.data) + b"\n")


def verify(names: list[str], receipts: list[dict], suite: str, head: str, tree: str) -> dict:
    """Return complete case observations, or name the failed proof obligation."""
    validate_inventory(names)
    if not HEX160.fullmatch(head) or not HEX160.fullmatch(tree):
        raise ValueError("head and tree must be full object IDs")
    if not receipts:
        raise ValueError("no executed receipts")
    seen: list[str] = []
    shards: list[str | None] = []
    observations = {}
    totals = set()
    for receipt in receipts:
        if set(receipt) != {"schema", "suite", "head", "tree", "inventory", "shard", "results"}:
            raise ValueError("receipt fields differ from schema")
        for key, want in (("schema", SCHEMA), ("suite", suite), ("head", head),
                          ("tree", tree), ("inventory", names)):
            if receipt[key] != want:
                raise ValueError(f"receipt {key} differs")
        shard = receipt["shard"]
        selected = partition(names, shard)
        if shard is not None:
            totals.add(parse_shard(shard)[1])
        shards.append(shard)
        results = receipt["results"]
        if not isinstance(results, list):
            raise ValueError("results must be a list")
        ran = []
        for result in results:
            fields = {"case", "outcome", "returncode", "output_sha256"}
            if set(result) not in (fields, fields | {"result_line"}):
                raise ValueError("result fields differ from schema")
            if "result_line" in result and result["result_line"] != "RESULT: PASS":
                raise ValueError("result-only verdict differs from success")
            name = result["case"]
            if not isinstance(name, str):
                raise ValueError("case name must be a string")
            rc = result["returncode"]
            outcome = result["outcome"]
            if (type(rc) is not int or outcome not in ("pass", "caught")
                    or (outcome == "pass" and rc != 0)
                    or (outcome == "caught" and rc <= 0)):
                raise ValueError(f"{name}: unsuccessful or inconsistent case verdict")
            digest = result["output_sha256"]
            if not isinstance(digest, str) or not HEX256.fullmatch(digest):
                raise ValueError(f"{name}: missing output digest")
            ran.append(name)
            observations[name] = result
        if ran != selected:
            raise ValueError(f"shard {shard}: executed cases differ from its inventory: {ran}")
        seen.extend(ran)
    if Counter(seen) != Counter(names):
        raise ValueError("executed union has missing or duplicated cases")
    if None in shards:
        if shards != [None]:
            raise ValueError("unsharded receipt mixed with other receipts")
    elif len(totals) != 1 or set(shards) != {f"{n}/{len(shards)}" for n in range(len(shards))}:
        raise ValueError("missing, duplicate or inconsistent shard coordinates")
    return observations


def read_receipts(paths: list[Path]) -> list[dict]:
    """Read receipts and bind every recorded digest to its retained output."""
    values = []
    for path in paths:
        value = json.loads(path.read_text())
        for result in value["results"]:
            filename = hashlib.sha256(result["case"].encode()).hexdigest() + ".log"
            output = path.with_suffix(".logs").joinpath(filename).read_bytes()
            if "result_line" in result:
                lines = re.findall(rb"^RESULT:.*$", output, re.MULTILINE)
                if lines != [result["result_line"].encode()]:
                    raise ValueError(f"{result['case']}: retained RESULT line differs")
            if hashlib.sha256(output).hexdigest() != result["output_sha256"]:
                raise ValueError(f"{result['case']}: retained output differs from receipt")
        values.append(value)
    return values


def main() -> int:
    """Check the actual union; optionally compare with an unsharded reference."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--inventory", type=Path, required=True)
    parser.add_argument("--suite", required=True)
    parser.add_argument("--head", required=True)
    parser.add_argument("--tree", required=True)
    parser.add_argument("--reference", type=Path)
    parser.add_argument("receipts", type=Path, nargs="+")
    args = parser.parse_args()
    try:
        names = json.loads(args.inventory.read_text())
        observations = verify(names, read_receipts(args.receipts), args.suite, args.head, args.tree)
        if args.reference:
            reference = read_receipts([args.reference])
            if reference[0]["shard"] is not None:
                raise ValueError("reference must be an unsharded run")
            original = verify(names, reference, args.suite, args.head, args.tree)
            for name in names:
                if observations[name] != original[name]:
                    raise ValueError(f"{name}: sharded outcome or checked output differs")
    except (OSError, ValueError, KeyError, TypeError) as exc:
        print(f"case union refused: {exc}")
        return 1
    print(f"case union: {len(names)} cases exactly once; observations verified")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
