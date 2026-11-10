# Round 5 evidence at 7c97e99f53ab0efc3e05e4617ee652dbab6e1b14

The head is four commits on round 4's `30ca4b21`. `dev-soft-core` is still `1d6bf555`, so nothing was merged.
Every run below is on a fresh clean clone of this head, except the sweep, which is explained in its own section.
The `*tree-after*` files record `git status` after each job. Every one is clean at this head.

## Workflow steps (`gates/verify.md`)

- The four workflows a pull_request to `dev-soft-core` triggers: `rtl-fast`, `elaborate`, `rtl` (as for a ready PR) and `docs`.
- 30 jobs. 152 `run:` steps ran, all rc 0. 198 did not run, each with its reason in `gates/tools/not_run.json`. Table: `gates/verify.md` (verify_wf rc 0).
- Runner: `gates/tools/run_wf.py`, one job per clone, step by step. Drivers: `gates/tools/drive.sh`.
  - Lists `r4-a.txt`, `r4-b.txt` and `r4-c.txt` ran first. A planned host power-off at 07:49 cut them.
  - Lists `r5-a.txt`, `r5-b.txt` and `r5-c.txt` ran what was left, each job on a fresh clone. The rtl-fast aggregate's one local step is in `r5-b.txt`.
  - Driver logs: `gates/drivers`. `drive-*5.log` are the resumed runs.
- The builder bank, `test_builder.py --require-rv32`: legs 0 and 1 in `docs`, and in `elaborate` with `--require-elaboration` too. Each pair's union is 107 gates exactly once, with the requirements judged on the union, rc 0 (`gates/union`, `scripts/ci_builder_legs.py union`).
- The LiteX simulations: `elaborate.elaborate-gates-1__gate_19`, 8 of 8 PASS (`gates/litex-sim-logs`).
- The saved-state writer gate: `docs.docs-gates-0__gate_28`, `OK across 5 shape(s), and every planted defect reddened`.
- The NVM record-space gate step, `docs.docs-gates-0__gate_26`, runs the format page's drift gate. It prints `0 finding(s)`, `control moved-lines: 0 finding(s)` and `self-test: PASS`. The reference gate prints `all 9 planted defects caught`.
- The store's suites, `rtl-fast.firmware-unit__ci_step_11`:
  - `OK across 5 shape(s), 728 tests`;
  - `save bound at 32x32/2if TDM8, change to read back: 321274 us during the erase, 325187 us during a compaction (bound 500 ms)`;
  - `append at 32x32/2if TDM8, due to read back: 175187 us; twice it 350374 us, the deadline 500 ms`.
- The coverage ratchet, `rtl-fast.firmware-unit__ci_step_12`: `firmware coverage: PASS (35 files)`.
- The control mutants, `rtl-fast.firmware-control-mutants__ci_step_9`: `mutants: 570 of 570 caught`.
- `cd tests && behave`, `rtl-fast.bdd-conformance__ci_step_5`: 508 scenarios passed, 0 failed.
- The firmware boundary, `rtl-fast.firmware-boundary__ci_step_9`: `ctrl_boundary: PASS`.

## Full sweep (`sweep/`), at `b6a60fbd`

- Four shard units, `scripts/run_all_suites.sh <logs> --wait --shard k/4`, spec `sweep/sweep-spec.json`, four CPUs each. The shard holding `capture_coherence` (shard 2) ran on four CPUs.
- 65 suites: 65 PASS, 0 FAIL, 0 TIMEOUT. Every shard's preflight passed, suite cancellation included. No suite-cancellation or `gptp_shadow` lifecycle failure occurred, so nothing was re-run.

| Shard | Suites | Passed | Checks | In-suite failures |
|---|---:|---:|---:|---:|
| 0 | 15 | 15 | 360,992 | 0 |
| 1 | 17 | 17 | 1,526,104 | 0 |
| 2 | 17 | 17 | 284,228 | 0 |
| 3 | 16 | 16 | 21,575 | 0 |

Why the sweep at `b6a60fbd` stands for this head:

