# q10b: restore the round-11 reentrant registrar visit inside the MSRP rx filter
# (snapshot() from interested_msrp), keeping the copy loop. Informative only:
# does any standing suite (plain, composition, debug guard) detect a filter that
# re-enters its owning application?
_OLD = "    // Observe the previous complete event from copied indication data only.\n"
_NEW = "    snapshot(i);\n    // Observe the previous complete event from copied indication data only.\n"
def _p(tag, suite, debug):
    return {"name": f"q10b-filter-reenters-visitor@{tag}", "test": "*", "old": _OLD, "new": _NEW,
            "needle": "", "path": "srp/srp_mbx.c", "suite": suite, "debug": debug, "expect": "ANY"}
PROBES = [_p("test_acmp_mbx", "test_acmp_mbx.cpp", False), _p("srp_mbx", "srp_mbx.cpp", False),
          _p("srp_debug", "srp_mbx.cpp", True)]
