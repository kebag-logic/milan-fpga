# R540-4 independent pass (written 2026-10-07T09:47:24Z, before reading any prior review report)

Exact head 0a45695db537badb8d7e9cbf578925fe5b89d647, tree 6d663f9b08d92b1e1b7202ce159b9e8e391d5f56.

Own verdict at this point: NEGATIVE.

Own findings:
- R540-4-01 MINOR (implementation, Robustness, Tests): a Flush retained after reservation failure moves the Registrar IN to LV without an observer record (mrp_mad.c:644-652 with the early return at mrp_mad.c:722-726), contrary to mrp.h:387. Probe: 45 of 114 Flush cases per profile show the gap; a one-line scratch fix removes it with suites and probe passing.
- R540-4-02 MINOR (Tests): replacement of an opposite Talker held in LV has no direct regression; plants p06 (skip leavetimer! delivery) and p09 (IN-only replacement) survive the enabled-profile suite, and p09 is killed in the default profile only through the fault-retry path. The reviewer probe kills both in both profiles.
- S1 SUGGESTION: a later LeaveAll in the same PDU is still applied after a reservation failure; the identical retry converges to the single-pass state.
- S2 SUGGESTION: Flush's LeaveAll request (base code) has no killing test (plant p13).

Own ledger at this point:

| Lens | State |
| --- | --- |
| Conformance | CLEAN |
| RTL (implementation source) | UNCLEAN (R540-4-01) |
| Robustness | UNCLEAN (R540-4-01) |
| Tests | UNCLEAN (R540-4-01, R540-4-02) |
| Docs | CLEAN |

Still to do after this receipt: map prior findings (R540-3, R541-3 and earlier) to this head, including y01, y02, y07 and the tester.md:143 item.
