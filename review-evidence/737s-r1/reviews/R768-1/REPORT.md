[R768] NEGATIVE - exact head aa3e2d85024c0aa17b32ed1165e23e65cfad49b0

# External review R768-1: issue #737 / PR #836 (LiteX simulations in three elaborate legs)

- Exact head `aa3e2d85024c0aa17b32ed1165e23e65cfad49b0`, tree `f91c0c585107d0606045a789ab4d5c8c86ce6ad0`.
- Source base and live dev at review time: `e61a4afaa54a598ceec08b7b5879285256cc60b6`.
- Round focus: CI only. Authority: #737 scope item 1 (GitHub CI at most 30 minutes per workflow; leg membership from the suite's own inventory; a final job proves the union; no timeout raised, no step made conditional, no test dropped). Also the manager's #737 comment on the `elaborate-gates-1` 45-minute cancellations.
- Every lens was applied: Conformance, RTL, Robustness, Tests, Docs.

## Verdict

**NEGATIVE.** Three MINOR findings are open. None of them lets a simulation go unrun or unreported, and no job is at its timeout:

- The union proof is sound. Every code mutant and receipt plant that drops, duplicates, moves or fails a simulation is refused. The refusal is printed by both the union CLI and the `elaborate` aggregate verifier, and it names the affected simulation.
- The largest exact-head hosted job was 1254 s, against the 2700 s limit.

The open findings are about whether the derived per-job bounds are honestly stated (focus item 4), and about a cache-save race that this change introduces.

## Findings

### F1 - MINOR - Conformance, Docs, Robustness - the cold-cache bound is exceeded at the exact head

- **Where:**
  - `docs/testing/CI_WORKFLOWS.md:3095-3096` ("A Verilator cache miss adds a source build, about 300 seconds, to each LiteX worker; the slowest then projects at 1040 seconds").
  - `docs/testing/CI_WORKFLOWS.md:3116-3118` (projection rows for `elaborate-gates-2..4`).
  - The PR body's "Derived per job" table and its Known limitations ("the cold case on all three LiteX workers (derived at most 1040 s)").
  - `scripts/ci_litex_legs.py:45-48`: the `LEG_BUDGET` derivation's 300-second cold allowance.
- **Evidence:** hosted `elaborate` run 41583428850 is at this exact head, and is the first run after this workflow edit.
  - Every workflow-hash-keyed cache missed, not only Verilator: sv2v, `elaborate-pip-git-pins`, `elaborate-sbt`, `elaborate-vexii` and Verilator all report "Cache not found" (`receipts/hosted/head-gates-2.results.txt`, `head-gates-4.results.txt`).
  - `elaborate-gates-4` took **1226 s**, against the derived cold maximum of 1039 s. Its Verilator build took 411 s, against the 300 s allowance. Its leg took 684 s, against 533 measured seconds.
  - Within that leg, `test_ctrl_memory` took 280 s against its `SECONDS` value of 113.
  - Worker 2 took 585 s. Worker 3, which restored the Verilator cache worker 2 saved, took 616 s (`receipts/hosted/run-41583428850-jobs-late.json`).
  - Cause: the member seconds were measured after builder leg 1 in the same job, on warm caches. They do not hold for a fresh LiteX worker on cold caches, and the cold allowance counts only one of the six caches that miss together.
- **Impact:**
  - The published cold bound is not a bound: the first hosted run exceeded it by 187 s (18 %).
  - The 1200-second `LEG_BUDGET` is derived from the same understated allowance. That job still finished inside 30 minutes, so nothing times out today. The margin a future re-partition would rely on is overstated.
- **Required outcome:**
  - The LiteX workers' cold-case projection covers every cache a workflow edit invalidates, and is reconciled with the exact-head hosted measurement (1226 s).
  - The `LEG_BUDGET` comment's allowance agrees with that projection.
- **Verification:** the docs table and the PR figures agree with run 41583428850 (or a later exact-head cold run), and `python3 scripts/ci_litex_legs.py legs` stays under the restated budget.

### F2 - MINOR - Conformance, Docs - the worker-1 projection and the setup figure leave out evidence the PR itself cites

- **Where:**
  - `docs/testing/CI_WORKFLOWS.md:3087-3090` ("worker one projects at its largest measured job time less that step, `2672 - 1485`") and `:3115` (`elaborate-gates-1 | 1187 | 1620 | 433`).
  - The PR body ("builder leg 1 869 to 1075 s"; `elaborate-gates-1 (2672 - 1485) 1187`).
  - `scripts/ci_litex_legs.py:46` ("less its measured 112 seconds of setup").
