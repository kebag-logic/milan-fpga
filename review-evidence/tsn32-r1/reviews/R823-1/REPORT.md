[R823] NEGATIVE - exact head 9043b926532dc4ffb57218ee0eebca7564262289

# R823-1: kebag-logic/tsn-c-stack PR #34 (issue #32), changed-sink ACMP walk

- Exact head `9043b926532dc4ffb57218ee0eebca7564262289`, tree `a77b293b7dd3c1d67ec853a12c672d3dd1d8733e`, base `main` `9deb0ddb299013fcf2d9df7ad3d31961a33013cd` (still `main` at review time). Merge commit `dd8b026f` (parents `fa31d4c8`, `9deb0ddb`), then `9043b926`.
- Reviewer: internal independent reviewer, cleared context, own detached clone. Public review start: https://github.com/kebag-logic/tsn-c-stack/pull/34#issuecomment-6788876835.
- Reconstructed from: CONTRIBUTING.md (the repository has no AGENTS.md), README, docs/, the issue #32 body (frozen acceptance 1 to 4; the issue has no comments), the PR body, ACMP-13 in docs/REQUIREMENTS.md and docs/requirements.json, the port contract in docs/PORTING.md, `git diff 9deb0ddb..9043b926`, `git diff fa31d4c8..9043b926`, the history, the author's published receipts in milan-fpga `f5200b66` `review-evidence/tsn32-r1`, and the public ACMP walk rulings and status on milan-fpga #665 (round 25 ruling 6751196896, round 25 STOP 6778599191, round 26 ruling 6779973927, round 26 STOP 6788757307, ruling 6788828284).
- Authorities: IEEE 1722.1-2021 8.2 (ACMP state machines) and Milan v1.2 5.5 (5.5.3.5), as the code cites them. The change is meant to keep behaviour exactly the same. So conformance means the calls, frames and their order are the same as `main`'s, and I checked that against `main`'s real core, not only against the head's test.

## Verdict

NEGATIVE. On the code, the head is correct. The changed-sink walk makes exactly the calls of `main`'s full walk, frame bytes and order included, in all 480 reviewer differential cases of `main`'s real `src/acmp.c` against the head's. The merge keeps both parents. All 470 plants are caught by their own assertion messages. CI rc 0 on hosted runs at the exact head and in the reviewer's local run (one environment stand-in, disclosed below). Three MINOR findings remain open:
- The 33-sink differential still avoids the second mark word's command and owed paths, a restriction the merge made unnecessary. Two planted second-word defects pass the whole suite.
- ACMP-13's "only the changed sinks" and "completion clears every mark" have no failing assertion. A plant that never clears the marks passes every gate.
- The parent consumer's firmware gates at this donor change are not evidenced.

## Findings

### R823-1-F1 (MINOR): the 33-sink differential leaves the second mark word's command and owed paths untested; two planted second-word defects escape every test and plant
- Lenses: Tests, Robustness.
- Where:
  - `tests/test_acmp_walk.cpp:187`: `commanded_sink()` folds every BIND_RX, UNBIND_RX and GET_RX_STATE for sink 32 onto sink 0 when `wide`.
  - `tests/test_acmp_walk.cpp:304`: `bool room = wide || ...` never withdraws transmit room at 33 sinks, so no frame is ever owed there.
  - The PR body says why: the test "was written before #31 widened the owed-release mask, when `1u << 32` would have been undefined".
