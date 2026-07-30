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


@then("a push is owed for stream info, counters, interface counters and SET replay")
def step_queues(context):
    for q in ("unsol_pend_r", "unsol_pend2_r", "unsol_pend3_r", "unsol_pend4_r"):
        assert q in context.rb, "missing push queue %s" % q


@then("the STREAM_INPUT counter push is gated on a changed counter")
def step_dirty(context):
    assert re.search(r"in0_cnt_dirty_p_i\s*\)\s*in0_dirty_r\s*<=\s*1'b1",
                     context.rb), "the push is not gated on a dirty pulse"


@then("the STREAM_INPUT counter push is rate limited to one per second")
def step_rl(context):
    m = re.search(r"in0_rl_ok\s*=\s*\(in0_rl_ms_r\s*>=\s*10'd(\d+)\)", context.rb)
    assert m, "no rate limiter on the STREAM_INPUT push"
    assert int(m.group(1)) == 1000, "limiter is %s ms, Milan 5.4.5 says 1 s" % m.group(1)


# ---- the acceptance tests for the per-sink fix (currently @wip) ------------
@then("the STREAM_INPUT dirty flag is per sink, not a single index-0 scalar")
def step_dirty_per_sink(context):
    m = re.search(r"logic\s*(\[[^\]]*\])?\s*in0_dirty_r\s*;", context.rb)
    assert m, "in0_dirty_r not found"
    assert m.group(1), (
        "in0_dirty_r is a SCALAR: only stream input 0 can ever raise an "
        "unsolicited counter push, so sinks 1..N-1 are silent (Milan 5.4.5 "
        "rate-limits PER DESCRIPTOR, implying one per sink)")


@then("the STREAM_INPUT rate limiter is per sink, not a single index-0 scalar")
def step_rl_per_sink(context):
    m = re.search(r"logic\s*\[9:0\]\s*in0_rl_ms_r\s*;", context.rb)
    assert not m, (
        "in0_rl_ms_r is a single 10-bit counter: the 1 s window is shared "
        "across every sink instead of being per descriptor")
