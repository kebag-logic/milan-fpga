[R636] POSITIVE - exact head 08adb21af0a72d839ce30b6c461503dad269d4d6

Internal independent review R636-4 of issue #737 / PR #739. This is a delta review, `84ee9ea1..08adb21a` (tree `e5cc5d163c974aaf1b6cb888dae9881267d787e6`), on the frozen issue acceptance, the round-4 assignment ([6180908502](https://github.com/kebag-logic/milan-fpga/issues/737#issuecomment-6180908502)), the STOP answer ([6181778634](https://github.com/kebag-logic/milan-fpga/issues/737#issuecomment-6181778634)) with its conditions ([6160937413](https://github.com/kebag-logic/milan-fpga/issues/737#issuecomment-6160937413)), and the author READY ([6183508390](https://github.com/kebag-logic/milan-fpga/issues/737#issuecomment-6183508390)). All five lenses were applied, each with artifact evidence. No BLOCKER, MAJOR or MINOR is open. One wording-only RESIDUE and three SUGGESTIONs are recorded.

This verdict covers the source at this exact head. It does not accept hosted timing, a signed build, a merge candidate or hardware evidence, and it does not authorize a merge.

## Summary

- **R636-3-F1 is resolved.** A production-path collector control now fails when collector reads stop sharing one deadline. Mutation `i3-no-shared-budget` makes `ci_runtime_evidence_selftest.py` return 1 (`collector reads took 960.0s`).
- **S1, S2 and S4 are resolved. Each mutation is killed by a semantic assertion:**
  - S1: a conditional and a `continue-on-error` preparation are each refused.
  - S2: client errors (400, 401, 404) are genuine failures in both the watcher and the collector. 403, 429, 5xx, timeouts and transport exhaustion stay observer-only. Each side has controls in both readers.
  - S4: the unbounded field-oracle build gives 2 `ci_events --check` findings.
- **R1 is resolved.** The `CI_WORKFLOWS.md` text now matches the code.
- **R2 is stale again.** The PR body still says the head "is not pushed", but it is now the published PR head. This is RESIDUE R636-4-R1.
- **S3, the builder split, follows the STOP answer:**
  - Only the driver entry point of `test_builder.py` changed. At the AST level, 0 of 542 top-level statements changed from `fa7347fc` to this head, and the 103-gate run list is identical.
  - The default run is unchanged. On this host, the round-3 driver and this head give the same verdict block. 100 gates print byte-identical output and 3 are identical after masking temporary names.
  - `test_baremetal_profile_contract` runs alone in leg 0.
  - Both requirements are judged on the union of the legs. The union refuses real flag-less leg receipts and names all 15 elaboration gates.
  - The unsharded run and the union of the legs give equal per-gate verdicts and an equal 17-row NOT RUN ledger on this host.
  - The 26.4-minute elaboration projection recomputes from hosted run 38495894212.
- **The runner trust boundary was not re-audited.** `scripts/act_ci.py` is unchanged in this delta (SHA-256 `f968f676…895c`).

## Reconstruction

**Read, in this order:**
- AGENTS.md and CONTRIBUTING.md (merge bar);
- the docs map;
- the issue body: scope, acceptance, the 2026-10-14 scope change and the fail-fast rules;
- the assignment, STOP, STOP answer and READY comments;
- `git diff 84ee9ea1..08adb21a` (14 files, +745/−79) and the history from `fa7347fc`;
- the live PR body;
- hosted runs for this head and for the baseline.

**Published evidence tree `988e9e89`.** It holds only round-1 to round-3 material. No round-4 builder receipts are published there. Source-head execution evidence for round 4 is therefore the author's described receipts plus this review's own execution.

**Prior findings.** The prior round-3 findings (R636-3, R637-3) were read only after this review's own pass over the diff. Another reviewer's round-4 report was not read.

## Findings

### R636-4-R1 - RESIDUE - Docs - PR #739 body, Status section, lines 25-26

