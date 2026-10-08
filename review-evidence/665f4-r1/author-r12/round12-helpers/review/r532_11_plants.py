# SPDX-License-Identifier: CERN-OHL-W-2.0
"""Reviewer plants for round R532-11 (srp_driver.py ... escape IF this.py).

Each is a single-site source change. The driver reports CAUGHT when any test
of the selected suite/filter fails and ESCAPED when it stays green; a compile
refusal is never a catch. Run once against the checkout's own suite filter
(SrpBinding.*:SrpFeedback.*) and once against a copy that also includes
r532_11_probe.hpp (filter R11Feedback.*).
"""
from srp_mutants import Defect

APP = 'app/ctrl_app_srp.c'
SRP = 'srp/srp_mbx.c'
SUITE = 'test_acmp_mbx.cpp'
FILTER = '*'

PROBES = (
    # Identical-identity supersession keeps the retired epoch's kind.
    Defect('p11-supersession-kind-stale', FILTER,
           '                s->feedback_kind = s->desired;\n', '', '', path=APP, suite=SUITE),
    # Link reset no longer latches the withdrawal of a destroyed registrar.
    Defect('p11-reset-withdrawal-lost', FILTER,
           '        capture(&i->sinks[k],previous);\n', '        (void)previous;\n', '', path=SRP, suite=SUITE),
    # Centisecond expiry is no longer observed at the tick boundary.
    Defect('p11-tick-snapshot-lost', FILTER,
           '            snapshot(&m->ifs[n]);', '            (void)m->ifs[n];', '', path=SRP, suite=SUITE),
    # The completed receive is no longer observed (last event of a PDU).
    Defect('p11-receive-snapshot-lost', FILTER,
           '        snapshot(i);\n    }\n    if (result == -SHLAN_ERROR_NO_MEMORY)',
           '        (void)i;\n    }\n    if (result == -SHLAN_ERROR_NO_MEMORY)', '', path=SRP, suite=SUITE),
    # A registration after the first withdrawal replaces the retained kind.
    Defect('p11-postwithdrawal-kind-overwrite', FILTER,
           'if (!s->withdrawn && s->desired) {', 'if (s->desired) {', '', path=SRP, suite=SUITE),
    # The settled-view entry is called without comparing the current kind.
    Defect('p11-kind-change-uncompared', FILTER,
           '} else if (registered &&\n                       app->acmp.acmp.sinks[sink].tk_failed != (registered == 1u)) {',
           '} else if (registered) {', '', path=APP, suite=SUITE),
    # The delivered withdrawal latch is not cleared.
    Defect('p11-withdrawn-not-cleared', FILTER,
           '                s->withdrawn = false;\n                acmp_tk_unregistered',
           '                acmp_tk_unregistered', '', path=APP, suite=SUITE),
)
