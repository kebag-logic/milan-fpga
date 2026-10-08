"""R532-13 reviewer-owned disposable probes against the round-13 standing tests.
Each probe plants one srp_mbx.c change and runs the named standing test; the
expected outcome is recorded and compared. Usage: <repo> <lwsrp> <out> <ifcount>"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import REPO, LWSRP, OUT
import srp_mutants
from srp_mutants import Defect
n = int(sys.argv[4])
T1 = 'SrpFeedback.FailedSinglePduWithdrawalThenRegistrationRetainsTheFirstEvent'
T2 = 'SrpFeedback.FailedReplacementWithdrawnInsideOnePduStillReprobes'
T3 = 'SrpFeedback.BothKindsFailedLeaveInsideOnePduIsNotAWithdrawal'
LEFT = '    } else if (type == MSRP_ATTR_TYPE_TALKER_ADV || type == MSRP_ATTR_TYPE_TALKER_FAILED) {'
srp_mutants.DEFECTS = (
    # Failed Lv ignored entirely by the leave indication: T1 and T2 must reprobe-fail.
    Defect('x1-leave-ignores-failed', T1, LEFT, '    } else if (type == MSRP_ATTR_TYPE_TALKER_ADV) {',
           'retained withdrawal reprobes', suite='test_acmp_mbx.cpp'),
    Defect('x1-leave-ignores-failed-t2', T2, LEFT, '    } else if (type == MSRP_ATTR_TYPE_TALKER_ADV) {',
           'retained withdrawal reprobes', suite='test_acmp_mbx.cpp'),
    # Any leave clears every kind: T3 must report a false withdrawal.
    Defect('x2-leave-clears-all-kinds', T3,
           'talker_changed(from_ctx(ctx),value,type == MSRP_ATTR_TYPE_TALKER_FAILED ? 1u : 2u,false);',
           'talker_changed(from_ctx(ctx),value,3u,false);',
           'continuous Advertise is not withdrawn', suite='test_acmp_mbx.cpp'),
    # The filter forgets the previous kind (observes only the delivered snapshot): T1 must catch.
    Defect('x3-filter-no-capture', T1,
           '        s->desired = (s->registered_kinds & 1u) ? 1u : (s->registered_kinds & 2u);\n        capture(s,previous);',
           '        (void)previous;',
           'retained withdrawal reprobes', suite='test_acmp_mbx.cpp'),
    # q04-equivalent observed by T2 as well (replacement Failed Lv clears the Advertise bit only).
    Defect('x4-q04-on-t2', T2,
           'talker_changed(from_ctx(ctx),value,type == MSRP_ATTR_TYPE_TALKER_FAILED ? 1u : 2u,false);',
           'talker_changed(from_ctx(ctx),value,2u,false);',
           'retained withdrawal reprobes', suite='test_acmp_mbx.cpp'),
)
failed = srp_mutants.campaign(OUT / f"extra-if{n}", LWSRP, 4, n)
print(f"extra probes IF={n}: {'FAIL' if failed else 'PASS'}")
sys.exit(1 if failed else 0)
