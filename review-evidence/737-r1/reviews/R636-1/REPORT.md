[R636] NEGATIVE - exact head cf9c936697a06e44c41681bcc12dc612a3242eb2

# R636-1: internal cleared-context review of PR #739 (issue #737, round 1)

- Head `cf9c936697a06e44c41681bcc12dc612a3242eb2`, tree `a5eb619c5c9ead508e7189fd77527d84d2c4fdda`. Source base `fa7347fc59173f90e4feec2df207692e6e6e72ec`, 24 commits, 65 files.
- Scope reviewed: the round-1 assignment (6160775078) and every later ruling: driver refactor (6160937413), signature design (6160962404), CI-contract ruling (6161122704), fail-fast (6161180121), media-clock ruling (6161771913), fork and tally ruling (6162403147), CPU rules (6166855177) moved into this round by 6167284204 and corrected by 6167288337. The scope change in 6166823105 is round 2 and is not scored here.
- Prior public review findings on this PR: none. At review start the PR held only two review-start notices and no review comments, so there is nothing to resolve or retain.
- All five lenses were applied. Each finding lists every lens it touches.

## Verdict basis

Two BLOCKERs, three MAJORs and three MINORs are open.

The design and most of the machinery are sound:
- driver-derived inventories;
- exact-once union verification;
- unchanged step conditions;
- cache keys;
- the CPU-range parser and admission gate;
- the manifest base.

My independent runs confirm them where I could execute them (see "Verified clean"). The rest does not work as written:
- Three of the six union jobs, and the `verilator-suites` collector, cannot derive their inventories on a hosted runner.
- The protected `docs-check` worker runs a selftest that needs a Git identity hosted runners do not have.
- The new fail-fast watcher hangs whenever rtl-full's scope gate skips its matrices.
- The watcher also turns any API error into whole-head cancellation.
- Worker time limits were set just above unmeasured projections, after the margin guard was re-based so that it no longer bounds them.

## Findings

### B1 - BLOCKER - Conformance, RTL (architecture/interface), Robustness, Tests
**Where:** `.github/workflows/rtl.yml`, jobs `union-milan_dp`, `union-milan_dp_render`, `union-pp_shadow` and `verilator-suites`. Generator: `scripts/ci_suite_workflows.py:13-41`. Callers: `scripts/ci_suite_pieces.py:81` (`union()` calls `inventory()` first) and `scripts/ci_suite_collect.py:42`.

**Problem:** the union jobs and the `verilator-suites` aggregate run `actions/checkout@v4` with its defaults, so no submodules are fetched. Each then derives the inventory afresh: `inventory()` runs `make ci-list` for `milan_dp`, `milan_dp_render` and `pp_shadow`. Those Makefiles evaluate `scripts/pp_srcs.py` and `print-srcs` at parse time, and both require `protocol-processor/hdl`.

**Evidence:** `receipts/probe-union-without-submodules.txt` uses a clean clone at the exact head with no submodules, which is the hosted union-job checkout.
- `milan_dp`, `milan_dp_render` and `pp_shadow` are refused with `Makefile:155: *** scripts/pp_srcs.py failed`.
- `milan_dp_mclk`, `capture_coherence` and `maap` pass.

The same derivation succeeds in a full checkout (`receipts/driver-inventories-at-head.txt`). The author's collector receipt (`physical-collector.json`) was produced in a full checkout. A local replay does not catch this either: the runner initialises submodules in the materialized checkout before act copies it into every job.

**Impact:** on every RTL-relevant PR, three union jobs fail. `verilator-suites` then fails its own "Require every case union to succeed" step and its collector, so the protected context is red whatever the tests did. Through the same-repository watcher, it also cancels the sibling workflows.

**Required outcome:** every job that derives a driver inventory has that driver's prerequisites, for example the same submodule fetch the workers use. The hosted environment and the local replay must agree on this.

**Verification:** a control that runs each union derivation from a submodule-less checkout of the head and requires success, plus one hosted run of the unions and the aggregate at a corrected head.

### B2 - BLOCKER - Tests, Robustness, Conformance
**Where:** `scripts/ci_case_receipts_selftest.py:37-45` (`git("commit", ...)`, "Run fixture Git with the existing configured identity"). It runs in the `docs-gates-0` step "CI scheduling and evidence controls" (`.github/workflows/docs.yml:441`, template `.github/ci-templates/docs.yml:461`).

