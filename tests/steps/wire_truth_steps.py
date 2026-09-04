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

from __future__ import annotations

import os
import struct
import sys
import tempfile
from pathlib import Path
from typing import TYPE_CHECKING

from behave import given, then, when

# The step signatures below name behave's own Context. It is imported for
# TYPE_CHECKING only, and the __future__ import above leaves every annotation
# unevaluated, so a behave release that moves that class cannot turn a type
# name into an ImportError in the middle of a suite run.
if TYPE_CHECKING:
    from behave.runner import Context

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "tb" / "tools"))

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
def step_wt_import(context: Context) -> None:
    """The analyser has to be there before any scenario can claim to have
    checked a frame: a missing WireTruth is a broken harness, not a clean
    capture."""
    assert hasattr(wt, "WireTruth"), "avtp_wire_truth.WireTruth missing"
    _reset(context)


# ------------------------------------------------------------ frame builders --
@given("a hand-built AAF frame with {ch:d} channels sequence {seq:d} "
       "timestamp {ts}")
def step_wt_aaf(context: Context, ch: int, seq: int, ts: str) -> None:
    """One Figure 26 AAF PCM AVTPDU built from the clause, not from our
    packetizer; above eight channels the sample count drops to one so the
    payload still fits a frame."""
    context.wt_frame = wt.build_aaf_frame(channels=ch, seq=seq,
                                          ts=int(str(ts), 0),
                                          sample_frames=6 if ch <= 8 else 1)
    _feed(context, context.wt_frame)


@given("a hand-built AAF frame that is illegal because {why}")
def step_wt_aaf_illegal(context: Context, why: str) -> None:
    """One deliberately illegal AAF header - 7.3.3's zero channels_per_frame,
    or 7.3.4's zero or over-wide bit_depth - so the analyser is shown
    saying NO."""
    kw = {"channels_per_frame is zero": dict(channels=0, sample_frames=0),
          "bit_depth is zero": dict(bit_depth=0),
          "bit_depth exceeds the format": dict(fmt=0x4, bit_depth=32)}[why]
    _feed(context, wt.build_aaf_frame(**kw))


@given("a hand-built AAF frame tagged with VID {vid:d}")
def step_wt_aaf_vid(context: Context, vid: int) -> None:
    """An AAF frame carrying an explicit C-Tag VID; VID 0 leaves the reserved
    SR tree and is a distinct defect from carrying the wrong one."""
    _feed(context, wt.build_aaf_frame(vid=vid))


@given("a hand-built silent AAF frame on stream {sid}")
def step_wt_aaf_silent(context: Context, sid: str) -> None:
    """An all-zero AAF frame on a named stream: what Milan 5.3.7.3 obliges an
    unfed bound talker to keep sending, and what a fed one must not send."""
    _feed(context, wt.build_aaf_frame(sid=int(str(sid), 0)))


@given("hand-built AAF frames with sequence numbers {seqs}")
def step_wt_aaf_seqs(context: Context, seqs: str) -> None:
    """A run of AAF frames with the listed sequence_num values, 125 us apart.
    The list is written to include the 255 -> 0 wrap, which is not a gap."""
    _reset(context)
    for i, s in enumerate(int(x) for x in seqs.split(",")):
        _feed(context, wt.build_aaf_frame(seq=s), ts=i * 0.000125)


@given("hand-built AAF frames whose timestamps step by {step:d} ns")
def step_wt_aaf_ts_step(context: Context, step: int) -> None:
    """Five AAF frames whose avtp_timestamp advances by a fixed step, so the
    one-AVTPDU-of-media expectation the analyser derives can be met or
    missed."""
    _reset(context)
    for i in range(5):
        _feed(context, wt.build_aaf_frame(seq=i, ts=i * step),
              ts=i * step / 1e9)


@given("a gPTP reference of {ns:d} ns")
def step_wt_gptp_ref(context: Context, ns: int) -> None:
    """Supplies the gPTP now, which is the only thing that makes class-A
    transit measurable; without it the analyser owes a SKIP."""
    _reset(context)
    context.wt_expect = wt.Expectation(gptp_ref_ns=ns)


@given("a hand-built AAF frame presented {ahead:d} ns after the reference")
def step_wt_aaf_ahead(context: Context, ahead: int) -> None:
    """An AAF frame presented a chosen distance ahead of the gPTP reference,
    which places it inside or outside the 2 ms class-A window."""
    ref = context.wt_expect.gptp_ref_ns
    _feed(context, wt.build_aaf_frame(ts=ref + ahead))


