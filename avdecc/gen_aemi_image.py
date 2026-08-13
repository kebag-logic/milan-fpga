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

USAGE
  avdecc/gen_aemi_image.py -o aem_desc.bin                     # built-in shape
  avdecc/gen_aemi_image.py --overlay sw/builder/out/<cfg>/aem_overlay.json \
                           -o aem_desc.bin -m aem_desc.map

The output is a flat image to be written at `PP_DESC_BASE_P`. `sw/litex`
computes that base from the SoC memory map; it is never restated here, because
this script has no way to know it and a guessed base is worse than no image.
"""
import argparse
import json
import os
import sys

_HERE = os.path.dirname(os.path.abspath(__file__))
_REPO = os.path.dirname(_HERE)
_DESC = os.path.join(_REPO, "protocol-processor", "hdl", "aecp", "desc")

sys.path.insert(0, _HERE)
sys.path.insert(0, _DESC)

import gen_aem_store as aem            # noqa: E402  (path set above)

try:
    import gen_desc_image as image     # noqa: E402
except ImportError:                    # pragma: no cover - submodule missing
    print("gen_aemi_image: the protocol-processor submodule is not checked "
          "out (no %s).\n  git submodule update --init protocol-processor"
          % os.path.relpath(_DESC, _REPO), file=sys.stderr)
    raise SystemExit(2)


def model_to_document(M):
    """gen_aem_store model -> the kl-aem-image document `build()` consumes.

    `M["directory"]` is the authority for both the membership and the byte
    span of every descriptor: entries are `(type, index, base, length)` into
    `M["rom"]`. Slicing the ROM rather than re-deriving the descriptors is the
    point - it is the same bytes the rest of the build agreed on.

    Names are left to the descriptors' own inline `object_name` fields, so no
    name table is emitted (`name_index` unset means "unnamed" to the packer).
    The store's name table is an optimisation for models that share strings;
    this one does not.
    """
    rom = M["rom"]
    descriptors = []
    for typ, idx, base, length in M["directory"]:
        descriptors.append({
            "configuration": 0,
            "type": int(typ),
            "index": int(idx),
            "bytes": rom[base:base + length].hex(),
        })
    return {
        "format": "kl-aem-image",
        "version": image.LAYOUT_VERSION,
        "descriptors": descriptors,
    }


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("-o", "--out", required=True,
                    help="flat image to write at PP_DESC_BASE_P")
    ap.add_argument("-m", "--map", help="human-readable layout report")
    ap.add_argument("--overlay", default=None,
                    help="sw/builder aem_overlay.json; omit for the built-in "
                         "shape")
    ap.add_argument("--json", default=None,
                    help="also write the intermediate kl-aem-image document")
    ap.add_argument("--line-bytes", type=int, default=576,
                    help="store line-buffer size to validate against; MUST "
                         "match PP_DESC_LINE_BYTES_P or a descriptor longer "
                         "than the buffer would be silently truncated on the "
                         "wire (default 576)")
    args = ap.parse_args()

    if args.overlay:
        with open(args.overlay, encoding="utf-8") as fh:
            M = aem.build_model(aem.spec_from_overlay(json.load(fh)))
        origin = args.overlay
    else:
        M = aem.build_model(aem.builtin_spec())
        origin = "built-in spec"

    doc = model_to_document(M)
    if args.json:
        with open(args.json, "w", encoding="utf-8") as fh:
            json.dump(doc, fh, indent=2)

    try:
        img, report = image.build(doc, args.line_bytes)
    except image.ImageError as exc:
        print(f"gen_aemi_image: {exc}", file=sys.stderr)
        return 1

    with open(args.out, "wb") as fh:
        fh.write(img)
    print(f"[gen_aemi_image] {origin}: {len(doc['descriptors'])} descriptors "
          f"-> {args.out}, {len(img)} bytes")
    if args.map:
        with open(args.map, "w", encoding="utf-8") as fh:
            fh.write(report)
    print(report, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
