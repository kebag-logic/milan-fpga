# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
#
# Steps for wire_truth_avtp.feature.
#
# These steps call tb/tools/avtp_wire_truth.py - the SAME module the on-bench
# runner and the campaign use - and never a copy of its logic. Two
# implementations of one decode is how the decode stops being one decode, and
# the whole point of this feature is that the analyser which will judge a real
# capture is itself judged first, against byte vectors built from the figures.
#
# Frames are built with the module's own build_aaf_frame / build_crf_frame /
# build_adp_frame helpers, which are written from IEEE 1722-2016 Figure 26 /
# Figure 72 and IEEE 1722.1-2021 6.2 - not from our RTL. That is what keeps the
# oracle independent: our packetizer could be wrong and these would still be
# right.

import os
import struct
import sys
import tempfile

from behave import given, then, when

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, os.path.join(ROOT, "tb", "tools"))

import avtp_wire_truth as wt  # noqa: E402


def _wt(context):
    """The analyser instance for this scenario, created on first use so a
    Given that sets an expectation can run before the frames are fed."""
    if getattr(context, "wt_obj", None) is None:
        context.wt_obj = wt.WireTruth(context.wt_expect)
        for ts, raw in context.wt_pending:
            context.wt_obj.feed(ts, raw)
        context.wt_pending = []
    return context.wt_obj


def _feed(context, raw, ts=0.0):
    context.wt_pending.append((ts, raw))
    context.wt_obj = None            # expectations may still change


def _reset(context):
    context.wt_expect = wt.Expectation()
    context.wt_pending = []
    context.wt_obj = None
    context.wt_verdicts = []


@given("the wire-truth analyser is importable")
def step_wt_import(context):
    assert hasattr(wt, "WireTruth"), "avtp_wire_truth.WireTruth missing"
    _reset(context)


# ------------------------------------------------------------ frame builders --
@given("a hand-built AAF frame with {ch:d} channels sequence {seq:d} "
       "timestamp {ts}")
def step_wt_aaf(context, ch, seq, ts):
    context.wt_frame = wt.build_aaf_frame(channels=ch, seq=seq,
                                          ts=int(str(ts), 0),
                                          sample_frames=6 if ch <= 8 else 1)
    _feed(context, context.wt_frame)


@given("a hand-built AAF frame that is illegal because {why}")
def step_wt_aaf_illegal(context, why):
    kw = {"channels_per_frame is zero": dict(channels=0, sample_frames=0),
          "bit_depth is zero": dict(bit_depth=0),
          "bit_depth exceeds the format": dict(fmt=0x4, bit_depth=32)}[why]
    _feed(context, wt.build_aaf_frame(**kw))


@given("a hand-built AAF frame tagged with VID {vid:d}")
def step_wt_aaf_vid(context, vid):
    _feed(context, wt.build_aaf_frame(vid=vid))


@given("a hand-built silent AAF frame on stream {sid}")
def step_wt_aaf_silent(context, sid):
    _feed(context, wt.build_aaf_frame(sid=int(str(sid), 0)))


@given("hand-built AAF frames with sequence numbers {seqs}")
def step_wt_aaf_seqs(context, seqs):
    _reset(context)
    for i, s in enumerate(int(x) for x in seqs.split(",")):
        _feed(context, wt.build_aaf_frame(seq=s), ts=i * 0.000125)


@given("hand-built AAF frames whose timestamps step by {step:d} ns")
def step_wt_aaf_ts_step(context, step):
    _reset(context)
    for i in range(5):
        _feed(context, wt.build_aaf_frame(seq=i, ts=i * step),
              ts=i * step / 1e9)


@given("a gPTP reference of {ns:d} ns")
def step_wt_gptp_ref(context, ns):
    _reset(context)
    context.wt_expect = wt.Expectation(gptp_ref_ns=ns)


@given("a hand-built AAF frame presented {ahead:d} ns after the reference")
def step_wt_aaf_ahead(context, ahead):
    ref = context.wt_expect.gptp_ref_ns
    _feed(context, wt.build_aaf_frame(ts=ref + ahead))


@given("a hand-built CRF frame")
def step_wt_crf(context):
    _feed(context, wt.build_crf_frame())


@given("a hand-built untagged CRF frame")
def step_wt_crf_untagged(context):
    _feed(context, wt.build_crf_frame(tagged=False))