@given("a hand-built CRF frame")
def step_wt_crf(context: Context) -> None:
    """A conformant Milan CRF Media Clock Stream frame - the second stream
    class the VLAN checks have to pass on, not just AAF."""
    _feed(context, wt.build_crf_frame())


@given("a hand-built untagged CRF frame")
def step_wt_crf_untagged(context: Context) -> None:
    """A CRF frame with no C-Tag at all. Milan 7.3.3 requires a Class A
    reservation to carry it, so the missing tag is the finding."""
    _feed(context, wt.build_crf_frame(tagged=False))


@given("a hand-built CRF frame with timestamp interval {iv:d}")
def step_wt_crf_interval(context: Context, iv: int) -> None:
    """A CRF frame whose timestamp_interval is not Milan 7.3.2's 96, so the
    format check is shown rejecting a plausible-looking media clock."""
    _reset(context)
    _feed(context, wt.build_crf_frame(interval=iv))


@given("hand-built CRF frames with sequence numbers {seqs}")
def step_wt_crf_seqs(context: Context, seqs: str) -> None:
    """CRF frames with the listed one-octet sequence_num values, 2 ms apart:
    10.4.6 wraps FF -> 00, which a 16-bit read scores as a gap of -255."""
    _reset(context)
    for i, s in enumerate(int(x) for x in seqs.split(",")):
        _feed(context, wt.build_crf_frame(seq=s), ts=i * 0.002)


@given("{n:d} hand-built CRF frames at {ms:d} ms spacing")
def step_wt_crf_train(context: Context, n: int, ms: int) -> None:
    """A CRF train at a chosen spacing, with the capture times and the CRF
    timestamps stepping together, so the PDU rate can be judged."""
    _reset(context)
    for i in range(n):
        _feed(context, wt.build_crf_frame(seq=i & 0xFF,
                                          ts=i * ms * 1_000_000),
              ts=i * ms / 1000.0)


@given("a hand-built ADPDU with available_index {ai:d}")
def step_wt_adp(context: Context, ai: int) -> None:
    """One ADPDU with a chosen available_index. Its subtype 0xFA is also the
    frame a decoder masking off the 1722-2011 cd bit turns into 0x7A."""
    _feed(context, wt.build_adp_frame(available_index=ai))


@given("hand-built ADPDUs with available indices {idxs}")
def step_wt_adps(context: Context, idxs: str) -> None:
    """A run of ADPDUs two seconds apart with the listed available_index
    values; a repeat is what makes a controller treat the entity as
    incoherent."""
    _reset(context)
    for i, a in enumerate(int(x) for x in idxs.split(",")):
        _feed(context, wt.build_adp_frame(available_index=a), ts=i * 2.0)


@given("a hand-built ADPDU that claims control_data_length {cdl:d}")
def step_wt_adp_liar(context: Context, cdl: int) -> None:
    """An ADPDU declaring a control_data_length it does not have, which is
    the defect a status-byte-only tool cannot see at all."""
    _reset(context)
    _feed(context, wt.build_adp_frame(cdl=cdl))


@given('the controller was told the format is "{fmt}"')
def step_wt_declared(context: Context, fmt: str) -> None:
    """The stream_format the controller was told, as an ATDECC hex qword -
    the declaration half of the declared-versus-wire comparison."""
    _reset(context)
    context.wt_expect = wt.Expectation(aaf_format=int(fmt, 16))


@given("stream {sid} is declared bound but unfed")
def step_wt_silent_stream(context: Context, sid: str) -> None:
    """Declares a stream bound but unfed, which Milan 5.3.7.3 obliges to keep
    sending SILENT FRAMES; sending nothing at all is the defect."""
    _reset(context)
    context.wt_expect = wt.Expectation(
        silent_stream_ids=(int(str(sid), 0),))


@given("stream {sid} is declared fed")
def step_wt_fed_stream(context: Context, sid: str) -> None:
    """Declares a stream fed, so an all-zero payload on it is the silence
    defect rather than the required silent fill."""
    _reset(context)
    context.wt_expect = wt.Expectation(fed_stream_ids=(int(str(sid), 0),))


# ---------------------------------------------------------------- pcap on disk --
@given("a written pcap of {n:d} tap records with a {hdr:d} octet header and "
       "an FCS")
