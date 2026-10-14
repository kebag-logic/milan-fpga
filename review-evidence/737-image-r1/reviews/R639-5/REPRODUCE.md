This packet reviews source head `4391f353690972f4844cb641b1e77fa94f38cdf4`.

Use a fresh packet scratch directory. The scripts take the checkout path as their first argument and keep disposable fixtures under `scratch/` next to the scripts. They do not write source fixes or invoke Docker. Python 3.12.3 with PyYAML is the reference interpreter. `probe-independent.py` uses the inventory main entry point with both command-line modes and compares safe sentinel fixtures with Bash and GNU Make 4.3.

```sh
python3 "$CHECKOUT/ci/image/prepare_parser.py" --output "$PACKET/scratch/shfmt"
python3 "$PACKET/probe-independent.py" "$CHECKOUT"
python3 "$PACKET/drift-controls.py" "$CHECKOUT"
python3 "$PACKET/verify-tree.py" "$CHECKOUT"
```

The drift driver expects `scratch/reference/bin/python3`. The review produced that executable wrapper with `extract-reference.py` from the authenticated cold image archive. To inspect the delivered pair, supply a directory containing `cold-a/image.tar`, `cold-b/image.tar`, `cold-a/context/` (the pinned source archives) and `cold-a/base-locked.tar`:

```sh
python3 "$PACKET/inspect-exports.py" "$CHECKOUT" "$EXPORT_DIRECTORY"
python3 "$PACKET/extract-reference.py" "$CHECKOUT"
python3 "$PACKET/extract-make.py" "$CHECKOUT"
python3 "$PACKET/audit-population.py" "$CHECKOUT"
```

Put `scratch/reference/bin` first on PATH when reproducing the reference-interpreter/Make probes. `inspect-exports.py` authenticates layer blobs and checks the lock before executing any extracted program. The downloaded source archives and image exports are not included in the publication packet.

`run-gates.py` consumes the public step plans and records every planned command, including explicit NOT RUN reasons. It is a bounded local subset of workflow execution, not a replacement for hosted/act acceptance. Set `REVIEW_VERILATOR_DIR` to the directory of the independently verified Verilator 5.050 executable. The executed review driver used that scoped path directly; the publishable driver makes it an environment parameter. Its original 540-second per-command limit expired on docs step 34; `retry-compiler-absent.py` gives that scoped check 1,800 seconds and records a separate result. No full builder/Yosys/parent/processor bank is enabled by these scripts. Shared SDK installation and orchestration self-tests are not run.

`public/` contains fetched executable receipts from commit `f4dc12aa4968489961047f67ce5c0e0b04367227`, under `review-evidence/737-image-r1`, not private lane notes. Original public Git blob and SHA-256 authentication records are retained. `publication-redactions.json` maps any local log path redactions to original/published hashes; replacements affect paths and account role labels only. MANIFEST.sha256 covers the actual publishable bytes. `scratch/` is never published.
