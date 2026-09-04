#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""fuzz_ptp_timing.py - sections 8-13 of the gPTP campaign: BTCA, the
Sync/Follow_Up pairs, the suffix acceptance rule, cease, the malformed storms
and the response drought that must make asCapable FALL.

WHAT A SECTION MAY ASSUME.  These methods are mixed into
`fuzz_ptp.Campaign` and reach the DUT only through the primitives that class
defines - `self.op/state/send/tick/reset/quiet_window/stable/...` and
`self.rep`, the `cosim.Report` every check is recorded in.  Nothing here holds
state of its own; the split is by SECTION, so one area of the campaign can be
read and changed without opening the other two."""
import random
from collections.abc import Sequence

import tsn_model
import wire

from fuzz_ptp_defs import (BUILD, D_NOM, FL_AMGM, FL_ASCAP, FL_SYNCOK, GMID,
                           HDR_FIELDS, MODELS, OUR_CID, PEER2_CID, PEER_CID,
                           SECOND, S_FLAGS, S_OFFSET, S_PDELAY, S_PDEXP,
                           S_RXDROP, S_TAPDROP)


class PtpTimingSections:
    """Sections 8-13, mixed into `fuzz_ptp.Campaign`."""

    # ----------------------------------------------------------- 8 BTCA
    def _btca_reject(self, label, issue, drop, **kw):
        """One illegal better vector: the plane must stay grandmaster.

        `drop` says whether the refusal is the parser's (a counted header
        drop) or the 10.3.10.2.1 qualification's (no drop at all); `issue`
        names a tracked gap when the refusal is not yet implemented.
        """
        self.become_gm()
        kw.setdefault("gm_identity", 0x2222)
        kw.setdefault("source_clock_identity", PEER2_CID)
        kw.setdefault("src", wire.GPTP_PEER2_MAC)
        f = wire.ptp_announce(sequence_id=self.nseq("announce"),
                              gm_priority1=1, **kw)
        before = self.state()
        after = self.send(f)
        held = self.gm_of(after) == OUR_CID
        if issue is None:
            self.rep.ck("%s: rejected, plane stays GM" % label, held,
                        "gm=%x" % self.gm_of(after))
            self.stable(label, before, after)
        else:
            self.eq_or_gap("%s: rejected, plane stays GM" % label,
                           self.gm_of(after), OUR_CID, issue)
        if drop is not None:
            self.rep.eq("%s: drop counted" % label,
                        after[S_RXDROP], before[S_RXDROP] + 1)
        else:
            # a qualifyAnnounce refusal is NOT a header drop: the frame
            # is well formed and the parser hands it over, and the
            # 10.3.10.2.1 rules refuse it before BTCA. The counter
            # holding is the whole accounting a refusal has (the donor
            # keeps no qualification counter), so it is asserted, not
            # merely left unchecked
            self.rep.eq("%s: parser drop counter unmoved" % label,
                        after[S_RXDROP], before[S_RXDROP])

    def _btca_rejects(self):
        """Every illegal better vector this campaign knows, refused in turn."""
        # parser-owned rejects: bad_r drops them at the header, counted, and
        # GM / parent / asCapable hold. The domain arm is the FPGA-gPTP #6
        # fix (8.1; IEEE 1588-2008 9.5.1); it is probed separately from the
        # Sync/Follow_Up side in sync_pairs so one fixed path cannot hide
        # the other
        self._btca_reject("better vector, version 1", None, drop=1, version_ptp=1)
        self._btca_reject("better vector, transportSpecific 0", None, drop=1,
                     transport_specific=0)
        self._btca_reject("better vector, domain 5 (8.1: single domain 0)",
                     None, drop=1, domain_number=5)
        # qualifyAnnounce (10.3.10.2.1), hard assertions since FPGA-gPTP #7:
        # (a) an Announce claiming our own clockIdentity, (b) stepsRemoved
        # at or above 255 -- the field is 16 bits, so its LOW BYTE is not
        # the test -- and (c) our identity anywhere in the path trace, which
        # is the loop an end station meets without forgery: our own Announce
        # returned by a bridge. Since the donor's strict PathTrace
        # validation (FPGA-gPTP #45; 802.1AS-2011 10.5.3.3.4) a present TLV
        # must open with the announced grandmasterIdentity and carry
        # exactly stepsRemoved+1 identities, so every fixture below is
        # wire-legal under those rules and lands its refusal in the
        # MICROCODE, where the drop counter holding is what places it
        self._btca_reject("better vector, own sourcePortIdentity (10.3.10.2.1a)",
                     None, drop=None, source_clock_identity=OUR_CID,
                     src=wire.GPTP_PEER2_MAC)
        # (b) can no longer ride a PathTrace TLV: stepsRemoved 255 demands
        # 256 identities, 2052 TLV octets, past the 1500-octet Ethernet
        # payload the parser admits (its MAX_MSG_LEN_C). The TLV-absent
        # 64-octet Announce (count and loop verdict honestly zero) is the
        # one wire-legal carrier left, and it reaches STEPS_MAX_C in
        # qualifyAnnounce with the parser satisfied
        self._btca_reject("better vector, stepsRemoved 255, no path trace "
                     "(10.3.10.2.1b)", None, drop=None, steps_removed=255,
                     path_trace=[])
        self._btca_reject("better vector, stepsRemoved 0x0100, no path trace "
                     "(10.3.10.2.1b)", None, drop=None,
                     steps_removed=0x0100, path_trace=[])
        # (c) is one coherent verdict now: the parser compares EVERY
        # declared hop with thisClock (not merely the eight it retains) and
        # the microcode refuses on bank word 12 bit 8. The first fixture
        # puts our identity behind the announced GM at the head; the
        # reflected-Announce pair names US as grandmaster (the only
        # wire-legal head for a path that starts with us), so their
        # plane-stays-GM check cannot bite alone and the teeth are the
        # parent and flags canaries of stable(): adopting the better
        # vector would move parent to the peer and clear AMGM
        self._btca_reject("better vector, our id in the path trace "
                     "(10.3.10.2.1c)", None, drop=None, gm_identity=0x3333,
                     steps_removed=1, path_trace=[0x3333, OUR_CID])
        self._btca_reject("better vector, our own Announce a bridge extended: "
                     "us the first path-trace hop (10.3.10.2.1c)", None,
                     drop=None, gm_identity=OUR_CID, steps_removed=1,
                     path_trace=[OUR_CID, PEER2_CID])
        # The cap edge (milan-fpga #219). The receive bank retains eight
        # hops; the walk verdict compares EVERY declared hop as the bytes
        # stream (donor #7), so the refusal must be identical on both
        # sides of the bank's cap. Before that lineage, index 7 was
        # refused while index 8 and beyond were ADOPTED with
        # stepsRemoved far below the 255 backstop - the exact three
        # placements measured in the #219 report, now hard-asserted.
        self._btca_reject("better vector, our id the eighth hop of eight "
                     "(cap edge, 10.3.10.2.1c)", None, drop=None,
                     gm_identity=0x5000, steps_removed=7,
                     path_trace=[0x5000, 0x5001, 0x5002, 0x5003, 0x5004,
                                 0x5005, 0x5006, OUR_CID])
        self._btca_reject("better vector, our id the ninth hop of nine "
                     "(first hop past the bank, 10.3.10.2.1c)", None,
                     drop=None, gm_identity=0x5100, steps_removed=8,
                     path_trace=[0x5100, 0x5101, 0x5102, 0x5103, 0x5104,
                                 0x5105, 0x5106, 0x5107, OUR_CID])
        self._btca_reject("better vector, our id the tenth hop of twelve "
                     "(deep in the once-blind region, 10.3.10.2.1c)",
                     None, drop=None, gm_identity=0x5200, steps_removed=11,
                     path_trace=[0x5200, 0x5201, 0x5202, 0x5203, 0x5204,
                                 0x5205, 0x5206, 0x5207, 0x5208, OUR_CID,
                                 0x520A, 0x520B])
        self._btca_reject("better vector, our own Announce reflected: us the "
                     "only path-trace hop (10.3.10.2.1c)", None, drop=None,
                     gm_identity=OUR_CID, path_trace=[OUR_CID])
        # the strict wire rules themselves (FPGA-gPTP #45; 10.5.3.3.4):
        # a head that is not the announced grandmaster, a count that is not
        # stepsRemoved+1, and the old wire-illegal (b) shape. Each is
        # refused AT THE PARSER, a counted header drop, before
        # qualifyAnnounce sees a bank
        self._btca_reject("better vector, path-trace head is not the announced "
                     "grandmaster (10.5.3.3.4)", None, drop=1,
                     gm_identity=0x3333, path_trace=[0x5555])
        self._btca_reject("better vector, one path-trace hop against "
                     "stepsRemoved 1 (10.5.3.3.4)", None, drop=1,
                     gm_identity=0x3333, steps_removed=1,
                     path_trace=[0x3333])
        self._btca_reject("better vector, stepsRemoved 255 on a one-hop path "
                     "trace (10.5.3.3.4)", None, drop=1, steps_removed=255)

    def btca(self) -> None:
        """Only a legal better vector moves the grandmaster: each
        10.3.10.2.1 disqualification is asserted on a WIRE-LEGAL fixture, so
        a parser that dropped the frame could not be mistaken for a pass."""
        self.rep.section("BTCA under fuzz: only a legal better vector moves "
                         "the grandmaster")
        # positive control: a clean better external master is adopted
        st = self.become_gm()
        self.rep.ck("baseline: plane is grandmaster", st[S_FLAGS] & FL_AMGM,
                    "flags=%x" % st[S_FLAGS])
        after = self.send(wire.ptp_announce(
            sequence_id=self.nseq("announce"), gm_identity=GMID,
            gm_priority1=100))
        self.tick(2)
        after = self.state()
        self.rep.eq("clean better master is adopted", self.gm_of(after), GMID)
        self.rep.eq("adopting master: no longer grandmaster",
                    after[S_FLAGS] & FL_AMGM, 0)
        self.rep.eq("parent follows the master port", self.parent_of(after),
                    PEER_CID)

        # Each rejection probe runs against the GM baseline: it becomes GM
        # (a re-establishable known state), then injects a vector that is
        # BETTER on merit (priority1 1 < our 248) but must be rejected for a
        # SEPARATE reason. If the plane stays GM the rule holds; if the
        # vector is adopted the missing check is a tracked gap.
        self._btca_rejects()

        # truncated-at-75 better announce (parser min is 78): parser-dropped
        self.become_gm()
        before = self.state()
        f = wire.ptp_announce(sequence_id=self.nseq("announce"),
                              gm_identity=0x2222, gm_priority1=1,
                              source_clock_identity=PEER2_CID,
                              src=wire.GPTP_PEER2_MAC, path_trace=[])
        after = self.send(f[:75])
        self.rep.eq("truncated better announce: plane stays GM",
                    self.gm_of(after), OUR_CID)
        self.rep.eq("truncated better announce: drop counted",
                    after[S_RXDROP], before[S_RXDROP] + 1)

        # a legal deep path trace is capped at 8 published hops but adopts;
        # wire-legal means the announced grandmaster heads the path and the
        # count is stepsRemoved+1 (10.5.3.3.4). Until #217 this 164-octet
        # frame was also the campaign's only above-minimum Announce
        # acceptance; the suffix_accept section now carries that duty by
        # name, so this fixture may be reshaped for the cap's own reasons
        self.become_gm()
        after = self.send(wire.ptp_announce(
            sequence_id=self.nseq("announce"), gm_identity=0x4444,
            gm_priority1=50, source_clock_identity=PEER2_CID,
            src=wire.GPTP_PEER2_MAC, steps_removed=11,
            path_trace=[0x4444] + [0x5000 + i for i in range(11)]))
        self.rep.eq("12-hop legal better vector still adopts (cap publishes 8)",
                    self.gm_of(after), 0x4444)
        # leave a clean GM baseline: let the adopted vectors expire so the
        # servo section starts from known state (0x4444 p50 would otherwise
        # outrank the GMID p100 the next section adopts)
        self.become_gm()

    # ------------------------------------------------------- 9 sync pairs
    def _sync_pair(self, delta, domain=0, fu_seq=None, fu_src=PEER_CID,
                   sync_flags=0x0208):
        """Send one Sync + Follow_Up pair and return the state after it."""
        sq = self.nseq("sync")
        st = self.state()
        at = self.phc_of(st)
        self.send(wire.ptp_sync(sequence_id=sq, flags=sync_flags,
                                domain_number=domain))
        self.send(wire.ptp_follow_up(
            sequence_id=sq if fu_seq is None else fu_seq,
            origin_ns=at - delta - D_NOM, domain_number=domain,
            source_clock_identity=fu_src))
        return self.tick(2)

    def _followup_shapes(self):
        """Every malformed Follow_Up is refused, and the pending Sync survives.

        The complete Follow_Up sent last is the proof: it still pairs with the
        Sync none of the refusals was allowed to consume.
        """
        # 802.1AS-2011 Table 11-9 makes the Follow_Up information TLV a
        # field of the 76-octet message (11.4.4.2.2 places it first after
        # the fixed fields; 11.4.4.3.2 to 11.4.4.3.5 fix its header at
        # tlvType 0x3, lengthField 28, organizationId 00-80-C2 and
        # organizationSubType 1), so a TLV-less, a physically truncated, a
        # wrong-tlvType and a short-DECLARED Follow_Up are each refused at
        # the parser, ahead of the servo (FPGA-gPTP #11); #140 asks for
        # both failure modes, bytes missing from the wire and a
        # messageLength that lies about them. None of the five may consume
        # the pending Sync: the complete Follow_Up after all of them still
        # pairs with it.
        self.refresh_master()
        sq = self.nseq("sync")
        st = self.state()
        at = self.phc_of(st)
        self.send(wire.ptp_sync(sequence_id=sq, flags=0x0208))
        # 40 us of skew: an accepted malformed Follow_Up would move the
        # published offset far outside the band a clean pair lands in
        bad_origin = at - 40000 - D_NOM
        full = wire.ptp_follow_up(sequence_id=sq, origin_ns=bad_origin)
        self.rep.eq("a complete Follow_Up is 90 bytes (Table 11-9: 76 octets)",
                    len(full), 90)
        for label, frame in (
                ("TLV-less Follow_Up (58 B)",
                 wire.ptp_follow_up(sequence_id=sq, origin_ns=bad_origin,
                                    tlv=False)),
                ("Follow_Up declaring 76 cut at 89 B", full[:89]),
                ("Follow_Up with tlvType 0x0008",
                 wire.ptp_follow_up(sequence_id=sq, origin_ns=bad_origin,
                                    tlv_type=0x0008)),
                # DECLARED length, not physical truncation: these two are
                # the complete 90 bytes and only messageLength lies, so the
                # parser's header arm at octets 2..3 is the only thing that
                # can refuse them (11.4.2.2 counts every octet through the
                # last TLV). 44 is the length the pre-#11 shape declared,
                # 75 one octet short of Table 11-9
                ("complete Follow_Up declaring messageLength 44",
                 wire.ptp_follow_up(sequence_id=sq, origin_ns=bad_origin,
                                    message_length=44)),
                ("complete Follow_Up declaring messageLength 75",
                 wire.ptp_follow_up(sequence_id=sq, origin_ns=bad_origin,
                                    message_length=75))):
            before = self.state()
            after = self.send(frame)
            self.rep.eq("%s: dropped and counted" % label,
                        after[S_RXDROP], before[S_RXDROP] + 1)
            self.rep.eq("%s: offset unmoved" % label,
                        after[S_OFFSET], before[S_OFFSET])
            self.rep.eq("%s: sync verdict unmoved" % label,
                        after[S_FLAGS] & FL_SYNCOK,
                        before[S_FLAGS] & FL_SYNCOK)
            self.stable(label, before, after)
        # the pending Sync survived all three refusals: 5 us of skew, so the
        # pairing is proven by a value no earlier state in this section holds
        self.send(wire.ptp_follow_up(sequence_id=sq,
                                     origin_ns=at - 5000 - D_NOM))
        after = self.tick(2)
        off = (after[S_OFFSET] - (1 << 32) if after[S_OFFSET] >> 31
               else after[S_OFFSET])
        self.rep.ck("the complete Follow_Up still pairs with the pending Sync",
                    abs(off - 5000) <= 300, "offset=%d" % off)

    def sync_pairs(self) -> None:
        """Sync consumption: a clean Sync/Follow_Up pair steers the servo to
        the planted offset, and every malformed Follow_Up shape cannot."""
        self.rep.section("sync consumption: clean pairs move the servo, "
                         "malformed ones cannot")

        # adopt GMID and settle a clean baseline before the servo probes
        self.master = (GMID, 100)
        self.refresh_master()
        self.tick(2)
        st = self._sync_pair(1000)
        off = st[S_OFFSET] - (1 << 32) if st[S_OFFSET] >> 31 else st[S_OFFSET]
        self.rep.ck("clean pair: offset lands near +1000",
                    abs(off - 1000) <= 300, "offset=%d" % off)
        self.rep.ck("clean pair: sync verdict up", st[S_FLAGS] & FL_SYNCOK,
                    "flags=%x" % st[S_FLAGS])
        # these two the servo correctly ignores (pairing rules work today)
        for label, kw in (
                ("Follow_Up with a foreign sequence",
                 dict(delta=40000, fu_seq=0xEEEE)),
                ("Follow_Up from a foreign source",
                 dict(delta=40000, fu_src=PEER2_CID))):
            self.refresh_master()
            before = self.state()
            b_off = before[S_OFFSET]
            after = self._sync_pair(**kw)
            self.rep.eq("%s: offset unmoved" % label, after[S_OFFSET], b_off)
            self.stable(label, before, after)
        # a domain-5 pair is refused at the header (8.1; IEEE 1588-2008
        # 9.5.1): both frames drop before the servo can see them, so the
        # offset, the sync verdict, GM, parent and asCapable hold and the
        # drops are counted. Probed separately from the BTCA-side domain
        # probe so one fixed path cannot hide the other (FPGA-gPTP #6)
        self.refresh_master()
        before = self.state()
        after = self._sync_pair(delta=40000, domain=5)
        self.rep.eq("pair in domain 5: offset unmoved",
                    after[S_OFFSET], before[S_OFFSET])
        self.rep.eq("pair in domain 5: both dropped and counted",
                    after[S_RXDROP], before[S_RXDROP] + 2)
        self.rep.eq("pair in domain 5: sync verdict unmoved",
                    after[S_FLAGS] & FL_SYNCOK, before[S_FLAGS] & FL_SYNCOK)
        self.stable("pair in domain 5", before, after)
        # the foreign Sync left no pending slot: a domain-0 Follow_Up with
        # its sequence pairs with nothing, so the Sync side is proven on
        # its own and not only through the Follow_Up's drop
        st = self.state()
        self.send(wire.ptp_follow_up(sequence_id=self.seq["sync"],
                                     origin_ns=self.phc_of(st) - 40000
                                     - D_NOM))
        after = self.tick(2)
        self.rep.eq("domain-0 Follow_Up after a domain-5 Sync: offset unmoved",
                    after[S_OFFSET], before[S_OFFSET])
        self._followup_shapes()
        # the servo recovers on the next clean pair
        self.refresh_master()
        st = self._sync_pair(1000)
        off = st[S_OFFSET] - (1 << 32) if st[S_OFFSET] >> 31 else st[S_OFFSET]
        self.rep.ck("recovery pair: offset back near +1000",
                    abs(off - 1000) <= 300, "offset=%d" % off)

    # --------------------------------------- 10 the accept side (issue #217)
    def _suffix_steer(self, label, delta, sync_suffix, fu_suffix):
        """One suffixed Sync/Follow_Up pair: admitted, and it steers the servo."""
        self.refresh_master()
        sq = self.nseq("sync")
        before = self.state()
        at = self.phc_of(before)
        self.send(wire.ptp_sync(sequence_id=sq, suffix=sync_suffix))
        after = self.send(wire.ptp_follow_up(
            sequence_id=sq, origin_ns=at - delta - D_NOM,
            suffix=fu_suffix))
        self.rep.eq("%s: parser drop counter unmoved" % label,
                    after[S_RXDROP], before[S_RXDROP])
        st = self.tick(2)
        off = (st[S_OFFSET] - (1 << 32) if st[S_OFFSET] >> 31
               else st[S_OFFSET])
        self.rep.ck("%s: consumed and steered, offset lands near %+d"
                    % (label, delta), abs(off - delta) <= 300,
                    "offset=%d" % off)

    def _suffix_exchange(self, label, resp_suffix, rfu_suffix):
        """One suffixed Pdelay pair by hand: it completes, and the ladder recovers."""
        self.responder(False)
        mark = len(self.txq)
        self.drain_tx()
        got_req = self.wait_tx(wire.PTP_PDELAY_REQ,
                               4 * SECOND) is not None
        self.tick(4)
        # answer the NEWEST outstanding request: the pairing arms
        # against the plane's latest sequence, and a 1 s cadence can
        # put a second request inside wait_tx's observation window
        reqs = self.tx_of_type(wire.PTP_PDELAY_REQ, mark)
        self.drain_tx()
        if not self.rep.ck("%s: an unanswered request to answer"
                           % label, got_req and len(reqs) > 0):
            self.responder(True)
            return
        rq = wire.PtpMsg(reqs[-1])
        t2 = self.phc_of(self.state()) + 5_000_000
        before = self.state()
        self.send(wire.ptp_pdelay_resp(
            sequence_id=rq.sequence_id, t2_ns=t2,
            requesting_clock_identity=OUR_CID,
            requesting_port_number=rq.source_port_number,
            source_clock_identity=PEER_CID, suffix=resp_suffix))
        self.send(wire.ptp_pdelay_resp_fu(
            sequence_id=rq.sequence_id, t3_ns=t2 + 200,
            requesting_clock_identity=OUR_CID,
            requesting_port_number=rq.source_port_number,
            source_clock_identity=PEER_CID, suffix=rfu_suffix))
        after = self.tick(2)
        self.rep.eq("%s: parser drop counter unmoved" % label,
                    after[S_RXDROP], before[S_RXDROP])
        self.rep.ck("%s: the exchange completes, peer delay "
                    "re-measured" % label,
                    after[S_PDELAY] != before[S_PDELAY],
                    "pdelay %d -> %d" % (before[S_PDELAY],
                                         after[S_PDELAY]))
        self.responder(True)
        st = self.state()
        spent = 0
        while not (st[S_FLAGS] & FL_ASCAP) and spent < 16 * SECOND:
            st = self.tick(200)
            spent += 200 * 10000
        self.rep.eq("after the %s probe: asCapable is whole" % label,
                    st[S_FLAGS] & FL_ASCAP, FL_ASCAP)
        self.rep.ck("after the %s probe: the delay is re-measured "
                    "from real exchanges" % label,
                    abs((st[S_PDELAY] & 0xFFFFFFFF) - st[S_PDEXP]) <= 32,
                    "pdelay=%d expect=%d" % (st[S_PDELAY], st[S_PDEXP]))

    def suffix_accept(self) -> None:
        """The accept side of the length oracle: one over-minimum frame per
        parsed type is not merely accepted but ACTED ON, so a parser narrowed
        to the exact minimum could not pass the truncation probes alone."""
        self.rep.section("the accept side of the length oracle: one "
                         "over-minimum frame per parsed type, accepted "
                         "and ACTED ON")
        # The truncation probes prove one byte below each per-type minimum
        # is refused; without this section nothing proves an octet ABOVE it
        # is accepted, so a parser narrowed to exact length would pass the
        # whole campaign (issue #217 -- Announce alone had incidental
        # coverage through the qualification fixtures). One probe per
        # parsed type carries the same legal 12-octet suffix TLV
        # (11.4.2.2: messageLength counts through the last TLV; 11.4.1: an
        # unrecognized TLV is ignored) and must be acted on downstream --
        # parser admission alone could pass against a plane that admits
        # and then discards. Each probe's teeth are proven by its own
        # planted narrowing, N10 to N15 in the README's mutation table:
        # restrict the parser's declared-length arm to that one type's
        # exact minimum and the probe here goes red by name.
        suf = wire.ptp_suffix_tlv()

        # Sync and Follow_Up: consumed and STEERED. The steering deltas
        # (3 us, 7 us) are values no earlier section leaves in the servo,
        # so the offset landing near them proves THIS pair was consumed.
        self.master = (GMID, 100)
        self.refresh_master()
        self.tick(2)

        self._suffix_steer("suffixed Sync, 44 plus 12 declared 56",
                           3000, suf, b"")
        self._suffix_steer("suffixed Follow_Up, 76 plus 12 declared 88",
                           7000, b"", suf)

        # Pdelay_Req: ANSWERED. Same downstream oracle as the reserved-
        # garbage probe: the responder role only sees a request the parser
        # admitted.
        self.drain_tx()
        seq = 0x51A0
        before = self.state()
        after = self.send(wire.ptp_pdelay_req(
            sequence_id=seq, suffix=suf, source_clock_identity=PEER2_CID,
            source_port_number=2, src=wire.GPTP_PEER2_MAC))
        self.rep.eq("suffixed Pdelay_Req, 54 plus 12 declared 66: parser "
                    "drop counter unmoved",
                    after[S_RXDROP], before[S_RXDROP])
        resp = self.wait_tx(wire.PTP_PDELAY_RESP, SECOND)
        self.rep.ck("suffixed Pdelay_Req, 54 plus 12 declared 66: answered "
                    "with its own sequence",
                    resp is not None and
                    wire.PtpMsg(resp).sequence_id == seq,
                    "seq=%s" % (resp and wire.PtpMsg(resp).sequence_id))

        # Pdelay_Resp and Pdelay_Resp_Follow_Up: the pair COMPLETES the
        # exchange -- the published neighborPropDelay is re-measured from
        # it. One hand exchange per type, the suffix on that type's frame
        # only, so a narrowing refuses exactly the frame under test: a
        # dropped Resp arms nothing and a dropped Follow_Up completes
        # nothing, and in both cases the delay stands still. The hand
        # exchange's timing is not the bench responder's (t4 - t1 spans
        # the observation ticks), so the delay it publishes is a value no
        # real exchange leaves; the recovery ladder behind each -- the
        # same one the foreign-portNumber probe proved -- re-measures and
        # re-climbs before anything else is graded.
        self._suffix_exchange("suffixed Pdelay_Resp, 54 plus 12 declared 66",
                              suf, b"")
        self._suffix_exchange("suffixed Pdelay_Resp_Follow_Up, 54 plus 12 "
                              "declared 66", b"", suf)

        # Announce: ADOPTED, and NAMED for length acceptance. Until this
        # probe the only over-minimum Announce acceptances were the
        # qualification fixtures and the 12-hop cap probe, whose lengths
        # are incidental to their purpose (issue #217): narrow any of
        # them for its own reason and the coverage vanished in silence.
        self.become_gm()
        before = self.state()
        self.send(wire.ptp_announce(
            sequence_id=self.nseq("announce"), gm_identity=0x7777,
            gm_priority1=100, source_clock_identity=PEER2_CID,
            src=wire.GPTP_PEER2_MAC, suffix=suf))
        after = self.tick(2)
        self.rep.eq("suffixed Announce, 76 plus 12 declared 88: parser "
                    "drop counter unmoved",
                    after[S_RXDROP], before[S_RXDROP])
        self.rep.eq("suffixed Announce, 76 plus 12 declared 88: length "
                    "accepted, better vector ADOPTED",
                    self.gm_of(after), 0x7777)
        # let the adopted vector expire: the next section starts from GM
        self.become_gm()

    # ---------------------------------------------------------- 11 cease
    def cease(self) -> None:
        """Milan 4.2.6.2.5: consecutive multi-responder intervals stop the
        Pdelay_Req cadence and the cease countdown restores it, while
        duplicates from ONE identity are not a storm and stop nothing."""
        self.rep.section("Milan 4.2.6.2.5: multiple responders cease "
                         "Pdelay_Req; duplicates do not")
        self.responder(False)

        def answer(req: bytes, cids: Sequence[int]) -> None:
            """Answer one Pdelay_Req with a Resp and Resp_Follow_Up from
            each identity in `cids`."""
            m = wire.PtpMsg(req)
            st = self.state()
            t2 = self.phc_of(st) + 5_000_000
            for i, cid in enumerate(cids):
                self.send(wire.ptp_pdelay_resp(
                    sequence_id=m.sequence_id, t2_ns=t2,
                    requesting_clock_identity=OUR_CID,
                    source_clock_identity=cid,
                    src=wire.GPTP_PEER2_MAC if i else wire.GPTP_PEER_MAC))
                self.send(wire.ptp_pdelay_resp_fu(
                    sequence_id=m.sequence_id, t3_ns=t2 + 200,
                    requesting_clock_identity=OUR_CID,
                    source_clock_identity=cid,
                    src=wire.GPTP_PEER2_MAC if i else wire.GPTP_PEER_MAC))

        def serve(blocks: int, cids: Sequence[int]) -> int:
            """Answer EVERY Pdelay_Req over `blocks`, in fine steps.

            The cease streak (4.2.6.2.5) needs CONSECUTIVE multi-answered
            intervals, so no request may go unanswered — wait_tx can skip a
            whole interval between its 150-block ticks, which resets the
            streak. Stepping finely and answering each request keeps it.
            """
            seen, done = 0, 0
            while done < blocks:
                n = min(20, blocks - done)
                self.tick(n)
                done += n
                while self.scan < len(self.txq):
                    f = self.txq[self.scan]
                    self.scan += 1
                    if len(f) > 14 and (f[14] & 0xF) == wire.PTP_PDELAY_REQ:
                        answer(f, cids)
                        seen += 1
            return seen

        # multi-identity intervals: answer every request with TWO identities;
        # requests must stop within a handful of intervals
        self.drain_tx()
        seen = serve(10 * 200, (PEER_CID, PEER2_CID))
        self.rep.ck("multi-identity intervals were answered", seen >= 3,
                    "answered=%d" % seen)
        self.drain_tx()
        mark = len(self.txq)
        self.tick(2 * 200)                        # two quiet intervals
        quiet = len(self.tx_of_type(wire.PTP_PDELAY_REQ, mark))
        self.rep.eq("multiple responders: requests CEASE (4.2.6.2.5)",
                    quiet, 0)
        resumed = self.wait_tx(wire.PTP_PDELAY_REQ, 8 * SECOND)
        self.rep.ck("requests resume after the cease timer",
                    resumed is not None)
        # duplicates from ONE identity are not a storm: many single-identity
        # intervals must NOT cease the requests
        self.drain_tx()
        kept = serve(6 * 200, (PEER_CID, PEER_CID))
        self.rep.ck("duplicate responses never cease the requests",
                    kept >= 4, "kept=%d" % kept)
        self.responder(True)

    # --------------------------------------------------------- 12 storms
    def storms(self, models: dict[str, tsn_model.Message], rounds: int) -> None:
        """Constrained-random illegal frames from every model, against the
        asCapable canary: the verdict must SURVIVE the storm, the drop count
        must only rise, and the plane must still adopt a master afterwards."""
        # climb FIRST (it opens its own section) so the storm checks below
        # are attributed to the storm section, not the re-climb
        st0 = self.state()
        if not (st0[S_FLAGS] & FL_ASCAP):
            self.climb("re-climb before the storm")
        self.rep.section("constrained-random storms + the asCapable canary")
        st0 = self.state()
        rnd = random.Random(self.seed ^ 0x8021A5)
        sent = 0
        st = st0
        for idx, (kind, _yml) in enumerate(MODELS):
            m = models.get(kind)
            if m is None:
                continue
            sets = m.random(rounds, self.seed + idx)
            self.rep.ck("%s: tsn-gen produced random field sets" % kind,
                        len(sets) > 0, "%d sets" % len(sets))
            for fs in sets:
                kw = {}
                for name in HDR_FIELDS:
                    if name in fs:
                        kw[name] = int(fs[name])
                kw.pop("message_length", None)     # length follows the body
                # pdelay answers now carry OUR requestingPortIdentity and
                # random sequence ids: since FPGA-gPTP #8 the 11.2.15.3
                # pairing is what filters them, so the storm drives the
                # qualification itself instead of being kept away from it
                # by a foreign requester (which the parser's own arm
                # already refused). The multi-responder cease is section
                # 10's; here the canary is that none of this moves
                # asCapable.
                if kind in ("pdelay_resp", "pdelay_resp_fu"):
                    kw["source_clock_identity"] = PEER2_CID
                    kw["requesting_clock_identity"] = OUR_CID
                    kw["sequence_id"] = 0xEE00 + (sent & 0xFF)
                build = BUILD[kind]
                if kind == "announce":
                    kw.setdefault("sequence_id", self.nseq("announce"))
                    frame = build(gm_identity=int(fs.get("gm_identity", 0)),
                                  gm_priority1=254, **kw)
                else:
                    kw.setdefault("sequence_id", self.nseq(kind))
                    frame = build(**kw)
                if rnd.random() < 0.2:
                    cut = rnd.randrange(1, len(frame))
                    frame = frame[:cut]
                st = self.send(frame)
                sent += 1
                if st is None:
                    break
            self.rep.ck("%s storm: DUT answered every frame" % kind,
                        st is not None, "%d frames" % len(sets))
        end = self.state()
        self.rep.ck("STATE STABLE: asCapable survived the storms",
                    end[S_FLAGS] & FL_ASCAP, "flags=%x" % end[S_FLAGS])
        self.rep.ck("storm drops counted monotonically",
                    end[S_RXDROP] >= st0[S_RXDROP], "rx_drop=%d" % end[S_RXDROP])
        self.rep.note("storm: %d frames, rx_drop %d -> %d"
                      % (sent, st0[S_RXDROP], end[S_RXDROP]))
        # liveness: the plane still adopts and still serves sync
        self.refresh_master()
        self.tick(2)
        st = self.state()
        self.rep.eq("STATE STABLE: still adopts the master after the storms",
                    self.gm_of(st), GMID)

    # -------------------------------------------------------- 13 drought
    def drought(self) -> None:
        """The other side of the canary: asCapable must FALL once the
        exchanges stop -- a plane still claiming it through a response
        drought lies to every AVB consumer above it -- and climb again when
        they resume."""
        self.rep.section("the two-sided canary: asCapable falls in a "
                         "response drought, then climbs again")
        self.responder(False)
        st = self.state()
        spent = 0
        while (st[S_FLAGS] & FL_ASCAP) and spent < 14 * SECOND:
            st = self.tick(200)
            spent += 200 * 10000
        self.rep.eq("drought: asCapable FELL (no asCapable lie)",
                    st[S_FLAGS] & FL_ASCAP, 0)
        st = self.climb("recovery")
        # assert asCapable SPECIFICALLY: FL_PRESENT|FL_ASCAP is truthy on
        # FL_PRESENT alone and could never fail (the vacuous-guard lesson)
        self.rep.eq("recovery: asCapable is whole again after the campaign",
                    st[S_FLAGS] & FL_ASCAP, FL_ASCAP)
        # a positive control for the tap-drop counter, which every other
        # probe only ever asserts UNMOVED: a >2 KB gPTP frame overflows the
        # tap FIFO and must be counted, so a stuck-at-0 dbg_tap_drop_o fails
        before = self.state()
        storm = wire.ptp_sync(sequence_id=0x7EEE) + bytes(3000)
        after = self.send(storm)
        self.rep.ck("tap-drop counter has a positive control (oversize drop)",
                    after[S_TAPDROP] > before[S_TAPDROP],
                    "tap_drop %d -> %d" % (before[S_TAPDROP], after[S_TAPDROP]))
