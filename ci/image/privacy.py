#!/usr/bin/env python3
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""Apply one privacy table, with byte-proved public upstream allowances."""

from __future__ import annotations

import hashlib
import io
import json
import os
from pathlib import Path
import pwd
import re
import socket
import subprocess
import tarfile
from typing import BinaryIO, Iterator
import zipfile


class Policy:
    """Read the committed rules and add this builder's actual identities."""

    def __init__(self) -> None:
        table = json.loads(Path(__file__).with_name("privacy.json").read_text())
        self.rules = []
        for row in table["rules"]:
            if "pattern" in row:
                pattern = row["pattern"].encode()
                needles = [value.encode().lower() for value in row["needles"]]
            elif "codepoints" in row:
                literal = bytes(row["codepoints"])
                needles = [literal.lower()]
                pattern = rb"(?<![A-Za-z0-9_])" + re.escape(literal) + rb"(?![A-Za-z0-9_])"
            else:
                values = {"builder-home": str(Path.home()),
                          "builder-account": pwd.getpwuid(os.getuid()).pw_name,
                          "builder-host": socket.gethostname()}
                literal = values[row["runtime"]].encode()
                needles = [literal.lower()]
                if row["runtime"] == "builder-account" and literal == b"root":
                    continue
                pattern = rb"(?<![A-Za-z0-9_])" + re.escape(literal) + rb"(?![A-Za-z0-9_])"
            self.rules.append((row["class"], re.compile(pattern, re.IGNORECASE), needles))

    def matches(self, data: bytes) -> set[str]:
        """Return classifications only; never echo protected bytes."""
        folded = data.lower()
        return {name for name, pattern, needles in self.rules
                if any(value in folded for value in needles) and pattern.search(data)}

    def measure(self, stream: BinaryIO) -> tuple[str, set[str]]:
        """Hash the complete member and scan across bounded chunk boundaries."""
        digest = hashlib.sha256()
        found = set()
        tail = b""
        while chunk := stream.read(1024 * 1024):
            digest.update(chunk)
            found.update(self.matches(tail + chunk))
            tail = (tail + chunk)[-4096:]
        return digest.hexdigest(), found


def public_source(row: dict[str, object]) -> bool:
    """First-party artifacts never grant an identity allowance."""
    return str(row["url"]).startswith("https://") and "kebag-logic" not in str(row["url"]).lower()


def tar_members(stream: BinaryIO) -> Iterator[tuple[str, BinaryIO]]:
    """Read regular members without unpacking paths or executing archive code."""
    with tarfile.open(fileobj=stream, mode="r|*") as archive:
        for member in archive:
            if member.isfile():
                yield member.name, archive.extractfile(member)


def deb_members(path: Path) -> Iterator[tuple[str, BinaryIO]]:
    """Read the distribution archive's data tar directly from its ar framing."""
    with path.open("rb") as stream:
        if stream.read(8) != b"!<arch>\n":
            raise ValueError("invalid distribution archive")
        while header := stream.read(60):
            size = int(header[48:58])
            payload = stream.read(size)
            if header[:16].strip().rstrip(b"/").startswith(b"data.tar"):
                if header[:16].strip().rstrip(b"/").endswith(b".zst"):
                    payload = subprocess.run(["zstd", "--decompress", "--stdout"], input=payload,
                                             stdout=subprocess.PIPE, check=True).stdout
                yield from tar_members(io.BytesIO(payload))
            if size % 2:
                stream.read(1)


def source_members(path: Path) -> Iterator[tuple[str, BinaryIO]]:
    """Support the recipe's public archive formats, without extraction."""
    if path.suffix == ".deb":
        yield from embedded_wheels(deb_members(path))
    elif zipfile.is_zipfile(path):
        with zipfile.ZipFile(path) as archive:
            for member in archive.infolist():
                if not member.is_dir():
                    with archive.open(member) as stream:
                        yield member.filename, stream
    elif tarfile.is_tarfile(path):
        with path.open("rb") as stream:
            yield from embedded_wheels(tar_members(stream))