**Problem:** the selftest's fixture commit depends on an ambient Git identity. Every existing fixture in this repository that commits supplies its own identity: `scripts/ci_scope_history.py:28,43`, `scripts/check_em_dash.py:442`, `scripts/check_gptp_docs.py:828`, `scripts/merge_containment_selftest.py:198` and `scripts/act_ci.py:6209`. This PR's own `d08c3d693` made the plan fixtures identity-independent, but this one was not.

**Evidence:**
- `receipts/selftests-without-git-identity.txt`: with no configured identity, this selftest returns rc 1, and the 11 other new selftests pass.
- `receipts/receipts-selftest-git-identity-error.txt`: `git commit` returns rc 128, "unable to auto-detect email address". With a fixture identity supplied, the same selftest passes.

**Impact:** a runner without a configured identity fails `docs-gates-0`. GitHub-hosted runners have none by default, and the act container very likely has none either. That makes the protected `docs-check` aggregate red on every PR. On a same-repository head the watcher then cancels all four workflows, and a local replay stops at its first failed job.

**Required outcome:** the selftest supplies its own fixture identity, without changing global configuration, as the sibling fixtures do.

**Verification:** run the selftest with an empty HOME and no identity; expect rc 0.

### F1 - MAJOR - Robustness, RTL (architecture: termination/default path), Conformance, Tests
**Where:** `scripts/ci_fail_fast.py:63-72` (`observe`: complete only when `set(names) == expected`) and `scripts/ci_runtime_workflows.py:82`. The generated rtl.yml `EXPECTED_JOBS` lists the expanded names `Verilator shard 0/16` … `Yosys shard 3/4`.

**Problem:** when `full-ci-gate` reports `run_full == 'false'` (a docs-only same-repository PR, or such a push to dev), GitHub skips the matrix jobs before expansion. It reports each one as a single job named by its raw expression.

**Evidence:**
- Hosted run 38273578232 reports `Verilator shard ${{ matrix.shard }}/${{ matrix.total }}` with conclusion skipped (`receipts/skipped-matrix-job-names-run-38273578232.json`).
- Fed that job list, the production `observe` returns `(False, None)`, with 20 expected names that can never appear (`receipts/probe-watch-skipped-matrix.txt`).
- The watcher's timeout is 120 minutes, and `ci-manifest` needs the watcher.

**Impact:** for every non-RTL same-repository head:
- the watcher polls for 120 minutes and ends unsuccessfully;
- the rtl-full run lasts about two hours and is not green;
- its manifest waits behind it;
- the 30-minute-per-workflow target fails for those heads.

No fixture exercises skipped matrices.

**Required outcome:** the watcher concludes correctly when jobs are skipped before matrix expansion. This applies to any job whose reported name is not its expanded name.

**Verification:** a fail-fast control fed the real skipped-matrix job shape, which must report completion with no failure, plus one hosted docs-only run.

### F2 - MAJOR - Robustness, RTL (architecture: error path), Conformance, Tests
**Where:** `scripts/ci_fail_fast.py:129-135`. The watch loop calls the API every 5 s with no error handling. The step `Cancel this run and sibling workflows` has `if: failure()`.

**Problem:** any HTTP or transport error while watching ends the watch step non-zero. Examples: a transient 5xx, a timeout, or 403 rate limiting. The failure-only step then cancels the run and every sibling workflow at the head.

**Evidence:**
- `receipts/probe-watch-api-error.txt`: a 403 and a 502 each raise out of `main()`, so the step fails and the next step is the cancel step.
- Each watcher makes about 12 requests a minute for its whole workflow. Four workflows at roughly 20-35 minutes each come to about 1,300 requests per head. GitHub documents a primary limit of 1,000 requests per hour per repository for the job token, shared with every other run in the repository.

**Impact:**
- An ordinary full PR run is likely to exhaust the limit.
- Any transient API error cancels a healthy head, so all four workflows stop, and the watcher job itself fails.
- This produces a false failure and wastes the hosted run. It is the opposite of the fail-fast intent: a failed job, not a failed observer, should stop the run.

**Required outcome:**
- An observer error is never treated as a failed job: retry with bounded backoff and honour the rate-limit headers.
- The request rate fits the documented limit with the four workflows, and other PRs, running together.

**Verification:** controls for 403/429 with rate-limit headers, for a 5xx and for a timeout. Each must not issue a cancel request.

### F3 - MAJOR - Robustness, Tests, Conformance
**Where:**
- `scripts/suite_shards.py:289-296`: `verilator_job_limits` rewrites `${{ matrix.shard == 15 && 60 || 29 }}` to 60.
- `scripts/suite_shards.py:402-405`: a new 1620-s bound.
- `scripts/ci_suite_workflows.py:58`: the 29-minute limit for regular workers.
- `scripts/ci_gate_workflows.py:134`: the 27-minute limit for gate workers.

