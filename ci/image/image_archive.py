#!/usr/bin/env python3
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""Verify exported OCI bytes and scan every layer and config for host identity."""

from __future__ import annotations

import argparse
import gzip
import hashlib
import json
from pathlib import Path
import tarfile
from typing import BinaryIO

import privacy


def scan(stream: BinaryIO, member: str) -> None:
    """Retain the strict no-provenance entry point for planted controls."""
    privacy.check_file(stream, member, privacy.Policy(), {}, [])


def blob(archive: tarfile.TarFile, digest: str) -> BinaryIO:
    """Open an OCI content-addressed member without extraction."""
    stream = archive.extractfile("blobs/" + digest.replace(":", "/"))
    if stream is None:
        raise ValueError("missing image blob")
    return stream


def object_blob(archive: tarfile.TarFile, descriptor: dict[str, object]) -> dict[str, object]:
    """Read and authenticate a small manifest or configuration blob."""
    with blob(archive, descriptor["digest"]) as stream:
        data = stream.read()
    if len(data) != descriptor["size"] or "sha256:" + hashlib.sha256(data).hexdigest() != descriptor["digest"]:
        raise ValueError("image metadata digest or size mismatch")
    return json.loads(data)


def inspect(path: Path, platform: str, upstream: dict | None = None) -> dict[str, object]:
    """Authenticate an exported image, inspect all layers, and report identity."""
    policy = privacy.Policy()
    allowed = []
    with tarfile.open(path) as archive:
        index = json.load(archive.extractfile("index.json"))
        if len(index["manifests"]) != 1:
            raise ValueError("expected one exported image")
        descriptor = index["manifests"][0]
        manifest = object_blob(archive, descriptor)
        if "manifests" in manifest:
            available = [item for item in manifest["manifests"]
                         if item.get("platform", {}).get("os", "") + "/" +
                         item.get("platform", {}).get("architecture", "") == platform]
            if len(available) != 1:
                raise ValueError("expected one image platform")
            descriptor = available[0]
            manifest = object_blob(archive, descriptor)
        config = object_blob(archive, manifest["config"])
        if policy.matches(json.dumps(config).encode()):
            raise ValueError("host identity in image config, history, environment or labels")
        layers = []
        for layer, diff_id in zip(manifest["layers"], config["rootfs"]["diff_ids"], strict=True):
            with blob(archive, layer["digest"]) as stream:
                actual = "sha256:" + hashlib.file_digest(stream, "sha256").hexdigest()
            if actual != layer["digest"]:
                raise ValueError("image layer digest mismatch")
            with blob(archive, layer["digest"]) as stream:
                raw = gzip.GzipFile(fileobj=stream) if "gzip" in layer["mediaType"] else stream
                actual = "sha256:" + hashlib.file_digest(raw, "sha256").hexdigest()
            if actual != diff_id:
                raise ValueError("image layer diff-id mismatch")
            with blob(archive, layer["digest"]) as stream, tarfile.open(fileobj=stream, mode="r|*") as entries:
                for member in entries:
                    fields = " ".join((member.name, member.linkname, member.uname, member.gname)).encode()
                    if policy.matches(fields):
                        raise ValueError("host identity in image member metadata")
                    if member.name.startswith("opt/tsn-gen/") and (
                            "__pycache__" in member.name or member.name.endswith((".pyc", ".log")) or
                            "CMakeFiles" in member.name or member.name.endswith("CMakeCache.txt")):
                        raise ValueError("oracle layer contains a forbidden build leftover")
                    if member.isfile():
                        privacy.check_file(entries.extractfile(member), member.name, policy, upstream or {}, allowed)
            layers.append({"oci_digest": layer["digest"], "diff_id": diff_id})
        return {"image_digest": descriptor["digest"], "image_id": manifest["config"]["digest"],
                "platform": config["os"] + "/" + config["architecture"], "layers": layers,
                "environment": config["config"].get("Env", []), "history": config.get("history", []),
                "upstream_allowances": allowed}


def main() -> int:
    """Inspect one locally exported image without accessing the daemon."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("archive", type=Path)
    parser.add_argument("--cache", type=Path, required=True)
    pins = json.loads(Path(__file__).with_name("sources.lock.json").read_text())
    parser.add_argument("--platform", default=pins["platform"])
    args = parser.parse_args()
    upstream = privacy.provenance(pins, args.cache, privacy.Policy())
    print(json.dumps(inspect(args.archive, args.platform, upstream), sort_keys=True, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
