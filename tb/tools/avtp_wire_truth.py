#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""avtp_wire_truth.py - decode AVTP off a capture and check the invariants that
declarations cannot see.

    # CLI over a ProfiShark inline tap (28-byte record header, FCS present)
    ./avtp_wire_truth.py capture.pcap --tap --expect-aaf-format 0205022001006000
    # every check as one JSON line per verdict, for a morning diff
    ./avtp_wire_truth.py capture.pcap --jsonl > verdicts.jsonl
    # the offline byte-vector self test (no capture, no hardware)
    ./avtp_wire_truth.py --self-test

WHY THIS EXISTS.  Every gate in this repo compares a DECLARATION against
another declaration.  The escape that started the whole accountability effort
(docs/testing/methodology.md, escape 1) was a talker advertising eight audio
channels while its framer emitted two: config, generated header, CSR and AEM
descriptor all agreed, and the only thing that disagreed was the wire.  This
module's oracle is THE WIRE plus THE CLAUSE - never our own model - so it can
fail against us.

LEVEL AND ORACLE (docs/testing/methodology.md §2).  L5 when it is handed a
capture from a tap (the wire, on hardware); L3 when it is handed hand-built
byte vectors from the standards, which is how its own decoders are tested.
It is structurally blind to anything that never reaches a frame: an internal
counter, a CSR, a controller's view.  Those are the matrix runner's job
(tb/tools/torture_campaign.py) and they are deliberately NOT duplicated here.

THE CLAUSES, quoted where a check depends on the exact words.

  IEEE 1722-2016 Figure 26 - the AAF PCM AVTPDU field layout used by
    decode_aaf(): subtype, sv/version/mr/tv, sequence_num, tu, stream_id,
    avtp_timestamp, format, nsr, channels_per_frame, bit_depth,
    stream_data_length, sp, evt.
  IEEE 1722-2016 Annex I.2.4/I.2.4.1 - the ATDECC AAF stream_format qword, and
    the sentence the declared-vs-actual check rests on: "This field matches the
    setting of the channels_per_frame field in the Stream AVTPDU when this
    stream format is the current format for the stream."  The same sentence is
    written for nsr, format and bit_depth.  That is what makes a mismatch a
    DEFECT rather than a difference of opinion.
  IEEE 1722-2016 7.3.3 - "The channels_per_frame field shall be set to the
    number of audio channels represented in the audio sample frame, a positive
    integer greater than zero (0)."
  IEEE 1722-2016 7.3.4 - "The bit_depth field ... shall not be set to a value
    of zero (0).  The value of bit_depth shall not be set to a number which is
    larger than the size of the format set in the format field."
  IEEE 1722-2016 7.3.5 - the PCM payload is a chronological sequence of sample
    frames, each carrying one sample per channel IN CHANNEL ORDER.  That is the
    whole basis of the per-channel identity decode.
  IEEE 1722-2016 4.4.4.6 - sequence_num "shall be incremented by one (1), with
    wrapping, on each subsequent" AVTPDU of the stream.
  IEEE 1722-2016 10.4.6 - the CRF sequence_num is ONE OCTET and wraps
    "from 11111111(2) to 00000000(2) (FF16 to 0016)".  A 16-bit reading of it
    is a silent bug, so the CRF decoder takes the octet.
  IEEE 1722-2016 Figure 72 / 10.4.x - the CRF AVTPDU layout: sv/mr/fs/tu,
    sequence_num, type, stream_id, pull, base_frequency, crf_data_length,
    timestamp_interval, crf_data.
  IEEE 1722-2016 Annex I.2.6 - the ATDECC CRF stream_format qword.  Its
    base_frequency width is the ONE field this file resolves from a known-good
    constant instead of the prose: Milan v1.2 Table 7.1 pins the CRF Media Clock
    Stream Format string at 0x041060010000BB80, which only decodes with a 29-bit
    base_frequency (0xBB80 = 48000), so that is the width used.
  Milan v1.2 7.3.2 - "The base frequency shall be 48000Hz.  Each PDU shall
    contain 1 timestamp, and the timestamp interval shall be 96."  48000/96 =
    500 PDU/s = one CRF PDU every 2 ms; that is where the expected rate comes
    from, not from measuring ourselves.
  Milan v1.2 7.3.3 - a Class A Stream Reservation "shall be used to
    transmit" a CRF Media Clock Stream.  So an UNTAGGED CRF
    frame is a finding, and this project has measured exactly that: 4001
    untagged CRF frames in 8 s on 2026-07-28.
  Milan v1.2 5.3.7.3 - "As long as a PAAD is declaring a Talker Advertise
    attribute and receiving a Listener Ready or Listener Ready Failed attribute
    for a Stream Output, it shall be streaming AVTP packets."  A bound talker
    with nothing to send therefore owes FRAMES, not silence - which is why
    "all-zero payload" is a PASS for a stream declared silent and a FAIL for
    one declared fed, and why the absence of frames is a FAIL for both.
  802.1Q-2018 9.5/9.6 - the C-TAG: TPID 0x8100 then TCI {PCP, DEI, VID}.
  IEEE 1722.1-2021 9.2.1.1.6 - control_data_length counts the octets after the
    field it follows; a frame shorter than that is malformed however correct
    its status byte is.  The frame that LIES about its length is a defect class
    this project has hit, so the control-plane check is length-first.