def step_wt_pcap(context: Context, n: int, hdr: int) -> None:
    """Writes a real pcap of ProfiShark-shaped tap records: a per-record
    header plus the kept FCS, which only decode once the reader is told
    the offset."""
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
    context.add_cleanup(lambda: Path(path).unlink(missing_ok=True))


@when("the analyser reads it with the tap offset")
def step_wt_read_tap(context: Context) -> None:
    """Reads that capture with the tap offset applied, which is the only way
    the AVTP frames inside it are found at all."""
    recs = wt.read_capture(context.wt_pcap, tap_header=context.wt_tap_header,
                           strip_fcs=True)
    context.wt_obj = wt.WireTruth(context.wt_expect).feed_capture(recs)
    context.wt_verdicts = context.wt_obj.check_capture_shape()


@when("the analyser reads it without the tap offset")
def step_wt_read_notap(context: Context) -> None:
    """Reads the same capture without the offset, producing 'no frames' from
    a file known to be full - the shape every false green here has."""
    recs = wt.read_capture(context.wt_pcap)
    context.wt_obj = wt.WireTruth(context.wt_expect).feed_capture(recs)
    context.wt_verdicts = context.wt_obj.check_capture_shape()


# -------------------------------------------------------------- decoder reads --
def _aaf(context):
    p = wt.decode_aaf(wt.decode_eth(context.wt_frame).payload)
    assert p is not None, "the hand-built frame did not decode as AAF PCM"
    return p


@then("the analyser reads channels_per_frame {n:d}")
def step_wt_read_cpf(context: Context, n: int) -> None:
    """channels_per_frame is a ten-bit field split across two octets; a
    decoder that reads one octet passes every stereo test ever written."""
    assert _aaf(context).channels_per_frame == n, \
        f"decoded {_aaf(context).channels_per_frame}, expected {n}"


@then("the analyser reads sequence_num {n:d}")
def step_wt_read_seq(context: Context, n: int) -> None:
    """sequence_num read straight off Figure 26 - the field the continuity
    checks later count gaps in."""
    assert _aaf(context).sequence_num == n


@then("the analyser reads avtp_timestamp {ts}")
def step_wt_read_ts(context: Context, ts: str) -> None:
    """avtp_timestamp off Figure 26, written as a hex literal so the four
    octets stay legible in wire order."""
    assert _aaf(context).avtp_timestamp == int(str(ts), 0)


@then("the analyser reads bit_depth {bd:d} and nsr {nsr:d} and format {f:d}")
def step_wt_read_fields(context: Context, bd: int, nsr: int, f: int) -> None:
    """bit_depth, nsr and format together: 7.3.4's legality rule is about the
    pair, so a decoder that reads them independently cannot enforce it."""
    p = _aaf(context)
    assert (p.bit_depth, p.nsr, p.fmt) == (bd, nsr, f), \
        f"decoded {(p.bit_depth, p.nsr, p.fmt)}"


@then("the analyser reads {n:d} sample events in the payload")
def step_wt_read_spf(context: Context, n: int) -> None:
    """The sample events the payload actually carries, derived from its
    length - the arithmetic that catches a header and payload disagreeing."""
    assert _aaf(context).sample_frames == n, \
        f"decoded {_aaf(context).sample_frames} sample events"


@then("the analyser classifies the frame as {name}")
def step_wt_classify(context: Context, name: str) -> None:
    """4.4.3.2 calls subtype 'The 1-octet subtype field'. Masking its top bit
    turns ADP (0xFA) into 0x7A and the ADP checks then silently never run."""
    st = wt.decode_eth(context.wt_frame).subtype \
        if getattr(context, "wt_frame", None) else \
        wt.decode_eth(context.wt_pending[-1][1]).subtype
    assert wt.SUBTYPE_NAMES.get(st) == name, \
        f"subtype {st:#04x} classified as {wt.SUBTYPE_NAMES.get(st)}"


@then("the analyser counts {n:d} ADPDU")
@then("the analyser counts {n:d} ADPDUs")
def step_wt_count_adp(context: Context, n: int) -> None:
    """How many ADPDUs survived classification - zero would mean the subtype
    was masked and every later ADP verdict was vacuous."""
    got = sum(len(v) for v in _wt(context).adp.values())
    assert got == n, f"{got} ADPDUs decoded, expected {n}"


