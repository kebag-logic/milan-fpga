Run from the reviewed checkout with a fresh packet directory. Copy the published
scripts into its `scripts/` directory first. Set `packet` to its absolute path.
All network access below is read-only. No suite or full bank is launched.

```sh
mkdir -p "$packet/scratch" "$packet/receipts" "$packet/public"
export TMPDIR="$packet/scratch" PYTHONDONTWRITEBYTECODE=1
python3 "$packet/scripts/review_checks.py" "$PWD" "$packet" gates
python3 "$packet/scripts/review_checks.py" "$PWD" "$packet" inventory
python3 "$packet/scripts/review_checks.py" "$PWD" "$packet" mutations
python3 "$packet/scripts/review_checks.py" "$PWD" "$packet" plants
bash "$packet/scripts/refresh-verbatim.sh" > "$packet/receipts/refresh-verbatim.log" 2>&1
printf '%s\n' "$?" > "$packet/receipts/refresh-verbatim.rc"
python3 "$packet/scripts/measure_review.py" "$PWD" "$packet"
python3 "$packet/scripts/new_suite_review.py" "$PWD" "$packet"
python3 -I "$packet/scripts/r626_mutate_original.py" "$PWD" "$packet/scratch/r626-original" --jobs 8
python3 -I "$packet/scripts/r626_mutate_with_driver.py" "$PWD" "$packet/scratch/r626-with-driver" --jobs 8
python3 "$packet/scripts/review_checks.py" "$PWD" "$packet" integrity
```

`gates` records each subprocess result; inspect every `.rc`. The original legacy
harness exposes its missing-driver fixture. The adapted version adds only that
input. Its old missing-duration replacement reports DRIFT; the separate
`mutations` mode proves the required behavior at this head.

For renderer-dependent documentation checks, install only in scratch:

```sh
python3 -m venv --system-site-packages "$packet/scratch/venv"
"$packet/scratch/venv/bin/python" -m pip install --require-hashes -r tools/markdown/requirements.txt
"$packet/scratch/venv/bin/python" scripts/gen_toc.py --check
"$packet/scratch/venv/bin/python" scripts/gen_toc.py --verify-anchors
"$packet/scratch/venv/bin/python" scripts/check_em_dash.py --base c6bd08c6
```

The workflow ownership shell was copied verbatim from the exact head. Run it
with `SHARD=0` through `4`, `SHARDS=5`, and distinct scratch `RUNNER_TEMP`
directories. Its recorded outputs are `receipts/ownership-*.log`.

The new-suite script refuses an existing `scratch/new-suite` directory. Use a
fresh packet for a full repeat. Its last measurement is deliberately synthetic;
the procedure through real preflight runs on an unpublished copy.
