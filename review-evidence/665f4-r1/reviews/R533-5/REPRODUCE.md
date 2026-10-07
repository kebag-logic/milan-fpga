Run from an isolated checkout at `500b8f64443777685e6a54049d933476710d26f0` with its required submodules initialized. Set `PACKET` to the directory containing this file. All disposable files go below `$PACKET/scratch`.

```sh
export PYTHONDONTWRITEBYTECODE=1
export TMPDIR="$PACKET/scratch"
python3 "$PACKET/scripts/focused.py" . --mode suites --jobs 4
python3 "$PACKET/scripts/focused.py" . --mode campaign --jobs 4
python3 "$PACKET/scripts/focused.py" . --mode probes --jobs 4
python3 sw/firmware/gtest/fw_coverage.py --check --jobs 4 --keep "$PACKET/scratch/coverage"
python3 scripts/check_submodule_docs.py
```

The four independent suite/campaign/probe/coverage invocations can run concurrently as foreground commands, for at most sixteen compilation jobs. Preserve each stdout/stderr stream and exit status. The probe collector intentionally records failing binaries and exits zero when the old-pin control and fault controls behave as expected. Inspect `receipts/probes.json` and each binary tally: the current head fails withdrawal/recovery at IF=1 and IF=2. Three deliberate plants fail their named tests at both counts. The former dependency pin must be available as an object:

```sh
git -C third_party/lwSRP fetch origin 23d9a8173b07503a0ee6e8528f922fceab4e67f0
```

For deliberate dependency mutations and the old-pin control, `focused.py` exports Git objects into scratch and bypasses the exact-pin check only for those labeled controls. The unmodified head is validated before that override. Production checkouts are never modified. The independent C++ probes use the real mailbox model, static allocator and production adapter.

Reconstruct the runtime and SDK from public data. The source fetcher requires the 57 published input hashes. Supply the pinned SDK archive as `SDK_ARCHIVE`; a fresh destination is required.

```sh
python3 "$PACKET/scripts/fetch_runtime.py"
python3 scripts/ci_rv32_sdk.py --archive "$SDK_ARCHIVE" --destination "$PACKET/scratch/sdk"
python3 "$PACKET/scripts/measure.py" .
python3 "$PACKET/scripts/integrity.py" .
```

`measure.py` runs four links concurrently and records four head plus four FC-base results. No runtime source is obtained from an author's local installation. Its external sources, revisions and hashes are in `receipts/runtime-inputs.json`. SDK archive SHA-256: `d42680e926542595c4c87629d33f5f90aac1e9a964c8955089e0514caa01b78f`.

Receipt paths are relative to this packet. Path-only normalization replaces local roots with `$REPO`, `$PACKET` and `$SDK_ARCHIVE`; original raw logs remain in unpublished scratch, and their original hashes are recorded in `receipts/receipt-provenance.json`. No diagnostics, assertion values or verdicts are changed. `scripts/package.py` generates that provenance and MANIFEST.sha256 after report completion.