@given("a hand-built CRF frame with timestamp interval {iv:d}")
def step_wt_crf_interval(context, iv):
    _reset(context)
    _feed(context, wt.build_crf_frame(interval=iv))


@given("hand-built CRF frames with sequence numbers {seqs}")
def step_wt_crf_seqs(context, seqs):
    _reset(context)
    for i, s in enumerate(int(x) for x in seqs.split(",")):
        _feed(context, wt.build_crf_frame(seq=s), ts=i * 0.002)


@given("{n:d} hand-built CRF frames at {ms:d} ms spacing")
def step_wt_crf_train(context, n, ms):
    _reset(context)
    for i in range(n):
        _feed(context, wt.build_crf_frame(seq=i & 0xFF,
                                          ts=i * ms * 1_000_000),
              ts=i * ms / 1000.0)


@given("a hand-built ADPDU with available_index {ai:d}")
def step_wt_adp(context, ai):
    _feed(context, wt.build_adp_frame(available_index=ai))


@given("hand-built ADPDUs with available indices {idxs}")
def step_wt_adps(context, idxs):
    _reset(context)
    for i, a in enumerate(int(x) for x in idxs.split(",")):
        _feed(context, wt.build_adp_frame(available_index=a), ts=i * 2.0)


@given("a hand-built ADPDU that claims control_data_length {cdl:d}")
def step_wt_adp_liar(context, cdl):
    _reset(context)
    _feed(context, wt.build_adp_frame(cdl=cdl))


@given('the controller was told the format is "{fmt}"')
def step_wt_declared(context, fmt):
    _reset(context)
    context.wt_expect = wt.Expectation(aaf_format=int(fmt, 16))


@given("stream {sid} is declared bound but unfed")
def step_wt_silent_stream(context, sid):
    _reset(context)
    context.wt_expect = wt.Expectation(
        silent_stream_ids=(int(str(sid), 0),))


@given("stream {sid} is declared fed")
def step_wt_fed_stream(context, sid):
    _reset(context)
    context.wt_expect = wt.Expectation(fed_stream_ids=(int(str(sid), 0),))


# ---------------------------------------------------------------- pcap on disk --
@given("a written pcap of {n:d} tap records with a {hdr:d} octet header and "
       "an FCS")
def step_wt_pcap(context, n, hdr):
    _reset(context)
    blob = bytearray(struct.pack("<IHHiIII", 0xA1B2C3D4, 2, 4, 0, 0, 65535, 1))
    for i in range(n):
        rec = b"\x00" * hdr + wt.build_aaf_frame(seq=i) + b"\xde\xad\xbe\xef"
        blob += struct.pack("<IIII", 100 + i, 0, len(rec), len(rec)) + rec
    fd, path = tempfile.mkstemp(suffix=".pcap")
    os.write(fd, bytes(blob))
    os.close(fd)
    context.wt_pcap = path
    context.wt_tap_header = hdr
    # the scenario writes a real file; behave tears it down so a suite run
    # leaves nothing in the temp directory
    context.add_cleanup(lambda: os.path.exists(path) and os.unlink(path))


@when("the analyser reads it with the tap offset")
def step_wt_read_tap(context):
    recs = wt.read_capture(context.wt_pcap, tap_header=context.wt_tap_header,
                           strip_fcs=True)
    context.wt_obj = wt.WireTruth(context.wt_expect).feed_capture(recs)
    context.wt_verdicts = context.wt_obj.check_capture_shape()


@when("the analyser reads it without the tap offset")
def step_wt_read_notap(context):
    recs = wt.read_capture(context.wt_pcap)
    context.wt_obj = wt.WireTruth(context.wt_expect).feed_capture(recs)
    context.wt_verdicts = context.wt_obj.check_capture_shape()


# -------------------------------------------------------------- decoder reads --
def _aaf(context):
    p = wt.decode_aaf(wt.decode_eth(context.wt_frame).payload)
    assert p is not None, "the hand-built frame did not decode as AAF PCM"
    return p


@then("the analyser reads channels_per_frame {n:d}")
def step_wt_read_cpf(context, n):
    assert _aaf(context).channels_per_frame == n, \
        f"decoded {_aaf(context).channels_per_frame}, expected {n}"


