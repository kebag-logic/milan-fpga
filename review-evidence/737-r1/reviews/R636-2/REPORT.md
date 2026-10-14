[R636] NEGATIVE - exact head 2658a64c408bf87ae36574f36a6deeb34b2f297f

# R636-2: internal cleared-context review of PR #739 (issue #737, rounds 1 and 2)

- **Head and range.** Head `2658a64c408bf87ae36574f36a6deeb34b2f297f`, tree `d78031e7fec0f8439161c59ddf105f68d4b426c8`.
  - Full range `fa7347fc..2658a64c`: 44 commits.
  - The PR's own content is `fa820988..2658a64c`, 68 files; `fa820988` is the merged dev.
  - Round-2 delta `cf9c9366..2658a64c`, including the dev merge `abf7a923`.
- **Scope applied.**
  - Round 1: the assignment 6160775078 and every later [A10] ruling. These are the driver refactor 6160937413, the signature design 6160962404, the CI-contract ruling 6161122704, fail-fast 6161180121, the media-clock ruling 6161771913, and the fork/tally ruling 6162403147. The CPU rules 6166855177 entered this round through 6167284204, with correction 6167288337.
  - Round 2: the fixes-only ruling 6169768594, its additions 6169805715, the OOM evidence 6170460727 and the measurement permission 6172868895.
  - Not scored: the scope change 6166823105 (RTL off PR triggers, signature gate), which is the follow-up PR.
- **Order.** I reconstructed the task in the required order. My verdict and ledger were fixed before I read the prior public findings.
- **Coverage.** All five lenses were applied. Every finding lists all the lenses it touches.

## Verdict basis

One MAJOR and one MINOR are open. Five SUGGESTIONs do not affect the verdict.

The round-2 fixes are real and I confirmed each one by execution:
- the nested compiler budget;
- fail-fast on collector and tail failures, on raw skipped-matrix names and on observer errors;
- the per-worker headroom rule for Verilator workers;
- public-head comparisons;
- the cache paragraph;
- dependency-ready dispatch;
- the dev merge count.

R636-1's two BLOCKERs (B1 and B2) are also closed.

Two problems remain:
- **F1.** This PR's own CI-contract self-test grew from about 33 s to about 12.3 min. It runs on docs leg 0 (`docs-gates-0`), which is therefore projected above the 1620-second per-worker allowance this PR documents. The sizing evidence never measured that gate.
- **F2.** The memory sizing omits the heaviest in-job class that every local replay runs: the Yosys source build at the job's full width.

## Findings

### R636-2-F1 - MAJOR - Conformance, RTL (architecture: timing effects), Robustness, Tests, Docs

**Where:**
- `.github/workflows/docs.yml:398-410`: in `docs-gates-0` (job at `:111`), the steps "CI event and SHA contract gate" (`ci_events.py --check` and `--selftest`) and "Local act runner contract gate".
- `scripts/ci_gate_workflows.py:23,65`: every docs gate except "End-station builder gates" is placed on leg 0.
- `scripts/ci_events.py:8822-8857`: `_selftest_generated_gates`, 1913 arms, each a full `deepcopy` plus `check()`.
- `docs/testing/CI_WORKFLOWS.md:2625-2637`: the gate-worker allowance paragraph.
- PR body: "docs about 26 minutes including collection".

**Authority:**
- Ruling 6169768594 item 3: "the existing headroom rule applies to each worker against its OWN limit … Add more shards where a worker exceeds the rule … Record each limit's margin."
- `CI_WORKFLOWS.md:2629-2630`: "The 60% scheduling allowance is therefore 1620 seconds per gate worker."
- Issue #737 acceptance 1: at most 30 minutes per workflow.

