# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
#
# Executable model of the announce-receipt half of the IEEE 802.1AS-2020 BMCA,
# plus the message-cadence budget that keeps the BMCA from ever being provoked.
#
# WHY A MODEL AND NOT A WIRE TEST. The wire half of this property needs the
# bench (two boards, a switch and a saturating load generator) and cannot run
# in CI. What CAN run in CI is the rule that turns an observed cadence into a
# verdict - and that rule is the thing that was missing when defect D7 ("the
# gPTP GM changed for no reason") went unreproduced for a day. The scenarios
# feed it REAL `pmc GET PORT_STATS_NP` deltas measured on 2026-07-28, one
# window that holds and one that breaks, so the check has a negative control
# and is not a tautology (methodology R2).
#
# The hardware acceptance procedure that produced those numbers is in
# docs/findings/GPTP_GM_LOSS_UNDER_RX_LOAD.md.

from __future__ import annotations

from typing import TYPE_CHECKING

from behave import given, when, then

if TYPE_CHECKING:  # behave is a test-only dependency; the annotation is lazy
    from behave.runner import Context


# --- IEEE 802.1AS-2020 defaults (Clause 10.6 intervals, Clause 10.3 BMCA) ---
# These are also exactly what Milan v1.2 4.2.6.2 requires of a PAAD.
DEFAULT_LOG_ANNOUNCE_INTERVAL = 0     # -> 1 Announce/s
DEFAULT_LOG_SYNC_INTERVAL = -3        # -> 8 Sync/s
DEFAULT_LOG_PDELAY_REQ_INTERVAL = 0   # -> 1 Pdelay_Req/s
ANNOUNCE_RECEIPT_TIMEOUT = 3          # announceReceiptTimeoutTime = N x interval
SYNC_RECEIPT_TIMEOUT = 3


def _interval(log_interval):
    """log message interval -> seconds (2**logInterval)."""
    return 2.0 ** log_interval


class Claimant:
    """One device advertising itself as a potential grandmaster."""

    def __init__(self, ident, priority1):
        self.ident = ident
        self.priority1 = priority1
        self.last_announce = None   # None = never announced

    def alive_at(self, now: float, timeout_time: float) -> bool:
        """Whether this claimant's announce information is still valid at `now`.

        A device that has never announced is not a candidate at all, which is
        why the never-announced case is False rather than an age comparison
        against a missing timestamp.
        """
        if self.last_announce is None:
            return False
        return (now - self.last_announce) < timeout_time


class GptpDomain:
    """The announce-receipt half of the BMCA, as a receiver sees it.

    Deliberately NOT a full BMCA: the dataset comparison here is priority1 then
    clockIdentity, which is the only part of Clause 10.3's comparison these
    scenarios exercise. Everything else (clockClass, accuracy, variance,
    stepsRemoved) is equal across the bench devices, so modelling it would add
    code that no scenario can distinguish - and an untestable branch is worse
    than an honest omission.
    """

    def __init__(self):
        self.now = 0.0
        self.announce_interval = _interval(DEFAULT_LOG_ANNOUNCE_INTERVAL)
        self.announce_receipt_timeout = ANNOUNCE_RECEIPT_TIMEOUT
        self.claimants = {}
        self.selected = None
        self.changes = 0

    @property
    def timeout_time(self) -> float:
        """announceReceiptTimeoutTime = announceReceiptTimeout x announceInterval."""
        return self.announce_receipt_timeout * self.announce_interval

    def add(self, ident: str, priority1: int) -> None:
        """Admit a claimant to the domain, silent until it first announces."""
        self.claimants[ident] = Claimant(ident, priority1)

    def announce_from(self, ident: str) -> None:
        """Stamp an Announce receipt from `ident` at the current domain time."""
        self.claimants[ident].last_announce = self.now

    def advance(self, seconds: float) -> None:
        """Move the domain clock forward; nothing expires until `reselect`."""
        self.now += seconds

    def reselect(self) -> None:
        """Re-run the selection over claimants whose announce info has not
        expired. Transitioning to a different master counts as a change; the
        FIRST acquisition does not (there was no previous master to change
        from)."""
        alive = [c for c in self.claimants.values()
                 if c.alive_at(self.now, self.timeout_time)]
        best = None
        if alive:
            best = sorted(alive, key=lambda c: (c.priority1, c.ident))[0].ident
        if best != self.selected:
            if self.selected is not None and best is not None:
                self.changes += 1
            self.selected = best


# ----------------------------------------------------------------- steps --

@given('a gPTP port with the 802.1AS default intervals')
def step_default_port(context: Context) -> None:
    """Open a domain at the spec defaults, asserting them so a silent change
    to the constants at the top of this file fails here rather than skewing
    every later verdict."""
    context.gptp = GptpDomain()
    assert context.gptp.announce_interval == 1.0
    assert context.gptp.timeout_time == 3.0


@given('grandmaster "{ident}" with priority1 {prio:d}')
def step_grandmaster(context: Context, ident: str, prio: int) -> None:
    """Seat `ident` as the master the scenario opens with - it announces once
    and is selected immediately, so a later switch away from it is a change
    and not a first acquisition."""
    context.gptp.add(ident, prio)
    context.gptp_gm = ident
    # it is already the master when the scenario opens
    context.gptp.announce_from(ident)
    context.gptp.reselect()


@given('a competing claimant "{ident}" with priority1 {prio:d}')
def step_claimant(context: Context, ident: str, prio: int) -> None:
    """Add the rival that makes the takeover observable: without a second
    announcing device a lost grandmaster leaves nobody to select."""
    context.gptp.add(ident, prio)
    context.gptp_other = ident
    context.gptp.announce_from(ident)
    context.gptp.reselect()


