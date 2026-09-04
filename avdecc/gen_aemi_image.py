#!/usr/bin/env python3
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""Emit the protocol processor's DRAM descriptor image from THIS repo's model.

Two halves of a supply chain existed and nothing joined them:

  * `avdecc/gen_aem_store.py` already builds every AEM descriptor of this
    end-station byte-exactly, from the build configuration, and has done so
    since the legacy AECP plane shipped;
  * `protocol-processor/hdl/aecp/desc/gen_desc_image.py` already packs a set of
    descriptors into the AEMI image `KL_aecp_desc_store` fetches from main
    memory.

Without the join a stock build enumerates NOTHING: the store finds no magic at
`PP_DESC_BASE_P`, refuses to serve, and every READ_DESCRIPTOR answers
`BAD_ARGUMENTS`. That reads exactly like a broken entity model, which is the
expensive way to discover a missing build step.

This script is the join, and it is deliberately thin. It imports both sides
rather than restating either:

  * the DESCRIPTOR BYTES come from `gen_aem_store.build_model()`, so the image
    cannot disagree with the shape the rest of the build was generated from;
  * the IMAGE LAYOUT comes from the submodule's `build()`, so the format lives
    in exactly one place - next to the RTL that parses it.

A copy of either would drift, and a drifted descriptor image is a device that
enumerates plausibly and wrongly.

WHY THE 64 KiB ROM CEILING DOES NOT APPLY HERE. `gen_aem_store` refuses a model
whose ROM exceeds the 16-bit store address space, and names the way out: "the
D6 split (BRAM hot stub + DRAM bulk descriptor tree), not a wider ROM". This
image IS the DRAM half. It is addressed by 32-bit main-memory offsets, so the
ceiling is the reserved region, not 65,536 bytes. The check is not bypassed
here; it simply is not this path's check.

THE IDENTITY SPANS ARE BAKED HERE. `gen_aem_store` zero-fills the ENTITY and
AVB_INTERFACE identity fields and records them in `M["OVERLAYS"]`: the legacy
plane substituted them byte-for-byte at read time from the CSR group
(`KL_aecp_aem_dyn_mux`, deleted in eff99a9c). `KL_aecp_desc_store` has no
identity input, so an image that ships those spans as written serves an ENTITY
descriptor whose entity_id, entity_model_id and entity_capabilities all read
zero - and a zero entity_capabilities has AEM_SUPPORTED clear, i.e. an entity
model that advertises that it has no entity model. IEEE 1722.1-2021 Table 7-2
does not leave this open: each of those fields "is the same as the ... field in
ATDECC Discovery Protocol". `apply_identity()` therefore writes the numbers ADP
already advertises into the ROM before the descriptors are sliced out of it.

USAGE
  avdecc/gen_aemi_image.py --overlay sw/builder/out/<cfg>/aem_overlay.json \
                           -o aem_desc.bin -m aem_desc.map

The overlay is REQUIRED. The built-in shape names no board, so it states
neither a station MAC nor an entity_id, and an image built from it would carry
exactly the zero identity block this join exists to prevent.