**Evidence (`receipts/contract-timing/`):**
- **Base cost.** At base `fa820988` the full self-test takes 33.4 s for 3,096 arms on this host. The hosted baseline window for the whole step (`--check` plus `--selftest`) was 37 s in run 38495894291, so this host is no slower than the hosted runner for this single-threaded work.
- **Head cost.** One `check()` of the head tree costs 0.364 s against 0.012 s at base (`per-check.txt`).
- **Full run cannot finish in one command.** A direct single-process run at the head passed 1,582 generated arms in 585 s, then reached my command bound.
- **Split run.** Splitting the self-test executed every arm exactly once: 3,180 non-generated arms plus 731 + 561 + 621 generated arms, 5,093 in all, every one passing. Each generated arm costs a full-tree check in the real run, so the real run takes about 43.6 s + 1,913 × 0.364 s ≈ 740 s, roughly 12.3 min.
- **Projection (`docs-gates-0-projection.json`).**
  - The hosted baseline `docs-check` took 2,039 s. Leg 0 keeps all of it except the 1,065-s builder gate.
  - Replace the contract step's 37 s with about 740 s, and add the new 14.4-s controls step.
  - That gives about 1,691 s before the record and upload steps and before any growth of the act runner self-test, against the 1,620-s allowance.
  - The workflow wall clock adds the aggregate, the collector, up to one 120-s watcher poll and the tail job. That is about 31-32 min, against the 30-min target.
- **Unmeasured gate.** The author's published docs-gate receipts (`author-r2/gate-receipts/docs-gates/`) contain no entries for gates 41 and 42, the two contract gates. So this cost was never measured. The PR body and `CI_WORKFLOWS.md` give no docs-worker projection that includes it.
- **Lower-confidence second case.** Yosys shard 0 now has a 29-min limit (`scripts/ci_suite_workflows.py:67`), giving a 60% bound of 1,044 s. Its cache-hit baseline was 494 s. With a cache miss, which any workflow-changing head forces because the recipe digest hashes every workflow file, it adds a roughly 10-minute Yosys build and is projected near 1,100 s. That is above the own-limit rule, though well under the timeout.

**Impact:**
- The docs workflow, one of the four that issue #737 must bring to 30 minutes or less, is projected to miss the target.
- Its leg 0 is projected above the per-worker headroom rule the owner ruled on. The cause is this PR's own test cost, not the product suites.
- A protected `docs-check` aggregate depends on that worker. Hosted variance then has less margin before the 45-minute limit than the rule intends.

**Required outcome:**
- Every generated gate worker, and every Yosys worker, is projected or measured at or below 60% of its own limit, with the contract gates included.
- Possible routes: give the contract and runner self-tests their own source-derived gate worker; or make each generated-gate arm cheaper (for example, regenerate the four workflows once per arm only for the mutated file); or add workers.
- `CI_WORKFLOWS.md` records each gate worker's projection and margin, and the PR body's docs projection is corrected.
- No arm is removed and no timeout is raised.

**Verification:**
- Time `ci_events.py --selftest` at the corrected head.
- Recompute `docs-gates-0` from the hosted baseline plus the measured gate times, and require 1,620 s or less.
- The manager's hosted readback of `docs-gates-0` and the docs span confirms it.

### R636-2-F2 - MINOR - Robustness, RTL (architecture: resource effects), Docs

**Where:**
- `scripts/act_ci.py:109` (`CONTAINER_MEMORY = "8g"`) and `:162` (`SLOT_MEMORY_MAX = "36G"`).
- `docs/testing/CI_WORKFLOWS.md:2346-2353`: "The largest measured class is capture at 6047100928 bytes … a margin of 42.05% … No cap increase or further compiler-budget reduction follows from these samples."
- Recipes: `.github/ci-templates/rtl.yml:253,519` and `rtl-fast.yml:169,285` run `make -C /tmp/yosys-src -j"$(nproc)"`.

**Authority:**
- 6170460727: "size CONTAINER_MEMORY and the job parallelism together, so that a 16-CPU job of every heavy class completes."
- 6169768594 item 4: "your own measurement of the heaviest job classes at 16 and 12 CPUs."
- This is R636-1-F4 narrowed: the job classes measured so far are now covered, but this one is not.

**Evidence:**
- **Rebuilt every replay.** The local workflow cache is per head (`act_ci.py:1577`, `state/<head>/workflow-cache`). So every local replay rebuilds Yosys in each Yosys-using job: four Yosys shards, `yosys-elaboration`, and Verilator shard 3. Up to four of them run at once, each at the full job width.
- **Measured peak.** I ran the workflow's exact Yosys v0.66 recipe (`86f2ddeb`, ABC `5d51a5e4`) at `-j16` in a bounded user cgroup (`receipts/yosys-build-j16/`).
  - It peaked at 7,687,254,016 bytes (7.16 GiB): 89.5% of the 8-GiB cap, a 10.5% margin.
  - It returned 0 after 329 s, with every memory event counter at zero.
  - The metric is cgroup `memory.peak`, the same one the author's receipts use.
