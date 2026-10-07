R549-1 reproduction instructions

Use the reviewed checkout at `c7b69cd0fb2bdf980546ab413b3b82198267cbd8`.
Set `REPO` to that checkout and `PINNED_VERILATOR` to the verified 5.050 executable.
These scripts derive the packet directory from their own location.
Generated files remain in `scratch/`; receipts go to `receipts/`.

Run these two commands concurrently using a foreground supervisor:

```sh
python3 scripts/run_focused.py mutants --repo "$REPO" --verilator "$PINNED_VERILATOR"
python3 scripts/run_focused.py differential --repo "$REPO" --verilator "$PINNED_VERILATOR"
```

Both must return 0. The first reports 23/23 campaign rows.
The second reports 12 clean cases and 16/16 rejected controls.
The executable adapter caps the differential driver's hardcoded compilation concurrency at four.
The candidate scripts and RTL remain unchanged.

After both finish:

```sh
python3 scripts/build_probes.py --repo "$REPO" --verilator "$PINNED_VERILATOR"
python3 scripts/audit_baseline.py --repo "$REPO"
python3 scripts/verify_tree.py --repo "$REPO"
```

The build script runs two foreground build tasks concurrently, each with `-j 4`.
Read the individual `.rc` files; its own exit is not an aggregate verdict.
At the reviewed head, the repository unit harness returns 0 with 120 checks.
The independent probe executable returns 1 with three failed claims.
Those failures are the observations discussed in REPORT.md, not passing gate evidence.
The matrix within that probe covers 144 cases with zero mismatches.
It excludes normative approval of the two expressly deferred compare_MAC cells.

The unit build enables coverage. Its raw coverage data remains in scratch.
Use the same pinned distribution's `verilator_coverage --annotate` on that data,
then the repository's `tb/verilator/avtp_rxmon/cov_gate.py` with threshold 95 and `KL_maap.sv`.
`receipts/coverage.log` distinguishes the repository's 167/167 line gate from other coverage metrics.

`audit_baseline.py` checks policies and identities against the source base.
It cannot validate unprovided raw measurements or reconstruct their input digests.
`verify_tree.py` independently hashes tracked bytes, checks file modes and the full index,
and validates all three required submodule registrations and gitlinks.

Publication logs preserve results and diagnostics with local absolute paths replaced
by role placeholders. Their pre-redaction copies remain in unpublished scratch.
The standard PDF, its extracted text and rendered page are never published.