- **Evidence:** The PR body reads "This head is not pushed; the coordinating role publishes it." PR #739's head is now `08adb21a`, so the sentence is stale. It is the same class as R636-3-R2. It is wording only: no measurement, figure, verdict, test, code or claim depends on it.
- **Required outcome (exact fix):** replace that sentence with "The coordinating role published this head."
- **Verification:** read the live PR body.

### R636-4-S1 - SUGGESTION - Robustness, Docs - `scripts/ci_builder_legs.py:96-99,163`; `sw/builder/test_builder.py:24611-24617`

- **Evidence:** `union` reuses the driver's `_require_elaboration_verdict`. For a passing union with recorded rows, the `elaborate` aggregate log prints "2 arm(s) did not run for recorded reasons, listed above". Nothing is listed above it in that log (`receipts/union-output-probe.txt`). The rows are named in each leg's own log and in `gate-union.json` (`not_run`), so the information is retained. The author disclosed this as an open risk.
- **Impact:** a misleading pointer in one log line. No verdict changes.
- **Suggested outcome:** print the union NOT RUN ledger before that line, or reword it for the union.

### R636-4-S2 - SUGGESTION - Robustness, Tests - `scripts/ci_suite_workflows.py:21-35`; `.github/workflows/elaborate.yml:565-581`

- **Evidence:** The `elaborate` aggregate now reads the driver inventory (`ci_gate_receipts.py verify` → `ci_builder_legs.inventory()` → `test_builder.py --list`, which imports `yaml`). The generator's reader list does not include that path. At this head the aggregate's pinned-reader step is present and unconditional.
- **Execution:** with only pinned PyYAML and no submodules, `--list` returns the 103 names in 0.4 s (`receipts/agg-list.*`).
- **Suggested outcome:** add the builder-inventory reader to `check_inventory_dependencies`, so that losing its preparation is refused at generation.

### R636-4-S3 - SUGGESTION - Tests - `sw/builder/test_builder.py:29157-29180`

- **Evidence:** No self-test runs the driver's `--gates` refusals (unknown, repeated, out-of-order, empty). This review ran them: all 7 cases return rc 1 before any gate runs (`receipts/driver-selection-probe.txt`).
- **Why this is a SUGGESTION:** the union independently refuses a leg whose selection or executed gate list differs from the measured partition. The self-test covers that ("changed selection" and "did not run its selection exactly once"), so the driver refusal is defence in depth.
- **Suggested outcome:** add one subprocess control for each refusal.

## Prior findings at this head

| Finding | Status at `08adb21a` | Evidence |
|---|---|---|
| R636-3-F1 (MINOR, Tests): no control for the shared read budget | **Resolved** | `ci_runtime_evidence_selftest.py:165-221` drives the production `main` with `runs/1` recovering on its 3rd read and the jobs page never recovering. The collector stops at 480 s ≤ 600 s; without a shared deadline the same reads take 960 s. Mutation `i3-no-shared-budget` (`ci_runtime_evidence.py:198` without the budget) is killed: `AssertionError: collector reads took 960.0s` |
| R636-3 S1: conditional preparation accepted | **Resolved** | `ci_gate_workflows_selftest.py:28-58` plants `if:` and `continue-on-error` in each reader job. `i1-conditional-prep-accepted` and `i1b-continue-on-error-accepted` are each killed (`accepted unprepared inventory reader: docs: if preparation in docs-gates-0`) |
| R636-3 S2: client errors observer-only | **Resolved** | One classifier, `ci_fail_fast.transient` (`:45-47`). Watcher `:152-156` and collector `ci_runtime_evidence.py:232-233` fail on 400, 401 and 404 after one request, with no observer output. Controls cover both sides in both readers. Killed: watcher-client-observer, collector-client-observer, 404-transient (watch, collect), 429-genuine (watch, collect), and URLError-genuine (watch, collect) |
| R636-3 S3: elaboration workflow projection | **Resolved** (see S3 below) | `CI_WORKFLOWS.md:2684-2694, 2707-2713, 2742-2745` |
| R636-3 S4: unbounded field-oracle build | **Resolved** | `rtl.yml:375`, template `rtl.yml:297` and contract `ci_events.py:561` use `--parallel "$CI_TOOL_BUILD_JOBS"`. Reverting the workflow and template gives `ci_events: 2 finding(s)` |
| R636-3-R1 (RESIDUE): `CI_WORKFLOWS.md:2347` | **Resolved** | `:2367-2370` names the Yosys and Verilator builds and says the field-oracle build is "bounded but not separately measured" |
| R636-3-R2 (RESIDUE): PR body push sentence | **Superseded by R636-4-R1** | The new sentence is stale in the same way |
| R637-3 | No open findings | |
| Round-2 findings | Closed at round 3, per both round-3 reviews | Untouched by this delta, except the reader controls that this delta strengthens |

