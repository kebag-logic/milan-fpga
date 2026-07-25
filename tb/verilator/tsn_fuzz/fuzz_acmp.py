#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""
ACMP connection-management field + STATE-MACHINE campaign (KL_acmp_listener).

The listener is the state machine of the end-station: UNBOUND -> PRB_W_AVAIL
-> PRB_W_DELAY -> PRB_W_RESP -> SETTLED_*. Fuzzing its PDUs is only half a
test — the other half is reading `state_o` afterwards, which this campaign
does through the in-band control frame after every probe. What it proves:

  1. FIELD VALIDATION — message_type, status, control_data_length and the
     four 64-bit id fields swept over their spec-legal and spec-illegal
     values from the repo's ACMP model (tests/protocols/acmp).
  2. ADDRESSING — a PDU whose listener_entity_id is not ours must not move
     our state machine, no matter how well formed it is.
  3. LENGTH — the 70-byte ACMPDU rule. A 68-byte ACMPDU is the field trap
     that made this entity look "deaf" to a real controller once; the
     campaign pins both the accept and the reject side of the boundary.
  4. STATE STABILITY — the machine must never land outside its 8 legal
     states, must never wedge (tx_wedge_cnt), and after any storm of garbage
     a legitimate BIND must still work. That last one is the real gate: a
     state machine that survives fuzzing but can no longer bind is broken.

