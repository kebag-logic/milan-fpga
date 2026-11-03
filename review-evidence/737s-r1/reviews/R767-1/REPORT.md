[R767] NEGATIVE - exact head aa3e2d85024c0aa17b32ed1165e23e65cfad49b0

Round R767-1, internal cleared-context review of PR #836 for issue #737 (CI only).
Head `aa3e2d85024c0aa17b32ed1165e23e65cfad49b0`, tree `f91c0c585107d0606045a789ab4d5c8c86ce6ad0`,
base and live dev `e61a4afaa54a598ceec08b7b5879285256cc60b6`. All five lenses applied.

## Verdict in one paragraph

The split works and is safe: every LiteX simulation belongs to exactly one leg, `--only` still
reconciles the whole inventory, and the union is refused, naming its cause, when a simulation is
dropped, moved, duplicated, lost with its leg or failing. That holds in the PR's own self-tests,
in 24 reviewer mutants and in a stub-interpreter end-to-end probe of the real runner path. The
generated workflow matches its generator. The first hosted elaborate run at this exact head
(41583428850, attempt 1, all caches cold) passed: 8 of 8 simulations, each once, and the
aggregate union passed. No job is near its 45-minute timeout (largest runner span 1253 s of
2700 s). The verdict is NEGATIVE for two MINOR measurement findings. **F1:** the per-member
seconds and the per-job bounds derived from them understate what a leg costs on its own worker.
On that same run, leg 2's worker took 1225 s against the stated cold maximum of 1039 s, and
`test_ctrl_memory` took 280 s against its recorded 113 s. **F2:** the workflow wall-clock claim
leaves out runner queueing, which three more runners per head make more likely. On that run a
LiteX worker waited 1269 s for a runner, and the aggregate ended at 2306 s.

## Findings

### F1 - MINOR - Conformance, Robustness, Docs - LiteX member seconds and per-job bounds are in-aggregate figures, not standalone leg costs

