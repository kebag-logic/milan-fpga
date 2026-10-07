# Reproduction

Use the exact reviewed source head and an empty writable packet directory.
The scripts accept source and packet paths as arguments.
Use existing installations of the graph renderer and its browser dependency.
No system-wide installation is performed by these scripts.

```sh
python3 scripts/prepare_dependency.py "$PACKET"
python3 scripts/run_checks.py "$SOURCE" "$PACKET"
python3 scripts/run_probes.py "$PACKET"
python3 scripts/replay_remaining.py "$SOURCE" "$PACKET"
NODE_PATH="$BROWSER_MODULES" node scripts/inspect_graphs.cjs "$PACKET"
python3 scripts/verify_integrity.py "$SOURCE" "$PACKET"
```

The dependency setup uses a pinned public tag and verifies its commit.
It builds with 16 jobs into scratch.
The source scripts use the published two-job build commands.
Independent checks run concurrently inside foreground processes; dependent mutations remain serial.

The integrity script compares against `receipts/initial_ls_files.txt`.
Capture that receipt with `git ls-files --stage` from the exact source checkout before running probes.
The expected source head and tree are pinned in the script.
All disposable exports and dependencies belong below `scratch/` and must not be published.

The preview script requires a resolvable browser automation package.
Set `BROWSER_MODULES` to the graph renderer's existing module search directory containing that package.
It stores its profile in scratch and emits native and 760-pixel-page previews.
Sampled edge geometry supplements a separate visual review of every distinct image.

Command streams retain their original content apart from portable source/packet path normalization.
Expected nonzero results are retained in individual `.rc` files.
The C receive probe intentionally confirms known deviations; passing it is not standards conformance.
