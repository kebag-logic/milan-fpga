Run from this evidence directory. Replace `<checkout>` with a clean checkout of `b911c11671cae329a99f5e413133b4bf6357fa7f`, with its three required submodules populated. Commands are portable across directories; scripts derive the evidence root from their own location. Python 3, Git 2.39+ and glibc locale tools/data are needed. The public download script additionally uses read-only authenticated `gh` access.

The focused parent-locale reproduction is the shortest way to examine F3:

```sh
rtk proxy python3 -B scripts/check_parent_locale.py <checkout> <new-output-directory> --full
```

Expected at the reviewed head: the previous-head path subset passes 22/22 in UTF-8 and Latin-1; the corrected head passes 22/22 in UTF-8 and 21/22 in Latin-1. The full corrected Latin-1 default run exits 1 with only `retention-literal-revert-'raw-\udcff'-path` failing. The reproduction driver's exit 0 asserts this failure matrix and is not a green source gate. After a correction, update no expectations merely to make the runner green: inspect the individual current-head self-test results and require the original assertions to pass.

The remaining review commands, each run from this evidence directory, are:

```sh
rtk proxy python3 scripts/receipt.py --out raw/selftest --cwd <checkout> -- rtk proxy python3 -B scripts/check_merge_containment.py --selftest
rtk proxy python3 -B scripts/run_public_examples.py <checkout> <new-examples-output>
rtk proxy python3 -B scripts/run_public_matrix.py <checkout> <new-matrix-output>
rtk proxy python3 -B scripts/transport_probe.py <checkout> <new-transport-output>
rtk proxy python3 -B scripts/run_restorations.py <checkout> <new-restoration-output>
rtk proxy python3 -B scripts/reconstruct_history.py <checkout> <new-history-output>
rtk proxy python3 -B scripts/verify_integrity.py <checkout> <new-integrity-json>
```

All these commands exited 0 in this review. The ordinary default self-test had 455 passing assertions. The matrix script also executed the base's 145-assertion self-test and checked their preservation in `raw/selftest.stdout`; run the first command before it. The restoration script expects four disposable mutants to exit 1, so its exit 0 means all four were detected. It uses two concurrent workers. The other test scripts run one fixture/child at a time. No production source is modified.

The original public shell fixture is under `public/review/R244-interrupted/locale_transport_probe.sh`. The example runner changes only its source selector and displayed label, then adds separately named positive controls to the disposable fixture histories. The original fixture's exit alone does not validate its outcomes; the Python runner asserts all eight negative/base results and six corrected positive controls.

The transport probe writes raw Git tree entries and checks native byte argv, including invalid filename bytes. RTK prefixes the outer shell invocations; direct Python subprocess calls to Git supply the byte-level oracle. `raw/transport-initial*` preserves the first failed reviewer-harness attempt, which incorrectly interposed the text wrapper on the invalid-byte oracle. Only `raw/transport/` and `raw/transport-run.*` are the corrected passing execution.

The initial complete Latin-1-parent command is recorded in `raw/parent-latin1-selftest.json`; its disposable locale path no longer exists. The first command above with `check_parent_locale.py --full` creates fresh private locale data and reproduces it. The focused comparison was also executed separately, with raw receipts under `raw/parent-locale-focused/`.

Read-only public evidence collection can be repeated with:

```sh
rtk proxy python3 -B scripts/download_evidence.py
```

It uses the archived immutable `raw/evidence-tree.json`, fetches selected blobs by exact OID, verifies their Git hashes and records SHA-256. It does not query any Actions/run/check endpoint. Public full-bank receipts are inspected evidence; none of these reproduction commands reruns a full parent/processor/Yosys/builder bank or executes act/the candidate act runner.