- Evidence:
  - The merge (`dd8b026f`) brought in #31's word-sized mask. So at this head the restriction is no longer needed. It leaves the merge's own conflict line untested by the differential at the only size with a second word: the release loop, `src/acmp.c:1311-1314`, which reads `o->release[k / 32u]` and marks. The same holds for the `bind()`, `unbind()` and `probe_left()` marks (`src/acmp.c:888`, `:924`, `:794`) for any sink at 32 or above.
  - The receipt shows owed-max 0 at 33 sinks, and no BIND_RX or UNBIND_RX reaches sink 32 (`receipts/differential-head-vs-main.log`, the `sinks=33 lift=0` line).
  - Reviewer fault probes (`scripts/probe_mutants.py`, `receipts/mutants/probe-results.json`): the head's `acmp_tests`, `acmp_wide` and `acmp_walk` all pass with
    - `bind-marks-only-word-zero` (BIND_RX marks only sinks below 32),
    - `unbind-marks-only-word-zero` (UNBIND_RX likewise),
    - `probe-left-marks-only-word-zero`.
  - The first two are caught only by the reviewer's lifted 33-sink differential: commands reach every sink and room is withdrawn (`DIVERGE sinks=33 ... lift=1`).
  - `release-marks-only-word-zero` is caught only incidentally, by #31's `acmp_wide`, and not by the walk test.
  - So a sink-32 defect in which a BIND_RX or UNBIND_RX does not publish, admit, persist or report until a later entry happens to mark the sink escapes the stack's gates. That breaks ACMP-10's publish-before-response and ACMP-13's order guarantees.
  - The reviewer's lifted run passes at the head, 240 cases against `main`. So lifting the restriction is feasible and the head is correct under it.
- Impact: acceptance item 1 ("identical callback traces at 1, 8, 32 and 33 sinks") and the review focus "#33's mask stays sized from ACMP_MAX_SINKS on every new path" are shown at 33 sinks only for entries that never touch the second word's command or owed paths. Acceptance item 2's plants include no second-word site except the two word-index plants.
- Required outcome:
  - At 33 sinks, let BIND_RX, UNBIND_RX and GET_RX_STATE reach every sink, sink 32 included, and withdraw transmit room as at 1, 8 and 32 sinks.
  - Add plants that the 33-sink differential kills by its own message: a mark missing only for the second word at `bind()`, `unbind()`, the release loop and `probe_left()`. Update the PR body's 33-sink paragraph.
- Verification: run `acmp_walk` and the campaign at the new head. The four second-word plants must be CAUGHT through `AcmpWalk.ThirtyThreeSinksMatchTheFullWalk` with "the changed-sink walk makes the full walk's calls".

### R823-1-F2 (MINOR): ACMP-13's "only the changed sinks" and "completion clears every mark" have no failing assertion
- Lenses: Tests.
- Where:
  - `src/acmp.c:553-554` (`memset(a->dirty, ...)`, `a->dirty_if = 0u`).
  - `docs/REQUIREMENTS.md:42` ("completion clears every mark") and `:49` ("publish, re-arm, admit, persist and report only the sinks the entry changed").
  - CONTRIBUTING.md: "A regression needs a failing assertion and a runnable planted defect."
- Evidence:
  - The reviewer probe `marks-never-cleared` removes both clearing lines. It passes `acmp_tests`, `acmp_wide`, `acmp_walk` and the old-versus-new differential (`receipts/mutants/probe-results.json`).
  - The reason: a core that never clears its marks walks every sink it ever touched, which makes the same calls. The differential compares calls only, and coverage counts the lines as executed either way.
  - The behaviour that sets ACMP-13 apart, the CPU cut issue #32 exists for (2,294 to 279 cycles at 32 sinks, reproduced in `receipts/bench-rerun.txt`), can therefore be reverted with every gate green.
- Impact: a silent regression of the requirement's purpose and of the cost the parent grades with.
- Required outcome: an assertion that fails when marks outlive their completion. For example, in `AcmpWalk` after each entry that completes, every `walked.a.dirty` word and `walked.a.dirty_if` are zero. Or a white-box count of the sinks a completion visits. Plus a plant that drops the clear, caught by that assertion's message.
- Verification: the new plant is CAUGHT in the campaign. The traceability row for ACMP-13 lists the asserting test.

### R823-1-F3 (MINOR): the parent consumer's firmware gates at this donor change are not evidenced
- Lenses: Tests, Robustness.
- Where: the donor bar's parent consumer gates. milan-fpga `dev` `46c971fa` and `dev-soft-core` `1d6bf555` both pin `third_party/tsn-c-stack` at `70936b77`, an ancestor of this head.
- Evidence:
  - The S2b lane's public receipts show the parent firmware gates only at the pin: `firmware-unit`, `firmware-control-mutants` (672/672), the AECP and SRP campaigns, `firmware-boundary` and `firmware-verilator`, all at `0b37f3d2` per STOP 6788757307.
  - The #32 change appears only as a scratch port used to grade the CPU load. DONOR-HANDOFF section 3: "the pin does not move"; ruling 6788828284 item 6: "The flip check is read at the pin".
  - No published receipt runs the parent's firmware unit tests, control mutants or boundary checks against the donor head or its port.
  - The only published parent-side build with #32 records a budget miss. Round 25 STOP 6778599191 item 5: "With tsn-c-stack#32 at the pin the arm is 132 bytes over its granule (123,012 bytes), so the pin move owes it 132 bytes" (the 8x8/2if `answering-every-port` arm). Round 26 does not restate it.
