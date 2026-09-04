#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""fuzz_ptp_bringup.py - sections 1-6 of the gPTP campaign: load the
models, cross-decode them against packet_gen, bring the plane up, climb to
asCapable, prove the grandmaster transmit path and gate the parser.

WHAT A SECTION MAY ASSUME.  These methods are mixed into
`fuzz_ptp.Campaign` and reach the DUT only through the primitives that class
defines - `self.op/state/send/tick/reset/quiet_window/stable/...` and
`self.rep`, the `cosim.Report` every check is recorded in.  Nothing here holds
state of its own; the split is by SECTION, so one area of the campaign can be
read and changed without opening the other two."""

import tsn_model
import wire

from fuzz_ptp_defs import (FL_AMGM, FL_ASCAP, GMID, MODELS, OUR_CID, PEER2_CID,
                           SECOND, S_FLAGS, S_OFFSET, S_PDELAY, S_PDEXP,
                           S_PROGRUN, S_RXDROP, S_TAPDROP, extract_fields)


class PtpBringUpSections:
    """Sections 1-6, mixed into `fuzz_ptp.Campaign`."""

    # ------------------------------------------------------------ 1 models
    def inventory(self) -> dict[str, tsn_model.Message]:
        """Load every 802.1AS model the campaign grades against.

        A model that will not load is a failed check HERE, naming itself,
        rather than a KeyError three sections later with no model name in
        the traceback."""
        self.rep.section("802.1AS model inventory (tsn-gen)")
        loaded = {}
        for kind, yml in MODELS:
            try:
                m = tsn_model.load("ptp", yml)
                loaded[kind] = m
                self.rep.ck("model %-16s loads" % kind, True,
                            "%d fields" % len(m.fields))
            except (OSError, ValueError, KeyError) as exc:
                self.rep.ck("model %-16s loads" % kind, False, str(exc))
        try:
            loaded["announce_pt1"] = tsn_model.load(
                "ptp", "8021as_announce.yaml",
                "as_announce::AS_ANNOUNCE::AS_ANNOUNCE_PT1_IF")
            self.rep.ck("model announce+path-trace loads", True,
                        "%d fields" % len(loaded["announce_pt1"].fields))
        except (OSError, ValueError, KeyError) as exc:
            self.rep.ck("model announce+path-trace loads", False, str(exc))
        try:
            loaded["eth"] = tsn_model.load("ptp", "8021as_eth_header.yaml")
            self.rep.ck("model eth header loads", True)
        except (OSError, ValueError, KeyError) as exc:
            self.rep.ck("model eth header loads", False, str(exc))
        return loaded

    # ------------------------------------------- 2 wire <-> model agreement
    def cross_decode(self, models: dict[str, tsn_model.Message]) -> None:
        """wire.py bytes vs packet_gen's independent dissection, NO shift.

        This is the measured premise the whole campaign stands on: the
        8021as_* models declare the full header (unlike the 1722.1 models
        and their missing nibble), so the model layout IS the wire layout.
        """
        self.rep.section("independent decode: wire.py vs packet_gen (no shift)")
        good = {
            "sync": wire.ptp_sync(sequence_id=0x1234),
            "follow_up": wire.ptp_follow_up(sequence_id=0x1234,
                                            origin_ns=1_000_000_123),
            "pdelay_req": wire.ptp_pdelay_req(sequence_id=0x2345),
            "pdelay_resp": wire.ptp_pdelay_resp(
                sequence_id=0x2345, t2_ns=5_000_000_000),
            "pdelay_resp_fu": wire.ptp_pdelay_resp_fu(
                sequence_id=0x2345, t3_ns=5_000_001_000),
            "announce": wire.ptp_announce(sequence_id=0x77, gm_identity=GMID,
                                          gm_priority1=100, path_trace=[]),
        }
        for kind, frame in good.items():
            m = models.get(kind)
            if m is None:
                continue
            dec = tsn_model.decode_ptp(m.yaml_dir, m.interface, frame[14:])
            if not self.rep.ck("%s: packet_gen decoded" % kind, bool(dec)):
                continue
            walked = extract_fields(m, frame)
            mism = [n for n in walked
                    if n in dec and int(dec[n]) != walked[n]]
            self.rep.ck("%s: every field agrees (walker == packet_gen)" % kind,
                        not mism,
                        ", ".join("%s %d!=%d" % (n, walked[n], int(dec[n]))
                                  for n in mism[:4]))
            msg = wire.PtpMsg(frame)
            self.rep.eq("%s: sequence_id agrees three ways" % kind,
                        (int(dec.get("sequence_id", -1)), msg.sequence_id),
                        (walked["sequence_id"], walked["sequence_id"]))

    # --------------------------------------------------------- 3 boot TX
    def boot(self, models: dict[str, tsn_model.Message]) -> None:
        """The plane's first transmission: a fresh plane sends a Pdelay_Req
        and NOTHING else, and every constrained field of that request is
        graded against the model."""
        self.rep.section("boot: the first Pdelay_Req, graded field by field")
        st0 = self.state()
        self.rep.eq("fresh plane: not asCapable", st0[S_FLAGS] & FL_ASCAP, 0)
        self.rep.eq("fresh plane: no drops", (st0[S_TAPDROP], st0[S_RXDROP]),
                    (0, 0))
        req = self.wait_tx(wire.PTP_PDELAY_REQ, 8 * SECOND)
        if not self.rep.ck("boot Pdelay_Req transmitted", req is not None):
            return
        self.rep.eq("boot req frame length", len(req), 68)
        m = wire.PtpMsg(req)
        eth = models.get("eth")
        if eth is not None:
            con = dict((n, c) for n, _b, c in eth.fields)
            self.rep.eq("boot req DA (11.3.4 / Table 11-1)",
                        m.dst.hex(), "%012x" % int(con["dst_mac"]["value"]))
            self.rep.eq("boot req EtherType", m.ethertype,
                        int(con["ethertype"]["value"]))
        self.grade_tx(models["pdelay_req"], req, "tx_pdreq")
        # OUR device emits correctionField 0 on Pdelay_Req. The shared tsn-gen
        # model deliberately leaves it UNCONSTRAINED, because 802.1AS Table 11-5
        # gives Pdelay_Req a correctionField role so a conformant requester MAY
        # send nonzero - a fact about the standard, not about us. That is why
        # the pin was removed from the model (#150); the assertion about what
        # THIS implementation transmits belongs here, beside the frame, not in
        # the oracle. grade_tx cannot carry it, so it is stated explicitly.
        self.rep.eq("tx_pdreq.correction_field is 0 (our device; #150)",
                    m.correction_field, 0)
        self.rep.eq("boot req source identity", m.source_clock_identity,
                    OUR_CID)
        # Milan: no Announce, no Sync before asCapable
        self.rep.eq("no Announce before asCapable",
                    len(self.tx_of_type(wire.PTP_ANNOUNCE)), 0)
        self.rep.eq("no Sync before asCapable",
                    len(self.tx_of_type(wire.PTP_SYNC)), 0)

    # ------------------------------------------------------------- 4 climb
    def climb(self, label: str = "climb") -> list[int] | None:
        """Exchanges up: asCapable must rise within the Milan ladder, and
        the measured peer delay must match the responder's own records."""
        self.rep.section("%s: exchanges up, asCapable within the ladder"
                         % label)
        self.responder(True)
        st = self.state()
        spent = 0
        while not (st[S_FLAGS] & FL_ASCAP) and spent < 16 * SECOND:
            st = self.tick(200)
            spent += 200 * 10000
        self.rep.ck("%s: asCapable rose" % label,
                    st[S_FLAGS] & FL_ASCAP, "flags=%x" % st[S_FLAGS])
        pd, exp = st[S_PDELAY], st[S_PDEXP]
        self.rep.ck("%s: pdelay matches the responder's records" % label,
                    abs((pd & 0xFFFFFFFF) - exp) <= 32,
                    "pdelay=%d expect=%d" % (pd, exp))
        return st

    # ------------------------------------------------------------ 5 GM TX
    def gm_tx(self, models: dict[str, tsn_model.Message]) -> None:
        """What the plane transmits once it self-declares grandmaster: the
        Announce, the Sync and the Follow_Up that pairs it, graded field by
        field, with the Follow_Up's origin proved to be live fabric time."""
        self.rep.section("as grandmaster: Announce / Sync / Follow_Up conform")
        # the plane self-declares grandmaster only after the announce-receipt
        # timeout elapses with no better master heard (802.1AS BMCA + Milan
        # Table 4.2) — not the instant asCapable rises
        st = self.become_gm()
        self.rep.ck("plane self-declares grandmaster after the receipt timeout",
                    st[S_FLAGS] & FL_AMGM, "flags=%x" % st[S_FLAGS])
        self.rep.eq("as GM the published identity is ours",
                    self.gm_of(st), OUR_CID)
        self.drain_tx()
        ann = self.wait_tx(wire.PTP_ANNOUNCE, 4 * SECOND)
        if self.rep.ck("Announce transmitted", ann is not None):
            am = wire.PtpMsg(ann)
            pt1 = am.message_length == 76 and "announce_pt1" in models
            self.grade_tx(models["announce_pt1" if pt1 else "announce"],
                          ann, "tx_announce")
            self.rep.eq("tx_announce grandmaster is us", am.gm_identity,
                        OUR_CID)
            self.rep.eq("tx_announce stepsRemoved", am.steps_removed, 0)
            self.rep.ck("tx_announce carries the path trace TLV (10.5.3.3)",
                        am.message_length == 76 and
                        am._be(78, 2) == 0x0008 and am._be(82, 8) == OUR_CID,
                        "ml=%d" % am.message_length)
        sync = self.wait_tx(wire.PTP_SYNC, 2 * SECOND)
        if self.rep.ck("Sync transmitted", sync is not None):
            sm = wire.PtpMsg(sync)
            # control 0x0 (Table 11-7) and the ten reserved bytes of a
            # two-step Sync (Table 11-8, all zero) are ordinary graded
            # fields: the donor's per-message TX control byte (FPGA-gPTP
            # #9) and its zeroed Sync body (FPGA-gPTP #10, #137). The model
            # grades origin_timestamp as the 80-bit zero body; the live
            # egress time is graded on the paired Follow_Up below, so
            # zeroing the Sync cannot hide a dead timestamp path
            self.grade_tx(models["sync"], sync, "tx_sync")
            self.rep.eq("tx_sync source identity", sm.source_clock_identity,
                        OUR_CID)
            fu = self.wait_tx(wire.PTP_FOLLOW_UP, SECOND)
            if self.rep.ck("Follow_Up pairs the Sync", fu is not None):
                fm = wire.PtpMsg(fu)
                self.rep.eq("tx_fu sequence pairs its sync",
                            fm.sequence_id, sm.sequence_id)
                # control 0x2 (Table 11-7) is an ordinary graded field too
                self.grade_tx(models["follow_up"], fu, "tx_fu",
                              skip=("precise_origin_seconds",
                                    "precise_origin_ns"))
                st2 = self.state()
                self.rep.ck("tx_fu origin is live fabric time",
                            0 < fm.ts_total_ns <= self.phc_of(st2),
                            "origin=%d phc=%d"
                            % (fm.ts_total_ns, self.phc_of(st2)))

    # ---------------------------------------------------- 6 parser gates
    def _gate_builders(self):
        """The four legal frame builders every parser gate below mutates."""
        good = {
            "sync": lambda **kw: wire.ptp_sync(
                sequence_id=self.nseq("sync"), **kw),
            "follow_up": lambda **kw: wire.ptp_follow_up(
                sequence_id=self.nseq("fu"), **kw),
            "pdelay_req": lambda **kw: wire.ptp_pdelay_req(
                sequence_id=self.nseq("pdreq"),
                source_clock_identity=PEER2_CID, src=wire.GPTP_PEER2_MAC,
                **kw),
            "announce": lambda **kw: wire.ptp_announce(
                sequence_id=self.nseq("announce"), gm_identity=GMID,
                gm_priority1=254, **kw),
        }
        return good

    def _gate_header_fields(self, models, good):
        """Every illegal transport/version/domain header value must drop."""
        # parser-owned rejects: per model, every illegal transport/version/
        # domain. domainNumber joined the header drop arms with FPGA-gPTP #6
        # (802.1AS-2011 8.1: a gPTP domain is domain 0; IEEE 1588-2008 9.5.1:
        # a message whose domainNumber does not match is not accepted for
        # processing). The probe list is asserted non-empty first: a model
        # that stopped pinning a field would otherwise skip the loop and
        # the suite would stay green having checked nothing
        for kind, build in good.items():
            m = models[kind]
            for field in ("transport_specific", "version_ptp",
                          "domain_number"):
                probes = m.illegal(field)[:3]
                self.rep.ck("%s %s: the model yields illegal probes"
                            % (kind, field), len(probes) > 0,
                            "%d probes" % len(probes))
                for v in probes:
                    before = self.state()
                    after = self.send(build(**{field: v}))
                    self.rep.eq("%s %s=%d: dropped and counted"
                                % (kind, field, v),
                                after[S_RXDROP], before[S_RXDROP] + 1)
                    self.stable("%s %s=%d" % (kind, field, v), before, after)

    # NOTE on quoting numbers about this group, learned the hard way
    # twice: a mutation figure is "campaign total minus what failed", so
    # ANY check added anywhere in this file re-prices every PASS count
    # quoted about any mutation, in the README, in a PR body or here,
    # while only a check added to THIS group moves its FAIL counts. A
    # sixth Pdelay_Req probe in another section is enough. Re-measure
    # before quoting, and prefer the fail side in anything committed.
    #
    # unknown message types with a full header: refused, counted, and
    # -- the half that matters -- SILENT. Both properties are graded
    # because the two are independent: between the #11 rework and
    # FPGA-gPTP #22's fix such a frame was neither refused NOR silent
    # (it dispatched into the timer program, which TRANSMITS), and the
    # two candidate fixes for #22 would each have satisfied only one
    # of them, a parser drop arm moving the counter and an
    # entry-table no-op stopping the transmission. The pinned parser
    # takes the first route and the silence follows from it; a suite
    # that graded only the counter could not tell the two apart.
    #
    # The silence probe is measured against a quiet window: empty
    # blocks first (so the plane's own 125 ms Sync and 1 s Pdelay_Req
    # cadence cannot account for what follows), then one frame, then
    # one 10,000-cycle block. Before the fix one unlisted-type frame
    # drew one Pdelay_Req in that block against zero for the
    # un-injected control, and twenty drew ten (802.1AS-2011 11.5.2.2
    # and Figure 11-8 leave the interval timer the only exit).
    def _gate_unknown_types(self):
        """An unlisted messageType is refused, counted, silent, and inert."""
        attempts = []
        for mt in (0x1, 0x4, 0x5, 0x6, 0x7, 0x9, 0xD, 0xE, 0xF):
            # Up to four attempts, and the ATTEMPT REPORTED is the first
            # one that either passes or fails for the reason this probe
            # exists. A 10,000-cycle block is a 25th of the 125 ms Sync
            # interval, so a window can carry the plane's own scheduled
            # Sync and Follow_Up however quiet its predecessors were (once
            # across the nine types, measured), and only THAT is worth
            # re-rolling. The two cases are distinguishable without
            # guessing: the plane's own cadence rides a frame the parser
            # REFUSED, so the drop counter advanced; a frame the parser
            # dispatched draws its transmission with the counter standing
            # still. So a missing drop ends the loop immediately and is
            # reported, and a retry can only ever re-roll a window whose
            # injected frame was already refused. Discarding a failing
            # attempt would make an INTERMITTENT regression -- the arm
            # working on alternate frames, which is the likely shape here
            # since the dispatch outcome is already bank-state dependent
            # -- pass by rerolling, with a log byte-identical to a clean
            # run because passing checks are not printed.
            quiet, drawn, tries = False, None, 0
            for tries in range(1, 5):    # attempts, reported below
                quiet = self.quiet_window()
                before = self.state()
                mark = len(self.txq)
                self.send(wire.ptp_frame(mt, bytes(20),
                                         sequence_id=self.nseq("x")))
                self.tick(1)
                drawn = len(self.txq) - mark
                after = self.state()
                if after[S_RXDROP] != before[S_RXDROP] + 1:
                    break                 # not refused: this attempt IS it
                if quiet and drawn == 0:
                    break
            attempts.append((mt, tries))
            self.rep.ck("unknown type 0x%X: a quiet window precedes it" % mt,
                        quiet, "%d attempt(s)" % tries)
            # The re-roll above is safe only because a frame the parser
            # REFUSED cannot also have dispatched: that is what lets a
            # non-empty window with an advanced drop counter be blamed on
            # the plane's own cadence. Assert it rather than trust it. The
            # engine brings `dbg_busy_o` out of the slice and the bench
            # wrapper counts its rising edges, so "did anything run?" is a
            # question about the window, not about an instant: a refused
            # frame must leave the uCPU program count exactly where it was.
            # Without this, a donor change that both counted AND dispatched
            # would put every attempt on the benign path and the re-roll
            # would hide it -- the same hiding the attempt-discarding loop
            # was fixed for in #210's second review round.
            self.rep.eq("unknown message type 0x%X: ran no program" % mt,
                        after[S_PROGRUN], before[S_PROGRUN])
            self.rep.eq("unknown message type 0x%X: dropped and counted"
                        % mt, after[S_RXDROP], before[S_RXDROP] + 1)
            self.rep.eq("unknown message type 0x%X: draws no transmission "
                        "(11.5.2.2)" % mt, drawn, 0)
            self.stable("unknown type 0x%X" % mt, before, after)
            # servo and pdelay ride with the silence: a request the
            # dispatch drew would be ANSWERED by the bench responder, and
            # a republished neighborPropDelay is the same defect one step
            # downstream
            self.rep.eq("unknown message type 0x%X: offset unmoved" % mt,
                        after[S_OFFSET], before[S_OFFSET])
            self.rep.eq("unknown message type 0x%X: peer delay unmoved"
                        % mt, after[S_PDELAY], before[S_PDELAY])
        # The attempt counts belong in the log even when everything passes:
        # `rep.ck`'s detail is printed on failure only, so a run that needed
        # four windows per type would otherwise read exactly like one that
        # needed one, and a rising collision rate (a changed cadence, a
        # different block size) would be invisible until the day it runs out
        # of retries.
        self.rep.note("unlisted-type windows: %s (%d re-roll(s) over %d "
                      "types)"
                      % (" ".join("0x%X:%d" % a for a in attempts),
                         sum(t - 1 for _, t in attempts), len(attempts)))

    def _gate_frame_shapes(self, good):
        """What never enters, what is cut too short, and what 11.4.1 ignores."""
        # classify negatives: never enter, never cost a drop
        for label, frame in (
                ("AVTP ethertype", wire.ptp_sync(sequence_id=1,
                                                 ethertype=0x22F0)),
                ("C-VLAN tagged gPTP",
                 wire.GPTP_MCAST_MAC + wire.GPTP_PEER_MAC +
                 b"\x81\x00\x00\x02" + wire.ptp_sync(sequence_id=2)[12:]),
                ("6-byte runt", b"\x01\x02\x03\x04\x05\x06")):
            before = self.state()
            after = self.send(frame)
            self.rep.eq("%s: invisible (no drop, no count)" % label,
                        (after[S_RXDROP], after[S_TAPDROP]),
                        (before[S_RXDROP], before[S_TAPDROP]))
            self.stable(label, before, after)
        # a 15-byte 0x88F7 runt IS classified, then parser-dropped
        before = self.state()
        after = self.send(wire.ptp_sync(sequence_id=3)[:15])
        self.rep.eq("15-byte gPTP runt: parser drop counted",
                    after[S_RXDROP], before[S_RXDROP] + 1)
        # truncation at the per-type minimum boundary (parser min_len map).
        # The boundary is the LEGAL frame: the Ethernet header the bench
        # puts in front of the PTP message, 14 bytes of DA, SA and
        # EtherType (the 11.4.1 NOTE counts 18 for header AND FCS, and no
        # FCS reaches this DUT), plus the message of 802.1AS-2011
        # Table 11-8 (Sync 44)
        # and Table 10-7 (Announce 64), for the Follow_Up the 76 octets of
        # Table 11-9, whose Follow_Up information TLV is a FIELD of the
        # message and not a suffix (11.4.4.2.2, 11.4.4.3): 90 bytes since
        # FPGA-gPTP #11, and for the Pdelay_Req the 54 octets of Table
        # 11-11, whose two ten-octet reserved fields are message fields
        # like any other: 68 bytes since FPGA-gPTP #12
        for kind, min_frame in (("sync", 58), ("follow_up", 90),
                                ("announce", 78), ("pdelay_req", 68)):
            f = good[kind]()
            before = self.state()
            after = self.send(f[:min_frame - 1])
            self.rep.eq("%s cut to %d B: dropped and counted"
                        % (kind, min_frame - 1),
                        after[S_RXDROP], before[S_RXDROP] + 1)
            self.stable("%s truncated" % kind, before, after)
        # reserved fields: garbage is IGNORED, not dropped (11.4.1)
        before = self.state()
        after = self.send(good["pdelay_req"](reserved0=0xF, reserved1=0xAA,
                                             reserved2=0xDEADBEEF))
        self.rep.eq("garbage reserved fields: NOT dropped (11.4.1)",
                    after[S_RXDROP], before[S_RXDROP])
        resp = self.wait_tx(wire.PTP_PDELAY_RESP, SECOND)
        self.rep.ck("garbage reserved fields: request still answered",
                    resp is not None)

    def parser_gates(self, models: dict[str, tsn_model.Message]) -> None:
        """The receive gates: what the parser must drop, drops and is
        counted; what 11.4.1 says a receiver ignores passes through with the
        state unmoved; and every frame shape outside the length oracle."""
        self.rep.section("parser gates: what must drop, drops; "
                         "what 11.4.1 ignores, passes")
        good = self._gate_builders()
        self._gate_header_fields(models, good)
        self._gate_unknown_types()
        self._gate_frame_shapes(good)