- `b6a60fbd..7c97e99f` changes eight files: `sw/firmware/ctrl/test/ctrl_configs.py`, `sw/firmware/ctrl/test/test_acmp_nvm.cpp`, `sw/firmware/ctrl_nvm/README.md`, and `nvm_fixture.py`, `nvm_mutants.py`, `nvm_rig.cpp`, `test_nvm_journal.cpp` and `test_nvm_write.cpp` under `sw/firmware/ctrl_nvm/test/`.
- A search of `tb/` and `scripts/run_all_suites.sh` for those paths finds two directories. One is `tb/verilator/ctrl_service_budget/README.md`. The other is `tb/verilator/nvm_split_target`, whose `target_cases.py` imports only `nvm_contract` and `nvm_klj3`, neither changed.
- Neither directory is one of the 65 sweep suites. `fw_service_budget`, which is, reads `milan_baremetal`, which is unchanged.

## Other gates (`extra/`)

- `extra.ctrl_nvm_selftest.log`: `test_ctrl_nvm.py --require-rv32 --self-test --jobs 8`, rc 0. It prints `OK across 5 shape(s), 728 tests, and all 191 planted defects reddened`: 183 planted defects and 8 controls.
- `extra.drift_gate.log`: `check_nvm_format_32x32.py` and its `--self-test`, rc 0. `0 finding(s)`, `self-test: PASS`.
- `extra.diff_check.log`: `git diff --check 1d6bf555 HEAD` against the merge base, rc 0.
- `extra.twin.log`: `make -j8 -C tb/verilator/milan_dp twin && make -j8 -C tb/verilator/milan_dp twin-plants`, rc 0. It prints `twin: 0 finding(s)`, and each of its 20 plants is refused twice, 40 refusal lines in all, as in round 4. The verdict lines are in `extra/twin-excerpt.txt`. The full log is over 200 KB and is listed in `extra/LARGE.tsv`.
- `extra.mem_head.log` and `extra.mem_base.log`: the split memory plan, below.

## The split memory plan (`memory/`)

`measure.sh` links the split size fixture at four points with the pinned SDK and plans each. It ran on clean clones of `30ca4b21` and of this head.

| Point | `30ca4b21` RAMB36 | This head RAMB36 |
|---|---:|---:|
| 1x1 | 37.5 | 39.0 |
| 1x1, two interfaces | 41.0 | 42.0 |
| 8x8 | 51.0 | 52.5 |
| 8x8, two interfaces | 57.5 (the ledger) | 59.5, refused |

- At this head the 8x8 two-interface point prints `REFUSED: allocation over budget: 59.5 RAMB36 (rom 125824 bytes in 126976, sram 114832 bytes in 116736) exceeds the 57.5-RAMB36 budget ledgered for 8x8, two interfaces` (`memory/at-7c97e99f/8x8-if2.log`, rc 2).
- `30ca4b21` plans that point at the ledger's 57.5 (rc 0).

## Planted-defect grading before the last two commits (`plant-grading/`)

These runs used the suite's own `plant_and_grade` on the working tree, keeping each named test's log.

- `g1`: the 12 planted defects that `d01c66ad`'s self-test missed, graded again before the fixes below: none caught, as that run said.
- `g3`: after the fixes, 9 of the 10 kept defects caught. `move_before_base_closes` was not caught.
- `g4`: after its fix, `move_before_base_closes` caught.
- `g5`: the four delta record defects caught, including the new `delta_crc16_unchecked`.
- Two of the 12 were dropped, `delta_count_unbounded` and `delta_overrun_unchecked`. The record rules and the pad rule refuse every delta either guard would, so no verdict can tell a store without them (the store's README).

## Earlier runs, superseded

- `superseded-system-cc/`: runs made while the RV32 arm fell back to the system compiler, because round 3's SDK home was gone. The pinned SDK was then installed offline, digest checked, and every gate above uses it.
- `first-run-b6a60fbd/`: `firmware-boundary` refused `scripts/check_nvm_format_32x32.py`, which now reads the store's constants, as an unregistered builder. Commit `d01c66ad` lists it among the programs that compile nothing.
- `second-run-d01c66ad/`: the control mutants caught 569 of 570, and the store's self-test missed 12 planted defects. Commits `a9c6391f` and `7c97e99f` fix both.
- `interrupted-poweroff/`: the partial logs of the four runs at this head that the 07:49 power-off cut: `firmware-control-mutants`, `docs-gates-1`, `elaborate-gates-1` and the store's self-test. None is counted above. Each ran again from a fresh clone.

Files over 200 KB are listed in each directory's `LARGE.tsv` by bytes and sha256. `RAW.tsv` holds the digest of each source before host prefixes were replaced.
