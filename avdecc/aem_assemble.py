#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""Assembly: a spec becomes a directory, a ROM image and its tables.

Split out of `gen_aem_store.py` (Rule 12). This is the file that decides
WHERE each descriptor sits - the two-level directory, the ROM image, the
overlay and write-back spans, the per-stream and dynamic-map tables - and
`build_model()` is the one entry point that returns all of it as a model
dict. The octets it places come from `aem_descriptors`, the map tables from
`aem_maps`, and the builtin shape from `aem_specs`.

Importing this module BUILDS the builtin model (`_M` and its aliases), which
is what importers of `gen_aem_store` have always got at import time.

`gen_aem_store` re-exports every name here.
"""
from collections.abc import Sequence
from typing import Any

from aem_descriptors import (AUDIO_CLUSTER, AUDIO_MAP, AUDIO_UNIT,
                             AVB_INTERFACE, CLOCK_DOMAIN, CLOCK_SOURCE,
                             CONFIGURATION, CONTROL, ENTITY, LOCALE,
                             NO_STRING, STREAM_INPUT, STREAM_OUTPUT,
                             STREAM_PORT_INPUT, STREAM_PORT_OUTPUT, STRINGS,
                             PortMapBounds, clock_source_shape,
                             d_audio_cluster, d_audio_map, d_audio_unit,
                             d_avb_interface, d_clock_domain, d_clock_source,
                             d_configuration, d_control_identify, d_entity,
                             d_locale, d_stream, d_stream_port, d_strings)
from aem_maps import static_map_tables
from aem_specs import builtin_spec

# ------------------------------------------------------------- assembly ----
def two_level_directory(
        directory: Sequence[tuple[int, int, int, int]]) -> dict[str, Any]:
    """Level-1 (type-direct-indexed) view of the descriptor directory.

    Derives, per descriptor type, {row of its first entry, entry count} and
    ASSERTS the layout the RTL's direct-indexed lookup depends on: each
    type's entries form ONE contiguous run of AEM_DIR_C rows, zero-based
    and ascending in descriptor_index. build_model's append order gives
    this structurally today; the assert turns a future interleave into a
    loud generator refusal instead of a silent mis-serve by the accessor.

    The table is zero-padded to a power of two (1 << AW rows) so the RTL
    can index it with the type's low bits unclamped: an absent type reads
    count 0 (miss) and a type at/above N is excluded by one range check.
    """
    runs = {}                       # type -> [first row, count]
    prev_t = None
    for row, (t, i, _b, _l) in enumerate(directory):
        if t not in runs:
            runs[t] = [row, 0]
        elif prev_t != t:
            raise ValueError(
                f"descriptor type 0x{t:04X} rows are not contiguous in the "
                f"directory (row {row} re-opens a run closed at row "
                f"{runs[t][0] + runs[t][1]}) - the two-level accessor "
                "needs one run per type; fix build_model's append order")
        if i != runs[t][1]:
            raise ValueError(
                f"type 0x{t:04X} descriptor_index not zero-based ascending: "
                f"row {row} carries index {i}, expected {runs[t][1]}")
        runs[t][1] += 1
        prev_t = t
    max_t = max(runs)
    if max_t >= 256:
        raise ValueError(
            f"descriptor type 0x{max_t:04X} would need a {max_t + 1}-row "
            "direct-indexed level-1 table - add a sparse first level "
            "before building models with types this high")
    aw = max(1, (max_t).bit_length())
    n = 1 << aw
    return dict(AW=aw, N=n,
                CNT=[runs.get(t, [0, 0])[1] for t in range(n)],
                ROW=[runs.get(t, [0, 0])[0] for t in range(n)])


def _two_level_resolve(l1, directory, t, i):
    """The RTL accessor's answer, modelled bit-for-bit: (found, base, len)."""
    if t >= l1["N"]:
        return (0, 0, 0)
    cnt, row = l1["CNT"][t], l1["ROW"][t]
    if i >= cnt:
        return (0, 0, 0)
    _t, _i, b, l = directory[row + i]
    return (1, b, l)