## S3: the builder driver split under the STOP answer

The answer's conditions, each checked:

1. **Only the entry point changed.**
   - `git diff 84ee9ea1..HEAD -- sw/builder/test_builder.py` has three hunks: the docstring (`:291-294`), `_gate_run_list` plus the receipt variable (`:29157-29185`), and the per-gate ledger, SUBSET line and receipt write (`:29270-29310`).
   - `scripts/driver_ast_diff.py` compares every top-level statement except the docstring and `__main__`, from `fa7347fc` to `08adb21a`. 542 statements were compared, including 96 local `test_*` functions, and 0 changed. The `for fn` run list has 103 entries at both revisions, in the same order. `test_declarations.py` and `test_clock_contract.py` are untouched.
   - No gate, assertion, fixture, timeout or NOT RUN arm changed.
2. **The default run is unchanged.**
   - The default path reads no new option, prints no SUBSET line when the selection equals the inventory, and computes the exit status exactly as before: the elaboration verdict only with `--require-elaboration`.
   - Executed on this host in clean copies: the `84ee9ea1` driver and the `08adb21a` driver, both with no options, each return rc 0 with `ALL GATES PASS EXCEPT 17 NOT RUN`.
   - The verdict block is identical with scratch paths masked. 100 gates print byte-identical output and 3 are identical after masking temporary names. There is no SUBSET line (`receipts/host/default-path-compare.txt`).
3. **Inventory, subset and receipt.**
   - `--list` prints the 103 names.
   - `--gates` refuses unknown, repeated, out-of-order, empty, missing and flag-as-value selections, all with rc 1 and no gate run.
   - The receipt is written with `open(..., "x")` only after every selected gate returned.
4. **Leg split from measurement.**
   - `ci_builder_legs.py:28-32,63-68`: `ISOLATED = ("test_baremetal_profile_contract",)`; leg 1 holds the other 102 gates in inventory order.
   - If the isolated gate leaves the inventory, the partition is refused (self-test).
5. **Requirements judged on the union** (`ci_builder_legs.py:131-170`):
   - Every leg exactly once, each leg's executed list equal to its partition, and every row a pass.
   - Each named owner present in the inventory, run, and run in a leg carrying its flag.
   - A leg whose own `--require-elaboration` verdict failed is refused.
   - Then the driver's own verdict is applied to the union ledger.
   - The owner names are checked against the driver source by AST: 15 `_litex_or_skip` gates and 1 `--require-rv32` reader (`ci_gate_workflows_selftest.py:171-183`).
   - Planted controls refuse by name: the elaboration gate deleted, lost with its leg, skipped in its leg, moved to a leg that never ran (3-leg patch), or run without the flag; the RV32 gate without its flag; a toolchain skip under a passing leg; a failed leg verdict; and six schema or identity corruptions.
   - **Real receipts on this host:**
     - Flag-less legs are refused by name: `--require-elaboration on the union: test_soc_option_refusals, … ran only in a leg without the flag`.
     - A flagged leg 1 (no LiteX here) is refused: `builder leg 1: its own --require-elaboration verdict did not pass`.
     - A flagged leg 0 with no RV32 compiler fails in the gate (`--require-rv32: the hosted firmware instruments must run`) and leaves no receipt.
     - Dropping `test_every_recipe_elaborates` from the real leg 1 is refused by name.
     - Losing real leg 1 is refused.
