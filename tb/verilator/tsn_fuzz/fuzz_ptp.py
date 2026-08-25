#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""
gPTP / 802.1AS field campaign against the fabric plane slice.

The DUT is the WHOLE slice the datapath splice instantiates — KL_gptp_shadow
(tap + engine + lane), the real timestamp_counter it steers, KL_gptp_txstamp
as the MAC boundary — at the bench's 2 MHz scaling. gPTP is a timer-driven
plane, so the campaign grades BOTH directions:

    our TX      every spec-constrained field of the plane's own Pdelay_Req,
                Announce, Sync and Follow_Up, graded against the tsn-gen
                8021as_* models (which pin the 802.1AS-2011 wire values and
                the Milan v1.2 Table 4.1 cadence bytes)
    peer RX     per-field illegal probes: what the parser must DROP
                (EtherType, transportSpecific, versionPTP, domainNumber,
                truncation) drops and counts; what 11.4.1 says a receiver
                must IGNORE
                (reserved fields) is accepted unchanged; what the µcode owns
                (BTCA compare, source matching, the Milan 4.2.6.2.5 cease
                rule) moves state ONLY the way the clause says

The state-stability canary is two-sided, like AAF's lock: asCapable must
SURVIVE every malformed storm while genuine exchanges continue, and must
FALL when the exchanges stop (a plane still reporting asCapable through a
response drought is lying to every AVB consumer above it) — then climb
again when they resume.

