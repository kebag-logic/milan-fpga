[R947] POSITIVE - exact head 6841c5e3be421dc59900b392b51cbc3c0a110471

Round R947-2 is the internal independent review of PR #1019. The PR relates to issue #1008 and does not close it. This round is a delta re-review.

- Head: `6841c5e3be421dc59900b392b51cbc3c0a110471`, tree `dbdf163a5c411ec9cb657608a0cb7535170d6261`.
- Previously reviewed head: `5b5b0765`.
- Source base: `c34e7d8b06739a22cc79997a9a1f4cbcd9bd0350`. Live dev at review time: `e275d7950ef3385753e6a15d2e191ba855b171ed`.

All five lenses were applied to the delta, and every prior finding was checked at its cause. No BLOCKER, MAJOR or MINOR finding is open. Two SUGGESTIONs and one RESIDUE are recorded below.

## Reconstruction

**Authorities read:**
- AGENTS.md and CONTRIBUTING.md (by reference).
- The issue #1008 body: objective, scope and acceptance 1-3. It asks for windows of at most about 1277 s on two runs, identical verdicts and receipts, and no raised limit.
- The PR body at the head.
- `docs/testing/CI_WORKFLOWS.md`: the fast-legs paragraph at :184-199, the projection table at :3453-3493 and the workflow-total paragraph at :3506-3511.

**Delta:** `5b5b0765..6841c5e3`. Five first-parent commits plus one merge:

