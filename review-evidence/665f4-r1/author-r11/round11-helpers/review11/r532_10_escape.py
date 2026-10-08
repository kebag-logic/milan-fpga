# SPDX-License-Identifier: CERN-OHL-W-2.0
"""Reviewer plants for round R532-10 (run by srp_driver.py ... escape IF this.py).

Each is a single-site source change; the driver reports CAUGHT when any test
of the stated suite fails, else ESCAPED.
"""
from srp_mutants import Defect

APP = 'app/ctrl_app_srp.c'
HDR = 'app/ctrl_app.h'
SUITE = 'test_acmp_mbx.cpp'

PROBES = (
    # A transient refusal on an earlier sink is forgotten once a later sink delivers.
    Defect('r10-transient-refusal-forgotten', '*',
           'pending = r->pending || pending;', 'pending = r->pending;', '', path=APP, suite=SUITE),
    # A parked request whose old-binding retirement is refused lets the loop sleep.
    Defect('r10-parked-retire-refusal-sleeps', '*',
           'pending = pending || r->pending;', 'pending = pending;', '', path=APP, suite=SUITE),
    # Feed the old binding's registration to a replacement still awaiting delivery.
    Defect('r10-feedback-ignores-pending', '*',
           'if (!r->pending && r->bound) {', 'if (r->bound) {', '', path=APP, suite=SUITE),
    # Understate the new per-sink feedback allowance four-fold.
    Defect('r10-feedback-allowance-quarter', '*',
           '(ACMP_MAX_SINKS * 4u)', '(ACMP_MAX_SINKS * 1u)', '', path=HDR, suite=SUITE),
    # Understate it to a fixed eight accesses regardless of sink count.
    Defect('r10-feedback-allowance-eight', '*',
           '(ACMP_MAX_SINKS * 4u)', '(8u)', '', path=HDR, suite=SUITE),
    # Feedback reads interface 0's snapshot for every sink.
    Defect('r10-feedback-interface-zero', '*',
           'app->srp->ifs[interface].sinks[sink].desired', 'app->srp->ifs[0].sinks[sink].desired', '',
           path=APP, suite=SUITE),
    # VID 0 is no longer parked (only the upper range).
    Defect('r10-park-vid0-missed', '*',
           'r->stream.vlan_id == 0 ||', 'false ||', '', path=APP, suite=SUITE),
    # Parking ignores the request's bound flag (unbind of an invalid stream stays parked).
    Defect('r10-park-ignores-unbind', '*',
           'r->parked = r->bound && (', 'r->parked = (', '', path=APP, suite=SUITE),
)