@then("the analyser reads sequence_num {n:d}")
def step_wt_read_seq(context, n):
    assert _aaf(context).sequence_num == n


@then("the analyser reads avtp_timestamp {ts}")
def step_wt_read_ts(context, ts):
    assert _aaf(context).avtp_timestamp == int(str(ts), 0)


@then("the analyser reads bit_depth {bd:d} and nsr {nsr:d} and format {f:d}")
def step_wt_read_fields(context, bd, nsr, f):
    p = _aaf(context)
    assert (p.bit_depth, p.nsr, p.fmt) == (bd, nsr, f), \
        f"decoded {(p.bit_depth, p.nsr, p.fmt)}"


@then("the analyser reads {n:d} sample events in the payload")
def step_wt_read_spf(context, n):
    assert _aaf(context).sample_frames == n, \
        f"decoded {_aaf(context).sample_frames} sample events"


@then("the analyser classifies the frame as {name}")
def step_wt_classify(context, name):
    st = wt.decode_eth(context.wt_frame).subtype \
        if getattr(context, "wt_frame", None) else \
        wt.decode_eth(context.wt_pending[-1][1]).subtype
    assert wt.SUBTYPE_NAMES.get(st) == name, \
        f"subtype {st:#04x} classified as {wt.SUBTYPE_NAMES.get(st)}"


@then("the analyser counts {n:d} ADPDU")
@then("the analyser counts {n:d} ADPDUs")
def step_wt_count_adp(context, n):
    got = sum(len(v) for v in _wt(context).adp.values())
    assert got == n, f"{got} ADPDUs decoded, expected {n}"


@then('stream_format "{fmt}" declares {n:d} channels')
def step_wt_fmt_channels(context, fmt, n):
    d = wt.parse_aaf_stream_format(fmt)
    assert d is not None and d.channels_per_frame == n, \
        f"{fmt} decodes to {d and d.channels_per_frame} channels"


@then('stream_format "{fmt}" has the up-to bit set')
def step_wt_fmt_ut(context, fmt):
    assert wt.parse_aaf_stream_format(fmt).ut == 1


@then('stream_format "{fmt}" declares {n:d} samples per frame')
def step_wt_fmt_spf(context, fmt, n):
    assert wt.parse_aaf_stream_format(fmt).samples_per_frame == n


@then("the Milan CRF stream format is {qw}")
def step_wt_crf_const(context, qw):
    assert wt.MILAN_CRF_FORMAT == int(str(qw), 0), \
        f"{wt.MILAN_CRF_FORMAT:#018x} is not the Milan Table 7.1 constant"


@then("it decodes to type {t:d} interval {iv:d} timestamps {n:d} pull {p:d} "
      "base {b:d}")
def step_wt_crf_const_fields(context, t, iv, n, p, b):
    d = wt.parse_crf_stream_format(wt.MILAN_CRF_FORMAT)
    assert (d.type, d.timestamp_interval, d.timestamps_per_pdu, d.pull,
            d.base_frequency) == (t, iv, n, p, b), \
        f"decoded {d}"


# ------------------------------------------------------------------- checks --
@when("the analyser checks the declared format against the wire")
def step_wt_check_fmt(context):
    context.wt_verdicts = _wt(context).check_aaf_declared_vs_wire()


@when("the analyser checks header legality")
def step_wt_check_hdr(context):
    context.wt_verdicts = _wt(context).check_aaf_header_legality()


@when("the analyser checks sequence continuity")
def step_wt_check_seq(context):
    context.wt_verdicts = _wt(context).check_sequence_continuity()


@when("the analyser checks the presentation timestamps")
def step_wt_check_ts(context):
    context.wt_verdicts = _wt(context).check_aaf_timestamps()


@when("the analyser checks the VLAN class")
def step_wt_check_vlan(context):
    context.wt_verdicts = _wt(context).check_vlan_class()


@when("the analyser checks zero fill")
def step_wt_check_zf(context):
    context.wt_verdicts = _wt(context).check_zero_fill()


@when("the analyser checks the CRF format and rate")
def step_wt_check_crf(context):
    context.wt_verdicts = (_wt(context).check_crf_format()
                           + _wt(context).check_crf_rate())


@when("the analyser checks the ADP frame rule")
def step_wt_check_adp(context):
    context.wt_verdicts = _wt(context).check_adp_frame_rule()


