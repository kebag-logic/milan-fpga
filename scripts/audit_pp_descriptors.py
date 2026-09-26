#!/usr/bin/env python3
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""Measure the shipping descriptor contract without changing its enforcement.

Emit decoded packed bytes and isolated probes for the #509 ownership audit.
Accepted invalid inputs are findings, never compliance passes. This command
does not replace the builder gates or certify arbitrary descriptor models.
"""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
from pathlib import Path
import struct
import subprocess
import sys
import tempfile
from typing import Any
from unittest.mock import patch

import yaml

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "sw" / "builder"))
sys.path.insert(0, str(ROOT / "avdecc"))
import endstation_builder as builder  # noqa: E402
import gen_aemi_image as join  # noqa: E402
import aem_assemble as assemble  # noqa: E402
import aem_descriptors as descriptors  # noqa: E402


class AuditError(RuntimeError):
    """Refuse untrustworthy evidence, independently of measured model refusals."""


def uint(data: bytes, offset: int, width: int = 2) -> int:
    """Read one complete big-endian field, refusing truncated evidence."""
    if offset < 0 or offset + width > len(data):
        raise ValueError(f"field {offset}+{width} outside {len(data)} bytes")
    return int.from_bytes(data[offset:offset + width], "big")


def packed_rows(blob: bytes) -> list[dict[str, Any]]:
    """Decode the actual index map, including repeated unequal-length runs."""
    if blob[:4] != b"AEMI" or uint(blob, 4) != 1:
        raise AuditError("invalid image magic or version")
    if uint(blob, 20, 4) != len(blob):
        raise AuditError("declared image length differs from packed bytes")
    if sum(struct.unpack_from(">8I", blob)) & 0xFFFFFFFF != 0xFFFFFFFF:
        raise AuditError("invalid image header checksum")
    rows = []
    next_index: dict[tuple[int, int], int] = {}
    for row in range(uint(blob, 8)):
        at = uint(blob, 12, 4) + 16 * row
        cfg, dtype, count, length, base, name, stride = struct.unpack_from(
            ">HHHHIHH", blob, at)
        key = (cfg, dtype)
        first = next_index.get(key, 0)
        for index in range(count):
            offset = base + index * stride
            data = blob[offset:offset + length]
            if len(data) != length:
                raise AuditError("descriptor extends beyond packed image")
            if (uint(data, 0), uint(data, 2)) != (dtype, first + index):
                raise AuditError("descriptor body type/index differs from directory")
            rows.append(dict(configuration=cfg, type=dtype, index=first + index,
                             image_offset=offset, length=length, stride=stride,
                             name_base=name, fields=descriptor_fields(dtype, data)))
        next_index[key] = first + count
    return rows


def descriptor_fields(dtype: int, data: bytes) -> dict[str, Any]:
    """Decode clause 7.2 fields independently of the descriptor constructors."""
    if dtype == 0:
        return dict(entity_id=f"0x{uint(data, 4, 8):016X}",
                    model_id=f"0x{uint(data, 12, 8):016X}",
                    capabilities=f"0x{uint(data, 20, 4):08X}",
                    talker_sources=uint(data, 24), talker_caps=uint(data, 26),
                    listener_sinks=uint(data, 28), listener_caps=uint(data, 30),
                    configurations=uint(data, 308), current_config=uint(data, 310))
    if dtype == 1:
        offset, count = uint(data, 72), uint(data, 70)
        return dict(counts_offset=offset, counts_count=count,
                    counts=[list(struct.unpack_from(">HH", data, offset + 4 * i))
                            for i in range(count)])
    if dtype == 2:
        offset, count = uint(data, 140), uint(data, 142)
        return dict(rates_offset=offset, rates_count=count,
                    current_rate=uint(data, 136, 4),
                    rates=[uint(data, offset + 4 * i, 4) for i in range(count)],
                    input_ports=[uint(data, 72), uint(data, 74)],
                    output_ports=[uint(data, 76), uint(data, 78)])
    if dtype in (5, 6):
        offset, count = uint(data, 82), uint(data, 84)
        return dict(formats_offset=offset, formats_count=count,
                    flags=uint(data, 72), current_format=f"0x{uint(data, 74, 8):016X}",
                    formats=[f"0x{uint(data, offset + 8 * i, 8):016X}" for i in range(count)],
                    buffer_ns=uint(data, 128, 4), redundant_offset=uint(data, 132),
                    redundant_count=uint(data, 134), timing=uint(data, 136))
    if dtype == 9:
        return dict(port_number=uint(data, 96), mac=data[70:76].hex(),
                    clock_identity=data[78:86].hex(), controls=uint(data, 98))
    if dtype == 10:
        return dict(source_type=uint(data, 72), location_type=uint(data, 82),
                    location_index=uint(data, 84))
    if dtype in (14, 15):
        return dict(clusters=uint(data, 12), base_cluster=uint(data, 14),
                    maps=uint(data, 16), base_map=uint(data, 18))
    if dtype == 20:
        return dict(channel_count=uint(data, 84))
    if dtype == 23:
        offset, count = uint(data, 4), uint(data, 6)
        return dict(mappings_offset=offset, mappings_count=count,
                    mappings=[list(struct.unpack_from(">4H", data, offset + 8 * i))
                              for i in range(count)])
    if dtype == 26:
        return dict(control_type=f"0x{uint(data, 82, 8):016X}",
                    reset_time=uint(data, 90, 4), values_offset=uint(data, 94))
    if dtype == 36:
        offset, count = uint(data, 72), uint(data, 74)
        return dict(sources_offset=offset, sources_count=count,
                    sources=[uint(data, offset + 2 * i) for i in range(count)])
    return {}


def generate(cfg: dict[str, Any]) -> tuple[dict[str, Any], bytes]:
    """Use the real parent join and the pinned processor packer."""
    overlay = builder.emit_aem_overlay(cfg)
    model = join.aem.build_model(join.aem.spec_from_overlay(overlay))
    document = join.model_to_document(model, join.identity_from_overlay(overlay))
    blob, _ = join.image.build(document, 576)
    if blob != builder._entity_model_image(cfg, overlay)["aem_desc.bin"]:
        raise AuditError("audit image differs from builder image")
    return document, blob


def tracked_configs() -> list[Path]:
    """Use Git's tracked population; scratch YAML never becomes evidence."""
    result = subprocess.run(
        ["git", "ls-files", "configs/endstation_*.yaml"], cwd=ROOT,
        check=True, capture_output=True, text=True)
    return [ROOT / name for name in sorted(result.stdout.splitlines())]


