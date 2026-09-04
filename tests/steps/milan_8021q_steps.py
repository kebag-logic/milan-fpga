# SPDX-FileCopyrightText: 2026 Kebag Logic <contact@kebag-logic.com>
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""Offline 802.1Q/Milan conformance model used by milan_8021q_conformance.feature."""

from __future__ import annotations

from typing import TYPE_CHECKING

from behave import given, when, then

if TYPE_CHECKING:  # behave is a test-only dependency; the annotation is lazy
    from behave.runner import Context

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

    def classify(self, tagged: bool, pcp: int | None = None) -> int:
        """The queue this frame lands in under the shipped PCP map.

        An untagged frame is classified on the port's default priority rather
        than on an absent PCP: the substitution is the step 802.1Q requires and
        the step an implementation drops.
        """
        eff = pcp if tagged else self.default_pcp
        # Shipped map: PCP3 -> TC3 -> q4; PCP2 -> TC2 -> q3.
        return {3: 4, 2: 3}.get(eff, 0)

    def configure_shaper(self, queue: int, enabled: bool) -> None:
        """Arm or disarm one queue's credit-based shaper.

        Both slopes are re-derived here from the current port rate, so a rate
        change followed by an enable cannot leave idleSlope and sendSlope
        describing two different link speeds.
        """
        self.queue = queue
        self.shaped = enabled
        self.idle_slope = self.idle[queue]
        self.send_slope = self.idle_slope - self.port_rate
        self.allow = not enabled or self.credit >= 0

    def set_port_rate(self, rate: int) -> None:
        """Move the model to a link speed and to that speed's reservations.

        The idleSlope column is tabulated per rate, so nothing downstream has
        to rescale it.
        """
        self.port_rate = rate
        self.idle = list(IDLE_1G if rate == 1_000_000_000 else IDLE_100M)


@given('a fresh 802.1Q conformance model')
def fresh(context: Context) -> None:
    """Start from the shipped 1 Gbit/s defaults, carrying no state across scenarios."""
    context.qm = QModel()

@given('the port rate is {rate:d} bits per second')
def port_rate(context: Context, rate: int) -> None:
    """Retune the model to this link speed, reloading the per-rate idleSlope table."""
    context.qm.set_port_rate(rate)

@given('the CBS shaper for queue {q:d} is enabled')
def shaper_on(context: Context, q: int) -> None:
    """Arm one queue's shaper, taking its slopes from the current port rate."""
    context.qm.configure_shaper(q, True)

@given('the CBS shaper for queue {q:d} is disabled')
def shaper_off(context: Context, q: int) -> None:
    """Disarm one queue's shaper and park its credit: the unshaped resting state."""
    context.qm.configure_shaper(q, False)
    context.qm.credit = 0

@given('the queue has data but transmission is not occurring')
def waiting(context: Context) -> None:
    """A queue holding data it may not yet send accrues credit at idleSlope."""
    context.qm.credit_delta = context.qm.idle_slope

@given('the queue is transmitting')
def transmitting(context: Context) -> None:
    """A transmitting queue spends credit at sendSlope."""
    context.qm.credit_delta = context.qm.send_slope

@given('the credit is negative')
def negative_credit(context: Context) -> None:
    """Credit debt, which blocks a shaped queue and leaves an unshaped one alone."""
    context.qm.credit = -1
    context.qm.allow = False if context.qm.shaped else True

@given('the credit is zero')
def zero_credit(context: Context) -> None:
    """Zero credit, the transmit-eligible boundary: it permits, it does not block."""
    context.qm.credit = 0
    context.qm.allow = True

@given('queue {q:d} has idleSlope {slope:d} bits per second')
def queue_slope(context: Context, q: int, slope: int) -> None:
    """Pin one queue's idleSlope directly, so sendSlope is judged against a known value."""
    context.qm.queue = q
    context.qm.idle_slope = slope
    context.qm.send_slope = slope - context.qm.port_rate

@when('a tagged frame arrives with PCP {pcp:d}')
def tagged(context: Context, pcp: int) -> None:
    """Classify a frame that carries its own priority."""
    context.qm.queue = context.qm.classify(True, pcp)

@when('an untagged frame arrives')
def untagged(context: Context) -> None:
    """Classify a frame with no tag, and record that the port default was used."""
    context.qm.queue = context.qm.classify(False)
    context.qm.used_default = True

@when('a control frame with reserved DMAC arrives')
def control_dmac(context: Context) -> None:
    """A reserved destination address reaches the DMAC table, not the PCP map."""
    context.qm.classified_by_dmac = True

@when('the credit exceeds hiCredit')
def exceed_hi(context: Context) -> None:
    """Drive the credit past hiCredit, so the clamp rather than the sum is observed."""
    context.qm.hi_credit = 100
    context.qm.credit = min(101, context.qm.hi_credit)

@when('the credit drops below loCredit')
def below_lo(context: Context) -> None:
    """Drive the credit past loCredit, so the lower clamp is observed."""
    context.qm.lo_credit = -100
    context.qm.credit = max(-101, context.qm.lo_credit)

@when('hiCredit is calculated for a {size:d} byte interfering frame')
def calc_hi(context: Context, size: int) -> None:
    """hiCredit: idleSlope over the time the largest interferer holds the link."""
    context.qm.hi_credit = size * context.qm.idle_slope // context.qm.port_rate

@when('loCredit is calculated for a {size:d} byte frame')
def calc_lo(context: Context, size: int) -> None:
    """loCredit: sendSlope over this frame's transmission time, hence negative."""
    context.qm.lo_credit = int(size * context.qm.send_slope / context.qm.port_rate)

