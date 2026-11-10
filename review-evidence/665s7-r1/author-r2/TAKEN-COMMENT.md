[A757] TAKEN

Round 2 on PR #874, adding commits on `5fb6904ffe12effc4bde6bf5313faea7a3beebdc` only (no merge, rebase, force or amend). Branch `665-s7-srp-tx`, base `dev-soft-core` `1d6bf555`.

Authoritative references: the round 2 ruling (PR #874 issuecomment-6763709522), items 1 and 2; R814-1 (PR #874 issuecomment-6763695560) F-1 and F-2; this issue's acceptance item 3; #665 issuecomment-6681686082 item 3 (SRP/MRP bound T_svc = 20 ms); IEEE 802.1Q-2018 10.7.4.1, 10.7.11 and Table 10-7; Milan v1.2 Table 4.3 (JoinTime 200 ms); `docs/reference/FR_NFR.md` 3.4.1.

Interpreted scope:
- F-1. The egress allowance becomes T_svc = 20 ms, derived from the source the firmware budget uses rather than a literal. `srptx_grade.py`, the `join-late-in-t-svc` plant (still just outside the new bound), the two READMEs and the PR body's item 3 row are restated, citing acceptance item 3 and #665 issuecomment-6681686082 item 3.
- F-2. The JoinTime interval `measure_time` computes is graded on both sides, against 10.7.4.1, 10.7.11 and Table 10-7 (Milan Table 4.3, 200 ms), widened by the allowance on each side as LeaveAll is. A short-Join-timer code mutant (10 cs and 15 cs arms) is refused by its own words and escapes without the new check.
- Item 5 (#608 in the production composition) stays owed; the fixture is not touched. Every existing shape's generated output stays byte-identical.

Validation plan, on a clean clone of the final head, all rc 0: `make srptx`, `srptx-plants`, `srptx-mutants`; every `run:` step of the jobs a pull request to `dev-soft-core` triggers, with a reason for each step that cannot run; the docs workflow; the full sweep in 4 shards; the firmware self-test, `fw_coverage.py --check` and every firmware mutant driver; S2's harness at 1x1/1if and 8x8/2if; `test_builder.py --require-rv32`; `cd tests && behave`; `git diff --check` against the merge base.

Blockers: one, in item 1. The source the firmware budget uses is `tb/verilator/ctrl_service_budget/scenario.py`, which `nvm_split_target/target_grade.py` already imports. At this base it reads `T_SVC_MS = 10.0`, the proposed figure (`:91`), and `CEILING_MS['srp'] = 18.0` (`:99`). The 20 ms values exist only on S2b's branch. So a `SVC_MS` derived from that source is 10 ms here, not the 20 ms of item 1 and acceptance item 3. Changing that source would change S2's budget harness and the NVM split target's bound, both outside this lane and both carried by S2b.

I will do item 2 and the rest of item 1, with the allowance held in one named constant from which every bound and the plant are derived. I will run `make srptx`, the plants and the mutants. Then I will STOP and name that line for a decision. The other exit also applies: STOP if the unplanted run's JoinTime intervals fall outside the two-sided bound, with the figures.