- **Where:**
  - `scripts/ci_litex_legs.py:29-48` (the `SECONDS` table, and the `LEG_BUDGET` comment's "112 seconds of setup, a 300-second cold Verilator build").
  - `docs/testing/CI_WORKFLOWS.md:3084-3096` ("about 300 seconds ... the slowest then projects at 1040 seconds") and table rows `:3116-3118` (740 / 724 / 739).
  - `docs/testing/CI_WORKFLOWS.md:1677-1680` (leg loads 534 / 518 / 533).
  - The PR body's "Legs and timing" and "Derived per job" tables (cold 1040 / 1024 / 1039 s).
- **Authority:**
  - #737 scope item 1: leg membership is derived from measured durations.
  - The coordinator's comment of 2026-11-02 on this issue: the projection table must state the measured span, not a projection.
  - The brief's question (4), whether the bound is stated honestly.
- **Evidence:** the member seconds are gaps between result lines inside the old whole aggregate. That aggregate ran on `elaborate-gates-1` after builder leg 1 in the same job. I recomputed them from the six cited hosted logs, and they match to within 1 s (`receipts/member_gaps_cited.log`). Standalone, at this exact head, they are not the same:

  | Member / job | Recorded (in-aggregate) | Exact-head hosted run 41583428850 | Author's local leg receipt |
  |---|---:|---:|---:|
  | `test_ctrl_memory` | 113 s | **280 s** | 206 s |
  | leg 2 total (`elaborate-gates-4`) | 533 s | **684 s** | 578 s |
  | Verilator cold build | "about 300 s" | 249 s and **411 s** | - |
  | `elaborate-gates-4` job, cold | derived at most 1039 s | **1225 s** | - |
  | setup allowance | 112 s (code comment) vs 143 s (docs, PR) | - | - |

  Sources: `receipts/member_gaps_exact_head.log`, `receipts/hosted/exact_head_elaborate_timing.txt`, and the author's published `review-evidence/737s-r1/author/receipts/litex-leg-2.json` (206 s). The author's own standalone receipt already showed `test_ctrl_memory` at 1.8 times its recorded value. A likely cause, not proven here: inside the old job, the member reused state the builder leg had just produced.
- **Impact:**
  - The stated per-job and cold bounds are wrong for the job this PR adds: it ran 186 s over its stated cold maximum on its first hosted run.
  - The partition and the 1200-second leg-budget refusal read figures that understate the standalone cost of some members by up to 2.5 times, so the guard's margin is smaller than documented.
  - There is no timeout risk today: 1225 s is 1475 s inside 45 minutes and 575 s inside 30 minutes.
- **Required outcome:**
  - `SECONDS` holds standalone per-member hosted seconds. Each leg receipt's own `verdicts.tsv` seconds from exact-head hosted runs are a ready source.
  - The partition is re-derived from those seconds.
  - The cold Verilator figure is restated from measured cold builds.
  - The setup allowance is one figure everywhere.
  - The CI_WORKFLOWS.md rows and prose, and the PR body, state measured spans for the LiteX workers, with the cold case taken from a measured cold run.
- **Verification:**
  - `python3 scripts/ci_litex_legs.py legs` prints the re-derived partition.
  - `ci_gate_workflows.py --check` and `ci_gate_workflows_selftest.py` pass.
  - Each documented LiteX-worker figure is at or above the exact-head hosted span (584 / 615 / 1225 s cold for run 41583428850), and the cited runs are named.

### F2 - MINOR - Conformance, Docs - the workflow wall-clock claim omits the queueing the three added runners incur

- **Where:**
  - The PR body: "Why three legs ... The wall clock does not change, because the builder workers bind it", and "Workflow ... 1745 s (29.1 min) ... 1497 s (25 min)".
  - `docs/testing/CI_WORKFLOWS.md:3156-3159`: elaboration projects at 1745 s, 55 s inside thirty minutes.
- **Authority:** #737 acceptance 1 (first job start to last job end, at most 30 min, with the union proofs passing), and the brief's question (4).
- **Evidence:** at this exact head, run 41583428850 (`receipts/hosted/exact_head_elaborate_timing.txt`):
  - `elaborate-gates-3` (LiteX leg 1) was queued 1269 s before its first step and ended 1882 s after the first job started.
  - The `elaborate` aggregate was queued 389 s and ended at 2306 s.
  - `Collect CI manifest` ended at 2824 s.
  - The four workflows at this head were running at the same time (docs, rtl-fast, and rtl-full with 19 shards).
  - Before this change the workflow had two worker runners; now it has five.
- **Impact:** the claim that a third leg costs only "about 143 s per run" of setup, and leaves the wall clock unchanged, is not borne out once runners are scarce. On this run the extra runner was the last job to start, and it set the workflow's end. Acceptance 1 was not met by this run, and the PR text does not say that queueing is outside the 1745-second figure.
- **Required outcome:**
  - The PR text and CI_WORKFLOWS.md state that the 1745 s projection excludes runner queueing.
  - The two-legs-or-three rationale accounts for one more concurrent runner per head.
  - The exact-head hosted spans of run 41583428850 are recorded against acceptance 1, with the queueing named as the cause.
  - Either the manager decides whether three legs or two better meets acceptance 1 under the account's runner limit, or the lane re-measures that.
- **Verification:**
  - The updated text names the queueing exclusion and run 41583428850's 1882 s / 2306 s spans.
  - The manager's hosted acceptance readback records the per-workflow wall clock against the stated bound.

### R1 - RESIDUE - Docs - "each refused by name" overstates the duplicate case

- **Where:** `docs/testing/CI_WORKFLOWS.md:1675-1676`.
- **Evidence:** a simulation run in a second leg is refused as "LiteX leg 2 did not run its selection exactly once: order or extra simulations". That names the leg, not the simulation. A red runner exit is likewise named by its leg (`receipts/e2e_baseline.log`). The "ran in more than one leg: X" branch at `scripts/ci_litex_legs.py:165-166` can only be reached through a partition defect (mutant S7).
- **Exact fix:** replace "are each refused by name" with "are each refused, naming the simulation or the leg".

### S1 - SUGGESTION - Tests - component self-tests miss three mutants that only the runtime union catches, and one placement invariant is untested

- **Evidence:** `receipts/mutants/mutants-*.json`.
  - These survive `run_litex_sims.sh --selftest`, `ci_litex_legs_selftest.py` and `ci_gate_workflows_selftest.py`, and are refused only by the runtime union path (the reviewer's end-to-end probe):
    - S1: `--only` silently runs at most two members.
    - S5: every verdict row says PASS.
    - S21: the leg runner records exit 0 whatever the runner returned.
  - S23 (`LITEX_WORKERS = (2, 3, 1)`, putting a LiteX leg back on builder worker 1, which is the #737 failure shape) is caught only incidentally, by the hard-coded job list in `scripts/ci_scope_history.py:296-300` (and, by the same count, the act scope fixture).
- **Optional change:**
  - Add a `--only` arm with three or more members.
  - Add an arm in which a failing member writes a FAIL row.
  - Add an assertion that LiteX workers are disjoint from builder workers.
  - Optionally, name the extra simulation in the "order or extra simulations" refusal.

### Observation, not a finding of this PR

On a Verilator cache miss, the "Cache exact package downloads 16" post-save fails with `tar: ../../_temp/ci_packages_16/lock: Cannot open: Permission denied`. That happened on `elaborate-gates-2` and `elaborate-gates-4` at this head. The step and its recipe predate this PR; it now runs on three workers instead of one. This is a candidate for a new Issue.

## Brief checks

1. **One owner per simulation, and the union proof.** Met.
   - `ci_litex_legs.py legs` gives 0/3 `test_soc_timing_cuts`; 1/3 `test_gmii_rx_capture`, `test_gptp_tx_timestamp`, `test_pp_boot_bus_freeze`, `test_pp_mem_bridge`; 2/3 `test_cpu_memory_port_cdc`, `test_ctrl_memory`, `test_retained_cdc_storage`. That is 8 of 8, disjoint (`receipts/gates/litex_legs_legs.log`).
   - **End-to-end probe** (`scripts/e2e_legs.py`, `receipts/e2e_baseline.log`): it runs the real `ci_litex_legs.py run` around the real runner with a stub interpreter. Both the union and `ci_gate_receipts.verify` refuse each plant:
     - a row dropped: "LiteX leg 1 did not run its selection exactly once: test_pp_boot_bus_freeze";
     - a member moved to another leg: "LiteX leg 1: selection differs from its measured leg";
     - a member duplicated into another leg: "LiteX leg 2 ... order or extra simulations";
     - a lost leg: "ran in no leg: ..." naming its four simulations;
     - a real failing member: "test_pp_boot_bus_freeze: FAIL in LiteX leg 1".
   - **Mutants** (`scripts/mutants.py`, 24 mutants; baseline green, with the three source dependencies initialised): 18 are killed by the PR's own self-tests; S1, S5 and S21 by the runtime union only; S23 incidentally. S4, S17 and S18 survive as equivalent mutants. In S4 the missing row is still refused at runtime by name. S17 and S18 each remove one of two redundant stale-table guards, the runner's truncate and the leg runner's unlink. The corrected S7, a member in two legs, is killed.
   - `--only` still reconciles the whole inventory: mutant S3, which narrows MISSING to the selection, is killed by the runner self-test.
2. **Generated, not hand-edited.** Met.
   - `ci_gate_workflows.py --check` gives rc 0.
   - Each generator mutant was regenerated before judging; S14, S15, S16 and S20 are killed by `ci_gate_workflows_selftest.py`.
   - The template change is a comment only (`.github/ci-templates/elaborate.yml:333-337`).
3. **Records.** Met, apart from the stated limits.
   - Local results: `ci_events.py --check` rc 0; `--selftest` rc 0 (2199 items, 5579 arms); `ci_scope.py --selftest` rc 0, including 150 elaborate.yml scope-history checks, 30 for each of the five workers; `ci_runtime_evidence_selftest.py` and `ci_manifest_selftest.py` rc 0.
   - The tool-cache isolation plans compute for all five workers, with the LiteX leg tail excluded by its declared reason (`receipts/toolcache_plans.log`).
   - The command-table pins equal the head blobs for `run_litex_sims.sh`, `ci_gate_workflows_selftest.py`, `ci_scope_history.py` and the new `ci_litex_legs.py`. The `act_ci.py` pin is stale at base and at head; the PR states this.
   - **Hosted at this exact head:**
     - docs run 41583428780 succeeded, including "Local act runner contract gate", which is the `act_ci.py --selftest` that holds the five-owner scope fixture;
     - elaborate's "Collect CI manifest" succeeded with the five workers and the aggregate.
4. **Bounds.** See F1 and F2.
   - No job is at risk of its timeout. Exact-head runner spans: 584, 1182, 1225, 1253 and 615 s against 2700 s; aggregate 35 s against 180 s.
   - Worker 0 measured 1253 s cold at this head; its projection is 1475 s, and it is unchanged by this PR.
5. **`ci/image/tool-inventory.json`.** The claim is verified.
   - `--check` refuses at base and at head with the same words: "changed declared script 'sw/builder/endstation_builder.py'". That file is untouched by this PR.
   - Limit: with the builder pin re-pinned, or with the pinned builder blob `a2e14de6` restored, base and head next refuse identically on further unrelated drift ("uncensused Python builtin 'exec'", then "undeclared executing or network script 'avdecc/gen_aemi_image.py'"). So whether this PR adds inventory drift of its own stays masked at both (`receipts/gates/inventory_unmask_*.log`).

## Gates run at this head (16 CPUs, private CPython 3.12.3 environment with the pinned PyYAML 6.0.2 and behave 1.3.3)

All rc 0 unless noted. Receipts are in `receipts/gates/`.

- `ci_gate_workflows.py --check` and `ci_gate_workflows_selftest.py` (17 s).
- `ci_litex_legs_selftest.py`.
- `run_litex_sims.sh --selftest` (16/16).
- `ci_litex_legs.py legs`.
- `ci_events.py --check` and `--selftest` (288 s).
- `ci_scope.py --selftest`.
- `ci_runtime_evidence_selftest.py` and `ci_manifest_selftest.py`.
- `behave` (508 scenarios).
- `check_py_idiom.py` and `check_sh_idiom.py`.
- `git diff --check e61a4afa HEAD`.
- `ci_tool_inventory.py --check`: rc 2 at both base and head, as described above.

## Hosted exact-head evidence inspected (read-only)

| Run | Workflow | State |
|---|---|---|
| 41583428850 | elaborate | All five workers, the aggregate and the manifest collector succeeded. |
| 41583428780 | docs | Completed, success. |
| rtl-fast, rtl-full | - | Still queued or running when inspected; not assessed. |

These are executed jobs, not skipped contexts. The manager owns hosted and act acceptance.

## Comment rule

The added lines in the delta show no lane labels, lane names, review rounds, reviewer IDs or issue-comment IDs: a scan of every added line in every file, excluding the generated command table, found none. All added Python lines are within 120 columns.

## Prior public review findings

There were none on PR #836 when this round started. The only comments are the two review-start notices. The parallel external round had not been read.

## Ledger (reviewer-owned)

| Lens | Result | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | UNCLEAN (F1, F2) | #737 body, scope and acceptance; coordinator comments of 2026-11-02 and 2026-11-03; `ci_litex_legs.py:29-48`; hosted runs 41470524727, 41526004847, 41554508699, 41476923392 (attempts 1-3) and exact-head 41583428850 | R767-1 | aa3e2d85024c0aa17b32ed1165e23e65cfad49b0 |
| RTL | CLEAN | `git diff --stat e61a4afa..aa3e2d85`: no `hdl/`, `tb/`, `syn/` or `sw/litex/*.py` file changed. The simulated designs and SoC inputs are byte-identical to base; only the CI orchestration changed | R767-1 | aa3e2d85024c0aa17b32ed1165e23e65cfad49b0 |
| Robustness | UNCLEAN (F1) | `run_litex_sims.sh:162-185,228-268,454-480` (usage errors, stale-table handling, verdict rows); `ci_litex_legs.py:63-172`; `ci_gate_receipts.py:63-135` (skip scope, LiteX receipts without a division); the e2e probe and 24 mutants | R767-1 | aa3e2d85024c0aa17b32ed1165e23e65cfad49b0 |
| Tests | CLEAN (S1 suggestion only) | `ci_litex_legs_selftest.py`; `ci_gate_workflows_selftest.py:506-643`; the runner `--selftest` arms `:419-444`; `ci_scope_history.py:294-300`; mutation table `receipts/mutants/` | R767-1 | aa3e2d85024c0aa17b32ed1165e23e65cfad49b0 |
| Docs | UNCLEAN (F1, F2; R1 residue) | `docs/testing/CI_WORKFLOWS.md:1589-1685,3023-3030,3081-3182`; `docs/testing/TESTING.md:687-720`; PR #836 body | R767-1 | aa3e2d85024c0aa17b32ed1165e23e65cfad49b0 |

## Real limits

- I did not run the real LiteX simulations locally: no LiteX environment was built in this review. Execution of the eight simulations rests on the exact-head hosted run 41583428850 (all PASS, once each) and on the author's published leg receipts.
- I did not run these myself: `act_ci.py --selftest` (not allowed), `ci_toolcache_isolation.py` (it needs network installs for five legs; only its plans were computed), the docs workflow's builder bank, Docker or act. The act selftest's exact-head result is the hosted docs run's.
- The tool-inventory question stays masked by unrelated drift at base and head (check 5).
- The queueing in F2 depends on the account's concurrent load. One run shows that it happens, not how often.
- The cause of `test_ctrl_memory`'s standalone cost is inferred, not traced.

## Pending manager duties

- Hosted and act acceptance of the current-dev merge candidate, with the builder and native banks, at the merge turn.
- Recording acceptance 1 against the exact-head hosted spans.
- Carrying R1 to the residue checklist.
- The decision in F2 on the number of legs under the runner limit.
- Re-review of the F1 and F2 fixes at a new head.

Physical calibration: NOT RUN. Field skips are not hardware proof.

R767-1 FINISHED
