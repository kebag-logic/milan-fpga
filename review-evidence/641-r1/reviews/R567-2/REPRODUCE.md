Review receipts are for head `614b4aa5f408d75673b546ce6efb6ef126437be2`.
Use a detached checkout with its three required submodules initialized.
Set `REPO` to that checkout and `PACKET` to this packet directory.
Set `MD_PYTHON` to the interpreter with the repository's pinned Markdown dependencies.
Use the assigned pinned 5.050 executable for the filter probe.

Run the foreground groups in order, waiting for each command to return:

```sh
python3 "$PACKET/scripts/audit_tree.py" "$REPO"
python3 "$PACKET/scripts/run_group.py" "$REPO" "$PACKET" "$PACKET/scripts/group1.json"
python3 "$PACKET/scripts/run_group.py" "$REPO" "$PACKET" "$PACKET/scripts/group2.json"
python3 "$PACKET/scripts/run_group.py" "$REPO" "$PACKET" "$PACKET/scripts/group3.json"
python3 "$PACKET/scripts/run_group.py" "$REPO" "$PACKET" "$PACKET/scripts/group4.json"
python3 "$PACKET/scripts/filter_guards.py" --repo "$REPO" --work "$PACKET/scratch/filter-guards" --verilator "$VERILATOR"
python3 "$PACKET/scripts/claim_scan.py" "$REPO"
python3 "$PACKET/scripts/audit_tree.py" "$REPO"
```

The groups run independent commands concurrently and wait for their exits.
The two shape self-tests inside group 4 run serially because they plant into the same checkout.
Group 1 downloads and builds Make 4.3 entirely under scratch, using `make -j16`.
Group 4 downloads and verifies converter 0.0.12 under scratch; converter 0.0.13 must be on PATH.
No shared install is performed. Detailed lint intermediates stay under scratch.

`fixture_custody.py` takes `--repo`, `--work`, and `--evidence`; the latter points to the public author measurement JSON files from the commit linked in REPORT.md. It generates only disposable image fixtures and compares them with the recorded traces.

The hosted snapshot/artifact scripts use read-only repository API calls. `audit_hosted_records.py REPO PACKET` checks the retained records against the source inventory without running synthesis.

Original failed review-driver receipts are retained: combined CI options were invalid, and the initial native diagnostic assertion expected the converted form. Corrected scripts are supplied; `group2-results.json` and `group5-results.json` record the successful replays. An expected illegal guard has exit 1; its enclosing control script requires that exit and returns 0.

Receipt paths are normalized to `$REPO`, `$PACKET`, and `$TOOLS`. No substantive output or result was removed from local test logs. Hosted log excerpts retain checkout/result lines; the complete published result artifacts are included separately. Scratch is not published.
