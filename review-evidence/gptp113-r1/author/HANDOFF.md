# [A854] gptp113 (FPGA-gPTP #113): HANDOFF

**Status (2026-11-26 08:22): REVIEW READY at `af11b3ef631eb44cdc1730cfb31bedda95c33dc5`.** Nothing is running.
Nothing was pushed or posted.

## Where things are

| What | Path / ref |
|---|---|
| FPGA-gPTP lane clone | `$VALIDATION_STORAGE/gptp113-a854`, branch `113-runner-ratchets` (2 commits on `3009f9a2`) |
| Consumer probe | `$VALIDATION_STORAGE/gptp113-a854-milan`, branch `gptp113-ratchet-probe` = `dev-soft-core` `c34e7d8b06` + `f791fdea1f` (gitlink only, local) |
| Lane tools | `$VALIDATION_STORAGE/gptp113-a854-tools` (`plants.py`, `engine_arm.sh`, `clock_sites.py`, `ast_same.py`, `index_receipts.py`); copies are in `receipts/tools/`, with their own host paths placeholdered |
| Raw logs | `$VALIDATION_STORAGE/gptp113-a854-logs`; cleaned copies are in `receipts/logs/`, indexed in `receipts/INDEX.md` |
| PR text | `PR-BODY.md` (Closes #113; no host paths, tool names or lane labels) |

## What was done

1. **Idiom.** `pass_run.py` gained docstrings on `chunk`, `forward`, `stop` and `main`. The test gained docstrings
   on `read`, `main` and `caller`, an annotation on `caller`'s `limit`, and `make()` dropped its unused `stdout`
   parameter (7 → 6).
2. **Evidence.** The test moved from `tb/verilator/engine/passes_test.py` to `tb/engine_passes_test.py` and now
   reaches the engine through `ENGINE = …/verilator/engine`. The engine Makefile's `passes-test` runs
   `python3 ../../engine_passes_test.py`. `docs/TEST_DEVELOPER.md` gained one row. The reasons for moving it are
   in REVIEW-READY.md.
3. **Proof.** Every item has its receipt in REVIEW-READY.md's table.
   - Consumer ratchets: rc 0/0 with the budgets unchanged; at `3009f9a2` they gave rc 1/1.
   - 13/13 plants caught at both layouts.
   - `passes-test`: 73/73 on four runs.
   - Engine `-j4`: the clean and planted-abort pairs are IDENTICAL.
   - `make docs`, `contract`, `lint`: rc 0.

## Resources

- **CPU.** Every heavy command ran in a user scope at CPU weight 20, with no booking.
- **ccache.** Only the shared `$VALIDATION_STORAGE/ccache`.
- **Verilator.** Pinned 5.050 (`$VALIDATION_TOOLS/verilator-v5.050`) for the engine runs and the head lint. The
  first `-r1` lint used the system's 5.054.
- **Scratch** is about 0.72 GB of the 6 GB allowed:
  - the consumer clone, 660 MB;
  - the gPTP clone, 11 MB;
  - `gptp113-a854-scratch`, 27 MB: four detached worktrees (`wt-base`, `wt-head`, `wt-base-abort`,
    `wt-head-abort`) with their `obj_dir`s, and `tmp/`.
- **Can be removed after review:** the four worktrees (`git -C $VALIDATION_STORAGE/gptp113-a854 worktree remove
  --force <path>`) and `gptp113-a854-scratch/tmp`. Nothing was deleted this session.

## Notes for the manager

- **For the pin lane (#1013).** When a later gPTP pin adopts PR #112's runner, a pin at or after `af11b3e`
  passes both consumer gates with the budgets as they are. The consumer needs no change, and no consumer file
  names the test.
- **The 90 s figure.** `docs/TEST_DEVELOPER.md` still says the passes check takes "about 90 seconds" (PR #112's
  figure). Under this host's load it took about 116 s. That was left as it is.
- **The background run.** The plant matrix was moved to the background by the 600 s foreground limit; it
  completed with exit 0. Everything else ran in the foreground.

REVIEW READY af11b3ef631eb44cdc1730cfb31bedda95c33dc5
