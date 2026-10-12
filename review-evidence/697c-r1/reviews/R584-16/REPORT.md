[R584] POSITIVE - exact head 27ee16b52ac49b6b2523dafbf45f3af7ff4bba8c

# R584-16: internal independent review of PR #705 (issue #697), round 18

Head `27ee16b52ac49b6b2523dafbf45f3af7ff4bba8c`, tree `f84ea680aafd3b578b03cee405aeb818bee8bf4a`, verified in a detached clone. This is a delta review from `5b4ea551` (POSITIVE from R584-15 and R585-16) to `27ee16b5`. The delta is the merge `ddbd7fd7` of dev `dc4d06cb` (#716, PR #724) plus one follow-up commit, `27ee16b5`. The assignment for the round is #697 comment 6130298041.

All five lenses were applied. No BLOCKER, MAJOR or MINOR is open, so the verdict is POSITIVE. This round records two RESIDUE items (PR-body wording) and one SUGGESTION.

## Scope reconstructed

- **Round-18 assignment.** Merge dev `dc4d06cb` with a merge commit so that both sides stand: #716's four firmware jobs with their step split, and this lane's `firmware-boundary` and `firmware-verilator` jobs, pin checks and boundary capture. No check may be dropped or run twice. Each job must stay within 60 % of its timeout. `ci_events.py --check` and `--selftest` must pass. Nothing else may change: the images must equal dev's entry for entry and all pin controls must hold. STOP if the merge needs a change to firmware behaviour, an image input or the pin.
- **#697 acceptance 1-5** is frozen. This delta has to leave it intact.
- **What the delta touches** (`git diff --name-only 5b4ea551 27ee16b5`): `.github/workflows/rtl-fast.yml`, `docs/testing/CI_WORKFLOWS.md`, `scripts/ci_events.py`, `sw/firmware/ctrl/test/test_ctrl_firmware.py`, `sw/firmware/ctrl/test/test_ctrl_firmware_shards.py` (dev's new file, taken unchanged) and `sw/firmware/ctrl/test/ctrl_configs.py` (`27ee16b5`, +2 lines). There is no RTL, firmware C, header, image builder, Makefile or gitlink change. The six gitlinks are unchanged; tsn-c-stack is still `405dc683…`.

## What was checked

| Check | Result | Receipt |
|---|---|---|
| The lane's per-file delta is preserved | In every one of the 67 non-conflicted files, the lane's change against dev is identical before the merge (`c6bd08c6..5b4ea551`) and after it (`dc4d06cb..27ee16b5`). Both lists hold the same 72 files. | commands in this report |
| `rtl-fast.yml`, job by job, across base, lane, dev and head | `firmware-boundary` and `firmware-verilator` equal the lane's. The three mutation jobs equal dev's except for the added `third_party/tsn-c-stack` fetch. `firmware-unit` is the base plus exactly two changes, the lane's fetch line and dev's `--shard 0/4`. Every other job equals all sides. The aggregate's `needs`, environment and loop are dev's nine plus the lane's two (11, none missing, none doubled). Top-level keys are unchanged. Every firmware job fetches tsn-c-stack. | `scripts/wf_merge_compare.py`, `receipts/wf_merge_compare.txt` |
| `ci_events.py` three-way | Apart from one hunk, the lane-to-head change is dev's diff exactly. That hunk is `RV32_REQUIRED_STEPS`: `firmware-unit` takes `FIRMWARE_PHASE_STEPS[0]`, each mutation job gets its own phase step (dev's controls), and `firmware-boundary`'s entry is kept (the lane's). The aggregate environment is the union. | `scripts/ci_events.py:7910-7920`, `:595-601` |
| `test_ctrl_firmware.py` three-way | The lane-to-head change is dev's diff exactly. `--build-only` refuses `--self-test` and `--shard` requires it (`:282-286`). `stack_pin()` runs in `main` before `cut_reuse` and any arm (`:304`). | `receipts/driver_arg_refusals.txt` (5 combinations, each rc 2) |
| `ci_events.py --check`, `--firmware-census`, `--selftest` at the head | `OK (2169 contract items)`, census `preserved: true` (19 baseline commands, 55 across four jobs), `selftest: PASS (2169 items, 3064 arms)` | `receipts/ci_events_check_selftest.log`, `ci_events_firmware_census.json` |
| Each merge choice undone alone, in a copy, then `--check` | 17 plants. 15 are refused (rc 1): each of the six firmware jobs' fetch without tsn-c-stack, `needs` without `firmware-boundary` or `firmware-aecp-mutants`, the loop without `firmware-verilator` or `firmware-srp-mutants`, the environment without control-mutants, `firmware-unit` without `--shard 0/4`, the SRP job on shard 2/4, the boundary job without `--require-rv32`, the AECP budget row dropped, and the control-mutants job removed. 2 pass: raising `firmware-verilator`'s timeout, and dropping `firmware-boundary` from the docs-only skip sentence. Both pass at the lane parent or at dev too (see R584-16-S1), so the merge did not introduce them. | `scripts/ci_merge_mutants.py`, `receipts/ci_merge_mutants.txt`, `boundary_timeouts_unpinned.txt`, `docs_skip_sentence_unpinned.txt` |
| `27ee16b5` registry entry | The boundary gate's text scan finds 36 builders. At the head each one is classified. With the new OUTSIDE entry removed in memory, exactly one program is unclassified: `test_ctrl_firmware_shards.py`. Run alone under an execve trace, the shard proof starts no process but its interpreter (1 execve), so "compiles nothing" holds. `ctrl_configs` is not loaded by `test_ctrl_firmware.py` or the shard proof, so the change cannot reach the firmware jobs. | `scripts/registry_probe.py`, `receipts/registry_probe.txt`, `shard_proof_standalone.execve.strace`, `shard_proof_standalone.log` |
| Boundary gate at the head, local | `ctrl_boundary.py --require-rv32 --selftest --without verilator`: PASS in 801 s. 2822 compiled sources of 3049 invocations, 0 findings, 105 boundary, 106 pin and 4 figure controls, 0 misbehaved. | `receipts/local_boundary.log`, `.rc` |
| Two dev phases at the head, local | `--shard 2/4` (AECP): PASS, 76 `[ok]`, 218 s. `--shard 3/4` (SRP and pin controls): PASS, 273 `[ok]`, 713 s. Each printed the shard proof's five PASS lines (916 invocations, shard sizes 60, 507, 77, 272) and `tsn-c-stack at 405dc683…` before building. | `receipts/local_aecp.log`, `local_srp.log` |
| The pin check in each shard form | With `third_party/tsn-c-stack/src/adp.c` edited, each `--shard i/4` exits 2 with `REFUSED: tsn-c-stack differs from the pinned 405dc683: src/adp.c`. The only compiler executions are `--version` probes. The file was restored and its sha256 re-checked. | `receipts/shard_pin_refusal_probe.txt`, `shard_pin_probe_0.execve.strace` |
| Images | `ctrl_image.py --base dc4d06cb`: `+0` in every section at both shapes. Head and base ELFs are byte-equal (`5a4086ce…`, `acb380ee…`), and these equal the matching rows of the author's published 35-image table. Neither side of the merge changes an image input (file lists above). | `receipts/ctrl_image_base_dc4d06cb.log`, `ctrl_image_elf_sha256.txt` |
| Hosted `rtl-fast` at the head (run 38297906261) | Every job succeeded. Each job's percentage of its timeout is below 60 %: `firmware-unit` 694 s (25.7 % of 45 min), control 757 s (28.0 %), AECP 251 s (9.3 %), SRP 730 s (27.0 %), `firmware-boundary` 678 s (37.7 % of 30), `firmware-verilator` 436 s (18.2 % of 40), `publication-census` 31.9 %, `yosys-elaboration` 37.6 %. Each firmware job's log shows its tsn-c-stack fetch, its own shard command, the shard proof line, `tsn-c-stack at 405dc683…` and its PASS. The control job reports `mutants: 506 of 506 caught`. Both boundary jobs report 106 pin controls, 0 misbehaved. | `receipts/hosted_rtl_fast_run_38297906261.json`, `hosted_rtl_fast_timings.txt`, `hosted_firmware_job_markers.txt`, `hosted_job_*.log.gz` |
| Docs gates | `check_em_dash.py`: 0 findings over 433 added lines (base dc4d06cb), 62 (base 5b4ea551) and 768 (base c20c85bd). `check_doc_paths`, `check_doc_style` and `check_submodule_docs`: OK. | `receipts/em_dash.txt`, `docs_quick.txt` |
| Clone restored | HEAD, index tree `f84ea680…`, empty `status --untracked-files=all`, `diff-index` rc 0. The six gitlinks are as recorded, and the tsn-c-stack and lwSRP checkouts are clean. | `receipts/restore_verification.txt` |

