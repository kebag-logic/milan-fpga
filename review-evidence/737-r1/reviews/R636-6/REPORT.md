[R636] NEGATIVE - exact head 47fd0d3c510000e9412a1613a723b61d4ef2ae4a

Round R636-6: internal, cleared-context review of PR #739 for issue #737. This is the exact-head review for merge.
- Head `47fd0d3c510000e9412a1613a723b61d4ef2ae4a`, tree `771055d82f5b90249c2610a6a20f1be36b15bf56`.
- Delta reviewed: `e3d25d96..47fd0d3c`, five commits.

## Verdict in one paragraph

The round-6 delta does what the assignment ([6187562969](https://github.com/kebag-logic/milan-fpga/issues/737#issuecomment-6187562969)) asks. I verified it:
- the docs builder now runs in the existing measured legs;
- the union judges exactly the template command's flags;
- the projections recompute exactly from the ruled inputs;
- reverting the generator makes the committed self-test fail;
- the test pages match the sixteen `--ci-pieces` workers;
- `scripts/act_ci.py` is byte-identical.

The verdict is NEGATIVE for one reason, F1 (BLOCKER), which the delta did not cause. It showed up in the exact-head hosted readback:
- **What fails.** The hosted docs workflow fails deterministically at this head, in `docs-gates-2` → `Local act runner contract gate` (`act_ci.py --selftest`).
- **Why.** The self-test's main-entry probe passes its synthetic 64-CPU booking to production `main()` without the CPU-count patch that the other main-path probes use. On the standard 4-CPU hosted runner, `main()` refuses with "CPU range 0-15 exceeds this host's 4 CPUs" before it reaches the lookup the probe is meant to interrupt.
- **Same failure at the round-5 head.** The hosted run at `e3d25d96` failed the same way.
- **Knock-on effect.** Cross-workflow fail-fast then cancelled the docs, elaborate, rtl-fast and rtl-full runs at this head.
- **What the fix needs.** `scripts/act_ci.py` is SHA-pinned, so the fix needs a coordinating-role decision.

Two RESIDUE items and two new SUGGESTIONs follow. Every prior round-5 finding is resolved.

## Reconstruction

I read, in order:
1. `AGENTS.md` and the review contract.
2. Issue #737: the body, the scope change [6166823105](https://github.com/kebag-logic/milan-fpga/issues/737#issuecomment-6166823105) (it replaces acceptance 1 and 3), the driver-refactor conditions [6160937413](https://github.com/kebag-logic/milan-fpga/issues/737#issuecomment-6160937413), the round-6 assignment, and the author's REVIEW READY [6189945844](https://github.com/kebag-logic/milan-fpga/issues/737#issuecomment-6189945844).
3. `git diff e3d25d96..47fd0d3c`, all five commits.
4. The public evidence at `26dd882d…/review-evidence/737-r1/author-r6/`.
5. Hosted runs at `f6260253` (docs 38601263556, elaborate 38601263659) and at this exact head (docs 38720602454, elaborate 38720602303, rtl-full 38720602398, rtl-fast 38720602241).

I read the prior round-5 findings, R636-5 [6187490136](https://github.com/kebag-logic/milan-fpga/pull/739#issuecomment-6187490136) and R637-5 [6187550918](https://github.com/kebag-logic/milan-fpga/pull/739#issuecomment-6187550918), only after my own pass over the delta.

**Evidence integrity.** The six round-6 evidence files I relied on match two references:
- their git blob ids in tree `26dd882d`;
- their `published_sha256` entries in `review-evidence/737-r1/MANIFEST.json` (`receipts/author_evidence_digests.txt`).

I found no detached signature for the author-r6 packet in that tree. Integrity rests on the manifest digests and the git object ids.

## Assignment checks

### (1) Docs builder in measured legs: holds

**Generated graph** (`.github/workflows/docs.yml`):
- Leg 0 is at `:591-595`. It keeps the `pip install` line, then `ci_builder_legs.py run 0 … -- python3 sw/builder/test_builder.py --require-rv32`, on `docs-gates-1`.
- Leg 1 is at `:738-742`, on `docs-gates-2`, before the two contract gates. This is template order: the template's builder step index 25 precedes indices 41 and 42, so the `success()` coupling equals the unsharded step order.
- Both workers retain `builder-leg-*.json` (`:611`, `:771`).
- Each docs worker carries every setup step, including `Fetch the builder source dependencies` and the RV32 SDK install, ahead of its leg.

**Generator** (`scripts/ci_gate_workflows.py`):
- `BUILDER_SPLIT` is at `:30` and `BUILDER_WORKERS` (docs (1, 2), elaborate (0, 1)) is at `:31`.
- `split_builder_run` (`:110-116`) requires that the step ends in its one driver command and that no preparation line runs the driver.
- `builder_leg_step` (`:128-138`) keeps the preparation lines byte for byte.
- `LONG_GATE` no longer names a docs step. The worker-0 check (`:92-93`) still holds.

**Union rules** (`scripts/ci_builder_legs.py`):
- `requirements()` (`:66-71`) reads the flags from the template command and refuses unknown or repeated flags. `union` (`:142-186`) judges only those flags.
- Every leg must carry exactly the command's flags (`:175-177`).
- The driver's elaboration verdict is applied only under `--require-elaboration` (`:179`).
- The production aggregate derives the flags from the template, not from any receipt (`scripts/ci_gate_receipts.py:121-122`, `:165-167`). So docs judges `--require-rv32` alone and elaborate judges both, as ruled.

**Equality with the unsharded run** (`round6-docs-builder-legs.json`, at `26838a11`):
- The reference ran 103 gates in 1443.72 s, with "ALL GATES PASS EXCEPT 2 NOT RUN" (gate 1b, gate 11).
- Leg 0 ran 1 gate in 1098.13 s and leg 1 ran 102 gates in 506.263 s. Each records one of the two NOT RUN rows.
- `union --workflow docs --reference` is equal to the unsharded run, with `verdicts_sha256 47dc3c6a…`. The union `not_run` equals the reference ledger.
- The production docs aggregate replay accepts the receipts: 43 source gates exactly once.
- Printed output: 98 gates identical, 4 identical after masking temporary paths and durations, and `test_nvm_firmware_shapes` differs only in its "caught by N named finding(s)" count. Its verdict is equal; the author disclosed the cause as a thread-pool search order that stops at the first named finding.

**Is the `26838a11` evidence valid at this head?** `git diff 26838a11..47fd0d3c` touches only Markdown and one comment in `scripts/suite_shards.py:69-70`. No executable byte that the measurement depends on changed.

**Planted controls** (`round6-docs-controls.json`):
- dm1, the boot-claim defect, fails the unsharded run and leg 0; leg 1 passes.
- dm2, the FPU refusal, fails the unsharded run and leg 1; leg 0 passes.
- dm3 ran leg 0 without `--require-rv32`. Both the production aggregate and `compare` refuse it by name: "test_baremetal_profile_contract ran only in a leg without the flag".

**Conditions of 6160937413:**
- The inventory comes from the driver.
- The union is exactly-once.
- Per-gate verdicts and the NOT RUN ledger are equal.
- Every planted defect is caught, and only in its owning leg.
- No gate is skipped, made conditional or given a longer timeout. `timeout-minutes` is 45 on every gate worker, as before.
- Condition 3 (build once) does not apply: the builder has no shared model build.

### (2) Projections: hold, and they recompute exactly

`scripts/recompute_projections.py` reads the saved `f6260253` job listings and gives `receipts/projection_recompute.txt`.

The hosted inputs are confirmed:
- docs job 2682 s: builder 1400, contract 37, runner 102;
- elaborate job 2447 s: gates 1763, LiteX 597, Verilator setup 2.

| Worker | Recomputed | Page (`CI_WORKFLOWS.md:2748-2752`) | Share of 2700 s |
|---|---:|---:|---:|
| `docs-gates-0` | 1394.137 → 1395 | 1395 | 51.7 % |
| `docs-gates-1` | 1247.407 → 1248 | 1248 | 46.2 % |
| `docs-gates-2` | 1072.100 → 1073 | 1073 | 39.7 % |
| `elaborate-gates-0` | 1474.052 → 1475 | 1475 | 54.6 % |
| `elaborate-gates-1` | 1352.757 → 1353 | 1353 | 50.1 % |

- **Workflows.** Docs is 1395 + 270 = 1665 s (27.75 min, 135 s margin). Elaborate is 1475 + 270 = 1745 s (29.08 min, 55 s margin).
- **Larger figure.** The rule is applied as ruled: the builder scale is max(1400, 1482.211, 1443.720) / 1443.720, and the elaboration scale is 1763 / 1433.969.
- **Setup and gaps.** My split of the hosted docs non-gate time gives 57 s; the page uses 59. The 2 s sits on the other side of the same total, and the rounded row is unchanged.
- **Arm count.** `ci_events.py --selftest` at this head passes "2187 contract items, 5215 arms" in 186 s (`receipts/head_ci_events_selftest.*`). R636-5 recorded 5,212 at `e3d25d96`. The page (`:2695-2697`) states both figures and explains the three added arms, which is the honest form of "correct the arm count to 5,212".
- **Sensitivity**, disclosed by the author. The contended final-bank elaboration leg 0 (1193 s) would put `elaborate-gates-0` at 1612 s and the workflow at 1882 s. It is not a ruled input, since it was measured with 3-5 jobs sharing 16 CPUs. The hosted readback that would settle it could not happen at this head: see F1 and the limits.

### (3) Generator revert probe: holds

- I copied `ci_suite_workflows.py` from `08adb21a` into a disposable clone of this head and regenerated. `rtl.yml` gains `5) test … = milan_dp ;;` and `--expect 6` (`receipts/revert_regen_rtl.diff`).
- After that, `ci_gate_workflows.py --check` returns rc 0 and `ci_events.py --check` returns rc 0 (2187 items), but `ci_gate_workflows_selftest.py` returns rc 1. It fails at `suite_generator_controls` (`:102`), on the assertion that no dedicated arm remains (`receipts/revert2_*`).
- Without regeneration, `--check` and `ci_events --check` also fail (`receipts/revert_*`).
- At the head, the same self-test passes (`receipts/head_gate_selftest.*`). It prints all three planted-template refusals: arm index, `--expect`, and total.

### (4) Test pages: hold

- `scripts/run_all_suites.sh --list` gives 63 suites (`receipts/default_list.txt`).
- The `--ci-pieces --shard i/16 --list` lists for i = 0..15 give 80 entries, no duplicates, 23 pieces from six suites, and a base-name union of 63 (`receipts/ci_pieces_16_lists.txt`).
- `milan_dp__0..3` are on workers 3, 0, 6 and 5, all distinct. `milan_dp_mclk__0` is alone on worker 15.
- This matches:
  - `TESTING.md:518-531`;
  - `tb/verilator/milan_dp/README.md:447-449`;
  - `RUNNING_TESTS.md:84-95`;
  - the disclosed `726_STREAM_COUNTERS.md:177-178` (`suite-union-milan_dp` joining four leg logs).

### (5) Residues

- R636-5-R1 is fixed with the exact text (`CI_WORKFLOWS.md:376-379`).
- R637-5-R2 is fixed in both places (`CI_WORKFLOWS.md:372`, `scripts/suite_shards.py:70`).
- R637-5-R1 is fixed in the round-5 paragraph, but the same sentence recurs in the round-6 Status (R1 below).
- A `/5` and `/6` search of the changed pages is clean apart from text marked historical.

### (6) `scripts/act_ci.py`: holds, but see F1

- SHA-256 is `f968f67655ac386ea703248b724c3781b95ec379d3a5287b378e470df81f895c` at this head, the same at `e3d25d96` and `08adb21a`, with no diff in the delta.
- Dev `f6260253` holds `506155c1…`. The PR changes the runner relative to its base, so dev's passing hosted gate says nothing about this runner.

## Findings

### F1 - BLOCKER - Conformance, Robustness, Tests - `scripts/act_ci.py:12180` (with `:15087-15090`, `:4675-4692`); hosted docs run 38720602454, job `docs-gates-2` 116373922720, step 18 - the runner contract gate fails deterministically on the standard hosted runner

**Authority and evidence.**
- Issue #737's replaced acceptance 1 ([6166823105](https://github.com/kebag-logic/milan-fpga/issues/737#issuecomment-6166823105)) reads: "GitHub CI on a PR: every workflow it runs finishes in at most 30 min." Docs is one of those workflows, and its `docs-check` aggregate requires every gate.
- AGENTS §7 requires that "required tests and local verification gates pass" and that "the current PR head" has its hosted evidence.
- The issue's fidelity aim is that the same head gets the same verdict locally and on GitHub.
- **Hosted, at this exact head:**
  - `docs-gates-2`: builder leg 1 passed in 287 s and the CI-event contract gate passed in 132 s.
  - `Local act runner contract gate` failed after 84 s. The first invocation reports "FAIL flat isolated full selftest uses the explicit shipping worktree". The second invocation reports "FAIL production main contains an interrupted early repository lookup" and "selftest: 2 FAILURE(S)". Both print "act-ci: REFUSED: CPU range 0-15 exceeds this host's 4 CPUs".
  - Fail-fast then cancelled every other docs and elaborate worker, and the rtl-full and rtl-fast runs at the same SHA. Their failures are all downstream aggregates (`receipts/hosted/exact_head_summary.txt`, `receipts/hosted/exact_head_run_*.jobs.json`).
- **Hosted, at the round-5 head `e3d25d96`:** run 38700974399, job 116308789608, fails identically (`receipts/hosted/runner_gate_failure.txt`). These are the only two hosted docs runs this branch has had, and both fail.
- **Cause, from the source:**
  - `selftest_configured` (`:15087-15090`) books the synthetic ranges `0-15,16-31,32-47,48-63`.
  - `selftest_main_entry_probe` (`:12157-12188`) calls `main([... "--pr", "1", "--cpu-ranges", ",".join(BOOKED_CPU_RANGES.get())])` with no `os.cpu_count` patch.
  - `parse_cpu_ranges` (`:4690-4692`) refuses any range whose last CPU is at or above `os.cpu_count()`.
  - So on any host with fewer than 64 CPUs, `main` returns `RC_REFUSED` before the `gh` lookup, the ready file is never written, and the probe fails.
  - The other main-path probes that pass `--cpu-ranges` are wrapped in `mock.patch.object(os, "cpu_count", return_value=512)` (`:13675`, `:14673`). This one is not.
  - The path came in with PR commit `8eab741af` ("Pin replay jobs at creation on externally booked CPU ranges"). Dev's runner has no `parse_cpu_ranges`.
- **Why local runs pass.** The author's local gate passes (109 s) because the shipping-image containers report the host's CPU count to `os.cpu_count()`, whatever their cpuset. That is an inference from the code, and it matches the observed local-pass / hosted-fail split.

**Impact.**
- No hosted docs run of this PR can pass. Merged into dev, the runner would make every later PR's docs workflow red.
- Fail-fast turns this into cancelled elaborate, rtl-fast and rtl-full runs at the same head. So the 30-minute hosted readback cannot be taken.
- The local replay and GitHub give different verdicts on the same head.

**Required outcome.**
- At the merge head, the runner contract gate passes on the standard hosted runner and still passes locally. The main-entry probe must exercise the interrupted lookup whatever the host's CPU count, and must still fail when that lookup is not contained.
- `scripts/act_ci.py` is pinned by SHA-256 under the round-6 ruling. The coordinating role must decide on the change and the repin, and that decision must be public. Moving this finding to another Issue does not resolve it.

**Verification.**
- An exact-head hosted docs run shows `Local act runner contract gate` succeeding on `docs-gates-2`.
- A local control with `os.cpu_count()` forced below 64 passes.
- A planted non-containment still fails the probe.

### R1 - RESIDUE - Docs - PR #739 body, Status, round-6 paragraph: "The author does not push; the coordinating role publishes this head."

- **Evidence.** The live PR head is `47fd0d3c510000e9412a1613a723b61d4ef2ae4a`, so the head is published. The round-5 paragraph was fixed, and the same sentence now recurs for round 6.
- **Exact fix.** Replace the sentence with "The coordinating role published this head."
- **Verification.** Read the live PR body against the PR head.

### R2 - RESIDUE - Docs - PR #739 body, "Known limitations / out of scope", last bullet

- **Evidence.** The bullet ends "It does not divide the docs builder, which now projects the docs workflow above 30 minutes." This round divides it, and the body's own table projects docs at 1665 s.
- **Exact fix.** Replace the bullet with: "The merged dev workload lengthens the docs builder and saved-state writer gates and the elaboration builder. Round 6 divides the docs builder into the two measured legs and re-projects both workflows from the merged-head inputs: docs 1665 s, elaboration 1745 s."
- **Verification.** Read the body against `CI_WORKFLOWS.md:2779-2789`.

### S1 - SUGGESTION - Tests - `scripts/ci_gate_workflows.py:144`, `scripts/ci_gate_workflows_selftest.py:362-385` - receipt retention on the docs builder workers has no committed check

- **Evidence.** I mutated `if leg in BUILDER_WORKERS[name]:` to `if name == "elaborate":` and regenerated. `docs.yml` then drops `builder-leg-*.json` from the `docs-gates-1` and `docs-gates-2` uploads. Despite that, `ci_gate_workflows.py --check`, `ci_events.py --check`, `ci_gate_workflows_selftest.py`, `ci_workflow_plan_selftest.py`, `ci_manifest_selftest.py`, `generate_ci_evidence_pins.py --check`, `ci_runtime_evidence_selftest.py`, `ci_fail_fast_selftest.py` and `ci_case_receipts_selftest.py` all return rc 0 (`receipts/mutations/m3-*`).
- **Why this is a SUGGESTION.** The regression fails closed on the very PR that introduces it. Docs is PR-triggered, and its aggregate refuses "executed builder division without builder receipts". That refusal is covered by the self-test for both workflows.
- **Suggested outcome.** In `case_step_controls` or the per-leg loop, assert that each worker in `BUILDER_WORKERS[name]` uploads `builder-leg-*.json`, and that no other worker does.

### S2 - SUGGESTION - Tests - `scripts/ci_gate_workflows.py:113-116` - the new "driver in a preparation line" refusal has no plant

- **Evidence.** I mutated the condition away. The gate self-test still passes (`receipts/mutations/mutations.txt`, M6). No template triggers that condition today.
- **Suggested outcome.** Add one planted template whose divided step runs the driver in a preparation line.

### Mutation probes

My probes (`scripts/mutation_probe.sh`, `receipts/mutations/`): the pristine self-test passes before and after.
- **Caught:**
  - M1: unchecked requirement flags;
  - M2: docs leg workers swapped;
  - M4: the aggregate judging both flags;
  - M5: per-leg flag equality removed.
- **Survived:** M3 (S1) and M6 (S2).

These complement the author's 6/6 battery in `round6-mutations.json`.

## Per-lens results at `47fd0d3c`

[R636] UNCLEAN Conformance - `scripts/act_ci.py:12180`; hosted docs run 38720602454 job 116373922720 step 18 - F1. Round-6 items (1)-(4) and (6) are otherwise proved:
- generated `docs.yml:591-595`, `:738-742`;
- `ci_builder_legs.py:66-71`, `:142-186`;
- `round6-docs-builder-legs.json` and `round6-docs-controls.json`;
- `receipts/projection_recompute.txt`;
- `receipts/revert2_*`;
- `receipts/ci_pieces_16_lists.txt`.

[R636] PASS RTL - `scripts/ci_gate_workflows.py:22-31, 67-98, 110-138, 141-160`; `scripts/ci_builder_legs.py:66-186`; `scripts/ci_gate_receipts.py:118-123, 160-168`; generated `docs.yml` worker and aggregate step lists - checked against the existing builder-leg contract (`CI_WORKFLOWS.md:1401-1450`).
- Docs legs land on workers 1 and 2. Worker 0 is unchanged, at 58 steps.
- `docs-check` needs all three workers.
- Template step order and `success()` coupling are preserved.
- The template is unchanged.
- The elaboration placement (0, 1) is unchanged.
- The HDL and the gitlinks are unchanged by the delta (`receipts/restore_verification.txt`).

[R636] UNCLEAN Robustness - `scripts/act_ci.py:4690-4692` with `:12180` - F1: configuration-dependent behaviour, the host CPU count. The delta's refusals are otherwise exercised:
- unknown or repeated flags;
- a leg carrying the other command's flags;
- a vacuous leg-0 run;
- a toolchain skip under `--require-elaboration`, refused, against the same skip retained for docs;
- the reverted generator (`receipts/mutations/mutations.txt`, `receipts/revert2_*`, `round6-docs-controls.json`).

[R636] UNCLEAN Tests - `scripts/act_ci.py:12157-12188` - F1: the runner self-test's result depends on the host CPU count. Otherwise:
- `ci_gate_workflows_selftest.py`, `ci_suite_pieces_selftest.py`, `suite_shards.py --selftest`, `ci_events.py --check`, `ci_events.py --selftest` (5,215 arms), `ci_workflow_plan_selftest.py`, `ci_manifest_selftest.py` and `generate_ci_evidence_pins.py --check` all return rc 0 at the head (`receipts/head_*`);
- the R637-5-F2 control bites;
- S1 and S2 are optional.

[R636] PASS Docs - `docs/testing/CI_WORKFLOWS.md:366-379, 1401-1450, 2686-2789, 2796-2806, 2975-2985`; `docs/testing/TESTING.md:515-531`; `docs/testing/RUNNING_TESTS.md:81-95`; `tb/verilator/milan_dp/README.md:444-451`; `docs/testing/726_STREAM_COUNTERS.md:174-178`; `scripts/suite_shards.py:67-70` - checked against the recomputation, the hosted job listings, the `--ci-pieces` lists and the generated workflows. R1 and R2 are RESIDUE in the PR body and do not affect coverage.

## Reviewer-owned coverage ledger

| Lens | Status | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | UNCLEAN (F1) | #737 acceptance (replaced 1 and 3), 6160937413, round-6 assignment; generated `docs.yml`; `round6-*` evidence; hosted runs 38601263556, 38601263659, 38720602454, 38720602303, 38700974399; `receipts/projection_recompute.txt` | R636-6 | `47fd0d3c510000e9412a1613a723b61d4ef2ae4a` |
| RTL | CLEAN | `scripts/ci_gate_workflows.py`, `ci_builder_legs.py`, `ci_gate_receipts.py` at the cited lines; generated `docs.yml`/`elaborate.yml` step lists; unchanged template and gitlinks | R636-6 | `47fd0d3c510000e9412a1613a723b61d4ef2ae4a` |
| Robustness | UNCLEAN (F1) | `scripts/act_ci.py:4675-4692, 12157-12188, 15087-15090`; mutation and revert probes; planted docs controls | R636-6 | `47fd0d3c510000e9412a1613a723b61d4ef2ae4a` |
| Tests | UNCLEAN (F1; S1 and S2 optional) | `receipts/head_*`, `receipts/revert*`, `receipts/mutations/*`; `round6-mutations.json`, `round6-generator-controls.json`; hosted runner-gate logs | R636-6 | `47fd0d3c510000e9412a1613a723b61d4ef2ae4a` |
| Docs | CLEAN (R1 and R2 RESIDUE) | the six pages and comment listed above; PR #739 body | R636-6 | `47fd0d3c510000e9412a1613a723b61d4ef2ae4a` |

## Prior findings at this head

| Prior item | Status at `47fd0d3c` | Evidence |
|---|---|---|
| R636-5-F1 = R637-5-F1 (MINOR: docs above 30 min after the merge; stale projections) | **Resolved** by projection. Hosted confirmation is blocked by F1 | Check (1) and check (2); `receipts/projection_recompute.txt` |
| R636-5-F2 (MINOR: `TESTING.md` six workers) | **Resolved** | Check (4); `TESTING.md:518-531`, README `:447-449`, `RUNNING_TESTS.md:84-95` |
| R637-5-F2 (MINOR: no committed generator self-check) | **Resolved** | `suite_generator_controls` (`ci_gate_workflows_selftest.py:92-133`); revert probe fails it (`receipts/revert2_gate_selftest.*`) |
| R636-5-R1 (RESIDUE: "replaces all three") | **Resolved**, exact text | `CI_WORKFLOWS.md:376-379` |
| R637-5-R1 / R636-5-R2 (RESIDUE: publication tense) | **Resolved** for round 5. **Recurs** for round 6 as R1 | PR body Status |
| R637-5-R2 (RESIDUE: "whose suites all passed") | **Resolved**, both sites | `CI_WORKFLOWS.md:372`; `suite_shards.py:70` |
| R636-5-S1 (SUGGESTION: generator refusals untested) | **Resolved** | Same as R637-5-F2 |
| R636-5-S2 (SUGGESTION: a stray extra `milan_dp` arm is not refused by the generator) | **Retained** | `ci_suite_workflows.py:106-112` unchanged. The new self-test pins only the real template's output |
| R636-4-S1 (SUGGESTION: "listed above" union log line) | **Retained**, now limited to `elaborate` | The docs union no longer calls `elaboration_verdict` (`ci_builder_legs.py:179`) |
| R636-4-S2 (SUGGESTION: builder-inventory reader absent from `check_inventory_dependencies`) | **Retained**, now applies to the docs aggregate too | `docs-check` installs the pinned PyYAML reader unconditionally (generated `docs.yml`), so it is safe at this head |
| R636-4-S3 (SUGGESTION: driver `--gates` refusals untested) | **Retained** | `sw/builder/test_builder.py` is not in the delta |
| R636-3 and earlier, R637-1 to R637-4 | Resolved earlier; not reopened by the delta | The delta touches only the files listed in check (1) and the pages |

## Real limits

- **What I ran.** I ran no docs-check, rtl-fast, builder, Verilator suite, Yosys or replay bank, and no `act_ci.py` or its self-test. F1 rests on the published hosted logs and on reading the source; I did not reproduce it locally. My execution was limited to:
  - the generator check, the scheduling, evidence and pieces self-tests, `suite_shards.py --selftest`, `ci_events.py --check` and `--selftest`;
  - the `--list` selections;
  - one revert probe and six mutation probes.
- **Where the docs evidence comes from.** The equality, controls and timings for the docs legs are the author's published receipts at `26838a11`. I checked them against the manifest digests and spot-checked them, but did not re-run them.
- **No hosted after-times.** Every exact-head job was cancelled near 10 minutes, because F1 tripped fail-fast. Only partial windows exist: docs builder leg 1 took 287 s on hosted (projection basis 520 s), and the two elaboration legs were still running at 537 and 542 s when cancelled. The elaboration margin of 55 s, and the 1193 s contended sensitivity, remain unconfirmed.
- **Scope-change items not re-judged.** The RTL workflows still trigger on `pull_request` at this head, which item 1 of the scope change removes. The PR body defers RTL trigger changes and signing to a follow-up under the fixes-only ruling, and earlier rounds accepted that. I did not re-judge it.
- **No manager source bank** runs at this head. Physical calibration was NOT RUN, and field skips are not hardware proof.
- **Probes and restore.** My probes ran in this clone and in disposable clones under `scratch/`. Afterwards (`receipts/restore_verification.txt`):
  - HEAD, index tree and worktree all equal `771055d8`;
  - no untracked or ignored files remain, after I removed the `__pycache__` directories my runs created;
  - all six gitlinks are as committed, and the submodule worktrees are clean;
  - `act_ci.py` SHA-256 is unchanged.

## Pending manager duties

- Decide F1. Because `scripts/act_ci.py` is SHA-pinned, its fix and repin need a public coordinating-role decision. Then re-read the exact-head hosted docs run.
- Read back the hosted docs and elaborate wall clocks against the 1665 s and 1745 s projections once a run is not cancelled. Distinguish executed jobs from skipped and cancelled contexts.
- Carry R1 and R2 to the residue checklist.
- Build and validate the current-dev merge candidate (source base `fa7347fc`, live dev `f6260253`) with the builder and native banks, and handle act acceptance.

## Receipts

Every published receipt is listed in `MANIFEST.sha256`. The scripts are `scripts/mutation_probe.sh` and `scripts/recompute_projections.py`.

R636-6 FINISHED
