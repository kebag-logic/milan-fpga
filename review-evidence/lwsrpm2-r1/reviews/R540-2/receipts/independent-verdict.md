# Independent verdict and ledger, written before reading prior review findings

Exact head a9cd5ef58a2478cb2ce4899b31aa02d5c2072646, tree bc5b80a60d923ce869647e3f3ba95276456864d1.
Delta 23d9a817..a9cd5ef5 (one commit).

Verdict: NEGATIVE.

| ID | Severity | Lenses | Location | Summary |
| --- | --- | --- | --- | --- |
| F1 | MAJOR | Conformance, Robustness, Tests, Docs | src/core/mrp_mad.c:353,359,959,997 | A changed MSRP Listener declaration or Talker value received while the Registrar is in LV is stored but never indicated; later JoinIn messages never indicate it either. Regression from 23d9a817. |
| F2 | MAJOR | Conformance, Robustness, Tests, Docs | src/core/mrp_pdu.c:135-211 | A later-version unknown MSRP message is no longer skipped by AttributeListLength. A non-generic vector or trailing octets inside the list reject the whole PDU and its following valid Listener. Regression from 23d9a817. |
| F3 | MINOR | Tests | tests/unit/review_test.c; src/core/mrp_mad.c:529-561,628-639,1027,1265,887-892 | Allocation-failure semantics of the new propagation queue have no test or reversal; six reviewer plants survive both profiles. |
| R1 | RESIDUE | Docs | doc/tools/README.md:31 | Carried licence wording from the merged licence PR is not applied. |
| R2 | RESIDUE | Docs | doc/manager.md:91-92 | Carried licence wording from the merged licence PR is not applied. |

| Lens | State |
| --- | --- |
| Conformance | UNCLEAN (F1, F2) |
| RTL | CLEAN (no HDL in scope; embedded list, freestanding and dispatch probes pass) |
| Robustness | UNCLEAN (F1, F2) |
| Tests | UNCLEAN (F1, F2, F3) |
| Docs | UNCLEAN (F1, F2 claim text); R1, R2 residue only |