WHAT THIS FILE DELIBERATELY DOES NOT DO.
  * It does not judge presentation time against gPTP unless a gPTP reference is
    SUPPLIED (--gptp-ref-ns / gptp_ref_ns=).  A pcap timestamp is the capture
    host's CLOCK_REALTIME, not the gPTP timebase, and comparing the two
    produces a confident number that means nothing.  Without a reference the
    class-A transit check reports SKIP with that reason attached (methodology
    R5: a structural zero is not a measurement).
  * It does not reserve, bind, or read a counter.  It reads frames.

WHERE THE PARTS LIVE.  This file is the CLI and the name every consumer
imports - `import avtp_wire_truth as wt` still reaches every public name below
- and the analyser itself is four siblings beside it, so no one of them has to
be read whole to change one thing:

  * `avtp_wire_truth_wire.py`     the constants, the pcap reader, the decoders
  * `avtp_wire_truth_checks.py`   `WireTruth`, the invariants over a capture
  * `avtp_wire_truth_identity.py` the per-channel identity property
  * `avtp_wire_truth_frames.py`   the hand-built byte-vector oracle
  * `avtp_wire_truth_selftest.py` the offline arms behind `--self-test`
"""
from __future__ import annotations

import argparse
import json
import sys

# Re-exported so `import avtp_wire_truth as wt` reaches the whole
# analyser through the one name every consumer already imports.
# ruff: noqa: F401
from avtp_wire_truth_wire import (AAF_FORMAT_BITS, AAF_FORMAT_NAMES,
                                  ADP_AVTPDU_LEN, ADP_CDL, ADP_FRAME_LEN,
                                  AVTP_TS_MOD, AafPdu, AafStreamFormat,
                                  CLASS_A_MAX_TRANSIT_NS, CONTROL_SUBTYPES,
                                  CRF_TYPE_AUDIO_SAMPLE, ControlPdu, CrfPdu,
                                  CrfStreamFormat, ETH_P_AVTP, ETH_P_MSRP,
                                  ETH_P_MVRP, EthFrame, Expectation,
                                  MILAN_CRF_BASE_HZ, MILAN_CRF_FORMAT,
                                  MILAN_CRF_TS_INTERVAL, MILAN_CRF_TS_PER_PDU,
                                  MRP_ATTR_EVENT, MRP_DECLARING_EVENTS,
                                  MRP_GROUP_DMAC, MSRP_ATTR_LEN,
                                  MSRP_ATTR_NAMES, MSRP_DOMAIN, MSRP_LISTENER,
                                  MSRP_LISTENER_DECL, MSRP_TALKER_ADVERTISE,
                                  MSRP_TALKER_FAILED, MVRP_VID, MrpAttribute,
                                  NSR_HZ, SR_CLASS_A_PCP, SR_VID_DEFAULT,
                                  SUBTYPE_AAF, SUBTYPE_ACMP, SUBTYPE_ADP,
                                  SUBTYPE_AECP, SUBTYPE_CRF, SUBTYPE_MAAP,
                                  SUBTYPE_NAMES, TPID_C_TAG, Verdict,
                                  decode_aaf, decode_control, decode_crf,
                                  decode_eth, decode_mrpdu,
                                  parse_aaf_stream_format,
                                  parse_crf_stream_format, read_capture)
from avtp_wire_truth_checks import WireTruth
from avtp_wire_truth_identity import channel_identity, check_walking_tone
from avtp_wire_truth_frames import (AafFrame, CrfFrame, TalkerAdvertise,
                                    build_aaf_frame, build_adp_frame,
                                    build_crf_frame, build_msrp_frame,
                                    build_mvrp_frame, msrp_domain_value,
                                    msrp_listener_value,
                                    msrp_talker_advertise_value)
from avtp_wire_truth_selftest import (_AafWireArms, _CaptureFormatArms,
                                      _ControlPlaneArms, _CrfWireArms,
                                      _SrpWireArms)


# ------------------------------------------------------------------ self test --
def self_test() -> int:
    """Byte-vector tests for every decoder and every check.  No capture, no
    hardware, no network.  Each block ends with a NEGATIVE control, because a
    check that cannot fail is not a check (methodology R2)."""
    import unittest

    class T(_AafWireArms, _CrfWireArms, _ControlPlaneArms, _SrpWireArms,
            _CaptureFormatArms, unittest.TestCase):
        pass

    r = unittest.TextTestRunner(verbosity=2).run(
        unittest.TestLoader().loadTestsFromTestCase(T))
    return 0 if r.wasSuccessful() else 1


# ------------------------------------------------------------------------ CLI --
def main() -> int:
    """The CLI: read a capture, report every verdict, exit 0 clean / 1 on a FAIL / 2 on a SKIP under --fail-on-skip."""
    ap = argparse.ArgumentParser(
        description="decode AVTP + MSRP/MVRP off a capture and check the wire "
                    "invariants - the oracle is the wire and the clause",
        epilog="FULL DOCS: docs/testing/RUNNING_TESTS.md.  HOW TO GET A "
               "CAPTURE: an INLINE tap, on the tap host (a different machine "
               "from the controller host).  `ip link set <if> up` is NOT enough "
               "- the tap does not flow until a capture socket opens it "
               "promiscuously, and operstate reads 'unknown' even when it works, "
               "so gate on rx_packets AFTER tcpdump starts.  Capture for a "
               "DURATION (`timeout 8 tcpdump ...`), never `-c N`: an AAF stream "
               "is ~8000 frames/s, so a few hundred frames is ~50 ms of wire "
               "time and shows no ADP/MRP/AECP at all.  The tap record header "
               "shifts every ether offset by +28, so the SRP filter is "
               "'ether[40:2]=0x22ea or ether[40:2]=0x88f5'.  EXIT: 0 clean, 1 a "
               "FAIL, 2 with --fail-on-skip and any SKIP.")
    ap.add_argument("pcap", nargs="?", help="pcap or pcapng capture")
    ap.add_argument("--self-test", action="store_true",
                    help="run the byte-vector unit tests and exit")
    ap.add_argument("--tap", action="store_true",
                    help="the capture came from a ProfiShark inline tap: a "
                         "28-octet record header before every frame AND the FCS "
                         "present. Every ether offset is +28, so a BPF filter "
                         "reads the EtherType at ether[40:2]")
    ap.add_argument("--tap-header", type=int, default=None,
                    help="record header octets to strip, overriding --tap. Use "
                         "0 for a capture that arrives already stripped - "
                         "assuming a header that is not there decodes to "
                         "nothing, and so does missing one that is")
    ap.add_argument("--strip-fcs", action="store_true")
    ap.add_argument("--talker-stream", action="append", default=[],
                    help="a stream_id (hex) that MUST carry an MSRP Talker "
                         "Advertise declaration, repeatable. Pass the entity's "
                         "WHOLE Stream Output set and the capture answers "
                         "'which of my talkers never declared' - without it the "
                         "check can only see a stream that streams without a "
                         "declaration, never one that is silently undeclared")
    ap.add_argument("--expect-aaf-format", default=None,
                    help="the 8-octet AAF stream_format the controller read "
                         "back (hex), e.g. 0205022001006000")
    ap.add_argument("--expect-crf-format", default=None,
                    help="CRF stream_format hex (default: the Milan Table 7.1 "
                         f"constant {MILAN_CRF_FORMAT:016x})")
    ap.add_argument("--sr-vid", type=int, default=SR_VID_DEFAULT)
    ap.add_argument("--silent-stream", action="append", default=[],
                    help="stream_id (hex) that is bound but unfed - must be "
                         "present AND silent (Milan 5.3.7.3)")
    ap.add_argument("--fed-stream", action="append", default=[],
                    help="stream_id (hex) that must carry non-zero audio")
    ap.add_argument("--adp-entity", action="append", default=[],
                    help="entity_id (hex) that must keep advertising")
    ap.add_argument("--gptp-ref-ns", type=int, default=None,
                    help="gPTP nanoseconds at the capture's FIRST frame; "
                         "without it the class-A transit check SKIPs")
    ap.add_argument("--max-transit-ns", type=int,
                    default=CLASS_A_MAX_TRANSIT_NS)
    ap.add_argument("--jsonl", action="store_true",
                    help="one JSON verdict per line instead of a table")
    ap.add_argument("--fail-on-skip", action="store_true",
                    help="treat SKIP as failure (for a gate that must be "
                         "fully wired)")
    a = ap.parse_args()

    if a.self_test:
        return self_test()
    if not a.pcap:
        ap.error("a capture is required (or --self-test)")

    hdr = a.tap_header if a.tap_header is not None else (28 if a.tap else 0)
    recs = read_capture(a.pcap, tap_header=hdr,
                        strip_fcs=a.strip_fcs or a.tap)
    exp = Expectation(
        aaf_format=int(a.expect_aaf_format, 16) if a.expect_aaf_format else None,
        crf_format=int(a.expect_crf_format, 16) if a.expect_crf_format else None,
        sr_vid=a.sr_vid,
        silent_stream_ids=tuple(int(s, 16) for s in a.silent_stream),
        fed_stream_ids=tuple(int(s, 16) for s in a.fed_stream),
        adp_entity_ids=tuple(int(s, 16) for s in a.adp_entity),
        talker_stream_ids=tuple(int(s, 16) for s in a.talker_stream),
        gptp_ref_ns=a.gptp_ref_ns, max_transit_ns=a.max_transit_ns)
    verdicts = WireTruth(exp).feed_capture(recs).checks()

    fails = sum(1 for v in verdicts if v.verdict == "FAIL")
    skips = sum(1 for v in verdicts if v.verdict == "SKIP")
    if a.jsonl:
        for v in verdicts:
            print(v.as_json())
    else:
        for v in verdicts:
            print(f"{v.verdict:5s} {v.check}")
            if v.verdict != "PASS":
                print(f"      clause: {v.clause}")
                print(f"      detail: {json.dumps(v.detail, sort_keys=True)}")
        print(f"\n{len(verdicts)} checks: {len(verdicts)-fails-skips} PASS, "
              f"{fails} FAIL, {skips} SKIP")
    if fails:
        return 1
    return 2 if (a.fail_on_skip and skips) else 0


if __name__ == "__main__":
    sys.exit(main())
