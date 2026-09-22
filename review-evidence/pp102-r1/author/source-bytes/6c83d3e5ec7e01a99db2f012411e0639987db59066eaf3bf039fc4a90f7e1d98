#!/usr/bin/env python3
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""Descriptor-image generator for KL_aecp_desc_store (docs/architecture/07 §3.3).

Turns a vendor-neutral JSON description of an AEM descriptor tree into the FLAT
MEMORY IMAGE the store fetches over its read-only memory master — a header, a
per-(configuration, type) index map, the concatenated descriptors in
(configuration, type, index) order, and the 64-byte name table of 07 §3.4.

The image lives in the integrator's main memory (the reference platform puts it
in DDR3), NOT in a $readmemh ROM: the consumer's model is already 22,561 bytes
at the 8x8 shape and grows with every stream, descriptor and localized string,
which is the wrong thing to spend RAMB tiles on.  Nothing here knows what the
memory is.

=============================================================================
INPUT FORMAT  (JSON; see example_milan_8.json)
=============================================================================

{
  "format": "kl-aem-image", "version": 1,
  "names": [ "entity name", "group name", ... ],   // 64-byte overlay entries
  "descriptors": [
    { "configuration": 0,            // configuration_index this belongs to
      "type": "ENTITY",              // name from TYPES, or 5 / "0x0005"
      "index": 0,                    // descriptor_index, dense from 0 per type
      "name_index": 0,               // optional: first name-table entry, else -1
      "pad_to": 312,                 // optional: zero-pad to this exact length
      "fields": [                    // ordered; concatenated big-endian
        {"name": "descriptor_type", "size": 2, "value": "0x0000"},
        {"name": "entity_name",     "size": 64, "string": "..."},
        {"name": "raw",             "size": 6,  "bytes": "001b92fffe01"},
        {"name": "reserved",        "size": 8}          // value defaults to 0
      ] },
    { "configuration": 0, "type": "AUDIO_MAP", "index": 0,
      "bytes": "00170000..." }       // alternative: the whole descriptor as hex
  ]
}

A field carries exactly one of `value` (big-endian unsigned integer, int or
"0x.." string), `string` (UTF-8, zero-padded/truncated to `size`), `bytes` (hex,
zero-padded/truncated to `size`), or nothing (zeros).

=============================================================================
OUTPUT IMAGE LAYOUT  (all multi-byte fields BIG-ENDIAN, the 1722.1 wire order)
=============================================================================

  header @0x00, 32 bytes = 4 x 64-bit beats
    +0x00 u32 magic            0x41454D49  ("AEMI")
    +0x04 u16 layout_version   1
    +0x06 u16 n_config         number of configurations
    +0x08 u16 n_entries        index-map entries (all configurations)
    +0x0A u16 n_names          64-byte name-table entries
    +0x0C u32 index_off        byte offset of the index-map array
    +0x10 u32 names_off        byte offset of the name table
    +0x14 u32 image_bytes      total image length
    +0x18 u16 desc_max_len     longest descriptor in the image
    +0x1A u16 reserved         0
    +0x1C u32 checksum         chosen so the eight u32 words sum to 0xFFFFFFFF

  The checksum is what separates "software has not loaded the image yet" from
  "silently wrong": uninitialised DRAM is not a recognisable zero, so the store
  refuses to serve anything until magic + version + checksum all agree.

  index map @index_off, n_entries x 16 bytes, sorted by (config, type)
    +0x00 u16 config_index
    +0x02 u16 descriptor_type
    +0x04 u16 count        descriptors of this type in this configuration
    +0x06 u16 elem_len     byte length of EACH of them
    +0x08 u32 elem_off     byte offset of index 0 (8-byte aligned)
    +0x0C u16 name_base    name-table entry of index 0 (0xFFFF = unnamed)
    +0x0E u16 elem_stride  elem_len rounded UP to a multiple of 8

  LAYOUT-VERSION-1 CONSTRAINT: every descriptor of one (configuration, type)
  has the SAME length, so a locate is elem_off + index*elem_stride with no
  second indirection and no DRAM round trip beyond the one that fetches the
  descriptor.  Milan §6.3/§6.4 rate-completeness and configuration-uniformity
  already force this for the stream descriptors; the generator REFUSES an input
  that violates it rather than emitting a layout the store cannot address.

  The STRIDE is separate from the LENGTH because a descriptor length is rarely
  a multiple of 8 (07 §3.2: CONFIGURATION 74+4n, AVB_INTERFACE 102,
  CLOCK_SOURCE 86) and the store fetches 64-bit beats: with a bare
  base + index*elem_len, descriptor 1 of such a type would start mid-beat and
  the whole line buffer would be byte-shifted.  Padding the STRIDE keeps every
  descriptor 8-aligned while elem_len stays the true wire length.

  descriptors, then the name table (n_names x 64 bytes), 8-byte aligned.