def document_row(document: dict[str, Any], dtype: int, index: int = 0) -> dict[str, Any]:
    """Locate a row by its externally declared type and descriptor index."""
    return next(row for row in document["descriptors"]
                if row["type"] == dtype and row["index"] == index)


def change_field(document: dict[str, Any], dtype: int, offset: int,
                 value: int, width: int = 2) -> None:
    """Change exactly one field in a fresh document's descriptor bytes."""
    row = document_row(document, dtype)
    data = bytearray.fromhex(row["bytes"])
    data[offset:offset + width] = value.to_bytes(width, "big")
    row["bytes"] = data.hex()


def resize_list(document: dict[str, Any], dtype: int, count: int) -> None:
    """Keep offset, count and extent consistent while changing list size."""
    row = document_row(document, dtype)
    data = bytearray.fromhex(row["bytes"])
    if dtype == 2:
        data = data[:144] + b"".join((48000 + i).to_bytes(4, "big") for i in range(count))
        data[142:144] = count.to_bytes(2, "big")
    else:
        data = data[:138] + data[138:146] * count
        data[84:86] = count.to_bytes(2, "big")
        data[132:134] = (138 + 8 * count).to_bytes(2, "big")
    row["bytes"] = data.hex()


def assert_packed_bytes(document: dict[str, Any], blob: bytes) -> None:
    """Prove accepted probes reached the packed image without normalization."""
    seen: dict[tuple[int, int], int] = {}
    for row in range(uint(blob, 8)):
        at = uint(blob, 12, 4) + 16 * row
        cfg, dtype, count, length, base, _, stride = struct.unpack_from(
            ">HHHHIHH", blob, at)
        first = seen.get((cfg, dtype), 0)
        for index in range(count):
            expected = document_row(document, dtype, first + index)
            offset = base + index * stride
            if blob[offset:offset + length] != bytes.fromhex(expected["bytes"]):
                raise AuditError(f"packer changed descriptor bytes: type {dtype}, "
                                 f"index {first + index}")
        seen[(cfg, dtype)] = first + count