@when("the analyser checks control length honesty")
def step_wt_check_cdl(context):
    context.wt_verdicts = _wt(context).check_control_length_honesty()


@when("the analyser checks the capture shape")
def step_wt_check_shape(context):
    context.wt_verdicts = _wt(context).check_capture_shape()


# ------------------------------------------------------------------ verdicts --
def _matching(context, needle):
    hits = [v for v in context.wt_verdicts if needle in v.check]
    assert hits, (f"no verdict matching {needle!r}; got "
                  f"{[v.check for v in context.wt_verdicts]}")
    return hits


@then('the analyser reports {want} on "{needle}"')
def step_wt_verdict(context, want, needle):
    hits = _matching(context, needle)
    got = {v.verdict for v in hits}
    assert want in got, (f"{needle}: verdicts {sorted(got)}, expected {want}; "
                         f"details {[v.detail for v in hits]}")
    context.wt_hit = [v for v in hits if v.verdict == want][0]


@then("every declared-vs-wire verdict is PASS")
@then("every sequence verdict is PASS")
@then("every VLAN verdict is PASS")
@then("every zero-fill verdict is PASS")
@then("every CRF format verdict is PASS")
@then("every ADP verdict is PASS")
def step_wt_all_pass(context):
    # A vacuous "all of nothing passed" is exactly the failure methodology R2
    # names: if the frames did not decode at all, the check list is empty and
    # an unguarded all() would report success. That is how a masked subtype
    # byte made the ADP checks pass by never running.
    assert context.wt_verdicts, (
        "no verdicts were produced - the frames did not decode, so this "
        "scenario would have passed without checking anything")
    # A SKIP naming an ABSENT family is not a failure of the family under test:
    # an AAF-only fixture legitimately produces one CRF SKIP (and vice versa),
    # and that SKIP is the empty-collection rule working, not a defect. What is
    # still refused is a scenario in which NOTHING ran at all.
    ran = [v for v in context.wt_verdicts if v.verdict != "SKIP"]
    assert ran, (
        "every verdict was a SKIP, so nothing was actually checked: "
        f"{[(v.check, v.detail.get('absent')) for v in context.wt_verdicts]}")
    bad = [v for v in ran if v.verdict != "PASS"]
    assert not bad, f"not PASS: {[(v.check, v.verdict, v.detail) for v in bad]}"


@then("the mismatch names channels_per_frame")
def step_wt_mismatch_cpf(context):
    assert "channels_per_frame" in context.wt_hit.detail["mismatches"], \
        context.wt_hit.detail


@then('the violation mentions "{needle}"')
def step_wt_violation(context, needle):
    vs = context.wt_hit.detail["violations"]
    assert any(needle in v for v in vs), f"{needle!r} not in {vs}"


@then("the gap count is {n:d}")
def step_wt_gapcount(context, n):
    assert context.wt_hit.detail["gap_count"] == n, context.wt_hit.detail


@then("the expected step is {n:d} ns")
def step_wt_expected_step(context, n):
    assert context.wt_hit.detail["expected_step_ns"] == n, context.wt_hit.detail


@then('the skip reason mentions "{needle}"')
def step_wt_skip_reason(context, needle):
    why = context.wt_hit.detail.get("why", "")
    assert needle in why, f"{needle!r} not in {why!r}"


@then("the verdict records that VID zero was seen")
def step_wt_vid0(context):
    assert context.wt_hit.detail["vid_zero_seen"] is True, context.wt_hit.detail


@then("the expected CRF rate is {pps:d} PDUs per second")
def step_wt_crf_pps(context, pps):
    hit = [v for v in context.wt_verdicts if "pdu-rate" in v.check][0]
    assert abs(hit.detail["expected_pps"] - pps) < 0.5, hit.detail


@then("the built ADPDU frame is {n:d} octets")
def step_wt_adp_len(context, n):
    assert len(wt.build_adp_frame()) == n, len(wt.build_adp_frame())
    assert wt.ADP_FRAME_LEN == n


@then("the liar's declared control_data_length is {n:d}")
def step_wt_liar_cdl(context, n):
    assert context.wt_hit.detail["liars"][0]["cdl"] == n, context.wt_hit.detail


