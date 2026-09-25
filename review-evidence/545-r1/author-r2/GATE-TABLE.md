# All gate attempts

| Name | Exit | Seconds | Command |
|---|---|---|---|
| unit-new | 0 | 5.284 | `taskset -c 10,11 make -C tb/verilator/mmcm_servo unit-build` |
| test-evidence | 0 | 5.373 | `python3 scripts/measure_test_evidence.py --check` |
| unit-run | 0 | 42.808 | `taskset -c 10,11 tb/verilator/mmcm_servo/obj_dir/Vservo_sim` |
| gmstep | 0 | 49.517 | `taskset -c 12-15 make -C tb/verilator/milan_dp gmstep` |
| ooc-head | 0 | 5.477 | `env OOC_TMP=/tmp/a305-ooc-head taskset -c 12-15 bash syn/yosys/ooc.sh KL_mmcm_drp_servo` |
| r301-tail | 0 | 10.037 | `env REPO=$LANES/545-crf-servo-slew PKT=/tmp/a305-probes/r301 VERILATOR=/usr/bin/verilator taskset -c 12-15 bash /tmp/a305-probes/r301-scripts/tail_probe/run.sh` |
| ooc-base | 0 | 4.327 | `env OOC_TMP=/tmp/a305-ooc-base taskset -c 12-15 bash /tmp/a305-area/base-ooc.sh KL_mmcm_drp_servo` |
| ooc-alignment | 1 | 0.465 | `env OOC_TMP=/tmp/a305-ooc-alignment taskset -c 12-15 bash /tmp/a305-area/alignment-ooc.sh KL_slew_alignment` |
| r300-latency-4-build | 0 | 4.524 | `verilator --cc --exe --build -j 2 -Wno-fatal -Wno-lint -Wno-UNUSEDSIGNAL --top-module latency_wrap -Mdir /tmp/a305-probes/r300-latency/4/obj $LANES/545-crf-servo-slew/hdl/ieee8021as/ptp_timestamp/ptp_csr_sync.sv $LANES/545-crf-servo-slew/hdl/ieee8021as/ptp_timestamp/timestamp_counter.sv /tmp/a305-probes/r300-latency/4/latency_wrap.sv /tmp/a305-evidence/review-evidence/545-r1/reviews/R300-1/scripts/latency_probe/sim_latency.cpp -o Vlat` |
| r300-latency-4 | 0 | 0.004 | `/tmp/a305-probes/r300-latency/4/obj/Vlat` |
| r300-latency-3-build | 0 | 4.677 | `verilator --cc --exe --build -j 2 -Wno-fatal -Wno-lint -Wno-UNUSEDSIGNAL --top-module latency_wrap -Mdir /tmp/a305-probes/r300-latency/3/obj $LANES/545-crf-servo-slew/hdl/ieee8021as/ptp_timestamp/ptp_csr_sync.sv $LANES/545-crf-servo-slew/hdl/ieee8021as/ptp_timestamp/timestamp_counter.sv /tmp/a305-probes/r300-latency/3/latency_wrap.sv /tmp/a305-evidence/review-evidence/545-r1/reviews/R300-1/scripts/latency_probe/sim_latency.cpp -o Vlat` |
| r300-latency-3 | 1 | 0.004 | `/tmp/a305-probes/r300-latency/3/obj/Vlat` |
| r300-latency-2-build | 0 | 4.526 | `verilator --cc --exe --build -j 2 -Wno-fatal -Wno-lint -Wno-UNUSEDSIGNAL --top-module latency_wrap -Mdir /tmp/a305-probes/r300-latency/2/obj $LANES/545-crf-servo-slew/hdl/ieee8021as/ptp_timestamp/ptp_csr_sync.sv $LANES/545-crf-servo-slew/hdl/ieee8021as/ptp_timestamp/timestamp_counter.sv /tmp/a305-probes/r300-latency/2/latency_wrap.sv /tmp/a305-evidence/review-evidence/545-r1/reviews/R300-1/scripts/latency_probe/sim_latency.cpp -o Vlat` |
| r300-latency-2 | 1 | 0.004 | `/tmp/a305-probes/r300-latency/2/obj/Vlat` |
| ooc-alignment-final | 0 | 2.674 | `env OOC_TMP=/tmp/a305-ooc-alignment-final taskset -c 12-15 bash /tmp/a305-area/alignment-ooc.sh KL_slew_alignment` |
| timing-base | 0 | 516.943 | `taskset -c 8,9 make -C /tmp/a305-timing/base/tb/verilator/mmcm_servo` |
| docs-no-git | 1 | 6.077 | `python3 /tmp/a305-docs-no-git/scripts/docs_check.py` |
| r300-step-dedupe-unit | 0 | 71.129 | `taskset -c 12-15 python3 /tmp/a305-evidence/review-evidence/545-r1/reviews/R300-1/scripts/reviewer_mutants.py $LANES/545-crf-servo-slew /tmp/a305-probes/r300-mutants step_dedupe_removed_unit /usr/bin/verilator` |
| docs-no-git-final | 0 | 8.177 | `python3 /tmp/a305-docs-no-git/scripts/docs_check.py` |
| test-evidence-final | 0 | 5.83 | `python3 scripts/measure_test_evidence.py --check` |
| datapath-sweep-00-05 | 0 | 314.424 | `taskset -c 12-15 python3 /tmp/a305-sweep.py 0 5` |
| builder | 0 | 582.767 | `python3 sw/builder/test_builder.py` |
| docs | 0 | 4.176 | `python3 scripts/docs_check.py` |
| doc-style | 0 | 0.065 | `python3 scripts/check_doc_style.py` |
| toc | 2 | 0.115 | `python3 scripts/gen_toc.py --check` |
| anchors | 2 | 0.114 | `python3 scripts/gen_toc.py --verify-anchors` |
| doc-paths | 0 | 0.114 | `python3 scripts/check_doc_paths.py` |
| matrix | 0 | 0.967 | `python3 docs/traceability/gen_module_matrix.py --check` |
| r301-coincide | 0 | 422.349 | `env PKT=/tmp/a305-probes/r301 VERILATOR=/usr/bin/verilator taskset -c 12-15 python3 /tmp/a305-probes/r301-scripts/coincide_probe.py` |
| toc-final | 0 | 2.623 | `env PYTHONPATH=/tmp/a305-markdown-deps python3 scripts/gen_toc.py --check` |
| anchors-final | 0 | 1.67 | `env PYTHONPATH=/tmp/a305-markdown-deps python3 scripts/gen_toc.py --verify-anchors` |
| gptp-shadow | 0 | 511.891 | `taskset -c 12-15 make -C tb/verilator/gptp_shadow -j8` |
| xvlog | 0 | 240.432 | `python3 scripts/xvlog_gate.py --check` |
| source-lists | 0 | 1.317 | `python3 scripts/check_rtl_source_lists.py` |
| sv-idiom | 0 | 0.416 | `python3 scripts/check_sv_idiom.py` |
| lint | 0 | 14.834 | `python3 scripts/lint_rtl.py --check` |
| cpp-idiom | 0 | 2.326 | `python3 scripts/check_cpp_idiom.py` |
| py-idiom | 0 | 9.181 | `python3 scripts/check_py_idiom.py` |
| ports | 0 | 4.423 | `python3 scripts/check_port_contracts.py` |
| naming | 0 | 0.466 | `python3 scripts/measure_naming.py --check` |
| behave | 0 | 1.17 | `bash -c 'cd tests && behave --no-capture -f plain'` |
| diff | 0 | 0.035 | `git diff --check` |
| datapath-sweep-05-20 | 0 | 405.076 | `taskset -c 12-15 python3 /tmp/a305-sweep.py 5 20` |
| r300-step-dedupe-suite | 0 | 686.706 | `taskset -c 12-15 python3 /tmp/a305-evidence/review-evidence/545-r1/reviews/R300-1/scripts/reviewer_mutants.py $LANES/545-crf-servo-slew /tmp/a305-probes/r300-mutants step_dedupe_removed_suite /usr/bin/verilator` |
| crf-rx | 0 | 791.913 | `taskset -c 10,11 make -C tb/verilator/crf_rx` |
| gmstep-mutants | 0 | 1088.758 | `taskset -c 12-15 make -C tb/verilator/milan_dp gmstep-mutants` |
| slew-mutants | 0 | 1142.751 | `taskset -c 10,11 make -C tb/verilator/mmcm_servo slew-mutants` |
| servo-clean | 0 | 0.016 | `taskset -c 10,11 make -C tb/verilator/mmcm_servo clean` |
| datapath-sweep-20-31 | 0 | 596.22 | `taskset -c 12-15 python3 /tmp/a305-sweep.py 20 31` |
| datapath-sweep-31-33 | 0 | 573.356 | `taskset -c 12-15 python3 /tmp/a305-sweep.py 31 33` |
| cpp-idiom-final | 0 | 1.166 | `python3 scripts/check_cpp_idiom.py` |
| gmstep-final | 0 | 50.567 | `taskset -c 12-15 make -C tb/verilator/milan_dp gmstep` |
| timing-round1 | 0 | 1652.793 | `taskset -c 8,9 make -C /tmp/a305-timing/round1/tb/verilator/mmcm_servo` |
| timing-round2 | 0 | 952.797 | `taskset -c 10,11 make -C tb/verilator/mmcm_servo` |
| em-dash | 0 | 3.023 | `env PYTHONPATH=/tmp/a305-markdown-deps python3 scripts/check_em_dash.py --base 5b73d3f47dfed519eb988c13d6beb1db664ef1e0` |
| docs-final | 0 | 4.121 | `python3 scripts/docs_check.py` |
| docs-no-git-head | 0 | 4.223 | `python3 /tmp/a305-docs-no-git/scripts/docs_check.py` |
| diff-final | 0 | 0.032 | `git diff --check` |
| gmstep-mutants-final | 0 | 712.353 | `taskset -c 12-15 make -C tb/verilator/milan_dp gmstep-mutants` |
| datapath-sweep-final-08 | 0 | 30.37 | `taskset -c 12-15 python3 /tmp/a305-sweep.py 8 9` |
| datapath-sweep-final-32 | 0 | 183.412 | `taskset -c 12-15 python3 /tmp/a305-sweep.py 32 33` |