def check_two_level(l1: dict[str, Any],
                    directory: Sequence[tuple[int, int, int, int]]) -> None:
    """1:1 equivalence gate: the two-level resolve answers EXACTLY like the
    linear scan it replaces, hits and misses alike, for every directory
    entry plus a fence of miss probes (index past each run, absent types,
    types past the table). Raises on the first divergence."""
    def linear(t: int, i: int) -> tuple[int, int, int]:
        """The scan the accessor replaces, kept as the reference answer."""
        f = (0, 0, 0)
        for (tt, ii, b, l) in directory:
            if tt == t and ii == i:
                f = (1, b, l)
        return f

    probes = set()
    for (t, i, _b, _l) in directory:
        probes |= {(t, i), (t, i + 1), (t, 0xFFFF)}
    for t in range(l1["N"] + 4):
        probes |= {(t, 0), (t, 1)}
    probes.add((0xFFFF, 0))
    for (t, i) in sorted(probes):
        want = linear(t, i)
        got = _two_level_resolve(l1, directory, t, i)
        if got != want:
            raise ValueError(
                f"two-level directory diverges from the linear scan at "
                f"type 0x{t:04X} index {i}: linear {want}, two-level {got}")


def named_structure(
        l1: dict[str, Any],
        directory: Sequence[tuple[int, int, int, int]],
        named: Sequence[tuple[int, int, int, int]],
) -> tuple[int, list[tuple[int, int, int, int]]]:
    """Split the SET/GET_NAME table into the structural rule + exceptions.

    Structural: a type whose EVERY directory entry is named, at name_index
    0, with object_name at descriptor base + 4 - resolvable through the
    two-level directory (mask hit -> AEM_DIR_C[row + index].base + 4).
    Everything else (ENTITY's two names at 48/180) stays an explicit
    emitted match line. Returns (mask, exceptions); raises if the split
    does not reproduce the NAMED list 1:1, hits and misses alike."""
    base = {(t, i): b for (t, i, b, _l) in directory}
    per_type = {}
    for (t, i, nidx, addr) in named:
        per_type.setdefault(t, []).append((i, nidx, addr))
    mask, exc = 0, []
    for t, entries in sorted(per_type.items()):
        structural = (
            t < l1["N"]
            and all(nidx == 0 and addr == base[(t, i)] + 4
                    for (i, nidx, addr) in entries)
            and sorted(i for (i, _n, _a) in entries)
            == list(range(l1["CNT"][t])))
        if structural:
            mask |= 1 << t
        else:
            exc += [(t, i, nidx, addr) for (i, nidx, addr) in entries]
    check_named(l1, directory, named, mask, exc)
    return mask, exc


def check_named(
        l1: dict[str, Any],
        directory: Sequence[tuple[int, int, int, int]],
        named: Sequence[tuple[int, int, int, int]],
        mask: int,
        exc: Sequence[tuple[int, int, int, int]],
) -> None:
    """1:1 equivalence gate for the name split: mask + exceptions answer
    EXACTLY like the flat NAMED table, hits and misses alike."""
    def resolve(t: int, i: int, nidx: int) -> tuple[int, int]:
        """The RTL's name lookup: `(found, object_name address)`."""
        for (et, ei, en, ea) in exc:
            if (t, i, nidx) == (et, ei, en):
                return (1, ea)
        if (t < l1["N"] and nidx == 0 and (mask >> t) & 1
                and i < l1["CNT"][t]):
            return (1, directory[l1["ROW"][t] + i][2] + 4)
        return (0, 0)

    want = {(t, i, n): a for (t, i, n, a) in named}
    probes = set(want)
    for (t, i, n) in list(want):
        probes |= {(t, i + 1, n), (t, i, n + 1), (t, 0xFFFF, n)}
    for t in range(l1["N"] + 4):
        probes.add((t, 0, 0))
    for key in sorted(probes):
        got = resolve(*key)
        exp = (1, want[key]) if key in want else (0, 0)
        if got != exp:
            raise ValueError(
                f"structural name lookup diverges from the NAMED table at "
                f"type 0x{key[0]:04X} index {key[1]} name_index {key[2]}: "
                f"table {exp}, structural {got}")