def embedded_wheels(members: Iterator[tuple[str, BinaryIO]]) -> Iterator[tuple[str, BinaryIO]]:
    """Authenticate wheel members through their containing pinned package bytes."""
    for name, stream in members:
        if not name.endswith(".whl"):
            yield name, stream
            continue
        data = stream.read()
        yield name, io.BytesIO(data)
        with zipfile.ZipFile(io.BytesIO(data)) as archive:
            for member in archive.infolist():
                if not member.is_dir():
                    with archive.open(member) as content:
                        yield name + "!" + member.filename, content


def provenance(pins: dict[str, object], cache: Path, policy: Policy) -> dict[str, dict[str, str]]:
    """Index only matching files, authenticating every source archive first."""
    result = base_provenance(pins, cache.parent / "base-locked.tar", policy) if "base" in pins else {}
    seen = set()
    rows = [(row, cache / "debs" / row["filename"]) for row in pins["packages"]]
    rows += [(row, cache / row["filename"]) for row in pins["sources"]]
    for row, path in rows:
        if not public_source(row) or row["sha256"] in seen:
            continue
        with path.open("rb") as stream:
            actual = hashlib.file_digest(stream, "sha256").hexdigest()
        if actual != row["sha256"] or path.stat().st_size != row["size"]:
            raise ValueError("privacy provenance source checksum or size mismatch")
        seen.add(actual)
        result[actual] = {"tool": row["tool"], "pin": row["version"],
                          "source_sha256": actual, "member_sha256": actual,
                          "source_member_id": hashlib.sha256(path.name.encode()).hexdigest(),
                          "whole_artifact": True}
        for name, stream in source_members(path):
            digest, findings = policy.measure(stream)
            if findings:
                result[digest] = {"tool": row["tool"], "pin": row["version"],
                                  "source_sha256": actual, "member_sha256": digest,
                                  "source_member_id": hashlib.sha256(name.encode()).hexdigest()}
    if any(row["tool"] == "VexiiRiscv" for row in pins["sources"]):
        import patch_provenance

        result.update(patch_provenance.provenance(pins, cache, policy))
    return result


def base_provenance(pins: dict[str, object], path: Path, policy: Policy) -> dict[str, dict[str, str]]:
    """Authenticate unchanged distribution files against the pinned public base."""
    from image_archive import blob, object_blob

    result = {}
    with tarfile.open(path) as archive:
        index = json.load(archive.extractfile("index.json"))
        descriptor = index["manifests"][0]
        if len(index["manifests"]) != 1 or descriptor["digest"] != pins["base"].split("@")[1]:
            raise ValueError("privacy base differs from the public source pin")
        manifest = object_blob(archive, descriptor)
        if "manifests" in manifest:
            candidates = [row for row in manifest["manifests"]
                          if row.get("platform", {}).get("os", "") + "/" +
                          row.get("platform", {}).get("architecture", "") == pins["platform"]]
            if len(candidates) != 1:
                raise ValueError("privacy base platform is ambiguous")
            manifest = object_blob(archive, candidates[0])
        for layer in manifest["layers"]:
            with blob(archive, layer["digest"]) as stream:
                if "sha256:" + hashlib.file_digest(stream, "sha256").hexdigest() != layer["digest"]:
                    raise ValueError("privacy base layer differs from public manifest")
            with blob(archive, layer["digest"]) as stream:
                for name, member in tar_members(stream):
                    digest, findings = policy.measure(member)
                    if findings:
                        result[digest] = {"tool": "base", "pin": pins["base"].split("@")[1],
                                          "source_sha256": layer["digest"].split(":")[1],
                                          "member_sha256": digest,
                                          "source_member_id": hashlib.sha256(name.encode()).hexdigest()}
    return result


def check_file(stream: BinaryIO, member: str, policy: Policy,
               upstream: dict[str, dict[str, str]], allowed: list[dict[str, object]]) -> None:
    """Refuse changed or unknown files; log each exact public member proof."""
    digest, findings = policy.measure(stream)
    if not findings:
        return
    if member.removeprefix("./").startswith("opt/tsn-gen/") or digest not in upstream:
        raise ValueError("image privacy refusal: " + ", ".join(sorted(findings)) +
                         "; member-id " + hashlib.sha256(member.encode()).hexdigest())
    allowed.append({**upstream[digest], "image_member_id": hashlib.sha256(member.encode()).hexdigest(),
                    "classes": sorted(findings)})