- **Evidence:**
  - The same docs paragraph (`:3094-3095`) and the `SECONDS` comment use run 41476923392 attempts 1 to 3 as evidence. In those attempts builder leg 1 took 1108, 1096 and 1119 s.
  - Worker 1 had already spent 1232, 1215 and 1217 s before its LiteX step started. So worker 1 without that step is at least 1232 s plus its post-steps, not 1187 s (`receipts/hosted/worker1-split.txt`, computed from the public jobs API).
  - The `LEG_BUDGET` comment subtracts 112 s of setup. That is the smallest outside-the-gate-steps value (run 41554508699). The docs and the PR use the largest, 143 s (run 41526004847).
- **Impact:**
  - Worker 1's projection, and its 433 s margin to the 1620 s job budget, are understated by at least 45 s.
  - The stated builder-leg range is wrong for runs the PR itself relies on.
  - The workflow bound does not move, because worker 0's 1475 s still binds.
- **Required outcome:** worker 1's projection, the builder-leg range and the `LEG_BUDGET` setup figure are each the maximum over the runs the text cites. Alternatively, the text names any run it excludes and says why.
- **Verification:** recompute from the jobs API for runs 41470524727, 41526004847, 41554508699 and 41476923392 attempts 1 to 3.

### F3 - MINOR - RTL (resource/timing effects), Robustness (inter-job ordering) - a LiteX worker wins the save race for the shared CPU-netlist cache and stores it empty

- **Where:**
  - `.github/workflows/elaborate.yml:615-622`, `:899-906` and `:1183-1190`. The three new LiteX workers restore and save the same `elaborate-vexii-...` key as the builder workers, and likewise the `elaborate-sbt`, pip and sv2v keys.
  - The template contract at `.github/ci-templates/elaborate.yml:213-217`: "a miss must cost one ~90 s Scala run".
- **Evidence:** in run 41583428850 at this head:
  - `elaborate-gates-2` finished first and saved `elaborate-vexii-e8d7156c...-0a027c1...` as a 202-byte archive ("Sent 202 of 202"), i.e. an empty `~/vexii-netlist-args`.
  - `elaborate-gates-0` and `elaborate-gates-1` then logged "Failed to save: Unable to reserve cache with key elaborate-vexii-..." (`receipts/hosted/head-gates-0.results.txt`, `-1`, `-2`).
  - At base, the first finisher holding that key was builder worker 0, which saved its generated arguments. In run 41470524727, worker 1's save was refused.
  - The key deliberately has no `restore-keys`. Every later run with this key therefore restores the empty entry, and each builder leg regenerates its VexiiRiscv netlist arguments on every run until a workflow or config input changes the key.
- **Impact:**
  - A recurring Scala-generation cost lands on the builder workers. Worker 0 is the job that binds the workflow: it is projected at 55 s inside 30 minutes, and measured 1254 s on this cold run.
  - The template's "one ~90 s Scala run per miss" silently becomes "every run".
  - Nothing fails and nothing is skipped. The cost is undocumented time on the binding job.
- **Required outcome:** one of the following; the design choice belongs to the executor.
  - The netlist-argument cache is saved only by a job that generates the arguments, or is otherwise protected from an empty first save.
  - Or the per-run regeneration cost is measured on a warm-key run and folded into the worker-0 and worker-1 projections and the docs.
- **Verification:** on a second hosted run with the same key, the `Cache the generated CPU metadata` restore on `elaborate-gates-0/1` is non-empty. Or the docs' worker-0 projection is shown to hold with the regeneration included.

### Suggestions (optional; they do not affect coverage)

- **S1 (Tests):** no offline selftest drives `ci_litex_legs.run()` itself (mutants L3, L4) or the aggregate's `rglob("litex-leg-*.json")` collection in `main()` (mutant G2). Each is refused at runtime by the union, by name. A sandbox arm through `run()` would catch it before a hosted run.
- **S2 (Tests):** the `repeated` branch of `union()` (`scripts/ci_litex_legs.py:162-166`) cannot be reached while the per-leg `executed != legs[leg]` check stands. Mutant L5b survives every detector. A direct plant, or a comment saying it is defence in depth, would make this explicit.
- **S3 (Robustness):** `--only a,` with a trailing comma is accepted as `--only a`, and a receipt `exit` of boolean `False` is accepted as 0. Neither is reachable from the generated step.

## Lens results

`[R768] PASS Tests - scripts/ci_litex_legs_selftest.py:58-158, scripts/ci_gate_workflows_selftest.py:534-642, scripts/run_litex_sims.sh:416-444 at aa3e2d85 - each new plant fails for its defect; independent mutation campaign agrees`