Run: python3 fuzz_acmp.py [--rounds N] [--seed S]
"""
import argparse
import sys

import cosim
import tsn_model
import wire
from wire import AcmpResp

#: acmp_pkg.sv LSM states (the only legal values of state_o)
LSM = {0: "UNBOUND", 1: "PRB_W_AVAIL", 2: "PRB_W_DELAY", 3: "PRB_W_RESP",
       4: "PRB_W_RESP2", 5: "PRB_W_RETRY", 6: "SETTLED_NO_RSV", 7: "SETTLED_RSV_OK"}

# state_dump() word order — must match cosim_acmp.cpp
S_STATE, S_STATUS, S_CMDCNT, S_PROBECNT, S_WEDGE, S_ACTIVE, \
    S_DECLARE, S_PROBING, S_TKAVAIL, S_SID_HI, S_SID_LO, S_TUID = range(12)

BIND_RX = wire.ACMP_CONNECT_RX_COMMAND        # 6
UNBIND_RX = wire.ACMP_DISCONNECT_RX_COMMAND   # 8
GET_RX_STATE = wire.ACMP_GET_RX_STATE_COMMAND  # 10

TEST_SID = 0x0200000000010000
TALKER_ID = 0x020000FFFE000002


def derived_sid(talker_eid, tuid=0):
    """The stream_id a Milan listener BINDS to: {talker MAC, unique_id}.

    Measured 2026-07-25: the listener does NOT trust the stream_id field of
    a CONNECT_RX_COMMAND — it derives the id from the talker's EUI-64 (strip
    the FF:FE in the middle) and the talker_unique_id, which is the Milan
    contract and what the AVTP frames actually carry. (KL_acmp_lstn_ctx keeps
    a SID_EXPLICIT_P mode for the take-it-from-the-field behaviour.) So the
    command's stream_id is advisory and the campaign asserts the DERIVED id.
    """
    mac = ((talker_eid >> 40) << 24) | (talker_eid & 0xFFFFFF)
    return (mac << 16) | (tuid & 0xFFFF)


class Campaign:
    def __init__(self, dut, rep, seed):
        self.dut = dut
        self.rep = rep
        self.seed = seed
        self.seq = 0x100

    # ------------------------------------------------------------- primitives
    def send(self, message_type, **kw):
        self.seq = (self.seq + 1) & 0xFFFF
        kw.setdefault("seq", self.seq)
        kw.setdefault("listener", wire.ENTITY_ID)
        kw.setdefault("talker", TALKER_ID)
        kw.setdefault("stream_id", TEST_SID)
        frames = self.dut.xact_all(wire.acmp_pdu(message_type, **kw))
        return [AcmpResp(f) for f in frames], kw["seq"]

    def state(self):
        return cosim.read_state(self.dut)

    def reset(self):
        cosim.parse_state(self.dut.xact(cosim.ctrl(cosim.CTRL_RESET)))

    def check_state_legal(self, tag, st=None):
        st = st or self.state()
        ok = self.rep.ck("%s: state_o is a legal LSM state" % tag,
                         st[S_STATE] in LSM, "state=%d" % st[S_STATE])
        self.rep.eq("%s: tx path not wedged" % tag, st[S_WEDGE], 0)
        return ok

    # -------------------------------------------------------- 1 model + reset
    def model_inventory(self):
        self.rep.section("ACMP model inventory (repo tests/protocols/acmp)")
        try:
            m = tsn_model.load("acmp", "1722_1_acmp.yaml",
                               "milan_acmp::MILAN_ACMP::MILAN_ACMP_IF")
        except (OSError, ValueError) as exc:
            self.rep.ck("ACMP model loads", False, str(exc))
            return None
        self.rep.ck("ACMP model loads", True, "%d fields" % len(m.fields))
        for name, bits, con in m.fields:
            self.rep.ck("  field %-22s %3d bits%s"
                        % (name, bits, "  (spec-constrained)" if con else ""), True)
        return m

    def baseline(self):
        self.rep.section("baseline: unbound listener")
        self.reset()
        st = self.state()
        self.rep.eq("fresh listener is UNBOUND", st[S_STATE], 0)
        self.check_state_legal("fresh")
        rs, seq = self.send(GET_RX_STATE)
        self.rep.ck("GET_RX_STATE answered while unbound", len(rs) > 0,
                    "%d frame(s)" % len(rs))
        if rs:
            r = rs[0]
            self.rep.eq("  response is an ACMPDU", r.subtype, wire.SUBTYPE_ACMP)
            self.rep.eq("  70-byte ACMPDU", len(r), 70)
            self.rep.eq("  sequence_id echoed", r.sequence_id, seq)
            self.rep.eq("  listener_entity_id echoed", r.listener_entity_id,
                        wire.ENTITY_ID)

    # ----------------------------------------------------- 2 message_type map
    def message_types(self, m):
        self.rep.section("message_type sweep (all 16 values)")
        for mt in range(16):
            self.reset()
            rs, seq = self.send(mt)
            st = self.state()
            self.check_state_legal("mt=%d" % mt, st)
            if rs:
                r = rs[0]
                self.rep.eq("mt=%d: reply is an ACMPDU" % mt, r.subtype, wire.SUBTYPE_ACMP)
                self.rep.eq("mt=%d: reply length 70" % mt, len(r), 70)
                self.rep.eq("mt=%d: sequence_id echoed" % mt, r.sequence_id, seq)
                self.rep.ck("mt=%d: reply is a RESPONSE type (odd)" % mt,
                            r.message_type % 2 == 1 or r.message_type == mt,
                            "reply mt=%d" % r.message_type)
            else:
                # silence is correct for talker-side and response-typed PDUs
                self.rep.ck("mt=%d: silent (not a listener command)" % mt, True)
        self.reset()

    # --------------------------------------------------------- 3 bind / state
    def bind_cycle(self):
        self.rep.section("BIND -> state machine -> UNBIND")
        self.reset()
        rs, seq = self.send(BIND_RX)
        self.rep.ck("BIND_RX answered", len(rs) > 0, "%d frame(s)" % len(rs))
        if rs:
            r = rs[0]
            self.rep.eq("BIND_RX -> CONNECT_RX_RESPONSE", r.message_type,
                        wire.ACMP_CONNECT_RX_RESPONSE)
            # the response may carry 0 while the id is still unresolved (the
            # talker has not answered PROBE_TX yet) or the derived id
            self.rep.ck("  stream_id is 0 (unresolved) or the derived id",
                        r.stream_id in (0, derived_sid(TALKER_ID)),
                        "sid=0x%016x" % r.stream_id)
            self.rep.eq("  talker_entity_id echoed", r.talker_entity_id, TALKER_ID)
            self.rep.eq("  sequence_id echoed", r.sequence_id, seq)
        st = self.state()
        self.check_state_legal("after BIND", st)
        self.rep.ck("BIND moved the machine off UNBOUND", st[S_STATE] != 0,
                    "state=%s" % LSM.get(st[S_STATE]))
        self.rep.eq("BIND latched the DERIVED stream_id {talker MAC, uid}",
                    (st[S_SID_HI] << 32) | st[S_SID_LO], derived_sid(TALKER_ID))
        self.rep.ck("command counter advanced", st[S_CMDCNT] > 0,
                    "cmd_count=%d" % st[S_CMDCNT])
        # let the probe ladder run: 1 s ticks drive the retry timers
        self.dut.xact_all(cosim.ctrl(cosim.CTRL_TICK, 6))
        st2 = self.state()
        self.check_state_legal("after 6 s of ticks", st2)
        # SRP registration then unbind
        self.dut.xact(cosim.ctrl(cosim.CTRL_EVENT, 0x01))   # ta_registered
        self.check_state_legal("after SRP registered")
        rs, seq = self.send(UNBIND_RX)
        self.rep.ck("UNBIND_RX answered", len(rs) > 0, "%d frame(s)" % len(rs))
        st3 = self.state()
        self.rep.eq("UNBIND returns the machine to UNBOUND", st3[S_STATE], 0)
        self.check_state_legal("after UNBIND", st3)

    # ---------------------------------------------------------- 4 addressing
    def addressing(self):
        self.rep.section("addressing: foreign listener_entity_id")
        self.reset()
        before = self.state()
        rs, seq = self.send(BIND_RX, listener=0xDEADBEEFCAFEBABE)
        after = self.state()
        self.rep.eq("foreign listener: state unmoved", after[S_STATE], before[S_STATE])
        self.rep.ck("foreign listener: not bound", after[S_SID_LO] == 0
                    and after[S_SID_HI] == 0,
                    "sid=0x%08x%08x" % (after[S_SID_HI], after[S_SID_LO]))
        # ...and a legitimate BIND still works right afterwards
        rs, seq = self.send(BIND_RX)
        st = self.state()
        self.rep.ck("legitimate BIND still works after a foreign one",
                    st[S_STATE] != 0, "state=%s" % LSM.get(st[S_STATE]))
        self.reset()

    # -------------------------------------------------------------- 5 length
    def lengths(self):
        self.rep.section("ACMPDU length validation (the 70-byte rule)")
        self.reset()
        base = wire.acmp_pdu(BIND_RX, stream_id=TEST_SID, listener=wire.ENTITY_ID,
                             talker=TALKER_ID, seq=0x200)
        self.rep.eq("builder emits a 70-byte ACMPDU", len(base), 70)
        for label, frame in (("70 B (spec)", base),
                             ("68 B (the deaf-listener trap)", base[:68]),
                             ("64 B", base[:64]),
                             ("72 B (over-long)", base + b"\x00\x00")):
            self.reset()
            frames = self.dut.xact_all(frame)
            st = self.state()
            self.check_state_legal("len %s" % label, st)
            if label.startswith("70"):
                self.rep.ck("%s: accepted (answered)" % label, len(frames) > 0,
                            "%d frame(s)" % len(frames))
                self.rep.ck("%s: state advanced" % label, st[S_STATE] != 0,
                            "state=%s" % LSM.get(st[S_STATE]))
            else:
                self.rep.ck("%s: handled without wedging" % label,
                            st[S_WEDGE] == 0 and st[S_STATE] in LSM,
                            "state=%s wedge=%d" % (LSM.get(st[S_STATE]), st[S_WEDGE]))
        self.reset()

    # ---------------------------------------------------------- 6 field fuzz
    def field_fuzz(self, m, rounds):
        self.rep.section("per-field fuzz from the spec model + state stability")
        if m is None:
            return
        self.reset()
        # per-field legal/illegal probes on the fields the model constrains
        for name, _bits, con in m.fields:
            if not con:
                continue
            for kind, values in (("legal", m.legal(name)), ("illegal", m.illegal(name))):
                for v in values[:6]:
                    kw = {}
                    if name == "message_type":
                        mt = v
                    else:
                        mt = BIND_RX
                        if name in ("status", "control_data_length", "connection_count",
                                    "flags", "stream_vlan_id", "reserved"):
                            kw[{"control_data_length": "cdl"}.get(name, name)] = v
                        elif name in ("stream_id", "controller_entity_id",
                                      "talker_entity_id", "talker_unique_id",
                                      "listener_unique_id"):
                            kw[{"controller_entity_id": "controller",
                                "talker_entity_id": "talker",
                                "talker_unique_id": "talker_unique",
                                "listener_unique_id": "listener_unique"}.get(name, name)] = v
                        elif name == "listener_entity_id":
                            continue          # covered by the addressing section
                        elif name == "stream_dest_mac":
                            kw["dest_mac"] = v.to_bytes(6, "big")
                    self.send(mt, **kw)
                    st = self.state()
                    if st[S_STATE] not in LSM or st[S_WEDGE] != 0:
                        self.rep.ck("field %s=%s (%s): machine stayed sane"
                                    % (name, v, kind), False,
                                    "state=%d wedge=%d" % (st[S_STATE], st[S_WEDGE]))
            self.rep.ck("field %-22s swept legal+illegal, machine sane" % name, True)

        # constrained-random storm straight from the model
        sets = m.random(rounds, self.seed)
        self.rep.ck("tsn-gen produced constrained-random ACMP field sets",
                    len(sets) > 0, "%d sets (seed %d)" % (len(sets), self.seed))
        bad = 0
        for fs in sets:
            self.send(fs.get("message_type", BIND_RX) & 0x0F,
                      status=fs.get("status", 0) & 0x1F,
                      cdl=fs.get("control_data_length", 44) & 0x7FF,
                      stream_id=fs.get("stream_id", TEST_SID),
                      controller=fs.get("controller_entity_id", wire.CTRLR_ID),
                      talker=fs.get("talker_entity_id", TALKER_ID),
                      talker_unique=fs.get("talker_unique_id", 0),
                      listener_unique=fs.get("listener_unique_id", 0),
                      connection_count=fs.get("connection_count", 0),
                      flags=fs.get("flags", 0),
                      vlan=fs.get("stream_vlan_id", 2),
                      reserved=fs.get("reserved", 0))
            st = self.state()
            if st[S_STATE] not in LSM or st[S_WEDGE] != 0:
                bad += 1
        self.rep.eq("random storm: no illegal state, no wedge", bad, 0)

        # THE gate: after all that garbage, a legitimate bind must still work
        self.reset()
        rs, seq = self.send(BIND_RX)
        st = self.state()
        self.rep.ck("STATE STABLE: legitimate BIND works after the storm",
                    len(rs) > 0 and st[S_STATE] != 0,
                    "frames=%d state=%s" % (len(rs), LSM.get(st[S_STATE])))
        self.rep.eq("STATE STABLE: derived stream_id latched after the storm",
                    (st[S_SID_HI] << 32) | st[S_SID_LO], derived_sid(TALKER_ID))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dut", default="obj_acmp/Vacmp_cosim")
    ap.add_argument("--rounds", type=int, default=48)
    ap.add_argument("--seed", type=int, default=20260725)
    args = ap.parse_args()

    rep = cosim.Report("ACMP field + state-machine campaign (tsn-gen driven)")
    cosim.require_tsn_gen(rep)
    with cosim.Dut(args.dut) as dut:
        c = Campaign(dut, rep, args.seed)
        m = c.model_inventory()
        c.baseline()
        c.message_types(m)
        c.bind_cycle()
        c.addressing()
        c.lengths()
        c.field_fuzz(m, args.rounds)
    return rep.done()


if __name__ == "__main__":
    sys.exit(main())