def _port_bounds(p):
    """A spec port's 7.2.13 bounds; a dynamic port declares no static map."""
    dyn = p.get("map_mode", "static") == "dynamic"
    return PortMapBounds(clusters=p["clusters"],
                         base_cluster=p["base_cluster"],
                         maps=0 if dyn else p["maps"],
                         base_map=0 if dyn else p["base_map"])


def _entity_descriptors(spec):
    """ENTITY through STRINGS: the descriptors a configuration always has."""
    si, so = spec["stream_inputs"], spec["stream_outputs"]
    descs = [
        (ENTITY,        0, d_entity(spec["entity"])),
        (CONFIGURATION, 0, d_configuration(len(si), len(so),
                                           len(spec["clock_sources"]))),
        (AUDIO_UNIT,    0, d_audio_unit(spec["rates"], spec["current_rate"],
                                        len(spec["ports_in"]),
                                        len(spec["ports_out"]))),
    ]
    for k, s in enumerate(si):
        descs.append((STREAM_INPUT, k,
                      d_stream(STREAM_INPUT, k, s["name"], 0x0003,
                               s["formats"], s["buffer"])))
    for k, s in enumerate(so):
        # CRF Media Clock Output (Milan 7.2.3): CLOCK_SYNC_SOURCE|CLASS_A
        # (1722.1 7.2.6.1 - the stream IS a clock sync source; Milan 7.3.3
        # mandates Class A). AAF outputs keep the deployed CLASS_A-only word.
        # Both get clock_domain_index 0 (7.2.6): 7.2.9.2 has no OUTPUT_STREAM
        # CLOCK_SOURCE type - domain membership is the STREAM field itself.
        flags = 0x0003 if s.get("kind", "aaf") == "crf" else 0x0002
        descs.append((STREAM_OUTPUT, k,
                      d_stream(STREAM_OUTPUT, k, s["name"], flags,
                               s["formats"])))
    descs.append((AVB_INTERFACE, 0, d_avb_interface(spec.get("gptp"))))
    for k, cs in enumerate(spec["clock_sources"]):
        descs.append((CLOCK_SOURCE, k,
                      d_clock_source(k, cs["name"], cs["cs_type"],
                                     cs["loc_type"], cs["loc_index"])))
    descs.append((CLOCK_DOMAIN, 0, d_clock_domain(len(spec["clock_sources"]))))
    descs.append((CONTROL, 0, d_control_identify()))
    descs.append((LOCALE, 0, d_locale()))
    descs.append((STRINGS, 0, d_strings(
        [spec["entity"]["name"], spec["rates_string"],
         spec["entity"]["vendor_name"], "", "", "", ""])))
    return descs