def packer_probes(document: dict[str, Any]) -> list[dict[str, Any]]:
    """Measure packer acceptance, with each mutation starting from pristine bytes."""
    cases = [
        ("control", "pristine shipping document", lambda d: None),
        ("L1", "output port shares input cluster block", lambda d: change_field(d, 15, 14, 0)),
        ("L2", "metadata index gap", lambda d: document_row(d, 10, 1).update(index=2)),
        ("L2", "duplicate row", lambda d: d["descriptors"].append(copy.deepcopy(d["descriptors"][0]))),
        ("packing", "ENTITY name differs from name table", lambda d: change_field(d, 0, 48, 0, 1)),
        ("L2", "wire index differs from metadata", lambda d: change_field(d, 10, 2, 9)),
        ("L2", "wire type differs from metadata", lambda d: change_field(d, 10, 0, 9)),
        ("L4", "buffer at 2126000 ns", lambda d: change_field(d, 5, 128, 2126000, 4)),
        ("L4", "buffer one ns below floor", lambda d: change_field(d, 5, 128, 2125999, 4)),
        ("L4", "CLASS_A cleared", lambda d: change_field(d, 5, 72, 1)),
        ("L4", "current format outside list", lambda d: change_field(d, 5, 74, 0, 8)),
        ("L4", "mixed AAF and CRF formats", lambda d: change_field(d, 5, 146, 0x041060010000BB80, 8)),
        ("L4", "47 formats at Table 7-8 cap", lambda d: resize_list(d, 5, 47)),
        ("L4", "48 formats below line-buffer cap", lambda d: resize_list(d, 5, 48)),
        ("L6", "source list reversed", lambda d: document_row(d, 36).update(
            bytes=document_row(d, 36)["bytes"][:-8] + "00010000")),
        ("L7", "input port declares a static map", lambda d: change_field(d, 14, 16, 1)),
        ("L7", "cluster channel_count two", lambda d: change_field(d, 20, 84, 2)),
        ("L7", "duplicate output stream channel", lambda d: change_field(d, 23, 18, 0)),
        ("L8", "CONTROL is not IDENTIFY", lambda d: change_field(d, 26, 82, 0, 8)),
        ("L9", "zero model ID", lambda d: change_field(d, 0, 12, 0, 8)),
        ("L9", "all-ones model ID", lambda d: change_field(d, 0, 12, 0xFFFFFFFFFFFFFFFF, 8)),
        ("L10", "eight full rate words", lambda d: resize_list(d, 2, 8)),
        ("L10", "nine full rate words", lambda d: resize_list(d, 2, 9)),
        ("L10", "offset 143", lambda d: change_field(d, 2, 140, 143)),
        ("L10", "count disagrees with extent", lambda d: change_field(d, 2, 142, 4)),
        ("L10", "one byte short", lambda d: document_row(d, 2).update(
            bytes=document_row(d, 2)["bytes"][:-2])),
        ("ADP", "ENTITY talker count disagrees", lambda d: change_field(d, 0, 24, 2)),
        ("ADP", "ENTITY listener count disagrees", lambda d: change_field(d, 0, 28, 3)),
    ]
    results = []
    for rule, label, mutate in cases:
        candidate = copy.deepcopy(document)
        mutate(candidate)
        try:
            blob, _ = join.image.build(candidate, 576)
            assert_packed_bytes(candidate, blob)
            results.append(dict(rule=rule, probe=label, result="accepted", image_bytes=len(blob)))
        except join.image.ImageError as exc:
            results.append(dict(rule=rule, probe=label, result="refused", reason=str(exc)))
    for length in (576, 577):
        opaque = dict(format="kl-aem-image", version=1, names=[], descriptors=[
            dict(configuration=0, type=0xFFFE, index=0,
                 bytes=(bytes.fromhex("fffe0000") + bytes(length - 4)).hex())])
        try:
            join.image.build(opaque, 576)
            results.append(dict(rule="packing", probe=f"opaque {length}-byte row", result="accepted"))
        except join.image.ImageError as exc:
            results.append(dict(rule="packing", probe=f"opaque {length}-byte row",
                                result="refused", reason=str(exc)))
    return results


def config_probes(path: Path) -> list[dict[str, Any]]:
    """Measure real loader and image refusals without writing tracked inputs."""
    eight = [192000, 96000, 44100, 88200, 176400, 32000, 24000, 48000]
    cases = [
        ("control", "unchanged YAML", lambda c: None),
        ("L3", "empty listener list", lambda c: c["streams"].update(listeners=[])),
        ("L4", "buffer one ns below floor", lambda c:
         c["streams"]["listeners"][0].update(buffer_length_ns=2125999)),
        ("L4", "non-Milan CRF word", lambda c:
         c["clocking"].update(crf_format="0x041060010000BB81")),
        ("L4", "48 AAF output formats", lambda c:
         c["streams"]["talkers"][0].update(formats=["0x0205022000806000"] * 48)),
        ("L4", "mixed output format families", lambda c:
         c["streams"]["talkers"][0].update(formats=["0x0205022000806000", "0x041060010000BB80"])),
        ("L6", "outputs without INTERNAL", lambda c:
         c["clocking"].update(media_clock_sources=["crf"], default_source="crf")),
        ("L7", "static input map", lambda c: c["streams"]["listeners"][0].update(map_mode="static")),
        ("L9", "zero model ID pin", lambda c:
         c["entity"].update(model_id_pin="0x0000000000000000")),
        ("L9", "all-ones model ID pin", lambda c:
         c["entity"].update(model_id_pin="0xFFFFFFFFFFFFFFFF")),
        ("L10", "eight distinct rates", lambda c: c["clocking"].update(audio_unit_rates_hz=eight)),
        ("L10", "nine distinct rates", lambda c: c["clocking"].update(audio_unit_rates_hz=eight + [22050])),
        ("L10", "duplicate rates", lambda c: c["clocking"].update(audio_unit_rates_hz=[48000, 48000])),
    ]
    results = []
    for rule, label, mutate in cases:
        raw = yaml.safe_load(path.read_text())
        mutate(raw)
        row = dict(rule=rule, probe=label)
        with tempfile.TemporaryDirectory(prefix="descriptor-probe-") as scratch:
            candidate = Path(scratch) / "config.yaml"
            candidate.write_text(yaml.safe_dump(raw))
            try:
                cfg = builder.load_config(candidate)
            except builder.ConfigError as exc:
                row.update(loader="refused", reason=str(exc))
            else:
                row["loader"] = "accepted"
                try:
                    _, blob = generate(cfg)
                    row.update(image="accepted", image_bytes=len(blob), rows=packed_rows(blob))
                except (ValueError, join.image.ImageError) as exc:
                    row.update(image="refused", reason=str(exc))
        results.append(row)
    return results