- Impact: review focus item 4 (the parent consumer gates still pass at this donor head) cannot be confirmed.
- Required outcome: one of the following.
  - Published receipts of the parent's firmware gates (at least `firmware-unit`, `firmware-control-mutants`, `firmware-boundary` and the budget harness's image build with its ROM granule check), built with this head's ACMP (its port to the pin) and rc 0.
  - Or a public manager ruling that defers the parent consumer bar for this donor PR to the pin move, with the 132-byte ROM granule debt tracked on an issue.
- Verification: the receipts or the ruling linked on PR #34.

### R823-1-R1 (RESIDUE)
- Where: `docs/VERIFICATION.md:24`.
- Defect: "The 18 changed-sink walk plants each drop one mark". `walk-mark-word-zero` and `walk-marked-word-zero` address the wrong mark word instead.
- Exact fix: "The 18 changed-sink walk plants each drop one mark or address the wrong mark word, built at 33 sinks ...".

### R823-1-R2 (RESIDUE)
- Where: PR #34 body, "Tests and plants", "18 new plants, one for each mark site and the two mark-word reads".
- Defect: `walk-mark-word-zero` plants the write in `mark()`, not a read.
- Exact fix: "18 new plants, one for each mark site, the mark word's write and its read".

### R823-1-R3 (RESIDUE)
- Where: PR #34 body, "Validation", "the host stands in with the pinned GoogleTest/GMock 1.14.0, Clang 18.1.3 and clang-tidy 18.1.3".
- Defect: the author's `clang-sanitizers-configure.log` identifies the C and C++ compilers as Clang 23.1.4. The validator calls `clang`, and the pinned directory provides only `clang-18`. Hosted CI at the exact head ran the CI image's own compiler and passed.
- Exact fix: append "; the Clang sanitizer configuration ran under the host's Clang 23.1.4".

### Suggestions (do not affect the verdict)
- R823-1-S1 (Tests):
  - At 1, 8 and 32 sinks the entry mix keeps the owed queue mostly full. At 8 sinks there are 604 sends in 6,000 steps, against 3,503 in 8,000 at 33 sinks with room always available (`receipts/differential-head-vs-main.log`).
  - Three plants are caught at one size only: `walk-expiry-unmarked` and `walk-kind-unmarked` at 33, `walk-probe-left-unmarked` at 32. The reviewer's multi-seed run kills each at several sizes.
  - Suggestion: several seeds per size, or a poll bias while frames are owed.
- R823-1-S2 (Robustness): `dirty_if` is a `uint32_t` set by `1u << interface`. A `_Static_assert(ACMP_MAX_INTERFACES <= 32u, ...)` next to #31's two asserts would tie its width to the configuration, as #31 did for the release mask.
- R823-1-S3 (Tests): the test's reference is the head's own core with every mark forced. It shares the merged release loop and every line that does not depend on marks with the core under test. The reviewer's differential against `main`'s real `src/acmp.c` (`scripts/trace_walk.cpp`, `scripts/differential.sh`) is literally "the old and the new finish()" of acceptance item 1. A comparable cross-version check could be kept beside the in-tree test.

## Prior public review findings
At this head PR #34 has no prior public review findings: its only comments are the two review-start notices, and it has no review objects or inline comments. Issue #32 has no comments. Nothing is carried over or resolved.

## Lens evidence