def _port_descriptors(spec):
    """STREAM_PORTs, their AUDIO_CLUSTERs and the AUDIO_MAPs they address."""
    descs = []
    # map_mode (gaps item 8, dynamic audio maps): a "dynamic" port carries
    # NO AUDIO_MAP descriptor and advertises number_of_maps=0 / base_map=0 -
    # the 1722.1-2021 7.2.13 dynamic-mapping capability signal ("These
    # Entities set the number_of_maps field to zero (0) and the base_map
    # field is ignored"). Milan v1.2 5.3.3.9 makes that the SHALL on the
    # listener side ("The Stream Port Input of a Configuration shall not
    # contain any AUDIO_MAP descriptor. Note: this means that a PAAD-AE
    # implements dynamic mappings on all of its Stream Port Inputs"), so
    # ANY subset of the input ports may be dynamic (roadmap 23). Outputs
    # stay static: 5.3.3.9 leaves them free and 5.4.2.26-28 mandate
    # NOT_SUPPORTED for a Stream Port Output that HAS Audio Maps.
    for k, p in enumerate(spec["ports_in"]):
        descs.append((STREAM_PORT_INPUT, k,
                      d_stream_port(STREAM_PORT_INPUT, k, 0x0001,
                                    _port_bounds(p))))
    # Outputs MAY be dynamic too (USER 08-01): Milan 5.3.3.9 leaves them
    # free, and 5.4.2.26-28 make GET/ADD/REMOVE_AUDIO_MAPPINGS a SHALL for
    # "each Stream Port Output that has no Audio Map" - so a dynamic output
    # port drops its AUDIO_MAP descriptor and signals 7.2.13 exactly like a
    # dynamic input.
    for k, p in enumerate(spec["ports_out"]):
        descs.append((STREAM_PORT_OUTPUT, k,
                      d_stream_port(STREAM_PORT_OUTPUT, k, 0x0000,
                                    _port_bounds(p))))
    n_in = sum(p["clusters"] for p in spec["ports_in"])
    n_out = sum(p["clusters"] for p in spec["ports_out"])
    # AUDIO_CLUSTER object_names (builder D10). Before 2026-07-28 every
    # cluster of every shape was literally named "Input" or "Output", which
    # told a controller operator nothing: on an 8x8 board Hive showed eighty
    # identical rows and no way to tell a pilot tone from a dead TDM slot
    # from a loopback lane. Names now come from the cluster's ROLE (the
    # builder's cluster_names(); the overlay carries them per cluster).
    # 1722.1-2021 6.2.2.8 lists object_name among the fields EXCLUDED from
    # "the structure of the data model", so this rename does NOT bump any
    # entity_model_id - and the descriptor is fixed-width (cstr pads to 64),
    # so no offset, length or directory entry moves either.
    names_in = spec.get("cluster_names_in") or ["Input"] * n_in
    names_out = spec.get("cluster_names_out") or ["Output"] * n_out
    if len(names_in) != n_in or len(names_out) != n_out:
        raise ValueError(f"cluster name count {len(names_in)}/{len(names_out)}"
                         f" != cluster count {n_in}/{n_out}")
    for k in range(n_in):
        descs.append((AUDIO_CLUSTER, k,
                      d_audio_cluster(k, names_in[k], NO_STRING)))
    for k in range(n_in, n_in + n_out):
        descs.append((AUDIO_CLUSTER, k,
                      d_audio_cluster(k, names_out[k - n_in], AUDIO_UNIT)))
    for k, rows in enumerate(spec["audio_maps"]):
        descs.append((AUDIO_MAP, k, d_audio_map(k, rows)))
    return descs


def _rom_image(descs):
    """The flat ROM and its `(type, index, base, length)` directory."""
    rom = b""
    directory = []           # (type, index, base, length)
    for t, i, img in descs:
        directory.append((t, i, len(rom), len(img)))
        rom += img
    n_clusters = sum(1 for t, _i, _img in descs if t == AUDIO_CLUSTER)
    # The svh addresses the store with 16-bit words throughout (AEM_DIR_C
    # {type, index, base, len}, the overlay/write-back/name tables, the MVU
    # scratch tail), so a ROM past 64 KiB would silently wrap instead of
    # failing. Say so here: the builder catches this as aem_rom_unsupported
    # and marks the shape "planned" rather than emitting a broken ROM.
    # Growing past this is D6's job (BRAM hot stub + DRAM bulk tree).
    if len(rom) + 64 > 0x10000:
        raise ValueError(
            f"AEM ROM {len(rom)} B + 64 B MVU scratch exceeds the 16-bit "
            f"store address space (65536 B) - {len(directory)} descriptors, "
            f"{n_clusters} AUDIO_CLUSTERs at {len(d_audio_cluster(0, '', 0))}"
            " B each. A model this large is the D6 split (BRAM hot stub + "
            "DRAM bulk descriptor tree), not a wider ROM")
    return rom, directory


def _read_overlays(base_of):
    """The ROM spans the live CSR/state wires overwrite as they are read."""
    # Dynamic read overlays: (rom_addr, nbytes, source). Sources are resolved
    # by KL_aecp_aem_dyn_mux from the live CSR/state wires.
    E = base_of(ENTITY); A = base_of(AVB_INTERFACE)
    overlays = [
        (E + 4,   8, "ENTITY_ID"),
        (E + 12,  8, "MODEL_ID"),
        (E + 20,  4, "ECAPS"),
        (E + 24,  2, "TALKER_SRC"),
        (E + 26,  2, "TALKER_CAP"),
        (E + 28,  2, "LISTEN_SINK"),
        (E + 30,  2, "LISTEN_CAP"),
        (E + 32,  4, "CTRL_CAP"),
        (E + 36,  4, "AVAIL_IDX"),
        (E + 40,  8, "ASSOC_ID"),
        (E + 48,  8, "ENT_NAME8"),   # first 8 chars of entity_name: board name
                                     # ("ARTY"/"ALINX") from the CSR, S50-set
        (E + 310, 2, "CURRENT_CFG"),
        (A + 70,  6, "MAC"),
        (A + 78,  8, "CLOCK_ID"),
    ]
    return overlays


