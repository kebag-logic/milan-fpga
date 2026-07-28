# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
#
# Offline models for tests/features/clkv_tu_lease.feature.
#
# TWO models, because the AVTP tu bit has two owners and the 2026-07-28
# defect lived in the seam between them:
#
#   TuEngine     mirrors hdl/ieee8021as/ptp_timestamp/KL_ptp_clock_validity.sv
#                - the fabric verdict, its lease countdown, its discontinuity
#                  holdover and its Milan Table 5.4 observation-interval
#                  counter.  Kept deliberately structural (one step() per
#                  quarter-tick) so it mirrors p_lease / p_hold / p_ival
#                  rather than restating their conclusions.
#
#   LeasePolicy  mirrors the decision table in gptp2csr.sh (milan-tests-avb
#                fpga/tools/gptp2csr.sh) - which ptp4l states justify writing
#                CLKV_CTRL[0] = 1.  This is the part that did not exist until
#                2026-07-28 and is why both boards emitted tu = 1 from boot
#                while being perfectly synchronised.
#
# The models are independent of each other and are wired together only in
# the two end-to-end scenarios, which is where the real defect was visible.

from behave import given, when, then   # noqa: F401  (behave injects these)


# ---------------------------------------------------------------------------
#  Fabric verdict - KL_ptp_clock_validity
# ---------------------------------------------------------------------------
class TuEngine:
    """One quarter-tick per step(). IVAL_Q quarter-ticks = one Milan Table 5.4
    observation interval (4 => 1.000 s, the largest Milan allows)."""

    IVAL_Q = 4
    HOLD_Q = 2          # HOLD_QTICK_P: 0.25..0.5 s, Milan v1.2 Annex B.1.1

    def __init__(self):
        self.sync_ok = False
        self.lease = 0
        self.no_lease = True
        self.hold = 0
        self.gm_id = 0
        self._ival = 0
        self._tu_seen = False
        self.tucnt = 0

    # -- CSR CLKV_CTRL 0x778 -------------------------------------------------
    def write_ctrl(self, sync_ok, wdog_q, disc=False):
        # RTL: sync_ok_r <= sw_sync_ok_i & (|sw_wdog_q_i)
        self.sync_ok = bool(sync_ok) and wdog_q != 0
        self.lease = wdog_q
        self.no_lease = (wdog_q == 0)
        if disc:
            self.hold = self.HOLD_Q

    # -- fabric-observed discontinuities -------------------------------------
    def phc_step(self):
        self.hold = self.HOLD_Q

    def publish_gm(self, gm_id):
        if gm_id != self.gm_id:
            self.hold = self.HOLD_Q
        self.gm_id = gm_id

    # -- the verdict ---------------------------------------------------------
    @property
    def tu(self):
        return 0 if (self.sync_ok and self.hold == 0) else 1

    @property
    def stat(self):
        return ((self.lease & 0xFFF) << 4) | ((1 if self.hold else 0) << 3) \
             | ((1 if self.no_lease else 0) << 2) \
             | ((1 if self.sync_ok else 0) << 1) | self.tu

    def step(self, n=1):
        """Advance n quarter-ticks."""
        for _ in range(n):
            if self.tu:
                self._tu_seen = True
            if self.lease:
                self.lease -= 1
                if self.lease == 0:
                    self.sync_ok = False
                    self.no_lease = True
            if self.hold:
                self.hold -= 1
            self._ival += 1
            if self._ival == self.IVAL_Q:
                self._ival = 0
                if self._tu_seen or self.tu:
                    self.tucnt += 1
                self._tu_seen = False


