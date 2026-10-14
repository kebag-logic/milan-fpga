[R636] NEGATIVE - exact head 84ee9ea119b548b4982d2c0988d8753a2ce4d0cf

# R636-3: internal cleared-context delta review of PR #739 (issue #737, round 3)

- **Head.** `84ee9ea119b548b4982d2c0988d8753a2ce4d0cf`, tree `4d44778bb1074178effb49e07480a33d95e8fd6d`. The PR head on GitHub is this commit.
- **Range.** The round-3 delta is `2658a64c..84ee9ea1`: 12 commits and 24 files. All of them are CI workflows, CI templates, CI scripts, `ci/constraints-ci.txt` and `docs/testing/CI_WORKFLOWS.md`. No HDL, testbench or firmware file changed. The full range is `fa7347fc..84ee9ea1`.
- **Scope applied.**
  - The round-3 ruling [6176299708](https://github.com/kebag-logic/milan-fpga/issues/737#issuecomment-6176299708), items 1-7.
  - The author's READY [6180445253](https://github.com/kebag-logic/milan-fpga/issues/737#issuecomment-6180445253).
  - The standing rulings: the scope change 6166823105, the CPU rules 6166855177, and the measurement permission 6172868895.
  - AGENTS.md, CONTRIBUTING.md §3 and §6, and docs/README.md.
- **Order.** I reconstructed the task in this order: contract, issue and rulings, the delta diff and history, then public evidence. My findings and lens results were fixed before I read the round-2 public reviews R637-2 (6175565890) and R636-2 (6176284934). The reconciliation below came after that. I read no private author material and no other round-3 reviewer report.
- **Coverage.** All five lenses were applied, each with artifact-specific evidence.

## Verdict basis

One MINOR finding is open, under Tests, so the verdict is NEGATIVE. The cause of every round-2 finding is closed at this head; each was confirmed by execution or mutation:

- **Inventory preparation.** Every inventory reader, `ci-manifest` included, prepares its pinned dependencies. The generator refuses an unprepared reader. A fresh checkout with no submodules refuses 3 of 6 inventories before preparation and derives all six after it (19/31/31/66/3/4).
- **Raw skipped matrices.** Raw names flow through the graph, the collector and the watcher. The result is an incomplete manifest with skipped legs, no success and no cancellation. Malformed and overlapping forms are refused. The fixture shape matches hosted run 38273578232 as read today.
- **Observer-only failures.** In both the watcher and the collector, these end with rc 0 and an explicit `observer_only_error`. The manifest is incomplete and no cancellation is granted. Genuine collector, tail and upload failures still cancel. The collector's 15-minute limit is above its 600-second shared read budget.
- **Worker timing.** Every gate and Yosys worker is projected within 60% of its own limit. No arm was removed and no worker timeout was raised.
- **Source tool builds.** These are bounded by `CI_TOOL_BUILD_JOBS`, and the receipts show at least 38.7% reserve.
- **S1, S2 and S4.** Removing each guard now fails its self-test.

The one open finding: the property that keeps collector API reads inside the collector's job limit is a single read budget shared across requests. No control can fail if that property is removed (F1).

## Findings

### R636-3-F1 - MINOR - Tests - `scripts/ci_runtime_evidence_selftest.py:98-126` (`observer_collector_controls`); `scripts/ci_runtime_evidence.py:198`

**Authority:**
- Ruling 6176299708 item 3: "The collector's job limit must exceed its read budget. Inject each failure through the real collector entry point and the generated graph, including a wait longer than the old allowance."
- AGENTS.md §6, Tests: "Each new test can fail for the defect it claims to detect."
- `docs/testing/CI_WORKFLOWS.md:2736-2739`: "Its API reads share one 600-second budget across all pages and run IDs … Individual requests consume that same budget."

**Evidence:**
- **The bound comes from one argument.** The collector's total read time is bounded only because `collect_api` builds `API(..., RETRY_BUDGET_SECONDS)` (`ci_runtime_evidence.py:198`). That makes every request share one deadline (`ci_fail_fast.py:62,71-72`).
- **The control cannot see it.** The shipped control makes every `urlopen` call fail. So collection stops at the first request (`runs/<id>`), and its assertion `elapsed <= RETRY_BUDGET_SECONDS` (line 126) is met with or without the shared deadline.
- **Mutation survives.** Mutation `i3-no-shared-budget` removes the third argument, and `ci_runtime_evidence_selftest.py` still returns 0 (`receipts/mutations/i3-no-shared-budget.json`).
- **The property matters.** Probe P1 drives the production `API` through two requests (`receipts/observer-probe.json`): `runs/1` recovers after two transient failures, then the jobs page never recovers.
  - At this head, with the shared budget, collection gives up after 480 s, or 580 s with `Retry-After: 290`.
  - With the budget removed, the same sequence takes 720 s, and 1,160 s with `Retry-After: 290`. That is past the 900-second collector job limit.

**Impact:**
- A later edit could drop or reset the shared deadline, for example by building `API` per run ID or per page, and every shipped control would stay green.
- The collector would then hit its job timeout during a rate-limit storm. That gives a failed conclusion with no observer-only output, so the tail guard cancels healthy same-head runs.
- That is exactly the R637-2-F3 failure mode that round 3 closed.
- The production code is correct today. Only the control is missing.

**Required outcome:** a control that fails when collector reads stop sharing one deadline. For example, one request recovers late and a later request keeps failing. Assert that total elapsed time stays within `RETRY_BUDGET_SECONDS`, and that the injected waits would exceed it without the shared deadline.

**Verification:** re-apply mutation `i3-no-shared-budget` (`scripts/mutate.py`), and require `ci_runtime_evidence_selftest.py` to return non-zero.

### RESIDUE (wording only; carried to the residue checklist)

- **R636-3-R1.** At `docs/testing/CI_WORKFLOWS.md:2347`, "Source builds use `CI_TOOL_BUILD_JOBS=min(available CPUs, 8)`" is broader than the code. The pinned field-oracle build still runs `cmake --build … --parallel` with no count (`.github/workflows/rtl.yml:374`, unchanged in this round). The measured classes are Yosys and Verilator only.
  - Exact fix: "The Yosys and Verilator source builds use `CI_TOOL_BUILD_JOBS=min(available CPUs, 8)`".
- **R636-3-R2.** The live PR body, line 21, ends "No push occurred." The PR head is now `84ee9ea1`.
  - Exact fix: replace it with "The coordinating role published this head."

### Suggestions (non-blocking)

- **S1** `scripts/ci_suite_workflows.py:30`: the generator check does not count a preparation step that has an `if:` or `continue-on-error`. No control covers that clause. Mutation `i1-conditional-prep-accepted` accepts any preparation and survives `ci_gate_workflows_selftest.py`. Add one planted conditional preparation.
- **S2** `scripts/ci_runtime_evidence.py:231` (and `ci_fail_fast.py` `watch`): every `OSError` counts as observer-only, including non-transient HTTP 401/404/400. P2 shows each raises after one attempt and is caught by that clause. The ruling lists 403, 429, 5xx, timeout and exhaustion. The resulting manifest is still incomplete, which is fail-closed, but a misconfiguration cancels nothing and the job goes green. Consider treating non-transient client errors as genuine.
- **S3** Elaboration workflow span: `elaborate-gates-0` is 1,561 s. The docs-style allowances add 60 s for the aggregate, 60 s for the collector, 120 s for the watcher interval and 30 s for the tail. That projects about 1,831 s, above 1,800 s. `CI_WORKFLOWS.md` records a workflow projection for docs only. Record the elaboration workflow projection too. The 30-minute decision rests on hosted readback.
- **S4** `.github/workflows/rtl.yml:374`: the field-oracle `cmake --build --parallel` has no job count, so GNU make runs unbounded. This is unchanged in this round and unmeasured. Bound it with `CI_TOOL_BUILD_JOBS`, or measure it.

## The author's open risk: docs at 2-6 s over 30 minutes

- **Recorded projection.** The docs projection is 1,776 s, with `docs-gates-1` = 1,386 + 120 s.
- **Where the risk comes from.** It rests on local builder windows. The 1,411-1,416 s figures came from the committed-head banks, shared with the rtl-fast bank.
- **Hosted baseline.** The public hosted baseline (`author-r3/baseline-docs.json`, `7032bca5`, run 38495894291) shows a builder window of 1,065 s. All setup steps before it summed to about 50 s on warm caches.
- **Projection from hosted figures.** On hosted figures, `docs-gates-1` is about 1,065 + 120 = 1,185 s, and the workflow is about 1,455 s (24 min).
- **Judgement.** The 2-6 s overrun is an artifact of local contention, not a defect at this head. It is still a projection, and hosted readback of `docs-gates-1` and the docs span decides. That is a pending manager duty.

## Items at their cause

| Item | Result | Evidence |
|---|---|---|
| 1. Inventory preparation | **Met.** `check_inventory_dependencies` runs inside `generate` for all four workflows. Preparation precedes every reader: `ci-manifest` in all four, unions, `verilator-suites`, `verilator-shards` and `docs-gates-0`. | `receipts/fresh-inventory.json`: before preparation, `milan_dp`, `milan_dp_render` and `pp_shadow` are refused; after the exact generated command, 19/31/31/66/3/4. Mutations `i1-check-noop` and `i1-collector-unprepared` are caught; the latter is caught by three controls. |
| 2. Raw skipped matrices | **Met.** `committed_plan` carries `skipped`. `api_evidence` records each covered leg as skipped with its plan condition, and `observe` accepts the raw name only when it is completed, skipped and step-free. | `receipts/hosted-38273578232-job-shape.json` matches the fixture. Mutations `i2-skip-as-success`, `i2-collector-no-raw`, `i2-collector-overlap` and `i2-watcher-unknown` are all caught. |
| 3. Observer-only failures | **Met in behaviour.** The control gap is F1. Watcher outage gives rc 0. Collector `OSError` gives rc 0, all results `unknown`, `observations.logs.observer_error`, and `observer_only_error` only if collect and upload both succeeded. `tail_failed` exempts both jobs only under that output. A head mismatch still gives rc 1. | Mutations `i3-collector-outage-fails`, `i3-watcher-outage-fails`, `i3-tail-ignores-collector`, `i3-collector-limit` and `i3-collector-no-output` are caught; `i3-no-shared-budget` survives (F1). The shipped controls inject 403, 429 and 502 (480 s each), a timeout (360 s) and 429 exhaustion. P3: the watcher (120 min) outlives the longest push/PR chain in each workflow: rtl 95, rtl-fast 70, elaborate 63. `physical-gptp` is schedule/dispatch-only, and the watcher, collector and tail do not run on those events. Docs shows 375 only because the 9-second `wire-accountability` job has no explicit limit; that is outside the delta. |
| 4. Worker headroom | **Met by recorded projection.** The two contract gates are on `docs-gates-2` (gate IDs 41/42 preserved). Yosys compilation is in `yosys-tool`; the shards download, restore and prove the version, with no dangling `cache-yosys` reference. | `receipts/battery/events-selftest.*`: 5,209 arms, rc 0, 225.5 s at this head under concurrent load, below the 316.686 s the projection keeps. `receipts/events-arm-comparison.txt`: the only 30 arm names absent against `2658a64c` are renumbered or moved generated-step arms, with 146 added. `receipts/timeout-comparison.txt`: only the collector (3→15, required by item 3) and the two new jobs (45, 29) differ. I checked the projection arithmetic for every worker in the `CI_WORKFLOWS.md` table. Mutations `i4-contract-on-worker0` and `i4-yosys-inline` are caught. `docs-gates-2` has only three submodules, and the event contract passes there from a fresh checkout (`receipts/worker2-events-*`). |
| 5. Source builds | **Met.** All nine Yosys and Verilator source builds across the four workflows, including `physical-gptp`, use `-j"$CI_TOOL_BUILD_JOBS"` after the budget step. | The author's public receipts `lane737-r3-{verilator,yosys}-{16,12}-j8.json` give peaks of 4,811,259,904, 4,793,225,216, 5,264,482,304 and 5,117,616,128 bytes, with zero memory events. Reserves are 43.99%, 44.20%, 38.71% and 40.42%, recomputed. Capture at 6,047,100,928 bytes keeps 29.60%. Mutation `i5-unbounded-tool-build` is caught. On a 4-CPU hosted runner, `min(4,8)=4`, unchanged. |
| 6. S1/S2/S4 controls | **Met.** | Mutations `s1-accept-failed`, `s2-allow-skipped` and `s4-drop-single-scope` are each caught. |
| 7. S3, S5(a) | Recorded for the #495 checklist, per the ruling. | |
| `0fd126de` bare-metal fix | **Met.** The two prose lines are reworded. `GO_ARCHIVE.format(sys.platform)` gives the same release archive name as before on the build host. `GO_SHA256` is unchanged, so another OS's archive is refused by digest. No commit in `fa7347fc..HEAD` touches `scripts/check_baremetal_only.py`. | `check_baremetal_only.py --check`: 0 findings over 1,331 files. |

## Host trust boundary (`scripts/act_ci.py`)

- **Runner checksum.** `sha256(scripts/act_ci.py)` at this head is `f968f67655ac386ea703248b724c3781b95ec379d3a5287b378e470df81f895c`, equal to the author's repinning value.
- **The only change.** The only `act_ci.py` change in this round is the `ci_workflow_plan.py` pin.
- **Helper pins.** All three pins equal the files' bytes (`receipts/runner-pins.txt`). `generate_ci_evidence_pins.py --check` passes. Helpers are staged from the runner's own directory (`act_ci.py:5794`).
- **New helper code.** `skipped_matrices` and the `skipped` field reuse the bounded, alias-free `workflow()` parser and `matrix_rows` and `rendered_name`, which already ran inside `expand_workflow` on the same bytes. They add no capability.
- **Result.** I found no trust-boundary change or escape. This is a static audit; the runner and its self-test were not executed.

## Prior public findings at this head

| Finding | Status at `84ee9ea1` | Evidence |
|---|---|---|
| R637-2-F2 (BLOCKER): collector inventories | **Resolved** | Item 1 above |
| R637-2-F1 (MAJOR): skipped matrices end to end | **Resolved** | Item 2 above |
| R637-2-F3 (MAJOR): observer errors authorize cancellation | **Resolved in behaviour, including job-timeout handling.** The collector limit is 900 s against a shared 600-s read budget, and the watcher outlives every watched push/PR chain. Its regression control is incomplete, and that is **retained as R636-3-F1 (MINOR, Tests)**. | Item 3, P1, P3 |
| R636-2-F1 (MAJOR): worker headroom | **Resolved** | Item 4 above |
| R636-2-F2 (MINOR): source-build sizing | **Resolved** | Item 5 above |
| R636-2-S1, S2, S4 | **Resolved** (each mutation caught) | Item 6 above |
| R636-2-S3, S5(a) | **Retained as residue** (#495), per ruling item 7 | |
| R636-2-S5(b): watcher red on exhaustion | **Resolved.** `watch` returns 0 with `observer_error=true`. | `ci_fail_fast_selftest.py`; mutation `i3-watcher-outage-fails` caught |

## Hosted evidence at this head

At 2026-10-14T23:36:02Z the queries returned 0 check runs and 0 workflow runs for `84ee9ea1` (`receipts/hosted-readback.txt`). The PR is `CONFLICTING` with live dev, so no job, executed or skipped, can be read. No span is claimed. The baseline for reference is `7032bca5`: docs 2,039 s for the single job.

## Reviewer-owned ledger

| Lens | CLEAN/UNCLEAN | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | Ruling 6176299708 items 1-7 checked against `ci_suite_workflows.py:21-35`, `ci_runtime_workflows.py:109-131`, `ci_runtime_evidence.py:118-236`, `ci_fail_fast.py:111-166`, `ci_gate_workflows.py:24,60-80,136-172`, the generated `.github/workflows/*.yml` and the `CI_WORKFLOWS.md:2346-2363,2641-2754` claims. Also: `receipts/fresh-inventory.json`, hosted job shape 38273578232, `timeout-comparison.txt`, `events-arm-comparison.txt`, the `0fd126de` diff, `check_baremetal_only.py --check`, and the `act_ci.py` pins | R636-3 | `84ee9ea119b548b4982d2c0988d8753a2ce4d0cf` |
| RTL (CI architecture; no HDL in the delta) | CLEAN | Generated job graphs: the `yosys-tool`→`yosys-shards` needs, conditions, artifact handoff and the `yosys-portability` skip handling (`rtl.yml` jobs `yosys-tool` and `yosys-shards`); `docs-gates-2` step list; CPU budget step order before every `-j"$CI_TOOL_BUILD_JOBS"` (nine builds); watcher and collector limits against the longest push/PR chains (`observer-probe.json` P3) | R636-3 | `84ee9ea119b548b4982d2c0988d8753a2ce4d0cf` |
| Robustness | CLEAN | Observer paths for 401, 403, 404, 429, 5xx, timeout and exhaustion (P1, P2 and the shipped controls); malformed, unknown and overlapping raw forms in the watcher and collector; genuine failure plus observer output (outputs require both collect and upload success); fresh checkout without submodules; `docs-gates-2` with three submodules; shared-budget behaviour of the production code (P1: 480 s and 580 s, both at most 600 s) | R636-3 | `84ee9ea119b548b4982d2c0988d8753a2ce4d0cf` |
| Tests | **UNCLEAN (F1)** | Battery of 19 controls at this head, all rc 0 (`receipts/battery/`), including `ci_events --selftest` with 5,209 arms. 19 targeted mutations (`receipts/mutations/`): 17 caught; 2 survived (`i3-no-shared-budget`, which is F1, and `i1-conditional-prep-accepted`, which is S1). Arm-name comparison against `2658a64c` (5,093 arms) | R636-3 | `84ee9ea119b548b4982d2c0988d8753a2ce4d0cf` |
| Docs | CLEAN (RESIDUE R1 and R2 carried) | `CI_WORKFLOWS.md:2346-2363` (resource table, recomputed reserves), `:2641-2721` (worker table, projection arithmetic, 1,776 s), `:2724-2753` (observer and skip behaviour, matched to code); live PR body projections; `docs_check`, `check_doc_style`, `check_doc_paths`, `gen_toc --check`, `check_em_dash` (bases `2658a64c` and `fa820988`) and `check_py_idiom`, all rc 0 | R636-3 | `84ee9ea119b548b4982d2c0988d8753a2ce4d0cf` |

## Real limits

- **Not run by this reviewer.** No Docker, act, host runner or `act_ci.py --selftest`. The runner contract gate rests on the author's receipt.
- **Source-build measurements.** I did not repeat the Yosys and Verilator source-build measurements. I checked the author's public receipts and recomputed their arithmetic.
- **Python environment.** Controls ran on CPython 3.12.3 with pure-Python PyYAML 6.0.3, not the pinned 6.0.2 wheel. The renderer-dependent gates ran on the pinned renderer under CPython 3.14.
- **Fresh-checkout probe.** It ran the exact generated preparation command, offline, against the review clone's own module repositories at the pinned commits, not the network origins.
- **Field-oracle build.** Not measured (S4).
- **Projections only.** The timing figures are projections; no hosted after-time exists at this head.
- **No hardware.** Physical calibration was NOT RUN, and field skips are not hardware proof.
- **No manager source bank.** No manager source bank at this exact head exists or is claimed. The author's gate receipts are source-head evidence. The current-dev candidate is separate.

## Pending manager duties

- Resolve the conflict with live dev `f6260253` and build the merge candidate. A commit that touches these CI artifacts un-covers the lenses at that head.
- Publish hosted readback per workflow and job. Include `docs-gates-1` and the docs span (the 2-6 s risk), `elaborate-gates-0` and the elaboration span (S3), and `yosys-tool` cold.
- Run a full trusted replay with per-job peaks, placements and live cancellation. Include `yosys-tool`'s artifact handoff under act.
- Repin the reviewed runner checksum `f968f676…`.
- Run the candidate builder and native banks, get merge authorization, and complete post-merge containment.
- Carry RESIDUE R1 and R2, and #495 S3/S5(a), to the residue checklist.

## Reviewer conduct and checkout integrity

- **No writes.** No source fix, commit, push, GitHub write, merge, author contact, Docker or act run, privilege use or hardware operation.
- **Disposable copies.** Probes and mutations ran only in disposable copies under `scratch/`.
- **Clone integrity.** `receipts/checkout-integrity.json` proves the review clone is byte-exact at the head and tree:
  - all 1,357 tracked blobs match in bytes and mode;
  - the index tree equals the head tree;
  - the five populated gitlinks match their pins, and `external` is uninitialised as at the start (`receipts/integrity-before.txt`);
  - status is empty, including ignored files.
- **Redactions.** Published logs have host path prefixes replaced by `$PACKET`, `$CLONE`, `$TOOLS` and `$HOME`. Mutation log digests are over the published logs.

R636-3 FINISHED
