Relates to #1008.

## Summary

Holds the fast workflow's slow jobs, and the docs gates, to #998's budget of 1276 s hosted, which is 30 minutes on a
runner 1.41 times as slow. The jobs run as fail-fast matrix legs, or on more workers. Every verdict, receipt,
required context, the cancellation contract and fork safety stay as they were. No job's limit is raised. It also
re-keys `gptp_shadow` as #1008's comments ask. Some jobs are still over the budget (see "Not in this PR"), so this
PR relates to #1008 and does not close it.

| Job | Slowest of 20 hosted runs, s | Now | Slowest leg, projected s | x 1.41 |
|---|---:|---|---:|---:|
| `firmware-control-mutants` | 2441 | 4 legs | 739 | 1042 |
| `firmware-aecp-mutants` | 1598 | 2 legs | 892 | 1257 |
| `firmware-srp-mutants` | 1828 | 2 legs | 1017 | 1434 |
| `firmware-unit` | 1880 | 3 legs | 1027 | 1448 |
| `publication-census` | 2657 | 5 legs + judge | 498 | 703 |
| `docs-gates-0` | 1717 | 2 steps moved to new workers | 738 | 1041 |
| `docs-gates-2` | 1389 | contract gates moved | 981 | 1383 |
| `docs-gates-3` (new) | | firmware controls and contract gates | 1237 | 1744 |
| `docs-gates-4` (new) | | saved-state writer | 879 | 1239 |

How a projection is made:
- A mutation leg gets its share of the undivided step's slowest hosted window. The share is the leg's share of
  the campaign as measured when the legs ran side by side. The job's slowest time outside that step is added.
- `firmware-unit`'s legs add each step's slowest window to the job's slowest time outside its steps.
- The docs rows use the policy page's component-maxima rule: the sum of each step's slowest window.

## What changed

**Campaign legs** (`--campaign-shard INDEX COUNT`, `sw/firmware/ctrl/test/test_ctrl_firmware.py`)
- The option divides the control, AECP or SRP phase of `--shard`.
- Each live table is dealt in order, so every defect goes to exactly one leg.
- Every leg runs its phase's controls. In the SRP phase these are the unnamed-test check and the lwSRP pin
  controls. SRP deals each of its three tables: two interfaces, one interface, and 8x8 with one interface.
- Before planting anything, each leg proves through the real driver that the legs together plant each live defect
  of the phase once, and that a dropped or duplicated leg is refused (`campaign_cases`). A narrowing combination
  is refused, as `--shard` refuses one.

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

**Contract** (`scripts/ci_events.py`, `check_fast_legs`, in the generated `rtl-fast.yml`)
- Each matrix is held exactly, `fail-fast: true` included.
- The judge must need its legs, and the legs keep 30 minutes.
- The aggregate must read each legs job.
- 22 new arms plant each defect.

**`gptp_shadow`** (`scripts/suite_shards.py`)
- Re-keyed to 517 s: the larger of 478 s and 517 s. These are worker 22/27 of runs 45657606190 and 45751066654,
  the first two complete hosted runs after #1003 at the base's gptp-processor pin (1213ac5b).
- Every regular worker still projects at most 1276 s. The heaviest is worker 0 at 1275 s.
- The policy page's table is updated.

## Verdict identity

The reference is the serial hosted run 45657606423 at 09201d35. Its `sw/`, `hdl/`, `configs/` and every
submodule are byte-equal to the base's. Every leg was run at a committed head.

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
- **`firmware-unit`:** each step's command is byte for byte the template's, on exactly one leg. The generator
  self-test holds this.

## Planted failures: a divided job still fails the run

- **Required-context shell.** The generated `rtl-fast` shell runs with each divided job's result set to `failure`,
  then to `cancelled`. It exits nonzero for every one of the five jobs. A failed census leg is tested with the
  judge skipped, as GitHub would skip it.
- **Census judge on real receipts.** Seven failures are planted into copies of the real receipts, and the judge
  refuses each:
  - an arm that failed;
  - a leg that exited 1;
  - a rule removal that is still refused;
  - a lost arm;
  - a missing leg;
  - a duplicated leg;
  - another head.
- **Campaign legs.** A failed campaign in each leg of each phase fails that leg. A dropped or duplicated leg is
  refused by the dispatch proof.
- **Contract.** For each matrix, the event self-test plants a dropped leg, `fail-fast: false`, the key left to its
  default, and the aggregate not reading it. It also plants a judge that does not need its legs and a raised legs
  limit. Each is refused.

**Cancellation and forks.**
- `strategy.fail-fast` is applied by the Actions service. A failed leg cancels its siblings on every event, a
  fork's included, and no step or token is involved.
- The watcher's same-repository condition is unchanged. No new job carries `permissions`.

## Gates

Every gate the change touches passes in a clean clone at the head (39 commands). The event self-test passes 2390
contract items and 6161 arms. The generator, leg, dispatch, suite-shard, code-quality and documentation gates
pass too.

## Runner-minutes

Means over the 20 measured runs of each workflow, with every hosted job counted, the watchers included:

- **rtl-fast: 263.9 before, about 269.2 after.**
  - Each added leg repeats its job's setup: 47-54 s on average.
  - The census judge costs about 60 s.
  - Against that, the census no longer builds Yosys: 225 s per run on average.
- **docs: 91.2 before, about 94.5 after.** Two more workers, each repeating the setup: 98 s on average.

## Not in this PR (#1008 stays open)

Each of these jobs was slowest in the measured runs where a tool was built inside its own timed window, or where
one item dominates it:

- **The cache-miss jobs.**
  - `firmware-verilator`: 1630 s, of which the Verilator build is 415 s.
  - `elaborate-gates-4`: 1422 s, of which the Verilator build is 415 s.
  - rtl-full's Verilator shards: up to 1702 s in the two runs where 7 and 8 workers built Verilator, and one
    worker also built Yosys. Without a build they reached at most 1253 s.
  - The Verilator cache key binds every workflow file, so any workflow change rebuilds Verilator in every job that
    uses it. A Verilator tool job like `yosys-tool` would fix all three.
- **`elaborate-gates-0` (1343 s) and `elaborate-gates-1` (1453 s).** Builder leg 0 is a single gate,
  `test_baremetal_profile_contract`, which runs up to 1157 s. It has to be made faster; it cannot be re-dealt.
- **rtl-full `Yosys shard 0/4` (1451 s).** One portability item dominates its 1412 s step.
- **`docs-gates-1`, the builder's leg 0, untouched.** Its slowest measured window is 1111 s, but by the
  component-maxima rule it projects at 1302 s. It is the same single gate as above.
