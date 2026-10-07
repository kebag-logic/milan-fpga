R551-2 reproduction

Use the reviewed detached source head and the existing pinned dependency
interpreter. Start with an empty packet scratch directory for the export
campaign. All disposable sources, CPU data and generated outputs stay there.
No installation or source patch is required.

Set `SOURCE` to the source checkout, `PACKET` to this packet and
`DEPENDENCY_PYTHON` to the dependency interpreter.

```sh
rtk proxy python3 "$PACKET/scripts/verify_tree.py" "$SOURCE"
rtk proxy python3 "$PACKET/scripts/run_focused.py" "$SOURCE" "$DEPENDENCY_PYTHON"
rtk proxy python3 "$PACKET/scripts/run_ax.py" "$SOURCE" "$DEPENDENCY_PYTHON"
rtk proxy python3 "$PACKET/scripts/publish_receipts.py" "$SOURCE"
rtk proxy python3 "$PACKET/scripts/verify_tree.py" "$SOURCE"
```

The unchanged public `export_compare.py` and R551-1 regression
`byte_count_underflow.py` have provenance in `receipts/public-evidence.json`.

`run_focused.py` runs eight light checks concurrently with separate logs and
exit-code receipts. Each child has a five-minute timeout. The builder check
invokes only the registered option test. `independent_options.py` changes
source strings in memory and never writes the recipe. It independently
observes both float-parser controls and the unknown-CPU control reaching setup.

`run_ax.py` prepares two detached scratch clones with registered pinned
submodules and an isolated CPU data copy. Configuration campaigns run
concurrently. Each runs baseline then candidate at the same path. Baseline
loads the recipe blob from the original source base; other production inputs
are unchanged by this PR. Equal timestamp and diagnostic ordering inputs
are set before generation. Each population must contain 32 paths with equal
raw bytes. Diagnostic logs are excluded. Software compilation and
implementation are disabled. CPU cache entries can be reused; this is not
a fresh CPU-generator campaign.

All drivers remain in the foreground and join their children. Maximum
campaign concurrency was eight light checks or two exports. No synthesis,
implementation or simulation build ran.

Focused logs need no redaction. Export logs have location-only redactions;
`receipts/log-provenance.json` records original and published digests.
Scratch is excluded from publication. `MANIFEST.sha256` enumerates every
published script and receipt, relative to this packet.
