[A727e]

## Contents

- **[Status](#status)** — Green/WIP/blocked, test tally, and `branch` -> `dev`.
- **[Linked Issue / roles](#linked-issue--roles)** — Public task, executor, and independent reviewers.
- **[Description](#description)** — What changed and why.
- **[Round 2](#round-2)** — The round 2 ruling's items and how each is answered.
- **[Round 3](#round-3)** — The round 3 ruling's items, the ruling on the item 1 STOP, and how each is answered.
- **[Authoritative references](#authoritative-references)** — Requirements/specification clauses and docs.
- **[How to get into the same state](#how-to-get-into-the-same-state)** — Copy-pasteable checkout/dependency/environment commands.
- **[How to validate](#how-to-validate)** — Exact reviewer commands and expected result.
- **[Known limitations / out of scope](#known-limitations--out-of-scope)** — What this deliberately does not do, and why.
- **[Definition of Done](#definition-of-done)** — The merge bar from [CONTRIBUTING.md](../CONTRIBUTING.md).

## Status

Ready for round 3 review at `3b323864`. Round 3 items 1 to 4 and the ruling on the item 1 STOP (option (d), the bound on the job limit) are committed. The three legs ran locally at that head, each simulation PASS once, and the dropped-simulation control was refused and then restored. Every local gate below exits 0 at that head. #737 acceptance 1 (the workflow inside 30 minutes) stays open. Branch `737-elab-split` -> `dev`, from `e61a4afa`.

## Linked Issue / roles

Relates to #737

Executor: `[A727e]` (round 3, item 1 under the STOP ruling, the workflow figure and corrections), `[A727d]` (round 3, items 1 to 4 before the STOP), `[A727c]` (round 2, items 3 to 5), `[A727b]` (round 2, items 1 and 2), `[A727]` (round 1)
Internal cleared-context reviewer: [R767]
External reviewer: [R768]

## Description

`elaborate-gates-1` ran builder leg 1 and then the whole standalone LiteX aggregate, eight simulations one after another. That made 2079 to 2672 seconds per job against a 45-minute limit. On PR #815 (run 41476923392, attempts 1 to 3) the job was cancelled at the limit, at 2735, 2734 and 2740 s. Hosted step times over those six runs: builder leg 1 869 to 1119 s, LiteX aggregate 1087 to 1511 s.

The generator now divides the template's "Standalone LiteX simulation aggregate" step into three measured legs on new workers, the same way it already divides the builder step. The template's commands, conditions and setup are unchanged.

| Piece | Change |
|---|---|
| `scripts/run_litex_sims.sh` | `--only NAME[,NAME...]` runs exactly those inventory members, in inventory order. The MISSING/UNLISTED reconciliation still covers the whole inventory in every leg. An unknown, repeated or empty name and a second `--only` are usage errors. Each run writes `<logdir>/verdicts.tsv`, one `name<TAB>verdict<TAB>seconds` row per member run. Its `--selftest` gains six checks (16 total). |
| `scripts/ci_litex_legs.py` (new) | Reads the inventory from `--list` and holds each member's hosted seconds measured alone in its leg (run 41583428850). It puts the longest first onto the least-loaded of three legs. It refuses an unmeasured member, a measurement for a member the inventory lost, and a leg above `LEG_BUDGET` at each member's largest measured seconds (`LARGEST`). `LEG_BUDGET` is derived from named constants: the LiteX worker's 45-minute limit less 600 s of headroom and the largest setup, cold Verilator build and self-test, 1181 s. `run N --receipt F -- scripts/run_litex_sims.sh <logdir>` adds the leg's `--only` and binds the verdict rows and the runner's exit to the head and tree. `union` requires every simulation exactly once, in its measured leg, PASS, with an integer exit 0. |
| `scripts/ci_gate_workflows.py` | `LITEX_SPLIT` / `LITEX_WORKERS = (2, 3, 4)`; only `elaborate-gates-1`, whose builder leg runs the elaboration gates, carries the CPU metadata cache and its fill step; the `elaborate` aggregate checks out the head alone; a LiteX worker that is also a builder worker is refused. The divided step must end in its one aggregate command, and a preparation line may only run `--selftest`. Verilator setup goes to the LiteX workers only. Each LiteX worker uploads its `litex-leg-N.json`. The LiteX workers carry none of the builders' four shared caches (sv2v archive, pinned pip downloads, Scala toolchain, generated CPU metadata). Every builder and LiteX worker must carry each of them exactly once before the LiteX copies are removed. |
| `scripts/ci_gate_receipts.py` | "Require every gate exactly once" also requires the LiteX union whenever a LiteX leg step ran, and refuses LiteX receipts from a skipped division. For `elaborate`, the gate-union digest covers the per-simulation verdicts. |
| `scripts/ci_litex_legs_selftest.py` (new), `scripts/ci_gate_workflows_selftest.py` | Each of these plants is refused: a simulation dropped from its leg, one run in a second leg, one outside the inventory, a FAIL, a SKIP, a TIMEOUT, a red exit, a boolean exit, a lost leg, a duplicated leg, a changed head, inventory or schema, an unmeasured member, a stale measurement, an over-budget leg, a LiteX leg on a builder worker, a builder without its CPU metadata cache, and a LiteX worker repeating it. The self-tests also hold each LiteX leg to the template's own step. They check that only LiteX workers set up Verilator and retain a LiteX receipt, and that only builders carry the four shared caches. |
| `.github/workflows/elaborate.yml` | Regenerated: `elaborate-gates-0..4`, and the aggregate `needs` all five. The template changes are comments only. |
| Job maps | `scripts/act_ci.py` scope fixture (5 owners), `scripts/ci_scope_history.py` (workers 2 to 4), `scripts/ci_toolcache_isolation.py` (every `elaborate-gates-N` read from the workflow), `ci/image/audit_population.py`. The act runner's trusted action set is unchanged. |
| Records | `ci/image/command-table.json`: re-pinned `run_litex_sims.sh`, `ci_gate_workflows_selftest.py` and `ci_scope_history.py`. It added `ci_litex_legs.py`, which round 2 re-pinned twice. The two older pins had drifted before this change; that drift was reviewed (one inventory line and a comment; two lines adding `fast_tool_controls`). |
| Docs | `docs/testing/CI_WORKFLOWS.md` (Elaboration, receipts, projection table, workflow total), `docs/testing/TESTING.md` section 2. |

No timeout is raised: workers keep 45 minutes and the aggregate keeps 3. No step is made conditional, and no simulation is dropped.

**Legs and timing.** A member's seconds are its own verdict row in the three leg receipts of run 41583428850. That is the first hosted run with the legs apart, at `aa3e2d85`. Inside the old aggregate, after a builder leg in the same job, members cost otherwise: `test_ctrl_memory` took 113 s there and 280 s alone.

| Leg | Worker | Members | Measured hosted s | Local leg command s at `e180ba30` (per member) |
|---|---|---|---:|---:|
| 0/3 | `elaborate-gates-2` | `test_gptp_tx_timestamp` | 461 | 528 (527) |
| 1/3 | `elaborate-gates-3` | `test_cpu_memory_port_cdc`, `test_gmii_rx_capture`, `test_pp_boot_bus_freeze`, `test_pp_mem_bridge`, `test_retained_cdc_storage` | 440 | 398 (87, 1, 30, 14, 265) |
| 2/3 | `elaborate-gates-4` | `test_ctrl_memory`, `test_soc_timing_cuts` | 520 | 690 (142, 548) |

The local runs used cold CPU metadata, as a LiteX worker now does, on a shared 16-CPU host with a newer Python and Verilator. They show that each member runs and passes once; the bounds come from the hosted figures.

**Derived per job (round 2 figures; round 3 rebuilds them from component maxima, see [Round 3](#round-3)).** Setup is one figure everywhere: a worker's job span less its gate steps and its Verilator source build. That holds checkout, installs, cache transfers, recording and upload. The largest over every elaboration worker of the cited runs is 143 s (worker 1, run 41526004847).

A LiteX worker projects at that setup, plus 3 s of self-test, plus its leg. A Verilator cache miss adds the measured cold build of 411 s (run 41583428850; the other cold build there took 249 s). That run is the cold case: a workflow edit changes the key of every cache that hashes the workflow files. Workers 2 and 4 missed each of them (sv2v, the pip pins, sbt, the CPU metadata and Verilator). Worker 3 started 1268 s later and restored what worker 2 had saved.

On that run the LiteX workers took 585, 616 and 1226 s. The same projection of that run's own legs (240, 500 and 681 s) gives 797, 1057 and 1238 s cold, each at or above the measured span.

**The cost of keeping the shared caches off the LiteX workers.** Every LiteX run now downloads the sv2v archive, the pip pins and sbt, and generates its CPU metadata cold. `test_ctrl_memory` takes 280 s with cold metadata, against about 110 s warm (100 to 113 s inside the old aggregate). The projections already carry this cost:

- No LiteX leg of run 41583428850 had CPU metadata, since worker 3 restored the empty entry worker 2 had saved. So every member's measured seconds is its cold figure.
- Workers 2 and 4 set up in 94 and 131 s with every download missed, inside the 143 s setup.

So "warm" below means only that Verilator was restored.

| Job | Derived s | Margin to 45 min | Margin to 30 min |
|---|---:|---:|---:|
| `elaborate-gates-0` (unchanged; projection, measured max 1254 cold, run 41583428850) | 1475 | 1225 | 325 |
| `elaborate-gates-1` (`2735 - 1495`, run 41476923392 attempt 1; 1183 at `aa3e2d85`) | 1240 | 1460 | 560 |
| `elaborate-gates-2` warm / cold | 607 / 1018 | 2093 / 1682 | 1193 / 782 |
| `elaborate-gates-3` warm / cold | 586 / 997 | 2114 / 1703 | 1214 / 803 |
| `elaborate-gates-4` warm / cold | 666 / 1077 | 2034 / 1623 | 1134 / 723 |

**Workflow (round 2 figures; round 3 states the workflow figure as a measurement against #737 acceptance 1, see [Round 3](#round-3)).** With the documented 270 s aggregate/collector/watcher/tail allowance, the workflow projects at 1745 s (29.1 min) on worker 0's projection. Before this change it was 2942 s (49 min) on worker 1's measured 2672 s. **The projection excludes runner queueing.**

Run 41583428850 did not meet #737 acceptance 1 (the workflow inside 30 minutes, first job start to last job end). Measured from the first job start in the jobs API's whole seconds, `elaborate-gates-3` ended at 1883 s, the `elaborate` aggregate at 2307 s and `Collect CI manifest` at 2825 s. The cause was runner queueing: `elaborate-gates-3` waited 1268 s for a runner and the aggregate 388 s. The docs, fast RTL and full RTL workflows of that head were running at the same time, the full one with 19 shards.

Three legs put one more concurrent runner per head in that queue than two would. But queueing is an account-level limit shared by every workflow at a head, and one runner fewer would not have brought that run inside 30 minutes. So the three legs are kept, by the manager's decision, and acceptance 1 under concurrency stays open on #737.

## Round 2

The manager's round 2 ruling on #737 is the authority, with its ruling on the item 3 STOP (option (B)). Reviews R767-1 and R768-1 were both NEGATIVE, on MINOR findings only.

| Item | Findings | Commit | Answer |
|---|---|---|---|
| 1. Bounds from standalone measurements | R767-1-F1, R768-1-F1 | `e80b44b5` | `SECONDS` comes from run 41583428850's leg receipts, and the legs are re-derived (461 / 440 / 520). There is one 143 s setup figure. The cold case uses the measured 411 s Verilator build and is reconciled with the measured cold `elaborate-gates-4` at 1226 s. `LEG_BUDGET` is 973 = 1800 - 270 - 143 - 411 - 3, which keeps a cold LiteX worker inside the workflow's 30 minutes, runner queueing excluded. The comment and `CI_WORKFLOWS.md` name the runs. |
| 2. Worker 1 and builder-leg figures | R768-1-F2 | `6a38c330` | Each figure is the maximum over the cited runs, run 41476923392 attempts 1 to 3 included: worker 1 1240 s, builder leg 1 869 to 1119 s, worker 0 measured 1254 s. Item 3 changes none of them. |
| 3. CPU-netlist cache race | R768-1-F3 | `0eb3f57e` | Option (B), through the template and the generator only. Workers 2 to 4 carry none of the four shared cache steps (CPU metadata, Scala toolchain, pip pins, sv2v): no restore and no save. So only the builders populate those keys. The LiteX workers keep the Verilator cache, which only they populate. The template contract text says so. The act runner's trusted action set is unchanged. The per-run cost and why the LiteX projections hold with it are stated above. A builder without one of the caches, or a LiteX worker repeating one, is refused. |
| 4. Wall clock and runner queueing | R767-1-F2 | `39e3e00f` | Three legs stay. The projection excludes runner queueing. Run 41583428850's spans (1882 s, 2306 s, 2824 s) are recorded against #737 acceptance 1, with queueing named as the cause. Acceptance 1 under concurrency stays open on #737. |
| 5. R767-1-R1 text; suggestions | R767-1-R1, R767-1-S1, R768-1-S1 to S3 | `e180ba30` | R1's exact text: "are each refused, naming the simulation or the leg". Applied: R768-1-S2 (a comment that the repeated-simulation branch is defence in depth); R768-1-S3's boolean exit (refused, with a plant); R767-1-S1's disjoint-worker assertion (generator check, with a plant). Declined: the `run_litex_sims.sh` arms (R767-1-S1's three-member `--only` and FAIL row, R768-1-S3's trailing comma), because each needs a new content pin for that script; the runtime union refuses a truncated selection and a FAIL row by name, and the generated step never emits a trailing comma. Also declined: a sandbox arm through `run()` (R767-1-S1's S21, R768-1-S1), which needs new stub-interpreter infrastructure; the real leg runs and verify controls of this round exercise that path. |

## Round 3

The manager's round 3 ruling on #737 is the authority, with its ruling on the item 1 STOP: option (d), with the bound placed on the job limit. Reviews R767-2 and R768-2 were both NEGATIVE, on the same three MINOR findings. Both confirmed that the round 2 code does what the rulings asked.

| Item | Findings | Commits | Answer |
|---|---|---|---|
| 1. Bounds from component maxima, on the job limit | R767-2-F2, R768-2-F1 | `f66312c4`, `4f6cf352`, `e2426156` | Every elaboration projection and `LEG_BUDGET` is a sum of components, each the largest value over the cited runs: 41470524727, 41476923392 attempts 1 to 3, 41526004847, 41554508699, 41583428850, and 41678609075 attempts 1 to 3. Setup is 485 s (worker 3, attempt 3) and the cold Verilator build 431 s. `LEG_BUDGET` = 2700 - 600 headroom - 485 - 431 - 3 = 1181 s, derived in `scripts/ci_litex_legs.py` from named constants. Its self-test requires each LiteX worker's generated limit to equal 2700 s, and a mutant that changes the limit fails it. `LARGEST` now holds `test_soc_timing_cuts` 510, `test_gptp_tx_timestamp` 462 and `test_ctrl_memory` 284, so the legs hold 462 / 448 / 794 at `LARGEST` and fit. The three legs stay and `SECONDS` still derives them. Each worker is compared with 2700 s: worker 0 1615 (margin 1085), worker 1 1604 (1096), LiteX cold 1381 / 1367 / 1713 (1319 / 1333 / 987), and LiteX with Verilator restored 950 / 936 / 1282. Attempt 3's spans of 906 / 930 / 1194 s are below these. The re-measurement rule is stated once, in `CI_WORKFLOWS.md`; the job limit and headroom are not measurements. The aggregate's span less its checkout is 85 s in attempt 3, of which 82 s came before its first step, so the rule takes it: 104 s against its 3 minutes, margin 76 s. |
| 2. CPU-metadata cache | R767-2-F1, R768-2-F2 | `a174e9e5` | The workflow, the LiteX code and a local run establish who generates the metadata. The gates `ci_builder_legs.py` names for `--require-elaboration` all run in builder leg 1 and elaborate the SoC through LiteX, and LiteX generates the metadata there. A local cold run of `test_every_recipe_elaborates` alone wrote it. Builder leg 0 elaborates nothing: worker 0 saved the key empty (200 or 201 B) at a cold key. No worker reads the metadata without generating it, because LiteX generates whatever it lacks. So `elaborate-gates-1` alone carries `Cache the generated CPU metadata` and the step that fills its directory. `elaborate-gates-0` carries neither, and the LiteX workers carry neither (option (B)). Generation refuses a worker missing or repeating either step, and elaboration gates split across builder legs. The template contract, the `BUILDER_CACHES` comment and `CI_WORKFLOWS.md` say so. The "about 110 s warm" figure for `test_ctrl_memory` is now named for what it was: metadata builder leg 1 had generated earlier in the same job, not a restore. |
| 3. The aggregate's checkout | R767-2-F3, R768-2-F3 | `e4d52a12`, `d153844b` | The `elaborate` aggregate reads only the head's tree: the receipts' source identity, the template and the runners' inventories. It now checks out the head at the default depth. Its limit stays 3 minutes against its 104 s projection. `Collect CI manifest` keeps its full fetch, because it reads the pull request's merge base; it took at most 149 s against 15 minutes. The workers keep theirs for the scope diff, under 45 minutes. The docs aggregate is unchanged. The act sandbox validation accepts the workflow. `d153844b` moves the paragraph back out of the receipts paragraph it had run into, and records that attempt 3 cancelled the old full-history fetch again. |
| 4. Residues and suggestions | R767-2-R1, R767-2-S1, R768-2-S1 to S4, R768-2-RS1 | `ae7412eb` | R767-2-R1 and R767-2-S1: the sentence is gone, and worker 1 now projects at its component sum, setup plus builder leg 1 (item 1). R768-2-S1 applied: the self-test names the shared caches, the metadata steps and their worker literally, and its mutant (the metadata cache dropped from `BUILDER_CACHES`) now fails it. R768-2-S2 applied: 1883 / 2307 / 2825 s, the jobs API's whole seconds. R768-2-S3: the fill step has left the LiteX workers (item 2). Declined: splitting the placement step, which still copies from an absent directory; it also places the VexiiRiscv source every worker needs, its script is pinned by the event contract, and the copy is a no-op. R768-2-S4: observation, no change. R768-2-RS1: its exact text, in the round 2 table above. |
| STOP ruling: the workflow figure | - | `4dc72137`, `3b323864` | The workflow figure is a measurement against #737 acceptance 1, not a bound, and acceptance 1 stays open on #737. By the component-maxima rule, with the 398 s allowance (aggregate 104, collector 149, watcher 120, tail 25), it is 2013 s with Verilator restored (builder worker 0) and 2111 s at a cold Verilator key (LiteX worker 4). The ruling's "about 1953 s" used the aggregate's figure before attempt 3, with a 338 s allowance. Most of the rise over attempt 1's maxima (1723 s) is setup: the full-history worker checkout (up to 208 s), the LiteX workers' uncached LiteX install (up to 143 s) and the VexiiRiscv placement (up to 59 s). Two candidates for acceptance 1 are recorded and not taken: a shallower worker checkout, which would widen the act checkout contract, and a pip cache on the LiteX workers, which would reverse option (B). Run 41678609075 did not meet acceptance 1 either. Attempt 1 ended at 1767 s, but its aggregate was cancelled before the union proof. Attempt 3 ended at 2646 s, after workers waited up to 1043 s for a runner. |

**The STOP and its ruling.** Attempt 3 of run 41678609075 finished after `f66312c4` was committed. All five workers passed and every simulation ran once. Its setups of 362 to 485 s and `test_soc_timing_cuts` at 510 s broke that commit's 30-minute-based `LEG_BUDGET` (543 s, which no three-leg partition fits) and its workflow projection. The manager ruled option (d). The bound is the job limit with 600 s of stated headroom. Three legs stay. The workflow figure is stated as a measurement against acceptance 1, which stays open.

## Authoritative references

- #737 scope item 1 (GitHub CI at most 30 min per workflow; leg membership from the suite's own inventory; a final job proves the union; no timeout raised, no step conditional, no test dropped) and acceptance 1, its [A10] comment on the `elaborate-gates-1` timeout, its [A10] round 2 ruling, its [A10] ruling on the item 3 STOP, its [A10] round 3 ruling and its [A10] ruling on the round 3 item 1 STOP (option (d)).
- `docs/testing/CI_WORKFLOWS.md` "Elaboration" and the gate-receipt and projection sections.
- `docs/testing/TESTING.md` section 2; #297 (the LiteX aggregate's pinned inventory and selftest).
- `docs/testing/CI_IMAGE.md` "Regenerating source closures" (content-hash review).

## How to get into the same state

```sh
git fetch origin && git checkout 737-elab-split   # head 3b323864, base dev e61a4afa
git submodule update --init third_party/verilog-axis protocol-processor gptp-processor
python3 -m venv "$SCRATCH/litex-venv" && export PATH="$SCRATCH/litex-venv/bin:$PATH"
python3 -m pip install pyyaml && python3 -m pip install -r sw/litex/litex_pins.txt
python3 scripts/ci_litex_env.py && sw/litex/patches/apply.sh
# Verilator and the pinned RV32 SDK at $HOME/br-milan-rv32/host, as the elaborate workflow installs them
```

## How to validate

```sh
python3 scripts/ci_gate_workflows.py --check
python3 scripts/ci_events.py --check && python3 scripts/ci_events.py --selftest
python3 scripts/ci_gate_workflows_selftest.py
(cd scripts && python3 ci_litex_legs_selftest.py)
scripts/run_litex_sims.sh --selftest
python3 scripts/ci_litex_legs.py legs
for leg in 0 1 2; do
  python3 scripts/ci_litex_legs.py run $leg --receipt "$SCRATCH/litex-leg-$leg.json" -- scripts/run_litex_sims.sh "$SCRATCH/logs-$leg"
done
python3 scripts/ci_litex_legs.py union --head "$(git rev-parse HEAD)" --tree "$(git rev-parse 'HEAD^{tree}')" "$SCRATCH"/litex-leg-{0,1,2}.json
(cd tests && behave --no-capture -f plain)
git diff --check e61a4afa HEAD
```

Expected result / pass criteria:

- Every command exits 0.
- `legs` prints `0/3 461s, at its largest 462s`, `1/3 440s, at its largest 448s` and `2/3 520s, at its largest 794s` with the members above; each is at most `LEG_BUDGET`, 1181.
- Each leg prints PASS once for each of its members, and `union` prints `litex: 8 simulations exactly once, each a pass`.
- If one simulation's row is removed from a leg receipt, `union` exits 1 with `LiteX leg N did not run its selection exactly once: <simulation>`. The aggregate verifier `scripts/ci_gate_receipts.py verify --workflow elaborate` gives the same refusal, prefixed `gate evidence refused:`.
- In the generated `elaborate.yml`, `elaborate-gates-2` to `-4` hold no `Cache verified sv2v archive`, `Cache the pinned pip downloads`, `Cache the Scala toolchain` or `Cache the generated CPU metadata` step. `elaborate-gates-0` and `-1` hold the first three once each, and only `elaborate-gates-1` holds the metadata cache and `Keep the generated CPU netlist arguments for the next run`. The `elaborate` aggregate's checkout carries no `fetch-depth`.

Measured at `3b323864` (16 CPUs). Each of these exited 0:

- `ci_gate_workflows.py --check`;
- `ci_events.py --check`, and its `--selftest` (2199 items, 5489 arms, 223 s);
- the gate workflow and LiteX leg self-tests;
- `run_litex_sims.sh --selftest` (16 checks);
- `legs`;
- the three leg commands, 571, 410 and 661 s, with each simulation PASS once: `test_gptp_tx_timestamp` 570; `test_cpu_memory_port_cdc` 92, `test_gmii_rx_capture` 0, `test_pp_boot_bus_freeze` 31, `test_pp_mem_bridge` 15, `test_retained_cdc_storage` 272; `test_ctrl_memory` 84, `test_soc_timing_cuts` 576;
- `union` over those receipts, and the aggregate verifier over them;
- `ci_scope.py --selftest`;
- behave (508 scenarios);
- `git diff --check e61a4afa HEAD`;
- the act sandbox validation of the workflow;
- the docs workflow run steps that read the changed docs, template and scripts.

The control drops `test_pp_boot_bus_freeze` from leg 1's real receipt. `union` and the aggregate verifier each refuse it with the words above, and both pass again once it is restored. A mutant that sets a LiteX worker's limit to 44 minutes fails the LiteX leg self-test, because `LEG_BUDGET` starts from 2700 s. The local leg times come from a shared host with a newer Python and Verilator, and `test_ctrl_memory` found CPU metadata a local run had already generated. They show that each member runs and passes once. The bounds come from the hosted figures.

## Known limitations / out of scope

- The legs come from one hosted run (`SECONDS`), and the bounds come from `LARGEST` and the component maxima. A later hosted measurement above a figure replaces it, by the rule in `CI_WORKFLOWS.md`, and a leg that no longer fits `LEG_BUDGET` is refused until the legs are re-derived.
- The workflow figure, 2013 s with Verilator restored and 2111 s cold, is above #737 acceptance 1's 30 minutes. It is a measurement, not a bound, and acceptance 1 stays open on #737, with the shallower worker checkout and a LiteX pip cache as candidates not taken here.
- Only a hosted run at the pushed head can show the non-empty `Cache the generated CPU metadata` restore, on `elaborate-gates-1` in its second attempt. The manager triggers it after the push.
- The docs workflow's `docs-check` aggregate has the same full-history checkout under the same 3-minute limit. It is not changed here: round 3's item 3 names elaborate jobs only.
- `ci/image/tool-inventory.json` is not regenerated. `scripts/ci_tool_inventory.py --check` already refuses at `e61a4afa`, on unrelated drift in `sw/builder/endstation_builder.py`, and gives the same refusal here. It still lists `elaborate-gates-0`'s `Cache the generated CPU metadata`. `ci/image/exec-audit-receipt.json` is an image trace pinned to an older source and is not regenerated either. The `act_ci.py` content pin is not refreshed, because it trails unrelated changes this PR did not review.
- `scripts/ci_toolcache_isolation.py` reads all five workers, and its step windows compute for each. It was not rerun here, because it needs network installs for every leg.

## Definition of Done

- [ ] Linked Issue acceptance criteria are satisfied (acceptance 1 under concurrency stays open on #737)
- [x] New or changed behavior has self-checking tests
- [x] Required local verification bar passes
- [ ] Self-test evidence is posted in a PR comment
- [x] No undocumented requirement or interface change remains
- [ ] Internal cleared-context review is positive
- [ ] External review is positive
- [ ] Blocking and major findings are fixed and re-reviewed
- [ ] No review round remains in flight
- [ ] Candidate merge result is validated per [CONTRIBUTING.md](../CONTRIBUTING.md)
- [x] Documentation is updated where needed
- [ ] Post-merge containment will be checked before the Issue moves to Done