def map_probes() -> list[dict[str, Any]]:
    """Exercise the existing parent map checker with cause-specific fixtures."""
    results = []
    for label, mutate in (
        ("legal output fanout", lambda s: s["audio_maps"].__setitem__(
            1, [[0, 0, 0, 0], [0, 1, 0, 0]])),
        ("duplicate output stream channel", lambda s: s["audio_maps"].__setitem__(
            1, [[0, 0, 0, 0], [0, 0, 1, 0]])),
    ):
        spec = join.aem._map_fixture()
        mutate(spec)
        try:
            join.aem.build_model(spec)
            results.append(dict(probe=label, result="accepted"))
        except ValueError as exc:
            results.append(dict(probe=label, result="refused", reason=str(exc)))
    return results


def identity_probe(path: Path) -> dict[str, Any]:
    """Reload the same input with a generator-owned field changed in memory."""
    cfg = builder.load_config(path)
    _, before = generate(cfg)
    original = assemble.d_control_identify

    def changed(*args: Any, **kwargs: Any) -> bytes:
        """Plant the known reset_time residue in memory only."""
        data = bytearray(original(*args, **kwargs))
        data[90:94] = (3).to_bytes(4, "big")
        return bytes(data)

    with patch.object(descriptors, "d_control_identify", changed), \
            patch.object(assemble, "d_control_identify", changed):
        _, after = generate(builder.load_config(path))
    return dict(model_id=cfg["entity"]["entity_model_id"],
                model_id_source=cfg["model_id"]["source"],
                before_sha256=hashlib.sha256(before).hexdigest(),
                after_sha256=hashlib.sha256(after).hexdigest(),
                changed_image_offsets=[i for i, (a, b) in enumerate(zip(before, after)) if a != b],
                before_entity=packed_rows(before)[0]["fields"],
                after_entity=packed_rows(after)[0]["fields"])


def check_identity_probe(path: Path) -> None:
    """Require the probe to detect a simulated identity-coverage repair."""
    original = builder.model_shape

    def including_identify(cfg: dict[str, Any]) -> dict[str, Any]:
        """Add generator-owned bytes to the real identity derivation input."""
        return dict(original(cfg), audit_identify=descriptors.d_control_identify().hex())

    with patch.object(builder, "model_shape", including_identify):
        result = identity_probe(path)
    if result["before_entity"]["model_id"] == result["after_entity"]["model_id"]:
        raise AuditError("identity probe missed changed generator bytes in model identity")


def main() -> None:
    """Print a reproducible measurement; no production policy changes."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    configs = []
    documents = {}
    for path in tracked_configs():
        cfg = builder.load_config(path)
        document, blob = generate(cfg)
        documents[path.stem] = document
        configs.append(dict(config=str(path.relative_to(ROOT)),
                            image_bytes=len(blob), sha256=hashlib.sha256(blob).hexdigest(),
                            model_id=cfg["model_id"], adp=builder.adp_shape(cfg),
                            rows=packed_rows(blob)))
    current = ROOT / "configs" / "endstation_arty_current.yaml"
    hashed = ROOT / "configs" / "endstation_arty_4x4.yaml"
    check_identity_probe(hashed)
    report = dict(configurations=configs,
                  packer_probes=packer_probes(documents[current.stem]),
                  config_probes=config_probes(current),
                  map_probes=map_probes(),
                  identity_probe=identity_probe(hashed),
                  multi_configuration="NOT RUN: every shipping image has one configuration")
    args.output.write_text(json.dumps(report, indent=2) + "\n")
    print(f"Measured {len(configs)} configurations; results: {args.output}")


if __name__ == "__main__":
    main()