The output is a flat image to be written at `PP_DESC_BASE_P`. `sw/litex`
computes that base from the SoC memory map; it is never restated here, because
this script has no way to know it and a guessed base is worse than no image.
"""
import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any

_HERE = Path(__file__).resolve().parent
_REPO = _HERE.parent
_DESC = _REPO / "protocol-processor" / "hdl" / "aecp" / "desc"

#: `str()`, not the `Path`: `sys.path` entries are looked up by the import
#: machinery's own path-hook cache, which is keyed on strings.
sys.path.insert(0, str(_HERE))
sys.path.insert(0, str(_DESC))

import gen_aem_store as aem            # noqa: E402  (path set above)

try:
    import gen_desc_image as image     # noqa: E402
except ImportError:                    # pragma: no cover - submodule missing
    print("gen_aemi_image: the protocol-processor submodule is not checked "
          "out (no %s).\n  git submodule update --init protocol-processor"
          % _DESC.relative_to(_REPO), file=sys.stderr)
    raise SystemExit(2)


#! 1722.1-2021 Table 6-3: AEM_SUPPORTED. With this bit clear a controller is
#! told the entity has no AEM at all, so it never issues READ_DESCRIPTOR - the
#! descriptor image below becomes unreachable no matter how correct it is.
AEM_SUPPORTED_C = 0x0000_0008

#! pp_adp_pkg::ADP_ENTITY_CAPS_C is where entity_capabilities exists - the ADP
#! engine takes wire bytes 34..37 straight from it (KL_adp_engine.sv
#! frame_byte_f), with no CSR in the path, so there is no run-time value for
#! the image to disagree with. Read, never restated: a copied mask diverges in
#! silence and this one carries AEM_SUPPORTED.
_PP_ADP_PKG = _REPO / "protocol-processor" / "hdl" / "adp" / "pp_adp_pkg.sv"

#! Overlay spans this join deliberately does NOT write, with the reason each
#! one is not a build constant. Anything not listed here and not resolved by
#! identity_from_overlay() makes apply_identity() refuse, so a span added to
#! gen_aem_store cannot slip through as zeros the way this whole set did.
UNBAKED_SPANS = {
    #! available_index counts THIS entity's advertisements and increments on
    #! every ADPDU (1722.1-2021 6.2.1.14; KL_adp_engine aidx_r). A flat image
    #! cannot track a counter. 0 is what it holds before the first
    #! advertisement, and Table 7-2 points a controller that cares at the
    #! ADPDU, which is live.
    "AVAIL_IDX",
    #! Not a placeholder: the ROM already carries this config's entity_name,
    #! and the deleted mux replaced its first 8 characters ONLY when the
    #! board-name CSR was provisioned - it kept the ROM bytes when it was not
    #! (KL_aecp_aem_dyn_mux OVL_ENT_NAME8_C). Leaving the configured name is
    #! that same fallback, and 1722.1-2021 6.2.2.8 excludes object_name from
    #! the model, so it is not an identity field either.
    "ENT_NAME8",
}


def adp_entity_capabilities() -> int:
    """entity_capabilities as the ADP engine advertises it."""
    m = re.search(r"ADP_ENTITY_CAPS_C\s*=\s*32'h([0-9A-Fa-f_]+)\s*;",
                  _PP_ADP_PKG.read_text(encoding="utf-8"))
    if not m:
        raise image.ImageError(
            f"no ADP_ENTITY_CAPS_C in {_PP_ADP_PKG.relative_to(_REPO)} - "
            "entity_capabilities has no other source, and Table 7-2 makes the "
            "ENTITY descriptor repeat the ADPDU's value")
    caps = int(m.group(1).replace("_", ""), 16)
    if not caps & AEM_SUPPORTED_C:
        raise image.ImageError(
            f"ADP advertises entity_capabilities 0x{caps:08X} with "
            "AEM_SUPPORTED clear (Table 6-3), so this image is an entity "
            "model no controller will ever ask for")
    return caps


def identity_from_overlay(ovl: dict[str, Any]) -> dict[str, bytes]:
    """The Table 7-2 identity, keyed by gen_aem_store's own overlay names.

    Every value is read from the artifact that already owns it - the overlay's
    `adp` block (endstation_builder.overlay_adp_block, the same adp_shape()
    that generates gen/adp_shape_defaults.svh and the same derive_entity_id()
    that generates milan-entity.conf) and pp_adp_pkg for the capabilities
    mask. Nothing is chosen here, because a value chosen here is a value that
    can disagree with the ADPDU, and Table 7-2 forbids exactly that.
    """
    adp = ovl.get("adp")
    if adp is None:
        raise image.ImageError(
            "overlay carries no 'adp' block (schema "
            f"{ovl.get('_schema_version')}, need 2.2+): it states neither the "
            "station MAC nor the resolved entity_id, so the ENTITY and "
            "AVB_INTERFACE identity spans cannot be filled. Regenerate it: "
            "python3 sw/builder/endstation_builder.py --write-rtl <cfg.yaml>")
    mac = bytes(int(x, 16) for x in str(adp["mac_address"]).split(":"))
    if len(mac) != 6:
        raise image.ImageError(f"mac_address {adp['mac_address']!r} is not an "
                               "EUI-48")
    #! 802.1AS-2011 8.5.2.2 (and IEEE 802-2014 8.2): clockIdentity is the
    #! station EUI-48 widened to EUI-64 by inserting FF-FE at the OUI
    #! boundary. Same recipe the deleted mux applied in RTL ({mac[47:24],
    #! 16'hFFFE, mac[23:0]}) and the same one derive_entity_id() applies to
    #! the entity_id, so the descriptor's clock_identity is the one the
    #! fabric time-sync engine announces.
    clock_id = mac[:3] + b"\xFF\xFE" + mac[3:]

    def u(value: str | int, nbytes: int) -> bytes:
        """A big-endian field of nbytes. The overlay writes a number either as
        JSON int or as a hex string, and both mean the same wire value."""
        return int(str(value), 16 if isinstance(value, str) else 10) \
            .to_bytes(nbytes, "big")

    return {
        "ENTITY_ID":   u(adp["entity_id"], 8),
        "MODEL_ID":    u(ovl["entity"]["entity_model_id"], 8),
        "ECAPS":       adp_entity_capabilities().to_bytes(4, "big"),
        "TALKER_SRC":  u(adp["talker_stream_sources"], 2),
        "TALKER_CAP":  u(adp["talker_capabilities"], 2),
        "LISTEN_SINK": u(adp["listener_stream_sinks"], 2),
        "LISTEN_CAP":  u(adp["listener_capabilities"], 2),
        #! ADP sends controller_capabilities as four zero bytes (KL_adp_engine
        #! frame_byte_f, wire bytes 46..49): this entity implements no
        #! controller, so Table 6-6's IMPLEMENTED bit is clear. Table 7-2 ties
        #! the descriptor to that, and 0 is the value, not the absence of one.
        "CTRL_CAP":    bytes(4),
        #! Likewise association_id, ADP wire bytes 70..77. 1722.1-2021
        #! 6.2.1.18: 0 means the entity is not associated with any other, and
        #! nothing in this build ever associates it.
        "ASSOC_ID":    bytes(8),
        #! current_configuration: d_configuration emits configurations_count
        #! = 1, so 0 is the only index SET_CONFIGURATION could ever select
        #! (1722.1-2021 7.2.1). It is dynamic in principle and single-valued
        #! in this model.
        "CURRENT_CFG": bytes(2),
        "MAC":         mac,
        "CLOCK_ID":    clock_id,
    }


def apply_identity(M: dict[str, Any], ident: dict[str, bytes]) -> bytes:
    """The ROM with every build-constant overlay span filled in.

    `M` is left untouched: the same model also generates the store's svh,
    whose RTL consumer carries its own overlay table, and only the DRAM image
    wants these bytes resolved ahead of time.
    """
    rom = bytearray(M["rom"])
    for base, nbytes, src in M["OVERLAYS"]:
        if src in UNBAKED_SPANS:
            continue
        if src not in ident:
            raise image.ImageError(
                f"overlay span {src} (ROM 0x{base:04X}, {nbytes} B) has no "
                "resolved value and is not in UNBAKED_SPANS - decide whether "
                "it is a build constant (bake it in identity_from_overlay) or "
                "genuinely dynamic (list it, with why), because shipping it "
                "unresolved ships zeros")
        val = ident[src]
        if len(val) != nbytes:
            raise image.ImageError(
                f"overlay span {src} is {nbytes} B in the ROM but the "
                f"resolved value is {len(val)} B")
        rom[base:base + nbytes] = val
    return bytes(rom)


def _descriptor_directory(M: dict[str, Any]) -> dict[tuple[int, int], tuple[int, int]]:
    """{(type, index): (base, length)} - the ROM span of every descriptor."""
    directory = {(int(typ), int(idx)): (int(base), int(length))
                 for typ, idx, base, length in M["directory"]}
    if len(directory) != len(M["directory"]):
        raise image.ImageError("descriptor directory contains duplicate keys")
    return directory


def _named_slots(M: dict[str, Any],
                 directory: dict[tuple[int, int], tuple[int, int]],
                 ) -> dict[tuple[int, int], dict[int, int]]:
    """{(type, index): {semantic index: ROM address}} from `M["NAMED"]`."""
    named = {}
    for typ, idx, semantic, addr in M["NAMED"]:
        key = (int(typ), int(idx))
        semantic = int(semantic)
        addr = int(addr)
        if key not in directory:
            raise image.ImageError(
                f"name for type 0x{key[0]:04X} index {key[1]} has no "
                "descriptor")
        slots = named.setdefault(key, {})
        if semantic in slots:
            raise image.ImageError(
                f"duplicate name for type 0x{key[0]:04X} index {key[1]} "
                f"semantic index {semantic}")
        slots[semantic] = addr
    return named


def _text_from_name(raw: bytes, who: str) -> str:
    """The string one NAME_BYTES ROM field holds, or why it cannot be one."""
    if len(raw) != image.NAME_BYTES:
        raise image.ImageError(
            f"{who} is {len(raw)} bytes, expected {image.NAME_BYTES}")
    head, separator, tail = raw.partition(b"\x00")
    if separator and any(tail):
        raise image.ImageError(
            f"{who} has nonzero bytes after its first NUL")
    try:
        text = (head if separator else raw).decode("utf-8")
    except UnicodeDecodeError as exc:
        raise image.ImageError(f"{who} is not valid UTF-8: {exc}") from exc
    if image.name_bytes(text) != raw:
        raise image.ImageError(
            f"{who} cannot be represented exactly by the image format")
    return text


def _name_table(rom: bytes,
                directory: dict[tuple[int, int], tuple[int, int]],
                named: dict[tuple[int, int], dict[int, int]],
                ) -> tuple[list[str], dict[tuple[int, int], int]]:
    """(the flat name table, {descriptor key: its first row in that table}).

    Every name is read out of the same inline ROM bytes READ_DESCRIPTOR serves,
    at the address `M["NAMED"]` gave it and only where that address is the one
    the descriptor's layout puts it at.
    """
    names = []
    first_name = {}
    per_type = {}
    for typ, idx in directory:
        per_type.setdefault(typ, []).append(idx)
    for typ, indices in sorted(per_type.items()):
        indices.sort()
        present = [(typ, idx) in named for idx in indices]
        if any(present) and not all(present):
            raise image.ImageError(
                f"type 0x{typ:04X} mixes named and unnamed descriptors")
        for idx in indices:
            key = (typ, idx)
            if key not in named:
                continue
            slots = named[key]
            expected = [0, 1] if typ == aem.ENTITY else [0]
            if sorted(slots) != expected:
                raise image.ImageError(
                    f"type 0x{typ:04X} index {idx} has semantic name "
                    f"indices {sorted(slots)}, expected {expected}")
            base, length = directory[key]
            expected_addr = {0: base + (48 if typ == aem.ENTITY else 4)}
            if typ == aem.ENTITY:
                expected_addr[1] = base + 180
            first_name[key] = len(names)
            for semantic in expected:
                addr = slots[semantic]
                if addr != expected_addr[semantic]:
                    raise image.ImageError(
                        f"type 0x{typ:04X} index {idx} semantic name "
                        f"{semantic} points to ROM 0x{addr:04X}, expected "
                        f"0x{expected_addr[semantic]:04X}")
                if addr < base or addr + image.NAME_BYTES > base + length:
                    raise image.ImageError(
                        f"type 0x{typ:04X} index {idx} semantic name "
                        f"{semantic} is outside its descriptor")
                names.append(_text_from_name(
                    rom[addr:addr + image.NAME_BYTES],
                    f"type 0x{typ:04X} index {idx} semantic name {semantic}"))
    return names, first_name


def _descriptor_rows(rom: bytes, M: dict[str, Any],
                     first_name: dict[tuple[int, int], int]) -> list[dict[str, Any]]:
    """One document row per directory entry, carrying its sliced ROM bytes."""
    descriptors = []
    for typ, idx, base, length in M["directory"]:
        desc = {
            "configuration": 0,
            "type": int(typ),
            "index": int(idx),
            "bytes": rom[base:base + length].hex(),
        }
        key = (int(typ), int(idx))
        if key in first_name:
            desc["name_index"] = first_name[key]
        descriptors.append(desc)
    return descriptors


def model_to_document(M: dict[str, Any], ident: dict[str, bytes]) -> dict[str, Any]:
    """gen_aem_store model -> the kl-aem-image document `build()` consumes.

    `M["directory"]` is the authority for both the membership and the byte
    span of every descriptor: entries are `(type, index, base, length)` into
    `M["rom"]`. Slicing the ROM rather than re-deriving the descriptors is the
    point - it is the same bytes the rest of the build agreed on.

    `ident` (identity_from_overlay) is REQUIRED and has no default. The
    Table 7-2 identity used to be applied by RTL at read time and the
    replacement supply chain simply did not carry the step forward; a default
    here would let the next caller drop it just as quietly.

    `M["NAMED"]` is the authority for the semantic names that SET_NAME and
    GET_NAME expose. The image format stores those names in one flat table,
    and its index rows carry the first entry for each descriptor run. This
    join derives that table from the same inline bytes READ_DESCRIPTOR serves,
    so all three command paths start coherent and the packer can enforce that
    they remain structurally addressable.
    """
    rom = apply_identity(M, ident)
    directory = _descriptor_directory(M)
    named = _named_slots(M, directory)
    names, first_name = _name_table(rom, directory, named)
    return {
        "format": "kl-aem-image",
        "version": image.LAYOUT_VERSION,
        "names": names,
        "descriptors": _descriptor_rows(rom, M, first_name),
    }


def main() -> int:
    """Join the two halves for one build configuration: the overlay's model,
    the Table 7-2 identity baked in, packed into the flat image the store
    fetches from `PP_DESC_BASE_P`. Any layout refusal is reported and returns
    1, because an image that packs wrongly enumerates wrongly."""
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("-o", "--out", required=True,
                    help="flat image to write at PP_DESC_BASE_P")
    ap.add_argument("-m", "--map", help="human-readable layout report")
    ap.add_argument("--overlay", required=True,
                    help="sw/builder aem_overlay.json; REQUIRED - it is the "
                         "only statement of the station MAC and entity_id "
                         "the Table 7-2 identity spans need")
    ap.add_argument("--json", default=None,
                    help="also write the intermediate kl-aem-image document")
    ap.add_argument("--line-bytes", type=int, default=576,
                    help="store line-buffer size to validate against; MUST "
                         "match PP_DESC_LINE_BYTES_P or a descriptor longer "
                         "than the buffer would be silently truncated on the "
                         "wire (default 576)")
    args = ap.parse_args()

    overlay, out = Path(args.overlay), Path(args.out)
    ovl = json.loads(overlay.read_text(encoding="utf-8"))
    M = aem.build_model(aem.spec_from_overlay(ovl))

    try:
        doc = model_to_document(M, identity_from_overlay(ovl))
        if args.json:
            Path(args.json).write_text(json.dumps(doc, indent=2),
                                       encoding="utf-8")
        img, report = image.build(doc, args.line_bytes)
    except image.ImageError as exc:
        print(f"gen_aemi_image: {exc}", file=sys.stderr)
        return 1

    out.write_bytes(img)
    #! The two paths are echoed AS THE CALLER TYPED THEM (args.overlay,
    #! args.out), not as the `Path`s above render them: a `Path` drops a
    #! leading `./` and a trailing separator, and this line is what a build
    #! log shows the operator when they go looking for the file they named.
    print(f"[gen_aemi_image] {args.overlay}: {len(doc['descriptors'])} "
          f"descriptors -> {args.out}, {len(img)} bytes")
    if args.map:
        Path(args.map).write_text(report, encoding="utf-8")
    print(report, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
