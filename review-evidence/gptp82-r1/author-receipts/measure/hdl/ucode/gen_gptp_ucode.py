#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""gPTP µcode ROM image generator -- v8, the announce qualification and the
Pdelay_Resp_Follow_Up pairing rounds.

FPGA-gPTP #39, found while the parent integrated complete egress-stamp tags:
the Sync counter remained wider than its 16-bit wire field. At Sync 65,536,
its bit 16 occupied the claim's new messageType nibble, so the type-0 return
could not clear the type-1 claim and every later Sync cadence was suppressed.
The Sync leg now bounds the counter before it builds the frame/claim and before
write-back. A separate regression image seeds S_SSEQ at 0x10000; the existing
high-bit S_MYSEQ image remains independent so both counter paths are proved.

FPGA-gPTP #68, the step-versus-slew policy the parent's media plane relies
on (docs/INTEGRATION.md), as the owner re-decided it on 2026-09-23. A
link-up pair steps the PHC when |offset| exceeds STEP_LINKUP_NS_C (20 us);
a locked pair steps above STEP_LOCKED_NS_C (100 us); every other pair
slews. A link-up pair is the first one consumed after asCapable rises,
which every reset forces; nothing else re-arms it (the manager's ruling on
#68). Every consumed pair locks the servo (S_LOCK), and a grandmaster
identity change, a Sync receipt timeout and a return from mastership all
leave it locked. The whole written trim, proportional plus integral, is
clamped to +-RATE_PPM_C, derived exactly as the parent derives the
envelope its egress reconstruction enforces (ppm_addend), so the plane
never holds a trim its consumer refuses. Inside +-20 us the PI is the v5
loop bit for bit wherever that loop stayed inside the envelope. The v5
notes below describe the rule #68 retires.

FPGA-gPTP #7, found by the parent's field campaign: the announce handler
fed BTCA every well-formed Announce, so a better vector that 802.1AS-2011
10.3.10.2.1 (qualifyAnnounce) disqualifies still moved the grandmaster.
The three rules now run ahead of every write the handler makes:

  * (a) sourcePortIdentity.clockIdentity equal to thisClock: an Announce
    that claims to come from our own clock (our own frame reflected by a
    switch, or forged) is not qualified. IEEE 1588-2008 9.3.2.5 a) is the
    same rule.
  * (b) stepsRemoved >= 255: not qualified (9.3.2.5 d): rogue frames are
    extinguished; the mandatory backup to the path trace).
  * (c) a present path trace TLV whose pathSequence contains thisClock: the
    loop-prevention rule. The streaming parser checks every declared hop,
    including those beyond the eight retained public slots, and reports the
    result beside the true count in bank word 12. A fixed Announce without
    PathTrace reports count and loop as zero; a present TLV must have the
    announced grandmaster at its head and N == stepsRemoved+1. The µcode
    therefore consumes one coherent qualification bit rather than walking a
    truncated storage window.

(d)'s pathTrace copy for a SlavePort is moot on a single-port end station: a
slave port transmits no Announce (the ANNTX leg is gated on the master role),
so the global array has no reader here.