6. **Unsharded equals union** (this host, which has no LiteX or RV32 compiler; see the limits):
   - Reference `run all`: rc 0 in 13:10, 17 NOT RUN. Leg 0: rc 0 in 11:04. Leg 1: rc 0 in 2:11.
   - Per-gate verdicts and NOT RUN rows are equal for all 103 gates, and the ordered 17-row ledger is equal. The only mask is the per-run scratch HOME path inside the gate-11 reason.
   - Printed output: 99 gates byte-identical, 4 identical after masking temporary names, 0 different (`receipts/host/host-compare.txt`, `printed-compare.txt`).
7. **Hosted wiring.**
   - The generator (`ci_gate_workflows.py:27,63-89,102-112,158-185`) turns the one template command into `gate_14_0` (worker 0) and `gate_14_1` (worker 1, before the Verilator setup and LiteX aggregate). Each keeps the template command verbatim after `--` and its scope condition (`elaborate.yml:189-193, 417-421`).
   - Both workers upload `builder-leg-*.json` (`elaborate.yml:215, 497`).
   - The aggregate (`ci_gate_receipts.py:110-124`) runs the union only when a builder case succeeded, and refuses builder receipts from a skipped division. Its output digest covers the builder union (`:162-165`).
   - Worker `timeout-minutes` stays 45 and the aggregate stays 3.
   - Mutation of the generator leg step is caught by `ci_gate_workflows.py --check`.
   - **In an aggregate-like environment** (fresh clone, no submodules, a venv holding only PyYAML), `test_builder.py --list` returns the 103 names in 0.41 s, peak 93 MB.
8. **Projection.** Hosted run `38495894212` at `7032bca5`, read from the API (`receipts/hosted-baseline-elaborate.txt`): job 2144 s, builder gate 1441 s, LiteX aggregate 593 s, Verilator cache 3 s.
   - Worker 0: 2144 − 593 − 3 − 1441 + 1028.283 × 1441/1292.671 (1146) + 60 = **1313 s**.
   - Worker 1: 2144 − 1441 + 367.305 × 1441/1292.671 (409) + 60 = **1172 s**.
   - Both are within 1620 s, which is 60% of the 45-minute limit. The margins are 307 s and 448 s.
   - Workflow: 1313 + 270 = 1583 s, **26.4 minutes**.
   - The arithmetic and the table in `CI_WORKFLOWS.md:2684-2713` match.

## Lens ledger (reviewer-owned)

