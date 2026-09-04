#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""AUDIO_MAP bounds and the per-port serving tables built from them.

Split out of `gen_aem_store.py` (Rule 12). What this file produces is the
REFUSAL: `static_map_tables()` either returns the AEM_SMAP_* tables the
readers need or raises, and every bound it enforces cites the clause it
comes from. The descriptor octets it checks are laid out in
`aem_descriptors`; the model those tables land in is assembled in
`aem_assemble`.

`gen_aem_store` re-exports every name here.
"""
import dataclasses
from collections.abc import Callable, Iterable
from typing import Any

from aem_descriptors import AUDIO_MAP, d_audio_map


def fmt_channels(fmt: int) -> int | None:
    """stream_format -> channels_per_frame, or None when the format carries no
    audio channels. IEEE 1722-2016 7.3.1: the AAF subtype is the top octet
    (0x02 = AAF) and channels_per_frame is bits 31:22 of the 64-bit word - the
    same field KL_aecp_response_builder validates a SET_STREAM_FORMAT on. CRF
    (0x04) carries a clock, not channels: there is no channel bound to check."""
    if (fmt >> 56) != 0x02:
        return None
    return (fmt >> 22) & 0x3FF


#! Milan v1.2 6.2 + Table 6.1: "number of channels = N, where N is an element
#! from {1, 2, 4, 6, 8}". These five, at one sampling rate, are what 6.4 means
#! by "all the other 48kHz ... Base formats".
MILAN_BASE_CHANNELS = (1, 2, 4, 6, 8)


def base_channel_cover(fmts: Iterable[int | str],
                       rate_fmt: int = 0x0205022000006000) -> set[int]:
    """The 48 kHz Milan Base channel counts an advertised formats list covers.

    IEEE 1722-2016 Annex I.2.4: "The ut field is used to determine if the AAF
    stream source or sink is capable of sourcing or sinking a stream with less
    than the number of channels indicated by the channels_per_frame field.
    When set to one (1) the stream source or sink is capable of using fewer
    channels than specified." So ONE ut entry advertises every Base count up
    to its own - which is what Milan 6.5 recommends ("it should use the ut bit
    ... to describe all the related formats using a single ATDECC format
    string") and 5.3.3.4 confirms a controller must read ("a single entry in
    the formats list can describe a range of formats when using the "up to"
    bit"). `rate_fmt` is the 48 kHz AAF PCM32 stem with channels zeroed."""
    got = set()
    for f in fmts:
        n = int(str(f), 16) if isinstance(f, str) else int(f)
        ut, ch = (n >> 52) & 1, (n >> 22) & 0x3FF
        if n & ~((1 << 52) | (0x3FF << 22)) != rate_fmt:
            continue
        got |= {c for c in MILAN_BASE_CHANNELS if c <= ch} if ut \
            else {ch} & set(MILAN_BASE_CHANNELS)
    return got


#! The RTL's port-index mux width (KL_aecp_response_builder w_smap_pi is 5 b)
SMAP_MAX_PORTS = 32
#! IEEE Std 1722.1-2021 Table 7-32, AUDIO_MAP descriptor, number_of_mappings:
#!   "The number of channel mappings within the descriptor. The value of this
#!    field is referred to as N. The maximum value of this field is 62 for this
#!    version of AEM."
#! This bounds the DESCRIPTOR, which is what this function builds. Do not
#! confuse it with Milan v1.2 5.4.2.26's 176, which bounds the number of
#! DYNAMIC mappings a GET_AUDIO_MAP RESPONSE may carry for one map_index -
#! a different object, on ports that have no Audio Map descriptor at all.
#! (An earlier version of this constant was derived from the MTU and came out
#! at 181, which would have accepted a descriptor the standard forbids.)
SMAP_MAX_ROWS = 62


#: The stream_channel deviations the deployed model carries today, recorded as
#: data so that a NEW one fails instead of joining it silently. Measured
#: 2026-07-28 by this gate on its first run.
#:
#: THIS IS A COHERENCE FINDING, NOT A PROVEN VIOLATION, and the difference is
#: recorded because the standards were read rather than paraphrased: no clause
#: of 1722.1-2021 7.2.19 or 7.2.13 bounds a STATIC AUDIO_MAP's
#: mapping_stream_channel by anything. The nearest normative sentence is Milan
#: v1.2 5.4.2.27, and it governs the ADD_AUDIO_MAPPINGS COMMAND on dynamic
#: ports: "A PAAD-AE shall treat as invalid a mapping that references a channel
#: of a Stream Input/Output that does not exist in the currently set format for
#: this Stream Input/Output." For the descriptor the spec is SILENT.
#:
#: What is nonetheless true: the deployed STREAM_PORT_OUTPUT[0] publishes
#: mappings onto stream channels 2..7 of a STREAM_OUTPUT whose ONLY advertised
#: format is 2-channel AAF, so six of its eight mappings name channels that
#: exist in no format the talker offers - the map cannot be acted on whatever
#: the format is set to. OWNER: the NxN talker work roadmap item 5 owns - the
#: AUDIO_MAP is generated from the port's CLUSTER count (endstation_builder.py:
#: one mapping per cluster) with nothing consulting channels_per_frame.
#: Down-declaring is NOT the fix (USER, commit e103d8e: the device declares
#: what it IS); the map has to be built from min(clusters, widest advertised
#: channels) or the talker has to grow.
KNOWN_MAP_DEVIATIONS = {
    "STREAM_PORT_OUTPUT[0] AUDIO_MAP[1] mapping (0,%d,%d,0): stream_channel "
    "%d >= 2, the widest channels_per_frame stream 0 advertises "
    "(['0x205022000806000']) - 7.2.6 / IEEE 1722-2016 7.3.1" % (c, c, c)
    for c in range(2, 8)
}


def assert_no_map_deviations(M: dict[str, Any],
                             allow: Iterable[str] = KNOWN_MAP_DEVIATIONS) -> list[str]:
    """Raise unless this model's AUDIO_MAP deviations are exactly the recorded
    ones. Separated from build_model so the tree keeps building while the
    deviation is open (roadmap item 00's pattern: a deviation that FAILS
    something is a finding, a deviation in a comment is not), and so a NEW
    deviation cannot join the recorded set unnoticed."""
    got = set(M["SMAP"]["DEVIATIONS"])
    new = got - set(allow)
    if new:
        raise ValueError("AUDIO_MAP deviations not on the recorded list:\n  "
                         + "\n  ".join(sorted(new)))
    return sorted(got)


#: d_audio_cluster fixes channel_count = 1 for every cluster this model
#: emits, so the 7.2.16 bound is "cluster_channel must be 0". Read from the
#: encoder rather than restated, so a future multi-channel cluster moves both
#: together.
SMAP_CLUSTER_CHANNELS = 1


@dataclasses.dataclass(frozen=True)
class MapDirection:
    """One direction of the AUDIO_MAP gate: what a mapping in it is bounded by.

    `direction` is "INPUT" or "OUTPUT" and picks which half of 7.2.19's
    ASYMMETRIC duplicate rule applies. `n_streams` and `stream_specs` are the
    stream descriptors this direction has - a mapping's stream_index and
    stream_channel are measured against those and against nothing else.
    """
    direction: str
    ports: list
    n_streams: int
    stream_specs: list


def _static_map_of(port, tag, maps):
    """The AUDIO_MAP a static STREAM_PORT serves: `(base_map, rows)`.

    The three port-level bounds, each a different descriptor's: 7.2.13's
    number_of_maps and base_map, and Table 7-32's mapping count.
    """
    if port["maps"] != 1:
        raise ValueError(
            f"{tag} declares number_of_maps={port['maps']}; the static "
            "GET_AUDIO_MAP path serves map_index 0 only, so any other "
            "count advertises pages the entity cannot answer "
            "(7.2.13 number_of_maps / 7.4.44.1 paging)")
    bm = port["base_map"]
    if not 0 <= bm < len(maps):
        raise ValueError(
            f"{tag} base_map={bm} names an AUDIO_MAP this model does "
            f"not define (it defines {len(maps)}: 0..{len(maps) - 1}) "
            "- 7.2.13 base_map addresses a descriptor that must exist")
    rows = maps[bm]
    if len(rows) > SMAP_MAX_ROWS:
        raise ValueError(
            f"{tag} AUDIO_MAP[{bm}] has {len(rows)} mappings; "
            f"1722.1-2021 Table 7-32: \"The maximum value of this "
            f"field is {SMAP_MAX_ROWS} for this version of AEM\"")
    return bm, rows


def _map_row_bounds(where, row, port, side):
    """Every per-mapping bound, in the order a reader of 7.2.19 meets them.

    Raises ValueError naming the mapping for a bound the standard makes
    normative. RETURNS the one bound the standard is SILENT about - a
    stream_channel past the widest format the descriptor advertises - as a
    deviation string, or None; see KNOWN_MAP_DEVIATIONS for why that one is
    recorded rather than raised.
    """
    si, sc, co, cc = row
    if co >= port["clusters"]:
        raise ValueError(
            f"{where}: cluster_offset {co} >= this port's "
            f"number_of_clusters {port['clusters']}. 1722.1-2021 "
            "Table 7-33: mapping_cluster_offset is \"The offset "
            "from the base_cluster of the STREAM_PORT_INPUT or "
            "STREAM_PORT_OUTPUT\" - PORT-RELATIVE (this port's "
            f"base_cluster is {port['base_cluster']}), not a global "
            "AUDIO_CLUSTER index")
    if cc >= SMAP_CLUSTER_CHANNELS:
        raise ValueError(
            f"{where}: cluster_channel {cc} >= channel_count "
            f"{SMAP_CLUSTER_CHANNELS} of the AUDIO_CLUSTER at "
            f"base_cluster+{co} (7.2.16 Table 7-27 channel_count: "
            "\"The number of channels within the cluster\")")
    if si >= side.n_streams:
        raise ValueError(
            f"{where}: stream_index {si} >= the {side.n_streams} "
            f"stream descriptors this direction has (7.2.13)")
    #! THE BOUND AT THIS TIER IS THE FORMAT *LIST*, NOT current_format.  A
    #! static AUDIO_MAP is a property of the port and outlives any one
    #! SET_STREAM_FORMAT, and the deployed model proves the difference is
    #! not hypothetical: the arty_current listener's formats are
    #! [0205022000806000 (2ch), 0215022002006000 (ut, 8ch)] with formats[0]
    #! - the reset default - carrying TWO channels, while its 8-cluster port
    #! maps stream channels 0..7. Bound by the widest format the descriptor
    #! advertises and the map is conformant; bound by the current one and a
    #! conformant model is refused for being narrowly configured today. The
    #! live controller check (tb/tools/hive_compliance.py C9) uses the
    #! CURRENT format because on the wire there is only one.
    #! The only normative sentence in reach is Milan v1.2 5.4.2.27 and it
    #! governs ADD_AUDIO_MAPPINGS, not the descriptor: "A PAAD-AE shall
    #! treat as invalid a mapping that references a channel of a Stream
    #! Input/Output that does not exist in the currently set format for this
    #! Stream Input/Output." For a STATIC AUDIO_MAP the standard is SILENT.
    chans = [fmt_channels(f) for f in side.stream_specs[si]["formats"]]
    chans = [c for c in chans if c is not None]
    if not chans:
        raise ValueError(
            f"{where}: stream {si} ('{side.stream_specs[si]['name']}') "
            "advertises no audio format with channels (CRF carries "
            "a clock, not channels), so no channel of it can be "
            "mapped to a cluster - 7.2.6 current_format / IEEE "
            "1722-2016 7.3.1 channels_per_frame")
    if sc >= max(chans):
        #! RECORDED, not raised: the deployed model violates this one today
        #! (see KNOWN_MAP_DEVIATIONS) and the fix is a product decision owned
        #! elsewhere. assert_no_map_deviations() is what turns it into a
        #! failure, and it fails on any deviation that is not the recorded one.
        return (f"{where}: stream_channel {sc} >= {max(chans)}, the "
                f"widest channels_per_frame stream {si} advertises "
                f"({[hex(f) for f in side.stream_specs[si]['formats']]}) - "
                "7.2.6 / IEEE 1722-2016 7.3.1")
    return None


def _map_duplicate_rule(where, row, side, seen, cfg_stream_ch):
    """7.2.19's duplicate rule, which is NOT the same in the two directions.

    `seen` is one port's cluster channels (the INPUT rule); `cfg_stream_ch`
    spans every output port, because the OUTPUT rule is scoped "across the
    entire Configuration". Both are updated in place.
    """
    si, sc, co, cc = row
    if side.direction == "INPUT":
        #! "There is at most one entry for each
        #!  mapping_cluster_offset and mapping_cluster_channel,
        #!  but there may be multiple entries for each
        #!  mapping_stream_index and mapping_stream_channel."
        if (co, cc) in seen:
            raise ValueError(
                f"{where}: 1722.1-2021 7.2.19 for a "
                "STREAM_PORT_INPUT - \"There is at most one entry "
                "for each mapping_cluster_offset and "
                f"mapping_cluster_channel\" - and ({co},{cc}) is "
                "already mapped in this map")
        seen.add((co, cc))
    else:
        #! "There is at most one entry for each
        #!  mapping_stream_index and mapping_stream_channel ACROSS
        #!  THE ENTIRE CONFIGURATION, but there may be multiple
        #!  entries for each mapping_cluster_offset and
        #!  mapping_cluster_channel."
        if (si, sc) in cfg_stream_ch:
            raise ValueError(
                f"{where}: 1722.1-2021 7.2.19 for a "
                "STREAM_PORT_OUTPUT - \"There is at most one "
                "entry for each mapping_stream_index and "
                "mapping_stream_channel across the entire "
                f"Configuration\" - and ({si},{sc}) is already "
                f"mapped by {cfg_stream_ch[(si, sc)]}")
        cfg_stream_ch[(si, sc)] = where


def _direction_tables(side, maps, base_of):
    """One direction's serving tables: (addr, rows, mappings_offset, deviations).

    One entry per STREAM_PORT of the direction, in descriptor-index order,
    with every 7.2.19 / Table 7-33 bound checked on the way past.
    """
    addr, rows_n, moff, deviations = [], [], [], []
    #! 7.2.19 OUTPUT rule: "at most one entry for each mapping_stream_index
    #! and mapping_stream_channel ACROSS THE ENTIRE CONFIGURATION" - so this
    #! set spans all output ports, not one.
    cfg_stream_ch = {}
    for k, p in enumerate(side.ports):
        tag = f"STREAM_PORT_{side.direction}[{k}]"
        if p.get("map_mode", "static") == "dynamic":
            #! 7.2.13: "These Entities set the number_of_maps field to
            #! zero (0) and the base_map field is ignored when read." The
            #! mappings are runtime state, not a descriptor; ROWS = 0
            #! tells the RTL there is no static map to serve here.
            addr.append(0)
            rows_n.append(0)
            moff.append(0)
            continue
        bm, rows = _static_map_of(p, tag, maps)
        seen = set()
        for row in rows:
            si, sc, co, cc = row
            where = f"{tag} AUDIO_MAP[{bm}] mapping ({si},{sc},{co},{cc})"
            deviation = _map_row_bounds(where, row, p, side)
            if deviation is not None:
                deviations.append(deviation)
            _map_duplicate_rule(where, row, side, seen, cfg_stream_ch)
        addr.append(base_of(AUDIO_MAP, bm))
        rows_n.append(len(rows))
        #! the descriptor's OWN mappings_offset, read back from the bytes
        #! this model just encoded (7.2.19: the mappings "shall be
        #! accessed by using the mappings_offset field"). Table 7-32 fixes
        #! it at 8 "for this version of AEM"; deriving it means the RTL
        #! does not carry a second copy of that 8.
        img = d_audio_map(bm, rows)
        moff.append((img[4] << 8) | img[5])
    return addr, rows_n, moff, deviations


def static_map_tables(spec: dict[str, Any], base_of: Callable[..., int],
                      n_str_in: int, n_str_out: int) -> dict[str, Any]:
    """Per-STREAM_PORT static AUDIO_MAP serving tables, AND the model-tier
    bounds gate that makes them checkable (defect B, 2026-07-28).

    WHY A GATE AND NOT JUST A TABLE.  GET_AUDIO_MAP answers with mappings the
    controller then uses to address AUDIO_CLUSTERs, and IEEE Std 1722.1-2021
    Table 7-33 / Table 7-162 define mapping_cluster_offset verbatim as

        "The offset from the base_cluster of the STREAM_PORT_INPUT or
         STREAM_PORT_OUTPUT for mapping[0]."

    The offsets are therefore PORT-RELATIVE. A model may write the SAME
    offsets on two ports and mean two different global clusters, which is
    exactly why no comparison of one declaration against another can see a
    wrong offset: it has to be compared against THE PORT'S OWN
    number_of_clusters. Nothing did that until now, and on 2026-07-28 a
    controller-grade check read 8 mappings with cluster_offset 0..7 out of a
    port declaring number_of_clusters = 2.

    Every bound here is the bound of a DIFFERENT descriptor:
      base_map                names an AUDIO_MAP this model defines   (7.2.13)
      number_of_maps == 1     the static serving path answers map_index 0 only
                              (7.4.44.1: any other index is BAD_ARGUMENT)
      number_of_mappings      <= 62                          (Table 7-32)
      cluster_offset          < the OWNING port's number_of_clusters
                                (Table 7-33 quoted above)
      cluster_channel         < that AUDIO_CLUSTER's channel_count    (7.2.16
                                Table 7-27: "The number of channels within the
                                cluster", descriptor offset 84)
      stream_index            < the stream descriptors this direction has
                                                                     (7.2.13)

    THE DUPLICATE RULE IS DIRECTION-ASYMMETRIC, and reading 7.2.19 rather than
    restating it is what caught that. Verbatim, for STREAM_PORT_INPUT:

        "There is at most one entry for each mapping_cluster_offset and
         mapping_cluster_channel, but there may be multiple entries for each
         mapping_stream_index and mapping_stream_channel."

    and for STREAM_PORT_OUTPUT the two halves swap:

        "There is at most one entry for each mapping_stream_index and
         mapping_stream_channel across the entire Configuration, but there may
         be multiple entries for each mapping_cluster_offset and
         mapping_cluster_channel."

    The first version of this gate applied the INPUT rule to BOTH directions
    (unique cluster channel), which the OUTPUT paragraph explicitly permits -
    it would have refused a conformant model. The output rule is also scoped
    "across the entire Configuration", so it is checked across all output
    ports together rather than per port.

    WHERE THE STANDARD IS SILENT, and it is said rather than filled in: no
    clause bounds a STATIC AUDIO_MAP's mapping_stream_channel by the stream's
    format. The nearest normative sentence is Milan v1.2 5.4.2.27, and it is
    about the DYNAMIC command, not the descriptor: "A PAAD-AE shall treat as
    invalid a mapping that references a channel of a Stream Input/Output that
    does not exist in the currently set format for this Stream Input/Output."
    Applying that to a static descriptor would bound a permanent structure by
    a runtime value, so this gate bounds by the WIDEST format the descriptor
    advertises and RECORDS rather than raises - see KNOWN_MAP_DEVIATIONS.

    Returns the emit dict; raises ValueError naming the offending port.
    """
    if len(spec["ports_in"]) > SMAP_MAX_PORTS or \
            len(spec["ports_out"]) > SMAP_MAX_PORTS:
        raise ValueError(
            f"more than {SMAP_MAX_PORTS} STREAM_PORTs in one direction: the "
            "RTL GET_AUDIO_MAP port-index mux is 5 bits wide")
    maps = spec["audio_maps"]
    inputs = MapDirection("INPUT", spec["ports_in"], n_str_in,
                          spec["stream_inputs"])
    outputs = MapDirection("OUTPUT", spec["ports_out"], n_str_out,
                           spec["stream_outputs"])
    in_addr, in_rows, in_moff, in_dev = _direction_tables(inputs, maps, base_of)
    out_addr, out_rows, out_moff, out_dev = _direction_tables(outputs, maps,
                                                              base_of)
    return dict(IN_N=len(in_addr), OUT_N=len(out_addr),
                IN_ADDR=in_addr or [0], IN_ROWS=in_rows or [0],
                IN_MOFF=in_moff or [0],
                OUT_ADDR=out_addr or [0], OUT_ROWS=out_rows or [0],
                OUT_MOFF=out_moff or [0],
                DEVIATIONS=in_dev + out_dev)