@then('stream_format "{fmt}" declares {n:d} channels')
def step_wt_fmt_channels(context: Context, fmt: str, n: int) -> None:
    """An ATDECC stream_format qword decoded to its channel count, per Annex
    I.2.4.1 - the declared value the wire is later held against."""
    d = wt.parse_aaf_stream_format(fmt)
    assert d is not None and d.channels_per_frame == n, \
        f"{fmt} decodes to {d and d.channels_per_frame} channels"


@then('stream_format "{fmt}" has the up-to bit set')
def step_wt_fmt_ut(context: Context, fmt: str) -> None:
    """The up-to bit out of Annex I.2.4.1: it says the channel count is an
    upper bound rather than the count on the wire, so it must be surfaced
    and not folded into the count."""
    assert wt.parse_aaf_stream_format(fmt).ut == 1


@then('stream_format "{fmt}" declares {n:d} samples per frame')
def step_wt_fmt_spf(context: Context, fmt: str, n: int) -> None:
    """samples_per_frame out of the same qword; with channels_per_frame it is
    what makes an AAF payload length predictable."""
    assert wt.parse_aaf_stream_format(fmt).samples_per_frame == n


@then("the Milan CRF stream format is {qw}")
def step_wt_crf_const(context: Context, qw: str) -> None:
    """Milan v1.2 Table 7.1 pins the whole CRF stream format as one constant,
    so the analyser holds the constant instead of re-deriving it."""
    assert wt.MILAN_CRF_FORMAT == int(str(qw), 0), \
        f"{wt.MILAN_CRF_FORMAT:#018x} is not the Milan Table 7.1 constant"


@then("it decodes to type {t:d} interval {iv:d} timestamps {n:d} pull {p:d} "
      "base {b:d}")
def step_wt_crf_const_fields(context: Context, t: int, iv: int, n: int,
                             p: int, b: int) -> None:
    """That constant decoded field by field. It only comes out right with a
    29-bit base_frequency, which is how the field width was settled rather
    than guessed from the prose."""
    d = wt.parse_crf_stream_format(wt.MILAN_CRF_FORMAT)
    assert (d.type, d.timestamp_interval, d.timestamps_per_pdu, d.pull,
            d.base_frequency) == (t, iv, n, p, b), \
        f"decoded {d}"


# ------------------------------------------------------------------- checks --
@when("the analyser checks the declared format against the wire")
def step_wt_check_fmt(context: Context) -> None:
    """Runs the declared-versus-wire comparison - the one check in the tree
    whose oracle is the wire and not another declaration."""
    context.wt_verdicts = _wt(context).check_aaf_declared_vs_wire()


@when("the analyser checks header legality")
def step_wt_check_hdr(context: Context) -> None:
    """Runs the 7.3.3 / 7.3.4 header legality checks, which report an illegal
    field rather than rounding it into range."""
    context.wt_verdicts = _wt(context).check_aaf_header_legality()


@when("the analyser checks sequence continuity")
def step_wt_check_seq(context: Context) -> None:
    """Runs sequence continuity over both stream classes at once: AAF's
    16-bit counter and CRF's 8-bit one wrap in different places."""
    context.wt_verdicts = _wt(context).check_sequence_continuity()


@when("the analyser checks the presentation timestamps")
def step_wt_check_ts(context: Context) -> None:
    """Runs the presentation-time checks - the per-PDU step, and the class-A
    transit window that SKIPs when no gPTP reference was supplied."""
    context.wt_verdicts = _wt(context).check_aaf_timestamps()


@when("the analyser checks the VLAN class")
def step_wt_check_vlan(context: Context) -> None:
    """Runs the C-Tag checks (present, PCP, DEI, VID) on every stream class
    seen, because a CRF stream owes the same reservation as an AAF one."""
    context.wt_verdicts = _wt(context).check_vlan_class()


@when("the analyser checks zero fill")
def step_wt_check_zf(context: Context) -> None:
    """Runs the Milan 5.3.7.3 zero-fill checks: an unfed bound stream owes
    silent frames, and a fed one must not be silent."""
    context.wt_verdicts = _wt(context).check_zero_fill()


@when("the analyser checks the CRF format and rate")
def step_wt_check_crf(context: Context) -> None:
    """Runs the Milan 7.3.2 CRF format check together with the PDU rate that
    format implies, since the rate is only meaningful once it holds."""
    context.wt_verdicts = (_wt(context).check_crf_format()
                           + _wt(context).check_crf_rate())


