[A776] REVIEW READY
Commit: 3bebf03a1d25bcbde9c0ec48dfd711af7280131e (round 2; round 1's head 5e6fef3e was POSITIVE from R833-1 and R834-1)
Changed:
- `d3202fa2`: one merge commit of `dev-soft-core` `cec88385` (#810 merged) into `897-split-as-path`. Two doc conflicts, each kept from both sides: `MAILBOX_SPLIT.md` (this branch's AECP-face test row with dev-soft-core's planted-defects row) and `SPLIT_CONTROL_MEMORY.md` section 5 (dev-soft-core's platform and harness-arm paragraphs with this branch's GET_AS_PATH paragraph). Six files auto-merged, and for each of this branch's 16 files the merge's diff from `cec88385` equals this branch's diff from `7f50ee6a`. Submodule pins are unchanged.
- `d395f682`: the images' sizes restated at the composed head (`SPLIT_CONTROL_MEMORY.md` sections 5 and 6, the plat README, the split boot README).
- `3bebf03a`: `tb/verilator/ctrl_service_budget/build.py` held within the 1,000-line module limit. It is exactly 1,000 lines at `cec88385`, and the change made it 1,001 ("long module 11 > ratchet 10"). The comment is rewrapped and no generated code changes; the harness ELFs are identical to the merge's.
Validation (one clean-clone pass at this head):
- every workflow job a PR to dev-soft-core triggers, each on its own fresh clone: 139 steps rc 0, 226 not run (each with its stated reason), 0 bad; every job's clone clean after;
- the full Verilator sweep as four shards: 65 suites, 0 failed. 62 passed in the sweep; the 3 its wall clock killed under CPU contention (milan_dp, milan_dp_render, mmcm_servo) passed re-run alone with 0 in-suite failures;
- the lane gates, all rc 0 (the flip check exits 1 at `cec88385` and here alike, with identical output; it is no merge gate);
- the three base reds green on the composed tree: `check_cpp_idiom.py` 0 ("multi-declarator declaration: 0 <= 0"), `ctrl_service_hooks/run.py --self-test` 0 (28 of 28 checks, 96 of 96 mutants), firmware-boundary 0 ("ctrl_boundary: PASS");
- firmware self-test PASS in its four shards: AECP campaign 236 of 236, control 699 of 699, SRP 340 ok; the nine AECP plants and `plat-as-path-unavailable` (platboot1, platboot2) each caught by name;
- `fw_coverage.py --check` PASS (39 files; `aecp_face.c` 179/179 lines, 160/160 branches);
- `test_builder.py --require-rv32` PASS; docs gates and `docs_check.py` 0 findings; bdd-conformance and behave 508 scenarios, 0 failed;
- the split boot simulation ready at 1x1/1if 26.354 ms, 8x8/1if 66.001 ms and 8x8/2if 68.389 ms, against 20,000 ms;
- the CPU budget harness at both points: fresh builds of arm A, `answering-ports` and `answering-every-port` at this head and at `cec88385`, sampled groups, 0 refusals, 0 budget, share or notice misses at both.
Acceptance criteria:
- #897 acceptance 1-4 are met (acceptance 3 as amended by the ruling, issuecomment-6828659285); acceptance 5 belongs to the bench lane.
- Load: 1x1/1if 0.501 (0.499 with tsn-c-stack#32) against 0.70, delta 0.000 against `cec88385`.
- ROM, `cec88385` -> this head:
  - fixture: 1x1/1if 38.5, 1x1/2if 41.0 -> 41.5, 8x8/1if 51.5, 8x8/2if 58.5 (124,136 B, 792 B before its next granule; cap 58.5);
  - platform: 39.5, 43.0, 53.0, and 8x8/2if 59.5 -> 60.0 (129,272 B, its entry's tiles; cap 60.5);
  - the harness arms at 8x8/2if: 58.5 each (A 124,136 B, `answering-ports` 124,320 B, `answering-every-port` 124,452 B);
  - nothing is over its cap, so #898 does not wait on #901.
Open risks/questions: none. Both 8x8/2if entries are now fully used: a granule more at that point is refused (the ROM debt owed to S14).
