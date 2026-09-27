# Completed round-2 resume gates

Candidate: `5d4cf33e3709c35d4f5bc90d3c5a2334ef3bfd8e`.

Every final gate below returned zero. Commands ran in the foreground without pipelines, with a 43,200-second outer timeout. The candidate snapshot measured before commit is byte-identical to this head; the full default sweep and builder runs started after the commit. Reviewer commands use a verified Git-free export. Prior receipt history remains in `pre-resume-completed-gates.json`.

| Gate | Exit | Seconds | Command |
|---|---:|---:|---|
| pp-shadow-default | 0 | 72.4 | `make -C tb/verilator/pp_shadow` |
| pending-mutant | 0 | 25.9 | `make -C tb/verilator/pp_shadow pending-mutant` |
| default-sweep | 0 | 4493.3 | `bash scripts/run_all_suites.sh /tmp/502-a345/sweep` |
| builder-present | 0 | 662.9 | `$WORKSPACE_HOME/litex-milan/venv/bin/python3 sw/builder/test_builder.py --require-rv32 --require-elaboration` |
| builder-absent | 0 | 461.3 | `$WORKSPACE_HOME/litex-milan/venv/bin/python3 -u /tmp/502-a345/full-builder-absent.py` |
| lint | 0 | 4.1 | `python3 scripts/lint_rtl.py --check` |
| ports | 0 | 2.3 | `python3 scripts/check_port_contracts.py` |
| naming | 0 | 0.5 | `python3 scripts/measure_naming.py --check` |
| test-evidence | 0 | 5.3 | `python3 scripts/measure_test_evidence.py --check` |
| docs | 0 | 4.2 | `python3 scripts/docs_check.py` |
| docs-no-git | 0 | 4.2 | `env GIT_DIR=/dev/null python3 scripts/docs_check.py` |
| em-dash-final | 0 | 3.0 | `python3 scripts/check_em_dash.py --base 831f94f4` |
| doc-style | 0 | 0.1 | `python3 scripts/check_doc_style.py` |
| toc | 0 | 2.5 | `python3 scripts/gen_toc.py --check` |
| anchors | 0 | 1.6 | `python3 scripts/gen_toc.py --verify-anchors` |
| doc-paths | 0 | 0.1 | `python3 scripts/check_doc_paths.py` |
| nvm-capture | 0 | 0.7 | `python3 scripts/check_nvm_capture.py` |
| area-original | 0 | 514.8 | `env OOC_TMP=/tmp/502-a345/area-original-results bash /tmp/502-a345/area-original/ooc.sh KL_pp_shadow milan_datapath` |
| area-minimal | 0 | 513.3 | `env OOC_TMP=/tmp/502-a345/area-minimal-results bash syn/yosys/ooc.sh KL_pp_shadow milan_datapath` |
| diff-check-final | 0 | 0.0 | `git diff --check 831f94f4 HEAD` |
| sv-idiom | 0 | 0.4 | `python3 scripts/check_sv_idiom.py` |
| cpp-idiom | 0 | 1.2 | `python3 scripts/check_cpp_idiom.py` |
| py-idiom | 0 | 3.2 | `python3 scripts/check_py_idiom.py` |
| wire-accountability | 0 | 0.2 | `python3 scripts/check_wire_accountability.py` |
| r329-unchanged | 0 | 74.2 | `python3 /tmp/502-a345/r329_mutants.py /tmp/502-a345/export /tmp/502-a345/r329-unchanged` |
| r328-unchanged | 0 | 75.4 | `python3 /tmp/502-a345/reviewer_mutants.py /tmp/502-a345/export /tmp/502-a345/r328-unchanged` |
| r329-probe-unchanged | 0 | 13.2 | `python3 /tmp/502-a345/r329_probe.py /tmp/502-a345/export /tmp/502-a345/r329-probe` |
| r329-reanchored | 0 | 202.2 | `python3 /tmp/502-a345/adapt-reviewers.py /tmp/502-a345/r329_mutants.py /tmp/502-a345/export /tmp/502-a345/r329-reanchored M1_drop_map M2_drop_name M4_wrong_phase_2 M5_early_phase_4 M6_add_only M8_input_ports_only M9_any_phase M10_late_mark` |
| r328-reanchored | 0 | 171.8 | `python3 /tmp/502-a345/adapt-reviewers.py /tmp/502-a345/reviewer_mutants.py /tmp/502-a345/export /tmp/502-a345/r328-reanchored drop_name drop_map phase4_validate phase1_begin_commit phase0_begin phase2_finish map_any_phase` |
| r328-oracle-static | 0 | 11.1 | `make run-base SIM_ARGS=--pending-only BUILD_DIR=/tmp/502-a345/r328-oracle/static CPP=r328_probe_main.cpp` |
| r328-oracle-dynamic | 0 | 12.1 | `make run-pending PENDING_BUILD_DIR=/tmp/502-a345/r328-oracle/dynamic CPP=r328_probe_main.cpp` |
| priority-static | 0 | 12.1 | `make run-base CPP=priority_probe_main.cpp 'VERILATOR=verilator /tmp/502-a345/priority_probes.vlt' SIM_ARGS=--pending-only BUILD_DIR=/tmp/502-a345/priority-static` |
| priority-dynamic | 0 | 13.1 | `make run-pending CPP=priority_probe_main.cpp 'VERILATOR=verilator /tmp/502-a345/priority_probes.vlt' PENDING_BUILD_DIR=/tmp/502-a345/priority-dynamic CXXFLAGS=-DPRIORITY_DYNAMIC=1` |
| minimal-equivalence | 0 | 0.1 | `python3 /tmp/502-a345/verify-minimal.py` |
| reviewer-results-audit | 0 | 0.0 | `python3 /tmp/502-a345/verify-reviewer-results.py` |
| final-tree-integrity | 0 | 0.2 | `python3 /tmp/502-a345/verify-final-tree.py` |
