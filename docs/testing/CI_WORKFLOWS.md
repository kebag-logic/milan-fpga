# CI workflow policy

The repository separates rapid pull-request feedback from exhaustive RTL
validation. This changes when hosted runners execute the long gates; it does not
reduce the local verification bar in [CONTRIBUTING.md](../../CONTRIBUTING.md).

## Contents

- **[Fast feedback](#fast-feedback)** -- What runs on every pull-request update and why docs-only changes avoid RTL tool setup.
- **[Exhaustive validation](#exhaustive-validation)** -- When the full Verilator and Yosys inventories run and how exact-head evidence is preserved.
- **[Nightly and manual dispatch](#nightly-and-manual-dispatch)** -- The cron on the tip of `dev`, how to start a run by hand, and the two situations in which an agent should.
- **[One authoritative SHA](#one-authoritative-sha)** -- How every job of a run is pinned to one tree, what the workers record, what the aggregates refuse, and the gate that holds the files to this page.
- **[Elaboration](#elaboration)** -- The two gate workers that install LiteX, check elaboration and run its simulations, and what makes the aggregate red.
- **[Pull-request state](#pull-request-state)** -- How draft and ready states control hosted long jobs without changing local responsibilities.
- **[Act-first local replication](#act-first-local-replication)** -- The required exact-head local response while hosted Actions runs in parallel.
- **[Protected merge bar](#protected-merge-bar)** -- The active `dev` ruleset, its seven exact required contexts, and why its update policy is loose.
- **[Issue closing on merge](#issue-closing-on-merge)** -- What `Closes #N` does now that `dev` is the default branch, and what still waits for containment.
- **[Local commands](#local-commands)** -- The serial commands that remain the authoritative developer-side gates.
- **[Failure and cancellation semantics](#failure-and-cancellation-semantics)** -- How missing artifacts, superseded commits, and resumed work are handled.
- **[Source-tool cache provenance](#source-tool-cache-provenance)** -- Bind installations to release, source, and recipe digests.

## Fast feedback

[The fast RTL workflow](../../.github/workflows/rtl-fast.yml) runs on every
pull-request update and on every push to `dev`. It produces one stable
`rtl-fast` verdict from:

- conservative change classification;
- ratcheted whole-tree Verilator lint for RTL/tooling-relevant changes;
- BDD conformance;
- a Yosys/sv2v elaboration smoke for `milan_datapath`, `KL_pp_shadow`, and
  `KL_gptp_shadow` when RTL or its tooling changes;
- the source-list checkers' own self-tests, and the two out-of-context read
  sets expanded for real, so a source `syn/yosys/run.sh` names and the tree no
  longer carries fails here rather than inside Vivado. Those read sets are
  printed by `run.sh --emit` rather than read out of it, and nothing in the
  record is filtered: a token that is not a `.sv`/`.v` source is refused, not
  dropped. The declaration of the top is resolved through `sv2v --top`, which
  this job installs, and through nothing else -- three models of the directive
  layer were each accepted and then broken by a construct they did not model
  ([R0] on PR #240, rounds one to three), so a missing front end is a refusal
  with no flag to soften it;
- the mailbox publication census, `publication-census` (#665), when RTL or
  its tooling changes (below);
- the bare-metal control-plane firmware's host unit tests, `firmware-unit`
  and three mutation jobs (#665, #716), for relevant changes.
  They run the GoogleTest suites of
  `sw/firmware/ctrl` and `sw/firmware/ctrl_nvm` at every shipped shape, the
  two freestanding RV32 object builds, the tally listener's planted failure and
  crash, and the line and branch coverage ratchet with its planted cases
  ([the harness page](../../sw/firmware/gtest/README.md)). GoogleTest and
  GoogleMock are the runner distribution's `libgtest-dev` and
  `libgmock-dev`; the job prints the versions it installed and the gcc and
  gcov the ratchet is measured with. The RV32 SDK is the docs job's pinned
  cache and install. It precedes both required RV32 arms.
  Their freestanding headers exclude the SDK's hosted C library.
  The RV32 self-test plants header, ABI, and runtime-dependency defects.
  These builds report objects and frames, not linked-image bounds.
  F4 initializes the public lwSRP submodule at its exact pin.
  Each of the four jobs also initializes `third_party/tsn-c-stack`, the cores' submodule (#697).
  None runs a capture: the TSN stack boundary is `firmware-boundary`'s.
  The control gate includes lwSRP, SRP and its mutation campaign.
  The saved-state mutation campaign remains local (see [Local commands](#local-commands)).
  The tally listener's mutations (`tally_selftest.py --mutants`) also remain local.
  The job runs the tally listener's planted cases.
  The four jobs' budgets are in the table below (#716).
- the TSN stack boundary over the compiles of every builder it judges but
  those that need Verilator, `firmware-boundary` (#697), when RTL or its
  tooling changes. The step is
  `ctrl_boundary.py --require-rv32 --selftest --without verilator`, given no
  capture: the gate runs each builder of its own known set
  (`ctrl_configs.BUILDERS`) under one capture of its own, by its builds and
  not its suites, and judges that capture.
  The suite builders run by their `--build-only`: the control gate builds and links every arm's binaries and its RV32 build, the store's gate every shape's binaries and its RV32 build, and the coverage gate both gates' coverage builds.
  None runs a binary, plants a defect or measures anything; each ends `BUILT`.
  The RV32 self-test runs as it is: it compiles its planted cases and runs no binary.
  The fifth builder is `sw/litex/test_ctrl_memory.py --build-only`.
  It compiles the reset entry and links its probe.
  The job installs `sw/litex/litex_pins.txt` for its imports.
  This mode needs no CPU generation or SoC simulations.
  The sixth builder runs `stream_counter_f5.py --build-only` at both shapes.
  It compiles and links the firmware mailbox fixture without execution.
  Its own capture remains mandatory beside the other five.
  A builder dropped from the known set is still found by text, and refuses the gate by name: a program that names the firmware's tree must be a known builder or listed with why it need not be, even where another builder still runs it.
  So does a known builder the capture holds nothing of from a run of its own, though another builder's run compiles it, as the coverage gate's runs the control and store gates; two standing controls plant each.
  The builders found by text that compile only in a suite, the planted-defect campaigns and the coverage reader's planted cases, are listed with what they compile there (`ctrl_configs.SUITES`).
  The capture (`ctrl_capture.py`): a recording wrapper on `PATH` for every compiler has the real compiler expand each invocation and list what each source's compile reads, runs the real compiler unchanged and records both with its exit status.
  The gate judges exactly the sources the capture recorded as compiled, each by the compiler's own dependency output for that invocation: `-M` with the invocation's own arguments, directory and environment, and `-H`'s tree of what the source's own `#include` lines read.
  It builds no include path and lists no source: it classifies each file a compile read by where it lives.
  A compile of a firmware source reads no stack file outside `include/`, and no firmware file includes one in any compile; the firmware's sources include the saved-state store's and both images' own.
  A compile of a stack source reads, through its own `#include` lines, only the stack's files and the C implementation's headers, and no stack file includes anything else.
  The stack's tests reach nothing of this repository outside the submodule.
  It refuses a missing or empty capture, a known builder the capture holds nothing of, an invocation the compiler could not expand, and a source a passing compile compiled whose dependency output failed or is incomplete, by name.
  It runs the stack's own gate and the image builders under the capture itself.
  The builders that need Verilator, which this job has none of, are named and left out (`--without verilator`); `firmware-verilator` judges them.
  The stack's own boundary gate runs with gcc and clang.
  Every Makefile target that builds against the stack has the pin check as a prerequisite.
  Its pin controls refuse a stack off its gitlink or differing from it, in the MAAP differential and the AECP tools too.
  Every mailbox bench target that reaches the stack refuses a poisoned one on the pin check.
  Its controls compile planted copies through captures of their own, four at once, the hosted runner's CPU count, and the stack's own self-test runs beside them.
  The capture's recorder is compiled C; to each compile it adds a dependency pass, a preprocessing of that compile's source.
  The compiler's own expansion runs once for each distinct argument vector and is reused for the rest.
  Its budget is the job's own 30 minutes.
  On the runner's Ubuntu 24.04 with four CPUs, a replica of the step at `0a9c5fa8` took 682 s, 38% of 1800 s.
  Of that the builds took 614 s: the control gate's 299 s, the coverage gate's 226 s, the store's 80 s and the RV32 self-test's 9 s.
- the same TSN stack boundary over the compiles only the builders that need
  Verilator make, `firmware-verilator` (#697), when RTL or its tooling
  changes: the mailbox bench at its default target, the MAAP differential
  with its self-test, and the AECP wire comparison at each processor
  reference it pins (`--every`: one interface at the processor's gitlink,
  two at the merged #69 revision, each tree taken from the processor
  submodule's own objects).
  Each runs by its own commands (`ctrl_configs.BUILDERS`) under the gate's own capture, with the pinned Verilator from the cache `verilator-lint` shares.
  The step is `ctrl_boundary.py --require-rv32 --selftest --only verilator`: the same judgement over that capture, with the controls that need it and the pin controls.
  Those controls replay the wire comparison's and the differential's own recorded compiles on a planted copy, and drop the wire comparison's compiles from the capture.
  It names the firmware builders and their controls as `firmware-boundary`'s.
  Each recorded compile is judged whole, in the job that ran it.
  Its budget is the job's own 40 minutes.
  On a hosted runner at `5b4f6fbe`, before the dependency pass, the step took 438 s (job 114344992708) and the job 473 s, a fifth of the 40 minutes.
  A replica of the step took 486 s on four CPUs of a shared host, where `5b4f6fbe`'s took 452 s, on the runner's Ubuntu 24.04 with its GCC 13.3, CPython 3.12.3, static GoogleTest 1.14.0 and clang 18.
  Of that, the bench took 58 s, the differential 143 s and the wire comparison at both references 215 s; the judgement and its controls took the rest.

Firmware work uses four independent jobs, each requiring `changes`.
The `rtl-fast` aggregate requires every job's result.
Failures and cancellations remain failures.
Each job retains the same relevance condition.

`firmware-unit` runs normal suites, saved-state tests, and RV32 controls.
It also runs the tally checks and complete coverage ratchet.
`firmware-control-mutants` runs the complete control mutation table.
`firmware-aecp-mutants` runs the complete AECP mutation table.
`firmware-srp-mutants` runs both SRP campaigns and pin controls.
The normal shard includes the SRP wire comparator self-test.
Both SRP interface campaigns retain F-INT's publication mutants.
The aggregate also requires the separate `publication-census` job.
It also requires the two TSN stack boundary jobs above (#697), which run none of the four phases.
All jobs verify the same pinned SDK.
Only that authenticated SDK is cached; builds remain fresh.

| Job | Timeout | Hosted acceptance ceiling | Prediction ceiling |
|---|---|---|---|
| `firmware-unit` | 45 min | 1890 s | 1620 s |
| `firmware-control-mutants` | 45 min | 1890 s | 1620 s |
| `firmware-aecp-mutants` | 45 min | 1890 s | 1620 s |
| `firmware-srp-mutants` | 45 min | 1890 s | 1620 s |

Acceptance requires ten consecutive hosted runs within each 70% ceiling.
Before review, four-CPU measurements must predict each job below 60%.
Scale them using the original job's hosted-to-local ratio.
Include checkout, installation, cache, and completion overhead.
Issue #716 records measurements and the hosted acceptance table.

The control driver's `--shard INDEX/4` selects complete phases.
Its default invocation remains complete and ordered.
Every sharded run checks the live default invocation inventory.
Omitted or duplicated invocations fail, including newly discovered suites.
The self-test plants both defects and a future suite.
Coverage remains one unsplit measurement, with unchanged suites and thresholds.
No coverage artifacts cross job boundaries.
The generated command census retains each command's conditions.
`ci_events.py` rejects differences after removing only shard arguments.
It also pins every worker and its 45-minute timeout.

A change containing only documentation skips the Verilator and Yosys setup
jobs, `publication-census`, all four firmware jobs, `firmware-boundary` and `firmware-verilator`.
Documentation is a top-level `*.md`, anything under `LICENSES/`, or a
`*.md`, `*.drawio`, `*.svg` or `*.png` under `docs/`, less the pages a gated
module reads (#444). A gated module is code under the six roots named below,
other than the builder bank that `docs-check` runs whole. A page a gated module
reads stays relevant even where `docs-check` runs the same check, as the tap
page below does. Everything else is RTL relevant whatever its
suffix: every file under
`tb/`, `hdl/`, `sw/`, `syn/`, `scripts/`, `tests/` and `configs/`, the diagram
assets outside `docs/`, every generator, manifest and budget under `docs/`, an
Issue template and the root `LICENSE`. The `tsn_fuzz` suite compares
[the AVTP record](../../hdl/ieee1722/avtp/doc/TEST_RESULTS.md) and
[the gPTP record](../../hdl/ieee8021as/gptp_plane/doc/TEST_RESULTS.md) with
the campaign it runs, so those two records are relevant by directory.

These pages under `docs/` are relevant because Python in a classifier-gated
job names them. The behave suite of `bdd-conformance`, which no docs job runs,
asserts on [REGISTER_MAP.md](../reference/REGISTER_MAP.md) and
[MILAN_V12_AUDIT_2026-08-16.md](MILAN_V12_AUDIT_2026-08-16.md). The trace
catalogue generator's `--check` compares
[TRACE_EVENTS.md](../reference/TRACE_EVENTS.md).
`sw/builder/test_clock_contract.py` checks [AAF_LATENCY_TAPS.md](../AAF_LATENCY_TAPS.md).
Its tap table follows the configured clocks and features.
The tap page remains relevant under the #582 decision.
Its reader is absent from `DOCS_JOB_PY`.
`docs-check` also runs it through the builder bank.
`yosys-elaboration` runs the resource gate's `check-baseline`, which holds
`syn/ooc/pp_resource_baseline.json` to the policy table in
[AREA_BUDGET.md](../design/AREA_BUDGET.md#the-resource-gate) (#234).
`sw/mailbox/gen_mailbox.py --check --crosscheck` compares
[MAILBOX_CONTRACT.md](../reference/MAILBOX_CONTRACT.md) with the page it
generates from `sw/mailbox/mailbox.yaml` and reads its constant table back
(#665). No `docs-check` step runs it.
`sw/litex/test_ctrl_memory.py`, in the LiteX aggregate of `elaborate`,
requires the rule table in section 3 of
[SPLIT_CONTROL_MEMORY.md](../design/SPLIT_CONTROL_MEMORY.md) to equal
`ctrl_memory.RULES` (#640). No `docs-check` step runs it either.
`sw/firmware/ctrl/test/ctrl_service_bounds.py` runs in `firmware-unit`.
It checks [MAILBOX_SPLIT.md](../design/MAILBOX_SPLIT.md) against compiled service bounds.
Its controls reject stale figures and conclusions (#665 F3b).
No `docs-check` step runs this check.
The classifier's
self-test, `scripts/ci_scope.py --selftest`, derives that list from the
Python, the Makefiles and the shell under `tests/`, `tb/`, `syn/`, `sw/`,
`hdl/` and `avdecc/` and refuses a table that differs from it.
The following pages stay documentation only.
Their readers run identical checks in always-run `docs-check`:

| Reader | Skipped job that runs it | `docs-check` runs it too |
|---|---|---|
| `sw/builder/test_builder.py`: six pages under `docs/` | `elaborate` (`--require-elaboration` grades only the LiteX arms) | yes, every arm that reads a page |
| `docs/traceability/gen_module_matrix.py --check`: the matrix artifacts | the `tsn_fuzz` suite | yes, the same command |
| `scripts/ci_events.py --check`: this page | none, it runs in `full-ci-gate` before the decision | yes, the same command |

The derivation is a net, not a proof, and the table above stays the author's
to keep true (#444, [R197] F5, [R198] N3). It resolves a page named by its
whole path, by a path a literal ends in (a relative literal, or an f-string
whose head is a variable), and by a bare file name, which is what an
`os.path.join` piece, a pathlib join or a `$(DOCS)/NAME.md` recipe leaves
behind; `scripts/ci_scope.py --selftest` plants a new reader in each of those
spellings and requires the scan to name it. It cannot see a name computed at
run time (`DOCS / f"{name}.md"`), a glob over a `docs/` directory, a page
named only inside a message, a reader outside those six roots (a script under
`scripts/` that a suite calls, a C++ bench, a workflow step), or a file kind
it does not read. A reader written that way must be added to `GATE_READ_DOCS`
by hand.

All three scope steps classify against the live base the job builds on.
Hosted PR jobs check out a synthetic merge at `GITHUB_SHA`.
They use `git diff --no-renames --name-only <merge>^1 <merge>`.
The first parent is the live base tip used for that merge.
This lists exactly what landing the PR would change in that base.
GitHub's recorded `pull_request.base.sha` is frozen when the PR opens.
After a lane merges newer dev, that recorded base can hide restored RTL.
A frozen-base diff can therefore incorrectly skip the RTL gates.

The replay checks out the PR head, identified by `PR_HEAD_SHA`.
With `ACT=true`, scope reads `refs/remotes/origin/<base-ref>`.
`PR_BASE_REF` binds to `github.event.pull_request.base.ref`.
The runner already fetched that ref and verified its live tip.
Scope first requires a unique merge base.
It composes live and head using `git merge-tree --write-tree`.
It compares the live base with that composed tree.
The resulting paths match hosted merge scope.
Base-side renames follow Git's merge result into their destination.
Identical RTL edits already on dev add no changed path.
A head-only merge-base diff can miss renamed gate inputs.
It therefore cannot substitute for the composed diff.
The frozen base SHA remains event metadata and is never a scope input.
This also works with the existing trusted runner's event payload.
Each scope checkout explicitly sets `fetch-depth: 0`.
Missing revisions or missing merge ancestry fail the scope step.
Ambiguous ancestry and merge conflicts also fail the step.
Replay requires Git supporting `merge-tree --write-tree` (2.38 or newer).
Older documentation branches remain documentation-only.
RTL changes and submodule pointers remain relevant.
Empty deltas retain the conservative relevant verdict.
Fast push events retain their before-to-after tree comparison.
An unknown push base retains the full tracked-file fallback.

The merge train validates composition before every merge.
Its current-dev candidate runs builder and full native banks.
Those banks catch interactions with intervening base changes.
Scope selection therefore need not charge those changes to PRs.
The hosted required contexts and merge validation remain mandatory.

The scope self-test executes each workflow's actual shell body.
It compares hosted merge checkouts with replay head checkouts.
Its histories cover documentation, RTL, gitlinks, and empty deltas.
REV merges newer dev, restores an RTL file, then edits documentation.
REV+E adds a later unrelated dev RTL commit.
Both must stay relevant; a two-documentation-path B16 shape stays docs-only.
Base-side rename and identical-edit controls require hosted/replay equality.
They reject replacing composition with a head-only merge-base diff.
Each control rejects its corresponding removed rule.
Mutations reject frozen-base scope and replay endpoint comparisons.
The CI-events gate pins these scripts and their event bindings.
The runner contract separately pins the classifier's history call.
Removed, discarded and zeroed history results fail its controls.

All three classifier-gated workflows build the changed-path list with
`git diff --no-renames --name-only`, so a rename reaches the classifier as
both of its sides ([R198] N2). With git's default rename detection the list
holds the destination alone, and renaming a gate-read page or an RTL source
to a documentation path classified the pull request as docs-only while the
gate that reads it skipped. `scripts/ci_events.py` pins the flag in each of
the three scripts.

The aggregate still completes,
so a docs-only PR does not leave a required verdict pending. Mixed changes are
treated as RTL relevant. An empty diff is RTL relevant.
On PRs, unresolvable revisions or merge ancestry fail scope.
On pushes, an unresolvable before-SHA selects every tracked file.
A submodule pointer (`protocol-processor`, `gptp-processor`,
`external`, `third_party/...`, read from `.gitmodules`) or `.gitmodules` itself
is never docs-only: it moves the RTL the sweep elaborates without touching a
file under `hdl/`, and `scripts/ci_scope.py --selftest` proves a classifier
that files any one of them, or widens the documentation classes, is
rejected.

The elaboration smoke proves that the integration-heavy source lists lower and
resolve. It does not replace generic synthesis and must not be reported as a
portability pass.

The mailbox publication census runs in a job of its own, `publication-census`
(`sw/mailbox/publication_census.py --check --selftest --jobs "$(nproc)"`,
#665, comment 6100024293), which installs the pinned Yosys from the same
cache key as `yosys-elaboration` and the same pinned sv2v release. It
elaborates `milan_datapath` with the recipe `syn/yosys/run.sh --emit
milan_datapath` prints, in every shape the builder builds (the recipe's, and
each `configs/*.yaml` with its generated header and the parameters
`endstation_builder.datapath_params()` states), refuses an sv2v or a Yosys
other than the versions `rtl-fast.yml` pins, and follows every class-D value
the datapath reads through each netlist. Its self-test elaborates one planted
copy per defect, then removes each of the census's rules in turn, on every
core of the runner. The aggregate `rtl-fast` requires the job. The mailbox suite's
`make census` runs it locally; the suite's default `make` does not, because
the Verilator worker that owns that suite has no Yosys.

## Exhaustive validation

[The exhaustive RTL workflow](../../.github/workflows/rtl.yml) runs when:

- a non-draft PR is opened or updated;
- a draft PR is marked ready for review;
- `dev` receives a push;
- the nightly schedule fires, at 01:17 UTC (`17 1 * * *`), on the tip of `dev`;
- someone dispatches it by hand, on any branch.

`dev` has been the repository default branch since 2026-08-22 (#174, decision
3; `main` is the release branch, fast-forwarded deliberately). GitHub runs
scheduled workflows from the default branch only, so the cron validates the
tip of `dev` as it stands at 01:17 UTC, and `workflow_dispatch` is launchable
for any branch. Both paths are in
[Nightly and manual dispatch](#nightly-and-manual-dispatch). Until 2026-08-22
the default was `main`, which carried neither trigger, and no scheduled or
dispatched run had ever occurred; the first scheduled run is recorded on #174.

The workflow keeps the public aggregate names `verilator-suites` and
`yosys-portability`. Both are required contexts on `dev`: an RTL/tooling-
relevant PR must run them successfully, while a docs-only PR emits them as
explicit successful skipped results.

Verilator schedules 79 units on sixteen native matrix workers. The ordinary
serial command still runs the original 62 suites. CI expands six long suites
into driver-derived case partitions: `milan_dp` (four legs), `milan_dp_mclk`
(four), `capture_coherence` (four), `maap` (four), `milan_dp_render` (three), and
`pp_shadow` (four). The source drivers enumerate 19, 31, 31, 66, 3 and 4 units,
respectively. A unit can carry several original checks; it is never split by
resetting a carried history. No test predicate or per-suite timeout changes.

`scripts/suite_shards.py` assigns the longest measured pieces first. It pins
`tsn_fuzz` to worker 1 and `chmap_capture` to worker 3 for their specialized
installs. Worker 15 owns only media-clock leg A, whose continuous history is
indivisible under #737's ruling. Fifteen workers project at most 1605 seconds
including a conservative 122-second setup allowance. Leg A projects to 1910
seconds before setup and 2032 seconds with it. This is the explicit round-one
exception; the coordinating role measures the actual hosted head before the
owner decides any remaining acceleration. Regular workers have 29-minute
limits; leg A retains a 60-minute allowance within its former 120-minute job
limit. The separate nightly physical-rate job keeps its existing deadline.

The selector refuses a missing or extra duration, duplicate ownership, a
changed specialized owner, or a regular worker projected above 1620 seconds.
Its existing 60%-of-deadline control remains as an additional bound against
the largest declared timeout. The figures for split suites apportion baseline
`7032bca5` windows using measured local leg durations; they are predictions,
not measurements of the resulting hosted graph. Refresh them from the next
complete hosted run. The ordinary unsharded scheduling mode remains available.

Every selected leg writes source-bound case receipts. Each of six union jobs
waits for the native worker matrix, independently enumerates its suite's
current driver inventory, and requires every case exactly once. Dropping a
case from every leg and every claimed inventory still fails against that fresh
inventory. The union checks verdicts and checked-output digests, then assembles
the original physical suite log. The final `verilator-suites` aggregate requires
all sixteen workers and all six unions. It rechecks raw case evidence against
the union artifact, proves every original log's ownership and exact head, then
runs the unchanged tally. Missing, duplicated, extra, failed, cancelled or
skipped workers cannot release the protected context.

Every Verilator worker also initializes `third_party/tsn-c-stack`: the `mbx`
suite's co-simulation links the firmware's ADP, ACMP and MAAP cores, which
come from that submodule (#697), whichever shard owns the suite. Every bench
target that compiles against the stack has the shared pin check as a
prerequisite, so a checkout off the gitlink or differing from it is refused,
never built, whichever target runs.

Each suite runs under a per-suite wall clock from the table in
`scripts/run_all_suites.sh`. The measured hosted worst case plus a stated
margin sets each named entry:

| Suite | Budget | Basis |
|---|---|---|
| every other default suite | 1800 s | retained; #673's near-limit survey appears below |
| `mmcm_servo` | 1800 s | hosted window 1159.1 s; 640.9 s remains (35.6% of budget) |
| `capture_coherence` | 2400 s | hosted PASS 1642.280 s; 757.720 s remains (31.6%) |
| `milan_dp_mclk` | 3600 s | hosted TIMEOUT 1800.008 s; completion maximum remains unknown |
| `milan_dp` | 4800 s | hosted PASS 3509.562 s; 1290.438 s remains (26.9%) |
| `milan_dp_gptp` (scheduled) | 5400 s | the physical-rate decision below |

[The #673 ruling](https://github.com/kebag-logic/milan-fpga/issues/673#issuecomment-6015726285)
authorizes those three increases within existing shard envelopes.
The survey covers ten hosted runs on 2026-10-06.
Its endpoints are `37420502040` and `37457223191`.
Available logs provide 425 completed suite windows.
Seven active jobs withheld logs; one run skipped suites.
These windows include tally overhead between adjacent verdicts.
Timeout windows establish cutoffs, never successful completion bounds.

| Suite above 60% | Largest window | Previous limit | Usage | Run / job |
|---|---|---|---|---|
| `capture_coherence` | 1642.280 s PASS | 1800 s | 91.24% | [37429204551 / 112155955445](https://github.com/kebag-logic/milan-fpga/actions/runs/37429204551/job/112155955445) |
| `milan_dp` | 3509.562 s PASS | 3600 s | 97.49% | [37424768281 / 112142195163](https://github.com/kebag-logic/milan-fpga/actions/runs/37424768281/job/112142195163) |
| `milan_dp_mclk` | 1800.008 s TIMEOUT | 1800 s | 100.00% | [37430728685 / 112160880744](https://github.com/kebag-logic/milan-fpga/actions/runs/37430728685/job/112160880744) |
| `milan_dp_render` | 1285.710 s PASS | 1800 s | 71.43% | [37429204551 / 112155955318](https://github.com/kebag-logic/milan-fpga/actions/runs/37429204551/job/112155955318) |
| `mmcm_servo` | 1147.315 s PASS | 1800 s | 63.74% | [37430728685 / 112160880744](https://github.com/kebag-logic/milan-fpga/actions/runs/37430728685/job/112160880744) |
| `pp_shadow` | 1201.263 s PASS | 1800 s | 66.74% | [37424768281 / 112142195196](https://github.com/kebag-logic/milan-fpga/actions/runs/37424768281/job/112142195196) |
| `milan_dp_gptp` | 5400.003 s TIMEOUT | 5400 s | 100.00% | [37430728685 / 112160880673](https://github.com/kebag-logic/milan-fpga/actions/runs/37430728685/job/112160880673) |

The largest completed `milan_dp_mclk` window was 1084.530 seconds.
It came from run `37424768281`, job `112142195210`.
The three default suites exceeding 80% receive increases.
The remaining default suites retain their limits.
The ruling assigns `milan_dp_gptp` scheduling to a follow-up.

Each envelope substitutes new limits for changed suites.
It adds each sibling's largest observed window independently.
Job overhead equals total job time minus suite windows.
The largest observed overhead is added for each shard.
This includes setup, preflights, tally, upload, and cleanup.
Every affected shard remains below 6480 seconds: 90% utilization.

| Shard | New limit | Sibling maxima sum | Maximum overhead | Envelope | Remaining / 7200 s |
|---|---|---|---|---|---|
| 1/5 | 2400 s | 3381.779 s | 117.580 s | 5899.359 s | 1300.641 s / 18.06% |
| 2/5 | 3600 s | 2517.453 s | 86.448 s | 6203.901 s | 996.099 s / 13.83% |
| 4/5 | 4800 s | 0 s | 89.438 s | 4889.438 s | 2310.562 s / 32.09% |

Overhead maxima come from jobs `112142195196`, `112155955407`, and `112142195163`.
No requested limit needs trimming under this measured envelope.
These samples cannot bound future runner or cache-miss delays.
Checks, campaigns, shard assignments, and job timeouts remain unchanged.
An explicit `SUITE_TIMEOUT` still overrides every selected suite's limit.

PR #563's first head timed out during servo mutations.

The #545 decision keeps all clean checks under 1800 seconds.

Its mutation campaign now runs explicitly under #367's rule.

The servo Makefile records the revised two-CPU local measurement.

The hosted sample covers head `b94f53cc` in merge `4bb4317`.

[Run 36113401588](https://github.com/kebag-logic/milan-fpga/actions/runs/36113401588),
[job 108001867446](https://github.com/kebag-logic/milan-fpga/actions/runs/36113401588/job/108001867446), passed.

The window ran from 08:33:57.4 to 08:53:16.4 UTC.

The previous `milan_dp` budget used 37 hosted runs.
Those ran between 2026-09-15 and 2026-09-19, after #447's split.
Passing runs took 1055-1773 s.
The slowest runner class took 1726-1773 s across 19 runs.
Two runs timed out 1 s and 13 s early.
That 1800 s deadline became 2700 s under #444.
A timeout still fails the worker with exit 92.
`scripts/measure_test_evidence.py` pins the budgets.

The 2026-09-24 samples prompted [decision 5820240308](https://github.com/kebag-logic/milan-fpga/issues/387#issuecomment-5820240308).
It raises `milan_dp` to 3600 s and retains its controls.
Windows run from `shard: 4/5` through `PASS milan_dp`.
Each row represents one hosted sample.

| Revision | Window | Checks | Hosted job |
|---|---|---|---|
| dev `9d3288107e` | 1296.1 s | 9635 | [107573353073](https://github.com/kebag-logic/milan-fpga/actions/runs/35981190398/job/107573353073) |
| dev `57456af9` | 2133.3 s | 9720 | [107688389193](https://github.com/kebag-logic/milan-fpga/actions/runs/36015896775/job/107688389193) |
| PR #555 head `a9636e0f` | 2264.9 s | 9775 | [107720800104](https://github.com/kebag-logic/milan-fpga/actions/runs/36025349467/job/107720800104) |
| PR #555 head `a21cd358` | 2459.9 s | 9781 | [107763352706](https://github.com/kebag-logic/milan-fpga/actions/runs/36038109516/job/107763352706) |

The PR samples build candidate merges onto dev `57456af9`.
The day's observed spread was 1296-2460 s.
The `a21cd358` sample left 240.1 s of 2700 s: 8.9%.
That crossed [decision 5819379503](https://github.com/kebag-logic/milan-fpga/issues/387#issuecomment-5819379503)'s 10% trigger.
That historical budget left 1140.1 s: 31.7%, approximately 32%.
These historical samples do not measure the corrected candidate.
The five default gmstep controls stayed in `run` (#602) until #621.
The additional controls stay in the explicit `gmstep-mutants` campaign.
Those historical hosted shards allowed 120 minutes; #737's current limits appear above.
If later exact-head margin falls below 10%, split further.

#621 split further. Its small-step phase took the gmstep leg from 48 s to
253 s of CPU, and `milan_dp` ran that leg seven times: the clean leg, the
driver's positive control and five controls. Hosted run 38048622822 then
timed out at 4800 s. Dev's own windows before it were already above 60% of
that budget: 2972.7 to 3519.6 s on the six dev pushes from runs 37968528697
to 38067159953. The leg and its five default controls therefore moved to the
`milan_dp_gm_steps` suite, which the stable hash then gave worker 3/5, the
default worker with the most headroom: its jobs took 459 to 680 s in those six runs.
#727 replaced the hash with the measured-time split, which places the suite
by its own recorded duration.
The new suite keeps the 1800 s default budget. The clean leg runs every
phase once; the controls run without the #621 phase, which holds none of
their named checks. Its README records the native per-leg times at base,
at the #621 head and at the split head. Natively the leg and its controls
were 21.9% of `milan_dp` at base. Removed from the six dev windows above,
that projects `milan_dp` to 2323 to 2750 s, at most 57.3% of 4800 s. The
new suite projects to about 909 s, 50.5% of 1800 s. Hosted runs at the
pushed head confirm or replace both projections.

The `physical-gptp` job owns the physical-rate `milan_dp_gptp` suite.
It runs nightly at 01:17 UTC and on manual dispatch.
PR and push events exclude this job from execution.
Physical regressions therefore report nightly, outside the required PR aggregate.
The sixteen default workers retain every other suite.

The physical suite has a 5400-second build-and-run deadline.
Its separate four-core `ubuntu-latest` job permits 120 minutes total.
The remaining 30 minutes allow toolchain installation and evidence upload.
These deadlines await successful hosted measurement; they promise no completion time.
The earlier 2400-second hosted timeout established no upper slowdown bound.
Reference-platform timings and the decision appear in the [suite README](../../tb/verilator/milan_dp/README.md#ax7101-1x1-eight-channel-gptp-physical-rate-run).

The physical job records and verifies the event's exact SHA.
It uploads `physical-gptp-logs`, separately from `suite-logs-*` artifacts.
Failing DUT control transcripts reside below its `controls/` subdirectory.
The passing tally reads only top-level suite logs.
The standard driver retains its preflights, lock, timeout, verdict, and tally:

```sh
VERILATOR_JOBS=4 scripts/run_all_suites.sh /tmp/physical-logs --physical-gptp
python3 scripts/suite_tally.py /tmp/physical-logs --quiet \
  --expect-suite-root tb/verilator --physical-gptp
```

`ci_events.py` pins the physical job's full step sequence.
It pins event conditions, cancellation, deadlines, checkout, tooling, and evidence bindings.
Mutation tests reject disabled steps, altered budgets, and unbound evidence.
The default shard command is pinned separately.
The selector and tally share the default/physical inventory partition.

Yosys runs the complete top inventory on four weighted workers, under the
pinned toolchain the workflow declares: `YOSYS_VERSION` names the one Yosys
the gate's verdict is taken with, built from the upstream tag with its bundled ABC
submodule on a cache miss and proved by a version step that fails on any
other binary, and the sv2v release install is verified against the SHA-256
recorded in the workflow text (#287). The measured
heavy tops are isolated, while smaller tops are assigned with deterministic
longest-processing-time scheduling. Each worker uploads one result record per
top. The `yosys-portability` aggregate rejects:

- missing, duplicate, or unexpected top evidence;
- malformed or unreadable evidence, including a PASS top record without a
  numeric `cells` count (`cells=?` was every CI record's value for as long
  as the column existed, and nothing refused it — #287);
- any failed or timed-out worker;
- a missing or failed blocking tied-input gate;
- structural-gate ownership that appears more than once.

The tap-purity report remains informational in the combined Yosys script, which
preserves the existing local policy. Its result is still recorded exactly once.

**The result cache (#350).** Each Yosys worker runs `run.sh` with `--cache`
pointing at `${{ runner.temp }}/yosys-result-cache`, restored and saved by
`actions/cache@v4`. A top is skipped only when a stored PASS entry matches the
digest of its staged sv2v output, the exact Yosys program, the Yosys version
string and the Yosys binary's digest, the sv2v version, and the
generated ROM bundle digest (#520); and even then the
count it publishes is re-derived from the entry's stored `stat -json` by
`syn/yosys/result_cache.py`, which refuses an entry whose stored JSON disagrees
with its own `cells=` line, whose status is not PASS, or whose record is
malformed, so the top runs live instead. A miss runs exactly as it always has,
and a hit publishes the same result record a live run publishes; the shipping
`run.sh --list` inventory, the program and the recorded `cells=` values are
untouched. The trust boundary is GitHub's cache scoping, stated and pinned
rather than assumed: the save key ends in the run's own `github.sha`, so a
pull request's writes land in per-head state that only its branch can read;
the `restore-keys` prefix `yosys-results-<YOSYS_VERSION>-shard<N>-` lets a run
read the newest lineage of the same worker from its own branch or from `dev`,
and the entries `dev` published (its pushes and the nightly) are the read-only
seed. No candidate can write a cache another branch reads, `run.sh` never
rewrites an existing entry, and the workflow passes no `--cache-seed`: the
restored directory is the seed. `syn/yosys/cache_selftest.py`, run by the fast
workflow's Yosys job, drives a cold run, a warm hit, a forged entry that must
be refused and a read-only seed against the real script.

The ROM bundle binds exact filenames and generated bytes.
PP images are `ltn_rom.hex` and `ucode.hex`.
The gPTP image is `gptp_ucode.hex`.
Generation and existing nonempty checks precede digesting and lookup.
Names use fixed lexical order, independent of directory enumeration.
Each NUL-terminated name precedes an eight-byte big-endian content length.
The image bytes follow; SHA256 covers the complete concatenation.
Every selected top uses this conservative three-image bundle.
Lookup and store share its identity in both modes.
Schema 2 entries require that identity in both cache tiers.
Old-schema evidence runs live; no old PASS is upgraded.
Real-gate controls vary each image while retaining other key inputs.
Failed generators and empty/missing images retain their existing refusals.

## Nightly and manual dispatch

**The nightly** validates whatever `dev` points at when the cron fires. Its
value is environment drift: the Verilator and Yosys build caches (both tools
are pinned and version-verified, so the drift a nightly can find is the
cache or its build inputs, not the version), the Yosys result cache seed it
republishes for `dev` (a nightly hit rate below the tree's change rate is a
cache-scoping finding), the jemalloc preload (a speed
choice `syn/yosys/run.sh` makes only when the
library is installed, never a pass criterion), the hash-locked HDL reference
parser install,
the pinned `tsn-gen` revision and the LiteX pins all move under a tree that
did not, and
without the nightly the next pull request is the first thing to find out. A
red nightly on a tree whose last push was green is therefore a toolchain or
dependency finding, not a regression of the tree; file it as an Issue against
the pin or cache it names. `gh run list --workflow rtl.yml --event schedule`
lists the scheduled runs.

**Manual dispatch** starts the exhaustive workflow on the tip of a branch:

```sh
gh workflow run rtl.yml --ref <branch>
gh run list --workflow rtl.yml --event workflow_dispatch --limit 3
```

The run uses the `rtl.yml` of that branch and validates that branch's tip,
pinned as `GITHUB_SHA` like every other event; there are no inputs. Its
concurrency group includes the branch ref and the physical-run category.
Push and pull-request runs cannot cancel scheduled or dispatched physical evidence.

An agent uses dispatch in two situations:

1. **A draft head that needs exhaustive evidence without flipping ready.** The
   draft state is the cost lever: hosted workers stay idle while a PR is
   changing. When a draft needs the full inventory once, for example to
   measure a sweep before asking for review, dispatch on the branch instead of
   marking the PR ready and back.
2. **Recovery after a cancelled or expired run.** A ready PR whose last full
   run was cancelled by a later push that never completed, or whose artifacts
   have passed their 3-day retention, is re-validated on its exact head
   without an empty commit.

The merge bar reads exact-head evidence. A dispatched run names the SHA it
validated in its gate output and in both aggregate verdicts, so a reviewer
compares that line with the PR head before counting it.

**The default-branch assertion.** The cron was inert for three weeks because
the default branch was `main`, and no gate that reads files can see that
repository setting. So `full-ci-gate` reads it live on every run, with
`gh api repos/<owner>/<repo> --jq .default_branch` handed to
`scripts/ci_events.py --require-default-branch`, and prints
`default_branch=<observed> expected=dev event=<event>`. A scheduled or
dispatched run refuses to continue unless the observed value is `dev`, naming
the branch it saw; a value it could not read refuses too, since an unknown is
not agreement. A pull-request or push run prints the value and carries on:
those runs are about the tree, not the setting, and a contributor's PR must
not go red for a repository setting it cannot change. A drift is therefore
visible on every run and fatal on the first run it would misdirect, instead
of surfacing as a nightly that silently stopped. `ci_events.py --check` holds
the assertion in its fail-closed shape. That shape is not only what the step
says: a check that reads a step's contents and nothing about the conditions
under which it runs holds the wrong perimeter, which is what #209 found. So it
is exactly these twelve things in the source workflow contract under
`.github/ci-templates/`. The generated workflows retain that contract and
add the exact installation-cache, execution-evidence and failure-cancellation
steps defined by the generators. `ci_events.py` checks both levels: all
original negative controls still run against the source contract, and every
generated job, step, condition, environment and permission must equal the
generator's output. Thus an extra generated step is accepted only when the
generator defines it; the numbered source-step counts below are not counts of
the instrumented job:

1. **The script text.** The step's `run:` is pinned verbatim (whitespace
   aside) to three lines: `set -euo pipefail`, one unconditional
   `observed="$(gh api ...)"` read, one verifier call after it. A substring
   recognizer was fooled by a decoy, a literal `observed=dev` beside a
   `gh api` inside `if false`; the pin refuses it, and the structural reasons
   name what a deviation did: a second assignment, a value not sourced from
   the live call, control flow around the read, a comment line, the call
   before the read.
2. **The step keys.** The step carries exactly `name`, `env` and `run`, and
   its `env` exactly `GH_TOKEN`. A key beside a canonical script decides
   whether, on which events, or by which interpreter it runs: `if: false`,
   an `if:` naming only the events the assertion does not govern,
   `shell: bash -n {0}` (parsed, never executed), `continue-on-error`, a
   `working-directory`, or a `GH_HOST` / `GH_CONFIG_DIR` that points `gh`
   away from this repository. Each refusal names the key.
3. **The job's run conditions.** `full-ci-gate` carries no `needs`, no `if`,
   no `continue-on-error` and no `defaults`, and the workflow carries no
   top-level `defaults` (a `defaults.run.shell: bash -n {0}` parses every
   script and executes none). `needs` is one of them because a job that needs
   another job is a dependent, and a dependent of a skipped job is skipped,
   taking every assertion inside it: a `noop` job carrying
   `if: ${{ github.event_name != 'schedule' }}` plus a `needs: [noop]` on the
   gate leaves every pinned character in place and stops the assertion running
   on the one event it exists for.
4. **The step sequence.** The gate job carries exactly five steps, in this
   order: the checkout with `fetch-depth: 0`, the pin step (`id: target`), the
   default-branch step, the contract step, and the decision step
   (`id: gate`). The order is part
   of the contract, because the assertion runs the `ci_events.py` the checkout
   brought and the decision diffs the tree that checkout produced; the count is
   part of it too, because a step inserted anywhere runs before everything
   after it and can change what those steps read, and an entry appended to
   `GITHUB_PATH` puts another `gh` ahead of the runner's. A refusal names the
   position, what belongs there, and what it found. The same pin reaches
   every job in the four files: the four non-RTL carriers through item 11
   (#295), the seven RTL jobs -- the two shard workers, the two exhaustive
   aggregates, `verilator-lint`, `bdd-conformance` and `yosys-elaboration`
   -- through item 12 (#406), and this job, the physical leg, the fast
   selector and the fast verdict through the same comparison, over the
   lists `RTL_SIBLING_STEP_LISTS` records beside their own rules. For the
   two RTL files that is a standing invariant and not an enumeration of
   today's jobs: the checker reads both files for their job lists and
   refuses, by name, any job of either whose whole step list nothing
   records, and any job a recorded list names that its file no longer
   declares. Whether a job is pinned is a COMPARISON, never a claim and
   never an inference from what some rule refuses: the recorded list is
   held against the live job by count, order, identity, key set, env
   bindings, recorded `if`, recorded `with` and the recorded `id`,
   `continue-on-error` and `working-directory`, and nothing short of that
   counts as coverage. A rule that refuses something about a job -- a step
   count, a `run` body, a script -- leaves which steps the job runs
   unheld, so it is not a pin. A job appended to `rtl.yml` or to
   `rtl-fast.yml` is therefore
   red until its own step list is recorded in `RTL_SEQUENCE_PINS`; in
   `rtl-fast.yml` it is red twice over, because the verdict must `needs`
   every other job in the file and the verdict's new result binding needs
   an entry in `INHERITED_STEP_ENV`. In `docs.yml` and `elaborate.yml` the
   pin covers the jobs those two files carry today: neither is read for its
   job list, so a job appended to either is not refused by this rule. The
   contract step is
   this gate's SECOND hosted runner (#261, maintainer review on PR #293):
   its script is exactly `python3 -m pip install --quiet pyyaml` followed by
   `python3 scripts/ci_events.py --check`, its keys exactly `name` and `run`,
   and it is refused when removed, given an `if`, a `continue-on-error`, a
   `|| true`, or moved behind the decision. It exists because `docs-check`
   cannot police itself: every job-level lever that neuters that job
   (`if: false`, a `needs` on a skipped job, `continue-on-error`,
   `defaults.run.shell: bash -n`) also prevents or neuters the one step in
   docs.yml that would have refused it, and a skipped or falsely green
   required context satisfies the ruleset. This job cannot be neutered the
   same way: a gate that is skipped or fails makes both required aggregates
   fail closed (item 8), so the finding reaches the merge bar from a job
   docs.yml does not gate. Measured under act: `if: false` on `docs-check`
   fails the contract step, `full-ci-gate` fails, and both aggregates fail on
   the absent gate.
5. **The sibling steps' keys.** The pin step, the contract step, the
   decision step and the
   checkout are pinned to their own key sets exactly as the default-branch
   step is, so `if: false`, an `if:` naming only some events, a `shell:`, a
   `continue-on-error` or a `working-directory` on any of them is refused by
   name; the decision step's `env` is exactly `EVENT_NAME`, `PR_DRAFT`,
   `PR_BASE_REF` and `PR_HEAD_SHA`.
   Each uses the source expression item 6 requires, and the checkout keeps `fetch-depth: 0` (the decision step
   needs the merge's first parent or the replay's live-base ancestry,
   which a shallow clone need not carry).
   `if: false` on the pin step or on the decision step leaves the assert step's script canonical and publishes no `run_full` at all.
   Additionally, neither the workflow's top-level `env` nor `full-ci-gate`'s
   own names any `GH_*` variable: the step's `env` is pinned to exactly
   `GH_TOKEN`, but a `GH_HOST` or `GH_CONFIG_DIR` set at either level above it
   reaches the same `gh` without appearing anywhere in the step. Item 12 widens that from `GH_*` to every name at every level.
6. **The env bindings.** A pinned step's `env` is held as a name *and* the
   source expression that name is bound to, because the name is not the
   contract. The decision step carries
   `EVENT_NAME: ${{ github.event_name }}`,
   `PR_DRAFT: ${{ github.event.pull_request.draft }}`,
   `PR_BASE_REF: ${{ github.event.pull_request.base.ref }}` and
   `PR_HEAD_SHA: ${{ github.event.pull_request.head.sha }}`; the
   default-branch step carries `GH_TOKEN: ${{ github.token }}`; each verifier
   step binds `GATE_SHA` to `full-ci-gate`'s `target_sha` output, derived from
   that job and output rather than restated. Names alone held nothing where it
   mattered: `PR_DRAFT: "true"` is valid workflow YAML that keeps all four
   names and all four keys and makes a ready RTL pull request publish
   `run_full=false`, on which both worker matrices skip, both aggregates skip
   under the no-op exception in item 8, and the skipped required contexts
   satisfy the ruleset -- a false green, not a refusal.
   Rebinding `PR_BASE_REF` changes the replay's live-base lookup.
   Rebinding `PR_HEAD_SHA` changes its scope endpoint.
   The `ACT` marker selects the source-head replay path; hosted uses the merge.
   `EVENT_NAME: pull_request` makes a non-PR run take that PR path. A refusal
   names the step, the variable, the expression required and the one found.
7. **The decision step's script.** Pinned verbatim after whitespace
   normalization, the way the default-branch step's is, and refused by naming
   the first line that differs rather than dumping the script. The
   normalization every pin shares is the shell's, not Python's (#444,
   [R197] F4, [R198] N1): a backslash-newline joins with nothing, words
   separate on space and tab, lines break on LF, and any other space,
   separator, control or unprintable character is refused by name instead of
   normalized away, because bash reads those as part of a word. Under the
   older rule a continuation inside a comparison (`!=\` then `success`), a
   no-break space or a U+2028 normalized to the canonical text while bash
   read a different script: both exhaustive aggregates' worker-result steps
   then exited 0 on a failed, cancelled or timed-out worker, and this step
   published `run_full=false` for a ready RTL pull request. The bindings in
   item 6 hold what the step reads; this holds what it does with what it read,
   because `run_full=true` rewritten to `run_full=false` changes no pinned
   name and no pinned key and publishes the explicit no-op on every ready RTL
   pull request. The structural reason is checked first: the selector's
   `--selftest` runs exactly once and before the script reads the selector's
   answer, so a selector is never trusted to decide a run without its own
   proof. Re-indenting the script or wrapping a continuation differently is
   the same script and still passes.
8. **The verifier steps.** Each aggregate's `--require-target-sha` step
   carries exactly `name`, `if`, `env` and `run`; its `if` is exactly
   `${{ always() }}` (any other condition can skip the verification, and a
   skipped step passes the job); its `env` exactly `GATE_SHA`; and its
   script equals a canonical form derived from the job's own download step
   and the worker matrix, so `--expect` is the shard count and no line can
   reassign a source before the call. The aggregate jobs keep their
   documented fail-closed `if` verbatim and carry no `continue-on-error` or
   `defaults`: they skip only when `full-ci-gate` succeeded and explicitly
   published `run_full=false`; any other selector result runs the aggregate
   into the SHA/shard refusal path.
9. **The published outputs.** `full-ci-gate`'s `outputs` map is a
   NAME to EXPRESSION mapping exactly as a step's `env` is, and it is held by
   the same comparison: exactly `run_full`, `rtl` and `target_sha`, bound to
   `${{ steps.gate.outputs.run_full }}`, `${{ steps.gate.outputs.rtl }}` and
   `${{ steps.target.outputs.target_sha }}`, each derived from the step that
   computes it rather than restated. This is the publication path, and it is
   not the same object as item 7: no downstream job reads the decision step's
   output, they read `needs.full-ci-gate.outputs.run_full`, which is this
   map. Checking only that `target_sha` existed therefore held nothing where
   it mattered, because `run_full: ${{ 'false' }}` is valid job-output YAML
   that leaves every pinned step key, every env binding and every character
   of the decision script in place while the job exports the literal `false`:
   both worker matrices skip, both aggregates skip under the item 8 no-op
   exception, and the skipped required contexts satisfy the ruleset. A
   refusal names the job, the output, the expression required and the one
   found.
10. **The consumers of that decision.** Every job that needs `full-ci-gate`
    carries a pinned `if`, with no residue. The workflow's aggregate is the
    job whose display name is the public required check the merge bar reads,
    and it carries the fail-closed `if` of item 8; every other job that needs
    the gate is a consumer, and carries exactly
    `${{ needs.full-ci-gate.outputs.run_full == 'true' }}` and no
    `continue-on-error` or `defaults`. A job added later that depends on the
    gate lands in the consumer class and is refused until it carries that
    `if`, so this perimeter is closed under addition rather than being a
    list of the escapes earlier rounds happened to find. The closure runs in
    both directions ([R2] on PR #239): every job an aggregate lists in its
    own `needs` is classified too, as the selector, as a consumer, or as a
    held contributor that carries no `needs`, `if`, `continue-on-error` or
    `defaults` of its own. A job wired straight into an aggregate without
    needing the selector, as `bdd-conformance` is, previously landed in no
    class, so an `if: false` on it retired the specification suite with
    every hosted context green and the aggregate accepting the skip.
    Separately, no expression anywhere in either RTL workflow may read an
    output a job does not publish, and no static `needs` chain of any kind,
    `.result` as well as `.outputs.<name>`, may name a job the reader does
    not list in `needs`: each mistake evaluates to the empty string, so
    every comparison against it is false and every step or job gated on it
    skips. The audit resolves GitHub's dotted, bracket and mixed static
    spellings --
    `needs.<job>.outputs.<name>`, `needs['job'].outputs.name` and
    `needs['job']['outputs']['name']` -- as the same reference. A dynamic
    `needs[...]` access is refused because the producer and output cannot be
    proved statically.

    `rtl-fast.yml` publishes the same shape, from its `changes` job to
    `verilator-lint` and `yosys-elaboration`, and is held by the same check.
    Its aggregate counts a skipped consumer as a pass on purpose, since a
    docs-only change legitimately runs no RTL lint. Therefore the producer is
    held too: `changes` carries no `needs`, `if`, `continue-on-error`,
    `defaults` or job-level `env`; the workflow carries no top-level
    `defaults`; and its exact
    two-step sequence is `actions/checkout@v4` with full history followed by
    the `scope` step. That step's keys and four env bindings are pinned, and
    its normalized canonical script must self-test `ci_scope.py`, derive the
    conservative changed-file set, read the selector answer and publish that
    answer. An empty or forced-false publication can no longer skip both RTL
    consumers into the accepted docs-only path.

    The verdict half of the fast lane is held the same way ([R2] on PR
    #239). Because the aggregate runs under `always() && !cancelled()`, its
    one verdict step is the entire conversion of four job results into the
    required `rtl-fast` context, and an `if` on that step, a result binding
    rebound to the literal `success`, or a `case` widened to
    `success|skipped|failure` each turned a FAILED fast job into a green
    required context while every job key stayed canonical. So the aggregate
    must list every other job of the workflow in its `needs`, which also
    refuses an entry quietly dropped from the verdict; its single step
    carries exactly `name`, `env` and `run`; its env is derived from that
    `needs` list, one `<JOB>_RESULT` name per needed job bound to
    `${{ needs.<job>.result }}`; and its normalized script equals the
    canonical form derived from the same list, whose `case` accepts exactly
    `success` and `skipped`. Each public check name (`verilator-suites`,
    `yosys-portability`, `rtl-fast`, `elaborate`, `docs-check`,
    `wire-accountability`, `docs-check-no-git`) must be carried by exactly
    one job, so a second job renamed to a required name cannot make the
    ruleset's binding ambiguous. The rule reads a job's `name` as a literal,
    and GitHub evaluates it as an expression, so a `name` containing `${{`
    is held too ([R4] on PR #293): it may reference nothing but
    `${{ matrix.<key> }}` lists of the job's own literal `strategy.matrix`
    -- the sharded workers' `Verilator shard ${{ matrix.shard }}/${{
    matrix.total }}` is the shape this tree carries -- every rendering is
    enumerated and refused if it equals a required name in any file, and
    any other expression (`${{ 'docs-check' }}`, a `github`, `vars` or
    `needs` context, a matrix carrying `include`/`exclude` or built by
    `fromJSON`, a referenced key that is not a non-empty list of literal
    scalars, a `${{` the expression scan does not match) is refused
    outright because it cannot be enumerated here. The lists must be
    literal to the last character: the runner evaluates `strategy` before
    the matrix expands, so `n: ["${{ 'docs-check' }}"]` under
    `name: ${{ matrix.n }}` publishes the required name while an
    enumeration would see the text ([R3] round 4 on PR #293).
    `name: ${{ 'docs-check' }}` on a `run: true` job published a second
    check run under a required name that no literal comparison saw, in all
    four workflow files. And the count is per name, not per file: a job in
    any of the four files whose display name is a required name another
    workflow owns is refused, because the merge bar binds the name and a
    docs.yml job literally named `elaborate` is a second `elaborate` on
    every pull request the two workflows share ([R4] round 2 on PR #293).
    Nor is it per inventory (maintainer review on PR #293): the reader
    lists every `.yml`/`.yaml` under `.github/workflows/`, inventoried or
    not, parses each, and builds one map from required name to
    `(file, job id)` over all of them; each of the seven names must map to
    exactly one entry, in its owning file, under its own id, and a job in
    an un-inventoried file may carry no expression `name` at all, because
    nothing outside the inventory is legitimately named by one. A fifth
    file carrying `docs-check` -- which GitHub runs and binds all the same
    -- was invisible to the four-file inventory and is refused naming the
    file and the job.
11. **The non-RTL required contexts.** `docs-check`, `wire-accountability`,
    `docs-check-no-git` and `elaborate` are four of the seven names the merge
    bar reads, and their workflows have no aggregate: the carrier job IS the
    required context, and a skipped required context satisfies the ruleset.
    Both workflows sat outside items 1--10 (#261, found by the round-6 review
    of PR #239): `if: false` on `docs-check` retired this gate itself, since
    docs.yml was then the only workflow that ran `--check` (the gate job of
    rtl.yml is the second runner since PR #293, item 4), and
    `continue-on-error` on `elaborate` retired the elaboration gate, each
    with `checked=171 findings=0`. So the job carrying each of those names is
    held at the job level exactly as an RTL contributor is: no `needs`, no
    `if`, no `continue-on-error`, no `defaults`, and no top-level `defaults`
    on the workflow, each refusal naming the job and the key. The builder
    contract already held `docs-check` and `elaborate` for its own reason;
    the rule now reaches `wire-accountability` and `docs-check-no-git`,
    which no builder step touches, and the three documentation names join
    the one-carrier rule of item 10. The name and the content are held on
    ONE job ([R3] on PR #293): the merge bar binds a display name, the
    content checks read `docs-check` and `elaborate` by job id, and held
    apart the real job renamed to `docs-check-real` beside a `run: true`
    job named `docs-check` passed with no finding -- the unique carrier had
    no neuter key, the id-named job kept its pinned steps, and the required
    context ran nothing. So the job whose id is the public name must carry
    it. The six gate steps inside the four jobs are pinned too (#295, #303
    and #378): `docs-check`'s ci_events, imported-gPTP and em-dash steps,
    `wire-accountability`'s gate step, `docs-check-no-git`'s single step,
    and `elaborate`'s scope step. The four documentation
    steps each carry exactly `name` and `run`, the em-dash step `name`,
    `env` and `run`. Their scripts equal the recorded
    canonical forms after whitespace normalization, so a
    step-level `if`,
    `shell`, `continue-on-error` or `working-directory`, and a `|| true`
    or any other rewrite beside the call, is refused naming the step;
    the imported-gPTP body is bound to the exact step name, so leaving the
    canonical calls under another recorded name while that named gate becomes
    `run: true` is also refused. Its two commands are indivisible evidence:
    the parent checker validates current links and integration facts, and the
    donor build validates the documentation at the exact linked commit;
    the em-dash body is bound the same way ([R0] on PR #384), because its
    event selection, its null and empty base refusals, the fetch of a base
    the shallow checkout lacks and the gate call are one script -- `--base
    HEAD` judges no line and a `|| true` reports none, and each left every
    recorded key, name and binding in place;
    `elaborate`'s scope step is held as the decide step is (item 7, the
    #209 precedent) -- keys exactly `name`, `id`, `env` and `run`, its three
    env bindings (`EVENT_NAME`, `PR_BASE_REF`, `PR_HEAD_SHA`) pinned to
    the source expressions in item 6, `ci_scope.py
    --selftest` exactly once and before the script reads the selector's
    answer, and the whole script canonical -- so `if: false` on the step
    that publishes the output every elaboration gate's guard reads, a
    script rewritten to publish a literal `rtl`, and a dropped self-test
    are each refused. Each gate step must also be PRESENT exactly once in
    the job of the required id: a job body replaced wholesale by
    `run: true` with the real body's id renamed away, a removed gate
    step, or an appended duplicate `X:` mapping -- which PyYAML parses
    last-wins, so the id-named job IS the stub -- is refused naming the
    job, and the self-test proves the last-wins parse on a real appended
    duplicate on disk. And each carrier's whole step list is pinned the
    way item 4 pins the gate job's: count, order, each step's identity
    (its literal `name`, or its `uses`), each step's exact key set and
    env bindings, each recorded `if` verbatim (the scope guard on
    `elaborate`'s gated steps, `always()` plus the guard on its cache
    write-back) and each recorded `with` mapping exactly -- `docs-check`'s
    em-dash gate (#378) is the one documentation step recorded with an
    `env`, its `EVENT_NAME`, `PR_BASE_REF` and `PUSH_BEFORE_SHA` bound to
    their source expressions, and `docs-check`'s checkout carries
    `fetch-depth: 0` because that step derives its base by merge-base
    against the base BRANCH: GitHub freezes `pull_request.base.sha` when the
    request opens while the job checks out the merge into the current base
    tip, so the recorded oid attributed other pull requests' lines to the
    branch under test (the maintainer's finding on PR #384, the same lesson
    as #292) -- so a `run:` or
    `uses:` step inserted anywhere in the four jobs -- a `BASH_ENV`
    written to `$GITHUB_ENV`, a `$GITHUB_PATH` prepend, a third-party
    action, or any content at all -- is refused naming the job and the
    position, as are a removed, reordered or renamed step, a loosened
    step `if`, and a rewritten cache or upload `with`.

    Every recognized carrier `run` body is also pinned (#407).
    `CARRIER_STEP_LISTS` records each canonical script beside its step identity.
    Existing canonical gate scripts are reused; specialized checks still apply.
    Comparison uses item 7's whitespace normalization.
    Refusals name the job, step, and first differing line.
    Missing script records fail closed, even with unchanged workflows.
    `uses` steps retain their recorded `with` mappings.

    Mutation arms derive from live carrier steps, independently of records.
    Each body faces replacement, appended-command, and `continue-on-error` controls.
    Every normalized line gets a trailing `|| true` control.
    These include bounded `--check` calls and the AC5 idiom call.
    Multi-command bodies additionally lose a command and reorder distinct lines.
    Bodies carrying proof/check flags additionally lose a flag.
    Python gates, bounded ratchets, builder gates, and reference builds participate.
    A checker returning no findings fails every mutation arm.
    Whitespace reformatting and matching record updates remain accepted.

    Every legitimate script edit explicitly updates its canonical entry.
    Both edits belong in the same commit.
    Mutation arms derive automatically from the live body, independently.
    Never regenerate expected scripts during checking from candidate workflows.
12. **The inherited execution environment.** None of the keys above is
    `env`, and a name set at the workflow or job level reaches every step's
    shell before any pinned script runs: `BASH_ENV` names a file bash
    sources at the start of every non-interactive shell -- which a `run:`
    step is -- so `env: BASH_ENV: scripts/ci-bypass.sh` with a checked-in
    file holding `python3() { return 0; }` turned every python gate of every
    protected job, the gate's contract step included, into a no-op with
    every pinned key and script character in place and the required context
    green (maintainer [R0] on PR #293). A blacklist of known names is the
    wrong shape, because the runner's shell honours more than this page can
    enumerate, so the environment is held by exact allowlist at all three
    levels, in every one of the four files: the workflow-level `env` names
    exactly what the tree carries today (`VERILATOR_VERSION` and
    `TSN_GEN_REV` in the exhaustive workflow, `VERILATOR_VERSION` in the fast
    one, nothing in the other two); no job carries a job-level `env`; and
    the names a job's steps bind stay inside that job's recorded set (the
    gate's five, the workers' shard and target names, the aggregates'
    `GATE_SHA` and `SHARD_RESULT`, the selectors' event names, the verdict
    step's result bindings, `elaborate`'s scope triple, `docs-check`'s
    em-dash gate triple (`EVENT_NAME`, `PR_BASE_REF`, `PUSH_BEFORE_SHA`),
    and nothing else in the documentation jobs). Each
    refusal names the scope, the job or step, and
    the surplus names. Measured under act: a job-level `BASH_ENV` on
    `docs-check` makes that job's own gates green and `full-ci-gate`'s
    contract step refuse it, so both required aggregates fail. Declared
    `env` is not the only key that reaches those shells ([R4] round 6 on
    PR #293): `jobs.<id>.container` carries its own `env` map and chooses
    the image every step's `python3` comes from, `services` starts more of
    them, a step's `shell` picks the interpreter, and GitHub can add a key
    tomorrow. So the KEY SETS are held the same way: a workflow may carry
    only `name`, `on`, `concurrency`, `env` and `jobs`; a job only `name`,
    `runs-on`, `timeout-minutes`, `steps`, `needs`, `if`, `outputs` and
    `strategy` -- and that rule reaches EVERY job, an added standalone one
    included: `defaults` and `continue-on-error` are refused here as well
    as by the per-class rules, because those classify only the jobs they
    know, and a new job carried either with no finding (maintainer [R0]
    round 4 on PR #293); a step only `name`, `run`, `uses`, `with`, `id`, `env`,
    `if`, `continue-on-error` and `working-directory` -- what the tree
    carries today -- and a surplus key is refused by name whatever it does.
    The runner sets the same inherited environment from INSIDE a job too
    ([R3] round 8 on PR #293): any `run:` step may write `$GITHUB_ENV` or
    prepend `$GITHUB_PATH` for every later step, and a local `./` or
    third-party `uses:` runs code this page never reads; one added line in
    any job without a pinned sequence set `BASH_ENV` at run time with every
    declared level clean. So those are held by allowlist as well: exactly
    four recorded steps may mention either file (the two Verilator PATH
    steps, the tsn-gen `TSN_GEN_ROOT` export, the sbt PATH step), each
    bound by its normalised SCRIPT and appearing exactly once in its job --
    a name alone let the writer's own script gain a hostile line, and an
    added step under a recorded name write anything ([R3] round 9 on PR
    #293) -- every other mention is refused naming the step, a `uses:`
    outside the five recorded `actions/*` versions is refused, every
    checkout's `with` may carry nothing but `fetch-depth: 0`, a job may
    carry `outputs` or `strategy` only where the tree records it, a step may
    carry `working-directory` only on the one step that records it and
    only with its recorded value -- the behave step, `tests`; anywhere else
    the key, and on that step any other value, redirects a gate to a
    checked-in decoy tree ([R4] round 7, [R3] round 10 on PR #293) -- and a
    non-mapping `env` is refused at every level. #295 closed the step-list
    class for the four non-RTL carriers (item 11) and #406 closed it for
    the seven RTL jobs -- the two shard workers, the two exhaustive
    aggregates, `verilator-lint`, `yosys-elaboration` and
    `bdd-conformance` -- so every job in the four files now carries the
    sequence pin of item 4: its step list is pinned by count, order,
    identity, key set, env bindings, recorded `if` verbatim and recorded
    `with` exactly, plus the `id`, `continue-on-error` and
    `working-directory` a step records (the workers' `strategy.matrix`
    stays with the shard-denominator rule, the result cache's `with` with
    #350's). An inserted step of ANY content -- one reaching
    the runner's environment file without spelling its name included (the
    `_runner_file_commands` glob, an indirect expansion, a checked-in
    script) -- is refused naming the job and the position, and so are a
    removed, reordered or renamed step, an `if: false` on an ungated
    step, a dropped or loosened guard on a gated one, and a rewritten
    cache, upload or download `with`. The cost is deliberate: a legitimate
    step change in an RTL job -- a bumped cache key, a new toolchain step,
    a renamed step -- is refused until the job's entry in `RTL_STEP_LISTS`
    (`scripts/ci_events.py`; the four carriers' entries are
    `CARRIER_STEP_LISTS`, and the gate job, the physical leg, the fast
    selector and the fast verdict are `RTL_SIBLING_STEP_LISTS`) changes
    with it in the same commit, and the refusal names the job, the
    position, what belongs there and what it found. WHICH jobs a step list
    must be recorded for is not decided in the checker at all, and neither
    is which of them count as held. The two RTL files are read for their
    job lists, every job either declares is held against its recorded list
    by that same comparison, and a job no list records is refused by name
    (item 4). So one edit dropping a job's entry leaves that job in its
    workflow held by nothing, and the tree red; and so does any line
    claiming that some other rule covers it, because coverage IS the
    comparison and there is no holder to claim. A rule that refuses a step
    count, a `run` body or a script is not a whole-list pin, and a rule
    that already refuses the live tree reports that refusal in the same
    verdict rather than anywhere the coverage decision could discard it.
    The self-test plants the edits rather than describing them: a dropped
    entry, an entry truncated to two steps, an entry with one recorded key
    removed, a list recorded for a job the file does not declare, and a
    job appended WITH its list recorded, which is accepted because
    recording what a job runs is the remedy rather than an exemption. The
    arms that hold each job are derived from the live job, not from a
    table of rows, so dropping a job's entry does not retire its arms
    either: they go on demanding the position and identity refusals the
    recorded list made, which the coverage refusal is not one of, so
    `--selftest` goes red beside `--check`. The trust boundary is the
    checker's source. Recording a step list for a job pins it to exactly
    the steps recorded, which is what review reads, and there is no way to
    mark a job pinned without writing down what it runs; an arbitrary
    rewrite of the checker is outside that boundary, and what stands
    against it is the gate's own proof -- the coverage rule uncalled, its
    recorded-list item, its must-exist item or its comparison removed each
    fail named `--selftest` arms with `--check` still green.

    Every recognized run script in those seven jobs is pinned (#439).
    `RTL_STEP_LISTS` records canonical normalized scripts beside their step identities.
    The sibling `full-ci-gate` SHA-pin script is also pinned:
    "Print the event and pin the one SHA this run validates".
    Its canonical record belongs to `RTL_SIBLING_STEP_LISTS`.
    Both use item 11's comparison and item 7's unchanged normalization.
    Refusals name the job, step, and first differing normalized line.
    Missing, empty, malformed, and stale records fail closed.
    Existing specialized checks and step-list membership authority remain independent.
    Action steps retain their recorded keys and `with` bindings.

    Maintain each canonical entry alongside its matching workflow script.
    Both edits belong in the same commit, as for carriers.
    Shared canonical constants avoid duplicating identical scripts.
    Separately specialized pins must still agree with any maintained body.
    Never derive expected scripts from candidate workflows during checking.

    The new controls derive their population from live RTL steps.
    Every normalized line faces swallowing, deletion, and replacement controls.
    Syntax and comment lines additionally participate in the textual comparison.
    The SHA controls delete its mismatch block and neutralize `exit 1`.
    Each requires the content comparison's own named first-line diagnostic.
    An earlier specialized refusal cannot satisfy that expectation.
    Record controls exercise the actual sequence-to-content comparison wiring independently.
    Removing the content comparison or either RTL condition fails controls.
    Matching script/record maintenance and existing whitespace reformatting remain accepted.

    The four non-RTL carriers now pin every recognized script (#407).
    Their maintenance remedy is recorded in item 11.
    The second runner checks these pins independently through `ci_events --check`.
    A swallowed Python idiom call therefore leaves that step green,
    but both jobs' contract steps refuse it by name.
    `docs-check` fails; the exhaustive aggregates also fail closed.

`--selftest` covers, one at a time: the step removed, the token missing, the
live read replaced by an echo, the event not passed, `|| true`, the decoy
itself, a literal after the real read and after the call, `gh api` in a
comment only, `observed` from another command, two assignments, the call
before the read, an extra line, a missing `set` line; each key escape above
on the step, on the job, on the workflow and on the verifier steps; the gate
given a `needs` on a job that skips on `schedule`; `if: false`, an event-only
`if`, a `shell:`, a `continue-on-error`, a `working-directory` and a dropped
env key on the pin and decision steps; `PR_DRAFT` forced to `true`,
`PR_BASE_REF` rebound to `${{ github.sha }}`, `EVENT_NAME` hard-coded to
`pull_request`, `GH_TOKEN` rebound to another token and a verifier's
`GATE_SHA` rebound to its own run; the decision script rewritten to publish
`run_full=false` always and stripped of the selector's self-test; the assert
step moved before the
checkout; a `GITHUB_PATH` step inserted before it; the pin step removed; the
pin and assert steps swapped; a checkout without `fetch-depth: 0`; a `GH_HOST`
on the job and on the workflow; a shard denominator missing or stale in its
matrix carrier, restated while the shard list grows, and stale in a worker's
display name; a
verifier that reassigns `GATE_SHA`, passes the wrong `--expect`, passes none,
or keeps `--expect` while the matrix grows; an aggregate `if` loosened or
dropped; the gate's `run_full` and `rtl` outputs each rebound to a literal
`false`, `run_full` rebound to the scope answer, `target_sha` rebound to the
run's own SHA, each of the three dropped, the whole map dropped and a surplus
output added; a worker gated on an output nobody publishes, on `if: false`, on
a value the decision never takes, made `continue-on-error`, given a
`defaults.run.shell`, or reading the gate's output without needing the gate; a
new job that depends on the gate and gates on nothing; in `rtl-fast.yml`, the
`changes` selector's `rtl` output rebound to a literal and dropped, and its two
consumers gated on a misspelt output and on `if: false`; the `changes` job and
scope step each given `if: false`, the job made `continue-on-error`, the scope
env rebound, the scope script made to export `rtl=false` and stripped of its
self-test, checkout/scope swapped, checkout made shallow, and a workflow
`defaults.run.shell` inserted; dotted/bracket, all-bracket and mixed
`needs...outputs` references to missing dependencies or outputs, plus a
dynamic bracket reference; the fast verdict step given `if: false`, a
`shell` and a `continue-on-error`, its lint result binding rebound to the
literal `success`, and its `case` widened to accept `failure`;
`bdd-conformance` dropped from the aggregate's `needs` and a new fast job
left outside them; `bdd-conformance` itself given `if: false`, a
`continue-on-error` and a `defaults.run.shell`; a `.result` read from a job
outside `needs`, in the dotted and in the bracket spelling; `verilator-lint`
renamed to the public name `rtl-fast`; a job-level `env` on the fast
selector; each of `docs-check`, `wire-accountability`, `docs-check-no-git`
and `elaborate` given a job-level `if: false`, a `continue-on-error` and a
`needs`, the two the builder contract never touches given a
`defaults.run.shell` too, a second job carrying each of the four names,
each documentation carrier renamed, each of the four carriers renamed
away while a `run: true` job takes its name, a fifth workflow file carrying
`docs-check` by name and `elaborate` by job id and naming a job by an
expression -- in the parsed world and, for the directory scan itself, as a
real file beside copies of the five, with an unparseable one refused as
cannot-run -- the gate's contract step removed, given `if: false`, given a
`continue-on-error`, made to swallow its exit status and moved behind the
decision, a job-level `BASH_ENV` on `docs-check`, `wire-accountability`,
`elaborate` and `full-ci-gate`, a benign job-level name, a workflow-level
`BASH_ENV` on docs.yml and rtl.yml, a benign workflow-level name on
rtl-fast.yml, a step-level `BASH_ENV` on the docs ci_events step, the
elaborate builder call and the wire-accountability gate step, a `container`
with its own `BASH_ENV` on `docs-check`, `full-ci-gate` and `elaborate`,
`services`, an `Env:` spelling, a benign job key, a workflow-level
`defaults`, a step `shell` and a benign step key, an inserted step writing
`$GITHUB_ENV` or `$GITHUB_PATH` in a documentation job and in an RTL
worker, a write added to an existing step, a recorded writer renamed, a
local and a third-party `uses:`, a recorded writer's script given a hostile
line and the tsn-gen export rewritten, an added step under a recorded name,
a recorded writer duplicated, a checkout given `ref` and `repository`, a
`strategy` and an `outputs` on a documentation job, a `working-directory`
on the docs ci_events step and on the other behave-job step, the behave
step pointed at a decoy tree, a non-mapping `env` at
the workflow and step level, a fifth workflow file on disk under both
suffixes as a literal pair, a decoy whose `name` is an
expression evaluating to a required name in each of the four files, a
matrix job whose `name` renders one (its own file's and another file's), and
the enumeration's edges - a matrix value that is itself an expression, an
unmatched `${{`, `include`, a `fromJSON` matrix, a missing key, an empty
list - and a literal decoy carrying a required name another file owns, in
each of the four files; each of the five non-RTL gate steps (`docs-check`'s
ci_events and imported-gPTP steps, `wire-accountability`'s gate step,
`docs-check-no-git`'s single step, `elaborate`'s scope step)
given an `if: false`, a
`continue-on-error`, a `shell`, a `working-directory` and a `|| true`, and
each removed; the elaborate scope script made to publish a literal
`rtl=false`, stripped of its `ci_scope.py --selftest`, running the
self-test after the answer is read, and its three env bindings rebound; each
of the four carriers' bodies replaced by a `run: true` stub behind a
renamed-away id and by a duplicate mapping's last-wins parse, plus an
appended duplicate `wire-accountability:` and `elaborate:` mapping as a
real file on disk; a `BASH_ENV`-writing, a `$GITHUB_PATH`-prepending, a
third-party-`uses:` and a benign step inserted into the four carriers, a
recognised step removed, swapped and renamed, a non-gate carrier step
given `if: false`, a gated `elaborate` step's `if` loosened, and a cache
and an upload `with` rewritten; the same nine levers on EVERY job the two
RTL files declare (#406), derived from that job's own steps -- a
`BASH_ENV`-writing, a `$GITHUB_PATH`-prepending, a third-party-`uses:` and
a benign step inserted, a recorded step removed, swapped and renamed, a
gated step's `if` dropped (a job recording no gated step given `if: false`
on its first step instead), and a recorded `with` rewritten (a job
recording none given one) -- plus a step appended after the recorded last
step, a step given a `shell`, a recorded env binding rebound (a job binding
none given one), a recorded action swapped to a third-party action under
its recorded name, and each recorded `id`, `continue-on-error` and
`working-directory` changed, every one refused naming the job and the
position; the coverage rule's own arms, a benign job appended to `rtl.yml`
and to `rtl-fast.yml`, a step-pinned job respelt in its file and a
step-pinned job made to render the verdict's required name, refused as
recorded by no step list, as recorded but absent, and as a second carrier
of a required name; and, planted as a stage rather than as edits to the
tree, a recorded list dropped, truncated, narrowed by one recorded key, a
list recorded for a job no file declares and a job appended with its list
recorded, the first four refused by name and the last accepted; the em-dash
gate step's `EVENT_NAME`
hard-coded, its `PR_BASE_REF` rebound to the frozen `base.sha`, its
`PUSH_BEFORE_SHA` dropped, its env given a `BASH_ENV`, the step given
`if: false` and removed, its body replaced by `true`, judging from HEAD,
judging from the frozen recorded base, swallowing its exit status, its push
base rewritten, its base-branch fetch, its null-base refusal and its
by-SHA fetch removed, and its body moved under another recorded
name; every recognized non-RTL carrier body (#407) replaced by `true`,
given an appended command, and made `continue-on-error`;
every normalized line separately given `|| true`, including non-last calls;
multi-command bodies stripped of their last command and distinct lines swapped;
an existing proof/check flag removed wherever present;
each missing canonical script record refused by name;
a script and its canonical record updated together, accepted;
every recognized seven-job RTL body and the sibling SHA-pin body (#439)
given the same per-line swallowing controls, then each line deleted and replaced;
the SHA-pin mismatch assertion removed and its `exit 1` replaced by `true`;
each new content record missing, empty, blank, malformed, or stale;
each matching script/record maintenance edit accepted by the sequence comparison;
the imported gPTP gate removed, replaced by
`true`, stripped of either command, given `|| true` on either command, and
moved under another recorded step name; a whitespace-only
reformatting of every carrier body and the specialized canonical scripts
that must still pass; and the
decision itself for every event class.

## One authoritative SHA

GitHub pins `GITHUB_SHA` once per run, for every event: the pushed commit, the
merge commit of a pull request, the tip of `dev` for a schedule, the tip of
the chosen ref for a dispatch. Every `actions/checkout` step that does not
override `ref` checks out that commit, so every job of an exhaustive run
validates one tree. The workflow makes that explicit and machine-checked
(#174, decision 2):

- the `full-ci-gate` job prints `event=... ref=... sha=...`, refuses a
  checkout whose `HEAD` is not `GITHUB_SHA`, and exports the SHA as its
  `target_sha` output;
- every Verilator and Yosys worker refuses to start unless its checkout, its
  `GITHUB_SHA` and the gate's `target_sha` are one value, then writes that
  value into a `TARGET_SHA` file beside its evidence, inside the artifact it
  uploads. The file is neither a `*.log` nor a `*.result`, so neither tally
  reads it;
- both aggregates run `scripts/ci_events.py --require-target-sha` over the
  downloaded shards before they tally anything, passing `--expect` the
  worker matrix size (`--expect 16` for Verilator, `--expect 4` for Yosys)
  and exactly three sources, `--sha gate="$GATE_SHA"`
  (the gate's `target_sha` through the step env), `--sha run="$GITHUB_SHA"`
  and `--sha checkout="$(git rev-parse HEAD)"`, and print the SHA in their
  verdict. The verifier refuses any other source set, a dropped source or an
  unknown label included, and any shard-directory count but `--expect`, so
  an aggregate cannot quietly stop proving that the gate, the run and its
  checkout agree, or tally three shards as four.

The shard count is defined by each worker's `strategy.matrix.shard` list and
carried into the jobs by the singleton `matrix.total` dimension. The worker
passes `--shard ${{ matrix.shard }}/${{ matrix.total }}` and names itself the
same way. `--check` requires that singleton to equal the shard-list length and
derives the aggregate's `--expect` from the list. It refuses a missing or stale
total and any literal or `strategy.job-total` denominator in a script or job
name. With a matrix of five and a stale total of four, the check fails before
shard 4/5's suites or tops can be omitted while the artifact counts agree.

The aggregates refuse, and the check fails rather than skips:

- `full-ci-gate` fails, is cancelled, or does not publish an explicit
  `run_full` result (only a successful `run_full=false` decision may skip an
  aggregate);
- a shard directory without a `TARGET_SHA` record, including the empty
  placeholder the aggregate creates when the download produced nothing;
- a record that is not a 40-digit hexadecimal commit id;
- a record naming any tree but this run's;
- a gate `target_sha`, aggregate `GITHUB_SHA` and aggregate checkout that are
  not one value, or a source set that is not exactly those three;
- fewer or more shard directories than the worker matrix produces.

`scripts/ci_events.py --check` holds the workflow files to this contract and
to the trigger contract above: no `actions/checkout` step in `rtl.yml`
overrides `ref`, every job that uploads an artifact records the SHA first,
every job that downloads artifacts verifies it, the gate carries the
default-branch assertion in its fail-closed shape, the trigger lists, the
`cancel-in-progress` rule and the public aggregate names `rtl-fast`,
`verilator-suites`, `yosys-portability`, and `elaborate` are what this page
says, and the cron time string on this page matches the YAML. Its
`--selftest` removes or alters each item on in-memory copies and requires
the check to catch every one, and fails if the checker is stubbed to find
nothing. `--check` runs in the hosted docs job and, since PR #293, in the
gate job of the exhaustive workflow (item 4 below); `--selftest` runs in the
docs job only, so the vacuity control has one hosted runner.

## Elaboration

[The elaboration workflow](../../.github/workflows/elaborate.yml) runs on every
pull-request update, on every push to `dev` and `main`, and on manual dispatch.
Its two gate workers install the pinned LiteX stack. The builder gate
observes what elaboration hands `Instance("milan_datapath")` (#154): every
argv-to-parameter chain used to be proven by source-text greps against
`sw/litex/milan_soc.py`, and a flag severed on its way to the parameter it
names read green at two independent hops.

It uses the same change classification as the fast workflow. A docs-only
change skips the gate workers' product checks and the protected `elaborate`
aggregate still completes. A relevant change installs the pinned LiteX of
[`sw/litex/litex_pins.txt`](../../sw/litex/litex_pins.txt), places the
VexiiRiscv source at the revision LiteX itself pins, applies the patch series
in [`sw/litex/patches/`](../../sw/litex/patches) with its `apply.sh`, and runs
`sw/builder/test_builder.py --require-elaboration --require-rv32` in worker 0:
gates 23f, 23g and 23h and
their mutation arms. Upstream LiteX elaborates no configuration in this tree
(#185), so the series is a required install step and gate 23h proves the
installed trees are upstream plus exactly that series.

Independently, worker 1 installs Verilator and runs
`scripts/run_litex_sims.sh`, the one aggregate that owns the standalone LiteX
simulations in `sw/litex/` (#297): its inventory is pinned in the runner and
reconciled against the directory in both directions, so a deleted test cannot
vanish silently and an unlisted new one is a red run, and its `--selftest`
executes first - it plants a failing simulation, a masked verdict, a missing
member, an unlisted extra and a member-declared skip in a sandbox and
requires the verdict each time. The simulation aggregate reuses the interpreter its worker
just installed and patched; locally the same command runs against any
interpreter that imports `migen` + `litex` and otherwise declares its skips
(exit 90), see [TESTING.md section 2](TESTING.md#2-litex-integration-checks---swlitextest_py).

The Verilator is there for one member. `test_gptp_tx_timestamp` (#360) drives
one stimulus through the CONVERTED MAC transmit chain and through the migen
objects it was converted from, and requires the two pad traces to agree; the
converted half is a Verilator build and the source half needs the pinned
LiteX stack, so the comparison needs both tools in one job and this is the
workflow that provisions the complete stack for these gates. Its cache key, build recipe and
version proof are the ones `rtl.yml` uses, so the two workflows restore one
artifact and `scripts/ci_events.py --check` refuses a `VERILATOR_VERSION`
that has drifted in any of the three files that name it. On a host without
Verilator the member declares a skip (`RESULT: SKIP`, counted skipped, never
failed) and the aggregate reports INCOMPLETE rather than a green that would
claim a comparison nobody ran.

The RV32 SDK this job installs serves one member the same way.
`test_ctrl_memory` (#640 M8a) links a probe through the split placement's
link script with it, found by `sw/firmware/gtest/fw_rv32.py` at the path the
SDK step installs; without a compiler that member declares a skip too.
Its SoC arm runs the end-station builder, so it needs the PyYAML this job
installs, and exports the split 1x1 SoC through the LiteX the pins install and
the patch series patches. It needs no firmware data package: as
`sw/builder/test_shipping_clock_constraints.py` does, its child refuses every
`pythondata_software_*` import and writes LiteX's headers without the firmware
make inputs, which name picolibc and compiler-rt. So the arm grades the same in
this job and on a host that has those packages. The split CPU is its own
VexiiRiscv argument set, so a cold metadata cache pays one more Scala run for it.

`actions/checkout` does not populate submodules. Both this job and the hosted
`docs-check` job run the full builder, whose source gates consume
`protocol-processor`, `gptp-processor`, and the five shipping primitives under
`third_party/verilog-axis`. Each job therefore initializes exactly those three
trees in one step before its builder call; the elaboration setup step carries
the same live RTL-scope `if` as the call. `scripts/ci_events.py --check` pins
checkout-before-setup-before-call order, the event-pinned checkout shape and
action version, the exact setup and builder commands, their execution controls,
and the complete dependency set. Its mutation suite independently removes every
tree, redirects or disables checkout, moves setup on either side of that order,
and disables or replaces the setup and builder calls. A local run with an
already initialized worktree is not evidence that a fresh hosted checkout has
the sources. The same contract pins one exact sv2v v0.0.12 install per
builder job — release artefact checksum included: the script verifies the
zip against the SHA-256 recorded in the workflow text before installing
(#287) — before the call and under the elaboration job's live RTL-scope
`if`: `dp_srcs.py` refuses to resolve a top without a front end, so a runner
without sv2v turns the builder gate red rather than green, and the mutation
suite drops the install, drifts its version, moves it after the call, and
disables its condition.

Both builder jobs provision the selected RV32 SDK (#504).
The selection is Bootlin `riscv32-ilp32d--glibc--stable-2025.08-1`, GCC 14.3.0.
The [installer](../../scripts/ci_rv32_sdk.py) pins its official URL and SHA256:
`d42680e926542595c4c87629d33f5f90aac1e9a964c8955089e0514caa01b78f`.
Verification precedes extraction and execution of `relocate-sdk.sh`.
The destination is `$HOME/br-milan-rv32/host`, the existing selector location.
Prepending `PATH` alone cannot override that absolute selector.
This SDK supplies verification tools, not product build settings.
Its default ISA, `rv32imafd` with ILP32D, is the census ISA.
The shipping hart is RV32I, so the census sees stores the product lacks.
FP stores and RV32A AMO and SC instructions are ordinary census output here.
The resolver classifies every store instruction in the census assembly.
It fails closed on unknown classes; a called function's stores are outside it.
See [the store classes](../integration/BAREMETAL_FIRMWARE.md#editing-contract-for-this-firmware).
The bare-metal scope gate masks exact SDK identity literals.
Masks apply only within the installer and its fixture.
Wrong-file, appended-term, and product-document controls remain refusals.

Both caches bind the complete digest, runner OS, and architecture.
They also bind installer revision `1` and installer source bytes.
Neither cache accepts prefix fallbacks.
Every hit verifies provenance and files before running cached tools.
The receipt binds provenance, destination, files, modes, and symlinks.
Missing, malformed, stale, and corrupt receipts fail closed.
Existing directories without receipts are refused, never overwritten.
Logs identify the compiler realpath, version, target, and relocated sysroot.
GitHub cache scoping supplies trust; receipts detect cache drift.
Receipts are not independent signatures over hostile cache contents.

The installer self-test drives the hosted path, which passes no `--archive`.
It serves unpinned, truncated, empty and near-pin archives as the download.
Each is refused before tar reads it or any script runs.
The self-test pins the provenance field set and installer digest itself.
It also retargets an installed symlink and plants an escaping compiler.
Each of those refusals fails if its guard is removed.

Both builder calls pass `--require-rv32`.
A missing compiler therefore fails, rather than weakening hosted coverage.
An alternate compiler cannot satisfy the required selector adoption.
Elaboration provisioning retains its existing RTL scope guard.
`docs-check` additionally runs the explicitly weaker compiler-absent control.
It executes gate 1b with every cross candidate hidden.
Host compilers answer version and target probes only.
Firmware compilation through a host compiler is refused.
The text refusals #408 and #409 retired are absent there, as on every machine.
Their replacing instruments decline, and their mutations report `NOT RUN`.
The existing AEM generator self-test remains scheduled unchanged.
`ci_events.py` pins new steps, cache inputs, order, and guards.
Its mutation controls remove adoption and provenance requirements independently.

Reproduce focused controls without changing the workstation compiler:

```sh
python3 scripts/ci_rv32_sdk_selftest.py
python3 sw/builder/test_firmware_compiler.py --selftest
sdk_trial=$(mktemp -d)
python3 scripts/ci_rv32_sdk.py --destination "$sdk_trial/host"
python3 scripts/ci_rv32_sdk.py --destination "$sdk_trial/host"
python3 sw/builder/test_firmware_compiler.py \
  --sdk-destination "$sdk_trial/host" --audit "$sdk_trial/compiler.jsonl"
python3 sw/builder/test_firmware_compiler.py \
  --absent --audit "$sdk_trial/absent.jsonl"
```

The local SDK run logs its exact `argv[0]` substitution.
It preserves every remaining compiler argument and subprocess option.
That measurement proves local compatibility, not hosted selector adoption.
The hosted builder uses its ordinary selector without substitution.
The full builder, native banks, and trusted act remain required.
Exact-head hosted acceptance remains separate from local installer evidence.
For offline reproduction, add `--archive <verified-download.tar.xz>` when installing.
The installer still checks the pinned digest.
An absent run with `--require-rv32` must fail explicitly.

`Capture measurement census and clock gate` runs in `docs-check` (#559).
It follows `NVM record-space gate`, before `Saved-state writer gate`.
Its command is `python3 scripts/check_nvm_capture.py`.
It regenerates each measured shape's closed-record census.
It checks receipt clocks, source hashes, rows, and maxima.
Embedded controls reject input drift and omitted OFF timing.
No target compiler, simulator, or LiteX installation is required.
`CARRIER_STEP_LISTS` pins its name, position, keys, and canonical script.
The job's recorded step count includes this gate.
Removal, reordering, renaming, and conditional execution are refused.
Script replacement, appended commands, and swallowed failures are refused.
`continue-on-error` and missing script records are refused too.

The `docs-check` job ends with three shape gates, in this order:
`Sweep/build shape gate` (`scripts/check_sweep_shape.py --self-test`),
`Deploy shape gate` (`scripts/check_deploy_shape.py --self-test`, wired by
#466) and `Entity shape gate` (`scripts/check_entity_shape.py --self-test`).
The deploy shape gate holds `sw/litex/deploy.sh` to the shape `sweep.sh`
builds (#453): the launch line `deploy.sh build --dry-run` prints must be the
`OPTS` of `configs/generated/sweep_opts_ax7101.sh` token for token and the
emission of `configs/endstation_ax7101_1x1_tdm8.yaml` flag for flag. The dry
run only prints, so the gate needs no LiteX, but loading the config reads the
gPTP engine generator, so it needs the `gptp-processor` checkout above and
fails, never passes, without it. `--self-test` grades the tracked `deploy.sh`
first and then proves its planted drifts are rejected. `CARRIER_STEP_LISTS`
records all three steps by name, position, and canonical script.
Removing, reordering, or rewriting one is refused by name (#407).
Script refusals also identify the first differing line.
Legitimate command edits require matching record updates, as item 11 describes.

`AEM store generator self-test` runs just before those three gates.
It calls `python3 avdecc/gen_aem_store.py --self-test` (#464).
The AUDIO_MAP bounds, directory and Base-format checks must each refuse.
Each AUDIO_MAP vector must be refused by its own bound.
The vectors mutate the self-test's own two-map fixture.
The deployed model stays the positive control.
No step ran this self-test before, so it rotted unseen.
It reads first-party files only and needs no submodule.
`CARRIER_STEP_LISTS` pins this step the same way (#407).

Three caches have separate keys and no prefix restore fallback. The Scala
toolchain key binds its version, source and build recipe. The pip download
cache binds its pin file and installation recipe and runs only under the RTL
scope. Its pins are full-SHA git revisions. The generated CPU metadata key hashes
the configs, `milan_soc.py`, `build.sh`, `sweep.sh`, the pins and the patch
series, because LiteX names those files from the CPU arguments alone and
skips the generator whenever the file exists, so a stale entry would
elaborate metadata built by the previous toolchain while reporting green.

The `elaborate` check fails when no interpreter can import LiteX, when the
interpreter's VexiiRiscv rejects the `--l2-*` arguments the series adds, and
when any gate fails. A recipe recorded as unrunnable (#184's Arty leg) skips
only when it fails with exactly the recorded diagnostic, and the verdict names
every arm that did not run rather than claiming every arm ran.

## Pull-request state

Open implementation PRs as drafts while work is changing. The fast workflow
runs on each commit, while the hosted exhaustive jobs remain skipped.

Before marking a PR ready:

1. run the applicable focused tests;
2. run the complete local gates required by
   [CONTRIBUTING.md](../../CONTRIBUTING.md);
3. post exact commands and results on the PR;
4. ensure the current commit is the one intended for review.

Marking the PR ready starts the hosted exhaustive jobs on that exact head. A
later commit to a ready PR cancels obsolete work and starts a new full run.
Convert the PR back to draft before resuming exploratory implementation. Do not
claim hosted long-gate success for a commit other than the current PR head. A
draft that needs the exhaustive gates once is dispatched by hand (see
[Nightly and manual dispatch](#nightly-and-manual-dispatch)) rather than
flipped ready and back.

A docs-only ready PR remains cheap: the long workflow starts, classifies the
diff, and skips its RTL workers with explicit skipped results. The two stable
aggregate contexts are still emitted, so the ruleset never waits for a check
name that the pull request cannot produce. A skipped job leaves no log, so
the gate's decision step prints the reason in its own, in the words of the
rule the classifier applied: `docs-only: every changed path is a top-level
*.md, under LICENSES/, or a *.md, *.drawio, *.svg or *.png under docs/ that
no skipped gate reads unless docs-check reads it too`.

## Act-first local replication

After a PR head is pushed, an agent must use `act` instead of waiting for
GitHub Actions to finish. Start the repository-owned runner immediately while
the hosted workflows continue in parallel. The runner's validation base is the
live remote `refs/heads/dev` tip, resolved once at invocation: that is the
commit the trusted worktree must be at, and the commit the fetch must return.
GitHub's recorded PR base oid (`baseRefOid`) is frozen when the PR is opened
and does not track the branch, so the runner prints both SHAs and the recorded
one never refuses a run; re-targeting a PR's base to refresh it (the old
`gh pr edit --base` flip) is no longer needed.
The generated event retains the recorded oid as metadata, plus the base ref and the PR's own head.
Hosted scope compares the synthetic merge against its live-base first parent.
Replay scope uses the fetched, verified `refs/remotes/origin/<base-ref>`.
It requires a unique merge base with the PR head.
It composes both tips and compares live against that tree.
This matches hosted scope through base-side renames and identical edits.
Merge conflicts fail scope before any documentation-only output.

The recorded oid never participates in either scope calculation.
The replay self-test checks the production payload through all three selectors.
It covers stale-base documentation, RTL, pointers, empty deltas, REV and REV+E.
It also checks base-side renames and identical edits on dev.
Fixture Git uses isolated configuration, identity, dates and home directories.
Controls reject inherited signing settings and writes through `GIT_DIR`.
The validation base still anchors every trust and fetch check.
Because the trusted worktree must sit at a moving branch
tip, fast-forward it before invoking; a `dev` push between the resolve and the
fetch refuses the run, and the fix is to fast-forward and re-run. The runner is
host-side
security code: from the candidate worktree, execute only the copy in a
separate, clean worktree at the validation base:

```sh
python3 -I /absolute/path/to/trusted-dev/scripts/act_ci.py --pr <number> --cpu-ranges "$BOOKED_CPU_RANGES"
```

Never invoke `scripts/act_ci.py` from the candidate worktree as the host-side
orchestrator. The candidate copy does run its offline `--selftest` inside the
disposable `docs` CI job; that contained check grants it no host or Docker
authority and is not the trusted invocation described here. Python isolated
mode prevents the candidate directory and ambient `PYTHONPATH` from supplying
imports to the host-side runner. The runner verifies that its own worktree and
bytes are clean at the validation base before it reads candidate content. A PR
that introduces the runner cannot bootstrap trust in its own code: an independent
reviewer must first audit the exact file, install that file outside the
candidate worktree with no writable mode bits, record its SHA-256, then use
`--trusted-install-sha256` together with explicit `--repo` and `--worktree`
arguments. That bootstrap is an independently granted trust decision, not an
executor shortcut. Later PRs, including changes to this runner, are validated
by the already-trusted base copy.

The independent bootstrap records both the source commit and file digest, then
uses a non-writable copy; `<candidate>` and `<audited-install>` are absolute
paths chosen by that reviewer:

```sh
install -m 0555 <candidate>/scripts/act_ci.py <audited-install>/act_ci.py
sha256sum <audited-install>/act_ci.py
python3 -I <audited-install>/act_ci.py --selftest \
  --worktree <candidate>
python3 -I <audited-install>/act_ci.py --pr <number> --cpu-ranges "$BOOKED_CPU_RANGES" \
  --repo kebag-logic/milan-fpga --worktree <candidate> \
  --trusted-install-sha256 <recorded-64-hex-digest>
```

The audited install may be flat as shown. The offline self-test binds its byte
check to that installed file. It requires no copied repository directory
shape. Scope fixtures are inline; no sibling import is required.
The ordinary self-test runs the complete isolated single-file self-test.
The isolated child skips only that launcher, preventing recursion.
A sibling import planted outside the scope-event graph must fail.
The docs workflow also runs the documented flat installation directly.
Its contract pins the empty temporary directory, mode and invocation.

The reviewer's audit of those exact installed bytes is the trust anchor. The
runner's check of `--trusted-install-sha256` is self-attestation and detects
drift after that audit; it cannot establish that substituted runner code is
trustworthy by itself.

The `--selftest --worktree <candidate>` command above is the offline construction
and negative-control gate; the explicit worktree tells an installed runner
which shipping workflows to audit. That worktree remains untrusted: the reader
opens every path component without following symlinks, opens the final entry
nonblocking, requires a regular file and checks its size before a bounded read.
The negative controls cover symlinks, FIFOs, devices, and oversized files, so
the host-side bootstrap cannot be redirected into an unbounded candidate read.
The default PR run executes `docs`,
`elaborate`, `rtl-fast`, and `rtl-full` in that order.
Use repeatable `--workflow <name>` options for a focused reproduction, and use
`--dry-run` to perform the trust, fetch, metadata, and byte checks, print the
planned action clones without performing them, and print the generated command
before consuming containers. The runner requires `gh`, Git,
PyYAML, Docker, and exactly `act` 0.2.89. A newer act is refused until its Docker
mount and cache behavior is audited and the repository pin is deliberately
updated. On a host where the current user cannot open the Docker socket, add
`--sudo`; this is non-interactive. Both the host-side Docker CLI and `act` pass
through the same explicit `env -i` assignments and private empty `HOME`, keeping
them on the same daemon (the default local one unless `--slot` selects another)
without inheriting root's Docker
`currentContext`, `DOCKER_CONFIG`, `DOCKER_CONTEXT`, `DOCKER_HOST`, credential
helpers, or other ambient environment. The offline self-test plants a fake
ambient current context and proves the two sudo prefixes remain identical apart
from their executable. An invoking environment that sets `DOCKER_HOST`,
`DOCKER_CONTEXT` or `DOCKER_CONFIG` is refused rather than silently dropped,
because only `--slot` selects a daemon (see
[Parallel replay slots](#parallel-replay-slots)).

An audited change to the runner's cache, interruption, or Docker cleanup
boundary must also run the live fault-injection gate. It first writes a marker
through the effective runner tool cache and proves a second fresh run cannot see
it. It then plants two act-shaped volumes the runner did not create, one
outside the sleeping job's workflow lease and one inside it, requires the
inside one to refuse acquisition while both survive, and removes the inside
one itself before it can start the sleeping job. It then starts a
harmless sleeping job, inspects the real cache mount and the two job volumes `act`
created for it, waits for the owned container, freezes the `act` process
group, delivers `SIGINT` to the runner, and requires the container, network,
tool-cache volume, both job volumes, and run directory to be absent afterward
while the planted outside volume survives. The gate then reconciles both
planted volumes on every exit, checks the outside one's survival before that
reconciliation on the success path, and reports a planted volume it cannot
remove on stderr and fails. With `--sudo`, the probe also requires a root
`act` child distinct from the sudo leader, sends `SIGSTOP` through privileged
`kill`, proves every process-group member is stopped, and proves the complete
group is absent before Docker teardown. Cancellation is serialized with that
STOP transition, and the monitor must signal completion and be joined before
Docker teardown can begin. The interrupted job also runs under the CPU-range
monitor described below. That monitor must have moved the job's container to a
range of its own, as `docker container inspect` shows it, and it is contained
and joined before Docker teardown as well. A separate delayed-mutation probe
times out a CLI
whose privileged child would create a labelled volume two seconds later, then
proves the whole CLI group is absent and the mutation never occurs:

```sh
python3 -I <audited-install>/act_ci.py --interrupt-selftest --cpu-ranges "$BOOKED_CPU_RANGES" \
  --act-bin <absolute-act-0.2.89> [--sudo]
```

The credential boundary has its own live negative control, the boundary
self-test. It plants, in the invoking process's environment and a throwaway
operator home, every secret the boundary must withhold: a GitHub token, a
credential helper and an SSH command that only record being invoked, a
credential store, a netrc line, `gh` and Docker auth files, an SSH agent
socket, and an authenticated proxy on the loopback interface that records who
presents credentials to it, beside a host loopback service. It then runs one
probe job through the real boundary and the runner's own git at a credential
challenge on GitHub (a repository that does not exist, so the server asks for
credentials) and at an SSH URL, and requires the job to report the token, the Docker
socket, the host loopback, an agent socket, proxy variables and credential
files all absent (the job reports names and states, never values), the two
clones to fail for the boundary's own reasons, and every recorder to stay
silent. The same probe job then runs with the boundary removed (the operator
environment passed through, the token sourced from it, act's default socket
mount and host network) and plain git runs under the planted environment; now
the job must report the token, the socket and the loopback visible, the proxy
must have recorded an authenticated `CONNECT`, the credential helper must have
been consulted and the SSH command must have run with the agent socket. A
probe that cannot see a removed boundary proves nothing about the real one, so
the second half is required for a pass. Host caches are covered by the
interruption probe's cross-run marker and by the per-run action and cache
directories above. The offline self-test pins the plants, the probe workflow's
admissibility under the trusted sandbox, the transcript grading and both
command shapes.

```sh
python3 -I <audited-install>/act_ci.py --boundary-selftest --cpu-ranges "$BOOKED_CPU_RANGES" \
  --act-bin <absolute-act-0.2.89> [--sudo]
```

The command reads the open PR from GitHub and refuses before validation when
the base is not `dev`, the head is cross-repository, the candidate worktree is
dirty or at a different SHA, or selected workflow bytes disagree with the
remote commit even when index flags hide the edit. Replacement refs are
refused. The selected-file byte verifier uses the same no-follow, nonblocking,
regular-file-only bounded reader as the workflow sandbox. A credential-free
HTTPS fetch into a new temporary Git repository
materializes the exact same-repository PR head and validation base without
using the candidate's object database, index, configuration, hooks, filters,
or worktree; a `dev` tip that moves between the invocation-time resolve and
that fetch refuses the run, naming both base SHAs. The PR number, state, draft
bit, base ref, head ref/SHA, repository, cross-repository bit, and URL are
queried again immediately before and after every workflow; any change
invalidates the whole run. A recorded base oid that moves is reported and does
not refuse: the runner prints the old and new values and retains the result,
because the validation base was resolved at invocation, those unrelated bytes
were not executed, and the exact PR head did not change.

This local replica validates the exact head tree, not GitHub's synthetic merge
commit. Hosted `pull_request` contexts validate `refs/pull/<number>/merge`, so
they remain the authority for current merge compatibility while the local run
provides earlier evidence about the candidate's own bytes. A later `dev` move
can therefore require new hosted merge-context checks without discarding an
otherwise complete local head-tree run.

Before any candidate-directed network operation, the runner parses the exact
committed `.gitmodules` blob and requires the trusted name/path/URL pairs with
no duplicate or extra configuration. It also requires the matching six
gitlink paths. Git disables every transport by default and enables only HTTPS;
the inactive SSH-only `external` entry must match the trusted manifest but is
never fetched. Only then, and only after selected workflows pass their static
sandbox scan, does the temporary checkout initialize the five allowlisted
public pinned dependencies (`third_party/verilog-axis`, `protocol-processor`,
`gptp-processor`, `third_party/lwSRP`, and `third_party/tsn-c-stack`). This
gives act's checkout copier the submodule-path parity that a hosted checkout exposes; each workflow's own submodule update
remains the authoritative, idempotent check of those pins.

The runner then populates the per-run action cache itself, serially, before
`act` may launch any job (#337). It reads every step-level `uses:` of the
selected workflows through the same bounded reader, re-checks each against the
audited action set (this is the step that puts candidate-named repositories on
the network, so the check is not inherited from the sandbox scan), and performs
each distinct clone `act` would otherwise perform lazily: a credential-free
HTTPS clone of `https://github.com/<owner>/<repo>` under the candidate fetch's
no-prompt, no-helper, HTTPS-only Git environment, then a detached checkout of
the ref (tag, origin branch, or SHA, in that order) in the directory `act`
derives from the `uses:` string (`actions-cache@v4` for `actions/cache@v4`).
Each action is reported with its resolved SHA; a failure refuses the run before
a container exists; `--dry-run` prints the plan and clones nothing. Every `act`
invocation then carries `--action-offline-mode`, so sibling jobs read the
populated directory and never fetch or check out. Without this, `act` clones
and checks out an action from whichever sibling job reaches it first while the
others copy the same directory into their containers; a copy taken
mid-checkout sees the default branch's file set or a torn bundle, which is how
`rtl-fast` lost `yosys-elaboration` to an `lstat` of `jest.config.ts` under
`actions-cache@v4` and to an `__dirname` error from a truncated
`dist/restore/index.js`. The offline self-test pins the collector, the
directory naming, the clone environment, the resolve order, the refusal on a
failed clone, the offline flag, and that the population precedes the Docker
boundary and the first `act` launch; the all-workflow ready run is the live
negative control, reproducing either symptom without the population and the
flag and neither with them.

Every host-side command routed through the runner's capture boundary, including
Git metadata, fetch, checkout, and submodule commands, runs in a distinct
tracked process group with a 30-minute upper bound. An interrupt or timeout
cannot release the caller until that complete group is terminated, reaped, and
proved absent. Offline controls deliver process-directed `SIGTERM` and `SIGHUP`
to a captured child tree, and both signals to a production-shaped Git fetch with
a remote-helper grandchild. Each requires the conventional interrupted status
and proves the helper group absent within a bounded post-exit window. The
helpers do not clean up their own children, so a cleanup implementation that
only signals the group leader cannot satisfy the controls. When the
host exposes the facility, the test harness temporarily becomes a child
subreaper. It, rather than act's bare PID 1, reaps already-exited probe
descendants; the runner must still terminate the executable group, and the
probe allows its complete 25-second escalation. A separate
production-entry control invokes the normal PR command path, interrupts its early
repository lookup, and therefore fails if signal containment is narrowed to
workflow execution again.

Probe clones give descendants a grace period to drain after their leader
exits. Only live process-group members count as survivors: a member whose
`/proc/<pid>/stat` state is `Z` has already exited and cannot continue the
probe. The act job container's PID 1 is act's own `tail` process, which reaps
no orphans, while the hosted VM's PID 1 reaps them. An unreaped zombie must
therefore not prevent draining in the local replica. The runner checks host
group membership before reading state, skipping foreign processes even when
their state is inaccessible. An unreadable member refuses the probe. Before
accepting a drained group, it sends `SIGSTOP` and requires two matching
inventories of confirmed group members and their states, repeating the stop
before the second scan. Confirmed members remain inventoried if their state
read races their disappearance; the second scan catches newly forked members.
Confirmed foreign PIDs never affect the comparison, even when they appear or
vanish between scans. Unanswerable membership queries refuse inspection;
already-vanished PIDs are skipped. A changing member inventory uses another
grace tick. Live members resume with `SIGCONT` after
inspection, including on an inspection failure. Any live member that outlives
the unchanged grace still causes refusal and `SIGKILL` of the group.

The synthetic pull-request event names the exact base and head. A draft uses
`synchronize`, retaining `draft=true`; a ready PR uses `ready_for_review`, so
the real exhaustive selector launches all workers. `act` copies the immutable
temporary checkout rather than fetching through `actions/checkout`. It starts
from an empty invocation directory with private `HOME`/XDG roots, a minimal
allowlisted environment, and explicit empty env, secret, variable, and input
files. `GITHUB_TOKEN` is explicitly empty, so neither the active `gh` credential
nor an SSH agent, proxy credential, runtime token, or other host secret reaches
candidate code.

Candidate jobs must use literal `ubuntu-latest`; reusable workflows and
job/service containers are refused because they can carry container options or
host-volume requests that the trusted scanner cannot safely delegate. Steps may
use only the repository's exact audited non-Docker action set
(`actions/checkout@v4`, `actions/cache@v4`, `actions/setup-python@v5`,
`actions/upload-artifact@v4`, and `actions/download-artifact@v4`). Direct
`docker://` actions, local actions (including `runs.using: docker`), and any
unaudited remote action are refused before `act` starts; otherwise act can build
or reuse a daemon-global action image outside the labelled run boundary. Offline
negative controls cover all three forms, neutral names, and an unapproved
version inside the otherwise trusted `actions/*` namespace. The act command
also disables the container Docker socket, uses an unpredictable
runner-created bridge network instead of the host network, applies the same
unpredictable ownership token as a container label, never bind-mounts the
operator's worktree, and supplies no privileged flag. Candidate workflow code
consequently runs only in the disposable job boundary.

Every local job gets an exclusively booked CPU range.
The manager supplies these through `--cpu-ranges`.
For example, `0-15,16-31,32-47,48-63` books four ranges.
This example is not a host allocation table.
The manager prevents overlap with other host work.
Each normal range contains sixteen CPUs, aligned to sixteen.
The fallback width is `FALLBACK_CPU_LIMIT=12`, aligned to twelve.
Missing, overlapping, unaligned and unavailable ranges are refused.
Eight-CPU ranges remain refused under the current owner ruling.
Daemon slot numbers never determine CPU numbers.

The dispatcher reserves a free range before executing a job.
Docker creates that job container directly on its reserved range.
No staging range or later CPU update exists.
A job waits until an admission token becomes available.
Its range stays reserved until the job's cleanup finishes.
Failed cleanup cancels admission before any range can be reused.
The run records each job's range in its scheduler events.
A read-only daemon monitor independently checks container placement.
Sharing, unbooked placement and later movement fail the replay.
Monitor failure also prevents a successful replay verdict.
`cpu-placements.json` retains reservations, inspection problems and peak concurrency.
CPU observations remain outside the canonical manifest comparison.

Every generated job reads its own CPU count with `nproc`.
Tool builds use that count for `make -j`; Verilator uses `VERILATOR_JOBS`.
Existing `-j 0` recipes use Verilator 5.050's process-affinity default.
They therefore see the container's booked CPU count.
Campaign pools use the smaller of that count and four.
This retains the measured memory bound on both 12- and 16-CPU jobs.
Simulation pools use the same bound; case drivers retain their two-run cap.
Outer suite make invocations remain serial to preserve shared build ownership.
The compiler inside the selected build receives the CPU budget.
The capture campaign divides that budget among its active build workers.
Controls execute the generated shell at one, four, twelve and sixteen CPUs.
They refuse zero CPUs and prove nested build budgets do not exceed the range.

One scheduler serves every selected, byte-identical workflow file.
`CONCURRENT_JOB_LIMIT=4` bounds admissions across workflows and nested matrices.
The pinned dispatcher is `0.2.89+milan-ci5`.
Vanilla dispatchers lack this combined admission and placement contract.
Each job waits only for its declared dependencies and a free range.
An unrelated job in an earlier plan stage cannot hold it back.
The dependency control keeps an independent job running until a ready
dependent job starts, so a stage barrier fails the control.
The build recipe verifies upstream source and compiler digests.
It runs original upstream controls and repeated race-enabled controls.
Controls prove nonoverlap, stable placement and failed-cleanup refusal.
Missing, insufficient and too-small ranges are independently refused.
The first failed job stops further admissions and cancels siblings.
Successful controls require every scheduled job to complete.
Hosted matrices retain `fail-fast: true`, including fork PRs.

Containers retain the measured eight-GiB limit, with no additional swap.
Four containers plus four-GiB overhead fit the 36-GiB slot cap.
The host now has 61 GB, shared with other work.
This policy leaves headroom without reserving all remaining host memory.
Measured peaks and their limits appear under resource bounds below.
Higher concurrency requires a new measured memory allocation.
The current runner deliberately keeps four as its maximum.

The placement monitor retains the audited signal-safe cleanup boundary.
Cleanup signals remain blocked while its reader is being joined.
The execution boundary opens its signal window during execution.
Every exit contains the event process and closes its pipe.
The reader must end before Docker boundary teardown starts.
A delayed inspection exercises that ordering in the offline controls.
Signals retain conventional status and cannot replace an earlier failure.
The existing containment, failed-reap and interrupted-join controls remain required.
Dry runs print manager-booked ranges for every daemon slot.

Every run and SHA gets fresh action/workspace, Actions-cache, artifact, event,
configuration, and input directories. `act` 0.2.89 also hard-codes the global
Docker volume name `act-toolcache`; the runner turns that otherwise persistent
slot into an exclusive ephemeral boundary. It refuses if that volume already
exists, creates it empty with the run's unpredictable ownership label, verifies
the label before every workflow, and removes it with an absence check after the
last owned container. The refusal names the
`org.kebag-logic.milan-act-ci.owner` label. Before removing an unlabelled legacy
cache, the operator must serialize every act runner and prove no container uses
it; absence of a label does not prove inactivity. A labelled cache must not be
removed until no runner, container, or network with its owner token remains.
The runner never deletes a
volume it does not own, by label or by the job-volume lease described below.
Concurrent runner invocations on one daemon fail closed because only one can
own the upstream global name; invocations in different replay slots each own
the name on their own daemon. If a Docker create call times out or is
interrupted after the daemon accepted it, the runner inspects the exact global
volume name and unpredictable network name, removes only resources carrying its
token, and verifies their absence before propagating the setup failure. The
offline self-test injects post-accept failures, ownership races, surviving
resources, rollback failures, and a daemon mutation that appears only after an
initial absence check. Each Docker CLI runs in a tracked process group; timeout
or interruption terminates and reaps that complete group (privileged from the
first signal under `--sudo`) before reconciliation begins. Rollback then
requires a continuous half-second absence window, removing a late owned
volume/network if the daemon completes an already-submitted request. The live
interruption self-test writes a
marker through
`RUNNER_TOOL_CACHE` in one run, creates a fresh second boundary, proves the
marker is absent there, inspects the effective container mount, and finally
proves interrupt cleanup removes the volume too.

`act` 0.2.89 also names each job's workspace and environment volumes
`act-<workflow>-<job>-<sha256>` and `...-env` from the workflow and job names,
never from a run token, and removes them only inside its own graceful teardown.
Forced process-group containment bypasses that path, and container removal
with `--volumes` drops only anonymous volumes, so an interrupted job used to
leave both named volumes behind. The runner therefore leases those names by
workflow: every selected workflow must declare a `name:` that sanitizes to a
prefix act keeps intact (at most 63 characters of letters, digits, and single
hyphens; act trims the part before the hash to 63 characters), no selected
name may be a hyphen-prefix of another, the boundary records the act prefix
derived from each name, every act command requires that lease, and the runner
refuses before any Docker mutation and again immediately before each act
spawn, in the PR run and in the live gate's three spawns, when any volume
inside the scope already exists or the volume inventory itself fails, naming
the volume and never removing it, because act would otherwise reuse it as the
candidate's workspace or environment. After the process group is proven absent
and owned-container removal has run, cleanup removes each volume inside the
scope without force, requires a stable absence window, and reports any
survivor, any volume another container still holds, and any failed inventory;
after each workflow the runner reconciles before it refuses, so drift observed
on a leftover container is named. A volume outside the scope is never touched:
an act-shaped volume from another workflow survives unless that workflow's
name hyphen-extends a selected name, an anonymous volume leaves with its
container, and a volume an owned container mounted outside the scope is
preserved and reported as lease drift, because only the lease proves this run
created a name: a rival can create a name between a gate's inventory and act's
own create, and act adopts it. The serialization the tool-cache name already
demands of one daemon also covers a rival running the same workflow name
concurrently on that daemon. The offline self-test pins the name derivation to a volume name
a live `act` 0.2.89 produced and pins that no shipping workflow name is a
hyphen-prefix of another.

A freshly created empty tool-cache volume also exposes a Docker daemon race
(#315). Sibling jobs in one workflow start their containers concurrently, and
every container create against an empty volume triggers the daemon's image
copy-up: an emptiness check followed by an unsynchronized directory copy of
the runner image's multi-gigabyte `/opt/hostedtoolcache`. Two creates that
pass the emptiness check together collide inside that copy, and the losing
sibling job dies during container setup with `failed to mkdir
.../act-toolcache/_data/Python: file exists`; a create arriving a moment
later instead sees the winner's first copied entries, skips its own copy, and
runs that job against a partially populated cache. The runner therefore seeds
the cache deterministically: after creating the labelled empty volume and
before `act` may launch any job, one owned seed container with no network
performs the only empty-volume mount, proves through its exit status that the
cache is populated, and is removed with the same owned-only, stable-absence
verification as every other runner resource. Every sibling job container then
mounts a complete non-empty cache and the daemon copy-up can never run
concurrently. Seeding adds that one copy-up (tens of seconds on a warm host)
to boundary creation, including under `--dry-run`, and the seed's own
thirty-minute pull-and-copy budget is bounded separately from ordinary Docker
CLI timeouts. The
offline self-test pins this mechanism as the regression control for the race:
building an act command from an unseeded boundary is refused, the seed must
run exactly once between volume and network creation carrying the ownership
label, the runner image, the exact cache mount, and no network, and a seed
that cannot prove a populated cache refuses the whole boundary and reconciles
both the seed container and the volume. Neutering the seeding call fails
those controls, so the race cannot silently return.

The artifact and cache servers bind only to the gateway address of the
runner-created bridge, so they are reachable by that run's job containers but
not advertised on the host's routable interface. Each workflow also receives a
freshly allocated nonzero artifact-listener port; act treats zero as random only
for its cache server. The offline self-test checks both bind arguments; actual
artifact transport is covered by the mandatory ready-state full run, whose
evidence must show both four-artifact aggregates downloading through that bridge
gateway. The interruption probe tests cleanup and tool-cache separation, not
artifact transfer. `rtl.yml` deliberately orders those aggregates:
`yosys-portability` directly needs `verilator-suites`. This leaves their
verdicts independent because the later job uses `always()` and still checks its
own workers, while serializing their first use of `actions/download-artifact`
under act v0.2.89. Without that edge, act can race initialization through its
shared action cache and one aggregate can observe no artifacts even after all
workers uploaded them. `scripts/ci_events.py --check` pins the edge and its
self-test removes it as a negative control.

Cleanup is restricted to the exact generated directory, the
labeled tool-cache volume, the act job volumes inside the leased workflow
scope, and the network whose ID, name, gateway, and
ownership label the runner recorded at creation. Mutable leases are registered before the
run directory, cache volume, or network can be accepted; post-create inspection
failures and the function-return handoff therefore still reconcile the exact
resource before propagating failure. Act process creation likewise blocks the
parent handler from unwinding until the returned process handle is stored, so
an interrupt cannot strand a process group between spawn and assignment. It
does not block the signal mask: caught parent dispositions reset on `exec`, and
a real-child negative control proves act inherits all three signals unblocked
and terminates on `SIGTERM`.
After every workflow and on every exceptional exit, the runner inventories
Docker, selects only containers carrying that token, attached to that network,
or sharing an owned container's network namespace, then stops and forcibly
removes them. It verifies that no owned container remains, then independently
attempts and verifies removal of the network, the tool-cache volume, and the
leased job volumes so a failure inspecting one cannot suppress teardown of the
others. After a workflow exits, a leftover owned container or job volume is
removed and refuses the run. Only then does
sudo ownership recovery and recursive run-directory removal begin. Any
unverifiable absence changes an otherwise green run to exit 2. `SIGINT`,
`SIGTERM`, and `SIGHUP` all unwind through this cleanup and retain their
conventional `128 + signal` exit status after cleanup (`130` for `SIGINT`). The
top-level Python handler only records the first signal and raises the cleanup
request; it does not change a signal mask or disposition during delivery, so a
deferred-signal race cannot escape the handler. Repeats of all three become
harmless until every nested cleanup and absence check completes; a first signal
that arrives after cleanup has already begun is blocked and delivered only after
that cleanup scope exits. The offline self-test injects failures into the mask
and disposition APIs while delivering a real `SIGINT`, and requires the handler
to avoid both APIs, return 130, and print its attributable post-cleanup
diagnostic. A synchronized process-directed `SIGINT` separately targets a
runner blocked on a non-cooperative child tree and requires the entire recorded
process group to be absent before the runner returns.
Every runner-created worker inherits those signals blocked, preventing the
Python handler from being dispatched through a monitor thread while main is in
a protected cleanup tail; the offline gate sends a process-directed signal with
a live worker and proves cleanup finishes before the conventional exit status.
The monitor's cancel, join, completion event, and dead-thread proof form another
protected cleanup tail, including when the first signal arrives during a join.
An operator interrupt first terminates and reaps the whole `act` process group.
Sudo launches use
privileged group signaling from the first signal rather than relying on a
partial unprivileged `killpg`, and privileged `kill -0` must prove no root group
member survived before Docker teardown begins. If kill or `kill -0` temporarily
fails, the runner enters a containment hold: bounded commands keep retrying and
Docker teardown remains paused until absence is actually established, with the
PGID and operator recovery action printed. Docker-daemon-owned containers are
independently contained by the same verified cleanup.

The sharded exhaustive workers (sixteen Verilator, four Yosys) carry their
checked denominator through the singleton `matrix.total` dimension.
`scripts/ci_events.py` proves that value
equals the `matrix.shard` list length and that every job name and shard command
uses it. Sharded matrices may not use `include` or `exclude`, because either can
change the produced job set independently of that list and carrier. This retains
GitHub's worker counts and avoids the negative `strategy.job-total`
values produced by `act` 0.2.89 without a local workflow edit.

Local success is early exact-head evidence, not a locally manufactured GitHub
status. The runner does not publish commit statuses, and the seven hosted
contexts in the protected merge bar below remain mandatory. Continue useful
local validation or review while they run; do not spend the interval polling
an unfinished hosted run.

### Parallel replay slots

On one Docker daemon, replays are serial. `act` 0.2.89's global names (the
`act-toolcache` volume, and the job volumes and job containers named from
workflow and job names) make a second concurrent replay on that daemon refuse,
as described above. `--slot N` runs a replay against a daemon of its own
instead (#532):

```sh
python3 -I /absolute/path/to/trusted-dev/scripts/act_ci.py --pr <number> --cpu-ranges "$BOOKED_CPU_RANGES" --sudo --slot 1
```

Slot 0 is the default and means the default local daemon, so a command without
`--slot` is exactly the replay described above. Slots 1 to 63 each start a
Docker daemon that the runner owns for one invocation, which requires `--sudo`.
The environment never selects a daemon. In every Docker-using mode, the runner
refuses an invoking environment that sets `DOCKER_HOST`, `DOCKER_CONTEXT` or
`DOCKER_CONFIG`. That includes slot 0, where those variables used to be
silently dropped. The Docker CLI and `act` receive a slot's socket only as an
assignment the runner makes from the slot number.

An isolated slot N consists of the following, in the order the runner creates
them:

- An exclusive host-wide lock, `/run/lock/milan-act-slot-N.lock`. A PR run
  takes it once the PR head is fetched and materialized, just before the
  slot's resources are created, and holds it until the slot's teardown ends.
  The file is created once through sudo and never replaced. A slot that
  another invocation holds refuses at that point, after the fetch rather than
  at startup, and nothing of the slot is touched.
- The network namespace `milan-act-slot-N`.
- The top-level slice `milan_act_slot_N.slice`, capped as a runtime property
  at `MemoryMax=36G` with no swap (`SLOT_MEMORY_MAX`).
- The uplink unit `milan-act-slot-N-net.service`. `pasta` configures the
  namespace from the host's addresses and gives it outbound connectivity
  through socket-level NAT. It forwards no port in either direction and does
  not map the gateway to the host's loopback, so connectivity needs no host
  firewall change.
- The runner's own nft table `inet milan_act_slot_N`, created whole or not at
  all. The uplink is the slot's only socket owner on the host, so every
  connection a slot job makes is one the host originates, on the host's
  output path. Two output rules match traffic from the slot's cgroup:
  - the first rejects every host-local address: the host loopback, the
    default daemon's bridge gateways, and any other replay's artifact and
    cache servers;
  - the second rejects whatever the host would send out of any interface but
    its uplinks, the interfaces carrying its unicast default routes, which
    the runner reads (`ip -json -4|-6 route show default`) before it creates
    anything. That covers a container behind any Docker bridge, a port Docker
    publishes on a host address (Docker rewrites the destination before this
    filter runs), and any other local bridge, tunnel or VM network.

  Docker isolates its bridge networks from each other only on the forward
  path, which host-originated traffic never takes. Without the second rule a
  slot reached the default daemon's containers, including a concurrent slot-0
  replay's job containers, which slot 0's own jobs cannot reach.
  DNS and the internet stay reachable through the uplinks. The slot resolves
  names through the host's configured nameservers, so those must be reached
  through an uplink and must not be addresses of the host itself. A host
  with no usable default route refuses the slot before anything is created.
  For the same reason, an operator's egress policy in Docker's `DOCKER-USER`
  chain, which sees only forwarded traffic, applies to slot 0's jobs but not
  to a slot's. A host that restricts job egress there must also restrict the
  host output of the slot slices, or its slots are less restricted than
  slot 0.
- The daemon unit `milan-act-slot-N-dockerd.service`, inside that namespace
  and slice. It has:
  - its own data-root `<slot-root>/slot-N`, exec-root, pidfile and socket
    `/run/milan-act-slot-N/docker.sock`;
  - its own containerd: the unit masks `/run/containerd`, so dockerd starts
    its own instead of attaching to the system containerd that the default
    daemon uses;
  - its own containerd namespaces and the address pool `10.231.N.0/24`, with
    no default bridge;
  - `/dev/null` as its configuration, so no host `daemon.json` applies;
  - the host service manager as its cgroup driver, with the slot slice as
    every container's parent;
  - labels carrying the slot number and the invocation's unpredictable token.

  Its own iptables management stays enabled and exists only in the slot
  namespace.

The units, the slice and the cgroup driver belong to the build host's service
manager, not to the product (#259's host-tooling non-goal, recorded for the
runner in #376). The bare-metal scope gate, `scripts/check_baremetal_only.py`,
therefore masks the runner's unit executable, its dockerd cgroup-driver value
and its cgroup-mount root only in their exact code contexts in
`scripts/act_ci.py`. The same literals in any other context or file, or in a
product document, are still refused, and the gate's self-test proves each of
those refusals.

The uplink uses the absolute `pasta` path from `SAFE_PATH`.
Its final symlink stays unresolved, preserving the multi-call mode.
Other host tools keep their resolved paths.

Before anything else touches the daemon, `docker info` through the slot socket
must report the slot label, the invocation token and the slot data-root. The
Docker CLI and `act` then both run under
`nsenter --net=/run/netns/milan-act-slot-N`, and the two sudo prefixes stay
identical apart from the executable. So `act` binds its artifact and cache
servers to the slot network's gateway inside the slot namespace, where neither
the host nor another slot can reach them. Because every global act name now
lives in the slot's own daemon, all of the following apply per slot unchanged:
the tool-cache refusal and seeding, the job-volume lease, the owned-container
cleanup, the absence windows and the interruption reconciliation above. A
replay in one slot cannot collide with a replay in another.

Resource bounds:

- CPU ranges are explicitly booked through `--cpu-ranges`.
  Slots isolate daemon resources, not host CPU allocations.
  Every concurrent replay must receive disjoint booked ranges.
- Four containers at eight GiB plus four GiB for daemon and service overhead
  fit the isolated slot's 36 GiB cap. This leaves room on the 61 GB shared
  host, but is not a reservation of all remaining host memory. Slot 0 has
  per-container limits; only isolated slots enforce the aggregate slice cap.
- Four concurrent real Yosys shards at sixteen CPUs each passed with cgroup
  peaks of 2635010048, 1635954688, 889298944 and 646090752 bytes. The sum of
  peaks, 5806354432 bytes, bounds that sample at 5.41 GiB. No memory-limit or
  OOM event occurred. An earlier two-GiB trial killed the largest shard, so
  that cap was rejected. This sample validates the proposed workload budget;
  it does not prove an upper bound for every future compiler or campaign.
- The publication census at four driver workers passed in 558.192 seconds
  with a cgroup peak of 5738594304 bytes (5.34 GiB) and no memory-limit or
  OOM event. Its earlier four-GiB trial killed an elaborator; the eight-GiB
  job cap accommodates this larger measured peak.
- A run with an OOM at the slot cap is refused, never reported as a verdict.
  After the workflows, the runner reads the slice's own `memory.events.local`,
  which counts only the slice's limit and never a job container's eight-GiB limit
  below it. Any `oom` there is exit 2 naming the cap, so an OOM at the cap
  cannot pass for the candidate's `FAILED`.
- That OOM is all the runner detects. Before one, the host reclaims memory
  at the cap, which can slow a job until its workflow times out. No `oom` is
  raised either for an allocation that fails without trying the OOM killer,
  such as a large contiguous one or one whose caller asked not to retry. A
  run hurt either way keeps its verdict, so a slot's `FAILED` can still be
  the cap's. After the workflows the runner prints the slice's memory peak
  and its `max` count, the number of times usage hit the cap. Usage includes
  cached file data, which the host reclaims at the cap as a matter of
  course, so a long run can show a nonzero count with no harm done. Those
  two numbers are the only sign of such harm, so replay a slot `FAILED` with
  a nonzero count in slot 0 before attributing it to the candidate. The cap's
  effect on the shipping workflows has not been measured yet; the run logs of
  the live proof below record each slot's peak and count.
- Slot 0 keeps only its per-container bounds. Whoever allocates slots keeps
  the concurrent caps, plus what slot 0 uses, within host RAM.

`--slot-root` (default `/var/lib/milan-act-ci`) holds every isolated slot's
persistent data-root. It and every directory above it, from `/` down, must be
a root-owned real directory (not a symlink) that is not writable by group or
other. Otherwise whoever controls an ancestor could redirect the root daemon's
data-root between the check and the daemon's start. The runner never creates
it; create it once with `sudo install -d -m 0755 -o root -g root <slot-root>`.
A filesystem mounted on a directory owned by a user can still hold a slot
root through a root-owned bind mount.

The data-root is the slot's image cache and the only slot resource kept between
invocations. It is not shared with the default daemon, because a shared
containerd would put every slot in that daemon's failure domain and on its
filesystem. The first use of a slot pulls the runner image; a `--dry-run`
primes it, because a dry run seeds the tool cache. Measured for
`catthehacker/ubuntu:full-latest`, that is about 19 GB of downloaded content
and about 56 GB unpacked: roughly 75 GB of disk per slot, pulled again
whenever the image changes.

Teardown runs on every exit, including a handled signal and a failed setup. It
runs after the Docker boundary's own teardown and before the run directory is
removed, and each step runs independently:

1. Stop the daemon unit, which takes its containerd and containers with it.
2. Stop the uplink.
3. Stop the slice, which ends anything still in it, and revert its cap.
4. Delete the table.
5. Delete the namespace.
6. Release the lock.

The runner then proves each resource absent:

- both units are unloaded;
- the runtime directory and the uplink's PID file are gone;
- the slice is inactive, with no cgroup and no runtime cap;
- the table and the namespace are gone.

An absence it cannot prove turns the run into exit 2, naming the slot and the
recovery commands. Each resource is recorded as attempted before the command
that creates it, so a create that is interrupted or fails midway is still torn
down. Holding the lock is what makes a resource under the slot's names this
invocation's own.

A dead invocation (`SIGKILL` or a host crash) can leave resources under its
slot's names. The next invocation of that slot finds them after taking the
lock, refuses before any mutation, adopts and removes nothing, and prints the
recovery commands:

```sh
sudo systemctl stop milan-act-slot-N-dockerd.service milan-act-slot-N-net.service milan_act_slot_N.slice
sudo systemctl revert milan_act_slot_N.slice
sudo nft delete table inet milan_act_slot_N
sudo ip netns delete milan-act-slot-N
```

Volumes and containers that such a run left inside the slot's data-root are
refused on the next run by the ordinary tool-cache and lease checks. To reset
a slot, delete its data-root (`sudo rm -rf <slot-root>/slot-N`); that costs
one fresh image pull. No slot resource is shared with another slot or with
the default daemon, and the firewall above keeps a slot's traffic off both.

The runner-change bootstrap rule applies to slots as to everything else. A PR
that changes the slot code is validated by the trusted base copy. The new
code's live behaviour is proved with an independently audited install:

- `--interrupt-selftest --sudo --slot N` runs the live interruption gate
  inside slot N, then proves the slot's own teardown.
- `--boundary-selftest` runs on slot 0 only. Its unboundaried arm must see
  the host loopback, and a slot namespace removes that by design.
- [`scripts/act_slot_proof.sh`](../../scripts/act_slot_proof.sh) is the live
  proof of parallel slots, run with the audited install. It records ten
  checks, in order:
  1. the interruption gate in slot A, which must pass and print the runner's
     own line that slot A was then torn down and proved absent;
  2. serial references for two PRs, each of which must complete;
  3. both PRs started together in slots A and B. Both must be seen holding
     their slots at one instant, before either has printed a verdict, and each
     must complete with its serial reference's verdict;
  4. while both hold their slots, the isolation control in each slot. The
     proof starts a listener container on a new bridge network of the default
     daemon, publishing a port on that network's gateway only. From inside the
     slot's namespace, the container's address and the published port must
     both be refused while `--probe-name` (default `github.com`) resolves and
     answers on 443. The same probe from the host's namespace must reach both,
     which shows the targets were live. The container and network are then
     removed and proved absent;
  5. the collision control with isolation: PR B starts in slot A while PR A
     holds it, and must be refused on the slot lock before PR A has printed a
     verdict. PR A must then complete with its serial verdict;
  6. the collision control without isolation: the same on slot 0, the one
     shared default daemon, where PR B must be refused on act's tool-cache or
     job-volume names. That is the collision slots exist to remove, so it is
     always part of the proof.

  A run completes only with exit 0 and a `PASS` line for every selected
  workflow, in order, or with exit 1, `PASS` lines up to the first workflow
  that failed and its `FAILED` line (the runner stops there). A refusal or a
  signal never completes, so runs that executed no workflow cannot prove
  anything. The proof prints `PROVED` and exits 0 only when all ten checks
  recorded `PASS`. It calls `sudo -n` itself for the default daemon's Docker
  CLI and for the probes, which run as root with a fixed PATH, in the slot's
  namespace or the host's. The probe's name lookup uses the host's resolver
  configuration; the replays themselves, whose image pulls and fetches run in
  the slot, are the end-to-end DNS evidence. The listener image
  (`--probe-image`, default the runner image) must already be on the default
  daemon, which the slot-0 serial references ensure; it is never pulled.

  `scripts/act_slot_proof.sh --selftest` grades those checks offline against
  a stand-in runner and a stand-in `sudo` in a scratch directory, with no
  Docker, privilege or network. It passes only when the honest case (in which
  one PR fails a workflow) proves, when every bad start is refused with exit 2
  before any check records anything, and when every broken case fails on the
  check meant to catch it. The bad starts are a slot that is not a number,
  slots A and B equal or either of them slot 0, a runner that is not the
  recorded digest or is group-writable, and a log directory that is not
  empty. The broken cases take away, one at a time, what the checks require:
  - a completed run: runs that refuse after taking their slots, a run that
    stops early, and runs refused after passing or after failing their
    workflows, graded at the serial reference, the parallel comparison and
    the collision holder;
  - the interruption gate: no teardown line for its slot, no `PASS` line, or
    a refusal after both;
  - the parallel runs: a verdict slot A or slot B changed, runs that never
    overlap, runs that never report their own slot daemons, and, for each
    run in turn, one that dies before taking its slot while the other holds
    its own, and one refused after taking its slot before the other takes
    its own. Each of those last four leaves exactly one of the overlap
    check's four conditions to catch it;
  - the isolation control: a target that cannot be started, a slot that
    reaches the container or the published port, slot B alone reaching the
    container, a slot that cannot reach `--probe-name`, a dead target, a host
    that cannot reach the container or only the published port, and a
    container or network that survives its removal or cannot be queried
    after it;
  - the collisions: a missing slot lock, a rival refused late, for another
    reason, or for the lock but with exit 1, a holder that changes its
    verdict, a shared daemon that does not collide, and a slot-0 rival
    refused for neither the tool cache nor a job volume.

  Where the proof judges runs while they hold their slots, the stand-in runs
  wait for that judgment rather than a timer. A parallel run holds its slot
  until the proof has failed the overlap check or recorded both isolation
  controls. A collision's holder holds its slot until the rival's run has
  returned, then for a fixed time that covers only the proof's next check,
  and a rival meant to be refused late waits for the holder to exit. So no
  case's grading depends on how fast a run starts. The case whose runs
  never overlap is the exception: its runs hold for a fixed time, in
  whichever order they start. The proof fails it in either order, but which
  overlap condition fails depends on the order, so each condition also has
  a case of its own.

  Two guards have no case. The ten-`PASS` count behind `PROVED` is a backstop
  that no case reaches, because a check is skipped only after another has
  recorded a `FAIL` (the isolation control after a failed overlap). The
  install check's refusal of a runner the non-root invoker can write although
  no write bit is set is not staged. A non-root user can write such a file
  only with a capability that overrides file modes, such as one kept inside
  a user namespace, or on a file system that does not enforce the mode, and
  the self-test depends on neither. Run the self-test before the live proof:

```sh
scripts/act_slot_proof.sh --selftest
scripts/act_slot_proof.sh --runner <audited-install>/act_ci.py \
  --sha256 <recorded-64-hex-digest> --act-bin <absolute-act-0.2.89> \
  --logs <new-log-directory> \
  --pr-a <number> --worktree-a <clean-checkout-at-its-head> \
  --pr-b <number> --worktree-b <clean-checkout-at-its-head> \
  --slot-a 1 --slot-root-a <slot-root> --slot-b 2 --slot-root-b <slot-root> \
  --cpu-ranges-a "$BOOKED_CPU_RANGES_A" --cpu-ranges-b "$BOOKED_CPU_RANGES_B" \
  [--workflow <name>]... [--probe-image <local-image-with-python3>]
```

The offline self-test of the runner pins:

- externally booked aligned CPU ranges and the host CPU boundary;
- the inherited-endpoint refusal, for each variable, in the PR run, the dry run
  and both live self-tests, before any collaborator runs;
- slot 0's environment, prefixes and act command, unchanged;
- slot N's derived names, which are disjoint across slots and identical for
  one slot, together with its endpoint parser and namespace prefix;
- disjoint per-job CPU bookings, retained from creation through cleanup;
- the uplink, daemon, firewall and every other host command and query, word
  for word, and the uplink discovery: which default routes count, and its
  refusals of no route, loopback, an unquotable name, malformed output and a
  failed query;
- acquisition order, and rollback of exactly the attempted resources at every
  step;
- the identity refusals, a busy lock, and each kind of residue, including a
  unit left in a failed, masked or transitional state;
- each kind of survivor the teardown proves absent: the daemon and uplink
  units, the runtime directory, the uplink's PID file, an active slice, its
  cgroup, its runtime cap, the table and the namespace;
- each proof whose query cannot answer, at residue time and at teardown,
  refusing rather than reading as absent;
- teardown running with every cleanup signal blocked, and an interrupted
  start;
- the memory cap: one OOM at the cap with no kill in the slice's own events,
  two OOMs, and unreadable or malformed events or either count missing, each
  refused after the whole slot is torn down; the peak
  and the number of cap hits printed; a `FAILED` run whose slice sat at the
  cap without an OOM keeping its `FAILED`; and a body that raises keeping its
  own error;
- the slot root and every directory above it, as checked on acquisition;
- the real lock's exclusivity, root-owner check (including its production
  default) and symlink refusal, the dangling-symlink probe, and the host
  command wrapper's `sudo -n`;
- the live interruption gate running in the slot the command line names,
  entered before act is resolved.

## Protected merge bar

The active repository ruleset named `dev merge bar` applies only to
`refs/heads/dev`. It has no bypass actor and enforces four rules:

- changes arrive through pull requests;
- branch deletion is forbidden;
- non-fast-forward updates are forbidden;
- these seven exact status-check contexts are required: `rtl-fast`,
  `docs-check`, `wire-accountability`, `docs-check-no-git`, `elaborate`,
  `verilator-suites`, and `yosys-portability`.

Required checks use the loose policy: an intervening merge to `dev` does not
force the PR to rerun the 23--26 minute `milan_datapath` Yosys job merely to
become current with the base. Reviewers still own exact-head and candidate-
merge validation under [CONTRIBUTING.md](../../CONTRIBUTING.md).

Conditional job skipping is part of the contract. A documentation-only PR
(the documentation classes in [Fast feedback](#fast-feedback)) must emit the two
exhaustive aggregate checks as skipped and must complete the
fast aggregate and `elaborate` check after their expensive steps skip. That is
permitted only when `full-ci-gate` itself succeeds and explicitly publishes
`run_full=false`; a gate failure, cancellation, or missing output makes both
aggregates run and fail on absent evidence, because a skipped required job
would otherwise satisfy the ruleset. Do not add workflow-level `paths`,
`paths-ignore`, or branch filtering to any required context: a workflow that
never starts leaves its required name pending. The three documentation jobs
are independent required siblings, so a failure in `wire-accountability` or
`docs-check-no-git` blocks the PR even when `docs-check` itself succeeds.
`scripts/ci_events.py --check` pins the complete generated job graphs and
the original ordered gate commands. Exactly one job carries each required name.
The independent `wire-accountability` and `docs-check-no-git` jobs retain their
unconditional execution. `docs-check` and `elaborate` are fail-closed aggregates
over two workers each. Their `always()` condition also runs the verifier after
a dependency fails or is cancelled. Missing, failed, cancelled and skipped
worker jobs all fail the aggregate.

The source inventories are `.github/ci-templates/docs.yml` and
`.github/ci-templates/elaborate.yml`. Edit those templates and run
`python3 scripts/ci_gate_workflows.py`; the workflow files are generated.
The generator preserves every original command, condition and environment.
It puts the 1065-second docs builder gate on one worker and the other gates
on the other. Elaboration separates its 1441-second builder gate from the
593-second standalone simulation aggregate. These are measured baseline step
windows; setup and evidence collection add to each worker's duration.
Workers have 27-minute limits and their aggregates have three-minute limits.

Each worker records the source gate IDs and the actual step outcomes reported
by the workflow runtime. The aggregate recomputes the inventory from the same
template and requires its exact union, with each gate executed once. Receipts
bind the full head, tree and template digest. The existing documentation-only
elaboration skip remains valid only with a recorded false scope and matching
skipped outcomes on both workers. It does not excuse a skipped worker job.
`ci_gate_workflows_selftest.py` drops one gate from every claim, corrupts source
identities and plants each unsuccessful job outcome; all must be refused.
The CI contract applies its original negative controls to the template steps
and separately mutates every generated worker and aggregate step.

Each workflow has a same-repository failure watcher and a terminal failure guard.
Only those two guarded jobs request `actions: write`, on a push or a PR whose
head belongs to this repository. The watcher reads actual job outcomes,
including the manifest collector, and cancels active runs of all four workflows
at the same head after a confirmed failure. The collector needs the original
jobs but not the watcher, so collection failures cannot hide behind a cycle.
The terminal guard needs the watcher and collector and catches failures in their
final evidence steps. Observer errors are reported separately and never authorize
cancellation; an evidence-tail failure after an observer error still does.
Fork PRs keep
native matrix cancellation and fail-closed aggregates; they never enter the
write-token job and do not cancel sibling workflows. There is no privileged
`workflow_run` controller. A cancellation may interrupt artifact upload; missing
evidence stays incomplete and can never compare as a valid build.

The watcher accepts a skipped matrix's raw expression name only when the API
reports that job completed and skipped. Its expansion comes from the generated
matrix; expanded and unexpanded results cannot both cover the same leg.
Controls retain the raw matrix names observed in run `38273578232`.
Each first-failure conclusion has a separate control: failure, cancelled,
timed_out and action_required.

Polling uses a 120-second interval. Four workflows use 120 polls per hour per
head; four concurrent heads use 480, leaving 520 of the documented
[1000 requests per hour per repository](https://docs.github.com/en/rest/using-the-rest-api/rate-limits-for-the-rest-api)
for collection, startup, retries and other operations when each job list fits
one page. Pagination adds requests and is never truncated. Read errors use at
most four attempts and a 600-second retry budget, with exponential backoff.
Both Retry-After and X-RateLimit-Reset are honored; a reset beyond the budget
ends observation without cancellation. HTTP 403, 429, 5xx and timeouts never
become failed-job conclusions. A successful response with no remaining quota
also delays the next read until reset. More concurrent work can exhaust the
shared allowance; the observer then reports unavailable rather than cancelling
healthy jobs. Detection latency is normally at most one polling interval plus
API latency, and can be longer during backoff.

Local replay uses one scheduler and stops its execution group at the first
failed job before cleaning owned containers and volumes. A queued job cannot
enter after failure. Repeated nested-matrix controls prove the global limit,
no later admission and joined cleanup; the no-failure control runs every leg.
Transport controls prove same-head sibling selection, fork zero-write behavior,
actual step/job mapping, cancellation and refusal of identical incomplete
manifests. See [CI execution signatures](CI_SIGNATURE.md) for the collector
schema, trusted helper pins and the remaining round-two authentication work.

The install caches have no broad fallback. Markdown downloads bind the renderer
versions, the hash-pinned requirements and the workflow recipe digest. LiteX
downloads bind the exact Git revisions in `litex_pins.txt` and the recipe digest.
The Scala cache binds sbt 1.10.7, the release archive SHA-256, the LiteX pins and
patches, and the recipe digest. The sbt archive is verified before extraction,
including after a cache hit. Generated CPU metadata also binds the workflow
recipe, in addition to the existing configuration, source, pin and patch inputs.
The workflow-file hash is conservative: an unrelated workflow edit may miss
the cache, but a changed installation command cannot reuse its predecessor.

The install-cache generator also covers every ordinary Python download,
verified sv2v archive and pinned field-oracle build. `ci/constraints-ci.txt`
fixes CPython 3.12 Linux x86_64 package URLs with exact versions and SHA-256;
`PIP_CONSTRAINT` applies them without changing any gate command. The download
cache key binds that complete source list, the existing requirements and LiteX
pins, and the generator/workflow recipe. sv2v's archive is verified on every
use, including cache hits. Its key binds v0.0.12 and the archive SHA-256. The
field-oracle cache binds its exact Git revision and the installation recipe;
the original checkout, submodule initialization and build still execute.

Distribution installs retain their existing package selection. Before each
ordinary install, `ci_install_cache.py` refreshes the package index and asks
APT for its exact download plan. The key contains separate digests of the
resolved versions, every archive URL/size/SHA-256, and the original install
recipe, plus the generator/workflow digest. Installation uses that prepared
index and a private archive directory; APT still verifies every archive.
The earlier index-update command is replaced only because preparation already
ran it. A conditional package fallback embedded inside a test remains intact.
Package metadata and resolver failures refuse setup. The install-cache controls
change each identity component and reject missing source hashes, duplicates,
broad fallback keys and changed cache paths. Test command bodies and their
conditions remain byte-identical under this transformation.

The cache controls remove each version, source and recipe component and add a
broad fallback; every altered key must be refused.

## Issue closing on merge

Since `dev` became the default branch on 2026-08-22, a PR body carrying the
GitHub keyword form `Closes #N` closes Issue N when the PR merges into `dev`.
The PR template therefore carries separate `Closes #` and `Relates to #`
lines; its former `Closes/relates to: #` line was not a form GitHub reads, and
a body written that way leaves the Issue open.

A closed Issue is not a finished one. The project board's Done transition
still waits for the post-merge containment check that
[CONTRIBUTING.md](../../CONTRIBUTING.md) requires, run when the branch has
stopped moving; an Issue the merge closed whose card is not Done is in that
window. `scripts/check_merge_review_integrity.py` keeps reporting a merged PR
whose linked Issue is open, for bodies in a form GitHub does not read and for
the history before 2026-08-22, when every PR merged into a non-default branch
and the keyword never fired.

Containment reports the proof named beside each verdict.
Ancestry and linear replay prove historical inclusion.
Later reversions leave those historical verdicts unchanged.
The optional `--current-retention` arm separately assesses linear replay retention.
Its unsupported histories and unproved paths remain `UNKNOWN`.
The [containment contract](../../CONTRIBUTING.md#21-the-issue-to-merge-lane)
defines the bounded proofs and their exit codes.

## Local commands

Sharding is a hosted-runner scheduling detail. The no-option commands remain
complete serial local gates:

```sh
suite_logs=$(mktemp -d)
scripts/run_all_suites.sh "$suite_logs"
syn/yosys/run.sh
```

Useful read-only inspection commands are:

```sh
scripts/run_all_suites.sh --ci-pieces --shard 0/16 --list
scripts/run_all_suites.sh --ci-pieces --shard 15/16 --list   # continuous media-clock history
syn/yosys/run.sh --list
syn/yosys/run.sh --shard 0/4 --list
```

The tsn-gen field campaigns in `tb/verilator/tsn_fuzz/` read
`TSN_GEN_ROOT` (default `~/tsn-gen`). Check that tree out at the revision
the exhaustive workflow pins as `TSN_GEN_REV` before recording local
campaign evidence: the freshness gate compares each committed
`TEST_RESULTS.md` with a run at that revision, so a report regenerated
at another one is not the report the hosted gate judges.

The elaboration gates run locally against any interpreter that imports
LiteX; without one they skip and the verdict says so:

```sh
MILAN_LITEX_PYTHON=$HOME/litex-milan/venv/bin/python3 \
  python3 sw/builder/test_builder.py --require-elaboration
```

The fast Yosys mode is diagnostic only:

```sh
syn/yosys/run.sh --mode elaborate --no-structural \
  --top milan_datapath --top KL_pp_shadow --top KL_gptp_shadow
```

The bare-metal firmware's host suites run locally as `firmware-unit` runs
them, and the TSN stack boundary as `firmware-boundary` and `firmware-verilator`
run it together. F4 fetches the pinned lwSRP and tsn-c-stack submodules and installs the pinned SDK before
the required RV32 control build and its `--self-test` mutation campaign.
The saved-state campaign remains a local `--self-test` addition, and the
tally listener's campaign uses `--mutants`
([the harness page](../../sw/firmware/gtest/README.md#run)):

```sh
python3 sw/firmware/gtest/tally_selftest.py --mutants
python3 sw/firmware/ctrl/test/test_ctrl_firmware.py --require-rv32 --self-test --lwsrp <lwSRP checkout>
python3 sw/firmware/ctrl/test/ctrl_boundary.py --require-rv32 --selftest
python3 sw/firmware/ctrl_nvm/test/test_ctrl_nvm.py --require-rv32 --self-test --jobs 16
python3 sw/firmware/gtest/fw_coverage.py --selftest
python3 sw/firmware/gtest/fw_coverage.py --check --lwsrp <lwSRP checkout> --jobs 16
```

The hosted control phases can also run separately:

```sh
python3 sw/firmware/ctrl/test/test_ctrl_firmware.py --require-rv32 --self-test --jobs 4 --shard 0/4
python3 sw/firmware/ctrl/test/test_ctrl_firmware.py --require-rv32 --self-test --jobs 4 --shard 1/4
python3 sw/firmware/ctrl/test/test_ctrl_firmware.py --require-rv32 --self-test --jobs 4 --shard 2/4
python3 sw/firmware/ctrl/test/test_ctrl_firmware.py --require-rv32 --self-test --jobs 4 --shard 3/4
python3 sw/firmware/ctrl/test/test_ctrl_firmware_shards.py
python3 scripts/ci_events.py --firmware-census
```

Run all four phases to reproduce the complete control gate.
Shard arguments cannot combine with coverage or mutation slicing.

The fast workflow derives `--jobs` from its visible CPU count, capped at four,
for lint, publication census, saved state and coverage. Python 3.12 reports the
host CPU count even inside a container with a smaller affinity set. Using
`nproc` and an explicit pool width preserves every check while bounding memory.

## Failure and cancellation semantics

A worker is not trusted merely because an aggregate job was able to download
something. Both aggregate jobs refuse evidence recorded for any tree but the
run's own (see [One authoritative SHA](#one-authoritative-sha)), compare
artifacts with the live repository inventory, and separately require every
worker result to be `success`.

Workflow concurrency retains the PR number or branch ref.
Push/PR runs share the default category; newer updates replace older runs.
A force-push to a PR branch is the same `synchronize` event under the same PR
number, so it cancels the superseded run like any other push.
Schedule/dispatch runs share a separate physical category for each ref.
A newer physical run replaces an older physical run.
Pushes cannot cancel physical evidence without starting a replacement.
`ci_events.py` pins this separation and tests its removal.


Push validation on `dev` checks the actual merge result. It complements, but
does not replace, the explicit post-merge containment check required by
[CONTRIBUTING.md](../../CONTRIBUTING.md).

## Source-tool cache provenance

Verilator and Yosys cache keys include three provenance inputs.
The release version remains explicit in workflow environment variables.
An immutable source commit follows that version in each key.
The build verifies that commit before configuration or compilation.
The recipe digest covers every committed workflow definition.
Operating-system identity also separates these cached installations.
No fallback restores another version, source, or recipe.
The CI contract pins these complete cache keys.
Its controls remove each provenance input and require refusal.

Verilator v5.050 uses source commit `848d926ebd4addacacd294dc84e35d9d4ae8078c`.
Yosys v0.66 uses source commit `86f2ddebce7e98ce7cacc27e8a5c14cb53b51b51`.
These are Git object digests, verified after the release checkout.
A changed workflow invalidates the recipe digest automatically.
Cache hits still require the existing installed-version checks.
