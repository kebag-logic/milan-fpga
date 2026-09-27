[A380] REVIEW READY
Commit: 68e801b2823f75e037152f7eb2ac4c5dcda5d919
Branch: 593-mr-tu-soak. Local commit; no push or PR edit.

Changed: all six round-2 items and both accepted suggestions are implemented in the planner, tests and documentation. The tu rise is correlated and every GM change is graded. Insufficient timestamp resolution yields NOT RUN, using derived limits of min(0.25, 0.5) seconds for tu and half the one-second counter-update ceiling for the two-sided mr cause window. Causes are consumed per stream, counter windows require capture coverage, and counter decreases are reported as resets. REQ-VER-06, TESTING 6d and the outgoing mr design row reference #602; the assigned PHC-step rule remains in force pending that decision.

Validation: all 35 assigned gate commands returned 0 at this exact committed head, in the foreground from $LANES/593-mr-tu-soak. Commands and receipts are recorded in HANDOFF.md and gates.json.
- python3 -B tb/tools/torture_campaign.py --self-test: 75 tests passed.
- python3 -B tb/tools/torture_release_mutants.py: 106/106 killed, including PR #586's original 25.
- Plan feature: 87 scenarios passed; torture tier: 232 scenarios passed.
- scripts/ci_scope.py --selftest, scripts/check_baremetal_only.py --check/--selftest, documentation gates and git diff --check: rc 0.
- Unchanged reviewer mutation drivers: 32 and 38 applicable controls killed, zero survivors. Superseded anchors are explicitly accounted; eight re-anchored or replacement controls are also killed.
- External probe with recorded capture spans: 21/21 cases met. The unchanged probes are retained; their short mr captures now correctly produce NOT RUN. Internal counter-under-count and omitted-GM-provenance suggestions were not assigned and remain disclosed in the handoff.

Acceptance criteria: assigned round-2 desk work met with the evidence above. HANDOFF.md, the updated PR-BODY.md with Round 2, bounded receipts and SHA-256/size manifest are prepared. Worktree clean; no firmware, RTL, builder or gitlink changes. Independent re-review remains required; no review verdict is claimed. Physical release qualification remains separate, and the PHC-step decision remains open as #602.
