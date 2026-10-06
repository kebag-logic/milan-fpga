Run from an isolated checkout at `0a004a8cc2ad879e74d8e4168bd4a39a12d5dbbe`.
Set `PACKET` to the directory holding this packet.
All disposable files belong in its `scratch/` directory.

```sh
export TMPDIR="$PACKET/scratch"
export PYTHONDONTWRITEBYTECODE=1
export PYTHON_CPU_COUNT=4
export MAKEFLAGS=-j16
python3 "$PACKET/verify_tree.py" .
python3 scripts/ci_rv32_sdk.py --destination "$PACKET/scratch/sdk"
export MILAN_RV32_CC="$PACKET/scratch/sdk/bin/riscv32-linux-gcc"
python3 "$PACKET/run_checks.py" . "$PACKET" controls
python3 "$PACKET/run_checks.py" . "$PACKET" firmware
PYTHON_CPU_COUNT=1 python3 "$PACKET/probe_rv32.py" . "$PACKET"
python3 scripts/docs_check.py
python3 scripts/check_doc_style.py
python3 -m venv "$PACKET/scratch/docs-venv"
"$PACKET/scratch/docs-venv/bin/python" -m pip install --require-hashes -r tools/markdown/requirements.txt
"$PACKET/scratch/docs-venv/bin/python" scripts/check_em_dash.py --base 6714181d
"$PACKET/scratch/docs-venv/bin/python" scripts/gen_toc.py --check
python3 "$PACKET/verify_tree.py" .
```

Use fresh scratch build directories for a repeat.
The host needs the documented C/C++ compilers, test libraries and PyYAML.
The three required submodules must be initialized at their gitlinks.
The SDK installer verifies the pinned archive and installed inventory.

`run_checks.py` remains a foreground supervisor until every child exits.
It runs independent commands concurrently with individual logs and exit files.
Its firmware phase allocates four compiler jobs per command, twelve total.
Each command has a 570-second limit; exit 124 means incomplete evidence.
The recorded run also overlapped lightweight checks within sixteen jobs.

The store campaign uses the published `public-evidence/author/nvm_foreground.py`.
Its bytes match the public evidence manifest.
It invokes the original complete driver with both `--require-rv32` and
`--self-test`, with four jobs. It only maps each worker's mutant build
directory onto a reusable path. Inventories, compile flags, source edits,
preprocessed cache keys, and named killing assertions remain unchanged.

`probe_rv32.py` copies only firmware sources into scratch.
It changes flags and disposable sources to exercise both real RV32 arms.
It imports the original store build module from the recorded base,
adding only `-fstack-usage` for the baseline frame measurement.
The original ctrl command must reproduce the missing ILP32 glibc stub.
The candidate must build and match its reported totals.

The hosted excerpt comes from public job `112422842862`, run `37508325617`.
Only relevant original log lines are selected; terminal color escapes
are removed. The job's complete log remains available through GitHub.
The run metadata and step conclusions are in `hosted-snapshot.json`.

The initial two Markdown-renderer checks refused absent dependencies.
Their `.rc` files remain as receipts; the `-complete` receipts record
the passing reruns after the locked renderer was installed in scratch.

No script runs a parent regression bank, hardware check, or local CI container.
