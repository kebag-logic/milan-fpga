#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""nvm_klj3.py - the split placement's saved-state container (KLJ3) and record codec (F07.8 layout 3), #823.

The reference the F1 store (sw/firmware/ctrl_nvm) is graded against, byte
for byte and verdict for verdict. It is the KLJ2 reference (scripts/nvm_klj2.py)
with the three changes of #823 decisions 1 and 2, and nothing else:

  * THE RECORD SPACE is layout 3, read from its one declaration
    (sw/firmware/ctrl_nvm/nvm_layout3.h, through scripts/nvm_layout3.py):
    1,129 ids, every block's base a constant at every shape;
  * THE RECORD FRAME is ten bytes, {magic 0x1722, layout_version 3,
    reserved 0, record_id, payload_length, crc16}, big-endian. The crc16 is
    the donor's CCITT-FALSE over the header without its own two bytes, then
    the payload, as in layout 2;
  * THE CONTAINER is KLJ3: KLJ2's forty header bytes and CRC-32 trailer, with
    the magic 'KLJ3' and the format word's major 3. Its length may reach the
    slot, one half of the 640 KiB journal_klj3 of sw/litex/milan_soc.py. A
    KLJ2 container is the previous format: refused VD_VER, never
    reinterpreted (decision 2).

The all-fabric placement keeps KLJ2 and layout 2; nothing here changes it.
"""

from __future__ import annotations

import struct
import sys
import zlib
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(HERE.parent / "sw/litex"))

import nvm_layout3                                            # noqa: E402
from flash_map import literal                                 # noqa: E402
from nvm_contract import (                                    # noqa: E402
    ALIGN, ERASED, KLJ2_HDR, KLJ2_MAGIC, KLJ2_TRAILER, MAP_ENTRY, NAME_BYTES,
    PAY, REC_MAGIC, VD_BLANK, VD_CRC, VD_ENT, VD_INCOMPLETE, VD_LEN, VD_MAGIC,
    VD_OK, VD_REC, VD_SHAPE, VD_VER, Ident, Key, Record, Shape)
from nvm_klj2 import crc16_ccitt                              # noqa: E402
from nvm_shape import output_map_entries                      # noqa: E402

#: The record space, as declared.
LAYOUT = nvm_layout3.read()
REC_HDR3 = LAYOUT.rec_hdr
KLJ3_MAGIC = 0x334A4C4B     # 'KLJ3' when hexdumped
KLJ3_FMT_VER = 0x0003_0000  # {major, minor}
#: The container's header and trailer: KLJ2's, word for word.
HDR = KLJ2_HDR
TRAILER = KLJ2_TRAILER
#: The split placement's journal, two slots, read as milan_soc.py states it.
JOURNAL = literal("FLASHBOOT_RESERVED")["journal_klj3"]
SLOT = JOURNAL["size"] // 2
#: Acceptance rule 3: a container is never longer than its slot.
KLJ3_MAX = SLOT
#: The channel-map ports the codec's tables hold, per direction.
MAP_PORTS = LAYOUT.block("MAPS_IN").cap

#: group -> the shape count it holds one record per, as the builder's split
#: output (emit_nvm_split) counts it; NAME is the builder's name count.
COUNTED = {"CFG_IDX": None, "SUID": None, "RATE": "AUDIO_UNIT", "CLKSRC": "CLOCK_DOMAIN",
           "MCR": "CLOCK_DOMAIN", "BINDING": "STREAM_INPUT", "FMT_IN": "STREAM_INPUT",
           "FMT_OUT": "STREAM_OUTPUT", "PT_OFS": "STREAM_OUTPUT", "MAPS_IN": "STREAM_PORT_INPUT",
           "MAPS_OUT": "STREAM_PORT_OUTPUT", "NAME": None}


def rid_of_key3(key: Key) -> int:
    """(group, index) -> record_id under layout 3."""
    group, index = key
    return LAYOUT.block(group).base + index


def key_of_id3(rid: int) -> Key | None:
    """record_id -> (group, index) under layout 3; None outside every block."""
    for b in LAYOUT.blocks:
        if b.base <= rid <= b.last:
            return (b.group, rid - b.base)
    return None


def inventory3(shape: Shape) -> list[Record]:
    """Every record of `shape` under layout 3: (group, index, id, payload,
    block), the id None for an index its block cannot reach."""
    dc, recs = shape.dc, []

    def add(group: str, index: int, payload: int) -> None:
        """Append one row, its id None when the group's block cannot reach the index."""
        b = LAYOUT.block(group)
        recs.append((group, index, b.base + index if index < b.cap else None, payload, b.cap))

    add("CFG_IDX", 0, PAY["CFG_IDX"])
    add("SUID", 0, PAY["SUID"])
    for u in range(dc["AUDIO_UNIT"]):
        add("RATE", u, PAY["RATE"])
    for d in range(dc["CLOCK_DOMAIN"]):
        add("CLKSRC", d, PAY["CLKSRC"])
        add("MCR", d, PAY["MCR"])
    for k in range(dc["STREAM_INPUT"]):
        add("BINDING", k, PAY["BINDING"])
        add("FMT_IN", k, PAY["FMT_IN"])
    for i in range(dc["STREAM_OUTPUT"]):
        add("FMT_OUT", i, PAY["FMT_OUT"])
        add("PT_OFS", i, PAY["PT_OFS"])
    for p in shape.spi:
        add("MAPS_IN", p["index"], p["clusters"] * MAP_ENTRY)
    for p in shape.spo:
        add("MAPS_OUT", p["index"], output_map_entries(shape, p) * MAP_ENTRY)
    for n in range(shape.names):
        add("NAME", n, NAME_BYTES)
    return recs


