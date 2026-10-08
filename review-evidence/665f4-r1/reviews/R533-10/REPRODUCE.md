R533-10 packet reproduction

Use a clean source checkout at `82a79638405c3365e4078da471be56758f8dd679`, with its exact lwSRP, protocol-processor, gptp-processor and verilog-axis submodules initialized. Keep this packet separate from the checkout. Python 3, Git, the native C/C++ compilers, CMake/Ninja, the repository test dependencies and coverage utilities are required. Public evidence auditing also uses the authenticated read-only GitHub CLI. No container, hardware or hosted execution is required by these scripts.

Set `REVIEW_PACKET` to this packet directory and run commands from the source root. `run_group.py` sets the temporary directory under packet scratch and disables Python bytecode output. Its task calls run concurrently inside one foreground process; it waits for every child. Use at most four workers with four compiler jobs each. Do not run multiple groups concurrently if their combined build concurrency exceeds 16. The original validation also ran the serial prior-probe group while the three four-job validation builds ran, respecting that ceiling.

```sh
export REVIEW_PACKET=/absolute/path/to/packet
mkdir -p "$REVIEW_PACKET/scratch" "$REVIEW_PACKET/receipts"
python3 "$REVIEW_PACKET/scripts/run_group.py" "$REVIEW_PACKET/scripts/native-group.json" --workers 2
python3 "$REVIEW_PACKET/scripts/run_group.py" "$REVIEW_PACKET/scripts/wire-group.json" --workers 2
python3 "$REVIEW_PACKET/scripts/run_group.py" "$REVIEW_PACKET/scripts/validation-group.json" --workers 4
python3 "$REVIEW_PACKET/scripts/run_group.py" "$REVIEW_PACKET/scripts/prior-group.json" --workers 1
python3 "$REVIEW_PACKET/scripts/run_group.py" "$REVIEW_PACKET/scripts/asan-group.json" --workers 1
```

The wire-group child tests intentionally exit 1 on the reviewed defective head: three executed failures and one passing control per interface count. Native, coverage, SDK, standing-mutation campaigns, prior-probe campaigns and the sanitizer accounting should exit 0. A mutation's inner suite normally exits 1 when caught; the accounting driver requires the expected executed failure. The original interface-factor plant is equivalent at IF=1 and must pass there. `run_group.py` itself does not aggregate intentional child failures; inspect every `.rc` and the execution JSON.

`focused.py` accepts `native`, `plants`, `independent` and `prior`, plus `--interfaces 1|2 --jobs 4 --source SOURCE --packet PACKET`. `prior_bounds.py` imports only the plant definitions from the preserved historical script; its current driver rejects compilation refusals. Each probe uses copied source/test files under scratch. No candidate file is patched.

For images, the validation group first extracts the repository-pinned SDK into `scratch/sdk`. Point `REVIEW_DEPENDENCIES` to a provisioned dependency root containing `litex/litex/soc/software`, `pythondata-software-picolibc/pythondata_software_picolibc/data` and `pythondata-software-compiler_rt/pythondata_software_compiler_rt/data`. Source hashes actually used are in `receipts/runtime-provenance.json`. The image script builds fresh runtime archives and compares the four images against the included public round-10 JSON.

```sh
export REVIEW_DEPENDENCIES=/absolute/path/to/runtime/dependencies
python3 "$REVIEW_PACKET/scripts/run_group.py" "$REVIEW_PACKET/scripts/images-group.json" --workers 1
```

For the documentation subset, set `REVIEW_DOCS_PYTHON` to the environment containing the repository's renderer dependencies (defaults to `python3`). It is used for the em-dash checker; the remaining commands use the normal interpreter.

```sh
python3 "$REVIEW_PACKET/scripts/run_group.py" "$REVIEW_PACKET/scripts/docs-group.json" --workers 4
PYTHONDONTWRITEBYTECODE=1 python3 "$REVIEW_PACKET/scripts/public_audit.py" --jobs 4
PYTHONDONTWRITEBYTECODE=1 python3 "$REVIEW_PACKET/scripts/integrity.py"
```

The public audit retrieves the exact evidence commit, hashes retained logs, and binds its changed-file inventory to source bytes. It does not execute the manager's banks. `integrity.py` independently hashes tracked Git blobs, checks executable/symlink modes, compares the whole index to the tree and validates required submodule contents at their gitlinks without refreshing the index.

The shipped receipts correspond to actual completed review runs. Only final executed wire-probe receipts are published. Two reviewer-script construction problems and their corrections are disclosed in `receipts/probe-construction.txt`. Re-running these commands overwrites receipts; use a fresh packet copy if preserving the originals.

Publication excludes all scratch contents. `receipts/publication.json` records path normalization and original/published hashes; diagnostics, test outcomes and numbers are unchanged. `MANIFEST.sha256` lists the report, reproduction notes, portable scripts and all publishable receipts, with paths relative to this directory.
