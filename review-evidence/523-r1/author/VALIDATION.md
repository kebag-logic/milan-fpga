# Author validation receipts

Exact source head: `b5ce20eca8b59709ec5bc6115e5e15bfc312f283`. Tree: `bfde1313250ae84105754af4b150325f55f5ef33`. Base: `483a133ed08867ea0d300d2b4a027b5b48a4282f`.

Every receipt records argv, cwd, relevant environment, start/end time, exit status, source head/tree/status/index and unfiltered output. Fixture logs retain handshake identities and verdicts. `run_receipt.py` reproduces this collection. `focused_gates.py final` is the sequential focused bank; choose a fresh label for reruns.

The complete real command was:

```sh
env VERILATOR=$VALIDATION_STORAGE/372-manager-candidate1/pinned-tool-bin/verilator VERILATOR_JOBS=8 make -C tb/verilator/gptp_shadow
```

Exit 0; 257.192 seconds; 309 PASS, 0 FAIL; nine mutation detections, zero campaign failures; six unchanged not-observable notes. The selector and underlying script/binary identities are in `tool-identity.json`; version is exactly 5.050. No shared tool was changed.

| Receipt | Exact command | Exit |
|---|---|---|
| `final-baremetal` | `python3 scripts/check_baremetal_only.py --check` | 0 |
| `final-baremetal-selftest` | `python3 scripts/check_baremetal_only.py --selftest` | 0 |
| `final-contents` | `python3 scripts/gen_toc.py --check` | 0 |
| `final-contents-anchors` | `python3 scripts/gen_toc.py --verify-anchors` | 0 |
| `final-doc-paths` | `python3 scripts/check_doc_paths.py` | 0 |
| `final-doc-style` | `python3 scripts/check_doc_style.py` | 0 |
| `final-doc-style-selftest` | `python3 scripts/check_doc_style.py --selftest` | 0 |
| `final-docs` | `python3 scripts/docs_check.py` | 0 |
| `final-em-dash` | `python3 scripts/check_em_dash.py --base 483a133ed08867ea0d300d2b4a027b5b48a4282f` | 0 |
| `final-evidence` | `python3 scripts/measure_test_evidence.py --check` | 0 |
| `final-evidence-selftest` | `python3 scripts/measure_test_evidence.py --selftest` | 0 |
| `final-fail-fast` | `python3 scripts/measure_fail_fast.py --check` | 0 |
| `final-fail-fast-selftest` | `python3 scripts/measure_fail_fast.py --selftest` | 0 |
| `final-gptp-docs` | `python3 scripts/check_gptp_docs.py --with-submodule` | 0 |
| `final-gptp-docs-selftest` | `python3 scripts/check_gptp_docs.py --selftest` | 0 |
| `final-mutation-lifecycle` | `python3 tb/verilator/gptp_shadow/test_mutant_lifecycle.py` | 0 |
| `final-populations` | `python3 $WORKSPACE_HOME/milan-fpga-management/2026-09-22/523-author/populations.py` | 0 |
| `final-process-budget` | `python3 $WORKSPACE_HOME/milan-fpga-management/2026-09-22/523-author/process_budget_receipt.py` | 0 |
| `final-python-idiom` | `python3 scripts/check_py_idiom.py` | 0 |
| `final-python-idiom-selftest` | `python3 scripts/check_py_idiom.py --selftest` | 0 |
| `final-shards-selftest` | `python3 scripts/suite_shards.py --selftest` | 0 |
| `final-shell-idiom` | `python3 scripts/check_sh_idiom.py` | 0 |
| `final-shell-idiom-selftest` | `python3 scripts/check_sh_idiom.py --selftest` | 0 |
| `final-shell-syntax` | `bash -n scripts/run_all_suites.sh` | 0 |
| `final-sweep-cancellation` | `python3 scripts/test_suite_cancellation.py` | 0 |
| `final-tally-count` | `python3 scripts/suite_tally.py $WORKSPACE_HOME/milan-fpga-management/2026-09-22/523-author/machine-tally --quiet` | 0 |
| `final-tally-selftest` | `python3 scripts/suite_tally.py --selftest` | 0 |
| `final-tally-verdict` | `python3 scripts/suite_tally.py --verdict $WORKSPACE_HOME/milan-fpga-management/2026-09-22/523-author/machine-tally/gptp_shadow.log` | 0 |

The actual full output also passes `suite_tally.py --verdict`, and the normal tally reads exactly `checks: 309   in-suite failures: 0`. No lifecycle fixture adds synthetic checks to the real machine tally.

`final-before.json` and `final-after.json` are exactly equal: all 860 parent tracked entries and all 539 files across three pins retain bytes, kinds, full filesystem modes and index records/flags. Both mutation-table ASTs match the base. `integrity.py` reproduces those checks without Git writes. Generated ignored build artifacts are not source inputs.

Failed probes remain under `receipts/` and `failed-probes/`; their failed exits are not counted above. Public original evidence is retained under `original-public/`. Its published SHA256SUMS has six mismatches, recorded in `public-evidence-verification.json`; all 22 downloaded readiness files match their exact public Git blob IDs. See `published-manifest-verdict.log` and the public issue provenance note.
