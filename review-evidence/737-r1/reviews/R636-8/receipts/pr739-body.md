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
- [Round 4](#round-4)
- [Round 5](#round-5)
- [Round 6](#round-6)
- [Round 7](#round-7)

## Status

Round 7 is complete at `fe2e2a54` on `737-ci-30min` -> `dev`, from `47fd0d3c`.
It fixes the runner self-test on hosts with fewer than 64 CPUs: the
main-entry probe now patches the CPU count as the other main-path probes
do. Only that self-test function of `scripts/act_ci.py` changes, under the
round-7 decision; its SHA-256 is now
`7ff18c6a89aeb40c54d44411ffc6ff766fe6aa0f29baf595ba1e2aa833a446fd`, for
repinning after review. A committed control runs the runner self-test at a
forced count of 4. The author does not push.

| Workflow | Measured baseline at `7032bca5` | Hosted at dev `f6260253` | Projection at this head |
|---|---:|---:|---|
| docs | about 34m00s | 44m42s, one job | about 27.75 minutes (1665 s), 135 s inside 30; slowest worker `docs-gates-0`, 1395 s |
| elaborate | 35m44s | 40m47s, one job | about 29.08 minutes (1745 s), 55 s inside 30; slowest worker `elaborate-gates-0`, 1475 s |
| rtl-fast | 19m03s | not re-measured | about 22 minutes including collection; not re-projected |
| rtl-full | 77m29s | not re-measured | unchanged; worker 3 projects at 1544 seconds; the continuous media-clock worker alone at 33m52s |

The projections are not hosted after-times. They include the watcher tail: up to
one 120-second polling interval, then the terminal guard, whose actual duration
is unmeasured. The accepted continuous-history exception remains above thirty
minutes. The coordinating role owns complete hosted timings.

Round 6 status (historical): round 6 was complete at `47fd0d3c`, from
`e3d25d96`. It divides the docs builder gate into the measured legs that elaboration
already uses: leg 0 on `docs-gates-1`, leg 1 beside the contract self-tests on
`docs-gates-2`. The union judges the requirement flags its template command
carries, so docs judges `--require-rv32` alone. The docs and elaboration
projections now use the merged-head inputs. A committed self-check pins the
generated Verilator graph, and the test pages describe the sixteen hosted
workers. `scripts/act_ci.py` is unchanged. The coordinating role published this head.

Round 5 status (historical): round 5 was complete at `e3d25d96`, from
`08adb21a`. It merged dev `f6260253` with merge commit `8db58305` and
re-projected the Verilator workers. The coordinating role published this head.

Round 4 status (historical): round 4 was complete at `08adb21a`, from
`84ee9ea1`; both round-4 reviews are POSITIVE there. The builder gate runs in
two measured legs, and its requirements are judged on their union. The
coordinating role published this head.

Round 3 status (historical): round 3 fixes were complete at `84ee9ea1`. The full
docs-check (40 steps) and rtl-fast (20 steps, twelve jobs) step sets passed on that
committed head. Both round-two reviews were NEGATIVE; the corrected head
required independent review and coordinating replay. The coordinating role published this head.

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
- Round-five merge ruling 6184143571 and round-four reviews 6183672250 / 6184124102.
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
python3 scripts/check_em_dash.py --base f6260253
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
  The required merges import the separately published dev changes.
- The merged dev workload lengthens the docs builder and saved-state writer
  gates and the elaboration builder. Round 6 divides the docs builder into the
  two measured legs and re-projects both workflows from the merged-head inputs:
  docs 1665 s, elaboration 1745 s.

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

## Round 4

Fixes under ruling 6180908502, from `84ee9ea1` to `08adb21a`. R637-3 is POSITIVE;
R636-3 is NEGATIVE for one MINOR. No review coverage is claimed.

| Item | Change | Evidence |
|---|---|---|
| 1. R636-3-F1 | A collector control lets `runs/<id>` recover on its third read while the jobs page never recovers, through the production entry point | Collection stops at 480 s, within the 600-second shared budget; the same reads without a shared deadline take 960 s. Removing the shared budget makes the self-test fail |
| S1 | Each of the thirteen inventory-reader jobs gets a planted `if:` and a planted `continue-on-error` preparation | All 26 are refused; accepting a conditional preparation makes the self-test fail |
| S2 | One classifier serves the retry loop, the watcher and the collector. Observer-only stays 403, 429, 5xx, timeouts and exhausted transport retries; 400, 401 and 404 are genuine failures | Client errors make one request, write no observer output and fail the job, so cancellation still follows. Six mutations across both sides each fail their self-test |
| S3 | `CI_WORKFLOWS.md` records the elaboration projection from hosted run `38495894212`; the builder gate runs in two measured legs (below) | Worker zero `2144 - 593 - 3 - 1441 + 1146 + 60 = 1313` s; the workflow is 1583 s (26.4 minutes). Undivided it was 1878 s (31.3 minutes) |
| S4 | The field-oracle `cmake --build --parallel` uses `CI_TOOL_BUILD_JOBS`; the contract pins the bounded line | The unbounded form fails the contract check. One execution: rc 0, 17.4 s, peak 0.84 GB, zero memory events |
| R1 | `CI_WORKFLOWS.md` names the Yosys and Verilator source builds in the measured bound | Exact text from the review |
| R2 | This body states that the coordinating role publishes the head | Status above |

### Round 4 S3: the builder gate in measured legs

Under the answer to the round-4 STOP, only the builder driver's entry point
changed. `sw/builder/test_builder.py --list` prints the ordered inventory of 103
gates. `--gates a,b` runs that subsequence and refuses unknown, repeated or
out-of-order names before any gate runs. `--receipt` records each gate's verdict
and the NOT RUN rows it added. The run list stays one literal tuple in the one
`for fn` loop that gate `test_rom_clock_skip_reaches_the_ledger` reads. With no
option every gate runs as before. No gate function, assertion, fixture, timeout,
NOT RUN arm or firmware behaviour changed.

`scripts/ci_builder_legs.py` holds the measured boundary. Leg 0 is
`test_baremetal_profile_contract` alone (945.2 of 1292.7 s, measured); leg 1 is
the other 102 gates in inventory order. The generator divides the template's one
command into `gate_14_0` on worker 0 and `gate_14_1` on worker 1, before the
LiteX aggregate. Each runs the template command after `--`, adding only the
selection and the receipt, bound to the head and tree. Two workers remain.

`--require-elaboration` and `--require-rv32` are judged on the union, never per
leg. The leg runner names the gates each requirement judges: the 15 gates that
consult the LiteX interpreter, and the bare-metal profile gate, the only reader
of `--require-rv32`. The self-test checks those names against the driver source.
The `elaborate` aggregate refuses unless every gate ran exactly once in its
measured leg and passed, and each named gate is in the fresh inventory and ran
in a leg carrying its flag. Then the driver's own `--require-elaboration` verdict
is applied to the union NOT RUN ledger. A skipped division may leave no builder
receipt.

| Leg | Worker | Measured (shared CPUs) | Scaled to hosted | Worker projection | Own bound |
|---|---|---:|---:|---:|---:|
| 0: `test_baremetal_profile_contract` | `elaborate-gates-0` | 1028.3 s | 1146 s | 1313 s | 1620 s |
| 1: the other 102 gates | `elaborate-gates-1` | 367.3 s | 409 s | 1172 s | 1620 s |

Scaling is `1441 / 1292.671`, from the hosted gate window and the unsharded
command measured alone. The legs ran beside other builder runs, which only
lengthens them; the uncontended split gives 1054 and 387 s.

Evidence in the shipping image (8 GiB, 16 CPUs, no network):

- **Equality.** The unsharded run and the two legs give equal per-gate verdicts
  and an equal NOT RUN ledger. The ledger is `[gate 1b]` MAKEFLAGS from leg 0
  and `[gate 11]` calibration report from leg 1. The union check passes, and
  the production aggregate accepts the real receipts. Printed output is equal
  too: 96 gates byte-identical and 7 identical once per-run temporary paths and
  elapsed seconds are masked.
- **Planted controls.** A reworded boot-order claim fails the unsharded run and
  leg 0 with the same assertion; leg 1 passes. A removed FPU refusal fails the
  unsharded run and leg 1 at `test_soc_option_refusals`.
- **Vacuous leg.** Leg 1 run without `--require-elaboration` passes by itself.
  The aggregate then refuses the union, naming all 15 elaboration gates.
- **Synthetic controls.** The self-test refuses, by name, an elaboration gate
  that is deleted, loses its leg, is skipped in its leg, is moved to a leg that
  never ran, or runs without its flag. It does the same for the RV32 gate
  without `--require-rv32`, and for a toolchain skip under a passing leg verdict.
- **Mutations.** Seven mutations each fail the scheduling self-test, including
  deleting `test_every_recipe_elaborates` from the real driver run list.

Executing the legs found two defects before any hosted run. The leg runner's
parser swallowed `--receipt`; the self-test now parses every generated leg body
through the production parser. A `gates = (...)` tuple broke the ledger gate
that reads the run list; the literal tuple is back in the loop.

Validation at `08adb21a`, in fresh clones in the shipping image, one 8 GiB
container without network:

- Docs-check: all 40 non-setup steps pass, including the builder gate on its
  default path (103 gates, no subset, 1363 s), the CI-event contract (5,212
  arms) and the scheduling and evidence controls with the builder-leg controls.
- docs-check-no-git passes.
- The runner contract gate passes both invocations (104.5 s) with a read-only
  candidate and no Docker socket. The runner digest is unchanged:
  `f968f67655ac386ea703248b724c3781b95ec379d3a5287b378e470df81f895c`.
- Elaboration legs and unsharded reference at this head: all rc 0. The union
  check against the reference passes, and its per-gate verdict digest is
  identical to the earlier run. The production aggregate accepts the receipts.
- rtl-fast: no step body changed. `pp_srcs.py --check --selftest` and the scope
  self-test, which read every tracked file, pass.

No test assertion, case, arm, timeout, firmware behaviour or linked image changed.

## Round 5

Merge of current dev under ruling 6184143571, from `08adb21a` to `e3d25d96`.
Both round-4 reviews are POSITIVE at `08adb21a`. No review coverage is claimed.

| Item | Change | Evidence |
|---|---|---|
| 1. Merge `f6260253` | `8db58305`, a merge commit with parents `08adb21a` and `f6260253`. Git reported conflicts in exactly `.github/workflows/rtl.yml`, `docs/testing/CI_WORKFLOWS.md` and `scripts/suite_shards.py` | Generated workflows come from the generator only; its freshness check passes, and they are byte-identical to `08adb21a`'s |
| 1. Sharding | `gptp_tables` enters the driver-derived inventory and balance whole, as every unsplit suite does: 63 default suites, 80 scheduled units. The physical-suite collector and the unchanged tally require its log from its owner | Planted controls below |
| 1. Template and generator | Dev's six-worker edits (matrix, shard 5/6 `milan_dp` arm, `--expect 6`) go into `.github/ci-templates/rtl.yml` by a clean three-way merge. The generator now derives the arm and the expectation from the template's own worker count and refuses a template whose arm or expectation does not match | The round-4 literal generator on this template would emit a shard-5 `milan_dp` arm and `--expect 6` into the sixteen-worker graph, and the contract check would not notice. With the derivation, a missing arm, a stale arm index or a mismatched expectation each stop generation |
| 1. Documentation | `CI_WORKFLOWS.md` keeps this branch's sixteen-worker text, dev's #713 facts (the provisional 1800-second figure, the sixth worker at 115 seconds, the refresh rule) and the suite's placement | Docs, style, paths, TOC and em-dash gates pass |
| 2. Re-projection | `e3d25d96` updates the sixteen Verilator rows of the projection table | Worker 3 carries `gptp_tables` at 1544 s: 76 s inside its 1620-second bound and 256 s inside 30 minutes before downstream collection |
| 3. Verification | Shipping image, fresh clones of `e3d25d96`, one 8 GiB container at a time, 16 CPUs, no network | Below |

The suite's figure is a hosted window, not the provisional `suite_timeout`
value. Run 38538854504 (PR #713, all workers passed) measured 474 seconds. Run
38601263345 (dev `f6260253`; its worker 0/6 passed all eight suites) measured
568 seconds. The table takes 568. At the provisional 1800 seconds the selector
would put the suite on worker 0 at 1922 seconds, over both limits.

| Worker | At `08adb21a` | At `e3d25d96` | Own 60% bound | Margin |
|---|---:|---:|---:|---:|
| 0/16 | 1605 | 1605 | 1620 | 15 |
| 1/16 | 1495 | 1541 | 1620 | 79 |
| 2/16 | 1572 | 1572 | 1620 | 48 |
| 3/16, with `gptp_tables` | 1494 | 1544 | 1620 | 76 |
| 4/16 to 14/16 | 1491 to 1521 | 1538 to 1543 | 1620 | 77 to 82 |
| 15/16, media-clock exception | 2032 | 2032 | 2160 | 128 |

Longest-first placement moves 56 other units between workers. Owners are
derived at run time, so no list is edited. Worker 3 runs `maap__2`,
`milan_dp__0`, `chmap_capture`, `gptp_tables` and `tdm_render`. With the
270-second tail used for docs and elaboration, a path through worker 3 alone
reaches about 30.2 minutes. Worker 0 and the media-clock exception still set
the workflow's end, and neither changed.

Planted controls for the suite, on the real inventory:

- Removing its duration is refused by the headroom gate and by sharded
  selection. The provisional 1800-second figure is refused at 1922 seconds.
- The production collector releases its log to the unchanged tally. It refuses
  the log when it is missing from worker 3, moved to worker 0, or duplicated.
- The unchanged tally refuses the complete set without it.

Verification at `e3d25d96`:

- Docs-check: all 40 steps and `wire-accountability` pass. That includes the
  builder on its default path (1482 s), the CI-event contract (2,187 items,
  5,212 arms) and the scheduling and union controls (63 parents, 80 units).
  Peak 4.58 GB, no memory events.
- docs-check-no-git passes.
- The runner contract gate passes both invocations (102 s) with a read-only
  candidate and no Docker socket. The runner digest is unchanged:
  `f968f67655ac386ea703248b724c3781b95ec379d3a5287b378e470df81f895c`.
- The generated worker 3/16 runs its budget, tree record, Verilator proof,
  ownership proof and shard steps. All five units pass, `gptp_tables` among
  them, with 5,518 checks. Its shard step takes 1121 s; peak 3.92 GB, no memory
  events.
- Dev changed the builder driver that elaboration divides, so the legs ran
  again. The unsharded reference, leg 0 and leg 1 all pass. Their union check
  passes, with a per-gate verdict digest identical to round 4's, and the
  production aggregate accepts the receipts.
- rtl-fast: all 20 steps across its twelve jobs pass with scope `rtl=true`.
  The image provides the pinned Yosys, so the two source builds are skipped.
  Peak 6.16 GB, no memory events.
- Host gates at the committed head: the generator freshness check, the
  CI-event contract, every scheduling, union, fail-fast, evidence, manifest and
  cache self-test, plus the docs, hygiene and em-dash gates (against `f6260253`
  and `08adb21a`). All return zero.

Open risk for the coordinating role. The merged #671 workload lengthens gates
that this PR's docs and elaboration workers carry. At dev `f6260253` the hosted
docs builder took 1400 s (1065 s at `7032bca5`), the saved-state writer gate
410 s (119 s), and the elaboration builder 1763 s (1441 s). The documented
method uses the larger builder figure. With the local 1482 s it puts
`docs-gates-1` at 1602 s, 18 s inside its bound, and the docs workflow at about
31.2 minutes. With the hosted figure the workflow is about 29.8 minutes.
Elaboration was re-measured at this head by the round-4 method. The legs and
the unsharded reference pass, and their union equals the unsharded run. The
command alone took 1434 s, and the legs scale to workers of 1473 s and 1353 s.
That puts the workflow at about 29.1 minutes. Every worker stays inside its own
bound. This round does not divide the docs builder.

No test assertion, case, arm, timeout, firmware behaviour or linked image was
changed by this round's author changes. The merge imports dev's published changes.

## Round 6

Fixes for R636-5 and R637-5 under the round-6 ruling, from `e3d25d96` to
`47fd0d3c`. Both reviews were NEGATIVE for MINOR findings only. No review
coverage is claimed.

| Item | Change | Evidence |
|---|---|---|
| 1. Docs builder in measured legs (R636-5-F1 = R637-5-F1) | `b06211642`: the generator divides the docs `End-station builder gates` step as it divides elaboration's. Leg 0 (`test_baremetal_profile_contract`) runs on `docs-gates-1`, leg 1 (the other 102 gates) on `docs-gates-2` beside the contract self-tests; the step's `pip install` line stays ahead of the leg runner. The template is unchanged | Equality, aggregate replay and planted controls below |
| 1. Union-level requirements | The union judges the flags the template command carries: docs `--require-rv32` alone, elaboration both. Every leg must carry exactly its command's flags. The driver's elaboration verdict applies to the union ledger only under `--require-elaboration`, as the driver applies it per process. `ci_builder_legs.py union` takes `--workflow` | Self-test controls and a 6/6 mutation battery |
| 1. Projections (`47fd0d3c5`) | Docs and elaboration rows and both workflow projections from the hosted `f6260253` windows (runs 38601263556, 38601263659), the round-5 local measurements and this round's docs-leg measurement, taking the larger figure where they differ and rounding up | Table below |
| 1. Arm count | 5,212 at `e3d25d96`; leg 1's step on `docs-gates-2` adds three generated-graph arms, so 5,215 now | CI-event self-test at this head: 2,187 items, 5,215 arms |
| 2. Generator self-check (R637-5-F2) | `26838a11c`: the gate-workflow self-test requires the generated sixteen-worker matrix, no `= milan_dp ;;` arm in the generated ownership step and exactly `--expect 16`; three planted templates (arm index, `--expect`, total) must each stop generation | Reverting `ci_suite_workflows.py` to `08adb21a` and regenerating passes the freshness and contract checks but fails the committed self-test |
| 3. Test pages (R636-5-F2) | `e958bdde8`: `TESTING.md` describes the sixteen `--ci-pieces` workers, `milan_dp` in four legs, `milan_dp_mclk__0` alone on the last worker and the template's six workers as generator input only, with `scripts/run_all_suites.sh --ci-pieces --shard 0/16 --list`. The `milan_dp` README and `RUNNING_TESTS.md` follow | A repository-wide search for shard denominators `/5` and `/6` leaves only named historical runs and the template's arm |
| 4. Residue | `3c5fc8361`: R636-5-R1 and R637-5-R2 with their exact texts; R637-5-R1 in this body's round-5 status | Exact texts in the commits |

Also changed, beyond the named lines: `RUNNING_TESTS.md` said the default
selection has 60 suites; the driver lists 63. `726_STREAM_COUNTERS.md` said
hosted shard 4/5 retains the stream-counter results; they now reach the
`milan_dp.log` that the `milan_dp` case union assembles. The second was needed
for the denominator search to come back clean.

Docs builder equality at `26838a11` (the shipping image, 8 GiB, 16 CPUs, no
network):

| Run | rc | Seconds | Verdict | Peak memory |
|---|---|---:|---|---:|
| Unsharded reference, alone | 0 | 1443.720 | `ALL GATES PASS EXCEPT 2 NOT RUN` | 4.81 GB |
| Leg 0, the generated `docs-gates-1` step | 0 | 1098.130 | `SUBSET: 1 of 103`, 1 NOT RUN | 0.74 GB |
| Leg 1, the generated `docs-gates-2` step, beside leg 0 | 0 | 506.263 | `SUBSET: 102 of 103`, 1 NOT RUN | 5.60 GB |

- `union --workflow docs --reference` passes: 103 gates exactly once,
  requirements judged on the union, equal to the unsharded run. The per-gate
  verdict digest, `47dc3c6a`, is the same as the elaboration unions of rounds 4
  and 5.
- The production docs aggregate accepts the real receipts: 43 source gates
  exactly once.
- No run recorded a memory event.
- The lone run measured the split: `test_baremetal_profile_contract` 1006 s,
  the other 102 gates 435 s. So the existing partition fits the docs command.
- Printed output matches for 102 of 103 gates, 4 of them after masking
  temporary paths and durations. In `test_nvm_firmware_shapes`, every line
  reads `self-test OK`, but the number of findings each self-test catches
  differs. Its fault search runs in a thread pool and stops at the first
  named finding, so that number depends on thread timing. Two unsharded runs
  differ in the same way.

Planted controls, each committed only inside a disposable clone:

| Control | Owning leg | Unsharded | Owning leg | Other leg |
|---|---|---|---|---|
| Boot-order claim reworded in `docs/integration/BAREMETAL_FIRMWARE.md` | 0 | rc 1, "bare-metal boot contract lost" | rc 1, same assertion | rc 0 |
| FPU refusal removed from `sw/litex/milan_soc.py` | 1 | rc 1 at `test_soc_option_refusals` | rc 1, same failure | rc 0 |
| Leg 0 run without `--require-rv32` | union | n/a | passes alone | Production docs aggregate refuses: "--require-rv32 on the union: test_baremetal_profile_contract ran only in a leg without the flag" |

Projections (each rounded up; the 270-second tail is 60 aggregate, 60
collector, 120 watcher interval and 30 tail):

| Worker | Inputs | Projected s | Margin to 1620 s |
|---|---|---:|---:|
| `docs-gates-0` | Hosted setup and gaps 59 s; each worker-0 step at the larger of hosted and local (1246.806 s); scheduling controls 28.331 s; 60 s recording | 1395 | 225 |
| `docs-gates-1` | 120 + leg 0, scaled by the slower local unsharded builder (1482.211 / 1443.720) | 1248 | 372 |
| `docs-gates-2` | 120 + CI-event 316.686 + runner 113.654 + 2 + leg 1, scaled the same way | 1073 | 547 |
| `elaborate-gates-0` | `2447 - 597 - 2 - 1763` + round-5 leg 0 scaled by `1763 / 1433.969` + 60 | 1475 | 145 |
| `elaborate-gates-1` | `2447 - 1763` + round-5 leg 1, scaled the same way, + 60 | 1353 | 267 |

The docs workflow projects at 1665 s, 135 s inside 30 minutes. Elaboration
projects at 1745 s, 55 s inside 30 minutes, so it is not divided further.
Every worker stays at or below 54.6% of its 45-minute limit.

Verification at `47fd0d3c5` (fresh clones, the shipping image, each generated
worker's gate steps exactly as written):

- `docs-gates-0`: 38 of 38 steps pass.
- `docs-gates-1`: builder leg 0 passes.
- `docs-gates-2`: builder leg 1 and the CI-event contract (2,187 items, 5,215
  arms) pass.
- The unsharded docs reference passes. The production docs aggregate and the
  equality check both accept the real receipts.
- The elaboration builder legs pass at this head, because the changed union
  code also runs there. The elaborate aggregate replay accepts them, with the
  same digest. Its LiteX aggregate step did not run in this bank, so that
  step's outcome in the replay is synthetic.
- docs-check-no-git and wire-accountability pass.
- The runner contract gate passes both invocations (109 s), and the runner
  digest is unchanged.
- Fifteen host gates pass on the clean head: docs, em-dash against `f6260253`
  and `e3d25d96`, style, paths, TOC, contract, generator freshness, shard
  self-test, idiom, hygiene and `git diff --check`.
- No run recorded a memory event.

Final-bank timings are not projection inputs. The bank ran three to five jobs
at once on the same 16 CPUs; the measurements ran one or two. Under that load
worker 0's steps took longer: compiler-absent controls 612.6 s against 558.6 s
alone. With those timings `docs-gates-0` would project at 1462 s and the docs
workflow at 1732 s. Elaboration leg 0 also took longer, 1193 s. Scaling
contended times by the uncontended hosted ratio would count the contention
twice. The exact-head hosted readback decides.

`scripts/act_ci.py` is byte-identical: SHA-256
`f968f67655ac386ea703248b724c3781b95ec379d3a5287b378e470df81f895c`. No gate
function, assertion inside a gate, fixture, timeout, NOT RUN arm, firmware
behaviour or linked image changed. `sw/builder/test_builder.py` is untouched.

## Round 7

Fixes for R636-6 under the round-7 decision, from `47fd0d3c` to `fe2e2a54`.
R637-6 is POSITIVE; R636-6 was NEGATIVE for one BLOCKER. No review coverage is
claimed.

| Item | Change | Evidence |
|---|---|---|
| 1. Runner self-test on small hosts (R636-6-F1) | `2db6c0f9d`: `selftest_main_entry_probe` (`scripts/act_ci.py:12168-12178`) adds `mock.patch.object(os, "cpu_count", return_value=512)` to its existing patch context, as the other main-path probes do (`:13675`, `:14675`). Six lines in that one self-test function; no production code path changes. SHA-256 `f968f676...895c` -> `7ff18c6a...46fd` | Controls below |
| 1. Committed control | New `scripts/act_ci_small_host_selftest.py`. It installs the runner read-only and runs its self-test in an isolated child whose `os.cpu_count()` reports 4 (`--cpus` 1 to 63). Then it runs the same self-test on a copy whose `main` no longer wraps its PR run in the cleanup-signal handlers. The clean run must pass. The planted run must fail the main-entry probe after reaching the lookup, not by the CPU refusal. Documented in `CI_WORKFLOWS.md` | Controls below |
| 2. R1, R2 | This body: the round-6 status ends "The coordinating role published this head."; the last limitation bullet uses the exact text given | This body |
| 2. S1 | `fe2e2a543`: `ci_gate_workflows_selftest.py` requires that the workers owning a builder leg are exactly `BUILDER_WORKERS`, and that exactly those workers upload `builder-leg-*.json` | Mutation battery below |
| 2. S2 | The same self-test plants, for docs and elaborate, a divided step that runs the driver in a preparation line, and one whose last line is not the driver. Each plant breaks one condition alone, and the generator must refuse each | Mutation battery below |

Small-host controls (an image like the hosted runner, CPython 3.12.3 with
PyYAML, no network or Docker socket, read-only source, fresh clone at
`fe2e2a54`):

| Run | Result |
|---|---|
| Control, 4 CPUs | rc 0, 69.0 s. Clean self-test `PASS`. The planted copy fails the main-entry probe alone. Its detail shows the lookup was reached, the runner died on the signal and the stub's process group survived |
| Control, 1 CPU | rc 0, same outcomes |
| Control against the `47fd0d3c` runner | rc 1. The clean run prints the hosted failure: "CPU range 0-15 exceeds this host's 4 CPUs". The planted run fails only by that refusal, which the control rejects |
| The docs `Local act runner contract gate` step, both invocations as written | rc 0, 102.6 s |

The control is a local command, not a CI step. The hosted gate already runs
on four CPUs, and a new step would change the generated graph and the contract
inventory. Its isolated child skips only the flat-install launcher, a fresh
interpreter the forced count cannot reach; every other arm runs under it.

Mutation battery (disposable clone; each mutation regenerated, so the
generator's `--check` passes under it):

| Mutation | Self-test at `47fd0d3c` | At `fe2e2a54` |
|---|---|---|
| Builder receipts retained only for elaboration (R636-6's S1 probe) | rc 0 | rc 1 |
| Builder receipts retained on every worker | not run | rc 1 |
| Driver-in-a-preparation-line refusal removed (R636-6's S2 probe) | rc 0 | rc 1 |
| Last-line refusal removed | not run | rc 1 |

Verification at `fe2e2a54`:

- The docs `CI scheduling and evidence controls` step (14 commands) passes in
  a fresh clone.
- `ci_events.py --check` and `--selftest` pass: 2,187 items, 5,215 arms.
- 17 host gates pass on the clean head, including docs-check, the em-dash
  check against `47fd0d3c`, the generator check, the runtime evidence
  self-test, the bare-metal check and self-test, Python idiom and hygiene.

No workflow template or generated workflow changed, so the round-6 banks and
projections stand. After review, the coordinating role repins the runner and
reads back the hosted docs run at this head; that readback is the exact check
for F1.

