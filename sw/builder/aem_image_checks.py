# SPDX-License-Identifier: CERN-OHL-W-2.0
"""Shipping L6/L10 checks on packed bytes, independent of model construction.

The processor packer owns generic image integrity. This reader follows its
version-1 index map, including repeated runs, and excludes stride padding.
Field positions are IEEE 1722.1-2021 7.2.3 and 7.2.32 wire positions, not
values imported from the constructors or recovered from the YAML model.
"""
import ast
from functools import cache
from pathlib import Path
import struct


class ImageCheckError(ValueError):
    """An emitted descriptor violates its shipping consumer contract."""


@cache
def _sampling_rate_walk() -> tuple[int, int]:
    """Derive the immediate-address walk from the pinned consumer, without executing it."""
    path = Path(__file__).resolve().parents[2] / "protocol-processor/hdl/aecp/ucode/gen_ucode.py"
    wanted = {"SSR_LIST_OFF", "SSR_WALK_MAX"}
    values = {}
    for node in ast.parse(path.read_text()).body:
        if not isinstance(node, ast.Assign):
            continue
        for target in node.targets:
            if isinstance(target, ast.Name) and target.id in wanted:
                if (target.id in values or not isinstance(node.value, ast.Constant)
                        or type(node.value.value) is not int or node.value.value <= 0):
                    raise ImageCheckError(f"L10_CONSUMER: cannot derive {target.id}")
                values[target.id] = node.value.value
    if values.keys() != wanted:
        raise ImageCheckError("L10_CONSUMER: missing sampling-rate walk constants")
    return values["SSR_LIST_OFF"], values["SSR_WALK_MAX"]


def _audio_unit(data: bytes, who: str, list_offset: int, walk_count: int) -> None:
    """Compare the declared rate list with its actual unpadded descriptor extent."""
    # 7.2.3: current_sampling_rate at 136, then two u16 list fields at 140.
    fields_end = 140 + struct.calcsize(">HH")
    if len(data) < fields_end:
        raise ImageCheckError(f"L10_HEADER: {who}: missing sampling-rate fields")
    offset, count = struct.unpack_from(">HH", data, 140)
    if offset != list_offset:
        raise ImageCheckError(f"L10_OFFSET: {who}: offset {offset}, consumer reads {list_offset}")
    if not count:
        raise ImageCheckError(f"L10_EMPTY: {who}: no sampling rates (Milan 5.3.3.3)")
    if count > walk_count:
        raise ImageCheckError(f"L10_COUNT: {who}: count {count} exceeds consumer walk {walk_count}")
    word_bytes = struct.calcsize(">I")  # Full sampling-rate word, including pull bits.
    extent_words, partial_bytes = divmod(len(data) - list_offset, word_bytes)
    if partial_bytes:
        raise ImageCheckError(f"L10_PARTIAL_WORD: {who}: rate extent ends with {partial_bytes} byte(s)")
    elif extent_words < count:
        raise ImageCheckError(f"L10_COUNT_EXTENT: {who}: count {count}, only {extent_words} whole words")
    elif extent_words > count:
        raise ImageCheckError(f"L10_EXTRA_WORDS: {who}: count {count}, extent has {extent_words} words")

    current = struct.unpack_from(">I", data, 136)[0]
    rates = struct.unpack_from(f">{count}I", data, offset)
    if current not in rates:
        raise ImageCheckError(f"L10_CURRENT: {who}: current rate {current} is not in {rates}")


def _clock_domain(data: bytes, who: str) -> None:
    """Prove the processor's range check equals membership in the served list."""
    # 7.2.32: source offset/count follow clock_source_index, at bytes 72/74.
    fields_end = 72 + struct.calcsize(">HH")
    if len(data) < fields_end:
        raise ImageCheckError(f"L6_HEADER: {who}: missing clock-source fields")
    offset, count = struct.unpack_from(">HH", data, 72)
    if offset != fields_end:  # IEEE 7.2.32 fixes the list immediately after the fields.
        raise ImageCheckError(f"L6_OFFSET: {who}: offset {offset}, expected {fields_end}")
    if not count:
        raise ImageCheckError(f"L6_EMPTY: {who}: no clock sources")
    list_end = offset + count * struct.calcsize(">H")
    if list_end > len(data):
        raise ImageCheckError(f"L6_EXTENT: {who}: source list {offset}..{list_end} outside descriptor")
    sources = list(struct.unpack_from(f">{count}H", data, offset))
    identity = list(range(count))
    if len(set(sources)) != count:
        raise ImageCheckError(f"L6_DUPLICATE: {who}: repeated source in {sources}")
    elif sorted(sources) != identity:
        raise ImageCheckError(f"L6_GAP: {who}: source list {sources} does not cover {identity}")
    elif sources != identity:
        raise ImageCheckError(f"L6_ORDER: {who}: source list {sources} is not in index order")


def validate_shipping_image(blob: bytes) -> None:
    """Check every packed AUDIO_UNIT and CLOCK_DOMAIN before shipping the image.

    Index offset, row count, descriptor lengths, strides and list fields all
    come from bytes. SET_SAMPLING_RATE supplies the walk offset and limit.
    No loader, overlay, descriptor constructor or packer report is consulted.
    This is semantic validation of packer output, not a replacement packer.
    """
    list_offset, walk_count = _sampling_rate_walk()
    try:
        if blob[:4] != b"AEMI" or struct.unpack_from(">H", blob, 4)[0] != 1:
            raise ImageCheckError("IMAGE_STRUCTURE: expected AEMI version 1")
        config_count = struct.unpack_from(">H", blob, 6)[0]
        if not config_count:
            raise ImageCheckError("IMAGE_CONFIGS: no shipping configurations")
        checked = [set() for _ in range(config_count)]
        row_count = struct.unpack_from(">H", blob, 8)[0]
        index_offset = struct.unpack_from(">I", blob, 12)[0]
        for row in range(row_count):
            cfg, dtype, count, length, base, _names, stride = struct.unpack_from(
                ">HHHHIHH", blob, index_offset + row * struct.calcsize(">HHHHIHH"))
            if cfg >= config_count:
                raise ImageCheckError(f"IMAGE_STRUCTURE: configuration {cfg} outside header count {config_count}")
            if dtype not in (0x0002, 0x0024):  # IEEE 7.2 AUDIO_UNIT / CLOCK_DOMAIN.
                continue
            for index in range(count):
                start = base + index * stride
                data = blob[start:start + length]
                if len(data) != length:
                    raise ImageCheckError("IMAGE_STRUCTURE: descriptor extends beyond image")
                who = f"configuration {cfg}, type 0x{dtype:04X}, image byte {start}"
                if dtype == 0x0002:
                    _audio_unit(data, who, list_offset, walk_count)
                else:
                    _clock_domain(data, who)
                checked[cfg].add(dtype)
        for cfg, types in enumerate(checked):
            if 0x0002 not in types:
                raise ImageCheckError(f"L10_MISSING: configuration {cfg}: no checked AUDIO_UNIT")
            if 0x0024 not in types:
                raise ImageCheckError(f"L6_MISSING: configuration {cfg}: no checked CLOCK_DOMAIN")
    except struct.error as exc:
        raise ImageCheckError(f"IMAGE_STRUCTURE: truncated packed field: {exc}") from exc
