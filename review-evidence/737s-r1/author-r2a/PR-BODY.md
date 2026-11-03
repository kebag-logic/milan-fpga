[A727b]

## Contents

- **[Status](#status)** — Green/WIP/blocked, test tally, and `branch` -> `dev`.
- **[Linked Issue / roles](#linked-issue--roles)** — Public task, executor, and independent reviewers.
- **[Description](#description)** — What changed and why.
- **[Round 2](#round-2)** — The round 2 ruling's items, what is done, and the open decision.
- **[Authoritative references](#authoritative-references)** — Requirements/specification clauses and docs.
- **[How to get into the same state](#how-to-get-into-the-same-state)** — Copy-pasteable checkout/dependency/environment commands.
- **[How to validate](#how-to-validate)** — Exact reviewer commands and expected result.
- **[Known limitations / out of scope](#known-limitations--out-of-scope)** — What this deliberately does not do, and why.
- **[Definition of Done](#definition-of-done)** — The merge bar from [CONTRIBUTING.md](../CONTRIBUTING.md).

## Status

BLOCKED at `6a38c330` on a decision for round 2 item 3 (the CPU-netlist cache race; see [Round 2](#round-2)). Items 1 and 2 are committed, and the fast gates pass at that head. Items 3 to 5, the local runs of the re-derived legs and the dropped-simulation control are still to do. Branch `737-elab-split` -> `dev`, from `e61a4afa`.

## Linked Issue / roles

Relates to #737

Executor: `[A727b]` (round 2), `[A727]` (round 1)
Internal cleared-context reviewer: [R767]
External reviewer: [R768]

## Description

`elaborate-gates-1` ran builder leg 1 and then the whole standalone LiteX aggregate, eight simulations one after another. That made 2079 to 2672 seconds per job against a 45-minute limit. On PR #815 (run 41476923392, attempts 1 to 3) the job was cancelled at the limit, at 2735, 2734 and 2740 s. Hosted step times over those six runs: builder leg 1 869 to 1119 s, LiteX aggregate 1087 to 1511 s.

The generator now divides the template's "Standalone LiteX simulation aggregate" step into three measured legs on new workers, the same way it already divides the builder step. The template's commands, conditions and setup are unchanged.

| Piece | Change |
|---|---|
| `scripts/run_litex_sims.sh` | `--only NAME[,NAME...]` runs exactly those inventory members, in inventory order. The MISSING/UNLISTED reconciliation still covers the whole inventory in every leg. An unknown, repeated or empty name and a second `--only` are usage errors. Each run writes `<logdir>/verdicts.tsv`, one `name<TAB>verdict<TAB>seconds` row per member run. Its `--selftest` gains six checks (16 total). |
| `scripts/ci_litex_legs.py` (new) | Reads the inventory from `--list` and holds each member's hosted seconds measured alone in its leg (run 41583428850). It puts the longest first onto the least-loaded of three legs. It refuses an unmeasured member, a measurement for a member the inventory lost, and a leg above 973 measured seconds. `run N --receipt F -- scripts/run_litex_sims.sh <logdir>` adds the leg's `--only` and binds the verdict rows and the runner's exit to the head and tree. `union` requires every simulation exactly once, in its measured leg, PASS, with exit 0. |
| `scripts/ci_gate_workflows.py` | `LITEX_SPLIT` / `LITEX_WORKERS = (2, 3, 4)`. The divided step must end in its one aggregate command, and a preparation line may only run `--selftest`. Verilator setup goes to the LiteX workers only. Each LiteX worker uploads its `litex-leg-N.json`. |
| `scripts/ci_gate_receipts.py` | "Require every gate exactly once" also requires the LiteX union whenever a LiteX leg step ran, and refuses LiteX receipts from a skipped division. For `elaborate`, the gate-union digest covers the per-simulation verdicts. |
| `scripts/ci_litex_legs_selftest.py` (new), `scripts/ci_gate_workflows_selftest.py` | Plants a simulation dropped from its leg, one run in a second leg, one outside the inventory, a FAIL, a SKIP, a TIMEOUT, a red exit, a lost leg, a duplicated leg, a changed head, inventory or schema, an unmeasured member, a stale measurement and an over-budget leg. Every plant is refused. It holds each LiteX leg to the template's own step, and checks that only LiteX workers set up Verilator and retain a LiteX receipt. |
| `.github/workflows/elaborate.yml` | Regenerated: `elaborate-gates-0..4`, aggregate `needs` all five. Template change is a comment only. |
| Job maps | `scripts/act_ci.py` scope fixture (5 owners), `scripts/ci_scope_history.py` (workers 2 to 4), `scripts/ci_toolcache_isolation.py` (every `elaborate-gates-N` read from the workflow), `ci/image/audit_population.py`. |
| Records | `ci/image/command-table.json`: re-pinned `run_litex_sims.sh`, `ci_gate_workflows_selftest.py` and `ci_scope_history.py`, and added and (round 2) re-pinned `ci_litex_legs.py`. The two older pins had drifted before this change; that drift was reviewed (one inventory line and a comment; two lines adding `fast_tool_controls`). |
| Docs | `docs/testing/CI_WORKFLOWS.md` (Elaboration, receipts, projection table, workflow total), `docs/testing/TESTING.md` section 2. |

No timeout is raised: workers keep 45 minutes and the aggregate keeps 3. No step is made conditional, and no simulation is dropped.

**Legs and timing.** A member's seconds are its own verdict row in the three leg receipts of run 41583428850. That is the first hosted run with the legs apart, at `aa3e2d85`. Inside the old aggregate, after a builder leg in the same job, members cost otherwise: `test_ctrl_memory` took 113 s there and 280 s alone.

| Leg | Worker | Members | Measured hosted s |
|---|---|---|---:|
| 0/3 | `elaborate-gates-2` | `test_gptp_tx_timestamp` | 461 |
| 1/3 | `elaborate-gates-3` | `test_cpu_memory_port_cdc`, `test_gmii_rx_capture`, `test_pp_boot_bus_freeze`, `test_pp_mem_bridge`, `test_retained_cdc_storage` | 440 |
| 2/3 | `elaborate-gates-4` | `test_ctrl_memory`, `test_soc_timing_cuts` | 520 |

**Derived per job.** Setup is one figure everywhere: a worker's job span less its gate steps and its Verilator source build. That holds checkout, installs, cache transfers, recording and upload. The largest over every elaboration worker of the cited runs is 143 s (worker 1, run 41526004847).

A LiteX worker projects at that setup, plus 3 s of self-test, plus its leg. A Verilator cache miss adds the measured cold build of 411 s (run 41583428850; the other cold build there took 249 s). That run is the cold case: a workflow edit changes the key of every cache that hashes the workflow files. Workers 2 and 4 missed each of them (sv2v, the pip pins, sbt, the CPU metadata and Verilator). Worker 3 started 1268 s later and restored what worker 2 had saved.

On that run the LiteX workers took 585, 616 and 1226 s. The same projection of that run's own legs (240, 500 and 681 s) gives 797, 1057 and 1238 s cold, each at or above the measured span.

| Job | Derived s | Margin to 45 min | Margin to 30 min |
|---|---:|---:|---:|
| `elaborate-gates-0` (unchanged; projection, measured max 1254 cold, run 41583428850) | 1475 | 1225 | 325 |
| `elaborate-gates-1` (`2735 - 1495`, run 41476923392 attempt 1; 1183 at `aa3e2d85`) | 1240 | 1460 | 560 |
| `elaborate-gates-2` warm / cold | 607 / 1018 | 2093 / 1682 | 1193 / 782 |
| `elaborate-gates-3` warm / cold | 586 / 997 | 2114 / 1703 | 1214 / 803 |
| `elaborate-gates-4` warm / cold | 666 / 1077 | 2034 / 1623 | 1134 / 723 |

Workflow, with the documented 270 s aggregate/collector/watcher/tail allowance: 1745 s (29.1 min) on worker 0's projection. Before this change it was 2942 s (49 min) on worker 1's measured 2672. The runner-queueing statement and the run 41583428850 spans against #737 acceptance 1 are round 2 item 4, still to do.

## Round 2

The manager's round 2 ruling on #737 is the authority. Reviews R767-1 and R768-1 were both NEGATIVE, on MINOR findings only.

| Item | Findings | State |
|---|---|---|
| 1. Bounds from standalone measurements | R767-1-F1, R768-1-F1 | Done, `e80b44b5`. `SECONDS` comes from run 41583428850's leg receipts, and the legs are re-derived (461 / 440 / 520). One 143 s setup figure; the cold case uses the measured 411 s Verilator build and is reconciled with the measured cold `elaborate-gates-4` at 1226 s. `LEG_BUDGET` is 973 = 1800 - 270 - 143 - 411 - 3, which keeps a cold LiteX worker inside the workflow's 30 minutes. The comment and `CI_WORKFLOWS.md` name the runs. |
| 2. Worker 1 and builder-leg figures | R768-1-F2 | Done, `6a38c330`. Each figure is the maximum over the cited runs, run 41476923392 attempts 1 to 3 included: worker 1 1240 s, builder leg 1 869 to 1119 s, worker 0 measured 1254 s. |
| 3. CPU-netlist cache race | R768-1-F3 | **Blocked on a decision.** `actions/cache/restore@v4` is refused by the local act runner's trusted action set (`scripts/act_ci.py` `TRUSTED_ACTION_USES`): "uses unapproved action 'actions/cache/restore@v4'". `scripts/ci_events.py` `RECORDED_ACTIONS` and `scripts/ci_tool_inventory.py` also name only `actions/cache@`. `actions/cache@v4` has no restore-only mode. So restore-only through the template and the generator alone is not possible, and the options are posted on #737. |
| 4. Wall clock and runner queueing | R767-1-F2 | Not started (after item 3). |
| 5. R767-1-R1 text; suggestions | R767-1-R1, R767-1-S1, R768-1-S1 to S3 | Not started. |

## Authoritative references

- #737 scope item 1 (GitHub CI at most 30 min per workflow; leg membership from the suite's own inventory; a final job proves the union; no timeout raised, no step conditional, no test dropped), its [A10] comment on the `elaborate-gates-1` timeout, and its [A10] round 2 ruling.
- `docs/testing/CI_WORKFLOWS.md` "Elaboration" and the gate-receipt and projection sections.
- `docs/testing/TESTING.md` section 2; #297 (the LiteX aggregate's pinned inventory and selftest).
- `docs/testing/CI_IMAGE.md` "Regenerating source closures" (content-hash review).

## How to get into the same state

```sh
git fetch origin && git checkout 737-elab-split   # head 6a38c330, base dev e61a4afa
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
python3 scripts/ci_litex_legs_selftest.py
scripts/run_litex_sims.sh --selftest
python3 scripts/ci_litex_legs.py legs
for leg in 0 1 2; do
  python3 scripts/ci_litex_legs.py run $leg --receipt "$SCRATCH/litex-leg-$leg.json" -- scripts/run_litex_sims.sh "$SCRATCH/logs-$leg"
done
python3 scripts/ci_litex_legs.py union --head "$(git rev-parse HEAD)" --tree "$(git rev-parse 'HEAD^{tree}')" "$SCRATCH"/litex-leg-{0,1,2}.json
(cd tests && behave --no-capture -f plain)
git diff --check e61a4afa HEAD
```

Expected result / pass criteria: every command exits 0. `legs` prints `0/3 461s`, `1/3 440s` and `2/3 520s` with the members above. Each leg prints PASS once for each of its members, and `union` prints `litex: 8 simulations exactly once, each a pass`. If one simulation's row is removed from a leg receipt, `union` exits 1 with `LiteX leg N did not run its selection exactly once: <simulation>`. The aggregate verifier `scripts/ci_gate_receipts.py verify --workflow elaborate` gives the same refusal, prefixed `gate evidence refused:`.

Measured at `6a38c330` (16 CPUs), all rc 0:
- `ci_gate_workflows.py --check`;
- `ci_events.py --check`, and its `--selftest` (5579 arms, 255 s);
- the gate workflow and LiteX leg self-tests;
- `run_litex_sims.sh --selftest`;
- `legs`;
- behave (508 scenarios);
- `git diff --check`;
- the Python idiom gate;
- the docs workflow run steps that read the changed docs and scripts.

Not yet run at this head: the three leg commands on the re-derived partition, and the dropped-simulation control.

## Known limitations / out of scope

- `SECONDS` comes from one hosted run. Inside the old aggregate, `test_soc_timing_cuts` measured 355 to 534 s, against 240 alone, so a later re-measure may raise a leg. A leg above 973 measured seconds is refused until a leg is added.
- `elaborate-gates-0` is unchanged. Its projection of 1475 s (measured maximum 1254) binds the workflow, at 55 s inside 30 minutes on the projection.
- `ci/image/tool-inventory.json` is not regenerated. `scripts/ci_tool_inventory.py --check` already refuses at `e61a4afa`, on unrelated drift in `sw/builder/endstation_builder.py`, and gives the same refusal here. `ci/image/exec-audit-receipt.json` is an image trace pinned to an older source and is not regenerated either. The `act_ci.py` content pin is not refreshed, because it trails unrelated changes this PR did not review.
- `scripts/ci_toolcache_isolation.py` now reads all five workers. It was not rerun here, because it needs network installs for every leg; its step plans for all five workers were computed and accepted.

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
- [ ] Candidate merge result is validated per [CONTRIBUTING.md](../CONTRIBUTING.md)
- [x] Documentation is updated where needed
- [ ] Post-merge containment will be checked before the Issue moves to Done
