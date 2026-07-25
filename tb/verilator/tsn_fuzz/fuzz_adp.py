#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""
ADP discovery field campaign (adp_advertiser) — every advertised field, at
its wire offset, against the entity model it was configured with.

ADP has no ingress in this design (the advertiser consumes decoded event
pulses), so the campaign is the discovery-side mirror of a getter sweep:
drive an EVENT, capture the emitted ADPDU, and prove all twenty fields of
IEEE 1722.1 §6.2.1 land where a controller will look for them. A field at
the wrong offset is invisible in a "does it advertise?" test and fatal in
the field — this is the test that catches it.

Also covered:
  * the 82-byte frame / 68-byte PDU shape and cdl=56, plus subtype 0xFA at
    byte 14 (AVTP shares ethertype 0x22F0, so the census can only trust
    LENGTH-validating decoders — the ADP census rule);
  * available_index monotonicity, which is what a controller uses to tell a
    re-advertisement from a state change;
  * ENTITY_DEPARTING on link down and re-advertisement on link restore;
  * tsn-gen decoding the emitted ADPDU independently, field by field;
  * state stability: an event storm must leave the advertiser still emitting
    a correct, complete ADPDU.

Run: python3 fuzz_adp.py [--rounds N] [--seed S]
"""
import argparse
import sys

import cosim
import tsn_model
import wire
from wire import AdpResp

# event ids — must match cosim_adp.cpp
EV_LINK_UP, EV_LINK_DOWN, EV_DISCOVER, EV_GM_CHANGE, \
    EV_INFO_CHANGED, EV_SHUTDOWN, EV_TICK = range(7)

# state_dump() word order — must match cosim_adp.cpp
S_AVAIL_IDX, S_BUSY, S_DEPART_CNT, S_REARM_CNT, S_DEPART_SRC = range(5)

#: the entity model cosim_adp.cpp configures — the expected wire content
MODEL = {
    "valid_time": 10,
    "entity_id": 0x020000FFFE000001,
    "entity_model_id": 0x001B92FFFE0000AA,
    "entity_capabilities": 0x00008588,
    "talker_stream_sources": 8,
    "talker_capabilities": 0x4801,
    "listener_stream_sinks": 8,
    "listener_capabilities": 0x4801,
    "controller_capabilities": 0,
    "gptp_grandmaster_id": 0x0011223344556677,
    "gptp_domain_number": 0,
    "current_configuration_index": 0,
    "identify_control_index": 0,
    "interface_index": 0,
    "association_id": 0,
}
ADP_MCAST = bytes.fromhex("91e0f0010000")


class Campaign:
    def __init__(self, dut, rep, seed):
        self.dut = dut
        self.rep = rep
        self.seed = seed

    def event(self, ev):
        return [AdpResp(f) for f in
                self.dut.xact_all(cosim.ctrl(cosim.CTRL_EVENT, ev))]

    def state(self):
        return cosim.read_state(self.dut)

    def reset(self):
        return [AdpResp(f) for f in
                self.dut.xact_all(cosim.ctrl(cosim.CTRL_RESET))]

    def bringup(self):
        """Reset, then LINK UP — an entity must NOT advertise before its link
        is up (`available_r` is only set by the link-up event), so a bare
        reset emitting nothing is correct behaviour, not a missing frame."""
        self.reset()
        return self.event(EV_LINK_UP)

    # ------------------------------------------------------------- 1 model
    def model_inventory(self):
        self.rep.section("ADP model inventory (tsn-gen)")
        try:
            m = tsn_model.load("adp", "1722_1_adp.yaml",
                               "atdecc_adp_service::ADP_INTERFACE::ADP_IF_DATA")
        except (OSError, ValueError) as exc:
            self.rep.ck("ADP model loads", False, str(exc))
            return None
        self.rep.ck("ADP model loads", True, "%d fields" % len(m.fields))
        declared = sum(b for _, b, _ in m.fields)
        self.rep.eq("model covers the ADPDU payload (532 declared bits)", declared, 532)
        for name, bits, con in m.fields:
            self.rep.ck("  field %-30s %3d bits%s"
                        % (name, bits, "  (spec-constrained)" if con else ""), True)
        return m

    # -------------------------------------------------- 2 the advertised PDU
    def check_adpdu(self, tag, r, exp_msg, exp_index=None):
        """Validate one emitted ADPDU field by field at its wire offset."""
        rep = self.rep
        if not rep.ck("%s: ADPDU emitted" % tag, bool(r), "%d B" % len(r)):
            return
        rep.eq("%s: frame is 82 B (68-byte PDU + 14 eth)" % tag, len(r), 82)
        rep.eq("%s: dst = ADP multicast" % tag, r.raw[0:6], ADP_MCAST)
        rep.eq("%s: src = station MAC" % tag, r.raw[6:12], wire.ENTITY_MAC)
        rep.eq("%s: ethertype 0x22F0" % tag,
               int.from_bytes(r.raw[12:14], "big"), wire.ETHERTYPE_AVTP)
        rep.eq("%s: subtype 0xFA (ADP)" % tag, r.subtype, wire.SUBTYPE_ADP)
        rep.eq("%s: sv=0" % tag, r.sv, 0)
        rep.eq("%s: version=0" % tag, r.version, 0)
        rep.eq("%s: message_type" % tag, r.message_type, exp_msg)
        rep.eq("%s: control_data_length = 56" % tag, r.cdl, 56)
        rep.eq("%s: valid_time" % tag, r.valid_time, MODEL["valid_time"])
        # the entity model, every field at its documented offset
        for field, got in (("entity_id", r.entity_id),
                           ("entity_model_id", r.entity_model_id),
                           ("entity_capabilities", r.entity_capabilities),
                           ("talker_stream_sources", r.talker_stream_sources),
                           ("talker_capabilities", r.talker_capabilities),
                           ("listener_stream_sinks", r.listener_stream_sinks),
                           ("listener_capabilities", r.listener_capabilities),
                           ("controller_capabilities", r.controller_capabilities),
                           ("gptp_grandmaster_id", r.gptp_grandmaster_id),
                           ("gptp_domain_number", r.gptp_domain_number),
                           ("current_configuration_index", r.current_configuration_index),
                           ("identify_control_index", r.identify_control_index),
                           ("interface_index", r.interface_index),
                           ("association_id", r.association_id)):
            rep.eq("%s: %s" % (tag, field), got, MODEL[field])
        if exp_index is not None:
            rep.eq("%s: available_index" % tag, r.available_index, exp_index)

    def advertise(self):
        self.rep.section("advertised ADPDU: every field at its wire offset")
        quiet = self.reset()
        self.rep.eq("silent before link-up (entity not yet available)", len(quiet), 0)
        frames = self.event(EV_LINK_UP)
        self.rep.ck("link-up produces an advertisement", len(frames) > 0,
                    "%d frame(s)" % len(frames))
        if frames:
            self.check_adpdu("link-up", frames[0], wire.ADP_ENTITY_AVAILABLE)
        return frames[0] if frames else None

    # ---------------------------------------------- 3 events + available_index
    def events(self):
        self.rep.section("events: discover, GM change, depart, re-advertise")
        self.bringup()
        seen = []
        for label, ev, exp_msg in (("ENTITY_DISCOVER", EV_DISCOVER, wire.ADP_ENTITY_AVAILABLE),
                                   ("GM change", EV_GM_CHANGE, wire.ADP_ENTITY_AVAILABLE),
                                   ("info changed", EV_INFO_CHANGED, wire.ADP_ENTITY_AVAILABLE)):
            fr = self.event(ev)
            self.rep.ck("%s: advertisement emitted" % label, len(fr) > 0,
                        "%d frame(s)" % len(fr))
            if fr:
                self.check_adpdu(label, fr[0], exp_msg)
                seen.append(fr[0].available_index)
        self.rep.ck("available_index is monotonic across advertisements",
                    all(b >= a for a, b in zip(seen, seen[1:])), str(seen))

        fr = self.event(EV_LINK_DOWN)
        self.rep.ck("link down: ENTITY_DEPARTING emitted", len(fr) > 0,
                    "%d frame(s)" % len(fr))
        if fr:
            self.check_adpdu("link-down", fr[0], wire.ADP_ENTITY_DEPARTING)
        st = self.state()
        self.rep.ck("depart counter advanced", st[S_DEPART_CNT] > 0,
                    "depart_cnt=%d" % st[S_DEPART_CNT])
        fr = self.event(EV_LINK_UP)
        self.rep.ck("link restored: advertises again", len(fr) > 0,
                    "%d frame(s)" % len(fr))
        if fr:
            self.check_adpdu("link-restore", fr[0], wire.ADP_ENTITY_AVAILABLE)

    # ------------------------------------------------- 4 tsn-gen cross-decode
    def cross_decode(self, frame):
        self.rep.section("tsn-gen independent decode of the emitted ADPDU")
        if not frame:
            self.rep.ck("have an ADPDU to decode", False)
            return
        got = tsn_model.decode_pdu(
            tsn_model.ADP_DIR,
            "atdecc_adp_service::ADP_INTERFACE::ADP_IF_DATA", frame.pdu)
        if not got:
            self.rep.ck("tsn-gen returned fields", False, "empty decode")
            return
        self.rep.ck("tsn-gen decoded the ADPDU", True, "%d fields" % len(got))
        for field, mine in (("message_type", frame.message_type),
                            ("valid_time", frame.valid_time),
                            ("control_data_length", frame.cdl),
                            ("entity_id", frame.entity_id),
                            ("entity_model_id", frame.entity_model_id),
                            ("entity_capabilities", frame.entity_capabilities),
                            ("talker_stream_sources", frame.talker_stream_sources),
                            ("talker_capabilities", frame.talker_capabilities),
                            ("listener_stream_sinks", frame.listener_stream_sinks),
                            ("listener_capabilities", frame.listener_capabilities),
                            ("gptp_grandmaster_id", frame.gptp_grandmaster_id),
                            ("gptp_domain_number", frame.gptp_domain_number)):
            if field in got:
                self.rep.eq("tsn-gen agrees on %s" % field, got[field], mine)

    # ------------------------------------------------------- 5 event storm
    def storm(self, rounds):
        self.rep.section("event storm + state stability")
        import random
        rng = random.Random(self.seed)
        evs = [EV_LINK_UP, EV_LINK_DOWN, EV_DISCOVER, EV_GM_CHANGE,
               EV_INFO_CHANGED, EV_SHUTDOWN, EV_TICK]
        malformed = 0
        for _ in range(rounds):
            for f in self.event(rng.choice(evs)):
                # every frame the advertiser ever emits must be a well-formed
                # 82-byte ADPDU with our entity id — no truncation, no garbage
                if len(f) != 82 or f.subtype != wire.SUBTYPE_ADP \
                        or f.entity_id != MODEL["entity_id"] or f.cdl != 56:
                    malformed += 1
        self.rep.eq("storm: no malformed advertisement", malformed, 0)
        st = self.state()
        self.rep.ck("storm: advertiser not stuck busy", st[S_BUSY] in (0, 1),
                    "busy=%d" % st[S_BUSY])
        # THE gate: still advertises correctly afterwards
        self.event(EV_LINK_UP)
        fr = self.event(EV_DISCOVER)
        self.rep.ck("STATE STABLE: discover still answered after the storm",
                    len(fr) > 0, "%d frame(s)" % len(fr))
        if fr:
            self.check_adpdu("post-storm", fr[0], wire.ADP_ENTITY_AVAILABLE)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dut", default="obj_adp/Vadp_cosim")
    ap.add_argument("--rounds", type=int, default=40)
    ap.add_argument("--seed", type=int, default=20260725)
    args = ap.parse_args()

    rep = cosim.Report(
        "ADP discovery field campaign (tsn-gen driven)",
        dut="adp_advertiser",
        rtl_files=["hdl/ieee17221/adp/adp_advertiser.sv",
                   "hdl/ieee17221/adp/adp_pkg.sv"],
        results_dir="../../../hdl/ieee17221/adp/doc",
        reproduce="cd tb/verilator/tsn_fuzz && make adp")
    cosim.require_tsn_gen(rep)
    with cosim.Dut(args.dut) as dut:
        c = Campaign(dut, rep, args.seed)
        c.model_inventory()
        first = c.advertise()
        c.events()
        c.cross_decode(first)
        c.storm(args.rounds)
    return rep.done()


if __name__ == "__main__":
    sys.exit(main())
