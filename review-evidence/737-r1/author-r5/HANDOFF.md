[A614]

# Lane 737 handoff

Status: Round 5 (merge current dev) at `e3d25d964b5bbf0187290d0a357c6a6e4c5afd17`, from `08adb21af0a72d839ce30b6c461503dad269d4d6` (assignment 6184143571). The merge of dev `f62602531d415d6c1cae1374a3cc2938faf54049` is `8db583050`; the re-projection is `e3d25d964`. See the **Round 5** section at the end; it supersedes the head and readiness statements above it.

Round 4 status (historical): both round-4 reviews are POSITIVE at `08adb21af0a72d839ce30b6c461503dad269d4d6`. The round-4 STOP at `6ab22bca` was answered, and the builder gate was divided into measured legs.

Round 3 status (historical): Round 3 is review ready at `84ee9ea119b548b4982d2c0988d8753a2ce4d0cf`. Items 1–6 have committed fixes and item 7 is recorded residue. The continued session found and fixed a failing bare-metal scope gate and two stale documentation figures. The full docs-check and rtl-fast step sets pass on the committed head. Both round-two reviews are NEGATIVE; fresh independent review and coordinating replay are required.
Branch: `737-ci-30min`; round-five head: `e3d25d964b5bbf0187290d0a357c6a6e4c5afd17`; round-four final head: `08adb21af0a72d839ce30b6c461503dad269d4d6`; round-four STOP head: `6ab22bca61a76c989ad9fbb94b9cde2639d38ca9`; round-three final head: `84ee9ea119b548b4982d2c0988d8753a2ce4d0cf` (round-two head `2658a64c408bf87ae36574f36a6deeb34b2f297f`); resumed measurement source: `21bd10cec1a999791c9cd2c6d37c52372fb1504e`.
The required merge of dev `fa8209889411e8ca95757174c981f720dbcd95a2` is commit `abf7a923a`. The round-five merge of dev `f62602531d415d6c1cae1374a3cc2938faf54049` is commit `8db583050`.
Origin is `https://github.com/kebag-logic/milan-fpga.git`.
Executor: [A614]. Independent reviewers: [R636] and [R637].
No push, PR write, rebase or hardware access occurred. No TAKEN comment was repeated.

The sections before **Round 2** retain the round-one implementation and validation record at `cf9c936697a06e44c41681bcc12dc612a3242eb2`. Their successful source gates are historical evidence, not a round-two review verdict or new hosted measurement. The round-two section supersedes their head, readiness, memory qualification and follow-up scope statements.

## Authority and completion boundary