| Lens | Result | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | **Round-4 items 1-3 against the assignment and the STOP answer:** `sw/builder/test_builder.py:29146-29310`, `scripts/ci_builder_legs.py:1-236`, `scripts/ci_gate_receipts.py:25-31,61-124,155-170`, `scripts/ci_gate_workflows.py:25-27,63-131,158-185`, `.github/workflows/elaborate.yml:189-215,417-421,520-583`. **Issue rules held:** no step made conditional, no test dropped, no timeout raised (45/3 unchanged). The 103-gate run list is unchanged (`receipts/driver-ast-diff.txt`). **Projection:** recomputed from the hosted API (`receipts/hosted-baseline-elaborate.txt`; 1313/1172/1583 s). **Prior-finding table above.** | R636-4 | `08adb21af0a72d839ce30b6c461503dad269d4d6` |
| RTL | CLEAN | **No HDL in the delta.** The RTL lens applies to the CI architecture: job graph, dependency and ordering, fail-closed paths, the leg↔worker mapping. `ci_gate_workflows.py --check` gives rc 0 (`receipts/host/selftests.log`), so the generated workflows equal the committed ones. The leg↔worker mapping, step order and upload paths were read in `elaborate.yml:10-238,238-520`. The aggregate refuses failed, cancelled and skipped jobs and mixed scope (`ci_gate_receipts.py:72-121`). `scripts/act_ci.py` is unchanged in the delta (SHA-256 `f968f67655ac386ea703248b724c3781b95ec379d3a5287b378e470df81f895c`). | R636-4 | `08adb21af0a72d839ce30b6c461503dad269d4d6` |
| Robustness | CLEAN (S1 and S2 recorded as SUGGESTIONs) | **Driver refusals:** 7 malformed selections, rc 1 (`receipts/driver-selection-probe.txt`). **Leg runner:** a missing driver receipt gives rc ≠ 0 (`receipts/host/fl0.*`); an identity change raises; `xb` refuses overwrite. **Union:** refuses a lost, duplicated or unknown leg, a changed head, a changed inventory, unknown flags, a failed verdict and a forged toolchain skip (self-test plus `receipts/host/host-compare.txt`). **Observer classifier:** both sides, in the watcher and the collector. **Aggregate-like `--list`:** with no submodules and only PyYAML it succeeds (`receipts/agg-list.*`). **Collector:** genuine client errors fail it with no observer output. | R636-4 | `08adb21af0a72d839ce30b6c461503dad269d4d6` |
| Tests | CLEAN (S3 recorded as a SUGGESTION) | **Self-tests at head, all rc 0** (`receipts/host/selftests.log`): `ci_gate_workflows.py --check`, `ci_gate_workflows_selftest.py`, `ci_fail_fast_selftest.py`, `ci_runtime_evidence_selftest.py`, `ci_events.py --check` (2186 items) and `--selftest` (5212 arms). **Mutations:** 24 semantic mutants, every one killed by an assertion or refusal; 4/4 pristine pass (`receipts/mutations/`). **Real-execution equality:** unsharded run = union of the legs (`receipts/host/host-compare.txt`, `printed-compare.txt`). **Default path:** round-3 driver = head driver (`receipts/host/default-path-compare.txt`). **Real-receipt planted controls:** as listed in S3 item 5. | R636-4 | `08adb21af0a72d839ce30b6c461503dad269d4d6` |
| Docs | CLEAN (RESIDUE R636-4-R1 carried) | **Pages read:** `docs/testing/CI_WORKFLOWS.md:1400-1427` (legs and union rules, matched to code), `:2367-2370` (R1), `:2684-2694` and `:2707-2713` (projection and table, recomputed), `:2742-2745`, `:2755-2759`, `:2781-2783`, `:2806-2809`, `:2920-2935` (the reproduction commands match `ci_builder_legs.parse`). The driver docstring `sw/builder/test_builder.py:287-294` was also read. **Live PR body:** Status, the Round 4 table and the S3 section were matched to code. Only R636-4-R1 is stale. **Doc gates, all rc 0** (`receipts/doc-checks.txt`): `docs_check` (207 pages); `check_doc_style`; `check_doc_paths` (986 paths); `check_em_dash` against `84ee9ea1` (75 lines) and `fa7347fc` (810 lines); `gen_toc --verify-anchors` (494) and `--check`; `check_py_idiom`. The renderer-dependent gates used the hash-pinned renderer in a disposable environment. | R636-4 | `08adb21af0a72d839ce30b6c461503dad269d4d6` |

## Mutation receipts

`scripts/mutations.py` applies each mutant by exact string replacement in a disposable copy. It runs the killing command, restores the files with `git checkout`, and checks that the copy is clean afterwards.

**Killed, each by a semantic assertion or refusal:**