def _writeback_targets(spec, base_of):
    """SET_* write-back addresses: which ROM field each command lands in."""
    si = spec["stream_inputs"]
    # SET_* write-back targets (rom_addr of the field inside its descriptor).
    # NOTE: the legacy WB_STREAM_FORMAT_C symbol reaches STREAM_OUTPUT[0]
    # only; multi-stream shapes get the per-descriptor WB_STRIN/STROUT_FMT_
    # ADDR_C arrays (PER_STREAM below) the gated RTL path indexes instead.
    wb = {
        "SAMPLING_RATE":   base_of(AUDIO_UNIT) + 136,
        "STREAM_FORMAT":   base_of(STREAM_OUTPUT) + 74,   # STREAM_OUTPUT[0] current
    }
    for k in range(len(si)):
        wb[f"STREAM_IN{k}_FMT"] = base_of(STREAM_INPUT, k) + 74
    wb["CLOCK_SRC_IDX"] = base_of(CLOCK_DOMAIN) + 70      # clock_source_index
    wb["CONTROL_CUR"] = base_of(CONTROL) + 108            # IDENTIFY current_value
    for k in range(len(spec["audio_maps"])):
        wb[f"AUDIO_MAP_{k}"] = base_of(AUDIO_MAP, k)      # GET_AUDIO_MAP source
    return wb


def _named_addresses(directory, entity_base):
    """SET/GET_NAME directory: (type, index, name_index) -> object_name addr."""
    E = entity_base
    # SET/GET_NAME directory: (type, index, name_index) -> object_name addr.
    # ENTITY carries two names (entity_name / group_name); every other named
    # descriptor has object_name at base+4, name_index 0.
    named = [(ENTITY, 0, 0, E + 48), (ENTITY, 0, 1, E + 180)] + [
        (t, i, 0, b + 4)
        for (t, i, b, _) in directory
        if t in (CONFIGURATION, AUDIO_UNIT, STREAM_INPUT, STREAM_OUTPUT,
                 AVB_INTERFACE, CLOCK_SOURCE, CLOCK_DOMAIN, CONTROL,
                 AUDIO_CLUSTER)
    ]
    return named


def _per_stream_tables(spec, base_of):
    """Per-descriptor stream-format tables, and whether the svh emits them."""
    si, so = spec["stream_inputs"], spec["stream_outputs"]
    # Per-descriptor stream-format tables (item-4 follow-up): kind flag,
    # reference entry (formats[0] = the current/base format the RTL
    # validates against) and SET/GET write-back address per STREAM_INPUT/
    # STREAM_OUTPUT descriptor. EMIT gates the svh block behind the stream
    # count so the deployed 1-AAF-in/1-out shape's svh (and the RTL path it
    # compiles) stays byte-identical (see emit_svh).
    per_stream = dict(
        IN_CRF=[s.get("kind", "aaf") == "crf" for s in si],
        IN_FMT0=[s["formats"][0] for s in si],
        OUT_FMT0=[s["formats"][0] for s in so],
        IN_WB=[base_of(STREAM_INPUT, k) + 74 for k in range(len(si))],
        OUT_WB=[base_of(STREAM_OUTPUT, k) + 74 for k in range(len(so))],
        EMIT=(len(si) > 2 or len(so) > 1),
    )
    return per_stream


