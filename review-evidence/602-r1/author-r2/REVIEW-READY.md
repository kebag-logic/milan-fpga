[A388] REVIEW READY

Commit: `471892a9bcc2d26fdcfc19db01949ecea83c5e0f` (local candidate on `602-phc-step-mr`; not pushed).

Changed: current PHC-only restart documentation and changelog, campaign inventory/routing, event-relative option-off checks with sibling isolation, and a 32-delay real CRF/settime coincidence test with a suppression control. RTL, configurations, builder code and submodule pins/contents remain unchanged from `49012143b335ea48d6a71c441a05d0c1796887ff`.

Validation at this committed head, all commands returned 0. `$ROOT` is `$LANES/602-phc-step-mr`; `$PACKET` is the round-2 evidence packet. Every command ran in the foreground with an explicit timeout and no pipeline.

- `make -C $ROOT/tb/verilator/milan_dp run`: full target passes; gmstep 103/103, render controls 6/6, default gmstep controls 6/6.
- `make -C $ROOT/tb/verilator/milan_dp gmstep-mutants`: 20/20 (two clean baselines, all eighteen controls caught).
- `make -C $ROOT/tb/verilator/tkdiag`: 96/96 and all four mutants caught.
- `python3 sw/builder/test_builder.py --require-rv32`: 358/358 mutations rejected, 53/53 RTL variants elaborated. `python3 $PACKET/builder_absent.py`: full bank, 256/256 mutations rejected, 53/53 RTL variants elaborated; all three compiler candidates audited absent.
- `python3 $PACKET/ooc_measure.py after`: both AX datapath shapes pass. The area question remains closed by the round-2 assignment.
- `python3 $PACKET/final_checks.py`: all 25 gates pass, including `scripts/lint_rtl.py --check --jobs 8`, `scripts/ci_scope.py --selftest`, both baremetal checks, documentation gates and diff hygiene.
- `python3 $PACKET/check_artifact_identity.py`: all fifty generated artifacts match across the five configurations. `python3 $PACKET/stale_doc_scan.py`: 41 candidates inspected in context, zero stale current-contract claims. `python3 $PACKET/audit_candidate.py`: clean worktree, unchanged protected bytes and submodules, valid final-head receipt hashes.

Acceptance evidence: adjtime-only fails only adjtime; settime-only leaves adjtime clean and fails settime mr/MEDIA_RESET; both-causes fails settime. The clean coincidence phase observes same-cycle overlap at delay 8 and exactly one outgoing toggle in each of 32 trials; its suppression mutant fails only the new named check.

`HANDOFF.md` contains per-item file:line references, reviewer-probe mappings, the full controls table, stale-document classification, gate commands/results and log sizes/SHA-256 values. `PR-BODY.md` has its Round 2 section and retains `[A383]` and `Closes #602`; the remote PR was not edited.

Evidence bounds: compiler-absent instruments and the unavailable historical placed calibration report are explicitly not run; compiler-present instruments passed. Simulated packet behavior does not establish physical clock continuity, an lwSRP reservation or placed area. Independent re-review remains required; this is no review verdict. No push, merge or hardware work was performed.
