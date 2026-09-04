#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""fuzz_ptp_responder.py - section 7 of the gPTP campaign: the Pdelay
responder role, in full - conformance, the refusals, the pairing rules, replay,
the port number and the port-number width.

WHAT A SECTION MAY ASSUME.  These methods are mixed into
`fuzz_ptp.Campaign` and reach the DUT only through the primitives that class
defines - `self.op/state/send/tick/reset/quiet_window/stable/...` and
`self.rep`, the `cosim.Report` every check is recorded in.  Nothing here holds
state of its own; the split is by SECTION, so one area of the campaign can be
read and changed without opening the other two."""

import tsn_model
import wire

from fuzz_ptp_defs import (FL_ASCAP, OUR_CID, PEER2_CID, PEER_CID, SECOND,
                           S_FLAGS, S_PDELAY, S_PDEXP, S_RXDROP)


class PtpResponderSections:
    """Section 7, mixed into `fuzz_ptp.Campaign`."""

    # ------------------------------------------- 7 the responder role
    def _unpaired_probe(self, label, frame):
        """A frame the pairing must not take: no delay, no asCapable move."""
        before = self.state()
        after = self.send(frame)
        self.rep.eq("%s: peer delay unmoved" % label,
                    after[S_PDELAY], before[S_PDELAY])
        self.rep.eq("%s: asCapable unmoved" % label,
                    after[S_FLAGS] & FL_ASCAP,
                    before[S_FLAGS] & FL_ASCAP)
        self.stable(label, before, after)

    def _responder_conformance(self, models):
        """A legal Pdelay_Req is answered and paired; an illegal one is not."""
        self.drain_tx()
        seq = 0x4321
        before = self.state()
        self.send(wire.ptp_pdelay_req(sequence_id=seq,
                                      source_clock_identity=PEER2_CID,
                                      source_port_number=2,
                                      src=wire.GPTP_PEER2_MAC))
        resp = self.wait_tx(wire.PTP_PDELAY_RESP, SECOND)
        if self.rep.ck("Pdelay_Resp answers the request", resp is not None):
            rm = wire.PtpMsg(resp)
            self.grade_tx(models["pdelay_resp"], resp, "tx_pdresp",
                          skip=("request_receipt_seconds",
                                "request_receipt_ns",
                                "requesting_clock_identity",
                                "requesting_port_number"))
            self.rep.eq("tx_pdresp echoes the sequence", rm.sequence_id, seq)
            self.rep.eq("tx_pdresp requestingPortIdentity",
                        (rm.requesting_clock_identity,
                         rm.requesting_port_number), (PEER2_CID, 2))
            self.rep.eq("tx_pdresp source identity is ours",
                        rm.source_clock_identity, OUR_CID)
            after = self.state()
            t2 = rm.ts_total_ns
            self.rep.ck("tx_pdresp t2 is live fabric time",
                        self.phc_of(before) <= t2 <= self.phc_of(after),
                        "t2=%d window=[%d,%d]" % (t2, self.phc_of(before),
                                                  self.phc_of(after)))
            rfu = self.wait_tx(wire.PTP_PDELAY_RESP_FU, SECOND)
            if self.rep.ck("Pdelay_Resp_Follow_Up pairs it",
                           rfu is not None):
                fm = wire.PtpMsg(rfu)
                self.grade_tx(models["pdelay_resp_fu"], rfu, "tx_pdrfu",
                              skip=("response_origin_seconds",
                                    "response_origin_ns",
                                    "requesting_clock_identity",
                                    "requesting_port_number"))
                self.rep.eq("tx_pdrfu echoes the sequence",
                            fm.sequence_id, seq)
                self.rep.eq("tx_pdrfu requestingPortIdentity",
                            (fm.requesting_clock_identity,
                             fm.requesting_port_number), (PEER2_CID, 2))
                self.rep.ck("t3 after t2, same clock",
                            fm.ts_total_ns >= t2,
                            "t2=%d t3=%d" % (t2, fm.ts_total_ns))
        # a request the parser must refuse draws NO response
        self.drain_tx()
        self.send(wire.ptp_pdelay_req(sequence_id=0x4399, version_ptp=3,
                                      source_clock_identity=PEER2_CID,
                                      src=wire.GPTP_PEER2_MAC))
        self.tick(20)
        bad = [f for f in self.tx_of_type(wire.PTP_PDELAY_RESP)
               if wire.PtpMsg(f).sequence_id == 0x4399]
        self.rep.eq("a version-3 request draws no response", len(bad), 0)
        # a request in a foreign domain draws no response either: the same
        # header drop arm covers the responder role (8.1; FPGA-gPTP #6)
        self.drain_tx()
        before = self.state()
        after = self.send(wire.ptp_pdelay_req(sequence_id=0x4398,
                                              domain_number=5,
                                              source_clock_identity=PEER2_CID,
                                              src=wire.GPTP_PEER2_MAC))
        self.rep.eq("a domain-5 request: dropped and counted",
                    after[S_RXDROP], before[S_RXDROP] + 1)
        self.tick(20)
        bad = [f for f in self.tx_of_type(wire.PTP_PDELAY_RESP)
               if wire.PtpMsg(f).sequence_id == 0x4398]
        self.rep.eq("a domain-5 request draws no response", len(bad), 0)

    def _responder_refusals(self):
        """Every short Pdelay_Req shape is refused ahead of the responder."""

        # 802.1AS-2011 Table 11-11 gives the Pdelay_Req 54 octets: the
        # 34-octet header and TWO ten-octet reserved fields (IEEE 1588-2008
        # 13.9 pads the request to the response's length so the timestamps
        # traverse identical paths). Three shapes, one per way of falling
        # short, refused at the parser ahead of the responder so none draws
        # the Pdelay_Resp + Resp_Follow_Up pair that would put our t2 and
        # t3 on the wire (FPGA-gPTP #12): the issue's header-only request
        # (48 bytes, declaring an honest 34, refused by both the byte-count
        # gate and the declared bound); one declaring the true 54 but cut
        # at 67 bytes (the byte-count gate alone); and one physically
        # complete at 68 bytes that LIES, declaring 34 (the declared bound
        # alone -- without it the first two shapes leave that arm
        # untested, since neither is a messageLength inconsistency).
        for label, seq, frame in (
                ("header-only Pdelay_Req (48 B)", 0x4396,
                 wire.ptp_pdelay_req(
                     sequence_id=0x4396, body_octets=0,
                     source_clock_identity=PEER2_CID,
                     src=wire.GPTP_PEER2_MAC)),
                ("Pdelay_Req declaring 54 cut at 67 B", 0x4397,
                 wire.ptp_pdelay_req(
                     sequence_id=0x4397,
                     source_clock_identity=PEER2_CID,
                     src=wire.GPTP_PEER2_MAC)[:67]),
                # the DECLARED arm on its own: all 68 bytes are present and
                # only messageLength lies, so the byte-count gate cannot
                # refuse this one and the header arm at octets 2..3 is the
                # only thing that can. 34 is the header-only length the
                # issue's shape declared honestly; here it is a lie
                ("complete Pdelay_Req declaring messageLength 34", 0x4394,
                 wire.ptp_pdelay_req(
                     sequence_id=0x4394, message_length=34,
                     source_clock_identity=PEER2_CID,
                     src=wire.GPTP_PEER2_MAC))):
            self.drain_tx()
            before = self.state()
            after = self.send(frame)
            self.rep.eq("%s: dropped and counted" % label,
                        after[S_RXDROP], before[S_RXDROP] + 1)
            self.stable(label, before, after)
            self.tick(20)
            self.rep.eq("%s: no Pdelay_Resp" % label,
                        len([f for f in self.tx_of_type(wire.PTP_PDELAY_RESP)
                             if wire.PtpMsg(f).sequence_id == seq]), 0)
            self.rep.eq("%s: no Pdelay_Resp_Follow_Up" % label,
                        len([f for f in
                             self.tx_of_type(wire.PTP_PDELAY_RESP_FU)
                             if wire.PtpMsg(f).sequence_id == seq]), 0)

    def _responder_pairing(self):
        """The complete request pairs, and nothing pairs while nothing is armed."""
        # neither refusal poisons the responder: the complete 54-octet
        # request right after them is answered with its own sequence
        self.drain_tx()
        good_seq = 0x4395
        self.send(wire.ptp_pdelay_req(sequence_id=good_seq,
                                      source_clock_identity=PEER2_CID,
                                      source_port_number=2,
                                      src=wire.GPTP_PEER2_MAC))
        resp = self.wait_tx(wire.PTP_PDELAY_RESP, SECOND)
        self.rep.ck("a complete request after the refusals is answered",
                    resp is not None and
                    wire.PtpMsg(resp).sequence_id == good_seq,
                    "seq=%s" % (resp and wire.PtpMsg(resp).sequence_id))
        rfu = self.wait_tx(wire.PTP_PDELAY_RESP_FU, SECOND)
        self.rep.ck("its Resp_Follow_Up pairs it",
                    rfu is not None and
                    wire.PtpMsg(rfu).sequence_id == good_seq,
                    "seq=%s" % (rfu and wire.PtpMsg(rfu).sequence_id))

        # 802.1AS-2011 11.2.15.3 (Figure 11-8): a Pdelay_Resp_Follow_Up is
        # consumed ONLY behind the Pdelay_Resp that answered our outstanding
        # request, from that responder. Hard assertions since FPGA-gPTP #8;
        # each unmatched frame carries our requestingPortIdentity, so
        # nothing but the pairing rule can refuse it, and a consumed one
        # would publish its own t3 and clear asCapable.
        # (a) NOTHING ARMED. Until a Pdelay_Resp answers our outstanding
        # request the pairing register holds no sequence, and every
        # Follow_Up must be refused on that alone.
        self._unpaired_probe(
            "stale Pdelay_Resp_Follow_Up ignored (11.2.15.3)",
            wire.ptp_pdelay_resp_fu(
                sequence_id=0xEEEE, t3_ns=1000,
                requesting_clock_identity=OUR_CID,
                source_clock_identity=PEER_CID))
        # sequence 0 ahead of any Pdelay_Resp: "armed with sequence 0" is
        # not "nothing armed", so a pairing register cleared to zero must
        # not read as a match
        self._unpaired_probe(
            "sequence-0 Pdelay_Resp_Follow_Up ahead of its Resp ignored",
            wire.ptp_pdelay_resp_fu(
                sequence_id=0, t3_ns=3000,
                requesting_clock_identity=OUR_CID,
                source_clock_identity=PEER_CID))


    def _pairing_domain_arm(self, oseq, armed_t2):
        """A foreign-domain response pair never reaches the pairing at all."""
        # #207 item 1: a foreign-domain response pair never reaches the
        # pairing at all (8.1; IEEE 1588-2008 9.5.1) and is counted
        # twice. It carries the plane's OWN outstanding sequenceId and
        # our requestingPortIdentity, so nothing but the domainNumber
        # arm can refuse it: were that arm removed the Resp would arm
        # the pairing and the Follow_Up would complete the exchange,
        # which is what makes "peer delay unmoved" load-bearing here.
        before = self.state()
        self.send(wire.ptp_pdelay_resp(
            sequence_id=oseq, t2_ns=armed_t2, domain_number=5,
            requesting_clock_identity=OUR_CID,
            source_clock_identity=PEER_CID))
        after = self.send(wire.ptp_pdelay_resp_fu(
            sequence_id=oseq, t3_ns=armed_t2 + 200, domain_number=5,
            requesting_clock_identity=OUR_CID,
            source_clock_identity=PEER_CID))
        self.rep.eq(
            "domain-5 Pdelay response pair: both dropped and counted",
            after[S_RXDROP], before[S_RXDROP] + 2)
        self.rep.eq("domain-5 Pdelay response pair: peer delay unmoved",
                    after[S_PDELAY], before[S_PDELAY])
        self.stable("domain-5 Pdelay response pair", before, after)


    def _pairing_sequence_arms(self, oseq, armed_t2):
        """The sequenceId and requestingPortIdentity arms of Figure 11-8."""
        # the RESP half of the same pairing (Figure 11-8's
        # WAITING_FOR_PDELAY_RESP arm): a Pdelay_Resp whose sequenceId
        # is not the outstanding one must arm NOTHING, so the Follow_Up
        # behind it cannot complete an exchange either. The low bytes
        # agree, so a Resp compare narrowed to one byte arms here and
        # the pair then publishes its own delay.
        wrong = (oseq ^ 0x0100) & 0xFFFF
        self.send(wire.ptp_pdelay_resp(
            sequence_id=wrong, t2_ns=armed_t2,
            requesting_clock_identity=OUR_CID,
            source_clock_identity=PEER_CID))
        self._unpaired_probe(
            "Pdelay_Resp at seq ^ 0x0100 arms nothing (11.2.15.3)",
            wire.ptp_pdelay_resp_fu(
                sequence_id=wrong, t3_ns=armed_t2 + 200,
                requesting_clock_identity=OUR_CID,
                source_clock_identity=PEER_CID))

        # 11.2.15.3 (Figure 11-8, WAITING_FOR_PDELAY_RESP), the THIRD
        # arm of that state: besides the sequenceId and the domain, a
        # Pdelay_Resp is taken only when its requestingPortIdentity is
        # OURS. The figure qualifies the WHOLE identity, clockIdentity
        # AND portNumber, and since the pin this PR advances to the
        # engine compares both (prog_rx_pdresp: bank word 6 against
        # S_CID, bank word 7 against OUR_PORTNUM_C, one branch each).
        # This probe drives
        # the clockIdentity half; the portNumber half is driven at the
        # end of this section, on its own exchange, as an ordinary
        # assertion (FPGA-gPTP #36, landed).
        # Every other probe in this section carries OUR_CID -
        # correctly, since they drive the sequence and responder
        # compares - so nothing drove this one, and the arm could be
        # deleted in silence (issue #223 measured exactly that: with it
        # gone the whole campaign stayed green).
        #
        # This Pdelay_Resp is right in every other respect: the plane's
        # own outstanding sequenceId, domain 0, from the usual
        # responder. Only the requestingPortIdentity is a stranger's,
        # so nothing but this arm can refuse it -- which is what makes
        # the Follow_Up behind it load-bearing. That Follow_Up carries
        # OUR_CID and is otherwise perfect, so it would complete the
        # exchange the instant the Resp armed anything: the delay it
        # would publish is a delay measured against a conversation
        # between two other stations.
        self.send(wire.ptp_pdelay_resp(
            sequence_id=oseq, t2_ns=armed_t2,
            requesting_clock_identity=PEER2_CID,
            source_clock_identity=PEER_CID))
        self._unpaired_probe(
            "Pdelay_Resp for another requester arms nothing (11.2.15.3)",
            wire.ptp_pdelay_resp_fu(
                sequence_id=oseq, t3_ns=armed_t2 + 200,
                requesting_clock_identity=OUR_CID,
                source_clock_identity=PEER_CID))


    def _pairing_identity_arms(self, oseq, armed_t2, oreq):
        """With the pairing armed for real, what the Follow_Up compares refuse."""
        # arm it for real: domain 0, our requestingPortIdentity, the
        # plane's outstanding sequenceId, from the usual responder
        self.send(wire.ptp_pdelay_resp(
            sequence_id=oseq, t2_ns=armed_t2,
            requesting_clock_identity=OUR_CID,
            source_clock_identity=PEER_CID))
        # the armed sequence with its HIGH byte flipped: the low bytes
        # agree, so a compare narrowed to one byte takes this frame and
        # publishes its t3
        self._unpaired_probe(
            "ARMED: Follow_Up at seq ^ 0x0100 ignored (11.2.15.3)",
            wire.ptp_pdelay_resp_fu(
                sequence_id=(oseq ^ 0x0100) & 0xFFFF,
                t3_ns=armed_t2 + 200,
                requesting_clock_identity=OUR_CID,
                source_clock_identity=PEER_CID))
        # the armed sequence from a DIFFERENT responder: Figure 11-8
        # requires the Follow_Up's sourcePortIdentity to equal the
        # Pdelay_Resp's, and this is the only probe that drives that
        # compare -- the identity half of issue #141's acceptance
        self._unpaired_probe(
            "ARMED: Follow_Up from another responder ignored (11.2.15.3)",
            wire.ptp_pdelay_resp_fu(
                sequence_id=oseq, t3_ns=armed_t2 + 200,
                requesting_clock_identity=OUR_CID,
                source_clock_identity=PEER2_CID))
        # THE ENGINE'S OWN QUALIFICATION, NOT AN ARM OF THE FIGURE.
        # The first cut of this probe called it the same Figure 11-8
        # arm as the Pdelay_Resp one above, and the #238 review was
        # right to refuse that. Figure 11-8's
        # WAITING_FOR_PDELAY_RESP_FOLLOW_UP transition qualifies the
        # Follow_Up on its sequenceId and on its sourcePortIdentity
        # equalling the stored Pdelay_Resp's -- the two compares
        # prog_leg_pdpost implements, and the two probes above are the
        # ones that drive them. It does not inspect the Follow_Up's
        # requestingPortIdentity; the engine's own header states the
        # figure's Follow_Up rule in exactly those terms. What checks
        # the requesting identity here is prog_rx_pdrfu and, for the
        # portNumber half, the head of the PDPOST leg, ahead of the
        # pairing, because the engine chose to. Worth having and worth
        # pinning -- an unimplemented arm no test drives is
        # indistinguishable from a deleted one -- but it is hardening,
        # so it is labelled hardening and is NOT conformance evidence
        # for Figure 11-8.
        #
        # The pairing is armed, and this Follow_Up carries the armed
        # sequenceId from the armed responder, so both of the figure's
        # own compares are satisfied: the requesting identity is the
        # only thing wrong with it. This probe plus the one before
        # "arm it for real" are what make the two guards separable
        # here -- deleting one must redden one probe and leave the
        # other green.
        self._unpaired_probe(
            "ARMED: Follow_Up for another requester ignored "
            "(engine hardening, not Figure 11-8)",
            wire.ptp_pdelay_resp_fu(
                sequence_id=oseq, t3_ns=armed_t2 + 200,
                requesting_clock_identity=PEER2_CID,
                source_clock_identity=PEER_CID))
        # the portNumber half of the SAME qualification, and the same
        # authority: hardening, not Figure 11-8. It is here because the
        # donor arm this PR pins (FPGA-gPTP #36) landed on both Pdelay
        # receive messages, and an arm no probe drives is
        # indistinguishable from a deleted one -- the whole reason #223
        # exists. Everything else about this Follow_Up is right: the
        # armed sequenceId, the armed responder, OUR clockIdentity. The
        # portNumber is DERIVED from the plane's own, never written
        # down, so it cannot quietly become a probe at our own port.
        self._unpaired_probe(
            "ARMED: Follow_Up at a foreign requesting portNumber "
            "ignored (engine hardening, not Figure 11-8)",
            wire.ptp_pdelay_resp_fu(
                sequence_id=oseq, t3_ns=armed_t2 + 200,
                requesting_clock_identity=OUR_CID,
                requesting_port_number=(
                    wire.PtpMsg(oreq).source_port_number ^ 0xFFFF),
                source_clock_identity=PEER_CID))

    def _responder_pairing_arms(self):
        """The armed pairing: one hand exchange, every compare driven once."""
        # (b) ARMED. The two compares of Figure 11-8's
        # WAITING_FOR_PDELAY_RESP_FOLLOW_UP arm -- the sequenceId and the
        # responder's sourcePortIdentity -- can only be exercised once the
        # pairing IS armed, and arming it needs a Pdelay_Resp carrying the
        # sequenceId of the request THE PLANE sent. That value is read from
        # the transmitted request itself: the bench's own injected-request
        # counter is a different number entirely, and a probe built on it
        # tests nothing (measured: with the counter as the base, deleting
        # either compare left this campaign green).
        # The bench responder is taken off for one exchange so the request
        # stays outstanding for us to answer by hand. That costs one lost
        # response, which the ladder absorbs; nothing here completes an
        # exchange, so no neighborPropDelay is computed and the Milan
        # 4.2.6.1.1 threshold is never approached.
        self.responder(False)
        self.drain_tx()
        oreq = self.wait_tx(wire.PTP_PDELAY_REQ, 4 * SECOND)
        if self.rep.ck("an unanswered request to arm against",
                       oreq is not None):
            oseq = wire.PtpMsg(oreq).sequence_id
            self.tick(4)
            armed_t2 = self.phc_of(self.state()) - 3000
            self._pairing_domain_arm(oseq, armed_t2)
            self._pairing_sequence_arms(oseq, armed_t2)
            self._pairing_identity_arms(oseq, armed_t2, oreq)
        self.responder(True)

    def _responder_replay(self):
        """A completed exchange cannot be completed again (Figure 11-8/Cor2)."""
        # Figure 11-8 as corrected by Cor2-2015: a COMPLETED exchange
        # cannot be completed again. The bench responder answers the
        # plane's request from PEER_CID, so replaying a Resp + Follow_Up
        # pair for that same sequenceId, from that same responder, is a
        # replay of a completed exchange. A pairing that re-armed after
        # completion would recompute neighborPropDelay from the replay and
        # publish it; the identical pair and one with t3 pushed 2 us out
        # must both leave the published delay and asCapable where the real
        # exchange left them. No drought is involved: the responder stays
        # on, so nothing here can walk the lost-response count.
        self.drain_tx()
        req = self.wait_tx(wire.PTP_PDELAY_REQ, 4 * SECOND)
        if self.rep.ck("a completed exchange to replay", req is not None):
            rseq = wire.PtpMsg(req).sequence_id
            self.tick(4)
            done = self.state()
            t2 = self.phc_of(done) - 3000

            def replay(t3_extra: int) -> list[int] | None:
                """Re-send the completed exchange's pair, with t3 moved by
                `t3_extra` nanoseconds."""
                self.send(wire.ptp_pdelay_resp(
                    sequence_id=rseq, t2_ns=t2,
                    requesting_clock_identity=OUR_CID,
                    source_clock_identity=PEER_CID))
                return self.send(wire.ptp_pdelay_resp_fu(
                    sequence_id=rseq, t3_ns=t2 + 200 + t3_extra,
                    requesting_clock_identity=OUR_CID,
                    source_clock_identity=PEER_CID))

            after = replay(0)
            self.rep.eq("identical replay of a completed pair: "
                        "peer delay unmoved", after[S_PDELAY],
                        done[S_PDELAY])
            self.rep.eq("identical replay of a completed pair: "
                        "asCapable unmoved", after[S_FLAGS] & FL_ASCAP,
                        done[S_FLAGS] & FL_ASCAP)
            after = replay(2000)
            self.rep.eq("t3-skewed replay of a completed pair: "
                        "peer delay unmoved", after[S_PDELAY],
                        done[S_PDELAY])
            self.rep.eq("t3-skewed replay of a completed pair: "
                        "asCapable unmoved", after[S_FLAGS] & FL_ASCAP,
                        done[S_FLAGS] & FL_ASCAP)


    def _responder_port_number(self):
        """The portNumber half of the Figure 11-8 requestingPortIdentity arm."""
        # ---- the portNumber half of the Figure 11-8 arm ----------------
        #
        # Figure 11-8's WAITING_FOR_PDELAY_RESP transition qualifies the
        # response on the WHOLE requestingPortIdentity - clockIdentity
        # == thisClock AND portNumber == thisPort. Until FPGA-gPTP #36
        # the engine implemented the first and not the second, and this
        # campaign reported the consequence as two tracked gaps: the pair
        # completed, neighborPropDelay was published at 4,054,625 ns
        # where the real exchange had left 599, and asCapable fell, from
        # a frame not addressed to this port. Both halves are compared at
        # the pin this PR advances to (bank word 6 against S_CID, bank
        # word 7 against OUR_PORTNUM_C in prog_rx_pdresp, and the
        # Follow_Up path's own portNumber term at the head of the PDPOST
        # leg rather than in prog_rx_pdrfu, because prog_rx_pdrfu's fixed
        # slot has exactly 48 free words behind it and that is the SERVO
        # leg's only home), so these are ORDINARY
        # ASSERTIONS now, not eq_or_gap, and the campaign carries no
        # tracked gap for #36.
        #
        # It keeps its own exchange rather than joining the ARMED block
        # above, because it is the probe that used to be allowed to
        # complete: it must stay measurable end to end, and the two
        # recovery checks behind it must keep asserting that the plane
        # re-measures and re-climbs on real exchanges. Those two are what
        # stopped a poisoned delay and a false asCapable from leaking
        # into the BTCA, servo and canary sections while the gap stood,
        # and they are what will catch a regression of this arm before
        # those sections grade a poisoned machine.
        self.responder(False)
        self.drain_tx()
        preq = self.wait_tx(wire.PTP_PDELAY_REQ, 4 * SECOND)
        if self.rep.ck("an unanswered request for the portNumber arm",
                       preq is not None):
            pseq = wire.PtpMsg(preq).sequence_id
            # DERIVED from the plane's own portNumber, never written
            # down: the complement of a 16-bit value can never equal it,
            # so this probe cannot quietly become a probe at OUR port the
            # day the plane's portNumber changes. A literal would.
            our_pn = wire.PtpMsg(preq).source_port_number
            foreign_pn = our_pn ^ 0xFFFF
            self.tick(4)
            pt2 = self.phc_of(self.state()) - 3000
            before = self.state()
            # right in every other respect: our clockIdentity, the
            # plane's own outstanding sequenceId, domain 0, the usual
            # responder. Only requestingPortIdentity.portNumber is a
            # stranger's, so THIS ARM is the only thing that can refuse
            # the pair.
            #
            # THE FOLLOW_UP CARRIES OUR OWN portNumber, and that is the
            # whole design of this probe. While the arm was missing on
            # both messages, a Follow_Up at the foreign portNumber was
            # equivalent; the moment the arm landed on both it stopped
            # being so, and a probe with the stranger's portNumber on
            # BOTH frames is refused by EITHER arm -- measured here:
            # bypassing the Pdelay_Resp arm alone left the campaign at
            # 602 pass, 0 fail, because the Follow_Up arm caught what the
            # Resp arm let through. That is a probe that cannot fail for
            # the reason it names. With a perfect Follow_Up behind it,
            # the Pdelay_Resp arm is the only thing standing between this
            # pair and a completed exchange.
            self.send(wire.ptp_pdelay_resp(
                sequence_id=pseq, t2_ns=pt2,
                requesting_clock_identity=OUR_CID,
                requesting_port_number=foreign_pn,
                source_clock_identity=PEER_CID))
            after = self.send(wire.ptp_pdelay_resp_fu(
                sequence_id=pseq, t3_ns=pt2 + 200,
                requesting_clock_identity=OUR_CID,
                requesting_port_number=our_pn,
                source_clock_identity=PEER_CID))
            gl = ("Pdelay_Resp at a foreign requesting portNumber arms "
                  "nothing (11.2.15.3)")
            self.rep.eq("%s: peer delay unmoved" % gl,
                        after[S_PDELAY], before[S_PDELAY])
            self.rep.eq("%s: asCapable unmoved" % gl,
                        after[S_FLAGS] & FL_ASCAP,
                        before[S_FLAGS] & FL_ASCAP)

    def _responder_port_width(self):
        """The full sixteen-bit portNumber compare, and the recovery after it."""
        # WIDTH-PINNING PROBE ([R2] of PR #238): a portNumber differing
        # from ours ONLY in the high byte. The complement probe above
        # differs in both bytes, so a compare silently narrowed below 16
        # bits would still refuse it -- the same silent-narrowing class
        # the clockIdentity half was bitten by (FPGA-gPTP #30). This pair
        # is refused only by the full 16-bit compare: same design, the
        # stranger's portNumber on the RESPONSE only, a perfect Follow_Up
        # behind it. The N9 plant (donor FMT_W narrowed to FMT_B) reddens
        # exactly this probe and no other.
        self.drain_tx()
        preq = self.wait_tx(wire.PTP_PDELAY_REQ, 4 * SECOND)
        if self.rep.ck("an unanswered request for the portNumber width "
                       "probe", preq is not None):
            pseq = wire.PtpMsg(preq).sequence_id
            our_pn = wire.PtpMsg(preq).source_port_number
            hi_pn = our_pn ^ 0xFF00
            self.tick(4)
            pt2 = self.phc_of(self.state()) - 3000
            before = self.state()
            self.send(wire.ptp_pdelay_resp(
                sequence_id=pseq, t2_ns=pt2,
                requesting_clock_identity=OUR_CID,
                requesting_port_number=hi_pn,
                source_clock_identity=PEER_CID))
            after = self.send(wire.ptp_pdelay_resp_fu(
                sequence_id=pseq, t3_ns=pt2 + 200,
                requesting_clock_identity=OUR_CID,
                requesting_port_number=our_pn,
                source_clock_identity=PEER_CID))
            gl = ("Pdelay_Resp at a high-byte-only foreign requesting "
                  "portNumber arms nothing (11.2.15.3, 16-bit compare)")
            self.rep.eq("%s: peer delay unmoved" % gl,
                        after[S_PDELAY], before[S_PDELAY])
            self.rep.eq("%s: asCapable unmoved" % gl,
                        after[S_FLAGS] & FL_ASCAP,
                        before[S_FLAGS] & FL_ASCAP)
        self.responder(True)
        # whatever this probe disturbs, the plane must repair from real
        # exchanges before the next section starts. Hard assertions, and
        # they were load-bearing while the arm was missing: if the plane
        # could NOT re-measure and re-climb, every section after this one
        # would be grading a poisoned machine. They stay, because that is
        # exactly the state a regression of the arm would leave behind.
        st = self.state()
        spent = 0
        while not (st[S_FLAGS] & FL_ASCAP) and spent < 16 * SECOND:
            st = self.tick(200)
            spent += 200 * 10000
        self.rep.eq("after the foreign portNumber probe: asCapable is whole",
                    st[S_FLAGS] & FL_ASCAP, FL_ASCAP)
        self.rep.ck("after the foreign portNumber probe: the delay is "
                    "re-measured from real exchanges",
                    abs((st[S_PDELAY] & 0xFFFFFFFF) - st[S_PDEXP]) <= 32,
                    "pdelay=%d expect=%d" % (st[S_PDELAY], st[S_PDEXP]))

    def responder_correct(self, models: dict[str, tsn_model.Message]) -> None:
        """The Pdelay responder role: a legal request is answered and the
        exchange pairs, while every refusal, replay and mismatched identity
        arm leaves the delay and asCapable exactly where they were."""
        self.rep.section("pdelay responder: Resp + Resp_Follow_Up conform")
        self._responder_conformance(models)
        self._responder_refusals()
        self._responder_pairing()
        self._responder_pairing_arms()
        self._responder_replay()
        self._responder_port_number()
        self._responder_port_width()
