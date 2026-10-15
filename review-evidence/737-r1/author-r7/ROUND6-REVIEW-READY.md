[A614] REVIEW READY

Commit: `47fd0d3c510000e9412a1613a723b61d4ef2ae4a`
Branch: `737-ci-30min`, from round-five head `e3d25d96`. The worktree is clean. Not pushed: origin holds `e3d25d96`, and the coordinating role publishes this head.

Round 6 ([6187562969](https://github.com/kebag-logic/milan-fpga/issues/737#issuecomment-6187562969)) is complete. Delta for review: `e3d25d96..47fd0d3c`, five commits.

**1. Docs builder in measured legs (R636-5-F1 = R637-5-F1)** (`b06211642` code, `47fd0d3c5` page).
- The generator divides the docs `End-station builder gates` step the way it divides elaboration's. Leg 0 (`test_baremetal_profile_contract`) runs on `docs-gates-1`. Leg 1 (the other 102 gates) runs on `docs-gates-2`, beside the contract self-tests. The step's `pip install` line stays ahead of the leg runner, and the template is unchanged.
- The three docs workers stay, so the runner and the manifest plan keep their shape.
- The union judges only the flags the template command carries: docs `--require-rv32` alone, elaboration both. Every leg must carry exactly its command's flags. The driver's elaboration verdict applies to the union only under `--require-elaboration`.
- `ci_builder_legs.py union` now takes `--workflow`.
- Equality at `26838a11`, in the shipping image at 16 CPUs:
  - The unsharded docs command took 1443.7 s alone. `test_baremetal_profile_contract` took 1006 s and the other gates 435 s, so the existing partition fits.
  - Leg 0 took 1098.1 s and leg 1 took 506.3 s, measured beside each other. Both pass.
  - `union --workflow docs --reference` is equal to the unsharded run: per-gate verdicts and the NOT RUN ledger match (digest `47dc3c6a`). The production docs aggregate accepts the real receipts, 43 source gates exactly once.
- Planted controls:
  - The boot-claim defect fails the unsharded run and leg 0; leg 1 passes.
  - The FPU-refusal defect fails the unsharded run and leg 1; leg 0 passes.
  - Leg 0 run without `--require-rv32` is refused by the production aggregate by name.
  - A 6/6 mutation battery fails the committed self-test.
- Projections, from the hosted `f6260253` windows (runs 38601263556 and 38601263659), the round-5 measurements and this round's docs legs. The larger figure is used where they differ, and each figure is rounded up.

  | Worker | Projected |
  |---|---:|
  | `docs-gates-0` | 1395 s |
  | `docs-gates-1` | 1248 s |
  | `docs-gates-2` | 1073 s |
  | `elaborate-gates-0` | 1475 s |
  | `elaborate-gates-1` | 1353 s |

  Every worker is within its 1620 s bound, at most 54.6% of its limit. The docs workflow projects at 1665 s, 135 s inside 30 minutes. Elaboration projects at 1745 s, 55 s inside, so it is not divided further.
- The arm count was 5,212 at `e3d25d96`. Leg 1's step adds three generated-graph arms, so it is 5,215 now.

**2. Generator self-check (R637-5-F2)** (`26838a11c`).
- `ci_gate_workflows_selftest.py` requires the generated sixteen-worker matrix, no `= milan_dp ;;` arm in the generated ownership step, and exactly `--expect 16`.
- Three planted templates must each stop generation: an arm index, an `--expect` value and a total that disagree with the template's own count.
- Reverting `ci_suite_workflows.py` to `08adb21a` and regenerating still passes the freshness and contract checks, but the committed self-test fails.

**3. Test pages (R636-5-F2)** (`e958bdde8`).
- `TESTING.md` now describes the sixteen `--ci-pieces` workers: `milan_dp` in four legs, `milan_dp_mclk__0` alone on the last worker, and the six-worker template as generator input only. Its example is `scripts/run_all_suites.sh --ci-pieces --shard 0/16 --list`.
- The `milan_dp` README and `RUNNING_TESTS.md` now match.
- Two adjacent lines also changed, disclosed: the stale "60 suites" count (the driver lists 63), and `726_STREAM_COUNTERS.md`'s "shard 4/5". The second was needed for the `/5` and `/6` search to come back clean.

**4. Residue** (`3c5fc8361`). R636-5-R1 and R637-5-R2 use the exact texts given. R637-5-R1 is fixed in the PR body's round-5 status.

**Verification at this head.** Fresh clones in the shipping image, 8 GiB, no network, each generated worker's gate steps run exactly as written. All pass, with no memory events.
- `docs-gates-0`: 38 of 38 steps.
- `docs-gates-1`: builder leg 0.
- `docs-gates-2`: builder leg 1, and the CI-event contract at 2,187 items and 5,215 arms.
- The unsharded docs reference, with the docs aggregate replay and the equality check.
- The elaboration builder legs, plus the elaborate aggregate replay. They ran because the changed union code runs there too.
- docs-check-no-git and wire-accountability.
- The runner contract gate (109 s). `scripts/act_ci.py` is byte-identical, SHA-256 `f968f676…895c`.
- Fifteen host gates on the clean head.

Acceptance criteria: round-6 items 1 to 4 are met, with the evidence above. The HANDOFF ledger records each replaced self-test assertion against its planted control. `scripts/ci_events.py` is unchanged.

Open risks/questions:
- Elaboration's margin is 55 s on the ruled inputs. The exact-head hosted readback decides.
- The final-bank timings are not projection inputs. That bank ran three to five jobs at once on 16 CPUs, so its times are longer: worker-0 steps, 612.6 s against 558.6 s for one step; elaboration leg 0, 1193 s. Scaling contended times by the uncontended hosted ratio would count the contention twice.
- `test_nvm_firmware_shapes` prints a different "caught by N named finding(s)" count from run to run. Its fault search stops at the first named finding across a thread pool. Two unsharded runs differ the same way, and the verdicts are equal.
- These are projections, not hosted times. This is an author handoff, not a review verdict.
