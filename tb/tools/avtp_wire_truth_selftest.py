#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""avtp_wire_truth_selftest.py - the offline arms: every decoder and every
check against hand-built byte vectors.  No capture, no hardware, no network.

Each block ends with a NEGATIVE control, because a check that cannot fail is
not a check (docs/testing/methodology.md R2).  Run it through the CLI:

    python3 avtp_wire_truth.py --self-test"""
from __future__ import annotations

import struct
from pathlib import Path

from avtp_wire_truth_wire import (ADP_CDL, ADP_FRAME_LEN,
                                  CRF_TYPE_AUDIO_SAMPLE, ETH_P_AVTP,
                                  Expectation, MILAN_CRF_BASE_HZ,
                                  MILAN_CRF_FORMAT, MILAN_CRF_TS_INTERVAL,
                                  MILAN_CRF_TS_PER_PDU, MSRP_DOMAIN,
                                  MSRP_LISTENER, MSRP_TALKER_ADVERTISE,
                                  TPID_C_TAG, decode_aaf, decode_crf,
                                  decode_eth, decode_mrpdu,
                                  parse_aaf_stream_format,
                                  parse_crf_stream_format, read_capture)
from avtp_wire_truth_checks import WireTruth
from avtp_wire_truth_identity import check_walking_tone
from avtp_wire_truth_frames import (TalkerAdvertise, build_aaf_frame,
                                    build_adp_frame, build_crf_frame,
                                    build_msrp_frame, build_mvrp_frame,
                                    msrp_domain_value, msrp_listener_value,
                                    msrp_talker_advertise_value)


# ------------------------------------------------------------------ self test --
class _AafWireArms:
    """AAF: the Figure 26 decode, the declared-vs-wire escape, sequence,
    VLAN, timestamps, zero fill and the per-channel identity."""

    def test_aaf_decode_matches_the_figure(self) -> None:
        """Every Figure 26 field survives the decode of a frame built, by hand,
        from that figure rather than from our packetizer."""
        f = build_aaf_frame(seq=7, channels=8, ts=0x11223344, tu=1)
        eth = decode_eth(f)
        self.assertTrue(eth.tagged)
        self.assertEqual((eth.pcp, eth.dei, eth.vid), (3, 0, 2))
        self.assertEqual(eth.ethertype, ETH_P_AVTP)
        p = decode_aaf(eth.payload)
        self.assertEqual(p.sequence_num, 7)
        self.assertEqual(p.channels_per_frame, 8)
        self.assertEqual(p.avtp_timestamp, 0x11223344)
        self.assertEqual(p.tu, 1)
        self.assertEqual(p.tv, 1)
        self.assertEqual(p.bit_depth, 32)
        self.assertEqual(p.nsr, 5)
        self.assertEqual(p.format_name, "INT_32BIT")
        self.assertEqual(p.sample_frames, 6)
        self.assertEqual(p.stream_data_length, 6 * 8 * 4)


    def test_aaf_channels_per_frame_spans_two_octets(self) -> None:
        """A 10-bit count split 2+8 across two octets survives the decode."""
        # 7.3.3 is a 10-bit field: 0x105 has to survive the 2+8 split
        f = build_aaf_frame(channels=0x105, sample_frames=1)
        p = decode_aaf(decode_eth(f).payload)
        self.assertEqual(p.channels_per_frame, 0x105)


    def test_aaf_stream_format_qword_round_trip(self) -> None:
        """The Annex I.2.4 field extraction, ut bit included - and a CRF qword
        handed to the AAF parser decodes to None rather than to nonsense."""
        d = parse_aaf_stream_format("0205022001006000")
        self.assertEqual(d.channels_per_frame, 4)
        self.assertEqual(d.nsr, 5)
        self.assertEqual(d.fmt, 2)
        self.assertEqual(d.bit_depth, 32)
        self.assertEqual(d.samples_per_frame, 6)
        self.assertEqual(d.ut, 0)
        self.assertEqual(parse_aaf_stream_format(0x0205022000806000)
                         .channels_per_frame, 2)
        self.assertEqual(parse_aaf_stream_format(0x0205022002006000)
                         .channels_per_frame, 8)
        self.assertEqual(parse_aaf_stream_format(0x0215022002006000).ut, 1)
        self.assertIsNone(parse_aaf_stream_format(MILAN_CRF_FORMAT))


    def test_declared_vs_wire_catches_the_2026_07_27_escape(self) -> None:
        """The escape itself: 8 channels declared, 2 on the wire, one FAIL
        naming channels_per_frame - and the honest pair still passes."""
        # a talker advertising 8 channels while the framer emits 2
        wt = WireTruth(Expectation(aaf_format=0x0205022002006000))
        wt.feed(0.0, build_aaf_frame(channels=2))
        bad = [v for v in wt.check_aaf_declared_vs_wire()
               if v.verdict == "FAIL"]
        self.assertEqual(len(bad), 1)
        self.assertIn("channels_per_frame", bad[0].detail["mismatches"])
        # NEGATIVE CONTROL: the honest pair must pass
        wt = WireTruth(Expectation(aaf_format=0x0205022000806000))
        wt.feed(0.0, build_aaf_frame(channels=2))
        self.assertTrue(all(v.verdict == "PASS"
                            for v in wt.check_aaf_declared_vs_wire()))


    def test_sequence_gap_and_wrap(self) -> None:
        """4.4.4.6: 255 -> 0 is a WRAP, a skipped number is a gap - and the CRF
        family, which saw no frames, says SKIP instead of emitting nothing."""
        wt = WireTruth()
        for s in (254, 255, 0, 1):
            wt.feed(0.0, build_aaf_frame(seq=s))
        vs = wt.check_sequence_continuity()
        self.assertTrue(all(v.verdict == "PASS" for v in vs
                            if v.check.startswith("wt.aaf.")), vs)
        # and the CRF family, which had NO frames, says SKIP rather than
        # emitting nothing: an absent family and a passing one must be
        # distinguishable in the log
        crf = [v for v in vs if v.check.startswith("wt.crf.")]
        self.assertEqual([v.verdict for v in crf], ["SKIP"])
        self.assertIn("CRF frames", crf[0].detail["absent"])
        wt = WireTruth()
        for s in (1, 2, 4):
            wt.feed(0.0, build_aaf_frame(seq=s))
        v = wt.check_sequence_continuity()[0]
        self.assertEqual(v.verdict, "FAIL")
        self.assertEqual(v.detail["gap_count"], 1)


    def test_vlan_checks_and_the_vid_zero_defect(self) -> None:
        """VID 0 on a stream frame and an untagged CRF are each a FAIL; the
        conformant C-TAG passes every VLAN check (the negative control)."""
        wt = WireTruth()
        wt.feed(0.0, build_aaf_frame(vid=0))
        v = [x for x in wt.check_vlan_class()
             if "c-tag-vid" in x.check][0]
        self.assertEqual(v.verdict, "FAIL")
        self.assertTrue(v.detail["vid_zero_seen"])
        wt = WireTruth()
        wt.feed(0.0, build_crf_frame(tagged=False))
        v = [x for x in wt.check_vlan_class()
             if "crf.c-tag-present" in x.check][0]
        self.assertEqual(v.verdict, "FAIL")
        # NEGATIVE CONTROL: the conformant tag passes every VLAN check
        wt = WireTruth()
        wt.feed(0.0, build_aaf_frame())
        wt.feed(0.0, build_crf_frame())
        self.assertTrue(all(x.verdict == "PASS"
                            for x in wt.check_vlan_class()))


    def test_header_legality_negatives(self) -> None:
        """The three headers 7.3.3/7.3.4 forbid outright - zero channels, zero
        bit_depth, and a bit_depth wider than its own format - each refused."""
        for kw, needle in ((dict(channels=0, sample_frames=0),
                            "channels_per_frame 0"),
                           (dict(bit_depth=0), "bit_depth 0"),
                           (dict(fmt=0x4, bit_depth=32),
                            "bit_depth 32 > format width 16")):
            wt = WireTruth()
            wt.feed(0.0, build_aaf_frame(**kw))
            v = wt.check_aaf_header_legality()[0]
            self.assertEqual(v.verdict, "FAIL", kw)
            self.assertTrue(any(needle in s
                                for s in v.detail["violations"]),
                            (kw, v.detail))


    def test_pts_step_is_one_avtpdu_of_media(self) -> None:
        """The PTS must advance by exactly one AVTPDU of media (6 samples at
        48 kHz = 125 us); a 500 us step on the same frames is a FAIL."""
        wt = WireTruth()
        for i in range(5):                      # 6 samples @48k = 125 us
            wt.feed(0.0, build_aaf_frame(seq=i, ts=i * 125_000))
        v = [x for x in wt.check_aaf_timestamps()
             if "pts-step" in x.check][0]
        self.assertEqual(v.verdict, "PASS")
        self.assertEqual(v.detail["expected_step_ns"], 125_000)
        wt = WireTruth()
        for i in range(5):
            wt.feed(0.0, build_aaf_frame(seq=i, ts=i * 500_000))
        v = [x for x in wt.check_aaf_timestamps()
             if "pts-step" in x.check][0]
        self.assertEqual(v.verdict, "FAIL")


    def test_class_a_transit_skips_without_a_gptp_reference(self) -> None:
        """Transit time is unmeasurable without a gPTP reference, so it SKIPs
        rather than assuming one; given a reference it passes at 1.5 ms and
        fails at 9 ms against the 2 ms class A budget."""
        wt = WireTruth()
        wt.feed(0.0, build_aaf_frame())
        v = [x for x in wt.check_aaf_timestamps()
             if "class-a-transit" in x.check][0]
        self.assertEqual(v.verdict, "SKIP")
        # with a reference it becomes a real check, both ways
        wt = WireTruth(Expectation(gptp_ref_ns=1_000_000))
        wt.feed(0.0, build_aaf_frame(ts=1_000_000 + 1_500_000))
        self.assertEqual([x for x in wt.check_aaf_timestamps()
                          if "class-a-transit" in x.check][0].verdict,
                         "PASS")
        wt = WireTruth(Expectation(gptp_ref_ns=1_000_000))
        wt.feed(0.0, build_aaf_frame(ts=1_000_000 + 9_000_000))
        self.assertEqual([x for x in wt.check_aaf_timestamps()
                          if "class-a-transit" in x.check][0].verdict,
                         "FAIL")


    def test_zero_fill_both_directions(self) -> None:
        """Milan 5.3.7.3 in both directions: a stream declared silent must be
        PRESENT and zero, a stream declared fed must not be zero, and no frames
        at all is a FAIL for either - absence is not silence."""
        sid = 0x020000000002_0000
        wt = WireTruth(Expectation(silent_stream_ids=(sid,)))
        wt.feed(0.0, build_aaf_frame(sid=sid))
        self.assertTrue(all(v.verdict == "PASS"
                            for v in wt.check_zero_fill()))
        # a stream declared silent that carries audio is a FAIL...
        tone = [[0x123456] * 2 for _ in range(6)]
        wt = WireTruth(Expectation(silent_stream_ids=(sid,)))
        wt.feed(0.0, build_aaf_frame(sid=sid, samples=tone))
        self.assertEqual(wt.check_zero_fill()[0].verdict, "FAIL")
        # ...and a declared-silent stream with NO frames is also a FAIL:
        # Milan 5.3.7.3 says it streams, so absence != silence
        wt = WireTruth(Expectation(silent_stream_ids=(sid,)))
        self.assertEqual(wt.check_zero_fill()[0].verdict, "FAIL")
        # a fed stream that is all zeros is the silence defect
        wt = WireTruth(Expectation(fed_stream_ids=(sid,)))
        wt.feed(0.0, build_aaf_frame(sid=sid))
        self.assertEqual(wt.check_zero_fill()[0].verdict, "FAIL")


    def test_walking_tone_identity(self) -> None:
        """A swap, a duplicate and a dropped channel are three DIFFERENT
        failures here, which is the whole reason the tone is per-channel:
        presence testing calls all three "audio present"."""
        n, ch = 6, 4
        good = [[1 << c for c in range(ch)] for _ in range(n)]
        p = decode_aaf(decode_eth(build_aaf_frame(
            channels=ch, sample_frames=n, samples=good)).payload)
        self.assertTrue(all(v.verdict == "PASS"
                            for v in check_walking_tone([p], ch)))
        # a SWAP of channels 1 and 2
        sw = [[1, 4, 2, 8] for _ in range(n)]
        p = decode_aaf(decode_eth(build_aaf_frame(
            channels=ch, sample_frames=n, samples=sw)).payload)
        vs = {v.check: v.verdict for v in check_walking_tone([p], ch)}
        self.assertEqual(vs["audio.identity.uncrossed"], "FAIL")
        # a DUPLICATE of channel 0 onto channel 1
        du = [[1, 1, 4, 8] for _ in range(n)]
        p = decode_aaf(decode_eth(build_aaf_frame(
            channels=ch, sample_frames=n, samples=du)).payload)
        vs = {v.check: v.verdict for v in check_walking_tone([p], ch)}
        self.assertEqual(vs["audio.identity.no-duplicate-neighbour"],
                         "FAIL")
        # a DROPPED channel 2
        dr = [[1, 2, 0, 8] for _ in range(n)]
        p = decode_aaf(decode_eth(build_aaf_frame(
            channels=ch, sample_frames=n, samples=dr)).payload)
        vs = {v.check: v.verdict for v in check_walking_tone([p], ch)}
        self.assertEqual(vs["audio.identity.no-silent-channel"], "FAIL")


class _CrfWireArms:
    """CRF: the Figure 72 decode, the one-octet sequence, the Milan
    stream-format constant and the media-clock rate."""

    def test_crf_stream_format_is_the_milan_constant(self) -> None:
        """Milan v1.2 Table 7.1's pinned qword decodes to the Annex I.2.6
        fields it names - the known-good vector the 29-bit base_frequency
        width was resolved from."""
        d = parse_crf_stream_format(MILAN_CRF_FORMAT)
        self.assertEqual(d.type, CRF_TYPE_AUDIO_SAMPLE)
        self.assertEqual(d.timestamp_interval, MILAN_CRF_TS_INTERVAL)
        self.assertEqual(d.timestamps_per_pdu, MILAN_CRF_TS_PER_PDU)
        self.assertEqual(d.pull, 0)
        self.assertEqual(d.base_frequency, MILAN_CRF_BASE_HZ)


    def test_crf_decode_matches_the_figure(self) -> None:
        """Every Figure 72 field survives the decode of a hand-built frame."""
        p = decode_crf(decode_eth(build_crf_frame(seq=250)).payload)
        self.assertEqual(p.sequence_num, 250)
        self.assertEqual(p.type, 1)
        self.assertEqual(p.base_frequency, 48000)
        self.assertEqual(p.timestamp_interval, 96)
        self.assertEqual(p.crf_data_length, 8)
        self.assertEqual(len(p.timestamps), 1)


    def test_crf_sequence_is_one_octet(self) -> None:
        """The CRF sequence is ONE octet: reading it as 16 bits would turn the
        FF -> 00 wrap into a gap of -255 and report a defect that is not one."""
        # 10.4.6: FF -> 00 is a WRAP, not a gap.  Reading the field as 16
        # bits would make this a gap of -255.
        wt = WireTruth()
        for s in (0xFE, 0xFF, 0x00):
            wt.feed(0.0, build_crf_frame(seq=s))
        v = [x for x in wt.check_sequence_continuity()
             if x.check.startswith("wt.crf.seq")][0]
        self.assertEqual(v.verdict, "PASS")


    def test_crf_rate_and_format(self) -> None:
        """Milan 7.3.2 fixes 48000 Hz and interval 96, so the expected media
        clock is 500 PDU/s - measured against the clause, not against us - and
        a non-Milan interval is a FAIL."""
        wt = WireTruth()
        for i in range(101):                     # 500 pps for 200 ms
            wt.feed(i * 0.002, build_crf_frame(seq=i & 0xFF,
                                               ts=i * 2_000_000))
        self.assertTrue(all(v.verdict == "PASS"
                            for v in wt.check_crf_format()))
        rate = [v for v in wt.check_crf_rate()
                if "pdu-rate" in v.check][0]
        self.assertEqual(rate.verdict, "PASS")
        self.assertAlmostEqual(rate.detail["expected_pps"], 500.0)
        # a non-Milan interval is a FAIL against Milan 7.3.2
        wt = WireTruth()
        wt.feed(0.0, build_crf_frame(interval=48))
        self.assertEqual(wt.check_crf_format()[0].verdict, "FAIL")


class _ControlPlaneArms:
    """ADP, the AVTP control length, and the empty-capture rule."""

    def test_adp_82_byte_rule_and_available_index(self) -> None:
        """The ADPDU is 82 octets and available_index must ADVANCE: a repeat
        is the 2026-07-12 incoherence a controller reads as a re-enumeration."""
        wt = WireTruth()
        for i in (1, 2, 3):
            wt.feed(0.0, build_adp_frame(available_index=i))
        self.assertTrue(all(v.verdict == "PASS"
                            for v in wt.check_adp_frame_rule()))
        self.assertEqual(len(build_adp_frame()), ADP_FRAME_LEN)
        # a short body breaks the 82-byte rule
        wt = WireTruth()
        wt.feed(0.0, build_adp_frame(body_len=40, cdl=ADP_CDL))
        self.assertEqual([v for v in wt.check_adp_frame_rule()
                          if "frame-82" in v.check][0].verdict, "FAIL")
        # a repeated available_index is the 2026-07-12 incoherence
        wt = WireTruth()
        for i in (5, 5, 6):
            wt.feed(0.0, build_adp_frame(available_index=i))
        self.assertEqual([v for v in wt.check_adp_frame_rule()
                          if "available-index" in v.check][0].verdict,
                         "FAIL")


    def test_control_length_lie(self) -> None:
        """A frame claiming 200 octets while carrying 56 is malformed however
        correct its status byte is (9.2.1.1.6); the honest one passes."""
        wt = WireTruth()
        wt.feed(0.0, build_adp_frame())
        self.assertEqual(wt.check_control_length_honesty()[0].verdict,
                         "PASS")
        wt = WireTruth()
        wt.feed(0.0, build_adp_frame(cdl=200))     # claims 200, carries 56
        v = wt.check_control_length_honesty()[0]
        self.assertEqual(v.verdict, "FAIL")
        self.assertEqual(v.detail["liars"][0]["cdl"], 200)


    def test_empty_capture_is_not_a_pass(self) -> None:
        """No stream frames reads FAIL, never PASS - a mirror port that never
        joined the group is this project's commonest false green."""
        self.assertEqual(WireTruth().check_capture_shape()[0].verdict,
                         "FAIL")


    def test_an_empty_capture_produces_NO_PASS_AND_NO_SILENCE(self) -> None:
        """The empty-collection rule, both halves.

        Eight of the twelve check families used to emit NOTHING on an empty
        capture - so the log could not tell "did not apply" from "was not
        run" - and wt.control.length-honest emitted PASS, because `not []`
        is True.  An empty capture is this project's commonest false green
        (a mirror port that never joined the multicast group), so:
          * no check may PASS, and
          * every family must be REPRESENTED, by a SKIP naming what was
            absent.
        """
        vs = WireTruth(Expectation()).checks()
        self.assertEqual([v.check for v in vs if v.verdict == "PASS"], [])
        shape = [v for v in vs if v.check ==
                 "wt.capture.stream-frames-present"]
        self.assertEqual([v.verdict for v in shape], ["FAIL"])
        names = {v.check for v in vs}
        for family in ("wt.aaf.header-legal", "wt.aaf.payload-arithmetic",
                       "wt.aaf.seq-continuity", "wt.crf.seq-continuity",
                       "wt.aaf.tv-set", "wt.aaf.pts-step",
                       "wt.aaf.class-a-transit", "wt.aaf.c-tag-present",
                       "wt.aaf.c-tag-pcp", "wt.aaf.c-tag-dei",
                       "wt.aaf.c-tag-vid", "wt.crf.c-tag-present",
                       "wt.crf.milan-format", "wt.crf.pdu-rate",
                       "wt.crf.timestamp-step", "wt.adp.frame-82",
                       "wt.adp.available-index-advances",
                       "wt.aaf.zero-fill", "wt.control.length-honest"):
            self.assertIn(family, names, f"{family} emitted nothing")
        for v in vs:
            if v.verdict == "SKIP":
                self.assertTrue(v.detail.get("why"), v.check)
        # and --fail-on-skip is what turns this honest SKIP set into a
        # non-zero exit for a gate that must be fully wired
        self.assertTrue(any(v.verdict == "SKIP" for v in vs))


