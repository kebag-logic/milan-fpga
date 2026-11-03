# HANDOFF — [A727b] issue #737 round 2, PR #836: STOPPED at item 3

Lane: $LANES/737-elab-split, branch 737-elab-split. Round 1 head aa3e2d85, base dev e61a4afa. Nothing pushed.
Head: 6a38c330a974b777b7d104d6c7c4747cdc1c84b2 (2 commits over aa3e2d85).
Scratch: $VALIDATION_STORAGE/737-a727b. CPUs: 48-63 (unit milan-737-a727b.service). Receipts: receipts/ beside this file.
Authority: the manager's round 2 ruling, issuecomment-6596926489. Reviews: R767-1 (issuecomment-6596919569) and R768-1 (issuecomment-6596681509).

## Status

- [x] TAKEN posted: issuecomment-6597066355
- [x] item 1, bounds from standalone measurements (R767-1-F1, R768-1-F1): commit e80b44b5
- [x] item 2, worker 1 and builder-leg figures (R768-1-F2): commit 6a38c330
- [ ] item 3, CPU-netlist cache race (R768-1-F3): **STOP**, needs a decision (below)
- [ ] item 4, wall clock (R767-1-F2): not started; it comes after item 3 in the ruling's order
- [ ] item 5, R767-1-R1 text and the suggestions: not started
- [x] fast gates at 6a38c330 (table below). The real leg runs and the dropped-simulation control were NOT run.
- [x] STOP posted on #737: see the last line of this file

## Why STOP (item 3)

The ruling says the LiteX workers restore the vexii, sbt, pip and sv2v keys and never save them, "for example with
`actions/cache/restore`", through the template and the generator only. I found no way to do both.

- **`actions/cache/restore@v4` is refused by the local act runner's trust set.** `scripts/act_ci.py:200`
  `TRUSTED_ACTION_USES` holds exactly five references: cache@v4, checkout@v4, download-artifact@v4, setup-python@v5
  and upload-artifact@v4. `validate_workflow_sandbox` (`scripts/act_ci.py:2084`) refuses any other reference. I tested
  this in a detached scratch worktree of aa3e2d85 (since removed). There the generator emitted `actions/cache/restore@v4`
  for the four caches on workers 2 to 4 (12 steps), and `act_ci.validate_workflow_sandbox(root, ["elaborate"])` gave:
  `Refusal workflow .github/workflows/elaborate.yml job elaborate-gates-2 step 5 uses unapproved action
  'actions/cache/restore@v4'; local, docker://, and unaudited remote actions can execute through the host Docker daemon`.
  The real head is accepted. `ci_events.py --check` passed on the probe, rc 0.
  Also affected: `scripts/ci_events.py:605` `RECORDED_ACTIONS` (checked at `:3232`) and the allowed prefixes in
  `scripts/ci_tool_inventory.py:280`. Both name only `actions/cache@`. The inventory check is already masked by
  unrelated drift.
- **`actions/cache@v4` cannot restore without saving.** It has no input that turns the save off, and it saves on
  every miss whose key was not an exact hit. Run 41583428850 shows the race:
  - worker 2 saved vexii as 202 bytes (empty), and also sbt 57 MB, pip 6 MB, sv2v 2 MB and Verilator 92 MB;
  - workers 0, 1 and 4 got "Unable to reserve cache" for the same keys;
  - worker 3 started 1268 s late and restored all of them, the empty vexii entry included
    (receipts/hosted/run-41583428850-cache-lines.txt).
- Options for the decision:
  - **(A)** Admit `actions/cache/restore@v4` (same repository and tag as the trusted `actions/cache@v4`) to
    `TRUSTED_ACTION_USES`, `RECORDED_ACTIONS` and the inventory's allowed prefixes. Then the generator emits it on
    workers 2 to 4. This touches `scripts/act_ci.py` (whose content pin is already stale), `scripts/ci_events.py` and
    `scripts/ci_tool_inventory.py`. It is outside "template and generator only", and it widens the act trust boundary.
  - **(B)** Through the generator only, workers 2 to 4 carry none of the four cache steps: no restore and no save.
    The builders alone then save those keys. Every LiteX run is then the measured cold case for those caches, which
    item 1's bounds already assume. The cost is warm-run time on every run: `test_ctrl_memory` measured 280 s alone
    with its metadata cold, against 100 to 113 s inside the old aggregate. This departs from the ruling's "restore".
