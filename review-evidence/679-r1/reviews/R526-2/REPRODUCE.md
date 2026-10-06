Run from a clean checkout of `04e1435a218908d2b12b4053e5dab2c2dcac2ebf`.
Initialize the three required submodules at their recorded pins.
Use an empty packet directory and copy this packet's `scripts/` there.
Provide the host test libraries, matching C/C++/coverage utilities and PyYAML.
All disposable output belongs under the new packet's `scratch/`.

Set `REVIEW_CHECKOUT` and `REVIEW_PACKET` to absolute paths, then run:

```sh
cd "$REVIEW_CHECKOUT"
mkdir -p "$REVIEW_PACKET/scratch" "$REVIEW_PACKET/receipts"
export TMPDIR="$REVIEW_PACKET/scratch"
export PYTHONDONTWRITEBYTECODE=1
python3 scripts/ci_rv32_sdk.py --destination "$REVIEW_PACKET/scratch/sdk"
python3 "$REVIEW_PACKET/scripts/run-checks.py" "$REVIEW_CHECKOUT" "$REVIEW_PACKET"
```

The coordinator runs the independent campaigns and suites concurrently,
awaiting all children in the foreground. It caps workers explicitly.
It records every command, return code and duration.
The store wrapper preserves the complete original campaign and its oracles.
It redirects only the physical per-worker mutant build directory.

The two renderer-dependent checks need the repository's locked packages.
Install those only in scratch, then repeat any setup refusals:

```sh
python3 -m venv --system-site-packages "$REVIEW_PACKET/scratch/doc-venv"
"$REVIEW_PACKET/scratch/doc-venv/bin/python" -m pip install \
  --cache-dir "$REVIEW_PACKET/scratch/pip-cache" --require-hashes \
  -r tools/markdown/requirements.txt
"$REVIEW_PACKET/scratch/doc-venv/bin/python" scripts/check_em_dash.py \
  --base 6714181d0c8a16e2983f85b724f4d688f5111835
"$REVIEW_PACKET/scratch/doc-venv/bin/python" scripts/gen_toc.py --check
```

Run the independent probes and final byte/index/gitlink proof:

```sh
python3 "$REVIEW_PACKET/scripts/runtime-binding-probe.py" "$REVIEW_CHECKOUT" "$REVIEW_PACKET"
python3 "$REVIEW_PACKET/scripts/local-data-probe.py" "$REVIEW_CHECKOUT" "$REVIEW_PACKET"
python3 "$REVIEW_PACKET/scripts/verify-tree.py" "$REVIEW_CHECKOUT"
```

Expected: both campaigns and standalone suites pass; all 76/106 mutants,
17 RV32 controls, and the 14-file coverage ratchet pass. Both masked runtime
dependencies fail for the named dependency, while global/weak definitions
pass and resolve in partial links. Every local t/b/d/r case stays unresolved.
Removing either external-definition filter breaks its committed control.
The final proof requires exact tracked bytes/modes/index and all three pins.

The initial renderer refusals in this packet remain receipts, not passes.
The locked rerun receipts carry the successful final documentation checks.
Hosted execution is independently identified by job URL and merge-tree proof
in the report. This reproduction does not run the manager's broader banks.
