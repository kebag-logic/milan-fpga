| Command | Exit | Receipt |
|---|---:|---|
| `./ooc.sh --record-rom-digests` | 0 | `record-rom-digests.log` |
| `make -C tb/verilator/mmcm_servo` | 0 | `servo-default-final.log` |
| `make -C tb/verilator/mmcm_servo mutants` | 0 | `servo-slew-mutants.log` |
| `make -C tb/verilator/crf_rx` | 0 | `crf-rx.log` |
| `make -C tb/verilator/gptp_shadow -j8` | 0 | `shadow-final.log` |
| `python3 gmstep_mutants.py --slew` | 0 | `gmstep-slew-mutants.log` |
| `python3 sw/builder/test_builder.py` | 0 | `builder.log` |
| `python3 scripts/docs_check.py` | 0 | `docs-final.log` |
| `python3 scripts/docs_check.py` | 0 | `docs-no-git-final.log` |
| `python3 scripts/check_em_dash.py --base 5b73d3f47dfed519eb988c13d6beb1db664ef1e0` | 0 | `em-dash-final.log` |
| `python3 scripts/check_doc_style.py` | 0 | `doc-style-final.log` |
| `python3 scripts/gen_toc.py --check` | 0 | `toc-final.log` |
| `python3 scripts/gen_toc.py --verify-anchors` | 0 | `anchors-final.log` |
| `python3 scripts/check_doc_paths.py` | 0 | `check_doc_paths.log` |
| `python3 docs/traceability/gen_module_matrix.py --check` | 0 | `static-recheck-4.log` |
| `python3 scripts/xvlog_gate.py --check` | 0 | `xvlog-final.log` |
| `python3 scripts/check_rtl_source_lists.py` | 0 | `check_rtl_source_lists.log` |
| `python3 scripts/check_sv_idiom.py` | 0 | `sv-final.log` |
| `python3 scripts/lint_rtl.py --check` | 0 | `lint-final.log` |
| `python3 scripts/check_cpp_idiom.py` | 0 | `cpp-final.log` |
| `python3 scripts/check_py_idiom.py` | 0 | `py-final.log` |
| `python3 scripts/check_port_contracts.py` | 0 | `check_port_contracts.log` |
| `python3 scripts/measure_naming.py --check` | 0 | `measure_naming.log` |
| `python3 scripts/measure_test_evidence.py --check` | 0 | `static-recheck-3.log` |
| `behave --no-capture -f plain` | 0 | `behave.log` |
| `git diff --check` | 0 | `diff-final.log` |
| `env OOC_TMP=/tmp/545-a303-area-base ./ooc.sh KL_mmcm_drp_servo` | 0 | `area-baseline.log` |
| `env OOC_TMP=/tmp/545-a303-area-servo ./ooc.sh KL_mmcm_drp_servo` | 0 | `area-servo.log` |
| `env OOC_TMP=/tmp/545-a303-area-alignment/results /tmp/545-a303-area-alignment/ooc.sh KL_slew_alignment` | 0 | `area-alignment.log` |
| `make -C tb/verilator/mmcm_servo_autorepair` | 0 | `servo-autorepair.log` |
| `make -C tb/verilator/gptp_txts run` | 0 | `gptp-txts-run.log` |
| Default milan_dp run sweep, exact recipe split into five foreground chunks | 0 for all 33 commands | `sweep-plan.json`, `sweep-results.jsonl`, `sweep-00.log` through `sweep-32.log` |