# ---------------------------------------------------------------------------
#  Software lease policy - gptp2csr.sh
# ---------------------------------------------------------------------------
class LeasePolicy:
    """Milan v1.2 4.4.2.1 derives Listener buffering from '... + 1 us (gPTP
    accuracy)', so 1000 ns is the budget the rest of the spec assumes."""

    def __init__(self, offset_ns=1000, lock_n=3):
        self.offset_ns = offset_ns
        self.lock_n = lock_n
        self.good_run = 0
        self.reason = "not-synchronised"

    def sample(self, port_state, gm_present, gm_identity,
               local_identity, master_offset):
        """One iteration of the daemon loop. Returns the sync_ok it would
        write. Every unparsable/unknown input falls through to False: the
        loop fails CLOSED."""
        ok = False
        if port_state == "SLAVE":
            if gm_present and master_offset is not None:
                if abs(master_offset) <= self.offset_ns:
                    ok, self.reason = True, "slave locked, offset %s ns" % master_offset
                else:
                    self.reason = ("slave but offset %s ns > %s ns"
                                   % (master_offset, self.offset_ns))
            else:
                self.reason = "portState SLAVE but no grandmaster reported"
        elif port_state in ("MASTER", "GRAND_MASTER"):
            # Our PHC DEFINES gPTP time rather than approximating it, so
            # 1722 4.4.4.7's "may not correspond to gPTP time" cannot apply.
            # Gated on portState: LISTENING/PRE_MASTER also report
            # gmPresent=false and are NOT yet a grandmaster.
            if not gm_present and gm_identity == local_identity:
                ok, self.reason = True, "grandmaster (own clockIdentity)"
            else:
                self.reason = "portState MASTER but grandmaster is %s" % gm_identity
        else:
            self.reason = "portState %s" % (port_state or "<no reply from ptp4l>")

        self.good_run = self.good_run + 1 if ok else 0
        # Claiming health is harder than losing it.
        return ok and self.good_run >= self.lock_n


# ---------------------------------------------------------------------------
#  Steps
# ---------------------------------------------------------------------------
LOCAL_CI = "020000fffe000002"


@given('a clock-validity engine with a {n:d}-quarter-tick observation interval')
def step_engine(context, n):
    context.eng = TuEngine()
    assert context.eng.IVAL_Q == n
    context.pol = LeasePolicy()
    context.port_state = None
    context.gm_present = False
    context.gm_identity = None
    context.master_offset = None
    context.tucnt_mark = 0
    context.claim = None
    context.last_claim = None
    context.daemon_alive = True


@when('nothing has ever written CLKV_CTRL')
def step_nothing(context):
    pass                                   # reset state is the whole point


@when('software leases the sync claim with sync_ok {s:d} and a lease of {q:d} quarter-seconds')
def step_lease(context, s, q):
    context.eng.write_ctrl(s, q)


@when('{n:d} quarter-ticks elapse with no further CLKV_CTRL write')
@when('{n:d} quarter-ticks elapse')
def step_elapse(context, n):
    context.tucnt_mark = context.eng.tucnt
    context.eng.step(n)