### Conformance (CLEAN)
- `src/acmp.c` delta read in full: `mark()`/`marked()` (`:209-219`); the skips in `publish()` (`:225`), `rearm()` (`:423`), `admit()` (`:514`) and `finish()` (`:536`); the clear (`:553`); and the 15 mark sites.
- Every field these walks compare (`bound`, `started`, state and stream, binding, `probing`, `acmp_status`, `tk_failed`, `change_owed`, the sink's timer and ADP deadlines, `timer_armed`) changes only after a mark of its sink or interface in the same entry, or in an entry whose marks a later completion consumes (`acmp_restore_binding` and `acmp_restore_rollback` then `acmp_open`).
- Refused entries (`room()`, `enter()` reentry, `impossible`, unknown sink, lock refusal, GET_RX_STATE, talker commands) mark nothing and change no compared field.
- Walk order stays ascending, so the per-controller order of responses and notices is unchanged.
- Executable: `scripts/differential.sh` built `main`'s `9deb0ddb` core and the head's core at 33 sinks under `-fsanitize=shift,undefined` and drove both with the test's generator (seed 0 is the test's own sequence). Cases: 1, 8, 32 and 33 sinks, 60 seeds each, in two mixes: the test's, and a lifted one in which commands reach every sink, room is withdrawn at 33, and restores may precede their `acmp_open` by several entries. Both mixes include entries that change a sink twice before completion and sinks unbound while frames are owed. 480 cases, 0 divergent: every send byte, clock read, timer, admission, publication, SRP call, persist and change report identical (`receipts/differential-head-vs-main.log`, rc 0).
- Control: the same driver flags `walk-expiry-unmarked`, `walk-kind-unmarked` and `walk-probe-left-unmarked` (`receipts/mutants/probe-results.json`).

### RTL / implementation (CLEAN)
- The mask is sized from `ACMP_MAX_SINKS`: `ACMP_DIRTY_WORDS` (`include/acmp.h:167`) uses #31's formula. Every new mask access indexes `k / 32u` with a shift below 32. The release loop reads `o->release[k / 32u]` (`src/acmp.c:1311`).
- The release loop rewrite (`if (bit) { mark; change_owed--; }`) gives the same uint8 arithmetic as `main`'s subtraction.
- `mark()` in `acmp_restore_binding` follows `sink_reset()`, so the interface bit uses the configured interface.
- Merge: `git diff 9deb0ddb..HEAD -- src/acmp.c` removes only the one release-loop line. `git diff fa31d4c8..HEAD` changes only #31's content, the loop and the shared 33-sink target. `tests/test_acmp_wide.cpp` and `scripts/check_conditionals.py` are byte-equal to `main`, and `tests/test_acmp_walk.cpp` is byte-equal to `fa31d4c8`. #31's `_Static_assert`s are kept.
- Bare-metal: the reviewer's `baremetal.py` run is rc 0, Debug and Release. The core imports are equal to `main`'s (`__mulsi3`, `__umodsi3`, `ctrl_reentry_assert`, `memcpy`, `memset`, `port_assert_failed`; Release without `__mulsi3` and `port_assert_failed`) (`receipts/rv32/results.json`, `receipts/baremetal.log`).

