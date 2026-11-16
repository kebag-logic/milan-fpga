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


def descriptors(blob: bytes) -> dict[tuple[int, int, int], bytes]:
    """Each descriptor's bytes in the image by (configuration, type, index), as aecp_image.c loads them."""
    entries = struct.unpack_from(">H", blob, 8)[0]
    directory = struct.unpack_from(">I", blob, 12)[0]
    found = {}
    for row in range(entries):
        cfg, typ, count, length, offset, _, stride = struct.unpack_from(">HHHHIHH", blob, directory + row * 16)
        for n in range(count):
            value = blob[offset + stride * n:offset + stride * n + length]
            found[cfg, typ, struct.unpack_from(">H", value, 2)[0]] = value
    return found


def key_domain(blob: bytes) -> list[str]:
    """The keys an AUDIO_MAP edit may hold (aecp_maps.c, #904, #894): at an output port a STREAM_OUTPUT and
    its channel, at an input port one of the port's clusters and its channel. The most streams and clusters
    a key may name, and the most channels each may have: every format a STREAM_OUTPUT advertises, and every
    cluster of a STREAM_PORT_INPUT, in any configuration."""
    found = descriptors(blob)

    def channels(value: bytes, at: int) -> int:
        """The AAF channel count of the stream format at `at`, 0 for any other format (aecp_maps.c, channels)."""
        word = struct.unpack_from(">Q", value, at)[0]
        return (word >> 22) & 1023 if word >> 56 == 2 else 0

    streams, stream_channels, clusters, cluster_channels = 0, 0, 0, 0
    for (cfg, typ, index), value in found.items():
        if typ == 6:
            start, count = struct.unpack_from(">HH", value, 82)
            widths = [channels(value, 74), *(channels(value, start + 8 * n) for n in range(count))]
            streams, stream_channels = max(streams, index + 1), max(stream_channels, *widths)
        if typ == 14:
            number, base = struct.unpack_from(">HH", value, 12)
            clusters = max(clusters, number)
            for n in range(number):
                cluster = found[cfg, 20, base + n]
                cluster_channels = max(cluster_channels, struct.unpack_from(">H", cluster, 84)[0])
    return [f"#define AECP_ENTITY_KEY_STREAMS {streams}u",
            f"#define AECP_ENTITY_KEY_STREAM_CHANNELS {stream_channels}u",
            f"#define AECP_ENTITY_KEY_CLUSTERS {clusters}u",
            f"#define AECP_ENTITY_KEY_CLUSTER_CHANNELS {cluster_channels}u"]


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
                ordinals[name + n] = (typ, first + n, 0)
            if typ == 0:
                ordinals[name + 1] = (0, 0, 1)
    if any(item is None for item in ordinals):
        raise ValueError("image has an unassigned writable name")
    runs = []  # the table's runs (aecp_nvm.h struct aecp_name_run): type, index, count, ordinal, name
    for ordinal, (typ, index, second) in enumerate(ordinals):
        if runs and not second and not runs[-1][4] and runs[-1][0] == typ and runs[-1][1] + runs[-1][2] == index:
            runs[-1][2] += 1
        else:
            runs.append([typ, index, 1, ordinal, second])
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
              f"#define AECP_ENTITY_OUTPUTS {overlay['descriptor_counts']['STREAM_OUTPUT']}u", *key_domain(blob)]
    result += [f"#define AECP_ENTITY_NAME_RUNS {len(runs)}u"]
    result += table_macro("AECP_ENTITY_NAMES_INIT", [f"{{AECP_CHANGE_NAME,{t},{i},{s}}}" for t, i, s in ordinals])
    result += table_macro("AECP_ENTITY_NAME_RUNS_INIT", ["{" + ",".join(map(str, r)) + "}" for r in runs])
    result += table_macro("AECP_ENTITY_MAPS_INIT(rows)", maps)
    # aecp_maps.c reads the constants alone; the tables below are each including unit's own
    result += ["#ifndef AECP_ENTITY_SHAPE_ONLY", "static const struct aecp_mapping aecp_map_defaults[] = {",
               *[f"\t{row}," for row in defaults or ["{0,0,0,0}"]], "};"]
    return result