class _SrpWireArms:
    """MSRP/MVRP: the byte layout from the clause, the Milan 5.3.7.3
    licence, and what a capture without an inline tap may say."""

    def test_msrp_decode_from_the_clause_byte_layout(self) -> None:
        """802.1Q-2018 35.2.2.8: StreamID(8) + DataFrameParameters(8) +
        TSpec(4) + PriorityAndRank(1) + AccumulatedLatency(4) = 25."""
        v = msrp_talker_advertise_value(TalkerAdvertise(
            stream_id=0x0200000000020003, dmac="91e0f000fe07", vid=2,
            max_frame=1024, max_interval=1, pcp=3, rank=1, latency=12345))
        self.assertEqual(len(v), 25)
        f = build_msrp_frame(attrs=[(MSRP_TALKER_ADVERTISE, v, [1], [])])
        got = decode_mrpdu(decode_eth(f).payload, "MSRP")
        self.assertEqual(len(got), 1)
        a = got[0]
        self.assertEqual(a.attr_name, "Talker Advertise")
        self.assertEqual(a.event, "JoinIn")
        self.assertTrue(a.declaring)
        self.assertEqual(a.fields["stream_id"], 0x0200000000020003)
        self.assertEqual(a.fields["destination_address"], "91e0f000fe07")
        self.assertEqual(a.fields["vlan_identifier"], 2)
        self.assertEqual(a.fields["max_frame_size"], 1024)
        self.assertEqual(a.fields["max_interval_frames"], 1)
        self.assertEqual(a.fields["priority"], 3)
        self.assertEqual(a.fields["accumulated_latency"], 12345)
        # a Listener attribute is 8 octets and its declaration TYPE rides
        # the FourPackedEvents vector, not the value
        f = build_msrp_frame(attrs=[(MSRP_LISTENER,
                                     msrp_listener_value(0x0200000000020003),
                                     [1], [2])])
        a = decode_mrpdu(decode_eth(f).payload, "MSRP")[0]
        self.assertEqual(a.fields["declaration"], "Ready")
        # a vector of N values increments the StreamID's unique_id
        f = build_msrp_frame(attrs=[(MSRP_LISTENER,
                                     msrp_listener_value(0x0200000000020000),
                                     [1, 1, 1], [2, 2, 3])])
        got = decode_mrpdu(decode_eth(f).payload, "MSRP")
        self.assertEqual([a.fields["stream_id"] for a in got],
                         [0x0200000000020000, 0x0200000000020001,
                          0x0200000000020002])
        self.assertEqual([a.fields["declaration"] for a in got],
                         ["Ready", "Ready", "Ready Failed"])
        # a truncated PDU decodes what it can rather than raising: a tap can
        # legitimately start mid-PDU
        self.assertEqual(decode_mrpdu(b"\x00\x01", "MSRP"), [])


    def test_the_srp_licence_is_visible_only_from_the_tap(self) -> None:
        """Milan v1.2 5.3.7.3 + 5.3.7.2, from the wire.

        This is the check set that found a real defect - only 2 of 5 talker
        stream_ids declaring a Talker Advertise - and it can only be made
        from an inline tap, because MSRP goes to 01:80:C2:00:00:0E and a
        bridge does not forward it.
        """
        sid = 0x0200000000020000
        w = WireTruth(Expectation(
            talker_stream_ids=(sid, sid + 1, sid + 2, sid + 3, sid + 4)))
        w.feed(0.0, build_aaf_frame(sid=sid, vid=2, pcp=3,
                                    dmac="91e0f000fe01"))
        w.feed(0.1, build_msrp_frame(attrs=[
            (MSRP_TALKER_ADVERTISE,
             msrp_talker_advertise_value(TalkerAdvertise(
                 stream_id=sid, dmac="91e0f000fe01", vid=2)),
             [1], []),
            (MSRP_TALKER_ADVERTISE,
             msrp_talker_advertise_value(TalkerAdvertise(
                 stream_id=sid + 1, dmac="91e0f000fe02", vid=2)),
             [1], []),
            (MSRP_LISTENER, msrp_listener_value(sid), [1], [2]),
            (MSRP_DOMAIN, msrp_domain_value(6, 3, 2), [1], [])]))
        w.feed(0.2, build_mvrp_frame(vids=(2,)))
        v = {x.check: x for x in w.check_srp_declarations()}
        # THE DEFECT: 3 of the 5 declared stream_ids never advertised
        t = v["wt.msrp.talker-advertise-declared"]
        self.assertEqual(t.verdict, "FAIL")
        self.assertEqual(t.detail["missing"],
                         [f"{sid + i:016x}" for i in (2, 3, 4)])
        # the licence half IS present for the stream that is running
        self.assertEqual(
            v["wt.msrp.listener-declaration-present"].verdict, "PASS")
        # the declaration and the frames agree about DMAC and VID
        self.assertEqual(v["wt.msrp.declared-dmac-matches-wire"].verdict,
                         "PASS")
        self.assertEqual(v["wt.msrp.declared-vid-matches-wire"].verdict,
                         "PASS")
        self.assertEqual(v["wt.msrp.domain-declared"].verdict, "PASS")
        self.assertEqual(v["wt.mvrp.sr-vid-declared"].verdict, "PASS")
        self.assertEqual(v["wt.msrp.tspec-declared"].verdict, "PASS")
        self._srp_licence_negative_controls(sid)

    def _srp_licence_negative_controls(self, sid):
        """One negative control per SRP check, because a check that cannot
        fail is not a check (methodology R2)."""
        # (a) frames on the wire with NO Listener Ready = unreserved
        w = WireTruth(Expectation(talker_stream_ids=(sid,)))
        w.feed(0.0, build_aaf_frame(sid=sid, dmac="91e0f000fe01"))
        w.feed(0.1, build_msrp_frame(attrs=[
            (MSRP_TALKER_ADVERTISE,
             msrp_talker_advertise_value(TalkerAdvertise(
                 stream_id=sid, dmac="91e0f000fe01")), [1], []),
            (MSRP_LISTENER, msrp_listener_value(sid), [1], [1])]))
        v = {x.check: x for x in w.check_srp_declarations()}
        self.assertEqual(
            v["wt.msrp.listener-declaration-present"].verdict, "FAIL")
        self.assertEqual(
            v["wt.msrp.listener-declaration-present"]
            .detail["without_listener_ready"], [f"{sid:016x}"])
        # (b) the DMAC on the wire is not the one declared
        w = WireTruth(Expectation(talker_stream_ids=(sid,)))
        w.feed(0.0, build_aaf_frame(sid=sid, dmac="91e0f000fe09"))
        w.feed(0.1, build_msrp_frame(attrs=[
            (MSRP_TALKER_ADVERTISE,
             msrp_talker_advertise_value(TalkerAdvertise(
                 stream_id=sid, dmac="91e0f000fe01", vid=2)),
             [1], [])]))
        v = {x.check: x for x in w.check_srp_declarations()}
        self.assertEqual(v["wt.msrp.declared-dmac-matches-wire"].verdict,
                         "FAIL")
        # (c) the VID on the wire is not the one declared
        w = WireTruth(Expectation(talker_stream_ids=(sid,)))
        w.feed(0.0, build_aaf_frame(sid=sid, dmac="91e0f000fe01", vid=5))
        w.feed(0.1, build_msrp_frame(attrs=[
            (MSRP_TALKER_ADVERTISE,
             msrp_talker_advertise_value(TalkerAdvertise(
                 stream_id=sid, dmac="91e0f000fe01", vid=2)),
             [1], [])]))
        v = {x.check: x for x in w.check_srp_declarations()}
        self.assertEqual(v["wt.msrp.declared-vid-matches-wire"].verdict,
                         "FAIL")
        # (d) a WITHDRAWN (Lv) Talker Advertise is not a declaration
        w = WireTruth(Expectation(talker_stream_ids=(sid,)))
        w.feed(0.1, build_msrp_frame(attrs=[
            (MSRP_TALKER_ADVERTISE,
             msrp_talker_advertise_value(
                 TalkerAdvertise(stream_id=sid)), [5], [])]))
        v = {x.check: x for x in w.check_srp_declarations()}
        self.assertEqual(v["wt.msrp.talker-advertise-declared"].verdict,
                         "FAIL")
        # (e) a frame larger than the declared MaxFrameSize is outside its
        #     own reservation
        w = WireTruth(Expectation(talker_stream_ids=(sid,)))
        w.feed(0.0, build_aaf_frame(sid=sid, dmac="91e0f000fe01",
                                    channels=8, sample_frames=48))
        w.feed(0.1, build_msrp_frame(attrs=[
            (MSRP_TALKER_ADVERTISE,
             msrp_talker_advertise_value(TalkerAdvertise(
                 stream_id=sid, dmac="91e0f000fe01",
                 max_frame=100)), [1], [])]))
        v = {x.check: x for x in w.check_srp_declarations()}
        self.assertEqual(v["wt.msrp.tspec-declared"].verdict, "FAIL")
        # (f) the wrong SR class A priority in the Domain attribute
        w = WireTruth()
        w.feed(0.1, build_msrp_frame(attrs=[
            (MSRP_DOMAIN, msrp_domain_value(6, 2, 2), [1], [])]))
        v = {x.check: x for x in w.check_srp_declarations()}
        self.assertEqual(v["wt.msrp.domain-declared"].verdict, "FAIL")
        # (g) MVRP registering a VID that is not the SR VID
        w = WireTruth(Expectation(sr_vid=2))
        w.feed(0.1, build_mvrp_frame(vids=(7,)))
        v = {x.check: x for x in w.check_srp_declarations()}
        self.assertEqual(v["wt.mvrp.sr-vid-declared"].verdict, "FAIL")


    def test_a_capture_with_no_MRP_says_it_needs_the_tap(self) -> None:
        """Every SRP check SKIPs and says INLINE TAP when no MRP was captured,
        so an unseeable exchange never reads as a clean one."""
        # A mirror port and the controller host can NEVER see these frames,
        # so the SKIP has to say that rather than reading as "no problem".
        w = WireTruth()
        w.feed(0.0, build_aaf_frame())
        vs = w.check_srp_declarations()
        self.assertTrue(vs)
        self.assertTrue(all(v.verdict == "SKIP" for v in vs))
        self.assertIn("INLINE TAP", vs[0].detail["absent"].upper()
                      + vs[0].clause.upper())


