# Reproducing the focused review

Use an isolated checkout containing the reviewed commit and its base, Python 3,
GNU make, and the stated synthesis/simulation installations. No script writes
the checkout's source. Choose a fresh output packet; all disposable files belong
under its `scratch/`. The checker mutation sweep is informative: its exit status
means the control and mutation construction were valid, not that all mutants
were killed. Read its summary.

Set `review_repo` to the checkout, `review_packet` to a fresh output packet, and
`review_scripts` to this published scripts directory. Create
`$review_packet/receipts`, `$review_packet/scratch/tmp`,
`$review_packet/scratch/head` and `$review_packet/scratch/main`. Export
`TMPDIR=$review_packet/scratch/tmp` and `PYTHONDONTWRITEBYTECODE=1` for every
Python command. Do not redirect work to shared or private author directories.

1. Run `verify_tree.py "$review_repo" 169073fe9751b873d140b46d4363e02ad4f56b88`.
   It verifies tracked blob bytes, executable modes, index, worktree and gitlinks.
2. Export that commit with `git -C "$review_repo" archive` and extract it into
   `scratch/head`. Export base `5dce647ab5a01a6ecff9a982b22e3a4a1d946d3d` into
   `scratch/main`. Verify each export with the third argument to `verify_tree.py`.
3. Run `vivado_ooc.sh "$review_packet/scratch/head" "$review_packet/scratch/viv_head"`
   and then the corresponding `scratch/main`/`scratch/viv_main` command.
   Each command holds `$VIVADO_LOCK` by default; pass the same local
   shared lock as a third argument if different. Set `VIVADO_SETTINGS` to the
   installed settings file if needed. Both runs use `make -j16 ooc`, run the
   two tops sequentially and retain logs, reports, timestamps and return codes.
   Run them in the foreground, never beside another heavy build.
4. Run `compare_reports.py "$review_packet"`, then
   `boundary_probes.py "$review_repo" "$review_packet"`. The latter consumes
   the newly generated raw head receipts and exact XDC path; it requires no
   further synthesis. Its make-flow checks use a harmless shell stub.
5. Run `quick_gates.py "$review_repo" "$review_packet" /path/to/pinned/verilator`.
   It verifies version 5.050 and runs only the five independent lightweight
   gates concurrently, each with its own log, rc and time file.
6. Run `mutate_checker.py "$review_repo/syn/ooc/check_ooc_clock.py" "$review_packet/scratch/mutants" --jobs 16`.
   For concurrent use with other light probes reduce `--jobs` so the total
   stays within 16. The recorded round's sweep is `checker_mutation_sweep.txt`.
7. Run `real_port_probe.py "$review_repo" "$review_packet"` under the same lock.
   It creates a fresh export, renames the engine's clock signal only, and runs
   the shipping runner. It expects that runner to return 1 with all named
   missing-clock findings. No background process is left behind.
8. After an independent verdict is written, `prior_resolution_probes.py` can
   recheck the prior public mutation variants and optional parser diagnostics.
   It requires `receipts/independent_verdict.md` to exist before running.
9. Re-run `verify_tree.py` on the source checkout after all probes. No tracked
   file needs restoration because all mutations were in disposable copies.

Published logs have path/host identifiers redacted by
`prepare_public_receipts.py`. Measurements and diagnostics are preserved.
Raw originals stay under unpublished `scratch/raw_receipts/`. To rerun the
receipt-based probes at another path, generate the two small OOC measurements
as above; do not mistake redacted full-path strings for a different checkout's
actual XDC path. No full simulation/builder bank, hosted workflow, container or
hardware run is part of this recipe.
