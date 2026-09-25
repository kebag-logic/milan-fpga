[R296] POSITIVE - exact head 6e4a3b420e055ef7529ceb16bb2ab5be93c34487

# R296-3 internal independent review: issue #551 / PR #553 (round 4, delta)

- Head: `6e4a3b420e055ef7529ceb16bb2ab5be93c34487`, tree `f4e0bc482e7ee734f9ff50c627cedfbc89beacad`, one commit on `f219a5ed`.
- Source base: `864b36f5e9450ef64f75ca3f0d68c44330e447d7`.
- Scope: delta review of `f219a5ed..6e4a3b42`. Round R296-2 covered `f219a5ed` in full.
- Assignment: issue 551 comment 5833406989. It covers two items, R296-2 N1 (= R297-2 F1) and R296-2 S2. It says "No other change".

## Verdict summary

The delta changes exactly two text files, and only the lines assigned:

- `tests/features/milan_streaming_licence.feature`: three comment lines.
- `tb/verilator/milan_dp/README.md`: one table cell.

The modes stay 100644 and no step text or assertion changes (`receipts/delta.raw`, `receipts/delta.diff`).

**N1 is closed.** The new scenario comment makes three claims, and each one holds:
- The real grant waits for the current TSpec. The README states the same at `README.md:424-428` and the traceability page at `docs/traceability/ieee8021q.md:67`.
- Processor #112 supplies this. The processor issue is CLOSED. Its fix `73a5478` is in the processor pin `990f9652`, and the lane pin `a8f8ce81` contains it.
- The pin was adopted through #508. PR #560 closes #508 and carries the pin commit `4072d389`.

**S2 is closed.** I reran the pre-#112 control independently and it matches the new README cell exactly: `[I]`=28, `[J]`=6, 34 of 415. The same fixture at the restored pin gives 415/0.

There is no open BLOCKER, MAJOR or MINOR. All five lenses are clean at this head.

## Findings

None open. One optional note:

**S1 - SUGGESTION - Docs - `tb/verilator/milan_dp/README.md:468` - the six `[J]` failures are not located.**
- The six `[J]` failures come from three of the four source/phase cases, two checks each. Source 1 at phase 0 passes. The two checks are "the optimistic window actually raised ACTIVE" and "ACTIVE rose within three admission rounds" (`receipts/crflic_ctl_pin_7a47f578.log:649-650,743-744,966-967`).
- Naming them would let a re-runner match the receipt line by line. The total is already correct, so this does not affect coverage.

## Assigned verification items