**Problem:** the existing safety control refuses a worker predicted above 60% of the job's timeout. CI_WORKFLOWS.md records it was motivated by #696 reaching its 120-minute limit. It is now evaluated against the 60-minute leg-A limit for all 16 workers. Meanwhile the PR lowered the regular workers' own limit to 29 minutes.

**Evidence:**
- `receipts/verilator-worker-headroom.txt`: the 15 regular workers are projected at 1491-1605 s, which is 86-92% of their own 1740-s limit. All 15 would be refused by the guard read against their own limit. The guard passes only because it reads 2160 s.
- These projections are apportioned from local leg times, not hosted measurements (CI_WORKFLOWS.md says so).
- The new 1620-s bound has no control: making it vacuous leaves `suite_shards.py --selftest` passing (`receipts/selftest-mutations.json`).
- Gate workers: `receipts/gate-worker-margin.json` matches the published hosted baseline step windows (run 38495894212). It puts `elaborate-gates-0` at no less than 1540 s against its new 1620-s limit, 95% with 80 s of margin. That is before the added steps, and before the cold caches that this head's new keys force on first use. The base elaborate job had no job-level limit.

**Impact:**
- Ordinary hosted variance or a cache miss converts slowness into a timed-out, red protected context. With `fail-fast: true` and the watcher, it cancels every workflow at the head.
- A control that guarded exactly this was re-based so the change would pass. AGENTS.md section 8 forbids weakening a test to obtain a pass.

**Required outcome:** either of these:
- every worker keeps the existing headroom rule against its own limit, with limits and worker counts sized to measured durations; or
- a public ruling explicitly accepts a reduced margin, with each limit's margin stated against hosted measurements.

The 1620-s refusal needs a planted control.

**Verification:** `suite_shards.py --selftest` refuses a regular worker over its own-limit bound, and the hosted per-job durations at the corrected head are recorded against each limit.

### F4 - MINOR - Conformance, Robustness
**Where:** `scripts/act_ci.py:109` (`CONTAINER_MEMORY = "8g"`, was 16g) and `:162` (`SLOT_MEMORY_MAX = "36G"`). Docs: CI_WORKFLOWS.md "Containers retain the measured eight-GiB limit".

**Problem:** CPU rule 4 requires the limit to be sized "from the measured peak memory per job". The recorded peaks come from:
- four Yosys shards (0.6-2.5 GiB);
- the publication census (5.34 GiB);
- Verilator suite workers run at "a two-build semaphore with four compiler jobs per build" (largest 4.13 GiB; HANDOFF.md).

No job was measured at the shipped configuration, where Verilator `-j 0` / `VERILATOR_JOBS` uses all 16 booked CPUs: `capture_coherence` running 4 builds of 4 compilers each, the 16-way compiles of the large datapath models, or the sbt/LiteX jobs. The issue's own baseline peaked at 18.3 GiB with four 4-CPU jobs.

**Impact:** the per-container cap was halved while compile parallelism quadrupled, without a peak measured for the heaviest jobs at that width. OOM kills would fail the replay, fail-closed, rather than size it.

**Required outcome:** peak memory per job class at the shipped 16- and 12-CPU widths, recorded, with the cap justified from it. The pending full replay can supply this if it records per-job peaks.

**Verification:** per-container `memory.peak` and OOM events for every job of one full replay.

### F5 - MINOR - Tests
**Where:** `scripts/ci_fail_fast_selftest.py`.

**Problem:** the first-failure set is `failure`, `cancelled`, `timed_out` and `action_required` (`ci_fail_fast.py:69-70`). Narrowing it to `failure` alone leaves the selftest passing (`receipts/selftest-mutations.json`).

**Impact:** nothing would catch a regression that stops the watcher reacting to a timed-out or cancelled first job. That is the likely first failure under F3's limits.

**Required outcome:** a control for each listed conclusion.

**Verification:** the same mutation is killed.

### F6 - MINOR - Tests, Docs
**Where:** published `review-evidence/737-r1/author/case-evidence/comparison-summary.json` and `source-correspondence.json`.

**Problem:** the recorded unsharded/sharded comparisons that the driver ruling requires are bound to heads absent from the public remote: `e06f342f`, `06880253` and `9dd0817d` (`receipts/snapshot-heads-public.txt`). Five of the six suites are therefore tied to a source a cold reviewer cannot open. Only the `9a76ed5cf` group is public, and I verified it identical to this head on the listed paths (`receipts/source-correspondence-recheck.txt`).

