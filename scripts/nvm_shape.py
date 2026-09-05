#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""nvm_shape.py - one config's persisted shape, and the inventory it implies.

Between the contract and the checks: run the generators for a config, read the
shape back out of what they produced, and expand it into the inventory rows
(`Record`) every later check is expressed over. The donor RTL is read here too
- REC_ID_BASE_P and LAYOUT_VER_P are taken from `KL_acmp_nvm_shadow.sv`
rather than mirrored, which is why this half needs the source list and the
codec half does not.
"""

from __future__ import annotations

import json
import math
import re
import struct
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from nvm_contract import (                                    # noqa: E402
    ALLOC, FIXED, FLASH_PAGE, LEDGER, MAP_ENTRY, NAME_BYTES, NAME_SLOTS, PAY,
    ROOT, SPI_HZ, T_PP_MAX_MS, T_SE_MAX_MS, Record, Shape)


SHADOW_STEM = "KL_acmp_nvm_shadow"
BASE_RE = re.compile(r"parameter\s+logic\s*\[7:0\]\s+REC_ID_BASE_P\s*=\s*8'h([0-9A-Fa-f]{2})")
LAYOUT_RE = re.compile(r"parameter\s+logic\s*\[7:0\]\s+LAYOUT_VER_P\s*=\s*8'h([0-9A-Fa-f]{2})")


def shadow_path() -> Path:
    """Locate the ACMP NVM shadow through the derived submodule source list."""
    sys.path.insert(0, str(ROOT / "scripts"))
    import pp_srcs
    hits = [s for s in pp_srcs.pp_sources()
            if Path(s).stem == SHADOW_STEM]
    if len(hits) != 1:
        sys.exit(f"FATAL: expected exactly one {SHADOW_STEM} source in the "
                 f"derived submodule list, found {len(hits)}. The donor "
                 f"renamed or duplicated it and this gate must be re-pointed, "
                 f"not relaxed.")
    return ROOT / hits[0]


def binding_base() -> int:
    """Read REC_ID_BASE_P out of the donor RTL rather than mirroring it."""
    shadow = shadow_path()
    m = BASE_RE.search(shadow.read_text())
    if not m:
        sys.exit(f"FATAL: REC_ID_BASE_P not found in {shadow.name}; the donor "
                 f"moved the parameter and this gate must be re-pointed, not "
                 f"relaxed.")
    return int(m.group(1), 16)


def layout_version() -> int:
    """Read LAYOUT_VER_P out of the donor RTL, for the same reason as the
    binding base: it is already fixed in landed gateware, and every record this
    gate frames has to carry the value the port will check."""
    shadow = shadow_path()
    m = LAYOUT_RE.search(shadow.read_text())
    if not m:
        sys.exit(f"FATAL: LAYOUT_VER_P not found in {shadow.name}; the donor "
                 f"moved the parameter and this gate must be re-pointed, not "
                 f"relaxed.")
    return int(m.group(1), 16)


def build(cfg: Path, out: Path) -> tuple[int, dict, list, list]:
    """Build one config and return (writable names, descriptor counts, ports)."""
    subprocess.run([sys.executable, str(ROOT / "sw/builder/endstation_builder.py"),
                    str(cfg), "-o", str(out)],
                   check=True, cwd=ROOT, stdout=subprocess.DEVNULL)
    stem = cfg.stem
    overlay = out / stem / "aem_overlay.json"
    img = out / f"{stem}.img.bin"
    subprocess.run([sys.executable, str(ROOT / "avdecc/gen_aemi_image.py"),
                    "--overlay", str(overlay), "-o", str(img),
                    "--line-bytes", "576"],
                   check=True, cwd=ROOT, stdout=subprocess.DEVNULL)
    blob = img.read_bytes()
    _, names = struct.unpack_from(">HH", blob, 8)
    o = json.loads(overlay.read_text())
    ports = o["stream_ports"]
    return names, o["descriptor_counts"], ports["input"], ports["output"]


def expected_names(dc: dict) -> int:
    """Re-derive the writable-name count from the descriptor shape alone.

    This is the SECOND derivation of a number the AEMI image header also
    carries. Grading the inventory against it catches an inventory that drops
    the name class, and grading it against the header catches a builder that
    changes one without the other.
    """
    return sum(dc.get(t, 0) * slots for t, slots in NAME_SLOTS.items())


def expected_records(dc: dict) -> dict:
    """The mandatory group -> cardinality ledger for one shape."""
    return {g: rule(dc) for g, (_cls, _clause, rule) in LEDGER.items()}


def conformant_floor(names: int, dc: dict) -> int:
    """The record count ANY allocation obeying the donor's F07.8 rule needs.

    F07.8 is "one record per item group and index", so the count is fixed by
    the shape and no allocation can do better. A perfectly packed allocation
    would place them at ids 0 .. floor-1, so `floor > FIXED.ID_SPACE` is an
    impossibility proof rather than a property of the layout in ALLOC.
    """
    return sum(expected_records(dc).values()) + names


def commit_worst_ms(image: int) -> float:
    """Worst-case flash transaction time for one whole-image A/B commit."""
    pages = math.ceil(image / FLASH_PAGE)
    readback_ms = image * 8 * 1000.0 / SPI_HZ
    return T_SE_MAX_MS + pages * T_PP_MAX_MS + readback_ms


def inventory(shape: Shape, base: int) -> list[Record]:
    """Return the record list: (group, index, id, payload_bytes)."""
    names, dc = shape.names, shape.dc
    recs = []

    def add(group: str, index: int, payload: int) -> None:
        """Append one row, with an id only when the group's block reaches
        this index; a row with no id is check 1's finding, not an error."""
        b, block = ALLOC[group]
        if group == "BINDING":
            b = base
        if index >= block:
            recs.append((group, index, None, payload, block))
        else:
            recs.append((group, index, b + index, payload, block))

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
        add("MAPS_OUT", p["index"], p["clusters"] * MAP_ENTRY)

    for n in range(names):
        add("NAME", n, NAME_BYTES)
    return recs