| Commit | What it changes |
|---|---|
| `d13db4c7` | The count contract and its arms |
| `e1793704` | The dispatch proof through `campaign_leg` |
| `d1b42005` | The docs figure and the generator comment |
| merge `5780feb8` | Merges dev-soft-core `4df125b8` (PR #1016) |
| `2f5f5d31` | The `gptp_shadow` re-key and the 27 Verilator rows |
| `6841c5e3` | The boundary-judge listing |

**The merge is clean.** `git merge-tree --write-tree d1b42005 4df125b8` gives `107952d3`, which is exactly the merge commit's tree. So there is no hand resolution.

The merge brings #1016's content: gPTP pin 3ce71b76, tsn-c-stack a795471c, three control defects, and the `gptp_shadow`/`gptp_plane` suite changes. That content is reviewed on its own PR. This round judges only what #1019 depends on from it: the control table size, the `gptp_shadow` timing, and the gitlinks.

The diffs and the evidence packet were read before any prior finding.

**Evidence packet:**
- Location: `review-evidence/cicd4-r2/` at commit `9141378262c3331229a56c23d2c2fbb14cd87b48`, branch `cicd4-review-evidence`.
- All 71 files match `MANIFEST.json`. None is unlisted and none is missing. Six entries are marked as path-redacted. Receipt: `receipts/packet_verify.log`.
- Limit: the packet is protected by a hash manifest in a published commit. It carries no cryptographic signature.

## Findings

### S1 - SUGGESTION - Tests, Robustness - the dispatch proof still does not drive `main()`'s use of the mapping

**Artifact:**
- `sw/firmware/ctrl/test/test_ctrl_firmware.py:396`, where `main()` calls `campaign_leg(args)`.
- `sw/firmware/ctrl/test/test_ctrl_firmware_shards.py:42`, where the proof calls `module.campaign_leg(args)` itself.

**Evidence:** the reviewer's probe `scripts/probe_dispatch.py` ran in a disposable clone at the head.

| Probe | Planted change | Proof result | Partition `main()` hands leg 1/4 of phase 1 | Receipt |
|---|---|---|---|---|
| Head | none | passes for phases 1/4, 2/4 and 3/4 | `[1, 4]` | `receipts/probes/dispatch_head.log` |
| M1 | `campaign_leg`'s body emptied | refuses control and AECP by duplicate defects; SRP correctly still passes, since it reads `campaign_shard` itself | n/a | `dispatch_mapping_noop.log` |
| M2 | only `main()`'s call at :396 deleted | passes for all three phases; `test_ctrl_firmware_shards.py` also passes | `None` | `dispatch_main_call_dropped.log`, `shards_gate_main_call_dropped.log` |

**Impact:** with M2, every control and AECP leg would plant its whole table. That is a superset, so no verdict is lost. The leg would then overrun its 30-minute limit and fail, so this fails closed.

This is the residual part of R947-1 F4. The PR body's "(`campaign_leg`), so dropping that mapping is refused too" is true of the function's body (M1), but not of its call site (M2).

**Optional outcome:** have the proof drive `main()` with `run_selected` intercepted, as the probe does, and assert the partition each leg is handed. Alternatively, word the PR line as "so emptying that mapping is refused too".

**Verification:** re-run M2; it should be refused.

### S2 - SUGGESTION - Robustness, Tests - the contract matches only the full option spelling, and the driver accepts abbreviations

**Artifact:**
- `scripts/ci_events.py:1377` (`CAMPAIGN_SHARD_RE`) and `:3937-3946`.
- The driver's default `argparse` parser at `test_ctrl_firmware.py:348`.

**Evidence:**
- `python3 sw/firmware/ctrl/test/test_ctrl_firmware.py --campaign-shar 0 4` is parsed as `--campaign-shard`: the error is the campaign-shard rule's, not "unrecognized".
- For the three campaign jobs this cannot hide a wrong COUNT. The contract requires exactly one full-spelling match, so a lone abbreviated command yields `[]` and is refused.
- In an undivided job, an abbreviated campaign shard would escape the "runs no `--campaign-shard`" item. The driver refuses `--campaign-shard` outside phases 1-3, so this has no current failure path.

**Optional outcome:** set `allow_abbrev=False` on the driver's parser, or widen the pattern to `--campaign-sh\w*`.

### RES1 - RESIDUE - Docs - the PR body's "For each matrix" list mixes per-matrix, per-campaign and single arms

**Artifact:** PR #1019 body, under "Planted failures", the bullet "**Contract.** For each matrix, the event self-test plants: ...".

**Evidence:** at the head, `ci_events._fast_leg_arms()` returns 35 arms (`scripts/ci_events.py:8473-8489`):
- 4 for each of the 5 matrices;
- 4 for each of the 3 campaign jobs;
- 1 undivided-job arm;
- 2 judge arms.

The list presents all of these as per-matrix. This is wording only: the "35 defects" figure elsewhere in the body is correct.

**Exact fix:** "For each matrix, the event self-test plants a dropped leg, `fail-fast: false`, the key left to its default and the aggregate not reading the legs. For each campaign job it plants the command's count one more and one fewer, leg 0 everywhere, and the phase run twice. It plants once each a campaign leg in an undivided job, a judge that does not need its legs, and a raised legs limit."

## Prior public findings, resolved or retained at this head

These were read after the independent pass above was complete. The sources are R947-1 and R948-1 at `review-evidence/cicd4-r1/reviews/`.

### R947-1 F1 (MINOR: Tests, Robustness): RESOLVED

The cause was that the command's COUNT was not held to its matrix. The contract now does this at `ci_events.py:1376-1378` and `:3937-3946`, with 13 new arms at `:8473-8489`. The generator self-test does it too, at `ci_fast_legs_selftest.py:111-116`.

The reviewer's own control (`scripts/probe_count.sh`) makes the generator emit COUNT+1 and then COUNT-1, and regenerates the workflows:
- `ci_events.py --check` refuses all three campaign jobs by name each time.
- `ci_fast_legs_selftest.py` fails at the new assertion (line 114). This was run with submodules linked read-only.
- After restoring, `--check` passes.

Receipts: `receipts/probes/count_plus1.log`, `count_minus1.log`, `fast_legs_selftest_count1.log`, `fast_legs_selftest_count-1.log` and `fast_legs_selftest_unplanted_probe.log`.

At the head, `ci_events.py --selftest` passes with 2409 contract items and 6174 arms. Its log shows all 13 new arms caught (`receipts/head-gates/ci_events_selftest.log`). There are 35 fast-leg arms in total.

### R947-1 F2 and R948-1 D1 (MINOR: Docs): RESOLVED

`CI_WORKFLOWS.md:3506-3511` now names `docs-gates-1` at 1302 s as the slowest docs worker, which matches the table row at :3454. It states that this is 26 s over the 1276-s budget and stays open on #1008.

Recomputed by the reviewer:
- 1302 + 60 + 60 + 120 + 30 = 1572 s, which is 26.2 minutes and 228 s inside 30 minutes.
- The superseded figure is kept as history: 1395 + 270 = 1665 s, 27.8 minutes.

### R947-1 F3 (MINOR: Docs): RESOLVED

`scripts/ci_gate_workflows.py:28-32` now cites the table's rule and gives:
- worker 3 at 1237 s, which is 479 + 373 + 109 = 961 s of steps plus 276 s of setup;
- `docs-gates-1` at 1302 s.

Both agree with the table rows at `CI_WORKFLOWS.md:3454` and `:3456`. Worker 4 also agrees: 603 + 276 = 879 s.

### R947-1 F4 (SUGGESTION: Tests): PARTLY RESOLVED, retained as S1

The mapping now lives in one function, used by both the driver and the proof. Emptying it is refused (M1). Dropping its call in `main()` is not (M2).

### R948-1 T1 (MINOR: Conformance, Tests, Docs): RESOLVED

The five original receipts are published with `SHA256SUMS`, and all five check OK.

| Leg | Head | Tree | Rows | Exit | Every row ok |
|---|---|---|---|---|---|
| 0 | `530149b5` | `08e15b7d` | 0 | 0 | yes |
| 1-4 | `530149b5` | `08e15b7d` | 41 each | 0 | yes |

That is 164 arms in total.

The reviewer replayed the union independently, without the author's script. It ran in a scratch clone at `530149b5dd1a94cc5011b17c9bb28af54bc79be3`, whose tree `08e15b7d` matches the receipts. `sw/mailbox` is byte-equal between that commit and the head.
- The union returns rc 0 with "0 of 57 rule(s) no arm proves".
- Its output is byte-identical to the author's `replay-union.log` (`receipts/probes/census_union_replay_530149b5.log`).
- Three plants of the reviewer's own are each refused (`scripts/census_plants.py`, `receipts/probes/census_own_plants.log`):
  - a failed row in leg 3;
  - another tree in leg 1;
  - a short selection in leg 2.

## Delta checks beyond the prior findings

**`gptp_shadow` re-key, 517 to 679 s (`scripts/suite_shards.py:108`).**
- `suite_shards.py --measure` over the published hosted log of run 45755846909, shard 22/27, gives `"gptp_shadow": 679` (`receipts/head-gates/measure_gptp_shadow.log`). The serial log shows `cls` passing at 05:18:46.81 and `gptp_shadow` at 05:30:04.92.
- At `d3cb3cf1`, the measured content, `tb/verilator/gptp_shadow` is tree `db12089e` and the `gptp-processor` gitlink is `3ce71b76`. Both are equal at the head.
- Limit: the 672-s figure from run 45735453538 is not in the packet. It is the smaller of the two, so it does not decide the key.

**The 27 Verilator rows (`CI_WORKFLOWS.md:3468-3494`).** `scripts/project_workers.py` recomputes every worker with the head's `suite_shards.balance(…, 27)` (`receipts/head-gates/project_workers.log`).
- All 27 rows match: projection, limit and margin.
- The largest regular worker is 1275 s, on workers 0 and 25, against a budget of 1276 s. The dedicated worker 26 is 1530 s against its 2160-s limit.
- `gptp_shadow` is re-dealt to worker 16.
- #979's two suites remain on workers 14 and 15, as :3505 states.

**Verdict identity after the merge.**
- The control table grows from 844 to 847 defects. Interleaved over the 4 legs it deals 212, 212, 212 and 211.
- AECP stays at 398 defects, dealt 199 and 199. SRP stays at 662.
- At the head, `test_ctrl_firmware_shards.py` reports 2008 invocations with shard sizes [98, 848, 399, 663].
- The PR body states that the serial comparisons are at the pre-merge base.

**Workflows unchanged by the merge.**
- `git diff 5b5b0765 HEAD -- .github` is empty, and so is the merge against its first parent.
- `ci_gate_workflows.py --check` returns rc 0 at the head. This is the regeneration check.

**Boundary fix (`ctrl_configs.py:171-172`).**
- The hosted firmware-boundary log at line 529 refused exactly `scripts/ci_fast_legs_selftest.py`.
- The reviewer's reproduction of the judge's text half (`scripts/boundary_scan.py`) gives:
  - "none" at the head;
  - `['scripts/ci_fast_legs_selftest.py']` with the new entry removed.
- Reading `ci_fast_legs_selftest.py:28-58` supports the "compiles nothing" claim: every campaign and `lwsrp_pin_arms` is stood in for, and the invalid-argument calls exit 2 before any build.

**Comment rule.** The 91 lines added by the PR's own commits contain no lane label, lane name, review round, reviewer ID or issue-comment ID. New comments cite #1008, and `_fast_leg_arms` also cites REQ-VER-01 and REQ-VER-04.

**PR text.** The body says "Relates to #1008" and lists what remains open: `docs-gates-1` at 1302 s, `elaborate-gates-0` and `-1`, the cache-miss jobs, and rtl-full Yosys shard 0/4. It names no private person, tool or model.

## Lens results (artifact-specific)

[R947] PASS Conformance - `CI_WORKFLOWS.md:195-197,3454,3506-3511`; `scripts/ci_events.py:3937-3946`; PR body "Not in this PR"; `receipts/probes/census_union_replay_530149b5.log` - The delta meets acceptance 2 (verdicts and receipts) and acceptance 3 (no `.github` change in the delta; the legs' 30-minute limit is held by the contract). Acceptance 1 is honestly partial: one run is measured, and `docs-gates-1` at 1302 s is disclosed as open. The PR therefore relates to #1008 rather than closing it, which is correct.

[R947] PASS RTL - `git merge-tree` result equal to merge tree `107952d3`; gitlinks `gptp-processor` 3ce71b76 and `third_party/tsn-c-stack` a795471c, both equal to `4df125b8`; `receipts/head-gates/project_workers.log` - The PR's own commits change no HDL, firmware or CDC. The scheduling architecture keeps every regular worker within 1276 s and the dedicated worker within its limit. The merge content is #1016's and was integrated without hand resolution.

[R947] PASS Robustness - `receipts/probes/count_plus1.log`, `count_minus1.log`, `dispatch_mapping_noop.log`, `census_own_plants.log`, `boundary_entry_removed.log` - COUNT±1, an emptied mapping, a failed census row, another tree, a short selection and a removed boundary entry are each refused. COUNT below the matrix fails closed in the driver. S2 is a hardening suggestion only.

[R947] PASS Tests - `receipts/head-gates/ci_events_selftest.log` (13 new arms caught); `receipts/probes/fast_legs_selftest_count1.log` (line 114); `receipts/probes/dispatch_head.log` - The new arms and the self-test fail for the defect they claim to catch. Each was shown by a reviewer-planted defect, not only by the author's. S1 is optional.

[R947] PASS Docs - `CI_WORKFLOWS.md:3468-3494` (27 rows recomputed), `:3506-3511` (arithmetic recomputed); `scripts/ci_gate_workflows.py:28-32`; `receipts/head-gates/docs_check.log`, `check_doc_style.log`, `check_doc_paths.log` - The figures are consistent with the table and with the generator. RES1 is wording residue and carries no figure.

## Reviewer-owned ledger

| Lens | CLEAN/UNCLEAN | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | issue #1008 acceptance 1-3; PR body; `CI_WORKFLOWS.md:195-197,3506-3511`; census receipts replayed at `530149b5` | R947-2 | 6841c5e3be421dc59900b392b51cbc3c0a110471 |
| RTL | CLEAN | delta file list (no HDL in the PR's own commits); merge-tree equality; gitlinks; `suite_shards.balance` loads | R947-2 | 6841c5e3be421dc59900b392b51cbc3c0a110471 |
| Robustness | CLEAN (S2 optional) | `ci_events.py:1376-1378,3937-3946`; `test_ctrl_firmware.py:266-271,396`; `census_legs.py` union under reviewer plants; `ctrl_configs.py:171-172` | R947-2 | 6841c5e3be421dc59900b392b51cbc3c0a110471 |
| Tests | CLEAN (S1 optional) | `ci_events.py:8473-8507`; `ci_fast_legs_selftest.py:111-116`; `test_ctrl_firmware_shards.py:39-42`; the reviewer's count, dispatch, census and boundary probes | R947-2 | 6841c5e3be421dc59900b392b51cbc3c0a110471 |
| Docs | CLEAN (RES1 residue) | `CI_WORKFLOWS.md:195-197,3453-3494,3506-3511`; `ci_gate_workflows.py:28-32`; PR body; added-line comment scan | R947-2 | 6841c5e3be421dc59900b392b51cbc3c0a110471 |

## Execution, limits and pending manager duties

**Run at the exact head in this clone (rc 0 unless noted; `receipts/head-gates/`):**
- `ci_events.py --check`: 2409 items.
- `ci_events.py --selftest`: 2409 items and 6174 arms.
- `ci_gate_workflows.py --check`.
- `ci_fast_legs_selftest.py`.
- `suite_shards.py --selftest`.
- `test_ctrl_firmware_shards.py`.
- `docs_check.py`, `check_doc_style.py`, `check_doc_paths.py`, `check_py_idiom.py` and `check_hygiene.py --check`.
- `suite_shards.py --measure` and `project_workers.py`.

A first launch used Python's isolation flag, which broke the scripts' sibling imports. It was discarded and is not published.

**Not runnable here:**
- `check_em_dash.py` and `gen_toc.py --check` exit 2 because the pinned Markdown renderer is not installed, and shared installs are not allowed. The author's receipts at the head show both passing.
- `check_doc_paths.py` reported "2 allowlisted" here against the author's "1". Both pass. The difference is probably environmental, since the `external` submodule is not initialised in this clone. It was not investigated further.

**Probes:** run in disposable clones under `scratch/`, with submodules linked read-only from this clone. Each planted file was restored with `git checkout`.

**Clone state:**
- The worktree and index match HEAD. The session-start status was clean, and the index hash `63a4c18e…` is equal before and after removing this review's untracked artifacts.
- The tracked mode/blob listing equals `git ls-tree -r HEAD`.
- The gitlinks are unchanged.
- The untracked `dispatch-build/` and `scripts/__pycache__/` created by this review's runs were removed.

**Not run:**
- the full mutation campaigns, which compile firmware;
- any parent, PP, gPTP, Yosys or builder bank;
- Docker/act;
- hardware.

Physical calibration was NOT RUN. No field skip is hardware proof.

**Source-head execution evidence:** the author's published gate receipts, plus the reviewer's focused gates and probes above. No manager source bank ran at this head, and none is claimed.

**Hosted state (informational, not acceptance; `receipts/hosted-exact-head-runs.tsv`, read 09:38Z):**
- rtl-fast 45791594690 in progress;
- docs 45791594446 queued;
- elaborate 45791594441 queued;
- rtl-full 45791594648 pending.

No exact-head job had executed when this was read.

**Pending manager duties:**
- Build the current-dev merge candidate (source base `c34e7d8b`, live dev `e275d795`) and run the builder and native banks at the merge turn.
- Own exact-head hosted and act acceptance. This includes `firmware-boundary` at this head, the job that failed at `5b5b0765`, and the second run that #1008 acceptance 1 asks for.
- Carry RES1 to the residue checklist.
- Keep #1008 open for the jobs the PR lists as still over budget.

R947-2 FINISHED
