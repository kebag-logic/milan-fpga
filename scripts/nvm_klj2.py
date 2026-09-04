#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""nvm_klj2.py - the KLJ2 container and F07.8 record codec.

The instrument `check_nvm_record_space.py` asks its questions with: assemble
the persisted set into the image the ACMP NVM shadow would store, and read it
back through the section 6.2 acceptance rules. It is a leaf - it imports the
contract and nothing else in this gate - so the bytes can be exercised
without the checks, and the checks cannot quietly become a restatement of the
encoder.
"""

from __future__ import annotations

import struct
import sys
import zlib
from collections.abc import Callable
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from nvm_contract import (                                    # noqa: E402
    ALIGN, ALLOC, FIXED, KLJ2_FMT_VER, KLJ2_HDR, KLJ2_MAGIC, KLJ2_TRAILER,
    NAME_BYTES, REC_HDR, REC_MAGIC, SEAM, VD_BLANK, VD_CRC, VD_ENT,
    VD_INCOMPLETE, VD_LEN, VD_MAGIC, VD_OK, VD_REC, VD_SHAPE, VD_VER,
    VENDOR_DEFAULT_NAME, Donor, Ident, Key)


# ---- the KLJ2 codec: this gate now builds the image and reads it back -----
#
# Rounds 1, 2 and 3 all found the same class of hole -- a check that reasons
# about the persisted set as counts or tables and therefore cannot see WHICH
# items it counted. Bytes settle every one of those questions, so the codec
# below is the instrument, and the checks are asked of an image rather than of
# a list.

_CRC16_TAB = []
for _b in range(256):
    _c = _b << 8
    for _ in range(8):
        _c = ((_c << 1) ^ 0x1021) & 0xFFFF if _c & 0x8000 else (_c << 1) & 0xFFFF
    _CRC16_TAB.append(_c)


def crc16_ccitt(data: bytes, crc: int = 0xFFFF) -> int:
    """CCITT-FALSE (poly 0x1021, init 0xFFFF), the donor's `crc16_f()` in
    `KL_acmp_nvm_shadow.sv`, table-driven so the omission sweep is affordable."""
    for b in data:
        crc = ((crc << 8) & 0xFFFF) ^ _CRC16_TAB[((crc >> 8) ^ b) & 0xFF]
    return crc


def id_blocks(base: int) -> list[tuple[str, int | None, int]]:
    """(group, base, block) for every allocated group, BINDING resolved."""
    return [(g, base if g == "BINDING" else b, blk)
            for g, (b, blk) in ALLOC.items()]


def key_of_id(rid: int, base: int, flat: bool) -> Key | None:
    """Invert the section 4.2 allocation: record_id -> (group, index)."""
    for g, b, blk in id_blocks(base):
        if b is not None and b <= rid < b + blk:
            return ("NAME", rid - b) if (flat and g == "NAMES_BANK") \
                else (g, rid - b)
    return None


def frame_record(rid: int, payload: bytes, layout: int) -> bytes:
    """One F07.8 frame: {magic 0x1722, layout_version, record_id,
    payload_length, crc16} big-endian, then the payload. The crc16 covers the
    header without its own two bytes and then the payload -- the donor's
    "header-sans-crc + payload" accumulate."""
    hdr = struct.pack(">HBBH", REC_MAGIC, layout, rid, len(payload))
    return hdr + struct.pack(">H", crc16_ccitt(hdr + payload)) + payload


def klj2_assemble(frames: dict[int, bytes], donor: Donor,
                  ident: Ident) -> tuple[bytes, dict[int, int]]:
    """Concatenate framed records in ASCENDING record_id (section 6.1) and wrap
    them in the container. Returns (blob, {record_id: offset inside the record
    area}) -- the offsets tb/verilator/nvm_backend grades the RTL against."""
    entity_id, model_id = ident.entity_id, ident.model_id
    body, offs = b"", {}
    for rid in sorted(frames):
        offs[rid] = len(body)
        body += frames[rid]
    body += b"\x00" * ((-len(body)) % ALIGN)
    img_len = KLJ2_HDR + len(body) + KLJ2_TRAILER
    hdr = struct.pack("<10I", KLJ2_MAGIC, KLJ2_FMT_VER, ident.seq, len(frames),
                      img_len,
                      entity_id & 0xFFFFFFFF, (entity_id >> 32) & 0xFFFFFFFF,
                      model_id & 0xFFFFFFFF, (model_id >> 32) & 0xFFFFFFFF,
                      donor.layout)
    blob = hdr + body
    return blob + struct.pack("<I", zlib.crc32(blob) & 0xFFFFFFFF), offs


def klj2_decode(blob: bytes, donor: Donor, ident: Ident,
                expect: dict[Key, int],
                flat: bool) -> tuple[int, dict[Key, bytes]]:
    """Apply ZERO records unless every section 6.2 test passes.

    `expect` is the exact per-shape mandatory set, {(group, index): payload
    length}, derived from the LEDGER and the descriptor shape rather than from
    the image. Round 3's acceptance order validated only the records that were
    PRESENT and said in as many words that an allocated id which is simply
    absent is not a failure, so a CRC-clean image could omit any mandatory
    item, publish an accepted sequence and silently restore a changed value to
    its vendor default. That sentence is withdrawn; absence is now VD_INCOMPLETE.
    """
    layout, base = donor.layout, donor.base
    entity_id, model_id = ident.entity_id, ident.model_id
    if len(blob) < KLJ2_HDR + KLJ2_TRAILER:
        return VD_LEN, {}
    if all(b == 0xFF for b in blob):
        return VD_BLANK, {}
    magic, ver, _seq, nrec, img_len, elo, ehi, mlo, mhi, rlay = \
        struct.unpack_from("<10I", blob, 0)
    if magic != KLJ2_MAGIC:
        return VD_MAGIC, {}
    if (ver >> 16) != (KLJ2_FMT_VER >> 16):
        return VD_VER, {}
    if not (44 <= img_len <= 65536) or len(blob) != img_len:
        return VD_LEN, {}
    if (zlib.crc32(blob[:-4]) & 0xFFFFFFFF) != \
            struct.unpack_from("<I", blob, img_len - 4)[0]:
        return VD_CRC, {}
    if (elo | (ehi << 32)) != entity_id:
        return VD_ENT, {}
    if (mlo | (mhi << 32)) != model_id:
        return VD_SHAPE, {}
    if rlay != layout:
        return VD_REC, {}

    applied, pos, end, last = {}, KLJ2_HDR, img_len - KLJ2_TRAILER, -1
    for _ in range(nrec):
        if pos + REC_HDR > end:
            return VD_LEN, {}
        rmagic, rver, rid, plen = struct.unpack_from(">HBBH", blob, pos)
        rcrc = struct.unpack_from(">H", blob, pos + 6)[0]
        if rmagic != REC_MAGIC or rver != layout:
            return VD_REC, {}
        if pos + REC_HDR + plen > end:
            return VD_LEN, {}
        pay = blob[pos + REC_HDR:pos + REC_HDR + plen]
        if crc16_ccitt(blob[pos:pos + 6] + pay) != rcrc:
            return VD_REC, {}
        if rid <= last:                     # section 6.1: ascending, normative
            return VD_REC, {}
        last = rid
        key = key_of_id(rid, base, flat)
        if key is None or key not in expect or expect[key] != plen:
            return VD_REC, {}
        applied[key] = pay
        pos += REC_HDR + plen
    if pos + ((-(pos - KLJ2_HDR)) % ALIGN) != end:
        return VD_LEN, {}
    if set(expect) - set(applied) and not SEAM.DECODE_ALLOW_ABSENT:
        return VD_INCOMPLETE, {}
    return VD_OK, applied


def name_table(n_names: int,
               overrides: dict[int, bytes] | None = None) -> Callable[[int], bytes]:
    """ordinal -> the 64-byte AEM string the entity currently holds.

    A name is a fixed 64-byte NUL-padded AEM string and `SET_NAME` writes all
    eight 64-bit lanes with no non-zero requirement, so EVERY 64-byte value is
    legal -- including all zeros, which is the empty string.
    """
    over = overrides or {}

    def val(ordinal: int) -> bytes:
        """The 64 bytes this ordinal holds: an override, the vendor default,
        or the all-zero tail of the last bank past the shape's last name."""
        if ordinal in over:
            return over[ordinal]
        if ordinal >= n_names:
            return b"\x00" * NAME_BYTES       # unused tail of the last bank
        return (VENDOR_DEFAULT_NAME + b" %d" % ordinal)[:NAME_BYTES] \
            .ljust(NAME_BYTES, b"\x00")
    return val


