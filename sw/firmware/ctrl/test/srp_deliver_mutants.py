# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""Planted defects of the SRP delivery's bound (#977, its ruling on round 9's STOP, item 2).

A delivery (ctrl_app_srp.c deliver) makes at most one binding change and, outside THE SETTLE, at most one loss
completion, each the first owed from its turn, the sink after the last it made, and where both are owed only the kind
the last delivery did not make; the rest stay pending, keep the loop awake and are delivered in turn, so each waits at
most 2 x n_sinks deliveries. THE SETTLE still completes every loss it owes. One defect a rule: every owed change made
at once, the turn taken from the first sink, every loss completed at once, a binding change made beside a loss, an owed
loss or an owed change leaving the loop asleep, and THE SETTLE completing none. srp_mutants.py plants each with the
rest of its table; each named test (srp_binding.hpp, D1 to D5) must fail on its own words.
"""
from __future__ import annotations

from typing import Callable, TypeVar

T = TypeVar("T")


def defects(kind: Callable[..., T]) -> tuple[T, ...]:
    """Every defect of the bound, built with srp_mutants.Defect."""
    return (
        kind('deliver-binds-every-owed', 'SrpBinding.D1ADeliveryMakesOneBindingChangeTheRestInTurn',
             '        if (r->pending && sink == bind) {\n', '        if (r->pending) {\n',
             'D1 one binding change a delivery', path='app/ctrl_app_srp.c', suite='test_acmp_mbx.cpp'),
        kind('deliver-bind-turn-from-the-first',
             'SrpBinding.D2ASinkOwedIsDeliveredWithinItsTurnWhateverAnotherOwesAgain',
             'const unsigned k = (app->srp_bind_turn + step) % n;', 'const unsigned k = step % n;',
             'D2 a sink owed waits at most n_sinks deliveries', path='app/ctrl_app_srp.c', suite='test_acmp_mbx.cpp'),
        kind('deliver-completes-every-loss', 'SrpBinding.D3ADeliveryCompletesOneLossOutsideTheSettle',
             'complete(app,sink,interface,sink == lose);', 'complete(app,sink,interface,true);',
             'D3 one loss completion a delivery outside THE SETTLE', path='app/ctrl_app_srp.c',
             suite='test_acmp_mbx.cpp'),
        kind('deliver-binds-beside-a-loss', 'SrpBinding.D3ADeliveryCompletesOneLossOutsideTheSettle',
             '    if (bind < n && lose < n) {\n', '    if (false) {\n',
             'D3 one of a binding change and a loss completion a delivery', path='app/ctrl_app_srp.c',
             suite='test_acmp_mbx.cpp'),
        kind('deliver-owed-loss-sleeps', 'SrpBinding.D5ALossLeftOwedKeepsTheLoopAwakeWithNoChangeOwed',
             'pending = r->pending || (delivered(r) && s->withdrawn) || pending;', 'pending = r->pending || pending;',
             'D5 a loss left owed keeps the loop awake', path='app/ctrl_app_srp.c',
             suite='test_acmp_mbx.cpp'),
        kind('deliver-owed-change-sleeps', 'SrpBinding.D1ADeliveryMakesOneBindingChangeTheRestInTurn',
             'pending = r->pending || (delivered(r) && s->withdrawn) || pending;',
             'pending = (delivered(r) && s->withdrawn) || pending;',
             'D1 a delivery that leaves a change owed keeps the loop awake', path='app/ctrl_app_srp.c',
             suite='test_acmp_mbx.cpp'),
        kind('settle-completes-no-loss', 'SrpBinding.D4TheSettleCompletesEveryLoss',
             'complete(app,sink,app->acmp.acmp.cfg.sink_interface[sink],true);',
             'complete(app,sink,app->acmp.acmp.cfg.sink_interface[sink],false);',
             'D4 THE SETTLE completes every loss it owes', path='app/ctrl_app_srp.c', suite='test_acmp_mbx.cpp'),
    )