Run: python3 fuzz_ptp.py [--rounds N] [--seed S]
"""
import argparse
import os
import random
import sys

import cosim
import tsn_model
import wire


def require_ptp_models(rep):
    """Skip cleanly when tsn-gen is present but lacks the 802.1AS models.

    The `protocols/data_link/ptp/8021as_*.yaml` models are a newer tsn-gen
    addition; a pinned rev (the CI one) can have `packet_gen` and the 1722.1
    models but not these. tsn_model.available() is TRUE there, so
    require_tsn_gen passes -- but every gPTP model load would fail and the
    campaign would crash on the first `models[...]` lookup. This is the same
    honest skip as require_tsn_gen: report why the total is smaller and exit 0,
    with NO pass/fail numbers (a "0 pass, 0 fail" would read as a campaign that
    ran and checked nothing). The AAF campaign, whose models ARE in every rev,
    is unaffected.
    """
    probe = os.path.join(tsn_model.PTP_DIR, "8021as_sync.yaml")
    if os.path.isfile(probe):
        return True
    print("  SKIP: tsn-gen has no 802.1AS models at %s" % tsn_model.PTP_DIR)
    print("        this rev predates protocols/data_link/ptp/ -- update the "
          "TSN_GEN pin to enable the gPTP field campaign")
    print("SUITE-SKIP: gPTP/802.1AS field campaign (tsn-gen lacks the 802.1AS "
          "models)")
    rep.note("campaign skipped (tsn-gen 802.1AS models absent), not a failure")
    sys.exit(0)

# state_dump() word order — must match cosim_ptp.cpp (APPEND ONLY)
(S_FLAGS, S_GM_HI, S_GM_LO, S_PAR_HI, S_PAR_LO, S_PDELAY, S_OFFSET,
 S_TAPDROP, S_RXDROP, S_PHC_HI, S_PHC_LO, S_TXCNT, S_TXTSSEQ, S_TXTSCNT,
 S_PDEXP, S_PROGRUN) = range(16)

FL_PRESENT, FL_AMGM, FL_ASCAP, FL_SYNCOK = 1, 2, 4, 8

#: bench identities (mirror cosim_ptp.cpp / tb/verilator/gptp_shadow)
OUR_CID = wire.GPTP_OUR_CID
PEER_CID = wire.GPTP_PEER_CID
PEER2_CID = wire.GPTP_PEER2_CID
GMID = 0x00AACCFFFE010203
D_NOM = 600

#: one CTRL_TICK block = 10,000 cycles = 5 ms of bench time (2 MHz);
#: the engine's second — the pdelay/announce interval — is 2,000,000 cycles
MS = 2000
SECOND = 1000 * MS

MODELS = [
    ("sync",     "8021as_sync.yaml"),
    ("follow_up", "8021as_follow_up.yaml"),
    ("pdelay_req", "8021as_pdelay_req.yaml"),
    ("pdelay_resp", "8021as_pdelay_resp.yaml"),
    ("pdelay_resp_fu", "8021as_pdelay_resp_follow_up.yaml"),
    ("announce", "8021as_announce.yaml"),
]

BUILD = {
    "sync": wire.ptp_sync,
    "follow_up": wire.ptp_follow_up,
    "pdelay_req": wire.ptp_pdelay_req,
    "pdelay_resp": wire.ptp_pdelay_resp,
    "pdelay_resp_fu": wire.ptp_pdelay_resp_fu,
    "announce": wire.ptp_announce,
}

PTP_TYPE = {
    "sync": wire.PTP_SYNC, "follow_up": wire.PTP_FOLLOW_UP,
    "pdelay_req": wire.PTP_PDELAY_REQ, "pdelay_resp": wire.PTP_PDELAY_RESP,
    "pdelay_resp_fu": wire.PTP_PDELAY_RESP_FU, "announce": wire.PTP_ANNOUNCE,
}

#: header fields every builder accepts by the model's own name
HDR_FIELDS = ("transport_specific", "reserved0", "version_ptp",
              "message_length", "domain_number", "reserved1", "flags",
              "correction_field", "reserved2", "source_clock_identity",
              "source_port_number", "sequence_id", "control",
              "log_message_interval")


def extract_fields(model, frame):
    """Walk the model's field list over the frame's PDU bits (from byte 14).

    The 8021as_* models declare the FULL layout in wire order, so the walk
    IS the decode — the cross-decode section proves the premise every run.
    """
    pdu = bytes(frame[14:])
    nbits = len(pdu) * 8
    val = int.from_bytes(pdu, "big")
    out, pos = {}, 0
    for name, bits, _con in model.fields:
        if pos + bits > nbits:
            break
        out[name] = (val >> (nbits - pos - bits)) & ((1 << bits) - 1)
        pos += bits
    return out


class Campaign:
    def __init__(self, dut, rep, seed):
        self.dut = dut
        self.rep = rep
        self.seed = seed
        self.seq = {}                     # per-type injected sequence ids
        self.txq = []                     # every frame the plane transmitted
        self.scan = 0                     # wait_tx cursor into txq
        self.master = None                # (gm_identity, p1) we must refresh

    # ------------------------------------------------------------- transport
    def op(self, payload):
        """One command; reply = ([tx frames...], state) — state is LAST."""
        frames = self.dut.xact_all(payload)
        if not frames:
            return [], None
        st = cosim.parse_state(frames[-1])
        tx = frames[:-1] if st else frames
        self.txq.extend(tx)
        return tx, (st or None)

    def state(self):
        _, st = self.op(cosim.ctrl(cosim.CTRL_STATE))
        return st

    def send(self, frame):
        """Inject one wire frame; returns the post-settle state."""
        _, st = self.op(frame)
        return st

    def tick(self, blocks):
        """Buy the plane time: blocks × 10,000 cycles."""
        st = None
        while blocks > 0:
            n = min(blocks, 200)
            _, st = self.op(cosim.ctrl(cosim.CTRL_TICK, n))
            blocks -= n
        return st

    def responder(self, on):
        _, st = self.op(cosim.ctrl(cosim.CTRL_EVENT, 1 if on else 0))
        return st

    def reset(self):
        self.txq = []
        self.scan = 0
        _, st = self.op(cosim.ctrl(cosim.CTRL_RESET))
        return st

    # ------------------------------------------------------------- utilities
    def nseq(self, kind):
        self.seq[kind] = (self.seq.get(kind, 0) + 1) & 0xFFFF
        return self.seq[kind]

    def refresh_master(self):
        """Keep the adopted master alive across long waits (3 s receipt)."""
        if self.master:
            gm, p1 = self.master
            self.send(wire.ptp_announce(sequence_id=self.nseq("announce"),
                                        gm_identity=gm, gm_priority1=p1))

    def wait_tx(self, mtype, budget, refresh=False):
        """The next plane TX frame of `mtype` within `budget` cycles."""
        spent = 0
        while True:
            while self.scan < len(self.txq):
                f = self.txq[self.scan]
                self.scan += 1
                if len(f) > 14 and (f[14] & 0xF) == mtype:
                    return f
            if spent >= budget:
                return None
            self.tick(150)                # 1.5 M cycles
            spent += 150 * 10000
            if refresh:
                self.refresh_master()

    def drain_tx(self):
        self.scan = len(self.txq)

    def quiet_window(self, tries=80):
        """Tick 10,000-cycle blocks until the plane is silent for two.

        The plane is a timer-driven TALKER (as grandmaster a Sync every
        125 ms and an Announce every second, a Pdelay_Req every second at
        any time), so a window a probe may call quiet has to be FOUND, not
        assumed: an empty window right before an injection is what makes
        "the injected frame drew this" a measurement rather than a
        coincidence. Two empty blocks say where the plane has NOT just
        transmitted; they say nothing about the next scheduled event, so
        the caller still has to tell a collision from a dispatch (the
        caller here does it by the drop counter, and re-rolls only the
        collision).
        """
        runs = 0
        for _ in range(tries):
            mark = len(self.txq)
            self.tick(1)
            runs = runs + 1 if len(self.txq) == mark else 0
            if runs >= 2:
                return True
        return False

    def tx_of_type(self, mtype, since=0):
        return [f for f in self.txq[since:]
                if len(f) > 14 and (f[14] & 0xF) == mtype]

    @staticmethod
    def gm_of(st):
        return (st[S_GM_HI] << 32) | st[S_GM_LO]

    @staticmethod
    def parent_of(st):
        return (st[S_PAR_HI] << 32) | st[S_PAR_LO]

    @staticmethod
    def phc_of(st):
        return (st[S_PHC_HI] << 32) | st[S_PHC_LO]

    def stable(self, label, before, after,
               mask=FL_PRESENT | FL_AMGM | FL_ASCAP):
        """The stability canary: flags/GM/parent unmoved by a probe.

        FL_AMGM is in the mask so a refusal that cleared the grandmaster
        flag while leaving gm_of() == OUR_CID cannot pass the GM check
        alone (the #218 review measured that hole at 547/0).
        """
        self.rep.eq("%s: flags stable" % label,
                    after[S_FLAGS] & mask, before[S_FLAGS] & mask)
        self.rep.eq("%s: GM unmoved" % label,
                    self.gm_of(after), self.gm_of(before))
        self.rep.eq("%s: parent unmoved" % label,
                    self.parent_of(after), self.parent_of(before))

    def eq_or_gap(self, label, got, exp, issue):
        """Conformant → a passing check; nonconformant → a TRACKED gap.

        The gap fires only on the mismatch, so the day the donor closes the
        issue the check turns green on its own and the gap count drops — the
        campaign ratchets the defect out rather than pinning a magic number.
        Every gap names its FPGA-gPTP issue, per the suite's gap contract.
        """
        if got == exp:
            return self.rep.ck("%s (conformant)" % label, True)
        self.rep.gap("%s" % label,
                     "FPGA-gPTP #%d: got=%s exp=%s" % (issue, got, exp))
        return False

    def grade_tx(self, model, frame, label, skip=(), gaps=None):
        """Every spec-constrained model field of OUR frame holds.

        `gaps={field: issue}` routes a known transmit-nonconformance to a
        tracked gap instead of a failure (see eq_or_gap).
        """
        gaps = gaps or {}
        got = extract_fields(model, frame)
        for name, _bits, con in model.fields:
            if name in skip or name not in got or not con:
                continue
            # ONE KIND PER FIELD, and tsn_model decides it, not this grader. A
            # field declaring two kinds is refused before any dispatch, with
            # the message legal()/illegal() raise for the same field, so the
            # three readers cannot resolve a combination three ways (#151).
            # The producer resolves it a fourth: packet_builder.cpp::pickValue
            # merges `value` into `values` and drops a `mask` or `range`
            # standing beside them, while the chain below used to stop at the
            # first kind it met, so `value: 3` beside `values: [1, 2, 3]`
            # would have graded a frame carrying 1 RED and blamed the DUT.
            refused = tsn_model.kind_conflict(name, con)
            if refused:
                self.rep.ck("%s.%s declares one constraint kind"
                            % (label, name), False, refused)
                continue
            # Dispatch order matches tsn_model.legal()/illegal() exactly:
            # value, values, range, mask. With one kind per field the order
            # decides nothing; it is kept identical so the three stay diffable.
            if "value" in con:
                if name in gaps:
                    self.eq_or_gap("%s.%s" % (label, name), got[name],
                                   int(con["value"]), gaps[name])
                else:
                    self.rep.eq("%s.%s" % (label, name), got[name],
                                int(con["value"]))
            elif "values" in con:
                self.rep.ck("%s.%s legal" % (label, name),
                            got[name] in [int(v) for v in con["values"]],
                            "got=%d" % got[name])
            elif "range" in con:
                lo, hi = int(con["range"][0]), int(con["range"][1])
                self.rep.ck("%s.%s in [%d,%d]" % (label, name, lo, hi),
                            lo <= got[name] <= hi, "got=%d" % got[name])
            elif "mask" in con:
                # A mask names the DEFINED bits; the spec claim is that no bit
                # outside that set is set. tsn_model already reads masks this
                # way for probe generation (legal/illegal), so grade to match.
                m = int(con["mask"][0])
                undef = got[name] & ~m
                self.rep.ck("%s.%s within defined bits" % (label, name),
                            undef == 0,
                            "got=0x%X undefined=0x%X mask=0x%X"
                            % (got[name], undef, m))
            else:
                # FAIL CLOSED. A constraint kind this grader does not know must
                # never pass in silence: that is exactly how an Announce `mask:`
                # pin left the campaign once already, with the tally unmoved and
                # nothing red to notice. Anyone adding a kind has to teach the
                # grader what it asserts before the suite will go green again.
                self.rep.ck("%s.%s constraint is gradeable" % (label, name),
                            False,
                            "ungradeable constraint kind %s -- teach grade_tx"
                            % sorted(con))
        return got

    def become_gm(self, budget=10 * SECOND):
        """Wait out the announce-receipt timeout: back to a clean GM baseline.

        A GM with no better master heard is the campaign's re-establishable
        baseline for the BTCA rejection probes — each defect probe adopts a
        bad master, and letting it expire returns the plane to GM=us so the
        next probe starts from known state.
        """
        st = self.state()
        spent = 0
        while not (st[S_FLAGS] & FL_AMGM) and spent < budget:
            st = self.tick(100)
            spent += 100 * 10000
        return st

    # ------------------------------------------------------------ 1 models
    def inventory(self):
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
    def cross_decode(self, models):
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
    def boot(self, models):
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
    def climb(self, label="climb"):
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
    def gm_tx(self, models):
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
    def parser_gates(self, models):
        self.rep.section("parser gates: what must drop, drops; "
                         "what 11.4.1 ignores, passes")
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

    # ------------------------------------------- 7 the responder role
    def responder_correct(self, models):
        self.rep.section("pdelay responder: Resp + Resp_Follow_Up conform")
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
        def unpaired_probe(label, frame):
            before = self.state()
            after = self.send(frame)
            self.rep.eq("%s: peer delay unmoved" % label,
                        after[S_PDELAY], before[S_PDELAY])
            self.rep.eq("%s: asCapable unmoved" % label,
                        after[S_FLAGS] & FL_ASCAP,
                        before[S_FLAGS] & FL_ASCAP)
            self.stable(label, before, after)

        # (a) NOTHING ARMED. Until a Pdelay_Resp answers our outstanding
        # request the pairing register holds no sequence, and every
        # Follow_Up must be refused on that alone.
        unpaired_probe(
            "stale Pdelay_Resp_Follow_Up ignored (11.2.15.3)",
            wire.ptp_pdelay_resp_fu(
                sequence_id=0xEEEE, t3_ns=1000,
                requesting_clock_identity=OUR_CID,
                source_clock_identity=PEER_CID))
        # sequence 0 ahead of any Pdelay_Resp: "armed with sequence 0" is
        # not "nothing armed", so a pairing register cleared to zero must
        # not read as a match
        unpaired_probe(
            "sequence-0 Pdelay_Resp_Follow_Up ahead of its Resp ignored",
            wire.ptp_pdelay_resp_fu(
                sequence_id=0, t3_ns=3000,
                requesting_clock_identity=OUR_CID,
                source_clock_identity=PEER_CID))

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
            unpaired_probe(
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
            unpaired_probe(
                "Pdelay_Resp for another requester arms nothing (11.2.15.3)",
                wire.ptp_pdelay_resp_fu(
                    sequence_id=oseq, t3_ns=armed_t2 + 200,
                    requesting_clock_identity=OUR_CID,
                    source_clock_identity=PEER_CID))

            # arm it for real: domain 0, our requestingPortIdentity, the
            # plane's outstanding sequenceId, from the usual responder
            self.send(wire.ptp_pdelay_resp(
                sequence_id=oseq, t2_ns=armed_t2,
                requesting_clock_identity=OUR_CID,
                source_clock_identity=PEER_CID))
            # the armed sequence with its HIGH byte flipped: the low bytes
            # agree, so a compare narrowed to one byte takes this frame and
            # publishes its t3
            unpaired_probe(
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
            unpaired_probe(
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
            unpaired_probe(
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
            unpaired_probe(
                "ARMED: Follow_Up at a foreign requesting portNumber "
                "ignored (engine hardening, not Figure 11-8)",
                wire.ptp_pdelay_resp_fu(
                    sequence_id=oseq, t3_ns=armed_t2 + 200,
                    requesting_clock_identity=OUR_CID,
                    requesting_port_number=(
                        wire.PtpMsg(oreq).source_port_number ^ 0xFFFF),
                    source_clock_identity=PEER_CID))
        self.responder(True)

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

            def replay(t3_extra):
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

    # ----------------------------------------------------------- 8 BTCA
    def btca(self):
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
        def reject_probe(label, issue, drop, **kw):
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

        # parser-owned rejects: bad_r drops them at the header, counted, and
        # GM / parent / asCapable hold. The domain arm is the FPGA-gPTP #6
        # fix (8.1; IEEE 1588-2008 9.5.1); it is probed separately from the
        # Sync/Follow_Up side in sync_pairs so one fixed path cannot hide
        # the other
        reject_probe("better vector, version 1", None, drop=1, version_ptp=1)
        reject_probe("better vector, transportSpecific 0", None, drop=1,
                     transport_specific=0)
        reject_probe("better vector, domain 5 (8.1: single domain 0)",
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
        reject_probe("better vector, own sourcePortIdentity (10.3.10.2.1a)",
                     None, drop=None, source_clock_identity=OUR_CID,
                     src=wire.GPTP_PEER2_MAC)
        # (b) can no longer ride a PathTrace TLV: stepsRemoved 255 demands
        # 256 identities, 2052 TLV octets, past the 1500-octet Ethernet
        # payload the parser admits (its MAX_MSG_LEN_C). The TLV-absent
        # 64-octet Announce (count and loop verdict honestly zero) is the
        # one wire-legal carrier left, and it reaches STEPS_MAX_C in
        # qualifyAnnounce with the parser satisfied
        reject_probe("better vector, stepsRemoved 255, no path trace "
                     "(10.3.10.2.1b)", None, drop=None, steps_removed=255,
                     path_trace=[])
        reject_probe("better vector, stepsRemoved 0x0100, no path trace "
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
        reject_probe("better vector, our id in the path trace "
                     "(10.3.10.2.1c)", None, drop=None, gm_identity=0x3333,
                     steps_removed=1, path_trace=[0x3333, OUR_CID])
        reject_probe("better vector, our own Announce a bridge extended: "
                     "us the first path-trace hop (10.3.10.2.1c)", None,
                     drop=None, gm_identity=OUR_CID, steps_removed=1,
                     path_trace=[OUR_CID, PEER2_CID])
        reject_probe("better vector, our own Announce reflected: us the "
                     "only path-trace hop (10.3.10.2.1c)", None, drop=None,
                     gm_identity=OUR_CID, path_trace=[OUR_CID])
        # the strict wire rules themselves (FPGA-gPTP #45; 10.5.3.3.4):
        # a head that is not the announced grandmaster, a count that is not
        # stepsRemoved+1, and the old wire-illegal (b) shape. Each is
        # refused AT THE PARSER, a counted header drop, before
        # qualifyAnnounce sees a bank
        reject_probe("better vector, path-trace head is not the announced "
                     "grandmaster (10.5.3.3.4)", None, drop=1,
                     gm_identity=0x3333, path_trace=[0x5555])
        reject_probe("better vector, one path-trace hop against "
                     "stepsRemoved 1 (10.5.3.3.4)", None, drop=1,
                     gm_identity=0x3333, steps_removed=1,
                     path_trace=[0x3333])
        reject_probe("better vector, stepsRemoved 255 on a one-hop path "
                     "trace (10.5.3.3.4)", None, drop=1, steps_removed=255)

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
    def sync_pairs(self):
        self.rep.section("sync consumption: clean pairs move the servo, "
                         "malformed ones cannot")

        def pair(delta, domain=0, fu_seq=None, fu_src=PEER_CID,
                 sync_flags=0x0208):
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

        # adopt GMID and settle a clean baseline before the servo probes
        self.master = (GMID, 100)
        self.refresh_master()
        self.tick(2)
        st = pair(1000)
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
            after = pair(**kw)
            self.rep.eq("%s: offset unmoved" % label, after[S_OFFSET], b_off)
            self.stable(label, before, after)
        # a domain-5 pair is refused at the header (8.1; IEEE 1588-2008
        # 9.5.1): both frames drop before the servo can see them, so the
        # offset, the sync verdict, GM, parent and asCapable hold and the
        # drops are counted. Probed separately from the BTCA-side domain
        # probe so one fixed path cannot hide the other (FPGA-gPTP #6)
        self.refresh_master()
        before = self.state()
        after = pair(delta=40000, domain=5)
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

        # the servo recovers on the next clean pair
        self.refresh_master()
        st = pair(1000)
        off = st[S_OFFSET] - (1 << 32) if st[S_OFFSET] >> 31 else st[S_OFFSET]
        self.rep.ck("recovery pair: offset back near +1000",
                    abs(off - 1000) <= 300, "offset=%d" % off)

    # --------------------------------------- 10 the accept side (issue #217)
    def suffix_accept(self):
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

        def steer(label, delta, sync_suffix, fu_suffix):
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

        steer("suffixed Sync, 44 plus 12 declared 56", 3000, suf, b"")
        steer("suffixed Follow_Up, 76 plus 12 declared 88", 7000, b"", suf)

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
        def exchange_completes(label, resp_suffix, rfu_suffix):
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

        exchange_completes("suffixed Pdelay_Resp, 54 plus 12 declared 66",
                           suf, b"")
        exchange_completes("suffixed Pdelay_Resp_Follow_Up, 54 plus 12 "
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
    def cease(self):
        self.rep.section("Milan 4.2.6.2.5: multiple responders cease "
                         "Pdelay_Req; duplicates do not")
        self.responder(False)

        def answer(req, cids):
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

        def serve(blocks, cids):
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
    def storms(self, models, rounds):
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
    def drought(self):
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


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dut", default="obj_ptp/Vptp_cosim")
    ap.add_argument("--rounds", type=int, default=32)
    ap.add_argument("--seed", type=int, default=20260819)
    args = ap.parse_args()

    rep = cosim.Report(
        "gPTP/802.1AS field campaign (tsn-gen driven)",
        dut="KL_gptp_shadow + timestamp_counter + KL_gptp_txstamp "
            "(the fabric slice, gptp-processor engine)",
        rtl_files=["hdl/ieee8021as/gptp_plane/KL_gptp_shadow.sv",
                   "hdl/ieee8021as/gptp_plane/KL_gptp_txstamp.sv",
                   "hdl/ieee8021as/ptp_timestamp/timestamp_counter.sv",
                   "gptp-processor/hdl/top/KL_gptp_engine.sv",
                   "gptp-processor/hdl/wire/KL_gptp_rx_parser.sv",
                   "gptp-processor/hdl/wire/KL_gptp_tx_slot.sv"],
        results_dir="../../../hdl/ieee8021as/gptp_plane/doc",
        reproduce="cd tb/verilator/tsn_fuzz && make ptp")
    cosim.require_tsn_gen(rep, "gPTP/802.1AS field campaign")
    require_ptp_models(rep)
    with cosim.Dut(args.dut) as dut:
        c = Campaign(dut, rep, args.seed)
        models = c.inventory()
        c.cross_decode(models)
        c.boot(models)
        c.climb()
        c.gm_tx(models)
        c.parser_gates(models)
        c.responder_correct(models)
        c.btca()
        c.sync_pairs()
        c.suffix_accept()
        c.cease()
        c.storms(models, args.rounds)
        c.drought()
    return rep.done()


if __name__ == "__main__":
    sys.exit(main())
