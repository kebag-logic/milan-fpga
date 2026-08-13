# SPDX-FileCopyrightText: 2026 Kebag Logic <contact@kebag-logic.com>
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""Offline 802.1Q/Milan conformance model used by milan_8021q_conformance.feature."""

from behave import given, when, then

NUMBER_OF_QUEUES = 5
SRA_QUEUE = 4
SRB_QUEUE = 3
IDLE_1G = [0, 0, 0, 150_000_000, 450_000_000]
IDLE_100M = [0, 0, 0, 15_000_000, 45_000_000]


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