def expected3(shape: Shape) -> dict[Key, int]:
    """{(group, index): payload length} of every record of `shape`."""
    return {(g, i): p for g, i, _r, p, _b in inventory3(shape)}


def erased_record3(plen: int) -> bytes:
    """A record of `plen` payload bytes that was never written: its whole span ERASED."""
    return bytes([ERASED]) * (REC_HDR3 + plen)


def frame_record3(rid: int, payload: bytes) -> bytes:
    """One layout 3 frame: the ten-byte header, then the payload."""
    hdr = struct.pack(">HBBHH", REC_MAGIC, LAYOUT.layout, 0, rid, len(payload))
    return hdr + struct.pack(">H", crc16_ccitt(hdr + payload)) + payload


def klj3_assemble(frames: dict[int, bytes], ident: Ident) -> tuple[bytes, dict[int, int]]:
    """The frames in ascending record_id inside a KLJ3 container: (blob,
    {record_id: offset inside the record area})."""
    body, offs = b"", {}
    for rid in sorted(frames):
        offs[rid] = len(body)
        body += frames[rid]
    body += b"\x00" * ((-len(body)) % ALIGN)
    img_len = HDR + len(body) + TRAILER
    hdr = struct.pack("<10I", KLJ3_MAGIC, KLJ3_FMT_VER, ident.seq, len(frames), img_len,
                      ident.entity_id & 0xFFFFFFFF, (ident.entity_id >> 32) & 0xFFFFFFFF,
                      ident.model_id & 0xFFFFFFFF, (ident.model_id >> 32) & 0xFFFFFFFF,
                      LAYOUT.layout)
    blob = hdr + body
    return blob + struct.pack("<I", zlib.crc32(blob) & 0xFFFFFFFF), offs


def klj3_decode(blob: bytes, ident: Ident, expect: dict[Key, int]) -> tuple[int, dict[Key, bytes]]:
    """Section 6.2 of docs/design/SAVED_STATE_FASTCONNECT.md over a KLJ3
    container: ZERO records unless every test passes. The order and every
    rule are klj2_decode's; what differs is the framing above and that a
    KLJ2 container is the previous format, VD_VER."""
    if len(blob) < HDR + TRAILER:
        return VD_LEN, {}
    if all(b == ERASED for b in blob[:HDR]):
        return VD_BLANK, {}
    magic, ver, _seq, nrec, img_len, elo, ehi, mlo, mhi, rlay = struct.unpack_from("<10I", blob, 0)
    if magic == KLJ2_MAGIC:
        return VD_VER, {}
    if magic != KLJ3_MAGIC:
        return VD_MAGIC, {}
    if (ver >> 16) != (KLJ3_FMT_VER >> 16):
        return VD_VER, {}
    if not (HDR + TRAILER <= img_len <= KLJ3_MAX) or len(blob) != img_len:
        return VD_LEN, {}
    if (zlib.crc32(blob[:-4]) & 0xFFFFFFFF) != struct.unpack_from("<I", blob, img_len - 4)[0]:
        return VD_CRC, {}
    if (elo | (ehi << 32)) != ident.entity_id:
        return VD_ENT, {}
    if (mlo | (mhi << 32)) != ident.model_id:
        return VD_SHAPE, {}
    if rlay != LAYOUT.layout:
        return VD_REC, {}
    applied, pos, end, last = {}, HDR, img_len - TRAILER, -1
    order = sorted((rid_of_key3(k), k) for k in expect)
    erased = set()
    for _ in range(nrec):
        if pos + REC_HDR3 > end:
            return VD_LEN, {}
        if all(b == ERASED for b in blob[pos:pos + REC_HDR3]):
            nxt = next(((r, k) for r, k in order if r > last), None)
            if nxt is None:
                return VD_REC, {}
            rid, key = nxt
            plen = expect[key]
            if pos + REC_HDR3 + plen > end:
                return VD_LEN, {}
            if any(b != ERASED for b in blob[pos + REC_HDR3:pos + REC_HDR3 + plen]):
                return VD_REC, {}
            erased.add(key)
            last = rid
            pos += REC_HDR3 + plen
            continue
        rmagic, rver, rres, rid, plen = struct.unpack_from(">HBBHH", blob, pos)
        rcrc = struct.unpack_from(">H", blob, pos + REC_HDR3 - 2)[0]
        if rmagic != REC_MAGIC or rver != LAYOUT.layout or rres != 0:
            return VD_REC, {}
        if pos + REC_HDR3 + plen > end:
            return VD_LEN, {}
        pay = blob[pos + REC_HDR3:pos + REC_HDR3 + plen]
        if crc16_ccitt(blob[pos:pos + REC_HDR3 - 2] + pay) != rcrc:
            return VD_REC, {}
        if rid <= last:
            return VD_REC, {}
        last = rid
        key = key_of_id3(rid)
        if key is None or key not in expect or expect[key] != plen:
            return VD_REC, {}
        applied[key] = pay
        pos += REC_HDR3 + plen
    if pos + ((-(pos - HDR)) % ALIGN) != end:
        return VD_LEN, {}
    if set(expect) - set(applied) - erased:
        return VD_INCOMPLETE, {}
    return VD_OK, applied


