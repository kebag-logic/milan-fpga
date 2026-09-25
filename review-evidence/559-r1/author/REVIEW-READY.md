[A307] REVIEW READY

Commit: `32076148acb0b9122e8c92a44f8e2ebbc8169280` (local, unpublished; branch `559-capture-copy`).

Changed: runnable product-CPU capture harness and full measurement receipt; snapshot-ownership section 18 and UNRESOLVED 6 now use measurements instead of the cost model. No product firmware, RTL, hold parameter or builder census list changed.

Measurement: 16 full closed-record captures at each shape under continuous READ_DESCRIPTOR ENTITY traffic at the MAC AXIS boundary. Firmware brackets ARM through successful ATTEST, including ownership reads, `nvm_rec_after()`, byte copy and fence. Every capture passes byte equality, attestation, closed ownership, successful controller responses and shared-memory read activity during the copy.

| Shape | Raw bytes / records | CPU/system MHz | Worst ms | 50 ms hold margin |
|---|---|---|---|---|
| 8x8 | 12,634 / 156 | 100/100 | 19.00433 | 2.6310x |
| 1x1 | 3,218 / 53 | 50/100 | 6.55479 | 7.6280x |

Acceptance: the 8x8 maximum is below 25 ms. The first assigned remedy applies: 50 ms is enough under the specified simulation route. All 32 rows and input hashes are in `tb/verilator/nvm_capture_cpu/measurements.json`; commands are in its adjacent README. Both missing-copy and missing-traffic negative controls are detected.

Validation: full builder with the pinned compiler and without a compiler; `make -C tb/verilator/nvm_cosim` (465 PASS, 39/39 mutants); `make -C tb/verilator/nvm_backend`; `python3 sw/firmware/nvm_hosttest/test_nvm_firmware.py --self-test`; all requested baremetal, documentation, style, Contents/anchor, path, module-matrix, parser, idiom, port-contract, naming, evidence and diff gates return 0. The compiler-present census ran; the compiler-absent census intentionally stands down. Both builder modes report the historical placement calibration arm NOT RUN because its report is absent. OOC is inapplicable without a product RTL change.

Exact gate commands below (all rc 0). The full builder additionally ran through the prescribed compiler argv mapping with `--require-rv32`, and through a wrapper hiding only its three compiler candidates in default mode. Both execute `sw/builder/test_builder.py` unchanged. Documentation renderer dependencies are the repository's locked versions.

```sh
make -C tb/verilator/nvm_cosim
make -C tb/verilator/nvm_backend
python3 sw/firmware/nvm_hosttest/test_nvm_firmware.py --self-test
python3 scripts/check_baremetal_only.py --check
python3 -B scripts/docs_check.py
env GIT_DIR=/dev/null python3 -B scripts/docs_check.py
python3 scripts/check_em_dash.py --base a3d795ae24202bb00cfa7ba0f5bfb4fffc1eb8e4
python3 scripts/check_doc_style.py
python3 scripts/gen_toc.py --check
python3 scripts/gen_toc.py --verify-anchors
python3 scripts/check_doc_paths.py
python3 docs/traceability/gen_module_matrix.py --check
python3 scripts/xvlog_gate.py --check
python3 scripts/check_sv_idiom.py
python3 scripts/check_cpp_idiom.py
python3 scripts/check_py_idiom.py
python3 scripts/check_port_contracts.py
python3 scripts/measure_naming.py --check
python3 scripts/measure_test_evidence.py --check
git diff --check
git diff --cached --check
```

Limits: simulated physical devices and MAC-boundary traffic; this does not close silicon timing, physical memory-ordering or debounce claims. Independent review and hosted checks remain. HANDOFF.md and PR-BODY.md are in the assigned output directory. No push or PR mutation was performed.
