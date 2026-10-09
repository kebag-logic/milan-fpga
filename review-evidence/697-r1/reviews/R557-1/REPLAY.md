Reviewer controls and receipts for R557-1

Set `REPO` to a clean checkout of the reviewed head. Set `PACKET` to this packet directory. Keep all temporary output under `PACKET/scratch`. Existing host dependencies are required; these scripts install nothing.

```sh
mkdir -p "$PACKET/scratch"
cd "$REPO"
gh api 'repos/kebag-logic/milan-fpga/git/trees/6aa25dec977c6ad78bf4ff6275de47fb81d0c246?recursive=1' > "$PACKET/scratch/source-tree.json"
python3 "$PACKET/scripts/fetch_source.py" "$PACKET/scratch/source-tree.json" "$PACKET/scratch/source"
python3 "$PACKET/scripts/audit_import.py" "$REPO" "$PACKET/scratch/source" "$PACKET/scratch/test-split.diff"
python3 "$PACKET/scripts/run_checks.py" "$REPO" "$PACKET/scratch/checks" "$PACKET/scratch/raw-checks"
python3 "$PACKET/scripts/audit_mutations.py" "$PACKET/scratch/source" "$REPO" "$PACKET/scratch/checks/mutations/results.json"
PYTHONDONTWRITEBYTECODE=1 python3 "$PACKET/scripts/probe_controls.py" "$REPO" "$PACKET/scratch/probes" "$PACKET/scratch/checks/mutations"
gcc -std=c11 -Wall -Wextra -Werror -Iinclude -Iexamples "$PACKET/scripts/adp_input_probe.c" src/adp.c examples/adp_port.c -o "$PACKET/scratch/adp-input-probe"
"$PACKET/scratch/adp-input-probe"
python3 "$PACKET/scripts/verify_checkout.py" "$REPO"
```

The ADP control returns 1 at the reviewed head because three malformed inputs are accepted. `probe_controls.py` returns 0 when its experiment completes; inspect its individual gate results. In particular, the stale-report campaign incorrectly returns 0, whereas deleting its XML makes it return 1. The controls modify only their disposable copies.

`run_checks.py` invokes native builds with `make -j16`. Independent analysis, mutation, and metadata campaigns run concurrently, with eight mutation workers. The two native test suites also run concurrently. Native full builds use separate phases to bound resource use. Library-only Release builds were separately run for both compilers with `TSN_TESTS=OFF`, concurrently, using `make -j16`.

The source-table audit evaluates only mutation-table assignments and definitions. It runs no parent test bank. The import audit shows exact residual test changes after the documented extraction. Original passing core assertions remain unchanged.

Published receipt text substitutes `$REPOSITORY`, `$REVIEW_PACKET`, and `$REVIEW_SCRATCH` for local locations. Original receipt hashes remain in [location-redactions.json](receipts/location-redactions.json). [MANIFEST.sha256](MANIFEST.sha256) covers the publishable files. No scratch content is published.
