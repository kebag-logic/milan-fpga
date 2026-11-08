#!/usr/bin/env python3
"""probe_mrp_table.py TREE - independent checks of TREE/tb/verilator/milan_dp/twin_mrp.py.

1. Its Table 10-3 rows against a second transcription (third_party/lwSRP/src/core/mrp_mad.c appl_table,
   hand-copied here), allowing only the differences a bracketed (optional) action explains.
2. Synthetic single-attribute traces through grade_attribute: each must be graded legal or illegal as
   IEEE 802.1Q-2018 Table 10-3 (and note 8, 10.7.6.3) requires.
Prints one line per check and "probe_mrp_table: PASS" or "FAIL"; exit 0 only on PASS.
"""
import sys
from pathlib import Path

tree = Path(sys.argv[1]).resolve()
sys.path.insert(0, str(tree / "tb/verilator/milan_dp"))
import twin_mrp as m  # noqa: E402

S = m.STATES
# lwSRP appl_table, (message, next) per state; None message = TX_MSG_NONE, "-" next = no change
L = {
    "New!": "VN VN - - VN VN VN VN VN VN VN VN",
    "Join!": "VP - - - - - AA AP QP - - VP",
    "Lv!": "- VO LA LA LA LA - - - AO QO -",
    "rNew!": "- - - - - - - - - - - -",
    "rJoinIn!": "AO AP - - QA - - QO - QP - -",
    "rIn!": "- - - - QA - - - - - - -",
    "rJoinMt!": "- - - - - AA - - AO - AP VO",
    "rMt!": "- - - - - AA - - AO - AP VO",
    "rLv!": "LO - - VN VP VP - LO LO VP VP -",
}
L_TX = ("- sJ sN sN sJ - sL - - sJ - s", "- AA AN QA QA - VO - - QA - VO")
L_TXLA = ("- s sN sN sJ sJ - - - sJ sJ -", "LO AA AN QA QA QA LO LO LO QA QA -")
ok = True


def say(cond, what):
    global ok
    ok &= bool(cond)
    print(f"[{'ok' if cond else 'FAIL'}] {what}")


for ev, row in L.items():
    want = {s: c for s, c in zip(S, row.split()) if c != "-"}
    got = m.TRANSITIONS[ev]
    say(got == want, f"Table 10-3 row {ev} equals the second transcription")
say(m.TRANSITIONS["rLA!"] == m.TRANSITIONS["rLv!"], "rLA! row equals rLv! row (Table 10-3)")
for name, (acts, nexts), (lacts, lnexts) in (("tx!", m.TX, L_TX), ("txLA!", m.TXLA, L_TXLA)):
    for s, la, ln in zip(S, lacts.split(), lnexts.split()):
        a = acts.get(s, "")
        n = nexts.get(s, s)
        ln = s if ln == "-" else ln
        same_act = a == la or (a.startswith("[") and la in ("-", a.strip("[]")))
        say(same_act and n == ln, f"{name} {s}: twin ({a or '-'}, {n}) vs second ({la}, {ln})")

part = m.Participant("MSRP", m.REGISTRAR["MSRP"], True)
mv = m.Participant("MVRP", m.REGISTRAR["MVRP"], True)


def trace(items, p=part):
    seen = []
    for it in items:
        if it[0] == "got":
            seen.append(m.Seen(it[1], got=it[2]))
        else:
            seen.append(m.Seen(it[1], it[2], it[3] if len(it) > 3 else False))
    return m.grade_attribute("probe", seen, p).findings


say(not trace([("tx", 200, "New"), ("tx", 400, "New"), ("tx", 1000, "JoinMt"), ("tx", 2000, "JoinMt")]),
    "New x2 then JoinMt, Registrar MT: legal (VN, AN, AA by note 8, QA/AA)")
say(trace([("tx", 200, "New"), ("tx", 1000, "JoinMt")]), "New x1 then JoinMt: illegal (AN's tx! sends New)")
say(trace([("tx", 200, "New"), ("tx", 1000, "JoinIn")], mv), "MVRP New x1 then JoinIn, Registrar MT: illegal")
say(trace([("tx", 200, "New"), ("tx", 400, "New"), ("tx", 1000, "JoinIn")], mv),
    "MVRP New x2 then JoinIn, Registrar MT: illegal (10.7.6.3)")
say(not trace([("got", 100, "rJoinIn!"), ("tx", 200, "New"), ("tx", 400, "New"), ("tx", 1000, "JoinIn")], mv),
    "MVRP Registrar IN by rJoinIn!, New x2, JoinIn: legal")
say(trace([("got", 100, "rJoinIn!"), ("tx", 200, "New"), ("tx", 1000, "JoinIn")], mv),
    "MVRP Registrar IN, New x1 then JoinIn: illegal (AN's tx! sends New whatever the Registrar)")
say(trace([("tx", 200, "New"), ("tx", 400, "New"), ("got", 500, "rJoinIn!"), ("tx", 1000, "JoinMt")]),
    "Registrar IN after a received JoinIn, then JoinMt: illegal")
say(not trace([("tx", 200, "New"), ("tx", 400, "New"), ("got", 500, "rJoinIn!"), ("got", 600, "rLv!"),
               ("tx", 1000, "JoinMt")]),
    "MSRP: rLv! takes IN to MT at once (Milan 4.2.7.2.2), so a later JoinMt is legal")
say(not trace([("tx", 200, "New"), ("tx", 400, "New"), ("got", 500, "rJoinIn!"), ("got", 600, "rLv!"),
               ("tx", 700, "JoinMt")], mv),
    "MVRP: rLv! takes IN to LV (Table 10-4), sJ from LV sends JoinMt: legal")
say(trace([("tx", 200, "Lv")]), "Lv before any declaration: illegal")
say(not trace([("tx", 200, "New"), ("tx", 400, "New"), ("tx", 1000, "JoinMt"), ("tx", 2000, "Lv"),
               ("tx", 3000, "Mt", True)]),
    "withdrawn Lv, then a LeaveAll carrying Mt: legal")
miss = trace([("tx", 200, "New"), ("tx", 400, "New"), ("tx", 1000, "JoinMt"), ("tx", 10000, None, True)])
say(miss, "a LeaveAll frame omitting a declared (QA/AA) attribute: illegal (txLA! sJ is not bracketed there)")
print(f"probe_mrp_table: {'PASS' if ok else 'FAIL'}")
sys.exit(0 if ok else 1)