The exact assignment is [round one](https://github.com/kebag-logic/milan-fpga/issues/737#issuecomment-6160775078).
The [driver ruling](https://github.com/kebag-logic/milan-fpga/issues/737#issuecomment-6160937413),
[finer-split guidance](https://github.com/kebag-logic/milan-fpga/issues/737#issuecomment-6160973660),
[contract ruling](https://github.com/kebag-logic/milan-fpga/issues/737#issuecomment-6161122704),
[fail-fast directive](https://github.com/kebag-logic/milan-fpga/issues/737#issuecomment-6161180121),
[media-clock ruling](https://github.com/kebag-logic/milan-fpga/issues/737#issuecomment-6161771913),
[fourth ruling](https://github.com/kebag-logic/milan-fpga/issues/737#issuecomment-6162403147),
and [manifest design](https://github.com/kebag-logic/milan-fpga/issues/737#issuecomment-6160962404)
were read exactly, together with the earlier registry, parallel-image and datapath guidance.

Round one keeps standard runners and caches. The separate image work and digest adoption,
authenticated signature, immutable action references and conditional-skip proof are round two.
The coordinating role owns pushing, hosted wall-clock measurement and one full trusted replay
of the final author head. This handoff does not claim those executions or a valid signed build.
The authorized media-clock exception still projects above 30 minutes; no test history was
reset, shortened, seeded or accelerated by changing its time scale.

## Implementation index

| File:line | Change |
|---|---|
| `.github/ci-templates/docs.yml:8` | Ordered source workflow contract; original test bodies and conditions remain checked. |
| `.github/ci-templates/elaborate.yml:69` | Ordered source workflow contract; original test bodies and conditions remain checked. |
| `.github/ci-templates/rtl-fast.yml:24` | Ordered source contract retains test predicates and conditions; campaign width derives from the job CPU budget. |
| `.github/ci-templates/rtl.yml:35` | Ordered source contract retains test predicates and conditions; physical-suite compilation uses the job budget. |
| `.github/workflows/docs.yml:4` | Generator-owned workflow with exact cache, scheduling, actual-evidence and same-repository cancellation steps. |
| `.github/workflows/elaborate.yml:9` | Generator-owned workflow with exact cache, scheduling, actual-evidence and same-repository cancellation steps. |
| `.github/workflows/rtl-fast.yml:10` | Generator-owned workflow with exact cache, scheduling, actual-evidence and same-repository cancellation steps. |
| `.github/workflows/rtl.yml:12` | Generator-owned workflow with exact cache, scheduling, actual-evidence and same-repository cancellation steps. |
| `ci/act/fail-fast.patch:1` | Select bounded nested admission and propagate recorded job errors before releasing admission. |
| `AGENTS.md:176` | Require explicit externally booked CPU ranges in the trusted-runner invocation. |
| `CONTRIBUTING.md:103` | Update the trusted replay invocation for the external CPU option. |
| `ci/act/cpu_ranges.go:14` | Parse aligned external leases, reserve before execution and bind initial container creation. |
| `ci/act/cpu_ranges_test.go:1` | Prove nonoverlap, stable creation options, malformed bookings and cleanup failure. |
| `scripts/act_slot_proof.sh:67` | Forward separate manager bookings through serial, concurrent and interruption proofs. |
| `ci/act/job_admission.go:1` | Global context-owned admission tokens shared by nested workflow and matrix executors. |
| `ci/act/parallel_executor_test.go:1` | Repeated race-enabled success, failure, cancellation and recorded-error controls. |
| `ci/constraints-ci.txt:1` | Twenty-eight exact Python distribution URLs with SHA-256 constraints. |
| `ci/requirements-evidence.txt:1` | Hash-pinned YAML reader dependency. |
| `docs/testing/CI_SIGNATURE.md:1` | Seven canonical sections, independent collectors, strict comparison and explicit round-two proof boundary. |
| `docs/testing/CI_WORKFLOWS.md:1` | Public scheduling, union, cache, resource, fail-fast and evidence contracts. |
| `scripts/act_ci.py:102` | One global four-job scheduler, separate sixteen-CPU ranges, measured memory caps, failure cleanup and isolated pinned evidence reader. |
| `scripts/build_ci_act.py:30` | Build the pinned local dispatcher with atomic fail-fast job admission. |
| `scripts/ci_capture_cases_selftest.py:17` | Prove capture campaign scheduling and thread-local checked-output observations. |
| `scripts/ci_case_receipts.py:32` | Prove executed case coverage against a driver's freshly derived inventory. |
| `scripts/ci_case_receipts_selftest.py:22` | Planted omissions and changed observations must fail executed-union proofs. |
| `scripts/ci_events.py:4386` | Original semantic assertions plus exact generated graphs; source/cache provenance and planted topology controls. |
| `scripts/ci_fail_fast.py:24` | Cancel same-repository runs at the first observed failed job. |
| `scripts/ci_fail_fast_selftest.py:12` | Prove first-failure selection, successful completion and fork write refusal. |
| `scripts/ci_gate_receipts.py:26` | Record actual step outcomes and refuse an incomplete parallel gate union. |
| `scripts/ci_gate_workflows.py:29` | Generate parallel gate jobs from the original, contract-checked step inventory. |
| `scripts/ci_gate_workflows_selftest.py:20` | Execute CPU budget shell at four widths, bound nested capture compilation, and retain scheduling/union controls. |
| `scripts/ci_install_cache.py:22` | Bind a package-download cache to the exact solver result and install recipe. |
| `scripts/ci_install_cache_selftest.py:15` | Prove installation caches bind sources and recipes without changing gates. |
| `scripts/ci_install_workflows.py:15` | Add exact download caches around existing installation commands only. |
| `scripts/ci_local_manifest.py:24` | Read source objects and scheduler telemetry using independently pinned code. |
| `scripts/ci_maap_cases_selftest.py:18` | Check MAAP receipt observations and inventory selection without changing predicates. |
| `scripts/ci_make_cases.py:30` | Run the case inventory owned by a suite Makefile, retaining executed receipts. |
| `scripts/ci_make_cases_selftest.py:12` | The Makefile case runner refuses failed builds and absent or masked verdicts. |
| `scripts/ci_manifest.py:28` | Canonical CI evidence and strict comparison, independent of transport. |
| `scripts/ci_manifest_selftest.py:14` | Planted manifest differences and incomplete evidence must never compare equal. |
| `scripts/ci_runtime_evidence.py:30` | Collect actual step contexts and API outcomes without filling gaps with success. |
| `scripts/ci_runtime_evidence_selftest.py:27` | Compare independent API and scheduler observations and plant runtime gaps. |
| `scripts/ci_runtime_workflows.py:28` | Derive job-local build and campaign budgets, retain actual evidence and add same-repository cancellation. |
| `scripts/ci_scope_history.py:142` | Each generated elaboration worker executes the unchanged historical scope predicates. |
| `scripts/ci_suite_collect.py:15` | Collect physical suite logs only after every executed case union succeeds. |
| `scripts/ci_suite_collect_selftest.py:16` | Exercise physical log collection, exact worker ownership and union byte binding. |
| `scripts/ci_suite_pieces.py:23` | Schedule driver-owned case partitions and prove their executed union. |
| `scripts/ci_suite_pieces_selftest.py:17` | Plant omissions against fresh driver inventories and actual union code. |
| `scripts/ci_suite_workflows.py:14` | Materialize exhaustive case workers and one executed union job per parent. |
| `scripts/ci_workflow_plan.py:28` | Recompute a CI job and step inventory from committed workflow bytes. |
| `scripts/ci_workflow_plan_selftest.py:47` | Prove exact matrix, dependency and step planning from immutable Git inputs. |
| `scripts/generate_ci_evidence_pins.py:15` | Bind the isolated runtime reader and its helpers to the audited runner bytes. |
| `scripts/run_all_suites.sh:150` | Optional CI pieces retain original suite timeouts, preflights, process ownership and tally. |
| `scripts/suite_shards.py:149` | Derived CI units, sixteen-worker capacity model and the explicitly authorized continuous-history exception. |
| `sw/firmware/ctrl/README.md:240` | Report the derived pin-control census of 155 after the scheduling targets add 35 existing prerequisite checks. |
| `tb/verilator/capture_coherence/Makefile:1` | Expose suite-owned case inventory and separate selected build/run targets without changing test assertions. |
| `tb/verilator/capture_coherence/mutants.py:140` | Derive campaign membership, select four disjoint legs, and retain thread-local checked output for executed-case receipts. |
| `tb/verilator/maap/Makefile:1` | Expose suite-owned case inventory and separate selected build/run targets without changing test assertions. |
| `tb/verilator/maap/mutants.py:213` | Register three positive variants and 63 original mutation arms, select four legs and retain each actual verdict and checked output. |
| `tb/verilator/milan_dp/Makefile:563` | Expose suite-owned case inventory and separate selected build/run targets without changing test assertions. |
| `tb/verilator/milan_dp_mclk/Makefile:29` | Expose suite-owned case inventory and separate selected build/run targets without changing test assertions. |
| `tb/verilator/milan_dp_mclk/mclk_mutants.py:78` | Expose the driver-owned 31-case inventory, keep continuous histories intact and record selected legs with original mutation outcomes. |
| `tb/verilator/milan_dp_mclk/sim_mclk.cpp:1177` | Emit the existing checked values for per-case equality; test predicates and carried history remain unchanged. |
| `tb/verilator/milan_dp_render/Makefile:204` | Expose suite-owned case inventory and separate selected build/run targets without changing test assertions. |
| `tb/verilator/pp_shadow/Makefile:147` | Expose suite-owned case inventory and separate selected build/run targets without changing test assertions. |

## Split inventories and executed equivalence

| Parent | Inventory authority | Cases / legs | Same-head full/sharded evidence and planted control |
|---|---|---:|---|
| media clock | `tb/verilator/milan_dp_mclk/mclk_mutants.py`, driver campaign inventory | 31 / 4 | Full and all four legs equal at `9dd0817da6d3f771a3bd1db5eca0f2ba63d0695d`; 16 real mutants remain caught; changed values and dropped/duplicated cases refused. |
| datapath | `tb/verilator/milan_dp/Makefile`, `CI_CASES`, `ci-list`, receipt-form registration | 19 / 4 | Full and legs equal at `e06f342f5c35ccd71c1902e32747422245407afa`; dropping counters or the real render-mutant group from every leg is refused. |
| MAAP | `tb/verilator/maap/mutants.py`, registered positive variants and mutation table | 66 / 4 | Three passing variants and 63 caught defects equal at `068802530c138eb1fdfaada374de4ecf9cf860a7`; actual-case omission from every claim is refused. |
| capture coherence | `tb/verilator/capture_coherence/mutants.py`, registered mutations and grouped datapath control | 31 units / 4 | Full and all legs equal at `068802530c138eb1fdfaada374de4ecf9cf860a7`; original 32 campaign checks preserved; removing the last actual mutant everywhere is refused. |
| datapath render | `tb/verilator/milan_dp_render/Makefile`, `RUN_CASES` and `ci-list` | 3 / 3 | Full and legs equal at `068802530c138eb1fdfaada374de4ecf9cf860a7`; five real planted defects remain caught; omission refused. |
| protocol shadow | `tb/verilator/pp_shadow/Makefile`, `RUN_CASES` and `ci-list` | 4 / 4 | Full and legs equal at `e06f342f5c35ccd71c1902e32747422245407afa`; 2,184 checks and real K10/K12 defect refusals preserved; omission refused. |
| docs | `.github/ci-templates/docs.yml`, every non-setup step in original order | 42 / 2 | Builder gate owns leg 1; all other gates own leg 0. Source-bound receipts require every gate once; dropping one gate from every claim is refused. All original local gate commands passed; artifact service actions remain for the complete hosted/trusted replay. |
| elaboration | `.github/ci-templates/elaborate.yml`, every non-setup step in original order | 2 / 2 | Builder owns leg 0; standalone simulation aggregate owns leg 1. Missing, duplicate, failed, cancelled, skipped and contradictory-scope controls are refused. The builder gate and all seven standalone simulations passed. |

The six case unions independently reread their parent inventories. Each verifies exact head,
tree, declared ownership, completed successful outcomes and checked-output hashes. The final
physical-suite collector rechecks those raw receipts, union metadata and actual log bytes,
then invokes the original tally over all 62 physical suites. Removing a case everywhere,
including all claimed inventories, cannot reduce the independently derived inventory.
Counter-only registrations use exactly exit status, RESULT line and full stdout SHA-256;
no check count is invented. The unchanged tally agrees between full and combined logs:
datapath 11,956; capture 21,196; MAAP 252; render 342; protocol shadow 2,184.

| Parent | Full local seconds | Leg seconds |
|---|---:|---|
| media clock | 462.87 | 434.51, 329.73, 318.23, 190.13 |
| datapath | 1020.88 | 176.12, 690.70, 538.29, 107.32 |
| MAAP | 716.40 | 169.26, 185.91, 155.49, 160.22 |
| capture coherence | 1667.92 | 621.90, 498.82, 325.82, 242.11 |
| render | 546.46 | 257.13, 21.18, 473.84 |
| protocol shadow | 373.88 | 145.20, 155.12, 156.71, 231.89 |

These comparisons used identical source heads on both sides. They are not final workflow
wall-clock measurements. Comparison receipts and actual omission controls are in the small
`resume4-*-equivalence.json` records; large logs and model artifacts stay in scratch with
size/SHA-256 entries. Final source-blob equivalence is recorded in `source-correspondence.json`. The three comparison snapshots are retained by `refs/validation/737-mclk`, `refs/validation/737-datapath` and `refs/validation/737-campaigns`; they are local validation snapshots, not claimed published commits.

The clean media-clock build was 30.18 seconds, against 428.72 seconds for the continuous A
history. Simulation dominates it, so a separate model artifact would not remove the critical
path. Distinct datapath configurations and mutation variants require their own model bytes;
selected Make targets retain shared prerequisites within each job. Compiler trials gave
441.52 and 414.49 seconds with identical checked output, but no compiler change was retained.
The two-thread trial remained incomplete after 1,650.76 seconds and was rejected. Its earlier
590-second incomplete trial is also retained, never counted as a pass.

## Hosted before and predicted after

Baseline jobs are measured at `7032bca5a51d8d97fcb73d7fc106ca4af21de38e` from the jobs API. After values are predictions for warm caches on standard runners, not a hosted rerun. Queue time, cold builds, network installs and new artifact overhead remain to be measured.

### rtl-full

```sh
gh api repos/kebag-logic/milan-fpga/actions/runs/38495894214/jobs
```

| Original job | API job ID | Measured before | Predicted after |
|---|---:|---:|---|
| full-ci-gate | 115631441324 | 0m50s | 0m50s plus execution-evidence overhead |
| Yosys shard 0/4 | 115631699014 | 8m14s | 8m14s plus execution-evidence overhead |
| Yosys shard 3/4 | 115631699114 | 0m31s | 0m31s plus execution-evidence overhead |
| Yosys shard 2/4 | 115631699117 | 0m32s | 0m32s plus execution-evidence overhead |
| Verilator shard 0/5 | 115631699137 | 69m48s | Replaced by the sixteen derived workers below |
| Verilator shard 3/5 | 115631699169 | 60m09s | Replaced by the sixteen derived workers below |
| Verilator shard 2/5 | 115631699198 | 70m10s | Replaced by the sixteen derived workers below |
| Verilator shard 1/5 | 115631699214 | 68m38s | Replaced by the sixteen derived workers below |
| Verilator shard 4/5 | 115631699226 | 55m32s | Replaced by the sixteen derived workers below |
| Yosys shard 1/4 | 115631699385 | 0m25s | 0m25s plus execution-evidence overhead |
| Physical gPTP (nightly and manual) | 115631700715 | 0m00s | Still skipped for push/PR; separate nightly/manual campaign |
| verilator-suites | 115653077431 | 0m07s | Under 1 minute after all workers and six case unions |
| yosys-portability | 115653119397 | 0m08s | Under 1 minute |

### elaborate

```sh
gh api repos/kebag-logic/milan-fpga/actions/runs/38495894212/jobs
```

| Original job | API job ID | Measured before | Predicted after |
|---|---:|---:|---|
| elaborate | 115631440899 | 35m44s | Protected union: under 1 minute; workers projected at 1313 s (21m53s, builder leg 0) and 1172 s (19m32s, builder leg 1 plus the LiteX aggregate); workflow about 26.4 minutes (Round 4 S3) |

### docs

```sh
gh api repos/kebag-logic/milan-fpga/actions/runs/38495894291/jobs
```

| Original job | API job ID | Measured before | Predicted after |
|---|---:|---:|---|
| wire-accountability | 115631441194 | 0m09s | 0m09s plus execution-evidence overhead |
| docs-check-no-git | 115631441331 | 0m12s | 0m12s plus execution-evidence overhead |
| docs-check | 115631441482 | 33m59s | Protected union: under 1 minute; workers approximately 22 and 19 minutes |

### rtl-fast

```sh
gh api repos/kebag-logic/milan-fpga/actions/runs/38495894211/jobs
```

| Original job | API job ID | Measured before | Predicted after |
|---|---:|---:|---|
| bdd-conformance | 115631440905 | 0m14s | 0m14s plus execution-evidence overhead |
| changes | 115631441106 | 0m29s | 0m29s plus execution-evidence overhead |
| yosys-elaboration | 115631592055 | 11m00s | 11m00s plus execution-evidence overhead |
| verilator-lint | 115631592063 | 0m40s | 0m40s plus execution-evidence overhead |
| publication-census | 115631592079 | 18m25s | 18m25s plus execution-evidence overhead |
| firmware-control-mutants | 115631592083 | 16m21s | 16m21s plus execution-evidence overhead |
| firmware-verilator | 115631592089 | 11m10s | 11m10s plus execution-evidence overhead |
| firmware-unit | 115631592104 | 10m45s | 10m45s plus execution-evidence overhead |
| firmware-srp-mutants | 115631592115 | 12m32s | 12m32s plus execution-evidence overhead |
| firmware-boundary | 115631592117 | 15m19s | 15m19s plus execution-evidence overhead |
| firmware-aecp-mutants | 115631592128 | 3m48s | 3m48s plus execution-evidence overhead |
| rtl-fast | 115636758266 | 0m04s | Under 1 minute |

### New Verilator workers

The weighted suite model includes 122 seconds of worker setup. It is a capacity estimate; it is not a measured new GitHub job duration. The media-clock history exception is authorized by the third and fourth rulings. The five ordinary split parents apportion their historical hosted window by the relative local leg wall times; the media-clock legs instead use the full-run speed ratio. This assumes the relative work distribution transfers between environments. Repeated setup, compiler contention, cache misses and new artifact overhead can change the result. The final local queue also enforces a global two-build limit, so its worker wall clocks are not direct hosted predictions.

| Worker | Predicted including setup |
|---:|---:|
| 0/16 | 26m45s |
| 1/16 | 24m55s |
| 2/16 | 26m12s |
| 3/16 | 24m54s |
| 4/16 | 25m21s |
| 5/16 | 24m52s |
| 6/16 | 24m55s |
| 7/16 | 24m58s |
| 8/16 | 24m53s |
| 9/16 | 24m53s |
| 10/16 | 24m57s |
| 11/16 | 24m57s |
| 12/16 | 24m53s |
| 13/16 | 24m51s |
| 14/16 | 24m54s |
| 15/16 | 33m52s |

Six new per-suite union jobs should each take under one minute after worker artifacts arrive; each has a two-minute limit. The manifest collector is budgeted at three minutes, and the watcher follows the worker critical path. These new jobs require hosted measurement.

The regular Verilator worker maximum is 26m45s. Media-clock worker 15 is projected at 33m52s including setup (31m49s for its carried history alone), before downstream collection. The exhaustive workflow therefore still projects above 30 minutes. The coordinating role measures the exact pushed head and takes that remaining choice to the owner.

Warm-cache workflow targets including final collection: docs about 26 minutes, elaborate about 30 minutes, rtl-fast about 22 minutes. These estimates leave limited elaboration margin. A cold source-tool build can exceed them; round two adopts prebuilt layers. No hosted after-time is claimed.

## CPU, concurrency, memory and fail-fast

The final policy accepts manager-supplied `--cpu-ranges`: aligned sixteen-CPU ranges,
or twelve-wide ranges aligned to twelve. `FALLBACK_CPU_LIMIT=12` is the one named
fallback setting. Correction 6167288337 supersedes the eight-CPU suggestion.
There is no host CPU allocation table, staging range or post-creation movement.
One shared admission gate reserves a free range before each job container is created.
The lease remains held through cleanup; failed cleanup stops admission before reuse.
Four jobs may run across workflows and nested matrices. Scheduler events record each
job's range. A read-only monitor rejects unbooked placement, overlap and movement;
a placement failure cleans resources and refuses before manifest emission.

Every generated job reads its own `nproc`. Tool builds and `VERILATOR_JOBS` use that
count; campaign and simulation pools retain a four-worker memory ceiling. Ordinary
case drivers retain two simulation workers. Capture divides compiler jobs among its
active workers. Outer suite make stays serial to preserve shared build ownership.
Existing `-j 0` recipes already use Verilator 5.050's process-affinity default. A
compiled probe using the installed production header reports exactly 1/4/12/16 for
those visible CPU counts. Its digests and results are in `verilator-affinity-proof.json`.
No test or Makefile change was needed for those defaults.

Each job has an 8 GiB memory cap with the same memory+swap cap. An isolated slot has a
36 GiB cap: four jobs plus 4 GiB for the daemon and services. Shared slot zero enforces
container caps without claiming an aggregate cgroup cap. The host now has 61 GB;
the manager books ranges and memory alongside other work. Four remains the maximum.

Before the placement rewrite, four real Yosys shards ran concurrently on separate ranges,
all rc 0. Their peaks were 2,635,010,048; 1,635,954,688; 889,298,944; and 646,090,752 bytes.
Times were 493, 282, 141 and 97 seconds; memory-event counters were zero. Their summed
peaks, 5,806,354,432 bytes (5.41 GiB), are an upper bound, not a simultaneous peak.
`four-job-memory.json` retains limits, a sample and hashes. The failed 2 GiB sizing trial
remains failed evidence. The publication census later measured 5,738,594,304 bytes
(5.34 GiB) under the 8 GiB cap, with no memory-limit/OOM event.

The final dispatcher is `0.2.89+milan-ci4`. `dispatcher-build-ci4.json` binds upstream
source, compiler, patch and controls. Unchanged upstream common tests and twenty
race-enabled repetitions pass. CPU controls cover disjoint reservations, stable creation
options, missing/too-small bookings and no reuse after failed cleanup. The binary is
30,184,848 bytes, SHA-256 `cc17cf09c134ef799b5f951bc6d43cf31c436d7ca3930ba8bded69c43107e48a`.
The executable and build inputs stay in scratch. Earlier ci1/ci2/ci3 receipts are historical.

The complete offline runner self-test passes inside a disposable CPython 3.12.3 job
without a Docker socket. All 44 slot-proof controls pass with explicit external bookings.
Generated-shell controls pass at 1/4/12/16 CPUs, refuse zero and bound nested compilation.
The candidate runner was never used as the host-side orchestrator. The final four-range
trusted replay remains with the coordinating role.

First failure closes admission and stops sibling work; telemetry retains failed, cancelled
and unstarted outcomes. Hosted matrices keep native fail-fast behavior. Only the guarded
same-repository watcher requests write permission and cancels sibling workflows. Forks
keep matrix cancellation and strict aggregates. API controls pass; no live cancellation
API operation was performed by this author.

The resumed author sweep shared the booked 112-127 range and a two-build semaphore,
with four compiler jobs per build. It is not a four-range replay demonstration. The
service peak was 4,343,873,536 bytes (4.05 GiB). One service-plus-four-workers sample was
8,099,319,808 bytes; its summed separate lifetime peaks were 14,066,679,808 bytes, an upper
bound across different times. The largest final worker cgroup peak was 4,437,954,560
bytes (4.13 GiB). Retained workers reported no memory-limit/OOM events. Resource records
distinguish actual samples from peak sums.

## Installation cache provenance

All installation keys bind version, source identity and recipe. There are no broad restore
fallbacks for these caches. Yosys and Verilator verify their immutable source revisions before
building and retain installed-version checks on hits. The exact generated key inventory is
`cache-key-inventory.json`; its job-temporary paths are container paths.

| Cache | Version and source binding | Recipe binding |
|---|---|---|
| Verilator | v5.050, commit `848d926ebd4addacacd294dc84e35d9d4ae8078c` | all committed workflow files |
| Yosys | v0.66, commit `86f2ddebce7e98ce7cacc27e8a5c14cb53b51b51` | all committed workflow files |
| RV32 SDK | v1, archive SHA-256 `d42680e926542595c4c87629d33f5f90aac1e9a964c8955089e0514caa01b78f` | SDK installer digest |
| Markdown | cmarkgfm 2025.10.22 / html5lib 1.1 and hash-pinned requirements | workflow digest |
| Python downloads | CPython 3.12.3; all 28 exact distribution URLs and SHA-256 values in `ci/constraints-ci.txt`; direct requirements and LiteX pins | install-generator and workflow digests |
| Evidence reader | PyYAML 6.0.2, source SHA-256 `d584d9ec91ad65861cc08d42e834324ef890a082e591037abe114850ff7bbc3e` | reader requirements, generators and workflows |
| LiteX downloads | exact Git revisions in `sw/litex/litex_pins.txt` | workflow digest; constrained transitive downloads use the Python key |
| Scala | sbt 1.10.7, SHA-256 `32c15233c636c233ee25a2c31879049db7021cfef70807c187515c39b96b0fe6`, LiteX pins and patches | workflow digest |
| sv2v | v0.0.12, SHA-256 `ff8c9eea5bc029b372fb4953427625cddb7cf7e58c1240623ac9f260818d5a00` | install-generator and workflow digests |
| Field oracle | exact content-addressed `TSN_GEN_REV` | install-generator and workflow digests |
| Distribution downloads | SHA-256 of resolved exact package/version inventory and SHA-256 of archive URLs, names, sizes and SHA-256 values | original install body plus generator/workflow digests |
| Generated CPU metadata | configurations, source builders, dependency pins and patches | workflow digest |

Distribution setup keeps its original package-resolution policy; the prepared index feeds
both the key calculation and the following install. Package hashes are still checked by APT.
The existing synthesis-result cache is separate from installation caches and keeps its own
content-validation gate. No new node-package installation exists in the four workflows.
All 28 constrained Python downloads were independently fetched and hash-checked. Fresh
Markdown, HDL, evidence, BDD, diagram and pinned LiteX installs passed. Actual package-plan
and GoogleTest/GoogleMock install checks passed. Missing source/version/recipe fields,
duplicate archive entries, weak digests and broad fallbacks are refused by controls.

## Manifest schema and controls

Canonical UTF-8 JSON uses sorted keys, integers, strict duplicate-key refusal and SHA-256.
The compared payload has exactly seven sections: `subject`, `definitions`, `environment`,
`plan`, `execution`, `inventories` and `results`. The subject binds head/tree and PR ancestry;
definitions bind every workflow digest; plan binds expanded jobs, matrix values, dependencies,
conditions, step names and command/action hashes. Execution and results come from actual
API or scheduler observations. Inventories bind driver-derived membership, executed unions
and per-case verdict-list hashes. Timing, runner identity, CPU count, logs and cache-hit
observations stay outside the signature.

The hosted final jobs read actual current-attempt job/step API data and uploaded receipts.
A completed readback can combine all four run IDs. The local runner records actual starts,
step outcomes, job outcomes and first failure, then invokes isolated digest-pinned readers.
Candidate paths and workflow blobs are data; candidate imports cannot supply reader code.
Fresh durable evidence is outside the candidate. Changed helpers, symlinks, injected import
paths, reused output directories, extra/missing/reordered steps, extra legs, wrong source
identity, changed tool/image provenance, omitted/duplicated cases and changed verdict hashes
are refused. Identical incomplete or cancelled documents never compare equal. The comparator
recomputes both plans from their source commits independently.

Round one deliberately reports unknown proofs as incomplete: no immutable image/layer lock,
action-SHA set, signing key or evaluated conditional-skip proof is invented. A final job cannot
claim its own future success. Hosted synthetic PR merges and local PR heads remain distinct
subjects. These base collectors therefore do not claim an authenticated standalone build or
satisfy the final one-to-one merge bar yet. The no-metadata docs recorder correction is being
validated; it snapshots actual checkout identity before the unchanged test removes metadata.

## CI assertion replacement ledger

Old positions below refer to base `fa7347fc`; new positions refer to the current
source. Every original negative arm remains in the source-contract self-test.
The exact generated-graph check is additional to that preserved contract.

| Old assertion (file:line) | New assertion | Planted control and executed result |
|---|---|---|
| `scripts/ci_events.py:911`, ordered docs/elaboration carrier steps | `scripts/ci_events.py:924` retains each original command; `:4386` requires exact generated workers and aggregates | `scripts/ci_events.py:8821` removes/changes every generated job/step/body and masks conditions; all refused in the final 5,020-arm run. |
| `scripts/ci_events.py:3170`, allowed job keys; `:4207`, global protected carriers | Preserved source key/carrier assertions at `:3226` and `:4263`, plus complete generated graph at `:4386` | Generated unexpected environment, masked job and omitted job controls; protected aggregate missing/failure/cancelled/skipped controls in `scripts/ci_gate_workflows_selftest.py:49`. |
| `scripts/ci_events.py:4250`, complete source sequence pin coverage | `scripts/ci_events.py:4306` retains sequence completeness; source and generated graph are checked separately | Original carrier mutation arms plus generated per-step omission/body/binding controls; source-order preservation in `scripts/ci_gate_workflows_selftest.py:27`. |
| Original five-worker matrix/aggregate in `.github/workflows/rtl.yml` and `scripts/ci_events.py:2168` | `scripts/ci_suite_workflows.py:47` derives sixteen native workers and six unions; `scripts/ci_events.py:2224` preserves original gate bodies | `scripts/ci_suite_pieces_selftest.py` checks physical/expanded inventory, specialized ownership and load; `scripts/ci_suite_collect_selftest.py` drops and duplicates actual owners/receipts/logs. |
| `scripts/ci_events.py:2092` and `:2096`, compiler cache key shapes | `:2136` and `:2145` require exact version, source revision and workflow digest; clone recipes verify the revision | `scripts/ci_events.py:8197` removes each provenance component; generated cache controls also plant arbitrary keys and restore fallbacks. |
| Original Markdown, LiteX, Scala, archive and distribution-install cache shapes | `scripts/ci_install_workflows.py:37` and `:61` bind exact inputs; `scripts/ci_install_cache.py:41` hashes resolved versions, archive identities and recipe | `scripts/ci_install_cache_selftest.py:26` changes version/source/recipe independently and refuses bad/duplicate archives; every generated cache rejects altered key/path/fallback. |
| `scripts/ci_events.py:534` and `:2168`, implicit/dynamic driver pool commands | `:542` and `:2224` pin explicit four-worker lint/publication/saved-state/coverage commands | Full original body controls still refuse changed commands. The actual unbounded lint trial failed, while the bounded unchanged gate passed; saved-state and coverage runs also passed at four. |
| `scripts/ci_events.py:1496`, direct workflow text loading and `:8236`, on-disk controls | `:1536` also loads source templates; `:8377` runs original mutation arms through that source contract | Full graph equality independently prevents template projection from hiding altered physical workflows; all original arms plus new graph controls pass. |
| `scripts/ci_scope_history.py:142`, read scope from old elaboration carrier | `:142` bounds extraction to each generated worker job; `:276` runs both workers | Every existing historical/different-ancestry/classifier refusal runs unchanged for each worker. |
| `scripts/suite_shards.py:304`, one literal timeout; `:390`, weighted headroom | `:289` parses the generated two-budget shape; `:384` retains the 60-percent bound and adds a 1,620-second regular-worker cap | Original malformed/duplicate timeout and table/ownership controls remain; new regular-worker overload and dedicated-history controls pass. The history exception is explicitly authorized. |
| `scripts/act_ci.py:102`, four CPUs; `:119`, one job; `:4724`, CPU layout | `:102` sixteen CPUs; `:106` four global admissions; `:4710` disjoint sixteen-CPU ranges | `:7593` and CPU-layout controls test workflow permutations, nested widths, too-small hosts and nonoverlap; real four-container CPU/memory proof passed. |
| `scripts/act_ci.py:181`, isolated-slot memory cap | `:168` 36 GiB, composed from four 8 GiB containers plus 4 GiB overhead | `scripts/act_ci.py:15081` refuses missing/changed cap; all original teardown/containment controls remain. Measured four-job cgroups had no memory events. |
| `scripts/act_ci.py:5823`, serial workflow execution | `:5949` sends verified byte-identical workflows to one global bounded dispatcher | `:15517` plants changed/missing/extra/symlinked workflows, forged output and actual failure; process-group cleanup and cancelled/unstarted distinctions pass. Race-enabled dispatcher controls prove nested admission. |

The canonical generated graph has no privileged fork controller. The runtime
controls additionally remove Git metadata after retaining a real checkout,
refuse another head/tree or another identity consumer, and preserve observed
failure rather than generating success. These collector controls add coverage;
they replace no product test.

## Completed local validation and remaining coordination

The complete workflow contract passed 2,186 items and 5,020 planted arms after the CPU-derived
workflow regeneration. The final offline runner self-test also passed in a
CPython 3.12.3 disposable job without a Docker socket. Gate/case unions, physical-log
ownership, manifest comparison, source-plan binding, runtime transports, fail-fast,
historical scope and original cancellation controls passed.

Thirty-nine original documentation gate commands passed, including the required RV32
builder (1,017.498 s), compiler-absent controls (438.178 s), saved-state writer (82.979 s),
evidence ratchets, source lists, idiom, hygiene and diagram checks. The separate no-Git
job passed after recording its actual checkout and removing only the disposable clone's
metadata; recording its observed outcome with the retained identity also passed. The
wire-accountability self-test passed. Fresh documentation, contents and hygiene gates pass.

Firmware unit, linked RV32, saved-state and coverage gates passed. All 506 control mutants
were caught; AECP and SRP mutation shards passed, the latter in 646.185 s. All fast synthesis
source-set, OOC, active-guard and result-cache controls passed. The publication census
passed at eight GiB in 558.192 s with peak 5,738,594,304 bytes and zero memory-limit/OOM
events. The earlier four-GiB refused trial is retained. Four full Yosys shards and their
live-inventory aggregate passed: 58 expected and observed tops, required structural evidence,
zero errors. The memory measurement did not execute the hosted TARGET_SHA step; it is
local synthesis evidence, not a claimed hosted aggregate verdict.

The exact elaboration command `python3 sw/builder/test_builder.py --require-elaboration --require-rv32`
passed in 22m18.04s at `9a76ed5c`, maximum child RSS 3,368,332 KiB. Its existing ledger
declares two uncovered arms: MAKEFLAGS += -e has no effect on this make, and the real
calibration report is absent. No elaboration arm lacked its toolchain. All seven standalone LiteX simulations passed with zero skips, failures or timeouts; the aggregate self-test passed all ten controls.

All sixteen selected workers passed at `9a76ed5cf99996f433c82bcfde2fdb01fc05d743`.
The final candidate reread all six real unions, then collected and tallied all 62 physical
logs: 2,187,186 checks and zero in-suite failures. `source-correspondence.json` proves six
unchanged source groups and records the narrow scheduling/receipt differences. The older
simulation snapshot is not represented as the final workflow head.
A reused-worktree attempt correctly refused two changed generated report timestamps. Those
reports and the refusal are retained, and only those two known generated reports are restored
between successful workers. The dirty-source check is unchanged.

The non-Verilator boundary completed all 112 boundary, 155 pin and four figure controls
without a misbehaving control, but refused the README's stale figure of 120 pin controls.
The added Make targets automatically add 35 controls. The README now reports 155. The unchanged gate passed with zero findings, zero misbehaving controls and all 2,852 compiled sources checked; the documentation correction is committed.
The Verilator boundary's first mailbox build refused a make directory message parsed as
part of its compiler recipe. A four-arm diagnostic reproduced the message with and without
compiler capture under the local forced parallel make environment. A fresh build with
`MAKEFLAGS='-j8 --no-print-directory'` passed all normal checks and caught all six mutants.
The full unchanged Verilator boundary gate passed with that logging-only setting: 830 compiled sources, zero findings, six boundary controls, 155 pin controls, four figure controls and no misbehaving controls. The resumed
suite queue used the same logging setting and completed. No test predicate,
firmware behavior or linked image was changed.

All six full/sharded comparisons were reread by the production receipt CLI, including raw
stdout hashes. New controls dropped an actual case from every claim and changed stdout
together with its receipt hash; all were refused. Small receipts and raw-output size/hash
inventories are in `case-evidence/`. Final source-blob correspondence is recorded in `source-correspondence.json`: six source groups match, with the narrow receipt/scheduling differences shown explicitly.

Validation uses isolated scratch worktrees. Source objects and supplied compiler files are
mounted read-only into disposable jobs. No toolchain, virtualenv, source export or large file
is placed in this output directory. Environmental failures are retained: missing alternate
Git objects, private cache permissions, missing expected SDK alias, implicit lint concurrency,
undersized memory trials, generated report timestamps and make directory chatter. No failed
or incomplete attempt is counted as a passing gate. Full workflow timing and signed replay
remain with the coordinating role after publication.

## Resume completion and retained evidence

The CPU rulings 6166855177 and 6167284204, corrected by 6167288337, landed in this round.
Trigger removal and the signature-gate scope change 6166823105 remain round two.
Resume commits: `8eab741afa9762a4bf4f5fe2ad4755d223d26740` (creation-time bookings),
`237f5c25c3ee11e95f7855d25ae660b74cea8ca0` (CPU-derived budgets and proof forwarding), and
`cf9c936697a06e44c41681bcc12dc612a3242eb2` (pinned affinity-default documentation).

Worker 11 initially failed when its unchanged mutation driver could not restore a planted
file through a read-only scratch Git index. Its normal checks passed. The failed attempt,
mutation diff and hashes are retained in `readonly-index-attempt.json`. The isolated file
was restored and the whole worker rerun with only its own worktree metadata writable.
All nine suites passed, including all six gptp_txts mutation controls. No predicate changed.

`gate-validation-index.json` indexes 94 actual command receipts, including three retained
failed-attempt records with named passing replacements. `cpu-budget-gate-results.json`,
`cpu-step-artifacts.json`, `cpu-budget-artifacts.json`, `final-head-gates.json`,
`affinity-documentation-gates.json` and `dispatcher-build-ci4.json` retain resume controls
and provenance. Large logs have size/SHA-256 entries; no output file exceeds 200 KB.
All four scratch source worktrees and the candidate are clean. No worker container remains.
No push, PR operation, merge, rebase or hardware access occurred.

Hosted after-times and the full trusted replay remain with the coordinating role. The
media-clock warm-cache projection remains 33m52s before downstream collection under the
explicit readiness exception; its continuous history is unchanged. No independent review
verdict, reviewer-owned completion ledger or merge authorization is claimed.

### Completed local worker receipts

These timings mix pre-power-off and resumed runs sharing author resources. They are
local gate evidence, not hosted after-times or dedicated-range replay timings.

| Worker | Seconds | Result |
|---:|---:|---|
| 0 | 1115.397 | rc 0 |
| 1 | 1083.412 | rc 0 |
| 2 | 602.460 | rc 0 |
| 3 | 1240.088 | rc 0 |
| 4 | 533.257 | rc 0 |
| 5 | 828.229 | rc 0 |
| 6 | 1190.783 | rc 0 |
| 7 | 1333.074 | rc 0 |
| 8 | 1264.631 | rc 0 |
| 9 | 1413.293 | rc 0 |
| 10 | 1273.922 | rc 0 |
| 11 | 860.652 | rc 0 |
| 12 | 1295.209 | rc 0 |
| 13 | 1466.094 | rc 0 |
| 14 | 1327.127 | rc 0 |
| 15 | 745.531 | rc 0 |

## Round 2

Historical disposition before ruling 6172868895: STOP, pending the resource decision below. Starting head `cf9c936697a06e44c41681bcc12dc612a3242eb2`; origin and branch verified. Public rulings: 6169768594 and 6169805715. Reviews: R636-1 and R637-1.

Sequence: merge dev `fa820988` and regenerate census; nested compiler budgets; hosted cancellation paths and observer retries; worker headroom; measured memory sizing; comparisons at public source head; cache documentation; dependency-ready dispatch. Commit each validated step. No push authorized.

The round-two change map and evidence below supplement the retained round-one record. Hosted timings and full replay remain manager-owned.

Item 0 completed: merge `abf7a923a` has ordered parents `cf9c9366` and `fa820988`. `sw/firmware/ctrl/README.md:255` was regenerated by the merged `ctrl_boundary.pin_controls` census: 161 controls, zero failures, all four figure mutations refused. Evidence: `round2-merge-census.log`. The merged stack pin is `70936b77`; its top-level directory and public origin were verified before updating.

Item 1: `tb/verilator/media_nco/Makefile:12` consumes `VERILATOR_JOBS`; `scripts/ci_gate_workflows_selftest.py:23` dry-runs every registered capture child recipe at budgets 1/3/4 for job widths 4/12/16 and refuses a planted unlimited child. Existing capture scheduling controls pass; media-NCO actual simulation passes 410/410. Python idiom gate passes. Evidence: `round2-nested-budget.log`, `round2-media-nco.log`.

R636-1 B1/B2: `scripts/ci_suite_workflows.py:14` installs inventory prerequisites before union and aggregate reads; `scripts/ci_suite_pieces_selftest.py:86` requires their placement. Fresh checkout plus the emitted initialization produced all six inventories (19/31/31/66/3/4), recorded in `round2-fresh-inventories.json`. `scripts/ci_case_receipts_selftest.py:35` supplies a disposable fixture environment; its selftest passes with global/system identity files disabled. The workflow contract and Python idiom gate pass.

Item 2 completed in `1f364265f`: `scripts/ci_fail_fast.py:26` bounds observer reads, honors rate-limit headers, separates observer errors from confirmed failed jobs, and recognizes unexpanded skipped matrices. `scripts/ci_runtime_workflows.py` makes collection independent of the watcher and adds a same-repository terminal cancellation guard. Controls cover collector and watcher-tail failures, all four failure conclusions, raw skipped matrix names from run 38273578232, 403/429/502/timeout reads, sibling requests and fork refusal. Workflow contract: 2186 items, 5093 arms, rc 0. See `round2-gate-artifacts.json`.

Item 6 completed in `c2acac074`: `docs/testing/CI_WORKFLOWS.md:1567` now describes exact Scala and pip keys without prefix fallback. Documentation hygiene passes.

Item 7 completed in `e3a92e582`: `ci/act/dependency_executor.go:20` validates and schedules a dependency graph, joins started jobs and preserves first failure. `ci/act/fail-fast.patch:66` uses it across the complete combined plan; each physical matrix leg still acquires the shared admission gate. `ci/act/dependency_executor_test.go:13` keeps an unrelated long job live until its ready dependent starts. `scripts/build_ci_act.py:27` binds version ci5, the graph and controls in the build receipt; `scripts/act_ci.py` requires that version. Upstream controls and 20 race repetitions pass. Binary hash and size only: `round2-dispatcher-build.json`. The disposable offline runner selftest passes.

The real dispatcher replay has the short job finish before the dependent starts, while the long job remains running; all finish successfully. The old dispatcher fails the identical control after waiting for its stage. `round2-dispatch-start-times.json` records ordered log lines and timestamps; `round2-dispatch-control.yml` is the fixture. This self-hosted scheduling control proves dependency order, not Docker CPU placement or a full workflow replay.

Item 7 cancellation follow-up `782a4db0c`: `ci/act/job_admission.go:56` now honors both dependency cancellation and the shared admission cancellation. `ci/act/dependency_executor_test.go:77` plants a matrix/preflight failure while an unrelated job is already admitted. The prior admission implementation fails this control after three seconds; the corrected build passes 20 race repetitions and upstream tests. The actual replay was repeated successfully with the final binary, SHA-256 `4d30fb23a2d2485ea7a48c6c679d4dd3b482eafe73d55c1ec544842f96bbd3f5`, 30195511 bytes. Its final build receipt and start-time table replace the provisional versions.

Item 3 completed in `fec1f17cc`: `scripts/suite_shards.py:289` reads each actual worker limit and `:398` applies its own 60% bound. `scripts/ci_suite_workflows.py:66` gives regular workers 45 minutes (1620-second scheduling allowance), retaining the separate 1620-second refusal; the excepted media-clock leg retains 60 minutes (2160-second allowance). `scripts/ci_gate_workflows.py:134` gives gate workers the same 45-minute safety deadline. No suite deadline changes. The 16-worker count is retained because all ordinary conservative projections fit the existing margin rule after correcting the newly introduced job limits.

Local evidence is in `round2-worker-headroom.json` and `round2-docs-headroom.json`. The local documentation gate windows project to 889.900 and 1139.498 seconds including a 122-second allowance, leaving 730.100 and 480.502 seconds inside the 60% bound. The elaboration builder measured 1338.040 seconds; adding 122 seconds leaves 159.960 seconds inside its bound. Hosted measurements do not exist at the reviewed head because of the merge conflict; the next hosted run remains a manager-owned sizing check. All 5093 workflow contract controls, case/gate unions, sweep cancellation, source-list and evidence-reader controls pass. `round2-headroom-artifacts.json` retains commands/log identities. Both borrowed-timeout and disabled-absolute-budget mutations are refused. The sweep cancellation test uses the system interpreter because the supplied CPython build omits the required Linux pidfd APIs; the workflow/data controls use CPython 3.12.3.

Current scope clarification: the round-two fixes-only ruling supersedes earlier references to removing RTL triggers or adding the signature gate in round two. Those changes and the switch to the prebuilt image belong to a follow-up PR.

Item 4 update: ruling 6170460727 reports SIGKILLs in the older replay at 16 census workers under 8 GiB. The current generated workflow already uses the memory-bounded four-worker campaign budget. Its actual census command in a 16-CPU, 8-GiB container at `fec1f17cc` passed 234 normal checks, all 120 planted arms and all 31 rule-removal controls. Peak 5860151296 bytes (5.458 GiB), every memory.events counter zero. `round2-census-memory-16.json` binds the image, command and log. The subsequent twelve-CPU census also passes, as recorded below. Other shipped-width heavy classes remain unmeasured.

Additional cancellation validation: the same sweep cancellation gate passes inside the disposable CPython 3.12.3 image, which supplies the Linux pidfd APIs. Evidence: `round2-cancellation-cpython.log`. The earlier system-interpreter result is supplementary, not the only passing result.

The 12-CPU census also passes: 5201534976-byte peak (4.844 GiB), zero memory-event counters, all 234 checks, 120 planted arms and 31 rule removals. It uses the emitted four-worker budget. This is a width benchmark inside the assigned die, not a fallback-range admission proof. `round2-census-memory-12.json` binds the result. The older coordinating replay requested 16 census workers; this lane already emits four and does not rewrite another candidate workflow. The remaining memory finding is not claimed closed.

Round-two timing qualification: the watcher runs concurrently with the workload graph and now waits for the collector too. Completion can add 0 to 120 seconds after the collector, followed by the terminal guard checkout and decision. The guard has a three-minute safety limit; its actual duration is not measured yet. Earlier workflow-level warm projections must include this additional tail budget; they are not a new less-than-30-minute verdict. Per-worker headroom figures remain as recorded above. The coordinating hosted run must measure the complete graph, including this tail.

The previously heaviest synthesis shard (0/4, milan_datapath) passes with cold result caches at both CPU widths, including tied-input and tap-purity checks. Peaks: 3745005568 bytes at sixteen CPUs; 3391201280 bytes at twelve. Every memory-event counter is zero. The sixteen-CPU command ran in 471.279 seconds; the twelve-CPU boundary-file duration is recorded in `round2-yosys-memory-12.json`. See the two `round2-yosys-memory-*.json` receipts for exact command, cap, result hashes and source qualification. This adds synthesis evidence, not shipped-width compiler evidence.

Item 5 completed in `21bd10cec`: all six public-head comparisons pass. `round2-case-evidence/comparison-summary.json` records all 154 inventory units and 23 legs; `round2-case-cli.json` and `.log` record six production CLI comparisons returning zero. Each independently re-derived inventory rejects a case dropped from every claim, and each reference comparison detects an altered observation. Large raw logs have size and SHA-256 entries instead of copied bytes.

Additional item-7 replay: two workflows deliberately reuse job ID `shared`. The independent workflow is already active before the prerequisite finishes. The new dispatcher starts the dependent before that unrelated workflow finishes, and all three jobs pass. The old dispatcher fails the same control and never starts the dependent. `round2-multiflow-control/start-times.json` retains the asserted event order and timestamps; both workflow fixtures and logs are included. This is a scheduling control with two admission slots, not a Docker-placement or full-replay claim.

### Round-two file map

The mandatory merge imports dev's already published implementation and stack pin. The author corrections after that merge are limited to CI scheduling, evidence controls, budgets and their documentation.

| File:line | Change |
|---|---|
| `sw/firmware/ctrl/README.md:255` | Census-generated conflict resolution in the required merge. |
| `tb/verilator/media_nco/Makefile:12` | Exported compiler budget replaces unlimited compilation. |
| `scripts/ci_gate_workflows_selftest.py:22` | Real capture-child recipes and unlimited-child control. |
| `scripts/ci_case_receipts_selftest.py:33` | Disposable Git fixture identity independent of host configuration. |
| `scripts/ci_suite_workflows.py:14` | Fresh inventory dependencies; own worker limits at line 66. |
| `scripts/ci_suite_pieces_selftest.py:79` | Generated inventory prerequisites and placement controls. |
| `scripts/ci_fail_fast.py:24` | Bounded reads, rate headers, skipped matrices, observer distinction and late-failure cancellation. |
| `scripts/ci_fail_fast_selftest.py:21` | Observer, graph, first-failure and fork controls. |
| `scripts/ci_runtime_workflows.py:76` | Watcher, independent collector and terminal cancellation guard. |
| `scripts/ci_runtime_evidence_selftest.py:160` | Both write-token jobs require same-repository guards. |
| `scripts/ci_gate_workflows.py:134` | Gate-worker safety deadlines preserve their own headroom. |
| `scripts/suite_shards.py:289` | Resolve every actual worker deadline and enforce its own 60% bound; independent absolute-bound control. |
| `.github/workflows/docs.yml:721` | Generated collector, watcher and terminal guard; worker deadlines at line 113. |
| `.github/workflows/elaborate.yml:594` | Generated collector, watcher and terminal guard; worker deadlines at line 12. |
| `.github/workflows/rtl-fast.yml:1240` | Generated collector, watcher and terminal guard; worker deadlines at line 402. |
| `.github/workflows/rtl.yml:586` | Generated inventory setup, worker deadline expression and terminal graph at line 1372. |
| `ci/act/dependency_executor.go:20` | Combined-plan dependency dispatch without stage barriers. |
| `ci/act/dependency_executor_test.go:13` | Ready-dependent, malformed graph, cancellation and admitted-job failure controls. |
| `ci/act/job_admission.go:53` | Preserve dependency and admission cancellation for running jobs. |
| `ci/act/fail-fast.patch:66` | Adapt the combined plan to dependency dispatch with shared physical-job admission. |
| `scripts/build_ci_act.py:27` | Bind the changed dispatcher sources, controls and ci5 build identity. |
| `scripts/act_ci.py:87` | Require that reviewed dispatcher build. |
| `docs/testing/CI_WORKFLOWS.md:356` | Worker headroom, exact cache keys at line 1582, dependency scheduling and qualified memory evidence at line 2278. |

All generated workflow edits were produced by the workflow generator. No test predicate, firmware implementation or linked image was changed by the author corrections. The required merge's incoming changes remain attributable to its public second parent.

### Public comparison execution notes

The full and sharded commands use the public source head `cf9c936697a06e44c41681bcc12dc612a3242eb2`, tree `a5eb619c5c9ead508e7189fd77527d84d2c4fdda`. All compiler commands retain four processes. After the capture and MAAP queues finished, the remaining independent media-clock legs and the two small suites used a private two-slot compiler semaphore. The prior controller was paused while its already running test completed uninterrupted, then retired; that child's own exit-status and wall-clock receipt records rc 0. This only changed orchestration, not source, checks or compiler arguments. `round2-comparison-environment.json` records the native environment. Its durations are case-comparison timings, not replacements for the container-based CI timing model.

### Round-two memory measurements

All commands below ran inside an eight-GiB container with swap also capped at eight GiB, using the generated CPU-budget step and its four-worker campaign ceiling. All listed commands returned zero; every `memory.events` counter was zero. Sixteen CPUs used the assigned die; twelve is a width benchmark within that die, not proof of aligned fallback booking.

| Class | Sixteen-CPU peak | Twelve-CPU peak | Command / evidence |
|---|---:|---:|---|
| Publication census | 5860151296 bytes | 5201534976 bytes | `python3 sw/mailbox/publication_census.py --check --selftest --jobs "$CI_CAMPAIGN_JOBS"`; `round2-census-memory-*.json`. |
| Heaviest synthesis shard | 3745005568 bytes | 3391201280 bytes | `syn/yosys/run.sh --shard 0/4 --results /scratch/results --cache /scratch/cache`; `round2-yosys-memory-*.json`. |
| Firmware control normal phase | 1365569536 bytes | 1372815360 bytes | `python3 sw/firmware/ctrl/test/test_ctrl_firmware.py --require-rv32 --self-test --jobs "$CI_CAMPAIGN_JOBS" --shard 0/4`; `round2-firmware-memory-*.json`. |

The firmware phase includes required RV32 linked-image checks and all 61 assigned live invocations. Its elapsed boundary-file durations are 285.877 and 298.022 seconds. It does not represent the three other mutation phases. The initial sixteen-CPU trial refused read-only generated configuration output. That attempt is retained in `round2-firmware-environment-attempt.json`; the passing replacement used a disposable writable `configs/generated` overlay while the candidate source remained read-only. No generated file was copied back into the candidate.

The census regression reported by the coordinating replay requested sixteen concurrent front ends. This lane's emitted four-worker budget passes at both CPU widths; the runner does not silently change an older candidate's explicit command. `CONTAINER_MEMORY` remains eight GiB and `SLOT_MEMORY_MAX` remains 36 GiB: four job caps plus four GiB overhead. Those are bounded allocations, not a claim that all remaining job classes have been measured. Shipped-width large compiler builds and the four-build capture pool remain the item-4 gap.

The public-head comparisons repair the review's inaccessible-source evidence. They are deliberately bound to the public PR head specified by item 5. The mandatory dev merge also imports product and linked-build changes. `round2-source-delta.json` lists that incoming delta separately from the author CI fixes; no empty source diff or current-candidate full-suite pass is claimed from these older-head comparisons. The coordinating replay must validate the merged candidate.

### Completed public-head comparisons

All rows use public head `cf9c936697a06e44c41681bcc12dc612a3242eb2` and its recorded tree. All references and legs return zero. Every row matches case outcomes, return codes and checked-output digests, refuses a case dropped from all claims, and detects an altered observation.

| Suite | Inventory source at public head | Units | Legs | Full reference seconds |
|---|---|---:|---:|---:|
| `milan_dp` | `tb/verilator/milan_dp/Makefile:595 ci-list / RUN_CASES` | 19 | 4 | 1786.608 |
| `capture_coherence` | `tb/verilator/capture_coherence/mutants.py:580 arm_units` | 31 | 4 | 1793.223 |
| `maap` | `tb/verilator/maap/mutants.py:253 run_inventory` | 66 | 4 | 822.725 |
| `milan_dp_mclk` | `tb/verilator/milan_dp_mclk/mclk_mutants.py:251 run_inventory` | 31 | 4 | 1130.247 |
| `milan_dp_render` | `tb/verilator/milan_dp_render/Makefile:212 ci-list / RUN_CASES` | 3 | 3 | 590.963 |
| `pp_shadow` | `tb/verilator/pp_shadow/Makefile:157 ci-list / RUN_CASES` | 4 | 4 | 539.425 |

Inventory units may contain complete mutation campaigns; they are not individual assertion counts. `round2-case-evidence/artifact-index.json` binds every retained or oversized artifact. `round2-export-comparisons.py` re-derives inventories from the specified source and repeats the comparisons and planted controls. Every executed full/leg command is recorded in its `.run.json`.

```sh
python3 round2-export-comparisons.py --source "$PUBLIC_CHECKOUT" --runs "$CASE_RUNS" --output "$CASE_EVIDENCE"
```

The final comparison documentation passed hygiene, style, path and generated-contents checks before commit. The committed head then passed all 339 em-dash controls with zero findings. `round2-comparison-docs.json`, `round2-comparison-docs.log` and `round2-final-em-dash.log` record them. `round2-validation-logs/artifact-index.json` indexes 47 other round-two logs and explicitly distinguishes planted failures and the missing-renderer environment attempt from their passing replacements.

### Historical STOP disposition and restart requirement

Item 4 cannot be claimed complete. The assignment requires peaks for heavy classes at the shipped sixteen/twelve-CPU settings. The session instruction limits each Verilator build to four compiler processes and allows at most two simultaneous builds. Measuring the shipped sixteen/twelve-process large builds and four-build capture pool requires an explicit exception to those limits, or coordinating-role measurements with per-job peaks and OOM events. The complete per-class replay must also measure the builder/JVM jobs. The earlier replay stopped before the remaining RTL jobs and supplies no such peaks.

The requested decision is either to supply that per-class sixteen/twelve-CPU replay evidence, or authorize scoped measurements of one eight-GiB container at a time with the shipped compiler/capture widths. No cap is raised, shipping compiler budget reduced, test changed or acceptance criterion relaxed. The existing eight-GiB/36-GiB allocations remain unproven for the unmeasured classes.

All started author tests are finished. `round2-final-state.json` records the clean worktree and service peak of 11367583744 bytes, below the 13 GB ceiling, with every memory-event counter zero. `round2-commits.json` lists twelve one-line commits without bodies or trailers, including the required merge. `round2-source-delta.json` separates that merge from the CI corrections. Public completion disposition: STOP, not REVIEW READY. The coordinating role still owns publication, repinning the changed runner/dispatcher, hosted timings, live cancellation evidence, full candidate replay and independent re-review.

### Resumed item-4 measurements

Starting head `21bd10cec1a999791c9cd2c6d37c52372fb1504e`, clean branch and expected origin confirmed. Ruling 6172868895 permits one eight-GiB container at a time for datapath compilation, the four-build capture campaign, and builder/JVM jobs, at sixteen then twelve CPUs. Per-container peaks, OOM counters, command identities and cap arithmetic will be recorded here. Earlier STOP disposition is historical. No push is authorized.

Datapath compile and simulation completed at both widths: 3349397504 and 2697302016 bytes, 65.267 and 75.441 seconds, rc 0. Both ran 3,751 checks with zero failures and zero memory-event counters. `build-nxn8` elaborates eight streams with loopback; each width started with an empty model object directory. `docs/testing/CI_WORKFLOWS.md:2321` records the measured class; `round2-datapath-memory-*.json` binds commands, image and artifacts. The initial ownership refusal is retained in scratch and is not counted as a passing measurement.

Datapath evidence committed as `8b2675658`. Documentation hygiene, style, paths, generated contents and the 339 em-dash controls pass, rc 0. Candidate tree is clean.

Capture measurements complete: sixteen CPUs peak at 6047100928 bytes (5.6318 GiB), twelve at 5042556928 bytes (4.6962 GiB). Both whole campaigns pass 32/32 checks with zero memory-event counters, in 480.432 and 484.113 seconds. Sampling observes four concurrent Verilator processes and 16/12 compiler processes. The generated budget is applied before dividing the compiler allowance by the four campaign workers, exactly as the suite-piece runner does. `round2-capture-memory-*.json` and the corresponding command scripts bind the evidence. Builder/JVM measurements are now running.

Capture documentation gates pass, rc 0; `round2-resumed-capture-docs.json` records commands and log hashes. The runner memory-comment correction remains pending the complete resource sizing step.

Capture evidence is committed as `21df9e03e`. The builder has reached actual JVM execution under the sixteen-CPU affinity.

The sixteen-CPU builder completes with rc 0 after 1385.762 seconds, peak 3523665920 bytes, all memory-event counters zero. Actual JVM execution was sampled. Its unchanged verdict names two NOT RUN arms: the inert MAKEFLAGS += -e control for this Make version, and the absent physical calibration report. Required RV32 and elaboration instruments ran; no toolchain elaboration arm was skipped. The twelve-CPU builder is running. The SDK-selector environment refusal is retained separately in `round2-resumed-attempts.json`.

Both builder widths now complete, rc 0. Twelve CPUs peaked at 3172597760 bytes (2.9547 GiB) in 1366.174 seconds, with every memory-event counter zero. Both runs retain the same two NOT RUN arms and actually execute the JVM. `round2-builder-memory-*.json` records commands, image, peaks, events, timing and artifact hashes. The sixteen-CPU container was removed before final configuration export; its retained launch command supplies requested caps and image, while the completed state and cgroup telemetry were captured before removal. The twelve-CPU configuration was directly inspected. Documentation checks pass and the builder evidence is committed as `7117417ee`. Standalone LiteX measurements are in progress.

The sixteen-CPU standalone LiteX aggregate passes all seven simulations with zero skips, failures or timeouts; its ten runner controls pass too. Peak 3745722368 bytes, every memory-event counter zero, elapsed 467.715 seconds. The twelve-CPU counterpart runs in a fresh container with empty CPU metadata. Its disposable timestamp-model object directory was cleared before that member started so it compiles at the second width.

The twelve-CPU standalone aggregate also passes all seven simulations and ten runner controls, with no skipped or timed-out simulations. Peak 3303358464 bytes, all memory-event counters zero, workload time 453.392 seconds. All eight resumed workload containers ran sequentially and returned zero. `round2-resumed-resource-summary.json` records their non-overlapping start/finish timeline and the complete fourteen-receipt resource table. The final resource documentation checks pass. The offline runner self-test initially refused a missing sudo executable in the measurement image; the unchanged test is rerunning in the existing derivative image whose only extra layer installs that prerequisite. The refusal is retained separately.

The derivative image also lacked the Docker CLI required by an offline command-construction control. Both environment refusals are retained as `round2-resumed-runner-selftest-missing-*.json`. The final unchanged offline self-test now uses the existing full CI image, pinned to `sha256:2d09d1152abecc5ed7799ead632f263d21ebec1f685809fe99c4e3e8801dadcc`, with verified CPython 3.12.3 and the required executables. It still has no network, Docker socket, credentials or writable candidate mount. This is a runner-control environment, separate from the workload measurement image.

### Resumed Round 2 completion

Final head: `2658a64c408bf87ae36574f36a6deeb34b2f297f`. Ruling 6172868895 is implemented. The eight newly authorized workload measurements all return zero, with every memory-event counter zero. Together with the earlier census, synthesis and firmware receipts, fourteen class/width measurements now support the resource sizing. The required dev merge and earlier fixes remain intact. No push or PR write occurred; all started work is finished.

| Resumed class | Sixteen-CPU peak, bytes | Twelve-CPU peak, bytes | Workload seconds, sixteen / twelve | Result |
|---|---:|---:|---:|---|
| Eight-stream datapath compile and simulation | 3349397504 | 2697302016 | 65.267 / 75.441 | 3,751 checks at each width |
| Capture campaign, four builds | 6047100928 | 5042556928 | 480.432 / 484.113 | 32 checks at each width |
| Builder with required RV32 and elaboration | 3523665920 | 3172597760 | 1385.762 / 1366.174 | rc 0; the two declared NOT RUN arms remain outside the verdict |
| Standalone LiteX aggregate | 3745722368 | 3303358464 | 467.715 / 453.392 | seven simulations and ten runner controls at each width; no skips or timeouts |

The builder's two uncovered arms are the inert `MAKEFLAGS += -e` mutation on this Make version and the absent physical calibration report. Required RV32 and elaboration instruments run; JVM execution was sampled in both builder and both standalone runs. No assertion, case, timeout, firmware behavior or linked image was changed to obtain these results.

The workload image is `sha256:94128cff4711ebfe6d3c5ac10bf88cdc9bac5caff4f4b28fc873fc83897d8427`, with CPython 3.12.3 and Verilator 5.050. The builder and standalone containers start with empty CPU metadata and preinstalled dependency caches. Datapath model objects are cold at both widths; the standalone timestamp model also compiles at both widths. The twelve-CPU booking measures width within the assigned die, not aligned fallback admission. Times exclude setup before the workload script and are not complete hosted workflow times.

`round2-resumed-resource-summary.json` binds all fourteen receipts and proves the eight successful resumed containers have non-overlapping start/finish intervals. Actual cgroup peaks/events and CPU-affinity observations were retained. The sixteen-CPU builder container was removed before final configuration export: its cap/image settings come from the retained launch command, while final state, affinity and cgroup measurements were captured before removal. Other resumed receipts include inspected Docker limits and final state. No successful measurement is inferred from an unsuccessful attempt.

Resource arithmetic:

- Maximum measured class: 6047100928 bytes (5.632 GiB), capture at sixteen CPUs.
- Keep `CONTAINER_MEMORY = "8g"`: 8589934592 - 6047100928 = 2542833664 bytes (2.368 GiB) margin, 42.05% above the observed peak.
- Keep `CONCURRENT_JOB_LIMIT = 4` and `SLOT_MEMORY_MAX = "36G"`: four 8-GiB caps plus a 4-GiB daemon/service allowance equal 36 GiB; `floor((36 - 4) / 8) = 4`.
- Four measured maxima plus that allowance total 28483371008 bytes (26.527 GiB), leaving 10171334656 bytes (9.473 GiB) below the slot cap. This is arithmetic on separate peaks, not a measured simultaneous slot peak or a guarantee for future workloads.
- Sampled service `memory.current` stayed at or below 506015744 bytes. Adding the full single-container cap gives 9095950336 bytes, below the 13 GB operating ceiling. The maximum sampled sum of service and container current memory was 5918969856 bytes. These are separate cgroups and sampled values; Docker memory is not claimed to be included in the service counter.

No higher cap or further compiler reduction is needed from these samples. Capture retains four workers with four compilers each at sixteen CPUs, or three each at twelve. The census retains its measured four-worker ceiling. The coordinating full replay remains necessary to observe the aggregate slot and complete workflow timing under contention; no newer supplementary replay peak was posted when checked before completion.

Resumed file map:

| File:line | Change |
|---|---|
| `docs/testing/CI_WORKFLOWS.md:2303` | Distinguish completed scoped measurements from the coordinating concurrent replay. |
| `docs/testing/CI_WORKFLOWS.md:2320` | Datapath compile and simulation peaks at both widths. |
| `docs/testing/CI_WORKFLOWS.md:2327` | Four-build capture peaks, compiler allocation and passing checks. |
| `docs/testing/CI_WORKFLOWS.md:2334` | Builder/JVM peaks and the two declared uncovered arms. |
| `docs/testing/CI_WORKFLOWS.md:2341` | Standalone LiteX results, peaks and timings. |
| `docs/testing/CI_WORKFLOWS.md:2347` | Job-cap margin and four-job admission arithmetic. |
| `scripts/act_ci.py:153` | Correct the stale 64-GB comment to the existing four eight-GiB job caps plus four-GiB overhead. |

Only that comment and documentation changed after the measurement head. `round2-resumed-final-state.json` verifies the runner AST is identical to the measurement head, the measurement checkout's tracked source is unchanged, the candidate is clean, all resumed commits have one-line subjects and empty bodies, and no measurement container remains active. Its runner SHA-256 is `5ccbd700ece6f8ce0558767c77fa44435c9dbb2d37c48cc44269790ec64474dd` for coordinating repinning.

Final local evidence:

- `round2-resumed-resource-docs.json`: documentation, style, paths and generated contents checks, all rc 0.
- `round2-resumed-resource-source-gates.json`: Python idiom and evidence-helper pin checks, rc 0.
- `round2-resumed-hygiene.json`: repository hygiene, rc 0.
- `round2-resumed-runner-selftest.json`: complete isolated offline runner self-test, rc 0, CPython 3.12.3. The final image is `sha256:2d09d1152abecc5ed7799ead632f263d21ebec1f685809fe99c4e3e8801dadcc`; network and Docker socket are absent, candidate mount read-only. The initial missing-sudo and missing-Docker-CLI environment refusals are retained separately.
- `round2-resumed-final-validation.json`: committed-head punctuation gate and its controls, rc 0; diff whitespace check, rc 0.
- `round2-resumed-artifacts/index.json`: 52 workload artifacts, including 48 small retained files. Larger logs are represented by byte size and SHA-256. No toolchain, installed package, tree export or file above 200 KB is in the output directory.
- `round2-resumed-attempts.json`: the superseded ownership and SDK-selector environment refusals, never counted as passing measurements.

Reproduce the resource commands with the emitted CPU-budget step in one eight-GiB container at a time, at sixteen then twelve CPUs:

```sh
make -C tb/verilator/milan_dp build-nxn8
make -C tb/verilator/milan_dp exec-nxn8
VERILATOR_JOBS=$(( CI_BUILD_JOBS / CI_CAMPAIGN_JOBS )) python3 tb/verilator/capture_coherence/mutants.py --whole-suite --jobs "$CI_CAMPAIGN_JOBS"
python3 sw/builder/test_builder.py --require-elaboration --require-rv32
scripts/run_litex_sims.sh --selftest
scripts/run_litex_sims.sh "$LITEX_LOGS"
```

Each `round2-<class>-memory-<width>-run.sh` records the exact budget setup. The retained launch records show boundary provisioning. Run the candidate runner only as an offline self-test inside the disposable job boundary:

```sh
python3 -I scripts/act_ci.py --selftest --worktree "$PWD"
```

The remaining completion work is coordinating publication/repinning, complete candidate replay, hosted workflow durations including collection/watcher tail, live cancellation evidence and independent re-review. The accepted continuous-history exception, public-head comparison qualification, and fixes-only follow-up scope in the earlier Round 2 record still apply. REVIEW READY is an author handoff, not a review verdict or merge authorization.

## Round 3

Starting head: `2658a64c408bf87ae36574f36a6deeb34b2f297f`. Origin and the clean local lane agree. Assignment 6176299708 governs these fixes. Both round-two reviews are NEGATIVE; no review coverage is claimed.

| Item | Status | Evidence |
|---|---|---|
| 1. Inventory preparation for every reader | Passed | Fresh checkout and per-consumer removal controls |
| 2. Skipped matrices through collection | Passed | Retained hosted shape through collector, watcher and graph |
| 3. Observer-only collector/watcher failures | Passed | Production entry, virtual-clock retry and graph controls |
| 4. Worker timing and headroom | Passed; head timing rechecked in the continued session | Dedicated contract worker and prerequisite synthesis tool build |
| 5. Source-build memory sizing | Passed | Four bounded shipping-image measurements and arithmetic |
| 6. Outcome, skipped-step and scope controls | Passed | All three independently removed guards fail |
| 7. Follow-up residue | Recorded for coordinating checklist | Hosted concurrency and cache-conditional equality belong to #495 |

No push, PR modification, product behaviour change or linked-image change is authorized. Final full documentation and fast RTL step sets must pass on the committed head before readiness.

Round 3 item 1 passes. `scripts/ci_runtime_workflows.py:109` supplies the collector's pinned inventory preparation. `scripts/ci_suite_workflows.py:20` refuses an unprepared consumer before generation; `scripts/ci_gate_workflows_selftest.py:23` removes preparation independently from all twelve affected jobs. All four workflows are regenerated. Fresh empty-submodule checkout preparation and production collection cover inventories 19/31/31/66/3/4, as recorded in `round3-fresh-collector.json`. Synthetic union inputs establish dependency availability only. The generator, contract check, gate controls, runtime controls and Python idiom gate return zero.

Round 3 item 2 passes. `scripts/ci_workflow_plan.py:152` derives raw matrix mappings from committed workflow definitions; the generator uses the same mapping for the watcher. `scripts/ci_runtime_evidence.py:125` records valid raw skipped matrices as skipped legs and rejects invalid states and overlaps in both orders. `scripts/ci_runtime_evidence_selftest.py:51` sends the retained run 38273578232 names through the generated graph, production collector entry and watcher, requiring incomplete evidence and no cancellation. The reader pins are regenerated. Runtime, planner, cancellation, generator, contract and Python idiom checks pass; `round3-item2-gates.json` records focused command results.

Round 3 item 3 passes. `scripts/ci_fail_fast.py:55` supports a shared read deadline; `:151` emits observer-only output and exits successfully. `scripts/ci_runtime_evidence.py:201` bounds all collector API reads together and preserves unknown results after observer failure. `scripts/ci_runtime_workflows.py:111` gives collection fifteen minutes for its ten-minute read budget plus preparation/upload, and exports observer-only status only after successful collection and upload. The tail also recognizes the collector's explicit output. `scripts/ci_runtime_evidence_selftest.py:97` injects 403, 429, 502, timeout and retry exhaustion through the production entry point; a virtual clock proves waits of 360/480 seconds exceed the previous allowance while staying bounded. Every observer-only result is rc 0, explicit, incomplete and invalid for equality, with zero writes. Genuine collector identity and terminal failures remain blocking. `docs/testing/CI_WORKFLOWS.md:2657` describes this behavior. Runtime, fail-fast, generator, contract, gate, documentation and Python idiom checks return zero.

Round 3 item 4 passes. `scripts/ci_gate_workflows.py:65` assigns the two contract gates to source-derived worker 2; `scripts/ci_gate_receipts.py:54` derives all required legs and still proves the complete union. `scripts/ci_events.py:4386` exposes the production single-workflow generation check; every generated mutation applies it to its changed file, preserving every arm. `scripts/ci_suite_workflows.py:68` moves the unchanged Yosys build/cache into a prerequisite and gives synthesis workers the head-bound tool archive. Scheduling controls verify both placements and unchanged build bodies. All workflows are regenerated.

`round3-contract-timing.json`: full self-test rc 0, 2,186 contract items and 5,206 arms, 316.686 seconds. `round3-runner-timing.json`: full isolated runner self-test rc 0, 38.772 seconds, CPython 3.12.3, read-only candidate mount and no network or Docker socket. The earlier bare-interpreter missing-PyYAML attempt is an environment refusal, not passing evidence. `round3-controls-timing.json`: full added controls step rc 0 in 23.699 seconds. `round3-worker-projections.json` lists each gate, synthesis and simulation worker with its own bound and margin. Docs workers project at 922/1506/478 seconds against 1620 each. Docs workflow conservatively projects at 1776 seconds including collection and watcher/tail allowances; this corrects the PR's old 26-minute projection. Hosted after-times remain unmeasured. The Yosys cold-tool projection is 720 seconds using the review's 600-second estimate and 120-second overhead, against 1044; current hosted readback remains necessary. Generator, runtime, fail-fast, suite-headroom, install-cache, contract, Python idiom and documentation gates all pass.

Round 3 item 6 passes while item 5 measurements continue sequentially. `scripts/ci_case_receipts_selftest.py:167` plants the actual driver spelling `failed`; `scripts/ci_manifest_selftest.py:95` compares two identical skipped-step manifests, including absent skip-reason evidence; `scripts/ci_gate_workflows_selftest.py:205` combines independently legitimate but contradictory elaboration scopes. `round3-item6-mutations.json` records rc 0 for each pristine self-test and nonzero for each independently removed production guard in a disposable checkout. Candidate production predicates remain unchanged. The Python idiom gate passes.

Item 2 follow-up: `e4e6e20e3` rejects unknown names and malformed raw matrix states in the watcher before selecting a failed job. The same negative fixtures now traverse both transports. Runtime and watcher controls and Python idiom checks pass.

Source sizing progress: Yosys at sixteen CPUs and sixteen compilers completes rc 0 but reaches the full 8 GiB cap with 174 max events; it does not meet the required reserve. Twelve CPUs/compilers completes rc 0 at 6816423936 bytes with zero events, only 20.646% below the cap; it also fails sizing acceptance. These are retained sizing counterexamples, not accepted shipping measurements. The next measurements bound source-build parallelism under the authorized eight-GiB cap.

Full-step timing correction: the runner contract step invokes its self-test twice, once directly and once as an installed isolated copy. Executing that exact emitted step succeeds in 113.654 seconds. `round3-runner-timing.json` now records the full command. The 38.772-second receipt above was the single isolated invocation, not the whole step. Worker 2 is conservatively updated to 553 seconds, leaving 1067 seconds against its own bound. The slowest docs worker and whole-workflow projection are unchanged.

Round 3 inventory follow-up at `3083347d6`: the docs scheduling self-tests call the real inventory too. `scripts/ci_gate_workflows.py:156` inserts pinned preparation before that control gate; `scripts/ci_suite_workflows.py:23` includes that consumer in construction checks. Removal controls now refuse all thirteen affected jobs. Scheduling controls and Python idiom checks return zero.

Round 3 resource work in progress: unrestricted Yosys at sixteen compilers reached the 8 GiB ceiling; twelve compilers left only 20.65% reserve. Unrestricted Verilator at sixteen compilers left only 19.07%. These are rejected sizing observations, not accepted shipping settings. The provisional source-build budget is `min(available CPUs, 8)`. Verilator then passes at sixteen and twelve CPUs with 4811259904 and 4793225216 byte peaks and zero memory-event counters. Yosys bounded measurements are running sequentially. Container and slot caps are unchanged.

Round 3 item 5 passes at `c93c303f34a5887c76ac6778778cebbcbc48d399`. `scripts/ci_runtime_workflows.py:35` emits `CI_TOOL_BUILD_JOBS=min(available CPUs, 8)`; the source templates consume it in all nine tool-build recipes and all four generated workflows carry it. `scripts/ci_gate_workflows_selftest.py:120` verifies the limit at 1/4/12/16 CPUs. The contract retains every test arm and changes only source compilation parallelism. `docs/testing/CI_WORKFLOWS.md:2347` records all four measurements and the unchanged slot arithmetic.

Accepted source builds (CPU widths 16/12, eight compiler processes): Verilator peaks 4811259904 / 4793225216 bytes; Yosys peaks 5264482304 / 5117616128 bytes. Each returns zero with all memory events zero. Source-build reserve is at least 38.713% of the 8 GiB cap. Capture remains largest at 6047100928 bytes, leaving 2542833664 bytes, 29.603% of the cap. Four caps plus 4 GiB overhead remain 36 GiB; admission remains four. See `round3-source-sizing.json` and its individual source receipts. Measurement images, source recipe digests, actual caps, counter values, log sizes and SHA-256 values are recorded; large logs stay in scratch.

Final validation starts on clean committed head `c93c303f34a5887c76ac6778778cebbcbc48d399` in independent disposable checkouts. The full source command bodies are retained. Campaigns use four workers; simulation scheduling uses one child at a time, with four compiler processes per Verilator build, to respect this session's two-build ceiling. This is full gate evidence, not a hosted timing measurement or a complete replay. The isolated runner executes both original self-test invocations without host orchestration authority.

### Round 3 continued session

The previous session ended on a service capacity error, not on a decision. Its committed steps map to the assignment as follows:

| Item | Commits | Re-check |
|---|---|---|
| 1 | `cb25fc6b2`, `3083347d6` | Pinned inventory preparation for every reader, including the docs scheduling controls; thirteen removal controls |
| 2 | `8a8833e4e`, `e4e6e20e3` | Raw skipped matrices through graph, collector and watcher; malformed states refused before failure selection |
| 3 | `4c6f5b7cd` | Observer-only outcomes are explicit, incomplete and grant no cancellation |
| 4 | `225135e22`, `2ac674b47` | Contract worker separated; runner step timing counts both invocations |
| 5 | `c93c303f3` | Source compilation bounded at `min(available CPUs, 8)` |
| 6 | `c8896fab2` | Three removed guards each fail their self-test |
| 7 | none | Residue recorded for the #495 checklist; no change |

Two follow-up commits:

- `bbb19cec8`: `docs/testing/CI_WORKFLOWS.md:2668` cited the 306.617-second Yosys build as the local full-width figure. That build ran unrestricted and is a rejected sizing counterexample. The sentence now cites the accepted bounded sixteen-CPU build, 360.05 seconds. The 600-second projection input and the table are unchanged.
- `0fd126de4`: the committed-head docs-check bank failed `Bare-metal scope gate` (`scripts/check_baremetal_only.py --check`, class T) with three findings introduced by this lane's own `e09a7f9cb` and `97488b829`. No hosted context has run on PR #739, so nothing reported this earlier, and earlier local validation did not execute this gate on those heads. Fixes: `ci/constraints-ci.txt:1` and `docs/testing/CI_WORKFLOWS.md:2787` drop the host OS word from prose. `scripts/build_ci_act.py:28` keeps the Go archive pattern; `:58` fills its OS segment from `sys.platform`. The gate itself is unchanged. Under #259's stated non-goal, the Go release archive names the build host, not a product path. A file-pinned allowance in the gate would instead change what the gate checks, which this lane may not do. On this host the derived name equals the previous literal. `GO_SHA256` still admits only the one pinned archive. The bare-metal check reports 0 findings across 1331 files; its self-test passes 700 arms. The Python idiom gate and self-test, hygiene, install-cache self-test, docs, em-dash, style, TOC, CI-event contract and generator checks all return 0.

- `84ee9ea11`: `docs/testing/CI_WORKFLOWS.md:2647` said the CI-event self-test "passes 5,206 arms". At `0fd126de4` the docs bank's contract step (`ci_events.py --check` and `--selftest`) passes 5,209 arms in 201.196 seconds. The page now gives both figures. Projections keep the slower 316.686-second figure, so the `docs-gates-2` row (553 seconds) is unchanged and conservative.

Dispatcher rebuild at `0fd126de4` (`round3-dispatcher-build.json`): `scripts/build_ci_act.py` returns 0, downloads the archive under its derived name, passes the twenty race repetitions and upstream controls, and reports version `0.2.89+milan-ci5`. The binary SHA-256 `4d30fb23a2d2485ea7a48c6c679d4dd3b482eafe73d55c1ec544842f96bbd3f5` is identical to the round-two build. Only `recipe_sha256` changes, to the new recipe file's digest `80b7c8468467b226e9106afe6c66f88cd0a2dd0e9a4fb2a18a36bd14a50d37f7`.

Builder timing observation: the `0fd126de4` docs bank's `End-station builder gates` step took 1411.366 seconds. That bank runs one simulation child (`SIM_JOBS=1`), not the shipped width, to respect this session's two-build ceiling, and it shares CPUs 112-127 with the concurrent rtl-fast bank. The `docs-gates-1` projection keeps the 1386-second figure from the round-two sixteen-CPU shipping-width measurement, which ran alone in its container. The final-head bank's builder step took 1415.634 seconds under the same conditions. With the contended figures, `docs-gates-1` would be 1531 to 1536 seconds, still within its 1620-second bound. The whole docs workflow would then be 1802 to 1806 seconds, up to 6 seconds over thirty minutes. Hosted readback decides this; the hosted builder window at `7032bca5` was 1065 seconds.

Every bank attempt, with its classification, is in `round3-bank-attempts.json`. Two `c93c303f3` attempts were setup refusals: the checkout object store referenced an alternate that was not mounted in the container. One `bbb19cec8` docs attempt was a genuine gate finding (fixed in `0fd126de4`). One `bbb19cec8` rtl-fast attempt and one `0fd126de4` docs attempt were harness defects: the step `working-directory` was ignored, and the JVM caches were not provisioned the way the round-two builder measurement provisioned them. None of these is passing evidence. At `0fd126de4` the docs bank (40 steps), rtl-fast bank (20 steps), docs-check-no-git and the isolated runner self-test all return 0.

Committed-head step banks run the exact source command bodies in the shipping job image (one 8 GiB container per bank, CPUs 112-127, no network). The scratch runner now applies each step's `working-directory`. The first attempt at `bbb19cec8` ran `bdd-conformance` from the repository root rather than `tests`. That was a harness defect, not a gate result. Runner contract self-test at `0fd126de4`: rc 0, 101.53 seconds for both invocations, read-only candidate mount, no network or Docker socket. docs-check-no-git at `0fd126de4`: rc 0.

Final committed-head validation at `84ee9ea119b548b4982d2c0988d8753a2ce4d0cf` (`round3-committed-gates.json`, `round3-committed-gates-resources.json`). Each bank starts from a clean checkout with no ignored files, using the shipping image `sha256:94128cff4711ebfe6d3c5ac10bf88cdc9bac5caff4f4b28fc873fc83897d8427`. Each container has an 8 GiB cap, CPUs 112-127 and no network; none was OOM-killed.

| Step set | Steps | Result | Notable step times, seconds | Sampled container peak, bytes |
|---|---:|---|---|---:|
| docs `docs-check` | 40 | all rc 0 | builder 1415.634; contract 225.451 (5,209 arms); bare-metal 27.23; scheduling controls 21.374 | 3491540992 |
| docs `docs-check-no-git` | 1 | rc 0 | 7.141 | not sampled (seconds) |
| rtl-fast, all twelve jobs | 20 | all rc 0; scope `rtl=true` | publication census 659.203; control mutants 833.755; boundary 801.838; firmware Verilator 584.334 | 6089998336 |
| docs `Local act runner contract gate` | both invocations | rc 0 | 103.81 | 2 GiB cap |

The bank runner executes every non-setup source step body unchanged. Setup steps are provisioned by the image. Two step bodies run outside the banks: the source Yosys build, sized separately in item 5, and the runner contract gate, run in its own read-only isolated container. The final `rtl-fast` aggregation step runs with every upstream result set to the recorded success. These are local gate results, not hosted timings, a complete replay or a review verdict.

Runner SHA-256 for coordinating repinning at this head: `f968f67655ac386ea703248b724c3781b95ec379d3a5287b378e470df81f895c` (`scripts/act_ci.py`, changed in round three by `8a8833e4e`).

Final audit: clean worktree; origin still at `2658a64c`; twelve round-three commits, each with a one-line subject and no body or trailer; `git diff --check 2658a64c HEAD` is clean; no measurement container is running; no output file exceeds 200 KB. No test assertion, case, arm, timeout, firmware behaviour or linked image was changed to obtain a pass.


REVIEW READY posted: https://github.com/kebag-logic/milan-fpga/issues/737#issuecomment-6180445253 (text in `ROUND3-REVIEW-READY.md`).

## Round 4

Starting head: `84ee9ea119b548b4982d2c0988d8753a2ce4d0cf` (origin has it). Assignment: [Round 4 for PR #739](https://github.com/kebag-logic/milan-fpga/issues/737#issuecomment-6180908502), with [R636-3](https://github.com/kebag-logic/milan-fpga/pull/739#issuecomment-6180902426). R637-3 is POSITIVE; R636-3 is NEGATIVE for one MINOR (F1). No review coverage is claimed by this section.

| Item | Status | Commit | Evidence |
|---|---|---|---|
| 1. F1 shared read budget control | Passed | `cadd00137` | `scripts/ci_runtime_evidence_selftest.py:165` drives the production collector entry (shared deadline built at `scripts/ci_runtime_evidence.py:198`): `runs/1` recovers on its third attempt (480 s), the jobs page never recovers. Collection stops at 480 s ≤ 600 s; the same reads through the production `API` without a shared deadline take 960 s. Mutation `i3-no-shared-budget` → rc 1 (`AssertionError: collector reads took 960.0s`); pristine copy rc 0 |
| 2/S1. Conditional preparation refused | Passed | `6c36e98f0` | `scripts/ci_gate_workflows_selftest.py:38` plants `if: ${{ false }}` and `continue-on-error: true` on the preparation of each of the 13 reader jobs; `check_inventory_dependencies` (`scripts/ci_suite_workflows.py:21`) refuses all 26, plus the 13 removals. Mutation `i1-conditional-prep-accepted` → rc 1 (`accepted unprepared inventory reader: docs: if preparation in docs-gates-0`); pristine copy rc 0 |
| 2/S2. Non-transient client errors are genuine | Passed | `81a55f1f4` | `scripts/ci_fail_fast.py:45` `transient()` is the one ruled observer-only set (403, 429, 5xx, timeouts, transport errors that outlast retries); the retry loop (`:94`), the watcher (`:153`) and the collector (`scripts/ci_runtime_evidence.py:232`) all use it. Genuine side: 400/401/404 make one request, no sleep, no observer output, rc 1 in both (`scripts/ci_fail_fast_selftest.py:44`, `scripts/ci_runtime_evidence_selftest.py:142`). Observer side keeps 403/429/502/timeout/exhaustion and adds a transport `URLError`. Mutations: collector or watcher treating client errors as observer-only, 403 made genuine, transport made genuine; each kills its self-test (6/6 rc 1); pristine copies rc 0. `docs/testing/CI_WORKFLOWS.md:2765` |
| 2/S3. Elaboration workflow projection | Projection recorded; the worker followed the answer to STOP (see Round 4 S3 worker below; now 1313 s and 26.4 minutes) | `6ab22bca6`, then `4e39fb266`..`08adb21af` | `docs/testing/CI_WORKFLOWS.md:2664` derives both workers from hosted run 38495894212 (`7032bca5`) by the docs worker-zero method: `2144 - 593 - 3 + 60 = 1608` and `2144 - 1441 + 60 = 763` (table rows `:2685-2686`, replacing the 1561/713 gate-window-plus-120 figures). `:2715` records the workflow projection: 1608 + 270 = 1878 s (31.3 min), above 30 minutes |
| 2/S4. Field-oracle build uses `CI_TOOL_BUILD_JOBS` | Passed | `80bdcd690` | `.github/ci-templates/rtl.yml:297` → generated `.github/workflows/rtl.yml:375` (`cmake --build … --target packet_gen --parallel "$CI_TOOL_BUILD_JOBS"`), after the budget step (step 1 of 25 in `verilator-shards`; the build is step 20). Contract `scripts/ci_events.py:561` pins the bounded line (ledger row below). Mutation `s4-unbounded-field-oracle` (template reverted, regenerated in the copy) → `ci_events.py --check` rc 1 with 2 findings; pristine copy rc 0. `docs/testing/CI_WORKFLOWS.md:2348` says it is bounded but not separately measured |
| 3/R1. `CI_WORKFLOWS.md` source-build sentence | Passed | `4f7c281e7` | `docs/testing/CI_WORKFLOWS.md:2347` now reads "The Yosys and Verilator source builds use `CI_TOOL_BUILD_JOBS=min(available CPUs, 8)`", the exact text in R636-3-R1 |
| 3/R2. PR body publication sentence | Passed (output file) | none (not a tree file) | `PR-BODY.md` Round 3 status line now ends "The coordinating role published this head.", replacing "No push occurred." |

### Round 4 CI assertion replacement

Per ruling 6161122704, condition 1 (equal or stronger):

| Old assertion (file:line) | New assertion | Planted control and executed result |
|---|---|---|
| `scripts/ci_events.py:561` at `84ee9ea1`: field-oracle script line `cmake --build "$RUNNER_TEMP/tsn-gen/build" --target packet_gen --parallel` (unbounded GNU make) | `scripts/ci_events.py:561`: the same line with `--parallel "$CI_TOOL_BUILD_JOBS"`; the rest of the 8-line canonical script and its writer binding are unchanged | `s4-unbounded-field-oracle`: the template is reverted to the unbounded line and regenerated, and `ci_events.py --check` fails with 2 findings (step script and recorded writer). Pristine copy: rc 0 over 2,186 contract items |

### Round 4 elaboration projection and the STOP

The `7032bca5` elaboration job (run 38495894212, job 115631440899) took 2144 s: setup 101 s, `Elaboration gates` 1441 s, Verilator setup 3 s, `Standalone LiteX simulation aggregate` 593 s, post steps 6 s. The docs worker-zero method (whole hosted job, minus steps the worker does not carry, plus 60 s for recording and upload) gives:

| Worker | Formula | Projected s | Own 60% bound | Margin |
|---|---|---:|---:|---:|
| `elaborate-gates-0` | `2144 - 593 - 3 + 60` | 1608 | 1620 | 12 |
| `elaborate-gates-1` | `2144 - 1441 + 60` | 763 | 1620 | 857 |

These replace the round-3 rows (1561 and 713, gate window plus 120 s), which assumed only 120 s of setup and evidence where the hosted job shows 107 s of setup and post steps before any new evidence step. Workflow: 1608 + 60 (aggregate) + 60 (collector) + 120 (one watcher interval) + 30 (tail) = 1878 s, 31.3 minutes, above thirty minutes. The predicted-after for `elaborate` in the **Hosted before and predicted after** section above is superseded by this figure.

A further worker is required by S3, and it cannot be built from existing steps. Worker zero's gate is one command, `python3 sw/builder/test_builder.py --require-elaboration --require-rv32`. The template's other non-setup step is already on worker one. Splitting the command means changing the driver's `__main__` (`sw/builder/test_builder.py:29141`) to run a selected subset of its 103 gate functions. Three things make that a STOP rather than an implementation choice:

- The round-1 assignment says to STOP "if a test cannot be sharded without changing it". The driver ruling 6160937413 allowed driver refactoring for `milan_dp` and `milan_dp_mclk` only, under four conditions.
- Verdict semantics would change. The `SKIPPED` ledger, the `ALL GATES PASS [EXCEPT n NOT RUN]` line and `--require-elaboration` (`sw/builder/test_builder.py:24587`) are evaluated per process. A leg that holds no elaboration row passes `--require-elaboration` vacuously, so the union would have to prove that the elaboration arms ran in some leg.
- The standing authorisation reserves test-semantics choices for a STOP.

Measurement for the decision (`round4-elab-gate-timing.json`): the unchanged command, under a line-stamping wrapper with an unbuffered parent, ran in the shipping image (8 GiB, CPUs 112-127, no network, 16 CPUs) at `4f7c281e7`. That head is identical to the final head except `docs/testing/CI_WORKFLOWS.md`. Result: rc 0, `ALL GATES PASS EXCEPT 2 NOT RUN` (the same two recorded arms, `[gate 1b]` MAKEFLAGS and `[gate 11]` calibration report), peak 3,717,427,200 bytes, every memory event zero, 1292.671 s over 103 gates.

| Gate function | Local seconds |
|---|---:|
| `test_baremetal_profile_contract` | 945.182 |
| `test_nvm_firmware_shapes` | 110.852 |
| `test_clock_crossing_constraints` | 108.940 |
| `test_soc_option_refusals` | 18.452 |
| all other 99 gates | 109.245 |

The best two-leg division is `test_baremetal_profile_contract` against the other 102 gates: 945.182 s and 347.139 s. Scaled to the hosted gate window (× 1441 / 1292.671), worker zero would take about 1054 + 167 = 1221 s, and the workflow about 1221 + 270 = 1491 s (24.9 minutes). A function-level split is therefore sufficient; no gate needs dividing internally. The hosted log cannot time individual gates, because the parent's stdout is block-buffered there (all headers flush at 01:49:50 and at exit).

Decision requested in the STOP: may this lane refactor `test_builder.py`'s `__main__` to expose its ordered gate list as an inventory and run a selected subset? The conditions would be those of 6160937413, plus a union check that the elaboration verdict's arms ran in some leg. Alternatively, keep one elaboration worker and let hosted readback decide the 31.3-minute projection; that is an owner-level choice.

### Round 4 validation at `6ab22bca61a76c989ad9fbb94b9cde2639d38ca9`

All receipts are in this directory. Large logs stay in scratch and are recorded by size and SHA-256.

| Evidence | Result | Receipt |
|---|---|---|
| Docs-check bank: every non-setup step except the untouched builder gate, plus the runner gate run separately | 39/39 rc 0; CI-event contract 226.575 s, 5,209 arms; scheduling and evidence controls 23.459 s; bare-metal 28.704 s | `round4-committed-gates.json` |
| docs-check-no-git | rc 0 | same |
| Runner contract gate (both invocations; read-only candidate, no network or Docker socket) | rc 0, 103.101 s; `scripts/act_ci.py` SHA-256 `f968f67655ac386ea703248b724c3781b95ec379d3a5287b378e470df81f895c`, unchanged from round 3 | same |
| Em-dash gate against `84ee9ea1` and `fa820988`; `git diff --check 84ee9ea1 HEAD`; hygiene | all rc 0 | same (`focused_gates_by_item`) |
| Focused gates per item (self-tests, generator check, contract check, Python idiom, evidence pins, install cache, docs, style, paths, TOC) | all rc 0 at each commit | same |
| Mutation battery at the final head | 9/9 mutations make their self-test or check fail; 4/4 pristine copies rc 0 | `round4-mutations.json` |
| Bounded field-oracle build, the generated step body executed once | rc 0, 17.355 s, 16 CPUs, `CI_TOOL_BUILD_JOBS=8`, peak 836,313,088 bytes, zero events. The clone line was not executed: the checkout was fetched on the host because container networking is unavailable | `round4-field-oracle-build.json` |
| Elaboration gate timing | as above | `round4-elab-gate-timing.json` |

rtl-fast: no step is touched. Both rtl-fast files are byte-identical to `84ee9ea1`, and no rtl-fast template step reads a changed file. The bank harness found and avoided one setup defect: a plain local clone inherits the lane's object alternate, which is outside the container mount. Git then fails inside the container, and the HDL-reference gate reports "dirty". Fresh `--no-local` clones fixed this. The first attempt is not counted as evidence.

Round 4 file map (`84ee9ea1..6ab22bca6`, six commits, each a one-line subject without body or trailer):

| Commit | Files |
|---|---|
| `cadd00137` | `scripts/ci_runtime_evidence_selftest.py`, `docs/testing/CI_WORKFLOWS.md` |
| `6c36e98f0` | `scripts/ci_gate_workflows_selftest.py` |
| `81a55f1f4` | `scripts/ci_fail_fast.py`, `scripts/ci_runtime_evidence.py`, `scripts/ci_fail_fast_selftest.py`, `scripts/ci_runtime_evidence_selftest.py`, `docs/testing/CI_WORKFLOWS.md` |
| `80bdcd690` | `.github/ci-templates/rtl.yml`, generated `.github/workflows/rtl.yml`, `scripts/ci_events.py`, `docs/testing/CI_WORKFLOWS.md` |
| `4f7c281e7` | `docs/testing/CI_WORKFLOWS.md` |
| `6ab22bca6` | `docs/testing/CI_WORKFLOWS.md` |

No push, PR write, rebase or hardware access occurred, and no TAKEN comment was repeated. No test assertion, case, arm, timeout, firmware behaviour or linked image was changed. The watcher and collector classification change is the one S2 decided. The evidence helper pins and the runner are unchanged.

STOP posted: https://github.com/kebag-logic/milan-fpga/issues/737#issuecomment-6181763440 (text in `ROUND4-STOP.md`). Exited measurement containers from this round remain stopped on the host (none running).

### Round 4 S3 worker, after the answer to STOP

Starting head: `6ab22bca61a76c989ad9fbb94b9cde2639d38ca9` (not pushed; origin at `84ee9ea1`). Ruling: [Answer to STOP 6181763440](https://github.com/kebag-logic/milan-fpga/issues/737#issuecomment-6181778634). It permits refactoring `sw/builder/test_builder.py`'s `__main__` under the 6160937413 conditions, plus (a) union-level `--require-elaboration`/`--require-rv32` and (b) a measured split. Final head: `08adb21af0a72d839ce30b6c461503dad269d4d6`.

| Step | Status | Commit | Evidence |
|---|---|---|---|
| 1. Driver entry point: inventory and named subset | Passed | `4e39fb266`, `0838c64f9` | `sw/builder/test_builder.py:29157` `_gate_run_list` (inside `__main__`): `--list` prints the ordered inventory (0.5 s, pyyaml only, no submodule); `--gates a,b` selects that subsequence and refuses unknown, repeated, out-of-order or missing names before any gate runs (rc 1); `:29186` the one `for fn in _gate_run_list(bank, (...))` loop keeps the literal 103-name tuple, unchanged in order and content; `:29279` a subset prints `SUBSET: n of 103 gates ran` before its verdict; `:29304` `--receipt` writes inventory, selection, requirement flags, each gate's verdict and the NOT RUN rows it added, and the per-process `--require-elaboration` status, only after every selected gate returned. With no option the run list, output, verdict lines and exit status are as before |
| 2. Leg runner and union judgement | Passed | `fb81a89e4`, `3ca77034f` | `scripts/ci_builder_legs.py:31` `ISOLATED` (measured), `:39` `REQUIRED`, `:63` `partition`, `:71` `run` (template command after `--`, receipt bound to head and tree before and after), `:96` `elaboration_verdict` (the driver's own function), `:131` `union`, `:173` `compare`, `:193` `parse` |
| 3. Generated elaboration workers and aggregate | Passed | `fb81a89e4`, `3ca77034f` | `scripts/ci_gate_workflows.py:27` `BUILDER_SPLIT`, `:79` divided cases `gate_14_0`/`gate_14_1`, `:102` `builder_leg_step`, `:120` builder receipts uploaded; `scripts/ci_gate_receipts.py:26` `Collected`, `:119` the builder union required when the legs ran and refused when they were skipped; regenerated `.github/workflows/elaborate.yml` |
| 4. Unsharded versus union equality in the shipping image | Passed at `0838c64f` and at the final head `08adb21a` | | `round4-s3-equality.json` |
| 5. Planted controls in the owning leg | Passed | | `round4-s3-controls.json`, `round4-s3-mutations.json` |
| 6. Projections and documentation | Passed | `08adb21af` | `docs/testing/CI_WORKFLOWS.md:1408`, `:2686`, `:2712`, `:2742`, `:2755`, `:2920` |
| 7. Final validation | Passed | | `round4-s3-final-gates.json`, below |

Two defects were found by execution before any hosted run and fixed in their own commits:

- `3ca77034f`: argparse's `REMAINDER` positional swallowed `--receipt`, so the generated leg step could not parse (rc 2 in the shipping image). `parse()` now splits at the first `--`. The scheduling self-test parses every generated leg body through the production parser, and mutation `b6-generated-leg-without-separator` makes it fail.
- `0838c64f9`: gate `test_rom_clock_skip_reaches_the_ledger` requires exactly one `for fn in` loop whose iterable names `test_rom_clock_contract`. A `gates = (...)` tuple broke it (the unsharded run failed at that gate, rc 1). The literal tuple is back inside the one loop, passed through the selection helper; the gate is unchanged and passes in the reference run and in leg 1.

Measured split (ruling item 4). Round-4 per-gate times, the unsharded command alone at 16 CPUs (`round4-elab-gate-timing.json`): `test_baremetal_profile_contract` 945.182 s, the other 102 gates 347.139 s, wall 1292.671 s. So leg 0 is that gate alone and leg 1 is every other gate in inventory order (`ISOLATED`). Hosted scaling factor `1441 / 1292.671`. Measured legs at `0838c64f` (8 GiB, CPUs 112-127, no network, beside other builder runs on the same CPUs, which only lengthens them): leg 0 1028.283 s, leg 1 367.305 s, unsharded 1394.817 s.

| Worker | Formula (hosted run 38495894212) | Projected s | Own 60% bound | Margin |
|---|---|---:|---:|---:|
| `elaborate-gates-0` (leg 0) | `2144 - 593 - 3 - 1441 + 1146 + 60` | 1313 | 1620 | 307 |
| `elaborate-gates-1` (leg 1, Verilator, LiteX aggregate) | `2144 - 1441 + 409 + 60` | 1172 | 1620 | 448 |

`1146 = 1028.283 x 1441 / 1292.671` and `409 = 367.305 x 1441 / 1292.671`; the uncontended per-gate split gives 1054 and 387. Workflow: 1313 + 60 (aggregate) + 60 (collector) + 120 (watcher interval) + 30 (tail) = 1583 s, about 26.4 minutes, within 30. Before the split: 1608 s and 1878 s (31.3 minutes). Two workers are kept, so job names, the runner's two-owner elaboration scope fixture and the manifest plan keep their shape; the runner is unchanged.

Union judgement (ruling item 3). `REQUIRED` in `scripts/ci_builder_legs.py:39` names the owners independently of the inventory: the 15 gates that call `_litex_or_skip` for `--require-elaboration`, and `test_baremetal_profile_contract` (the only gate reading `--require-rv32`) for `--require-rv32`. `builder_owner_controls` (`scripts/ci_gate_workflows_selftest.py:171`) checks those names against the driver source by AST on every run. The union refuses unless every owner is in the fresh driver inventory, ran, and ran in a leg whose argv carried its flag. It then applies the driver's own `_require_elaboration_verdict` to the union NOT RUN ledger. A leg whose own per-process verdict failed is refused too.

Equality (ruling item 5), at `0838c64f` in the shipping image (`round4-s3-equality.json`):

- Unsharded `run all`: rc 0, `ALL GATES PASS EXCEPT 2 NOT RUN` (`[gate 1b]` MAKEFLAGS arm, `[gate 11]` calibration report), 103 rows, peak 3,513,835,520 bytes, zero memory events.
- Leg 0: rc 0, 1 row, NOT RUN `[gate 1b]`, peak 615,874,560 bytes. Leg 1: rc 0, 102 rows, NOT RUN `[gate 11]`, peak 3,237,867,520 bytes.
- `ci_builder_legs.py union --reference`: rc 0, "103 gates exactly once; requirements judged on the union; equal to the unsharded run". Every per-gate row (verdict and NOT RUN rows) and the ordered ledger are equal.
- Production aggregate replay (`ci_gate_receipts.py record` for both workers, then `verify` over the real builder receipts in the downloaded-artifact layout): rc 0, "elaborate: 3 source gates exactly once; all worker jobs successful"; the union digest covers steps and builder verdicts.
- Printed output, beyond the ruling: of 103 gates, 96 print byte-identical output in the legs and the unsharded run, and 7 are identical once per-run temporary paths and elapsed-second figures are masked. None differs otherwise.

Planted controls (ruling items 2 and 3; `round4-s3-controls.json`):

| Control | Owning leg | Unsharded | Owning leg | Other leg |
|---|---|---|---|---|
| M1: boot-order claim reworded in `docs/integration/BAREMETAL_FIRMWARE.md` | 0 | rc 1 at `test_baremetal_profile_contract` (162 s), "bare-metal boot contract lost" | rc 1, same assertion (9 s) | leg 1 rc 0 (388 s) |
| M2: FPU refusal removed from `sw/litex/milan_soc.py` | 1 | rc 1 at `test_soc_option_refusals` (2 s), the planted option reaches setup | rc 1, same failure | leg 0 rc 0 (1027.9 s) |
| Leg 1 run without `--require-elaboration` | union | n/a | the leg itself passes, rc 0 (the vacuous pass) | production aggregate with the real leg 0: rc 1, "--require-elaboration on the union: test_soc_option_refusals, ... ran only in a leg without the flag", naming all 15 |

Each planted defect was committed only inside its disposable clone and run through the leg runner exactly as the generated step runs it; a failing leg writes no receipt. Synthetic union controls in `ci_gate_workflows_selftest.py` (each refused by name): elaboration gate deleted from the inventory, its leg lost, skipped inside its leg, moved to a leg that never ran, run without the flag; the RV32 gate run without `--require-rv32`; a toolchain skip under a passing leg verdict; a failed own verdict; failed gate, changed selection, duplicated leg, changed head, changed driver inventory, unknown flag; a lost measured gate; an unequal NOT RUN row against the reference.

Mutation battery at `08adb21af` (`round4-s3-mutations.json`): 7/7 mutations make `ci_gate_workflows_selftest.py` fail; 2/2 pristine copies pass. `d1-elaboration-gate-deleted-from-inventory` deletes `test_every_recipe_elaborates` from the real driver run list and is refused "--require-elaboration on the union: test_every_recipe_elaborates absent from the driver inventory".

### Round 4 S3 CI assertion replacement

Per ruling 6161122704, condition 1 (equal or stronger). `scripts/ci_events.py` is unchanged; the contract still pins the template's one builder command, and the generated legs are held by `check_generated_workflow`.

| Old assertion (file:line at `6ab22bca`) | New assertion | Planted control and executed result |
|---|---|---|
| `scripts/ci_gate_workflows.py:69`: exactly one case on leg 1, and a leg-0 case | `:82`: exactly one case named the measured long gate, and a leg-0 case; for `elaborate`, exactly `LEGS` divided builder cases. For docs only the long gate takes leg 1, so the two are equivalent | Long gate renamed, long gate duplicated (docs and elaborate) and builder command renamed: all refused (`generator-controls`, rc 0 harness) |
| `scripts/ci_gate_workflows_selftest.py:180`: each generated gate step equals its template step | Undivided steps unchanged. A divided step equals `builder_leg_step(template)`, ends with ` -- <template command>`, keeps every other key, and parses through the production parser to that leg, receipt and command | `b6-generated-leg-without-separator`: rc 1 |
| `:183`: worker gate steps in template order, by `original.index(step)` | Same order through the case-id map, plus the worker's gate count | Pristine rc 0; divided steps are not template-equal, so `index()` cannot locate them |
| `:229`: case count equals non-setup template steps | Distinct template indices equal non-setup steps, and divided cases equal `LEGS` (0 for docs) | Pristine rc 0 |

### Round 4 S3 final validation at `08adb21af0a72d839ce30b6c461503dad269d4d6`

Fresh `--no-local` clones in the shipping image (`sha256:94128cff...7d8427`), 8 GiB, CPUs 112-127, no network. `08adb21a` differs from the measurement head `0838c64f` only in `docs/testing/CI_WORKFLOWS.md`, and the equality was repeated at `08adb21a` itself.

| Evidence | Result | Receipt |
|---|---|---|
| Builder legs and unsharded reference at `08adb21a` | Reference rc 0, 1311.061 s, `ALL GATES PASS EXCEPT 2 NOT RUN`, peak 3,723,018,240 B; leg 0 rc 0, 984.818 s, peak 619,937,792 B; leg 1 rc 0, 348.095 s, peak 3,440,762,880 B; every memory event zero | `round4-s3-equality.json` (`final_head`), `round4-s3-receipt-f-*.json` |
| `ci_builder_legs.py union --reference` at `08adb21a` | rc 0: 103 gates exactly once, requirements judged on the union, equal to the unsharded run. Per-gate verdict digest `47dc3c6a...` is identical to the `0838c64f` run | same |
| Production aggregate replay at `08adb21a` | `ci_gate_receipts.py verify` rc 0 over the real leg receipts | same |
| Printed output at `08adb21a` | 96 byte-identical, 7 identical after masking temporary paths and elapsed seconds, 0 different | same |
| Docs-check bank: all 40 non-setup steps | 40/40 rc 0. Builder gate (default path, 103 gates, no SUBSET line, same verdict) 1363.253 s; CI-event contract 203.179 s, 5,212 arms; scheduling and evidence controls 22.719 s, with the builder-leg controls; em-dash, TOC, style, paths, bare-metal, idiom gates | `round4-s3-final-gates.json` |
| docs-check-no-git | rc 0, 6.509 s | same |
| Runner contract gate (both invocations, read-only candidate, no network or Docker socket) | rc 0, 104.526 s; `scripts/act_ci.py` SHA-256 `f968f67655ac386ea703248b724c3781b95ec379d3a5287b378e470df81f895c`, unchanged | same |
| Mutation battery | 7/7 killed, 2/2 pristine pass | `round4-s3-mutations.json` |
| rtl-fast | No template or workflow byte changed and no step body reads a changed file; `pp_srcs.py --check --selftest` (reads every tracked file) and `ci_scope.py --selftest` rc 0 on the host | `round4-s3-final-gates.json` |

The final legs ran faster than at `0838c64f` (984.8/348.1 s against 1028.3/367.3 s). The projection keeps the slower pair, which is the conservative choice.

Round 4 S3 file map (`6ab22bca..08adb21a`; each commit has a one-line subject, no body and no trailer):

| Commit | Files |
|---|---|
| `4e39fb266` | `sw/builder/test_builder.py` (entry point and module docstring) |
| `fb81a89e4` | `scripts/ci_builder_legs.py` (new), `scripts/ci_gate_workflows.py`, `scripts/ci_gate_receipts.py`, `scripts/ci_gate_workflows_selftest.py`, generated `.github/workflows/elaborate.yml` |
| `3ca77034f` | `scripts/ci_builder_legs.py`, `scripts/ci_gate_workflows_selftest.py` |
| `0838c64f9` | `sw/builder/test_builder.py` |
| `08adb21af` | `docs/testing/CI_WORKFLOWS.md` |

Superseded attempts (not evidence): at `fb81a89e` the leg command could not parse (rc 2, fixed in `3ca77034`); at `3ca77034` the unsharded run failed at `test_rom_clock_skip_reaches_the_ledger` (rc 1, fixed in `0838c64f`), and its leg-0 run was stopped. Their run directories are kept in scratch under `runs-fb81a89e-parse-refused` and `runs-3ca77034-loop-shape-refused`.

No push, PR write, rebase or hardware access occurred, and no TAKEN comment was repeated. No gate function, assertion, fixture, timeout, NOT RUN arm, firmware behaviour or linked image changed. Every measurement container has exited.


REVIEW READY posted: https://github.com/kebag-logic/milan-fpga/issues/737#issuecomment-6183508390 (text in `ROUND4-REVIEW-READY.md`).

## Round 5

Starting head: `08adb21af0a72d839ce30b6c461503dad269d4d6` (origin has it). Assignment: [Round 5 for PR #739](https://github.com/kebag-logic/milan-fpga/issues/737#issuecomment-6184143571). Both round-4 reviews are POSITIVE at `08adb21a`: [R637-4](https://github.com/kebag-logic/milan-fpga/pull/739#issuecomment-6183672250) and [R636-4](https://github.com/kebag-logic/milan-fpga/pull/739#issuecomment-6184124102). No review coverage is claimed by this section. Work in progress; this section is updated as each item passes.

| Item | Status | Commit | Evidence |
|---|---|---|---|
| 1. Merge `origin/dev` `f6260253` | Committed; host gates pass | `8db583050` | Parents `08adb21a`, `f6260253`. Details below |
| 2. Re-project the worker the added suite lands on | Committed; host gates pass | `e3d25d964` | Worker 3 at 1544 s; details below |
| 3. Verify the committed merge head in the shipping image | Passed | | docs-check (41 steps), docs-check-no-git, runner gate, worker 3/16 and rtl-fast (20 steps) all rc 0; details below |

### Round 5 item 1: the merge

`8db583050` is a merge commit with ordered parents `08adb21af0a72d839ce30b6c461503dad269d4d6` and `f62602531d415d6c1cae1374a3cc2938faf54049`. `git fetch origin dev` gave `f6260253`. Git reported conflicts in exactly the three files the assignment names; everything else from dev merged cleanly and is attributable to the second parent (53 files, including the `gptp-processor` gitlink `7dda9c3b` -> `e4869fd0`; its top-level directory and origin `https://github.com/Mister-M-alt/FPGA-gPTP.git` were checked before updating it).

| File:line | Resolution |
|---|---|
| `scripts/suite_shards.py:22` (docstring) | This branch's docstring kept. Dev's only change there rewrapped "all five Verilator workers" in the refresh paragraph that this branch had already replaced |
| `scripts/suite_shards.py:146` | `WORKER_OVERHEAD_SECONDS = (122,) * 16` and the split-parent tables kept; dev's six-entry tuple belongs to its six-worker layout |
| `scripts/suite_shards.py:101` | `"gptp_tables": 568` (dev merged it at the provisional 1800). The figure is a hosted window, not the `suite_timeout` figure, so `PROVISIONAL_SUITES` stays empty (`:141`). The comment at `:68` names both hosted runs |
| `scripts/suite_shards.py:873` | Landmark kept as `milan_dp_mclk__0` on the last worker; the comment now says so (dev's auto-merged text said worker 5 runs `milan_dp`, which is false on sixteen workers) |
| `.github/ci-templates/rtl.yml:141,161,162,228,429` | Dev's six `rtl.yml` edits applied to the source template by `git merge-file` (template, dev's old `rtl.yml`, dev's new `rtl.yml`): clean, no conflict. The template now has dev's six-worker matrix, its `5)` `milan_dp` arm and `--expect 6` |
| `scripts/ci_suite_workflows.py:101-128` | The generator read literal `4)` and `--expect 5`. It now derives both from the template's own `matrix.total` and refuses a template whose ownership arm or verifier expectation does not match it |
| `.github/workflows/rtl.yml` | Regenerated by `python3 scripts/ci_gate_workflows.py`, never hand-merged. The output is byte-identical to `08adb21a`'s generated file, and `git diff 08adb21a HEAD -- .github/workflows` is empty |
| `docs/testing/CI_WORKFLOWS.md:348,367` | All six hunks keep this branch's sixteen-worker text. Counts move to 80 units and 63 suites. One paragraph keeps dev's #713 facts (provisional 1800 s figure, added sixth worker at 115 s overhead, refresh rule) and states the placement. The other hunks only changed five to six workers |

Contract count: `ci_events.py --check` reports 2,187 items against 2,186 at `08adb21a`. An item-by-item comparison of both trees (`round5-contract-items.json`) shows the only difference: the template now has six matrix names, `Verilator shard 0/6` to `5/6`, where it had five. The other two changed items are the same checks with 6 in place of 5.

Generator controls (`round5-generator-controls.json`, disposable clones of the head):

| Control | Result |
|---|---|
| Pristine `ci_gate_workflows.py --check` | rc 0 |
| M1: the `08adb21a` literal generator on the merged six-worker template | It emits a shard-5 `milan_dp` arm and `--expect 6` into the sixteen-worker graph. `ci_events.py --check` still returns rc 0, because the contract checks the template, and the generated graph only against the generator. Hosted, that graph fails closed (shard 5 holds more than `milan_dp`; sixteen shard directories against `--expect 6`). This is why the generator now derives both values |
| M2: template without its dedicated arm | rc 1, "template ownership step lacks its dedicated milan_dp arm" |
| M3: template verifier `--expect 7` with six workers | rc 1, "template verifier lacks its worker-count expectation" |
| M4: template arm index 4 with six workers | rc 1, same arm refusal |

### Round 5 item 2: where `gptp_tables` lands

Hosted windows (`round5-gptp-tables-hosted.json`; measured with dev's own `suite_shards.py --measure`):

| Run | Event, head | Worker | `gptp_tables` window |
|---|---|---|---:|
| 38538854504 | pull_request, `7fb3664b` (PR #713), all six workers passed | 0/6 | 474 s |
| 38601263345 | push, `f6260253` (merged dev); worker 0/6 passed all 8 suites, worker 2/6 timed out in `milan_dp_gm_steps` and `milan_dp_mclk` | 0/6 | 568 s |

The table takes the larger, 568 s. The provisional 1800 s figure cannot be kept: the selector would put the suite first on worker 0 at 1922 s, over both the 1620-second absolute budget and its 60% bound, and the shard self-test fails (planted control below).

| Worker | Before the merge | After | Own 60% bound | Margin |
|---|---:|---:|---:|---:|
| 0/16 | 1605 | 1605 | 1620 | 15 |
| 1/16 | 1495 | 1541 | 1620 | 79 |
| 2/16 | 1572 | 1572 | 1620 | 48 |
| **3/16 (`gptp_tables`)** | 1494 | **1544** | 1620 | **76** |
| 4/16 | 1521 | 1540 | 1620 | 80 |
| 5/16 | 1492 | 1539 | 1620 | 81 |
| 6/16 | 1495 | 1539 | 1620 | 81 |
| 7/16 | 1498 | 1540 | 1620 | 80 |
| 8/16 | 1493 | 1541 | 1620 | 79 |
| 9/16 | 1493 | 1543 | 1620 | 77 |
| 10/16 | 1497 | 1540 | 1620 | 80 |
| 11/16 | 1497 | 1539 | 1620 | 81 |
| 12/16 | 1493 | 1539 | 1620 | 81 |
| 13/16 | 1491 | 1538 | 1620 | 82 |
| 14/16 | 1494 | 1538 | 1620 | 82 |
| 15/16 (media-clock exception) | 2032 | 2032 | 2160 | 128 |

All figures include the 122-second setup allowance. Longest-first placement moves 56 other units between workers when the suite enters; the selector derives every owner at run time, so no list is edited. Worker 3 now runs `maap__2`, `milan_dp__0`, `chmap_capture`, `gptp_tables` and `tdm_render`. Against the 30-minute target, worker 3 leaves 256 s before downstream collection. Using the 270-second aggregate, collector, watcher and tail allowance applied to docs and elaboration, a path through worker 3 alone reaches 1814 s, 14 s over 30 minutes. It does not set the workflow end: worker 0 (1605 s, unchanged) and the media-clock exception (2032 s, unchanged) are longer. With the 474-second figure the suite lands on worker 14 at 1531 s instead.

`CI_WORKFLOWS.md:2731-2746` carries the new rows and `:2749` the worker-3 margin (`e3d25d964`).

Planted controls for the placement and the union proof (`round5-gptp-tables-controls.json`, all pass at `e3d25d96`):

- The inventory comes from the driver's discovery: 63 default suites and 80 units, with `gptp_tables` among them.
- Removing its duration is refused by the headroom gate and by sharded selection. The provisional 1800-second figure is refused (worker 0/16 at 1922 s).
- `suite_shards.py --ci-pieces --shard 3/16` prints it.
- The production collector, on the real inventory, releases its log to the unchanged tally. It refuses the log missing from worker 3, moved to worker 0, or duplicated on worker 0, and the restored fixture passes again. The unchanged tally refuses the complete set without it.

### Round 5 item 3: verification at `e3d25d964b5bbf0187290d0a357c6a6e4c5afd17`

Fresh `--no-local` clones of the committed head, the five pinned submodules checked by top-level directory, origin and gitlink (`final/validation-source-*.json` in scratch). One container at a time on CPUs 64-79 (this session's die), shipping image `sha256:94128cff...7d8427`, 8 GiB, no network, exact template step bodies, `PUSH_BEFORE_SHA` = dev `f6260253`.

| Evidence | Result | Receipt |
|---|---|---|
| Docs-check bank: all 40 non-setup `docs-check` steps, plus `wire-accountability` | 41/41 rc 0. Builder gate 1482.211 s (default path); CI-event contract 214.758 s; saved-state writer 174.183 s; scheduling and evidence controls 23.006 s. Peak 4,576,628,736 B, every memory event zero | `round5-final-gates.json` |
| docs-check-no-git | rc 0, 7.343 s | same |
| Runner contract gate (both invocations; read-only candidate, no network or Docker socket) | rc 0, 101.992 s. `scripts/act_ci.py` SHA-256 `f968f67655ac386ea703248b724c3781b95ec379d3a5287b378e470df81f895c`, unchanged; `git diff 08adb21a HEAD -- scripts/act_ci.py` is empty | same |
| Generated worker 3/16 (where `gptp_tables` lands): budget, tree record, Verilator proof, ownership proof with `suite_shards.py --selftest`, and the shard step | rc 0. `PASS` for `maap__2`, `milan_dp__0`, `chmap_capture`, `gptp_tables`, `tdm_render`; 5,518 checks, 0 in-suite failures; shard step 1121.216 s. By log modification times `gptp_tables` took about 409 s. Peak 3,919,286,272 B, zero events | `round5-worker-3-of-16.json` |
| rtl-fast bank: every non-setup step of all twelve jobs (the two source Yosys builds skipped; the image provides the pinned Yosys) | 20/20 rc 0 across twelve jobs, scope `rtl=true`, 5,120.9 s of steps. Census 633.767 s; control mutants 845.070 s; firmware boundary 875.336 s; firmware Verilator 582.181 s. Peak 6,157,991,936 B, every memory event zero | `round5-final-gates.json` |
| Host gates at the committed head `e3d25d96` (clean tree): generator `--check`; CI-event `--check` (2,187 items); shard, collector, pieces, gate-workflow, plan, fail-fast, runtime-evidence, manifest, case-receipt and install-cache self-tests; evidence pins; idiom; hygiene; `pp_srcs.py --check --selftest`; scope self-test; bare-metal check; em-dash against `f6260253` and `08adb21a`; `git diff --check 08adb21a HEAD`; docs, style, paths, TOC. The CI-event `--selftest` (2,187 items, 5,212 arms) ran inside the docs bank, and also on the host at the merge tree (218.7 s) | 26/26 rc 0 | `round5-final-gates.json` |
| Elaboration builder legs at the merged head (beyond item 3: dev changed `sw/builder/test_builder.py`, which the legs divide). Unsharded reference, leg 0 and leg 1 run beside each other on CPUs 64-79 | All rc 0. Reference 1506.554 s, `ALL GATES PASS EXCEPT 2 NOT RUN`, peak 4,705,251,328 B; leg 0 1081.009 s, peak 645,799,936 B; leg 1 495.144 s, peak 5,707,837,440 B; every memory event zero. `ci_builder_legs.py union --reference`: 103 gates exactly once, requirements judged on the union, equal to the unsharded run; per-gate verdict digest `47dc3c6a...`, identical to round 4's. Production aggregate replay (`ci_gate_receipts.py verify`) rc 0 | `round5-builder-legs.json`, `round5-builder-receipt-*.json` |
| Union proofs including `gptp_tables` | Collector and pieces self-tests on the real 63-suite, 80-unit inventory; the placement and collector controls above | `round5-gptp-tables-controls.json` |

One harness attempt is not evidence: the first runner-gate launch failed on the host before starting its container, because the launcher's interpreter had no PyYAML. It was rerun with the scratch interpreter that has it.

### Round 5 open risk: the merged dev workload moves the docs and elaboration projections

Not part of the assignment's re-projection, which covers the worker the added suite lands on, and not written into `CI_WORKFLOWS.md`, whose round-5 additions are limited to the merged suite's placement. Recorded here because the merge brings in #671's larger saved-state campaign, and it lengthens two gates that this PR's docs and elaboration workers carry.

| Step window | `7032bca5` (runs 38495894291, 38495894212) | `f6260253` (runs 38601263556, 38601263659) |
|---|---:|---:|
| docs-check job | 2039 s | 2682 s |
| End-station builder gates (docs) | 1065 s | 1400 s |
| Saved-state writer gate (docs) | 119 s | 410 s |
| elaborate job | 2144 s | 2447 s |
| Elaboration gates (builder) | 1441 s | 1763 s |

The documented formulas (`CI_WORKFLOWS.md:2688-2706`), with these figures (`round5-dev-workload.json`):

| Worker | Formula and basis | Projected s | Margin to 1620 s | Workflow with the 270 s tail |
|---|---|---:|---:|---:|
| `docs-gates-0` | `2682 - 1400 - 37 - 102 + 23.699 + 60` | 1227 | 393 | |
| `docs-gates-1` | larger builder figure + 120: local 1482.211 s at `e3d25d96` (docs bank) | 1602 | 18 | 1872 s, about 31.2 minutes |
| `docs-gates-1` | the hosted 1400 s + 120 instead | 1520 | 100 | 1790 s, about 29.8 minutes |
| `elaborate-gates-0` / `-1` | measured at `e3d25d96` by the round-4 method: legs run beside each other (1081.009 / 495.144 s), scaled by `1763 / 1433.969`, the unsharded command run alone | 1473 / 1353 | 147 / 267 | 1743 s, about 29.1 minutes |
| `elaborate-gates-0` / `-1` | the same scale on the lone run's per-gate split (972.509 / 460.324 s) | 1340 / 1310 | 280 / 310 | |

The lone unsharded elaboration run at `e3d25d96` took 1433.969 s (round 4: 1292.671 s). By gate, `test_baremetal_profile_contract` took 972.509 s (945.182), `test_nvm_firmware_shapes` 202.7 s (110.852), and the other 101 gates 257.6 s; the growth is mostly in leg 1. Peak 4,791,652,352 B, every memory event zero (`round5-dev-workload.json`).

Every worker stays within its own 60% bound, and elaboration stays within 30 minutes. The documentation workflow, by the method `CI_WORKFLOWS.md` already uses (the larger local builder figure), now projects about 31.2 minutes, above 30. This round changes neither the docs builder nor the elaboration partition, and `CI_WORKFLOWS.md` keeps its `7032bca5`-based docs and elaboration rows. Dividing the docs builder by measured legs, as elaboration's is, would be new work for the coordinating role to decide.

### Round 5 file map and closing record

| Commit | Files |
|---|---|
| `8db583050` (merge; parents `08adb21a`, `f6260253`) | Author resolutions: `.github/ci-templates/rtl.yml`, `scripts/ci_suite_workflows.py`, `scripts/suite_shards.py`, `docs/testing/CI_WORKFLOWS.md`; `.github/workflows/rtl.yml` regenerated (equal to the first parent). Dev's 53 other changed files merge without conflict and are attributable to the second parent. `git show --cc --name-only` also lists `scripts/ci_events.py` and `sw/builder/test_builder.py`, which differ from both parents only because both sides edited them and Git combined the edits without conflict |
| `e3d25d964` | `docs/testing/CI_WORKFLOWS.md` (Verilator projection rows and the worker-3 margin) |

Each commit has a one-line subject, no body and no trailer, with the configured identity.

CI assertion replacement: none by the author this round. `scripts/ci_events.py` changed only through the merge: dev's six-worker literals (canonical ownership arm `5)`, `--expect 6`, and its fixtures), which hold the template. The contract passes at 2,187 items and 5,212 arms.

`scripts/act_ci.py` is unchanged (SHA-256 `f968f67655ac386ea703248b724c3781b95ec379d3a5287b378e470df81f895c`), so no STOP was needed. No push, PR write, rebase or hardware access occurred, and no TAKEN comment was repeated. No test assertion, case, arm, timeout, firmware behaviour or linked image was changed by the author; the merge imports dev's published changes, including #671's firmware and test changes and #713's suite. Every round-5 container has exited. Scratch clones, logs over 200 KB and the item lists stay in scratch and are recorded by size and SHA-256.

REVIEW READY posted: https://github.com/kebag-logic/milan-fpga/issues/737#issuecomment-6187136845 (text in `ROUND5-REVIEW-READY.md`).
