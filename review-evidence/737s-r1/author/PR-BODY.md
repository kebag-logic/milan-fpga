[A727]

## Contents

- **[Status](#status)** — Green/WIP/blocked, test tally, and `branch` -> `dev`.
- **[Linked Issue / roles](#linked-issue--roles)** — Public task, executor, and independent reviewers.
- **[Description](#description)** — What changed and why.
- **[Authoritative references](#authoritative-references)** — Requirements/specification clauses and docs.
- **[How to get into the same state](#how-to-get-into-the-same-state)** — Copy-pasteable checkout/dependency/environment commands.
- **[How to validate](#how-to-validate)** — Exact reviewer commands and expected result.
- **[Known limitations / out of scope](#known-limitations--out-of-scope)** — What this deliberately does not do, and why.
- **[Definition of Done](#definition-of-done)** — The merge bar from [CONTRIBUTING.md](../CONTRIBUTING.md).

## Status

GREEN locally at `aa3e2d85` — every gate below rc 0 except the planted controls, which are refused as intended. The three LiteX legs pass locally: 8 of 8 simulations, each once. Branch `737-elab-split` -> `dev`, from `e61a4afa`.

## Linked Issue / roles

Relates to #737

Executor: `[A727]`
Internal cleared-context reviewer: [R767]
External reviewer: [R768]

## Description

`elaborate-gates-1` ran builder leg 1 and then the whole standalone LiteX aggregate, eight simulations one after another. That made 2079 to 2672 seconds per job against a 45-minute limit, and on PR #815 it was cancelled at the limit with every simulation passing. Hosted step times: builder leg 1 869 to 1075 s, LiteX aggregate 1087 to 1485 s.

The generator now divides the template's "Standalone LiteX simulation aggregate" step into three measured legs on new workers, the same way it already divides the builder step. The template's commands, conditions and setup are unchanged.

| Piece | Change |
|---|---|
| `scripts/run_litex_sims.sh` | `--only NAME[,NAME...]` runs exactly those inventory members, in inventory order. The MISSING/UNLISTED reconciliation still covers the whole inventory in every leg. An unknown, repeated or empty name and a second `--only` are usage errors. Each run writes `<logdir>/verdicts.tsv`, one `name<TAB>verdict<TAB>seconds` row per member run. Its `--selftest` gains six checks (16 total). |
| `scripts/ci_litex_legs.py` (new) | Reads the inventory from `--list`, holds each member's largest measured hosted seconds, and puts the longest first onto the least-loaded of three legs. It refuses an unmeasured member, a measurement for a member the inventory lost, and a leg above 1200 measured seconds. `run N --receipt F -- scripts/run_litex_sims.sh <logdir>` adds the leg's `--only` and binds the verdict rows and the runner's exit to the head and tree. `union` requires every simulation exactly once, in its measured leg, PASS, with exit 0. |
| `scripts/ci_gate_workflows.py` | `LITEX_SPLIT` / `LITEX_WORKERS = (2, 3, 4)`. The divided step must end in its one aggregate command, and a preparation line may only run `--selftest`. Verilator setup goes to the LiteX workers only. Each LiteX worker uploads its `litex-leg-N.json`. |
| `scripts/ci_gate_receipts.py` | "Require every gate exactly once" also requires the LiteX union whenever a LiteX leg step ran, and refuses LiteX receipts from a skipped division. For `elaborate`, the gate-union digest covers the per-simulation verdicts. |
| `scripts/ci_litex_legs_selftest.py` (new), `scripts/ci_gate_workflows_selftest.py` | Plants a simulation dropped from its leg, one run in a second leg, one outside the inventory, a FAIL, a SKIP, a TIMEOUT, a red exit, a lost leg, a duplicated leg, a changed head, inventory or schema, an unmeasured member, a stale measurement and an over-budget leg. Every plant is refused, by name. It holds each LiteX leg to the template's own step, and checks that only LiteX workers set up Verilator and retain a LiteX receipt. |
| `.github/workflows/elaborate.yml` | Regenerated: `elaborate-gates-0..4`, aggregate `needs` all five. Template change is a comment only. |
| Job maps | `scripts/act_ci.py` scope fixture (5 owners), `scripts/ci_scope_history.py` (workers 2 to 4), `scripts/ci_toolcache_isolation.py` (every `elaborate-gates-N` read from the workflow), `ci/image/audit_population.py`. |
| Records | `ci/image/command-table.json`: re-pinned `run_litex_sims.sh`, `ci_gate_workflows_selftest.py` and `ci_scope_history.py`, and added `ci_litex_legs.py`. The two older pins had drifted before this change; that drift was reviewed (one inventory line and a comment; two lines adding `fast_tool_controls`). |
| Docs | `docs/testing/CI_WORKFLOWS.md` (Elaboration, receipts, projection table, workflow total), `docs/testing/TESTING.md` section 2. |

No timeout is raised: workers keep 45 minutes and the aggregate keeps 3. No step is made conditional, and no simulation is dropped.

**Legs and timing.** Member seconds are the largest hosted times over runs 41470524727, 41526004847 and 41554508699, and over #815's run 41476923392 attempts 1 to 3.

| Leg | Worker | Members | Measured hosted s | Local leg command s |
|---|---|---|---:|---:|
| 0/3 | `elaborate-gates-2` | `test_soc_timing_cuts` | 534 | 566 |
| 1/3 | `elaborate-gates-3` | `test_gmii_rx_capture`, `test_gptp_tx_timestamp`, `test_pp_boot_bus_freeze`, `test_pp_mem_bridge` | 518 | 589 |
| 2/3 | `elaborate-gates-4` | `test_cpu_memory_port_cdc`, `test_ctrl_memory`, `test_retained_cdc_storage` | 533 | 578 |

Derived per job. A LiteX worker is 143 s of setup and evidence (the most worker 1 spent outside its gate steps), plus 3 s of selftest, plus its leg, plus 60 s. A cold Verilator source build adds about 300 s.

| Job | Derived s | Margin to 45 min | Margin to 30 min |
|---|---:|---:|---:|
| `elaborate-gates-0` (unchanged; projection, measured max 1227) | 1475 | 1225 | 325 |
| `elaborate-gates-1` (`2672 - 1485`) | 1187 | 1513 | 613 |
| `elaborate-gates-2` warm / cold | 740 / 1040 | 1960 / 1660 | 1060 / 760 |
| `elaborate-gates-3` warm / cold | 724 / 1024 | 1976 / 1676 | 1076 / 776 |
| `elaborate-gates-4` warm / cold | 739 / 1039 | 1961 / 1661 | 1061 / 761 |

Workflow, with the documented 270 s aggregate/collector/watcher/tail allowance: 1745 s (29.1 min) on worker 0's projection, and 1497 s (25 min) on its measured maximum. Before this change it was 2942 s (49 min) on worker 1's measured 2672.

Why three legs: two legs (760/825 s) would also fit. Three leave more room for hosted variance (the aggregate ranged 1087 to 1485 s on one day) and for a new multi-minute simulation before a re-partition. They also keep each leg's command short enough to run whole locally in one go. The cost is one more runner's setup, about 143 s per run. The wall clock does not change, because the builder workers bind it.

## Authoritative references

- #737 scope item 1 (GitHub CI at most 30 min per workflow; leg membership from the suite's own inventory; a final job proves the union; no timeout raised, no step conditional, no test dropped), and its [A10] comment on the `elaborate-gates-1` timeout.
- `docs/testing/CI_WORKFLOWS.md` "Elaboration" and the gate-receipt and projection sections.
- `docs/testing/TESTING.md` section 2; #297 (the LiteX aggregate's pinned inventory and selftest).
- `docs/testing/CI_IMAGE.md` "Regenerating source closures" (content-hash review).

## How to get into the same state

```sh
git fetch origin && git checkout 737-elab-split   # head aa3e2d85, base dev e61a4afa
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
scripts/run_litex_sims.sh --selftest
python3 scripts/ci_litex_legs.py legs
for leg in 0 1 2; do
  python3 scripts/ci_litex_legs.py run $leg --receipt "$SCRATCH/litex-leg-$leg.json" -- scripts/run_litex_sims.sh "$SCRATCH/logs-$leg"
done
python3 scripts/ci_litex_legs.py union --head "$(git rev-parse HEAD)" --tree "$(git rev-parse 'HEAD^{tree}')" "$SCRATCH"/litex-leg-{0,1,2}.json
(cd tests && behave --no-capture -f plain)
git diff --check e61a4afa HEAD
```

Expected result / pass criteria: every command exits 0. Each leg prints PASS once for each of its members. `union` prints `litex: 8 simulations exactly once, each a pass`. If one simulation's row is removed from a leg receipt, `union` exits 1 with `LiteX leg 1 did not run its selection exactly once: test_pp_boot_bus_freeze`. The aggregate verifier `scripts/ci_gate_receipts.py verify --workflow elaborate` gives the same refusal, prefixed `gate evidence refused:`.

Measured at `aa3e2d85` (16 CPUs): ci_events selftest 5579 arms PASS, 263 s. Gate workflow selftest PASS. run_litex_sims selftest 16/16. Legs 566 / 589 / 578 s, all PASS. behave: 508 scenarios passed. The docs workflow's run steps pass, with installs replaced by the same pinned requirements in a private venv; the end-station builder bank was not rerun, because it reads none of the changed files.

## Known limitations / out of scope

- The figures are hosted measurements plus allowances, not a hosted run of this head. The first hosted run after any workflow edit misses the Verilator cache, whose key hashes the workflow files, so it is the cold case on all three LiteX workers (derived at most 1040 s).
- `elaborate-gates-0` is unchanged. Its projection of 1475 s (measured maximum 1227) now binds the workflow, at 55 s inside 30 minutes on the projection.
- `ci/image/tool-inventory.json` is not regenerated. `scripts/ci_tool_inventory.py --check` already refuses at `e61a4afa`, on unrelated drift in `sw/builder/endstation_builder.py`, and gives the same refusal here. `ci/image/exec-audit-receipt.json` is an image trace pinned to an older source and is not regenerated either. The `act_ci.py` content pin is not refreshed, because it trails unrelated changes this PR did not review.
- `scripts/ci_toolcache_isolation.py` now reads all five workers. It was not rerun here, because it needs network installs for every leg; its step plans for all five workers were computed and accepted.
- Member seconds need a hosted re-measure when a simulation's cost changes. A leg above 1200 measured seconds is refused until a leg is added.

## Definition of Done

- [ ] Linked Issue acceptance criteria are satisfied
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