FPGA-gPTP #8, found by the parent's field campaign: the
Pdelay_Resp_Follow_Up handler qualified requestingPortIdentity and
nothing else, so ONE unsolicited Follow_Up carrying our identity and a
stale sequenceId computed a delay from whatever t1/t2/t4 were lying in
scratch, published 20 ms of neighborPropDelay and dropped asCapable.
802.1AS-2011 11.2.15.3 (Figure 11-8, the MDPdelayReq state machine) is
now the receive rule on both messages:

  * WAITING_FOR_PDELAY_RESP: a Pdelay_Resp is taken only when its
    sequenceId is the OUTSTANDING request's (S_MYSEQ - 1 on the wire's
    16 bits) and its requestingPortIdentity is ours. It arms the
    pairing: S_RSPSEQ holds the sequence with bit 16 set (a zero word is
    "no response"), S_RSPSRC the responder's clockIdentity.
  * WAITING_FOR_PDELAY_RESP_FOLLOW_UP: a Pdelay_Resp_Follow_Up is
    consumed only when it carries the armed sequenceId and comes from
    the armed responder (the figure's "sourcePortIdentity equal to the
    Pdelay_Resp's"); consumption clears the arm, so a duplicate pairs
    with nothing. Every other Follow_Up is ignored: neighborPropDelay,
    the ladder and asCapable do not move, nothing is counted lost.
  * Each new Pdelay_Req clears the arm: a Follow_Up for a superseded
    request cannot pair with the new request's t1.
  * A completed exchange stays completed: while S_PDGOT stands (set by
    both verdict paths, cleared by each new request) a Pdelay_Resp for
    the outstanding sequenceId does not re-arm, so a replayed or
    duplicated pair neither recomputes neighborPropDelay nor climbs the
    ladder twice in one interval (Figure 11-8 as corrected by
    Cor2-2015: after the pair, only the interval timer leaves
    WAITING_FOR_PDELAY_INTERVAL_TIMER). The identity bookkeeping of the
    cease rule still sees that response.

With more than one responder in an interval the LAST matching
Pdelay_Resp owns the stored t2/t4 and the pairing, which keeps one
exchange's timestamps from one clock; the multiple-responder policy
itself stays the Milan 4.2.6.2.5 cease rule below (the 2011 figure's
RESET on a second response is not adopted, as the v7 round decided for
same-identity duplicates). Identity scope on the Pdelay_Resp is the
WHOLE requestingPortIdentity the figure names, the clockIdentity and
the 16-bit portNumber behind it (bank words 6 and 7), so a response
addressed to another port of this clock arms nothing (FPGA-gPTP #36).
The Follow_Up's own requestingPortIdentity is not an arm of the figure
at all; the portNumber half of the engine's hardening check on it sits
in the PDPOST leg, where the ROM had room for it.

--- v7, the cease-rule round ---

The round that deliberately ends the zero-RTL era: the engine grows a
SECOND message bank (each accepted frame lands in the bank its event
names, retiring the torn-read window the v6 announce guard could only
narrow) and the scratch doubles to 64 words. On that room, the last
missing Milan v1.2 4.2.6 behavior lands:

  * The multiple-responder cease rule (4.2.6.2.5): a Pdelay_Req
    answered by responses from MORE THAN ONE clock identity, for three
    successive requests, stops Pdelay_Req transmission (the storm
    guard for daisy-chained non-AVB switches). Entering the cease
    clears asCapable and the ladder, and the pdelay COMPLETION path is
    gated too -- a forged or late exchange cannot climb the ladder
    while ceased. The resume is a CADENCE COUNTDOWN in scratch (the
    --cease-ms argument, 5 minutes by default, in 1 s cadence beats):
    scratch survives a warm reset and the engine's boot re-arms the
    cadence, so a reset during a cease still completes it -- a
    timer-armed resume would die with the reset and strand the cease
    until a bitstream reload (the review's stranded-cease finding).
    Duplicate responses from the SAME identity are not a storm.

--- v6, the full-compare round ---

v5 closed the loop; v6 completes the receive-side state machines of
802.1AS-2011 that the two-node bench let v3 defer:

  * Full BTCA (10.3.4/10.3.5): the plane keeps a BEST-VECTOR record
    {p1, cq, p2 | stepsRemoved+1, gmIdentity, sourcePortIdentity} --
    initialized to our own vector, replaced by any better announce,
    refreshed unconditionally by the CURRENT parent's announces (a
    parent update, including degradation). The compare is the spec's
    lexicographic order: priority vector, then grandmasterIdentity,
    then stepsRemoved (receiver-side +1), then sourcePortIdentity.
    After every processed announce our own vector contests the best:
    losing adopts (with the sync-ok verdict cleared ONLY on a GM
    change -- v5 cleared it on every parent refresh, a 1 Hz flicker
    this round retires), winning becomes master, and become resets
    the best record to ourselves.
  * Sync/Follow_Up pairing (11.4.4): the Follow_Up must match the
    pending Sync's sequenceId AND sourcePortIdentity, or it pairs with
    nothing. The source is held in the master-role slot 6 alias (a
    slave never runs the sync-TX builder), voided at adoption.
  * asCapable gates consumption (10.2.4.1): a fall while slave stops
    Sync/Follow_Up processing -- the servo no longer steers on a link
    whose delay verdict is dead. Pdelay keeps running; it is how the
    verdict is earned back.
  * The two-step Sync body is the ten reserved zero bytes required by
    Table 11-8. The paired Follow_Up carries the live egress timestamp
    as its preciseOriginTimestamp.

Identity scope: "sourcePortIdentity" in the pairing and the BTCA
tiebreak is the clockIdentity alone; the 16-bit portNumber (bank w3)
never joins a compare -- honest for single-port end stations, revisit
with any multi-port work.

At this v4 point still deliberately out (retired by later rounds): the
multiple-responder cease rule of Milan 4.2.6.2.5, which needs more
per-interval state than the 32-word scratch has left, and a complete
Announce epoch owner beyond the live parser bank.

--- v5, the servo round ---

v4 gave the plane its verdicts; v5 makes it act on them: the PHC servo
lands and observe-only retires. On every accepted Sync + Follow_Up as
slave, the measured offset drives the parent `timestamp_counter`'s two
knobs through the engine's PHC region:

  * |offset| > 20 us (the v5 rule on every pair, retired by #68 above):
    STEP -- one adjtime write of -offset re-bases the clock at once,
    and the addend is rewritten to the bare integrator: the rate
    estimate survives the step while the stale proportional term (moot
    after a re-base) is dropped. This is the DLL policy of the GM-loss
    design (the parent's GM_LOSS_RECOVERY.md): a prior controller slews a
    60 s cliff for 40 minutes; the fabric servo re-bases in one write.
  * otherwise: SLEW -- a PI controller in Q8.24 addend units. The loop
    gain is CLOCK-AWARE: the generator computes the ns-to-addend factor
    from --clk-hz (an addend unit is worth clk/8/2^24 ns of phase per
    125 ms sync interval), so kp = 3/4 and ki = 1/4 of the normalized
    gain hold at any clock and the closed loop is (z - 1/2)^2,
    critically damped. The integrator clamps at +-200 ppm so a
    pathological peer cannot wind it up.

The addend sign: offset is local minus master, so the correction is its
negation. A frequency-offset master converges to zero phase error (the
integrator carries the rate); the engine suite proves it closed-loop
against a +140 ppm master, deliberately above half the clamp.

--- v4, the asCapable round ---

v3 made the plane a bilateral BMCA participant and a transmitting
grandmaster; the bench interop round then listed what still separated it
from the 802.1AS state machines of record. v4 lands three of those as
ROM words on the same engine (zero RTL change):

  * The asCapable ladder (802.1AS-2011 10.2.4.1 with the Milan v1.2
    profile): asCapable rises after 2 successful Pdelay Resp + Resp_FU
    exchanges (Milan 4.2.6.2.4 bounds it in [2, 5]); it falls when the
    count of consecutive unanswered Pdelay_Reqs EXCEEDS
    allowedLostResponses = 3 (802.1AS-2011 11.2.12.4: at the fourth)
    or when the measured neighborPropDelay exceeds
    neighborPropDelayThresh = 800 ns (Milan 4.2.6.1.1, copper), with the
    Milan 4.2.6.2.7 floor: negative delays down to -80 ns do NOT clear
    it. asCapable is publish-flags bit 2, and it gates what the spec
    says it gates: Announce processing, the master TX cadences, and the
    become-master transition. Both Pdelay roles keep running regardless
    (they are how asCapable is EARNED back).
  * The receipt timeouts of Milan Table 4.2 beyond announce (v3):
    syncReceiptTimeout 375 ms (timer slot 4) clears the sync-ok verdict
    (flags bit 3, set on each completed Sync+Follow_Up as slave);
    followUpReceiptTimeout 125 ms (timer slot 5) invalidates a Sync
    whose Follow_Up never came, so a late Follow_Up is discarded
    instead of pairing with a stale ingress timestamp.
  * neighborRateRatio (802.1AS-2011 11.2.15.3, successive-response
    form): nrr = (t3_n - t3_prev) / (t4_n - t4_prev) as a Q2.30
    fixed-point ratio (OP_MULDIV earns its LUTs here), and the link
    delay becomes D = (nrr*(t4-t1) - (t3-t2)) / 2. Windows wider than
    2^32 ns (a silent peer) skip the update rather than divide stale.

Publish flags: bit0 gm_present, bit1 am_gm, bit2 asCapable, bit3
sync_ok. Every writer read-modify-writes so the verdicts compose.

Fixed entry table (mirrored by KL_gptp_engine): 16 SYNC · 64 FOLLOWUP ·
128 ANNOUNCE · 192 PDELAY_REQ · 256 PDELAY_RESP · 320 PDELAY_RESP_FU ·
384 SIGNALING · 448 TX_TS · 512 TIMER (slot 0 init+pdelay, 1 sync TX,
2 announce receipt, 3 announce TX, 4 sync receipt, 5 FU receipt) ·
704 TB battery. Shared legs are auto-packed into the free gaps by a
two-pass assembler (sizes first, then bases), so a leg outgrowing the
768.. tail is a solved problem instead of a manual repack.

Still deliberately out (each a later round): stepsRemoved tie-breaks
(two-node link), the multiple-responder cease rule of Milan 4.2.6.2.5,
and sourcePortIdentity matching on Sync.
"""

import argparse
from dataclasses import dataclass

DEPTH = 1024
WMASK = (1 << 48) - 1

# ---- encoding (gptp_ucpu_pkg.sv) -------------------------------------------
OPS = {
    "NOP": 0, "BR": 1, "BRS": 2, "END": 3, "MOVE": 4, "CMP": 5, "MASK": 6,
    "DADDR": 7, "RDST": 8, "WRST": 9, "NRD": 10, "NWR": 11, "CPBUF": 12,
    "CHKL": 13, "CHKA": 14, "MAPV": 15, "GATH": 16, "RCTR": 17,
    "IOPEN": 18, "INEXT": 19, "APP": 20, "COMMIT": 21, "NVM": 22,
    "NTFY": 23, "SETS": 24, "SETL": 25, "BHDR": 26, "BFLD": 27,
    "SEND": 28, "ALU": 29, "MD": 30,
}
FMT_B, FMT_W, FMT_D, FMT_Q = 0, 1, 2, 3
ALU_ADD, ALU_SUB, ALU_AND, ALU_OR, ALU_XOR, ALU_SHL, ALU_SHR, ALU_SAR = \
    range(8)
MD_MULS, MD_DIVU = 0, 1
BRS_NZOK, BRS_ITER, BRS_Z, BRS_LT, BRS_OVF = range(5)

RG_BANK, RG_TS, RG_SCR, RG_PUB, RG_PHC, RG_TMR = (
    0x00000, 0x10000, 0x20000, 0x30000, 0x40000, 0x50000)

# ---- scratch map -----------------------------------------------------------
# v6 reclaimed three write-only slots (the old S_OFFSET/S_AMGM/S_TICK:
# pub word 4 is the offset record, flags bit 1 is the role, the tick
# counter had no reader) for the BTCA best-vector record, and slot 6 is
# role-exclusive: sync-seq-in-flight while master, the pending Sync's
# sourcePortIdentity while slave (adopt clears it at the role change).
S_SYNCTS, S_HDR, S_BESTPV, S_BESTID = 0, 1, 2, 3
S_PDELAY, S_T2, S_SSEQFLY = 4, 5, 6
S_SYNCSRC = S_SSEQFLY                    # the slave-role alias
S_PDOK, S_PDLOST = 7, 8                  # asCapable ladder counters
S_FUORG = 9                              # 0xC2000001 (info-TLV org tail)
S_MYPV = 10                              # our {p1, cq, p2, 16'0} vector
S_PDGOT = 11                             # exchange seen since last req
S_NR3, S_NR4, S_NRR = 12, 13, 14         # nrr window + Q2.30 ratio
# S_NR4 is read only behind nonzero S_NR3. The rate-window save writes
# both together, and a step clears S_NR3. No independent init is needed.
S_INTG = 15                              # servo integrator, addend units
S_T1, S_T4, S_TXQ_TMR = 16, 17, 18       # S_TXQ_TMR took the cell the one
                                         # shared pending kind used before
                                         # the claims were split per frame
S_RQCID, S_BESTSRC, S_RQSEQ, S_RQPN, S_INIT, S_MYSEQ = 19, 20, 21, 22, 23, 24
S_CID, S_1E9, S_HDR8, S_SALO = 25, 26, 27, 28
S_SSEQ, S_ASEQ, S_ANNBODY = 29, 30, 31
# the widened half (the engine's 64-word scratch, v7)
S_RSP1, S_IVMULTI, S_MULTI, S_CEASE = 32, 33, 34, 35
S_CEASECNT = 36                          # cadence beats to resume
# INVARIANT for S_CEASECNT and S_MULTI, which the init leg deliberately
# does NOT zero. Each is read only behind a gate, S_CEASE and S_IVMULTI
# respectively, and each gate has exactly ONE writer that can set it
# nonzero, which writes the guarded cell in the same straight-line block:
# the cease arm sets S_CEASE then S_CEASECNT two instructions later, and
# the storm arm sets S_IVMULTI in prog_rx_pdresp while the cadence beat's
# other branch writes S_MULTI before S_IVMULTI can ever be 1. That is
# what the safety rests on, NOT on the init list: scratch is LUTRAM with
# no reset (KL_gptp_engine.sv:143-149), so a warm reset does not run the
# init leg at all, and gate and guarded cell simply carry over TOGETHER
# and stay mutually consistent. There is no partial-reset path that could
# clear one and not the other. ADDING A SECOND WRITER to either gate
# breaks this: give the guarded cell an init write again, or write it in
# the new writer's own block.
S_TXQ_RESP = 41                          # the second egress-timestamp
                                         # claim. Each claim holds the
                                         # {messageType, sequenceId} its
                                         # frame went out with, or'd with
                                         # TXP_PEND_C while that frame's
                                         # stamp is owed and
                                         # with TXP_SYNC_C when the frame
                                         # is a Sync, and zero once the
                                         # stamp has been taken. Two cells
                                         # are enough: the two timer-driven
                                         # transmitters already exclude
                                         # each other (each skips its beat
                                         # while a timer-driven stamp is
                                         # owed), so no second timer-driven
                                         # frame joins them, and each
                                         # stamp goes to the frame whose
                                         # sequenceId it names (FPGA-gPTP
                                         # #28)
S_RSPSEQ, S_RSPSRC = 39, 40              # the armed Pdelay_Resp: its
                                         # sequenceId | RSP_ARMED_C, and
                                         # its sourcePortIdentity (written
                                         # before it is ever read: no init)
# ---- the requester's own pairing state (FPGA-gPTP #31) ---------------------
S_T1V = 37       # "S_T1 holds this request's own t1". A measured t1 may be
                 # numeric zero, so the value cannot carry its own validity.
S_PDWAIT = 38    # "a complete Pdelay pair is waiting for that t1"
S_T3 = 42        # the waiting pair's t3, guarded by S_PDWAIT
# S_T1V and S_PDWAIT get RESET-BACKED validity in the engine
# (KL_gptp_engine.sv region 2, the idiom S_TXQ_TMR and S_TXQ_RESP already
# run): scratch is LUTRAM with no reset and a warm reset does not run the
# init leg at all, so without it a retained cell would present a pre-reset
# t1, or a pre-reset deferred pair, as live. S_T1V is in the init clear
# list below for the cold path as well.
#
# INVARIANT for S_T3, the same one S_CEASE/S_CEASECNT and S_IVMULTI/S_MULTI
# carry: it is read only behind the S_PDWAIT gate, and the ONE writer that
# can set that gate writes S_T3 in the same straight-line block (the PDPOST
# deferral arm). Gate and guarded cell therefore carry over a warm reset
# together, and S_PDWAIT's reset-backed validity closes the cell for the
# reset case. ADDING A SECOND WRITER to either breaks this.
# ---- the servo's lock state (FPGA-gPTP #68) ---------------------------------
S_LOCK = 43      # 0 when the next pair is a link-up, else what a locked
                 # servo adds to the link-up step threshold
S_PDSTEP = 44    # current request overlaps our own PHC step
# Every request clears this before any matching response can complete.
# A step sets it without changing response-loss or multiple-peer accounting.
# Warm reset invalidates pairing; its next request establishes a fresh flag.
# INVARIANT for S_LOCK: WRITTEN BEFORE IT IS READ after every reset, cold or
# warm, with no init write and no reset-backed validity. Its only reader is
# the SERVO leg, which runs only while asCapable stands. Reset clears the
# publish flags, and asCapable has ONE setter, the verdict in PDPAIR, which
# writes S_LOCK in the same block whenever it finds the flag clear. So a
# pre-reset lock can never reach the first pair after a reset. ADDING A
# SECOND asCapable SETTER breaks this: it must write S_LOCK as well. That
# rise is also the ONLY unlock (#68 ruling): a receipt timeout, a
# grandmaster change and becoming grandmaster leave S_LOCK alone.
# S_BESTPV holds {p1, cq, p2} in [63:16] and stepsRemoved+1 in [15:0]
# (steps ranks BELOW the identity in 10.3.5, so it never joins the
# packed compare -- the pv compare masks the low 16 first)

# ---- 802.1AS-2011 10.3.10.2.1 qualifyAnnounce -----------------------------
STEPS_MAX_C = 255               # stepsRemoved >= this: not qualified (b)

# ---- 802.1AS-2011 11.2.15.3 Pdelay_Resp / Resp_Follow_Up pairing ------------
TXT_TYPE_SHIFT_C = 16           # claim bits [19:16] carry messageType
TXT_TYPE_MASK_C = 0xF << TXT_TYPE_SHIFT_C
TXT_PDREQ_C = 0x2 << TXT_TYPE_SHIFT_C
TXT_PDRESP_C = 0x3 << TXT_TYPE_SHIFT_C
TXP_PEND_C = 0x100000           # "a stamp is owed for this frame" and,
TXP_SYNC_C = 0x200000           # for the timer-driven claim, "the frame
                                # is a Sync, so its stamp builds the
                                # Follow_Up". Both sit above the 16-bit
                                # sequenceId in the claim cell, ABOVE the
                                # messageType nibble a bank-word-0 read
                                # leaves at bits [19:16], which is why
                                # they start at bit 20 and why every claim
                                # is masked to TXQ_MASK_C before it is
                                # compared: the sequenceId is 16 bits on
                                # the wire, the counters behind it are not
TXQ_MASK_C = 0xFFFF | TXT_TYPE_MASK_C | TXP_PEND_C | TXP_SYNC_C
TXT_OK_C = 0x800000             # the dispatched result's outcome bit. It
                                # and the producer's generation at bits
                                # 27:24 sit ABOVE TXQ_MASK_C, so neither
                                # disturbs a masked claim compare. ok low
                                # is an explicit LOST result: it retires
                                # its own claim, writes no time and builds
                                # no companion
RSP_ARMED_C = 0x10000           # set above the 16-bit sequenceId in
                                # S_RSPSEQ: a zero word is "no response"
OUR_PORTNUM_C = 1               # thisPort. ONE definition, read by both
                                # sides: e_hdr writes it into every
                                # sourcePortIdentity we transmit, and the
                                # Pdelay receive guards qualify a received
                                # requestingPortIdentity.portNumber
                                # against it. A second copy would let the
                                # transmit and receive halves drift apart
                                # in silence

# ---- our clock vector (Milan defaults) -------------------------------------
P1_C, P2_C = 248, 248
CQ_C = 0xF8FE436A               # class 248, accuracy 0xFE, variance 0x436A
UTC_OFF_C = 37

# ---- Milan v1.2 profile numbers --------------------------------------------
NPD_HI_C = 800                  # neighborPropDelayThresh ns, 4.2.6.1.1
NPD_LO_C = 80                   # negative-delay floor ns, 4.2.6.2.7
ASCAP_UP_C = 2                  # exchanges to asCapable, 4.2.6.2.4 in [2,5]
LOST_N_C = 3                    # allowedLostResponses, 802.1AS-2011 10.2.4.1
SYNC_RTO_MS_C = 375             # syncReceiptTimeout, Table 4.2
FU_RTO_MS_C = 125               # followUpReceiptTimeout, Table 4.2
CEASE_N_C = 3                   # successive multi-answered reqs, 4.2.6.2.5
CEASE_MS_C = 300_000            # resume after 5 min (--cease-ms overrides)
                                # counted down in 1 s cadence beats

# ---- servo constants (clock-aware, set by set_servo_gains) -----------------
STEP_LINKUP_NS_C = 20000        # a link-up pair steps above this, ns (#68)
STEP_LOCKED_NS_C = 100000       # a locked pair steps above this, ns (#68)
# #75: distinguish transient phase correction from ordinary PI tracking.
# Two consecutive consumed pairs inside this inclusive band complete a slew.
# This is a completion tolerance, not another step threshold or a rate bound.
SLEW_SETTLED_NS_C = 100
RATE_PPM_C = 200                # the rate envelope, ppm: the integrator clamp
                                # and, since #68, the whole written trim
GAIN_S_C = 6                    # ns -> addend units: (off * GAIN_M) >> 6
GAIN_M_C = 86                   # for the 100 MHz default; see set_servo_gains
ILIM_C = 33554                  # RATE_PPM_C in addend units at that clock

# ---- what this run actually uses -------------------------------------------
# Seeded from the constants above and MUTATED IN PLACE by the CLI and by
# set_servo_gains. The constants stay the literal, one-per-file declarations
# sw/builder/endstation_builder.py and sw/builder/test_builder.py parse as the
# engine's authority, so an override must not rebind them: it moves the value
# here, where every reader looks.
RUNTIME = {
    "p1": P1_C,                 # --p1
    "cease_ms": CEASE_MS_C,     # --cease-ms
    "gain_m": GAIN_M_C,         # --clk-hz, through set_servo_gains
    "ilim": ILIM_C,             # --clk-hz, through set_servo_gains: the
                                # +-RATE_PPM_C envelope in addend units
}


def ppm_addend(ppm: int, clk_hz: int) -> int:
    """`ppm` of relative frequency in Q8.24 addend units at `clk_hz`. A unit
    adds 2^-24 ns per tick, so this is ppm * 2^24 * 1000 / clk_hz, rounded
    half up in exact integers. The parent's KL_gptp_txret.sv derives
    PHC_ADJ_MAX_C, the addend envelope outside which it refuses every
    egress timestamp, with this expression: RECON_REL_PPM_P = 200 and
    PHC_CLK_HZ_P = the clock given here. So the two agree to the unit at
    every clock, ties included."""
    return (ppm * (1 << 24) * 1000 + clk_hz // 2) // clk_hz


def set_servo_gains(clk_hz: int) -> None:
    """An addend unit adds 2^-24 ns per tick; one 125 ms sync interval is
    clk/8 ticks, so one unit is clk/8/2^24 ns of phase per interval. The
    PI shifts assume normalized gain, hence M/2^6 = 2^24/(clk/8). The rate
    envelope clamps the integrator and, since #68, the whole written
    trim."""
    RUNTIME["gain_m"] = round((1 << 24) * 64 * 8 / clk_hz)
    RUNTIME["ilim"] = ppm_addend(RATE_PPM_C, clk_hz)
    assert 0 < RUNTIME["gain_m"] < (1 << 24), RUNTIME["gain_m"]
    assert 2 * RUNTIME["ilim"] + 1 < (1 << 24), RUNTIME["ilim"]

# publish flags bits
FL_PRESENT_C, FL_AMGM_C, FL_ASCAP_C, FL_SYNCOK_C = 1, 2, 4, 8

# 802.1AS-2011 Table 11-7 controlField values for every message this plane
# transmits. Keep the map exhaustive so adding a TX message cannot silently
# inherit the old shared delay-management value.
TX_CONTROL_BY_TYPE_C = {
    0x0: 0x0,  # Sync
    0x2: 0x5,  # Pdelay_Req
    0x3: 0x5,  # Pdelay_Resp
    0x8: 0x2,  # Follow_Up
    0xA: 0x5,  # Pdelay_Resp_Follow_Up
    0xB: 0x5,  # Announce
}

# The 802.1AS-2011 flags word every message this plane transmits carries, in
# wire order: flagField octet 0 in bits 15:8, octet 1 in bits 7:0.
#
# 11.4.2 takes the common header of 10.5.2 for Sync, Follow_Up, Pdelay_Req,
# Pdelay_Resp and Pdelay_Resp_Follow_Up "except as noted in the following
# subclauses", and 11.4.2.3 is such a note for the whole flags field:
# Table 11-4 defines twoStepFlag for Sync and Pdelay_Resp alone, and "for
# message types where the bit is not defined in Table 11-4, the value of the
# bit is set to FALSE". So the media-dependent table REPLACES Table 10-6 for
# those five, including its all-message ptpTimescale entry, and each of them
# transmits 0x0200 or 0x0000 and nothing else. Announce is not in 11.4.1's
# list and keeps the common 10.5.2.2.6 value.
#
# Cor1-2013 renumbers twoStepFlag to octet 0 bit 2 and ptpTimescale to octet 1
# bit 4. Under the 6.3.4.2 numbering, where bit 1 is the least significant of
# an octet, both wire masks are the ones below (FPGA-gPTP #64).
#
# One entry per type, like the control map above, so the wire value is stated
# once: this defect was two header call sites restating the rule and getting
# it wrong. 11.4.1 also requires reserved fields transmitted zero and IGNORED
# on reception, so nothing here is a receive predicate.
TX_FLAGS_BY_TYPE_C = {
    0x0: 0x0200,  # Sync: twoStepFlag
    0x2: 0x0000,  # Pdelay_Req
    0x3: 0x0200,  # Pdelay_Resp: twoStepFlag
    0x8: 0x0000,  # Follow_Up
    0xA: 0x0000,  # Pdelay_Resp_Follow_Up
    0xB: 0x0008,  # Announce: ptpTimescale, the common Table 10-6 entry
}

# ---- register conventions --------------------------------------------------
R0, RA, RB, RC, RD_, RT, RU, RSEC, RNS, RP = 0, 1, 2, 3, 4, 5, 6, 7, 8, 9
RV, RW = 10, 11
REV, RTS0 = 15, 14

# shared-leg bases: filled by the packing pass, referenced through LB[]
LB = {}


@dataclass(frozen=True)
class Insn:
    """One instruction's fields, named as gptp_ucpu_pkg.sv names them and in
    the order it packs them into the 48-bit ROM word. Frozen: an emitted
    instruction is a record, not a builder."""
    op: str
    rd: int = 0
    ra: int = 0
    rb: int = 0
    fmt: int = 0
    cnd: int = 0
    imm: int = 0

    def word(self) -> int:
        """The packed 48-bit ROM word."""
        assert 0 <= self.imm < (1 << 24), hex(self.imm)
        return ((OPS[self.op] << 43) | (self.rd << 39) | (self.ra << 35) |
                (self.rb << 31) | (self.fmt << 28) | (self.cnd << 24) |
                self.imm)


def splitmix48(i: int) -> int:
    """Filler for a ROM address no program claims.

    SplitMix64 of the address itself, truncated to the ROM word: unowned
    space is neither zero nor a repeat, and two builds of one image are
    still byte-identical."""
    z = (i + 0x9E3779B97F4A7C15) & ((1 << 64) - 1)
    z = ((z ^ (z >> 30)) * 0xBF58476D1CE4E5B9) & ((1 << 64) - 1)
    z = ((z ^ (z >> 27)) * 0x94D049BB133111EB) & ((1 << 64) - 1)
    return (z ^ (z >> 31)) & WMASK


class Prog:
    """Tiny two-pass assembler; local labels plus absolute targets."""

    def __init__(self, base):
        self.base = base
        self.items = []

    def emit(self, op: str, label: str | int | None = None,
             **kw: int) -> None:
        """Queue one instruction; `label` is a local name or an absolute
        µPC, resolved into `imm` by the second pass."""
        self.items.append((op, kw, label))

    def label(self, name: str) -> None:
        """Name the address the next emitted instruction will occupy."""
        self.items.append(("label", name))

    def words(self) -> list[int]:
        """Resolve every label against this program's real base and pack
        the result into ROM words."""
        addr, labels = self.base, {}
        for it in self.items:
            if it[0] == "label":
                labels[it[1]] = addr
            else:
                addr += 1
        out = []
        for it in self.items:
            if it[0] == "label":
                continue
            op, kw, label = it
            if label is not None:
                kw = dict(kw, imm=labels[label] if isinstance(label, str)
                          else label)
            out.append(Insn(op, **kw).word())
        return out


# ---- emit helpers ----------------------------------------------------------

def e_const(p: Prog, rd: int, value: int) -> None:
    """Load a constant of any width into rd, 24 bits at a time: MOVE's
    immediate is one chunk wide, so anything larger is shifted in."""
    chunks = []
    v = value
    while True:
        chunks.append(v & 0xFFFFFF)
        v >>= 24
        if v == 0:
            break
    chunks.reverse()
    p.emit("MOVE", rd=rd, ra=0, imm=chunks[0])
    for c in chunks[1:]:
        p.emit("ALU", rd=rd, ra=rd, rb=0, cnd=ALU_SHL, imm=24)
        if c:
            p.emit("MOVE", rd=RT, ra=0, imm=c)
            p.emit("ALU", rd=rd, ra=rd, rb=RT, cnd=ALU_OR)


def e_guard_init(p: Prog, end_label: str) -> None:
    """Fall through only once S_INIT stands: a handler that ran before the
    timer's init leg seeded scratch would decide on uninitialised cells."""
    p.emit("RDST", rd=RA, imm=RG_SCR | S_INIT, fmt=FMT_Q)
    p.emit("CMP", ra=RA, rb=0, fmt=FMT_D, imm=1)
    p.emit("BRS", cnd=BRS_Z, label="run")
    p.emit("BR", label=end_label)
    p.label("run")


def e_flags(p: Prog, andm: int | None = None, orm: int | None = None) -> None:
    """Read-modify-write the publish flags word (clobbers RT)."""
    p.emit("RDST", rd=RT, imm=RG_PUB | 2, fmt=FMT_Q)
    if andm is not None:
        p.emit("ALU", rd=RT, ra=RT, rb=0, cnd=ALU_AND, imm=andm)
    if orm:
        p.emit("ALU", rd=RT, ra=RT, rb=0, cnd=ALU_OR, imm=orm)
    p.emit("WRST", ra=RT, imm=RG_PUB | 2, fmt=FMT_Q)


def e_flag_gate(p: Prog, mask: int, want: int, tag: str,
                out_label: str) -> None:
    """Fall through when (flags & mask) == want, else branch out."""
    p.emit("RDST", rd=RT, imm=RG_PUB | 2, fmt=FMT_Q)
    p.emit("ALU", rd=RT, ra=RT, rb=0, cnd=ALU_AND, imm=mask)
    p.emit("CMP", ra=RT, rb=0, fmt=FMT_D, imm=want)
    p.emit("BRS", cnd=BRS_Z, label=f"fg_{tag}")
    p.emit("BR", label=out_label)
    p.label(f"fg_{tag}")


def e_hdr(p: Prog, mtype: int, seq_reg: int, logint: int,
          msglen: int) -> None:
    """Bytes 0..47: eth + 802.1AS common header.

    controlField and the flags word are both properties of the message type,
    so both are read from their maps rather than passed: a call site cannot
    hand this builder a flags word the standard does not allow for the type
    it is building."""
    control = TX_CONTROL_BY_TYPE_C[mtype]
    flags = TX_FLAGS_BY_TYPE_C[mtype]
    p.emit("RDST", rd=RC, imm=RG_SCR | S_HDR8, fmt=FMT_Q)
    p.emit("BFLD", ra=RC, fmt=FMT_Q)
    p.emit("RDST", rd=RC, imm=RG_SCR | S_SALO, fmt=FMT_Q)
    p.emit("BFLD", ra=RC, fmt=FMT_D)
    p.emit("MOVE", rd=RT, ra=0, imm=0x88F7)
    p.emit("BFLD", ra=RT, fmt=FMT_W)
    p.emit("MOVE", rd=RT, ra=0, imm=0x10 | mtype)
    p.emit("BFLD", ra=RT, fmt=FMT_B)
    p.emit("MOVE", rd=RT, ra=0, imm=0x02)
    p.emit("BFLD", ra=RT, fmt=FMT_B)
    p.emit("MOVE", rd=RT, ra=0, imm=msglen)
    p.emit("BFLD", ra=RT, fmt=FMT_W)
    p.emit("BFLD", ra=0, fmt=FMT_B)
    p.emit("BFLD", ra=0, fmt=FMT_B)
    if flags:
        p.emit("MOVE", rd=RT, ra=0, imm=flags)
        p.emit("BFLD", ra=RT, fmt=FMT_W)
    else:
        p.emit("BFLD", ra=0, fmt=FMT_W)
    p.emit("BFLD", ra=0, fmt=FMT_Q)
    p.emit("BFLD", ra=0, fmt=FMT_D)
    p.emit("RDST", rd=RC, imm=RG_SCR | S_CID, fmt=FMT_Q)
    p.emit("BFLD", ra=RC, fmt=FMT_Q)
    p.emit("MOVE", rd=RT, ra=0, imm=OUR_PORTNUM_C)
    p.emit("BFLD", ra=RT, fmt=FMT_W)
    p.emit("BFLD", ra=seq_reg, fmt=FMT_W)
    p.emit("MOVE", rd=RT, ra=0, imm=control)
    p.emit("BFLD", ra=RT, fmt=FMT_B)
    p.emit("MOVE", rd=RT, ra=0, imm=logint)
    p.emit("BFLD", ra=RT, fmt=FMT_B)


def e_ts_fields(p: Prog, ns_reg: int) -> None:
    """Append the 10-byte PTP Timestamp (48-bit seconds, 32-bit
    nanoseconds) for the nanosecond count in ns_reg."""
    p.emit("RDST", rd=RP, imm=RG_SCR | S_1E9, fmt=FMT_Q)
    p.emit("MD", rd=RSEC, ra=ns_reg, rb=RP, cnd=MD_DIVU)
    p.emit("MD", rd=RT, ra=RSEC, rb=RP, cnd=MD_MULS)
    p.emit("ALU", rd=RNS, ra=ns_reg, rb=RT, cnd=ALU_SUB)
    p.emit("ALU", rd=RU, ra=RSEC, rb=0, cnd=ALU_SHR, imm=32)
    p.emit("BFLD", ra=RU, fmt=FMT_W)
    p.emit("BFLD", ra=RSEC, fmt=FMT_D)
    p.emit("BFLD", ra=RNS, fmt=FMT_D)


def e_full_ts(p: Prog, rd: int) -> None:
    """Fold the received frame's seconds and nanoseconds (bank words 4 and
    5) into one 64-bit nanosecond value in rd."""
    p.emit("RDST", rd=RSEC, imm=RG_BANK | 4, fmt=FMT_Q)
    p.emit("RDST", rd=RP, imm=RG_SCR | S_1E9, fmt=FMT_Q)
    p.emit("MD", rd=rd, ra=RSEC, rb=RP, cnd=MD_MULS)
    p.emit("RDST", rd=RNS, imm=RG_BANK | 5, fmt=FMT_Q)
    p.emit("ALU", rd=rd, ra=rd, rb=RNS, cnd=ALU_ADD)


def e_ult64(p: Prog, ra: int, rb: int, less_label: str, geq_label: str,
            tag: str) -> None:
    """Branch to less_label when u64 rf[ra] < rf[rb]; geq on >; falls
    through on equal."""
    p.emit("ALU", rd=RT, ra=ra, rb=0, cnd=ALU_SHR, imm=32)
    p.emit("ALU", rd=RU, ra=rb, rb=0, cnd=ALU_SHR, imm=32)
    p.emit("CMP", ra=RT, rb=RU, fmt=FMT_D)
    p.emit("BRS", cnd=BRS_LT, label=less_label)
    p.emit("BRS", cnd=BRS_Z, label=f"lo_{tag}")
    p.emit("BR", label=geq_label)
    p.label(f"lo_{tag}")
    p.emit("CMP", ra=ra, rb=rb, fmt=FMT_D)
    p.emit("BRS", cnd=BRS_LT, label=less_label)
    p.emit("BRS", cnd=BRS_Z, label=f"eq_{tag}")
    p.emit("BR", label=geq_label)
    p.label(f"eq_{tag}")


def e_sat(p: Prog, reg: int, lim: int, tag: str) -> None:
    """Saturate the signed rf[reg] to [-lim, +lim] in place (clobbers RU and
    RW). In range exactly when (reg + lim) u<= 2 lim, i.e. when that sum
    divided by 2 lim + 1 is zero; out of range, the sum's sign picks the
    bound: s = sum >>a 63 is 0 or -1, and (lim ^ s) - s is +lim or -lim.
    Exact for every reg up to 2^63 - 1 - lim; above that the sum wraps
    negative and the result is -lim. Every caller stays far inside: the
    integrator input is the clamped integrator plus one PI term, and the
    whole trim is either the PI output for an offset of at most
    STEP_LOCKED_NS_C (a slew) or the clamped integrator alone (a step)."""
    assert 0 < 2 * lim + 1 < (1 << 24), lim
    p.emit("ALU", rd=RW, ra=reg, rb=0, cnd=ALU_ADD, imm=lim)
    p.emit("MD", rd=RU, ra=RW, rb=0, cnd=MD_DIVU, imm=2 * lim + 1)
    p.emit("CMP", ra=RU, rb=0, fmt=FMT_Q, imm=0)
    p.emit("BRS", cnd=BRS_Z, label=f"{tag}_ok")
    p.emit("ALU", rd=RU, ra=RW, rb=0, cnd=ALU_SAR, imm=63)
    p.emit("MOVE", rd=reg, ra=0, imm=lim)
    p.emit("ALU", rd=reg, ra=reg, rb=RU, cnd=ALU_XOR)
    p.emit("ALU", rd=reg, ra=reg, rb=RU, cnd=ALU_SUB)
    p.label(f"{tag}_ok")


# ---- RX handlers -----------------------------------------------------------

def prog_rx_sync(base: int) -> Prog:
    """Sync receipt (entry 16): park the receipt stamp, the header and the
    sourcePortIdentity, then arm the Follow_Up watch. Heard while master it
    writes nothing: slot 6 then holds our own in-flight Sync sequence.
    """
    p = Prog(base)
    # gate FIRST: a rogue Sync heard while master must not touch the
    # slot-6 alias (it holds OUR in-flight FU sequence in that role)
    e_flag_gate(p, FL_PRESENT_C | FL_AMGM_C | FL_ASCAP_C,
                FL_PRESENT_C | FL_ASCAP_C, "sl", "out")
    p.emit("WRST", ra=RTS0, imm=RG_SCR | S_SYNCTS, fmt=FMT_Q)
    p.emit("RDST", rd=RA, imm=RG_BANK | 0, fmt=FMT_Q)
    p.emit("WRST", ra=RA, imm=RG_SCR | S_HDR, fmt=FMT_Q)
    p.emit("RDST", rd=RA, imm=RG_BANK | 2, fmt=FMT_Q)
    p.emit("WRST", ra=RA, imm=RG_SCR | S_SYNCSRC, fmt=FMT_Q)
    p.emit("MOVE", rd=RT, ra=0, imm=FU_RTO_MS_C)
    p.emit("WRST", ra=RT, imm=RG_TMR | 5, fmt=FMT_Q)
    p.label("out")
    p.emit("END")
    return p


def prog_rx_followup(base: int) -> Prog:
    """Follow_Up receipt (entry 64): pair it with the pending Sync on
    sequenceId and sourcePortIdentity, publish the offset (local minus
    master, less correctionField and the link delay), then run SERVO."""
    p = Prog(base)
    e_guard_init(p, "out")
    # an asCapable fall stops consumption: the servo must not steer on
    # a link whose delay verdict is dead (802.1AS-2011 10.2.4.1)
    e_flag_gate(p, FL_PRESENT_C | FL_AMGM_C | FL_ASCAP_C,
                FL_PRESENT_C | FL_ASCAP_C, "sl", "out")
    # a Sync must be pending and valid: the FU-receipt timeout zeroes it,
    # so a Follow_Up later than 125 ms pairs with nothing and is dropped
    p.emit("RDST", rd=RD_, imm=RG_SCR | S_SYNCTS, fmt=FMT_Q)
    p.emit("CMP", ra=RD_, rb=0, fmt=FMT_Q, imm=0)
    p.emit("BRS", cnd=BRS_Z, label="out")
    # 11.4.4 pairing: the FU must match the pending Sync's sequenceId
    # and sourcePortIdentity, or it pairs with nothing
    p.emit("RDST", rd=RT, imm=RG_SCR | S_HDR, fmt=FMT_Q)
    p.emit("ALU", rd=RT, ra=RT, rb=0, cnd=ALU_SHR, imm=32)
    p.emit("RDST", rd=RU, imm=RG_BANK | 0, fmt=FMT_Q)
    p.emit("ALU", rd=RU, ra=RU, rb=0, cnd=ALU_SHR, imm=32)
    p.emit("ALU", rd=RU, ra=RU, rb=0, cnd=ALU_AND, imm=0xFFFF)
    p.emit("CMP", ra=RT, rb=RU, fmt=FMT_W)
    p.emit("BRS", cnd=BRS_Z, label="srcck")
    p.emit("BR", label="out")
    p.label("srcck")
    p.emit("RDST", rd=RT, imm=RG_SCR | S_SYNCSRC, fmt=FMT_Q)
    p.emit("RDST", rd=RU, imm=RG_BANK | 2, fmt=FMT_Q)
    p.emit("CMP", ra=RT, rb=RU, fmt=FMT_Q)
    p.emit("BRS", cnd=BRS_Z, label="paired")
    p.emit("BR", label="out")
    p.label("paired")
    e_full_ts(p, RA)
    p.emit("RDST", rd=RB, imm=RG_BANK | 1, fmt=FMT_Q)
    p.emit("ALU", rd=RB, ra=RB, rb=0, cnd=ALU_SAR, imm=16)
    p.emit("ALU", rd=RA, ra=RA, rb=RB, cnd=ALU_ADD)
    p.emit("RDST", rd=RB, imm=RG_SCR | S_PDELAY, fmt=FMT_Q)
    p.emit("ALU", rd=RA, ra=RA, rb=RB, cnd=ALU_ADD)
    p.emit("ALU", rd=RA, ra=RD_, rb=RA, cnd=ALU_SUB)
    p.emit("WRST", ra=RA, imm=RG_PUB | 4, fmt=FMT_Q)
    p.emit("BR", label=LB["SERVO"])
    p.label("out")
    p.emit("END")
    return p


def prog_leg_servo(base: int) -> Prog:
    """Accepted Sync+FU as slave; RA = offset (local minus master).
    The #68 step-vs-slew policy into the PHC region, then the
    receipt-timeout tail."""
    p = Prog(base)
    # ---- the servo: offset is local minus master, correction negates --
    # FPGA-gPTP #68: the step threshold T is STEP_LINKUP_NS_C plus S_LOCK,
    # so 20 us at link-up and 100 us once locked. Step when |offset| > T,
    # i.e. (offset + T) u> 2T: exactly when that sum divided by 2T + 1 is
    # nonzero. A slewed offset is therefore never over 100 us, which keeps
    # the MULS operand (32 x 32) exact without saturating it
    assert STEP_LINKUP_NS_C < STEP_LOCKED_NS_C < (1 << 23)
    p.emit("RDST", rd=RB, imm=RG_SCR | S_LOCK, fmt=FMT_Q)
    p.emit("ALU", rd=RB, ra=RB, rb=0, cnd=ALU_ADD, imm=STEP_LINKUP_NS_C)
    p.emit("ALU", rd=RW, ra=RA, rb=RB, cnd=ALU_ADD)
    p.emit("ALU", rd=RB, ra=RB, rb=RB, cnd=ALU_ADD)
    p.emit("ALU", rd=RB, ra=RB, rb=0, cnd=ALU_ADD, imm=1)
    p.emit("MD", rd=RU, ra=RW, rb=RB, cnd=MD_DIVU)
    p.emit("CMP", ra=RU, rb=0, fmt=FMT_Q, imm=0)
    p.emit("BRS", cnd=BRS_Z, label="sv_slew")
    p.emit("ALU", rd=RB, ra=R0, rb=RA, cnd=ALU_SUB)          # -offset
    p.emit("WRST", ra=RB, imm=RG_PHC | 1, fmt=FMT_Q)         # adjtime
    # A phase change is not oscillator drift (802.1AS-2020 11.2.19.3.3).
    # Re-seed the next rate window, retaining the last measured ratio.
    p.emit("WRST", ra=0, imm=RG_SCR | S_NR3, fmt=FMT_Q)
    p.emit("MOVE", rd=RT, ra=0, imm=1)
    p.emit("WRST", ra=RT, imm=RG_SCR | S_PDSTEP, fmt=FMT_Q)
    # the rate estimate survives the step AND becomes the whole addend:
    # the re-base just made the stale proportional term moot
    p.emit("RDST", rd=RT, imm=RG_SCR | S_INTG, fmt=FMT_Q)
    p.emit("BR", label=LB["SVRATE"])
    p.label("sv_slew")
    p.emit("BR", label=LB["SLEW"])
    return p


def prog_leg_slew(base: int) -> Prog:
    """Publish transient-versus-tracking policy, then compute the PI trim."""
    p = Prog(base)
    # Publish the policy verdict before the affected rate write. PHC word 2
    # holds the remaining in-band pairs (0..2), reset independently of scratch.
    # The step gate already bounds RA to +-100 us. Its biased low word
    # compares unsigned below 2B+1 exactly inside the signed tracking band.
    p.emit("RDST", rd=RB, imm=RG_PHC | 2, fmt=FMT_Q)
    p.emit("ALU", rd=RW, ra=RA, rb=0, cnd=ALU_ADD, imm=SLEW_SETTLED_NS_C)
    p.emit("CMP", ra=RW, rb=0, fmt=FMT_D, imm=2 * SLEW_SETTLED_NS_C + 1)
    p.emit("BRS", cnd=BRS_LT, label="sv_tracking")
    p.emit("MOVE", rd=RB, ra=0, imm=3)                       # reload, then -1
    p.label("sv_tracking")
    p.emit("CMP", ra=RB, rb=0, fmt=FMT_Q, imm=0)
    p.emit("BRS", cnd=BRS_Z, label="sv_decided")
    p.emit("ALU", rd=RB, ra=RB, rb=0, cnd=ALU_SUB, imm=1)
    p.label("sv_decided")
    p.emit("WRST", ra=RB, imm=RG_PHC | 2, fmt=FMT_Q)
    p.emit("MOVE", rd=RB, ra=0, imm=RUNTIME["gain_m"])
    p.emit("MD", rd=RT, ra=RA, rb=RB, cnd=MD_MULS)           # off * M
    p.emit("ALU", rd=RT, ra=RT, rb=0, cnd=ALU_SAR, imm=GAIN_S_C)
    p.emit("ALU", rd=RB, ra=RT, rb=0, cnd=ALU_SAR, imm=2)    # ki term
    p.emit("RDST", rd=RC, imm=RG_SCR | S_INTG, fmt=FMT_Q)
    p.emit("ALU", rd=RC, ra=RC, rb=RB, cnd=ALU_ADD)
    e_sat(p, RC, RUNTIME["ilim"], "sv_i")                    # +-ILIM
    p.emit("WRST", ra=RC, imm=RG_SCR | S_INTG, fmt=FMT_Q)
    p.emit("ALU", rd=RB, ra=RT, rb=0, cnd=ALU_SAR, imm=2)
    p.emit("ALU", rd=RT, ra=RT, rb=RB, cnd=ALU_SUB)          # kp = 3/4
    p.emit("ALU", rd=RT, ra=RT, rb=RC, cnd=ALU_ADD)          # + I
    p.emit("BR", label=LB["SVRATE"])
    return p


def prog_leg_svrate(base: int) -> Prog:
    """Replace the rate and finish a consumed pair's policy transaction."""
    p = Prog(base)
    # the whole trim, proportional plus integral, stays inside the rate
    # envelope the parent's egress reconstruction enforces
    e_sat(p, RT, RUNTIME["ilim"], "sv_a")                    # +-200 ppm
    p.emit("ALU", rd=RT, ra=R0, rb=RT, cnd=ALU_SUB)          # negate
    p.emit("WRST", ra=RT, imm=RG_PHC | 0, fmt=FMT_Q)         # adjfine
    p.emit("WRST", ra=0, imm=RG_SCR | S_SYNCTS, fmt=FMT_Q)   # consumed
    p.emit("MOVE", rd=RT, ra=0, imm=SYNC_RTO_MS_C)
    p.emit("WRST", ra=RT, imm=RG_TMR | 4, fmt=FMT_Q)         # sync watch
    p.emit("WRST", ra=0, imm=RG_TMR | 5, fmt=FMT_Q)          # FU watch off
    # a consumed pair locks the servo; only an asCapable rise unlocks it
    p.emit("MOVE", rd=RT, ra=0, imm=STEP_LOCKED_NS_C - STEP_LINKUP_NS_C)
    p.emit("WRST", ra=RT, imm=RG_SCR | S_LOCK, fmt=FMT_Q)
    e_flags(p, orm=FL_SYNCOK_C)
    p.emit("COMMIT")
    p.emit("END")
    return p


def prog_rx_announce(base: int) -> Prog:
    """Announce receipt (entry 128): 10.3.10.2.1 qualifyAnnounce runs ahead
    of every write this handler makes, so only a qualified vector reaches
    BTCA and a disqualified one moves no grandmaster."""
    p = Prog(base)
    e_guard_init(p, "out")
    # 802.1AS: a port that is not asCapable does not enter the contest
    e_flag_gate(p, FL_ASCAP_C, FL_ASCAP_C, "ac", "out")
    # ---- 10.3.10.2.1 qualifyAnnounce, ahead of every write -----------
    # (a) sent by this time-aware system: sourcePortIdentity.clockIdentity
    #     equal to thisClock (IEEE 1588-2008 9.3.2.5 a); an Announce that
    #     claims our own identity never re-elects anything
    p.emit("RDST", rd=RD_, imm=RG_BANK | 2, fmt=FMT_Q)     # their source
    p.emit("RDST", rd=RT, imm=RG_SCR | S_CID, fmt=FMT_Q)
    p.emit("CMP", ra=RD_, rb=RT, fmt=FMT_Q)
    p.emit("BRS", cnd=BRS_Z, label="out")
    # (b) stepsRemoved >= 255 (IEEE 1588-2008 9.3.2.5 d): rogue frames
    #     are extinguished; the raw field, before the receiver-side +1
    p.emit("RDST", rd=RC, imm=RG_BANK | 10, fmt=FMT_Q)
    p.emit("ALU", rd=RC, ra=RC, rb=0, cnd=ALU_SHR, imm=48)  # stepsRemoved
    p.emit("CMP", ra=RC, rb=0, fmt=FMT_W, imm=STEPS_MAX_C)
    p.emit("BRS", cnd=BRS_LT, label="steps_ok")
    p.emit("BR", label="out")
    p.label("steps_ok")
    # (c) for a present TLV, the parser has already checked its framing, head
    #     and count, and compared EVERY hop (not merely stored w16..w23) with
    #     thisClock. For an absent TLV both count and loop are zero. Word 12
    #     bit 8 is the complete loop verdict in either case.
    p.emit("RDST", rd=RV, imm=RG_BANK | 12, fmt=FMT_Q)
    p.emit("ALU", rd=RV, ra=RV, rb=0, cnd=ALU_SHR, imm=8)
    p.emit("CMP", ra=RV, rb=0, fmt=FMT_D, imm=0)
    p.emit("BRS", cnd=BRS_Z, label="qualified")
    p.emit("BR", label="out")
    p.label("qualified")
    # ---- (d) qualified: the vector, published raw first (bench) -------
    p.emit("RDST", rd=RA, imm=RG_BANK | 8, fmt=FMT_Q)   # their {utc,p1,cq,p2}
    p.emit("WRST", ra=RA, imm=RG_PUB | 5, fmt=FMT_Q)    # publish raw: bench
    p.emit("ALU", rd=RA, ra=RA, rb=0, cnd=ALU_SHL, imm=16)  # {p1,cq,p2,0}
    p.emit("RDST", rd=RB, imm=RG_BANK | 9, fmt=FMT_Q)   # their gm identity
    p.emit("ALU", rd=RC, ra=RC, rb=0, cnd=ALU_ADD, imm=1)  # steps+1
    p.emit("ALU", rd=RC, ra=RC, rb=0, cnd=ALU_AND, imm=0xFFFF)
    # Source, vector, GM, steps, count and every retained hop are frozen in
    # the single Announce context from event enqueue through handler END.
    # Chasing Announces are explicitly dropped/counted while it is owned, so
    # neither parser-bank reuse nor an ABA sequence collision can splice it.
    p.emit("BR", label=LB["BTCA"])
    p.label("out")
    p.emit("END")
    return p


def prog_rx_pdreq(base: int) -> Prog:
    """Pdelay_Req receipt (entry 192): answer a neighbour's request with a
    Pdelay_Resp carrying t2 and its requestingPortIdentity, and claim the
    egress stamp the paired Follow_Up will carry as t3."""
    p = Prog(base)
    e_guard_init(p, "out")
    # IEEE 1588-2008 9.5.2.2: "A message received at the same port that
    # issued the message shall be ignored". The subclause identifies that
    # by comparing the received sourcePortIdentity against the port's own
    # portIdentity, both members; this gate compares the clockIdentity
    # member alone (bank word 2), which is the identity scope this plane
    # keeps everywhere -- see the note at the head of this file. Table
    # 17's third row, our clockIdentity from a different portNumber, is
    # therefore refused here as well, which 9.5.2.2 does not require of a
    # single-port end station and 9.5.2.3 handles for boundary clocks;
    # the portNumber half is #30's, not this round's.
    #
    # 802.1AS-2011 Figure 11-9, the MDPdelayResp machine this handler
    # implements, carries no such condition of its own, so 9.5.2.2 is the
    # whole mandate on this side, unlike the requester side where Figure
    # 11-8 states it (FPGA-gPTP #26). 802.1AS-2011 7.1 is what makes it
    # bind: the standard is a stand-alone document and a proper profile
    # of 1588, so the base clause applies through the profile rather than
    # through any 802.1AS clause of its own.
    #
    # Answering our own reflected request is not merely useless: before
    # #28, a response could steal the egress timestamp our outstanding
    # Pdelay_Req was waiting for. The type-qualified claim below closes
    # that routing ambiguity, while this identity gate remains required
    # by the base protocol.
    #
    # Refusing ahead of the scratch writes is belt-and-braces, not
    # load-bearing: measured, moving the compare below them leaves the
    # suite at 340/340, because S_RQSEQ, S_RQCID and S_RQPN are consumed
    # within this same pass and by a PDPOST leg that a refused request
    # never arms. It stays first because "no residue" is cheaper to keep
    # true than to re-argue. RB carries their source on to S_RQCID below
    p.emit("RDST", rd=RB, imm=RG_BANK | 2, fmt=FMT_Q)            # their source
    p.emit("RDST", rd=RT, imm=RG_SCR | S_CID, fmt=FMT_Q)
    p.emit("CMP", ra=RB, rb=RT, fmt=FMT_Q)
    p.emit("BRS", cnd=BRS_Z, label="out")
    p.emit("RDST", rd=RA, imm=RG_BANK | 0, fmt=FMT_Q)
    p.emit("ALU", rd=RA, ra=RA, rb=0, cnd=ALU_SHR, imm=32)
    p.emit("WRST", ra=RA, imm=RG_SCR | S_RQSEQ, fmt=FMT_Q)
    p.emit("WRST", ra=RB, imm=RG_SCR | S_RQCID, fmt=FMT_Q)
    p.emit("RDST", rd=RC, imm=RG_BANK | 3, fmt=FMT_Q)
    p.emit("WRST", ra=RC, imm=RG_SCR | S_RQPN, fmt=FMT_Q)
    e_hdr(p, 0x3, RA, 0x7F, 54)
    e_ts_fields(p, RTS0)
    p.emit("RDST", rd=RB, imm=RG_SCR | S_RQCID, fmt=FMT_Q)
    p.emit("BFLD", ra=RB, fmt=FMT_Q)
    p.emit("RDST", rd=RC, imm=RG_SCR | S_RQPN, fmt=FMT_Q)
    p.emit("BFLD", ra=RC, fmt=FMT_W)
    # RA still holds the request's sequenceId, the one this response
    # carries and the one the stamper reads back at the MAC boundary
    p.emit("ALU", rd=RT, ra=RA, rb=0, cnd=ALU_OR,
           imm=TXP_PEND_C | TXT_PDRESP_C)
    p.emit("WRST", ra=RT, imm=RG_SCR | S_TXQ_RESP, fmt=FMT_Q)
    p.emit("SEND")
    p.label("out")
    p.emit("END")
    return p


def prog_rx_pdresp(base: int) -> Prog:
    """Pdelay_Resp receipt (entry 256): arm the Follow_Up pairing and store
    t2/t4 when the response answers our outstanding request, and keep the
    Milan 4.2.6.2.5 count of distinct responders in this interval."""
    p = Prog(base)
    e_guard_init(p, "out")
    _pdresp_addressed_to_us(p)
    _pdresp_answers_the_outstanding_request(p)
    _pdresp_arm_the_pairing(p)
    _pdresp_count_distinct_responders(p)
    p.label("out")
    p.emit("END")
    return p


def _pdresp_addressed_to_us(p):
    """Every reason this response is not ours, ahead of any write: the two
    halves of its requestingPortIdentity, and our own frame reflected back.

    Leaves RB holding thisClock and RC the responder's clockIdentity; both
    are read by the arm and by the bookkeeping further down."""
    # 11.2.15.3 (Figure 11-8, WAITING_FOR_PDELAY_RESP): the response is
    # ours only when its requestingPortIdentity is THIS PORT'S -- both
    # halves. The clockIdentity is bank word 6, the 16-bit portNumber
    # bank word 7, and they are separate branches so each is its own arm
    # to plant against (FPGA-gPTP #36)
    p.emit("RDST", rd=RA, imm=RG_BANK | 6, fmt=FMT_Q)
    p.emit("RDST", rd=RB, imm=RG_SCR | S_CID, fmt=FMT_Q)
    p.emit("CMP", ra=RA, rb=RB, fmt=FMT_Q)
    p.emit("BRS", cnd=BRS_Z, label="myclk")
    p.emit("BR", label="out")
    p.label("myclk")
    p.emit("RDST", rd=RA, imm=RG_BANK | 7, fmt=FMT_Q)
    p.emit("CMP", ra=RA, rb=0, fmt=FMT_W, imm=OUR_PORTNUM_C)
    p.emit("BRS", cnd=BRS_Z, label="mine")
    p.emit("BR", label="out")
    p.label("mine")
    # IEEE 1588-2008 9.5.2.2: "A message received at the same port that
    # issued the message shall be ignored", identified by comparing the
    # received sourcePortIdentity against the port's own portIdentity
    # (its Table 17). 802.1AS-2011 Figure 11-8 carries the same condition
    # into this machine: asCapable is set only if
    # rcvdPdelayRespPtr->sourcePortIdentity.clockIdentity != thisClock. So
    # our own request reflected back by a loop or a misconfigured bridge
    # is not a neighbour response: refuse it here, ahead of the pairing
    # and of the 4.2.6.2.5 bookkeeping alike, because it is not a
    # responder at all (FPGA-gPTP #23). RB still holds thisClock and RC
    # carries their source from here to the arm below
    p.emit("RDST", rd=RC, imm=RG_BANK | 2, fmt=FMT_Q)            # their source
    p.emit("CMP", ra=RC, rb=RB, fmt=FMT_Q)
    p.emit("BRS", cnd=BRS_Z, label="out")


def _pdresp_answers_the_outstanding_request(p):
    """The sequenceId arm of the same figure, on the wire's 16 bits.

    Leaves RT holding the response's own sequenceId, which the arm below
    writes back with its armed bit set."""
    # 11.2.15.3 (Figure 11-8, WAITING_FOR_PDELAY_RESP): the response must
    # carry the sequenceId of OUR outstanding request, S_MYSEQ - 1 on the
    # wire's 16 bits (S_MYSEQ is never 0 here: the init leg sends the
    # first request in the dispatch that sets S_INIT, and scratch
    # survives a warm reset)
    p.emit("RDST", rd=RU, imm=RG_SCR | S_MYSEQ, fmt=FMT_Q)
    p.emit("ALU", rd=RU, ra=RU, rb=0, cnd=ALU_SUB, imm=1)
    p.emit("ALU", rd=RU, ra=RU, rb=0, cnd=ALU_AND, imm=0xFFFF)
    p.emit("RDST", rd=RT, imm=RG_BANK | 0, fmt=FMT_Q)
    p.emit("ALU", rd=RT, ra=RT, rb=0, cnd=ALU_SHR, imm=32)
    p.emit("ALU", rd=RT, ra=RT, rb=0, cnd=ALU_AND, imm=0xFFFF)   # their seq
    p.emit("CMP", ra=RT, rb=RU, fmt=FMT_W)
    p.emit("BRS", cnd=BRS_Z, label="rs_ok")
    p.emit("BR", label="out")
    p.label("rs_ok")


def _pdresp_arm_the_pairing(p):
    """Arm the Follow_Up pairing and store t2/t4, unless this interval's
    exchange is already complete or its pair already frozen.

    Both refusals branch to the bookkeeping rather than to the exit, so the
    4.2.6.2.5 count still sees a response whose operands are refused."""
    # Figure 11-8 (as corrected by Cor2-2015): once the outstanding
    # request's pair has completed, the machine waits for the interval
    # timer, and a further Pdelay_Resp for that sequenceId is not an
    # exchange. S_PDGOT is set by both verdict paths of the completion
    # and cleared by each new request, so while it stands nothing
    # re-arms: a replayed pair can neither recompute the delay nor climb
    # the ladder a second time in one interval. The Milan 4.2.6.2.5
    # identity bookkeeping below still sees every matching response
    p.emit("RDST", rd=RU, imm=RG_SCR | S_PDGOT, fmt=FMT_Q)
    p.emit("CMP", ra=RU, rb=0, fmt=FMT_D, imm=0)
    p.emit("BRS", cnd=BRS_Z, label="arm")
    p.emit("BR", label="multi")                                   # completed
    p.label("arm")
    # A complete pair is already frozen, waiting only for its own t1
    # (FPGA-gPTP #31). Its identity and its t2/t3/t4 are THIS exchange's
    # operands and must not be rewritten: a later response carries another
    # exchange's times, and the deferred tail would compute from a mixture.
    # Fall through to the 4.2.6.2.5 bookkeeping, which still sees every
    # matching response, so the distinct-responder verdict is unchanged
    p.emit("RDST", rd=RU, imm=RG_SCR | S_PDWAIT, fmt=FMT_Q)
    p.emit("CMP", ra=RU, rb=0, fmt=FMT_D, imm=0)
    p.emit("BRS", cnd=BRS_Z, label="arm_go")
    p.emit("BR", label="multi")                                   # frozen
    p.label("arm_go")
    # arm the Follow_Up pairing: this sequence, this responder. The LAST
    # matching response before the Follow_Up owns the stored t2/t4, so
    # the Follow_Up must come from it; a second identity is the Milan
    # 4.2.6.2.5 bookkeeping below, not a reset
    p.emit("ALU", rd=RT, ra=RT, rb=0, cnd=ALU_OR, imm=RSP_ARMED_C)
    p.emit("WRST", ra=RT, imm=RG_SCR | S_RSPSEQ, fmt=FMT_Q)
    p.emit("WRST", ra=RC, imm=RG_SCR | S_RSPSRC, fmt=FMT_Q)
    e_full_ts(p, RA)
    p.emit("WRST", ra=RA, imm=RG_SCR | S_T2, fmt=FMT_Q)
    p.emit("WRST", ra=RTS0, imm=RG_SCR | S_T4, fmt=FMT_Q)


def _pdresp_count_distinct_responders(p):
    """The Milan 4.2.6.2.5 identity bookkeeping for this interval, reached
    by every matching response: the armed one and the two refused above."""
    p.label("multi")
    # 4.2.6.2.5 bookkeeping: a SECOND distinct responder identity in
    # one request interval marks it multi (duplicates are not a storm)
    p.emit("RDST", rd=RB, imm=RG_SCR | S_RSP1, fmt=FMT_Q)
    p.emit("CMP", ra=RB, rb=0, fmt=FMT_Q, imm=0)
    p.emit("BRS", cnd=BRS_Z, label="rsp1")
    p.emit("CMP", ra=RB, rb=RC, fmt=FMT_Q)
    p.emit("BRS", cnd=BRS_Z, label="out")
    p.emit("MOVE", rd=RT, ra=0, imm=1)
    p.emit("WRST", ra=RT, imm=RG_SCR | S_IVMULTI, fmt=FMT_Q)
    p.emit("BR", label="out")
    p.label("rsp1")
    p.emit("WRST", ra=RC, imm=RG_SCR | S_RSP1, fmt=FMT_Q)


def prog_rx_pdrfu(base: int) -> Prog:
    """Pdelay_Resp_Follow_Up receipt (entry 320): compute t3 and hand the
    exchange to PDPOST, which owns the sequence and responder pairing
    rules; only the requesting clockIdentity is checked here."""
    p = Prog(base)
    e_guard_init(p, "out")
    p.emit("RDST", rd=RA, imm=RG_BANK | 6, fmt=FMT_Q)
    p.emit("RDST", rd=RB, imm=RG_SCR | S_CID, fmt=FMT_Q)
    p.emit("CMP", ra=RA, rb=RB, fmt=FMT_Q)
    p.emit("BRS", cnd=BRS_Z, label="mine")
    p.emit("BR", label="out")
    p.label("mine")
    e_full_ts(p, RC)                                    # RC = t3
    p.emit("BR", label=LB["PDPOST"])
    p.label("out")
    p.emit("END")
    return p


def prog_rx_signal(base: int) -> Prog:
    """Signaling receipt (entry 384): accepted and dropped. This plane
    negotiates no message intervals, so there is nothing to consume."""
    p = Prog(base)
    p.emit("END")
    return p


def e_txq_match(p: Prog, t1: str, sync: str, resp: str) -> None:
    """Route one dispatched result to the claim it names, or fall through.

    ONE source for the routing rule, read by both the valid handler and the
    lost arm below, so the two can never disagree about which claim a
    result owns. Clobbers RU, RA and RB; leaves the fall-through case (a
    result no outstanding frame claims) to the caller."""
    p.emit("ALU", rd=RU, ra=REV, rb=0, cnd=ALU_AND,
           imm=0xFFFF | TXT_TYPE_MASK_C)
    p.emit("ALU", rd=RU, ra=RU, rb=0, cnd=ALU_OR, imm=TXP_PEND_C)
    p.emit("RDST", rd=RA, imm=RG_SCR | S_TXQ_TMR, fmt=FMT_Q)
    p.emit("ALU", rd=RA, ra=RA, rb=0, cnd=ALU_AND, imm=TXQ_MASK_C)
    p.emit("CMP", ra=RA, rb=RU, fmt=FMT_Q)
    p.emit("BRS", cnd=BRS_Z, label=t1)
    p.emit("ALU", rd=RB, ra=RU, rb=0, cnd=ALU_OR, imm=TXP_SYNC_C)
    p.emit("CMP", ra=RA, rb=RB, fmt=FMT_Q)
    p.emit("BRS", cnd=BRS_Z, label=sync)
    p.emit("RDST", rd=RA, imm=RG_SCR | S_TXQ_RESP, fmt=FMT_Q)
    p.emit("ALU", rd=RA, ra=RA, rb=0, cnd=ALU_AND, imm=TXQ_MASK_C)
    p.emit("CMP", ra=RA, rb=RU, fmt=FMT_Q)
    p.emit("BRS", cnd=BRS_Z, label=resp)


def prog_tx_ts(base: int) -> Prog:
    """Match the result to a claim by {messageType, sequenceId}.

    The parent stamper returns both fields from the PTP header beside the
    timestamp. The engine packs messageType in REV[19:16] and sequenceId
    in REV[15:0]. Every transmitter that needs a stamp leaves the same pair
    in its claim, so credit is order-independent even when both ends start
    their 16-bit counters at zero. Frames that deliberately leave no claim
    (Announce and both Follow_Up kinds) cannot clear another frame's claim,
    because their messageType differs. Two frames of one claimed type are
    never outstanding at once; the transmitter-side claim gates establish
    that invariant.

    REV[23] is the outcome. A result with it clear carries no time: it goes
    to TXLOST, which retires the SAME claim this routing names and touches
    nothing else (FPGA-gPTP #31). The valid t1 tail is TXT1OK, and the
    lost arm is TXLOST, because entry 448 is a 64-word slot shared with the
    packer's first-fit space; keeping both tails packable is what lets the
    ROM hold the whole result face."""
    p = Prog(base)
    p.emit("ALU", rd=RW, ra=REV, rb=0, cnd=ALU_AND, imm=TXT_OK_C)
    p.emit("CMP", ra=RW, rb=0, fmt=FMT_D, imm=0)
    p.emit("BRS", cnd=BRS_Z, label=LB["TXLOST"])
    e_txq_match(p, "t1", "sync", "resp")
    p.emit("END")                      # a result no outstanding frame claims
    p.label("resp")
    p.emit("WRST", ra=0, imm=RG_SCR | S_TXQ_RESP, fmt=FMT_Q)
    p.emit("BR", label=LB["RFU"])
    p.label("sync")
    p.emit("WRST", ra=0, imm=RG_SCR | S_TXQ_TMR, fmt=FMT_Q)
    p.emit("BR", label=LB["SYNCFU"])
    p.label("t1")
    p.emit("WRST", ra=0, imm=RG_SCR | S_TXQ_TMR, fmt=FMT_Q)
    p.emit("BR", label=LB["TXT1OK"])
    return p


def prog_leg_txlost(base: int) -> Prog:
    """An explicitly lost result: retire its own claim and nothing else.

    Scope is the whole point. A lost Pdelay_Req stamp is the only one that
    owns the requester's pairing state, so it alone clears S_T1V and
    S_PDWAIT; a lost Sync or Pdelay_Resp stamp retires its own claim, sends
    no companion and must leave an unrelated requester exchange exactly
    where it was. No arm writes a time: a fabricated t1 is worse than a
    missing one, because the delay it computes looks ordinary."""
    p = Prog(base)
    e_txq_match(p, "t1", "sync", "resp")
    p.emit("END")                      # a result no outstanding frame claims
    p.label("sync")
    p.emit("WRST", ra=0, imm=RG_SCR | S_TXQ_TMR, fmt=FMT_Q)
    p.emit("END")                      # no SYNCFU: there is no origin time
    p.label("resp")
    p.emit("WRST", ra=0, imm=RG_SCR | S_TXQ_RESP, fmt=FMT_Q)
    p.emit("END")                      # no RFU: there is no t3 to carry
    p.label("t1")
    p.emit("WRST", ra=0, imm=RG_SCR | S_TXQ_TMR, fmt=FMT_Q)
    p.emit("WRST", ra=0, imm=RG_SCR | S_T1V, fmt=FMT_Q)
    p.emit("WRST", ra=0, imm=RG_SCR | S_PDWAIT, fmt=FMT_Q)
    p.emit("END")
    return p


def prog_leg_txt1ok(base: int) -> Prog:
    """A valid t1: record it, declare it valid, and release any pair that
    has been waiting for it.

    S_T1 may be numeric zero, which is why the validity is its own cell.
    A Pdelay_Resp_Follow_Up that completed its pairing before this result
    arrived left its whole exchange frozen behind S_PDWAIT; consuming the
    gate here is what makes the deferred tail run exactly once, and it is
    consumed BEFORE the tail reads the operands."""
    p = Prog(base)
    p.emit("WRST", ra=RTS0, imm=RG_SCR | S_T1, fmt=FMT_Q)
    p.emit("MOVE", rd=RT, ra=0, imm=1)
    p.emit("WRST", ra=RT, imm=RG_SCR | S_T1V, fmt=FMT_Q)
    p.emit("RDST", rd=RA, imm=RG_SCR | S_PDWAIT, fmt=FMT_Q)
    p.emit("CMP", ra=RA, rb=0, fmt=FMT_D, imm=0)
    p.emit("BRS", cnd=BRS_Z, label="out")            # nothing deferred
    p.emit("WRST", ra=0, imm=RG_SCR | S_PDWAIT, fmt=FMT_Q)
    p.emit("RDST", rd=RC, imm=RG_SCR | S_T3, fmt=FMT_Q)
    p.emit("BR", label=LB["PDEPOCH"])
    p.label("out")
    p.emit("END")
    return p


def prog_tmr(base: int, mac: int, seq_seed: int = 0,
             sync_seq_seed: int = 0) -> Prog:
    """The 1 s timer program: the event-slot dispatch, the one-shot init, the
    cadence gate and the Milan cease rule, then the packed request leg."""
    p = Prog(base)
    _tmr_slot_dispatch(p)
    _tmr_init_once(p, mac, seq_seed, sync_seq_seed)
    _tmr_cadence_gate(p)
    _tmr_cease_rule(p)
    p.emit("WRST", ra=0, imm=RG_SCR | S_PDSTEP, fmt=FMT_Q)
    p.emit("BR", label=LB["PDREQ"])
    return p


def _tmr_slot_dispatch(p):
    """Event slot -> leg. Slot 0 is this program's own cadence."""
    p.emit("CMP", ra=REV, rb=0, fmt=FMT_W, imm=0)
    p.emit("BRS", cnd=BRS_Z, label="slot0")
    p.emit("CMP", ra=REV, rb=0, fmt=FMT_W, imm=1)
    p.emit("BRS", cnd=BRS_Z, label=LB["SYNCTX"])
    p.emit("CMP", ra=REV, rb=0, fmt=FMT_W, imm=2)
    p.emit("BRS", cnd=BRS_Z, label=LB["BECGATE"])
    p.emit("CMP", ra=REV, rb=0, fmt=FMT_W, imm=3)
    p.emit("BRS", cnd=BRS_Z, label=LB["ANNTX"])
    p.emit("CMP", ra=REV, rb=0, fmt=FMT_W, imm=4)
    p.emit("BRS", cnd=BRS_Z, label=LB["SRTO"])
    p.emit("CMP", ra=REV, rb=0, fmt=FMT_W, imm=5)
    p.emit("BRS", cnd=BRS_Z, label=LB["FUTO"])
    p.emit("END")
    p.label("slot0")


def _tmr_init_once(p, mac, seq_seed, sync_seq_seed):
    """The init leg, taken exactly once: our clock vector, the frame
    constants derived from `mac`, and the scratch cells cleared at boot."""
    cid = ((mac >> 24) << 40) | (0xFFFE << 24) | (mac & 0xFFFFFF)
    hdr8 = (0x0180C200000E << 16) | ((mac >> 32) & 0xFFFF)
    salo = mac & 0xFFFFFFFF
    mypv = (RUNTIME["p1"] << 56) | (CQ_C << 24) | (P2_C << 16)
    annbody = (UTC_OFF_C << 48) | (RUNTIME["p1"] << 32) | CQ_C
    p.emit("RDST", rd=RA, imm=RG_SCR | S_INIT, fmt=FMT_Q)
    p.emit("CMP", ra=RA, rb=0, fmt=FMT_D, imm=1)
    p.emit("BRS", cnd=BRS_Z, label="cadence")
    p.emit("MOVE", rd=R0, ra=0, imm=0)
    e_const(p, RP, 1_000_000_000)
    p.emit("WRST", ra=RP, imm=RG_SCR | S_1E9, fmt=FMT_Q)
    e_const(p, RC, cid)
    p.emit("WRST", ra=RC, imm=RG_SCR | S_CID, fmt=FMT_Q)
    p.emit("WRST", ra=RC, imm=RG_SCR | S_BESTID, fmt=FMT_Q)
    p.emit("WRST", ra=RC, imm=RG_SCR | S_BESTSRC, fmt=FMT_Q)
    e_const(p, RC, hdr8)
    p.emit("WRST", ra=RC, imm=RG_SCR | S_HDR8, fmt=FMT_Q)
    e_const(p, RC, salo)
    p.emit("WRST", ra=RC, imm=RG_SCR | S_SALO, fmt=FMT_Q)
    e_const(p, RC, mypv)
    p.emit("WRST", ra=RC, imm=RG_SCR | S_MYPV, fmt=FMT_Q)
    p.emit("WRST", ra=RC, imm=RG_SCR | S_BESTPV, fmt=FMT_Q)  # steps 0: us
    e_const(p, RC, annbody)
    p.emit("WRST", ra=RC, imm=RG_SCR | S_ANNBODY, fmt=FMT_Q)
    e_const(p, RC, 0xC2000001)
    p.emit("WRST", ra=RC, imm=RG_SCR | S_FUORG, fmt=FMT_Q)
    for s in (((S_MYSEQ,) if not seq_seed else ()) +
              ((S_SSEQ,) if not sync_seq_seed else ()) + (
              S_SYNCTS, S_PDELAY, S_T2, S_SSEQFLY,
              S_PDOK, S_PDLOST, S_PDGOT, S_NR3, S_NRR, S_INTG,
              S_T1, S_T4, S_TXQ_TMR, S_TXQ_RESP,
              S_ASEQ,
              S_RSP1, S_IVMULTI, S_CEASE,
              S_RSPSEQ, S_T1V)):
        p.emit("WRST", ra=0, imm=RG_SCR | s, fmt=FMT_Q)
    # S_PDWAIT is deliberately NOT in that list either: it is the gate of
    # the S_T3 invariant recorded at the scratch map, and its own RTL
    # validity register clears at every reset, cold or warm.
    # S_CEASECNT and S_MULTI are deliberately NOT in that list, which is
    # where the words for the mask below and for the seeded regression
    # image came from. Each is read only behind a gate cell, and the one
    # writer that can open that gate writes the guarded cell in the same
    # straight-line block. See the invariant beside their definitions:
    # note that this list is NOT what makes it safe, since after a warm
    # reset this leg does not run at all
    seed = seq_seed or sync_seq_seed
    if seed:
        # REGRESSION IMAGES ONLY: start exactly one sequence counter above
        # 16 bits so its claim tag carries bits owned by messageType/flags.
        # One shared seed arm keeps the already-full seeded timer program at
        # 192 words. The shipping image never takes this branch.
        p.emit("MOVE", rd=RT, ra=0, imm=seed)
        seed_cell = S_MYSEQ if seq_seed else S_SSEQ
        p.emit("WRST", ra=RT, imm=RG_SCR | seed_cell, fmt=FMT_Q)
    p.emit("MOVE", rd=RT, ra=0, imm=1)
    p.emit("WRST", ra=RT, imm=RG_SCR | S_INIT, fmt=FMT_Q)
    p.emit("MOVE", rd=RT, ra=0, imm=3000)
    p.emit("WRST", ra=RT, imm=RG_TMR | 2, fmt=FMT_Q)   # announce receipt


def e_credit_gate(p: Prog, skip_label: str) -> None:
    """Skip this initiating beat while the transmit path has no credit.

    Placed AFTER the leg's own timer re-arm, so a withheld beat is retried
    at the next cadence rather than lost. Only the three INITIATING legs
    carry this gate: a Pdelay_Resp answers a neighbour's request, and both
    Follow_Up companions complete a frame already on the wire, so gating
    any of them would drop mandatory service rather than postpone it."""
    p.emit("RDST", rd=RB, imm=RG_TS | 2, fmt=FMT_Q)
    p.emit("CMP", ra=RB, rb=0, fmt=FMT_D, imm=0)
    p.emit("BRS", cnd=BRS_Z, label=skip_label)


def _tmr_cadence_gate(p):
    """Re-arm the 1 s beat, then run only with credit and a free TX queue."""
    p.label("cadence")
    p.emit("MOVE", rd=RT, ra=0, imm=1000)
    p.emit("WRST", ra=RT, imm=RG_TMR | 0, fmt=FMT_Q)
    e_credit_gate(p, "beat_off")
    p.emit("RDST", rd=RB, imm=RG_SCR | S_TXQ_TMR, fmt=FMT_Q)
    p.emit("CMP", ra=RB, rb=0, fmt=FMT_D, imm=0)
    p.emit("BRS", cnd=BRS_Z, label="send")
    p.label("beat_off")
    p.emit("END")
    p.label("send")


def _tmr_cease_rule(p):
    """Milan 4.2.6.2.5: while ceased, no requests; count the resume down,
    and start the cease on CEASE_N_C successive multi-answered intervals."""
    p.emit("RDST", rd=RA, imm=RG_SCR | S_CEASE, fmt=FMT_Q)
    p.emit("CMP", ra=RA, rb=0, fmt=FMT_D, imm=1)
    p.emit("BRS", cnd=BRS_Z, label="quiet")
    p.emit("BR", label="storm_ck")
    p.label("quiet")
    # the countdown to resume: reset-proof (scratch survives, the boot
    # re-arms this cadence), one beat per second
    p.emit("RDST", rd=RB, imm=RG_SCR | S_CEASECNT, fmt=FMT_Q)
    p.emit("ALU", rd=RB, ra=RB, rb=0, cnd=ALU_SUB, imm=1)
    p.emit("WRST", ra=RB, imm=RG_SCR | S_CEASECNT, fmt=FMT_Q)
    p.emit("CMP", ra=RB, rb=0, fmt=FMT_D, imm=0)
    p.emit("BRS", cnd=BRS_Z, label="resume")
    p.emit("END")
    p.label("resume")
    p.emit("BR", label=LB["RESUME"])
    p.label("storm_ck")
    p.emit("RDST", rd=RB, imm=RG_SCR | S_IVMULTI, fmt=FMT_Q)
    p.emit("CMP", ra=RB, rb=0, fmt=FMT_D, imm=1)
    p.emit("BRS", cnd=BRS_Z, label="was_multi")
    p.emit("WRST", ra=0, imm=RG_SCR | S_MULTI, fmt=FMT_Q)   # streak over
    p.emit("BR", label="iv_clear")
    p.label("was_multi")
    p.emit("RDST", rd=RC, imm=RG_SCR | S_MULTI, fmt=FMT_Q)
    p.emit("ALU", rd=RC, ra=RC, rb=0, cnd=ALU_ADD, imm=1)
    p.emit("WRST", ra=RC, imm=RG_SCR | S_MULTI, fmt=FMT_Q)
    p.emit("CMP", ra=RC, rb=0, fmt=FMT_D, imm=CEASE_N_C)
    p.emit("BRS", cnd=BRS_LT, label="iv_clear")
    # cease: stop requesting, drop the verdict, load the countdown
    p.emit("MOVE", rd=RT, ra=0, imm=1)
    p.emit("WRST", ra=RT, imm=RG_SCR | S_CEASE, fmt=FMT_Q)
    p.emit("MOVE", rd=RT, ra=0, imm=max(1, RUNTIME["cease_ms"] // 1000))
    p.emit("WRST", ra=RT, imm=RG_SCR | S_CEASECNT, fmt=FMT_Q)
    p.emit("WRST", ra=0, imm=RG_SCR | S_PDOK, fmt=FMT_Q)
    e_flags(p, andm=FL_PRESENT_C | FL_AMGM_C | FL_SYNCOK_C)
    p.emit("COMMIT")
    p.emit("WRST", ra=0, imm=RG_SCR | S_IVMULTI, fmt=FMT_Q)
    p.emit("WRST", ra=0, imm=RG_SCR | S_RSP1, fmt=FMT_Q)
    p.emit("END")
    p.label("iv_clear")
    p.emit("WRST", ra=0, imm=RG_SCR | S_IVMULTI, fmt=FMT_Q)
    p.emit("WRST", ra=0, imm=RG_SCR | S_RSP1, fmt=FMT_Q)


def prog_leg_pdreq(base: int) -> Prog:
    """The request leg of the 1 s beat, reached only from the cease rule's
    fall-through.

    It is a packed leg rather than the tail of the fixed timer entry for
    one measured reason: entry 512 is a 192-word slot, the dispatch, init,
    cadence gate and cease rule above it already fill 139 words (140 in a
    seeded regression image), and this leg is 59 words with its pairing
    clears. Left in place it would run past entry 704. The packer puts it
    in free space instead, which is what that two-pass assembler is for."""
    p = Prog(base)
    _tmr_pdelay_request(p)
    return p


def _tmr_pdelay_request(p):
    """Judge the previous request (802.1AS-2011 10.2.4.1 lost-response
    accounting), then queue this interval's Pdelay_Req."""
    # ---- lost-response accounting (802.1AS-2011 10.2.4.1): before each
    # new request, judge the last one; skip until a first was ever sent
    p.emit("RDST", rd=RA, imm=RG_SCR | S_MYSEQ, fmt=FMT_Q)
    p.emit("CMP", ra=RA, rb=0, fmt=FMT_D, imm=0)
    p.emit("BRS", cnd=BRS_Z, label="pd_go")
    p.emit("RDST", rd=RB, imm=RG_SCR | S_PDGOT, fmt=FMT_Q)
    p.emit("CMP", ra=RB, rb=0, fmt=FMT_D, imm=0)
    p.emit("BRS", cnd=BRS_Z, label="pd_lost")
    p.emit("WRST", ra=0, imm=RG_SCR | S_PDLOST, fmt=FMT_Q)
    p.emit("BR", label="pd_go")
    p.label("pd_lost")
    p.emit("RDST", rd=RB, imm=RG_SCR | S_PDLOST, fmt=FMT_Q)
    p.emit("ALU", rd=RB, ra=RB, rb=0, cnd=ALU_ADD, imm=1)
    p.emit("WRST", ra=RB, imm=RG_SCR | S_PDLOST, fmt=FMT_Q)
    # 802.1AS-2011 11.2.12.4: the verdict falls when the count EXCEEDS
    # allowedLostResponses -- at the fourth, not the third
    p.emit("CMP", ra=RB, rb=0, fmt=FMT_D, imm=LOST_N_C + 1)
    p.emit("BRS", cnd=BRS_LT, label="pd_go")
    p.emit("WRST", ra=0, imm=RG_SCR | S_PDOK, fmt=FMT_Q)
    e_flags(p, andm=FL_PRESENT_C | FL_AMGM_C | FL_SYNCOK_C)
    p.emit("COMMIT")
    p.label("pd_go")
    p.emit("WRST", ra=0, imm=RG_SCR | S_PDGOT, fmt=FMT_Q)
    p.emit("WRST", ra=0, imm=RG_SCR | S_RSPSEQ, fmt=FMT_Q)  # no arm yet
    # A new request supersedes the previous one whole: its t1 is no longer
    # this exchange's, and a pair still waiting for that t1 can never be
    # completed. Cancel both here, where the commitment is made, so no
    # later result or Follow_Up can pair across the interval boundary
    p.emit("WRST", ra=0, imm=RG_SCR | S_T1V, fmt=FMT_Q)
    p.emit("WRST", ra=0, imm=RG_SCR | S_PDWAIT, fmt=FMT_Q)
    p.emit("RDST", rd=RA, imm=RG_SCR | S_MYSEQ, fmt=FMT_Q)
    e_hdr(p, 0x2, RA, 0x00, 54)
    p.emit("BFLD", ra=0, fmt=FMT_Q)
    p.emit("BFLD", ra=0, fmt=FMT_Q)
    p.emit("BFLD", ra=0, fmt=FMT_D)
    # S_MYSEQ is a free-running counter and the sequenceId on the wire is
    # its low 16 bits, so the tag MUST be bounded before the flags are
    # or'd in: raw, its bit 21 is TXP_SYNC_C and every Pdelay_Req stamp
    # from request 2,097,152 onwards, 24.3 days at this cadence, would be
    # routed to the Sync Follow_Up leg. Masking here also bounds the
    # counter itself, since the write-back below takes the masked value
    p.emit("ALU", rd=RA, ra=RA, rb=0, cnd=ALU_AND, imm=0xFFFF)
    p.emit("ALU", rd=RT, ra=RA, rb=0, cnd=ALU_OR,
           imm=TXP_PEND_C | TXT_PDREQ_C)
    p.emit("WRST", ra=RT, imm=RG_SCR | S_TXQ_TMR, fmt=FMT_Q)
    p.emit("ALU", rd=RA, ra=RA, rb=0, cnd=ALU_ADD, imm=1)
    p.emit("WRST", ra=RA, imm=RG_SCR | S_MYSEQ, fmt=FMT_Q)
    p.emit("SEND")
    p.emit("END")


def prog_tb_battery(base: int) -> Prog:
    """The µCPU bench battery (entry 704): one ALU or MD result per scratch
    slot, so the testbench reads back every opcode's arithmetic."""
    p = Prog(base)
    for n, cnd in enumerate([ALU_ADD, ALU_SUB, ALU_AND, ALU_OR, ALU_XOR,
                             ALU_SHL, ALU_SHR, ALU_SAR]):
        p.emit("ALU", rd=1, ra=RTS0, rb=REV, cnd=cnd)
        p.emit("WRST", ra=1, imm=RG_SCR | n, fmt=FMT_Q)
    p.emit("MD", rd=1, ra=RTS0, rb=REV, cnd=MD_MULS)
    p.emit("WRST", ra=1, imm=RG_SCR | 8, fmt=FMT_Q)
    p.emit("MD", rd=1, ra=RTS0, rb=REV, cnd=MD_DIVU)
    p.emit("WRST", ra=1, imm=RG_SCR | 9, fmt=FMT_Q)
    p.emit("ALU", rd=1, ra=RTS0, rb=0, cnd=ALU_ADD, imm=0xABC)
    p.emit("WRST", ra=1, imm=RG_SCR | 10, fmt=FMT_Q)
    p.emit("ALU", rd=1, ra=RTS0, rb=0, cnd=ALU_SHR, imm=16)
    p.emit("WRST", ra=1, imm=RG_SCR | 11, fmt=FMT_Q)
    p.emit("END")
    return p


# ---- shared legs (auto-packed) ---------------------------------------------

def prog_btca(base: int) -> Prog:
    """RA = their {p1,cq,p2,16'0}, RB = their gmId; the bank still holds
    the announce. 10.3.4/10.3.5: a parent update replaces the best
    unconditionally; anything else must beat it lexicographically --
    pv, then gmId, then stepsRemoved(+1), then sourcePortIdentity.
    Afterwards our own vector contests whatever the best now is."""
    p = Prog(base)
    p.emit("RDST", rd=RT, imm=RG_SCR | S_BESTSRC, fmt=FMT_Q)
    p.emit("CMP", ra=RD_, rb=RT, fmt=FMT_Q)
    p.emit("BRS", cnd=BRS_Z, label="take")                 # parent update
    p.emit("RDST", rd=RV, imm=RG_SCR | S_BESTPV, fmt=FMT_Q)
    p.emit("ALU", rd=RV, ra=RV, rb=0, cnd=ALU_SHR, imm=16)
    p.emit("ALU", rd=RV, ra=RV, rb=0, cnd=ALU_SHL, imm=16)  # steps out
    p.emit("RDST", rd=RW, imm=RG_SCR | S_BESTID, fmt=FMT_Q)
    e_ult64(p, RA, RV, "take", "ours", "pv")
    e_ult64(p, RB, RW, "take", "ours", "id")
    p.emit("RDST", rd=RU, imm=RG_SCR | S_BESTPV, fmt=FMT_Q)
    p.emit("ALU", rd=RU, ra=RU, rb=0, cnd=ALU_AND, imm=0xFFFF)
    p.emit("CMP", ra=RC, rb=RU, fmt=FMT_W)                 # steps low16
    p.emit("BRS", cnd=BRS_LT, label="take")
    p.emit("BRS", cnd=BRS_Z, label="srctie")
    p.emit("BR", label="ours")
    p.label("srctie")
    # NEVER hand RT/RU to e_ult64: they are its scratch registers
    p.emit("RDST", rd=RW, imm=RG_SCR | S_BESTSRC, fmt=FMT_Q)
    e_ult64(p, RD_, RW, "take", "ours", "sp")
    p.emit("BR", label="take")                             # identical
    p.label("take")
    p.emit("ALU", rd=RU, ra=RA, rb=RC, cnd=ALU_OR)         # pv | steps
    p.emit("WRST", ra=RU, imm=RG_SCR | S_BESTPV, fmt=FMT_Q)
    p.emit("WRST", ra=RB, imm=RG_SCR | S_BESTID, fmt=FMT_Q)
    p.emit("WRST", ra=RD_, imm=RG_SCR | S_BESTSRC, fmt=FMT_Q)
    # Stage this taken Announce's frozen PathTrace into the raw publish bank.
    # Address 7 atomically copies the count/tail-only publication snapshot and
    # clears inactive tail words. Handler reads independently use the compact
    # serial ann_ctx_r port; spending fourteen ROM words to copy the same path
    # through that port would overflow this deliberately full µcode image.
    # `they_win` is also reachable from a later worse Announce, so that later
    # frame never executes this `take` block and cannot replace the selected
    # path. The wrapper samples the raw bank only at the final COMMIT.
    p.emit("WRST", ra=0, imm=RG_PUB | 7, fmt=FMT_Q)
    p.label("ours")
    # the contest: {mypv, our cid, steps 0} vs the (updated) best
    p.emit("RDST", rd=RA, imm=RG_SCR | S_MYPV, fmt=FMT_Q)
    p.emit("RDST", rd=RV, imm=RG_SCR | S_BESTPV, fmt=FMT_Q)
    p.emit("ALU", rd=RV, ra=RV, rb=0, cnd=ALU_SHR, imm=16)
    p.emit("ALU", rd=RV, ra=RV, rb=0, cnd=ALU_SHL, imm=16)
    p.emit("RDST", rd=RB, imm=RG_SCR | S_CID, fmt=FMT_Q)
    p.emit("RDST", rd=RW, imm=RG_SCR | S_BESTID, fmt=FMT_Q)
    e_ult64(p, RA, RV, "we_win", "they_win", "opv")
    e_ult64(p, RB, RW, "we_win", "they_win", "oid")
    p.emit("RDST", rd=RU, imm=RG_SCR | S_BESTPV, fmt=FMT_Q)
    p.emit("CMP", ra=RU, rb=0, fmt=FMT_W, imm=0)
    p.emit("BRS", cnd=BRS_Z, label="we_win")     # stored steps 0 = us
    p.label("they_win")
    # A zero write resolves the path-stage guard without changing the raw
    # selected path; a worse current Announce may reach here without `take`,
    # in which case the prior best path remains in command.
    p.emit("WRST", ra=0, imm=RG_PUB | 6, fmt=FMT_Q)
    p.emit("RDST", rd=RC, imm=RG_SCR | S_BESTSRC, fmt=FMT_Q)
    p.emit("WRST", ra=RC, imm=RG_PUB | 1, fmt=FMT_Q)       # parent
    p.emit("RDST", rd=RT, imm=RG_PUB | 0, fmt=FMT_Q)
    p.emit("CMP", ra=RT, rb=RW, fmt=FMT_Q)
    p.emit("BRS", cnd=BRS_Z, label="same_gm")
    # a GM change is the full adoption; a refresh must NOT clear the
    # sync-ok verdict (v5 flickered it at the parent's announce rate)
    p.emit("WRST", ra=RW, imm=RG_PUB | 0, fmt=FMT_Q)
    e_flags(p, andm=FL_ASCAP_C, orm=FL_PRESENT_C)
    p.emit("WRST", ra=0, imm=RG_SCR | S_SYNCTS, fmt=FMT_Q)
    p.emit("WRST", ra=0, imm=RG_SCR | S_SYNCSRC, fmt=FMT_Q)
    p.emit("RDST", rd=RT, imm=RG_SCR | S_TXQ_TMR, fmt=FMT_Q)
    p.emit("ALU", rd=RT, ra=RT, rb=0, cnd=ALU_AND, imm=TXP_SYNC_C)
    p.emit("CMP", ra=RT, rb=0, fmt=FMT_D, imm=0)
    p.emit("BRS", cnd=BRS_Z, label="pk")
    p.emit("WRST", ra=0, imm=RG_SCR | S_TXQ_TMR, fmt=FMT_Q)  # FU build void
    p.label("pk")
    p.emit("WRST", ra=0, imm=RG_TMR | 1, fmt=FMT_Q)        # sync TX off
    p.emit("WRST", ra=0, imm=RG_TMR | 3, fmt=FMT_Q)        # ann TX off
    p.label("same_gm")
    p.emit("MOVE", rd=RT, ra=0, imm=3000)
    p.emit("WRST", ra=RT, imm=RG_TMR | 2, fmt=FMT_Q)       # receipt watch
    p.emit("COMMIT")
    p.emit("END")
    p.label("we_win")
    e_flag_gate(p, FL_AMGM_C, 0, "nm", "held")             # already GM?
    p.emit("BR", label=LB["BECOME"])
    p.label("held")
    p.emit("END")
    return p


def prog_becgate(base: int) -> Prog:
    """Announce receipt expiry: only an asCapable port may become master."""
    p = Prog(base)
    e_flag_gate(p, FL_ASCAP_C, FL_ASCAP_C, "bg", "held")
    p.emit("BR", label=LB["BECOME"])
    p.label("held")
    p.emit("MOVE", rd=RT, ra=0, imm=3000)
    p.emit("WRST", ra=RT, imm=RG_TMR | 2, fmt=FMT_Q)  # keep watching
    p.emit("END")
    return p


def prog_become(base: int) -> Prog:
    """Take the grandmaster role: publish our own identity, reset the
    best-vector record to ourselves, and swap the slave's receipt watches
    for the Sync and Announce transmit cadences."""
    p = Prog(base)
    # Retire the slave's phase correction before publishing mastership.
    # Word 3 replaces the trim with the retained rate estimate and clears
    # the slew verdict on that same PHC write, just as a step's rate tail.
    p.emit("RDST", rd=RT, imm=RG_SCR | S_INTG, fmt=FMT_Q)
    p.emit("ALU", rd=RT, ra=R0, rb=RT, cnd=ALU_SUB)
    p.emit("WRST", ra=RT, imm=RG_PHC | 3, fmt=FMT_Q)
    p.emit("RDST", rd=RC, imm=RG_SCR | S_CID, fmt=FMT_Q)
    p.emit("WRST", ra=RC, imm=RG_PUB | 0, fmt=FMT_Q)
    p.emit("WRST", ra=RC, imm=RG_PUB | 1, fmt=FMT_Q)
    # the best-vector record returns to ourselves: a dead parent's
    # claim expires with the receipt timeout that brought us here
    p.emit("RDST", rd=RT, imm=RG_SCR | S_MYPV, fmt=FMT_Q)
    p.emit("WRST", ra=RT, imm=RG_SCR | S_BESTPV, fmt=FMT_Q)
    p.emit("WRST", ra=RC, imm=RG_SCR | S_BESTID, fmt=FMT_Q)
    p.emit("WRST", ra=RC, imm=RG_SCR | S_BESTSRC, fmt=FMT_Q)
    e_flags(p, andm=FL_ASCAP_C, orm=FL_PRESENT_C | FL_AMGM_C)
    p.emit("MOVE", rd=RT, ra=0, imm=1)
    # A nonzero write is the self-master form of the same publication
    # transaction: one GM entry and an erased tail.
    p.emit("WRST", ra=RT, imm=RG_PUB | 6, fmt=FMT_Q)
    p.emit("WRST", ra=RT, imm=RG_TMR | 1, fmt=FMT_Q)  # sync now
    p.emit("MOVE", rd=RT, ra=0, imm=2)
    p.emit("WRST", ra=RT, imm=RG_TMR | 3, fmt=FMT_Q)  # announce now
    p.emit("WRST", ra=0, imm=RG_TMR | 2, fmt=FMT_Q)   # stop the watch
    p.emit("WRST", ra=0, imm=RG_TMR | 4, fmt=FMT_Q)   # a master expects
    p.emit("WRST", ra=0, imm=RG_TMR | 5, fmt=FMT_Q)   #   no sync
    p.emit("COMMIT")
    p.emit("END")
    return p


def prog_leg_pdpost(base: int) -> Prog:
    """Pdelay exchange complete; RC = t3. The pairing gates, then either
    the arithmetic tail or the wait for this exchange's own t1.

    The Follow_Up's own dispatch consumes its bank words inside the gates
    above, while its event still owns that bank. Only the bank-independent
    tail is deferred, so nothing here outlives the bank it reads."""
    p = Prog(base)
    _pdpost_pairing_gates(p)
    _pdpost_defer_until_t1(p)
    p.emit("BR", label=LB["PDEPOCH"])
    return p


def _pdpost_defer_until_t1(p):
    """Freeze this complete pair when its own t1 has not arrived yet.

    The requester's t1 is the egress timestamp of the Pdelay_Req this
    exchange answers. It can arrive after the Follow_Up: the result path
    can be back-pressured, and the parent may hold a result behind other
    frames. Before FPGA-gPTP #31 the tail simply ran with whatever S_T1
    held, which is a delay computed from another request's time.

    S_T3 is written only on the deferring arm, two instructions before the
    gate it is guarded by and in the same straight-line block, so it is
    never read without S_PDWAIT standing (see the invariant at the scratch
    map). S_T2, S_T4, S_RSPSEQ and S_RSPSRC are already this pair's own and
    are frozen against a later response by the S_PDWAIT test in
    prog_rx_pdresp; a later Follow_Up finds S_RSPSEQ already cleared by
    `paired`, so nothing can overwrite the frozen pair either."""
    p.emit("RDST", rd=RT, imm=RG_SCR | S_T1V, fmt=FMT_Q)
    p.emit("CMP", ra=RT, rb=0, fmt=FMT_D, imm=1)
    p.emit("BRS", cnd=BRS_Z, label="t1_here")
    p.emit("WRST", ra=RC, imm=RG_SCR | S_T3, fmt=FMT_Q)
    p.emit("MOVE", rd=RT, ra=0, imm=1)
    p.emit("WRST", ra=RT, imm=RG_SCR | S_PDWAIT, fmt=FMT_Q)
    p.emit("END")
    p.label("t1_here")


def prog_leg_pdepoch(base: int) -> Prog:
    """Retain a valid delay when a complete exchange spans a PHC step."""
    p = Prog(base)
    # A complete crossing exchange proves peer liveness, but its timestamps
    # cannot measure delay (802.1AS-2020 11.2.19.3.4). Keep the last delay
    # and capability ladder; an unanswered request still uses the loss path.
    p.emit("RDST", rd=RT, imm=RG_SCR | S_PDSTEP, fmt=FMT_Q)
    p.emit("CMP", ra=RT, rb=0, fmt=FMT_D, imm=0)
    p.emit("BRS", cnd=BRS_Z, label=LB["PDPAIR"])
    p.emit("WRST", ra=RT, imm=RG_SCR | S_PDGOT, fmt=FMT_Q)
    p.emit("END")
    return p


def prog_leg_pdpair(base: int) -> Prog:
    """The bank-independent tail of a complete Pdelay exchange; RC = t3.

    Entered through PDEPOCH from the Follow_Up or a deferred t1 result.
    Reads only scratch and publication, never a released message bank.
    """
    p = Prog(base)
    _pdpost_neighbor_rate_ratio(p)
    _pdpost_corrected_delay(p)
    _pdpost_verdict(p)
    p.emit("COMMIT")
    p.emit("END")
    return p


def _pdpost_pairing_gates(p):
    """Every reason to refuse this Follow_Up, ahead of any write: the port
    number, the armed sequenceId, the armed responder, and the cease."""
    # 11.2.15.3 (Figure 11-8, WAITING_FOR_PDELAY_RESP_FOLLOW_UP): the
    # Follow_Up is consumed only when a Pdelay_Resp with this sequenceId
    # answered the outstanding request (the arm is cleared by each new
    # request and by consumption) and it comes from that responder;
    # anything else is ignored here, ahead of every write, and
    # neighborPropDelay, the ladder and asCapable stay where they are.
    # This leg is the Follow_Up handler's only continuation; it lives
    # here rather than in the fixed slot so SERVO keeps its 48-word home
    # behind that slot (the ROM is 88 percent full; see the packer)
    # the portNumber half of prog_rx_pdrfu's requesting-identity check,
    # which is the ENGINE'S OWN hardening and not an arm of the figure
    # (the figure names the sequenceId and the sourcePortIdentity, the
    # two compares below). It is here and not beside its clockIdentity
    # half for one measured reason: prog_rx_pdrfu's fixed slot has 48
    # free words behind it and that is SERVO's only home, so four words
    # spent there cost the packer the whole leg. This leg is the
    # Follow_Up handler's only continuation and nothing is written
    # before it, so the frame is refused in the same place either way
    p.emit("RDST", rd=RT, imm=RG_BANK | 7, fmt=FMT_Q)
    p.emit("CMP", ra=RT, rb=0, fmt=FMT_W, imm=OUR_PORTNUM_C)
    p.emit("BRS", cnd=BRS_Z, label="fu_pn")
    p.emit("END")
    p.label("fu_pn")
    p.emit("RDST", rd=RT, imm=RG_BANK | 0, fmt=FMT_Q)
    p.emit("ALU", rd=RT, ra=RT, rb=0, cnd=ALU_SHR, imm=32)
    p.emit("ALU", rd=RT, ra=RT, rb=0, cnd=ALU_AND, imm=0xFFFF)
    p.emit("ALU", rd=RT, ra=RT, rb=0, cnd=ALU_OR, imm=RSP_ARMED_C)
    p.emit("RDST", rd=RU, imm=RG_SCR | S_RSPSEQ, fmt=FMT_Q)
    p.emit("CMP", ra=RT, rb=RU, fmt=FMT_Q)
    p.emit("BRS", cnd=BRS_Z, label="fu_seq")
    p.emit("END")
    p.label("fu_seq")
    p.emit("RDST", rd=RT, imm=RG_BANK | 2, fmt=FMT_Q)
    p.emit("RDST", rd=RU, imm=RG_SCR | S_RSPSRC, fmt=FMT_Q)
    p.emit("CMP", ra=RT, rb=RU, fmt=FMT_Q)
    p.emit("BRS", cnd=BRS_Z, label="paired")
    p.emit("END")
    p.label("paired")
    p.emit("WRST", ra=0, imm=RG_SCR | S_RSPSEQ, fmt=FMT_Q)  # one FU per Resp
    # ceased: no exchange may climb the ladder (a forged or straggling
    # response pair must not re-raise asCapable mid-cease)
    p.emit("RDST", rd=RT, imm=RG_SCR | S_CEASE, fmt=FMT_Q)
    p.emit("CMP", ra=RT, rb=0, fmt=FMT_D, imm=0)
    p.emit("BRS", cnd=BRS_Z, label="live")
    p.emit("END")
    p.label("live")


def _pdpost_neighbor_rate_ratio(p):
    """The nrr window (802.1AS-2011 11.2.15.3): Q2.30 (t3-prev3)/(t4-prev4),
    skipped whenever the window is first, stale or zero."""
    p.emit("RDST", rd=RD_, imm=RG_SCR | S_T4, fmt=FMT_Q)
    p.emit("RDST", rd=RA, imm=RG_SCR | S_NR3, fmt=FMT_Q)
    p.emit("CMP", ra=RA, rb=0, fmt=FMT_Q, imm=0)
    p.emit("BRS", cnd=BRS_Z, label="save")           # first exchange
    p.emit("ALU", rd=RA, ra=RC, rb=RA, cnd=ALU_SUB)  # num = t3 - prev3
    p.emit("RDST", rd=RB, imm=RG_SCR | S_NR4, fmt=FMT_Q)
    p.emit("ALU", rd=RB, ra=RD_, rb=RB, cnd=ALU_SUB)  # den = t4 - prev4
    p.emit("ALU", rd=RT, ra=RB, rb=0, cnd=ALU_SHR, imm=32)
    p.emit("CMP", ra=RT, rb=0, fmt=FMT_D, imm=0)
    p.emit("BRS", cnd=BRS_Z, label="den32")
    p.emit("BR", label="save")                       # stale window: skip
    p.label("den32")
    p.emit("CMP", ra=RB, rb=0, fmt=FMT_D, imm=0)
    p.emit("BRS", cnd=BRS_Z, label="save")           # zero window
    p.emit("ALU", rd=RA, ra=RA, rb=0, cnd=ALU_SHL, imm=30)
    p.emit("MD", rd=RV, ra=RA, rb=RB, cnd=MD_DIVU)   # Q2.30 ratio
    p.emit("WRST", ra=RV, imm=RG_SCR | S_NRR, fmt=FMT_Q)
    p.label("save")
    p.emit("WRST", ra=RC, imm=RG_SCR | S_NR3, fmt=FMT_Q)
    p.emit("WRST", ra=RD_, imm=RG_SCR | S_NR4, fmt=FMT_Q)


def _pdpost_corrected_delay(p):
    """The published link delay: D = (nrr*(t4-t1) - (t3-t2)) / 2."""
    p.emit("RDST", rd=RB, imm=RG_SCR | S_T1, fmt=FMT_Q)
    p.emit("ALU", rd=RB, ra=RD_, rb=RB, cnd=ALU_SUB)  # turn = t4 - t1
    p.emit("RDST", rd=RV, imm=RG_SCR | S_NRR, fmt=FMT_Q)
    p.emit("CMP", ra=RV, rb=0, fmt=FMT_Q, imm=0)
    p.emit("BRS", cnd=BRS_Z, label="uncorr")         # no ratio yet
    p.emit("MD", rd=RB, ra=RV, rb=RB, cnd=MD_MULS)
    p.emit("ALU", rd=RB, ra=RB, rb=0, cnd=ALU_SHR, imm=30)
    p.label("uncorr")
    p.emit("RDST", rd=RT, imm=RG_SCR | S_T2, fmt=FMT_Q)
    p.emit("ALU", rd=RC, ra=RC, rb=RT, cnd=ALU_SUB)  # resid = t3 - t2
    p.emit("ALU", rd=RD_, ra=RB, rb=RC, cnd=ALU_SUB)
    p.emit("ALU", rd=RD_, ra=RD_, rb=0, cnd=ALU_SAR, imm=1)
    p.emit("WRST", ra=RD_, imm=RG_SCR | S_PDELAY, fmt=FMT_Q)
    p.emit("WRST", ra=RD_, imm=RG_PUB | 3, fmt=FMT_Q)


def _pdpost_verdict(p):
    """The threshold verdict and the asCapable ladder: good iff
    -80 <= D <= 800, i.e. (D + 80) u<= 880. The one asCapable setter, so
    it also arms the #68 link-up, and nothing else does: a rise, which it
    tells by finding the flag clear, writes S_LOCK zero (see the invariant
    at the scratch map).
    Both verdicts mark the exchange answered, so that write leads."""
    p.emit("MOVE", rd=RT, ra=0, imm=1)
    p.emit("WRST", ra=RT, imm=RG_SCR | S_PDGOT, fmt=FMT_Q)  # it DID answer
    p.emit("ALU", rd=RT, ra=RD_, rb=0, cnd=ALU_ADD, imm=NPD_LO_C)
    p.emit("ALU", rd=RU, ra=RT, rb=0, cnd=ALU_SHR, imm=32)
    p.emit("CMP", ra=RU, rb=0, fmt=FMT_D, imm=0)
    p.emit("BRS", cnd=BRS_Z, label="lowck")
    p.emit("BR", label="bad")
    p.label("lowck")
    p.emit("CMP", ra=RT, rb=0, fmt=FMT_D, imm=NPD_HI_C + NPD_LO_C + 1)
    p.emit("BRS", cnd=BRS_LT, label="good")
    p.emit("BR", label="bad")
    p.label("good")
    p.emit("WRST", ra=0, imm=RG_SCR | S_PDLOST, fmt=FMT_Q)
    p.emit("RDST", rd=RT, imm=RG_SCR | S_PDOK, fmt=FMT_Q)
    p.emit("ALU", rd=RT, ra=RT, rb=0, cnd=ALU_ADD, imm=1)
    p.emit("WRST", ra=RT, imm=RG_SCR | S_PDOK, fmt=FMT_Q)
    p.emit("CMP", ra=RT, rb=0, fmt=FMT_D, imm=ASCAP_UP_C)
    p.emit("BRS", cnd=BRS_LT, label="done")          # Milan: not before 2
    p.emit("RDST", rd=RT, imm=RG_PUB | 2, fmt=FMT_Q)
    p.emit("ALU", rd=RU, ra=RT, rb=0, cnd=ALU_AND, imm=FL_ASCAP_C)
    p.emit("ALU", rd=RT, ra=RT, rb=0, cnd=ALU_OR, imm=FL_ASCAP_C)
    p.emit("WRST", ra=RT, imm=RG_PUB | 2, fmt=FMT_Q)
    p.emit("CMP", ra=RU, rb=0, fmt=FMT_D, imm=FL_ASCAP_C)
    p.emit("BRS", cnd=BRS_Z, label="done")           # already capable
    p.emit("WRST", ra=0, imm=RG_SCR | S_LOCK, fmt=FMT_Q)  # rose: link-up
    p.emit("BR", label="done")
    p.label("bad")
    p.emit("WRST", ra=0, imm=RG_SCR | S_PDOK, fmt=FMT_Q)
    e_flags(p, andm=FL_PRESENT_C | FL_AMGM_C | FL_SYNCOK_C)
    p.label("done")


def prog_leg_resume(base: int) -> Prog:
    """The cease countdown reached zero: requests resume; asCapable
    re-earns through the ladder as ever (PDGOT set: no phantom lost)."""
    p = Prog(base)
    p.emit("WRST", ra=0, imm=RG_SCR | S_CEASE, fmt=FMT_Q)
    p.emit("WRST", ra=0, imm=RG_SCR | S_MULTI, fmt=FMT_Q)
    p.emit("WRST", ra=0, imm=RG_SCR | S_IVMULTI, fmt=FMT_Q)
    p.emit("WRST", ra=0, imm=RG_SCR | S_RSP1, fmt=FMT_Q)
    p.emit("WRST", ra=0, imm=RG_SCR | S_PDLOST, fmt=FMT_Q)
    p.emit("MOVE", rd=RT, ra=0, imm=1)
    p.emit("WRST", ra=RT, imm=RG_SCR | S_PDGOT, fmt=FMT_Q)
    p.emit("END")
    return p


def prog_leg_srto(base: int) -> Prog:
    """Sync receipt timeout (375 ms): the sync-ok verdict falls. The servo
    stays locked, so the next pair still uses the locked threshold (#68)."""
    p = Prog(base)
    e_flags(p, andm=FL_PRESENT_C | FL_AMGM_C | FL_ASCAP_C)
    p.emit("COMMIT")
    p.emit("END")
    return p


def prog_leg_futo(base: int) -> Prog:
    """Follow_Up receipt timeout (125 ms): the pending Sync is void."""
    p = Prog(base)
    p.emit("WRST", ra=0, imm=RG_SCR | S_SYNCTS, fmt=FMT_Q)
    p.emit("END")
    return p


def prog_leg_rfu(base: int) -> Prog:
    """Transmit the Pdelay_Resp_Follow_Up: the egress stamp of the response
    we just sent, addressed to the stored requestingPortIdentity."""
    p = Prog(base)
    p.emit("RDST", rd=RA, imm=RG_SCR | S_RQSEQ, fmt=FMT_Q)
    e_hdr(p, 0xA, RA, 0x7F, 54)
    e_ts_fields(p, RTS0)
    p.emit("RDST", rd=RB, imm=RG_SCR | S_RQCID, fmt=FMT_Q)
    p.emit("BFLD", ra=RB, fmt=FMT_Q)
    p.emit("RDST", rd=RC, imm=RG_SCR | S_RQPN, fmt=FMT_Q)
    p.emit("BFLD", ra=RC, fmt=FMT_W)
    p.emit("SEND")
    p.emit("END")
    return p


def prog_leg_syncfu(base: int) -> Prog:
    """Transmit the two-step Follow_Up: the Sync's egress stamp as
    preciseOriginTimestamp, plus the 802.1AS information TLV."""
    p = Prog(base)
    p.emit("RDST", rd=RA, imm=RG_SCR | S_SSEQFLY, fmt=FMT_Q)
    e_hdr(p, 0x8, RA, 0xFD, 76)
    e_ts_fields(p, RTS0)                             # preciseOrigin = t1
    p.emit("MOVE", rd=RT, ra=0, imm=0x03001C)        # TLV type 3, len 28
    p.emit("BFLD", ra=RT, fmt=FMT_D)
    p.emit("MOVE", rd=RT, ra=0, imm=0x0080)
    p.emit("BFLD", ra=RT, fmt=FMT_W)                 # org 00-80-
    p.emit("RDST", rd=RT, imm=RG_SCR | S_FUORG, fmt=FMT_Q)
    p.emit("BFLD", ra=RT, fmt=FMT_D)                 # C2 + subtype 000001
    p.emit("BFLD", ra=0, fmt=FMT_D)                  # cumScaledRateOffset
    p.emit("BFLD", ra=0, fmt=FMT_W)                  # gmTimeBaseIndicator
    p.emit("BFLD", ra=0, fmt=FMT_Q)                  # lastGmPhaseChange
    p.emit("BFLD", ra=0, fmt=FMT_D)                  #   (12 bytes)
    p.emit("BFLD", ra=0, fmt=FMT_D)                  # scaledLastGmFreqChg
    p.emit("SEND")
    p.emit("END")
    return p


def prog_leg_synctx(base: int) -> Prog:
    """The 125 ms Sync cadence: re-arm the beat, then send only as an
    asCapable grandmaster with no timer-driven stamp still owed, bounding
    the free-running counter to 16 bits before it enters the claim."""
    p = Prog(base)
    p.emit("MOVE", rd=RT, ra=0, imm=125)
    p.emit("WRST", ra=RT, imm=RG_TMR | 1, fmt=FMT_Q)
    e_flag_gate(p, FL_AMGM_C, FL_AMGM_C, "gm", "skip")
    e_flag_gate(p, FL_ASCAP_C, FL_ASCAP_C, "ac", "skip")
    e_credit_gate(p, "skip")
    p.emit("RDST", rd=RB, imm=RG_SCR | S_TXQ_TMR, fmt=FMT_Q)
    p.emit("CMP", ra=RB, rb=0, fmt=FMT_D, imm=0)
    p.emit("BRS", cnd=BRS_Z, label="build")
    p.label("skip")
    p.emit("END")                                    # skip this beat
    p.label("build")
    p.emit("RDST", rd=RA, imm=RG_SCR | S_SSEQ, fmt=FMT_Q)
    # S_SSEQ is free-running but both the frame sequenceId and its claim are
    # 16 bits. Bound it before type/flags are or'd into the claim and before
    # write-back; otherwise bit 16 becomes messageType 1 at Sync 65,536 and
    # no type-0 timestamp can clear the claim (#39).
    p.emit("ALU", rd=RA, ra=RA, rb=0, cnd=ALU_AND, imm=0xFFFF)
    p.emit("WRST", ra=RA, imm=RG_SCR | S_SSEQFLY, fmt=FMT_Q)
    e_hdr(p, 0x0, RA, 0xFD, 44)
    # 802.1AS-2011 Table 11-8: a two-step Sync carries ten reserved
    # bytes, all zero. The actual egress time arrives through the TX
    # timestamp event and is written into the paired Follow_Up.
    p.emit("BFLD", ra=0, fmt=FMT_Q)
    p.emit("BFLD", ra=0, fmt=FMT_W)
    p.emit("ALU", rd=RT, ra=RA, rb=0, cnd=ALU_OR,
           imm=TXP_PEND_C | TXP_SYNC_C)
    p.emit("WRST", ra=RT, imm=RG_SCR | S_TXQ_TMR, fmt=FMT_Q)
    p.emit("ALU", rd=RA, ra=RA, rb=0, cnd=ALU_ADD, imm=1)
    p.emit("WRST", ra=RA, imm=RG_SCR | S_SSEQ, fmt=FMT_Q)
    p.emit("SEND")
    p.emit("END")
    return p


def prog_leg_anntx(base: int) -> Prog:
    """The 1 s Announce cadence: our priority vector, grandmasterIdentity
    and a one-hop path trace, sent only while an asCapable grandmaster with
    transmit credit. The skipped beat now ends the program rather than
    sitting between the gates and the body, so the gates fall straight
    through into the build and no branch around them is needed.
    """
    p = Prog(base)
    p.emit("MOVE", rd=RT, ra=0, imm=1000)
    p.emit("WRST", ra=RT, imm=RG_TMR | 3, fmt=FMT_Q)
    e_flag_gate(p, FL_AMGM_C, FL_AMGM_C, "gm", "skip")
    e_flag_gate(p, FL_ASCAP_C, FL_ASCAP_C, "ac", "skip")
    e_credit_gate(p, "skip")
    p.emit("RDST", rd=RA, imm=RG_SCR | S_ASEQ, fmt=FMT_Q)
    e_hdr(p, 0xB, RA, 0x00, 76)
    p.emit("BFLD", ra=0, fmt=FMT_Q)                  # 10 reserved bytes
    p.emit("BFLD", ra=0, fmt=FMT_W)
    p.emit("RDST", rd=RC, imm=RG_SCR | S_ANNBODY, fmt=FMT_Q)
    p.emit("BFLD", ra=RC, fmt=FMT_Q)                 # utc,res,p1,cq
    p.emit("MOVE", rd=RT, ra=0, imm=P2_C)
    p.emit("BFLD", ra=RT, fmt=FMT_B)                 # priority2
    p.emit("RDST", rd=RC, imm=RG_SCR | S_CID, fmt=FMT_Q)
    p.emit("BFLD", ra=RC, fmt=FMT_Q)                 # grandmasterIdentity
    p.emit("BFLD", ra=0, fmt=FMT_W)                  # stepsRemoved
    p.emit("MOVE", rd=RT, ra=0, imm=0xA0)
    p.emit("BFLD", ra=RT, fmt=FMT_B)                 # timeSource internal
    p.emit("MOVE", rd=RT, ra=0, imm=0x080008)
    p.emit("BFLD", ra=RT, fmt=FMT_D)                 # path trace TLV hdr
    p.emit("RDST", rd=RC, imm=RG_SCR | S_CID, fmt=FMT_Q)
    p.emit("BFLD", ra=RC, fmt=FMT_Q)                 # our hop
    p.emit("ALU", rd=RA, ra=RA, rb=0, cnd=ALU_ADD, imm=1)
    p.emit("WRST", ra=RA, imm=RG_SCR | S_ASEQ, fmt=FMT_Q)
    p.emit("SEND")
    p.emit("END")
    p.label("skip")
    p.emit("END")                                    # skip this beat
    return p


# ---- build: fixed entries + auto-packed shared legs ------------------------

LEG_FNS = [
    ("BTCA", prog_btca), ("BECOME", prog_become), ("BECGATE", prog_becgate),
    ("RFU", prog_leg_rfu), ("SYNCFU", prog_leg_syncfu),
    ("SYNCTX", prog_leg_synctx), ("ANNTX", prog_leg_anntx),
    ("PDPOST", prog_leg_pdpost), ("PDPAIR", prog_leg_pdpair),
    ("PDEPOCH", prog_leg_pdepoch),
    ("SRTO", prog_leg_srto),
    ("FUTO", prog_leg_futo), ("SERVO", prog_leg_servo),
    ("SLEW", prog_leg_slew), ("SVRATE", prog_leg_svrate),
    ("RESUME", prog_leg_resume), ("PDREQ", prog_leg_pdreq),
    ("TXLOST", prog_leg_txlost), ("TXT1OK", prog_leg_txt1ok),
]


def build(mac: int, seq_seed: int = 0,
          sync_seq_seed: int = 0) -> tuple[list[int], int]:
    """The complete ROM image and how many of its words are real code.

    Two passes: measure every program with placeholder bases, first-fit the
    shared legs into the gaps the fixed entry table leaves, then emit with
    the real bases. An entry that would run into the next one, or a leg
    that does not fit anywhere, is an assertion rather than a bad image."""
    assert not (seq_seed and sync_seq_seed), "seed one counter per image"
    fixed = [
        (16, prog_rx_sync), (64, prog_rx_followup), (128, prog_rx_announce),
        (192, prog_rx_pdreq), (256, prog_rx_pdresp), (320, prog_rx_pdrfu),
        (384, prog_rx_signal), (448, prog_tx_ts),
        (512, lambda b: prog_tmr(b, mac, seq_seed, sync_seq_seed)),
        (704, prog_tb_battery),
    ]

    # pass 1: measure (word counts are independent of branch targets)
    for name, _ in LEG_FNS:
        LB[name] = 0
    fixed_sz = [(b, len(fn(b).words())) for b, fn in fixed]
    leg_sz = [(name, len(fn(0).words())) for name, fn in LEG_FNS]

    # a fixed program must not run into the next fixed entry
    fbases = sorted(b for b, _ in fixed) + [DEPTH]
    for b, sz in fixed_sz:
        nxt = min(x for x in fbases if x > b)
        assert b + sz <= nxt, f"fixed {b} is {sz} words, next entry {nxt}"

    # Free gaps between fixed programs, including the unused 0..15 prefix.
    # The engine only dispatches the fixed entries above; shared legs can
    # safely occupy this prefix. Reset never executes an instruction.
    gaps = []
    prev_end = 0
    for b, sz in sorted(fixed_sz):
        if b > prev_end:
            gaps.append([prev_end, b])
        prev_end = b + sz
    if prev_end < DEPTH:
        gaps.append([prev_end, DEPTH])

    # first-fit decreasing; every leg must land
    for name, sz in sorted(leg_sz, key=lambda x: -x[1]):
        for g in gaps:
            if g[1] - g[0] >= sz:
                LB[name] = g[0]
                g[0] += sz
                break
        else:
            raise AssertionError(f"leg {name} ({sz} words) does not fit")

    # pass 2: emit with real bases
    rom = [None] * DEPTH
    used = 0
    progs = fixed + [(LB[name], fn) for name, fn in LEG_FNS]
    for base, fn in progs:
        words = fn(base).words()
        for i, word in enumerate(words):
            assert rom[base + i] is None, f"overlap at {base + i}"
            rom[base + i] = word
        used += len(words)
    for i in range(DEPTH):
        if rom[i] is None:
            rom[i] = splitmix48(i)
    return rom, used


def main() -> None:
    """Write the hex image the CLI describes and report its packing."""
    ap = argparse.ArgumentParser()
    ap.add_argument("-o", "--out", default="gptp_ucode.hex")
    ap.add_argument("--seq-seed", type=lambda s: int(s, 0), default=0,
                    help="seed S_MYSEQ at init; a REGRESSION IMAGE only, "
                         "for proving a claim tag above 16 bits is bounded")
    ap.add_argument("--sync-seq-seed", type=lambda s: int(s, 0), default=0,
                    help="seed S_SSEQ at init; a REGRESSION IMAGE only, "
                         "for proving a Sync claim above 16 bits is bounded")
    ap.add_argument("--mac", type=lambda s: int(s, 0), default=0x02A1B2C3D4E5)
    ap.add_argument("--p1", type=int, default=248,
                    help="our announced priority1 (lower wins BTCA)")
    ap.add_argument("--clk-hz", type=int, default=100_000_000,
                    help="engine clock; sets the servo's ns-to-addend gain")
    ap.add_argument("--cease-ms", type=int, default=300_000,
                    help="cease-rule resume delay (Milan: 5 minutes)")
    args = ap.parse_args()
    RUNTIME["cease_ms"] = args.cease_ms
    assert 0 < RUNTIME["cease_ms"] < (1 << 24), RUNTIME["cease_ms"]
    RUNTIME["p1"] = args.p1
    set_servo_gains(args.clk_hz)
    rom, used = build(args.mac, args.seq_seed, args.sync_seq_seed)
    with open(args.out, "w", encoding="ascii") as f:
        for word in rom:
            f.write(f"{word:012X}\n")
    legs = " ".join(f"{n}@{LB[n]}" for n, _ in LEG_FNS)
    print(f"{args.out}: {DEPTH} words, {used} real "
          f"({100.0 * used / DEPTH:.1f}%), mac {args.mac:012X}")
    print(f"legs: {legs}")


if __name__ == "__main__":
    main()