- **F1:** `i3-no-shared-budget`.
- **S1:** `i1-conditional-prep-accepted`, `i1b-continue-on-error-accepted`.
- **S2:**
  - client errors made observer-only: `s2-watcher-client-observer`, `s2-collector-client-observer`;
  - classifier too broad or too narrow: `s2-404-transient-watch` and `-collect`, `s2-429-genuine-watch` and `-collect`;
  - transport errors made genuine: `s2-urlerror-genuine-watch` and `-collect`.
- **S3:**
  - union checks removed: `s3-unjudged-accepted`, `s3-absent-accepted`, `s3-no-union-elaboration-verdict`, `s3-leg-verdict-ignored`, `s3-missing-leg-accepted`;
  - comparison and aggregate weakened: `s3-compare-ignores-not-run`, `s3-aggregate-skips-union`, `s3-aggregate-no-union-call`;
  - owner list and generator: `s3-owner-list-short`, `s3-generator-leg-wrong`.
- **S4:** `s4-unbounded-field-oracle`.

**Pristine copies:** `pristine-gate`, `pristine-fail`, `pristine-runtime` and `pristine-generator` all pass.

**Not counted:** one malformed mutant, `s2-transport-genuine-watch`. It died with an `AttributeError` from the mutant itself, and the corrected `s2-urlerror-*` pair replaces it. `summary.jsonl` also keeps the first, malformed run of the `s2-urlerror-*` pair. Its logs were overwritten by the corrected run, whose kills are semantic.

## Real limits

- **Not run in the shipping image.** Docker is outside this review's permissions, so the unsharded-versus-legs equality was not rerun there. It was run on this host instead:
  - there is no LiteX interpreter, so the 15 elaboration gates record `no-litex`;
  - the RISC-V cross compiler was hidden, so the firmware instruments stood down;
  - the gates ran in 12-13 minutes rather than the image's 22.
  - The compiler-on and LiteX-on arms are therefore covered only by the author's shipping-image equality, which is described in the READY comment and PR body and is not published as receipts.
- **No hosted runs at this head.** There are no hosted runs and no check contexts for `08adb21a` (API: 0 check runs). All timings are projections from the `7032bca5` baseline. Hosted readback decides the elaboration span and the per-worker windows.
- **Host differences.** Host Python is 3.14, while hosted runners use 3.12. Host load was high from other work, so host times are not timing evidence.
- **Physical calibration NOT RUN.** Field and calibration skips are not hardware proof.
- **Local runner not exercised.** No act replay or local runner execution was done, by assignment.

## Pending manager duties

- Publish the author's round-4 shipping-image receipts (unsharded and leg receipts, union `--reference` output, aggregate replay), or link them, so that a cold reviewer can open them.
- Validate the current-dev merge candidate: source base `fa7347fc` against live dev `f6260253`, with the builder and native banks, at the merge turn. Run the hosted and act acceptance, including exact-head hosted readback for `elaborate-gates-0`/`-1` and the elaboration span (26.4-minute projection) and the docs span (29.6-minute projection).
- Carry RESIDUE R636-4-R1 to the residue checklist. Decide whether to take SUGGESTIONs S1-S3.
- Merge only with explicit maintainer authorization and the full completion bar.

## Clone integrity

The review clone `$REVIEWS/r636-4-737` was never modified; every probe used disposable copies under `scratch/`. `scripts/verify_clone.sh` reports `CLONE EXACT` (`receipts/clone-verify.txt`):

- HEAD `08adb21a`, tree `e5cc5d16`; the index tree equals the commit tree;
- 1358 tracked blobs match their committed bytes and modes;
- the status is clean;
- the gitlinks `gptp-processor 7dda9c3b`, `protocol-processor 2ad2f845`, `third_party/lwSRP 08ee86e8`, `third_party/tsn-c-stack 70936b77` and `third_party/verilog-axis 48ff7a7e` are checked out at their recorded commits, and `external` is not initialised.

R636-4 FINISHED
