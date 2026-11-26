Relates to #1008.

## Summary

Holds the fast workflow's slow jobs, and the docs gates, to #998's budget of 1276 s hosted, which is 30 minutes on a
runner 1.41 times as slow. The jobs run as fail-fast matrix legs, or on more workers. Every verdict, receipt,
required context, the cancellation contract and fork safety stay as they were. No job's limit is raised. It also
re-keys `gptp_shadow` as #1008's comments ask. Some jobs are still over the budget (see "Not in this PR"), so this
PR relates to #1008 and does not close it.

## Measured: this PR's own hosted run

These are the run's measured windows, not projections. Run 45783522388 (rtl-fast), at 5b5b0765, is the first run
after the workflow change, so every cache keyed on the workflow files missed.

| Job | Slowest of the 20 earlier runs, s | Legs in run 45783522388, s | Slowest leg x 1.41 |
|---|---:|---|---:|
| `firmware-control-mutants` | 2441 | 573, 712, 517, 502 | 1004 |
| `firmware-aecp-mutants` | 1598 | 610, 629 | 887 |
| `firmware-srp-mutants` | 1828 | 751, 980 | 1382 |
| `firmware-unit` | 1880 | 973, 209, 587 | 1372 |
| `publication-census` | 2657 | legs 298, 368, 375, 379, 336; judge 36 | 534 |
| `docs-gates-0` | 1717 | 456 (run 45783522301) | 643 |
| `docs-gates-2` | 1389 | 658 | 928 |
| `docs-gates-3` (new) | | 671 | 946 |
| `docs-gates-4` (new) | | 554 | 781 |

- Every divided leg is within 1276 s. #1008's acceptance 1 asks for two runs, so this is one of the two.
- In the same run, the untouched jobs were all within 1276 s too:
  - `firmware-verilator` 1147 s and `firmware-boundary-capture (0)` 1017 s;
  - in elaborate, `elaborate-gates-1` 1258 s;
  - in rtl-full, `Prepare pinned Yosys` 1163 s, a cold build after the workflow change;
  - every rtl-full Verilator shard that finished, at most 987 s. The others were cancelled; see below.

**The run failed.** `firmware-boundary`, the boundary judge, refused this PR's new
`scripts/ci_fast_legs_selftest.py`. That program names the firmware's tree, and it was not listed in
`ctrl_configs.OUTSIDE` among the programs that compile none of the firmware. The head's fail-fast watcher then
cancelled the rest of rtl-fast and rtl-full: rtl-full's unions failed on their cancelled shards. The fix lists the
self-test in `OUTSIDE`; it compiles nothing, since every campaign it drives is stood in for. The judge's text scan
(`ctrl_configs.held`) now passes at the head.

## Projected from the 20 earlier runs (unchanged method)

| Job | Now | Slowest leg, projected s | x 1.41 |
|---|---|---:|---:|
| `firmware-control-mutants` | 4 legs | 739 | 1042 |
| `firmware-aecp-mutants` | 2 legs | 892 | 1257 |
| `firmware-srp-mutants` | 2 legs | 1017 | 1434 |
| `firmware-unit` | 3 legs | 1027 | 1448 |
| `publication-census` | 5 legs + judge | 498 | 703 |
| `docs-gates-0` / `-2` / `-3` / `-4` | 2 steps moved to 2 new workers | 738 / 981 / 1237 / 879 | 1744 at most |

How a projection is made:
- A mutation leg gets its share of the undivided step's slowest hosted window. The share is the leg's share of
  the campaign as measured when the legs ran side by side. The job's slowest time outside that step is added.
- `firmware-unit`'s legs add each step's slowest window to the job's slowest time outside its steps.
- The docs rows use the policy page's component-maxima rule: the sum of each step's slowest window, setup included.

## What changed

**Campaign legs** (`--campaign-shard INDEX COUNT`, `sw/firmware/ctrl/test/test_ctrl_firmware.py`)
- The option divides the control, AECP or SRP phase of `--shard`.
- Each live table is dealt in order, so every defect goes to exactly one leg.
- Every leg runs its phase's controls: the unnamed-test check in the control phase, and the two lwSRP pin controls
  in the SRP phase. SRP deals each of its three tables: two interfaces, one interface, and 8x8 with one interface.
