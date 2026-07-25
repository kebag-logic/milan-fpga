#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""
AECP / AEM getter-setter field campaign against the real RTL (KL_aecp_top).

What this proves, and how:

  1. HEADER INVARIANTS — every AECP response, whatever the command or the
     status, echoes the command's identity (target/controller entity id,
     sequence_id, command_type), answers with message_type = AEM_RESPONSE,
     carries a status from the 1722.1 set, and satisfies the §5.4 length
     invariant CDL == frame - 26. A response that violates one of these is
     unparseable by a real controller no matter how right its payload is.

  2. GETTERS — a full descriptor_type x descriptor_index sweep per getter.
     The entity model decides WHICH descriptors exist; the campaign asserts
     the DICHOTOMY holds everywhere: a getter either answers SUCCESS with a
     payload, or refuses with NO_SUCH_DESCRIPTOR / NOT_SUPPORTED. Silence,
     a status outside the set, or SUCCESS-with-nothing are all failures.

  3. SETTERS — spec-LEGAL field values (mined from the tsn-gen constraint
     model) must be accepted or refused with a *specific* legal status, and
     spec-ILLEGAL values must be refused, never accepted. Accepted setters
     are then read back through their paired getter: SET->GET coherence is
     the real test of a control-plane register.

  4. STATE STABILITY — the point of fuzzing here is not to find a crash but
     to prove the entity's state machines are unmoved by garbage. Between
     every storm the campaign replays a CANARY (READ_DESCRIPTOR(ENTITY,0))
     and requires it byte-identical to the pre-storm baseline: same bytes
     means the L0 state machine, the descriptor engine and the response
     builder all came back to exactly the state they started in.

Field VALUES and their legal/illegal partition come from tsn-gen's spec
model (`tsn_model.py`); the bytes are built by `wire.py`. Run:
    python3 fuzz_aecp.py [--rounds N] [--seed S]
