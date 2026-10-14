[A614]

# Lane 737 handoff

Status: REVIEW READY for the authorized round-one scope. Local gates pass; hosted timing, the full trusted replay and independent reviews remain with the coordinating and review roles.
Branch: `737-ci-30min`; base `fa7347fc59173f90e4feec2df207692e6e6e72ec`.
Current committed head: `cf9c936697a06e44c41681bcc12dc612a3242eb2`; tree `a5eb619c5c9ead508e7189fd77527d84d2c4fdda`.
All sixteen selected workers, six real unions, the physical collector and original tally pass: 2,187,186 checks, zero in-suite failures, across all 62 physical suite logs.
Origin was verified as `https://github.com/kebag-logic/milan-fpga.git`.
This resume began after the planned power-off at `776ed299ba6318ae1e4d154cbe856273fdd5e7e6`, with a clean tree.
Executor: [A614]. Independent reviewers: [R636] and [R637].
No push, PR operation, merge, rebase, sub-agent or hardware access occurred.
No new TAKEN comment was posted. The preceding record is retained as HANDOFF-history.md;
its earlier pending and STOP descriptions are historical, not the current status.

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
| elaborate | 115631440899 | 35m44s | Protected union: under 1 minute; workers approximately 26 and 12 minutes |

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