### Robustness (UNCLEAN: F1, F3)
- Reentry is still refused before any mark. `acmp_timer_expired` with an out-of-range interface returns before it marks.
- Marks left by restores survive to the next completion. The lifted mix exercises this with intervening entries: no divergence.
- Open: F1 (second-word paths unguarded) and F3 (parent consumer unevidenced; a published 132-byte ROM granule overrun with #32).

### Tests (UNCLEAN: F1, F2, F3)
- Reviewer run of the Linux `run:` step, `python3 scripts/validate.py --work build-validation-r2 --jobs 12 --graphs`, on a clean clone of the exact head:
  - 26 of the 27 gates it ran are rc 0, among them `entity-golden`, `entity-controls`, `boundary`, `needles`, `assertion-templates`, `dependencies`, `comments`, `conditionals`, `port-contracts`, `acmp-cache`, `registration-controls`, `license`, `traceability`, `test-inventory`, `coverage-controls`, `privacy-selftest`, `privacy`, `gcc-*`, `coverage`, `static-analysis`, `mutation`, `mutation-controls` and `graphs` (`receipts/validate/gates.json`).
  - `clang-sanitizers-build` rc 2 is environmental. The pinned Clang 18.1.3 cannot parse this host's libstdc++ 16 headers (`receipts/validate/clang-sanitizers-build.first-errors.txt`), so the validator's own rc is 1.
  - The same configuration under the host Clang 23.1.4, the compiler the author's receipt also shows, is rc 0 with 10/10 CTest binaries, `acmp_walk` among them (`receipts/sanitizers-standin.log`).
- Mutation: `{"CAUGHT": 470, "ESCAPED": 0, "ERROR": 0}`. The driver grades CAUGHT only when every listed test fails with its needle inside the instrumented assertion message (`scripts/mutation.py:96-109,249`). So each of the 18 `walk-*` plants fails by its own words ("the changed-sink walk makes the full walk's calls").
- The two plants changed on both sides: `acmp-unbind-srp-after-response` is CAUGHT by `AcmpCore.A3UnbindInEveryState`, and `acmp-first-owed-releases-every-change` by `AcmpCore.A19TwoOwedResponsesForOneSinkReleaseTogether`. #31's re-anchored `acmp-wide-release-loop-word-ignored` and `acmp-wide-release-loop-word-off-by-one` are CAUGHT by their `AcmpWide` tests (`receipts/validate/mutation-results-summary.json`).
- Coverage: `src/acmp.c` 847/847 lines and 436/436 branches (`receipts/validate/coverage.log`).
- Plant table merge (`scripts/plant_merge.py`, `receipts/plant-merge.txt`):
  - 444 at the merge base, 462 on the draft, 452 at `main`, 470 at the head; no duplicates; nothing lost from either parent.
  - Both parents' orders are kept, and the last three are the entity plants.
  - 13 base plants re-anchored by the walk keep their defect, and the 3 structural re-anchors on the merged loop are the same defects (`receipts/plant-defects.txt`).
  - `acmp-timer-port-called-every-time` and `acmp-publish-stream-cache-stale` move to the new A17 and A31 assertions (`receipts/plant-delta.txt`).
- Hosted at the exact head: `quality` and `bare-metal` both completed with success on the push run 42972778067 and the pull_request run 42972806247. Every step, including "Validate the portable cores" and "Validate the freestanding cores", concluded success (`receipts/hosted-ci-jobs.json`). The manager owns hosted acceptance.
- Acceptance item 4: the author's benchmark source, rebuilt by the reviewer against `main` and the head at `ACMP_MAX_SINKS=32u` on one pinned CPU, gives 558 to 124 (8 sinks) and 2,325 to 279 (32 sinks) at -O2, and 992 to 217 and 3,875 to 465 at -Os. That is within about 3 % of the PR's table (`receipts/bench-rerun.txt`). Host TSC only. The PR states no parent target figure; the parent's graded effect is the manager's.
- Open: F1, F2 and F3.

### Docs (CLEAN; RESIDUE R1 to R3)
- Read: ACMP-13 in `docs/REQUIREMENTS.md:38-49`, `docs/requirements.json`, `scripts/requirement_records.py`, the PORTING storage rows and "ACMP changed-sink walk" section, `docs/VERIFICATION.md:24`, the CHANGELOG entry, and the regenerated `docs/TESTS.md` and `docs/TRACEABILITY.md` (their generator gates are rc 0).
- The PORTING list of marking entries matches the 15 mark sites in the code.
- Comment rule: the delta's new source comments are `// REQ: ACMP-13` (with ACMP-10, -09, -05 in the test) and one `scripts/mutation.py` comment naming #31 and #32. No lane labels, lane names, review rounds, reviewer IDs or issue-comment IDs. The `r630-3-*` plant names in `docs/TESTS.md` rows are existing names moved by renumbering, not new instances.
- Privacy: the PR body and delta name no private host, tool or model.
- Commits are one-line subjects with no body, trailers or footer, as CONTRIBUTING requires.
- R1 to R3 are wording only.

## Reviewer-owned ledger

| lens | CLEAN/UNCLEAN | examined artifacts | covering round | exact head |
|---|---|---|---|---|
| Conformance | CLEAN | `src/acmp.c` full read (delta and every compared field); IEEE 1722.1-2021 8.2 and Milan v1.2 5.5.3.5 as cited; 480-case differential of `main`'s real core against the head's (`receipts/differential-head-vs-main.log`) | R823-1 | 9043b926532dc4ffb57218ee0eebca7564262289 |
| RTL / implementation | CLEAN | `include/acmp.h`, `src/acmp.c`, the merge diffs against both parents, bare-metal Debug/Release imports (`receipts/rv32/results.json`) | R823-1 | 9043b926532dc4ffb57218ee0eebca7564262289 |
| Robustness | UNCLEAN (F1, F3) | refusal, reentry and restore paths; second-word fault probes (`receipts/mutants/probe-results.json`); parent pin and #665 public receipts | R823-1 | 9043b926532dc4ffb57218ee0eebca7564262289 |
| Tests | UNCLEAN (F1, F2, F3) | `tests/test_acmp_walk.cpp`, A17/A31 additions, `tests/mutations.json` merge, validate run, sanitizer stand-in, mutation 470/0/0, coverage, hosted job steps, benchmark rerun | R823-1 | 9043b926532dc4ffb57218ee0eebca7564262289 |
| Docs | CLEAN (RESIDUE R1-R3) | REQUIREMENTS, requirements.json, PORTING, VERIFICATION, CHANGELOG, TESTS, TRACEABILITY, PR body, commit messages, comment rule, privacy | R823-1 | 9043b926532dc4ffb57218ee0eebca7564262289 |

## Real limits
- The host is not the CI image:
  - GCC 16.2.1 and libstdc++ 16, cppcheck 2.22.0, a RISC-V `riscv64-elf` GCC 16.2.0 and QEMU 11.1.3.
  - The pinned GoogleTest/GMock 1.14.0 and clang-tidy 18.1.3 were used. The pinned Clang 18.1.3 served the gates that call `clang-18`.
  - The Clang sanitizer configuration ran under the host Clang 23.1.4 as a stand-in.
  - The campaign ran with `--jobs 12`.
  - The dependency install steps were not run.
- The reviewer's validate run's own rc is 1, solely from the environmental `clang-sanitizers-build`. The exact-head hosted `quality` job, run with the CI image's compiler, is the source of the in-image result.
- Hosted job logs were not downloaded: only job and step conclusions were read.
- The reviewer's differential reuses the in-tree test's entry generator, widened, so it shares that generator's view of which entries matter.
- No parent (milan-fpga) gate, bank or image was run by the reviewer, as this review's scope rules out. The parent conclusions rest on public receipts and comments.
- The benchmark is a host x86 TSC measurement, not the RV32 image.
- Physical calibration NOT RUN. No hardware proof, and no field skip counts as one.
- No manager source bank is claimed or inferred at this head.

## Pending manager duties
- Hosted and act acceptance at the exact head. Observed: hosted `quality` and `bare-metal` success on both events.
- The current-dev merge candidate's builder and native banks at the merge turn (source base `9deb0ddb`; milan-fpga live dev `46c971fa0a09e2c8ca21acb95769defdc06c3068`), receipts linked on the PR.
- F3's parent consumer bar: either receipts of the parent's firmware gates with this change, or a ruling deferring it to the pin move, with the 132-byte ROM granule debt tracked.
- The second independent review, and carrying R1 to R3 to the residue checklist.

## Packet
- `scripts/`: `trace_walk.cpp` and `differential.sh` (the old-versus-new differential), `probe_mutants.py` (fault probes; restores the probe tree's `src/acmp.c` and checks its hash), `plant_merge.py`, `plant_delta.py`, `plant_defects.py` (plant table merge analysis), `launch.sh`, `shim-clang.sh`, `shim-clangxx.sh`, `sanitizers_standin.sh` (environment; set `TSN_TOOLS` to the pinned tool root), `bench_finish_author_copy.c` (the author's benchmark source, unchanged).
- `receipts/`: every receipt cited above. Host paths are replaced by `<packet>`, `<clone>`, `<tools>`, `<slots>` and `<home>`.
- Integrity after the probes (`receipts/integrity.txt`):
  - the review clone is at `9043b926`, tree `a77b293b`, with a clean worktree, index equal to HEAD, and no untracked or ignored files;
  - `git ls-files -s` and `git ls-tree -r HEAD` give the same mode, blob and path digest;
  - there are no gitlinks and no `.gitmodules`, so no submodules are required;
  - every probe tree is at head with no tracked change.

R823-1 FINISHED
