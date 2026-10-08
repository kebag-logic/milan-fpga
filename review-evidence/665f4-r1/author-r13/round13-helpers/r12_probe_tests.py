# Runs the reviewer probe tests (probe-tests/r12_failed_intrapdu.hpp, appended to a
# disposable candidate copy's srp_feedback.hpp) unmodified and against probes q04, q06 and q13.
_T1 = "SrpFeedback.R12FailedSinglePduWithdrawalThenRegistrationRetainsTheFirstEvent"
_T2 = "SrpFeedback.R12BothKindsFailedLeaveInsideOnePduIsNotAWithdrawal"
_LEFT = "talker_changed(from_ctx(ctx),value,type == MSRP_ATTR_TYPE_TALKER_FAILED ? 1u : 2u,false);"
_T3 = "SrpFeedback.R12FailedReplacementWithdrawnInsideOnePduStillReprobes"
_SETF = "talker_changed(from_ctx(ctx),&value->talker,1u,true);"
_CLR = "            s->registered_kinds &= (uint8_t)~kind;"
def _p(name, test, old, new, needle, expect):
    return {"name": name, "test": test, "old": old, "new": new, "needle": needle,
            "path": "srp/srp_mbx.c", "suite": "test_acmp_mbx.cpp", "expect": expect}
PROBES = [
    _p("t1-baseline", _T1, _LEFT, _LEFT, "retained withdrawal reprobes", "SURVIVED"),
    _p("t1-q04-leave-clears-advertise-only", _T1, _LEFT, "talker_changed(from_ctx(ctx),value,2u,false);",
       "retained withdrawal reprobes", "CAUGHT"),
    _p("t2-baseline", _T2, _CLR, _CLR, "continuous Advertise is not withdrawn", "SURVIVED"),
    _p("t2-q06-change-clears-both-kinds", _T2, _CLR, "            s->registered_kinds = 0;",
       "continuous Advertise is not withdrawn", "CAUGHT"),
    _p("t3-baseline", _T3, _SETF, _SETF, "retained withdrawal reprobes", "SURVIVED"),
    _p("t3-q13-failed-indication-as-advertise", _T3, _SETF, "talker_changed(from_ctx(ctx),&value->talker,2u,true);",
       "retained withdrawal reprobes", "CAUGHT"),
    _p("t3-q04-leave-clears-advertise-only", _T3, _LEFT, "talker_changed(from_ctx(ctx),value,2u,false);",
       "retained withdrawal reprobes", "CAUGHT"),
]
