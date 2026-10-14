#!/usr/bin/env python3
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""Validate recipe declarations separately from a measured image identity."""

from __future__ import annotations

import hashlib
import json
import re


def canonical(value: object) -> bytes:
    """Encode declarations without formatting-dependent identity."""
    return json.dumps(value, sort_keys=True, separators=(",", ":")).encode()


def digest(value: object) -> str:
    """Hash a canonical recipe declaration."""
    return hashlib.sha256(canonical(value)).hexdigest()


def identity(value: object, prefix: str = "sha256:") -> bool:
    """Reject malformed and placeholder digests without claiming authentication."""
    return isinstance(value, str) and bool(re.fullmatch(prefix + r"[0-9a-f]{64}", value)) and value != prefix + "0" * 64


def validate(lock: dict[str, object], pins: dict[str, object], recipe: str,
             layers: list[dict[str, object]]) -> None:
    """Validate every required field and recompute all recipe-side layer records."""
    keys = {"schema", "platform", "base", "recipe_digest", "image_digest", "image_id", "base_layers", "layers"}
    if set(lock) != keys or type(lock["schema"]) is not int or lock["schema"] != 2:
        raise ValueError("unsupported or incomplete image lock schema")
    if lock["platform"] != pins["platform"] or lock["base"] != pins["base"]:
        raise ValueError("image lock platform or base differs from source pins")
    if lock["recipe_digest"] != recipe:
        raise ValueError("image lock does not describe the current recipe")
    if not all(identity(lock[name]) for name in ("image_digest", "image_id")):
        raise ValueError("malformed image identity")
    if not isinstance(lock["base_layers"], list) or not lock["base_layers"]:
        raise ValueError("missing base layers")
    if lock["base_layers"] != pins["base_layers"]:
        raise ValueError("base layer records differ from the pinned base")
    for row in lock["base_layers"]:
        if (not isinstance(row, dict) or set(row) != {"oci_digest", "diff_id"}
                or not all(identity(v) for v in row.values())):
            raise ValueError("malformed base layer")
    if not isinstance(lock["layers"], list) or len(lock["layers"]) != len(layers):
        raise ValueError("image lock layer population differs from recipe")
    for actual, expected in zip(lock["layers"], layers, strict=True):
        if not isinstance(actual, dict) or set(actual) != set(expected) | {"oci_digest", "diff_id"}:
            raise ValueError("malformed tool layer record")
        if any(actual[key] != value for key, value in expected.items()):
            raise ValueError(f"image lock layer recipe mismatch: {expected['tool']}")
        if not identity(actual["oci_digest"]) or not identity(actual["diff_id"]):
            raise ValueError("malformed tool layer identity")


def verify_artifact(lock: dict[str, object], artifact: dict[str, object]) -> None:
    """Bind a schema-checked declaration to measured manifest/config/layer bytes."""
    for key in ("image_digest", "image_id", "platform"):
        if lock[key] != artifact[key]:
            raise ValueError(f"image artifact differs from lock: {key}")
    recorded = [*lock["base_layers"], *lock["layers"]]
    measured = artifact["layers"]
    if len(recorded) != len(measured):
        raise ValueError("image artifact layer count differs from lock")
    for row, found in zip(recorded, measured, strict=True):
        if any(row[key] != found[key] for key in ("oci_digest", "diff_id")):
            raise ValueError("image artifact layer identity differs from lock")