# --------------------------------------- the empty-collection rule, end to end --
@when("the analyser checks an empty capture end to end")
def step_wt_empty_all(context):
    context.wt_verdicts = wt.WireTruth(wt.Expectation()).checks()


@then("no check verdict is PASS")
def step_wt_no_pass(context):
    passing = [v.check for v in context.wt_verdicts if v.verdict == "PASS"]
    assert not passing, (
        f"{passing} PASSED on an empty capture - an empty collection is not "
        f"evidence of health, and `not []` being True is how "
        f"wt.control.length-honest used to pass with no control frames at all")


#: Every check family the analyser owes.  Listed by NAME here on purpose: a
#: family that silently stops emitting is otherwise indistinguishable in the log
#: from a family that passed.
WT_FAMILIES = (
    "wt.capture.stream-frames-present", "wt.aaf.declared-vs-wire",
    "wt.aaf.header-legal", "wt.aaf.payload-arithmetic",
    "wt.aaf.seq-continuity", "wt.crf.seq-continuity", "wt.aaf.tv-set",
    "wt.aaf.pts-step", "wt.aaf.class-a-transit", "wt.aaf.c-tag-present",
    "wt.aaf.c-tag-pcp", "wt.aaf.c-tag-dei", "wt.aaf.c-tag-vid",
    "wt.crf.c-tag-present", "wt.crf.c-tag-pcp", "wt.crf.c-tag-dei",
    "wt.crf.c-tag-vid", "wt.aaf.zero-fill", "wt.crf.milan-format",
    "wt.crf.pdu-rate", "wt.crf.timestamp-step", "wt.adp.frame-82",
    "wt.adp.available-index-advances", "wt.control.length-honest",
    "wt.msrp.talker-advertise-declared",
    "wt.msrp.listener-declaration-present",
    "wt.msrp.declared-dmac-matches-wire", "wt.msrp.declared-vid-matches-wire",
    "wt.msrp.tspec-declared", "wt.msrp.domain-declared",
    "wt.mvrp.sr-vid-declared")


@then("every check family is represented")
def step_wt_families(context):
    got = {v.check for v in context.wt_verdicts}
    missing = [f for f in WT_FAMILIES if f not in got]
    assert not missing, (
        f"{missing} emitted NOTHING, so the log cannot tell 'did not apply' "
        f"from 'was not run'")


@then("every SKIP names what was absent")
def step_wt_skips_named(context):
    bad = [v.check for v in context.wt_verdicts
           if v.verdict == "SKIP" and not v.detail.get("why")]
    assert not bad, bad


@then("the capture-shape verdict is FAIL")
def step_wt_shape_fail(context):
    hits = [v for v in context.wt_verdicts
            if v.check == "wt.capture.stream-frames-present"]
    assert hits and hits[0].verdict == "FAIL", hits


# ---------------------------------------------------------------- SRP / MRP --
@given("a hand-built MSRP Talker Advertise for stream {sid}")
def step_wt_msrp_ta(context, sid):
    frame = wt.build_msrp_frame(attrs=[(
        wt.MSRP_TALKER_ADVERTISE,
        wt.msrp_talker_advertise_value(stream_id=int(sid, 16),
                                       dmac="91e0f000fe07", vid=2,
                                       max_frame=1024, max_interval=1),
        [1], [])])
    context.wt_frame = frame


@given("a hand-built MSRP Listener Ready for stream {sid}")
def step_wt_msrp_lr(context, sid):
    context.wt_frame = wt.build_msrp_frame(attrs=[(
        wt.MSRP_LISTENER, wt.msrp_listener_value(int(sid, 16)), [1], [2])])


@when("the analyser decodes the MRPDU")
def step_wt_mrp_decode(context):
    eth = wt.decode_eth(context.wt_frame)
    proto = "MSRP" if eth.ethertype == wt.ETH_P_MSRP else "MVRP"
    context.wt_attrs = wt.decode_mrpdu(eth.payload, proto)
    assert context.wt_attrs, "the MRPDU decoded to no attributes at all"
    context.wt_attr = context.wt_attrs[0]


@then("the attribute is a Talker Advertise")
def step_wt_attr_ta(context):
    assert context.wt_attr.attr_name == "Talker Advertise", context.wt_attr


