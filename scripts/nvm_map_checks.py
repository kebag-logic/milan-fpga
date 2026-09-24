#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""Issue #501: output-map capacity on journal bytes and a frozen 1x1 image.

The restore here is a record-level map-store model, not the donor writer or
the product's edit face. It starts with a populated store, clears it, decodes
the complete journal, and restores only decoded entries. Each port is exercised
separately: all keys may belong to any one port, never several simultaneously.
The backend suite independently exercises the resulting spans in actual RTL.
"""

from __future__ import annotations

import hashlib
import struct

from nvm_contract import (MAP_ENTRY, SEAM, VD_OK, VD_REC, VERDICT_NAME,
                          Donor, Ident, Key, Record, Shape)
from nvm_klj2 import (erased_record, frame_record, klj2_assemble, klj2_decode,
                      payload_bytes)

# Captured from the complete deterministic --emit-record-table image at
# 573f0052a0e4412e81f0845438fcec2086ce5d55, before any layout edit. Includes
# header, every record, padding and trailer, with the emit identity below.
BASE_1X1_SHA256 = "103ce107b1402884914036a363055800ad2cd97b8067df41f5cc54be9d3a3aea"
EMIT_IDENT = Ident(7, 0x0011223344556677, 0x8899AABBCCDDEEFF)
UNUSED = b"\xff" * MAP_ENTRY


def check_1x1_digest(shape: Shape, recs: list[Record], donor: Donor) -> list[str]:
    """Compare the actual emitted 1x1 image with the pre-change SHA-256."""
    if shape.cfg.stem != "endstation_ax7101_1x1_tdm8":
        return []
    frames = {}
    for group, index, rid, plen, _block in recs:
        if rid is None or rid > 255:
            return []  # Namespace checks own unframeable inventories.
        payload = payload_bytes(group, index, rid, plen)
        if SEAM.CHANGE_1X1_IMAGE and group == "CFG_IDX":
            payload = bytes([payload[0] ^ 1]) + payload[1:]
        frames[rid] = frame_record(rid, payload, donor.layout)
    blob, _offsets = klj2_assemble(frames, donor, EMIT_IDENT)
    digest = hashlib.sha256(blob).hexdigest()
    if digest != BASE_1X1_SHA256:
        return [f"{shape.cfg.stem}: 1x1 image digest changed: {digest}; "
                f"pre-change emit {BASE_1X1_SHA256}"]
    return []


def _restore(payload: bytes) -> dict[tuple[int, int], tuple[int, int]]:
    """Decode packed AEM mappings; reject holes and duplicate stream keys."""
    restored = {}
    unused_seen = False
    for pos in range(0, len(payload), MAP_ENTRY):
        entry = payload[pos:pos + MAP_ENTRY]
        if entry == UNUSED:
            unused_seen = True
            continue
        if unused_seen or len(entry) != MAP_ENTRY:
            raise ValueError("noncanonical map tail")
        stream, channel, cluster, cluster_channel = struct.unpack(">4H", entry)
        if (stream, channel) in restored:
            raise ValueError("duplicate stream/channel key")
        restored[stream, channel] = (cluster, cluster_channel)
    return restored


def _round_trip_map(shape: Shape, recs: list[Record], donor: Donor,
                    expect: dict[Key, int], target: Record, count: int) -> list[str]:
    """Save one fan-out set; clear its store; restore from a decoded journal."""
    group, port, rid, plen, _block = target
    keys = [(stream, channel) for stream in range(shape.dc["STREAM_OUTPUT"])
            for channel in range(8)][:count]
    # Every key feeds from one cluster, so cluster count cannot bound fan-out.
    wanted = dict.fromkeys(keys, (0, 0))
    payload = b"".join(struct.pack(">4H", *key, *value)
                       for key, value in wanted.items())
    if len(payload) > plen:
        return [f"{shape.cfg.stem}: output-record capacity: {group}[{port}] "
                f"cannot save {count} keys in {plen // MAP_ENTRY} entries"]
    payload += UNUSED * ((plen - len(payload)) // MAP_ENTRY)
    frames = {r: erased_record(p) for _g, _i, r, p, _b in recs if r is not None}
    frames[rid] = frame_record(rid, payload, donor.layout)
    blob, _ = klj2_assemble(frames, donor, EMIT_IDENT)
    live = dict(wanted)
    live.clear()
    if live:
        return [f"{shape.cfg.stem}: map store was not cleared before restore"]
    verdict, applied = klj2_decode(blob, donor, EMIT_IDENT, expect)
    if verdict != VD_OK or set(applied) != {(group, port)}:
        return [f"{shape.cfg.stem}: output-record capacity: {group}[{port}] "
                f"journal decode {VERDICT_NAME[verdict]}, {len(applied)} applied"]
    live.update(_restore(applied[group, port]))
    if live != wanted:
        return [f"{shape.cfg.stem}: cleared-first map restore lost keys on port {port}"]
    # One more than capacity is a CRC-clean framed record, but not this layout.
    # The decoder must refuse the whole journal with zero records applied.
    frames[rid] = frame_record(rid, payload + struct.pack(">4H", len(keys), 0, 0, 0),
                               donor.layout)
    oversized, _ = klj2_assemble(frames, donor, EMIT_IDENT)
    verdict, applied = klj2_decode(oversized, donor, EMIT_IDENT, expect)
    if verdict != VD_REC or applied:
        return [f"{shape.cfg.stem}: over-capacity journal was not refused atomically"]
    return []


def check_output_maps(shape: Shape, recs: list[Record], donor: Donor,
                      expect: dict[Key, int]) -> list[str]:
    """Grade full key-space and old-capacity-plus-one sets for every grown port."""
    if any(r is None or r > 255 for _g, _i, r, _p, _b in recs):
        return []
    targets = {row[1]: row for row in recs if row[0] == "MAPS_OUT"}
    findings = []
    for port in shape.spo:
        keys = shape.dc["STREAM_OUTPUT"] * 8
        if port.get("map_mode") != "dynamic" or keys <= port["clusters"]:
            continue
        target = targets.get(port["index"])
        if target is None:
            continue  # The independent key-set oracle owns missing records.
        for count in (port["clusters"] + 1, keys):
            findings += _round_trip_map(shape, recs, donor, expect, target, count)
    return findings
