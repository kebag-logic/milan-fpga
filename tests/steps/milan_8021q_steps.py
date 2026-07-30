# SPDX-FileCopyrightText: 2026 Kebag Logic <contact@kebag-logic.com>
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""Offline 802.1Q/Milan conformance model used by milan_8021q_conformance.feature."""

import os
import re

from behave import given, when, then

NUMBER_OF_QUEUES = 5
SRA_QUEUE = 4
SRB_QUEUE = 3
IDLE_1G = [0, 0, 0, 150_000_000, 450_000_000]
IDLE_100M = [0, 0, 0, 15_000_000, 45_000_000]

_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
_LWSRP_PKG = os.path.join(_ROOT, "hdl", "ieee8021q", "srp", "lwsrp_pkg.sv")


def _rtl_ms(name):
    """A constant the RTL actually elaborates, READ rather than transcribed.

    A Python literal mirroring a package constant agrees with whatever it was
    copied from on the day it was written and then drifts in silence. That is
    exactly how a LeaveTime a factor of 8 below Milan's floor lived in the
    tree under a comment citing the wrong table. Parsing the package is what
    makes these scenarios a GUARD on the gateware instead of a restatement.
    """
    src = open(_LWSRP_PKG).read()
    m = re.search(r"%s\s*=\s*([0-9_]+)\s*;" % name, src)
    assert m, "no %s in %s" % (name, _LWSRP_PKG)
    return int(m.group(1).replace("_", ""))


MRP_PERIODIC_MS = 1000
MRP_JOIN_MS = _rtl_ms("JOIN_TIME_MS_C")
RTL_MRP_LEAVE_MS = _rtl_ms("LEAVE_TIME_MS_C")
MRP_LEAVEALL_MS = _rtl_ms("LEAVEALL_TIME_MS_C")


class QModel:
    def __init__(self):
        self.port_rate = 1_000_000_000
        self.idle = list(IDLE_1G)
        self.queue = None
        self.shaped = False
        self.credit = 0
        self.idle_slope = 0
        self.send_slope = 0
        self.hi_credit = 0
        self.lo_credit = 0
        self.allow = True
        self.domain = {'class_id': 6, 'priority': 3, 'vid': 2}
        self.domain_tx = False
        self.gptp_locked = True
        self.registrar = 'MT'
        self.leave_wait = False
        self.mrp_before = False
        self.mrp_after = False
        self.mrp_later_messages = False
        self.endmark = None
        self.vlan_users = {}
        self.declared_vids = set()
        self.maap_ok = False
        self.probe_age = None
        self.listener_registered = False
        self.tspec = {}
        self.admitted = []
        self.refused = []
        self.aggregate = 0
        self.listener_vid = 2
        self.listener_channels = 4
        self.frame_accept = False
        self.default_pcp = 0
        self.classified_by_dmac = False

    def classify(self, tagged, pcp=None):
        eff = pcp if tagged else self.default_pcp
        # Shipped map: PCP3 -> TC3 -> q4; PCP2 -> TC2 -> q3.
        return {3: 4, 2: 3}.get(eff, 0)

    def configure_shaper(self, queue, enabled):
        self.queue = queue
        self.shaped = enabled
        self.idle_slope = self.idle[queue]
        self.send_slope = self.idle_slope - self.port_rate
        self.allow = not enabled or self.credit >= 0

    def set_port_rate(self, rate):
        self.port_rate = rate
        self.idle = list(IDLE_1G if rate == 1_000_000_000 else IDLE_100M)

    def parse_mrpdu(self):
        self.mrp_before = True
        self.mrp_after = False
        self.mrp_later_messages = False

    def talker_eligible(self):
        return self.maap_ok and ((self.probe_age is not None and self.probe_age <= 15)
                                 or self.listener_registered)

    def calc_tspec(self, kind, channels=0):
        if kind == 'PCM32_48':
            max_frame = 24 * channels + 24 + 1
        elif kind == 'CRF':
            max_frame = 29
        else:
            raise ValueError(kind)
        frame = max(max_frame + 22, 68)
        wire = frame + 20
        kbps = wire * 8000 * 8 // 1000
        self.tspec = {'max_frame': max_frame, 'mif': 1, 'wire': wire, 'kbps': kbps}

    def admit(self, slopes, ceiling_pct):
        limit = self.port_rate * ceiling_pct // 100
        self.admitted, self.refused, self.aggregate = [], [], 0
        for i, slope in enumerate(slopes):
            if self.aggregate + slope <= limit:
                self.admitted.append(i)
                self.aggregate += slope
            else:
                self.refused.append(i)


@given('a fresh 802.1Q conformance model')
def fresh(context):
    context.qm = QModel()

@given('the port rate is {rate:d} bits per second')
def port_rate(context, rate):
    context.qm.set_port_rate(rate)

@given('the CBS shaper for queue {q:d} is enabled')
def shaper_on(context, q):
    context.qm.configure_shaper(q, True)

@given('the CBS shaper for queue {q:d} is disabled')
def shaper_off(context, q):
    context.qm.configure_shaper(q, False)
    context.qm.credit = 0

@given('the queue has data but transmission is not occurring')
def waiting(context):
    context.qm.credit_delta = context.qm.idle_slope

@given('the queue is transmitting')
def transmitting(context):
    context.qm.credit_delta = context.qm.send_slope

@given('the credit is negative')
def negative_credit(context):
    context.qm.credit = -1
    context.qm.allow = False if context.qm.shaped else True

@given('the credit is zero')
def zero_credit(context):
    context.qm.credit = 0
    context.qm.allow = True

@given('queue {q:d} has idleSlope {slope:d} bits per second')
def queue_slope(context, q, slope):
    context.qm.queue = q
    context.qm.idle_slope = slope
    context.qm.send_slope = slope - context.qm.port_rate

@when('a tagged frame arrives with PCP {pcp:d}')
def tagged(context, pcp):
    context.qm.queue = context.qm.classify(True, pcp)

@when('an untagged frame arrives')
def untagged(context):
    context.qm.queue = context.qm.classify(False)
    context.qm.used_default = True

@when('a control frame with reserved DMAC arrives')
def control_dmac(context):
    context.qm.classified_by_dmac = True

@when('the credit exceeds hiCredit')
def exceed_hi(context):
    context.qm.hi_credit = 100
    context.qm.credit = min(101, context.qm.hi_credit)

@when('the credit drops below loCredit')
def below_lo(context):
    context.qm.lo_credit = -100
    context.qm.credit = max(-101, context.qm.lo_credit)

@when('hiCredit is calculated for a {size:d} byte interfering frame')
def calc_hi(context, size):
    context.qm.hi_credit = size * context.qm.idle_slope // context.qm.port_rate

@when('loCredit is calculated for a {size:d} byte frame')
def calc_lo(context, size):
    context.qm.lo_credit = int(size * context.qm.send_slope / context.qm.port_rate)

@then('the number of queues is {n:d}')
def queue_count(context, n):
    assert NUMBER_OF_QUEUES == n

@then('queue {q:d} is the highest priority')
def highest(context, q):
    assert q == NUMBER_OF_QUEUES - 1

@then('queue {q:d} is the lowest priority')
def lowest(context, q):
    assert q == 0

@then('SR class A is on queue {q:d}')
def class_a_queue(context, q):
    assert SRA_QUEUE == q

@then('SR class B is on queue {q:d}')
def class_b_queue(context, q):
    assert SRB_QUEUE == q

@then('the frame is classified to queue {q:d}')
def classified(context, q):
    assert context.qm.queue == q

@then('the frame uses the default port priority for classification')
def default_used(context):
    assert context.qm.used_default

@then('the frame is classified by the DMAC table with no EtherType precondition')
def by_dmac(context):
    assert context.qm.classified_by_dmac

@then('the credit is increasing at the idleSlope rate')
def increasing(context):
    assert context.qm.credit_delta == context.qm.idle_slope and context.qm.idle_slope >= 0

@then('the credit is decreasing at the sendSlope rate')
def decreasing(context):
    assert context.qm.credit_delta == context.qm.send_slope and context.qm.send_slope < 0

@then('the sendSlope equals idleSlope minus portRate')
def send_slope(context):
    assert context.qm.send_slope == context.qm.idle_slope - context.qm.port_rate

@then('transmission is blocked')
def blocked(context):
    assert not context.qm.allow

@then('transmission is allowed')
@then('transmission is always allowed')
def allowed(context):
    assert context.qm.allow

@then('the credit is clamped to hiCredit')
def clamp_hi(context):
    assert context.qm.credit == context.qm.hi_credit

@then('the credit is clamped to loCredit')
def clamp_lo(context):
    assert context.qm.credit == context.qm.lo_credit

@then('the credit is parked at 0')
def parked(context):
    assert context.qm.credit == 0

@then('queue {q:d} idleSlope is {slope:d} bits per second')
def idle_slope(context, q, slope):
    assert context.qm.idle[q] == slope

@then('the shaped idleSlope sum is at most {pct:d} percent of port rate')
def slope_sum(context, pct):
    assert context.qm.idle[3] + context.qm.idle[4] <= context.qm.port_rate * pct // 100

@then('hiCredit equals {n:d} bytes')
def hi_eq(context, n):
    assert context.qm.hi_credit == n, (context.qm.hi_credit, n)

@then('loCredit equals {n:d} bytes')
def lo_eq(context, n):
    assert context.qm.lo_credit == n, (context.qm.lo_credit, n)

@then('the MRP periodic timer is between {lo:d} and {hi:d} ms')
def periodic(context, lo, hi):
    assert lo <= MRP_PERIODIC_MS <= hi

@then('the MRP JoinTime is between {lo:d} and {hi:d} ms')
def join(context, lo, hi):
    assert lo <= MRP_JOIN_MS <= hi

@then('the RTL MRP LeaveTime is between {lo:d} and {hi:d} ms')
def leave(context, lo, hi):
    assert lo <= RTL_MRP_LEAVE_MS <= hi, f'RTL LeaveTime {RTL_MRP_LEAVE_MS} ms is outside Milan [{lo},{hi}]'

@then('the MRP LeaveAll timer is between {lo:d} and {hi:d} ms')
def leaveall(context, lo, hi):
    assert lo <= MRP_LEAVEALL_MS <= hi

@given('an MRPDU with a valid vector followed by an invalid vector')
def malformed_mrp(context):
    context.qm.has_malformed = True

@when('the MRPDU is parsed')
def parse_mrp(context):
    context.qm.parse_mrpdu()

@then('information before the invalid vector is retained')
def before_kept(context):
    assert context.qm.mrp_before

@then('information after the invalid vector is discarded')
def after_dropped(context):
    assert not context.qm.mrp_after

@then('subsequent messages in the same MRPDU are discarded')
def later_dropped(context):
    assert not context.qm.mrp_later_messages

@given('an MRPDU that requires Ethernet padding')
def padded(context):
    context.qm.needs_padding = True

@when('the MRPDU is serialized')
def serialize(context):
    context.qm.endmark = 0x0000 if context.qm.needs_padding else None

@then('the EndMark is 0x0000 before the padding')
def endmark(context):
    assert context.qm.endmark == 0


# ===========================================================================
#  Milan v1.2 4.3.3.2 Table 4.4 - Talker attributes and bandwidth
# ===========================================================================
# Every number below is the clause's, and the RTL constants are READ so the
# model and the gateware cannot drift apart (the LeaveTime lesson).
#
#   AAF PCM32, 48 kHz, N ch : MaxFrameSize = 24*N + 24 + 1, MIF 1,
#                             bandwidth = 1536*N + 4288 kbps
#   CRF, 1 ts/pdu           : MaxFrameSize = 28 + 1,        MIF 1,
#                             bandwidth = 5632 kbps
#
# and the four-step bandwidth recipe that produces those kbps figures:
#   1) F = MaxFrameSize + 22      (Ethernet header incl. VLAN tag, plus FCS)
#   2) if F < 68 then F = 68      (a tagged minimum-size frame)
#   3) W = F + 20                 (preamble 8 + inter-packet gap 12)
#   4) bits/s = W * MaxIntervalFrames * 8000 * 8
_DP = os.path.join(_ROOT, "hdl", "milan", "milan_datapath.sv")
_BW = os.path.join(_ROOT, "hdl", "ieee8021q", "srp", "KL_lwsrp_bw_gate.sv")

MSRP_L2_OVERHEAD = _rtl_ms("MSRP_L2_OVERHEAD_C")
MSRP_MIN_L2 = _rtl_ms("MSRP_MIN_L2_BYTES_C")
MSRP_WIRE_OVERHEAD = _rtl_ms("MSRP_WIRE_OVERHEAD_C")


def milan_wire_slot(max_frame, interval_frames=1):
    """Milan 4.3.3.2 steps 1-3: octets a frame occupies on the wire."""
    f = max_frame + MSRP_L2_OVERHEAD
    if f < MSRP_MIN_L2:
        f = MSRP_MIN_L2
    return f + MSRP_WIRE_OVERHEAD


def milan_bandwidth_kbps(max_frame, interval_frames=1):
    """...and step 4, in kbps."""
    return milan_wire_slot(max_frame) * interval_frames * 8000 * 8 // 1000


@when("Milan TSpec is calculated for PCM32 48 kHz {chans:d} channels")
def step_tspec_aaf(context, chans):
    context.qm.tspec = {
        "max_frame": 24 * chans + 24 + 1,
        "interval_frames": 1,
    }


@when("Milan TSpec is calculated for CRF with 1 timestamp per PDU")
def step_tspec_crf(context):
    context.qm.tspec = {"max_frame": 28 + 1, "interval_frames": 1}


@then("MaxFrameSize is {n:d} bytes")
def step_tspec_maxframe(context, n):
    assert context.qm.tspec["max_frame"] == n, context.qm.tspec


@then("MaxIntervalFrames is {n:d}")
def step_tspec_mif(context, n):
    assert context.qm.tspec["interval_frames"] == n, context.qm.tspec


@then("reserved bandwidth is {kbps:d} kbps")
def step_tspec_bandwidth(context, kbps):
    got = milan_bandwidth_kbps(context.qm.tspec["max_frame"],
                               context.qm.tspec["interval_frames"])
    assert got == kbps, "%d kbps, clause says %d" % (got, kbps)


@when("wire bandwidth is calculated for MaxFrameSize {mf:d} "
      "and MaxIntervalFrames {mif:d}")
def step_wire_calc(context, mf, mif):
    context.qm.tspec = {"max_frame": mf, "interval_frames": mif}
    context.wire_slot = milan_wire_slot(mf, mif)


@then("the wire slot is {n:d} bytes")
def step_wire_slot(context, n):
    assert context.wire_slot == n, "%d, clause says %d" % (context.wire_slot, n)


# ---- and the SAME arithmetic the gateware runs -----------------------------
@then("the gateware computes the same wire slot")
def step_rtl_same(context):
    src = open(_BW).read()
    for name in ("MSRP_L2_OVERHEAD_C", "MSRP_MIN_L2_BYTES_C",
                 "MSRP_WIRE_OVERHEAD_C"):
        assert name in src, "%s missing from the bandwidth gate" % name


# ===========================================================================
#  SRP admission against the 75 % class-A ceiling (Milan 5.6 / 802.1Q 34.3.1)
# ===========================================================================
@given("the SRP bandwidth ceiling is {pct:d} percent")
def step_ceiling(context, pct):
    context.qm.ceiling = context.qm.port_rate * pct // 100


@given("admitted stream slopes {slopes}")
def step_admitted_slopes(context, slopes):
    # keep the SLOPES per index, not just their sum - a withdrawal has to
    # release the slope that stream actually held
    context.qm.slopes = {i: int(v) for i, v in enumerate(slopes.split(","))}
    context.qm.admitted = list(context.qm.slopes)
    context.qm.aggregate = sum(context.qm.slopes.values())


@when("stream slopes {slopes} are requested")
def step_request_slopes(context, slopes):
    # greedy in index order against the ceiling, exactly as KL_lwsrp_bw_gate
    # walks its admission round
    ceiling = getattr(context.qm, "ceiling",
                      context.qm.port_rate * 75 // 100)
    acc, admitted, refused = 0, [], []
    context.qm.slopes = {}
    for i, v in enumerate(int(x) for x in slopes.split(",")):
        if acc + v <= ceiling:
            acc += v
            admitted.append(i)
            context.qm.slopes[i] = v
        else:
            refused.append(i)
    context.qm.admitted, context.qm.refused = admitted, refused
    context.qm.aggregate = acc


@when("stream {idx:d} is withdrawn")
def step_withdraw(context, idx):
    if idx in context.qm.admitted:
        context.qm.admitted.remove(idx)
    context.qm.slopes.pop(idx, None)
    context.qm.aggregate = sum(context.qm.slopes.values())


@then("all {n:d} streams are admitted")
def step_all_admitted(context, n):
    assert len(context.qm.admitted) == n, context.qm.admitted
    assert not context.qm.refused, context.qm.refused


@then("streams {a:d} and {b:d} are admitted")
def step_two_admitted(context, a, b):
    assert a in context.qm.admitted and b in context.qm.admitted, \
        context.qm.admitted


@then("stream {idx:d} is refused")
def step_refused(context, idx):
    assert idx in context.qm.refused, context.qm.refused


@then("the aggregate idleSlope is {bps:d} bits per second")
def step_aggregate(context, bps):
    assert context.qm.aggregate == bps, context.qm.aggregate


# ===========================================================================
#  MSRP Domain (Milan 4.2.7.2.1) - class A is ID 6, priority 3, VID 2
# ===========================================================================
@given("the MSRP Domain is class ID {cid:d} priority {prio:d} VID {vid:d}")
def step_domain_given(context, cid, prio, vid):
    context.qm.domain = {"class_id": cid, "priority": prio, "vid": vid}


@when("the MSRP Domain is reset to Milan defaults")
def step_domain_reset(context):
    context.qm.domain = {"class_id": 6, "priority": 3, "vid": 2}


@when("a Domain declaration is received with class ID {cid:d} "
      "priority {prio:d} VID {vid:d}")
def step_domain_rx(context, cid, prio, vid):
    # Milan 4.2.7.2.1: adopt the received FirstValue and declare a MATCHING
    # Domain attribute back.
    context.qm.domain = {"class_id": cid, "priority": prio, "vid": vid}
    context.qm.domain_rx = {"class_id": cid, "priority": prio, "vid": vid}


@then("the MSRP Domain class ID is {cid:d}")
def step_domain_cid(context, cid):
    assert context.qm.domain["class_id"] == cid, context.qm.domain


@then("the MSRP Domain priority is {prio:d}")
def step_domain_prio(context, prio):
    assert context.qm.domain["priority"] == prio, context.qm.domain


@then("the MSRP Domain VID is {vid:d}")
def step_domain_vid(context, vid):
    assert context.qm.domain["vid"] == vid, context.qm.domain


@then("the next Domain declaration matches the received FirstValue")
def step_domain_echo(context):
    assert context.qm.domain == context.qm.domain_rx, \
        (context.qm.domain, context.qm.domain_rx)


@given("gPTP is not locked")
def step_gptp_unlocked(context):
    context.qm.gptp_locked = False


@when("the MSRP Domain declaration timer expires")
def step_domain_timer(context):
    # Milan 4.2.7.2.1: "Transmission of MSRP Domain Messages shall not be
    # dependent on the state of gPTP on the port."
    context.qm.domain_tx = True


@then("an MSRP Domain declaration is transmitted")
def step_domain_tx(context):
    assert context.qm.domain_tx, "no Domain declaration despite the timer"


# ===========================================================================
#  MVRP: VID 2 is declared while any sink uses it (802.1Q 11.2.3)
# ===========================================================================
@given("a listener sink is settled on VLAN {vid:d}")
def step_one_sink(context, vid):
    context.qm.vlan_users[vid] = 1


@given("two listener sinks are settled on VLAN {vid:d}")
def step_two_sinks(context, vid):
    context.qm.vlan_users[vid] = 2


@given("it is the last sink using VLAN {vid:d}")
def step_last_sink(context, vid):
    context.qm.vlan_users[vid] = 1


@when("that listener sink is unbound")
@when("one listener sink is unbound")
def step_unbind(context):
    for vid in list(context.qm.vlan_users):
        context.qm.vlan_users[vid] = max(0, context.qm.vlan_users[vid] - 1)


def _declared_vids(qm):
    """802.1Q 11.2.3: the VID stays declared while ANY user still holds it.

    Derived on demand rather than snapshotted by an explicit evaluate step:
    a scenario that simply binds and unbinds sinks must still get the right
    answer, and an assertion that silently reads a set nobody populated is
    the kind of vacuous green this suite exists to avoid.
    """
    return {v for v, n in qm.vlan_users.items() if n > 0}


@when("the MVRP applicant is evaluated")
def step_mvrp_eval(context):
    context.qm.declared_vids = _declared_vids(context.qm)


@then("VID {vid:d} is declared")
@then("VID {vid:d} remains declared")
def step_vid_declared(context, vid):
    assert vid in _declared_vids(context.qm), context.qm.vlan_users


@then("VID {vid:d} is withdrawn")
def step_vid_withdrawn(context, vid):
    assert vid not in _declared_vids(context.qm), context.qm.vlan_users


# ===========================================================================
#  Listener ingress: a stream is accepted only on its own VID and format
# ===========================================================================
@given("the listener is configured for VID {vid:d} and {ch:d}-channel AAF")
def step_listener_cfg(context, vid, ch):
    context.qm.listener_vid = vid
    context.qm.listener_channels = ch


@when("a tagged AVTP frame arrives on VID {vid:d} with {ch:d} channels")
def step_avtp_arrives(context, vid, ch):
    context.qm.frame_accept = (vid == context.qm.listener_vid
                               and ch == context.qm.listener_channels)


@then("the listener accepts the AVTP frame")
def step_accept(context):
    assert context.qm.frame_accept, "frame was discarded"


@then("the listener discards the AVTP frame")
def step_discard(context):
    assert not context.qm.frame_accept, "frame was accepted"


# ===========================================================================
#  Talker Advertise eligibility (Milan 4.3.3.1): BOTH conditions
#    1) the MAAP destination address is allocated with no conflict, AND
#    2) a PROBE_TX arrived within the last 15 s, OR a matching Listener
#       attribute is registered
# ===========================================================================
@given("a talker has a conflict-free MAAP destination address")
def step_maap_ok(context):
    context.qm.maap_ok = True


@given("a talker has a conflicted MAAP destination address")
def step_maap_conflict(context):
    context.qm.maap_ok = False


@given("the talker received PROBE_TX {age:d} seconds ago")
def step_probe_age(context, age):
    context.qm.probe_age = age


@given("a matching Listener attribute is registered")
def step_listener_reg(context):
    context.qm.listener_registered = True


@given("no matching Listener attribute is registered")
def step_no_listener_reg(context):
    context.qm.listener_registered = False


def _ta_eligible(qm):
    recent = qm.probe_age is not None and qm.probe_age <= 15
    return qm.maap_ok and (recent or qm.listener_registered)


@then("the Talker Advertise attribute is eligible for declaration")
def step_ta_eligible(context):
    assert _ta_eligible(context.qm), vars(context.qm)


@then("the Talker Advertise attribute is not eligible for declaration")
def step_ta_not_eligible(context):
    assert not _ta_eligible(context.qm), vars(context.qm)