- **Not in the author's evidence.** None of the seven measured classes includes a toolchain source build. The synthesis measurement used an already-installed Yosys.

**Impact:**
- The heaviest known in-job class runs much closer to the cap than the documented 42% margin.
- A different compiler or allocator, or page-cache pressure, could OOM-kill a toolchain build. The replay then refuses or fails rather than reporting a test verdict.
- No OOM was observed, so this is a sizing-evidence gap, not a demonstrated failure.

**Required outcome:**
- Measure the Yosys and Verilator source builds at 16 and 12 CPUs in the shipping job image.
- Record them in the resource-bounds list, and re-derive the largest class and its margin.
- If the margin is inadequate, bound that build's `-j` by memory or raise the cap within the slot arithmetic.

**Verification:** `memory.peak` and `memory.events` receipts for both builds at both widths, and the corrected resource paragraph.

### Suggestions (non-blocking)

- **S1** `scripts/ci_case_receipts_selftest.py:167`: the planted bad outcome is `"failure"`, but drivers write `"failed"` (`ci_make_cases.py:68`, the maap and capture receipts).
  - Adding `"failed"` to the accepted outcomes in `ci_case_receipts.py:197` survives the self-test (`receipts/mutation-probes.json`).
  - The leg job's non-zero exit still blocks such a union, so this is defence in depth.
- **S2** (R636-1-S2, retained): allowing skipped steps in `completion_errors` (`ci_manifest.py:129`) survives `ci_manifest_selftest.py`. Add a control with two identical manifests that each contain a skipped step.
- **S3** (R636-1-S3, retained): each workflow's watcher holds a hosted runner for the whole run. One head now defines 62 jobs across the four workflows after matrix expansion, four of them watchers. Check the account's concurrent-job limit before relying on the wall clock.
- **S4** (R636-1-S1, retained): removing the single-scope consistency check (`ci_gate_receipts.py:98`, `len(scopes) != 1`) survives `ci_gate_workflows_selftest.py` (`receipts/prior-findings/s1-mixed-scope-mutant.txt`).
- **S5** Two design notes for round 2:
  - Cache-conditional build steps are `success` on a miss and `skipped` on a hit. A hosted manifest and a local one, whose cache is always cold, will differ in `execution` even though the signature design excludes cache state.
  - On observer exhaustion the watcher job itself ends red (`ci_fail_fast.py:144`, exit 2). No cancel is issued, which is correct, but the workflow run shows a failure on a healthy head. Consider reporting that state without a failed job.

## Prior public findings at this head

