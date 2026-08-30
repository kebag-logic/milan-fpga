#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""
AAF / AVTP stream field campaign (parser -> rx monitor -> depacketizer).

AAF is the data plane, so "did it answer?" is meaningless — the DUT answers
in COUNTERS. Every fuzzed stream PDU is graded by which counter moved, which
makes the accept/reject verdict per field directly observable:

    good PDU            frames_rx++, pcm_pdus++, and after a few, media LOCK
    sequence jump       seq_mismatch++ / stream_interrupted++ ... but LOCKED
    unsupported format  unsupported_fmt++ and frames_rx UNCHANGED (rejected
                        before acceptance, so no bad audio reaches fabric)
    foreign stream_id   nothing moves at all (not our stream)
    non-AAF subtype     ignored by the parser

The gate that matters for audio is the last column: **a malformed PDU must
never knock a locked stream out of lock**. An unlock is an audible dropout
and a Milan compliance failure, so the campaign asserts lock survival after
every single malformed probe and after a full random storm.

Run: python3 fuzz_aaf.py [--rounds N] [--seed S]
"""
import argparse
import random
import sys

import cosim
import tsn_model
import wire

# state_dump() word order — must match cosim_aaf.cpp (APPEND ONLY)
(C_FRAMES, C_LOCKCNT, C_UNLOCKCNT, C_INTERRUPT, C_SEQMM, C_TSUNC, C_UNSUPFMT,
 C_MRESET, C_LATE, C_EARLY, C_LOCKED, C_PCMPDUS, C_PCMDROPS, C_MATCH,
 C_LASTTS, C_PARSED, C_MATCHED) = range(17)

NAMES = ["frames_rx", "media_locked_cnt", "media_unlocked_cnt", "stream_interrupted",
         "seq_mismatch", "ts_uncertain", "unsupported_fmt", "media_reset",
         "late_ts", "early_ts", "media_locked", "pcm_pdus", "pcm_drops",
         "match", "last_ts", "parser_parsed", "parser_matched"]

#: the bench stream (mirrors tb/verilator/avtp_rxmon and cosim_aaf.cpp)
SID = 0x020000FFFE010000
GOOD = dict(stream_id=SID, sv=1, tv=1, aaf_format=0x02, nsr=0x05,
            channels_per_frame=8, bit_depth=32, avtp_timestamp=0xA55AC33C,
            stream_data_length=64)


class Campaign:
    def __init__(self, dut, rep, seed):
        self.dut = dut
        self.rep = rep
        self.seed = seed
        self.seq = 0

    # ------------------------------------------------------------- primitives
    def pdu(self, **kw):
        cfg = dict(GOOD)
        cfg.update(kw)
        if "sequence_num" not in cfg:
            self.seq = (self.seq + 1) & 0xFF
            cfg["sequence_num"] = self.seq
        return wire.aaf_pdu(**cfg)

    def send(self, **kw):
        """Feed one PDU; the reply IS the counter snapshot."""
        return cosim.parse_state(self.dut.xact(self.pdu(**kw)))

    def state(self):
        return cosim.read_state(self.dut)

    def reset(self):
        self.seq = 0
        return cosim.parse_state(self.dut.xact(cosim.ctrl(cosim.CTRL_RESET)))

    def lock_stream(self, n=10):
        """Drive the stream to media lock and return the locked snapshot."""
        st = self.reset()
        for _ in range(n):
            st = self.send()
        return st

    def delta(self, before, after):
        return {NAMES[i]: after[i] - before[i]
                for i in range(len(NAMES)) if after[i] != before[i]}

    # -------------------------------------------------------------- 1 model
    def model_inventory(self):
        self.rep.section("AVTP stream model inventory (tsn-gen)")
        try:
            m = tsn_model.load("avtp", "1722_avtp_common_stream.yaml",
                               "1722_avtp_common_stream::AVTP_STREAM::AVTP_STREAM_IF")
        except (OSError, ValueError) as exc:
            self.rep.ck("AVTP stream model loads", False, str(exc))
            return None
        self.rep.ck("AVTP stream model loads", True, "%d fields" % len(m.fields))
        for name, bits, con in m.fields:
            self.rep.ck("  field %-24s %3d bits%s"
                        % (name, bits, "  (spec-constrained)" if con else ""), True)
        return m

    # ----------------------------------------------------------- 2 baseline
    def baseline(self):
        self.rep.section("baseline: a good stream locks and reaches the depacketizer output")
        st0 = self.reset()
        self.rep.eq("fresh stack: not locked", st0[C_LOCKED], 0)
        self.rep.eq("fresh stack: no frames", st0[C_FRAMES], 0)
        st = st0
        for i in range(10):
            st = self.send()
        self.rep.eq("10 good PDUs -> frames_rx", st[C_FRAMES], 10)
        self.rep.eq("10 good PDUs -> pcm_pdus (payload reached fabric output)",
                    st[C_PCMPDUS], 10)
        self.rep.eq("media LOCKED", st[C_LOCKED], 1)
        self.rep.ck("lock counted exactly once", st[C_LOCKCNT] == 1,
                    "media_locked_cnt=%d" % st[C_LOCKCNT])
        self.rep.eq("no spurious unlock", st[C_UNLOCKCNT], 0)
        self.rep.eq("no sequence mismatch on a clean run", st[C_SEQMM], 0)
        self.rep.eq("no unsupported-format hits on a clean run", st[C_UNSUPFMT], 0)
        self.rep.eq("no dropped PCM", st[C_PCMDROPS], 0)

    # ------------------------------------------------- 3 per-field verdicts
    def field_verdicts(self):
        self.rep.section("per-field accept/reject verdicts (lock must survive)")
        # label, PDU overrides, counter that must move, frames_rx accepted?
        #
        # channels_per_frame is deliberately absent: the listener follows WIRE
        # TRUTH for the channel count rather than rejecting a PDU that
        # disagrees with the bound format's declared channels. That is the fix
        # for the declared-8ch / wire-2ch silence bug — a talker sending fewer
        # channels than the format advertises must still render, de-interleaved
        # by the PDU's own count (the wire_chans path the chmap64 render
        # crossbar consumes). Covered as an ACCEPTED probe below, not a
        # rejection.
        probes = [
            ("sequence jump", dict(sequence_num=0x7F), C_SEQMM, True),
            ("unsupported bit_depth", dict(bit_depth=17), C_UNSUPFMT, False),
            ("unsupported nsr", dict(nsr=0x0F), C_UNSUPFMT, False),
            ("unsupported aaf_format", dict(aaf_format=0xFF), C_UNSUPFMT, False),
        ]
        for label, kw, counter, accepted in probes:
            before = self.lock_stream()
            self.rep.eq("%s: locked before the probe" % label, before[C_LOCKED], 1)
            after = self.send(**kw)
            moved = self.delta(before, after)
            self.rep.ck("%s: flagged (%s moved)" % (label, NAMES[counter]),
                        after[counter] > before[counter], str(moved))
            if accepted:
                self.rep.ck("%s: still accepted (frames_rx advanced)" % label,
                            after[C_FRAMES] > before[C_FRAMES], str(moved))
            else:
                self.rep.eq("%s: REJECTED before acceptance (frames_rx frozen)"
                            % label, after[C_FRAMES], before[C_FRAMES])
                self.rep.eq("%s: no bad payload reached fabric output" % label,
                            after[C_PCMPDUS], before[C_PCMPDUS])
            self.rep.eq("%s: STREAM STAYS LOCKED" % label, after[C_LOCKED], 1)
            self.rep.eq("%s: no unlock event" % label,
                        after[C_UNLOCKCNT], before[C_UNLOCKCNT])

    def wire_truth(self):
        """channels_per_frame follows the WIRE, it does not reject the PDU."""
        self.rep.section("wire-truth channel count (declared-vs-wire mismatch)")
        for chans in (1, 2, 3, 4, 8):
            before = self.lock_stream()
            after = self.send(channels_per_frame=chans)
            self.rep.ck("channels_per_frame=%d: accepted (wire truth)" % chans,
                        after[C_FRAMES] > before[C_FRAMES],
                        str(self.delta(before, after)))
            self.rep.eq("channels_per_frame=%d: not flagged unsupported" % chans,
                        after[C_UNSUPFMT], before[C_UNSUPFMT])
            self.rep.eq("channels_per_frame=%d: reaches fabric output" % chans,
                        after[C_PCMPDUS], before[C_PCMPDUS] + 1)
            self.rep.eq("channels_per_frame=%d: STREAM STAYS LOCKED" % chans,
                        after[C_LOCKED], 1)

    # ------------------------------------------------------- 4 non-our-stream
    def foreign(self):
        self.rep.section("foreign stream_id and non-AAF subtypes are ignored")
        for label, kw in (("foreign stream_id", dict(stream_id=0xDEADBEEFCAFEBABE)),
                          ("stream_id off by one", dict(stream_id=SID + 1)),
                          ("CVF subtype 0x03", dict()),
                          ("control subtype 0xFB", dict())):
            before = self.lock_stream()
            if label == "CVF subtype 0x03":
                frame = bytearray(self.pdu()); frame[14] = 0x03
                after = cosim.parse_state(self.dut.xact(bytes(frame)))
            elif label == "control subtype 0xFB":
                frame = bytearray(self.pdu()); frame[14] = 0xFB
                after = cosim.parse_state(self.dut.xact(bytes(frame)))
            else:
                after = self.send(**kw)
            moved = self.delta(before, after)
            self.rep.eq("%s: not accepted as our stream" % label,
                        after[C_FRAMES], before[C_FRAMES])
            self.rep.eq("%s: nothing reached fabric output" % label,
                        after[C_PCMPDUS], before[C_PCMPDUS])
            self.rep.eq("%s: STREAM STAYS LOCKED" % label, after[C_LOCKED], 1)
            if moved:
                self.rep.note("%s moved: %s" % (label, moved))

    # ------------------------------------------------ 4b the ACCEPT VERDICT
    def accept_verdict(self):
        """The listener ACCEPT VERDICT itself, graded on the parser counters.

        Every other section of this campaign fuzzes fields of a frame that
        ALREADY matched. This one fuzzes the match: the parser's own
        free-running `parsed`/`matched` counters — the sources milan_datapath
        publishes as APRB_PARSED `0x8B4` / APRB_MATCHED `0x8B8` — are graded
        against an exact model: accept **iff** the eight wire bytes at o+4
        equal the bound stream_id, MS byte first.

        That makes the open 8×8 blocker's signature a verdict this campaign
        can state rather than infer: *PARSED climbs, MATCHED does not*. The
        population is the way software and the wire can disagree while both
        ends believe they agree — every single-bit flip across the full 64,
        the byte-reversal, the `SID_LO`/`SID_HI` transposition, per-byte
        corruption — plus a seeded random sid population.
        """
        self.rep.section("listener ACCEPT VERDICT: wire stream_id vs bound sid")
        st = self.lock_stream()
        self.rep.eq("locked before the sid sweep", st[C_LOCKED], 1)

        def probe(label, sid, expect_match):
            before = self.state()
            after = self.send(stream_id=sid)
            if not after:
                self.rep.ck("%s: DUT answered" % label, False, "no state")
                return None
            self.rep.eq("%s: parser PARSED climbs" % label,
                        after[C_PARSED] - before[C_PARSED], 1)
            self.rep.eq("%s: parser MATCHED %s" % (label,
                        "climbs" if expect_match else "STATIC"),
                        after[C_MATCHED] - before[C_MATCHED],
                        1 if expect_match else 0)
            self.rep.eq("%s: frames_rx %s" % (label,
                        "advanced" if expect_match else "frozen"),
                        after[C_FRAMES] - before[C_FRAMES],
                        1 if expect_match else 0)
            return after

        # the exact bound sid: the positive control the whole section rests on
        probe("exact bound sid", SID, True)

        # every single-bit flip: the compare must be all 64 bits wide
        bad = 0
        for b in range(64):
            before = self.state()
            after = self.send(stream_id=SID ^ (1 << b))
            if not after:
                bad += 1
                continue
            if (after[C_PARSED] - before[C_PARSED] != 1 or
                    after[C_MATCHED] != before[C_MATCHED] or
                    after[C_FRAMES] != before[C_FRAMES]):
                bad += 1
                self.rep.note("bit %d flip was not rejected cleanly: %s"
                              % (b, self.delta(before, after)))
        self.rep.eq("all 64 single-bit sid flips rejected, all parsed", bad, 0)

        # the named ways a controller and the wire disagree
        rev = int.from_bytes(SID.to_bytes(8, "big"), "little")
        transposed = ((SID >> 32) | ((SID & 0xFFFFFFFF) << 32)) & (2 ** 64 - 1)
        named = [("byte-reversed sid (LE/BE confusion)", rev),
                 ("SID_LO/SID_HI transposed", transposed),
                 ("all-ones sid", 2 ** 64 - 1),
                 ("zero sid", 0),
                 ("sid + 1 (uid off by one)", SID + 1),
                 ("sid - 1", SID - 1)]
        for label, sid in named:
            probe(label, sid, sid == SID)
        # per-byte corruption: each wire byte of the sid is load-bearing
        for i in range(8):
            probe("wire sid byte %d corrupted" % i, SID ^ (0xFF << (8 * i)), False)

        # a VLAN-tagged frame carrying the bound sid must accept identically:
        # the header offset moves by 4 and the verdict must not
        before = self.state()
        tagged = wire.aaf_pdu(**dict(GOOD, sequence_num=(self.seq + 1) & 0xFF,
                                     vlan=2))
        self.seq = (self.seq + 1) & 0xFF
        after = cosim.parse_state(self.dut.xact(tagged))
        self.rep.eq("C-VLAN tagged, bound sid: parser PARSED climbs",
                    after[C_PARSED] - before[C_PARSED], 1)
        self.rep.eq("C-VLAN tagged, bound sid: parser MATCHED climbs",
                    after[C_MATCHED] - before[C_MATCHED], 1)
        self.rep.eq("C-VLAN tagged, bound sid: accepted (frames_rx)",
                    after[C_FRAMES] - before[C_FRAMES], 1)
        # ...and a tagged frame carrying a FOREIGN sid is still rejected, so
        # the tagged path is not a blanket accept
        before = self.state()
        tagged_bad = wire.aaf_pdu(**dict(GOOD, stream_id=SID ^ 0x0100,
                                         sequence_num=(self.seq + 1) & 0xFF,
                                         vlan=2))
        self.seq = (self.seq + 1) & 0xFF
        after = cosim.parse_state(self.dut.xact(tagged_bad))
        self.rep.eq("C-VLAN tagged, foreign sid: PARSED climbs",
                    after[C_PARSED] - before[C_PARSED], 1)
        self.rep.eq("C-VLAN tagged, foreign sid: MATCHED STATIC",
                    after[C_MATCHED] - before[C_MATCHED], 0)

        # seeded random sid population, verdict predicted by the model
        rnd = random.Random(self.seed ^ 0x5A1D)
        mism = 0
        for _ in range(96):
            sid = rnd.getrandbits(64)
            if rnd.random() < 0.25:
                sid = SID              # keep a real accept population in the mix
            before = self.state()
            after = self.send(stream_id=sid)
            want = 1 if sid == SID else 0
            if not after or after[C_MATCHED] - before[C_MATCHED] != want \
                    or after[C_PARSED] - before[C_PARSED] != 1:
                mism += 1
                self.rep.note("random sid 0x%016X mis-verdicted: %s"
                              % (sid, self.delta(before, after or before)))
        self.rep.eq("96 random stream_ids: verdict matched the model every time",
                    mism, 0)

        end = self.state()
        self.rep.ck("sid sweep: parser saw every probe",
                    end[C_PARSED] > st[C_PARSED],
                    "parsed %d -> %d, matched %d -> %d"
                    % (st[C_PARSED], end[C_PARSED], st[C_MATCHED], end[C_MATCHED]))

        # The gate here is the OPPOSITE of every other section's. Elsewhere a
        # malformed PDU must never unlock the stream; here the frames are
        # perfectly formed and simply are not ours, so a sustained accept
        # drought MUST unlock — a listener still reporting MEDIA_LOCKED while
        # it accepts nothing is lying to the controller, and that is exactly
        # the state a silicon read must be able to tell apart from a healthy
        # one (PARSED climbing + MATCHED static + UNLOCKED = "not my stream",
        # not "no traffic").
        st2 = self.lock_stream()
        self.rep.eq("re-locked before the accept drought", st2[C_LOCKED], 1)
        drought = st2
        for _ in range(60):
            drought = self.send(stream_id=SID ^ 0xDEAD)
        self.rep.eq("accept drought: parser PARSED climbed by 60",
                    drought[C_PARSED] - st2[C_PARSED], 60)
        self.rep.eq("accept drought: parser MATCHED never moved",
                    drought[C_MATCHED], st2[C_MATCHED])
        self.rep.eq("accept drought: frames_rx never moved",
                    drought[C_FRAMES], st2[C_FRAMES])
        self.rep.eq("accept drought: nothing reached fabric output",
                    drought[C_PCMPDUS], st2[C_PCMPDUS])
        self.rep.eq("accept drought: media UNLOCKED (no LOCKED lie)",
                    drought[C_LOCKED], 0)
        self.rep.ck("accept drought: unlock counted",
                    drought[C_UNLOCKCNT] > st2[C_UNLOCKCNT],
                    "unlock cnt %d -> %d" % (st2[C_UNLOCKCNT], drought[C_UNLOCKCNT]))
        fresh = self.lock_stream()
        self.rep.eq("re-locks cleanly after the drought", fresh[C_LOCKED], 1)

    # ------------------------------------------------------- 5 truncation
    def truncation(self):
        self.rep.section("truncated / oversized stream PDUs")
        full = self.pdu()
        for label, frame in (("header cut mid-stream_id", full[:24]),
                             ("header only, no payload", full[:38]),
                             ("one byte of payload", full[:39]),
                             ("declared 64 B, sent 8 B",
                              wire.aaf_pdu(**dict(GOOD, sequence_num=5,
                                                  payload=bytes(8)))),
                             ("oversized payload", full + bytes(256))):
            before = self.lock_stream()
            after = cosim.parse_state(self.dut.xact(frame))
            if not after:
                self.rep.ck("%s: DUT still responsive" % label, False, "no state")
                continue
            self.rep.eq("%s: STREAM STAYS LOCKED" % label, after[C_LOCKED], 1)
            self.rep.ck("%s: no PCM overrun" % label,
                        after[C_PCMDROPS] == before[C_PCMDROPS],
                        "drops %d -> %d" % (before[C_PCMDROPS], after[C_PCMDROPS]))
            self.rep.ck("%s: counters stayed monotonic" % label,
                        all(after[i] >= before[i] for i in
                            (C_FRAMES, C_PCMPDUS, C_SEQMM, C_UNSUPFMT)), "")

    # ------------------------------------------------------------ 6 storm
    def storm(self, m, rounds):
        self.rep.section("tsn-gen constrained-random storm + lock stability")
        if m is None:
            return
        sets = m.random(rounds, self.seed)
        self.rep.ck("tsn-gen produced constrained-random AVTP field sets",
                    len(sets) > 0, "%d sets (seed %d)" % (len(sets), self.seed))
        before = self.lock_stream()
        self.rep.eq("locked before the storm", before[C_LOCKED], 1)
        last = before
        for fs in sets:
            last = self.send(
                sequence_num=fs.get("sequence_num", 0) & 0xFF,
                sv=fs.get("sv", 1) & 1,
                version=fs.get("version", 0) & 7,
                mr=fs.get("mr", 0) & 1,
                tv=fs.get("tv", 1) & 1,
                tu=fs.get("tu", 0) & 0x7F,
                avtp_timestamp=fs.get("avtp_timestamp", 0xA55AC33C),
                stream_data_length=min(fs.get("stream_data_length", 64) & 0xFFFF, 512),
                stream_id=SID)                      # keep it OUR stream
            if not last:
                break
        self.rep.ck("storm: DUT answered every PDU", bool(last), "")
        if last:
            self.rep.eq("storm: counters never went backwards",
                        all(last[i] >= before[i] for i in
                            (C_FRAMES, C_PCMPDUS, C_SEQMM, C_UNSUPFMT, C_LOCKCNT)), True)
            self.rep.note("storm deltas: %s" % self.delta(before, last))
        # THE gate: a good PDU is still accepted and the stream is usable
        after = self.send()
        self.rep.ck("STATE STABLE: good PDU still accepted after the storm",
                    after[C_FRAMES] > (last or before)[C_FRAMES],
                    "frames_rx=%d" % after[C_FRAMES])
        self.rep.eq("STATE STABLE: stream still locked", after[C_LOCKED], 1)
        # and the stack still re-locks cleanly from scratch
        fresh = self.lock_stream()
        self.rep.eq("STATE STABLE: re-locks from reset after the storm",
                    fresh[C_LOCKED], 1)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dut", default="obj_aaf/Vaaf_cosim")
    ap.add_argument("--rounds", type=int, default=48)
    ap.add_argument("--seed", type=int, default=20260725)
    args = ap.parse_args()

    rep = cosim.Report(
        "AAF/AVTP stream field campaign (tsn-gen driven)",
        dut="avtp_stream_parser -> KL_avtp_rx_monitor -> KL_aaf_rx_depacketizer",
        rtl_files=["hdl/ieee1722/avtp/avtp_stream_parser.sv",
                   "hdl/ieee1722/avtp/KL_avtp_rx_monitor.sv",
                   "hdl/ieee1722/avtp/avtp_subtype_pkg.sv",
                   "hdl/ieee1722/aaf/KL_aaf_rx_depacketizer.sv"],
        results_dir="../../../hdl/ieee1722/avtp/doc",
        reproduce="cd tb/verilator/tsn_fuzz && make aaf")
    cosim.require_tsn_gen(rep)
    with cosim.Dut(args.dut) as dut:
        c = Campaign(dut, rep, args.seed)
        m = c.model_inventory()
        c.baseline()
        c.field_verdicts()
        c.wire_truth()
        c.foreign()
        c.accept_verdict()
        c.truncation()
        c.storm(m, args.rounds)
    return rep.done()


if __name__ == "__main__":
    sys.exit(main())
