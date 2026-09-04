#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""hive_compliance_oracle.py - the Hive-grade rules that need no network.

C9's bounds rule and C10's over-read rule, as pure functions, plus the
self-test that fires them at crafted vectors. They live apart from
`hive_compliance.py` for the reason `--self-test` exists at all (methodology
R2): the live subject may legitimately return zero mappings and pass
vacuously, so the rules have to be provable offline, and a rule that can be
imported without a socket is a rule a reader can run.

Nothing here touches the wire; the only thing it borrows from
`hive_compliance_wire` is `AM_HDR`, which is a clause-fixed payload offset
(7.4.44.2) rather than a second statement of the rule.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from hive_compliance_wire import AM_HDR                       # noqa: E402


def audio_map_overreads(mappings: list[tuple[int, int, int, int]],
                        n_mappings: int, payload_len: int,
                        desc_rows: list[tuple[int, int, int, int]] | None,
                        desc_len: int | None,
                        desc_declared: int | None = None) -> list[str]:
    """C10's whole rule, as a pure function so it can be self-tested offline.

    GET_AUDIO_MAP does not just have to be IN RANGE, it has to be THIS PORT'S
    MAP.  Bounds alone cannot see a map served out of the wrong descriptor
    whenever the neighbouring descriptor happens to hold in-range numbers, and
    on 2026-07-28 the entity served STREAM_PORT_OUTPUT[0] from AUDIO_MAP[1] -
    STREAM_PORT_INPUT[1]'s map - with a hardcoded 8 mappings and a hardcoded
    64-byte region out of a descriptor holding 16, putting 48 octets of
    whatever followed it in the descriptor ROM on the wire.

    mappings    : the 8-byte rows parsed out of the GET_AUDIO_MAP response
    n_mappings  : number_of_mappings the response DECLARED
    payload_len : octets of AEM payload the response actually carried
    desc_rows   : the same rows read out of the port's own AUDIO_MAP
                  descriptor via READ_DESCRIPTOR (base_map), or None when the
                  port declares number_of_maps = 0 and has no descriptor -
                  then only the self-consistency half is checked
    desc_len    : octets of that descriptor, or None with desc_rows None
    desc_declared: the descriptor's OWN number_of_mappings, which may exceed
                  the rows that fit in it - that gap IS defect B; defaults to
                  len(desc_rows)

    -> list of human-readable violations (empty = conformant)
    """
    out = []
    # (a) the response must CARRY what it declares. 1722.1-2021 7.4.44.2,
    #     verbatim: "The number_of_mappings field is set to the number of
    #     mappings contained in the mappings field." So the payload is
    #     12 + 8*number_of_mappings and anything shorter is a count a
    #     controller will read past the end of.
    if payload_len < AM_HDR + 8 * n_mappings:
        out.append(f"declares {n_mappings} mappings but the payload is "
                   f"{payload_len} B, short of {AM_HDR + 8 * n_mappings}")
    if len(mappings) < n_mappings:
        out.append(f"declares {n_mappings} mappings, {len(mappings)} parsed")
    if desc_rows is None:
        return out
    if desc_declared is None:
        desc_declared = len(desc_rows)
    # (b) the descriptor must HOLD what IT declares (the same rule one tier
    #     down: a controller that trusts an AUDIO_MAP's own count and reads
    #     8 rows out of a 24-byte descriptor reads 6 rows of neighbours)
    if desc_len is not None and desc_len < 8 + 8 * desc_declared:
        out.append(f"AUDIO_MAP descriptor declares {desc_declared} mappings "
                   f"but is {desc_len} B, short of {8 + 8 * desc_declared}")
    # (c) and the served rows must BE the port's own rows. Compared as a
    #     multiset, not in order: 7.4.44 does not fix an ordering, so
    #     requiring one would be inventing a rule (methodology R3). What it
    #     DOES catch is a row that is not in this port's map at all.
    have = list(desc_rows)
    for m in mappings:
        if m in have:
            have.remove(m)
        else:
            out.append(f"served mapping {m} is not in this port's own "
                       f"AUDIO_MAP (7.2.19: the map belongs to the port)")
    if n_mappings != desc_declared:
        out.append(f"serves {n_mappings} mappings where the port's own "
                   f"AUDIO_MAP descriptor declares {desc_declared}")
    return out


