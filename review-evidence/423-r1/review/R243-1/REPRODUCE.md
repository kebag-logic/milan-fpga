# R243-1 reproduction

Use the exact source checkout `df53dfa116b34816db0193230ad9833e67bf46dd` at `$VALIDATION_STORAGE/reviews/r243-423-r1`, with the three required submodules initialized to their recorded pins. Git 2.55.0 and Python were used. These scripts do not run hardware, CI/act, or full native/build gates.

Scripts locate their output directory from their own file. Run `matrix_review.py` in a fresh copy of this packet without `matrix-repos/`; it creates deterministic disposable fixture repositories and refuses to overwrite existing scenario directories. The original public `public-fixtures/fixtures.py` and `fixture-matrix.json` must remain beside it. Keep `public-history-data.json` for `public_retention.py`. `download_evidence.py` needs read-only public GitHub access through gh. Other history/control runs are offline except `public_history.py`, which additionally observes the public donor main with ls-remote.

Representative commands from the source checkout (all output goes to the management packet or disposable scratch):

```sh
rtk proxy python3 -B scripts/check_merge_containment.py --selftest
rtk proxy python3 -B $WORKSPACE_HOME/milan-fpga-management/2026-09-22/423-r1-r243/baseline/check_merge_containment.py --selftest
rtk proxy python3 -B $WORKSPACE_HOME/milan-fpga-management/2026-09-22/423-r1-r243/matrix_review.py
rtk proxy python3 -B $WORKSPACE_HOME/milan-fpga-management/2026-09-22/423-r1-r243/independent_histories.py
rtk proxy python3 -B $WORKSPACE_HOME/milan-fpga-management/2026-09-22/423-r1-r243/alignment_review.py
rtk proxy python3 -B $WORKSPACE_HOME/milan-fpga-management/2026-09-22/423-r1-r243/public_history.py
rtk proxy python3 -B $WORKSPACE_HOME/milan-fpga-management/2026-09-22/423-r1-r243/public_retention.py
rtk proxy python3 -B $WORKSPACE_HOME/milan-fpga-management/2026-09-22/423-r1-r243/source_integrity.py final
```

All expect exit 0. The history scripts assert the expected contained/STRANDED/UNKNOWN verdict and corresponding CLI exit; UNKNOWN/1 inside an expected refusal case is successful verification, not containment. The matrix script additionally asserts ten exact mutant change sets. The alignment script tests 1,920 bounded raw merges and does not claim general proof.

`run_receipt.py` wraps an rtk-prefixed command, recording stdout/stderr and JSON command/cwd/status/time/hash receipts. Supply a fresh run name to preserve existing measurements. For example:

```sh
rtk proxy python3 $WORKSPACE_HOME/milan-fpga-management/2026-09-22/423-r1-r243/run_receipt.py reproduced-selftest -- rtk proxy python3 -B scripts/check_merge_containment.py --selftest
```

For publication, retain original and path-neutralized identities separately. Public manager evidence retains its own executor/source identities; it is not reviewer-run evidence. Raw conflict-marker labels include temporary paths and therefore can differ across runs; statuses and exact-tip comparisons are the assertions.