## Findings

### R584-16-RES-1 - RESIDUE - Docs - the PR body still says the head is not pushed

- **Artifact:** PR #705 body, `## Round 18`, "Open, for the manager", item (c): "#716's hosted acceptance at the new head, ten consecutive runs, is the manager's; the head is not pushed;".
- **Evidence:** the PR head is `27ee16b5`, and hosted `rtl-fast` run 38297906261 succeeded at it (`receipts/hosted_check_runs_at_head.tsv`). This is the same wording that R584-15-RES-1 fixed for Round 17, now back in the Round 18 section.
- **Impact:** wording only. No measurement, figure, verdict, test or code depends on it.
- **Exact fix:** replace that item with "(c) #716's hosted acceptance at the new head, ten consecutive runs, is the manager's; the head was pushed after this section was prepared, and its hosted runs are the manager's to accept;".
- **Verification:** re-read the item.

### R584-16-RES-2 - RESIDUE - Docs - a timing measured at the merge commit is labelled as the head's

- **Artifact:** PR #705 body, `## Round 18`, budget table, row `firmware-control-mutants`, column "Replica, head / dev beside it": `888 / 860 s`. The sentence after the table says "Each head job ran beside dev's in the replica, and the ratios (0.998 to 1.033) …". The Status bullet says "control 763 s … dev's own jobs beside them took 590, 860, 182 and 569 s".
- **Evidence:** the REVIEW READY (#697 comment 6131138314) says "control: 763 s … At the merge: 888 s, dev beside it 860 s". So the paired control run, and the 1.033 ratio (888/860), come from `ddbd7fd7`, not `27ee16b5`. Between the two commits only `ctrl_configs.py` changes, and neither the control driver nor the shard proof loads it (checked: `ctrl_configs` is absent from `sys.modules` after importing both). So the figure is a valid measurement of the code the head runs. Only its label is wrong.
- **Impact:** wording only. No figure changes, and the 60 % verdict rests on hosted timings, which at this head give 28.0 % for the control job.
- **Exact fix:**
  - Table cell: "888 / 860 s (at the merge `ddbd7fd7`; 763 s alone at the head)".
  - Sentence: "Each job ran beside dev's in the replica (the control job at the merge `ddbd7fd7`, whose control-gate code the head does not change), and the ratios (0.998 to 1.033) …".
  - Status bullet: "dev's own jobs took 590, 860 (beside the merge's 888 s), 182 and 569 s".
- **Verification:** re-read the three places.

### R584-16-S1 - SUGGESTION - Tests, Robustness - the boundary jobs' timeouts are not pinned, unlike #716's four

- **Artifact:** `scripts/ci_events.py` `check_firmware_layout` (pins the four `FIRMWARE_JOBS` at 45 minutes and their budget rows). `.github/workflows/rtl-fast.yml` `firmware-boundary` (`timeout-minutes: 30`) and `firmware-verilator` (`40`).
- **Evidence:** raising both timeouts still passes `--check`, both at the lane parent `5b4ea551` and at the head (`receipts/boundary_timeouts_unpinned.txt`). The docs-only skip sentence is not pinned either, and that is also true at dev `dc4d06cb` (`receipts/docs_skip_sentence_unpinned.txt`). Neither gap comes from the merge.
- **Suggested outcome:** pin the two boundary jobs' timeouts as #716 pins its four.

## Prior public findings at this head

| Finding | Status at `27ee16b5` | Evidence |
|---|---|---|
| R584-15-RES-1 (Round 17 item (d), "head not pushed") | APPLIED: PR body Round 17 item (d) carries its exact text. The same wording comes back in Round 18 as R584-16-RES-1. | live PR body |
| R585-16-RES-1 (allowlist "no key that names a program") | RETAINED RESIDUE. Round 18 allowed no other change, so it was not applied in the tree. Its exact fix is recorded in the PR body's Round 18 Residue paragraph. The text is unchanged at `sw/firmware/ctrl/README.md:181`, `ctrl_build.py:199` and `:551-552`. | source; live PR body |
| R584-15-S1, R585-16-S1 | RETAINED SUGGESTIONS. The files they name are untouched by the delta. | delta file list |
| R585-14-S1, R584-13-S1, R585-13-S1/S3, R584-11-S1, R584-9-S1, R585-2-S2, R584-8-RES-1 and the residue carried for #495 | RETAINED. They are outside this delta and were not re-verified one by one. | delta file list |

## Lens results

[R584] PASS Conformance - receipts/wf_merge_compare.txt, rtl-fast.yml:312-586 and :587-630, ci_events.py:595-601 and :7910-7920, receipts/ctrl_image_*.txt, hosted_rtl_fast_timings.txt - round-18 items 1-3 checked against the assignment. Both sides stand, no job is dropped or doubled, and the aggregate is complete. Every job is under 60 % by hosted timing at the head. Check and self-test pass. Images are equal to dev's. #697 acceptance 1-5 is unaffected, because no core, header, image input or gitlink changes. `27ee16b5` touches only the gate's registry, which the boundary job needs.

[R584] PASS RTL - git diff --name-only 5b4ea551 27ee16b5 (no .sv/.v, no firmware C), rtl-fast.yml job graph (needs, if, timeout-minutes), test_ctrl_firmware.py:142-220 and :262-311 - no RTL or firmware source is in the delta. The CI job graph and the driver's CLI contract (`--shard` and `--build-only` exclusive, phases complete and disjoint, the pin before the first build) are consistent across both parents.

[R584] PASS Robustness - receipts/driver_arg_refusals.txt, shard_pin_refusal_probe.txt, shard_proof_standalone.log, rtl-fast.yml:587-630 (aggregate `if: always() && !cancelled()`, success|skipped) - invalid and incompatible shard arguments refuse with rc 2. An edited stack is refused by name in every shard form before any compile. A failed normal suite still stops mutations. All six firmware jobs share the same `changes` relevance condition.

[R584] PASS Tests - receipts/ci_merge_mutants.txt (15 of 15 merge-choice plants refused; 2 gaps that predate the merge, R584-16-S1), registry_probe.txt, local_boundary.log (105/106/4, 0 misbehaved), local_aecp.log, local_srp.log, hosted_firmware_job_markers.txt - each check the resolution relies on can fail for the defect it guards. The real gates pass at the head, locally and hosted.

[R584] PASS Docs - docs/testing/CI_WORKFLOWS.md:44-66, :115-157 and :2448-2460, test_ctrl_firmware.py:96-117, ctrl_configs.py:162-163, PR #705 body (Status, Round 18), receipts/em_dash.txt, docs_quick.txt - the four jobs, the boundary jobs, the skip list and the budgets are stated for both sides, and the docstring states both `--build-only` and `--shard`. The em-dash and doc gates are clean. Two wording residues are carried to the checklist (RES-1, RES-2).

## Reviewer ledger

| Lens | Result | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | Round-18 assignment, #697 acceptance, `rtl-fast.yml`, `ci_events.py`, image ELFs, hosted timings | R584-16 | `27ee16b52ac49b6b2523dafbf45f3af7ff4bba8c` |
| RTL | CLEAN | Delta file list (no RTL), job graph, driver dispatch and CLI | R584-16 | `27ee16b52ac49b6b2523dafbf45f3af7ff4bba8c` |
| Robustness | CLEAN | Argument refusals, pin-before-build per shard, aggregate semantics | R584-16 | `27ee16b52ac49b6b2523dafbf45f3af7ff4bba8c` |
| Tests | CLEAN (S1 optional) | CI merge mutants, registry probe, boundary gate, AECP/SRP shards, hosted firmware jobs | R584-16 | `27ee16b52ac49b6b2523dafbf45f3af7ff4bba8c` |
| Docs | CLEAN (RESIDUE RES-1, RES-2 to the checklist) | `CI_WORKFLOWS.md`, driver docstring, `ctrl_configs.py`, PR body, docs gates | R584-16 | `27ee16b52ac49b6b2523dafbf45f3af7ff4bba8c` |

## Real limits

- **Host toolchain, not the runner's replica.** The local runs used CPython 3.14.7, GCC 16.2.1 and Git 2.56.0, with a pinned copy of GoogleTest 1.14.0 and clang 18. The pinned RV32 SDK (archive sha256 `d42680e9…`) was installed and receipt-verified from a local archive into scratch. Local wall times come from a shared host running several jobs at once and are not budget evidence; the budget verdict uses hosted timings. A home-directory path in one strace receipt is redacted to `/home/<user>`.
- **Not run locally:**
  - `firmware-unit` (shard 0/4) and the control shard (1/4). Their exact-head evidence is the hosted run's.
  - `firmware-verilator`'s gate (no Verilator was used). Its evidence is the hosted job.
  - The SRP-image half of the 35-image table. Only the two `ctrl_image` shapes were rebuilt; the rest relies on the unchanged-input argument and the author's published table.
  - The docs job's full command list.
  - Any act or replica run.
- **Hosted runs still in flight at the snapshot** (19:56 UTC): `elaborate` and the five `rtl-full` Verilator shards, so the `verilator-suites` aggregate had not run yet. Twenty checks had succeeded and one (Physical gPTP) was skipped by design; none had failed. The merge changes no RTL and no `rtl-full`/`elaborate` workflow.
- **No hardware proof.** Physical calibration was NOT RUN, and field skips are not hardware proof.
- **No manager source bank** runs at this head, and none is claimed.

## Pending manager duties

- **Hosted acceptance.** Accept hosted results at the exact head, including the in-flight `elaborate`, the Verilator shards and `verilator-suites`/`yosys-portability`, plus #716's ten-run hosted acceptance.
- **Merge-turn validation.** Build and validate the current-dev merge candidate (builder and native banks) at the merge turn.
- **`27ee16b5`.** Rule on it as the one change beyond the four conflicts. This review finds it necessary and confined to the gate's registry.
- **Residue checklist.** Carry R584-16-RES-1, R584-16-RES-2 and the retained R585-16-RES-1 with their exact fixes. R584-16-S1 and the retained suggestions are optional.

R584-16 FINISHED