| Finding | Status at `2658a64c` | Evidence |
|---|---|---|
| R637-1-F1 (MAJOR): nested budget, media-NCO `-j 0` | **Resolved.** `media_nco/Makefile:17` now uses `-j $(VERILATOR_JOBS)`. The capture worker exports `cpus // 4` (`ci_suite_pieces.py:69-73`). | Restoring `-j 0` makes `ci_gate_workflows_selftest.py` fail on the real media-NCO child recipe (`prior-findings/r637f1-nco-j0-mutant.*`). |
| R637-1-F2 (MAJOR): collector and watcher-tail failures | **Resolved.** The collector is in `EXPECTED_JOBS` and no longer needs the watcher. `ci-cancel-tail` needs both and cancels on confirmed failures. Fork exclusion is kept. | `fail_fast_self.log`. My mutant that ignores collector failures in `tail_failed` is caught (`mutation-probes.json`). |
| R637-1-F3 (MINOR): stale cache paragraph | **Resolved.** `CI_WORKFLOWS.md:1582-1589` says no prefix fallback. No `restore-keys` remain on tool or installation caches. The `yosys-results` result cache keeps its documented prefix (`:594`). | grep of the workflows and templates |
| R636-1-B1 (BLOCKER): union inventories without submodules | **Resolved.** Every union job and `verilator-suites` has "Fetch inventory dependencies". | In a copy with submodules removed, the three Makefile inventories are refused. With exactly those four submodules, all six derive: 19/3/4/31/31/66 (`prior-findings/b1-*`). |
| R636-1-B2 (BLOCKER): Git identity in a self-test | **Resolved.** | All seven new self-tests return 0 with an empty HOME and no global or system Git configuration (`prior-findings/b2-no-identity.txt`). |
| R636-1-F1 (MAJOR): skipped matrices | **Resolved.** `SKIPPED_MATRICES` maps raw names to their expansions; a raw name counts only if completed and skipped. | Self-test fixtures use the raw names from run 38273578232. My status-check mutant is equivalent, because a failed raw-name job is caught first. |
| R636-1-F2 (MAJOR): observer errors | **Resolved.** GETs get 4 attempts within a 600-s budget, honouring `Retry-After` and `X-RateLimit-*`. A 120-s poll gives 120 requests per hour per head; the arithmetic is in `CI_WORKFLOWS.md:2672-2684`. | Mutants where 5xx is not transient, or an observer error counts as a failure, are both caught. |
| R636-1-F3 (MAJOR): headroom rule | **Partially resolved; the gate-worker part is retained as R636-2-F1.** Verilator workers are projected at 1,491-1,605 s against their own 1,620-s bound, and leg A at 2,032 s against 2,160 s. | Planted 1,620-s and own-limit controls pass (`suite_shards_self.log`). My mutant moving 1,620 to 1,700 is caught. |
| R636-1-F4 (MINOR): memory sized from peaks | **Partially resolved; retained, narrowed, as R636-2-F2.** Seven classes are measured at 16 and 12 CPUs; the source-build class is missing. | `author-r2/round2-*-memory-*.json`, `receipts/yosys-build-j16/` |
| R636-1-F5 (MINOR): one control per conclusion | **Resolved.** | Dropping `action_required` is caught. |
| R636-1-F6 (MINOR): public-head comparisons | **Resolved.** The comparisons are at public `cf9c9366`, the PR head when ruled, and I extended them to the exact head (below). | `published-case-verification.json`, `exact-head-legs-comparison.json` |
| R636-1-S1 to S5 | S1 retained (S4 above); S2 retained (S2); S3 retained (S3). S4 (piece inherits the parent timeout) is documented at `run_all_suites.sh:398`. S5 (`MAKEFLAGS`): still no hosted observation. | |

## Round-2 items judged at their cause

1. **Nested compiler budget.** Closed, as R637-1-F1 above. Capture runs four workers, each with `VERILATOR_JOBS = cpus // 4` and `MAKEFLAGS=-j1`. The census and firmware campaigns use `CI_CAMPAIGN_JOBS = min(cpus, 4)`.
2. **Fail-fast.** Closed. Each of the four conclusions has a control. Fork events never enter the write-token jobs.
   - That separation is checked in the workflow `if:` and again before any API call (`ci_fail_fast.py:197`).
   - The fork control passes, and my mutant that permits forks is caught.
   - POST failures are reported and never retried as reads.
   - The local supervisor (`ReplayEvents`, `act_ci.py:5693-5728`) raises at the first `jobResult` that is not success or skipped. That terminates the act process group, then cleanup runs. `--failed` marks unconcluded jobs `cancelled`, so the manifest is incomplete.
3. **Headroom.** Closed for Verilator workers. Open for `docs-gates-0` (F1).
4. **Memory.** The census is bounded to four workers and measured at 5.46 GiB and 4.84 GiB, with zero events. The seven classes are recorded; the toolchain-build class is open (F2).
5. **Six comparisons.**
   - I re-verified all six published full and sharded receipt sets with the PR's own `verify()`. I re-derived all six driver inventories at the exact head; each is identical to the published inventory. A case dropped from every leg is refused in each suite (`published-case-verification.json`).
   - The published per-case logs are not in the packet, so the digest-to-log binding was not re-checked for the 154 published units.
   - **Exact-head execution.** At `2658a64c` I ran three production legs through `ci_suite_pieces.py run`: `milan_dp_render__1`, `pp_shadow__0` and `maap__0`. All 19 units match the published unsharded run in outcome, return code and checked-output SHA-256 (`exact-head-legs-comparison.json`). That includes 15 maap mutants caught in their owning leg; the legs report 71 render checks and 609 pp_shadow checks.