def split_counts(space: dict) -> dict[str, int]:
    """group -> count, from the builder's split output (nvm_split.json)."""
    if space.get("layout") != LAYOUT.layout or space.get("id_space") != LAYOUT.id_space:
        raise ValueError(f"the builder's split output is layout {space.get('layout')} with "
                         f"{space.get('id_space')} ids; this codec is layout {LAYOUT.layout} with "
                         f"{LAYOUT.id_space}")
    counts = {b["group"]: int(b["count"]) for b in space["blocks"]}
    if set(counts) != {b.group for b in LAYOUT.blocks}:
        raise ValueError(f"the builder's split output names the blocks {sorted(counts)}")
    for b in space["blocks"]:
        block = LAYOUT.block(b["group"])
        if b["first_id"] != block.base or b["capacity"] != block.cap:
            raise ValueError(f"the builder's split output places {b['group']} at {b['first_id']} "
                             f"with {b['capacity']} ids; the declaration says {block.base} and {block.cap}")
    return counts


def split_constants(space: dict, shape: Shape) -> dict[str, int]:
    """The MILAN_NVM3_* constants the F1 store is built against: each count
    from the builder's split output, every port's map entries from the shape
    (the #501 rule for an output port), and the two held equal."""
    counts = split_counts(space)
    dc = shape.dc
    seen = {g: (dc[t] if t else (shape.names if g == "NAME" else 1)) for g, t in COUNTED.items()}
    wrong = sorted(g for g in seen if seen[g] != counts[g])
    if wrong:
        raise ValueError(f"the builder's split output counts {[(g, counts[g]) for g in wrong]}; "
                         f"the shape has {[(g, seen[g]) for g in wrong]}")
    out = {
        "MILAN_NVM3_N_STREAM_IN": counts["BINDING"],
        "MILAN_NVM3_N_STREAM_OUT": counts["FMT_OUT"],
        "MILAN_NVM3_N_SPORT_IN": counts["MAPS_IN"],
        "MILAN_NVM3_N_SPORT_OUT": counts["MAPS_OUT"],
        "MILAN_NVM3_N_AUDIO_UNIT": counts["RATE"],
        "MILAN_NVM3_N_CLK_DOM": counts["CLKSRC"],
        "MILAN_NVM3_N_NAME": counts["NAME"],
    }
    for label, ports in (("IN", shape.spi), ("OUT", shape.spo)):
        entries = {p["index"]: (output_map_entries(shape, p) if label == "OUT" else p["clusters"])
                   for p in ports}
        for k in range(MAP_PORTS):
            out[f"MILAN_NVM3_MAP{label}_ENTRIES_{k}"] = entries.get(k, 0)
    return out


def image_bytes(shape: Shape) -> int:
    """The KLJ3 container of every record of `shape`."""
    area = sum(REC_HDR3 + p for _g, _i, _r, p, _b in inventory3(shape))
    return HDR + area + (-area) % ALIGN + TRAILER


def stage_bytes(shape: Shape) -> int:
    """The F1 store's stage for `shape`: its container and one record header
    of look-ahead (sw/firmware/ctrl_nvm/nvm_shape.h NVM_STAGE_BYTES)."""
    return image_bytes(shape) + REC_HDR3
