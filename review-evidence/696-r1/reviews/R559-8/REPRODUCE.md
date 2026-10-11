# R559-8 reproduction

Use a fresh packet directory containing these scripts, with `scratch/` beneath it. `source` must be an isolated clean checkout of `aa980479aafd1d72c72015707fa6618b5aa47cb1`, with the three required submodules at their committed pins. Do not run against an active implementation checkout. Scripts accept source paths and keep builds/probes under the packet. Public API collection is read-only.

The original run used `$VALIDATION_TOOLS/pinned-verilator-5.050/verilator`; identity/hash and host versions are in `environment.json`. A reproducer may supply an equivalent verified 5.050 executable as `compiler`. Keep at most 16 compilation jobs in aggregate and remain within 12 GB. Run foreground orchestration, with no concurrent implementation route. `run_focused.py` runs the MAAP target, two datapath legs and lint concurrently; the probe script runs three independent builds concurrently.

```sh
python3 -I verify_tree.py "$source" > integrity-before.json
python3 -I audit_delta.py "$source" > composition.json
python3 -I audit_record.py "$source" > record-policy-delta.json
python3 -I record_vs_lane_routes.py "$source" 09c7231e 32582421 aa980479 > record-vs-lane-routes.log
python3 -I run_focused.py "$source" --compiler "$compiler"
```

After the focused runner creates `scratch/exact-tree`, execute these additional legs there. In the original run they overlapped the serial mutation campaign, with two compiler jobs per build. Counter recipes build their two legs concurrently. No source checkout is changed.

```sh
packet=$(pwd)
make -j16 -C "$packet/scratch/exact-tree/tb/verilator/milan_dp" \
  -f "$packet/counter_legs.mk" review-nxn review-nxn8 \
  VERILATOR="$compiler" VERILATOR_JOBS=2
make -j16 -C "$packet/scratch/exact-tree/tb/verilator/maap" integration-build \
  DP_MDIR=obj_review_integration VERILATOR="$compiler" VERILATOR_JOBS=2
(cd "$packet/scratch/exact-tree/tb/verilator/maap/obj_review_integration" && ./maap_integration)
python3 -I probe_wiring.py "$packet/scratch/exact-tree" --compiler "$compiler" --jobs 3
```

Capture counter and standalone integration stdout/stderr and exit statuses to the named `.log`/`.rc` files. The wiring script records statuses itself: each successful probe has build rc 0, run rc 1 and the named assertion. Clean commands must exit 0. Put temporary files and dependency installations under `scratch/`.

The docs run used a disposable environment with pinned hashed dependencies:

```sh
python3 -m venv scratch/doc-venv
scratch/doc-venv/bin/python -m pip install --require-hashes -r "$source/tools/markdown/requirements.txt"
scratch/doc-venv/bin/python -I run_docs.py "$source"
python3 -I verify_tree.py "$source" > integrity-after.json
git -C "$source" status --short --untracked-files=all > final-status.log
```

The twelve gate arguments/statuses are in `docs-results.json`. The baseline check validates the stored record; it does not measure an implementation.

`collect_public.py` extracts the requested historical receipts from git object `97f433d668907446e83c074b21e81d03a34988af`, verifies available published provenance entries, and records public decisions and a hosted snapshot. Do not attribute these old executions to the current head. `public-evidence/pr-body.json` is a separate read-only PR snapshot. Prior finding extracts preserve public URLs and were read after the independent pass.

`record_vs_lane_routes.py` is unchanged from the R558-9 public script: git blob `4b50af5e7b4bb59ecc7a9cd29b92f769fad93709`, path `review-evidence/696-r1/reviews/R558-9/scripts/record_vs_lane_routes.py`, evidence commit `c3708afa649adc2516c099f719b9ea36d7ee072f`. At this head historical base equality is correctly NO while both lane verdicts are PASS. `audit_record.py` additionally checks 66 inventory cells and unchanged policy.

`receipt-redactions.json` records compiler-path substitutions and hashes before/after. Originals remain only in unpublished `scratch/raw-logs/`; no assertion, diagnostic, result or exit status is changed. `scratch/` is excluded from `MANIFEST.sha256`. Verify publication files with `sha256sum -c MANIFEST.sha256` from the packet directory.