=============================================================================
USAGE
=============================================================================
  gen_desc_image.py -i example_milan_8.json -o image.bin [-m image.map]
"""
import argparse
import json
import sys
from typing import Any

# IEEE 1722.1-2021 Table 7-2 descriptor types (the ones 07 §3.1 names, plus the
# handful a Milan PAAD may still carry).  A numeric type is always accepted.
TYPES = {
    "ENTITY": 0x0000, "CONFIGURATION": 0x0001, "AUDIO_UNIT": 0x0002,
    "VIDEO_UNIT": 0x0003, "SENSOR_UNIT": 0x0004,
    "STREAM_INPUT": 0x0005, "STREAM_OUTPUT": 0x0006,
    "JACK_INPUT": 0x0007, "JACK_OUTPUT": 0x0008,
    "AVB_INTERFACE": 0x0009, "CLOCK_SOURCE": 0x000A,
    "MEMORY_OBJECT": 0x000B, "LOCALE": 0x000C, "STRINGS": 0x000D,
    "STREAM_PORT_INPUT": 0x000E, "STREAM_PORT_OUTPUT": 0x000F,
    "EXTERNAL_PORT_INPUT": 0x0010, "EXTERNAL_PORT_OUTPUT": 0x0011,
    "AUDIO_CLUSTER": 0x0014, "AUDIO_MAP": 0x0017,
    "CONTROL": 0x001A, "SIGNAL_SELECTOR": 0x001B,
    "CLOCK_DOMAIN": 0x0024,
}

MAGIC = 0x41454D49
LAYOUT_VERSION = 1
HDR_BYTES = 32
IDX_BYTES = 16
NAME_BYTES = 64
NAME_NONE = 0xFFFF


class ImageError(Exception):
    pass


def _u(value):
    """int, or a decimal/hex string."""
    if isinstance(value, bool):
        raise ImageError("bool is not a descriptor value")
    if isinstance(value, int):
        return value
    return int(str(value), 0)


def _type_code(spec):
    if isinstance(spec, str) and spec in TYPES:
        return TYPES[spec]
    try:
        return _u(spec)
    except (ValueError, ImageError):
        raise ImageError(f"unknown descriptor type {spec!r}")


def field_bytes(fld: dict[str, Any]) -> bytes:
    """One field's wire bytes, big-endian and exactly `size` long. A field that
    sets more than one of value/string/bytes is refused rather than resolved by
    precedence, because which one won would be invisible in the image."""
    size = _u(fld["size"])
    if size < 0:
        raise ImageError(f"negative size in field {fld.get('name')}")
    given = [k for k in ("value", "string", "bytes") if k in fld]
    if len(given) > 1:
        raise ImageError(f"field {fld.get('name')!r} sets {given} — pick one")
    if "value" in fld:
        val = _u(fld["value"])
        if val < 0 or val >= (1 << (8 * size)):
            raise ImageError(f"field {fld.get('name')!r} value does not fit "
                             f"{size} bytes")
        return val.to_bytes(size, "big")
    if "string" in fld:
        raw = str(fld["string"]).encode("utf-8")[:size]
        return raw + b"\x00" * (size - len(raw))
    if "bytes" in fld:
        raw = bytes.fromhex("".join(str(fld["bytes"]).split()))
        if len(raw) > size:
            raise ImageError(f"field {fld.get('name')!r} has {len(raw)} bytes "
                             f"for size {size}")
        return raw + b"\x00" * (size - len(raw))
    return b"\x00" * size


def descriptor_bytes(desc: dict[str, Any]) -> bytes:
    """One descriptor's wire bytes, from its fields or its literal hex - never
    both. Shorter than type+index is not a descriptor and is refused."""
    if "bytes" in desc and "fields" in desc:
        raise ImageError("a descriptor sets both 'bytes' and 'fields'")
    if "bytes" in desc:
        body = bytes.fromhex("".join(str(desc["bytes"]).split()))
    else:
        body = b"".join(field_bytes(f) for f in desc.get("fields", []))
    if "pad_to" in desc:
        want = _u(desc["pad_to"])
        if len(body) > want:
            raise ImageError(f"descriptor is {len(body)} bytes, pad_to {want}")
        body += b"\x00" * (want - len(body))
    if len(body) < 4:
        raise ImageError("a descriptor is at least its type+index (4 bytes)")
    return body


def name_bytes(name: str) -> bytes:
    """One name-table entry, exactly 64 bytes."""
    raw = str(name).encode("utf-8")[:NAME_BYTES]
    return raw + b"\x00" * (NAME_BYTES - len(raw))


def _grouped_descriptors(model):
    """{(configuration, type): {index: (body, name_index)}} from the document.

    This is where a descriptor stops being JSON: its bytes are assembled, its
    name_index is normalised (-1 and absent both mean NAME_NONE) and a second
    descriptor claiming an occupied (cfg, type, index) is refused.
    """
    groups = {}
    for desc in model.get("descriptors", []):
        cfg = _u(desc.get("configuration", 0))
        typ = _type_code(desc["type"])
        idx = _u(desc.get("index", 0))
        body = descriptor_bytes(desc)
        nidx = _u(desc.get("name_index", NAME_NONE))
        if nidx == -1:
            nidx = NAME_NONE
        if nidx < 0 or nidx > NAME_NONE:
            raise ImageError(f"cfg {cfg} type 0x{typ:04X} index {idx} has "
                             f"invalid name_index {nidx}")
        key = (cfg, typ)
        if idx in groups.setdefault(key, {}):
            raise ImageError(f"duplicate descriptor cfg {cfg} type "
                             f"0x{typ:04X} index {idx}")
        groups[key][idx] = (body, nidx)
    if not groups:
        raise ImageError("the model declares no descriptors")
    return groups


def _check_name_binding(cfg, typ, want, members, names):
    """Refuse a group whose names the index map could not address.

    One index-map row holds only the first name-table entry. Therefore every
    member of a named multi-descriptor group must consume the next table entry,
    while an unnamed group must be unnamed throughout. ENTITY is the sole
    exception: its one descriptor consumes two consecutive entries for
    entity_name and group_name. Each name is also checked against the inline
    bytes READ_DESCRIPTOR serves, so the two can never disagree on the wire.
    """
    named = [members[i][1] != NAME_NONE for i in want]
    if any(named) and not all(named):
        raise ImageError(f"cfg {cfg} type 0x{typ:04X} mixes named and "
                         "unnamed descriptors in one index run")
    if typ == TYPES["ENTITY"]:
        if want != [0]:
            raise ImageError(f"cfg {cfg} ENTITY must contain only index 0")
        body, nidx = members[0]
        if nidx == NAME_NONE:
            raise ImageError(f"cfg {cfg} ENTITY has no name_index")
        if len(body) < 244:
            raise ImageError(f"cfg {cfg} ENTITY is {len(body)} bytes; "
                             "entity_name and group_name require 244")
        if nidx + 2 > len(names):
            raise ImageError(f"cfg {cfg} ENTITY names {nidx} and "
                             f"{nidx + 1} exceed table size {len(names)}")
        if body[48:112] != name_bytes(names[nidx]):
            raise ImageError(f"cfg {cfg} ENTITY entity_name differs from "
                             f"name-table entry {nidx}")
        if body[180:244] != name_bytes(names[nidx + 1]):
            raise ImageError(f"cfg {cfg} ENTITY group_name differs from "
                             f"name-table entry {nidx + 1}")
    elif all(named):
        base = members[0][1]
        for i in want:
            body, nidx = members[i]
            if nidx != base + i:
                raise ImageError(
                    f"cfg {cfg} type 0x{typ:04X} index {i} has name_index "
                    f"{nidx}; expected contiguous entry {base + i}")
            if len(body) < 68:
                raise ImageError(f"cfg {cfg} type 0x{typ:04X} index {i} "
                                 f"is {len(body)} bytes; object_name "
                                 "requires 68")
            if nidx >= len(names):
                raise ImageError(
                    f"cfg {cfg} type 0x{typ:04X} index {i} name_index "
                    f"{nidx} exceeds table size {len(names)}")
            if body[4:68] != name_bytes(names[nidx]):
                raise ImageError(
                    f"cfg {cfg} type 0x{typ:04X} index {i} object_name "
                    f"differs from name-table entry {nidx}")


def _index_runs(cfg, typ, want, members, line_bytes):
    """One index-map entry per maximal run of equal-length descriptors.

    A type does NOT have to be one uniform run. A Milan end-station puts its
    media sink and its CRF sink both under STREAM_INPUT, and 07 §3.2's format
    list makes them different lengths (AAF advertising two formats is 148
    bytes, CRF advertising one is 140) — so REFUSING a mixed-length type
    refused every real build of this device, not a corner case. It is also not
    a model defect to fix upstream: 1722.1 §7.2.6 sizes a stream descriptor by
    its own number_of_formats, and a CRF sink cannot advertise AAF formats to
    pad itself level.

    The layout is unchanged and still version 1. A type with mixed lengths is
    emitted as SEVERAL index entries, one per maximal run of equal-length
    descriptors, in ascending index order — each internally uniform, so the
    "locate = elem_off + i*stride, no second indirection" property survives
    intact. What absorbs the split is the SCAN: entries for one (cfg, type) are
    contiguous and ordered, so the store accumulates the counts it has walked
    past and subtracts that running base from the key. A type that is uniform
    emits exactly one entry and the running base stays zero — byte-identical to
    before, which is why no version bump is owed and old images still load.
    """
    runs = []
    for i in want:
        body, nidx = members[i]
        if runs and len(runs[-1]["bodies"][0]) == len(body):
            runs[-1]["bodies"].append(body)
        else:
            runs.append({"first": i, "name_base": nidx, "bodies": [body]})
    entries = []
    for run in runs:
        elem_len = len(run["bodies"][0])
        if elem_len > line_bytes:
            raise ImageError(
                f"cfg {cfg} type 0x{typ:04X} index {run['first']} is "
                f"{elem_len} bytes, over the {line_bytes}-byte store line "
                f"buffer — the store would answer NO_SUCH_DESCRIPTOR for it")
        entries.append({"cfg": cfg, "type": typ, "count": len(run["bodies"]),
                        "elem_len": elem_len, "name_base": run["name_base"],
                        "stride": (elem_len + 7) & ~7,
                        "first": run["first"],
                        "bodies": run["bodies"]})
    return entries


def _index_entries(groups, names, line_bytes):
    """Every index-map entry, in (configuration, type, index) order."""
    entries = []
    for (cfg, typ) in sorted(groups):
        members = groups[(cfg, typ)]
        want = sorted(members)
        if want != list(range(len(want))):
            raise ImageError(f"cfg {cfg} type 0x{typ:04X} indices are not "
                             f"dense from 0: {want} (07 §3.1 rule L2)")
        _check_name_binding(cfg, typ, want, members, names)
        entries.extend(_index_runs(cfg, typ, want, members, line_bytes))
    return entries


def _render_image(entries, names, n_config):
    """(image bytes, the header numbers the report restates).

    Lays the descriptors out at their 8-aligned strides, writes the name table
    and the index map behind them, then closes the header with the checksum
    that makes its eight u32 words sum to 0xFFFFFFFF. Each entry learns its own
    `elem_off` here, which is what the report prints.
    """
    index_off = HDR_BYTES
    cursor = index_off + IDX_BYTES * len(entries)
    cursor = (cursor + 7) & ~7
    blobs = []
    for ent in entries:
        ent["elem_off"] = cursor
        for body in ent["bodies"]:
            blobs.append((cursor, body))
            cursor += ent["stride"]

    names_off = cursor
    cursor += NAME_BYTES * len(names)
    image_bytes = (cursor + 7) & ~7
    desc_max = max(e["elem_len"] for e in entries)

    img = bytearray(image_bytes)
    for off, body in blobs:
        img[off:off + len(body)] = body
    for i, nm in enumerate(names):
        img[names_off + i * NAME_BYTES:
            names_off + (i + 1) * NAME_BYTES] = name_bytes(nm)

    for i, ent in enumerate(entries):
        at = index_off + i * IDX_BYTES
        img[at:at + IDX_BYTES] = (
            ent["cfg"].to_bytes(2, "big") + ent["type"].to_bytes(2, "big")
            + ent["count"].to_bytes(2, "big")
            + ent["elem_len"].to_bytes(2, "big")
            + ent["elem_off"].to_bytes(4, "big")
            + (ent["name_base"] & 0xFFFF).to_bytes(2, "big")
            + ent["stride"].to_bytes(2, "big"))

    head = (MAGIC.to_bytes(4, "big") + LAYOUT_VERSION.to_bytes(2, "big")
            + n_config.to_bytes(2, "big") + len(entries).to_bytes(2, "big")
            + len(names).to_bytes(2, "big") + index_off.to_bytes(4, "big")
            + names_off.to_bytes(4, "big") + image_bytes.to_bytes(4, "big")
            + desc_max.to_bytes(2, "big") + b"\x00\x00")
    words = [int.from_bytes(head[i:i + 4], "big") for i in range(0, 28, 4)]
    checksum = (0xFFFFFFFF - (sum(words) & 0xFFFFFFFF)) & 0xFFFFFFFF
    img[0:HDR_BYTES] = head + checksum.to_bytes(4, "big")

    return bytes(img), {"n_config": n_config, "index_off": index_off,
                        "names_off": names_off, "image_bytes": image_bytes,
                        "desc_max": desc_max, "checksum": checksum,
                        "n_names": len(names)}


def _render_report(entries, layout):
    """The human-readable map: the header, then one row per index-map entry."""
    report = [
        f"magic AEMI  layout_version {LAYOUT_VERSION}",
        f"configurations {layout['n_config']}  index entries {len(entries)}  "
        f"names {layout['n_names']}",
        f"index_off 0x{layout['index_off']:06X}  "
        f"names_off 0x{layout['names_off']:06X}  "
        f"image_bytes {layout['image_bytes']}  "
        f"desc_max_len {layout['desc_max']}",
        f"checksum 0x{layout['checksum']:08X}",
        "",
        # `first` is printed because a mixed-length type occupies several rows
        # and two rows with the same cfg+type would otherwise read as a
        # duplicate entry rather than as the index ranges they are.
        "  cfg  type    first  count  elem_len  stride  elem_off   name_base",
    ]
    for ent in entries:
        nm = "-" if ent["name_base"] == NAME_NONE else str(ent["name_base"])
        report.append(f"  {ent['cfg']:>3}  0x{ent['type']:04X}  "
                      f"{ent['first']:>5}  "
                      f"{ent['count']:>5}  {ent['elem_len']:>8}  "
                      f"{ent['stride']:>6}  "
                      f"0x{ent['elem_off']:06X}  {nm:>9}")
    return "\n".join(report) + "\n"


def build(model: dict[str, Any], line_bytes: int = 576) -> tuple[bytes, str]:
    """model (parsed JSON) -> (image bytes, human-readable map)."""
    if model.get("format") != "kl-aem-image":
        raise ImageError("input is not a kl-aem-image document")
    if _u(model.get("version", 0)) != LAYOUT_VERSION:
        raise ImageError(f"input version {model.get('version')} != "
                         f"{LAYOUT_VERSION}")

    names = [str(n) for n in model.get("names", [])]
    if len(names) >= NAME_NONE:
        raise ImageError(f"the name table has {len(names)} entries; maximum "
                         f"is {NAME_NONE - 1}")

    entries = _index_entries(_grouped_descriptors(model), names, line_bytes)

    n_config = len({e["cfg"] for e in entries})
    if sorted({e["cfg"] for e in entries}) != list(range(n_config)):
        raise ImageError("configuration indices are not dense from 0")

    img, layout = _render_image(entries, names, n_config)
    return img, _render_report(entries, layout)


def main() -> int:
    """Pack one model document into the flat image the store fetches, and write
    the layout map beside it. A refused layout returns 1 and writes nothing,
    because a partially written image would be fetched as a whole one."""
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("-i", "--input", required=True, help="model JSON")
    ap.add_argument("-o", "--out", required=True, help="flat memory image")
    ap.add_argument("-m", "--map", help="human-readable layout report")
    ap.add_argument("--line-bytes", type=int, default=576,
                    help="store line-buffer size to validate against (576)")
    args = ap.parse_args()
    with open(args.input, encoding="utf-8") as fh:
        model = json.load(fh)
    try:
        img, report = build(model, args.line_bytes)
    except ImageError as exc:
        print(f"gen_desc_image: {exc}", file=sys.stderr)
        return 1
    with open(args.out, "wb") as fh:
        fh.write(img)
    if args.map:
        with open(args.map, "w", encoding="utf-8") as fh:
            fh.write(report)
    print(f"{args.out}: {len(img)} bytes")
    print(report, end="")
    return 0


if __name__ == "__main__":
    sys.exit(main())
