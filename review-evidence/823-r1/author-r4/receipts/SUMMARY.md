# Round 4 evidence at 30ca4b216e6f7dd386e1d0a0015b0b23b4e08c14

Every run below is on a fresh clean clone of this head, the merge of `dev-soft-core` `1d6bf555` plus round 4's fixes.
The `*tree-after*` files record `git status` after each job; every one is clean.

## Workflow steps (`gates/verify.md`)

- The four workflows a pull_request to `dev-soft-core` triggers: `rtl-fast` (with `split-cdc`, new on `1d6bf555`), `elaborate`, `rtl` (as for a ready PR) and `docs`.
- 152 `run:` steps ran, all rc 0. 198 did not run, each with its reason in `gates/tools/not_run.json`. Table: `gates/verify.md` (verify_wf rc 0).
- Runner: `gates/tools/run_wf.py`, one job per clone, step by step. Drivers: `gates/tools/drive.sh` with the lists `gates/tools/r4-a.txt`, `r4-b.txt` and `r4-c.txt`. Their logs are in `gates/drivers`.
- The rtl-fast aggregate's one local step ran on its own (`gates/drivers/drive-agg.log`).
- The builder bank: legs 0 and 1 in `docs` (`--require-rv32`) and in `elaborate` (`--require-elaboration`). The union of each pair is 107 gates exactly once, requirements judged on the union, rc 0 (`gates/union`, `scripts/ci_builder_legs.py union`).
- The LiteX simulations: `elaborate.elaborate-gates-1__gate_19`, 8 of 8 PASS (`gates/litex-sim-logs`).
- The saved-state writer gate: `docs.docs-gates-0__gate_28`, `OK across 5 shape(s), and every planted defect reddened`.
- The format page's drift gate in the docs workflow: `docs.docs-gates-0__gate_26` (the NVM record-space gate step). It prints `0 finding(s)`, `control moved-lines: 0 finding(s)` and `self-test: PASS`.

## Full sweep (`sweep/`)

- Four shard units, `scripts/run_all_suites.sh <logs> --wait --shard k/4`, spec `sweep/sweep-spec.json`, four CPUs each. The shard holding `capture_coherence` (shard 2) ran on four CPUs.
- 65 suites: 65 PASS, 0 FAIL, 0 TIMEOUT. Every shard's preflight passed, suite cancellation included.

| Shard | Suites | Passed | Checks | In-suite failures |
|---|---:|---:|---:|---:|
| 0 | 15 | 15 | 360,992 | 0 |
| 1 | 17 | 17 | 1,526,104 | 0 |
| 2 | 17 | 17 | 284,228 | 0 |
| 3 | 16 | 16 | 21,575 | 0 |

## Other gates (`extra/`)

- `extra.ctrl_nvm_selftest.log`: `test_ctrl_nvm.py --require-rv32 --self-test --jobs 8`, rc 0. It prints `OK across 5 shape(s), 506 tests, and all 130 planted defects reddened`: 127 planted defects, plus the controls of the NAME refusal and the two map-width refusals.
- `extra.drift_gate.log`: `check_nvm_format_32x32.py` and its `--self-test`, rc 0.
- `extra.diff_check.log`: `git diff --check 1d6bf555 HEAD` against the merge base, rc 0.
- `extra.twin.log`: `make -j8 -C tb/verilator/milan_dp twin && make -j8 -C tb/verilator/milan_dp twin-plants`, rc 0. This is the two-placement simulation from `1d6bf555`, which compiles this store. `twin: 0 finding(s)`, and each of its 20 plants is refused twice (against its own half and between the placements). The verdict lines are in `extra/twin-excerpt.txt`; the full log is over 200 KB and is listed in `extra/LARGE.tsv`.

## Before the commits (`pre-commit/`)

- `grade1.log`: the new planted defects, graded on the working tree with the suite's own `plant_and_grade`, all caught: `legacy_any_nonblank_header`, `ver_overrides_own_refusal`, `legacy_b_wrong_place`, `erase_first_block_every_time`, `step_bytes_layout2`, and the two width controls.
- `f1-1x1.log`: the F1 suite at 1x1, rc 0.
- `test_ctrl_memory_fix.log`: `sw/litex/test_ctrl_memory.py` (LiteX venv) after the rule-text fix, PASS.
- `probes/mapout_assert_removed.log`: with the output-width assert removed, a 65,536-entry output map is refused by two errors. One is the slot assert. The other is `-Werror=type-limits` in `nvm_klj2.c`.

## The first head, `8c66ab1e` (`first-run-8c66ab1e/`)

- The first full run was on `8c66ab1e`. Its `elaborate-gates-1` LiteX aggregate failed: `test_ctrl_memory` reads the memory plan's rule table against `ctrl_memory.RULES`, and only the page said KLJ3.
- Commit `30ca4b21` says KLJ3 in `ctrl_memory.RULES`, and every gate above was then run again on it.
- The failing log and the drivers' logs of that run are kept here.

Files over 200 KB are listed in each directory's `LARGE.tsv` by bytes and sha256. `RAW.tsv` holds the digest of each source before host prefixes were replaced.