@when('the grandmaster announces every {period:g} s for {span:g} s')
def step_announce_normally(context: Context, period: float, span: float) -> None:
    """Both devices keep announcing - a competing claimant on a real segment
    does not go quiet just because it lost."""
    steps = int(round(span / period))
    for _ in range(steps):
        context.gptp.advance(period)
        context.gptp.announce_from(context.gptp_gm)
        if getattr(context, 'gptp_other', None):
            context.gptp.announce_from(context.gptp_other)
        context.gptp.reselect()


@when('the grandmaster stops announcing for {span:g} s')
def step_announce_gap(context: Context, span: float) -> None:
    """Only the grandmaster goes silent. This is what a saturating RX flood
    does to the board: the control loop never runs, so nothing is transmitted."""
    period = context.gptp.announce_interval
    elapsed = 0.0
    while elapsed < span:
        step = min(period, span - elapsed)
        context.gptp.advance(step)
        elapsed += step
        if getattr(context, 'gptp_other', None):
            context.gptp.announce_from(context.gptp_other)
        context.gptp.reselect()


@then('the selected grandmaster is "{ident}"')
def step_check_selected(context: Context, ident: str) -> None:
    """Name the device the domain should be locked to at the end of the run."""
    assert context.gptp.selected == ident, \
        f"selected grandmaster {context.gptp.selected!r}, expected {ident!r}"


@then('the grandmaster changed {n:d} times')
def step_check_changes(context: Context, n: int) -> None:
    """Pin the number of grandmaster transitions, which is the quantity defect
    D7 was reported against: a domain that ends on the right device having
    flapped on the way there is still a failure."""
    assert context.gptp.changes == n, \
        f"grandmaster changed {context.gptp.changes} times, expected {n}"


# --------------------------------------------------- cadence budget rule --
#
# WHAT THIS RULE CAN AND CANNOT PROVE. A count over a window does not show
# where the gaps were. The half that IS rigorous is the sufficient direction:
# a receipt timeout needs `timeout` CONSECUTIVE missing messages, so losing
# fewer than `timeout` messages in the whole window cannot produce one. The
# budget therefore certifies safety when the shortfall is <= timeout-1, and
# refuses to certify beyond that - it does not claim a timeout definitely
# happened. Stated plainly so nobody reads "breaks" as "a timeout occurred".

def _budget(delivered, window_s, interval_s, timeout):
    expected = int(window_s / interval_s)
    allowed_short = timeout - 1
    return delivered, expected, (delivered >= expected - allowed_short)


def _check(context, kind, interval_s, timeout, verdict):
    delivered, expected, ok = _budget(
        context.gptp_observed, context.gptp_window, interval_s, timeout)
    short = expected - delivered
    if verdict == 'holds':
        assert ok, (f"{kind} cadence budget should hold: {delivered} delivered, "
                    f"{expected} due over {context.gptp_window} s "
                    f"(short {short}, allowed {timeout - 1})")
    elif verdict == 'breaks':
        assert not ok, (f"{kind} cadence budget should break: {delivered} delivered, "
                        f"{expected} due over {context.gptp_window} s "
                        f"(short {short}, allowed {timeout - 1})")
    else:
        raise AssertionError(f"unknown verdict {verdict!r}")


@when('{sent:d} Announce messages are observed over {window:g} s')
def step_obs_announce(context: Context, sent: int, window: float) -> None:
    """Record a measured Announce count and its window. Recording is all a
    When does here - the budget rule that turns it into a verdict is the Then,
    so one measurement can be asked to hold or to break."""
    context.gptp_observed, context.gptp_window = sent, window


@when('{sent:d} Sync messages are observed over {window:g} s')
def step_obs_sync(context: Context, sent: int, window: float) -> None:
    """Record a measured Sync count and its window; Sync is due eight times
    per second, so the same shortfall costs far more of its budget."""
    context.gptp_observed, context.gptp_window = sent, window


@when('{sent:d} Pdelay_Req messages are observed over {window:g} s')
def step_obs_pdelay(context: Context, sent: int, window: float) -> None:
    """Record a measured Pdelay_Req count and its window - the exchange whose
    starvation costs the port asCapable rather than the grandmaster."""
    context.gptp_observed, context.gptp_window = sent, window


@then('the announce cadence budget {verdict}')
def step_budget_announce(context: Context, verdict: str) -> None:
    """Grade the recorded Announce count against announceReceiptTimeout: a
    shortfall under the timeout cannot have produced a receipt timeout."""
    _check(context, 'announce', _interval(DEFAULT_LOG_ANNOUNCE_INTERVAL),
           ANNOUNCE_RECEIPT_TIMEOUT, verdict)


@then('the sync cadence budget {verdict}')
def step_budget_sync(context: Context, verdict: str) -> None:
    """Grade the recorded Sync count against syncReceiptTimeout, at the 8/s
    interval that makes the same absolute loss a much larger shortfall."""
    _check(context, 'sync', _interval(DEFAULT_LOG_SYNC_INTERVAL),
           SYNC_RECEIPT_TIMEOUT, verdict)


@then('the pdelay cadence budget {verdict}')
def step_budget_pdelay(context: Context, verdict: str) -> None:
    """Grade the recorded Pdelay_Req count; the failure it guards is the port
    losing asCapable, not the domain choosing a different grandmaster."""
    # asCapable depends on the pdelay exchange continuing; the peer drops
    # asCapable after `neighborPropDelayThresh`/missed-response handling, and
    # a port that is not asCapable leaves the domain (Clause 11.2 / AS-8).
    _check(context, 'pdelay', _interval(DEFAULT_LOG_PDELAY_REQ_INTERVAL),
           ANNOUNCE_RECEIPT_TIMEOUT, verdict)