- Before planting anything, each leg proves through the real driver that the legs together plant each live defect
  of the phase once, and that a dropped or duplicated leg is refused (`campaign_cases`).
  - The proof derives each leg through the driver's own mapping of a leg onto its phase's partition
    (`campaign_leg`), so dropping that mapping is refused too.
  - A narrowing combination is refused, as `--shard` refuses one.

**Census legs** (`sw/mailbox/census_legs.py`)
- Leg 0 runs the census check over every shape.
- Legs 1-4 run the self-test's arms, each netlist rider beside its host. The order is the serial self-test's
  inventory (`census_selftest.jobs_for`, factored out unchanged).
- Each leg uploads a receipt with its source identity, inventory, selection and verdicts.
- `publication-census` then judges the union, using no tool:
  - every arm exactly once, each one passing;
  - the same head, tree and inventory in every receipt;
  - each rule's removal, judged by the unchanged `mutations()`.

**Generator** (`scripts/ci_fast_legs.py`, applied by `scripts/ci_gate_workflows.py`)
- The templates keep each complete command; the generator emits the matrices.
- Each matrix keeps GitHub's own `fail-fast: true`.
- The census legs restore the Yosys tree that `yosys-tool` built, with `fail-on-cache-miss`. The generator refuses a
  census recipe that is not `yosys-elaboration`'s. On a cache miss Yosys is now built once, not in the job: in 6 of
  the 20 runs that build took 732-838 s of the census window.
- The aggregate `rtl-fast` also requires `publication-census-legs`, because a failed leg skips the judge.

**Docs** (`DOCS_WORKERS`): two workers are added.
- `docs-gates-3` runs the compiler-absent firmware controls and both contract gates.
- `docs-gates-4` runs the saved-state writer.
- Each step runs whole, with its receipt.

**Contract** (`scripts/ci_events.py`, `check_fast_legs`, applied to the generated `rtl-fast.yml`)
- Each matrix is held exactly, `fail-fast: true` included.
- Each campaign job runs its phase once, as `--campaign-shard "${{ matrix.leg }}" COUNT`, where COUNT is its own
  matrix's leg count. Every other job runs no campaign leg.
  - A COUNT above the matrix's would leave a share of the phase in no leg while every leg passed. The generator's
    self-test holds the same.
- The judge must need its legs, the legs keep 30 minutes, and the aggregate must read each legs job.
- The event self-test plants 35 defects in the generated graph, each refused by name.

**`gptp_shadow`** (`scripts/suite_shards.py`)
- Re-keyed to 679 s for the merged gPTP pin 3ce71b76 and its suite. That is the larger of:
  - 679 s on worker 22/27 of run 45755846909, at d3cb3cf1, whose content is this merge's dev-soft-core;
  - 672 s on run 45735453538, at the same pin, before that suite's last two changes.
- Before the merge it was 517 s, from runs 45657606190 and 45751066654 at pin 1213ac5b.
- Every regular worker still projects at most 1276 s. The heaviest are workers 0 and 25, at 1275 s. The policy
  page's table is updated.
- One complete hosted run has the merged content exactly. The second run #1008 asks for is the next one.