def payload_bytes(group: str, index: int, rid: int, plen: int,
                  nval: Callable[[int], bytes] | None = None) -> bytes:
    """Deterministic record content.

    With `nval`, a name bank is the eight 64-byte slots of ordinals
    8*index .. 8*index+7. Without it every record follows one arithmetic rule,
    which is the form `--emit-record-table` publishes: the C++ in
    tb/verilator/nvm_backend regenerates the same bytes independently, so a
    disagreement about WHERE a record starts shows up as a byte mismatch
    instead of as agreement about nothing.
    """
    if group == "NAMES_BANK" and nval is not None:
        return b"".join(nval(index * FIXED.NAMES_PER_BANK + slot)
                        for slot in range(FIXED.NAMES_PER_BANK))
    return bytes(((rid * 131 + j * 17) & 0xFF) for j in range(plen))


def names_from_image(applied: dict[Key, bytes],
                     n_names: int) -> dict[int, bytes]:
    """ordinal -> 64 bytes, for the ordinals THIS SHAPE has.

    Presence is a property of the SHAPE, never of the content. Ordinal
    >= n_names maps to no descriptor, so the tail of the last bank is never
    read, and an all-zero slot INSIDE the shape is therefore the empty name --
    a legal value Milan 5.3.13 requires to survive -- rather than an absence.
    """
    if SEAM.NAMES_TAIL_FROM_CONTENT:
        n_names = 0
        for (g, i), pay in applied.items():
            if g != "NAMES_BANK":
                continue
            for slot in range(FIXED.NAMES_PER_BANK):
                if any(pay[slot * NAME_BYTES:(slot + 1) * NAME_BYTES]):
                    n_names = max(n_names, i * FIXED.NAMES_PER_BANK + slot + 1)
    out = {}
    for k in range(n_names):
        bank, slot = divmod(k, FIXED.NAMES_PER_BANK)
        pay = applied.get(("NAMES_BANK", bank))
        if pay is None:
            continue
        v = pay[slot * NAME_BYTES:(slot + 1) * NAME_BYTES]
        if SEAM.NAME_PRESENCE_FROM_CONTENT and not any(v):
            continue                        # round 3: "no name stored"
        out[k] = v
    return out
