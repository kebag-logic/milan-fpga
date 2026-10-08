# SPDX-License-Identifier: CERN-OHL-W-2.0
"""Reviewer plants against the reviewer's own discriminating probes (R532-10).

Run from a disposable copy whose test_acmp_mbx.cpp includes
r532_10_probe_guard.hpp; CAUGHT means the named probe test fails.
"""
from srp_mutants import Defect

APP = 'app/ctrl_app_srp.c'
SUITE = 'test_acmp_mbx.cpp'

PROBES = (
    Defect('r10-feedback-ignores-pending', 'SrpBinding.R10ReplacementAwaitingDeliveryGetsNoOldRegistration',
           'if (!r->pending && r->bound) {', 'if (r->bound) {', '', path=APP, suite=SUITE),
    Defect('r10-transient-refusal-forgotten', 'SrpBinding.R10EarlierSinkTransientRefusalKeepsDeliveryAwake',
           'pending = r->pending || pending;', 'pending = r->pending;', '', path=APP, suite=SUITE),
)