@when("the analyser checks the ADP frame rule")
def step_wt_check_adp(context: Context) -> None:
    """Runs the 1722.1 6.2.1 ADP checks: the 82-octet frame, and the
    available_index that must advance on every advertisement."""
    context.wt_verdicts = _wt(context).check_adp_frame_rule()


@when("the analyser checks control length honesty")
def step_wt_check_cdl(context: Context) -> None:
    """Runs the control_data_length honesty check, which holds a frame's
    declared length against the octets it actually carries."""
    context.wt_verdicts = _wt(context).check_control_length_honesty()


@when("the analyser checks the capture shape")
def step_wt_check_shape(context: Context) -> None:
    """Runs the capture-shape check, which refuses to read an absence of
    stream frames as a clean capture."""
    context.wt_verdicts = _wt(context).check_capture_shape()


# ------------------------------------------------------------------ verdicts --
def _matching(context, needle):
    hits = [v for v in context.wt_verdicts if needle in v.check]
    assert hits, (f"no verdict matching {needle!r}; got "
                  f"{[v.check for v in context.wt_verdicts]}")
    return hits


@then('the analyser reports {want} on "{needle}"')
def step_wt_verdict(context: Context, want: str, needle: str) -> None:
    """Asserts the wanted verdict on the checks whose name contains the
    needle, and keeps the matching one for the detail steps that follow."""
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
def step_wt_all_pass(context: Context) -> None:
    """Every verdict that ran is PASS, with the two vacuity guards that stop
    an empty or all-SKIP verdict list from passing a scenario for free."""
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
def step_wt_mismatch_cpf(context: Context) -> None:
    """The declared-versus-wire failure names the field that differed, so the
    log does not leave a reader to re-derive which half was wrong."""
    assert "channels_per_frame" in context.wt_hit.detail["mismatches"], \
        context.wt_hit.detail


@then('the violation mentions "{needle}"')
def step_wt_violation(context: Context, needle: str) -> None:
    """The legality failure quotes the offending value and not just the field
    name, so the verdict is actionable without re-opening the capture."""
    vs = context.wt_hit.detail["violations"]
    assert any(needle in v for v in vs), f"{needle!r} not in {vs}"


@then("the gap count is {n:d}")
def step_wt_gapcount(context: Context, n: int) -> None:
    """How many discontinuities the sequence check counted - a wrap must not
    be one of them."""
    assert context.wt_hit.detail["gap_count"] == n, context.wt_hit.detail


@then("the expected step is {n:d} ns")
def step_wt_expected_step(context: Context, n: int) -> None:
    """The presentation-time step the analyser derived from the format, which
    is what keeps the check independent of what the frames happen to do."""
    assert context.wt_hit.detail["expected_step_ns"] == n, context.wt_hit.detail


@then('the skip reason mentions "{needle}"')
def step_wt_skip_reason(context: Context, needle: str) -> None:
    """A SKIP has to name what was missing; an unexplained SKIP reads in the
    log exactly like a check that passed."""
    why = context.wt_hit.detail.get("why", "")
    assert needle in why, f"{needle!r} not in {why!r}"


@then("the verdict records that VID zero was seen")
def step_wt_vid0(context: Context) -> None:
    """VID zero is recorded as its own fact in the verdict, so it is not
    filed under 'the wrong VID' when the two have different consequences."""
    assert context.wt_hit.detail["vid_zero_seen"] is True, context.wt_hit.detail


@then("the expected CRF rate is {pps:d} PDUs per second")
def step_wt_crf_pps(context: Context, pps: int) -> None:
    """The expected CRF rate comes from the stream format, so it is a
    prediction the capture is held to, not a measurement of the capture."""
    hit = [v for v in context.wt_verdicts if "pdu-rate" in v.check][0]
    assert abs(hit.detail["expected_pps"] - pps) < 0.5, hit.detail


@then("the built ADPDU frame is {n:d} octets")
def step_wt_adp_len(context: Context, n: int) -> None:
    """The built ADPDU is the clause's 82 octets and the module constant
    agrees with the builder - a fixture that drifts from the rule tests
    nothing."""
    assert len(wt.build_adp_frame()) == n, len(wt.build_adp_frame())
    assert wt.ADP_FRAME_LEN == n


