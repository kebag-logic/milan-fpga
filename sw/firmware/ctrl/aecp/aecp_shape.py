# SPDX-License-Identifier: CERN-OHL-W-2.0
"""Derive static AECP map pools and name ordinals from existing shape outputs."""
from __future__ import annotations
import struct
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
sys.path.insert(0, str(ROOT / "scripts"))
from nvm_contract import Shape
from nvm_shape import output_map_entries


def table_macro(name: str, rows: list[str]) -> list[str]:
    """Emit an initializer, without allocating another writable table."""
    return [f"#define {name} {{ \\", *[f"\t{row}, \\" for row in rows], "}"]


def storage(overlay: dict, blob: bytes) -> list[str]:
    """The #658 identity and DR5 record capacities, independent of live state."""
    entries, names = struct.unpack_from(">HH", blob, 8)
    directory = struct.unpack_from(">I", blob, 12)[0]
    ordinals = [None] * names
    indexes = {}
    for row in range(entries):
        cfg, typ, count, _, _, name, _ = struct.unpack_from(">HHHHIHH", blob, directory + row * 16)
        first = indexes.get((cfg, typ), 0)
        indexes[cfg, typ] = first + count
        if name != 0xffff:
            for n in range(count):
                ordinals[name + n] = f"{{AECP_CHANGE_NAME,{typ},{first+n},0}}"
            if typ == 0:
                ordinals[name + 1] = "{AECP_CHANGE_NAME,0,0,1}"
    if any(item is None for item in ordinals):
        raise ValueError("image has an unassigned writable name")
    ports = overlay["stream_ports"]
    shape = Shape(Path(), names, overlay["descriptor_counts"], ports["input"], ports["output"])
    maps, defaults = [], []
    total, maximum = 0, 0
    for direction, typ in (("input", 14), ("output", 15)):
        streams = overlay["stream_inputs" if typ == 14 else "stream_outputs"]
        for index, port in enumerate(ports[direction]):
            if port.get("map_mode") != "dynamic":
                continue
            capacity = port["clusters"] if typ == 14 else output_map_entries(shape, port)
            start = len(defaults)
            if index < len(streams) and streams[index].get("kind", "aaf") == "aaf":
                channels = (int(streams[index]["formats"][0], 16) >> 22) & 1023
                defaults += [f"{{{index},{channel},{channel},0}}"
                             for channel in range(min(8, channels, port["clusters"]))]
            count = len(defaults) - start
            page = port["map_page"] if typ == 14 else 176
            maps.append(f"{{{typ},{index},0,{page},(rows)+{total},0,{capacity},"
                        f"aecp_map_defaults+{start},{count}}}")
            total += capacity
            maximum = max(maximum, capacity)
    result = [f"#define AECP_ENTITY_NAMES {names}u", f"#define AECP_ENTITY_MAPS {len(maps)}u",
              f"#define AECP_ENTITY_MAP_ROWS {total}u", f"#define AECP_ENTITY_MAP_MAX {maximum}u",
              f"#define AECP_ENTITY_OUTPUTS {overlay['descriptor_counts']['STREAM_OUTPUT']}u"]
    result += table_macro("AECP_ENTITY_NAMES_INIT", ordinals)
    result += table_macro("AECP_ENTITY_MAPS_INIT(rows)", maps)
    result += ["static const struct aecp_mapping aecp_map_defaults[] = {",
               *[f"\t{row}," for row in defaults or ["{0,0,0,0}"]], "};"]
    return result
