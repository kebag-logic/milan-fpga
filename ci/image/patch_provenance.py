#!/usr/bin/env python3
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""Reproduce committed patches and preserve per-line upstream provenance."""

from __future__ import annotations

import hashlib
from pathlib import Path
import re
import subprocess
import tarfile
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from privacy import Policy


ROOT = Path(__file__).resolve().parents[2]
PATCHES = Path("sw/litex/patches")


def committed(path: Path) -> bytes:
    """Refuse a patch or series whose working bytes differ from its commit."""
    data = (ROOT / path).read_bytes()
    recorded = subprocess.check_output(["git", "--no-replace-objects", "show", f"HEAD:{path}"], cwd=ROOT)
    if hashlib.sha256(data).digest() != hashlib.sha256(recorded).digest():
        raise ValueError("privacy patch differs from its committed file")
    return data


def apply_hunk(lines: list[tuple[bytes, int | None]], hunk: list[bytes],
               policy: Policy) -> list[tuple[bytes, int | None]]:
    """Apply one exact unified hunk, carrying only unchanged line identities."""
    match = re.fullmatch(rb"@@ -(\d+)(?:,(\d+))? \+(\d+)(?:,(\d+))? @@[^\n]*\n", hunk[0])
    if match is None:
        raise ValueError("unsupported privacy patch hunk")
    _, old_count, start, new_count = match.groups()
    before = [line[1:] for line in hunk[1:] if line[:1] in (b" ", b"-")]
    positions = [i for i in range(len(lines) - len(before) + 1)
                 if [line for line, _ in lines[i:i + len(before)]] == before]
    if len(positions) != 1:
        raise ValueError("privacy patch context missing or ambiguous")
    offset = positions[0]
    consumed = 0
    output = []
    for line in hunk[1:]:
        if line[:1] in (b" ", b"-"):
            if offset + consumed >= len(lines) or lines[offset + consumed][0] != line[1:]:
                raise ValueError("privacy patch does not match the pinned member")
            if line[:1] == b" ":
                output.append(lines[offset + consumed])
            consumed += 1
        elif line[:1] == b"+":
            if policy.matches(line[1:]):
                raise ValueError("privacy identity on a first-party patch-added line")
            output.append((line[1:], None))
        else:
            raise ValueError("unsupported privacy patch line")
    if consumed != int(old_count or b"1") or len(output) != int(new_count or b"1"):
        raise ValueError("privacy patch hunk counts disagree")
    return lines[:offset] + output + lines[offset + consumed:]


def patched(lines: list[tuple[bytes, int | None]], patch: bytes, policy: Policy) -> list[tuple[bytes, int | None]]:
    """Replay the diff without fuzz or whitespace changes; reject added identities."""
    hunks = re.split(rb"(?m)(?=^@@ )", patch)
    if len(hunks) == 1:
        raise ValueError("privacy patch has no hunks")
    for hunk in hunks[1:]:
        lines = apply_hunk(lines, hunk.splitlines(keepends=True), policy)
    return lines


def source_file(row: dict, cache: Path, member: str) -> tuple[bytes, str]:
    """Authenticate the public archive before selecting its exact tree member."""
    path = cache / row["filename"]
    with path.open("rb") as stream:
        actual = hashlib.file_digest(stream, "sha256").hexdigest()
    if actual != row["sha256"] or path.stat().st_size != row["size"]:
        raise ValueError("privacy patched source checksum or size mismatch")
    with tarfile.open(path) as archive:
        matches = [item for item in archive if item.isfile() and item.name.partition("/")[2] == member]
        if len(matches) != 1:
            raise ValueError("privacy patched source member missing or ambiguous")
        return archive.extractfile(matches[0]).read(), matches[0].name


def provenance(pins: dict, cache: Path, policy: Policy) -> dict:
    """Bind each allowed postimage to upstream bytes and every committed patch."""
    series = committed(PATCHES / "apply.sh")
    match = re.search(rb"(?ms)^SERIES=\(\n(.*?)^\)", series)
    if match is None:
        raise ValueError("unsupported committed privacy patch series")
    rows = {row["tool"]: row for row in pins["sources"]}
    files = {}
    for entry in match[1].decode().splitlines():
        selected = re.fullmatch(r'\s*"([\w]+)\s+([\w.-]+\.patch)"\s*', entry)
        if selected is None:
            raise ValueError("unsupported committed privacy patch entry")
        tool, name = selected.groups()
        patch = committed(PATCHES / name)
        targets = re.findall(rb"(?m)^--- a/(.+)\n\+\+\+ b/(.+)\n", patch)
        if len(targets) != 1 or targets[0][0] != targets[0][1]:
            raise ValueError("privacy patch must modify one existing member")
        target = targets[0][0].decode()
        prefix = "pythondata_cpu_vexiiriscv/verilog/ext/VexiiRiscv/"
        source = "VexiiRiscv" if target.startswith(prefix) else tool
        row = rows[source]
        if "kebag-logic" in row["url"].lower() or not row["url"].startswith("https://"):
            raise ValueError("first-party patch input cannot grant provenance")
        key = (source, target.removeprefix(prefix))
        if key not in files:
            original, member = source_file(row, cache, key[1])
            lines = original.splitlines(keepends=True)
            files[key] = {"original": original, "member": member, "patches": [],
                          "lines": list(zip(lines, range(1, len(lines) + 1)))}
        state = files[key]
        state["lines"] = patched(state["lines"], patch, policy)
        state["patches"].append({"path": str(PATCHES / name), "sha256": hashlib.sha256(patch).hexdigest()})
    return records(files, rows, policy, hashlib.sha256(series).hexdigest())


def records(files: dict, rows: dict, policy: Policy, series_hash: str) -> dict:
    """Record only fully reproduced files whose matches retain upstream lines."""
    result = {}
    for (source, _), state in files.items():
        matches = [{"output_line": number, "upstream_line": origin}
                   for number, (line, origin) in enumerate(state["lines"], 1) if policy.matches(line)]
        if any(match["upstream_line"] is None for match in matches):
            raise ValueError("privacy identity on a modified upstream line")
        if not matches:
            continue
        digest = hashlib.sha256(b"".join(line for line, _ in state["lines"])).hexdigest()
        row = rows[source]
        result[digest] = {"tool": source, "pin": row["version"], "source_sha256": row["sha256"],
                          "source_member_id": hashlib.sha256(state["member"].encode()).hexdigest(),
                          "upstream_member_sha256": hashlib.sha256(state["original"]).hexdigest(),
                          "member_sha256": digest, "patches": state["patches"],
                          "series_sha256": series_hash, "unchanged_matches": matches}
    return result
