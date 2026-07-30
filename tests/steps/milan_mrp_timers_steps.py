# SPDX-FileCopyrightText: 2026 Kebag Logic <contact@kebag-logic.com>
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""Milan MRP timer + instantaneous-Leave guards (4.2.7.1.1 / 4.2.7.2.2).

Every value here is READ OUT OF THE RTL. A transcribed constant cannot fail:
it agrees with whatever it was copied from and then drifts in silence, which
is exactly how a LeaveTime a factor of 8 below Milan's floor survived in the
tree with a comment cheerfully citing the wrong table.
"""

import os
import re

from behave import given, when, then

_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
_SRP = os.path.join(_ROOT, "hdl", "ieee8021q", "srp")
_PKG = os.path.join(_SRP, "lwsrp_pkg.sv")
_REGISTRAR = os.path.join(_SRP, "KL_lwsrp_registrar.sv")
_CTX = os.path.join(_SRP, "KL_lwsrp_ctx.sv")


def _strip(src):
    src = re.sub(r"/\*.*?\*/", "", src, flags=re.S)
    return re.sub(r"//[^\n]*", "", src)


def _pkg_ms(name):
    m = re.search(r"%s\s*=\s*([0-9_]+)\s*;" % name, open(_PKG).read())
    assert m, "no %s in %s" % (name, _PKG)
    return int(m.group(1).replace("_", ""))


@given("the MRP timers the lwSRP package elaborates")
def step_pkg_timers(context):
    context.timers = {
        "join": _pkg_ms("JOIN_TIME_MS_C"),
        "leave": _pkg_ms("LEAVE_TIME_MS_C"),
        "leaveall": _pkg_ms("LEAVEALL_TIME_MS_C"),
    }


@then("the JoinTime is between {lo:d} and {hi:d} ms")
def step_join(context, lo, hi):
    v = context.timers["join"]
    assert lo <= v <= hi, "JoinTime %d outside Milan [%d,%d]" % (v, lo, hi)


@then("the LeaveTime is between {lo:d} and {hi:d} ms")
def step_leave(context, lo, hi):
    v = context.timers["leave"]
    assert lo <= v <= hi, (
        "LeaveTime %d ms is outside Milan Table 4.3 [%d,%d] - the 802.1Q "
        "Table 10-7 base value (600-1000 ms) is NOT conformant for a PAAD"
        % (v, lo, hi))


@then("the LeaveAll time is between {lo:d} and {hi:d} ms")
def step_leaveall(context, lo, hi):
    v = context.timers["leaveall"]
    assert lo <= v <= hi, "LeaveAllTime %d outside Milan [%d,%d]" % (v, lo, hi)


@given("an MSRP Registrar is in state IN")
def step_registrar_in(context):
    context.reg_src = _strip(open(_REGISTRAR).read())
    context.ctx_src = _strip(open(_CTX).read())


@when("an MSRP Leave event is received")
def step_registrar_rlv(context):
    # the arm guarded by the explicit LV event ALONE; a LeaveAll has its own
    # arm and must keep its timer, which is what the clause leaves alone.
    m = re.search(
        r"lstn_lv_evt_w\s*&&\s*listener_reg_o\s*\)\s*begin(.*?)end\s+else",
        context.reg_src, flags=re.S)
    assert m, "no explicit-rLv arm in KL_lwsrp_registrar"
    context.rlv_arm = " ".join(m.group(1).split())


@then("the Registrar deregisters immediately")
def step_registrar_mt(context):
    assert "listener_reg_o <= 1'b0" in context.rlv_arm, context.rlv_arm


@then("the explicit-Leave path does not arm the LeaveTime timer")
def step_registrar_no_timer(context):
    assert "LEAVE_TIME_MS_C" not in context.rlv_arm, context.rlv_arm
    assert "lstn_leave_r <= '0" in context.rlv_arm, context.rlv_arm


@then("no per-lane Registrar arms the LeaveTime timer on an explicit Leave")
def step_ctx_lanes(context):
    # the context table carries the same registrar per lane, in BOTH
    # directions (talker-dir Listener attribute, listener-dir TA/TF). Every
    # explicit-Leave arm must be instantaneous too.
    arms = re.findall(r"lv_w\[l\]\s*&&\s*\w+_r\[l\]\s*\)\s*begin(.*?)end",
                      context.ctx_src, flags=re.S)
    assert arms, "no per-lane rLv arms found in KL_lwsrp_ctx"
    for arm in arms:
        body = " ".join(arm.split())
        assert "LEAVE_TIME_MS_C" not in body, (
            "a per-lane rLv still arms the leave timer: %s" % body)


# The 802.1Q conformance feature words the same two assertions differently;
# both phrasings ride the SAME registrar read, so the two features cannot
# drift into disagreeing about what 4.2.7.2.2 requires.
@then("the MSRP Registrar state is MT")
def step_registrar_state_mt(context):
    step_registrar_mt(context)


@then("no LeaveTime wait is required")
def step_registrar_no_wait_alias(context):
    step_registrar_no_timer(context)