6. **Cache paragraph.** Closed, as R637-1-F3.
7. **Dev merge.** `abf7a923` is a true merge of `fa820988`.
   - The README count is 161 = 126 (dev) + 35.
   - The +35 is reproduced from the head's own `ctrl_pin.stack_targets`: the `milan_dp` Makefile split raises stack-reaching targets from 6 to 41 (`prior-findings/pin-target-counts.txt`).
   - I did not execute the census self-test itself.
8. **No stage barrier.** Closed. With the patched dispatcher built from the pinned act source and verified Go 1.25.0:
   - the race controls pass `-count=10`;
   - the unchanged `./pkg/common` upstream tests pass;
   - the patched `pkg/runner` passes `go vet`;
   - a planted stage barrier (each job also waits for every earlier-listed job) fails both scheduling fixtures (`go-dispatcher/`).

## Trust-boundary audit of `scripts/act_ci.py` and `scripts/build_ci_act.py`

- **Runner checksum.** The head runner's SHA-256 is `5ccbd700…74dd`, equal to the author's stated checksum. The three helper pins match the files byte for byte.
- **CPU ranges.**
  - Ranges come only from `--cpu-ranges`. The runner accepts only 16-wide ranges, or ranges of the one named `FALLBACK_CPU_LIMIT = 12`, aligned to their own width, disjoint and inside the host.
  - The dispatcher re-validates them from the command-line environment (`config.Env`). Neither workflow `env` nor a candidate `.env` can override that: `--env-file` points at an empty runner-owned file, and command-line values win.
  - The cpuset is appended at initial container creation (`JobCPUOptions`). A job whose options try to set cpuset or `--cpus` is refused.
  - No `container update` remains. The monitor is read-only and catches sharing, an unbooked or empty placement, and a move after creation; each of those has a control.
- **Bypass routes.** Containers that would bypass job options (job `container:`, `services:`, `docker://`, unaudited actions) are statically refused (`act_ci.py:2058-2081`).
- **Lease lifetime.** A range is released only after the job executor returns. That includes `--rm` container removal through act's post-executor.
- **Manifest collection.**
  - The evidence helpers run with `-I`, after digest checks, from a private copy.
  - ZIP members are read as bounded data, never extracted.
  - The evidence directory is refused inside the candidate tree.
- **Act build script.** `build_ci_act.py` pins the act tarball and Go archive by SHA-256, extracts with `filter="data"`, applies the patch with `--fuzz=0`, and rechecks its input digests after the build.
- **Result.** I found no trust-boundary defect.

## Hosted evidence at this head

| Workflow | First job start | Last job end | Span at `2658a64c` |
|---|---|---|---|
| docs | none | none | NOT AVAILABLE |
| elaborate | none | none | NOT AVAILABLE |
| rtl-fast | none | none | NOT AVAILABLE |
| rtl-full | none | none | NOT AVAILABLE |

- **Query.** At 2026-10-14T19:08:00Z, `actions/runs?head_sha=2658a64c…` returned `total_count 0`, and the PR status rollup is empty (`hosted-runs-at-head.json`, `pr-state.json`).
- **Why no runs.** The PR is `CONFLICTING` with live dev `f6260253`, in `.github/workflows/rtl.yml`, `docs/testing/CI_WORKFLOWS.md` and `scripts/suite_shards.py`. Dev has since registered a gPTP table suite and a six-worker balance (`live-dev-conflicts.txt`). No job, executed or skipped, can be read.
- **Baseline for reference** (7032bca5): rtl-full 77m29s, elaborate 35m44s, docs 34m00s, rtl-fast 19m03s.
- **Acceptance.** The 30-minute acceptance is the manager's call. The accepted media-clock leg-A exception (about 33.9 min projected) stands.

## Reviewer-owned ledger

