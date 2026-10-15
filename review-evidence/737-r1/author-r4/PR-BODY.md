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

## Status

Round 4 is complete at `08adb21a` on `737-ci-30min` -> `dev`, from `84ee9ea1`.
Every round-4 item is committed and passes: the shared-budget control, the
conditional-preparation control, the client-error classification, the bounded
field-oracle build, both wording residues, and the elaboration worker. Under
the answer to the round-4 STOP, the builder gate runs in two measured legs, and
its requirements are judged on their union. The elaboration workflow now
projects at about 26.4 minutes. This head is not pushed; the coordinating role
publishes it.

| Workflow | Measured baseline at `7032bca5` | Current projection |
|---|---:|---|
| docs | about 34m00s | about 29.6 minutes with aggregate, collection and watcher tail |
| elaborate | 35m44s | about 26.4 minutes with aggregate, collection and watcher tail |
| rtl-fast | 19m03s | about 22 minutes including collection |
| rtl-full | 77m29s | continuous media-clock worker alone projects at 33m52s |

The projections are not hosted after-times. They include the watcher tail: up to
one 120-second polling interval, then the terminal guard, whose actual duration
is unmeasured. The accepted continuous-history exception remains above thirty
minutes. The coordinating role owns complete hosted timings.

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