- **Mutation campaign:**
  - 36 code mutants and 9 receipt plants were run end to end, through the real runner, the leg runner, the union CLI and the `ci_gate_receipts.py verify` CLI, with stub members.
  - The code mutants covered: the runner's `--only`, reconciliation and verdict rows; the partition, `run()` and `union()`; the aggregate verifier; the generator; the generated workflow; and the template.
  - 34 of 36 mutants were killed. L10 is a legitimate re-partition. L5b is the unreachable redundant check (S2).
  - Every mutant that changes which simulations run is refused by both the union and the aggregate verifier, naming the simulation (`receipts/mutants-table.md`, `receipts/data-mutants/data-mutants.json`).
  - The PR's quoted refusal is reproduced verbatim: `LiteX leg 1 did not run its selection exactly once: test_pp_boot_bus_freeze`, which the aggregate prefixes with `gate evidence refused:` (plant D1).
- **Gate runs:** the gates the PR lists, all rc 0 at head on CPUs 16-31 (`receipts/gates-head/`):
  - ci_events `--check` (2199 items) and `--selftest` (5579 arms);
  - `ci_gate_workflows.py --check` and its selftest;
  - `ci_litex_legs_selftest.py`;
  - `run_litex_sims.sh --selftest` (16/16);
  - `ci_scope.py --selftest`, including the scope-history arms for workers 2 to 4;
  - `ci_litex_legs.py legs`;
  - behave (508 scenarios);
  - `git diff --check`.

What the other four lenses verified clean, beside their open findings:

- **Conformance:**
  - Each simulation is owned by exactly one leg, derived from the runner's `--list` (`legs`: 534 / 518 / 533 s).
  - `SECONDS` matches the hosted logs to within 1 s of rounding (`receipts/hosted/member-seconds.txt`).
  - No timeout is raised (workers 45 min, aggregate 3 min), no step is made conditional, the triggers are unchanged and no simulation is dropped (`receipts/workflow-structure.txt`).
  - At the exact head, hosted workers 2, 3 and 4 ran 1, 4 and 3 members, each PASS, and the reconciliation covered all 8 in each (`receipts/hosted/head-gates-{2,3,4}.results.txt`).
- **RTL (CI architecture):**
  - The generated delta against base is exactly: workers 2 to 4 added; worker 1 loses its Verilator setup and the LiteX step; the `elaborate`, `ci-manifest` and `ci-fail-fast` job lists widen; worker 0 is identical.
  - The generator refuses a template whose aggregate is not its last line, is repeated, or carries its own `--only` (W4, W5).
- **Robustness:**
  - Each of these is refused: a missing or unlisted member file, a masked verdict, a declared skip, a failure, a red exit, a lost or duplicated leg, a foreign head, and a narrowed selection (R6b to R11, D1 to D9).
  - A LiteX receipt from a skipped division is refused (G3).
- **Docs:**
  - TESTING.md section 2 and the CI_WORKFLOWS.md Elaboration and receipt prose match the code.
  - No comment-rule residue (bench lane labels, lane names, review rounds, reviewer or issue-comment IDs) appears in any added line of the delta.

### Focus items

1. **Ownership and union proof:** sound, as above. `run_litex_sims.sh --only` still reconciles the whole inventory. Mutant R3 narrows the reconciliation and is caught by the runner selftest. With a deleted member file, the leg is red in every leg (R7).
2. **Regeneration:**
   - The workflow is regenerated, and `ci_gate_workflows.py --check` passes.
   - Hand edits W2 and W3 fail `--check`. The gate selftest regenerates from the template and does not see them, so `--check` is the guard.
   - `docs.yml:436-437` runs `--check` and the selftest on pull requests.
3. **Records:**
   - ci_events `--check` and `--selftest` pass.
   - `ci/image/command-table.json` pins match the head bytes for `run_litex_sims.sh`, `ci_gate_workflows_selftest.py`, `ci_scope_history.py` and the new `ci_litex_legs.py`. The `act_ci.py` pin mismatches at both base and head, as the PR states (`receipts/command-table-pins.txt`).
   - The act scope fixture requires 5 owners, and the workflow has exactly `elaborate-gates-0..4`.
   - Tool-cache isolation plans compute for all five workers (`receipts/toolcache-plans.txt`).
   - The manifest plan and its `gate/elaborate` union expectation derive from the workflow files (`scripts/ci_manifest.py:133-136`), so no static job map is left unmapped. The per-simulation LiteX union enters `gate/elaborate`'s `verdicts_sha256` without timing fields.
   - `ci/image/tool-inventory.json` and `exec-audit-receipt.json` still name only workers 0 and 1; the PR acknowledges both are stale.