def _dynmap_tables(spec):
    """Listener-side dynamic audio-map engine constants (empty when static)."""
    si = spec["stream_inputs"]
    # Dynamic-map engine constants (gaps item 8, generalized to EVERY
    # STREAM_PORT_INPUT by roadmap 23). Gated exactly like PER_STREAM:
    # emitted ONLY when at least one input port is map_mode dynamic, so a
    # fully static shape's svh (and the RTL path it compiles) stays
    # byte-identical. Milan 5.4.2.26 partitioning: a port's cluster channels
    # (mono clusters, d_audio_cluster channel_count=1 => keys == clusters)
    # are split into fixed subsets of PAGE keys; number_of_maps =
    # ceil(clusters/PAGE) is returned per port no matter the live mapping
    # count. PAGE is capped at 9 by the RTL const-scratch: the page walk's
    # last row starts at 6 + 8*(PAGE-1) and is 8 bytes long, so 8*PAGE + 5
    # must stay inside const_q's 80 bytes. It is SHARED by every dynamic
    # port (the RTL page origin is a constant multiply); per-port cluster
    # counts may still differ.
    #
    # The store key is the GLOBAL cluster index (base_cluster + offset),
    # which is exactly the render crossbar's map-RAM address - one key space
    # for the model, the fabric and the CSR 0x900 debug port alike.
    pin, pout = spec["ports_in"], spec["ports_out"]
    dyn_in = [p for p in pin if p.get("map_mode", "static") == "dynamic"]
    dynmap = dict(EMIT=bool(dyn_in))
    if dynmap["EMIT"]:
        explicit = {int(p["map_page"]) for p in dyn_in if p.get("map_page")}
        if len(explicit) > 1:
            raise ValueError("every dynamic STREAM_PORT_INPUT must share one "
                             f"map_page (RTL partition constant): "
                             f"{sorted(explicit)}")
        page = explicit.pop() if explicit \
            else min(max(p["clusters"] for p in dyn_in), 8)
        if not 1 <= page <= 9:
            raise ValueError(f"map_page {page} outside 1..9 (the RTL "
                             "GET_AUDIO_MAP const-scratch bound)")
        keys = max(p["base_cluster"] + p["clusters"] for p in dyn_in)
        if keys > 64:
            raise ValueError(f"{keys} dynamic cluster keys exceeds the 64-key "
                             "render map address space (chmap64)")

        def _dyn(p):
            return p.get("map_mode", "static") == "dynamic"

        # A mapping may reference ANY STREAM_INPUT (1722.1-2021 Table 7-33:
        # mapping_stream_index is "the STREAM_INPUT or STREAM_OUTPUT
        # descriptor index for the stream carrying this channel"), so the
        # engine validates the stream channel against THAT stream's current
        # format (Milan 5.3.10.1 / 5.4.2.27). CRF inputs carry no audio
        # channels and are not mappable.
        si_aaf = [s.get("kind", "aaf") == "aaf" for s in si]
        si_ch = [((s["formats"][0] >> 22) & 0x3FF) if a else 0
                 for s, a in zip(si, si_aaf)]
        dynmap.update(
            KEYS=keys, PAGE=page,
            NPORTS=len(pin),
            PDYN=[_dyn(p) for p in pin],
            PBASE=[p["base_cluster"] for p in pin],
            PCLS=[p["clusters"] for p in pin],
            #: dynamic -> ceil(clusters/PAGE) partitions; static -> its
            #: declared AUDIO_MAP count (GET serves the ROM descriptor)
            PNMAPS=[(-(-p["clusters"] // page) if _dyn(p) else p["maps"])
                    for p in pin],
            NSTRIN=len(si), SAAF=si_aaf, SCH=si_ch,
            PHYS=CHMAP_PHYS_DEPTH)
    return dynmap


def _odmap_tables(spec, dynmap_emit):
    """Talker-side dynamic audio-map engine constants (empty when static)."""
    so = spec["stream_outputs"]
    pout = spec["ports_out"]
    # Talker-side dynamic-map engine constants (USER 08-01: "enable dynamic
    # mapping on stream_output as well"). Gated like DYNMAP: emitted only
    # when at least one OUTPUT port is map_mode dynamic. The engine's key is
    # the port's STREAM channel (Milan 5.4.2.26 note: "at most one dynamic
    # mapping per Stream Output's channel" - the stream channel is the
    # natural unique key), 8 keys per port (the DMAP_CHMAX ch[2:0] fabric
    # bound). Vendor validity rules (1722.1-2021 7.4.45.1 says validity "is
    # governed by a set of vendor defined rules"):
    #   * mapping_stream_index must be the port's OWN stream (the capture
    #     crossbar routes port j's clusters into stream j - 1:1 fabric);
    #   * records arrive in L/R-adjacent pairs mapping stream channels
    #     {2m, 2m+1} to the two halves of ONE source pair (the capture map
    #     is PAIR-slot granular; a half-armed slot would make GET report a
    #     route that carries no audio - the same wire-truth refusal the
    #     input side applies to keys past the render crossbar);
    #   * a cluster is projectable only where CSRC marks a live source
    #     behind it (ring/tone/loopback/physical bounds, resolved HERE).
    # The partition of 5.4.2.26 is over the Stream Output's channels: <= 8
    # of them, so every port is a single page (number_of_maps = 1).
    dyn_out = [p for p in pout if p.get("map_mode", "static") == "dynamic"]
    odmap = dict(EMIT=bool(dyn_out))
    if odmap["EMIT"] and not dynmap_emit:
        # the RTL nests `AEM_ODYNMAP inside `AEM_DYNMAP (the walk states are
        # shared), and Milan 5.3.3.9 makes dynamic INPUTS mandatory anyway
        raise ValueError("dynamic STREAM_PORT_OUTPUTs require dynamic "
                         "STREAM_PORT_INPUTs (Milan 5.3.3.9 mandates them)")
    if odmap["EMIT"]:
        so_ch = [((s["formats"][0] >> 22) & 0x3FF) for s in so]
        # packetizer pair-slot base per STREAM_OUTPUT (its prefix-sum space)
        slotb_str, acc = [], 0
        for c in so_ch:
            slotb_str.append(acc)
            acc += (c + 1) // 2
        pcbase, csrc, init = [], [], []
        for j, p in enumerate(pout):
            pcbase.append(len(csrc))
            stream = p.get("stream_index", j)
            srcs = p.get("cluster_sources")
            if srcs is None:
                if p.get("map_mode", "static") == "dynamic":
                    raise ValueError(
                        f"ports_out[{j}]: dynamic output lacks explicit "
                        "cluster_sources/source topology; regenerate the "
                        "AEM overlay")
                # A static port needs no capture-crossbar template. Keep a
                # zero-invalid row only so a mixed legacy model retains the
                # table shape when another port enables the dynamic engine.
                srcs = [dict(src=0, idxh=0, idx=0, half=0, valid=False)
                        for _ in range(p["clusters"])]
            if len(srcs) != p["clusters"]:
                raise ValueError(
                    f"ports_out[{j}]: {len(srcs)} cluster_sources for "
                    f"{p['clusters']} clusters")
            csrc.extend(srcs)
            # identity image: stream channel c <- the port's primary
            # cluster run (offset c of the identity rows the static map
            # declared), kept only where the source pair really projects
            ic0 = p.get("identity_offset", 0)
            for c in range(8):
                co = ic0 + c
                ok = (c < so_ch[stream] and co < p["clusters"]
                      and srcs[co].get("valid", True)
                      and (srcs[co]["src"] == 4 or srcs[co]["half"] == c % 2))
                init.append(dict(v=ok, co=co if ok else 0))
        odmap.update(
            KEYS=8 * len(pout), NPORTS=len(pout),
            PDYN=[p.get("map_mode", "static") == "dynamic" for p in pout],
            PCLS=[p["clusters"] for p in pout],
            PCBASE=pcbase,
            PSTR=[p.get("stream_index", j) for j, p in enumerate(pout)],
            SLOTB=[slotb_str[p.get("stream_index", j)]
                   for j, p in enumerate(pout)],
            SCH=[so_ch[p.get("stream_index", j)]
                 for j, p in enumerate(pout)],
            CSRC=csrc, INIT=init)
    return odmap


def build_model(spec: dict[str, Any]) -> dict[str, Any]:
    """Assemble ROM + directory + overlay/write-back/name tables from a spec
    (builtin_spec() or spec_from_overlay()). Returns the model dict the
    emitters consume."""
    si, so = spec["stream_inputs"], spec["stream_outputs"]
    descs = _entity_descriptors(spec) + _port_descriptors(spec)
    rom, directory = _rom_image(descs)

    def base_of(t: int, i: int = 0) -> int:
        """This model's ROM offset for one `(type, index)` descriptor."""
        return next(b for (tt, ii, b, _) in directory if tt == t and ii == i)

    overlays = _read_overlays(base_of)
    wb = _writeback_targets(spec, base_of)
    named = _named_addresses(directory, base_of(ENTITY))

    # svh validation tables: first AAF input / the CRF input (the legacy
    # single-stream symbols, always emitted — the RTL default/reset reach)
    fmts = next(s["formats"] for s in si if s.get("kind", "aaf") == "aaf")
    crf_fmts = next(s["formats"] for s in si if s.get("kind") == "crf")

    per_stream = _per_stream_tables(spec, base_of)
    dynmap = _dynmap_tables(spec)
    odmap = _odmap_tables(spec, dynmap["EMIT"])

    # Static AUDIO_MAP serving tables + the model's own bounds gate (defect B,
    # 2026-07-28). Emitted for EVERY shape, static or dynamic, because the
    # static GET_AUDIO_MAP path exists in every build - the tables are what let
    # it answer from the ADDRESSED PORT'S OWN base_map instead of a hardcoded
    # descriptor index (defect A).
    smap = static_map_tables(spec, base_of, len(si), len(so))

    # Two-level directory (accessor area lever): derive the level-1 table,
    # prove it answers exactly like the linear scan, and split the NAMED
    # table into structural-rule + exceptions. All three raise on a model
    # whose layout the direct-indexed RTL could mis-serve.
    l1 = two_level_directory(directory)
    check_two_level(l1, directory)
    name_mask, name_exc = named_structure(l1, directory, named)

    #  the CLOCK_SOURCE shape travels with the model, because the RTL needs
    #  two facts about it that no other field carries: how many sources the
    #  configuration declares, and which one is the CRF
    _n_cs, _crf_ix = clock_source_shape(spec["clock_sources"])
    return dict(rom=rom, directory=directory, ROM_SIZE=len(rom),
                OVERLAYS=overlays, WB=wb, NAMED=named,
                N_CLKSRC=_n_cs,
                CRF_CLKSRC=_crf_ix,
                L1=l1, NAME_MASK=name_mask, NAME_EXC=name_exc,
                RATES=spec["rates"], FORMATS=fmts, CRF_FMTS=crf_fmts,
                PER_STREAM=per_stream, DYNMAP=dynmap, ODMAP=odmap, SMAP=smap)


#: Render-crossbar DEPTH: how many physical output channels
#: KL_chan_map_render holds a map word for, i.e. milan_datapath's
#: CHMAP_PHYS_C (2 I2S + 8 TDM). sw/builder/test_builder.py gate 17c asserts
#: this equals that localparam, so the AEM refusal and the fabric write gate
#: can never disagree about which keys exist.
#:
#: NOT the same number as audio_interface.physical_channels.render, which is
#: how many of those channels reach a PIN on a given board (arty_4x4 says 2,
#: ax7101_8x8 says 0). A key inside the crossbar but past the routed width
#: still maps onto a parked wire - that is the separate, pre-existing
#: physical source-coverage gap, graded by scripts/check_wire_accountability.py
#: and deliberately NOT silently closed here.
CHMAP_PHYS_DEPTH = 10

SRC_IDS = {name: n for n, name in enumerate(
    ["ENTITY_ID", "MODEL_ID", "ECAPS", "TALKER_SRC", "TALKER_CAP",
     "LISTEN_SINK", "LISTEN_CAP", "CTRL_CAP", "AVAIL_IDX", "ASSOC_ID",
     "CURRENT_CFG", "MAC", "CLOCK_ID", "ENT_NAME8"])}

# Module-level model = the builtin shape (import-compatible aliases: the
# builder test gate and the doc generator read these).
_M = build_model(builtin_spec())
rom = _M["rom"]
directory = _M["directory"]
ROM_SIZE = _M["ROM_SIZE"]
OVERLAYS = _M["OVERLAYS"]
WB = _M["WB"]
NAMED = _M["NAMED"]

def base_of(t: int, i: int = 0) -> int:
    """ROM offset of one `(type, index)` descriptor in the BUILTIN model.

    Resolves against the module-level `directory` above - build_model()'s own
    resolver closes over the model it is assembling, so it cannot answer for
    an importer that only has the builtin shape.
    """
    return next(b for (tt, ii, b, _) in directory if tt == t and ii == i)
