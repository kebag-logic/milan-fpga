R559-9 reproducer and receipt scope

Run from the packet directory, substituting the exact-head checkout path. Build products, package installation and temporary files stay in `scratch/`. No repository source edit is required.

```sh
rtk proxy python3 scripts/audit_delta.py <checkout>
rtk proxy python3 scripts/run_checks.py <checkout>
rtk proxy python3 scripts/run_maap.py <checkout> <scoped-5.050-compiler>
rtk proxy python3 -I scripts/R558-9/record_vs_lane_routes.py <checkout> c6bd08c6f52632c6d33d834ce842ac3cf63f29cc 26e2748f47b0d8fa533f53203264d9f31fc13c48
rtk proxy python3 -I scripts/R558-11/check_plan_composition.py <checkout>
rtk proxy python3 -I scripts/check_record_wording.py <checkout> 26e2748f47b0d8fa533f53203264d9f31fc13c48
rtk proxy python3 -I scripts/check_record_wording.py <checkout> b075a994f6daae3b406bce415a837b7c401712d5
rtk proxy python3 scripts/audit_delta.py <checkout>
```

All commands should exit zero except the pre-fix wording control, which must exit one and name M5. The two imported scripts are unmodified published scripts; `receipts/prior-script-provenance.json` records their immutable URLs and blob IDs. They report numerical comparisons and reference candidates. Their exit status alone is not a semantic wording verdict. The separate wording control and manual reading supply that check.

The documentation checks require the repository's hash-locked Markdown dependencies. The first local attempt correctly refused three checks because the renderer was absent. Those outputs remain under `receipts/setup-refusals/`. An isolated `scratch/venv` was then created with system packages visible, and its interpreter installed `<checkout>/tools/markdown/requirements.txt` with `pip install --no-cache-dir --require-hashes`. Only the three affected checks were retried with that interpreter. `receipts/checks.json` and `checks-retry.json` preserve both attempts. No shared package installation was changed.

The actual clean simulation commands were `make -j16 -C tb/verilator/maap run VERILATOR=<scoped-5.050-compiler> VERILATOR_JOBS=8 MDIR=<packet>/scratch/unit` and `make -j16 -C tb/verilator/maap integration-build VERILATOR=<scoped-5.050-compiler> VERILATOR_JOBS=8 DP_MDIR=<packet>/scratch/integration`, followed by `./maap_integration` from that build directory. `run_maap.py` reproduces these clean targets concurrently, with at most sixteen compiler jobs in total. It does not run the mutation campaign. In this review the unit build overlapped package setup; integration ran later. Every launched process was awaited in the foreground.

`receipts/unit.log` and `integration-build.log` retain the complete command output except the scoped compiler installation prefix, replaced with `<compiler-install>` for public attribution. `receipts/redactions.json` binds original and published hashes. Raw build logs stay unpublished in `scratch/`. `compiler-identity.json` records the selected version and hashes. No simulation result is changed by the path substitution.

`receipts/public-source/` contains unchanged historical published source receipts, retrieved by immutable blob ID from the requested evidence snapshot. Their provenance is in `public-source-provenance.json`. These are source-history evidence, not new runs at this review head. `hosted-checks.json` is a read-only snapshot with individual status, conclusion, exact head, timestamps and job URLs. Pending and skipped jobs are not executed successes.

The audit independently hashes every tracked blob, compares executable modes and all stage-zero index entries, and verifies the three required registered submodule checkouts against their gitlinks. Git replacement objects are disabled. No source restoration was necessary because this review never changed source files.

Only `MANIFEST.sha256` entries and `REPORT.md` are publication inputs. `scratch/` is excluded.
