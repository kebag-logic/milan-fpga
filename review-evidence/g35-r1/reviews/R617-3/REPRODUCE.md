Run from a fresh detached source clone at `49b9d0fdab9956d5294e60a07bbb8dfb9a23a78c` containing both parents and base `5dce647ab5a01a6ecff9a982b22e3a4a1d946d3d`. The source clone is read-only throughout these scripts. Set `REPO` to its path and `PACKET` to this packet. The simulation compiler argument must identify version 5.050; its version and SHA-256 are recorded before use.

```sh
python3 "$PACKET/audit_merge.py" "$REPO"
python3 "$PACKET/audit_citations.py" "$REPO"
python3 "$PACKET/run_focused.py" "$REPO" --compiler /path/to/pinned/verilator --jobs 4
```

`audit_merge.py` computes each three-way file result with `git merge-file -p` only when both parent blobs changed. It creates no commit, branch, index entry or worktree merge. It compares every path/mode/blob against the published head and verifies the two declared conflict resolutions exactly. It also hashes every tracked worktree blob and compares every index entry, checks nested gitlinks and verifies unchanged parser/test and receive-contract content.

`audit_citations.py` uses the included `authority/` copies from parent `ac2c5e77bba1c0ae20ce2f69f711a1d17ead94a5`. All 31 pinned citation occurrences and 14 distinct targets are checked, together with the retained gap links. Semantic checks are recorded in REPORT.md. These files were read from that commit's public contents API. Public URLs are present in the source documentation and citations receipt.

`run_focused.py` requires a fresh `scratch/source` destination; choose a new packet output with `--packet` for another run. It exports the exact source tree under scratch, runs `make -j16 docs`, the contract check, and OOC precheck/selftest concurrently with the parser suite and mutation builds. Each compiler process uses four build jobs; at most two such builds overlap. All foreground child processes and futures are joined. Every child writes a separate log and return-code file. No full engine/parent/builder bank, synthesis run, hardware operation or detached job is started.

The mutation runner imports the unchanged committed definitions and verdict function. It replaces build/run plumbing only to cap concurrency and retain raw outputs. Every mutation pattern must match once. A build failure never counts as a caught mutant. The clean runtime must return 0; all eight defective runtimes must return 1 and fail every assigned check name. `mutations.rc` and `focused.rc` must return 0. The expected clean suite total is 337; the mutation ledger total is 9.

`collect_public.py` reads public author receipts at evidence commit `3e8c823acbb589151b5ccfd53f1399a89f4fa6ae`, verifies their published SHA-256 values and collects source-head hosted metadata and pinned parent gitlinks. It requires an authenticated read-capable `gh` session. It makes no GitHub write and does not download reviewer reports. Running it later refreshes time-sensitive hosted metadata; the bundled snapshot is the one assessed in REPORT.md.

`INDEPENDENT_VERDICT.md` records the verdict and ledger written before prior review comments were opened. The final report reconciles those findings without republishing the other reviewers' reports.

Only files in `MANIFEST.sha256` and REPORT.md are publication inputs. Scratch exports, object files, copied mutant sources, cached API payloads, and other unlisted files are excluded. Validate the published subset with `sha256sum -c MANIFEST.sha256` from the packet root.
