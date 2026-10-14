[A614]

# Lane 737 handoff

Status: REVIEW READY for the fixes-only Round 2. Scoped item-4 measurements and final local checks pass. Both round-one reviews remain NEGATIVE; independent re-review and the coordinating full replay remain required.
Branch: `737-ci-30min`; final head: `2658a64c408bf87ae36574f36a6deeb34b2f297f`; resumed measurement source: `21bd10cec1a999791c9cd2c6d37c52372fb1504e`.
The required merge of dev `fa8209889411e8ca95757174c981f720dbcd95a2` is commit `abf7a923a`.
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
