# HANDOFF — [A727] issue #737, elaborate LiteX aggregate split

Lane: $LANES/737-elab-split, branch 737-elab-split, base dev e61a4afa (local only; nothing pushed).
Head: aa3e2d85024c0aa17b32ed1165e23e65cfad49b0 (6 commits over e61a4afa).
Scratch: $VALIDATION_STORAGE/737-a727. CPUs booked: 64-79 (unit milan-737-a727.service). Receipts: receipts/ beside this file.

## Status

- [x] remote https://github.com/kebag-logic/milan-fpga.git, base e61a4afa = origin/dev at start
- [x] TAKEN posted: issuecomment-6594976273
- [x] design and implementation
- [x] gates (table below), all at head aa3e2d85
- [x] REVIEW READY posted: issuecomment-6596110490 (head aa3e2d85)

## What changed

The defect: `elaborate-gates-1` ran builder leg 1 (869-1075 s hosted) and then the whole standalone LiteX
aggregate (1087-1485 s) under a 45-minute limit; 2079-2672 s per job, cancelled at the limit on #815.

The generator now divides the template's "Standalone LiteX simulation aggregate" step into three measured
legs on new workers `elaborate-gates-2`, `-3`, `-4`, the same way it already divides the builder step.
Workers 0 and 1 keep the two builder legs and lose the aggregate and the Verilator setup. Leg membership is
derived from `run_litex_sims.sh --list` and measured hosted seconds (longest first onto the least-loaded leg);
an unmeasured member, a stale measurement and a leg above 1200 measured seconds are refused. Each leg runs
the template's own command through `scripts/ci_litex_legs.py run N --receipt ... -- scripts/run_litex_sims.sh <logdir>`,
which adds `--only <leg members>`; the runner still reconciles the whole inventory (MISSING/UNLISTED) in every
leg and writes `verdicts.tsv`. The `elaborate` aggregate ("Require every gate exactly once",
`ci_gate_receipts.py verify`) now also requires the LiteX union: every simulation exactly once, in its
measured leg, PASS, runner exit 0; the gate-union digest covers the per-simulation verdicts for
`ci_runtime_evidence`. No timeout raised (workers keep 45 min, aggregate 3 min), no step made conditional,
no simulation dropped.

Why three legs and not two: two legs (760/825 measured s) would also meet the bound (slowest derived
~1031 s warm). Three (534/518/533) leave more margin under hosted variance (the aggregate step ranged
1087-1485 s across same-day runs) and room for a new multi-minute simulation before a re-partition; and
each leg's command then fits one local foreground run here (the 825 s leg would not). Cost: one more
runner's setup, about 143 s of runner time per run; wall clock unchanged (builder workers bind it).

## Per-leg timing (measured and derived)

Hosted measured, from `gh api .../actions/runs/<id>/jobs` and the job logs (gaps between consecutive result lines):