**Impact:** five of the six equivalence claims cannot be independently reconstructed (AGENTS.md section 2). I re-ran one suite at this exact head (see below), but the others rest on author assertion.

**Required outcome:** publish the snapshot commits, or record the comparisons at a public head.

**Verification:** each comparison's head is fetchable and its listed paths diff empty against the merge candidate.

## Suggestions (non-blocking)

- **S1** `ci_gate_workflows_selftest.py`: no control for mixed scopes across the two elaborate workers. With leg 0 false and skipped and leg 1 true and successful, removing the consistency line (`ci_gate_receipts.py:98`) survives.
- **S2** `ci_manifest_selftest.py`: removing the step-level skip/failure refusal survives. Add a control with identical manifests that contain a skipped step.
- **S3** Each workflow's watcher holds a hosted runner for the whole run. Check the account's concurrent-job limit against about 40 simultaneous jobs per head before relying on the wall clock.
- **S4** `run_all_suites.sh:398`: each CI piece inherits its parent suite's full `suite_timeout`. No value is raised, but the per-case bound is looser than the parent's. Consider stating that in CI_WORKFLOWS.md.
- **S5** Every generated job now exports `MAKEFLAGS=-j1 --no-print-directory`. No hosted or replay execution at this head shows that the existing MAKEFLAGS-sensitive controls behave the same; the hosted run should be checked for them.

## Verified clean at this head (evidence per lens)

| Lens | Path:line / artifact | What was checked, against what |
|---|---|---|
| Conformance | `.github/ci-templates/*.yml` vs base `fa7347fc:.github/workflows/*.yml` | Templates equal the base workflows except cache keys/recipes, digest checks, `--jobs` budgets, `fail-fast: true` and the new controls step. No step condition was added or changed: `receipts/template-step-preservation.json` has zero `if` differences, and only setup/install run text changed. No timeout was raised. All runners are `ubuntu-latest`. |
| Conformance | 6 driver inventories (`receipts/driver-inventories-at-head.txt`) | Each comes from the driver's own `--list`/`ci-list`: 19, 31, 31, 66, 3 and 4 cases, equal to the published inventories. The strided legs cover each case exactly once. |
| Conformance | `receipts/cache-keys-at-head.txt` | Install and source-tool keys bind version, source digest and recipe digest. No install cache has a restore-keys fallback; the only fallback is the pre-existing Yosys result cache. |
| RTL | `git diff fa7347fc..cf9c9366 -- hdl sw .gitmodules third_party protocol-processor gptp-processor` (excluding one README count) | Empty. The split Makefile `build-*` recipes reuse the original Verilator lines unchanged. `-j 0` became `-j $(VERILATOR_JOBS)`, which defaults to 0. `sim_mclk.cpp` adds only an opt-in pass echo, and the mutant verdict still requires a named `[FAIL]`. |
| RTL | `ci/act/cpu_ranges.go`, `job_admission.go`, `fail-fast.patch`; `scripts/act_ci.py:4675-4707,4787-4793,5819-5892` | Ranges: aligned 16 or `FALLBACK_CPU_LIMIT=12`; overlap, missing and too-small ranges are refused by name. A token is reserved before create, `--cpuset-cpus` is set at create, and any options override is refused. The lease is held until the executor returns. One combined act invocation serves all workflows (one gate, limit 4). The monitor fails the run on update/move. Input digests equal the dispatcher receipt (`receipts/dispatcher-input-digests-at-head.txt`). |
| Robustness | `scripts/ci_case_receipts.py`, `ci_gate_receipts.py`, `ci_manifest.py` | Unions refuse missing, duplicate, failed, cancelled and skipped legs. The protected aggregates conclude `cancelled` in cancelled runs (`receipts/cancelled-rtl-fast-runs-jobs.json`). The comparator refuses incomplete and identical-cancelled manifests. |
| Tests | Real exact-head run of `pp_shadow`, unsharded and 4 legs (`receipts/pp-shadow-probe/`, `pp-shadow-union-controls.txt`, `pp-shadow-union-job-entry.txt`) | The production comparison is equal (4 cases, 2184 checks, rc 0). Refused: a leg removed, a case dropped from its leg, one checked byte changed (`vid73`), a duplicated leg, a wrong head, a missing worker, a missing log, and a log reporting a failure. |
| Tests | 17 selftests (`receipts/selftests/`) | All rc 0, including the CI contract (2186 items, 5020 arms). With both union checks removed together, the receipts selftest is killed (`receipts/selftest-mutation-union-both.txt`). |
| Docs | `docs/testing/CI_WORKFLOWS.md`, `docs/testing/CI_SIGNATURE.md` | Unit counts (79/62), case counts, baseline windows (1065/1441/593 s, re-derived from the hosted API: `receipts/doc-figure-checks.txt`, `baseline-runs-api-readback.json`), worker limits, the fork limit and the round-1 manifest boundary match the code. The F-findings need doc updates when fixed. |