@when('software renews a {q:d}-quarter-second lease every {every:d} quarter-ticks for {total:d} quarter-ticks')
def step_renew(context, q, every, total):
    context.eng.write_ctrl(1, q)
    for _ in range(total // every):
        context.eng.step(every)
        context.eng.write_ctrl(1, q)


@given('software holds a long-lived sync claim')
def step_longlease(context):
    context.eng.write_ctrl(1, 4000)
    context.eng.step(1)                    # settle past any startup holdover
    context.eng.hold = 0
    assert context.eng.tu == 0, "precondition: tu must be clear before the event"


@when('the published grandmaster identity changes to {gm}')
def step_gm_change(context, gm):
    context.eng.publish_gm(int(gm, 16))


@when('the fabric observes a {event}')
def step_phc(context, event):
    assert event in ("settime", "adjtime")
    context.eng.phc_step()


@then('tu stays asserted for at least {n:d} quarter-tick')
@then('tu stays asserted for at least {n:d} quarter-ticks')
def step_tu_held(context, n):
    for i in range(n):
        assert context.eng.tu == 1, "tu dropped after %d quarter-ticks" % i
        context.eng.step(1)


@then('the tu bit is {v:d}')
@when('the tu bit is {v:d}')
def step_tu(context, v):
    assert context.eng.tu == v, \
        "tu = %d, expected %d (CLKV_STAT=0x%X)" % (context.eng.tu, v, context.eng.stat)


@then('CLKV_STAT reports no live lease')
def step_stat_nolease(context):
    assert (context.eng.stat >> 2) & 1 == 1, "CLKV_STAT=0x%X" % context.eng.stat


@then('CLKV_STAT reports sync_ok set')
def step_stat_sync(context):
    assert (context.eng.stat >> 1) & 1 == 1, "CLKV_STAT=0x%X" % context.eng.stat


@then('CLKV_STAT reports sync_ok clear')
def step_stat_nosync(context):
    assert (context.eng.stat >> 1) & 1 == 0, "CLKV_STAT=0x%X" % context.eng.stat


@then('CLKV_STAT reports a holdover in progress')
def step_stat_hold(context):
    assert (context.eng.stat >> 3) & 1 == 1, "CLKV_STAT=0x%X" % context.eng.stat


@then('CLKV_TUCNT did not move')
def step_tucnt_frozen(context):
    d = context.eng.tucnt - context.tucnt_mark
    assert d == 0, "CLKV_TUCNT advanced by %d on a healthy clock" % d


@then('CLKV_TUCNT advanced by {n:d}')
def step_tucnt_adv(context, n):
    d = context.eng.tucnt - context.tucnt_mark
    assert d == n, "CLKV_TUCNT advanced by %d, expected %d" % (d, n)


# -- policy steps -----------------------------------------------------------
@given('ptp4l reports portState {state} with a grandmaster present')
def step_slave(context, state):
    context.port_state = state
    context.gm_present = True
    context.gm_identity = "020000fffe000001"


@given('ptp4l reports portState {state} with no grandmaster present')
def step_master(context, state):
    context.port_state = state
    context.gm_present = False
    context.gm_identity = LOCAL_CI


@given('the reported grandmaster identity is our own clockIdentity')
def step_gm_is_us(context):
    context.gm_identity = LOCAL_CI


@given('the servo reports a master_offset of {off:d} ns')
def step_offset(context, off):
    context.master_offset = off


@given('pmc returns nothing at all')
def step_pmc_dead(context):
    context.port_state = None
    context.gm_present = False
    context.gm_identity = None
    context.master_offset = None


def _sample(context, n=1):
    for _ in range(n):
        context.claim = context.pol.sample(
            context.port_state, context.gm_present, context.gm_identity,
            LOCAL_CI, context.master_offset)
    return context.claim


@when('the policy has seen {n:d} consecutive good sample')
@when('the policy has seen {n:d} consecutive good samples')
def step_n_samples(context, n):
    context.pol.good_run = 0
    _sample(context, n)


@when('one bad sample arrives')
def step_bad_sample(context):
    context.master_offset = 216446000000000
    _sample(context, 1)


@then('the lease policy claims sync')
def step_claims(context):
    got = context.claim if context.claim is not None else _sample(context, context.pol.lock_n)
    assert got is True, "policy refused to claim: %s" % context.pol.reason


@then('the lease policy refuses to claim')
def step_refuses(context):
    got = context.claim if context.claim is not None else _sample(context, context.pol.lock_n)
    assert got is False, "policy claimed sync when it must not (%s)" % context.pol.reason


@then('the reason mentions the offset')
def step_reason(context):
    assert "offset" in context.pol.reason, context.pol.reason


# -- end to end -------------------------------------------------------------
@when('the daemon runs for {n:d} quarter-ticks')
def step_daemon_runs(context, n):
    """One daemon iteration every 8 quarter-ticks (POLL=2 s), each renewing an
    8 s = 32 quarter-tick lease.  It therefore takes LOCK_N iterations - 24
    quarter-ticks - before the claim is asserted at all, which is the
    behaviour, not an artefact: claiming health is deliberately slow.
    The rising edge also sets CLKV_CTRL[1], the W1S discontinuity report that
    holds tu for a further 0.25-0.5 s (Milan v1.2 Annex B.1.1), so tu only
    goes clear once that holdover has also elapsed."""
    context.daemon_alive = True
    for i in range(n):
        if i % 8 == 0 and context.daemon_alive:
            claim = context.pol.sample(context.port_state, context.gm_present,
                                       context.gm_identity, LOCAL_CI,
                                       context.master_offset)
            disc = claim and context.last_claim is not True
            context.eng.write_ctrl(1 if claim else 0, 32, disc=disc)
            context.last_claim = claim
        context.eng.step(1)
    context.tucnt_mark = context.eng.tucnt


@when('the daemon is killed')
def step_daemon_killed(context):
    context.daemon_alive = False
    context.tucnt_mark = context.eng.tucnt


@then('CLKV_TUCNT did not move over the last {n:d} quarter-ticks')
def step_tucnt_frozen_window(context, n):
    mark = context.eng.tucnt
    context.eng.step(n)
    d = context.eng.tucnt - mark
    assert d == 0, "CLKV_TUCNT advanced by %d while the daemon was healthy" % d


@then('CLKV_TUCNT advanced over the last {n:d} quarter-ticks')
def step_tucnt_moved_window(context, n):
    mark = context.eng.tucnt
    context.eng.step(n)
    d = context.eng.tucnt - mark
    assert d > 0, "CLKV_TUCNT frozen after the daemon died - tu is not being counted"
