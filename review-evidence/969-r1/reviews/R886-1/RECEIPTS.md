R886-1 receipt guide

REPORT.md contains the verdict, findings and reviewer-owned ledger. MANIFEST.sha256 is the publication allowlist. Paths in that manifest are relative to this packet. Verify it from the packet directory with `sha256sum -c MANIFEST.sha256`.

The raw test receipts retain assertion text, counts, outcomes and exit codes. Only local path prefixes are replaced: `<checkout>` is the detached review clone, `<packet>` is this evidence directory, `<home>` is the local home prefix and `<tools>` is the local dependency directory. The unredacted originals are confined to unpublished scratch. A base failure is expected; a head probe failure is finding F1.

Use the portable drivers with paths of your choice:

```sh
python3 run_focused.py CHECKOUT PACKET
python3 run_probes.py CHECKOUT PACKET
python3 run_plants.py CHECKOUT PACKET
python3 run_small_gates.py CHECKOUT PACKET --litex-python LITEX_PYTHON --markdown-python MARKDOWN_PYTHON
python3 verify_tree.py CHECKOUT
```

Run drivers sequentially relative to one another. Independent arms inside a driver run concurrently and are joined before it exits. `run_focused.py` prepares the base-adapter copy consumed by `run_probes.py`. Head tests use the checked-out sources. The probe driver records each executable's status in its `.rc` file and in probe-results.json; its own orchestration exit is not a test verdict. Each plant's log is in plant-logs, with per-configuration outcomes in plants-results.json. The small-gate receipt commands identify the exact graders, memory test and documentation checks that ran; the wrapper supplies their required interpreters explicitly.

evidence-download-verification.txt records checksums of all 58 files in the author's immutable packet. published-gate-extracts.txt contains selected results from that packet, not new reviewer executions. hosted-snapshot.json contains only a point-in-time hosted status observation. The public discovery snapshots retained outside the manifest are not publication artifacts.

package_receipts.py applies the path substitutions and regenerates the manifest. It never selects scratch. Reproduction changes receipts; regenerate their manifest after any rerun.