4. **Timing:** F1, F2 and F3.
   - No job is at its timeout: the exact-head maximum was 1254 s, against 2700 s.
   - Worker 0's 55 s workflow margin is a projection. Worker 0 measured 1254 s, cold, at this head.
5. **Tool inventory:**
   - With the checksum-pinned parser, `ci_tool_inventory.py --check` refuses at base and at head with the same `changed declared script 'sw/builder/endstation_builder.py'`. This PR does not touch that file.
   - Re-pinning only that declaration in a disposable clone reveals a second refusal, identical at both revisions and also unrelated: `uncensused Python builtin 'exec' at sw/builder/endstation_builder.py` (`receipts/tool-inventory/`).
   - The claim holds.

## Completion ledger (reviewer-owned)

| Lens | Result | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | UNCLEAN (F1, F2) | #737 scope item 1 and the manager's timeout comment; `scripts/ci_litex_legs.py`; `scripts/run_litex_sims.sh`; generated `.github/workflows/elaborate.yml`; hosted runs 41470524727, 41476923392 a1-a3, 41526004847, 41554508699, 41583428850 | R768-1 | aa3e2d85024c0aa17b32ed1165e23e65cfad49b0 |
| RTL | UNCLEAN (F3) | `.github/ci-templates/elaborate.yml`; structural diff of `.github/workflows/elaborate.yml` against base; `scripts/ci_gate_workflows.py`; cache save/restore lines of run 41583428850 | R768-1 | aa3e2d85024c0aa17b32ed1165e23e65cfad49b0 |
| Robustness | UNCLEAN (F1, F3) | runner `--only` and reconciliation; `union()`; `ci_gate_receipts.verify`; mutants R1-R11, L1-L12, G1-G4 and plants D1-D9 | R768-1 | aa3e2d85024c0aa17b32ed1165e23e65cfad49b0 |
| Tests | CLEAN | `scripts/ci_litex_legs_selftest.py`; `scripts/ci_gate_workflows_selftest.py`; `scripts/run_litex_sims.sh --selftest`; 45-plant mutation campaign; every listed gate rc 0 | R768-1 | aa3e2d85024c0aa17b32ed1165e23e65cfad49b0 |
| Docs | UNCLEAN (F1, F2) | `docs/testing/CI_WORKFLOWS.md` (Elaboration, receipts, projection table and prose); `docs/testing/TESTING.md` section 2; PR body; comment-rule scan of every added line | R768-1 | aa3e2d85024c0aa17b32ed1165e23e65cfad49b0 |

## Real limits

- **Real LiteX simulations were not run locally.** No migen or LiteX environment was installed. The leg runner, runner, union and aggregate verifier were exercised end to end with stub members.
  - Real-simulation evidence is the exact-head hosted run 41583428850: workers 2 to 4 passed 1 + 4 + 3 = 8 members, each once.
  - Its `elaborate` aggregate job ran after 388 s in the queue and printed `elaborate: 5 source gates exactly once; all worker jobs successful`, conclusion success. With executed LiteX steps, that verdict requires the LiteX union (`receipts/hosted/head-aggregate.results.txt`, `run-41583428850-jobs-final.json`).
  - This is an inspection of hosted evidence, not hosted acceptance.
- **Tool-inventory unmasking stopped at the second unrelated refusal.** A further refusal on this PR's own files beyond it is not excluded. This PR's declared pins were checked directly by hash.
- **The tool-cache isolation control was not executed.** Its plans were computed only.
- **No act, host act_ci or act_ci selftest was run, per the round rules.** The act scope-fixture change was checked statically.
- **Workflow wall clock:** the exact-head `elaborate` run took 2307 s from its first job start to its last job end, over 30 minutes. `elaborate-gates-3` waited 1268 s for a runner and the aggregate waited 388 s. Runner queueing predates this PR: `elaborate-gates-1` waited 1414 s and 824 s in base-era runs (`receipts/hosted/queue-delays.txt`). It is not attributed to this change.

## Pending manager duties

- Hosted and act acceptance, and the current-dev merge candidate with its builder and native banks.
- Accept or reject the exact-head hosted `elaborate` evidence (run 41583428850: aggregate success; 2307 s wall clock including 1656 s of queueing). Judge the #737 30-minute acceptance net of runner queueing.
- Physical calibration is NOT RUN, and field skips are not hardware proof.

## Prior public review findings

Read after this verdict and ledger were written. At this head PR #836 holds no prior review findings: its conversation has two review-start notices only (R767-1 and R768-1), and there are no PR reviews and no inline comments. Nothing is to be resolved or retained, and F1 to F3 are new in this round.

R768-1 FINISHED