class _CaptureFormatArms:
    """The capture itself: the 28-octet ProfiShark record header and the
    pcap round trip."""

    def test_the_28_octet_tap_record_header_is_handled_and_tested(self) -> None:
        """The ProfiShark inline tap prepends a 28-octet record header, so
        EVERY ether offset shifts by +28: in a BPF filter the EtherType is
        ether[40:2] and the DMAC is at 28.  A decoder that ignores it sees
        garbage; one that assumes it on an already-stripped capture also sees
        garbage.  Both directions are tested."""
        import os
        import struct as _s
        import tempfile
        frames = [build_aaf_frame(seq=i) for i in range(3)]
        blob = bytearray(_s.pack("<IHHiIII", 0xA1B2C3D4, 2, 4, 0, 0,
                                 65535, 1))
        for i, fr in enumerate(frames):
            rec = b"\x00" * 28 + fr + b"\xde\xad\xbe\xef"
            blob += _s.pack("<IIII", i, 0, len(rec), len(rec)) + rec
        fd, name = tempfile.mkstemp(suffix=".pcap")
        path = Path(name)
        try:
            os.write(fd, bytes(blob))
            os.close(fd)
            w = WireTruth().feed_capture(
                read_capture(path, tap_header=28, strip_fcs=True))
            self.assertEqual(w.check_capture_shape()[0].verdict, "PASS")
            # and the same capture read WITHOUT the offset decodes to nothing
            w = WireTruth().feed_capture(
                read_capture(path, tap_header=0, strip_fcs=False))
            self.assertEqual(w.check_capture_shape()[0].verdict, "FAIL")
            # the EtherType offset the BPF filter must use
            rec = b"\x00" * 28 + frames[0]
            self.assertEqual(rec[40:42], _s.pack(">H", TPID_C_TAG))
            self.assertEqual(rec[28:34], frames[0][0:6])
        finally:
            path.unlink(missing_ok=True)


    def test_pcap_round_trip_with_tap_header_and_fcs(self) -> None:
        """A tap-shaped pcap survives read_capture frame-for-frame, timestamps
        included - and reading the same file WITHOUT the offset must not read
        as clean, because a wrong offset decodes to nothing, not to an error."""
        import tempfile, os
        frames = [build_aaf_frame(seq=i) for i in range(3)]
        blob = bytearray(struct.pack("<IHHiIII", 0xa1b2c3d4, 2, 4, 0, 0,
                                     65535, 1))
        for i, fr in enumerate(frames):
            rec = b"\x00" * 28 + fr + b"\xde\xad\xbe\xef"   # tap + FCS
            blob += struct.pack("<IIII", 100 + i, 0, len(rec), len(rec))
            blob += rec
        fd, name = tempfile.mkstemp(suffix=".pcap")
        path = Path(name)
        try:
            os.write(fd, bytes(blob))
            os.close(fd)
            recs = read_capture(path, tap_header=28, strip_fcs=True)
            self.assertEqual([r[1] for r in recs], frames)
            self.assertEqual(recs[1][0], 101.0)
            wt = WireTruth().feed_capture(recs)
            self.assertEqual(wt.check_capture_shape()[0].verdict, "PASS")
            # WITHOUT the tap offset the same file must NOT read as clean
            wt = WireTruth().feed_capture(read_capture(path))
            self.assertEqual(wt.check_capture_shape()[0].verdict, "FAIL")
        finally:
            path.unlink(missing_ok=True)
