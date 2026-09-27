[A377] REVIEW READY
Commit: 95bea7cf82fcf7cf034c156ef7aa6800ee769e05

Changed: the soak planner now checks recorded mr causes, the eight-PDU hold per stream, distinct caused toggles backing MEDIA_RESET increments, and the resolution-aware 0.25 s tu minimum after a GM change. REQ-VER-06 and TESTING 6d describe the evidence schema and derived windows. Missing evidence is NOT RUN.

Validation at this committed head, all rc 0:
- `python3 -B tb/tools/torture_campaign.py --self-test`: 66 tests pass, including the seven requested cases and boundary/missing-evidence controls.
- `python3 -B tb/tools/torture_release_mutants.py`: 44 mutants killed by named assertion failures, including 19 new controls.
- `python3 -B -m behave tests/features/torture_campaign_plan.feature -f progress`: 86 scenarios and 353 steps pass.
- `python3 scripts/ci_scope.py --selftest` and `python3 scripts/check_baremetal_only.py --check` / `--selftest`: pass.
- Documentation gates: `docs_check.py`; `check_em_dash.py --base 6d5ebd7357c1e468e446f18a61527c5be6118a04` and `--selftest`; `check_doc_style.py` and its self-test; `check_feature_status.py --self-test`; `check_doc_paths.py`; `check_archive.py` and its self-test; `gen_toc.py --selftest`, `--verify-anchors`, and `--check`: pass.
- gPTP, solution and submodule documentation checks and self-tests; traceability no-drift check; Python idiom, hygiene and ownership checks and self-tests: pass.
- `git diff --check` and `git diff 6d5ebd7357c1e468e446f18a61527c5be6118a04 HEAD --check`: pass.

Base: 6d5ebd7357c1e468e446f18a61527c5be6118a04. All 33 gates ran in the foreground from the physical candidate path, without pipelines. The worktree is clean.

Acceptance criteria: assigned desk criteria met. HANDOFF.md contains the file:line change list, clause-to-check map, self-test and mutant tables, and exact-head gate table. PR-BODY.md is prepared with Closes #593.

Review boundary: these checks do not establish physical release qualification. GM_LOSS_RECOVERY.md:155 currently documents outgoing mr toggles on PHC steps; an observed toggle still needs a separately recorded permitted media-clock cause to pass this corrected gate. Talker behavior remains outside this assignment, with #74. Independent review is pending.