def audio_map_violations(mappings: list[tuple[int, int, int, int]],
                         n_streams: int, stream_channels: dict[int, int],
                         number_of_clusters: int,
                         cluster_channels: dict[int, int]) -> list[str]:
    """C9's whole rule, as a pure function so it can be self-tested offline.

    mappings          : [(stream_index, stream_channel, cluster_offset,
                          cluster_channel)]
    n_streams         : how many stream descriptors THIS direction answers
    stream_channels   : {stream_index: channel count of its current format},
                        missing = unknown (that one bound is not asserted)
    number_of_clusters: the answering STREAM_PORT's number_of_clusters
    cluster_channels  : {cluster_offset: channel_count of the AUDIO_CLUSTER at
                        base_cluster + offset}, missing = unknown

    -> list of human-readable violations (empty = conformant)
    """
    out = []
    for si, sc, co, cc in mappings:
        if si >= n_streams:
            out.append(f"stream_index {si} >= {n_streams} streams")
        elif si in stream_channels and sc >= stream_channels[si]:
            out.append(f"stream_channel {sc} >= stream {si} format channels "
                       f"{stream_channels[si]}")
        if co >= number_of_clusters:
            out.append(f"cluster_offset {co} >= number_of_clusters "
                       f"{number_of_clusters} (port-RELATIVE, 7.2.19)")
        elif co in cluster_channels and cc >= cluster_channels[co]:
            out.append(f"cluster_channel {cc} >= cluster {co} channel_count "
                       f"{cluster_channels[co]}")
    return out


def aaf_channels(fmt: int) -> int | None:
    """current_format -> channels_per_frame, or None when the format is not an
    audio format that has one. IEEE 1722-2016 7.3.1: the AAF stream_format
    subtype is the top octet (0x02 = AAF), channels_per_frame is bits 31:22 of
    the 64-bit word - the same field KL_aecp_response_builder validates on.
    CRF (0x04) carries a clock, not channels: no bound to assert."""
    if (fmt >> 56) != 0x02:
        return None
    return (fmt >> 22) & 0x3FF


def self_test() -> int:
    """Negative control for C9 (methodology R2). The live subject may return
    zero mappings and pass vacuously; these vectors prove the rule bites."""
    ok = True

    def t(name: str, got: list[str], exp_n: int) -> None:
        """One offline vector: the predicate must find exactly `exp_n` of them."""
        nonlocal ok
        good = (len(got) == exp_n)
        ok = ok and good
        print(f"  [{'ok  ' if good else 'FAIL'}] {name}: {len(got)} "
              f"violation(s), expected {exp_n}" + (f"  {got}" if got else ""))

    sch = {0: 8, 1: 2}
    cch = {0: 1, 1: 1, 8: 1}
    t("conformant 8-channel map",
      audio_map_violations([(0, c, c, 0) for c in range(8)], 2, sch, 8, cch),
      0)
    t("a SECOND port may reuse the SAME port-relative offsets",
      audio_map_violations([(1, 0, 0, 0), (1, 1, 1, 0)], 2, sch, 8, cch), 0)
    t("GLOBAL cluster index where the clause wants a port-relative offset",
      audio_map_violations([(0, 0, 9, 0)], 2, sch, 8, cch), 1)
    t("stream_index past the descriptors that answer",
      audio_map_violations([(9, 0, 0, 0)], 2, sch, 8, cch), 1)
    t("stream_channel past the current format's channel count",
      audio_map_violations([(1, 5, 0, 0)], 2, sch, 8, cch), 1)
    t("cluster_channel past that cluster's channel_count",
      audio_map_violations([(0, 0, 0, 3)], 2, sch, 8, cch), 1)
    t("unknown format -> that ONE bound is not asserted, the others still are",
      audio_map_violations([(0, 999, 99, 0)], 2, {}, 8, cch), 1)

    # ---- C10: the served map is THIS PORT'S map, whole and no more -------
    # The vectors are the measured defect, not invented shapes: the deployed
    # 8x8 output port's own AUDIO_MAP holds 2 rows in 24 bytes, and the RTL
    # served 8 rows / 64 bytes out of the INPUT port's 72-byte map instead.
    own2 = [(0, 0, 0, 0), (0, 1, 1, 0)]                     # its own 2 rows
    other8 = [(1, c, c, 0) for c in range(8)]               # input port 1's
    t("conformant: the port's own 2 rows, declared and carried",
      audio_map_overreads(own2, 2, AM_HDR + 16, own2, 24), 0)
    t("rows in a different ORDER are still the same map (no clause fixes one)",
      audio_map_overreads(own2[::-1], 2, AM_HDR + 16, own2, 24), 0)
    t("DEFECT A: 8 rows from ANOTHER port's map on a 2-row port",
      #  8 not-mine + count 8 != 2
      audio_map_overreads(other8, 8, AM_HDR + 64, own2, 24), 9)
    t("declares more mappings than the payload carries (the read-past cue)",
      audio_map_overreads(own2, 8, AM_HDR + 16, own2, 24), 3)
    t("DEFECT B: a descriptor that declares more rows than it can hold",
      audio_map_overreads(own2, 2, AM_HDR + 16, own2 + own2 + own2 + own2,
                          24), 2)
    t("no AUDIO_MAP descriptor (7.2.13 number_of_maps=0) -> only the "
      "self-consistency half applies",
      audio_map_overreads(own2, 2, AM_HDR + 16, None, None), 0)
    print("\nC9/C10 self-test:", "PASS" if ok else "FAIL")
    return 0 if ok else 1