- I rejected the hacks within `actions/cache@v4`: a per-worker key with restore-keys (the template forbids
  restore-keys on vexii, and a stale or empty entry gets pinned), and deleting the cached paths before the post-save
  (it relies on the action's missing-path warning).

## Findings and changes (file:line at 6a38c330)

| Finding | Item | Change |
|---|---|---|
| R767-1-F1, R768-1-F1 | 1 | `scripts/ci_litex_legs.py:29-46` `SECONDS` now holds each member's own `verdicts.tsv` seconds from the three leg receipts of run 41583428850 (receipts/hosted/run-41583428850-litex-leg-{0,1,2}.json). `:48-54` `LEG_BUDGET` is 973 = 1800 - 270 (aggregate/collector/watcher/tail) - 143 (setup) - 411 (cold Verilator) - 3 (self-test); runner queueing is excluded. The old value was 1200 with a 112 s setup and a 300 s cold allowance. `docs/testing/CI_WORKFLOWS.md:1669-1685` gives member seconds, budget and leg loads. `:3102-3118` defines the one setup figure and the cold projection, reconciled with the measured spans. `:3138-3140` has the table rows. `ci/image/command-table.json:13611-13614` re-pins `ci_litex_legs.py` (sha256 f137d754...). |
| R768-1-F2 | 2 | `docs/testing/CI_WORKFLOWS.md:3092-3100`: 41476923392 attempts 1 to 3 are named (step 1495/1511/1506, job 2735/2734/2740); builder leg 1 is 869 to 1119 s; worker 1 is `2735 - 1495` = 1240 (attempt 1); its exact-head 1183 is stated. `:3137` worker 1 row 1240 / 380. `:3178-3180` worker 0's measured maximum is 1254 s cold (run 41583428850). It was 1227. |
| R768-1-F3 | 3 | not changed: STOP (above) |
| R767-1-F2 | 4 | not changed (after item 3) |
| R767-1-R1, S1; R768-1-S1..S3 | 5 | not changed. Plan, not yet applied: R1's exact text at `CI_WORKFLOWS.md:1681`. R768-1-S2 is a defence-in-depth comment at `ci_litex_legs.py` `union()`'s `repeated` branch. R767-1-S1 is an assertion that LiteX workers are disjoint from builder workers (the #737 failure shape). R768-1-S3's boolean exit check fits the `ci_litex_legs.py` pin already being refreshed. Decline the `run_litex_sims.sh` arms (R767-1-S1 `--only` with three or more members and a FAIL row; R768-1-S3 trailing comma), because they need a new pin for that script and the runtime union already refuses each by name. Decline R768-1-S1 (a sandbox arm through `run()`) for the same runtime-union reason. |

## Per-leg timing (measured and derived)

Setup = a worker's job span less its gate steps and its Verilator source build, from the jobs API (receipts/hosted/cited-runs-timing.txt, timing.py).
The largest value over every elaborate worker of runs 41470524727, 41526004847, 41554508699, 41476923392 a1-a3 and 41583428850 is **143 s** (worker 1, 41526004847).
The cold setups at the exact head were 94 (w2), 131 (w4), 124 (w0) and 108 (w1); worker 3's warm setup was 114.
Cold Verilator builds were 249 (w2) and **411** (w4). The leg step less the sum of its members was 2/2/3 s, so the self-test allowance is **3 s**.

Re-derived partition (`python3 scripts/ci_litex_legs.py legs`, receipts/g05-litex-legs.log):

| Leg | Worker | Members (SECONDS) | Leg s | Derived warm s (143+3+leg) | Derived cold s (+411) | Margin to 1620 / 1800 (cold) |
|---|---|---|---:|---:|---:|---:|
| 0/3 | elaborate-gates-2 | gptp_tx_timestamp 461 | 461 | 607 | 1018 | 602 / 782 |
| 1/3 | elaborate-gates-3 | cpu_memory_port_cdc 70, gmii_rx_capture 0, pp_boot_bus_freeze 25, pp_mem_bridge 14, retained_cdc_storage 331 | 440 | 586 | 997 | 623 / 803 |
| 2/3 | elaborate-gates-4 | ctrl_memory 280, soc_timing_cuts 240 | 520 | 666 | 1077 | 543 / 723 |

Reconciliation with run 41583428850's old legs, by the same method:

| Old leg | Leg s (members) | Derived cold | Measured span | Note |
|---|---:|---:|---:|---|
| 0 (w2) | 240 | 797 | 585 | every workflow-keyed cache missed |
| 1 (w3) | 500 | 1057 (warm 646) | 616 | restored worker 2's saves |
| 2 (w4) | 681 | 1238 | 1226 | every workflow-keyed cache missed; Verilator 411 |

Other workers (measured spans from the jobs API):

| Job | Runs | Figure |
|---|---|---|
| elaborate-gates-0 | 1015, 1227, 992, 833 (a1, reused in a2/a3), 1254 (exact head, cold) | projection 1475 unchanged; measured max 1254 |
| elaborate-gates-1 less LiteX step | 992, 1072, 1187, 1240 (a1), 1223 (a2), 1234 (a3); exact head 1183 | 1240 |
| builder leg 1 | 869, 929, 1075, 1108, 1096, 1119, exact head 1075 | 869 to 1119 |

Exact-head spans for item 4 (not yet applied), measured from the first job start: gates-3 ends at 1883, `elaborate` at 2307 and
`Collect CI manifest` at 2825. The ruling's 1882 / 2306 / 2824 differ by 1 s of rounding. gates-3 was queued 1268 s and `elaborate` 388 s
(receipts/hosted/run-41583428850-spans-from-run-start.txt).

Caveat: `SECONDS` comes from one hosted run. In-aggregate figures for `test_soc_timing_cuts` ranged from 355 to 534 s, against 240 alone,
so a re-measure over later exact-head runs may raise a leg.

## Records touched

| Record | Touched | How / why not |
|---|---|---|
| ci/image/command-table.json | yes | `ci_litex_legs.py` re-pinned to its new content (CI_IMAGE.md "Review script changes before updating their content hashes") |
| .github/workflows/elaborate.yml | no | membership is computed at run time from `ci_litex_legs.py`; `--check` rc 0 |
| scripts/ci_events.py | no | `--check` rc 0, `--selftest` rc 0 (5579 arms) |
| docs/testing/TESTING.md | no | names no figures |

## Gate table (at 6a38c330; logs and rc in receipts/)

| Gate | rc | s |
|---|---:|---:|
| g01 python3 scripts/ci_gate_workflows.py --check | 0 | 0 |
| g02 python3 scripts/ci_events.py --check | 0 | 1 |
| g03 python3 scripts/ci_events.py --selftest (2199 items, 5579 arms; log 360 KB, sha in .ref) | 0 | 255 |
| g04 scripts/run_litex_sims.sh --selftest | 0 | 2 |
| g05 python3 scripts/ci_litex_legs.py legs (461 / 440 / 520) | 0 | 1 |
| g11 cd tests && behave --no-capture -f plain (508 scenarios; log in .ref) | 0 | 4 |
| g12 git diff --check e61a4afa HEAD | 0 | 0 |
| g13 python3 scripts/ci_gate_workflows_selftest.py | 0 | 20 |
| g14 python3 scripts/ci_litex_legs_selftest.py | 0 | 0 |
| g15 python3 scripts/check_py_idiom.py | 0 | 6 |
| d05 d06 d07 d33 d36 d40 d42 d47 d50: docs workflow run steps that read the changed docs and scripts | all 0 | see receipts |
| each re-derived leg's own command run locally | NOT RUN | STOP before REVIEW READY |
| dropped-simulation control on real leg receipts | NOT RUN | needs the real leg receipts |

The Python used was a scratch copy of round 1's pinned docs venv (CPython 3.14, PyYAML 6.0.3, behave). docs.yml is unchanged since e61a4afa,
so round 1's extracted step bodies were reused.

## Next author

Once the manager decides item 3, do item 3, then 4, then 5. Then run the three leg commands locally on the re-derived partition, the
dropped-simulation control, the full gates and the docs steps, and post REVIEW READY.

STOP posted: issuecomment-6597376686 (head 6a38c330a974b777b7d104d6c7c4747cdc1c84b2); text in receipts/stop.md
