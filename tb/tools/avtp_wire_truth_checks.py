#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""avtp_wire_truth_checks.py - THE INVARIANTS: `WireTruth`, which
accumulates per-stream state over a capture and then renders verdicts.

Every check has a stable name and carries its clause, so a morning's run
diffs against yesterday's.  The decoders it reads through are in
`avtp_wire_truth_wire.py`; the byte vectors that prove each check can FAIL are
in `avtp_wire_truth_selftest.py`."""
from __future__ import annotations

import struct
from typing import Iterable, Optional

from avtp_wire_truth_wire import (AAF_FORMAT_NAMES, ADP_CDL, ADP_FRAME_LEN,
                                  AVTP_TS_MOD, CONTROL_SUBTYPES, ETH_P_AVTP,
                                  ETH_P_MSRP, ETH_P_MVRP, Expectation,
                                  MILAN_CRF_FORMAT, MSRP_DOMAIN, MSRP_LISTENER,
                                  MSRP_TALKER_ADVERTISE, MSRP_TALKER_FAILED,
                                  NSR_HZ, SUBTYPE_AAF, SUBTYPE_ADP,
                                  SUBTYPE_CRF, SUBTYPE_NAMES, Verdict,
                                  _mod_delta, _nothing_to_check, _v,
                                  decode_aaf, decode_control, decode_crf,
                                  decode_eth, decode_mrpdu,
                                  parse_aaf_stream_format,
                                  parse_crf_stream_format)


class WireTruth:
    """Accumulates per-stream state over a capture, then renders verdicts.

    Every check has a stable name and carries its clause.  Adding one is a
    method plus one line in `checks()`; that is the extension contract, and it
    is the same contract torture_campaign.py uses (see
    docs/testing/RUNNING_TESTS.md).
    """

    def __init__(self, expect: Optional[Expectation] = None):
        self.expect = expect or Expectation()
        self.frames = 0
        self.non_avtp = 0
        self.aaf: dict[int, list] = {}
        self.crf: dict[int, list] = {}
        self.adp: dict[int, list] = {}
        self.control: list = []
        self.untagged_stream_frames = 0
        self.short_frames = 0
        #: MSRP / MVRP attributes, one record per VALUE.  These frames go to
        #: 01:80:C2:00:00:0E, which a bridge does NOT forward, so an INLINE TAP
        #: is the only place they can be seen - and therefore the only place the
        #: Listener Ready half of the Milan v1.2 5.3.7.3 licence is visible.
        self.mrp: list = []
        self.msrp_frames = 0
        self.mvrp_frames = 0

    # -- ingest ------------------------------------------------------------
    def feed(self, ts: float, raw: bytes) -> None:
        """Ingest one captured frame, filing it under the family its EtherType
        and subtype name.  A frame that will not decode and a non-AVTP one are
        each COUNTED, which is how the capture-shape check tells an empty
        capture from one read at the wrong tap offset."""
        self.frames += 1
        eth = decode_eth(raw)
        if eth is None:
            self.short_frames += 1
            return
        if eth.ethertype in (ETH_P_MSRP, ETH_P_MVRP):
            proto = "MSRP" if eth.ethertype == ETH_P_MSRP else "MVRP"
            if proto == "MSRP":
                self.msrp_frames += 1
            else:
                self.mvrp_frames += 1
            for at in decode_mrpdu(eth.payload, proto):
                self.mrp.append((ts, eth, at))
            return
        if eth.ethertype != ETH_P_AVTP:
            self.non_avtp += 1
            return
        st = eth.subtype
        if st == SUBTYPE_AAF:
            pdu = decode_aaf(eth.payload)
            if pdu:
                self.aaf.setdefault(pdu.stream_id, []).append((ts, eth, pdu))
                if not eth.tagged:
                    self.untagged_stream_frames += 1
        elif st == SUBTYPE_CRF:
            pdu = decode_crf(eth.payload)
            if pdu:
                self.crf.setdefault(pdu.stream_id, []).append((ts, eth, pdu))
                if not eth.tagged:
                    self.untagged_stream_frames += 1
        elif st in CONTROL_SUBTYPES:
            c = decode_control(eth.payload)
            if c:
                self.control.append((ts, eth, c))
                if st == SUBTYPE_ADP:
                    ai = (struct.unpack(">I", eth.payload[36:40])[0]
                          if len(eth.payload) >= 40 else None)
                    self.adp.setdefault(c.target_entity_id, []).append(
                        (ts, eth.wire_len, c, ai))

    def feed_capture(self, records: Iterable[tuple[float, bytes]]) -> "WireTruth":
        """Ingest a whole capture, returning self so a read can chain into
        `.checks()` without naming the accumulator."""
        for ts, raw in records:
            self.feed(ts, raw)
        return self

    # -- checks ------------------------------------------------------------
    def checks(self) -> list[Verdict]:
        """Every verdict this capture supports, one family at a time.

        The families are called unconditionally on purpose: one that found
        nothing to run on returns a SKIP naming what was absent, so the log
        can never lose the difference between "did not apply" and "was not
        run" (see _nothing_to_check)."""
        out: list[Verdict] = []
        out += self.check_capture_shape()
        out += self.check_aaf_declared_vs_wire()
        out += self.check_aaf_header_legality()
        out += self.check_aaf_payload_arithmetic()
        out += self.check_sequence_continuity()
        out += self.check_aaf_timestamps()
        out += self.check_vlan_class()
        out += self.check_zero_fill()
        out += self.check_crf_format()
        out += self.check_crf_rate()
        out += self.check_adp_frame_rule()
        out += self.check_control_length_honesty()
        out += self.check_srp_declarations()
        return out

    def check_capture_shape(self) -> list[Verdict]:
        """A capture with no stream frames must not read as a clean pass - the
        commonest false green in this project is an empty capture (a mirror
        port that never subscribed to the multicast group)."""
        n = sum(len(v) for v in self.aaf.values()) + \
            sum(len(v) for v in self.crf.values())
        return [Verdict("wt.capture.stream-frames-present",
                        "PASS" if n else "FAIL",
                        "docs/findings/BENCH_TOPOLOGY.md - a mirror port sees "
                        "control frames only; stream truth needs an inline tap",
                        {"frames": self.frames, "stream_frames": n,
                         "aaf_streams": len(self.aaf),
                         "crf_streams": len(self.crf),
                         "non_avtp": self.non_avtp,
                         "undecodable": self.short_frames})]

    def check_aaf_declared_vs_wire(self) -> list[Verdict]:
        """The escape that started this module: what the controller was told
        against what the first frame of each stream carries.

        I.2.4.1 says each qword field "matches the setting of the ... field in
        the Stream AVTPDU when this stream format is the current format", which
        is what makes a difference a DEFECT and not two opinions.  With no
        declared format supplied the check SKIPs rather than inventing one."""
        want = self.expect.aaf_format
        if want is None:
            return [Verdict("wt.aaf.declared-vs-wire", "SKIP",
                            "IEEE 1722-2016 I.2.4.1",
                            {"why": "no declared stream_format supplied - pass "
                                    "the GET_STREAM_FORMAT readback with "
                                    "--expect-aaf-format"})]
        d = parse_aaf_stream_format(want)
        if d is None:
            return [Verdict("wt.aaf.declared-vs-wire", "FAIL",
                            "IEEE 1722-2016 I.2.4",
                            {"why": "declared format is not an AAF format",
                             "declared": f"{int(want):016x}"})]
        out = []
        for sid, recs in sorted(self.aaf.items()):
            _, _, p = recs[0]
            bad = {}
            if p.channels_per_frame != d.channels_per_frame:
                bad["channels_per_frame"] = [d.channels_per_frame,
                                             p.channels_per_frame]
            if p.nsr != d.nsr:
                bad["nsr"] = [d.nsr, p.nsr]
            if p.fmt != d.fmt:
                bad["format"] = [d.fmt, p.fmt]
            if p.bit_depth != d.bit_depth:
                bad["bit_depth"] = [d.bit_depth, p.bit_depth]
            spf = p.sample_frames
            if spf is not None and d.samples_per_frame and \
                    spf != d.samples_per_frame:
                bad["samples_per_frame"] = [d.samples_per_frame, spf]
            out.append(_v(f"wt.aaf.declared-vs-wire.{sid:016x}", not bad,
                          "IEEE 1722-2016 I.2.4.1: the stream_format field "
                          "'matches the setting of the ... field in the Stream "
                          "AVTPDU when this stream format is the current "
                          "format for the stream'",
                          declared=f"{int(want):016x}", mismatches=bad,
                          measured_on_frames=len(recs)))
        return out or [Verdict("wt.aaf.declared-vs-wire", "SKIP",
                               "IEEE 1722-2016 I.2.4.1",
                               {"why": "no AAF frames in the capture"})]

    def check_aaf_header_legality(self) -> list[Verdict]:
        """The field-legality rules that hold with NO declaration at all."""
        if not self.aaf:
            return [_nothing_to_check(
                "wt.aaf.header-legal",
                "IEEE 1722-2016 7.3.3, 7.3.4, Tables 9 and 11", "AAF frames")]
        out = []
        for sid, recs in sorted(self.aaf.items()):
            bad = []
            for _, _, p in recs:
                if p.channels_per_frame == 0:
                    bad.append("channels_per_frame 0 (7.3.3: > 0)")
                if p.bit_depth == 0:
                    bad.append("bit_depth 0 (7.3.4: not zero)")
                sb = p.sample_bits
                if sb and p.bit_depth > sb:
                    bad.append(f"bit_depth {p.bit_depth} > format width {sb} "
                               "(7.3.4)")
                if p.fmt not in AAF_FORMAT_NAMES:
                    bad.append(f"format {p.fmt:#x} reserved (Table 9)")
                if p.nsr not in NSR_HZ:
                    bad.append(f"nsr {p.nsr:#x} reserved (Table 11)")
                if p.sv != 1:
                    bad.append("sv 0 with a stream_id present (4.4.4.2)")
                if p.version != 0:
                    bad.append(f"version {p.version} (4.4.4.3: 0)")
                if bad:
                    break
            out.append(_v(f"wt.aaf.header-legal.{sid:016x}", not bad,
                          "IEEE 1722-2016 7.3.3, 7.3.4, Tables 9 and 11",
                          violations=sorted(set(bad)), frames=len(recs)))
        return out

    def check_aaf_payload_arithmetic(self) -> list[Verdict]:
        """stream_data_length must describe the payload that is really there,
        and must divide evenly into whole sample events (7.3.5)."""
        if not self.aaf:
            return [_nothing_to_check(
                "wt.aaf.payload-arithmetic",
                "IEEE 1722-2016 4.4.4.10 + 7.3.5", "AAF frames")]
        out = []
        for sid, recs in sorted(self.aaf.items()):
            bad = []
            for _, eth, p in recs:
                if len(p.payload) < p.stream_data_length:
                    bad.append(f"sdl {p.stream_data_length} > payload "
                               f"{len(p.payload)}")
                if p.sample_frames is None:
                    bad.append(f"sdl {p.stream_data_length} is not a whole "
                               f"number of {p.channels_per_frame}-channel "
                               f"sample events at format "
                               f"{p.format_name}")
                if bad:
                    break
            spf = {p.sample_frames for _, _, p in recs}
            out.append(_v(f"wt.aaf.payload-arithmetic.{sid:016x}", not bad,
                          "IEEE 1722-2016 4.4.4.10 stream_data_length + 7.3.5 "
                          "interleaved sample events",
                          violations=bad, sample_frames_seen=sorted(
                              x for x in spf if x is not None)))
        return out

    def check_sequence_continuity(self) -> list[Verdict]:
        """4.4.4.6 for AAF and 10.4.6 for CRF: +1 with wrapping.  A Listener
        may JOIN at any value (10.4.6), so the first frame sets the base and is
        never a gap."""
        out = []
        for kind, table, mod, clause in (
                ("aaf", self.aaf, 256, "IEEE 1722-2016 4.4.4.6"),
                ("crf", self.crf, 256, "IEEE 1722-2016 10.4.6 (ONE octet, "
                                       "FF16 -> 0016)")):
            if not table:
                out.append(_nothing_to_check(f"wt.{kind}.seq-continuity",
                                             clause, f"{kind.upper()} frames"))
                continue
            for sid, recs in sorted(table.items()):
                gaps, prev = [], None
                for i, (ts, _, p) in enumerate(recs):
                    if prev is not None:
                        step = _mod_delta(p.sequence_num, prev, mod)
                        if step != 1:
                            gaps.append({"at_frame": i, "prev": prev,
                                         "got": p.sequence_num, "step": step})
                    prev = p.sequence_num
                out.append(_v(f"wt.{kind}.seq-continuity.{sid:016x}",
                              not gaps, clause,
                              gaps=gaps[:8], gap_count=len(gaps),
                              frames=len(recs)))
        return out

    def check_aaf_timestamps(self) -> list[Verdict]:
        """Three separate properties, kept separate on purpose.

        (a) tv: with sp = 0 every AVTPDU carries a valid presentation time
            (4.4.4.5 / 7.5), so tv = 0 on a normal frame is a finding.
        (b) the presentation-time STEP between consecutive frames equals
            sample_frames / fs - that is a property of the wire alone and needs
            no gPTP reference.
        (c) the presentation OFFSET against gPTP, which needs a reference and
            SKIPS without one rather than guessing.
        """
        if not self.aaf:
            return [_nothing_to_check(n, c, "AAF frames") for n, c in (
                ("wt.aaf.tv-set", "IEEE 1722-2016 4.4.4.5 tv / 7.5"),
                ("wt.aaf.pts-step", "IEEE 1722-2016 7.5 / Milan 5.3.7.6"),
                ("wt.aaf.class-a-transit", "802.1BA-2011 class A 2 ms"))]
        out = []
        for sid, recs in sorted(self.aaf.items()):
            tv_bad = [i for i, (_, _, p) in enumerate(recs)
                      if p.sp == 0 and p.tv == 0]
            out.append(_v(f"wt.aaf.tv-set.{sid:016x}", not tv_bad,
                          "IEEE 1722-2016 4.4.4.5 tv / 7.5 sparse mode",
                          frames_without_tv=len(tv_bad),
                          first_offenders=tv_bad[:8]))

            _, _, p0 = recs[0]
            fs = NSR_HZ.get(p0.nsr)
            spf = p0.sample_frames
            if fs and spf:
                want = round(spf * 1e9 / fs)
                steps, bad = [], []
                for i in range(1, len(recs)):
                    a = recs[i - 1][2].avtp_timestamp
                    b = recs[i][2].avtp_timestamp
                    d = _mod_delta(b, a, AVTP_TS_MOD)
                    steps.append(d)
                    # one media clock tick of slack: the framer times off the
                    # audio clock, so +/- 1 sample period is honest jitter
                    if abs(d - want) > round(1e9 / fs) + 1:
                        bad.append({"at_frame": i, "step_ns": d})
                out.append(_v(f"wt.aaf.pts-step.{sid:016x}",
                              not bad and len(steps) > 0,
                              "IEEE 1722-2016 7.5 / Milan 5.3.7.6: the "
                              "presentation time advances by one AVTPDU of "
                              "media, so the step is sample_frames/fs",
                              expected_step_ns=want, steps=len(steps),
                              violations=bad[:8], violation_count=len(bad)))
            else:
                out.append(Verdict(f"wt.aaf.pts-step.{sid:016x}", "SKIP",
                                   "IEEE 1722-2016 7.5",
                                   {"why": "nsr is 'user specified' or the "
                                           "payload is not a whole number of "
                                           "sample events - no nominal step "
                                           "exists on the wire"}))

            if self.expect.gptp_ref_ns is None:
                out.append(Verdict(f"wt.aaf.class-a-transit.{sid:016x}", "SKIP",
                                   "802.1BA-2011 class A 2 ms",
                                   {"why": "no gPTP reference supplied; a pcap "
                                           "timestamp is the capture host's "
                                           "CLOCK_REALTIME and comparing it to "
                                           "an AVTP timestamp produces a "
                                           "confident number that means "
                                           "nothing (methodology R5)",
                                    "supply": "--gptp-ref-ns"}))
            else:
                t0 = recs[0][0]
                bad = []
                for i, (ts, _, p) in enumerate(recs):
                    now = (self.expect.gptp_ref_ns
                           + round((ts - t0) * 1e9)) % AVTP_TS_MOD
                    ahead = _mod_delta(p.avtp_timestamp, now, AVTP_TS_MOD)
                    # a presentation time in the past decodes as ~2^32 ahead
                    if ahead > self.expect.max_transit_ns:
                        bad.append({"at_frame": i, "ahead_ns": ahead})
                out.append(_v(f"wt.aaf.class-a-transit.{sid:016x}", not bad,
                              "802.1BA-2011 / Milan: class A presentation is "
                              "within 2 ms of transmission",
                              budget_ns=self.expect.max_transit_ns,
                              violations=bad[:8], violation_count=len(bad)))
        return out

    def check_vlan_class(self) -> list[Verdict]:
        """802.1Q 9.5/9.6 + Milan 7.3.3 for CRF: every SR stream frame carries
        a C-TAG with the SR class A PCP, DEI 0, and the SR VID.  VID 0 gets its
        own verdict line because it is not merely wrong, it is the specific
        past defect that made frames flood unshaped."""
        out = []
        for kind, table in (("aaf", self.aaf), ("crf", self.crf)):
            if not table:
                out += [_nothing_to_check(
                    f"wt.{kind}.c-tag-{w}",
                    "802.1Q-2018 9.5/9.6 + Milan v1.2 7.3.3 / 4.2.7.2.1",
                    f"{kind.upper()} frames")
                    for w in ("present", "pcp", "dei", "vid")]
                continue
            for sid, recs in sorted(table.items()):
                untagged = sum(1 for _, e, _ in recs if not e.tagged)
                pcps = sorted({e.pcp for _, e, _ in recs if e.tagged})
                deis = sorted({e.dei for _, e, _ in recs if e.tagged})
                vids = sorted({e.vid for _, e, _ in recs if e.tagged})
                out.append(_v(f"wt.{kind}.c-tag-present.{sid:016x}",
                              untagged == 0,
                              "802.1Q-2018 9.5 + Milan v1.2 7.3.3 (CRF) / "
                              "4.2.7.2.1: an SR stream is carried tagged; an "
                              "undeclared multicast DMAC is just multicast and "
                              "floods (measured 2026-07-28: 4001 untagged CRF "
                              "frames in 8 s)",
                              untagged_frames=untagged, frames=len(recs)))
                out.append(_v(f"wt.{kind}.c-tag-pcp.{sid:016x}",
                              pcps == [self.expect.sr_class_a_pcp],
                              "802.1Q-2018 34.5 / Milan v1.2 4.2.7.2.1: SR "
                              "class A priority",
                              expected=self.expect.sr_class_a_pcp,
                              observed=pcps))
                out.append(_v(f"wt.{kind}.c-tag-dei.{sid:016x}",
                              deis in ([0], []),
                              "802.1Q-2018 9.6: an SR class A stream is never "
                              "drop-eligible", observed=deis))
                if self.expect.sr_vid is None:
                    out.append(Verdict(f"wt.{kind}.c-tag-vid.{sid:016x}",
                                       "SKIP", "802.1Q-2018 9.6",
                                       {"why": "no SR VID supplied"}))
                else:
                    out.append(_v(f"wt.{kind}.c-tag-vid.{sid:016x}",
                                  vids == [self.expect.sr_vid],
                                  "802.1Q-2018 9.6 + the bench SR VID: VID 0 "
                                  "leaves the reserved SR tree, is stripped on "
                                  "egress and floods unshaped",
                                  expected=self.expect.sr_vid, observed=vids,
                                  vid_zero_seen=0 in vids))
        return out

    def check_zero_fill(self) -> list[Verdict]:
        """Milan 5.3.7.3: a bound talker STREAMS.  So a talker with no audio
        source owes present-and-silent frames, and a fed one owes non-zero
        samples.  Both directions are asserted, because a check that can only
        say 'silent' cannot tell zero-fill from a dead framer."""
        out = []
        if not self.expect.silent_stream_ids and not self.expect.fed_stream_ids:
            out.append(Verdict(
                "wt.aaf.zero-fill", "SKIP", "Milan v1.2 5.3.7.3",
                {"why": "no stream was declared silent-but-bound or fed, so "
                        "'silence' and 'absence' cannot be told apart here; "
                        "pass --silent-stream / --fed-stream",
                 "absent": "a silent/fed declaration"}))
        for sid in self.expect.silent_stream_ids:
            recs = self.aaf.get(int(sid), [])
            if not recs:
                out.append(_v(f"wt.aaf.zero-fill-present.{int(sid):016x}",
                              False,
                              "Milan v1.2 5.3.7.3: 'As long as a PAAD is "
                              "declaring a Talker Advertise attribute and "
                              "receiving a Listener Ready or Listener Ready "
                              "Failed attribute for a Stream Output, it shall "
                              "be streaming AVTP packets'",
                              why="declared silent-but-bound and NO frames "
                                  "reached the tap - silence is not the same "
                                  "as absence"))
                continue
            nz = [i for i, (_, _, p) in enumerate(recs)
                  if any(b for b in p.payload)]
            out.append(_v(f"wt.aaf.zero-fill-silent.{int(sid):016x}", not nz,
                          "Milan v1.2 5.3.7.3 + 5.3.7.3 zero-fill: an unfed "
                          "bound talker frames silence",
                          frames=len(recs), non_zero_frames=len(nz)))
        for sid in self.expect.fed_stream_ids:
            recs = self.aaf.get(int(sid), [])
            nz = [i for i, (_, _, p) in enumerate(recs)
                  if any(b for b in p.payload)]
            out.append(_v(f"wt.aaf.fed-non-silent.{int(sid):016x}",
                          bool(recs) and len(nz) == len(recs),
                          "IEEE 1722-2016 7.3.5: a fed talker's payload "
                          "carries samples; all-zero on a fed stream is the "
                          "silence defect, not zero-fill",
                          frames=len(recs), non_zero_frames=len(nz)))
        return out

    def check_crf_format(self) -> list[Verdict]:
        """Milan 7.3.2 pins base_frequency, timestamps_per_pdu and
        timestamp_interval; Table 7.1 pins type and pull too."""
        out = []
        if not self.crf:
            return [_nothing_to_check("wt.crf.milan-format",
                                      "Milan v1.2 7.3.2 + Table 7.1",
                                      "CRF frames")]
        want = self.expect.crf_format if self.expect.crf_format is not None \
            else MILAN_CRF_FORMAT
        d = parse_crf_stream_format(want)
        for sid, recs in sorted(self.crf.items()):
            _, _, p = recs[0]
            bad = {}
            if p.base_frequency != d.base_frequency:
                bad["base_frequency"] = [d.base_frequency, p.base_frequency]
            if p.timestamp_interval != d.timestamp_interval:
                bad["timestamp_interval"] = [d.timestamp_interval,
                                             p.timestamp_interval]
            if p.type != d.type:
                bad["type"] = [d.type, p.type]
            if p.pull != d.pull:
                bad["pull"] = [d.pull, p.pull]
            tspp = p.crf_data_length // 8
            if tspp != d.timestamps_per_pdu:
                bad["timestamps_per_pdu"] = [d.timestamps_per_pdu, tspp]
            if p.crf_data_length % 8:
                bad["crf_data_length"] = ["multiple of 8", p.crf_data_length]
            out.append(_v(f"wt.crf.milan-format.{sid:016x}", not bad,
                          "Milan v1.2 7.3.2: 'The base frequency shall be "
                          "48000Hz.  Each PDU shall contain 1 timestamp, and "
                          "the timestamp interval shall be 96.' + Table 7.1",
                          declared=f"{int(want):016x}", mismatches=bad,
                          frames=len(recs)))
        return out

    def check_crf_rate(self) -> list[Verdict]:
        """The PDU rate the format DEMANDS versus the rate on the wire, and the
        timestamp step inside the stream.  base_frequency / (interval * per_pdu)
        = 48000/96 = 500 PDU/s = one every 2 ms."""
        if not self.crf:
            return [_nothing_to_check(n, "Milan v1.2 7.3.2 + IEEE 1722-2016 "
                                         "10.4.12/10.4.13", "CRF frames")
                    for n in ("wt.crf.pdu-rate", "wt.crf.timestamp-step")]
        out = []
        for sid, recs in sorted(self.crf.items()):
            _, _, p = recs[0]
            per = max(1, p.crf_data_length // 8)
            if not p.timestamp_interval or not p.base_frequency:
                out.append(Verdict(f"wt.crf.pdu-rate.{sid:016x}", "SKIP",
                                   "Milan v1.2 7.3.2",
                                   {"why": "interval or base_frequency is 0"}))
                continue
            want_pps = p.base_frequency / (p.timestamp_interval * per)
            span = recs[-1][0] - recs[0][0]
            got = (len(recs) - 1) / span if span > 0 else None
            ok = got is not None and abs(got - want_pps) <= max(
                1.0, 0.05 * want_pps)
            out.append(Verdict(f"wt.crf.pdu-rate.{sid:016x}",
                               "PASS" if ok else ("SKIP" if got is None
                                                  else "FAIL"),
                               "Milan v1.2 7.3.2 + IEEE 1722-2016 10.4.12: "
                               "base_frequency / (timestamp_interval x "
                               "timestamps_per_pdu)",
                               {"expected_pps": want_pps, "observed_pps": got,
                                "frames": len(recs), "span_s": span}))
            step_ns = round(p.timestamp_interval * 1e9 / p.base_frequency)
            bad = []
            for i in range(1, len(recs)):
                a = recs[i - 1][2].timestamps[-1] if recs[i - 1][2].timestamps \
                    else None
                b = recs[i][2].timestamps[0] if recs[i][2].timestamps else None
                if a is None or b is None:
                    continue
                d = b - a
                if abs(d - step_ns * per) > step_ns:
                    bad.append({"at_frame": i, "step_ns": d})
            out.append(_v(f"wt.crf.timestamp-step.{sid:016x}", not bad,
                          "IEEE 1722-2016 10.4.12/10.4.13: consecutive CRF "
                          "timestamps are one timestamp_interval of media "
                          "events apart",
                          expected_step_ns=step_ns * per,
                          violations=bad[:8], violation_count=len(bad)))
        return out

    def check_adp_frame_rule(self) -> list[Verdict]:
        """The 82-byte ADPDU rule and the available_index monotonicity.

        1722.1-2021 6.2.1: the ADPDU is 68 octets, so 82 on the wire, and
        control_data_length is 56.  6.2.2.10: available_index increments on
        every transmitted ADPDU - a repeated value makes a controller treat the
        entity as incoherent, which is exactly what bump-on-change-only did to
        us in 2026-07-12.
        """
        out = []
        if not self.adp:
            out += [_nothing_to_check(n, "IEEE 1722.1-2021 6.2.1 / 6.2.2.10",
                                      "ADPDUs")
                    for n in ("wt.adp.frame-82",
                              "wt.adp.available-index-advances")]
        for eid, recs in sorted(self.adp.items()):
            wrong_len = [(n, l) for n, (_, l, _, _) in enumerate(recs)
                         if l != ADP_FRAME_LEN]
            wrong_cdl = [(n, c.control_data_length)
                         for n, (_, _, c, _) in enumerate(recs)
                         if c.control_data_length != ADP_CDL]
            out.append(_v(f"wt.adp.frame-82.{eid:016x}",
                          not wrong_len and not wrong_cdl,
                          "IEEE 1722.1-2021 6.2.1: a 4-octet control header + "
                          "an 8-octet entity_id + 56 octets = 68, i.e. 82 on "
                          "the wire with the Ethernet header",
                          expected_frame_len=ADP_FRAME_LEN,
                          expected_cdl=ADP_CDL,
                          wrong_length=wrong_len[:8],
                          wrong_cdl=wrong_cdl[:8], adpdus=len(recs)))
            idx = [ai for _, _, _, ai in recs if ai is not None]
            repeats = [i for i in range(1, len(idx))
                       if _mod_delta(idx[i], idx[i - 1], 1 << 32) == 0]
            out.append(_v(f"wt.adp.available-index-advances.{eid:016x}",
                          not repeats and len(idx) > 1,
                          "IEEE 1722.1-2021 6.2.2.10: available_index "
                          "increments on every transmitted ADPDU; a repeated "
                          "index reads as an incoherent entity",
                          adpdus=len(idx), repeats=len(repeats),
                          first=idx[0] if idx else None,
                          last=idx[-1] if idx else None))
        for eid in self.expect.adp_entity_ids:
            e = int(eid)
            out.append(_v(f"wt.adp.alive.{e:016x}", e in self.adp,
                          "IEEE 1722.1-2021 6.2.6: an available entity "
                          "re-advertises within valid_time; silence for the "
                          "whole capture is the dormancy signature",
                          adpdus=len(self.adp.get(e, []))))
        return out

    def check_control_length_honesty(self) -> list[Verdict]:
        """The frame must be at least as long as it claims to be.  This is the
        check a status-byte-only tool cannot make, and the defect it catches is
        real: a frame that declares control_data_length 84 and puts 20 octets
        on the wire."""
        if not self.control:
            return [_nothing_to_check(
                "wt.control.length-honest",
                "IEEE 1722.1-2021 9.2.1.1.6", "control frames (ADP/AECP/ACMP/"
                "MAAP)")]
        liars = []
        for i, (_, eth, c) in enumerate(self.control):
            if c.avtpdu_len < c.declared_avtpdu_len:
                liars.append({"n": i, "subtype": SUBTYPE_NAMES.get(c.subtype),
                              "cdl": c.control_data_length,
                              "declared_avtpdu": c.declared_avtpdu_len,
                              "actual_avtpdu": c.avtpdu_len})
        return [_v("wt.control.length-honest", not liars,
                   "IEEE 1722.1-2021 9.2.1.1.6: control_data_length counts the "
                   "octets after target_entity_id; a shorter frame is "
                   "malformed however correct its status byte is",
                   control_frames=len(self.control), liars=liars[:8],
                   liar_count=len(liars))]


    # -- SRP, which only the inline tap can see ---------------------------
    def srp_state(self) -> dict:
        """The SRP declarations the capture actually contains, per stream_id."""
        talkers, listeners, domains, vids = {}, {}, [], []
        for _ts, _e, at in self.mrp:
            f = at.fields
            if at.protocol == "MVRP":
                if at.declaring and f.get("vid") is not None:
                    vids.append(f["vid"])
                continue
            if at.attr_type in (MSRP_TALKER_ADVERTISE, MSRP_TALKER_FAILED):
                sid = f.get("stream_id")
                if sid is None:
                    continue
                rec = talkers.setdefault(sid, {"advertise": False,
                                               "failed": False,
                                               "withdrawn": False, "fields": f})
                if at.attr_type == MSRP_TALKER_ADVERTISE:
                    rec["advertise"] = rec["advertise"] or at.declaring
                else:
                    rec["failed"] = rec["failed"] or at.declaring
                if not at.declaring:
                    rec["withdrawn"] = True
                rec["fields"] = f
                rec["last_event"] = at.event
            elif at.attr_type == MSRP_LISTENER:
                sid = f.get("stream_id")
                if sid is None:
                    continue
                rec = listeners.setdefault(sid, {"declarations": [],
                                                 "ready": False})
                rec["declarations"].append(
                    {"event": at.event,
                     "declaration": f.get("declaration")})
                if at.declaring and f.get("declaration") in ("Ready",
                                                             "Ready Failed"):
                    rec["ready"] = True
            elif at.attr_type == MSRP_DOMAIN and at.declaring:
                domains.append(f)
        return {"talkers": talkers, "listeners": listeners,
                "domains": domains, "mvrp_vids": sorted(set(vids))}

    def check_srp_declarations(self) -> list[Verdict]:
        """The SRP half of the Milan v1.2 5.3.7.3 licence, from the WIRE.

        5.3.7.3: "As long as a PAAD is declaring a Talker Advertise attribute
        and receiving a Listener Ready or Listener Ready Failed attribute for a
        Stream Output, it shall be streaming AVTP packets."  Both halves of that
        conjunction are MSRP declarations on 01:80:C2:00:00:0E, which no bridge
        forwards - so this is the ONE check set that CANNOT be made from the
        controller host and CAN be made from an inline tap.  Its value is proven:
        it is how "only 2 of 5 talker stream_ids declare a Talker Advertise" was
        found, from the wire, with no board access at all.

        5.3.7.4 makes the Stream Destination MAC Address and the Stream VLAN ID
        SRP parameters of the Stream Output, so the declaration and the frames
        must agree about both - a stream whose DMAC or VID differs from its own
        declaration is riding outside its reservation.
        """
        out = []
        if not self.mrp:
            return [_nothing_to_check(
                n, "802.1Q-2018 35.2.2 + Milan v1.2 5.3.7.3: MSRP/MVRP go to "
                   "01:80:C2:00:00:0E, which a bridge does not forward, so only "
                   "an INLINE TAP can see them",
                "MSRP/MVRP frames (an inline tap capture is required; a mirror "
                "port and the controller host can never see these)")
                for n in ("wt.msrp.talker-advertise-declared",
                          "wt.msrp.listener-declaration-present",
                          "wt.msrp.declared-dmac-matches-wire",
                          "wt.msrp.declared-vid-matches-wire",
                          "wt.msrp.tspec-declared",
                          "wt.msrp.domain-declared",
                          "wt.mvrp.sr-vid-declared")]
        st = self.srp_state()
        streaming = sorted(self.aaf) + sorted(self.crf)
        expected = sorted(int(s) for s in self.expect.talker_stream_ids) \
            or streaming
        out.append(self._srp_talker_advertise(st, expected, streaming))
        out.append(self._srp_listener_licence(st, streaming))
        out += self._srp_declaration_matches_wire(st)
        out.append(self._srp_tspec(st))
        out += self._srp_domain_and_vid(st)
        return out

    def _srp_talker_advertise(self, st, expected, streaming) -> Verdict:
        """(1) every stream that IS on the wire, and every stream the
        controller says should be, must have a Talker Advertise declared."""
        if not expected:
            return Verdict("wt.msrp.talker-advertise-declared", "SKIP",
                           "Milan v1.2 5.3.7.4",
                           {"why": "no stream frames in the capture and no "
                                   "--talker-stream given, so there is no "
                                   "stream whose declaration to look for"})
        missing = [f"{s:016x}" for s in expected
                   if not st["talkers"].get(s, {}).get("advertise")]
        failed = [f"{s:016x}" for s in expected
                  if st["talkers"].get(s, {}).get("failed")]
        return _v("wt.msrp.talker-advertise-declared", not missing,
                  "Milan v1.2 5.3.7.2: 'For each of the Stream Outputs "
                  "of its currently set Configuration, a PAAD shall "
                  "always declare an MSRP Talker attribute as soon as it "
                  "has valid SRP parameters for this stream' + 802.1Q-"
                  "2018 35.2.2.8.3",
                  expected=[f"{s:016x}" for s in expected],
                  declared=sorted(f"{s:016x}" for s, r
                                  in st["talkers"].items()
                                  if r.get("advertise")),
                  missing=missing, talker_failed=failed,
                  streams_on_the_wire=[f"{s:016x}" for s in streaming])

    def _srp_listener_licence(self, st, streaming) -> Verdict:
        """(2) the LISTENER half of the licence."""
        if not streaming:
            return Verdict("wt.msrp.listener-declaration-present", "SKIP",
                           "Milan v1.2 5.3.7.3",
                           {"why": "no stream frames in the capture, so no "
                                   "stream needs a Listener declaration"})
        unlicensed = [f"{s:016x}" for s in streaming
                      if not st["listeners"].get(s, {}).get("ready")]
        return _v("wt.msrp.listener-declaration-present",
                  not unlicensed,
                  "Milan v1.2 5.3.7.3: a talker is licensed to stream "
                  "only while it is 'receiving a Listener Ready or "
                  "Listener Ready Failed attribute for a Stream "
                  "Output', so frames on the wire without one are "
                  "unreserved",
                  streaming=[f"{s:016x}" for s in streaming],
                  listener_declarations={
                      f"{s:016x}": r["declarations"][-3:]
                      for s, r in st["listeners"].items()},
                  without_listener_ready=unlicensed)

    def _srp_declaration_matches_wire(self, st) -> list[Verdict]:
        """(3) the declaration and the frames must agree about DMAC and VID."""
        out = []
        for name, key, getter, clause in (
                ("wt.msrp.declared-dmac-matches-wire", "destination_address",
                 lambda e: e.dst.hex(),
                 "Milan v1.2 5.3.7.4: the Stream Destination MAC Address is an "
                 "SRP parameter of the Stream Output, so the declared "
                 "DataFrameParameters.destination_address and the wire DMAC are "
                 "one value"),
                ("wt.msrp.declared-vid-matches-wire", "vlan_identifier",
                 lambda e: e.vid,
                 "Milan v1.2 5.3.7.4 + 802.1Q-2018 9.6: the Stream VLAN ID is "
                 "an SRP parameter, so the declared vlan_identifier and the "
                 "C-TAG VID are one value")):
            bad, checked = {}, []
            for table in (self.aaf, self.crf):
                for sid, recs in table.items():
                    decl = st["talkers"].get(sid, {}).get("fields", {})
                    if key not in decl:
                        continue
                    _t, eth, _p = recs[0]
                    got = getter(eth)
                    want = decl[key]
                    checked.append(f"{sid:016x}")
                    if key == "destination_address":
                        if got.lower() != str(want).lower():
                            bad[f"{sid:016x}"] = {"declared": want,
                                                  "on_the_wire": got}
                    elif got != want:
                        bad[f"{sid:016x}"] = {"declared": want,
                                              "on_the_wire": got}
            if not checked:
                out.append(Verdict(name, "SKIP", clause,
                                   {"why": "no stream in the capture has a "
                                           "Talker Advertise declaring this "
                                           "parameter, so there is nothing to "
                                           "compare"}))
            else:
                out.append(_v(name, not bad, clause, checked=checked,
                              mismatches=bad))
        return out

    def _srp_tspec(self, st) -> Verdict:
        """(4) the TSpec, recorded against the frames actually seen."""
        tspec, tbad = {}, {}
        for sid, r in st["talkers"].items():
            f = r.get("fields", {})
            if "max_frame_size" not in f:
                continue
            tspec[f"{sid:016x}"] = {
                "max_frame_size": f["max_frame_size"],
                "max_interval_frames": f["max_interval_frames"],
                "priority": f.get("priority"), "rank": f.get("rank"),
                "accumulated_latency_ns": f.get("accumulated_latency")}
            recs = self.aaf.get(sid) or self.crf.get(sid) or []
            if recs:
                # the tap adds no octets to wire_len here (read_capture strips the
                # record header), and MaxFrameSize excludes the 4-octet FCS and
                # the 14/18-octet Ethernet header per 802.1Q-2018 35.2.2.8.5
                biggest = max(len(p.payload) + 24 for _t, _e, p in recs
                              if hasattr(p, "payload"))
                if f["max_frame_size"] and biggest > f["max_frame_size"]:
                    tbad[f"{sid:016x}"] = {
                        "declared_max_frame_size": f["max_frame_size"],
                        "largest_avtpdu_seen": biggest}
            if f["max_interval_frames"] == 0:
                tbad.setdefault(f"{sid:016x}", {})["max_interval_frames"] = 0
        if not tspec:
            return Verdict("wt.msrp.tspec-declared", "SKIP",
                           "802.1Q-2018 35.2.2.8.5",
                           {"why": "no Talker Advertise in the capture "
                                   "carries a TSpec"})
        return _v("wt.msrp.tspec-declared", not tbad,
                  "802.1Q-2018 35.2.2.8.5 TSpec: MaxFrameSize is the "
                  "largest frame the reservation covers and "
                  "MaxIntervalFrames the count per class measurement "
                  "interval; a frame larger than the declaration is "
                  "outside the reservation it claims",
                  declared=tspec, violations=tbad)

    def _srp_domain_and_vid(self, st) -> list[Verdict]:
        """(5) the SR Domain, and the MVRP VID registration."""
        out = []
        if not st["domains"]:
            out.append(Verdict("wt.msrp.domain-declared", "SKIP",
                               "802.1Q-2018 35.2.2.9 + Milan v1.2 4.2.7.2",
                               {"why": "no MSRP Domain attribute in the "
                                       "capture; a short capture can miss one "
                                       "because Domain is re-declared on the "
                                       "MRP timers, not per frame",
                                "absent": "MSRP Domain attribute"}))
        else:
            want_pcp = self.expect.sr_class_a_pcp
            bad = [d for d in st["domains"]
                   if d.get("sr_class_id") == 6
                   and d.get("sr_class_priority") != want_pcp]
            out.append(_v("wt.msrp.domain-declared", not bad,
                          "802.1Q-2018 35.2.2.9 + Milan v1.2 4.2.7.2.1: the SR "
                          "class A Domain attribute carries the class's "
                          "priority and VID, and the frames must use them",
                          domains=st["domains"], expected_class_a_pcp=want_pcp,
                          mismatches=bad))
        if not st["mvrp_vids"]:
            out.append(Verdict("wt.mvrp.sr-vid-declared", "SKIP",
                               "802.1Q-2018 11.2.3.1.2",
                               {"why": "no MVRP VID declaration in the capture; "
                                       "MVRP re-declares on its own timers, so "
                                       "a short capture can miss it",
                                "absent": "MVRP VID attribute"}))
        elif self.expect.sr_vid is None:
            out.append(Verdict("wt.mvrp.sr-vid-declared", "SKIP",
                               "802.1Q-2018 11.2.3.1.2",
                               {"why": "no expected SR VID supplied",
                                "observed": st["mvrp_vids"]}))
        else:
            out.append(_v("wt.mvrp.sr-vid-declared",
                          self.expect.sr_vid in st["mvrp_vids"],
                          "802.1Q-2018 11.2.3.1.2: the SR VID is registered by "
                          "MVRP; an unregistered VID is not pruned to the "
                          "listeners and the stream floods",
                          expected=self.expect.sr_vid,
                          observed=st["mvrp_vids"]))
        return out