@then("the liar's declared control_data_length is {n:d}")
def step_wt_liar_cdl(context: Context, n: int) -> None:
    """The verdict carries what the liar declared, which is the number an
    engineer needs to find the offending code path."""
    assert context.wt_hit.detail["liars"][0]["cdl"] == n, context.wt_hit.detail


# --------------------------------------- the empty-collection rule, end to end --
@when("the analyser checks an empty capture end to end")
def step_wt_empty_all(context: Context) -> None:
    """Runs every check family over a capture with nothing in it - this
    project's commonest false green."""
    context.wt_verdicts = wt.WireTruth(wt.Expectation()).checks()


@then("no check verdict is PASS")
def step_wt_no_pass(context: Context) -> None:
    """No check may report PASS on an empty capture, because an empty
    collection is not evidence of health."""
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
def step_wt_families(context: Context) -> None:
    """Every family in WT_FAMILIES is represented by name, because a family
    that silently stops emitting is invisible in the log."""
    got = {v.check for v in context.wt_verdicts}
    missing = [f for f in WT_FAMILIES if f not in got]
    assert not missing, (
        f"{missing} emitted NOTHING, so the log cannot tell 'did not apply' "
        f"from 'was not run'")


@then("every SKIP names what was absent")
def step_wt_skips_named(context: Context) -> None:
    """Every SKIP names what was absent, which is what keeps a SKIP from
    reading as a pass."""
    bad = [v.check for v in context.wt_verdicts
           if v.verdict == "SKIP" and not v.detail.get("why")]
    assert not bad, bad


@then("the capture-shape verdict is FAIL")
def step_wt_shape_fail(context: Context) -> None:
    """The capture-shape family specifically FAILs, rather than the scenario
    settling for some other check having failed instead."""
    hits = [v for v in context.wt_verdicts
            if v.check == "wt.capture.stream-frames-present"]
    assert hits and hits[0].verdict == "FAIL", hits


# ---------------------------------------------------------------- SRP / MRP --
@given("a hand-built MSRP Talker Advertise for stream {sid}")
def step_wt_msrp_ta(context: Context, sid: str) -> None:
    """A hand-built MSRP Talker Advertise: the 25-octet FirstValue of
    802.1Q-2018 35.2.2.8, built from the clause and not from our SRP
    stack."""
    frame = wt.build_msrp_frame(attrs=[(
        wt.MSRP_TALKER_ADVERTISE,
        wt.msrp_talker_advertise_value(stream_id=int(sid, 16),
                                       dmac="91e0f000fe07", vid=2,
                                       max_frame=1024, max_interval=1),
        [1], [])])
    context.wt_frame = frame


@given("a hand-built MSRP Listener Ready for stream {sid}")
def step_wt_msrp_lr(context: Context, sid: str) -> None:
    """A hand-built MSRP Listener Ready. 35.2.2.8.2 puts the declaration type
    in a separate FourPackedEvents vector, not in the 8-octet value."""
    context.wt_frame = wt.build_msrp_frame(attrs=[(
        wt.MSRP_LISTENER, wt.msrp_listener_value(int(sid, 16)), [1], [2])])


@when("the analyser decodes the MRPDU")
def step_wt_mrp_decode(context: Context) -> None:
    """Decodes the MRPDU, picking MSRP or MVRP off the ethertype, and keeps
    the first attribute for the field steps that follow."""
    eth = wt.decode_eth(context.wt_frame)
    proto = "MSRP" if eth.ethertype == wt.ETH_P_MSRP else "MVRP"
    context.wt_attrs = wt.decode_mrpdu(eth.payload, proto)
    assert context.wt_attrs, "the MRPDU decoded to no attributes at all"
    context.wt_attr = context.wt_attrs[0]


@then("the attribute is a Talker Advertise")
def step_wt_attr_ta(context: Context) -> None:
    """The attribute type is Talker Advertise, which is what every field step
    after it assumes."""
    assert context.wt_attr.attr_name == "Talker Advertise", context.wt_attr


@then("the declared destination address is {mac}")
def step_wt_attr_dmac(context: Context, mac: str) -> None:
    """The declared Stream Destination MAC out of DataFrameParameters - a
    Milan 5.3.7.4 SRP parameter, so it has to match the tag on the wire."""
    assert context.wt_attr.fields["destination_address"] == mac, \
        context.wt_attr.fields


