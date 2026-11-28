DRAFT of the reviewer's own independent pass at c0b625d1792e61b8e99944daea65b842e6b9dcde (content fixed before any
other reviewer's findings at this head were read; see the report's limits for the order in which it was saved).

Own verdict: NEGATIVE.

Own findings:
- F1 BLOCKER Tests, Docs: hosted firmware-boundary fails at the head; egress_mii.py is unlisted in ctrl_configs.
- F2 MAJOR Conformance, RTL, Tests, Docs: no public receipts for the image at aa53840d9.
- F3 MINOR Docs: harness README names the round-7 qualification as the installed row's.
- F4 MINOR Docs: section 15 states the non-carrying census's observed maxima.
- F5 MINOR Tests, Docs: egress agreement check does not compare the beat-in it documents.
- F6 MINOR Tests: census_extract self-test does not bind the production read limit.
- F7 MINOR Tests, Docs: egress_fixed.py fails under its documented -I invocation.

Own ledger: Conformance UNCLEAN (F2); RTL UNCLEAN (F2); Robustness CLEAN; Tests UNCLEAN (F1, F2, F5, F6, F7);
Docs UNCLEAN (F1, F2, F3, F4, F5, F7).