| Lens | CLEAN/UNCLEAN | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | UNCLEAN (F1) | Issue body and every [A10] ruling listed above; templates vs `fa820988` workflows (no test step removed, conditions kept, timeouts only lowered, `ubuntu-latest` only); cache keys; CPU rules; fail-fast; manifest base; `CI_SIGNATURE.md` | R636-2 | `2658a64c408bf87ae36574f36a6deeb34b2f297f` |
| RTL (architecture and resources; no product HDL changed in `fa820988..HEAD`) | UNCLEAN (F1, F2) | `ci/act/*.go` and `fail-fast.patch` (built and tested); `act_ci.py` diff; dependency graph and admission; per-job budgets; `tb/verilator/*/Makefile` splits; `sim_mclk.cpp:1177` (echo only); Yosys `-j16` peak | R636-2 | `2658a64c408bf87ae36574f36a6deeb34b2f297f` |
| Robustness | UNCLEAN (F1 timeout margin, F2 memory margin) | `ci_fail_fast.py` retry, rate-limit, 409 and fork paths; cancel and terminate paths; malformed, duplicate and missing receipts; incomplete manifests; CPU-range refusals; OOM-bounded census | R636-2 | `2658a64c408bf87ae36574f36a6deeb34b2f297f` |
| Tests | UNCLEAN (F1) | 24 offline gates rc 0 (`offline-gates/`); `ci_events --selftest`, all 5,093 arms in four parts; 10 planted mutants (6 caught, 2 equivalent, 2 reported as S1/S2); media-NCO, mixed-scope and stage-barrier mutants; exact-head legs; Go race and upstream tests | R636-2 | `2658a64c408bf87ae36574f36a6deeb34b2f297f` |
| Docs | UNCLEAN (F1, F2) | `CI_WORKFLOWS.md` sections on sharding (`:348-395`), CPU and concurrency (`:1925-1994`), resources (`:2300-2360`), gates and fail-fast (`:2621-2729`), cache (`:1582`, `:2856-2872`); `CI_SIGNATURE.md`; AGENTS/CONTRIBUTING `--cpu-ranges` lines; PR body | R636-2 | `2658a64c408bf87ae36574f36a6deeb34b2f297f` |

## Real limits

- **No Docker, act or host runner.** I did not run Docker, act, `act_ci.py`, its self-test or `act_slot_proof.sh`. The dispatcher was exercised only through its Go unit and race tests and `go vet`.
- **Contract self-test was split.** It was executed split into four in-process parts, each arm once, because one run exceeds the 10-minute command bound. The full-run duration is extrapolated from measured per-check cost and agrees with a 585-s partial direct run.
- **Exact-head simulation covered 19 units only** (three legs). The other 135 units rest on the author's `cf9c9366` receipts, re-verified for union and equality, plus inventory identity at the head. The dev merge changed no file in those six suites, but no full exact-head bank was run.
- **Yosys measurement conditions.** The build used host GCC 16.2.1 in a user cgroup, not the CI image's compiler. The docs leg-0 figure is a projection from the hosted baseline and local timings, not a hosted measurement.
- **Pin-control census not executed.** The count is checked by target arithmetic only.
- **No hardware.** Physical calibration NOT RUN; field skips are not hardware proof.
- **Not claimed.** No manager source bank at this head exists or is claimed. Author gate receipts are author source-validation evidence.

## Pending manager duties

- Rebase the merge candidate onto live dev `f6260253`: regenerate `rtl.yml` from its template and register dev's new gPTP table suite in the CI piece and duration tables. Under AGENTS.md section 7, a commit that changes these artifacts un-covers the lenses at that head.
- Then complete:
  - hosted readback per workflow and job at a pushed head, including `docs-gates-0` (F1) and Yosys shard 0 on a cache miss;
  - a full trusted replay with per-job peaks, start times and placements;
  - live cancellation evidence;
  - candidate builder and native banks;
  - re-pinning the reviewed runner checksum;
  - merge authorization;
  - post-merge containment.

## Reviewer conduct

No source fixes, commits, pushes, GitHub writes, merges, author contact, Docker or act runs, privilege use or hardware operations. Probes ran only in disposable copies under `scratch/` and each restored its exact bytes. My clone is verified at the exact head and tree:
- all 1,357 tracked blobs have the right bytes, kind and mode;
- the index tree equals the head tree;
- the five populated gitlinks match, and `external` is uninitialised as recorded;
- status is clean including ignored files, after removing my bytecode caches (`receipts/checkout-integrity.json`).

R636-2 FINISHED