| Run | w0 job s | w1 job s | builder leg 1 s | LiteX step s | w1 outside its 2 gate steps |
|---|---:|---:|---:|---:|---:|
| 41470524727 (dev push) | 1015 | 2079 | 869 | 1087 | 123 |
| 41526004847 (#810) | 1227 | 2233 | 929 | 1161 | 143 |
| 41554508699 (#834) | 992 | 2672 | 1075 | 1485 | 112 |
| 41476923392 attempts 1-3 (#815) | - | cancelled at limit | - | - | - |

Per-simulation hosted maximum over the 3 passing runs and #815's attempts 1-3 (these are `SECONDS` in
scripts/ci_litex_legs.py:34): soc_timing_cuts 534, gptp_tx_timestamp 477, retained_cdc_storage 348,
ctrl_memory 113, cpu_memory_port_cdc 72, pp_boot_bus_freeze 26, pp_mem_bridge 14, gmii_rx_capture 1.

| Leg | Worker | Members | Measured hosted s | Local measured s (leg command, CPUs 64-79) |
|---|---|---|---:|---:|
| 0/3 | elaborate-gates-2 | test_soc_timing_cuts | 534 | 566 (sim 565) |
| 1/3 | elaborate-gates-3 | gmii_rx_capture, gptp_tx_timestamp, pp_boot_bus_freeze, pp_mem_bridge | 518 | 589 (0, 543, 31, 14) |
| 2/3 | elaborate-gates-4 | cpu_memory_port_cdc, ctrl_memory, retained_cdc_storage | 533 | 578 (88, 206, 284) |

Local differs from hosted: Python 3.14 (hosted 3.12), host Verilator 5.052 (hosted pinned 5.050), a cold
Scala metadata run inside ctrl_memory (hosted restores it from cache), shared host.

Derived per-job worst case (docs/testing/CI_WORKFLOWS.md method; LiteX worker = 143 s outside the gate steps
+ 3 s selftest + leg seconds + 60 s recording/upload; cold = +300 s Verilator source build on a cache miss):

| Job | Derived s | vs 45-min timeout (2700) | vs 30 min (1800) | vs 60% bound (1620) |
|---|---:|---:|---:|---:|
| elaborate-gates-0 (unchanged; doc projection, measured max 1227) | 1475 | 1225 | 325 | 145 |
| elaborate-gates-1 (2672 - 1485) | 1187 | 1513 | 613 | 433 |
| elaborate-gates-2 warm / cold | 740 / 1040 | 1960 / 1660 | 1060 / 760 | 880 / 580 |
| elaborate-gates-3 warm / cold | 724 / 1024 | 1976 / 1676 | 1076 / 776 | 896 / 596 |
| elaborate-gates-4 warm / cold | 739 / 1039 | 1961 / 1661 | 1061 / 761 | 881 / 581 |
| elaborate (aggregate), measured max 61 | 61 | 119 of its 180 | - | - |

Workflow: slowest worker + the doc's 270 s aggregate/collector/watcher/tail allowance = 1745 s (29.1 min)
on worker 0's projection, 1497 s (25 min) on its measured maximum. Before: worker 1's measured 2672 s
put it at 2942 s (49 min). Note: the first hosted run after any workflow edit misses the Verilator cache
(its key hashes the workflow files), so this PR's first run is the cold case on all three LiteX workers.

## Changes (file:line)

Commits (one-line subjects, no body, no trailers):
- c35e416d Run a named subset of the standalone LiteX simulations with --only ... (#737)
- bcee9fdc Run the LiteX simulations in three measured legs on elaborate workers of their own ... (#737)
- a04a1892 Map the three LiteX elaborate workers in the act scope fixture, the scope history, ... (#737)
- 7b5fd6f7 Describe the three measured LiteX legs, their union proof and the elaborate worker projections ... (#737)
- 789a7651 Pin the reviewed LiteX leg runner and the three changed LiteX and gate scripts in the image command table (#737)
- aa3e2d85 Wrap the LiteX union's verdict digest within the 120-column Python rule and re-pin the leg runner (#737)

- scripts/run_litex_sims.sh:38 doc block; :128 SELECTED; :166 select_members; :196/:236/:267 verdicts.tsv;
  :419 four new selftest arms (6 checks; 16 total); :463 `--only` parsing; :474 refusal outside a run.
- scripts/ci_litex_legs.py (new): :34 SECONDS, :44 LEGS = 3, :48 LEG_BUDGET, :52 inventory, :63 partition,
  :94 run, :121 union, :175 parse (`run`, `union`, `legs`).
- scripts/ci_litex_legs_selftest.py (new): :42 partition controls, :58 union controls, :97 split controls,
  :116 step controls, :136 worker controls (Verilator only on LiteX workers, receipt retention), :149 verify controls.
- scripts/ci_gate_workflows.py:40-42 LITEX_SPLIT/LITEX_WORKERS/LITEX_COMMAND (LONG_GATE removed); :107 divided;
  :113 case_inventory; :188 split_litex_run; :201 litex_leg_step; :220 litex receipt upload; :407 Verilator setup
  only on LiteX workers; :413 leg step.
- scripts/ci_gate_receipts.py:32 Collected.litex; :86/:122/:130 LiteX union in verify; :169/:180 CLI.
- scripts/ci_gate_workflows_selftest.py:26, :511, :537 retention_controls, :558, :572, :623, :639, :642.
- .github/ci-templates/elaborate.yml:333 comment only; .github/workflows/elaborate.yml regenerated
  (jobs at :10, :245, :480, :764, :1048).
- scripts/act_ci.py:6421 scope fixture owner count 2 -> 5; scripts/ci_scope_history.py:296-300 adds workers 2-4;
  scripts/ci_toolcache_isolation.py:62/:418 legs derived from the workflow's elaborate-gates-N jobs;
  ci/image/audit_population.py:51-53 job list.
- docs/testing/CI_WORKFLOWS.md:1592-1606 (tool-cache control), :1623, :1654-1685 (LiteX legs), :3026, :3084-3098
  (projection), :3115-3118 (table), :3156-3161 (workflow), :3170-3180 (receipts); docs/testing/TESTING.md:690, :709-719.
- ci/image/command-table.json:13588, :13611, :13659, :13754.

## Records touched

| Record | Touched | How / why not |
|---|---|---|
| .github/workflows/elaborate.yml | yes | regenerated by `python3 scripts/ci_gate_workflows.py`; `--check` rc 0 |
| scripts/ci_events.py | no change needed | it compares the workflow with the generator's output; `--check` rc 0, `--selftest` rc 0 (5579 arms) |
| ci/image/command-table.json | yes | documented procedure "Review script changes before updating their content hashes": re-pinned run_litex_sims.sh, ci_gate_workflows_selftest.py, ci_scope_history.py and added ci_litex_legs.py. The two older pins had drifted before this lane; I reviewed that drift (an inventory line and a comment; two lines adding fast_tool_controls). act_ci.py's pin NOT refreshed: 221 lines of unrelated drift since the pinned dcd4d98a |
| ci/image/tool-inventory.json | no | `ci_tool_inventory.py --write/--check` refuses at base e61a4afa and at head on unrelated drift ("changed declared script 'sw/builder/endstation_builder.py'"); receipts g18-* |
| ci/image/exec-audit-receipt.json, exec-audit.json | no | image trace receipt pinned at source 54fbcba6, regenerated only by the image trace procedure (docker, every docs/elaborate/rtl-fast step); not maintained per change |
| ci/image/audit_population.py | yes | elaborate job list gains workers 2-4 so the next trace reaches them |
| act job map | yes | scripts/act_ci.py:6421 scope-fixture owners; the act selftest (d39) passes with 18 elaborate scope arms |
| local act job set, signed local manifest | no change needed | derived from the committed workflows (ci_workflow_plan, ci_local_manifest, ci_manifest); their selftests pass in d47 |
| scope history, tool-cache isolation control | yes | ci_scope_history.py now 45 elaborate cases (9 x 5 workers); ci_toolcache_isolation.py reads every elaborate-gates-N (not run: needs network installs of five legs; its plan computation checked for all five) |

## Gate table (all at head aa3e2d85; logs and rc in receipts/)

| Gate | rc | s |
|---|---:|---:|
| g01 python3 scripts/ci_gate_workflows.py --check | 0 | 0 |
| g02 python3 scripts/ci_events.py --check | 0 | 1 |
| g03 python3 scripts/ci_events.py --selftest (5579 arms; log 360 KB, sha in .ref) | 0 | 263 |
| g04 scripts/run_litex_sims.sh --selftest (16 checks) | 0 | 2 |
| g05 leg 0: python3 scripts/ci_litex_legs.py run 0 --receipt ... -- scripts/run_litex_sims.sh <logdir> | 0 | 566 |
| g06 leg 1 | 0 | 589 |
| g07 leg 2 | 0 | 578 |
| g08 ci_litex_legs.py union over the three real receipts: "litex: 8 simulations exactly once, each a pass" | 0 | 0 |
| g09a control: test_pp_boot_bus_freeze dropped from leg 1's receipt: "LiteX leg 1 did not run its selection exactly once: test_pp_boot_bus_freeze" | 1 (expected) | 0 |
| g09b control: leg 1 receipt lost: "LiteX simulations ran in no leg: test_gmii_rx_capture, test_gptp_tx_timestamp, test_pp_boot_bus_freeze, test_pp_mem_bridge" | 1 (expected) | 0 |
| g09c restored: union passes | 0 | 0 |
| g10a ci_gate_receipts.py verify (the "Require every gate exactly once" step) with real LiteX receipts, recorded step receipts, stand-in builder receipts | 0 | 1 |
| g10b same, simulation dropped: "gate evidence refused: LiteX leg 1 did not run its selection exactly once: test_pp_boot_bus_freeze" | 1 (expected) | 1 |
| g10c same, restored | 0 | 1 |
| g11 cd tests && behave --no-capture -f plain (508 scenarios; log in .ref) | 0 | 3 |
| g12 git diff --check e61a4afa HEAD | 0 | 0 |
| g13 python3 scripts/ci_gate_workflows_selftest.py | 0 | 14 |
| g14 python3 scripts/ci_litex_legs_selftest.py | 0 | 0 |
| g15/g15b check_py_idiom.py and --selftest | 0/0 | 5/5 |
| g16/g16b check_sh_idiom.py and --selftest | 0/0 | 0/0 |
| g17 python3 scripts/ci_scope.py --selftest (scope history, 45 elaborate cases) | 0 | 28 |
| g18 ci_tool_inventory.py --check (pre-existing refusal, same at base) | 2 | 0 |
| d01-d50 docs workflow run steps (docs-check, wire-accountability, docs-check-no-git) | all 0 | see receipts |

Docs workflow steps not run as written: the package installs (replaced by a scratch venv with the same pinned
requirements), the submodule fetches (already initialised), sv2v install (on PATH), "End-station builder
gates" (reads none of the changed files, only a comment names elaborate.yml; its legs run over 1000 s), and
d38 CI event gate (same commands as g02/g03 at the same head). d20 installed the pinned SDK into scratch,
since the host SDK lacks the provenance receipt the verifier requires. d21 ran 644 s and finished after the
harness moved it to background at the 600 s mark; it exited 0.

## Open risks / questions

- The derived figures are hosted measurements plus allowances, not a hosted run of this head. The first
  hosted run will be the Verilator-cold case; the derived cold LiteX worker is 1040 s.
- Worker 0's projection (1475 s, measured hosted max 1227) is unchanged by this lane and now binds the
  workflow: 55 s inside 30 min on the projection.
- SECONDS needs a hosted re-measure when a simulation changes cost; LEG_BUDGET refuses a leg above 1200 s.