@then("the declared destination address is {mac}")
def step_wt_attr_dmac(context, mac):
    assert context.wt_attr.fields["destination_address"] == mac, \
        context.wt_attr.fields


@then("the declared vlan identifier is {vid:d}")
def step_wt_attr_vid(context, vid):
    assert context.wt_attr.fields["vlan_identifier"] == vid, \
        context.wt_attr.fields


@then("the declared MaxFrameSize is {n:d}")
def step_wt_attr_mfs(context, n):
    assert context.wt_attr.fields["max_frame_size"] == n, context.wt_attr.fields


@then("the attribute is declaring")
def step_wt_attr_declaring(context):
    assert context.wt_attr.declaring, context.wt_attr.event


@then('the listener declaration is "{decl}"')
def step_wt_attr_decl(context, decl):
    assert context.wt_attr.fields.get("declaration") == decl, \
        context.wt_attr.fields


@given("the entity declares {n:d} talker stream ids from {base}")
def step_wt_srp_expect(context, n, base):
    b = int(base, 16)
    context.wt_expect_streams = tuple(b + i for i in range(n))
    context.wt = wt.WireTruth(wt.Expectation(
        talker_stream_ids=context.wt_expect_streams))


@given("only stream {a} and {b} advertise")
def step_wt_srp_two(context, a, b):
    for sid in (int(a, 16), int(b, 16)):
        context.wt.feed(0.0, wt.build_msrp_frame(attrs=[(
            wt.MSRP_TALKER_ADVERTISE,
            wt.msrp_talker_advertise_value(stream_id=sid), [1], [])]))


@given('a stream on the wire whose only Listener declaration is "{decl}"')
def step_wt_srp_asking_failed(context, decl):
    code = {v: k for k, v in wt.MSRP_LISTENER_DECL.items()}[decl]
    sid = 0x0200000000020000
    context.wt = wt.WireTruth(wt.Expectation(talker_stream_ids=(sid,)))
    context.wt.feed(0.0, wt.build_aaf_frame(sid=sid, dmac="91e0f000fe01"))
    context.wt.feed(0.1, wt.build_msrp_frame(attrs=[
        (wt.MSRP_TALKER_ADVERTISE,
         wt.msrp_talker_advertise_value(stream_id=sid, dmac="91e0f000fe01"),
         [1], []),
        (wt.MSRP_LISTENER, wt.msrp_listener_value(sid), [1], [code])]))


@given("a stream whose wire {parameter} differs from its declaration")
def step_wt_srp_mismatch(context, parameter):
    sid = 0x0200000000020000
    context.wt = wt.WireTruth(wt.Expectation(talker_stream_ids=(sid,)))
    if parameter == "dmac":
        context.wt.feed(0.0, wt.build_aaf_frame(sid=sid, dmac="91e0f000fe09",
                                                vid=2))
    else:
        context.wt.feed(0.0, wt.build_aaf_frame(sid=sid, dmac="91e0f000fe01",
                                                vid=5))
    context.wt.feed(0.1, wt.build_msrp_frame(attrs=[(
        wt.MSRP_TALKER_ADVERTISE,
        wt.msrp_talker_advertise_value(stream_id=sid, dmac="91e0f000fe01",
                                       vid=2), [1], [])]))


@given("a stream on the wire with no MRP frames captured at all")
def step_wt_srp_no_mrp(context):
    context.wt = wt.WireTruth(wt.Expectation())
    context.wt.feed(0.0, wt.build_aaf_frame())


@when("the analyser checks the SRP declarations")
def step_wt_srp_check(context):
    context.wt_verdicts = context.wt.check_srp_declarations()


@then("the missing declarations are named")
def step_wt_srp_missing(context):
    hit = [v for v in context.wt_verdicts
           if v.check == "wt.msrp.talker-advertise-declared"][0]
    assert hit.detail["missing"], hit.detail


@then("every SRP verdict is SKIP")
def step_wt_srp_all_skip(context):
    bad = [(v.check, v.verdict) for v in context.wt_verdicts
           if v.verdict != "SKIP"]
    assert context.wt_verdicts and not bad, bad


@then("the SRP skip says an inline tap is required")
def step_wt_srp_needs_tap(context):
    txt = " ".join(v.clause + " " + str(v.detail)
                   for v in context.wt_verdicts).upper()
    assert "INLINE TAP" in txt, txt[:300]