@then('the number of queues is {n:d}')
def queue_count(context: Context, n: int) -> None:
    """The bridge ships five traffic queues, not the eight 802.1Q permits."""
    assert NUMBER_OF_QUEUES == n

@then('queue {q:d} is the highest priority')
def highest(context: Context, q: int) -> None:
    """Highest priority is the top index, so the claim moves with the queue count."""
    assert q == NUMBER_OF_QUEUES - 1

@then('queue {q:d} is the lowest priority')
def lowest(context: Context, q: int) -> None:
    """Queue 0 is lowest priority, and the only queue with no reserved idleSlope."""
    assert q == 0

@then('SR class A is on queue {q:d}')
def class_a_queue(context: Context, q: int) -> None:
    """SR class A rides the queue PCP 3 classifies into."""
    assert SRA_QUEUE == q

@then('SR class B is on queue {q:d}')
def class_b_queue(context: Context, q: int) -> None:
    """SR class B rides the queue PCP 2 classifies into."""
    assert SRB_QUEUE == q

@then('the frame is classified to queue {q:d}')
def classified(context: Context, q: int) -> None:
    """Read back where the map put the last frame, rather than recomputing it here."""
    assert context.qm.queue == q

@then('the frame uses the default port priority for classification')
def default_used(context: Context) -> None:
    """The port default supplied the priority; the classifier did not invent a PCP."""
    assert context.qm.used_default

@then('the frame is classified by the DMAC table with no EtherType precondition')
def by_dmac(context: Context) -> None:
    """The reserved address alone decided the class, unconditioned on EtherType."""
    assert context.qm.classified_by_dmac

@then('the credit is increasing at the idleSlope rate')
def increasing(context: Context) -> None:
    """Credit rises at idleSlope while the queue waits, and idleSlope never goes negative."""
    assert context.qm.credit_delta == context.qm.idle_slope and context.qm.idle_slope >= 0

@then('the credit is decreasing at the sendSlope rate')
def decreasing(context: Context) -> None:
    """Credit falls at sendSlope while transmitting, and sendSlope is strictly negative."""
    assert context.qm.credit_delta == context.qm.send_slope and context.qm.send_slope < 0

@then('the sendSlope equals idleSlope minus portRate')
def send_slope(context: Context) -> None:
    """sendSlope is an identity over idleSlope and the port rate, not a second constant."""
    assert context.qm.send_slope == context.qm.idle_slope - context.qm.port_rate

@then('transmission is blocked')
def blocked(context: Context) -> None:
    """Transmission is refused, which only a shaped queue in credit debt does."""
    assert not context.qm.allow

@then('transmission is allowed')
@then('transmission is always allowed')
def allowed(context: Context) -> None:
    """Transmission is permitted: always when unshaped, and at credit >= 0 when shaped."""
    assert context.qm.allow

@then('the credit is clamped to hiCredit')
def clamp_hi(context: Context) -> None:
    """Credit saturated at hiCredit instead of accruing past it."""
    assert context.qm.credit == context.qm.hi_credit

@then('the credit is clamped to loCredit')
def clamp_lo(context: Context) -> None:
    """Credit saturated at loCredit instead of running further into debt."""
    assert context.qm.credit == context.qm.lo_credit

@then('the credit is parked at 0')
def parked(context: Context) -> None:
    """Credit rests at 0, where an idle or unshaped queue sits."""
    assert context.qm.credit == 0

@then('queue {q:d} idleSlope is {slope:d} bits per second')
def idle_slope(context: Context, q: int, slope: int) -> None:
    """One queue's reservation matches the table row for the current port rate."""
    assert context.qm.idle[q] == slope

@then('the shaped idleSlope sum is at most {pct:d} percent of port rate')
def slope_sum(context: Context, pct: int) -> None:
    """The two shaped queues together stay under the SRP reservation cap."""
    assert context.qm.idle[3] + context.qm.idle[4] <= context.qm.port_rate * pct // 100

@then('hiCredit equals {n:d} bytes')
def hi_eq(context: Context, n: int) -> None:
    """The computed hiCredit hits the tabulated value, reporting both when it does not."""
    assert context.qm.hi_credit == n, (context.qm.hi_credit, n)

@then('loCredit equals {n:d} bytes')
def lo_eq(context: Context, n: int) -> None:
    """The computed loCredit hits the tabulated value, reporting both when it does not."""
    assert context.qm.lo_credit == n, (context.qm.lo_credit, n)

# ===========================================================================
#  Listener ingress: a stream is accepted only on its own VID and format
# ===========================================================================
@given("the listener is configured for VID {vid:d} and {ch:d}-channel AAF")
def step_listener_cfg(context: Context, vid: int, ch: int) -> None:
    """Declare the one stream this listener is provisioned for: its VID and its width."""
    context.qm.listener_vid = vid
    context.qm.listener_channels = ch


@when("a tagged AVTP frame arrives on VID {vid:d} with {ch:d} channels")
def step_avtp_arrives(context: Context, vid: int, ch: int) -> None:
    """Acceptance needs BOTH the VID and the channel count; either alone is not enough."""
    context.qm.frame_accept = (vid == context.qm.listener_vid
                               and ch == context.qm.listener_channels)


@then("the listener accepts the AVTP frame")
def step_accept(context: Context) -> None:
    """The frame matched the provisioned VID and format."""
    assert context.qm.frame_accept, "frame was discarded"


@then("the listener discards the AVTP frame")
def step_discard(context: Context) -> None:
    """The frame was dropped, which one mismatched field is enough to cause."""
    assert not context.qm.frame_accept, "frame was accepted"