## Hosted wall clock at this head

- No hosted run exists at this head: `actions/runs?head_sha=cf9c9366…` returns `total_count 0`, and the branch has none (`receipts/hosted-runs-at-head.txt`).
- PR #739 reports `mergeable: false`, `mergeable_state: dirty`.
- A merge-tree against live dev `fa820988` conflicts in `sw/firmware/ctrl/README.md` (`receipts/merge-tree-live-dev.txt`). This is consistent with no `pull_request` runs being created.
- Baseline, first job start to last job end, read back from the API at `7032bca5`: docs 34.0 min, elaborate 35.7, rtl-fast 19.1, rtl-full 77.5.
- There are no after-times to report. The 30-minute acceptance remains the manager's call.

## Reviewer-owned ledger

| Lens | Status | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | UNCLEAN (B1, B2, F1, F2, F3, F4) | rulings 6160775078…6167288337; templates vs base; generated workflows; inventories; cache keys; act_ci CPU/memory policy | R636-1 | cf9c936697a06e44c41681bcc12dc612a3242eb2 |
| RTL | UNCLEAN (B1, F1, F2) | hdl/sw/submodule diff (empty); split Makefiles; sim_mclk.cpp; ci/act Go admission/placement; act_ci scheduler; watcher control flow | R636-1 | cf9c936697a06e44c41681bcc12dc612a3242eb2 |
| Robustness | UNCLEAN (B1, B2, F1, F2, F3, F4) | union/gate/manifest refusal paths; watcher error and termination paths; timeouts vs projections; memory caps | R636-1 | cf9c936697a06e44c41681bcc12dc612a3242eb2 |
| Tests | UNCLEAN (B1, B2, F1, F2, F3, F5, F6) | 17 selftests; 9+1 selftest mutations; exact-head pp_shadow equivalence and planted controls; evidence re-read | R636-1 | cf9c936697a06e44c41681bcc12dc612a3242eb2 |
| Docs | UNCLEAN (F6) | CI_WORKFLOWS.md, CI_SIGNATURE.md, AGENTS/CONTRIBUTING lines, PR body, published evidence packet | R636-1 | cf9c936697a06e44c41681bcc12dc612a3242eb2 |

## Real limits

- **Hosted/act behaviour is inferred, not observed.** No hosted run exists at this head, and Docker/act were out of scope for me. B1, B2, F1 and F2 rest on:
  - exact-head reproductions of the hosted conditions (no submodules, no Git identity);
  - a real hosted job list from an earlier run;
  - GitHub's documented token limit;
  - production code paths.
- **Go controls not re-run.** I did not run the patched dispatcher's Go tests (no Go toolchain, and building act was out of scope). I verified only that its input bytes equal the published build receipt.
- **Python version.** Selftests ran on CPython 3.14 with PyYAML 6.0.3, not the pinned 3.12.3 / 6.0.2. The 3.12.3 interpreter available here lacks PyYAML.
- **One suite re-run.** Only `pp_shadow` was re-run end to end at this head. The other five equivalence and mutant claims rest on the published receipts (see F6). maap: 63 of 66 caught; media clock: 16 of 31 caught; both bound to non-public heads.
- **Not run.** No physical calibration, hardware, full banks or Vivado. Field skips are not hardware proof.
- **Clone restored.** After the probes, the review clone was verified byte-exact: 1353 tracked blobs and modes, the index, and 5 initialised gitlinks match; `external` is uninitialised as at start. I removed only the bytecode my own imports created (`receipts/clone-restore-verification.txt`).

## Pending manager duties

- Resolve the `sw/firmware/ctrl/README.md` conflict with live dev, so hosted runs can exist at all.
- Record the per-workflow hosted wall clocks, and per-job durations against each new limit (F3).
- Run the full trusted replay with booked ranges, recording per-job memory peaks (F4) and CPU placements.
- Validate the current-dev merge candidate, then post-merge containment.
- Independent external review (R637).

R636-1 FINISHED
