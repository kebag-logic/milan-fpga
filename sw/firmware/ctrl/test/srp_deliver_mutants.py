# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""Planted defects of the SRP delivery's bound (#977, its ruling of 2026-11-27 on the delivery bound, item 2).

A delivery (ctrl_app_srp.c deliver) makes at most one binding change and, outside THE SETTLE, at most one loss
completion, each the first owed from its turn, the sink after the last it made, and where both are owed only the kind
the last delivery did not make; the rest stay pending, keep the loop awake and are delivered in turn, so each waits at
most 2 x n_sinks deliveries of passes that took no SRP record: a pass that carries a record alone makes no binding
change (its ruling of 2026-11-27 on the alone records, item 4). THE SETTLE still completes every loss it owes. One
defect a rule: every owed change made at once, the turn taken from the first sink, every loss completed at once, a
binding change made beside a loss, a binding change made again where both are owed after one, the loss turn taken from
the first sink or never advanced, a loss completed again where both are owed after one, an owed loss or an owed change
leaving the loop asleep, THE SETTLE completing none, and a record's pass taking a loss's turn or making a binding
change. srp_mutants.py plants each with the rest of its table; each named test (srp_binding.hpp, D1 to D10) must fail
on its own words. The two of a record's pass bite only where THE SETTLE carries a record alone, the one-interface
shapes, so their names take srp_drain_mutants.PREFIX and test_ctrl_firmware.py plants them there; the rest are
unprefixed, so its two-interface campaign (srp-mutants) plants them.
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
        kind('deliver-both-owed-binds-after-a-change',
             'SrpBinding.D7WithBothOwedAfterABindingChangeADeliveryCompletesTheLoss',
             '        if (app->srp_lost_last) {\n', '        if (true) {\n',
             'D7 with both owed after a binding change, the delivery completes the loss', path='app/ctrl_app_srp.c',
             suite='test_acmp_mbx.cpp'),
        kind('deliver-loss-turn-from-the-first',
             'SrpBinding.D8ASinksLossIsCompletedWithinItsTurnWhateverAnotherLosesAgain',
             'const unsigned k = (app->srp_loss_turn + step) % n;', 'const unsigned k = step % n;',
             "D8 a sink's loss waits at most n_sinks deliveries", path='app/ctrl_app_srp.c', suite='test_acmp_mbx.cpp'),
        kind('deliver-loss-turn-never-advanced',
             'SrpBinding.D8ASinksLossIsCompletedWithinItsTurnWhateverAnotherLosesAgain',
             'app->srp_loss_turn = (uint8_t)((lose + 1u) % n);', 'app->srp_loss_turn = app->srp_loss_turn;',
             "D8 a sink's loss waits at most n_sinks deliveries", path='app/ctrl_app_srp.c', suite='test_acmp_mbx.cpp'),
        kind('deliver-loss-always-first', 'SrpBinding.D9WithBothOwedAfterALossADeliveryMakesTheBindingChange',
             '        if (app->srp_lost_last) {\n', '        if (false) {\n',
             'D9 with both owed after a loss completion, the delivery makes the binding change',
             path='app/ctrl_app_srp.c', suite='test_acmp_mbx.cpp'),
        kind('srp-977-deliver-loss-in-a-records-pass', 'SrpBinding.D10ARecordsPassTakesNoTurn',
             'for (unsigned step = 0; step < n && lose == n && !settles; ++step) {',
             'for (unsigned step = 0; step < n && lose == n; ++step) {',
             "D10 a record's pass takes no turn", path='app/ctrl_app_srp.c', suite='test_acmp_mbx.cpp'),
        kind('srp-977-deliver-binds-in-a-records-pass',
             'SrpBinding.D6ARecordsPassMakesNoBindingChangeTheNextDeliveryMakesIt',
             'for (unsigned step = 0; step < n && bind == n && !settles; ++step) {',
             'for (unsigned step = 0; step < n && bind == n; ++step) {',
             "D6 a record's pass makes no binding change", path='app/ctrl_app_srp.c', suite='test_acmp_mbx.cpp'),
    )
