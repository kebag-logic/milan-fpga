[R545] NEGATIVE - exact head ced667d8ee35929ab5f9e77a1c5396e173a693d8

Independent verdict recorded 2026-10-07T12:49:26.650657+00:00, before reading prior public findings or any other reviewer's report.
All five lenses have been applied independently. Frozen issue #16 acceptance is satisfied; a documentation measurement defect remains open.

Finding R545-1-F1 — MINOR — Docs.
Artifacts: doc/manager.md:56–57 and doc/tester.md:193.
The manager guide retains 86 tests / 19885 assertions OFF and 86 / 19873 ON. The exact head executes 87 / 19901 and 87 / 19889.
The tester guide retains 93 reversals; the exact head defines and executes 94 in each profile.
Authority/evidence: issue #16; the changed README.md:45 and doc/tester.md:29,69; receipts/OFF-ctest.log, ON-ctest.log, OFF-reversals.log, ON-reversals.log and reversal-audit.json.
Impact: public current-result figures conflict across the documentation and understate this PR's added test and reversal.
Required outcome: update doc/manager.md to 87 tests / 19901 assertions OFF and 87 / 19889 ON; update doc/tester.md:193 to 94 reversals.
Verification: compare every reported current total with the exact-head executable receipts, then rerun documentation checks on the corrected head.
This is not RESIDUE: the required correction changes reported measurements and figures.

| lens | CLEAN/UNCLEAN | examined artifacts | covering round | exact head |
| --- | --- | --- | --- | --- |
| Conformance | CLEAN | Local IEEE 802.1Q-2018 Table 10-3 notes 4/5; issue #16; mrp.h API; integration_test.c:324,352; unchanged mrp_mad.c:507 | R545-1 | ced667d8ee35929ab5f9e77a1c5396e173a693d8 |
| RTL | CLEAN | Not applicable: full four-file diff and tree inventory contain no RTL change; source tree unchanged | R545-1 | ced667d8ee35929ab5f9e77a1c5396e173a693d8 |
| Robustness | CLEAN | independent app lifetimes, deterministic wire vectors, state/instance/registration checks; mutation runner baseline/build/failure/restoration contracts; all named failures audited in both profiles | R545-1 | ced667d8ee35929ab5f9e77a1c5396e173a693d8 |
| Tests | CLEAN | Both profile builds, 87-unit suites, three scenarios / ten steps each; 94 reversals each and restored passing suites; raw per-command receipts | R545-1 | ced667d8ee35929ab5f9e77a1c5396e173a693d8 |
| Docs | UNCLEAN | CONTRIBUTING, README, all guides and doc/tools; numeric cross-check F1; sentence/reference/self-test/link gates pass; 27 graphs rendered and visually inspected | R545-1 | ced667d8ee35929ab5f9e77a1c5396e173a693d8 |

Limits: focused host evidence only. Scenario return checks do not establish independent switch state. No hardware, physical calibration, target integration or final current-dev candidate was exercised. Full manager banks are outside this execution scope. Exact-head hosted checks, statuses and workflow runs have zero entries; this supplies no hosted pass. Final review still needs public prior-finding reconciliation, current manager-comment inventory, tracked-byte/mode/index integrity receipt, and manifest completion.
