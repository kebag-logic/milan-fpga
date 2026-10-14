[A614]

## Contents

- [Status](#status)
- [Linked Issue / roles](#linked-issue--roles)
- [Description](#description)
- [Authoritative references](#authoritative-references)
- [How to get into the same state](#how-to-get-into-the-same-state)
- [How to validate](#how-to-validate)
- [Known limitations / out of scope](#known-limitations--out-of-scope)
- [Definition of Done](#definition-of-done)
- [Round 2](#round-2)
- [Round 3](#round-3)

## Status

Round 3 fixes are complete on `737-ci-30min` -> `dev` at `84ee9ea1`. The full
docs-check (40 steps) and rtl-fast (20 steps, twelve jobs) step sets pass on that
committed head. Both round-two reviews are NEGATIVE; the corrected head
requires independent review and coordinating replay. No push occurred.

| Workflow | Measured baseline at `7032bca5` | Earlier warm projection |
|---|---:|---|
| docs | about 34m00s | about 29.6 minutes with aggregate, collection and watcher tail |
| elaborate | 35m44s | about 30 minutes including collection |
| rtl-fast | 19m03s | about 22 minutes including collection |
| rtl-full | 77m29s | continuous media-clock worker alone projects at 33m52s |

The projections are not hosted after-times. They also require the round-two
watcher tail: up to one 120-second polling interval, then the terminal guard.
Its actual duration is unmeasured. The accepted continuous-history exception
remains above thirty minutes. The coordinating role owns complete hosted timings.

## Linked Issue / roles

Relates to #737

Executor: `[A614]`
Internal cleared-context reviewer: `[R636]`
External reviewer: `[R637]`

## Description

Six long suites now expose cases from their own inventories. Independent workers
execute those cases, and union jobs require each case exactly once. The protected
aggregate also verifies the original physical-suite logs. Documentation and
elaboration have three and two source-derived workers respectively, with their
protected aggregates retained. Existing test assertions and suite deadlines are preserved.

The local dispatcher admits up to four jobs across workflows and nested matrices.
Each container keeps an explicitly booked sixteen-CPU range; the named fallback
uses twelve CPUs. Dependency-ready jobs start without an unrelated stage barrier.
First failure closes admission and cancels running work. Hosted cancellation also
covers collectors and watcher tails, while preserving the fork write restriction.

Each job derives its build budget from CPU affinity. Campaigns retain four workers;
capture divides its compiler budget across those workers. Containers retain an
8 GiB cap, with 36 GiB for an isolated slot. Scoped measurements below establish
workload peaks; complete replay evidence remains separate.

Caches bind exact versions, source identities and recipes without Scala or pip
prefix fallback. Both execution paths collect the canonical seven-section manifest
from actual observations. Comparison refuses changed or incomplete evidence.
Authentication and evaluated skip proofs remain follow-up work.

## Authoritative references

- Issue #737 assignment 6160775078 and its driver, topology and fail-fast rulings.
- Round-three fixes-only ruling 6176299708 and reviews 6175565890 / 6176284934.
- Round-two fixes-only ruling 6169768594 and additions 6169805715.
- Census regression 6170460727 and measurement authorization 6172868895.
- CPU rules 6166855177, 6167284204 and correction 6167288337.
- [Workflow policy](docs/testing/CI_WORKFLOWS.md).
- [Signature contract](docs/testing/CI_SIGNATURE.md).
- [Verification requirements](REQUIREMENTS.md#8-verification-and-release-acceptance).
- [Contribution and merge rules](CONTRIBUTING.md).

## How to get into the same state

Use CPython 3.12.3 and the workflow's pinned dependencies, including Verilator
5.050. Verify each initialized submodule's root and own origin before operating
inside it. Keep scratch and build products outside the candidate checkout.

```sh
git switch 737-ci-30min
git submodule update --init third_party/verilog-axis protocol-processor gptp-processor third_party/tsn-c-stack third_party/lwSRP
python3 --version
verilator --version
```

## How to validate

Run each command directly and retain its exit status. The handoff indexes the
round-two commands, logs, comparisons and planted controls.

```sh
python3 scripts/ci_gate_workflows.py --check
python3 scripts/ci_events.py --check
python3 scripts/ci_events.py --selftest
python3 scripts/ci_gate_workflows_selftest.py
python3 scripts/ci_suite_pieces_selftest.py
python3 scripts/ci_suite_collect_selftest.py
python3 scripts/ci_case_receipts_selftest.py
python3 scripts/ci_fail_fast_selftest.py
python3 scripts/ci_manifest_selftest.py
python3 scripts/ci_runtime_evidence_selftest.py
python3 scripts/generate_ci_evidence_pins.py --check
python3 scripts/suite_shards.py --selftest
scripts/act_slot_proof.sh --selftest
python3 scripts/check_py_idiom.py
python3 scripts/check_hygiene.py
python3 scripts/check_baremetal_only.py --check
python3 scripts/docs_check.py
python3 scripts/check_doc_style.py
python3 scripts/check_doc_paths.py
python3 scripts/gen_toc.py --check
python3 scripts/check_em_dash.py --base fa820988
```

For resource reproduction, use one 8 GiB container at a time, at sixteen and then
twelve CPUs. Apply the generated CPU-budget step. Start datapath builds with empty
object directories. Run the unchanged workloads:

```sh
make -C tb/verilator/milan_dp build-nxn8
make -C tb/verilator/milan_dp exec-nxn8
VERILATOR_JOBS=$(( CI_BUILD_JOBS / CI_CAMPAIGN_JOBS )) python3 tb/verilator/capture_coherence/mutants.py --whole-suite --jobs "$CI_CAMPAIGN_JOBS"
python3 sw/builder/test_builder.py --require-elaboration --require-rv32
scripts/run_litex_sims.sh --selftest
scripts/run_litex_sims.sh "$LITEX_LOGS"
```

Read each container's `memory.peak` and `memory.events` before exit. Retain Docker's
actual limits, CPU set and final state. The receipts also identify the image,
compiler budget, command script and oversized artifacts by size and SHA-256.

Run the candidate runner's offline self-test only inside a disposable job boundary:

```sh
python3 -I scripts/act_ci.py --selftest --worktree "$PWD"
```

The coordinating role performs the full replay through the separately trusted runner:

```sh
python3 -I "$TRUSTED_RUNNER" --pr 739 --cpu-ranges "$BOOKED_CPU_RANGES" --evidence-directory "$EVIDENCE_DIR"
```

Expected: required commands return zero, planted defects are refused, unions are
complete, and incomplete manifests cannot compare equal. A local measurement is
not a hosted timing result or a signed build verdict.

## Known limitations / out of scope

- The coordinating role still owns publication, runner repinning, full candidate
  replay, hosted timings and live cancellation evidence.
- The media-clock carried history remains intact under the accepted exception.
- The public-head case comparisons use `cf9c9366`. They do not claim unchanged
  product inputs after the required dev merge; the merged candidate needs replay.
- The builder reports two existing NOT RUN arms: an inert `MAKEFLAGS += -e`
  control on this Make version, and the unavailable physical calibration report.
  Required RV32 and elaboration instruments run; no physical evidence is claimed.
- Prebuilt-image adoption, RTL trigger changes, signing and conditional-skip
  authentication belong to a follow-up PR under the fixes-only ruling.
- Author corrections change no firmware behavior, linked image or test predicate.
  The required merge imports the separately published dev changes.

## Definition of Done

- [ ] Linked Issue acceptance criteria are satisfied
- [x] New or changed behavior has self-checking tests
- [ ] Required local verification bar passes
- [ ] Self-test evidence is posted in a PR comment
- [x] No undocumented requirement or interface change remains
- [ ] Internal cleared-context review is positive
- [ ] External review is positive
- [ ] Blocking and major findings are fixed and re-reviewed
- [ ] No review round remains in flight
- [ ] Candidate merge result is validated per [CONTRIBUTING.md](CONTRIBUTING.md)
- [x] Documentation is updated where needed
- [ ] Post-merge containment will be checked before the Issue moves to Done

## Round 2

The required merge of dev `fa820988` is `abf7a923a`. Its conflicting control count
was regenerated through the census: 161 controls and four figure mutations pass.
Subsequent corrections address nested compiler budgets, hosted inventory
prerequisites, fixture identity, skipped matrices, observer retries, late
cancellation, worker headroom, cache documentation and dependency-ready dispatch.

The workflow contract passes 2,186 items and 5,093 controls. Every worker retains
its own 60% headroom rule; borrowed-limit and disabled-1620-second mutations fail.
The dispatcher passes twenty race repetitions and upstream controls. Two actual
scheduling fixtures start a ready dependent before an unrelated long job finishes;
the previous dispatcher fails them. One fixture also reuses job IDs across workflows.

All six public-head full/sharded comparisons pass: 154 inventory units across
23 legs, with equal outcomes, return codes and checked-output digests. Every suite
refuses a dropped case and detects an altered observation. The six production CLI
comparisons return zero.

| Measured workload | Sixteen-CPU peak, GiB | Twelve-CPU peak, GiB |
|---|---:|---:|
| Publication census, four workers | 5.458 | 4.844 |
| Heaviest synthesis shard | 3.488 | 3.158 |
| Firmware normal phase, required RV32 checks | 1.272 | 1.279 |
| Eight-stream datapath build and simulation | 3.119 | 2.512 |
| Full capture campaign, four builds | 5.632 | 4.696 |
| Builder with required RV32 and elaboration | 3.282 | 2.955 |
| Standalone elaboration simulations | 3.489 | 3.077 |

Every measurement returns zero with every memory-event counter zero.
Datapath passes 3,751 checks at each width; capture passes all 32 at each width.
Sampling observes four capture builds and 16/12 compiler processes. Census passes
234 normal checks, 120 planted arms and 31 rule removals at each width, using the
emitted four-worker ceiling that prevents the reported sixteen-worker exhaustion.

The prior STOP is answered by ruling 6172868895. All eight resumed workloads
run sequentially in one 8 GiB container at a time. LiteX passes seven simulations
and ten runner controls at each width, with no skips or timeouts. Builder and
standalone runs execute the JVM with empty CPU metadata and cached dependencies.
Twelve CPUs measures width within the assigned die, not aligned fallback admission.

The largest measured peak is capture at 6047100928 bytes (5.632 GiB). Keeping the
8 GiB cap leaves 2542833664 bytes (2.368 GiB), 42.05% above that peak. Four caps
plus 4 GiB overhead equal the 36 GiB slot cap: `floor((36 - 4) / 8) = 4` jobs.
Four measured maxima plus overhead total 26.527 GiB. This sum is not an observed
concurrent slot peak; complete replay remains the coordinating check.

The receipts retain cgroup peaks/events, command scripts, source/image identities
and artifact digests. The sixteen-CPU builder container was removed before its
configuration export; its retained launch command supplies cap/image settings,
while completed state and cgroup measurements were captured before removal.
Other resumed receipts include directly inspected Docker limits. Superseded
environment refusals are retained separately from passing evidence.

The resumed edits record these measurements and correct a stale memory comment.
The runner AST is unchanged from the measurement head. The complete offline runner
self-test passes inside a disposable full CI container with CPython 3.12.3 and no
network or Docker socket. Documentation, Python idiom, evidence-helper pins,
hygiene and committed-head punctuation checks pass.

## Round 3

Fixes under ruling 6176299708, from round-two head `2658a64c` to `84ee9ea1`.
Both round-two reviews are NEGATIVE; no review coverage is claimed.

| Item | Change | Evidence |
|---|---|---|
| 1. R637-2-F2 | Every inventory reader, including the collector and the docs scheduling controls, gets pinned dependency preparation; the generator refuses an unprepared reader | Removing preparation from each of the thirteen readers fails; a fresh checkout without submodules prepares and collects all six unions (19/31/31/66/3/4 legs) |
| 2. R637-2-F1 | Raw skipped-matrix names from committed definitions flow through graph, collector and watcher | The retained hosted job shape yields skipped legs, an incomplete manifest, no success and no cancellation; unknown names, invalid raw states and raw/expanded overlap are refused in both orders, before failure selection |
| 3. R637-2-F3, R636-2-S5(b) | Watcher and collector observer-only failures end without a failed conclusion, emit `observer_only_error`, mark the manifest incomplete and grant no cancellation | 403, 429, 502, timeout and retry exhaustion through the production entry point and generated graph; virtual-clock waits of 360/480 s exceed the old allowance; the 15-minute collector limit exceeds its 600-second read budget; genuine collection, tail and upload failures still cancel |
| 4. R636-2-F1 | Both contract self-tests move to source-derived worker `docs-gates-2`; each generated arm regenerates only its mutated workflow; Yosys compilation moves to prerequisite `yosys-tool` | Worker table below; no arm removed, no timeout raised |
| 5. R636-2-F2 | Source compilation uses `CI_TOOL_BUILD_JOBS=min(available CPUs, 8)` | Source-build table below |
| 6. R636-2-S1, S2, S4 | Self-tests plant the drivers' real `failed` outcome, compare skipped-step manifests and combine contradictory scopes | Removing each production guard makes its self-test fail |
| 7. R636-2-S3, S5(a) | None | Hosted concurrent job limit and cache-conditional manifest steps go to the #495 checklist |

Worker projections from the `7032bca5` hosted baseline plus measured gate times:

| Worker | Projected s | Own 60% bound s | Margin s |
|---|---:|---:|---:|
| `docs-gates-0` | 922 | 1620 | 698 |
| `docs-gates-1` | 1506 | 1620 | 114 |
| `docs-gates-2` | 553 | 1620 | 1067 |
| `elaborate-gates-0` | 1561 | 1620 | 59 |
| `elaborate-gates-1` | 713 | 1620 | 907 |
| `yosys-tool`, cold | 720 | 1044 | 324 |
| `yosys-shards 0/4` | 554 | 1044 | 490 |
| slowest regular Verilator shard | 1605 | 1620 | 15 |
| media-clock exception | 2032 | 2160 | 128 |

The docs workflow projects at 1776 seconds (29.6 minutes) with aggregate,
collector, one watcher interval and tail. The CI-event self-test measured
316.686 seconds for 5,206 arms; at this head it passes 5,209 arms, and its whole
contract step took 201.196 and 225.451 seconds in the two committed-head banks.
Projections keep 316.686. The isolated runner contract step, both invocations,
takes 101.53 to 113.654 seconds. In the docs bank the builder step took 1411 to
1416 seconds with one simulation child, sharing its CPUs with the rtl-fast bank.
`docs-gates-1` keeps the 1386-second shipping-width figure. With the contended
figures it would be 1531 to 1536 seconds (within 1620), and the workflow 1802 to
1806 seconds, up to 6 seconds over thirty minutes. Hosted readback decides; the hosted builder window
was 1065 seconds. The Yosys cold projection uses the review's 600-second estimate;
the bounded sixteen-CPU local build took 360.05 seconds.

Source builds, one 8 GiB container at a time in the shipping image:

| Source tool | CPUs | Compilers | Peak bytes | Reserve below cap |
|---|---:|---:|---:|---:|
| Verilator | 16 | 8 | 4811259904 | 43.99% |
| Verilator | 12 | 8 | 4793225216 | 44.2% |
| Yosys | 16 | 8 | 5264482304 | 38.713% |
| Yosys | 12 | 8 | 5117616128 | 40.423% |

Each bounded build returns zero with every memory-event counter zero.
Unrestricted builds were rejected: Yosys at sixteen compilers reached the cap with
174 max events; twelve compilers kept 20.65%; Verilator at sixteen kept 19.07%.
The largest accepted class remains capture at 6047100928 bytes, leaving
2542833664 bytes, 29.60% of the cap. Four caps plus 4 GiB overhead stay at
36 GiB, and admission stays at four jobs.

Continued-session corrections:

- The committed-head docs bank failed the bare-metal scope gate on three
  host-OS words that this lane added in its dispatcher and cache commits. Two
  prose lines are reworded. `scripts/build_ci_act.py` now fills the Go archive's
  OS segment from `sys.platform`; the pinned digest still admits one archive. The
  gate is unchanged. A rebuilt dispatcher has the same binary digest as round two.
- `docs/testing/CI_WORKFLOWS.md` cited the rejected unrestricted Yosys build and
  a stale contract arm count; both now state the accepted figures.

Committed-head validation runs the exact source step bodies in the shipping job
image, one 8 GiB container per bank, without network. At `84ee9ea1`:
docs-check passes all 40 steps, rtl-fast passes all 20 steps across its twelve
jobs with scope `rtl=true`, docs-check-no-git passes, and the isolated runner
contract self-test passes with a read-only candidate mount and no Docker socket.
Sampled container peaks were 3.25 GiB (docs) and 5.67 GiB (rtl-fast) under the
8 GiB cap. Setup steps come from the image; the source Yosys build is sized
separately above. These are local gate results, not hosted timings or a replay.
Runner SHA-256 for repinning: `f968f67655ac386ea703248b724c3781b95ec379d3a5287b378e470df81f895c`.