**Base:** dev-soft-core 4df125b8 (PR #1016) is merged in. The workflows regenerate unchanged.

## Verdict identity

The reference is the serial hosted run 45657606423 at 09201d35. Its `sw/`, `hdl/`, `configs/` and every
submodule are byte-equal to the pre-merge base. Every leg was run at a committed head.

- **Control:** 4 legs, 211 mutants each. The legs' 844 verdict lines, each with its first failing check, are the
  serial run's 844 as a multiset. Each leg prints "211 of 211 caught" and PASS.
- **AECP:** 2 legs, 199 defects each. The legs' 398 verdicts are the serial run's 398. Both legs pass.
- **SRP:** 2 legs, 332 and 330 defects. The legs' 662 defect verdicts are the serial run's 662. Each leg runs the
  two lwSRP pin controls, and its lines equal the serial run's. Both legs pass.
- **Census:**
  - Leg 0 prints the serial check's 22 lines; only the duration differs.
  - The judge prints the serial self-test's 222 arm and rule lines in the same order. One line differs only by a
    heap address inside a Yosys cell name.
  - The summary still reads "0 of 164 arm(s) failed" and "0 of 57 rule(s) no arm proves".
- **The census receipts are retained** with their SHA-256 values, at their execution head 530149b5 (tree
  08e15b7d). These are the five original receipts the judge read.
  - A replay at that head, with the published command, passes. Its output is identical to the original judge's.
  - The same replay refuses each of the seven planted faults.
- **`firmware-unit`:** each step's command is byte for byte the template's, on exactly one leg. The generator
  self-test holds this.
- **After the merge.** dev-soft-core 4df125b8 adds three control defects (`ctrl_mutants.py`), 844 to 847. Each
  leg's dispatch proof covers the table it runs, and at the head it deals the 847 as 212, 212, 212 and 211, each
  once. The AECP (398) and SRP (662) tables are unchanged. The serial comparisons above are at the pre-merge base.

## Planted failures: a divided job still fails the run

- **Required-context shell.** The generated `rtl-fast` shell runs with each divided job's result set to `failure`,
  then to `cancelled`. It exits nonzero for every one of the five jobs. A failed census leg is tested with the
  judge skipped, as GitHub would skip it.
- **Census judge on the original receipts.** Seven failures are planted into copies, and the judge refuses each:
  - an arm that failed;
  - a leg that exited 1;
  - a rule removal that is still refused;
  - a lost arm;
  - a missing leg;
  - a duplicated leg;
  - another head.
- **Campaign legs.**
  - A failed campaign in each leg of each phase fails that leg.
  - A dropped or duplicated leg is refused by the dispatch proof, and so is a leg that would plant the whole table.
- **Campaign count.** A generator that emits one more leg in the command than its matrix holds is refused by the
  contract for all three campaign jobs, and by the generator's self-test.
- **Contract.** For each matrix, the event self-test plants:
  - a dropped leg;
  - `fail-fast: false`;
  - the key left to its default;
  - the aggregate not reading the legs;
  - the command's count one more and one fewer, leg 0 everywhere, and the phase run twice;
  - a campaign leg in an undivided job;
  - a judge that does not need its legs;
  - a raised legs limit.

  Each is refused.
- **Cancellation and forks.**
  - `strategy.fail-fast` is applied by the Actions service. A failed leg cancels its siblings on every event, a
    fork's included, and no step or token is involved.
  - The watcher's same-repository condition is unchanged. No new job carries `permissions`.

## Gates

Every gate the change touches passes in a clean clone at the head. That is 40 commands, the boundary judge's text
scan among them. The event self-test passes 2409 contract items and 6174 arms.

## Runner-minutes

Means over the 20 measured runs of each workflow, with every hosted job counted, the watchers included:

- **rtl-fast: 263.9 before, about 269.2 after.**
  - Each added leg repeats its job's setup: 47-54 s on average.
  - The census judge costs about 60 s; it measured 36 s in run 45783522388.
  - Against that, the census no longer builds Yosys: 225 s per run on average.
- **docs: 91.2 before, about 94.5 after.** Two more workers, each repeating the setup: 98 s on average.

## Not in this PR (#1008 stays open)

- **The cache-miss jobs.**
  - Over the 20 earlier runs:
    - `firmware-verilator`: 1630 s, of which the Verilator build is 415 s;
    - `elaborate-gates-4`: 1422 s, of which the Verilator build is 415 s;
    - rtl-full's Verilator shards: up to 1702 s in the runs where 7 and 8 workers built Verilator. Without a build
      they reached at most 1253 s.
  - The Verilator cache key binds every workflow file, so any workflow change rebuilds Verilator in every job that
    uses it. A Verilator tool job like `yosys-tool` would fix all three.
- **`elaborate-gates-0` (1343 s) and `elaborate-gates-1` (1453 s).**
  - `elaborate-gates-0` runs the builder's leg 0, a single gate, `test_baremetal_profile_contract`, up to 1157 s.
    It has to be made faster; it cannot be re-dealt.
  - `elaborate-gates-1` runs leg 1, up to 1300 s.
- **rtl-full `Yosys shard 0/4` (1451 s).** One portability item dominates its 1412 s step.
- **`docs-gates-1`, the builder's leg 0, untouched.** Its slowest measured window is 1111 s, and 717 s in this
  run, but by the component-maxima rule it projects at 1302 s, over the budget. It is the same single gate as
  above.
