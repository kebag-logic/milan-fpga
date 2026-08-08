# SPDX-FileCopyrightText: 2026 Kebag Logic <contact@kebag-logic.com>
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""Unsolicited-notification guards, read out of the RTL (never transcribed)."""

import os
import re

from behave import given, then

_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
_RB = os.path.join(_ROOT, "hdl", "ieee17221", "aecp",
                   "KL_aecp_response_builder.sv")


def _strip(src):
    src = re.sub(r"/\*.*?\*/", "", src, flags=re.S)
    return re.sub(r"//[^\n]*", "", src)


@given("the AECP response builder RTL")
def step_rb(context):
    context.rb_raw = open(_RB).read()
    context.rb = _strip(context.rb_raw)


@then("REGISTER and DEREGISTER_UNSOLICITED_NOTIFICATION are handled")
def step_reg(context):
    pkg = open(os.path.join(_ROOT, "hdl", "ieee17221", "aecp",
                            "aecp_pkg.sv")).read()
    for c in ("CMD_REGISTER_UNSOLICITED_NOTIFICATION",
              "CMD_DEREGISTER_UNSOLICITED_NOTIFICATION"):
        assert c in pkg, c
    assert "unsol_valid_r" in context.rb, "no registration table"


@then("a push is owed for stream info, input counters, interface counters and SET replay")
def step_queues(context):
    # the surviving class family after gh #60 F2/F3: the legacy stream-0-only
    # counters queue (unsol_pend2_r) is RETIRED - sink 0 rides bit 0 of the
    # per-sink class, the CRF sink its own scalar class
    for q in ("unsol_pend_r", "unsol_pend3_r", "unsol_pend4_r",
              "unsol_pend10_r", "unsol_pend11_r"):
        assert q in context.rb, "missing push queue %s" % q
    assert "unsol_pend2_r" not in context.rb, (
        "the retired stream-0-only counters queue is back: its payload read "
        "the in0_* legacy ports, which the datapath muxes by clock source, "
        "so its push could disagree with the solicited answer (gh #60 F3)")


@then("the STREAM_INPUT counter push is gated on a changed counter")
def step_dirty(context):
    assert re.search(r"rxdiag_dirty_p_i\[k\]\s*\)\s*in_dirty_r\[k\]\s*<=\s*1'b1",
                     context.rb), "the push is not gated on a dirty pulse"


@then("the STREAM_INPUT counter push is rate limited to one per second")
def step_rl(context):
    m = re.search(r"w_in_rl_ok\[k\]\s*=\s*\(in_rl_ms_r\[k\]\s*>=\s*10'd(\d+)\)",
                  context.rb)
    assert m, "no rate limiter on the STREAM_INPUT push"
    assert int(m.group(1)) == 1000, "limiter is %s ms, Milan 5.4.5 says 1 s" % m.group(1)


# ---- the per-sink law (gh #60 F2 landed the fix these once prescribed) -----
@then("the STREAM_INPUT dirty flag is per sink, not a single index-0 scalar")
def step_dirty_per_sink(context):
    m = re.search(r"logic\s*(\[[^\]]*\])?\s*in_dirty_r\s*;", context.rb)
    assert m, "in_dirty_r not found"
    assert m.group(1), (
        "in_dirty_r is a SCALAR: only stream input 0 can ever raise an "
        "unsolicited counter push, so sinks 1..N-1 are silent (Milan 5.4.5 "
        "rate-limits PER DESCRIPTOR, implying one per sink)")


@then("the STREAM_INPUT rate limiter is per sink, not a single index-0 scalar")
def step_rl_per_sink(context):
    assert re.search(r"logic\s*\[9:0\]\s*in_rl_ms_r\s*\[RXD_MAX_C\]\s*;",
                     context.rb), (
        "in_rl_ms_r is not a per-descriptor window array: the 1 s window "
        "would be shared across every sink instead of being per descriptor")


@then("the CRF Media Clock Input has its own counter push class")
def step_crf_class(context):
    # its own descriptor (index n_aaf_sinks_i) => its own dirty + window
    assert re.search(r"crf_cnt_dirty_p_i\s*\)\s*crfcnt_dirty_r\s*<=\s*1'b1",
                     context.rb), "no CRF dirty gate"
    assert re.search(r"w_crfcnt_rl_ok\s*=\s*\(crfcnt_rl_ms_r\s*>=\s*10'd1000\)",
                     context.rb), "no CRF 1 s window"


@then("a push is owed for the lock auto-expiry")
def step_lock_queue(context):
    assert "unsol_pend12_r" in context.rb, "no lock-expiry push queue"
    assert re.search(r"if \(lock_expired_p_i\)", context.rb), (
        "the lock-expiry queue is not armed from the L0 pulse")


@then("the lock expiry pulse fires only from the countdown")
def step_lock_pulse(context):
    l0 = _strip(open(os.path.join(_ROOT, "hdl", "ieee17221", "aecp",
                                  "KL_aecp_l0_state.sv")).read())
    sets = re.findall(r"lock_expired_p_o\s*<=\s*1'b1", l0)
    assert len(sets) == 1, (
        "lock_expired_p_o has %d set sites; the Milan 5.4.2.2 note names the "
        "AUTOMATIC unlock alone, so only the countdown may pulse" % len(sets))
    expiry = l0[l0.index("lock_timer_r == 17'd0"):]
    assert re.search(r"lock_expired_p_o\s*<=\s*1'b1", expiry[:400]), (
        "the single pulse site is not inside the timer-expiry branch")