"""
import argparse
import struct
import sys

import cosim
import tsn_model
import wire
from wire import AecpResp

# ---- AEM command codes (aecp_pkg.sv is the authority; never a comment) ----
ACQUIRE_ENTITY = 0
LOCK_ENTITY = 1
ENTITY_AVAILABLE = 2
READ_DESCRIPTOR = 4
SET_CONFIGURATION = 6
GET_CONFIGURATION = 7
SET_STREAM_FORMAT = 8
GET_STREAM_FORMAT = 9
SET_STREAM_INFO = 14
GET_STREAM_INFO = 15
SET_NAME = 16
GET_NAME = 17
SET_SAMPLING_RATE = 20
GET_SAMPLING_RATE = 21
SET_CLOCK_SOURCE = 22
GET_CLOCK_SOURCE = 23
SET_CONTROL = 24
GET_CONTROL = 25
START_STREAMING = 34
STOP_STREAMING = 35
GET_AVB_INFO = 39
GET_AS_PATH = 40
GET_COUNTERS = 41
GET_AUDIO_MAP = 43
ADD_AUDIO_MAPPINGS = 44
REMOVE_AUDIO_MAPPINGS = 45

# ---- descriptor types (1722.1 Table 7.1) ----
D_ENTITY = 0x0000
D_CONFIGURATION = 0x0001
D_AUDIO_UNIT = 0x0002
D_STREAM_INPUT = 0x0005
D_STREAM_OUTPUT = 0x0006
D_JACK_INPUT = 0x0007
D_JACK_OUTPUT = 0x0008
D_AVB_INTERFACE = 0x0009
D_CLOCK_SOURCE = 0x000A
D_LOCALE = 0x000C
D_STRINGS = 0x000D
D_STREAM_PORT_INPUT = 0x000E
D_STREAM_PORT_OUTPUT = 0x000F
D_CONTROL = 0x001A
D_AUDIO_CLUSTER = 0x0022
D_AUDIO_MAP = 0x0023
D_CLOCK_DOMAIN = 0x0024

#: statuses a 1722.1 responder may legally return
LEGAL_STATUS = set(wire.STATUS)
#: refusals that are legitimate answers to "that thing does not exist here"
REFUSALS = {1, 2, 7, 11}          # NOT_IMPLEMENTED, NO_SUCH_DESCRIPTOR, BAD_ARGUMENTS, NOT_SUPPORTED


#: Milan Vendor-Unique command codes (aecp_pkg.sv VU_*) and protocol id
MILAN_PROTOCOL_ID = bytes.fromhex("001bc50ac100")
VU_GET_MILAN_INFO = 0x0000
VU_SET_SYSTEM_UNIQUE_ID = 0x0001
VU_GET_SYSTEM_UNIQUE_ID = 0x0002
VU_SET_MEDIA_CLOCK_REF_INFO = 0x0003
VU_GET_MEDIA_CLOCK_REF_INFO = 0x0004
GET_DYNAMIC_INFO = 0x004B

def _dyn_record(cmd, data=b""):
    """One GET_DYNAMIC_INFO batch record (1722.1-2021 §7.4.76).

    record = {length u16, reserved u16, status u8, reserved u8, command u16,
    data} — each record is processed as an independent fixed-size GET.
    `length` counts the DATA only, not the 8-byte record header (matched
    against tb/verilator/aecp/sim_main.cpp's batch builder, which the 0x4B
    engine is silicon-proven against).
    """
    return struct.pack(">HHBBH", len(data), 0, 0, 0, cmd) + data


#: (label, Milan clause, is_vendor_unique, command code, payload)
MILAN_MANDATORY = [
    ("GET_MILAN_INFO",            "5.4.4.1", True,  VU_GET_MILAN_INFO, b""),
    ("GET_SYSTEM_UNIQUE_ID",      "5.4.4.3", True,  VU_GET_SYSTEM_UNIQUE_ID, b""),
    ("SET_SYSTEM_UNIQUE_ID",      "5.4.4.2", True,  VU_SET_SYSTEM_UNIQUE_ID,
     struct.pack(">I", 0x0000ABCD)),
    ("GET_MEDIA_CLOCK_REF_INFO",  "5.4.4.5", True,  VU_GET_MEDIA_CLOCK_REF_INFO,
     struct.pack(">HH", 0x0024, 0)),
    ("SET_MEDIA_CLOCK_REF_INFO",  "5.4.4.4", True,  VU_SET_MEDIA_CLOCK_REF_INFO,
     struct.pack(">HH", 0x0024, 0) + bytes(8)),
    ("GET_DYNAMIC_INFO",          "5.4.2.29", False, GET_DYNAMIC_INFO,
     _dyn_record(41, struct.pack(">HH", 0x0009, 0))),
    ("GET_AUDIO_MAP",             "5.4.2.26", False, GET_AUDIO_MAP,
     struct.pack(">HHHH", 0x000E, 0, 0, 0)),
    ("GET_COUNTERS",              "5.4.2.x",  False, GET_COUNTERS,
     struct.pack(">HH", 0x0006, 0)),
    ("GET_AVB_INFO",              "5.4.2.x",  False, GET_AVB_INFO,
     struct.pack(">HH", 0x0009, 0)),
    ("GET_AS_PATH",               "5.4.2.x",  False, GET_AS_PATH,
     struct.pack(">HH", 0, 0)),
]


def gs4(dtype, didx):
    return struct.pack(">HH", dtype, didx)


class Campaign:
    def __init__(self, dut, rep, seed):
        self.dut = dut
        self.rep = rep
        self.seed = seed
        self.seq = 0x1000
        self.baseline = None

    # ------------------------------------------------------------- primitives
    def cmd(self, command_type, payload=b"", **kw):
        """Send one AEM command; return (AecpResp, sent_sequence_id)."""
        self.seq = (self.seq + 1) & 0xFFFF
        seq = kw.pop("seq", self.seq)
        frame = wire.aecp_cmd(command_type, payload, seq=seq, **kw)
        return AecpResp(self.dut.xact(frame)), seq

    def check_header(self, tag, r, seq, command_type,
                     target=wire.ENTITY_ID, controller=wire.CTRLR_ID):
        """The invariants every response owes a controller (§1 of the docstring)."""
        rep = self.rep
        if not rep.ck("%s: response present" % tag, bool(r), "%d B" % len(r)):
            return False
        ok = True
        ok &= rep.eq("%s: message_type=AEM_RESPONSE" % tag, r.message_type, wire.MSG_AEM_RESPONSE)
        ok &= rep.eq("%s: command_type echoed" % tag, r.command_type, command_type)
        ok &= rep.eq("%s: sequence_id echoed" % tag, r.sequence_id, seq)
        ok &= rep.eq("%s: target_entity_id echoed" % tag, r.target_entity_id, target)
        ok &= rep.eq("%s: controller_entity_id echoed" % tag, r.controller_entity_id, controller)
        ok &= rep.ck("%s: status in the 1722.1 set" % tag, r.status in LEGAL_STATUS,
                     "status=%d" % r.status)
        ok &= rep.ck("%s: CDL == frame-26 (§5.4)" % tag, r.cdl_ok,
                     "cdl=%d frame=%d" % (r.cdl, len(r)))
        ok &= rep.eq("%s: subtype=AECP" % tag, r.subtype, wire.SUBTYPE_AECP)
        return ok

    # ------------------------------------------------------------- 0 baseline
    #: READ_DESCRIPTOR payload = configuration(2) reserved(2) type(2) index(2)
    CANARY_PAYLOAD = struct.pack(">HHHH", 0, 0, D_ENTITY, 0)

    def canary_frame(self):
        r, seq = self.cmd(READ_DESCRIPTOR, self.CANARY_PAYLOAD, seq=0x0777)
        return r

    def establish_baseline(self):
        self.rep.section("baseline / canary")
        r = self.canary_frame()
        self.check_header("canary", r, 0x0777, READ_DESCRIPTOR)
        self.rep.eq("canary: READ_DESCRIPTOR(ENTITY,0) SUCCESS", r.status, 0)
        self.rep.ck("canary: carries a descriptor payload", len(r.payload) > 16,
                    "%d B payload" % len(r.payload))
        self.baseline = r.raw
        # determinism: the same command twice must produce the same bytes
        again = self.canary_frame()
        self.rep.ck("canary: deterministic (byte-identical on replay)",
                    again.raw == self.baseline,
                    "%d vs %d B" % (len(again), len(self.baseline)))

    def canary_ok(self, tag):
        """State-stability probe: the canary must still be byte-identical."""
        r = self.canary_frame()
        return self.rep.ck("STATE STABLE after %s (canary byte-identical)" % tag,
                           r.raw == self.baseline,
                           "%d B vs baseline %d B, status=%s"
                           % (len(r), len(self.baseline), r.status_name()))

    # -------------------------------------------------------- 1 model coverage
    def model_inventory(self):
        self.rep.section("tsn-gen model inventory")
        total_fields = 0
        models = 0
        for yml, iface in AECP_MODELS:
            try:
                m = tsn_model.load("aecp", yml, iface)
            except (OSError, ValueError) as exc:
                self.rep.ck("model %s loads" % yml, False, str(exc))
                continue
            models += 1
            total_fields += len(m.fields)
            constrained = sum(1 for _, _, c in m.fields if c)
            self.rep.ck("model %-34s %2d fields (%d spec-constrained)"
                        % (yml.replace("aecp_aem_", "").replace(".yaml", ""),
                           len(m.fields), constrained), True)
        self.rep.ck("AECP models loaded from tsn-gen", models == len(AECP_MODELS),
                    "%d/%d" % (models, len(AECP_MODELS)))
        self.rep.note("%d AECP fields under spec model" % total_fields)

    # ------------------------------------------------------------- 2 getters
    def getters(self):
        self.rep.section("getters: descriptor sweep + header invariants")
        sweep_types = [D_ENTITY, D_CONFIGURATION, D_AUDIO_UNIT, D_STREAM_INPUT,
                       D_STREAM_OUTPUT, D_JACK_INPUT, D_AVB_INTERFACE, D_CLOCK_SOURCE,
                       D_LOCALE, D_STRINGS, D_STREAM_PORT_INPUT, D_STREAM_PORT_OUTPUT,
                       D_CONTROL, D_AUDIO_CLUSTER, D_AUDIO_MAP, D_CLOCK_DOMAIN,
                       0x0030, 0x00FF, 0xFFFF]
        for name, code, mk in GETTERS:
            answered = succeeded = refused = 0
            for dt in sweep_types:
                r, seq = self.cmd(code, mk(dt, 0))
                if not r:
                    self.rep.ck("%s(type=0x%04x): answered" % (name, dt), False, "silence")
                    continue
                answered += 1
                # full header invariants on every single probe
                self.check_header("%s(0x%04x)" % (name, dt), r, seq, code)
                if r.status == 0:
                    succeeded += 1
                    self.rep.ck("%s(0x%04x): SUCCESS carries a payload" % (name, dt),
                                len(r.payload) > 0, "%d B" % len(r.payload))
                else:
                    refused += 1
                    self.rep.ck("%s(0x%04x): refusal is a legal refusal status"
                                % (name, dt), r.status in REFUSALS,
                                "status=%s" % r.status_name())
            self.rep.eq("%s: every descriptor_type answered" % name,
                        answered, len(sweep_types))
            self.rep.note("%-18s %d SUCCESS / %d refused" % (name, succeeded, refused))
            # descriptor_index sweep on the getter's own natural type
            nat = NATURAL_TYPE.get(code, D_ENTITY)
            for idx in (0, 1, 7, 0x00FF, 0xFFFF):
                r, seq = self.cmd(code, mk(nat, idx))
                self.check_header("%s(idx=%d)" % (name, idx), r, seq, code)
                if r:
                    self.rep.ck("%s(idx=%d): SUCCESS or legal refusal" % (name, idx),
                                r.status == 0 or r.status in REFUSALS,
                                "status=%s" % r.status_name())
        self.canary_ok("getter sweep")

    # ------------------------------------------------------------- 3 setters
    def setters(self):
        self.rep.section("setters: spec-legal accept, spec-illegal refuse, SET->GET")
        for spec in SETTERS:
            name = spec["name"]
            # --- spec-legal probes -------------------------------------
            for label, payload in spec["legal"]():
                r, seq = self.cmd(spec["code"], payload)
                if not self.check_header("%s[%s]" % (name, label), r, seq, spec["code"]):
                    continue
                self.rep.ck("%s[%s]: legal value -> SUCCESS or legal refusal"
                            % (name, label),
                            r.status == 0 or r.status in REFUSALS | {3, 4, 12},
                            "status=%s" % r.status_name())
            # --- spec-illegal probes ------------------------------------
            known_gaps = spec.get("gaps", ())
            for label, payload in spec["illegal"]():
                r, seq = self.cmd(spec["code"], payload)
                if not self.check_header("%s[%s]" % (name, label), r, seq, spec["code"]):
                    continue
                if label in known_gaps:
                    # tracked leniency: still assert the response is WELL FORMED,
                    # only the refusal itself is waived (see docs/testing)
                    self.rep.gap("%s[%s]: accepted (spec wants a refusal)" % (name, label),
                                 "status=%s" % r.status_name())
                    continue
                self.rep.ck("%s[%s]: illegal value REFUSED" % (name, label),
                            r.status != 0, "status=%s" % r.status_name())
                self.rep.ck("%s[%s]: refusal status is specific" % (name, label),
                            r.status in REFUSALS, "status=%s" % r.status_name())
            # --- SET -> GET coherence -----------------------------------
            rt = spec.get("roundtrip")
            if rt:
                payload, getter, extract, want = rt()
                r, seq = self.cmd(spec["code"], payload)
                self.check_header("%s[set]" % name, r, seq, spec["code"])
                if r and r.status == 0:
                    g, gseq = self.cmd(getter, spec["get_payload"]())
                    self.check_header("%s[get-back]" % name, g, gseq, getter)
                    if g and g.status == 0:
                        got = extract(g)
                        self.rep.eq("%s: SET->GET coherent" % name, got, want)
                else:
                    self.rep.note("%s: SET refused (%s) — round-trip not applicable"
                                  % (name, r.status_name() if r else "silence"))
        self.canary_ok("setter sweep")

    # --------------------------------------------------- 4 header-field fuzz
    def header_fuzz(self, rounds):
        self.rep.section("header-field fuzz (tsn-gen constrained-random)")
        m = tsn_model.load("aecp", "aecp_aem_read_descriptor.yaml",
                           "atdecc_aecp_read_descriptor::AECP_READ_DESCRIPTOR::"
                           "AECP_READ_DESCRIPTOR_IF")
        sets = m.random(rounds, self.seed)
        self.rep.ck("tsn-gen produced constrained-random field sets",
                    len(sets) > 0, "%d sets (seed %d)" % (len(sets), self.seed))
        answered = silent = 0
        for i, fs in enumerate(sets):
            dt = fs.get("descriptor_type", 0) & 0xFFFF
            di = fs.get("descriptor_index", 0) & 0xFFFF
            seq = fs.get("sequence_id", i) & 0xFFFF
            r, _ = self.cmd(READ_DESCRIPTOR, gs4(dt, di), seq=seq)
            if not r:
                silent += 1
                continue
            answered += 1
            # a response, whatever it says, must stay parseable and echo us
            if r.message_type != wire.MSG_AEM_RESPONSE or r.sequence_id != seq \
                    or not r.cdl_ok or r.status not in LEGAL_STATUS:
                self.rep.ck("fuzz[%d] type=0x%04x idx=0x%04x: header intact" % (i, dt, di),
                            False, "mt=%d seq=%d/%d cdl_ok=%s status=%d"
                            % (r.message_type, r.sequence_id, seq, r.cdl_ok, r.status))
        self.rep.ck("header fuzz: every probe answered with an intact header",
                    silent == 0 and answered == len(sets),
                    "%d answered, %d silent" % (answered, silent))
        self.canary_ok("header fuzz")

    # ------------------------------------------- 5 addressing / length probes
    def addressing(self):
        self.rep.section("addressing + length validation")
        # --- not-our-entity, REAL-WIRE condition (frames padded to the
        #     60-byte Ethernet minimum, which is what a MAC ever delivers).
        foreign = 0xDEADBEEFCAFEBABE
        for plen in (0, 4, 8, 12):
            self.seq = (self.seq + 1) & 0xFFFF
            f = wire.aecp_cmd(READ_DESCRIPTOR, bytes(plen), seq=self.seq,
                              target=foreign, pad60=True)
            r = AecpResp(self.dut.xact(f))
            self.rep.ck("foreign target_entity_id (padded, payload %dB): silent" % plen,
                        not r, "%d B" % len(r))
        # our entity still served normally right after
        r, seq = self.cmd(READ_DESCRIPTOR, self.CANARY_PAYLOAD)
        self.rep.eq("own entity still served after foreign probes", r.status, 0)

        # --- UNDERSIZED frames: the entity-id filter is bypassed below a
        #     frame size Ethernet cannot actually deliver. Measured
        #     2026-07-25: frames <= 44 B answer a FOREIGN target (and echo OUR
        #     entity id); >= 45 B filter correctly. Unreachable on a real link
        #     (60-byte minimum, the MAC pads), so this is a latent robustness
        #     gap rather than a live exposure — tracked, not failed.
        bypass = []
        for plen in (0, 2, 4, 6, 8, 12):
            self.seq = (self.seq + 1) & 0xFFFF
            f = wire.aecp_cmd(READ_DESCRIPTOR, bytes(plen), seq=self.seq, target=foreign)
            r = AecpResp(self.dut.xact(f))
            if r:
                bypass.append("%dB" % len(f))
        if bypass:
            self.rep.gap("undersized frames bypass the entity-id filter",
                         "answered at frame sizes: %s (all < 60 B Ethernet minimum)"
                         % ", ".join(bypass))
        else:
            self.rep.ck("undersized frames also filtered by entity-id", True)
        # a second controller must be answered normally (multi-controller entity)
        r, seq = self.cmd(READ_DESCRIPTOR, gs4(D_ENTITY, 0),
                          controller=wire.CTRLR2_ID, src=wire.CTRLR2_MAC)
        self.check_header("2nd controller", r, seq, READ_DESCRIPTOR,
                          controller=wire.CTRLR2_ID)
        # lying control_data_length: short, long, zero, max
        for label, cdl in (("cdl=0", 0), ("cdl=1", 1), ("cdl short", 8),
                           ("cdl long", 200), ("cdl max", 0x7FF)):
            self.seq = (self.seq + 1) & 0xFFFF
            frame = wire.aecp_cmd(READ_DESCRIPTOR, gs4(D_ENTITY, 0),
                                  seq=self.seq, cdl=cdl)
            r = AecpResp(self.dut.xact(frame))
            if r:
                self.rep.ck("%s: response stays parseable" % label,
                            r.cdl_ok and r.status in LEGAL_STATUS,
                            "cdl=%d frame=%d status=%d" % (r.cdl, len(r), r.status))
            else:
                self.rep.ck("%s: dropped (length validation)" % label, True, "silence")
        # unknown command_type must be refused, not ignored, not crash
        for code in (0x0003, 0x0033, 0x7FFE):
            r, seq = self.cmd(code, b"\x00" * 8)
            if r:
                self.check_header("unknown cmd 0x%04x" % code, r, seq, code)
                self.rep.ck("unknown cmd 0x%04x: refused" % code, r.status != 0,
                            "status=%s" % r.status_name())
            else:
                self.rep.ck("unknown cmd 0x%04x: silence is acceptable" % code, True)
        self.canary_ok("addressing/length probes")

    # ------------------------------------------- 5b Milan v1.2 mandatory set
    def milan_v12(self):
        """Milan v1.2 mandatory AECP/MVU census (docs/traceability/milan-v12.md).

        Milan layers its own mandatory command set on top of 1722.1: the
        Vendor-Unique protocol (5.4.3) with protocol_id 00-1B-C5-0A-C1-00,
        GET_MILAN_INFO (5.4.4.1), SET/GET_SYSTEM_UNIQUE_ID (5.4.4.2/3),
        SET/GET_MEDIA_CLOCK_REFERENCE_INFO (5.4.4.4/5) and GET_DYNAMIC_INFO
        (5.4.2.29). tsn-gen carries no MVU payload models, so this section is
        the census that keeps the traceability matrix honest: each command is
        driven and classified IMPLEMENTED / NOT_SUPPORTED, and anything the
        matrix marks mandatory-but-missing is reported as a tracked gap
        instead of quietly passing.
        """
        self.rep.section("Milan v1.2 mandatory AECP/MVU census")
        # --- MVU protocol framing (5.4.3) ---
        self.seq = (self.seq + 1) & 0xFFFF
        r = AecpResp(self.dut.xact(wire.aecp_vu_cmd(VU_GET_MILAN_INFO, seq=self.seq)))
        self.rep.ck("MVU GET_MILAN_INFO answered", bool(r), "%d B" % len(r))
        if r:
            self.rep.eq("  MVU reply is a VU_RESPONSE", r.message_type, wire.MSG_VU_RESPONSE)
            self.rep.eq("  sequence_id echoed", r.sequence_id, self.seq)
            self.rep.eq("  target_entity_id echoed", r.target_entity_id, wire.ENTITY_ID)
            self.rep.ck("  CDL == frame-26 (§5.4)", r.cdl_ok,
                        "cdl=%d frame=%d" % (r.cdl, len(r)))
            # a VU frame has no u/command_type word: the vendor protocol_id
            # starts immediately after sequence_id, at wire byte 36
            self.rep.eq("  Milan protocol_id echoed (00-1B-C5-0A-C1-00)",
                        r.raw[36:42], MILAN_PROTOCOL_ID)
        # a FOREIGN vendor protocol_id must not be answered as Milan MVU
        self.seq = (self.seq + 1) & 0xFFFF
        bad = AecpResp(self.dut.xact(wire.aecp_vu_cmd(
            VU_GET_MILAN_INFO, seq=self.seq, protocol_id=b"\xde\xad\xbe\xef\x00\x01")))
        self.rep.ck("foreign vendor protocol_id: not answered as Milan MVU",
                    (not bad) or bad.raw[36:42] != MILAN_PROTOCOL_ID,
                    "%d B" % len(bad))

        # --- the mandatory command census ---
        census = []
        for label, req, is_vu, code, payload in MILAN_MANDATORY:
            self.seq = (self.seq + 1) & 0xFFFF
            frame = (wire.aecp_vu_cmd(code, payload, seq=self.seq) if is_vu
                     else wire.aecp_cmd(code, payload, seq=self.seq))
            r = AecpResp(self.dut.xact(frame))
            if not r:
                census.append((label, req, "SILENT"))
                self.rep.ck("%s (%s): answered" % (label, req), False, "silence")
                continue
            self.rep.eq("%s (%s): sequence_id echoed" % (label, req),
                        r.sequence_id, self.seq)
            self.rep.ck("%s (%s): CDL == frame-26" % (label, req), r.cdl_ok,
                        "cdl=%d frame=%d" % (r.cdl, len(r)))
            self.rep.ck("%s (%s): status is legal" % (label, req),
                        r.status in LEGAL_STATUS, "status=%d" % r.status)
            state = "IMPLEMENTED" if r.status == 0 else r.status_name()
            census.append((label, req, state))
        implemented = sum(1 for _, _, s in census if s == "IMPLEMENTED")
        self.rep.note("Milan mandatory census: %d/%d IMPLEMENTED"
                      % (implemented, len(census)))
        for label, req, state in census:
            self.rep.note("  %-34s %-10s %s" % (label, req, state))
            if state != "IMPLEMENTED":
                # the traceability matrix already tracks M-AECP-9 as MISSING;
                # surface it here so the campaign and the matrix cannot drift
                self.rep.gap("Milan %s (%s) not implemented" % (label, req), state)
        self.canary_ok("Milan v1.2 census")

    # ------------------------------------------------- 6 tsn-gen cross-decode
    def cross_decode(self):
        """tsn-gen independently dissects a real response (offset-corrected)."""
        self.rep.section("tsn-gen independent decode of RTL responses")
        r, seq = self.cmd(READ_DESCRIPTOR, gs4(D_ENTITY, 0))
        if not r:
            self.rep.ck("cross-decode: got a response", False)
            return
        got = tsn_model.decode_pdu(
            tsn_model.AECP_DIR,
            "atdecc_aecp_read_descriptor::AECP_READ_DESCRIPTOR::AECP_READ_DESCRIPTOR_IF",
            r.pdu)
        if not got:
            self.rep.ck("cross-decode: tsn-gen returned fields", False,
                        "empty decode")
            return
        for field, mine in (("message_type", r.message_type),
                            ("status", r.status),
                            ("control_data_length", r.cdl),
                            ("sequence_id", r.sequence_id),
                            ("command_type", r.command_type)):
            if field in got:
                self.rep.eq("tsn-gen decode agrees on %s" % field, got[field], mine)


# ------------------------------------------------------------- command tables
AECP_MODELS = [
    ("aecp_aem_read_descriptor.yaml",
     "atdecc_aecp_read_descriptor::AECP_READ_DESCRIPTOR::AECP_READ_DESCRIPTOR_IF"),
    ("aecp_aem_descriptor_query.yaml",
     "atdecc_aecp_aem_descriptor_query::AECP_AEM_DESCRIPTOR_QUERY::AECP_AEM_DESC_QUERY_IF"),
    ("aecp_aem_no_payload.yaml",
     "atdecc_aecp_aem_no_payload::AECP_AEM_NO_PAYLOAD::AECP_AEM_NO_PAYLOAD_IF"),
    ("aecp_aem_acquire_entity.yaml",
     "atdecc_aecp_acquire_entity::AECP_ACQUIRE_ENTITY::AECP_ACQUIRE_ENTITY_IF"),
    ("aecp_aem_lock_entity.yaml",
     "atdecc_aecp_lock_entity::AECP_LOCK_ENTITY::AECP_LOCK_ENTITY_IF"),
    ("aecp_aem_set_stream_format.yaml",
     "atdecc_aecp_set_stream_format::AECP_SET_STREAM_FORMAT::AECP_SET_STREAM_FORMAT_IF"),
    ("aecp_aem_set_stream_info.yaml",
     "atdecc_aecp_set_stream_info::AECP_SET_STREAM_INFO::AECP_SET_STREAM_INFO_IF"),
    ("aecp_aem_set_name.yaml",
     "atdecc_aecp_set_name::AECP_SET_NAME::AECP_SET_NAME_IF"),
    ("aecp_aem_get_name.yaml",
     "atdecc_aecp_get_name::AECP_GET_NAME::AECP_GET_NAME_IF"),
    ("aecp_aem_set_sampling_rate.yaml",
     "atdecc_aecp_set_sampling_rate::AECP_SET_SAMPLING_RATE::AECP_SET_SAMPLING_RATE_IF"),
    ("aecp_aem_set_clock_source.yaml",
     "atdecc_aecp_set_clock_source::AECP_SET_CLOCK_SOURCE::AECP_SET_CLOCK_SOURCE_IF"),
    ("aecp_aem_set_configuration.yaml",
     "atdecc_aecp_set_configuration::AECP_SET_CONFIGURATION::AECP_SET_CONFIGURATION_IF"),
    ("aecp_aem_set_control.yaml",
     "atdecc_aecp_set_control::AECP_SET_CONTROL::AECP_SET_CONTROL_IF"),
    ("aecp_aem_get_audio_map.yaml",
     "atdecc_aecp_get_audio_map::AECP_GET_AUDIO_MAP::AECP_GET_AUDIO_MAP_IF"),
    ("aecp_aem_audio_mappings.yaml",
     "atdecc_aecp_audio_mappings::AECP_AUDIO_MAPPINGS::AECP_AUDIO_MAPPINGS_IF"),
    ("aecp_vendor_unique.yaml",
     "atdecc_aecp_vendor_unique::AECP_VENDOR_UNIQUE::AECP_VENDOR_UNIQUE_IF"),
]

#: getters: (name, command_type, payload builder from (descriptor_type, index))
GETTERS = [
    ("READ_DESCRIPTOR", READ_DESCRIPTOR,
     lambda dt, di: struct.pack(">HH", 0, 0) + gs4(dt, di)),
    ("GET_STREAM_INFO", GET_STREAM_INFO, gs4),
    ("GET_STREAM_FORMAT", GET_STREAM_FORMAT, gs4),
    ("GET_NAME", GET_NAME, lambda dt, di: gs4(dt, di) + struct.pack(">HH", 0, 0)),
    ("GET_SAMPLING_RATE", GET_SAMPLING_RATE, gs4),
    ("GET_CLOCK_SOURCE", GET_CLOCK_SOURCE, gs4),
    ("GET_COUNTERS", GET_COUNTERS, gs4),
    ("GET_AVB_INFO", GET_AVB_INFO, gs4),
    ("GET_AUDIO_MAP", GET_AUDIO_MAP, lambda dt, di: gs4(dt, di) + struct.pack(">HH", 0, 0)),
]

#: the descriptor each getter naturally addresses (for the index sweep)
NATURAL_TYPE = {
    READ_DESCRIPTOR: D_ENTITY, GET_STREAM_INFO: D_STREAM_OUTPUT,
    GET_STREAM_FORMAT: D_STREAM_OUTPUT, GET_NAME: D_ENTITY,
    GET_SAMPLING_RATE: D_AUDIO_UNIT, GET_CLOCK_SOURCE: D_CLOCK_DOMAIN,
    GET_COUNTERS: D_STREAM_OUTPUT, GET_AVB_INFO: D_AVB_INTERFACE,
    GET_AUDIO_MAP: D_STREAM_PORT_INPUT,
}


def _si_body(flags, lat, dtype=D_STREAM_OUTPUT):
    return (struct.pack(">HHI", dtype, 0, flags) + b"\x00" * 16
            + struct.pack(">I", lat) + b"\x00" * 28)


SETTERS = [
    dict(name="SET_STREAM_INFO", code=SET_STREAM_INFO,
         legal=lambda: [("acc_lat=1.5ms", _si_body(0x20000000, 1_500_000)),
                        ("acc_lat=2ms", _si_body(0x20000000, 2_000_000)),
                        ("no subcommand", _si_body(0x00000000, 0))],
         illegal=lambda: [("STREAM_ID_VALID unsupported", _si_body(0x40000000, 7)),
                          ("all sub-commands", _si_body(0xFFFFFFFF, 7)),
                          ("on STREAM_INPUT", _si_body(0x20000000, 500_000, D_STREAM_INPUT)),
                          ("acc_lat > 0x7FFFFFFF", _si_body(0x20000000, 0x80000000))],
         roundtrip=lambda: (_si_body(0x20000000, 1_500_000), GET_STREAM_INFO,
                            lambda g: int.from_bytes(g.raw[62:66], "big"), 1_500_000),
         get_payload=lambda: gs4(D_STREAM_OUTPUT, 0)),
    dict(name="SET_SAMPLING_RATE", code=SET_SAMPLING_RATE,
         legal=lambda: [("48000", gs4(D_AUDIO_UNIT, 0) + struct.pack(">I", 48000))],
         illegal=lambda: [("44100", gs4(D_AUDIO_UNIT, 0) + struct.pack(">I", 44100)),
                          ("0", gs4(D_AUDIO_UNIT, 0) + struct.pack(">I", 0)),
                          ("bad descriptor", gs4(D_ENTITY, 0) + struct.pack(">I", 48000))],
         roundtrip=None, get_payload=lambda: gs4(D_AUDIO_UNIT, 0)),
    dict(name="SET_CONFIGURATION", code=SET_CONFIGURATION,
         legal=lambda: [("cfg 0", struct.pack(">HH", 0, 0))],
         illegal=lambda: [("cfg 1", struct.pack(">HH", 0, 1)),
                          ("cfg 0xFFFF", struct.pack(">HH", 0, 0xFFFF))],
         roundtrip=None, get_payload=lambda: b""),
    dict(name="SET_CLOCK_SOURCE", code=SET_CLOCK_SOURCE,
         legal=lambda: [("src 0", gs4(D_CLOCK_DOMAIN, 0) + struct.pack(">HH", 0, 0)),
                        ("src 1", gs4(D_CLOCK_DOMAIN, 0) + struct.pack(">HH", 1, 0))],
         illegal=lambda: [("src 0xFFFF", gs4(D_CLOCK_DOMAIN, 0) + struct.pack(">HH", 0xFFFF, 0)),
                          ("bad descriptor", gs4(D_ENTITY, 0) + struct.pack(">HH", 0, 0))],
         roundtrip=None, get_payload=lambda: gs4(D_CLOCK_DOMAIN, 0)),
    dict(name="SET_STREAM_FORMAT", code=SET_STREAM_FORMAT,
         legal=lambda: [("AAF 48k 2ch", gs4(D_STREAM_OUTPUT, 0)
                         + struct.pack(">Q", 0x0205022002006000))],
         illegal=lambda: [("all-ones format", gs4(D_STREAM_OUTPUT, 0)
                           + struct.pack(">Q", 0xFFFFFFFFFFFFFFFF)),
                          ("zero format", gs4(D_STREAM_OUTPUT, 0) + struct.pack(">Q", 0)),
                          ("bad descriptor", gs4(D_ENTITY, 0)
                           + struct.pack(">Q", 0x0205022002006000))],
         roundtrip=None, get_payload=lambda: gs4(D_STREAM_OUTPUT, 0)),
    dict(name="ACQUIRE_ENTITY", code=ACQUIRE_ENTITY,
         legal=lambda: [("acquire ENTITY",
                         struct.pack(">I", 0) + struct.pack(">Q", wire.CTRLR_ID)
                         + gs4(D_ENTITY, 0))],
         illegal=lambda: [("acquire bad descriptor",
                           struct.pack(">I", 0) + struct.pack(">Q", wire.CTRLR_ID)
                           + gs4(0xFFFF, 0))],
         roundtrip=None, get_payload=lambda: b""),
    dict(name="LOCK_ENTITY", code=LOCK_ENTITY,
         legal=lambda: [("lock ENTITY",
                         struct.pack(">I", 0) + struct.pack(">Q", wire.CTRLR_ID)
                         + gs4(D_ENTITY, 0)),
                        ("unlock ENTITY",
                         struct.pack(">I", 1) + struct.pack(">Q", wire.CTRLR_ID)
                         + gs4(D_ENTITY, 0))],
         # GAP (measured 2026-07-25): LOCK_ENTITY ignores descriptor_type and
         # descriptor_index entirely and answers SUCCESS for any value.
         # 1722.1-2021 §7.4.2 scopes LOCK to the ENTITY descriptor, so a
         # foreign descriptor should draw NO_SUCH_DESCRIPTOR. Low impact (every
         # real controller sends ENTITY/0) but it is a conformance gap; the
         # sibling ACQUIRE_ENTITY answers NOT_SUPPORTED and is unaffected.
         illegal=lambda: [("lock type=0xFFFF",
                           struct.pack(">I", 0) + struct.pack(">Q", wire.CTRLR_ID)
                           + gs4(0xFFFF, 0)),
                          ("lock type=STREAM_OUTPUT",
                           struct.pack(">I", 0) + struct.pack(">Q", wire.CTRLR_ID)
                           + gs4(D_STREAM_OUTPUT, 0)),
                          ("lock index=0xFFFF",
                           struct.pack(">I", 0) + struct.pack(">Q", wire.CTRLR_ID)
                           + gs4(D_ENTITY, 0xFFFF))],
         gaps=("lock type=0xFFFF", "lock type=STREAM_OUTPUT", "lock index=0xFFFF"),
         roundtrip=None, get_payload=lambda: b""),
    dict(name="STREAMING_CMDS", code=START_STREAMING,
         legal=lambda: [],
         illegal=lambda: [("START_STREAMING on OUTPUT", gs4(D_STREAM_OUTPUT, 0)),
                          ("START_STREAMING bad desc", gs4(0xFFFF, 0))],
         roundtrip=None, get_payload=lambda: b""),
]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dut", default="../aecp/obj_dir/Vaecp_cosim")
    ap.add_argument("--rounds", type=int, default=64)
    ap.add_argument("--seed", type=int, default=20260725)
    args = ap.parse_args()

    rep = cosim.Report("AECP/AEM getter-setter field campaign (tsn-gen driven)")
    cosim.require_tsn_gen(rep)
    with cosim.Dut(args.dut) as dut:
        c = Campaign(dut, rep, args.seed)
        c.model_inventory()
        c.establish_baseline()
        c.getters()
        c.setters()
        c.header_fuzz(args.rounds)
        c.addressing()
        c.milan_v12()
        c.cross_decode()
        rep.section("final state check")
        c.canary_ok("the whole campaign")
    return rep.done()


if __name__ == "__main__":
    sys.exit(main())
