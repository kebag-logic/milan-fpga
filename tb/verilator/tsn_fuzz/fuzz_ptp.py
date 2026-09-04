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

WHERE THE PARTS LIVE.  This file is the entry point and `Campaign` itself: the
primitives every section drives the DUT through, and the run order.  The
sections are three siblings beside it, mixed into `Campaign`, so one area can
be read without the other two:

  * `fuzz_ptp_defs.py`      the state_dump word order, identities, model list
  * `fuzz_ptp_bringup.py`   1-6 models, cross-decode, boot, climb, gm, parser
  * `fuzz_ptp_responder.py` 7  the Pdelay responder role
  * `fuzz_ptp_timing.py`    8-13 BTCA, sync pairs, suffix, cease, storms
"""
import argparse
import sys
from collections.abc import Sequence

import cosim
import tsn_model
import wire

# Re-exported: `import fuzz_ptp` reaches the campaign's whole
# vocabulary through the one name its consumers already import.
# ruff: noqa: F401
from fuzz_ptp_defs import (BUILD, D_NOM, FL_AMGM, FL_ASCAP, FL_PRESENT,
                           FL_SYNCOK, FieldModel, GMID, HDR_FIELDS, MODELS, MS,
                           OUR_CID, PEER2_CID, PEER_CID, PTP_TYPE, SECOND,
                           S_FLAGS, S_GM_HI, S_GM_LO, S_OFFSET, S_PAR_HI,
                           S_PAR_LO, S_PDELAY, S_PDEXP, S_PHC_HI, S_PHC_LO,
                           S_PROGRUN, S_RXDROP, S_TAPDROP, S_TXCNT, S_TXTSCNT,
                           S_TXTSSEQ, extract_fields, require_ptp_models)
from fuzz_ptp_bringup import PtpBringUpSections
from fuzz_ptp_responder import PtpResponderSections
from fuzz_ptp_timing import PtpTimingSections


class Campaign(PtpBringUpSections, PtpResponderSections,
               PtpTimingSections):
    def __init__(self, dut, rep, seed):
        self.dut = dut
        self.rep = rep
        self.seed = seed
        self.seq = {}                     # per-type injected sequence ids
        self.txq = []                     # every frame the plane transmitted
        self.scan = 0                     # wait_tx cursor into txq
        self.master = None                # (gm_identity, p1) we must refresh

    # ------------------------------------------------------------- transport
    def op(self, payload: bytes) -> tuple[list[bytes], list[int] | None]:
        """One command; reply = ([tx frames...], state) — state is LAST."""
        frames = self.dut.xact_all(payload)
        if not frames:
            return [], None
        st = cosim.parse_state(frames[-1])
        tx = frames[:-1] if st else frames
        self.txq.extend(tx)
        return tx, (st or None)

    def state(self) -> list[int] | None:
        """The plane's observable state right now, as the STATE word list."""
        _, st = self.op(cosim.ctrl(cosim.CTRL_STATE))
        return st

    def send(self, frame: bytes) -> list[int] | None:
        """Inject one wire frame; returns the post-settle state."""
        _, st = self.op(frame)
        return st

    def tick(self, blocks: int) -> list[int] | None:
        """Buy the plane time: blocks × 10,000 cycles."""
        st = None
        while blocks > 0:
            n = min(blocks, 200)
            _, st = self.op(cosim.ctrl(cosim.CTRL_TICK, n))
            blocks -= n
        return st

    def responder(self, on: bool) -> list[int] | None:
        """Turn the bench's Pdelay responder on or off."""
        _, st = self.op(cosim.ctrl(cosim.CTRL_EVENT, 1 if on else 0))
        return st

    def reset(self) -> list[int] | None:
        """Reset the DUT and the transmit log together: a surviving `scan`
        would index into a previous life's frames."""
        self.txq = []
        self.scan = 0
        _, st = self.op(cosim.ctrl(cosim.CTRL_RESET))
        return st

    # ------------------------------------------------------------- utilities
    def nseq(self, kind: str) -> int:
        """The next injected sequenceId for one message kind, wrapped to
        the wire's 16 bits."""
        self.seq[kind] = (self.seq.get(kind, 0) + 1) & 0xFFFF
        return self.seq[kind]

    def refresh_master(self) -> None:
        """Keep the adopted master alive across long waits (3 s receipt)."""
        if self.master:
            gm, p1 = self.master
            self.send(wire.ptp_announce(sequence_id=self.nseq("announce"),
                                        gm_identity=gm, gm_priority1=p1))

    def wait_tx(self, mtype: int, budget: int,
                refresh: bool = False) -> bytes | None:
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

    def drain_tx(self) -> None:
        """Forget every frame transmitted so far, so the next `wait_tx`
        measures only what the probe about to run draws."""
        self.scan = len(self.txq)

    def quiet_window(self, tries: int = 80) -> bool:
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

    def tx_of_type(self, mtype: int, since: int = 0) -> list[bytes]:
        """Every logged transmission of one messageType from `since` on."""
        return [f for f in self.txq[since:]
                if len(f) > 14 and (f[14] & 0xF) == mtype]

    @staticmethod
    def gm_of(st: list[int]) -> int:
        """The published grandmasterIdentity out of a state dump."""
        return (st[S_GM_HI] << 32) | st[S_GM_LO]

    @staticmethod
    def parent_of(st: list[int]) -> int:
        """The published parent (source) identity out of a state dump."""
        return (st[S_PAR_HI] << 32) | st[S_PAR_LO]

    @staticmethod
    def phc_of(st: list[int]) -> int:
        """The fabric PHC's nanosecond count out of a state dump."""
        return (st[S_PHC_HI] << 32) | st[S_PHC_LO]

    def stable(self, label: str, before: list[int], after: list[int],
               mask: int = FL_PRESENT | FL_AMGM | FL_ASCAP) -> None:
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

    def eq_or_gap(self, label: str, got: int, exp: int, issue: int) -> bool:
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

    def grade_tx(self, model: FieldModel, frame: bytes, label: str,
                 skip: Sequence[str] = (),
                 gaps: dict[str, int] | None = None) -> dict[str, int]:
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

    def become_gm(self, budget: int = 10 * SECOND) -> list[int] | None:
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


def main() -> int:
    """Run every section against one DUT and return the suite's exit
    status: nonzero only when a graded check failed."""
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
