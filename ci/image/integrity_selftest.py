#!/usr/bin/env python3
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""Exercise image lock, privacy, normalization and package-root refusals offline."""

import copy
import io
import json
from pathlib import Path
import struct
import tempfile
from unittest.mock import patch

import build
from build_selftest import refused
import image_archive
import image_lock
import normalize
import resolve_packages


def locks() -> None:
    """Distinguish complete declaration consistency from actual image identity."""
    pins = json.loads((build.HERE / "sources.lock.json").read_text())
    recipe = build.recipe_digest()
    expected = build.layer_records(pins)
    layers = [{**row, "oci_digest": "sha256:" + "a" * 64, "diff_id": "sha256:" + "b" * 64} for row in expected]
    lock = {"schema": 2, "platform": pins["platform"], "base": pins["base"], "recipe_digest": recipe,
            "base_layers": pins["base_layers"], "image_digest": "sha256:" + "c" * 64,
            "image_id": "sha256:" + "d" * 64, "layers": layers}
    image_lock.validate(lock, pins, recipe, expected)
    for key, value in (("layers", []), ("platform", "wrong"), ("base", "moving"),
                       ("image_digest", "sha256:" + "0" * 64), ("schema", True), ("base_layers", [])):
        changed = copy.deepcopy(lock)
        changed[key] = value
        refused(lambda: image_lock.validate(changed, pins, recipe, expected), f"lock {key}")
    for field in ("version", "source_digest"):
        changed = copy.deepcopy(lock)
        changed["layers"][0]["tools"][0][field] = "wrong"
        refused(lambda: image_lock.validate(changed, pins, recipe, expected), f"layer {field}")
    for field in ("recipe_digest", "oci_digest", "extra"):
        changed = copy.deepcopy(lock)
        changed["layers"][0][field] = "wrong"
        refused(lambda: image_lock.validate(changed, pins, recipe, expected), f"layer {field}")
    artifact = {key: lock[key] for key in ("platform", "image_digest", "image_id")}
    artifact["layers"] = [*lock["base_layers"], *lock["layers"]]
    image_lock.verify_artifact(lock, artifact)
    changed = copy.deepcopy(lock)
    changed["image_digest"] = "sha256:" + "e" * 64
    image_lock.validate(changed, pins, recipe, expected)
    refused(lambda: image_lock.verify_artifact(changed, artifact), "unverified image identity")
    changed_pins = copy.deepcopy(pins)
    next(row for row in changed_pins["sources"] if row["tool"] == "litex")["version"] = "different"
    altered = build.layer_records(changed_pins)
    changed_groups = [a["tool"] for a, b in zip(expected, altered, strict=True) if a != b]
    assert changed_groups == ["litex"], changed_groups
    print("PASS: independent layer recipe identities and full lock schema")


def privacy_and_normalization() -> None:
    """Plant host paths in contents/metadata and normalize a dated trust store."""
    planted = b"/home/" + b"fixture-account/private/source.c"
    refused(lambda: image_archive.scan(io.BytesIO(planted), "fixture"), "host source path")
    refused(lambda: image_archive.scan(io.BytesIO(b"x" * (1024 * 1024 - 4) + b"\x00" + planted), "fixture"),
            "host path split across chunks")
    image_archive.scan(io.BytesIO(b"cpan/t/data/snippets/example"), "relative fixture")
    with tempfile.TemporaryDirectory(prefix="image-integrity-") as directory:
        root = Path(directory)
        store = root / "cacerts"
        prefix = struct.pack(">IIIIH", 0xFEEDFEED, 2, 1, 2, 1) + b"a"
        suffix = struct.pack(">H", 5) + b"X.509" + struct.pack(">I", 4) + b"cert" + b"x" * 20
        store.write_bytes(prefix + struct.pack(">Q", 1234) + suffix)
        normalize.java_store(store, 42)
        first = store.read_bytes()
        store.write_bytes(prefix + struct.pack(">Q", 9876) + suffix)
        normalize.java_store(store, 42)
        assert store.read_bytes() == first
        pycache = root / "__pycache__"
        pycache.mkdir()
        (pycache / "fixture.pyc").write_bytes(b"transient")
        with patch("os.chown"):
            normalize.normalize(root, 42)
        assert not pycache.exists()
        assert store.stat().st_mtime == 42
        metadata = root / "ci/image"
        metadata.mkdir(parents=True)
        (metadata / "tool-inventory.json").write_text('{"tools": []}')
        declared = {"runtime": [{"package": "unused", "path": "consumer",
                                 "literal": "not present", "reason": "fixture"}],
                    "recipe": []}
        (metadata / "package_roots.json").write_text(json.dumps(declared))
        (root / "consumer").write_text("no installation")
        refused(lambda: resolve_packages.roots(root), "distribution root without a consumer")
    print("PASS: privacy boundaries and deterministic runtime metadata")


def main() -> int:
    """Keep refusal controls independent of any built image or network."""
    locks()
    privacy_and_normalization()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
