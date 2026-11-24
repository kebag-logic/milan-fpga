#!/usr/bin/env python3
"""Show that the Registrar's step after txLAF! decides a grade, so the escaped mutant is not equivalent.

Usage (from a directory holding a copy of tb/verilator/milan_dp's Python files): txlaf_registrar_probe.py
A Domain declared and sent JoinMt until QA, a peer's JoinIn received (Registrar IN), then a full LeaveAll MRPDU that
leaves the Domain out (txLAF!: QA to VP; the sLA's rLA! takes the Registrar IN to LV), then a tx! from VP: sJ with
the Registrar LV sends JoinMt. Prints the findings; the correct grade has none, a grade that keeps the Registrar IN
across txLAF! expects JoinIn and reports one.
"""
import twin_mrp as tm

msrp = tm.Participant("MSRP", tm.REGISTRAR["MSRP"], True)
seen = [tm.Seen(0, "JoinMt"), tm.Seen(100, "JoinMt"), tm.Seen(200, got="rJoinIn!"),
        tm.Seen(1000, None, True, full=True), tm.Seen(1010, "JoinMt")]
trace = tm.grade_attribute("Domain", seen, msrp)
print(f"findings={len(trace.findings)} configs={sorted(trace.configs)}")
for f in trace.findings:
    print("  " + f)