| item | result | evidence |
|---|---|---|
| The comment says the grant waits for the current TSpec (processor #112, adopted through #508), with no residual window and no pending fix | MET | `milan_streaming_licence.feature:92-94`. Processor #112 is CLOSED. `73a5478` is an ancestor of `a8f8ce81` and `990f9652`. PR #560 "Closes #508" and contains `4072d389` (the `a8f8ce81` pin). The `[I]` wording matches `sim_crf_licence.cpp:59-61,1086-1088`. |
| Step text and assertions unchanged | MET | Every changed line in the feature starts with `#`. `milan_streaming_licence_steps.py` is not in the delta (`receipts/delta.raw`). The worktree blob equals the HEAD blob (`receipts/restore_verification.txt`). |
| `grep -rnE "Residual\|pending fix\|previous slope" tests/` is empty | MET | rc 1, no output. Outside `tests/`, the only hits are unrelated (a history page, and a bench comment at `sim_crf_licence.cpp:1087` that correctly states that no previous slope may decide the grant). |
| `behave` passes all scenarios | MET | The licence feature passes 5/0 (`receipts/behave_licence_head.log`). The full suite passes 14 features, 344 scenarios and 1739 steps with 0 failures (`receipts/behave_full_head.log`). |
| The BDD mutant script catches all four mutants | MET | `scripts/bdd_mutants.py` is my portable reimplementation of the public round's script. It runs on a copy under scratch. Both clean arms pass 5/0. ACTIVE-only, raw-grant-only, OR and extra-term each give rc 1, 4/1, with the exact-composition signature (`receipts/bdd_mutants.log`, `receipts/bdd-*.log`). |
| README states 28 `[I]` + 6 `[J]` = 34 for the pre-`a8f8ce81` control, and a rerun matches | MET | `scripts/crflic_control.sh` builds the head tree with the processor at `7a47f578` using the pinned 5.050 simulator. The result is 415 checks, 34 failures: I=28, J=6 (`receipts/crflic_ctl_pin_7a47f578.log`, `receipts/crflic_ctl_fail_by_section.txt`). The same script at `990f9652` gives 415/0, `RESULT: PASS` (`receipts/crflic_head_pin_990f9652.log`). |
| `docs_check` in both modes | MET | With git: rc 0, 0 findings, scrub 23/23 (`receipts/docs_check_git.log`). Without git, on a `git archive` extraction: rc 0, 0 findings, 22/22, with inventory parity skipped as designed (`receipts/docs_check_nogit.log`). |
| `check_em_dash` | MET | `--base 864b36f5`: 0 findings over 197 added lines. `--base f219a5ed`: 0 over 1. `--selftest`: 339/339 (`receipts/em_dash_*.log`). The renderer comes from the hash-pinned `tools/markdown/requirements.txt` in a disposable environment (`receipts/markdown_venv_freeze.txt`). |
| `gen_toc --verify-anchors` | MET | 174 cross-page fragment links reproduced, rc 0. `--check` also returns rc 0 (`receipts/gen_toc_*.log`). |
| Nothing but the two text files changed | MET | `receipts/delta.raw` lists two `M` entries, both 100644. The commit message is one line with no trailers. |

The other gates are all rc 0:
- `check_doc_style`
- `check_doc_paths`: 847 paths
- `check_feature_status`

Evidence is in `receipts/check_*.log`.

## Prior public review findings: resolved or retained at this head

These were read only after my own pass above.

| finding | status | evidence |
|---|---|---|
| R296-2 N1 (MINOR, Conformance/Tests/Docs) = R297-2 F1 (MINOR, Docs/Conformance) | CLOSED | See the first three verification rows. |
| R296-2 S2 (SUGGESTION, Docs) | CLOSED | README:468 states 34 = 28 `[I]` + 6 `[J]`, and my rerun reproduces it. |
| R296-2 S1 (SUGGESTION, Tests); R297-2 S1, S2 (SUGGESTION) | RETAINED as optional | The assignment routes them to #495. SUGGESTION does not affect coverage. |
| R296-1 F1-F4; R297-1 F1-F4 | CLOSED (unchanged) | These were closed at `f219a5ed` in round 2. The delta touches none of their artifacts, and the head-pin `[I]`/`[J]` and BDD reruns still pass. |

## Clean lenses (evidence)

```text
[R296] PASS Conformance - tests/features/milan_streaming_licence.feature:4,87-95; tb/verilator/milan_dp/README.md:424-428,468; processor pin 990f9652 (contains 73a5478); PR #560 (Closes #508); processor issue #112 state CLOSED - checked the new comment against assignment 5833406989 item 1 and the round-2 required outcome. It no longer claims a residual window or a pending fix, and every claim it makes is true at this head. FR-SRP-03's "MUST NOT transmit" is met for changed TSpecs (receipts/crflic_head_pin_990f9652.log, 415/0) and fails only on the pre-#112 control (34).
[R296] PASS RTL - receipts/delta.raw (no hdl/ or processor path in f219a5ed..6e4a3b42; gitlinks 990f9652/e5dcea6e/48ff7a7e unchanged); hdl/milan/milan_datapath.sv lwsrp_stream_gate assignment asserted equal to ACTIVE & real grant by scripts/bdd_mutants.py; receipts/crflic_head_pin_990f9652.log - checked: the RTL that R296-2 covered clean is byte-identical here (blob ef5cb9d4). The rebuilt head elaborates and passes 415/0 on the pinned 5.050 simulator.
[R296] PASS Robustness - receipts/crflic_head_pin_990f9652.log and receipts/crflic_ctl_pin_7a47f578.log (sim_crf_licence.cpp [G]-[J], both sources, both round phases) - checked: refused re-declarations with the same and a changed previous TSpec never open a gate, a counter pair or a reset at the pin. The pre-#112 processor is caught on all four [I] cases and three [J] cases. The delta changes no bench or RTL behaviour.
[R296] PASS Tests - tests/features/milan_streaming_licence.feature (comment-only delta); tests/steps/milan_streaming_licence_steps.py (blob ea20363b, unchanged); receipts/bdd_mutants.log, bdd-*.log, behave_full_head.log, behave_licence_head.log - checked: the scenario still fails on all four wrong-composition mutants and passes clean before and after. The full suite passes 344/0. The comment now names the executable arm that grades the claim (obj_crflic [I]), and the control receipt confirms that arm can fail.
[R296] PASS Docs - tb/verilator/milan_dp/README.md:468; tests/features/milan_streaming_licence.feature:92-94; receipts/docs_check_git.log, docs_check_nogit.log, em_dash_*.log, gen_toc_check.log, gen_toc_verify_anchors.log, check_doc_style.log, check_doc_paths.log, check_feature_status.log - checked: the README count matches an independent rerun exactly. The table row keeps its three cells. The feature comment agrees with README:424-428 and ieee8021q.md:67. A tree search finds no remaining residual or pending-fix wording and no stale "fails 28" count. All doc gates return rc 0. S1 is optional.
```

## Reviewer-owned ledger

| lens | CLEAN/UNCLEAN | examined artifacts | covering round | exact head |
|---|---|---|---|---|
| Conformance | CLEAN | Assignment 5833406989; feature:87-95; README:424-428,468; ieee8021q.md:67; processor #112 (CLOSED), `73a5478` in `990f9652`; PR #560 Closes #508; `receipts/crflic_head_pin_990f9652.log`, `crflic_ctl_pin_7a47f578.log` | R296-3 | 6e4a3b420e055ef7529ceb16bb2ab5be93c34487 |
| RTL | CLEAN | `receipts/delta.raw` (no RTL or gitlink change); the gate assignment asserted in `scripts/bdd_mutants.py`; `receipts/crflic_head_pin_990f9652.log` (rebuilt, 415/0); `receipts/restore_verification.txt` (datapath blob identical). Unchanged from R296-2's clean coverage at ancestor `f219a5ed`. | R296-3 | 6e4a3b420e055ef7529ceb16bb2ab5be93c34487 |
| Robustness | CLEAN | `sim_crf_licence.cpp` [G]-[J] via both crflic receipts; `crflic_ctl_fail_by_section.txt` | R296-3 | 6e4a3b420e055ef7529ceb16bb2ab5be93c34487 |
| Tests | CLEAN | feature and steps; `receipts/bdd_mutants.log`, `bdd-*.log`, `behave_full_head.log`, `behave_licence_head.log`; the control receipt | R296-3 | 6e4a3b420e055ef7529ceb16bb2ab5be93c34487 |
| Docs | CLEAN (S1 optional) | README:468; feature:92-94; all doc-gate receipts listed above | R296-3 | 6e4a3b420e055ef7529ceb16bb2ab5be93c34487 |

## Real limits

- This is a delta review. Full-diff coverage of `864b36f5..f219a5ed` rests on R296-2. This round re-established only the delta and the reruns listed here.
- I did not run the full parent, processor, gPTP, Yosys or builder banks, or `make crflic-mutants` (the six RTL licence mutants). The delta touches no RTL and no bench source.
- The control ran in a disposable tree. The processor was cloned there at `7a47f578`, so the review clone's submodule was never repinned.
- Hosted evidence at this head is a snapshot and is incomplete. 10 contexts are success, including `bdd-conformance`, `docs-check-no-git`, `verilator-lint`, `full-ci-gate` and Yosys shards 0-3/4. 8 are in progress: Verilator shards 0-4/5, `yosys-elaboration`, `docs-check` and `elaborate`. 1 is skipped: Physical gPTP, nightly/manual (`receipts/hosted_checks_6e4a3b42.tsv`). A skipped context is not evidence.
- Physical calibration was NOT RUN. Field skips are not hardware proof.
- No Docker or act run was made.

## Pending manager duties

- Accept the hosted and act evidence at the exact head, including the in-progress Verilator shards, `yosys-elaboration`, `docs-check` and `elaborate`.
- Build and validate the final current-dev candidate at the merge turn. The source base is `864b36f5`; live dev is `fd9e0ebf2bbaa38330e99d1c489f01a820f1c363`.
- Carry out post-merge containment.
- Route S1 (optional) to #495 with the other suggestions, if wanted.
- A maintainer must authorize the merge.

## Restoration

- The review clone is at HEAD `6e4a3b42`, tree `f4e0bc48`, and the index tree equals the HEAD tree.
- `git status --porcelain --ignored` is empty after I removed the caches that test runs produced.
- The blob bytes of the four inspected files equal HEAD.
- The gitlinks match: `protocol-processor` `990f9652`, `gptp-processor` `e5dcea6e`, `third_party/verilog-axis` `48ff7a7e`, and `external` `efeb541a` (uninitialised, as found). Each initialised submodule is clean.
- See `receipts/restore_verification.txt`.
- Build logs have host paths replaced by `<VERILATOR_ROOT>`, `<PINNED_VERILATOR_5.050>` and `<SCRATCH>`.

R296-3 FINISHED
