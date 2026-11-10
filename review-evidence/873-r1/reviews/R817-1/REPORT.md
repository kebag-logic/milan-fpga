[R817] POSITIVE - exact head 88e1041c9b100c389f3629dfcf3185ad3be9c3f4

# R817-1: internal cleared-context review of issue #873 / PR #875

- Exact head `88e1041c9b100c389f3629dfcf3185ad3be9c3f4`, tree `aadd493164d34bd1e5c65b165abff6f8e2b1d1a4`.
- Three commits on source base `45c0b56c1f4a8a52878815fdcb1359d18e2c5b1c` (also the live `dev` tip named in this round's brief).
- Delta: `scripts/act_ci.py` (+364/-59) and `docs/testing/CI_WORKFLOWS.md` (+65/-10). No workflow, dispatcher (`ci/act/*.go`), evidence-format or attestation file is touched.
- Order of reconstruction: AGENTS.md and CONTRIBUTING.md, then docs/README.md, then the #873 body and its public comments, then the #737 CPU rulings, `ci/act/cpu_ranges.go` and `job_admission.go`, then the diff and its history, then the published evidence packet (`review-evidence/873-r1` at `5e97bbf7`) and the exact-head hosted check runs.
- Prior public review findings on PR #875: none. Before this round the PR held only the two review-start comments, R817-1 and R818-1, so there was nothing to resolve or retain.

Verdict: **POSITIVE**. Findings: no BLOCKER, MAJOR, MINOR or RESIDUE. Four SUGGESTIONs (S1 to S4) and two observations outside the reviewed delta (O1, O2). All five lenses are covered clean at this head.

## What was checked against the brief's six questions

1. **The default command line behaves exactly as before. This is shown by executed probes, not taken from the author's text.** `scripts/probe_default_equivalence.py` loads the base and head runners side by side (receipt `receipts/probe-default-equivalence.log`, rc 0). It found these identical:
   - `parse_cpu_ranges`: result or refusal text over 3,031 generated inputs, at host sizes 1, 12, 16, 32, 64, 128 and 512;
   - `job_cpu_ranges`: over five booked-range sets, concurrency 0 to 10, and slots 0, 1 and 63;
   - `replay_container_concurrency`: on every shipping workflow and on all four together (4 each);
   - the full act argv `build_act_command` emits for every workflow and five range sets, as base vs head-default vs head with an explicit `--jobs 4 --job-cpus 16 --job-memory 8`. The probe printed `--concurrent-jobs 4`, `MILAN_CI_FALLBACK_CPUS=12` and the `--memory=8g --memory-swap=8g` option word;
   - `main()`: status, final error line and reached collaborators for 13 argvs. These cover accepted 16- and 12-CPU ranges; 8- and 6-CPU ranges refused at the default; unaligned, overlapping, beyond-host and missing ranges; `--pr 0`; `--dry-run`; both live self-tests; and `--selftest` with a PR argument. The only difference is the argparse usage banner, which now lists the three new options; the error line is identical.

   `scripts/probe_constants.py` (rc 0) also finds all 73 module constants shared by base and head equal. `SLOT_MEMORY_MAX` is still `"36G"`. The removed names are exactly `CONCURRENT_JOB_LIMIT`, `CONTAINER_CPU_LIMIT`, `CONTAINER_MEMORY`, `FALLBACK_CPU_LIMIT` and `SLOT_JOB_RANGES`.
2. **Every `--cpu-ranges` refusal holds at every width.** The same probe checks the head's `parse_cpu_ranges` against an oracle written from #873's words: canonical text, a width the geometry names, aligned to that width, within the host, pairwise disjoint. It runs over the same 3,031 inputs at geometries 4x16x8, 4x8x8, 8x8x4, 4x6x8 and 8x6x4, at host sizes 6 to 512, and matches in every one of the 35 combinations.
3. **Memory is bounded by construction, and refused before any collaborator.**
   - An exhaustive grid in the same probe (jobs -1 to 10, widths 0/4/6/8/12/16/32, memory -1 to 10 GiB) shows `JobGeometry` accepts exactly the shapes with 1 <= jobs <= 8, width in {16, 8, 6}, 1 <= cap <= 8, jobs x cap + 4 <= 36 and jobs x width <= 64.
   - `main` builds the geometry before `--cpu-ranges` is parsed, inside the same `Refusal` handler, before `execute_pr_run` (`scripts/act_ci.py:17479-17484`). The arms show `reached == []` for the memory, CPU and ninth-job refusals.
   - The runtime admission word is checked separately by `scripts/probe_admission_bound.py` (rc 0). `--concurrent-jobs` is `min(jobs, booked ranges)` when 1, exactly `jobs`, `jobs + 1` or 12 ranges are booked, at 4x16x8, 8x6x4 and 2x16x8. So the slot never needs more than jobs x cap + 4 GiB.
   - The geometry is read only on the main thread. `run_with_cleanup_signals` calls the action inline (`scripts/act_ci.py:477-485`), and the CPU monitor's reader thread never reads `JOB_GEOMETRY`. A new thread's empty context therefore cannot silently fall back to the default.
4. **The measured basis and the 4 GiB judgement.** See "Judgement on the 4 GiB cap" below. In short: a 4 GiB cap carries a real risk of OOM for the upper tail. The runner fails closed on that in an isolated slot. Raising the slot limit is not required for this PR to be correct, and the PR rightly leaves it to the host owner.
5. **Self-test arms and planted defects.**
   - Clean clones, 82 s wall time, all concurrent:
     - head `--selftest`: PASS with 657 `ok` (rc 0);
     - head flat isolated install: PASS with 655;
     - base: 623 and 621;
     - head small-host control: PASS.
   - With label line numbers normalised, every one of the base's 623 (621 flat) arms is present and passing at head as a multiset. Exactly 34 arms are new (`receipts/arms/`).
   - The author's 22 published planted defects were re-run from the data fields of `mutants.json` with a reviewer-owned harness (`scripts/replay_author_mutants.py`). All 22 were killed, and each observed FAIL set equals the published one. Two of them (default width 8, and the inclusive memory bound) end in an uncaught `Refusal` whose text names the cause. The inclusive memory bound fails at import, because the default geometry itself is refused.
   - 18 independent reviewer mutants (`scripts/plant_defects.py`): 16 killed and 2 survived (S1, S2). Neither survivor can produce a false attestation.
6. **Docs.** `docs/testing/CI_WORKFLOWS.md:2272-2283, 2339-2340, 2355-2406, 2831-2833` state:
   - the width rule;
   - the admission bound;
   - both construction bounds with `SLOT_SERVICE_MEMORY_GIB=4`, `SLOT_MEMORY_MAX=36G` and `REPLAY_CPU_LIMIT=64`;
   - a five-row table, whose rows match the exhaustive grid;
   - #835's measured basis, matching the #873 body word for word in its figures;
   - the unchanged default;
   - the 4 GiB caveat;
   - the calibration the manager owes (item 4), with "Until that replay is recorded here, the default does not change."

## Judgement on the 4 GiB cap (brief question 4)

- **Would 4 GiB OOM the jobs that peaked above it?** Some of them, plausibly yes. "Not necessarily" is right only for a peak made of page cache.
  - Evidence that peaks are real working set for these tools: `CI_WORKFLOWS.md` records a 2 GiB trial that killed the largest Yosys shard (2.45 GiB peak under 8 GiB), and an earlier 4 GiB trial of the publication census that "killed an elaborator".
  - Measured classes above 4 GiB at 12 CPUs, the narrowest width measured:
    - capture campaign: 5042556928 B = 4.70 GiB;
    - Yosys source build: 5117616128 B = 4.77 GiB;
    - Verilator source build: 4793225216 B = 4.46 GiB;
    - census: 5201534976 B = 4.84 GiB.
  - #835's container maximum was 7.8 GiB, and its median 3.4 GiB.
  - At 6 CPUs some budgets shrink by design. `CI_TOOL_BUILD_JOBS` and `VERILATOR_JOBS` follow `nproc`. The census derives `floor(2 x 4 GiB / (3 x 1242214400)) = 2` workers from its own `memory.max`. Campaign pools stay at 4. None of these classes has been measured at 6 CPUs or at a 4 GiB cap, so a 4 GiB OOM in the 8 x 6 calibration is a realistic outcome, not an edge case.
- **Does the runner stay honest if it OOMs?** Yes, in an isolated slot. Slot 1 and above read the slice's hierarchical `memory.events`, so any OOM refuses the evidence (`valid build: False`, rc 2). That is a valid "4 GiB is too small" calibration result, not a candidate verdict. In slot 0 an OOM is not counted (`CI_WORKFLOWS.md:2881-2883`) and would surface as a job `FAILED`. That limitation exists at base too and is not changed by this PR. It makes running the calibration in an isolated slot a manager duty (below).
- **Should the slot limit rise instead?** It is not required for this PR. #873 item 2 binds the geometry to "the slot's memory limit" and does not ask to change it, and the PR keeps the bound fail-closed. Some arithmetic for the owner's decision, using the 73980592128 B (68.9 GiB) host measured during this round:
  - 8 x 8 GiB + 4 = 68 GiB is 99% of the host, so it is not viable on a shared host;
  - 8 x 6 GiB + 4 = 52 GiB is 75% of the host;
  - 8 x 5 GiB + 4 = 44 GiB is 64% of the host.

  Inside today's 36G, 4 GiB is the only per-job cap that allows 8 jobs. Shapes inside 36G with a larger per-job cap are 6 x 8 CPUs at 5 GiB (34 GiB, 48 CPUs) and 5 x 6 CPUs at 6 GiB (34 GiB, 30 CPUs).

  Recommendation: run item 4 at 8 x 6 x 4 GiB in an isolated slot first. If its `slot-memory.json` shows `oom_free: false`, the cap/slot choice becomes a recorded host-allocation decision, not a code change in this lane. Raising the cap pre-emptively would trade host headroom that is shared with other work for an outcome that has not been measured.

## Findings

### S1 SUGGESTION - Tests - `scripts/act_ci.py:4947`; new arms `scripts/act_ci.py:7871-8004` - no arm books more ranges than `--jobs`
- Authority/evidence: The construction bound (#873 item 2) holds at runtime only because act's admission word is `min(geometry.jobs, len(booked ranges))`.
  - Reviewer mutant M07 (`str(len(BOOKED_CPU_RANGES.get()))`) survives the full head self-test (`receipts/planted-defects.log`, `receipts/planted-M07.log`).
  - The same mutant survives at base (`receipts/base-m07-selftest.log`, rc 0), so the gap predates this PR.
  - Today's code is correct (`receipts/probe-admission-bound.log`).
  - No new arm claims this property: the 8-job arms book exactly 8 ranges.
- Impact: none at this head. A future regression of the clamp would not be caught offline. Live, the placement audit compares each container to `ranges[:jobs]`, so a container on a further range is "unbooked" and the replay is refused. The slot would already have run over-subscribed by then, but no false attestation is possible.
- Recommended: an arm booking `jobs + 1` or more ranges, at the default and at 8 x 6 x 4, that requires `--concurrent-jobs == jobs`.
- Verification: M07 is killed by name.

### S2 SUGGESTION - Tests - `scripts/act_ci.py:4622`, arm at `scripts/act_ci.py:7253` - the OOM refusal's named cap is pinned only against itself
- Evidence: Reviewer mutant M17 (the refusal names `DEFAULT_JOB_GEOMETRY.container_memory` rather than the run's cap) survives, because the arm compares `message == memory.refusal()`.
- Impact: message text only. During an 8 x 4 GiB run the operator could read "8g" while the verdict stays correct.
- Recommended: one arm under a 4 GiB geometry requiring "a job container's 4g".

### S3 SUGGESTION - Docs - `docs/testing/CI_WORKFLOWS.md:2401` and `:2403` - say where an OOM is counted, and the calibration's cap
- Evidence: "But an OOM anywhere in the slot refuses the replay (below)" is accurate only through its "(below)" pointer to the slot-0 caveat at `:2881-2883`. The calibration sentence at `:2403` gives no cap, though `:2397` implies 4 GiB.
- Recommended wording: "But in an isolated slot an OOM anywhere refuses the replay; slot 0 does not count it (below)." and "...at eight jobs of six CPUs and four GiB, in an isolated slot, ...".

### S4 SUGGESTION - Docs - `docs/testing/CI_WORKFLOWS.md:2386-2392` - link the measured basis
- Evidence: The figures (7.7 of 64 CPUs, 2.0 and 7.3 busy CPUs, 3.4 and 7.8 GiB, 149 min, 71 jobs, 574 job-minutes, 137 to 150 min) match the frozen #873 body. Neither the doc nor the issue links the replay receipt they came from, and none was found on PR #835. A cold reader can trace them to #873 but no further.
- Recommended: cite "#873" next to the figures, plus the receipt location once published.

### Observations outside the reviewed delta (not findings against this head)
- **O1.** `docs/testing/CI_WORKFLOWS.md:2382` and `:2719` (unchanged by this PR) say "The host now has 61 GB". The host measured 73980592128 B (68.9 GiB) during this round. This is a candidate for a separate issue. It is not this lane's scope (AGENTS section 4).
- **O2.** The author's calibration plan in the evidence packet (`author/CALIBRATION.md`, not in the head tree or the PR body) says "Yosys source builds at 5.26 GiB". The recorded 5264482304 B is 4.90 GiB (5.26 GB). The manager should correct this before using that plan.

### Comment-rule check (owner 2026-10-15)
- The 380 added lines of the delta contain no lane labels, review rounds, reviewer IDs, issue-comment IDs or U+2014.
- They cite only #730, #737, #835 and #873 (`git diff 45c0b56c..88e1041c | grep '^+'`, scanned in this round).
- An existing self-test label carries a reviewer ID ("R633-4's point"). It predates the delta, is tracked by #746, and is not RESIDUE here.

## Per-lens clean results

```text
[R817] PASS Conformance - scripts/act_ci.py:107-126,4742-4796,4835-4866,4903-4952,17356-17370,17479-17484; #873 items 1,2,3,5; ci/act/cpu_ranges.go:16-73 - item 1: constants replaced by JobGeometry, 8 jobs accepted on 6/8-CPU aligned ranges with --job-cpus, refusals unchanged at every width (oracle, 35 combinations); item 2: jobs x cap + 4 <= 36 and jobs x width <= 64 refused before any collaborator (exhaustive grid; arms reached == []); item 3: 623/621 base arms retained, 34 new; item 5: docs state basis and default; item 4 is the manager's calibration (pending duty). Pinned dispatcher contract holds: fallback 6/8 within 1..16, range width == fallback, limit = min(jobs, ranges) <= len(ranges).
[R817] PASS RTL - scripts/act_ci.py:477-485,4742-4796,4857-4866,4903-4952,5499-5613,6017-6040; ci/act/cpu_ranges.go; ci/act/job_admission.go - no HDL in the delta; the lens is applied to the runner's architecture and its interfaces: the context variable is read only on the main thread (no thread-context fallback to the default), the dispatcher receives a fallback and ranges it accepts, the placement audit's range set equals the dispatcher's admitted set, the evidence files' formats are unchanged, and the slot unit still sets MemoryMax=36G (constants probe).
[R817] PASS Robustness - receipts/probe-default-equivalence.log, receipts/probe-admission-bound.log, scripts/act_ci.py:4760-4786 - malformed input (non-integer, bool, string, float), min/max (0/9 jobs, widths 4/12/32, caps 0/9, exact bounds), fewer/more booked ranges than jobs, host sizes 1 to 512, the default configuration byte-identical to base, and --selftest combined with each geometry option all refused or handled as specified.
[R817] PASS Tests - receipts/head-selftest.log, receipts/head-flat-selftest.log, receipts/arms/arm-retention-summary.txt, receipts/author-mutants-replay.log, receipts/planted-defects.log - 657/655 ok at head, all base arms retained, 34 new; the author's 22 planted defects reproduce with identical FAIL sets; 16 of 18 reviewer mutants are killed and the 2 survivors are S1/S2 (no false-attestation path).
[R817] PASS Docs - docs/testing/CI_WORKFLOWS.md:2272-2283,2339-2340,2355-2406,2831-2833; receipts/gates/*.log - every geometry statement checked against code and the exhaustive grid; measured figures equal #873's; docs_check, doc_style, doc_paths, docs_inventory --check, ci_events --check, py_idiom, hygiene and todo-ownership gates pass on a clean clone with submodules at their gitlinks; behave 508/508; git diff --check clean; U+2014 absent from the delta.
```

## Reviewer-owned completion ledger

| Lens | Result | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | #873 body and comments; `scripts/act_ci.py` delta; `ci/act/cpu_ranges.go`; default-equivalence, oracle and grid probes | R817-1 | `88e1041c9b100c389f3629dfcf3185ad3be9c3f4` |
| RTL | CLEAN | Runner architecture and interfaces: threading, dispatcher contract, placement audit, evidence formats, constants (no HDL in the delta) | R817-1 | `88e1041c9b100c389f3629dfcf3185ad3be9c3f4` |
| Robustness | CLEAN | Boundary, malformed-input and over-booked probes; geometry refusals; usage errors | R817-1 | `88e1041c9b100c389f3629dfcf3185ad3be9c3f4` |
| Tests | CLEAN (S1, S2 optional) | Head, base and flat self-tests; arm retention; 22 author and 18 reviewer planted defects | R817-1 | `88e1041c9b100c389f3629dfcf3185ad3be9c3f4` |
| Docs | CLEAN (S3, S4 optional) | `docs/testing/CI_WORKFLOWS.md` delta; docs gates; behave; comment-rule scan | R817-1 | `88e1041c9b100c389f3629dfcf3185ad3be9c3f4` |

## Real limits of this round

- No replay, no `--dry-run` against GitHub, no Docker, no act, no slot, and no live self-test. The geometry's effect on act is proved offline on the generated argv, as the existing arms prove the default.
- The pinned Go dispatcher was read, not executed: no Go toolchain is on this host.
- `check_em_dash.py` refused to judge because its pinned Markdown renderer is not installed here (`receipts/gates/em_dash.log`, rc 2). A direct scan of the delta for U+2014 found none. The author's packet reports the full `docs.yml` steps.
- The `external` submodule is not initialised in either clone. The gates that need submodules ran with `protocol-processor`, `gptp-processor`, `lwSRP` and `tsn-c-stack` at their gitlinks.
- Hosted runs at this head were still in flight when snapshotted at 2026-11-10T10:28:37Z (`receipts/hosted-check-runs-snapshot.tsv`): 13 completed success, 1 skipped (Physical gPTP, nightly/manual), 20 in progress and 18 queued. No hosted verdict is claimed.
- No manager source bank was run or inferred. Physical calibration NOT RUN, and #873 item 4 is NOT RUN.

## Pending manager duties

1. **#873 item 4, the calibration replay** (this PR's own act): 8 x 6 CPUs at `--job-memory 4`, **in an isolated slot (1 or above)** so an OOM is counted, on a head that also has a 4 x 16 receipt. It runs from the independently audited install of this head's runner (the runner-change bootstrap). Report wall time, per-job durations, suite timeouts and `slot-memory.json` peak/max/oom.
   - The docs say the result is "recorded here". A follow-up commit to `CI_WORKFLOWS.md` therefore changes the Docs lens's scope and needs a Docs re-cover at that head.
   - Record publicly on #873 that item 4 is the manager's. Today only the executor's TAKEN comment and the PR body say so, while the PR carries `Closes #873`.
2. If the calibration ends `oom_free: false`, record the cap/slot choice as a host-allocation decision (see the judgement above).
3. Exact-head hosted `rtl-fast`, `verilator-suites` and `yosys-portability` evidence; the act replay of the exact head; current-dev candidate validation; post-merge containment.
4. Merge only with explicit maintainer authorisation and the second (external) positive review.
5. O1 and O2 above, and optionally S1 to S4.

## Packet

- `scripts/`: portable probes and harnesses, each with usage in its docstring or header. All are run as `python3 -I <script> ...` or `sh verify_integrity.sh <checkout>`.
- `receipts/`: raw logs and rc files. Scratch paths are rewritten to `<packet>` and `<review-clone>`. `receipts/inputs/author-mutants.json` is the published input (sha256 `8cca76a5734f04ba07742d291feea63ee73afb7cd2c9f0c0364dd7b9017c8f54`).
- **Clone integrity after the probes** (`receipts/integrity.txt`): both the review clone and the scratch head clone are at `88e1041c`, tree `aadd4931`, status clean, worktree and index equal to HEAD, no assume-unchanged or skip-worktree entries. Index and tree agree on every mode, blob and path. Blob ids and modes of `scripts/act_ci.py` (`41f9ae12`, 755) and `docs/testing/CI_WORKFLOWS.md` (`ac6a16e4`, 644) match HEAD. All six gitlinks match the tree: `external efeb541a`, `gptp-processor 1616fc8f`, `protocol-processor 044cb25f`, `third_party/lwSRP 08ee86e8`, `third_party/tsn-c-stack 70936b77`, `third_party/verilog-axis 48ff7a7e`.

R817-1 FINISHED