@then("the declared vlan identifier is {vid:d}")
def step_wt_attr_vid(context: Context, vid: int) -> None:
    """The declared Stream VLAN ID, the other 5.3.7.4 SRP parameter the wire
    is later held against."""
    assert context.wt_attr.fields["vlan_identifier"] == vid, \
        context.wt_attr.fields


@then("the declared MaxFrameSize is {n:d}")
def step_wt_attr_mfs(context: Context, n: int) -> None:
    """MaxFrameSize out of the TSpec, which only lands if the 25-octet value
    was split at the clause's boundaries."""
    assert context.wt_attr.fields["max_frame_size"] == n, context.wt_attr.fields


@then("the attribute is declaring")
def step_wt_attr_declaring(context: Context) -> None:
    """The attribute is a declaration and not a withdrawal: the MRP event
    says so, and the value alone cannot tell the two apart."""
    assert context.wt_attr.declaring, context.wt_attr.event


@then('the listener declaration is "{decl}"')
def step_wt_attr_decl(context: Context, decl: str) -> None:
    """The Listener declaration type, which rides the FourPackedEvents
    vector; a decoder that reads only the value sees nothing here."""
    assert context.wt_attr.fields.get("declaration") == decl, \
        context.wt_attr.fields


@given("the entity declares {n:d} talker stream ids from {base}")
def step_wt_srp_expect(context: Context, n: int, base: str) -> None:
    """The entity's whole Stream Output set, which Milan 5.3.7.2 requires
    each of to declare - passing the set is what lets the capture answer
    which of them never did."""
    b = int(base, 16)
    context.wt_expect_streams = tuple(b + i for i in range(n))
    context.wt = wt.WireTruth(wt.Expectation(
        talker_stream_ids=context.wt_expect_streams))


@given("only stream {a} and {b} advertise")
def step_wt_srp_two(context: Context, a: str, b: str) -> None:
    """Only two of those stream ids actually advertise, reproducing the
    2-of-5 defect this check set found on the bench from the wire alone."""
    for sid in (int(a, 16), int(b, 16)):
        context.wt.feed(0.0, wt.build_msrp_frame(attrs=[(
            wt.MSRP_TALKER_ADVERTISE,
            wt.msrp_talker_advertise_value(stream_id=sid), [1], [])]))


@given('a stream on the wire whose only Listener declaration is "{decl}"')
def step_wt_srp_asking_failed(context: Context, decl: str) -> None:
    """A stream whose frames are on the wire while its only Listener
    declaration is one that licenses nothing - 5.3.7.3 wants Ready or
    Ready Failed."""
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
def step_wt_srp_mismatch(context: Context, parameter: str) -> None:
    """A stream riding a DMAC or a VID it never declared, which puts it
    outside its own reservation though every frame looks well formed."""
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
def step_wt_srp_no_mrp(context: Context) -> None:
    """Stream frames with no MRP frames at all - what a mirror port and the
    controller host always see, since a bridge does not forward MRP."""
    context.wt = wt.WireTruth(wt.Expectation())
    context.wt.feed(0.0, wt.build_aaf_frame())


@when("the analyser checks the SRP declarations")
def step_wt_srp_check(context: Context) -> None:
    """Runs the SRP declaration checks over whatever MRP the capture holds."""
    context.wt_verdicts = context.wt.check_srp_declarations()


@then("the missing declarations are named")
def step_wt_srp_missing(context: Context) -> None:
    """The failure names the stream ids that never declared, which is the
    list an engineer acts on."""
    hit = [v for v in context.wt_verdicts
           if v.check == "wt.msrp.talker-advertise-declared"][0]
    assert hit.detail["missing"], hit.detail


@then("every SRP verdict is SKIP")
def step_wt_srp_all_skip(context: Context) -> None:
    """Without MRP frames every SRP verdict is a SKIP, and there is at least
    one: silence from the family would be indistinguishable from a pass."""
    bad = [(v.check, v.verdict) for v in context.wt_verdicts
           if v.verdict != "SKIP"]
    assert context.wt_verdicts and not bad, bad


@then("the SRP skip says an inline tap is required")
def step_wt_srp_needs_tap(context: Context) -> None:
    """The SKIP says an inline tap is required, because the capture point is
    the reason the frames are absent, not a healthy fabric."""
    txt = " ".join(v.clause + " " + str(v.detail)
                   for v in context.wt_verdicts).upper()
    assert "INLINE TAP" in txt, txt[:300]
