# Round 2 gate commands and receipts

Commands below are the executed shell text. Log contents remain outside this packet; each receipt gives their digest and byte size.

## builder 01: builder-elaboration

Head: `342f20ef1fb29167c388b6f1fa3bc9851c3876e3`. GNU Make 4.3. Exit: 0.

Working directory: `$LANES/682-pp-pin3`.

```sh
python3 sw/builder/test_builder.py --require-elaboration --require-rv32
```

Log: `$VALIDATION_STORAGE/682-a554/round2/acceptance/builder/01-builder-elaboration.log`; 101,688 bytes; SHA-256 `36eb3b23894f4b3ad292bfaabbf0af6bede74049daccbd0254531eed69f14665`.

## final-builder 01: builder-elaboration

Head: `591a5752e6a587b28b501e2d02d6a9d0293f3ba2`. GNU Make 4.3. Exit: 0.

Working directory: `$LANES/682-pp-pin3`.

```sh
python3 sw/builder/test_builder.py --require-elaboration --require-rv32
```

Log: `$VALIDATION_STORAGE/682-a554/round2/acceptance/final-builder/01-builder-elaboration.log`; 101,688 bytes; SHA-256 `f930eab0271b64766ced191cc75fec7a3e8a11757da2002f1ef3f6f6fc1319f0`.

## final-contract 01: bdd

Head: `591a5752e6a587b28b501e2d02d6a9d0293f3ba2`. GNU Make 4.3. Exit: 0.

Working directory: `$LANES/682-pp-pin3/tests`.

```sh
behave --no-capture -f plain
```

Log: `$VALIDATION_STORAGE/682-a554/round2/acceptance/final-contract/01-bdd.log`; 196,684 bytes; SHA-256 `51b8b6a7363520d5e0933ee092832fdfd1bed6802eb9d2ef5509e47af77d7a96`.

## final-firmware 01: sdk-controls

Head: `591a5752e6a587b28b501e2d02d6a9d0293f3ba2`. GNU Make 4.3. Exit: 0.

Working directory: `$LANES/682-pp-pin3`.

```sh
python3 scripts/ci_rv32_sdk_selftest.py
```

Log: `$VALIDATION_STORAGE/682-a554/round2/acceptance/final-firmware/01-sdk-controls.log`; 5,759 bytes; SHA-256 `d69908ab906d5da88f8fc979377224d4ed7e6ded54134f407d21ada0bd172840`.

## final-firmware 02: rv32-object-controls

Head: `591a5752e6a587b28b501e2d02d6a9d0293f3ba2`. GNU Make 4.3. Exit: 0.

Working directory: `$LANES/682-pp-pin3`.

```sh
python3 sw/firmware/gtest/fw_rv32_selftest.py --require-rv32
```

Log: `$VALIDATION_STORAGE/682-a554/round2/acceptance/final-firmware/02-rv32-object-controls.log`; 793 bytes; SHA-256 `9cd3b019b88560e4f902812b20cbb7d859405f50f0e686d6d71b6474287e7c94`.

## final-firmware 03: firmware-tally-controls

Head: `591a5752e6a587b28b501e2d02d6a9d0293f3ba2`. GNU Make 4.3. Exit: 0.

Working directory: `$LANES/682-pp-pin3`.

```sh
python3 sw/firmware/gtest/tally_selftest.py --mutants
```

Log: `$VALIDATION_STORAGE/682-a554/round2/acceptance/final-firmware/03-firmware-tally-controls.log`; 3,982 bytes; SHA-256 `02268c336448885863d0308d88968cde7fe44eedb9743f0589fc01020f7eca11`.

## final-firmware 04: firmware-ctrl

Head: `591a5752e6a587b28b501e2d02d6a9d0293f3ba2`. GNU Make 4.3. Exit: 0.

Working directory: `$LANES/682-pp-pin3`.

```sh
python3 sw/firmware/ctrl/test/test_ctrl_firmware.py --require-rv32 --self-test --lwsrp $VALIDATION_STORAGE/665fc-a555/lwSRP
```

Log: `$VALIDATION_STORAGE/682-a554/round2/acceptance/final-firmware/04-firmware-ctrl.log`; 23,476 bytes; SHA-256 `70820d126ace9848395aef61f50515e1da118ff50ec1b8d35fd0eaefca2dcbd9`.

## final-firmware 05: firmware-nvm

Head: `591a5752e6a587b28b501e2d02d6a9d0293f3ba2`. GNU Make 4.3. Exit: 0.

Working directory: `$LANES/682-pp-pin3`.

```sh
python3 sw/firmware/ctrl_nvm/test/test_ctrl_nvm.py --require-rv32 --self-test --jobs 4
```

Log: `$VALIDATION_STORAGE/682-a554/round2/acceptance/final-firmware/05-firmware-nvm.log`; 23,916 bytes; SHA-256 `aea051a1d34f92741e4ffe7fab6493cb0571302c02eb174026c74242b99fe548`.

## final-firmware 06: firmware-coverage-controls

Head: `591a5752e6a587b28b501e2d02d6a9d0293f3ba2`. GNU Make 4.3. Exit: 0.

Working directory: `$LANES/682-pp-pin3`.

```sh
python3 sw/firmware/gtest/fw_coverage.py --selftest
```

Log: `$VALIDATION_STORAGE/682-a554/round2/acceptance/final-firmware/06-firmware-coverage-controls.log`; 3,710 bytes; SHA-256 `3788b02a1c5d91d7ff2c8581f2ed09040261511d92565dd669103fee911dca0b`.

## final-firmware 07: firmware-coverage

Head: `591a5752e6a587b28b501e2d02d6a9d0293f3ba2`. GNU Make 4.3. Exit: 0.

Working directory: `$LANES/682-pp-pin3`.

```sh
python3 sw/firmware/gtest/fw_coverage.py --check --lwsrp $VALIDATION_STORAGE/665fc-a555/lwSRP --jobs 4
```

Log: `$VALIDATION_STORAGE/682-a554/round2/acceptance/final-firmware/07-firmware-coverage.log`; 2,684 bytes; SHA-256 `befe0d36062c14d49bce4b527247f24a7cf2ad4b47c5d8f7a6f781f457721477`.

## final-markdown 01: markdown-docs

Head: `591a5752e6a587b28b501e2d02d6a9d0293f3ba2`. GNU Make 4.3. Exit: 0.

Working directory: `$LANES/682-pp-pin3`.

```sh
$VALIDATION_TOOLS/md-venv-40cdefe08ebd/bin/python scripts/docs_check.py
```

Log: `$VALIDATION_STORAGE/682-a554/round2/acceptance/final-markdown/01-markdown-docs.log`; 128 bytes; SHA-256 `fc436feec99782d1c4b428f118726d0c38006a1c13747c8dad0e204129beda64`.

## final-markdown 02: markdown-toc-controls

Head: `591a5752e6a587b28b501e2d02d6a9d0293f3ba2`. GNU Make 4.3. Exit: 0.

Working directory: `$LANES/682-pp-pin3`.

```sh
$VALIDATION_TOOLS/md-venv-40cdefe08ebd/bin/python scripts/gen_toc.py --selftest
```

Log: `$VALIDATION_STORAGE/682-a554/round2/acceptance/final-markdown/02-markdown-toc-controls.log`; 38 bytes; SHA-256 `d7fd5f6ebcdd25e6cf93b623b0fba00cfa32d19c812ce34eb6b8d8b352ac9b32`.

## final-markdown 03: markdown-anchor-check

Head: `591a5752e6a587b28b501e2d02d6a9d0293f3ba2`. GNU Make 4.3. Exit: 0.

Working directory: `$LANES/682-pp-pin3`.

```sh
$VALIDATION_TOOLS/md-venv-40cdefe08ebd/bin/python scripts/gen_toc.py --verify-anchors
```

Log: `$VALIDATION_STORAGE/682-a554/round2/acceptance/final-markdown/03-markdown-anchor-check.log`; 64 bytes; SHA-256 `209c26680521fd5191a675649418cddef43b035d2858a8688877c3bd07094c96`.

## final-markdown 04: markdown-toc-check

Head: `591a5752e6a587b28b501e2d02d6a9d0293f3ba2`. GNU Make 4.3. Exit: 0.

Working directory: `$LANES/682-pp-pin3`.

```sh
$VALIDATION_TOOLS/md-venv-40cdefe08ebd/bin/python scripts/gen_toc.py --check
```

Log: `$VALIDATION_STORAGE/682-a554/round2/acceptance/final-markdown/04-markdown-toc-check.log`; 94 bytes; SHA-256 `35e7e86e67b2d3d3968be2ae5107b946549d31bc8426a393fdae86c12f341b47`.

## final-resources 01: route-1x1

Head: `591a5752e6a587b28b501e2d02d6a9d0293f3ba2`. GNU Make 4.3. Exit: 0.

Working directory: `$LANES/682-pp-pin3`.

```sh
python3 syn/ooc/pp_resource_gate.py check $VALIDATION_STORAGE/682-a554/round2/work/ax7101/gateware --endpoint route-1x1
```

Log: `$VALIDATION_STORAGE/682-a554/round2/acceptance/final-resources/01-route-1x1.log`; 593 bytes; SHA-256 `2ca20be2737097c53a7907da0cabb7de63a00c68bd0171d2eea1db82c6949e9c`.

## final-resources 02: ooc-1x1

Head: `591a5752e6a587b28b501e2d02d6a9d0293f3ba2`. GNU Make 4.3. Exit: 0.

Working directory: `$LANES/682-pp-pin3`.

```sh
python3 syn/ooc/pp_resource_gate.py check $VALIDATION_STORAGE/682-a554/round2/work/ax7101-ooc --endpoint ooc-1x1
```

Log: `$VALIDATION_STORAGE/682-a554/round2/acceptance/final-resources/02-ooc-1x1.log`; 378 bytes; SHA-256 `1497ef241c7693598d85d9e76208172f422b40af299db3799d87c0291e09ec3c`.

## final-resources 03: ooc-8x8

Head: `591a5752e6a587b28b501e2d02d6a9d0293f3ba2`. GNU Make 4.3. Exit: 0.

Working directory: `$LANES/682-pp-pin3`.

```sh
python3 syn/ooc/pp_resource_gate.py check $VALIDATION_STORAGE/682-a554/round2/work/ax8x8-ooc --endpoint ooc-8x8
```

Log: `$VALIDATION_STORAGE/682-a554/round2/acceptance/final-resources/03-ooc-8x8.log`; 377 bytes; SHA-256 `085dede82739485596ecdd3b6383ddc7de15cbaa105e91ba821c917ebf89a60a`.

## final-resources 04: resource-policy

Head: `591a5752e6a587b28b501e2d02d6a9d0293f3ba2`. GNU Make 4.3. Exit: 0.

Working directory: `$LANES/682-pp-pin3`.

```sh
python3 syn/ooc/pp_resource_gate.py check-baseline
```

Log: `$VALIDATION_STORAGE/682-a554/round2/acceptance/final-resources/04-resource-policy.log`; 27 bytes; SHA-256 `2114d909e60add091220b415987d4409a611d70c9e84f1bb9e0ae12d6a2f14a0`.

## final-resources 05: capture-receipt

Head: `591a5752e6a587b28b501e2d02d6a9d0293f3ba2`. GNU Make 4.3. Exit: 0.

Working directory: `$LANES/682-pp-pin3`.

```sh
python3 scripts/check_nvm_capture.py
```

Log: `$VALIDATION_STORAGE/682-a554/round2/acceptance/final-resources/05-capture-receipt.log`; 324 bytes; SHA-256 `9a4196c774ce4ddfa9980cf9345d111028f3afa812677fe5bab392f81c955439`.

## final-resources 06: exact-resource-inputs

Head: `591a5752e6a587b28b501e2d02d6a9d0293f3ba2`. GNU Make 4.3. Exit: 0.

Working directory: `$LANES/682-pp-pin3`.

```sh
python3 $VALIDATION_STORAGE/682-a554/round2/verify-record-inputs.py
```

Log: `$VALIDATION_STORAGE/682-a554/round2/acceptance/final-resources/06-exact-resource-inputs.log`; 278 bytes; SHA-256 `b80d5cc237b2a35454d1e8fb166dafcca3fd4bdd41213111744e0aef9db50a06`.

## final-sweep 01: parent-sweep

Head: `591a5752e6a587b28b501e2d02d6a9d0293f3ba2`. GNU Make 4.3. Exit: 0.

Working directory: `$LANES/682-pp-pin3`.

```sh
bash scripts/run_all_suites.sh $VALIDATION_STORAGE/682-a554/round2/final/parent-suite-logs
```

Log: `$VALIDATION_STORAGE/682-a554/round2/acceptance/final-sweep/01-parent-sweep.log`; 1,986 bytes; SHA-256 `6733832edf5eef0081417ef79144772f40371957beea9060dff78991ca092f59`.

## final-sweep 02: parent-tally

Head: `591a5752e6a587b28b501e2d02d6a9d0293f3ba2`. GNU Make 4.3. Exit: 0.

Working directory: `$LANES/682-pp-pin3`.

```sh
python3 scripts/suite_tally.py $VALIDATION_STORAGE/682-a554/round2/final/parent-suite-logs --quiet --expect-suite-root tb/verilator
```

Log: `$VALIDATION_STORAGE/682-a554/round2/acceptance/final-sweep/02-parent-tally.log`; 617 bytes; SHA-256 `0b6abbe752ae9d3cbfaddf18bc01a6532f8df75d7d5a4824d183e349ebd4d8a7`.

## final-synthesis 01: lint

Head: `591a5752e6a587b28b501e2d02d6a9d0293f3ba2`. GNU Make 4.3. Exit: 0.

Working directory: `$LANES/682-pp-pin3`.

```sh
python3 scripts/lint_rtl.py --check --self-test
```

Log: `$VALIDATION_STORAGE/682-a554/round2/acceptance/final-synthesis/01-lint.log`; 14,888 bytes; SHA-256 `fdfaa1c6d9058fd1f1d30ef75e8590d1e633c21b21ff6fb7455e0542dc99123a`.

## final-synthesis 02: pp-sources

Head: `591a5752e6a587b28b501e2d02d6a9d0293f3ba2`. GNU Make 4.3. Exit: 0.

Working directory: `$LANES/682-pp-pin3`.

```sh
python3 scripts/pp_srcs.py --check --selftest
```

Log: `$VALIDATION_STORAGE/682-a554/round2/acceptance/final-synthesis/02-pp-sources.log`; 955 bytes; SHA-256 `fad5e1b9dd5f465b7fcb2334e2abe6c6db44be93b5bb12afb3a35f3ebf432e1a`.

## final-synthesis 03: scope

Head: `591a5752e6a587b28b501e2d02d6a9d0293f3ba2`. GNU Make 4.3. Exit: 0.

Working directory: `$LANES/682-pp-pin3`.

```sh
python3 scripts/ci_scope.py --selftest
```

Log: `$VALIDATION_STORAGE/682-a554/round2/acceptance/final-synthesis/03-scope.log`; 6,877 bytes; SHA-256 `cda2e3e13229332d91d0863932d724a7fdeef280c924f262aa43f5d5448c62da`.

## final-synthesis 04: yosys

Head: `591a5752e6a587b28b501e2d02d6a9d0293f3ba2`. GNU Make 4.3. Exit: 0.

Working directory: `$LANES/682-pp-pin3`.

```sh
bash syn/yosys/run.sh --results $VALIDATION_STORAGE/682-a554/round2/final/yosys-results
```

Log: `$VALIDATION_STORAGE/682-a554/round2/acceptance/final-synthesis/04-yosys.log`; 6,182 bytes; SHA-256 `520ab8a4c74e041db8f7a2de42adea1e472ae20244bf7be9764535a7e4653556`.

## final-synthesis 05: yosys-tally

Head: `591a5752e6a587b28b501e2d02d6a9d0293f3ba2`. GNU Make 4.3. Exit: 0.

Working directory: `$LANES/682-pp-pin3`.

```sh
bash syn/yosys/run.sh --list > $VALIDATION_STORAGE/682-a554/round2/final/yosys-expected.txt
python3 scripts/yosys_tally.py $VALIDATION_STORAGE/682-a554/round2/final/yosys-results --expected $VALIDATION_STORAGE/682-a554/round2/final/yosys-expected.txt --require-structural
```

Log: `$VALIDATION_STORAGE/682-a554/round2/acceptance/final-synthesis/05-yosys-tally.log`; 49 bytes; SHA-256 `ca886fa4ca355ab8ad0ad261ad5d583dc524bc0f89466f52032de7cfc3d667c4`.

## final-synthesis 06: fast-elaboration

Head: `591a5752e6a587b28b501e2d02d6a9d0293f3ba2`. GNU Make 4.3. Exit: 0.

Working directory: `$LANES/682-pp-pin3`.

```sh
bash syn/yosys/run.sh --mode elaborate --no-structural --top milan_datapath --top KL_pp_shadow --top KL_gptp_shadow
```

Log: `$VALIDATION_STORAGE/682-a554/round2/acceptance/final-synthesis/06-fast-elaboration.log`; 369 bytes; SHA-256 `b07aa0caefde92c83defb48336b45d06f106325af111710b39d327e529599073`.

## final-synthesis 07: dp-source-controls

Head: `591a5752e6a587b28b501e2d02d6a9d0293f3ba2`. GNU Make 4.3. Exit: 0.

Working directory: `$LANES/682-pp-pin3`.

```sh
python3 syn/ooc/dp_srcs.py --selftest
```

Log: `$VALIDATION_STORAGE/682-a554/round2/acceptance/final-synthesis/07-dp-source-controls.log`; 36 bytes; SHA-256 `d1d5a4fa150962bc8cd53e563cde50da65cc8cfeee212d82e10bc293848bd428`.

## final-synthesis 08: ooc-tcl-controls

Head: `591a5752e6a587b28b501e2d02d6a9d0293f3ba2`. GNU Make 4.3. Exit: 0.

Working directory: `$LANES/682-pp-pin3`.

```sh
python3 syn/ooc/ooc_tcl_selftest.py
```

Log: `$VALIDATION_STORAGE/682-a554/round2/acceptance/final-synthesis/08-ooc-tcl-controls.log`; 45 bytes; SHA-256 `c8115f5fe4b9eadf2c9d635505578b1b267023a61a32f8aebff7ad568f0b21eb`.

## final-synthesis 09: baseline-controls

Head: `591a5752e6a587b28b501e2d02d6a9d0293f3ba2`. GNU Make 4.3. Exit: 0.

Working directory: `$LANES/682-pp-pin3`.

```sh
python3 syn/ooc/pp_baseline.py --selftest
```

Log: `$VALIDATION_STORAGE/682-a554/round2/acceptance/final-synthesis/09-baseline-controls.log`; 3,552 bytes; SHA-256 `38447b45845c6359701b872e20ef9a967b37fc74bcd2e31f5ec04597663dc2d3`.

## final-synthesis 10: baseline-mutants

Head: `591a5752e6a587b28b501e2d02d6a9d0293f3ba2`. GNU Make 4.3. Exit: 0.

Working directory: `$LANES/682-pp-pin3`.

```sh
python3 syn/ooc/pp_baseline_mutants.py
```

Log: `$VALIDATION_STORAGE/682-a554/round2/acceptance/final-synthesis/10-baseline-mutants.log`; 1,262 bytes; SHA-256 `c61da14188c61f28ddce19916a58bcf07e368851751321f9f498dcc6385d2dc4`.

## final-synthesis 11: baseline-reports

Head: `591a5752e6a587b28b501e2d02d6a9d0293f3ba2`. GNU Make 4.3. Exit: 0.

Working directory: `$LANES/682-pp-pin3`.

```sh
python3 syn/ooc/pp_baseline_reports_selftest.py
```

Log: `$VALIDATION_STORAGE/682-a554/round2/acceptance/final-synthesis/11-baseline-reports.log`; 96 bytes; SHA-256 `e2b4102612b453b76c0af51f99091bbb1e1a36adafecc9f6c6b8eb345bbc81fe`.

## final-synthesis 12: resource-controls

Head: `591a5752e6a587b28b501e2d02d6a9d0293f3ba2`. GNU Make 4.3. Exit: 0.

Working directory: `$LANES/682-pp-pin3`.

```sh
python3 syn/ooc/pp_resource_gate.py --selftest
```

Log: `$VALIDATION_STORAGE/682-a554/round2/acceptance/final-synthesis/12-resource-controls.log`; 25,156 bytes; SHA-256 `160855c6f5d252fde05cf983fe3dd19877501d6587e740deb60fe5ddf7017800`.

## final-synthesis 13: resource-mutants

Head: `591a5752e6a587b28b501e2d02d6a9d0293f3ba2`. GNU Make 4.3. Exit: 0.

Working directory: `$LANES/682-pp-pin3`.

```sh
python3 syn/ooc/pp_resource_gate_mutants.py
```

Log: `$VALIDATION_STORAGE/682-a554/round2/acceptance/final-synthesis/13-resource-mutants.log`; 5,862 bytes; SHA-256 `e566898c471e0694e1e7c16accc1c1e30b6b7187dbf9b3282829a8dfd3e4fdf4`.

## final-synthesis 14: resource-baseline

Head: `591a5752e6a587b28b501e2d02d6a9d0293f3ba2`. GNU Make 4.3. Exit: 0.

Working directory: `$LANES/682-pp-pin3`.

```sh
python3 syn/ooc/pp_resource_gate.py check-baseline
```

Log: `$VALIDATION_STORAGE/682-a554/round2/acceptance/final-synthesis/14-resource-baseline.log`; 27 bytes; SHA-256 `2114d909e60add091220b415987d4409a611d70c9e84f1bb9e0ae12d6a2f14a0`.

## final-synthesis 15: dp-sources

Head: `591a5752e6a587b28b501e2d02d6a9d0293f3ba2`. GNU Make 4.3. Exit: 0.

Working directory: `$LANES/682-pp-pin3`.

```sh
python3 syn/ooc/dp_srcs.py --top milan_datapath > /dev/null
python3 syn/ooc/dp_srcs.py --top KL_pp_shadow > /dev/null
```

Log: `$VALIDATION_STORAGE/682-a554/round2/acceptance/final-synthesis/15-dp-sources.log`; 0 bytes; SHA-256 `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`.

## final-synthesis 16: yosys-ooc-controls

Head: `591a5752e6a587b28b501e2d02d6a9d0293f3ba2`. GNU Make 4.3. Exit: 0.

Working directory: `$LANES/682-pp-pin3`.

```sh
python3 syn/yosys/ooc_selftest.py
```

Log: `$VALIDATION_STORAGE/682-a554/round2/acceptance/final-synthesis/16-yosys-ooc-controls.log`; 43 bytes; SHA-256 `d4febc14ba490cf79a72567d657e1653d21792043ae463564d52c831f69179e0`.

## final-synthesis 17: yosys-cache-controls

Head: `591a5752e6a587b28b501e2d02d6a9d0293f3ba2`. GNU Make 4.3. Exit: 0.

Working directory: `$LANES/682-pp-pin3`.

```sh
python3 syn/yosys/cache_selftest.py
```

Log: `$VALIDATION_STORAGE/682-a554/round2/acceptance/final-synthesis/17-yosys-cache-controls.log`; 190 bytes; SHA-256 `d8e090cf8c0c656d14381ecbb41901c83ad1870f0f38fed8b382815197e4dfa5`.

## final-vendor 01: xvlog

Head: `591a5752e6a587b28b501e2d02d6a9d0293f3ba2`. GNU Make 4.3. Exit: 0.

Working directory: `$LANES/682-pp-pin3`.

```sh
test "$(git -C protocol-processor rev-parse --show-toplevel)" = "$PWD/protocol-processor"
python3 scripts/xvlog_gate.py --check
```

Log: `$VALIDATION_STORAGE/682-a554/round2/acceptance/final-vendor/01-xvlog.log`; 721 bytes; SHA-256 `1c0d7a7bf120fe6c8d00aee69f966596e243b137fea381269c3dc1435c82e8d6`.

## firmware 01: firmware-tally-controls

Head: `342f20ef1fb29167c388b6f1fa3bc9851c3876e3`. GNU Make 4.3. Exit: 0.

Working directory: `$LANES/682-pp-pin3`.

```sh
python3 sw/firmware/gtest/tally_selftest.py --mutants
```

Log: `$VALIDATION_STORAGE/682-a554/round2/acceptance/firmware/01-firmware-tally-controls.log`; 3,982 bytes; SHA-256 `02268c336448885863d0308d88968cde7fe44eedb9743f0589fc01020f7eca11`.

## firmware 02: firmware-ctrl

Head: `342f20ef1fb29167c388b6f1fa3bc9851c3876e3`. GNU Make 4.3. Exit: 0.

Working directory: `$LANES/682-pp-pin3`.

```sh
python3 sw/firmware/ctrl/test/test_ctrl_firmware.py --require-rv32 --self-test --lwsrp $VALIDATION_STORAGE/665fc-a555/lwSRP
```

Log: `$VALIDATION_STORAGE/682-a554/round2/acceptance/firmware/02-firmware-ctrl.log`; 18,268 bytes; SHA-256 `87ed506551d20c0e21ea8a8ec618fbe4c50a54d532da941b437071d7beeea726`.

## firmware 03: firmware-nvm

Head: `342f20ef1fb29167c388b6f1fa3bc9851c3876e3`. GNU Make 4.3. Exit: 0.

Working directory: `$LANES/682-pp-pin3`.

```sh
sudo -n --preserve-env=PATH,MAKEFLAGS,PYTHONHASHSEED,PYTHON_CPU_COUNT,VERILATOR,VERILATOR_JOBS unshare --mount --propagation private $VALIDATION_STORAGE/682-a554/round2/control/nvm-pinned-sdk.sh python3 sw/firmware/ctrl_nvm/test/test_ctrl_nvm.py --require-rv32 --self-test --jobs 4
```

Log: `$VALIDATION_STORAGE/682-a554/round2/acceptance/firmware/03-firmware-nvm.log`; 22,991 bytes; SHA-256 `63ac74e489511b08437b6b3bee83956df493285c015701d6c60354edd3e4452c`.

## firmware 04: firmware-coverage-controls

Head: `342f20ef1fb29167c388b6f1fa3bc9851c3876e3`. GNU Make 4.3. Exit: 0.

Working directory: `$LANES/682-pp-pin3`.

```sh
python3 sw/firmware/gtest/fw_coverage.py --selftest
```

Log: `$VALIDATION_STORAGE/682-a554/round2/acceptance/firmware/04-firmware-coverage-controls.log`; 3,710 bytes; SHA-256 `3788b02a1c5d91d7ff2c8581f2ed09040261511d92565dd669103fee911dca0b`.

## firmware 05: firmware-coverage

Head: `342f20ef1fb29167c388b6f1fa3bc9851c3876e3`. GNU Make 4.3. Exit: 0.

Working directory: `$LANES/682-pp-pin3`.

```sh
python3 sw/firmware/gtest/fw_coverage.py --check --lwsrp $VALIDATION_STORAGE/665fc-a555/lwSRP --jobs 4
```

Log: `$VALIDATION_STORAGE/682-a554/round2/acceptance/firmware/05-firmware-coverage.log`; 2,684 bytes; SHA-256 `0ca531aa8fc378ee3a9c0b6c277abfbd8ee8a76b6ecbe588c73150c157e5b17c`.

## images 01: ExtraPostPlacementOpt

Head: `342f20ef1fb29167c388b6f1fa3bc9851c3876e3`. GNU Make 4.3. Exit: 0.

Working directory: `$VALIDATION_STORAGE/682-a554/round2/work/images/ExtraPostPlacementOpt/gateware`.

```sh
flock $VIVADO_LOCK vivado -mode batch -source finish.tcl -nojournal -log bitstream.log
"$LITEX_PYTHON" $VALIDATION_STORAGE/682-a554/round2/finish-image-check.py ExtraPostPlacementOpt
python3 "$REPO/sw/litex/layout_from_soch.py" $VALIDATION_STORAGE/682-a554/round2/work/images/ExtraPostPlacementOpt --bit $VALIDATION_STORAGE/682-a554/round2/work/images/ExtraPostPlacementOpt/gateware/alinx_ax7101.bit
python3 $VALIDATION_STORAGE/682-a554/round2/check-image-manifest-repeat.py ExtraPostPlacementOpt
python3 "$REPO/sw/litex/check_gptp_owner_pair.py" --layout $VALIDATION_STORAGE/682-a554/round2/work/images/ExtraPostPlacementOpt/flashboot_layout.json --expected-owner fabric --bit $VALIDATION_STORAGE/682-a554/round2/work/images/ExtraPostPlacementOpt/gateware/alinx_ax7101.bit --aem $VALIDATION_STORAGE/682-a554/round2/work/images/ExtraPostPlacementOpt/aem_desc.bin --expected-fpga-part xc7a100tfgg484
"$LITEX_PYTHON" $VALIDATION_STORAGE/682-a554/round2/run-image-preflight.py ExtraPostPlacementOpt
```

Log: `$VALIDATION_STORAGE/682-a554/round2/acceptance/images/01-ExtraPostPlacementOpt.log`; 45,755 bytes; SHA-256 `25a9b13fb2248c8eb380e691ed6a787c075f418759d567e1cb5f200992d58e2d`.

## lifecycle-diagnostic 01: gptp-lifecycle-recheck

Head: `342f20ef1fb29167c388b6f1fa3bc9851c3876e3`. GNU Make 4.3. Exit: 1.

Working directory: `$LANES/682-pp-pin3`.

```sh
python3 tb/verilator/gptp_shadow/test_mutant_lifecycle.py
```

Log: `$VALIDATION_STORAGE/682-a554/round2/acceptance/lifecycle-diagnostic/01-gptp-lifecycle-recheck.log`; 1,823 bytes; SHA-256 `163ffaebfffd4d2ab9a5bb3a7f14be879403229e34227ead5b8f9d9e25573222`.

## lifecycle-make-diagnostic 01: gptp-lifecycle-make-recheck

Head: `342f20ef1fb29167c388b6f1fa3bc9851c3876e3`. GNU Make 4.3. Exit: 0.

Working directory: `$LANES/682-pp-pin3`.

```sh
make -C tb/verilator/gptp_shadow -j8 lifecycle
```

Log: `$VALIDATION_STORAGE/682-a554/round2/acceptance/lifecycle-make-diagnostic/01-gptp-lifecycle-make-recheck.log`; 11,254 bytes; SHA-256 `51b614cc066c88a4c346cb2d01a7f7edc3f5c2fd05b7b334b68797cedbd3968c`.

## markdown 01: markdown-docs

Head: `342f20ef1fb29167c388b6f1fa3bc9851c3876e3`. GNU Make 4.3. Exit: 0.

Working directory: `$LANES/682-pp-pin3`.

```sh
$VALIDATION_TOOLS/md-venv-40cdefe08ebd/bin/python scripts/docs_check.py
```

Log: `$VALIDATION_STORAGE/682-a554/round2/acceptance/markdown/01-markdown-docs.log`; 128 bytes; SHA-256 `95f7175d0c2b4e833c08575992fc43ac2af2b0b20e7e6563042d98d000907a51`.

## markdown 02: markdown-toc-controls

Head: `342f20ef1fb29167c388b6f1fa3bc9851c3876e3`. GNU Make 4.3. Exit: 0.

Working directory: `$LANES/682-pp-pin3`.

```sh
$VALIDATION_TOOLS/md-venv-40cdefe08ebd/bin/python scripts/gen_toc.py --selftest
```

Log: `$VALIDATION_STORAGE/682-a554/round2/acceptance/markdown/02-markdown-toc-controls.log`; 38 bytes; SHA-256 `d7fd5f6ebcdd25e6cf93b623b0fba00cfa32d19c812ce34eb6b8d8b352ac9b32`.

## markdown 03: markdown-anchor-check

Head: `342f20ef1fb29167c388b6f1fa3bc9851c3876e3`. GNU Make 4.3. Exit: 0.

Working directory: `$LANES/682-pp-pin3`.

```sh
$VALIDATION_TOOLS/md-venv-40cdefe08ebd/bin/python scripts/gen_toc.py --verify-anchors
```

Log: `$VALIDATION_STORAGE/682-a554/round2/acceptance/markdown/03-markdown-anchor-check.log`; 64 bytes; SHA-256 `e469857b312e5786e37e249d8e941bb0e036a71a30d87c5cc7dfbd73d5d66d09`.

## markdown 04: markdown-toc-check

Head: `342f20ef1fb29167c388b6f1fa3bc9851c3876e3`. GNU Make 4.3. Exit: 0.

Working directory: `$LANES/682-pp-pin3`.

```sh
$VALIDATION_TOOLS/md-venv-40cdefe08ebd/bin/python scripts/gen_toc.py --check
```

Log: `$VALIDATION_STORAGE/682-a554/round2/acceptance/markdown/04-markdown-toc-check.log`; 94 bytes; SHA-256 `35e7e86e67b2d3d3968be2ae5107b946549d31bc8426a393fdae86c12f341b47`.

## nvm-isolated-check 01: nvm-quick-isolated

Head: `342f20ef1fb29167c388b6f1fa3bc9851c3876e3`. GNU Make 4.3. Exit: 0.

Working directory: `$LANES/682-pp-pin3`.

```sh
make -C tb/verilator/nvm_cosim -j8 quick JOBS=2 POOL=2
```

Log: `$VALIDATION_STORAGE/682-a554/round2/acceptance/nvm-isolated-check/01-nvm-quick-isolated.log`; 227 bytes; SHA-256 `acd676ed5d070aef0cb74ccb0f726f651649175d8615983ee3f618b40bea7725`.

## parent 01: physical-gptp

Head: `342f20ef1fb29167c388b6f1fa3bc9851c3876e3`. GNU Make 4.3. Exit: 0.

Working directory: `$LANES/682-pp-pin3`.

```sh
make -C tb/verilator/milan_dp_gptp -j8 VERILATOR_JOBS=2
```

Log: `$VALIDATION_STORAGE/682-a554/round2/acceptance/parent/01-physical-gptp.log`; 93,974 bytes; SHA-256 `72e9447facfa1b600dfd5d795d66d723e265132181ca5a53c5ebf2038c398e68`.

## parent 02: nvm-lint

Head: `342f20ef1fb29167c388b6f1fa3bc9851c3876e3`. GNU Make 4.3. Exit: 0.

Working directory: `$LANES/682-pp-pin3`.

```sh
make -C tb/verilator/nvm_cosim -j8 lint
```

Log: `$VALIDATION_STORAGE/682-a554/round2/acceptance/parent/02-nvm-lint.log`; 29,697 bytes; SHA-256 `2554112c7fc7662a378deca37d572da41a8dde9ede6189a129f218ce81a66a18`.

## parent 03: nvm-quick

Head: `342f20ef1fb29167c388b6f1fa3bc9851c3876e3`. GNU Make 4.3. Exit: 0.

Working directory: `$LANES/682-pp-pin3`.

Potentially contended scenario outputs; retained as historical evidence, superseded by the isolated NVM quick recheck.

```sh
make -C tb/verilator/nvm_cosim -j8 quick JOBS=2 POOL=2
```

Log: `$VALIDATION_STORAGE/682-a554/round2/acceptance/parent/03-nvm-quick.log`; 227 bytes; SHA-256 `acd676ed5d070aef0cb74ccb0f726f651649175d8615983ee3f618b40bea7725`.

## parent 04: litex-driver-controls

Head: `342f20ef1fb29167c388b6f1fa3bc9851c3876e3`. GNU Make 4.3. Exit: 0.

Working directory: `$LANES/682-pp-pin3`.

```sh
bash scripts/run_litex_sims.sh --selftest
```

Log: `$VALIDATION_STORAGE/682-a554/round2/acceptance/parent/04-litex-driver-controls.log`; 743 bytes; SHA-256 `59239532665913c93c6803a07126225f6ec393de1df48e679dab173624a5dddd`.

## parent 05: litex-sims

Head: `342f20ef1fb29167c388b6f1fa3bc9851c3876e3`. GNU Make 4.3. Exit: 0.

Working directory: `$LANES/682-pp-pin3`.

```sh
bash scripts/run_litex_sims.sh $VALIDATION_STORAGE/682-a554/round2/litex-sim-logs
```

Log: `$VALIDATION_STORAGE/682-a554/round2/acceptance/parent/05-litex-sims.log`; 312 bytes; SHA-256 `893d1cd5e084c49493eba898f15d916a0f3cdee420a4cc39896f434742bd4ef6`.

## processors 01: processor-sweep

Head: `342f20ef1fb29167c388b6f1fa3bc9851c3876e3`. GNU Make 4.3. Exit: 0.

Working directory: `$LANES/682-pp-pin3`.

```sh
test "$(git -C protocol-processor rev-parse --show-toplevel)" = "$PWD/protocol-processor"
PATH=$VALIDATION_STORAGE/661-a537/sv2v013/bin:$PATH bash protocol-processor/scripts/run_suites.sh
```

Log: `$VALIDATION_STORAGE/682-a554/round2/acceptance/processors/01-processor-sweep.log`; 1,750 bytes; SHA-256 `b37107cafb110e9a76737445437ee30a81673f33ec403875c8c27b1f5840c64a`.

## processors 02: gptp

Head: `342f20ef1fb29167c388b6f1fa3bc9851c3876e3`. GNU Make 4.3. Exit: 0.

Working directory: `$LANES/682-pp-pin3`.

```sh
make -C gptp-processor -j8 contract tb lint
```

Log: `$VALIDATION_STORAGE/682-a554/round2/acceptance/processors/02-gptp.log`; 14,041 bytes; SHA-256 `b80bd7d32cb6e1d12ff7cb4d416980dda092a6f5cc19f60efb3070c0cef906e5`.

## processors 03: bdd

Head: `342f20ef1fb29167c388b6f1fa3bc9851c3876e3`. GNU Make 4.3. Exit: 0.

Working directory: `$LANES/682-pp-pin3/tests`.

```sh
behave --no-capture -f plain
```

Log: `$VALIDATION_STORAGE/682-a554/round2/acceptance/processors/03-bdd.log`; 196,684 bytes; SHA-256 `bdb7efa83b917b6e7afe2f9e7aea836dc32309455420cc01157fab4a767beff8`.

## refresh-builder 01: builder-elaboration

Head: `5428b044176f95248e6916dc00dd89c0df154078`. GNU Make 4.3. Exit: 0.

Working directory: `$LANES/682-pp-pin3`.

Execution environment: `{"JOBS": "2", "LAW_BOUNDARY_JOBS": "4", "LITEX_ENV_CC_TRIPLE": "riscv32-linux", "MAKEFLAGS": "-j8 --no-print-directory", "POOL": "2", "PYTHONHASHSEED": "0", "PYTHON_CPU_COUNT": "4", "TSN_GEN_ROOT": "$VALIDATION_STORAGE/682-a554/round2/restored-dependencies/tsn-gen", "VERILATOR": "$VALIDATION_TOOLS/pinned-verilator-5.050/verilator", "VERILATOR_JOBS": "2"}`.

```sh
python3 sw/builder/test_builder.py --require-elaboration --require-rv32
```

Log: `$VALIDATION_STORAGE/682-a554/round2/acceptance/refresh-builder/01-builder-elaboration.log`; 101,687 bytes; SHA-256 `845c7b2d69f5a742b7acf4d21ff6f5c5105bcfbfe045e977cef71fc182871ef9`.

## refresh-field 01: oracle-configure

Head: `5428b044176f95248e6916dc00dd89c0df154078`. GNU Make 4.3. Exit: 0.

Working directory: `$LANES/682-pp-pin3`.

Execution environment: `{"JOBS": "2", "LAW_BOUNDARY_JOBS": "4", "LITEX_ENV_CC_TRIPLE": "riscv32-linux", "MAKEFLAGS": "-j8 --no-print-directory", "POOL": "2", "PYTHONHASHSEED": "0", "PYTHON_CPU_COUNT": "4", "TSN_GEN_ROOT": "$VALIDATION_STORAGE/682-a554/round2/restored-dependencies/tsn-gen", "VERILATOR": "$VALIDATION_TOOLS/pinned-verilator-5.050/verilator", "VERILATOR_JOBS": "2"}`.

```sh
cmake -S $VALIDATION_STORAGE/682-a554/round2/restored-dependencies/tsn-gen -B $VALIDATION_STORAGE/682-a554/round2/restored-dependencies/tsn-gen/build -DCMAKE_BUILD_TYPE=Release -DENABLE_PARSER_TESTS=OFF
```

Log: `$VALIDATION_STORAGE/682-a554/round2/acceptance/refresh-field/01-oracle-configure.log`; 3,789 bytes; SHA-256 `914c87164139807bb86fe0df5dcffea67d75f66a7e55312302da4910f1ad9bd2`.

## refresh-field 02: oracle-build

Head: `5428b044176f95248e6916dc00dd89c0df154078`. GNU Make 4.3. Exit: 0.

Working directory: `$LANES/682-pp-pin3`.

Execution environment: `{"JOBS": "2", "LAW_BOUNDARY_JOBS": "4", "LITEX_ENV_CC_TRIPLE": "riscv32-linux", "MAKEFLAGS": "-j8 --no-print-directory", "POOL": "2", "PYTHONHASHSEED": "0", "PYTHON_CPU_COUNT": "4", "TSN_GEN_ROOT": "$VALIDATION_STORAGE/682-a554/round2/restored-dependencies/tsn-gen", "VERILATOR": "$VALIDATION_TOOLS/pinned-verilator-5.050/verilator", "VERILATOR_JOBS": "2"}`.

```sh
cmake --build $VALIDATION_STORAGE/682-a554/round2/restored-dependencies/tsn-gen/build --target packet_gen --parallel 4
```

Log: `$VALIDATION_STORAGE/682-a554/round2/acceptance/refresh-field/02-oracle-build.log`; 4,367 bytes; SHA-256 `5a4271a9c562432ebc3d2a667270e7a358d22392754632511f15035a13ab79df`.

## refresh-field 03: tsn-fuzz

Head: `5428b044176f95248e6916dc00dd89c0df154078`. GNU Make 4.3. Exit: 0.

Working directory: `$LANES/682-pp-pin3`.

Execution environment: `{"JOBS": "2", "LAW_BOUNDARY_JOBS": "4", "LITEX_ENV_CC_TRIPLE": "riscv32-linux", "MAKEFLAGS": "-j8 --no-print-directory", "POOL": "2", "PYTHONHASHSEED": "0", "PYTHON_CPU_COUNT": "4", "TSN_GEN_ROOT": "$VALIDATION_STORAGE/682-a554/round2/restored-dependencies/tsn-gen", "VERILATOR": "$VALIDATION_TOOLS/pinned-verilator-5.050/verilator", "VERILATOR_JOBS": "2"}`.

```sh
test -x $VALIDATION_STORAGE/682-a554/round2/restored-dependencies/tsn-gen/build/traffic-gen/packet_gen
make -C tb/verilator/tsn_fuzz
```

Log: `$VALIDATION_STORAGE/682-a554/round2/acceptance/refresh-field/03-tsn-fuzz.log`; 11,269 bytes; SHA-256 `0af049c53889ad04b84efb97553cfd9bc1fa5e2c0217a9eeaad0a9cf88421c38`.

## refresh-field 04: tsn-verdict

Head: `5428b044176f95248e6916dc00dd89c0df154078`. GNU Make 4.3. Exit: 0.

Working directory: `$LANES/682-pp-pin3`.

Execution environment: `{"JOBS": "2", "LAW_BOUNDARY_JOBS": "4", "LITEX_ENV_CC_TRIPLE": "riscv32-linux", "MAKEFLAGS": "-j8 --no-print-directory", "POOL": "2", "PYTHONHASHSEED": "0", "PYTHON_CPU_COUNT": "4", "TSN_GEN_ROOT": "$VALIDATION_STORAGE/682-a554/round2/restored-dependencies/tsn-gen", "VERILATOR": "$VALIDATION_TOOLS/pinned-verilator-5.050/verilator", "VERILATOR_JOBS": "2"}`.

```sh
python3 scripts/suite_tally.py --verdict $VALIDATION_STORAGE/682-a554/round2/acceptance/refresh-field/03-tsn-fuzz.log
```

Log: `$VALIDATION_STORAGE/682-a554/round2/acceptance/refresh-field/04-tsn-verdict.log`; 0 bytes; SHA-256 `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`.

## refresh-field 05: field-completeness

Head: `5428b044176f95248e6916dc00dd89c0df154078`. GNU Make 4.3. Exit: 0.

Working directory: `$LANES/682-pp-pin3`.

Execution environment: `{"JOBS": "2", "LAW_BOUNDARY_JOBS": "4", "LITEX_ENV_CC_TRIPLE": "riscv32-linux", "MAKEFLAGS": "-j8 --no-print-directory", "POOL": "2", "PYTHONHASHSEED": "0", "PYTHON_CPU_COUNT": "4", "TSN_GEN_ROOT": "$VALIDATION_STORAGE/682-a554/round2/restored-dependencies/tsn-gen", "VERILATOR": "$VALIDATION_TOOLS/pinned-verilator-5.050/verilator", "VERILATOR_JOBS": "2"}`.

```sh
python3 $VALIDATION_STORAGE/682-a554/round2/check-refreshed-field.py
```

Log: `$VALIDATION_STORAGE/682-a554/round2/acceptance/refresh-field/05-field-completeness.log`; 106 bytes; SHA-256 `1dd208a39feea42e3697da525eb9f83057d42a8905f293b638244a420a2ab10f`.

## refresh-firmware 01: sdk-controls

Head: `5428b044176f95248e6916dc00dd89c0df154078`. GNU Make 4.3. Exit: 0.

Working directory: `$LANES/682-pp-pin3`.

Execution environment: `{"JOBS": "2", "LAW_BOUNDARY_JOBS": "4", "LITEX_ENV_CC_TRIPLE": "riscv32-linux", "MAKEFLAGS": "-j8 --no-print-directory", "POOL": "2", "PYTHONHASHSEED": "0", "PYTHON_CPU_COUNT": "4", "TSN_GEN_ROOT": "$VALIDATION_STORAGE/682-a554/round2/restored-dependencies/tsn-gen", "VERILATOR": "$VALIDATION_TOOLS/pinned-verilator-5.050/verilator", "VERILATOR_JOBS": "2"}`.

```sh
python3 scripts/ci_rv32_sdk_selftest.py
```

Log: `$VALIDATION_STORAGE/682-a554/round2/acceptance/refresh-firmware/01-sdk-controls.log`; 5,759 bytes; SHA-256 `b92571400fe49b3a60f67673cabbe80cd0b6c5ea3ebb08244eb5d96498a64c2e`.

## refresh-firmware 02: rv32-object-controls

Head: `5428b044176f95248e6916dc00dd89c0df154078`. GNU Make 4.3. Exit: 0.

Working directory: `$LANES/682-pp-pin3`.

Execution environment: `{"JOBS": "2", "LAW_BOUNDARY_JOBS": "4", "LITEX_ENV_CC_TRIPLE": "riscv32-linux", "MAKEFLAGS": "-j8 --no-print-directory", "MILAN_RV32_CC": "$VALIDATION_STORAGE/682-a554/round2/tool-prefixes/rv32-sdk/bin/riscv32-linux-gcc", "POOL": "2", "PYTHONHASHSEED": "0", "PYTHON_CPU_COUNT": "4", "TSN_GEN_ROOT": "$VALIDATION_STORAGE/682-a554/round2/restored-dependencies/tsn-gen", "VERILATOR": "$VALIDATION_TOOLS/pinned-verilator-5.050/verilator", "VERILATOR_JOBS": "2"}`.

```sh
python3 sw/firmware/gtest/fw_rv32_selftest.py --require-rv32
```

Log: `$VALIDATION_STORAGE/682-a554/round2/acceptance/refresh-firmware/02-rv32-object-controls.log`; 793 bytes; SHA-256 `9cd3b019b88560e4f902812b20cbb7d859405f50f0e686d6d71b6474287e7c94`.

## refresh-firmware 03: firmware-tally-controls

Head: `5428b044176f95248e6916dc00dd89c0df154078`. GNU Make 4.3. Exit: 0.

Working directory: `$LANES/682-pp-pin3`.

Execution environment: `{"JOBS": "2", "LAW_BOUNDARY_JOBS": "4", "LITEX_ENV_CC_TRIPLE": "riscv32-linux", "MAKEFLAGS": "-j8 --no-print-directory", "POOL": "2", "PYTHONHASHSEED": "0", "PYTHON_CPU_COUNT": "4", "TSN_GEN_ROOT": "$VALIDATION_STORAGE/682-a554/round2/restored-dependencies/tsn-gen", "VERILATOR": "$VALIDATION_TOOLS/pinned-verilator-5.050/verilator", "VERILATOR_JOBS": "2"}`.

```sh
python3 sw/firmware/gtest/tally_selftest.py --mutants
```

Log: `$VALIDATION_STORAGE/682-a554/round2/acceptance/refresh-firmware/03-firmware-tally-controls.log`; 3,982 bytes; SHA-256 `02268c336448885863d0308d88968cde7fe44eedb9743f0589fc01020f7eca11`.

## refresh-firmware 04: firmware-ctrl

Head: `5428b044176f95248e6916dc00dd89c0df154078`. GNU Make 4.3. Exit: 0.

Working directory: `$LANES/682-pp-pin3`.

Execution environment: `{"JOBS": "2", "LAW_BOUNDARY_JOBS": "4", "LITEX_ENV_CC_TRIPLE": "riscv32-linux", "MAKEFLAGS": "-j8 --no-print-directory", "MILAN_RV32_CC": "$VALIDATION_STORAGE/682-a554/round2/tool-prefixes/rv32-sdk/bin/riscv32-linux-gcc", "POOL": "2", "PYTHONHASHSEED": "0", "PYTHON_CPU_COUNT": "4", "TSN_GEN_ROOT": "$VALIDATION_STORAGE/682-a554/round2/restored-dependencies/tsn-gen", "VERILATOR": "$VALIDATION_TOOLS/pinned-verilator-5.050/verilator", "VERILATOR_JOBS": "2"}`.

```sh
python3 sw/firmware/ctrl/test/test_ctrl_firmware.py --require-rv32 --self-test --lwsrp $VALIDATION_STORAGE/665fc-a555/lwSRP --jobs 4
```

Log: `$VALIDATION_STORAGE/682-a554/round2/acceptance/refresh-firmware/04-firmware-ctrl.log`; 39,463 bytes; SHA-256 `7e5b4fb06949bdf7fd21ba21631cb23e2296cef7e6b84028a81f7784812fec18`.

## refresh-firmware 05: firmware-coverage-controls

Head: `5428b044176f95248e6916dc00dd89c0df154078`. GNU Make 4.3. Exit: 0.

Working directory: `$LANES/682-pp-pin3`.

Execution environment: `{"JOBS": "2", "LAW_BOUNDARY_JOBS": "4", "LITEX_ENV_CC_TRIPLE": "riscv32-linux", "MAKEFLAGS": "-j8 --no-print-directory", "POOL": "2", "PYTHONHASHSEED": "0", "PYTHON_CPU_COUNT": "4", "TSN_GEN_ROOT": "$VALIDATION_STORAGE/682-a554/round2/restored-dependencies/tsn-gen", "VERILATOR": "$VALIDATION_TOOLS/pinned-verilator-5.050/verilator", "VERILATOR_JOBS": "2"}`.

```sh
python3 sw/firmware/gtest/fw_coverage.py --selftest
```

Log: `$VALIDATION_STORAGE/682-a554/round2/acceptance/refresh-firmware/05-firmware-coverage-controls.log`; 3,710 bytes; SHA-256 `3788b02a1c5d91d7ff2c8581f2ed09040261511d92565dd669103fee911dca0b`.

## refresh-firmware 06: firmware-coverage

Head: `5428b044176f95248e6916dc00dd89c0df154078`. GNU Make 4.3. Exit: 0.

Working directory: `$LANES/682-pp-pin3`.

Execution environment: `{"JOBS": "2", "LAW_BOUNDARY_JOBS": "4", "LITEX_ENV_CC_TRIPLE": "riscv32-linux", "MAKEFLAGS": "-j8 --no-print-directory", "POOL": "2", "PYTHONHASHSEED": "0", "PYTHON_CPU_COUNT": "4", "TSN_GEN_ROOT": "$VALIDATION_STORAGE/682-a554/round2/restored-dependencies/tsn-gen", "VERILATOR": "$VALIDATION_TOOLS/pinned-verilator-5.050/verilator", "VERILATOR_JOBS": "2"}`.

```sh
python3 sw/firmware/gtest/fw_coverage.py --check --lwsrp $VALIDATION_STORAGE/665fc-a555/lwSRP --jobs 4
```

Log: `$VALIDATION_STORAGE/682-a554/round2/acceptance/refresh-firmware/06-firmware-coverage.log`; 3,005 bytes; SHA-256 `173dbff52a82557f6b44df9af37d262af0cbc7626d342ce51f10b32d5bbe7d13`.

## refresh-mailbox 01: mbx

Head: `5428b044176f95248e6916dc00dd89c0df154078`. GNU Make 4.3. Exit: 0.

Working directory: `$LANES/682-pp-pin3`.

Execution environment: `{"JOBS": "2", "LAW_BOUNDARY_JOBS": "4", "LITEX_ENV_CC_TRIPLE": "riscv32-linux", "MAKEFLAGS": "-j8 --no-print-directory", "POOL": "2", "PYTHONHASHSEED": "0", "PYTHON_CPU_COUNT": "4", "TSN_GEN_ROOT": "$VALIDATION_STORAGE/682-a554/round2/restored-dependencies/tsn-gen", "VERILATOR": "$VALIDATION_TOOLS/pinned-verilator-5.050/verilator", "VERILATOR_JOBS": "2"}`.

```sh
make -C tb/verilator/mbx VBUILD_JOBS=2
```

Log: `$VALIDATION_STORAGE/682-a554/round2/acceptance/refresh-mailbox/01-mbx.log`; 19,127 bytes; SHA-256 `86872f1b175f97e725cbb758437d4bcb72047216083b988ba3aa985e0ba68d61`.

## refresh-mailbox 02: mbx-verdict

Head: `5428b044176f95248e6916dc00dd89c0df154078`. GNU Make 4.3. Exit: 0.

Working directory: `$LANES/682-pp-pin3`.

Execution environment: `{"JOBS": "2", "LAW_BOUNDARY_JOBS": "4", "LITEX_ENV_CC_TRIPLE": "riscv32-linux", "MAKEFLAGS": "-j8 --no-print-directory", "POOL": "2", "PYTHONHASHSEED": "0", "PYTHON_CPU_COUNT": "4", "TSN_GEN_ROOT": "$VALIDATION_STORAGE/682-a554/round2/restored-dependencies/tsn-gen", "VERILATOR": "$VALIDATION_TOOLS/pinned-verilator-5.050/verilator", "VERILATOR_JOBS": "2"}`.

```sh
python3 scripts/suite_tally.py --verdict $VALIDATION_STORAGE/682-a554/round2/acceptance/refresh-mailbox/01-mbx.log
```

Log: `$VALIDATION_STORAGE/682-a554/round2/acceptance/refresh-mailbox/02-mbx-verdict.log`; 0 bytes; SHA-256 `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`.

## refresh-markdown 01: markdown-docs

Head: `5428b044176f95248e6916dc00dd89c0df154078`. GNU Make 4.3. Exit: 0.

Working directory: `$LANES/682-pp-pin3`.

Execution environment: `{"JOBS": "2", "LAW_BOUNDARY_JOBS": "4", "LITEX_ENV_CC_TRIPLE": "riscv32-linux", "MAKEFLAGS": "-j8 --no-print-directory", "POOL": "2", "PYTHONHASHSEED": "0", "PYTHON_CPU_COUNT": "4", "TSN_GEN_ROOT": "$VALIDATION_STORAGE/682-a554/round2/restored-dependencies/tsn-gen", "VERILATOR": "$VALIDATION_TOOLS/pinned-verilator-5.050/verilator", "VERILATOR_JOBS": "2"}`.

```sh
$VALIDATION_TOOLS/md-venv-40cdefe08ebd/bin/python scripts/docs_check.py
```

Log: `$VALIDATION_STORAGE/682-a554/round2/acceptance/refresh-markdown/01-markdown-docs.log`; 128 bytes; SHA-256 `9de597c20c044953930a35a471dc8e5592ecc57b24be4c395bf381c1e72e2052`.

## refresh-markdown 02: markdown-toc-controls

Head: `5428b044176f95248e6916dc00dd89c0df154078`. GNU Make 4.3. Exit: 0.

Working directory: `$LANES/682-pp-pin3`.

Execution environment: `{"JOBS": "2", "LAW_BOUNDARY_JOBS": "4", "LITEX_ENV_CC_TRIPLE": "riscv32-linux", "MAKEFLAGS": "-j8 --no-print-directory", "POOL": "2", "PYTHONHASHSEED": "0", "PYTHON_CPU_COUNT": "4", "TSN_GEN_ROOT": "$VALIDATION_STORAGE/682-a554/round2/restored-dependencies/tsn-gen", "VERILATOR": "$VALIDATION_TOOLS/pinned-verilator-5.050/verilator", "VERILATOR_JOBS": "2"}`.

```sh
$VALIDATION_TOOLS/md-venv-40cdefe08ebd/bin/python scripts/gen_toc.py --selftest
```

Log: `$VALIDATION_STORAGE/682-a554/round2/acceptance/refresh-markdown/02-markdown-toc-controls.log`; 38 bytes; SHA-256 `d7fd5f6ebcdd25e6cf93b623b0fba00cfa32d19c812ce34eb6b8d8b352ac9b32`.

## refresh-markdown 03: markdown-anchor-check

Head: `5428b044176f95248e6916dc00dd89c0df154078`. GNU Make 4.3. Exit: 0.

Working directory: `$LANES/682-pp-pin3`.

Execution environment: `{"JOBS": "2", "LAW_BOUNDARY_JOBS": "4", "LITEX_ENV_CC_TRIPLE": "riscv32-linux", "MAKEFLAGS": "-j8 --no-print-directory", "POOL": "2", "PYTHONHASHSEED": "0", "PYTHON_CPU_COUNT": "4", "TSN_GEN_ROOT": "$VALIDATION_STORAGE/682-a554/round2/restored-dependencies/tsn-gen", "VERILATOR": "$VALIDATION_TOOLS/pinned-verilator-5.050/verilator", "VERILATOR_JOBS": "2"}`.

```sh
$VALIDATION_TOOLS/md-venv-40cdefe08ebd/bin/python scripts/gen_toc.py --verify-anchors
```

Log: `$VALIDATION_STORAGE/682-a554/round2/acceptance/refresh-markdown/03-markdown-anchor-check.log`; 64 bytes; SHA-256 `2085cd5b07944246d79457654dfb861a2b81a1c93936c4428b0ac2895b44371e`.

## refresh-markdown 04: markdown-toc-check

Head: `5428b044176f95248e6916dc00dd89c0df154078`. GNU Make 4.3. Exit: 0.

Working directory: `$LANES/682-pp-pin3`.

Execution environment: `{"JOBS": "2", "LAW_BOUNDARY_JOBS": "4", "LITEX_ENV_CC_TRIPLE": "riscv32-linux", "MAKEFLAGS": "-j8 --no-print-directory", "POOL": "2", "PYTHONHASHSEED": "0", "PYTHON_CPU_COUNT": "4", "TSN_GEN_ROOT": "$VALIDATION_STORAGE/682-a554/round2/restored-dependencies/tsn-gen", "VERILATOR": "$VALIDATION_TOOLS/pinned-verilator-5.050/verilator", "VERILATOR_JOBS": "2"}`.

```sh
$VALIDATION_TOOLS/md-venv-40cdefe08ebd/bin/python scripts/gen_toc.py --check
```

Log: `$VALIDATION_STORAGE/682-a554/round2/acceptance/refresh-markdown/04-markdown-toc-check.log`; 94 bytes; SHA-256 `327a49b965f12e7f77c6ab1ae5812d3fed54f2dd64786e400f71111120c97fbd`.

## refresh-records 01: generated-record-repeatability

Head: `5428b044176f95248e6916dc00dd89c0df154078`. GNU Make 4.4.1. Exit: 0.

Working directory: `$LANES/682-pp-pin3`.

Execution environment: `{"JOBS": "2", "LAW_BOUNDARY_JOBS": "4", "LITEX_ENV_CC_TRIPLE": "riscv32-linux", "MAKEFLAGS": "-j8 --no-print-directory", "POOL": "2", "PYTHONHASHSEED": "0", "PYTHON_CPU_COUNT": "4", "TSN_GEN_ROOT": "$VALIDATION_STORAGE/667-a551/tsn-gen", "VERILATOR": "$VALIDATION_TOOLS/pinned-verilator-5.050/verilator", "VERILATOR_JOBS": "2"}`.

```sh
python3 $VALIDATION_STORAGE/682-a554/round2/verify-refresh-records.py
```

Log: `$VALIDATION_STORAGE/682-a554/round2/acceptance/refresh-records/01-generated-record-repeatability.log`; 258 bytes; SHA-256 `9ea22aaa883f791ac12c06c2b73e0fc96d098c9858a37e27967d8bde43eea747`.

## refresh-records-final 01: generated-record-repeatability

Head: `5428b044176f95248e6916dc00dd89c0df154078`. GNU Make 4.3. Exit: 0.

Working directory: `$LANES/682-pp-pin3`.

Execution environment: `{"JOBS": "2", "LAW_BOUNDARY_JOBS": "4", "LITEX_ENV_CC_TRIPLE": "riscv32-linux", "MAKEFLAGS": "-j8 --no-print-directory", "MILAN_RV32_CC": "$VALIDATION_STORAGE/682-a554/round2/tool-prefixes/rv32-sdk/bin/riscv32-linux-gcc", "POOL": "2", "PYTHONHASHSEED": "0", "PYTHON_CPU_COUNT": "4", "TSN_GEN_ROOT": "$VALIDATION_STORAGE/682-a554/round2/restored-dependencies/tsn-gen", "VERILATOR": "$VALIDATION_TOOLS/pinned-verilator-5.050/verilator", "VERILATOR_JOBS": "2"}`.

```sh
python3 $VALIDATION_STORAGE/682-a554/round2/verify-refresh-records.py
```

Log: `$VALIDATION_STORAGE/682-a554/round2/acceptance/refresh-records-final/01-generated-record-repeatability.log`; 258 bytes; SHA-256 `9ea22aaa883f791ac12c06c2b73e0fc96d098c9858a37e27967d8bde43eea747`.

## refresh-resources 01: route-1x1

Head: `5428b044176f95248e6916dc00dd89c0df154078`. GNU Make 4.3. Exit: 0.

Working directory: `$LANES/682-pp-pin3`.

Execution environment: `{"JOBS": "2", "LAW_BOUNDARY_JOBS": "4", "LITEX_ENV_CC_TRIPLE": "riscv32-linux", "MAKEFLAGS": "-j8 --no-print-directory", "POOL": "2", "PYTHONHASHSEED": "0", "PYTHON_CPU_COUNT": "4", "TSN_GEN_ROOT": "$VALIDATION_STORAGE/682-a554/round2/restored-dependencies/tsn-gen", "VERILATOR": "$VALIDATION_TOOLS/pinned-verilator-5.050/verilator", "VERILATOR_JOBS": "2"}`.

```sh
python3 syn/ooc/pp_resource_gate.py check $VALIDATION_STORAGE/682-a554/round2/work/ax7101/gateware --endpoint route-1x1
```

Log: `$VALIDATION_STORAGE/682-a554/round2/acceptance/refresh-resources/01-route-1x1.log`; 593 bytes; SHA-256 `2ca20be2737097c53a7907da0cabb7de63a00c68bd0171d2eea1db82c6949e9c`.

## refresh-resources 02: ooc-1x1

Head: `5428b044176f95248e6916dc00dd89c0df154078`. GNU Make 4.3. Exit: 0.

Working directory: `$LANES/682-pp-pin3`.

Execution environment: `{"JOBS": "2", "LAW_BOUNDARY_JOBS": "4", "LITEX_ENV_CC_TRIPLE": "riscv32-linux", "MAKEFLAGS": "-j8 --no-print-directory", "POOL": "2", "PYTHONHASHSEED": "0", "PYTHON_CPU_COUNT": "4", "TSN_GEN_ROOT": "$VALIDATION_STORAGE/682-a554/round2/restored-dependencies/tsn-gen", "VERILATOR": "$VALIDATION_TOOLS/pinned-verilator-5.050/verilator", "VERILATOR_JOBS": "2"}`.

```sh
python3 syn/ooc/pp_resource_gate.py check $VALIDATION_STORAGE/682-a554/round2/work/ax7101-ooc --endpoint ooc-1x1
```

Log: `$VALIDATION_STORAGE/682-a554/round2/acceptance/refresh-resources/02-ooc-1x1.log`; 378 bytes; SHA-256 `1497ef241c7693598d85d9e76208172f422b40af299db3799d87c0291e09ec3c`.

## refresh-resources 03: ooc-8x8

Head: `5428b044176f95248e6916dc00dd89c0df154078`. GNU Make 4.3. Exit: 0.

Working directory: `$LANES/682-pp-pin3`.

Execution environment: `{"JOBS": "2", "LAW_BOUNDARY_JOBS": "4", "LITEX_ENV_CC_TRIPLE": "riscv32-linux", "MAKEFLAGS": "-j8 --no-print-directory", "POOL": "2", "PYTHONHASHSEED": "0", "PYTHON_CPU_COUNT": "4", "TSN_GEN_ROOT": "$VALIDATION_STORAGE/682-a554/round2/restored-dependencies/tsn-gen", "VERILATOR": "$VALIDATION_TOOLS/pinned-verilator-5.050/verilator", "VERILATOR_JOBS": "2"}`.

```sh
python3 syn/ooc/pp_resource_gate.py check $VALIDATION_STORAGE/682-a554/round2/work/ax8x8-ooc --endpoint ooc-8x8
```

Log: `$VALIDATION_STORAGE/682-a554/round2/acceptance/refresh-resources/03-ooc-8x8.log`; 377 bytes; SHA-256 `085dede82739485596ecdd3b6383ddc7de15cbaa105e91ba821c917ebf89a60a`.

## refresh-resources 04: resource-policy

Head: `5428b044176f95248e6916dc00dd89c0df154078`. GNU Make 4.3. Exit: 0.

Working directory: `$LANES/682-pp-pin3`.

Execution environment: `{"JOBS": "2", "LAW_BOUNDARY_JOBS": "4", "LITEX_ENV_CC_TRIPLE": "riscv32-linux", "MAKEFLAGS": "-j8 --no-print-directory", "POOL": "2", "PYTHONHASHSEED": "0", "PYTHON_CPU_COUNT": "4", "TSN_GEN_ROOT": "$VALIDATION_STORAGE/682-a554/round2/restored-dependencies/tsn-gen", "VERILATOR": "$VALIDATION_TOOLS/pinned-verilator-5.050/verilator", "VERILATOR_JOBS": "2"}`.

```sh
python3 syn/ooc/pp_resource_gate.py check-baseline
```

Log: `$VALIDATION_STORAGE/682-a554/round2/acceptance/refresh-resources/04-resource-policy.log`; 27 bytes; SHA-256 `2114d909e60add091220b415987d4409a611d70c9e84f1bb9e0ae12d6a2f14a0`.

## refresh-resources 05: capture-receipt

Head: `5428b044176f95248e6916dc00dd89c0df154078`. GNU Make 4.3. Exit: 0.

Working directory: `$LANES/682-pp-pin3`.

Execution environment: `{"JOBS": "2", "LAW_BOUNDARY_JOBS": "4", "LITEX_ENV_CC_TRIPLE": "riscv32-linux", "MAKEFLAGS": "-j8 --no-print-directory", "POOL": "2", "PYTHONHASHSEED": "0", "PYTHON_CPU_COUNT": "4", "TSN_GEN_ROOT": "$VALIDATION_STORAGE/682-a554/round2/restored-dependencies/tsn-gen", "VERILATOR": "$VALIDATION_TOOLS/pinned-verilator-5.050/verilator", "VERILATOR_JOBS": "2"}`.

```sh
python3 scripts/check_nvm_capture.py
```

Log: `$VALIDATION_STORAGE/682-a554/round2/acceptance/refresh-resources/05-capture-receipt.log`; 324 bytes; SHA-256 `9a4196c774ce4ddfa9980cf9345d111028f3afa812677fe5bab392f81c955439`.

## refresh-resources 06: exact-resource-inputs

Head: `5428b044176f95248e6916dc00dd89c0df154078`. GNU Make 4.3. Exit: 0.

Working directory: `$LANES/682-pp-pin3`.

Execution environment: `{"JOBS": "2", "LAW_BOUNDARY_JOBS": "4", "LITEX_ENV_CC_TRIPLE": "riscv32-linux", "MAKEFLAGS": "-j8 --no-print-directory", "POOL": "2", "PYTHONHASHSEED": "0", "PYTHON_CPU_COUNT": "4", "TSN_GEN_ROOT": "$VALIDATION_STORAGE/682-a554/round2/restored-dependencies/tsn-gen", "VERILATOR": "$VALIDATION_TOOLS/pinned-verilator-5.050/verilator", "VERILATOR_JOBS": "2"}`.

```sh
python3 $VALIDATION_STORAGE/682-a554/round2/verify-record-inputs.py
```

Log: `$VALIDATION_STORAGE/682-a554/round2/acceptance/refresh-resources/06-exact-resource-inputs.log`; 278 bytes; SHA-256 `b80d5cc237b2a35454d1e8fb166dafcca3fd4bdd41213111744e0aef9db50a06`.

## resources 01: route-1x1

Head: `342f20ef1fb29167c388b6f1fa3bc9851c3876e3`. GNU Make 4.3. Exit: 0.

Working directory: `$LANES/682-pp-pin3`.

```sh
python3 syn/ooc/pp_resource_gate.py check $VALIDATION_STORAGE/682-a554/round2/work/ax7101/gateware --endpoint route-1x1
```

Log: `$VALIDATION_STORAGE/682-a554/round2/acceptance/resources/01-route-1x1.log`; 593 bytes; SHA-256 `2ca20be2737097c53a7907da0cabb7de63a00c68bd0171d2eea1db82c6949e9c`.

## resources 02: ooc-1x1

Head: `342f20ef1fb29167c388b6f1fa3bc9851c3876e3`. GNU Make 4.3. Exit: 0.

Working directory: `$LANES/682-pp-pin3`.

```sh
python3 syn/ooc/pp_resource_gate.py check $VALIDATION_STORAGE/682-a554/round2/work/ax7101-ooc --endpoint ooc-1x1
```

Log: `$VALIDATION_STORAGE/682-a554/round2/acceptance/resources/02-ooc-1x1.log`; 378 bytes; SHA-256 `1497ef241c7693598d85d9e76208172f422b40af299db3799d87c0291e09ec3c`.

## resources 03: ooc-8x8

Head: `342f20ef1fb29167c388b6f1fa3bc9851c3876e3`. GNU Make 4.3. Exit: 0.

Working directory: `$LANES/682-pp-pin3`.

```sh
python3 syn/ooc/pp_resource_gate.py check $VALIDATION_STORAGE/682-a554/round2/work/ax8x8-ooc --endpoint ooc-8x8
```

Log: `$VALIDATION_STORAGE/682-a554/round2/acceptance/resources/03-ooc-8x8.log`; 377 bytes; SHA-256 `085dede82739485596ecdd3b6383ddc7de15cbaa105e91ba821c917ebf89a60a`.

## resources 04: resource-policy

Head: `342f20ef1fb29167c388b6f1fa3bc9851c3876e3`. GNU Make 4.3. Exit: 0.

Working directory: `$LANES/682-pp-pin3`.

```sh
python3 syn/ooc/pp_resource_gate.py check-baseline
```

Log: `$VALIDATION_STORAGE/682-a554/round2/acceptance/resources/04-resource-policy.log`; 27 bytes; SHA-256 `2114d909e60add091220b415987d4409a611d70c9e84f1bb9e0ae12d6a2f14a0`.

## resources 05: capture-receipt

Head: `342f20ef1fb29167c388b6f1fa3bc9851c3876e3`. GNU Make 4.3. Exit: 0.

Working directory: `$LANES/682-pp-pin3`.

```sh
python3 scripts/check_nvm_capture.py
```

Log: `$VALIDATION_STORAGE/682-a554/round2/acceptance/resources/05-capture-receipt.log`; 324 bytes; SHA-256 `9a4196c774ce4ddfa9980cf9345d111028f3afa812677fe5bab392f81c955439`.

## resources 06: exact-resource-inputs

Head: `342f20ef1fb29167c388b6f1fa3bc9851c3876e3`. GNU Make 4.3. Exit: 0.

Working directory: `$LANES/682-pp-pin3`.

```sh
python3 $VALIDATION_STORAGE/682-a554/round2/verify-record-inputs.py
```

Log: `$VALIDATION_STORAGE/682-a554/round2/acceptance/resources/06-exact-resource-inputs.log`; 278 bytes; SHA-256 `b80d5cc237b2a35454d1e8fb166dafcca3fd4bdd41213111744e0aef9db50a06`.

## sweep 01: parent-sweep

Head: `342f20ef1fb29167c388b6f1fa3bc9851c3876e3`. GNU Make 4.3. Exit: 1.

Working directory: `$LANES/682-pp-pin3`.

```sh
bash scripts/run_all_suites.sh $VALIDATION_STORAGE/682-a554/round2/parent-suite-logs
```

Log: `$VALIDATION_STORAGE/682-a554/round2/acceptance/sweep/01-parent-sweep.log`; 1,430 bytes; SHA-256 `c6e6d92723e6906ebe81c92c1bd8aa62a0e624af54cbbf3e9d6288bec87b7ded`.

## sweep 02: parent-tally

Head: `342f20ef1fb29167c388b6f1fa3bc9851c3876e3`. GNU Make 4.3. Exit: 0.

Working directory: `$LANES/682-pp-pin3`.

```sh
python3 scripts/suite_tally.py $VALIDATION_STORAGE/682-a554/round2/parent-suite-logs --quiet --expect-suite-root tb/verilator
```

Log: `$VALIDATION_STORAGE/682-a554/round2/acceptance/sweep/02-parent-tally.log`; 39 bytes; SHA-256 `cb79611bcc0de14461d5bd2e201e00d3576db6e8f9bc82c95aa37c1ea6ab118e`.

## synthesis 01: lint

Head: `342f20ef1fb29167c388b6f1fa3bc9851c3876e3`. GNU Make 4.3. Exit: 0.

Working directory: `$LANES/682-pp-pin3`.

```sh
python3 scripts/lint_rtl.py --check --self-test
```

Log: `$VALIDATION_STORAGE/682-a554/round2/acceptance/synthesis/01-lint.log`; 14,888 bytes; SHA-256 `fdfaa1c6d9058fd1f1d30ef75e8590d1e633c21b21ff6fb7455e0542dc99123a`.

## synthesis 02: pp-sources

Head: `342f20ef1fb29167c388b6f1fa3bc9851c3876e3`. GNU Make 4.3. Exit: 0.

Working directory: `$LANES/682-pp-pin3`.

```sh
python3 scripts/pp_srcs.py --check --selftest
```

Log: `$VALIDATION_STORAGE/682-a554/round2/acceptance/synthesis/02-pp-sources.log`; 955 bytes; SHA-256 `fad5e1b9dd5f465b7fcb2334e2abe6c6db44be93b5bb12afb3a35f3ebf432e1a`.

## synthesis 03: scope

Head: `342f20ef1fb29167c388b6f1fa3bc9851c3876e3`. GNU Make 4.3. Exit: 0.

Working directory: `$LANES/682-pp-pin3`.

```sh
python3 scripts/ci_scope.py --selftest
```

Log: `$VALIDATION_STORAGE/682-a554/round2/acceptance/synthesis/03-scope.log`; 6,877 bytes; SHA-256 `94cc98b3dc0fc8fc8ddba008723ab266f0b8705762f3b88e14df6f2edf8c3ece`.

## synthesis 04: yosys

Head: `342f20ef1fb29167c388b6f1fa3bc9851c3876e3`. GNU Make 4.3. Exit: 0.

Working directory: `$LANES/682-pp-pin3`.

```sh
bash syn/yosys/run.sh --results $VALIDATION_STORAGE/682-a554/round2/yosys-results
```

Log: `$VALIDATION_STORAGE/682-a554/round2/acceptance/synthesis/04-yosys.log`; 6,182 bytes; SHA-256 `3878f06a08331614b19f0c56a8937774a21fd10ae50c1ecac44e21beefa94f21`.

## synthesis 05: yosys-tally

Head: `342f20ef1fb29167c388b6f1fa3bc9851c3876e3`. GNU Make 4.3. Exit: 0.

Working directory: `$LANES/682-pp-pin3`.

```sh
bash syn/yosys/run.sh --list > $VALIDATION_STORAGE/682-a554/round2/yosys-expected.txt
python3 scripts/yosys_tally.py $VALIDATION_STORAGE/682-a554/round2/yosys-results --expected $VALIDATION_STORAGE/682-a554/round2/yosys-expected.txt --require-structural
```

Log: `$VALIDATION_STORAGE/682-a554/round2/acceptance/synthesis/05-yosys-tally.log`; 49 bytes; SHA-256 `ca886fa4ca355ab8ad0ad261ad5d583dc524bc0f89466f52032de7cfc3d667c4`.

## synthesis 06: fast-elaboration

Head: `342f20ef1fb29167c388b6f1fa3bc9851c3876e3`. GNU Make 4.3. Exit: 0.

Working directory: `$LANES/682-pp-pin3`.

```sh
bash syn/yosys/run.sh --mode elaborate --no-structural --top milan_datapath --top KL_pp_shadow --top KL_gptp_shadow
```

Log: `$VALIDATION_STORAGE/682-a554/round2/acceptance/synthesis/06-fast-elaboration.log`; 369 bytes; SHA-256 `b07aa0caefde92c83defb48336b45d06f106325af111710b39d327e529599073`.

## synthesis 07: dp-source-controls

Head: `342f20ef1fb29167c388b6f1fa3bc9851c3876e3`. GNU Make 4.3. Exit: 0.

Working directory: `$LANES/682-pp-pin3`.

```sh
python3 syn/ooc/dp_srcs.py --selftest
```

Log: `$VALIDATION_STORAGE/682-a554/round2/acceptance/synthesis/07-dp-source-controls.log`; 36 bytes; SHA-256 `d1d5a4fa150962bc8cd53e563cde50da65cc8cfeee212d82e10bc293848bd428`.

## synthesis 08: ooc-tcl-controls

Head: `342f20ef1fb29167c388b6f1fa3bc9851c3876e3`. GNU Make 4.3. Exit: 0.

Working directory: `$LANES/682-pp-pin3`.

```sh
python3 syn/ooc/ooc_tcl_selftest.py
```

Log: `$VALIDATION_STORAGE/682-a554/round2/acceptance/synthesis/08-ooc-tcl-controls.log`; 45 bytes; SHA-256 `c8115f5fe4b9eadf2c9d635505578b1b267023a61a32f8aebff7ad568f0b21eb`.

## synthesis 09: baseline-controls

Head: `342f20ef1fb29167c388b6f1fa3bc9851c3876e3`. GNU Make 4.3. Exit: 0.

Working directory: `$LANES/682-pp-pin3`.

```sh
python3 syn/ooc/pp_baseline.py --selftest
```

Log: `$VALIDATION_STORAGE/682-a554/round2/acceptance/synthesis/09-baseline-controls.log`; 3,552 bytes; SHA-256 `9664efc64a54da38f120bcb6a575568f214243445823ecebfa87e88633475d24`.

## synthesis 10: baseline-mutants

Head: `342f20ef1fb29167c388b6f1fa3bc9851c3876e3`. GNU Make 4.3. Exit: 0.

Working directory: `$LANES/682-pp-pin3`.

```sh
python3 syn/ooc/pp_baseline_mutants.py
```

Log: `$VALIDATION_STORAGE/682-a554/round2/acceptance/synthesis/10-baseline-mutants.log`; 1,262 bytes; SHA-256 `c61da14188c61f28ddce19916a58bcf07e368851751321f9f498dcc6385d2dc4`.

## synthesis 11: baseline-reports

Head: `342f20ef1fb29167c388b6f1fa3bc9851c3876e3`. GNU Make 4.3. Exit: 0.

Working directory: `$LANES/682-pp-pin3`.

```sh
python3 syn/ooc/pp_baseline_reports_selftest.py
```

Log: `$VALIDATION_STORAGE/682-a554/round2/acceptance/synthesis/11-baseline-reports.log`; 96 bytes; SHA-256 `e2b4102612b453b76c0af51f99091bbb1e1a36adafecc9f6c6b8eb345bbc81fe`.

## synthesis 12: resource-controls

Head: `342f20ef1fb29167c388b6f1fa3bc9851c3876e3`. GNU Make 4.3. Exit: 0.

Working directory: `$LANES/682-pp-pin3`.

```sh
python3 syn/ooc/pp_resource_gate.py --selftest
```

Log: `$VALIDATION_STORAGE/682-a554/round2/acceptance/synthesis/12-resource-controls.log`; 25,156 bytes; SHA-256 `160855c6f5d252fde05cf983fe3dd19877501d6587e740deb60fe5ddf7017800`.

## synthesis 13: resource-mutants

Head: `342f20ef1fb29167c388b6f1fa3bc9851c3876e3`. GNU Make 4.3. Exit: 0.

Working directory: `$LANES/682-pp-pin3`.

```sh
python3 syn/ooc/pp_resource_gate_mutants.py
```

Log: `$VALIDATION_STORAGE/682-a554/round2/acceptance/synthesis/13-resource-mutants.log`; 5,862 bytes; SHA-256 `e566898c471e0694e1e7c16accc1c1e30b6b7187dbf9b3282829a8dfd3e4fdf4`.

## synthesis 14: resource-baseline

Head: `342f20ef1fb29167c388b6f1fa3bc9851c3876e3`. GNU Make 4.3. Exit: 0.

Working directory: `$LANES/682-pp-pin3`.

```sh
python3 syn/ooc/pp_resource_gate.py check-baseline
```

Log: `$VALIDATION_STORAGE/682-a554/round2/acceptance/synthesis/14-resource-baseline.log`; 27 bytes; SHA-256 `2114d909e60add091220b415987d4409a611d70c9e84f1bb9e0ae12d6a2f14a0`.

## synthesis 15: dp-sources

Head: `342f20ef1fb29167c388b6f1fa3bc9851c3876e3`. GNU Make 4.3. Exit: 0.

Working directory: `$LANES/682-pp-pin3`.

```sh
python3 syn/ooc/dp_srcs.py --top milan_datapath > /dev/null
python3 syn/ooc/dp_srcs.py --top KL_pp_shadow > /dev/null
```

Log: `$VALIDATION_STORAGE/682-a554/round2/acceptance/synthesis/15-dp-sources.log`; 0 bytes; SHA-256 `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`.

## synthesis 16: yosys-ooc-controls

Head: `342f20ef1fb29167c388b6f1fa3bc9851c3876e3`. GNU Make 4.3. Exit: 0.

Working directory: `$LANES/682-pp-pin3`.

```sh
python3 syn/yosys/ooc_selftest.py
```

Log: `$VALIDATION_STORAGE/682-a554/round2/acceptance/synthesis/16-yosys-ooc-controls.log`; 43 bytes; SHA-256 `d4febc14ba490cf79a72567d657e1653d21792043ae463564d52c831f69179e0`.

## synthesis 17: yosys-cache-controls

Head: `342f20ef1fb29167c388b6f1fa3bc9851c3876e3`. GNU Make 4.3. Exit: 0.

Working directory: `$LANES/682-pp-pin3`.

```sh
python3 syn/yosys/cache_selftest.py
```

Log: `$VALIDATION_STORAGE/682-a554/round2/acceptance/synthesis/17-yosys-cache-controls.log`; 190 bytes; SHA-256 `d8e090cf8c0c656d14381ecbb41901c83ad1870f0f38fed8b382815197e4dfa5`.

## vendor 01: xvlog

Head: `342f20ef1fb29167c388b6f1fa3bc9851c3876e3`. GNU Make 4.3. Exit: 0.

Working directory: `$LANES/682-pp-pin3`.

```sh
test "$(git -C protocol-processor rev-parse --show-toplevel)" = "$PWD/protocol-processor"
python3 scripts/xvlog_gate.py --check
```

Log: `$VALIDATION_STORAGE/682-a554/round2/acceptance/vendor/01-xvlog.log`; 721 bytes; SHA-256 `1c0d7a7bf120fe6c8d00aee69f966596e243b137fea381269c3dc1435c82e8d6`.

## docs-workflow 01: Build the validated HDL reference

Head: `342f20ef1fb29167c388b6f1fa3bc9851c3876e3`. GNU Make 4.3. Exit: 0.

Working directory: `$LANES/682-pp-pin3`.

```sh
set -euo pipefail
python3 -m pip install --quiet --require-hashes \
  -r tools/hdl_reference/requirements.txt
python3 scripts/gen_hdl_reference.py --selftest
python3 scripts/gen_hdl_reference.py \
  --output "$RUNNER_TEMP/milan-hdl-reference"
```

Log: `$VALIDATION_STORAGE/682-a554/round2/docs-workflow/01.log`; 809 bytes; SHA-256 `088fbef396a621eebc5626dd0801c537d6a8e59d7d172713ca16595fc37ba31e`.

## docs-workflow 02: Install the python gate dependencies

Head: `342f20ef1fb29167c388b6f1fa3bc9851c3876e3`. GNU Make 4.3. Exit: 0.

Working directory: `$LANES/682-pp-pin3`.

```sh
python3 -m pip install --quiet pyyaml
```

Log: `$VALIDATION_STORAGE/682-a554/round2/docs-workflow/02.log`; 0 bytes; SHA-256 `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`.

## docs-workflow 03: Install the pinned Markdown renderer

Head: `342f20ef1fb29167c388b6f1fa3bc9851c3876e3`. GNU Make 4.3. Exit: 0.

Working directory: `$LANES/682-pp-pin3`.

```sh
python3 -m pip install --quiet --cache-dir ~/.cache/milan-markdown-pip \
  --require-hashes -r tools/markdown/requirements.txt
```

Log: `$VALIDATION_STORAGE/682-a554/round2/docs-workflow/03.log`; 0 bytes; SHA-256 `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`.

## docs-workflow 04: Install diagram gate dependencies

Head: `342f20ef1fb29167c388b6f1fa3bc9851c3876e3`. GNU Make 4.3. Exit: 0.

Working directory: `$LANES/682-pp-pin3`.

```sh
sudo apt-get update -qq
sudo apt-get install -y --no-install-recommends librsvg2-bin
python3 -m pip install --quiet wavedrom==2.0.3.post3
```

Log: `$VALIDATION_STORAGE/682-a554/round2/docs-workflow/04.log`; 2,323 bytes; SHA-256 `faf885b9b16c31d3e646e863a9b0c209c95dbb81ed14d29ceeb39f4f244c6fe2`.

## docs-workflow 05: Link health, wording, dead-reference and local-info gate

Head: `342f20ef1fb29167c388b6f1fa3bc9851c3876e3`. GNU Make 4.3. Exit: 0.

Working directory: `$LANES/682-pp-pin3`.

```sh
python3 scripts/docs_check.py
```

Log: `$VALIDATION_STORAGE/682-a554/round2/docs-workflow/05.log`; 128 bytes; SHA-256 `95f7175d0c2b4e833c08575992fc43ac2af2b0b20e7e6563042d98d000907a51`.

## docs-workflow 06: Added-line em-dash gate

Head: `342f20ef1fb29167c388b6f1fa3bc9851c3876e3`. GNU Make 4.3. Exit: 0.

Working directory: `$LANES/682-pp-pin3`.

```sh
set -euo pipefail
case "$EVENT_NAME" in
  pull_request)
    if [ -z "$PR_BASE_REF" ]; then
      echo "the pull_request event names no base branch"; exit 2
    fi
    git fetch --quiet origin "$PR_BASE_REF"
    base="$(git merge-base HEAD FETCH_HEAD || true)"
    ;;
  push) base="$PUSH_BEFORE_SHA" ;;
  *) echo "a $EVENT_NAME event carries no base to judge from"; exit 2 ;;
esac
if [ -z "$base" ] || [ "$base" = 0000000000000000000000000000000000000000 ]; then
  echo "the $EVENT_NAME event names no base commit"; exit 2
fi
git cat-file -e "$base^{commit}" 2>/dev/null || git fetch --quiet --depth=1 origin "$base"
python3 scripts/check_em_dash.py --base "$base"
```

Log: `$VALIDATION_STORAGE/682-a554/round2/docs-workflow/06.log`; 140 bytes; SHA-256 `6607028893354f4226637a85f1c81531090904664dc340084585296a11a37772`.

## docs-workflow 07: Concise audience documentation gate

Head: `342f20ef1fb29167c388b6f1fa3bc9851c3876e3`. GNU Make 4.3. Exit: 0.

Working directory: `$LANES/682-pp-pin3`.

```sh
python3 scripts/check_doc_style.py
python3 scripts/check_doc_style.py --selftest
python3 scripts/check_gptp_docs.py
python3 scripts/check_gptp_docs.py --selftest
```

Log: `$VALIDATION_STORAGE/682-a554/round2/docs-workflow/07.log`; 167 bytes; SHA-256 `05d6ef2302a6c0467ad437209233733e93bcb2941539103e26c51b988a28637a`.

## docs-workflow 08: Audience diagram no-drift gate

Head: `342f20ef1fb29167c388b6f1fa3bc9851c3876e3`. GNU Make 4.3. Exit: 0.

Working directory: `$LANES/682-pp-pin3`.

```sh
python3 docs/DOC_MAP.gen.py --check
python3 docs/DOC_MAP.gen.py --selftest
python3 docs/diagrams/timesync_chain.gen.py --check
python3 docs/diagrams/timesync_chain.gen.py --selftest
```

Log: `$VALIDATION_STORAGE/682-a554/round2/docs-workflow/08.log`; 242 bytes; SHA-256 `79dce4dc64e4d57851e37c5bac0a829304d65207659bb65049e11b7d0683f069`.

## docs-workflow 09: Product solution source-fact gate

Head: `342f20ef1fb29167c388b6f1fa3bc9851c3876e3`. GNU Make 4.3. Exit: 0.

Working directory: `$LANES/682-pp-pin3`.

```sh
python3 scripts/check_solution_docs.py
python3 scripts/check_solution_docs.py --selftest
```

Log: `$VALIDATION_STORAGE/682-a554/round2/docs-workflow/09.log`; 146 bytes; SHA-256 `9ef43cc924919e10ccb30a9419819d20b849d787a8f37fcabba22e2159d3167d`.

## docs-workflow 10: Verified submodule documentation gate

Head: `342f20ef1fb29167c388b6f1fa3bc9851c3876e3`. GNU Make 4.3. Exit: 0.

Working directory: `$LANES/682-pp-pin3`.

```sh
python3 docs/diagrams/submodule_boundaries.gen.py --check
python3 docs/diagrams/submodule_boundaries.gen.py --selftest
python3 scripts/check_submodule_docs.py
python3 scripts/check_submodule_docs.py --selftest
```

Log: `$VALIDATION_STORAGE/682-a554/round2/docs-workflow/10.log`; 227 bytes; SHA-256 `cd9f3e7404ce8e884eded8567a1b2560dc22cc7a4b5796601edb295cb725cc64`.

## docs-workflow 11: HDL timing diagram no-drift gate

Head: `342f20ef1fb29167c388b6f1fa3bc9851c3876e3`. GNU Make 4.3. Exit: 0.

Working directory: `$LANES/682-pp-pin3`.

```sh
python3 scripts/gen_wavedrom.py --selftest
python3 scripts/gen_wavedrom.py docs/diagrams/wd_axis_backpressure.json --background=white --check
python3 scripts/gen_wavedrom.py docs/diagrams/wd_cdc_handshake.json --background=white --check
python3 scripts/gen_wavedrom.py docs/diagrams/wd_gptp_pdelay.json --background=white --check
```

Log: `$VALIDATION_STORAGE/682-a554/round2/docs-workflow/11.log`; 241 bytes; SHA-256 `af9493d0e4acd65eb64ba2bbe7103a2c6f957ecca650a938cdc18d70396a57ea`.

## docs-workflow 12: Published diagram PNG gate

Head: `342f20ef1fb29167c388b6f1fa3bc9851c3876e3`. GNU Make 4.3. Exit: 0.

Working directory: `$LANES/682-pp-pin3`.

```sh
python3 scripts/check_diagram_pngs.py
python3 scripts/check_diagram_pngs.py --selftest
```

Log: `$VALIDATION_STORAGE/682-a554/round2/docs-workflow/12.log`; 125 bytes; SHA-256 `17d1d2360a98e818f8706a8165affff7c873cb06b4fe8db4c48300e103e51c1e`.

## docs-workflow 13: Milan feature-status consistency gate

Head: `342f20ef1fb29167c388b6f1fa3bc9851c3876e3`. GNU Make 4.3. Exit: 0.

Working directory: `$LANES/682-pp-pin3`.

```sh
python3 scripts/check_feature_status.py --self-test
```

Log: `$VALIDATION_STORAGE/682-a554/round2/docs-workflow/13.log`; 1,500 bytes; SHA-256 `77f7649b1865c0daf4f3de04dd18c78be4885c9c94a8f03fd1e4f262758c3184`.

## docs-workflow 14: Traceability matrix no-drift gate

Head: `342f20ef1fb29167c388b6f1fa3bc9851c3876e3`. GNU Make 4.3. Exit: 0.

Working directory: `$LANES/682-pp-pin3`.

```sh
python3 docs/traceability/gen_module_matrix.py --check
```

Log: `$VALIDATION_STORAGE/682-a554/round2/docs-workflow/14.log`; 118 bytes; SHA-256 `d0be3b6428ae2079134f2a21b2972c524a26103b0e9c8b64039bb24ae22797dc`.

## docs-workflow 15: Fetch the builder source dependencies

Head: `342f20ef1fb29167c388b6f1fa3bc9851c3876e3`. GNU Make 4.3. Exit: 0.

Working directory: `$LANES/682-pp-pin3`.

```sh
git submodule update --init third_party/verilog-axis protocol-processor gptp-processor
```

Log: `$VALIDATION_STORAGE/682-a554/round2/docs-workflow/15.log`; 0 bytes; SHA-256 `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`.

## docs-workflow 16: Imported gPTP documentation gate

Head: `342f20ef1fb29167c388b6f1fa3bc9851c3876e3`. GNU Make 4.3. Exit: 0.

Working directory: `$LANES/682-pp-pin3`.

```sh
python3 scripts/check_gptp_docs.py --with-submodule
make -C gptp-processor docs
```

Log: `$VALIDATION_STORAGE/682-a554/round2/docs-workflow/16.log`; 2,736 bytes; SHA-256 `2ee7c1389f730f5d60e04123c4e7b04cd555da58393dccf27b73d1265fc5d481`.

## docs-workflow 17: Code-quality measurement self-tests

Head: `342f20ef1fb29167c388b6f1fa3bc9851c3876e3`. GNU Make 4.3. Exit: 0.

Working directory: `$LANES/682-pp-pin3`.

```sh
python3 scripts/measure_control_flow.py --selftest
python3 scripts/measure_cohesion.py --selftest
```

Log: `$VALIDATION_STORAGE/682-a554/round2/docs-workflow/17.log`; 3,293 bytes; SHA-256 `862838344ece59e4179fd4bcfe04f85ee320f0601c325014b2509717db13368b`.

## docs-workflow 18: Install the pinned sv2v release

Head: `342f20ef1fb29167c388b6f1fa3bc9851c3876e3`. GNU Make 4.3. Exit: 0.

Working directory: `$LANES/682-pp-pin3`.

```sh
set -euo pipefail
ver=v0.0.12
sha256=ff8c9eea5bc029b372fb4953427625cddb7cf7e58c1240623ac9f260818d5a00
url="https://github.com/zachjs/sv2v/releases/download/${ver}/sv2v-Linux.zip"
curl -fsSL "$url" -o /tmp/sv2v.zip
echo "${sha256}  /tmp/sv2v.zip" | sha256sum -c -
unzip -q -o /tmp/sv2v.zip -d /tmp/sv2v
sudo install -m755 "$(find /tmp/sv2v -name sv2v -type f | head -1)" \
  /usr/local/bin/sv2v
sv2v --version
```

Log: `$VALIDATION_STORAGE/682-a554/round2/docs-workflow/18.log`; 31 bytes; SHA-256 `176b5effd5ab230db92a3088fc5e8a688744dc1203991c6e71b25f2a29925e0d`.

## docs-workflow 19: Bare-metal scope gate

Head: `342f20ef1fb29167c388b6f1fa3bc9851c3876e3`. GNU Make 4.3. Exit: 0.

Working directory: `$LANES/682-pp-pin3`.

```sh
python3 scripts/check_baremetal_only.py --check
python3 scripts/check_baremetal_only.py --selftest
```

Log: `$VALIDATION_STORAGE/682-a554/round2/docs-workflow/19.log`; 115 bytes; SHA-256 `950de2aeb3a9f18d708c04f4f31b457b937373e7d920ffb598868e673ef6da5d`.

## docs-workflow 20: Install and verify the pinned RV32 SDK

Head: `342f20ef1fb29167c388b6f1fa3bc9851c3876e3`. GNU Make 4.3. Exit: 0.

Working directory: `$LANES/682-pp-pin3`.

```sh
set -euo pipefail
python3 scripts/ci_rv32_sdk_selftest.py
python3 scripts/ci_rv32_sdk.py --destination "$HOME/br-milan-rv32/host"
```

Log: `$VALIDATION_STORAGE/682-a554/round2/docs-workflow/20.log`; 8,119 bytes; SHA-256 `e5a75a51015c2695e39c9bbac61e1210aac769d1961f83c9f5b7dd9ce43684d6`.

## docs-workflow 21: Compiler-absent firmware controls

Head: `342f20ef1fb29167c388b6f1fa3bc9851c3876e3`. GNU Make 4.3. Exit: 0.

Working directory: `$LANES/682-pp-pin3`.

```sh
set -euo pipefail
python3 sw/builder/test_firmware_compiler.py --selftest
python3 sw/builder/test_firmware_compiler.py --absent --audit "$RUNNER_TEMP/rv32-absent.jsonl"
```

Log: `$VALIDATION_STORAGE/682-a554/round2/docs-workflow/21.log`; 52,033 bytes; SHA-256 `728dd6b0e10d09010be54fc357ce9594e10241d44d28b85039c6ac7bd26e0b6b`.

## docs-workflow 22: End-station builder gates

Head: `342f20ef1fb29167c388b6f1fa3bc9851c3876e3`. GNU Make 4.3. Exit: 0.

Working directory: `$LANES/682-pp-pin3`.

```sh
python3 -m pip install --quiet pyyaml
python3 sw/builder/test_builder.py --require-rv32
```

Log: `$VALIDATION_STORAGE/682-a554/round2/docs-workflow/22.log`; 101,744 bytes; SHA-256 `5a51c21a9d801b84984728c0cb22d5b75f28d06a134b418964631eb77f405a7b`.

## docs-workflow 23: NVM record-space gate

Head: `342f20ef1fb29167c388b6f1fa3bc9851c3876e3`. GNU Make 4.3. Exit: 0.

Working directory: `$LANES/682-pp-pin3`.

```sh
python3 scripts/check_nvm_record_space.py
python3 scripts/check_nvm_record_space.py --self-test
```

Log: `$VALIDATION_STORAGE/682-a554/round2/docs-workflow/23.log`; 9,588 bytes; SHA-256 `7969fb65ae1ea9d608146bed63d697587402331dc1efa2c128e61861a7f6493e`.

## docs-workflow 24: Capture measurement census and clock gate

Head: `342f20ef1fb29167c388b6f1fa3bc9851c3876e3`. GNU Make 4.3. Exit: 0.

Working directory: `$LANES/682-pp-pin3`.

```sh
python3 scripts/check_nvm_capture.py
```

Log: `$VALIDATION_STORAGE/682-a554/round2/docs-workflow/24.log`; 324 bytes; SHA-256 `9a4196c774ce4ddfa9980cf9345d111028f3afa812677fe5bab392f81c955439`.

## docs-workflow 25: Saved-state writer gate

Head: `342f20ef1fb29167c388b6f1fa3bc9851c3876e3`. GNU Make 4.3. Exit: 0.

Working directory: `$LANES/682-pp-pin3`.

```sh
python3 sw/firmware/nvm_hosttest/test_nvm_firmware.py --self-test
```

Log: `$VALIDATION_STORAGE/682-a554/round2/docs-workflow/25.log`; 5,189 bytes; SHA-256 `cba18482dbf27c70ee56b28a8fbbe7bfdc2cc49b4644a42daa5ad4db8f6d4972`.

## docs-workflow 26: SoC source-list gate (Vivado would fail 40 min in without this)

Head: `342f20ef1fb29167c388b6f1fa3bc9851c3876e3`. GNU Make 4.3. Exit: 0.

Working directory: `$LANES/682-pp-pin3`.

```sh
python3 scripts/check_soc_sources.py
python3 scripts/check_soc_sources.py --selftest
command -v tclsh >/dev/null || {
  sudo apt-get update -qq
  sudo apt-get install -y --no-install-recommends tcl
}
python3 sw/litex/iob_pack_selftest.py
```

Log: `$VALIDATION_STORAGE/682-a554/round2/docs-workflow/26.log`; 4,733 bytes; SHA-256 `7c34f57b723fa707a2eadc1915b61980ed407fd0cf480238032e391030f053f9`.

## docs-workflow 27: RTL source-list drift gate

Head: `342f20ef1fb29167c388b6f1fa3bc9851c3876e3`. GNU Make 4.3. Exit: 0.

Working directory: `$LANES/682-pp-pin3`.

```sh
python3 scripts/check_rtl_source_lists.py
python3 scripts/check_rtl_source_lists.py --selftest
```

Log: `$VALIDATION_STORAGE/682-a554/round2/docs-workflow/27.log`; 3,453 bytes; SHA-256 `be8805dc2fee50eddcf0b966ea5728febdeed2e7b9f288ba358f41c1fe4b7041`.

## docs-workflow 28: Boundary-unit naming ratchet

Head: `342f20ef1fb29167c388b6f1fa3bc9851c3876e3`. GNU Make 4.3. Exit: 0.

Working directory: `$LANES/682-pp-pin3`.

```sh
python3 scripts/measure_naming.py --check
python3 scripts/measure_naming.py --selftest
```

Log: `$VALIDATION_STORAGE/682-a554/round2/docs-workflow/28.log`; 40,634 bytes; SHA-256 `3d6d291b5e41999df546421642ddf9cc98237dcdea8d047c54edf0e9a7089f3e`.

## docs-workflow 29: Port contract gate

Head: `342f20ef1fb29167c388b6f1fa3bc9851c3876e3`. GNU Make 4.3. Exit: 0.

Working directory: `$LANES/682-pp-pin3`.

```sh
python3 scripts/check_port_contracts.py
python3 scripts/check_port_contracts.py --selftest
```

Log: `$VALIDATION_STORAGE/682-a554/round2/docs-workflow/29.log`; 5,040 bytes; SHA-256 `ce53539b1c4806c705ca06eead5c465effd50782d8393272c91afcbdd93d59d1`.

## docs-workflow 30: Fail-fast ratchet

Head: `342f20ef1fb29167c388b6f1fa3bc9851c3876e3`. GNU Make 4.3. Exit: 0.

Working directory: `$LANES/682-pp-pin3`.

```sh
python3 scripts/measure_fail_fast.py --check
python3 scripts/measure_fail_fast.py --selftest
```

Log: `$VALIDATION_STORAGE/682-a554/round2/docs-workflow/30.log`; 12,682 bytes; SHA-256 `3fbed56aa0724496465ce6f185d931ddb1a3ee49bb28a1ff77e1051981a700dd`.

## docs-workflow 31: TODO ownership gate

Head: `342f20ef1fb29167c388b6f1fa3bc9851c3876e3`. GNU Make 4.3. Exit: 0.

Working directory: `$LANES/682-pp-pin3`.

```sh
python3 scripts/check_todo_ownership.py
python3 scripts/check_todo_ownership.py --selftest
```

Log: `$VALIDATION_STORAGE/682-a554/round2/docs-workflow/31.log`; 2,745 bytes; SHA-256 `3b70a725de2fda0df9f14fee49a3c84a53dcbe768f04e8e3558005bab8ac7999`.

## docs-workflow 32: Test-evidence ratchet

Head: `342f20ef1fb29167c388b6f1fa3bc9851c3876e3`. GNU Make 4.3. Exit: 0.

Working directory: `$LANES/682-pp-pin3`.

```sh
python3 scripts/measure_test_evidence.py --check
python3 scripts/measure_test_evidence.py --selftest
```

Log: `$VALIDATION_STORAGE/682-a554/round2/docs-workflow/32.log`; 20,766 bytes; SHA-256 `6162e40a0b084c014771b2f9a22fcbaf6fa61f425fac6dfe2cd03604e6f2ce65`.

## docs-workflow 33: Mechanical hygiene ratchet

Head: `342f20ef1fb29167c388b6f1fa3bc9851c3876e3`. GNU Make 4.3. Exit: 0.

Working directory: `$LANES/682-pp-pin3`.

```sh
python3 scripts/check_hygiene.py --check
python3 scripts/check_hygiene.py --selftest
```

Log: `$VALIDATION_STORAGE/682-a554/round2/docs-workflow/33.log`; 3,845 bytes; SHA-256 `421bda4ac43de970c5a077837255b31d6e7d9ef31d8eea9139ac3d79793eae30`.

## docs-workflow 34: SystemVerilog idiom gate

Head: `342f20ef1fb29167c388b6f1fa3bc9851c3876e3`. GNU Make 4.3. Exit: 0.

Working directory: `$LANES/682-pp-pin3`.

```sh
python3 scripts/check_sv_idiom.py
python3 scripts/check_sv_idiom.py --selftest
```

Log: `$VALIDATION_STORAGE/682-a554/round2/docs-workflow/34.log`; 3,173 bytes; SHA-256 `ccd900273b796fdfcf74e586f952eadfc9f6f6b1ad448b891183f939a49df728`.

## docs-workflow 35: C and C++ idiom gate

Head: `342f20ef1fb29167c388b6f1fa3bc9851c3876e3`. GNU Make 4.3. Exit: 0.

Working directory: `$LANES/682-pp-pin3`.

```sh
python3 scripts/check_cpp_idiom.py
python3 scripts/check_cpp_idiom.py --selftest
```

Log: `$VALIDATION_STORAGE/682-a554/round2/docs-workflow/35.log`; 3,909 bytes; SHA-256 `bc6066d1b32fae4b0b50356485841a20e4d2cc6e776dd1c77a856b17e7d6ea01`.

## docs-workflow 36: Python idiom gate

Head: `342f20ef1fb29167c388b6f1fa3bc9851c3876e3`. GNU Make 4.3. Exit: 0.

Working directory: `$LANES/682-pp-pin3`.

```sh
python3 scripts/check_py_idiom.py
python3 scripts/check_py_idiom.py --selftest
```

Log: `$VALIDATION_STORAGE/682-a554/round2/docs-workflow/36.log`; 2,992 bytes; SHA-256 `9e42c4fc44579972e35b868bd73766c5f443532ca7ab1444c33c8a387a3baa24`.

## docs-workflow 37: Shell idiom gate

Head: `342f20ef1fb29167c388b6f1fa3bc9851c3876e3`. GNU Make 4.3. Exit: 0.

Working directory: `$LANES/682-pp-pin3`.

```sh
python3 scripts/check_sh_idiom.py
python3 scripts/check_sh_idiom.py --selftest
```

Log: `$VALIDATION_STORAGE/682-a554/round2/docs-workflow/37.log`; 2,696 bytes; SHA-256 `a57f331056f1f93e369a05fc919fd7d91a98638253282a970a118711a46e20e1`.

## docs-workflow 38: CI event and SHA contract gate

Head: `342f20ef1fb29167c388b6f1fa3bc9851c3876e3`. GNU Make 4.3. Exit: 0.

Working directory: `$LANES/682-pp-pin3`.

```sh
python3 scripts/ci_events.py --check
python3 scripts/ci_events.py --selftest
```

Log: `$VALIDATION_STORAGE/682-a554/round2/docs-workflow/38.log`; 150,954 bytes; SHA-256 `3767e4f29189dd88f59c1a5f47af09c982a473198e6dec7211e769d5cb19088c`.

## docs-workflow 39: Local act runner contract gate

Head: `342f20ef1fb29167c388b6f1fa3bc9851c3876e3`. GNU Make 4.3. Exit: 0.

Working directory: `$LANES/682-pp-pin3`.

```sh
python3 scripts/act_ci.py --selftest
```

Log: `$VALIDATION_STORAGE/682-a554/round2/docs-workflow/39.log`; 36,483 bytes; SHA-256 `876a6eca5975005e4e1d1ddddad9f74d2443039a10df8b7f590e4c781632fdab`.

## docs-workflow 40: Doc cited-path gate

Head: `342f20ef1fb29167c388b6f1fa3bc9851c3876e3`. GNU Make 4.3. Exit: 0.

Working directory: `$LANES/682-pp-pin3`.

```sh
python3 scripts/check_doc_paths.py
```

Log: `$VALIDATION_STORAGE/682-a554/round2/docs-workflow/40.log`; 85 bytes; SHA-256 `14e8073fd597e8c2e74483ee4f15374aa0f669038c0af1acafb7b47d130467ff`.

## docs-workflow 41: Archive integrity gate

Head: `342f20ef1fb29167c388b6f1fa3bc9851c3876e3`. GNU Make 4.3. Exit: 0.

Working directory: `$LANES/682-pp-pin3`.

```sh
python3 scripts/check_archive.py
python3 scripts/check_archive.py --selftest
```

Log: `$VALIDATION_STORAGE/682-a554/round2/docs-workflow/41.log`; 128 bytes; SHA-256 `1a15e66a07892f544c4b9bee75201ff9acaf3edd2c37963a780f8473466d50cb`.

## docs-workflow 42: Per-page contents gate

Head: `342f20ef1fb29167c388b6f1fa3bc9851c3876e3`. GNU Make 4.3. Exit: 0.

Working directory: `$LANES/682-pp-pin3`.

```sh
python3 scripts/gen_toc.py --selftest
python3 scripts/gen_toc.py --verify-anchors
python3 scripts/gen_toc.py --check
```

Log: `$VALIDATION_STORAGE/682-a554/round2/docs-workflow/42.log`; 196 bytes; SHA-256 `ff56ad0513c9dee04354e1aca0d5cb8a1ca6fca74da4e8fc69ca6a2c15ea77c6`.

## docs-workflow 43: AEM store generator self-test

Head: `342f20ef1fb29167c388b6f1fa3bc9851c3876e3`. GNU Make 4.3. Exit: 0.

Working directory: `$LANES/682-pp-pin3`.

```sh
python3 avdecc/gen_aem_store.py --self-test
```

Log: `$VALIDATION_STORAGE/682-a554/round2/docs-workflow/43.log`; 3,596 bytes; SHA-256 `9f126bf9dfc7cb552a2414b98d2792449dc4ae126395997750d5039cb896f022`.

## docs-workflow 44: Sweep/build shape gate

Head: `342f20ef1fb29167c388b6f1fa3bc9851c3876e3`. GNU Make 4.3. Exit: 0.

Working directory: `$LANES/682-pp-pin3`.

```sh
python3 scripts/check_sweep_shape.py --self-test
```

Log: `$VALIDATION_STORAGE/682-a554/round2/docs-workflow/44.log`; 19,682 bytes; SHA-256 `54e5aef2df2f176d77be448d61334a42e1349f9fab02bd5cfd5b46d2cb30870d`.

## docs-workflow 45: Deploy shape gate

Head: `342f20ef1fb29167c388b6f1fa3bc9851c3876e3`. GNU Make 4.3. Exit: 0.

Working directory: `$LANES/682-pp-pin3`.

```sh
python3 scripts/check_deploy_shape.py --self-test
```

Log: `$VALIDATION_STORAGE/682-a554/round2/docs-workflow/45.log`; 9,270 bytes; SHA-256 `6e4bb815d4a015fc437da1e1584f8755b4feba5ab5272421126ca193b0a58610`.

## docs-workflow 46: Entity shape gate

Head: `342f20ef1fb29167c388b6f1fa3bc9851c3876e3`. GNU Make 4.3. Exit: 0.

Working directory: `$LANES/682-pp-pin3`.

```sh
python3 scripts/check_entity_shape.py --self-test
```

Log: `$VALIDATION_STORAGE/682-a554/round2/docs-workflow/46.log`; 25,694 bytes; SHA-256 `7c1cc4d5ce778537bd27790e075eb0d8159cf6c1281870eb96142e9465eff19c`.

## docs-workflow 47: Fetch the engine authority the builder derives from

Head: `342f20ef1fb29167c388b6f1fa3bc9851c3876e3`. GNU Make 4.3. Exit: 0.

Working directory: `$LANES/682-pp-pin3`.

```sh
git submodule update --init gptp-processor
```

Log: `$VALIDATION_STORAGE/682-a554/round2/docs-workflow/47.log`; 0 bytes; SHA-256 `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`.

## docs-workflow 48: Advertised-vs-emitted gate (green since 2026-07-28, item 00)

Head: `342f20ef1fb29167c388b6f1fa3bc9851c3876e3`. GNU Make 4.3. Exit: 0.

Working directory: `$LANES/682-pp-pin3`.

```sh
python3 -m pip install --quiet pyyaml
python3 scripts/check_wire_accountability.py --self-test
```

Log: `$VALIDATION_STORAGE/682-a554/round2/docs-workflow/48.log`; 4,965 bytes; SHA-256 `bd97b8b53304baf2b912ac2e4ec507e3b8f9ae4c5c2511b5dc69a41d2cbdd3d4`.

## docs-workflow 49: Strip git metadata, then run the docs gate

Head: `342f20ef1fb29167c388b6f1fa3bc9851c3876e3`. GNU Make 4.3. Exit: 0.

Working directory: `$VALIDATION_STORAGE/682-a554/round2/docs-no-git`.

```sh
rm -rf .git
python3 scripts/docs_check.py
python3 scripts/check_feature_status.py
```

Log: `$VALIDATION_STORAGE/682-a554/round2/docs-workflow/49.log`; 225 bytes; SHA-256 `48a2b69085b306b603be36ddfe94d2b095006d8d0fb247f6d0e0d2d9a9f8492c`.

## render 01: adopted-full

Head: `342f20ef1fb29167c388b6f1fa3bc9851c3876e3`. GNU Make 4.3. Exit: 2.

Working directory: `$LANES/682-pp-pin3`.

Expected retained #657 failures; accepted only through the separate passing differential under the public round-2 ruling. Prior runs use exactly the old gitlink and both patches reversed; full campaigns retain actual leg stdout.

```sh
make -C tb/verilator/milan_dp_render tdm8render-mutants
```

Log: `$VALIDATION_STORAGE/682-a554/round2/render/adopted/full.log`; 134,918 bytes; SHA-256 `8d8fb709a0a811ec8a7c619fabcf1de9f2ef4a02733c2e1e87284eca5afc53a0`.

## render 02: adopted-cases

Head: `342f20ef1fb29167c388b6f1fa3bc9851c3876e3`. GNU Make 4.3. Exit: 1.

Working directory: `$LANES/682-pp-pin3`.

Expected retained #657 failures; accepted only through the separate passing differential under the public round-2 ruling. Prior runs use exactly the old gitlink and both patches reversed; full campaigns retain actual leg stdout.

```sh
python3 $VALIDATION_STORAGE/682-a554/round2/render-recheck.py adopted
```

Log: `$VALIDATION_STORAGE/682-a554/round2/render/adopted/cases.log`; 437 bytes; SHA-256 `2626f1c1a06e51ff3a5556a8723907878270ff191cfe05386159b689cf219729`.

## render 03: prior-full

Head: `342f20ef1fb29167c388b6f1fa3bc9851c3876e3`. GNU Make 4.3. Exit: 2.

Working directory: `$LANES/682-pp-pin3`.

Expected retained #657 failures; accepted only through the separate passing differential under the public round-2 ruling. Prior runs use exactly the old gitlink and both patches reversed; full campaigns retain actual leg stdout.

```sh
make -C tb/verilator/milan_dp_render tdm8render-mutants
```

Log: `$VALIDATION_STORAGE/682-a554/round2/render/prior/full.log`; 141,894 bytes; SHA-256 `327a984fb0bb8b7424d45de3d4be9e5ed5caf1286c80616ea01493d8f97baf3c`.

## render 04: prior-cases

Head: `342f20ef1fb29167c388b6f1fa3bc9851c3876e3`. GNU Make 4.3. Exit: 1.

Working directory: `$LANES/682-pp-pin3`.

Expected retained #657 failures; accepted only through the separate passing differential under the public round-2 ruling. Prior runs use exactly the old gitlink and both patches reversed; full campaigns retain actual leg stdout.

```sh
python3 $VALIDATION_STORAGE/682-a554/round2/render-recheck.py prior
```

Log: `$VALIDATION_STORAGE/682-a554/round2/render/prior/cases.log`; 437 bytes; SHA-256 `2626f1c1a06e51ff3a5556a8723907878270ff191cfe05386159b689cf219729`.

## render 05: differential

Head: `342f20ef1fb29167c388b6f1fa3bc9851c3876e3`. GNU Make 4.3. Exit: 0.

Working directory: `$LANES/682-pp-pin3`.

Acceptance 4 render result: unchanged from dev; #657. Both full campaigns, all 32 verdicts, all four failure cases, assertions and counts, and actual clean-epoch bytes agree.

```sh
python3 $VALIDATION_STORAGE/682-a554/round2/compare-render.py
```

Log: `$VALIDATION_STORAGE/682-a554/round2/render/differential.log`; 323 bytes; SHA-256 `279ca0d303c5ca031aa4bb1ca04d6ffa405174283e8660bdcf3bce731b946175`.

## final-docs-workflow 01: Build the validated HDL reference

Head: `591a5752e6a587b28b501e2d02d6a9d0293f3ba2`. GNU Make 4.3. Exit: 0.

Working directory: `$LANES/682-pp-pin3`.

```sh
set -euo pipefail
python3 -m pip install --quiet --require-hashes \
  -r tools/hdl_reference/requirements.txt
python3 scripts/gen_hdl_reference.py --selftest
python3 scripts/gen_hdl_reference.py \
  --output "$RUNNER_TEMP/milan-hdl-reference"
```

Log: `$VALIDATION_STORAGE/682-a554/round2/final/docs-workflow/01.log`; 815 bytes; SHA-256 `3f0b6e69b6eaea619c7739b8968fd8acb93de4ba8ceb1593e5ea2e79719a54c3`.

## final-docs-workflow 02: Install the python gate dependencies

Head: `591a5752e6a587b28b501e2d02d6a9d0293f3ba2`. GNU Make 4.3. Exit: 0.

Working directory: `$LANES/682-pp-pin3`.

```sh
python3 -m pip install --quiet pyyaml
```

Log: `$VALIDATION_STORAGE/682-a554/round2/final/docs-workflow/02.log`; 0 bytes; SHA-256 `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`.

## final-docs-workflow 03: Install the pinned Markdown renderer

Head: `591a5752e6a587b28b501e2d02d6a9d0293f3ba2`. GNU Make 4.3. Exit: 0.

Working directory: `$LANES/682-pp-pin3`.

```sh
python3 -m pip install --quiet --cache-dir ~/.cache/milan-markdown-pip \
  --require-hashes -r tools/markdown/requirements.txt
```

Log: `$VALIDATION_STORAGE/682-a554/round2/final/docs-workflow/03.log`; 0 bytes; SHA-256 `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`.

## final-docs-workflow 04: Install diagram gate dependencies

Head: `591a5752e6a587b28b501e2d02d6a9d0293f3ba2`. GNU Make 4.3. Exit: 0.

Working directory: `$LANES/682-pp-pin3`.

```sh
sudo apt-get update -qq
sudo apt-get install -y --no-install-recommends librsvg2-bin
python3 -m pip install --quiet wavedrom==2.0.3.post3
```

Log: `$VALIDATION_STORAGE/682-a554/round2/final/docs-workflow/04.log`; 2,323 bytes; SHA-256 `b2e81dfc1cdaccffe8cc4797206bff45b6ac7062f46fa28d2934487412bd5909`.

## final-docs-workflow 05: Link health, wording, dead-reference and local-info gate

Head: `591a5752e6a587b28b501e2d02d6a9d0293f3ba2`. GNU Make 4.3. Exit: 0.

Working directory: `$LANES/682-pp-pin3`.

```sh
python3 scripts/docs_check.py
```

Log: `$VALIDATION_STORAGE/682-a554/round2/final/docs-workflow/05.log`; 128 bytes; SHA-256 `fc436feec99782d1c4b428f118726d0c38006a1c13747c8dad0e204129beda64`.

## final-docs-workflow 06: Added-line em-dash gate

Head: `591a5752e6a587b28b501e2d02d6a9d0293f3ba2`. GNU Make 4.3. Exit: 0.

Working directory: `$LANES/682-pp-pin3`.

```sh
set -euo pipefail
case "$EVENT_NAME" in
  pull_request)
    if [ -z "$PR_BASE_REF" ]; then
      echo "the pull_request event names no base branch"; exit 2
    fi
    git fetch --quiet origin "$PR_BASE_REF"
    base="$(git merge-base HEAD FETCH_HEAD || true)"
    ;;
  push) base="$PUSH_BEFORE_SHA" ;;
  *) echo "a $EVENT_NAME event carries no base to judge from"; exit 2 ;;
esac
if [ -z "$base" ] || [ "$base" = 0000000000000000000000000000000000000000 ]; then
  echo "the $EVENT_NAME event names no base commit"; exit 2
fi
git cat-file -e "$base^{commit}" 2>/dev/null || git fetch --quiet --depth=1 origin "$base"
python3 scripts/check_em_dash.py --base "$base"
```

Log: `$VALIDATION_STORAGE/682-a554/round2/final/docs-workflow/06.log`; 140 bytes; SHA-256 `86bf2eb3b4a40f9719621e7df026a43789789318b5c7d214b81a1579a199f316`.

## final-docs-workflow 07: Concise audience documentation gate

Head: `591a5752e6a587b28b501e2d02d6a9d0293f3ba2`. GNU Make 4.3. Exit: 0.

Working directory: `$LANES/682-pp-pin3`.

```sh
python3 scripts/check_doc_style.py
python3 scripts/check_doc_style.py --selftest
python3 scripts/check_gptp_docs.py
python3 scripts/check_gptp_docs.py --selftest
```

Log: `$VALIDATION_STORAGE/682-a554/round2/final/docs-workflow/07.log`; 167 bytes; SHA-256 `05d6ef2302a6c0467ad437209233733e93bcb2941539103e26c51b988a28637a`.

## final-docs-workflow 08: Audience diagram no-drift gate

Head: `591a5752e6a587b28b501e2d02d6a9d0293f3ba2`. GNU Make 4.3. Exit: 0.

Working directory: `$LANES/682-pp-pin3`.

```sh
python3 docs/DOC_MAP.gen.py --check
python3 docs/DOC_MAP.gen.py --selftest
python3 docs/diagrams/timesync_chain.gen.py --check
python3 docs/diagrams/timesync_chain.gen.py --selftest
```

Log: `$VALIDATION_STORAGE/682-a554/round2/final/docs-workflow/08.log`; 242 bytes; SHA-256 `79dce4dc64e4d57851e37c5bac0a829304d65207659bb65049e11b7d0683f069`.

## final-docs-workflow 09: Product solution source-fact gate

Head: `591a5752e6a587b28b501e2d02d6a9d0293f3ba2`. GNU Make 4.3. Exit: 0.

Working directory: `$LANES/682-pp-pin3`.

```sh
python3 scripts/check_solution_docs.py
python3 scripts/check_solution_docs.py --selftest
```

Log: `$VALIDATION_STORAGE/682-a554/round2/final/docs-workflow/09.log`; 146 bytes; SHA-256 `9ef43cc924919e10ccb30a9419819d20b849d787a8f37fcabba22e2159d3167d`.

## final-docs-workflow 10: Verified submodule documentation gate

Head: `591a5752e6a587b28b501e2d02d6a9d0293f3ba2`. GNU Make 4.3. Exit: 0.

Working directory: `$LANES/682-pp-pin3`.

```sh
python3 docs/diagrams/submodule_boundaries.gen.py --check
python3 docs/diagrams/submodule_boundaries.gen.py --selftest
python3 scripts/check_submodule_docs.py
python3 scripts/check_submodule_docs.py --selftest
```

Log: `$VALIDATION_STORAGE/682-a554/round2/final/docs-workflow/10.log`; 227 bytes; SHA-256 `cd9f3e7404ce8e884eded8567a1b2560dc22cc7a4b5796601edb295cb725cc64`.

## final-docs-workflow 11: HDL timing diagram no-drift gate

Head: `591a5752e6a587b28b501e2d02d6a9d0293f3ba2`. GNU Make 4.3. Exit: 0.

Working directory: `$LANES/682-pp-pin3`.

```sh
python3 scripts/gen_wavedrom.py --selftest
python3 scripts/gen_wavedrom.py docs/diagrams/wd_axis_backpressure.json --background=white --check
python3 scripts/gen_wavedrom.py docs/diagrams/wd_cdc_handshake.json --background=white --check
python3 scripts/gen_wavedrom.py docs/diagrams/wd_gptp_pdelay.json --background=white --check
```

Log: `$VALIDATION_STORAGE/682-a554/round2/final/docs-workflow/11.log`; 241 bytes; SHA-256 `af9493d0e4acd65eb64ba2bbe7103a2c6f957ecca650a938cdc18d70396a57ea`.

## final-docs-workflow 12: Published diagram PNG gate

Head: `591a5752e6a587b28b501e2d02d6a9d0293f3ba2`. GNU Make 4.3. Exit: 0.

Working directory: `$LANES/682-pp-pin3`.

```sh
python3 scripts/check_diagram_pngs.py
python3 scripts/check_diagram_pngs.py --selftest
```

Log: `$VALIDATION_STORAGE/682-a554/round2/final/docs-workflow/12.log`; 125 bytes; SHA-256 `17d1d2360a98e818f8706a8165affff7c873cb06b4fe8db4c48300e103e51c1e`.

## final-docs-workflow 13: Milan feature-status consistency gate

Head: `591a5752e6a587b28b501e2d02d6a9d0293f3ba2`. GNU Make 4.3. Exit: 0.

Working directory: `$LANES/682-pp-pin3`.

```sh
python3 scripts/check_feature_status.py --self-test
```

Log: `$VALIDATION_STORAGE/682-a554/round2/final/docs-workflow/13.log`; 1,500 bytes; SHA-256 `77f7649b1865c0daf4f3de04dd18c78be4885c9c94a8f03fd1e4f262758c3184`.

## final-docs-workflow 14: Traceability matrix no-drift gate

Head: `591a5752e6a587b28b501e2d02d6a9d0293f3ba2`. GNU Make 4.3. Exit: 0.

Working directory: `$LANES/682-pp-pin3`.

```sh
python3 docs/traceability/gen_module_matrix.py --check
```

Log: `$VALIDATION_STORAGE/682-a554/round2/final/docs-workflow/14.log`; 118 bytes; SHA-256 `d0be3b6428ae2079134f2a21b2972c524a26103b0e9c8b64039bb24ae22797dc`.

## final-docs-workflow 15: Fetch the builder source dependencies

Head: `591a5752e6a587b28b501e2d02d6a9d0293f3ba2`. GNU Make 4.3. Exit: 0.

Working directory: `$LANES/682-pp-pin3`.

```sh
git submodule update --init third_party/verilog-axis protocol-processor gptp-processor
```

Log: `$VALIDATION_STORAGE/682-a554/round2/final/docs-workflow/15.log`; 0 bytes; SHA-256 `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`.

## final-docs-workflow 16: Imported gPTP documentation gate

Head: `591a5752e6a587b28b501e2d02d6a9d0293f3ba2`. GNU Make 4.3. Exit: 0.

Working directory: `$LANES/682-pp-pin3`.

```sh
python3 scripts/check_gptp_docs.py --with-submodule
make -C gptp-processor docs
```

Log: `$VALIDATION_STORAGE/682-a554/round2/final/docs-workflow/16.log`; 2,736 bytes; SHA-256 `2ee7c1389f730f5d60e04123c4e7b04cd555da58393dccf27b73d1265fc5d481`.

## final-docs-workflow 17: Code-quality measurement self-tests

Head: `591a5752e6a587b28b501e2d02d6a9d0293f3ba2`. GNU Make 4.3. Exit: 0.

Working directory: `$LANES/682-pp-pin3`.

```sh
python3 scripts/measure_control_flow.py --selftest
python3 scripts/measure_cohesion.py --selftest
```

Log: `$VALIDATION_STORAGE/682-a554/round2/final/docs-workflow/17.log`; 3,293 bytes; SHA-256 `862838344ece59e4179fd4bcfe04f85ee320f0601c325014b2509717db13368b`.

## final-docs-workflow 18: Install the pinned sv2v release

Head: `591a5752e6a587b28b501e2d02d6a9d0293f3ba2`. GNU Make 4.3. Exit: 0.

Working directory: `$LANES/682-pp-pin3`.

```sh
set -euo pipefail
ver=v0.0.12
sha256=ff8c9eea5bc029b372fb4953427625cddb7cf7e58c1240623ac9f260818d5a00
url="https://github.com/zachjs/sv2v/releases/download/${ver}/sv2v-Linux.zip"
curl -fsSL "$url" -o /tmp/sv2v.zip
echo "${sha256}  /tmp/sv2v.zip" | sha256sum -c -
unzip -q -o /tmp/sv2v.zip -d /tmp/sv2v
sudo install -m755 "$(find /tmp/sv2v -name sv2v -type f | head -1)" \
  /usr/local/bin/sv2v
sv2v --version
```

Log: `$VALIDATION_STORAGE/682-a554/round2/final/docs-workflow/18.log`; 31 bytes; SHA-256 `176b5effd5ab230db92a3088fc5e8a688744dc1203991c6e71b25f2a29925e0d`.

## final-docs-workflow 19: Bare-metal scope gate

Head: `591a5752e6a587b28b501e2d02d6a9d0293f3ba2`. GNU Make 4.3. Exit: 0.

Working directory: `$LANES/682-pp-pin3`.

```sh
python3 scripts/check_baremetal_only.py --check
python3 scripts/check_baremetal_only.py --selftest
```

Log: `$VALIDATION_STORAGE/682-a554/round2/final/docs-workflow/19.log`; 115 bytes; SHA-256 `49df7412f69dfd61d608af572b802a0dc8a41c826a32489a9593650d01e869c0`.

## final-docs-workflow 20: Install and verify the pinned RV32 SDK

Head: `591a5752e6a587b28b501e2d02d6a9d0293f3ba2`. GNU Make 4.3. Exit: 0.

Working directory: `$LANES/682-pp-pin3`.

```sh
set -euo pipefail
python3 scripts/ci_rv32_sdk_selftest.py
python3 scripts/ci_rv32_sdk.py --destination "$HOME/br-milan-rv32/host"
```

Log: `$VALIDATION_STORAGE/682-a554/round2/final/docs-workflow/20.log`; 8,119 bytes; SHA-256 `77efe26f02c22a2534493d675d8ef0ca3413a370ed93903c1b1ce95165860195`.

## final-docs-workflow 21: Compiler-absent firmware controls

Head: `591a5752e6a587b28b501e2d02d6a9d0293f3ba2`. GNU Make 4.3. Exit: 0.

Working directory: `$LANES/682-pp-pin3`.

```sh
set -euo pipefail
python3 sw/builder/test_firmware_compiler.py --selftest
python3 sw/builder/test_firmware_compiler.py --absent --audit "$RUNNER_TEMP/rv32-absent.jsonl"
```

Log: `$VALIDATION_STORAGE/682-a554/round2/final/docs-workflow/21.log`; 52,039 bytes; SHA-256 `578394ea1b5c9ab583e239eb6a7e0393c1569ef56357e745ff21902433c8a2b6`.

## final-docs-workflow 22: End-station builder gates

Head: `591a5752e6a587b28b501e2d02d6a9d0293f3ba2`. GNU Make 4.3. Exit: 0.

Working directory: `$LANES/682-pp-pin3`.

```sh
python3 -m pip install --quiet pyyaml
python3 sw/builder/test_builder.py --require-rv32
```

Log: `$VALIDATION_STORAGE/682-a554/round2/final/docs-workflow/22.log`; 101,744 bytes; SHA-256 `87d9400d823bd6d0cce2f7c19ed2b800a57b4456ec9dddca00b0cab9d9c0abd5`.

## final-docs-workflow 23: NVM record-space gate

Head: `591a5752e6a587b28b501e2d02d6a9d0293f3ba2`. GNU Make 4.3. Exit: 0.

Working directory: `$LANES/682-pp-pin3`.

```sh
python3 scripts/check_nvm_record_space.py
python3 scripts/check_nvm_record_space.py --self-test
```

Log: `$VALIDATION_STORAGE/682-a554/round2/final/docs-workflow/23.log`; 9,588 bytes; SHA-256 `7969fb65ae1ea9d608146bed63d697587402331dc1efa2c128e61861a7f6493e`.

## final-docs-workflow 24: Capture measurement census and clock gate

Head: `591a5752e6a587b28b501e2d02d6a9d0293f3ba2`. GNU Make 4.3. Exit: 0.

Working directory: `$LANES/682-pp-pin3`.

```sh
python3 scripts/check_nvm_capture.py
```

Log: `$VALIDATION_STORAGE/682-a554/round2/final/docs-workflow/24.log`; 324 bytes; SHA-256 `9a4196c774ce4ddfa9980cf9345d111028f3afa812677fe5bab392f81c955439`.

## final-docs-workflow 25: Saved-state writer gate

Head: `591a5752e6a587b28b501e2d02d6a9d0293f3ba2`. GNU Make 4.3. Exit: 0.

Working directory: `$LANES/682-pp-pin3`.

```sh
python3 sw/firmware/nvm_hosttest/test_nvm_firmware.py --self-test
```

Log: `$VALIDATION_STORAGE/682-a554/round2/final/docs-workflow/25.log`; 5,189 bytes; SHA-256 `cba18482dbf27c70ee56b28a8fbbe7bfdc2cc49b4644a42daa5ad4db8f6d4972`.

## final-docs-workflow 26: SoC source-list gate (Vivado would fail 40 min in without this)

Head: `591a5752e6a587b28b501e2d02d6a9d0293f3ba2`. GNU Make 4.3. Exit: 0.

Working directory: `$LANES/682-pp-pin3`.

```sh
python3 scripts/check_soc_sources.py
python3 scripts/check_soc_sources.py --selftest
command -v tclsh >/dev/null || {
  sudo apt-get update -qq
  sudo apt-get install -y --no-install-recommends tcl
}
python3 sw/litex/iob_pack_selftest.py
```

Log: `$VALIDATION_STORAGE/682-a554/round2/final/docs-workflow/26.log`; 4,733 bytes; SHA-256 `7c34f57b723fa707a2eadc1915b61980ed407fd0cf480238032e391030f053f9`.

## final-docs-workflow 27: RTL source-list drift gate

Head: `591a5752e6a587b28b501e2d02d6a9d0293f3ba2`. GNU Make 4.3. Exit: 0.

Working directory: `$LANES/682-pp-pin3`.

```sh
python3 scripts/check_rtl_source_lists.py
python3 scripts/check_rtl_source_lists.py --selftest
```

Log: `$VALIDATION_STORAGE/682-a554/round2/final/docs-workflow/27.log`; 3,453 bytes; SHA-256 `be8805dc2fee50eddcf0b966ea5728febdeed2e7b9f288ba358f41c1fe4b7041`.

## final-docs-workflow 28: Boundary-unit naming ratchet

Head: `591a5752e6a587b28b501e2d02d6a9d0293f3ba2`. GNU Make 4.3. Exit: 0.

Working directory: `$LANES/682-pp-pin3`.

```sh
python3 scripts/measure_naming.py --check
python3 scripts/measure_naming.py --selftest
```

Log: `$VALIDATION_STORAGE/682-a554/round2/final/docs-workflow/28.log`; 40,634 bytes; SHA-256 `ad6af3b1bb7cbfe3e761b8105d59a1fac1937cd0ab6c437b8298f61304a7e81b`.

## final-docs-workflow 29: Port contract gate

Head: `591a5752e6a587b28b501e2d02d6a9d0293f3ba2`. GNU Make 4.3. Exit: 0.

Working directory: `$LANES/682-pp-pin3`.

```sh
python3 scripts/check_port_contracts.py
python3 scripts/check_port_contracts.py --selftest
```

Log: `$VALIDATION_STORAGE/682-a554/round2/final/docs-workflow/29.log`; 5,040 bytes; SHA-256 `72a62b76b7c80018909615134728c909abb86662481704f5a9edbe5337f1e653`.

## final-docs-workflow 30: Fail-fast ratchet

Head: `591a5752e6a587b28b501e2d02d6a9d0293f3ba2`. GNU Make 4.3. Exit: 0.

Working directory: `$LANES/682-pp-pin3`.

```sh
python3 scripts/measure_fail_fast.py --check
python3 scripts/measure_fail_fast.py --selftest
```

Log: `$VALIDATION_STORAGE/682-a554/round2/final/docs-workflow/30.log`; 12,682 bytes; SHA-256 `3fbed56aa0724496465ce6f185d931ddb1a3ee49bb28a1ff77e1051981a700dd`.

## final-docs-workflow 31: TODO ownership gate

Head: `591a5752e6a587b28b501e2d02d6a9d0293f3ba2`. GNU Make 4.3. Exit: 0.

Working directory: `$LANES/682-pp-pin3`.

```sh
python3 scripts/check_todo_ownership.py
python3 scripts/check_todo_ownership.py --selftest
```

Log: `$VALIDATION_STORAGE/682-a554/round2/final/docs-workflow/31.log`; 2,745 bytes; SHA-256 `10183ae2429bc9507cee2955b0d27ef5f720f5d944a04055f204ff54904b9baa`.

## final-docs-workflow 32: Test-evidence ratchet

Head: `591a5752e6a587b28b501e2d02d6a9d0293f3ba2`. GNU Make 4.3. Exit: 0.

Working directory: `$LANES/682-pp-pin3`.

```sh
python3 scripts/measure_test_evidence.py --check
python3 scripts/measure_test_evidence.py --selftest
```

Log: `$VALIDATION_STORAGE/682-a554/round2/final/docs-workflow/32.log`; 20,766 bytes; SHA-256 `6162e40a0b084c014771b2f9a22fcbaf6fa61f425fac6dfe2cd03604e6f2ce65`.

## final-docs-workflow 33: Mechanical hygiene ratchet

Head: `591a5752e6a587b28b501e2d02d6a9d0293f3ba2`. GNU Make 4.3. Exit: 0.

Working directory: `$LANES/682-pp-pin3`.

```sh
python3 scripts/check_hygiene.py --check
python3 scripts/check_hygiene.py --selftest
```

Log: `$VALIDATION_STORAGE/682-a554/round2/final/docs-workflow/33.log`; 3,847 bytes; SHA-256 `daf965548668bbdaace4c6f0e4571e525c262141de1654bf312b9d5bee0dd8e2`.

## final-docs-workflow 34: SystemVerilog idiom gate

Head: `591a5752e6a587b28b501e2d02d6a9d0293f3ba2`. GNU Make 4.3. Exit: 0.

Working directory: `$LANES/682-pp-pin3`.

```sh
python3 scripts/check_sv_idiom.py
python3 scripts/check_sv_idiom.py --selftest
```

Log: `$VALIDATION_STORAGE/682-a554/round2/final/docs-workflow/34.log`; 3,173 bytes; SHA-256 `ccd900273b796fdfcf74e586f952eadfc9f6f6b1ad448b891183f939a49df728`.

## final-docs-workflow 35: C and C++ idiom gate

Head: `591a5752e6a587b28b501e2d02d6a9d0293f3ba2`. GNU Make 4.3. Exit: 0.

Working directory: `$LANES/682-pp-pin3`.

```sh
python3 scripts/check_cpp_idiom.py
python3 scripts/check_cpp_idiom.py --selftest
```

Log: `$VALIDATION_STORAGE/682-a554/round2/final/docs-workflow/35.log`; 3,909 bytes; SHA-256 `302f2a969fb19d5a52d868e0bcadabe7f389d131c99f803a85569a71dc420d62`.

## final-docs-workflow 36: Python idiom gate

Head: `591a5752e6a587b28b501e2d02d6a9d0293f3ba2`. GNU Make 4.3. Exit: 0.

Working directory: `$LANES/682-pp-pin3`.

```sh
python3 scripts/check_py_idiom.py
python3 scripts/check_py_idiom.py --selftest
```

Log: `$VALIDATION_STORAGE/682-a554/round2/final/docs-workflow/36.log`; 2,992 bytes; SHA-256 `5d40c19346e47439dd4fcab904b58a65f6a35a934a75fd7bffcd18b8ecc1b1c5`.

## final-docs-workflow 37: Shell idiom gate

Head: `591a5752e6a587b28b501e2d02d6a9d0293f3ba2`. GNU Make 4.3. Exit: 0.

Working directory: `$LANES/682-pp-pin3`.

```sh
python3 scripts/check_sh_idiom.py
python3 scripts/check_sh_idiom.py --selftest
```

Log: `$VALIDATION_STORAGE/682-a554/round2/final/docs-workflow/37.log`; 2,696 bytes; SHA-256 `a57f331056f1f93e369a05fc919fd7d91a98638253282a970a118711a46e20e1`.

## final-docs-workflow 38: CI event and SHA contract gate

Head: `591a5752e6a587b28b501e2d02d6a9d0293f3ba2`. GNU Make 4.3. Exit: 0.

Working directory: `$LANES/682-pp-pin3`.

```sh
python3 scripts/ci_events.py --check
python3 scripts/ci_events.py --selftest
```

Log: `$VALIDATION_STORAGE/682-a554/round2/final/docs-workflow/38.log`; 151,577 bytes; SHA-256 `d7490f337de8e6f9456bdd2d75332bb10b44de58765e9cab1054d4b0d00e34a5`.

## final-docs-workflow 39: Local act runner contract gate

Head: `591a5752e6a587b28b501e2d02d6a9d0293f3ba2`. GNU Make 4.3. Exit: 0.

Working directory: `$LANES/682-pp-pin3`.

```sh
python3 scripts/act_ci.py --selftest
```

Log: `$VALIDATION_STORAGE/682-a554/round2/final/docs-workflow/39.log`; 36,483 bytes; SHA-256 `876a6eca5975005e4e1d1ddddad9f74d2443039a10df8b7f590e4c781632fdab`.

## final-docs-workflow 40: Doc cited-path gate

Head: `591a5752e6a587b28b501e2d02d6a9d0293f3ba2`. GNU Make 4.3. Exit: 0.

Working directory: `$LANES/682-pp-pin3`.

```sh
python3 scripts/check_doc_paths.py
```

Log: `$VALIDATION_STORAGE/682-a554/round2/final/docs-workflow/40.log`; 85 bytes; SHA-256 `14e8073fd597e8c2e74483ee4f15374aa0f669038c0af1acafb7b47d130467ff`.

## final-docs-workflow 41: Archive integrity gate

Head: `591a5752e6a587b28b501e2d02d6a9d0293f3ba2`. GNU Make 4.3. Exit: 0.

Working directory: `$LANES/682-pp-pin3`.

```sh
python3 scripts/check_archive.py
python3 scripts/check_archive.py --selftest
```

Log: `$VALIDATION_STORAGE/682-a554/round2/final/docs-workflow/41.log`; 128 bytes; SHA-256 `1a15e66a07892f544c4b9bee75201ff9acaf3edd2c37963a780f8473466d50cb`.

## final-docs-workflow 42: Per-page contents gate

Head: `591a5752e6a587b28b501e2d02d6a9d0293f3ba2`. GNU Make 4.3. Exit: 0.

Working directory: `$LANES/682-pp-pin3`.

```sh
python3 scripts/gen_toc.py --selftest
python3 scripts/gen_toc.py --verify-anchors
python3 scripts/gen_toc.py --check
```

Log: `$VALIDATION_STORAGE/682-a554/round2/final/docs-workflow/42.log`; 196 bytes; SHA-256 `d42332a0ab9bd6e7afdb6d5b5dd5b405b5932fd7c4fac938a30b2f4095af42e0`.

## final-docs-workflow 43: AEM store generator self-test

Head: `591a5752e6a587b28b501e2d02d6a9d0293f3ba2`. GNU Make 4.3. Exit: 0.

Working directory: `$LANES/682-pp-pin3`.

```sh
python3 avdecc/gen_aem_store.py --self-test
```

Log: `$VALIDATION_STORAGE/682-a554/round2/final/docs-workflow/43.log`; 3,596 bytes; SHA-256 `9f126bf9dfc7cb552a2414b98d2792449dc4ae126395997750d5039cb896f022`.

## final-docs-workflow 44: Sweep/build shape gate

Head: `591a5752e6a587b28b501e2d02d6a9d0293f3ba2`. GNU Make 4.3. Exit: 0.

Working directory: `$LANES/682-pp-pin3`.

```sh
python3 scripts/check_sweep_shape.py --self-test
```

Log: `$VALIDATION_STORAGE/682-a554/round2/final/docs-workflow/44.log`; 19,682 bytes; SHA-256 `63ac1436c4d6292a3ec5cfaf3cdd0dab09751bb6ad647e16a8cd1da4f7de2c04`.

## final-docs-workflow 45: Deploy shape gate

Head: `591a5752e6a587b28b501e2d02d6a9d0293f3ba2`. GNU Make 4.3. Exit: 0.

Working directory: `$LANES/682-pp-pin3`.

```sh
python3 scripts/check_deploy_shape.py --self-test
```

Log: `$VALIDATION_STORAGE/682-a554/round2/final/docs-workflow/45.log`; 9,270 bytes; SHA-256 `6e4bb815d4a015fc437da1e1584f8755b4feba5ab5272421126ca193b0a58610`.

## final-docs-workflow 46: Entity shape gate

Head: `591a5752e6a587b28b501e2d02d6a9d0293f3ba2`. GNU Make 4.3. Exit: 0.

Working directory: `$LANES/682-pp-pin3`.

```sh
python3 scripts/check_entity_shape.py --self-test
```

Log: `$VALIDATION_STORAGE/682-a554/round2/final/docs-workflow/46.log`; 25,694 bytes; SHA-256 `7c1cc4d5ce778537bd27790e075eb0d8159cf6c1281870eb96142e9465eff19c`.

## final-docs-workflow 47: Fetch the engine authority the builder derives from

Head: `591a5752e6a587b28b501e2d02d6a9d0293f3ba2`. GNU Make 4.3. Exit: 0.

Working directory: `$LANES/682-pp-pin3`.

```sh
git submodule update --init gptp-processor
```

Log: `$VALIDATION_STORAGE/682-a554/round2/final/docs-workflow/47.log`; 0 bytes; SHA-256 `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`.

## final-docs-workflow 48: Advertised-vs-emitted gate (green since 2026-07-28, item 00)

Head: `591a5752e6a587b28b501e2d02d6a9d0293f3ba2`. GNU Make 4.3. Exit: 0.

Working directory: `$LANES/682-pp-pin3`.

```sh
python3 -m pip install --quiet pyyaml
python3 scripts/check_wire_accountability.py --self-test
```

Log: `$VALIDATION_STORAGE/682-a554/round2/final/docs-workflow/48.log`; 4,965 bytes; SHA-256 `bd97b8b53304baf2b912ac2e4ec507e3b8f9ae4c5c2511b5dc69a41d2cbdd3d4`.

## final-docs-workflow 49: Strip git metadata, then run the docs gate

Head: `591a5752e6a587b28b501e2d02d6a9d0293f3ba2`. GNU Make 4.3. Exit: 0.

Working directory: `$VALIDATION_STORAGE/682-a554/round2/final/docs-no-git`.

```sh
rm -rf .git
python3 scripts/docs_check.py
python3 scripts/check_feature_status.py
```

Log: `$VALIDATION_STORAGE/682-a554/round2/final/docs-workflow/49.log`; 225 bytes; SHA-256 `34fd54c631eacc71969002478f61c08b7d936b20d201e15dd27abc71e8669d77`.

## refresh-docs-workflow 01: Build the validated HDL reference

Head: `5428b044176f95248e6916dc00dd89c0df154078`. GNU Make 4.3. Exit: 0.

Working directory: `$LANES/682-pp-pin3`.

```sh
set -euo pipefail
python3 -m pip install --quiet --require-hashes \
  -r tools/hdl_reference/requirements.txt
python3 scripts/gen_hdl_reference.py --selftest
python3 scripts/gen_hdl_reference.py \
  --output "$RUNNER_TEMP/milan-hdl-reference"
```

Log: `$VALIDATION_STORAGE/682-a554/round2/refresh/docs-workflow/01.log`; 817 bytes; SHA-256 `bcfb2b736e14772928de54c323dc6166465e81c3fcc10fbce6e8b96a2905cd8c`.

## refresh-docs-workflow 02: Install the python gate dependencies

Head: `5428b044176f95248e6916dc00dd89c0df154078`. GNU Make 4.3. Exit: 0.

Working directory: `$LANES/682-pp-pin3`.

```sh
python3 -m pip install --quiet pyyaml
```

Log: `$VALIDATION_STORAGE/682-a554/round2/refresh/docs-workflow/02.log`; 0 bytes; SHA-256 `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`.

## refresh-docs-workflow 03: Install the pinned Markdown renderer

Head: `5428b044176f95248e6916dc00dd89c0df154078`. GNU Make 4.3. Exit: 0.

Working directory: `$LANES/682-pp-pin3`.

```sh
python3 -m pip install --quiet --cache-dir ~/.cache/milan-markdown-pip \
  --require-hashes -r tools/markdown/requirements.txt
```

Log: `$VALIDATION_STORAGE/682-a554/round2/refresh/docs-workflow/03.log`; 0 bytes; SHA-256 `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`.

## refresh-docs-workflow 04: Install diagram gate dependencies

Head: `5428b044176f95248e6916dc00dd89c0df154078`. GNU Make 4.3. Exit: 0.

Working directory: `$LANES/682-pp-pin3`.

```sh
sudo apt-get update -qq
sudo apt-get install -y --no-install-recommends librsvg2-bin
python3 -m pip install --quiet wavedrom==2.0.3.post3
```

Log: `$VALIDATION_STORAGE/682-a554/round2/refresh/docs-workflow/04.log`; 2,323 bytes; SHA-256 `83e0678c915bb0e1bca480d0e5c1d71bb40af48ebdbdc21976658e511897bea4`.

## refresh-docs-workflow 05: Link health, wording, dead-reference and local-info gate

Head: `5428b044176f95248e6916dc00dd89c0df154078`. GNU Make 4.3. Exit: 0.

Working directory: `$LANES/682-pp-pin3`.

```sh
python3 scripts/docs_check.py
```

Log: `$VALIDATION_STORAGE/682-a554/round2/refresh/docs-workflow/05.log`; 128 bytes; SHA-256 `9de597c20c044953930a35a471dc8e5592ecc57b24be4c395bf381c1e72e2052`.

## refresh-docs-workflow 06: Added-line em-dash gate

Head: `5428b044176f95248e6916dc00dd89c0df154078`. GNU Make 4.3. Exit: 0.

Working directory: `$LANES/682-pp-pin3`.

```sh
set -euo pipefail
case "$EVENT_NAME" in
  pull_request)
    if [ -z "$PR_BASE_REF" ]; then
      echo "the pull_request event names no base branch"; exit 2
    fi
    git fetch --quiet origin "$PR_BASE_REF"
    base="$(git merge-base HEAD FETCH_HEAD || true)"
    ;;
  push) base="$PUSH_BEFORE_SHA" ;;
  *) echo "a $EVENT_NAME event carries no base to judge from"; exit 2 ;;
esac
if [ -z "$base" ] || [ "$base" = 0000000000000000000000000000000000000000 ]; then
  echo "the $EVENT_NAME event names no base commit"; exit 2
fi
git cat-file -e "$base^{commit}" 2>/dev/null || git fetch --quiet --depth=1 origin "$base"
python3 scripts/check_em_dash.py --base "$base"
```

Log: `$VALIDATION_STORAGE/682-a554/round2/refresh/docs-workflow/06.log`; 140 bytes; SHA-256 `9768aeb548e607b4bd7e5685d0452c6e9d35a03a508e9e2d7910cd4dafc8e90d`.

## refresh-docs-workflow 07: Concise audience documentation gate

Head: `5428b044176f95248e6916dc00dd89c0df154078`. GNU Make 4.3. Exit: 0.

Working directory: `$LANES/682-pp-pin3`.

```sh
python3 scripts/check_doc_style.py
python3 scripts/check_doc_style.py --selftest
python3 scripts/check_gptp_docs.py
python3 scripts/check_gptp_docs.py --selftest
```

Log: `$VALIDATION_STORAGE/682-a554/round2/refresh/docs-workflow/07.log`; 167 bytes; SHA-256 `05d6ef2302a6c0467ad437209233733e93bcb2941539103e26c51b988a28637a`.

## refresh-docs-workflow 08: Audience diagram no-drift gate

Head: `5428b044176f95248e6916dc00dd89c0df154078`. GNU Make 4.3. Exit: 0.

Working directory: `$LANES/682-pp-pin3`.

```sh
python3 docs/DOC_MAP.gen.py --check
python3 docs/DOC_MAP.gen.py --selftest
python3 docs/diagrams/timesync_chain.gen.py --check
python3 docs/diagrams/timesync_chain.gen.py --selftest
```

Log: `$VALIDATION_STORAGE/682-a554/round2/refresh/docs-workflow/08.log`; 242 bytes; SHA-256 `79dce4dc64e4d57851e37c5bac0a829304d65207659bb65049e11b7d0683f069`.

## refresh-docs-workflow 09: Product solution source-fact gate

Head: `5428b044176f95248e6916dc00dd89c0df154078`. GNU Make 4.3. Exit: 0.

Working directory: `$LANES/682-pp-pin3`.

```sh
python3 scripts/check_solution_docs.py
python3 scripts/check_solution_docs.py --selftest
```

Log: `$VALIDATION_STORAGE/682-a554/round2/refresh/docs-workflow/09.log`; 146 bytes; SHA-256 `9ef43cc924919e10ccb30a9419819d20b849d787a8f37fcabba22e2159d3167d`.

## refresh-docs-workflow 10: Verified submodule documentation gate

Head: `5428b044176f95248e6916dc00dd89c0df154078`. GNU Make 4.3. Exit: 0.

Working directory: `$LANES/682-pp-pin3`.

```sh
python3 docs/diagrams/submodule_boundaries.gen.py --check
python3 docs/diagrams/submodule_boundaries.gen.py --selftest
python3 scripts/check_submodule_docs.py
python3 scripts/check_submodule_docs.py --selftest
```

Log: `$VALIDATION_STORAGE/682-a554/round2/refresh/docs-workflow/10.log`; 227 bytes; SHA-256 `cd9f3e7404ce8e884eded8567a1b2560dc22cc7a4b5796601edb295cb725cc64`.

## refresh-docs-workflow 11: HDL timing diagram no-drift gate

Head: `5428b044176f95248e6916dc00dd89c0df154078`. GNU Make 4.3. Exit: 0.

Working directory: `$LANES/682-pp-pin3`.

```sh
python3 scripts/gen_wavedrom.py --selftest
python3 scripts/gen_wavedrom.py docs/diagrams/wd_axis_backpressure.json --background=white --check
python3 scripts/gen_wavedrom.py docs/diagrams/wd_cdc_handshake.json --background=white --check
python3 scripts/gen_wavedrom.py docs/diagrams/wd_gptp_pdelay.json --background=white --check
```

Log: `$VALIDATION_STORAGE/682-a554/round2/refresh/docs-workflow/11.log`; 241 bytes; SHA-256 `af9493d0e4acd65eb64ba2bbe7103a2c6f957ecca650a938cdc18d70396a57ea`.

## refresh-docs-workflow 12: Published diagram PNG gate

Head: `5428b044176f95248e6916dc00dd89c0df154078`. GNU Make 4.3. Exit: 0.

Working directory: `$LANES/682-pp-pin3`.

```sh
python3 scripts/check_diagram_pngs.py
python3 scripts/check_diagram_pngs.py --selftest
```

Log: `$VALIDATION_STORAGE/682-a554/round2/refresh/docs-workflow/12.log`; 125 bytes; SHA-256 `17d1d2360a98e818f8706a8165affff7c873cb06b4fe8db4c48300e103e51c1e`.

## refresh-docs-workflow 13: Milan feature-status consistency gate

Head: `5428b044176f95248e6916dc00dd89c0df154078`. GNU Make 4.3. Exit: 0.

Working directory: `$LANES/682-pp-pin3`.

```sh
python3 scripts/check_feature_status.py --self-test
```

Log: `$VALIDATION_STORAGE/682-a554/round2/refresh/docs-workflow/13.log`; 1,500 bytes; SHA-256 `77f7649b1865c0daf4f3de04dd18c78be4885c9c94a8f03fd1e4f262758c3184`.

## refresh-docs-workflow 14: Traceability matrix no-drift gate

Head: `5428b044176f95248e6916dc00dd89c0df154078`. GNU Make 4.3. Exit: 0.

Working directory: `$LANES/682-pp-pin3`.

```sh
python3 docs/traceability/gen_module_matrix.py --check
```

Log: `$VALIDATION_STORAGE/682-a554/round2/refresh/docs-workflow/14.log`; 118 bytes; SHA-256 `d0be3b6428ae2079134f2a21b2972c524a26103b0e9c8b64039bb24ae22797dc`.

## refresh-docs-workflow 15: Fetch the builder source dependencies

Head: `5428b044176f95248e6916dc00dd89c0df154078`. GNU Make 4.3. Exit: 0.

Working directory: `$LANES/682-pp-pin3`.

```sh
git submodule update --init third_party/verilog-axis protocol-processor gptp-processor
```

Log: `$VALIDATION_STORAGE/682-a554/round2/refresh/docs-workflow/15.log`; 0 bytes; SHA-256 `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`.

## refresh-docs-workflow 16: Imported gPTP documentation gate

Head: `5428b044176f95248e6916dc00dd89c0df154078`. GNU Make 4.3. Exit: 0.

Working directory: `$LANES/682-pp-pin3`.

```sh
python3 scripts/check_gptp_docs.py --with-submodule
make -C gptp-processor docs
```

Log: `$VALIDATION_STORAGE/682-a554/round2/refresh/docs-workflow/16.log`; 2,736 bytes; SHA-256 `2ee7c1389f730f5d60e04123c4e7b04cd555da58393dccf27b73d1265fc5d481`.

## refresh-docs-workflow 17: Code-quality measurement self-tests

Head: `5428b044176f95248e6916dc00dd89c0df154078`. GNU Make 4.3. Exit: 0.

Working directory: `$LANES/682-pp-pin3`.

```sh
python3 scripts/measure_control_flow.py --selftest
python3 scripts/measure_cohesion.py --selftest
```

Log: `$VALIDATION_STORAGE/682-a554/round2/refresh/docs-workflow/17.log`; 3,293 bytes; SHA-256 `862838344ece59e4179fd4bcfe04f85ee320f0601c325014b2509717db13368b`.

## refresh-docs-workflow 18: Install the pinned sv2v release

Head: `5428b044176f95248e6916dc00dd89c0df154078`. GNU Make 4.3. Exit: 0.

Working directory: `$LANES/682-pp-pin3`.

```sh
set -euo pipefail
ver=v0.0.12
sha256=ff8c9eea5bc029b372fb4953427625cddb7cf7e58c1240623ac9f260818d5a00
url="https://github.com/zachjs/sv2v/releases/download/${ver}/sv2v-Linux.zip"
curl -fsSL "$url" -o /tmp/sv2v.zip
echo "${sha256}  /tmp/sv2v.zip" | sha256sum -c -
unzip -q -o /tmp/sv2v.zip -d /tmp/sv2v
sudo install -m755 "$(find /tmp/sv2v -name sv2v -type f | head -1)" \
  /usr/local/bin/sv2v
sv2v --version
```

Log: `$VALIDATION_STORAGE/682-a554/round2/refresh/docs-workflow/18.log`; 31 bytes; SHA-256 `176b5effd5ab230db92a3088fc5e8a688744dc1203991c6e71b25f2a29925e0d`.

## refresh-docs-workflow 19: Bare-metal scope gate

Head: `5428b044176f95248e6916dc00dd89c0df154078`. GNU Make 4.3. Exit: 0.

Working directory: `$LANES/682-pp-pin3`.

```sh
python3 scripts/check_baremetal_only.py --check
python3 scripts/check_baremetal_only.py --selftest
```

Log: `$VALIDATION_STORAGE/682-a554/round2/refresh/docs-workflow/19.log`; 115 bytes; SHA-256 `821b14c7b7602fb0eb2324b506ad9098d840ec28628ab146bca7aeaab31ff7aa`.

## refresh-docs-workflow 20: Install and verify the pinned RV32 SDK

Head: `5428b044176f95248e6916dc00dd89c0df154078`. GNU Make 4.3. Exit: 0.

Working directory: `$LANES/682-pp-pin3`.

```sh
set -euo pipefail
python3 scripts/ci_rv32_sdk_selftest.py
python3 scripts/ci_rv32_sdk.py --destination "$HOME/br-milan-rv32/host"
```

Log: `$VALIDATION_STORAGE/682-a554/round2/refresh/docs-workflow/20.log`; 8,119 bytes; SHA-256 `bc748996f0846efd76f61e2aec52b050db1da455529fe10b340b637c051e2448`.

## refresh-docs-workflow 21: Compiler-absent firmware controls

Head: `5428b044176f95248e6916dc00dd89c0df154078`. GNU Make 4.3. Exit: 0.

Working directory: `$LANES/682-pp-pin3`.

```sh
set -euo pipefail
python3 sw/builder/test_firmware_compiler.py --selftest
python3 sw/builder/test_firmware_compiler.py --absent --audit "$RUNNER_TEMP/rv32-absent.jsonl"
```

Log: `$VALIDATION_STORAGE/682-a554/round2/refresh/docs-workflow/21.log`; 52,041 bytes; SHA-256 `d0709afe4c5f022260d7e46acf58ff9da0a487a84942d24c957601bd7dc17572`.

## refresh-docs-workflow 22: End-station builder gates

Head: `5428b044176f95248e6916dc00dd89c0df154078`. GNU Make 4.3. Exit: 0.

Working directory: `$LANES/682-pp-pin3`.

```sh
python3 -m pip install --quiet pyyaml
python3 sw/builder/test_builder.py --require-rv32
```

Log: `$VALIDATION_STORAGE/682-a554/round2/refresh/docs-workflow/22.log`; 101,744 bytes; SHA-256 `ab9f69abd55e0b0ff475b40f4ab314e1eb98e40a1cb2ad1de39c39853fe27440`.

## refresh-docs-workflow 23: NVM record-space gate

Head: `5428b044176f95248e6916dc00dd89c0df154078`. GNU Make 4.3. Exit: 0.

Working directory: `$LANES/682-pp-pin3`.

```sh
python3 scripts/check_nvm_record_space.py
python3 scripts/check_nvm_record_space.py --self-test
```

Log: `$VALIDATION_STORAGE/682-a554/round2/refresh/docs-workflow/23.log`; 9,588 bytes; SHA-256 `7969fb65ae1ea9d608146bed63d697587402331dc1efa2c128e61861a7f6493e`.

## refresh-docs-workflow 24: Capture measurement census and clock gate

Head: `5428b044176f95248e6916dc00dd89c0df154078`. GNU Make 4.3. Exit: 0.

Working directory: `$LANES/682-pp-pin3`.

```sh
python3 scripts/check_nvm_capture.py
```

Log: `$VALIDATION_STORAGE/682-a554/round2/refresh/docs-workflow/24.log`; 324 bytes; SHA-256 `9a4196c774ce4ddfa9980cf9345d111028f3afa812677fe5bab392f81c955439`.

## refresh-docs-workflow 25: Saved-state writer gate

Head: `5428b044176f95248e6916dc00dd89c0df154078`. GNU Make 4.3. Exit: 0.

Working directory: `$LANES/682-pp-pin3`.

```sh
python3 sw/firmware/nvm_hosttest/test_nvm_firmware.py --self-test
```

Log: `$VALIDATION_STORAGE/682-a554/round2/refresh/docs-workflow/25.log`; 5,189 bytes; SHA-256 `cba18482dbf27c70ee56b28a8fbbe7bfdc2cc49b4644a42daa5ad4db8f6d4972`.

## refresh-docs-workflow 26: SoC source-list gate (Vivado would fail 40 min in without this)

Head: `5428b044176f95248e6916dc00dd89c0df154078`. GNU Make 4.3. Exit: 0.

Working directory: `$LANES/682-pp-pin3`.

```sh
python3 scripts/check_soc_sources.py
python3 scripts/check_soc_sources.py --selftest
command -v tclsh >/dev/null || {
  sudo apt-get update -qq
  sudo apt-get install -y --no-install-recommends tcl
}
python3 sw/litex/iob_pack_selftest.py
```

Log: `$VALIDATION_STORAGE/682-a554/round2/refresh/docs-workflow/26.log`; 4,733 bytes; SHA-256 `7c34f57b723fa707a2eadc1915b61980ed407fd0cf480238032e391030f053f9`.

## refresh-docs-workflow 27: RTL source-list drift gate

Head: `5428b044176f95248e6916dc00dd89c0df154078`. GNU Make 4.3. Exit: 0.

Working directory: `$LANES/682-pp-pin3`.

```sh
python3 scripts/check_rtl_source_lists.py
python3 scripts/check_rtl_source_lists.py --selftest
```

Log: `$VALIDATION_STORAGE/682-a554/round2/refresh/docs-workflow/27.log`; 3,453 bytes; SHA-256 `be8805dc2fee50eddcf0b966ea5728febdeed2e7b9f288ba358f41c1fe4b7041`.

## refresh-docs-workflow 28: Boundary-unit naming ratchet

Head: `5428b044176f95248e6916dc00dd89c0df154078`. GNU Make 4.3. Exit: 0.

Working directory: `$LANES/682-pp-pin3`.

```sh
python3 scripts/measure_naming.py --check
python3 scripts/measure_naming.py --selftest
```

Log: `$VALIDATION_STORAGE/682-a554/round2/refresh/docs-workflow/28.log`; 40,634 bytes; SHA-256 `ad6af3b1bb7cbfe3e761b8105d59a1fac1937cd0ab6c437b8298f61304a7e81b`.

## refresh-docs-workflow 29: Port contract gate

Head: `5428b044176f95248e6916dc00dd89c0df154078`. GNU Make 4.3. Exit: 0.

Working directory: `$LANES/682-pp-pin3`.

```sh
python3 scripts/check_port_contracts.py
python3 scripts/check_port_contracts.py --selftest
```

Log: `$VALIDATION_STORAGE/682-a554/round2/refresh/docs-workflow/29.log`; 5,040 bytes; SHA-256 `72a62b76b7c80018909615134728c909abb86662481704f5a9edbe5337f1e653`.

## refresh-docs-workflow 30: Fail-fast ratchet

Head: `5428b044176f95248e6916dc00dd89c0df154078`. GNU Make 4.3. Exit: 0.

Working directory: `$LANES/682-pp-pin3`.

```sh
python3 scripts/measure_fail_fast.py --check
python3 scripts/measure_fail_fast.py --selftest
```

Log: `$VALIDATION_STORAGE/682-a554/round2/refresh/docs-workflow/30.log`; 12,682 bytes; SHA-256 `3fbed56aa0724496465ce6f185d931ddb1a3ee49bb28a1ff77e1051981a700dd`.

## refresh-docs-workflow 31: TODO ownership gate

Head: `5428b044176f95248e6916dc00dd89c0df154078`. GNU Make 4.3. Exit: 0.

Working directory: `$LANES/682-pp-pin3`.

```sh
python3 scripts/check_todo_ownership.py
python3 scripts/check_todo_ownership.py --selftest
```

Log: `$VALIDATION_STORAGE/682-a554/round2/refresh/docs-workflow/31.log`; 2,745 bytes; SHA-256 `10561e66d8780f7ff930a768aa20aa5a4b96ba78ee29ab2ee537deb577c0df67`.

## refresh-docs-workflow 32: Test-evidence ratchet

Head: `5428b044176f95248e6916dc00dd89c0df154078`. GNU Make 4.3. Exit: 0.

Working directory: `$LANES/682-pp-pin3`.

```sh
python3 scripts/measure_test_evidence.py --check
python3 scripts/measure_test_evidence.py --selftest
```

Log: `$VALIDATION_STORAGE/682-a554/round2/refresh/docs-workflow/32.log`; 20,766 bytes; SHA-256 `6162e40a0b084c014771b2f9a22fcbaf6fa61f425fac6dfe2cd03604e6f2ce65`.

## refresh-docs-workflow 33: Mechanical hygiene ratchet

Head: `5428b044176f95248e6916dc00dd89c0df154078`. GNU Make 4.3. Exit: 0.

Working directory: `$LANES/682-pp-pin3`.

```sh
python3 scripts/check_hygiene.py --check
python3 scripts/check_hygiene.py --selftest
```

Log: `$VALIDATION_STORAGE/682-a554/round2/refresh/docs-workflow/33.log`; 3,847 bytes; SHA-256 `278016932202046492104d01ce45472981270e852379d098f33d0251024769eb`.

## refresh-docs-workflow 34: SystemVerilog idiom gate

Head: `5428b044176f95248e6916dc00dd89c0df154078`. GNU Make 4.3. Exit: 0.

Working directory: `$LANES/682-pp-pin3`.

```sh
python3 scripts/check_sv_idiom.py
python3 scripts/check_sv_idiom.py --selftest
```

Log: `$VALIDATION_STORAGE/682-a554/round2/refresh/docs-workflow/34.log`; 3,173 bytes; SHA-256 `ccd900273b796fdfcf74e586f952eadfc9f6f6b1ad448b891183f939a49df728`.

## refresh-docs-workflow 35: C and C++ idiom gate

Head: `5428b044176f95248e6916dc00dd89c0df154078`. GNU Make 4.3. Exit: 0.

Working directory: `$LANES/682-pp-pin3`.

```sh
python3 scripts/check_cpp_idiom.py
python3 scripts/check_cpp_idiom.py --selftest
```

Log: `$VALIDATION_STORAGE/682-a554/round2/refresh/docs-workflow/35.log`; 3,909 bytes; SHA-256 `b8717d3988b724a233037e112619b6056ae6a75066ade22db0cb1f23cb435591`.

## refresh-docs-workflow 36: Python idiom gate

Head: `5428b044176f95248e6916dc00dd89c0df154078`. GNU Make 4.3. Exit: 0.

Working directory: `$LANES/682-pp-pin3`.

```sh
python3 scripts/check_py_idiom.py
python3 scripts/check_py_idiom.py --selftest
```

Log: `$VALIDATION_STORAGE/682-a554/round2/refresh/docs-workflow/36.log`; 2,992 bytes; SHA-256 `e14702c126a3bb1c93f88f0b3c5fd09127f315a38d7de6b44979b740a5f0e227`.

## refresh-docs-workflow 37: Shell idiom gate

Head: `5428b044176f95248e6916dc00dd89c0df154078`. GNU Make 4.3. Exit: 0.

Working directory: `$LANES/682-pp-pin3`.

```sh
python3 scripts/check_sh_idiom.py
python3 scripts/check_sh_idiom.py --selftest
```

Log: `$VALIDATION_STORAGE/682-a554/round2/refresh/docs-workflow/37.log`; 2,696 bytes; SHA-256 `a57f331056f1f93e369a05fc919fd7d91a98638253282a970a118711a46e20e1`.

## refresh-docs-workflow 38: CI event and SHA contract gate

Head: `5428b044176f95248e6916dc00dd89c0df154078`. GNU Make 4.3. Exit: 0.

Working directory: `$LANES/682-pp-pin3`.

```sh
python3 scripts/ci_events.py --check
python3 scripts/ci_events.py --selftest
```

Log: `$VALIDATION_STORAGE/682-a554/round2/refresh/docs-workflow/38.log`; 151,577 bytes; SHA-256 `d7490f337de8e6f9456bdd2d75332bb10b44de58765e9cab1054d4b0d00e34a5`.

## refresh-docs-workflow 39: Local act runner contract gate

Head: `5428b044176f95248e6916dc00dd89c0df154078`. GNU Make 4.3. Exit: 0.

Working directory: `$LANES/682-pp-pin3`.

```sh
python3 scripts/act_ci.py --selftest
```

Log: `$VALIDATION_STORAGE/682-a554/round2/refresh/docs-workflow/39.log`; 36,483 bytes; SHA-256 `876a6eca5975005e4e1d1ddddad9f74d2443039a10df8b7f590e4c781632fdab`.

## refresh-docs-workflow 40: Doc cited-path gate

Head: `5428b044176f95248e6916dc00dd89c0df154078`. GNU Make 4.3. Exit: 0.

Working directory: `$LANES/682-pp-pin3`.

```sh
python3 scripts/check_doc_paths.py
```

Log: `$VALIDATION_STORAGE/682-a554/round2/refresh/docs-workflow/40.log`; 85 bytes; SHA-256 `14e8073fd597e8c2e74483ee4f15374aa0f669038c0af1acafb7b47d130467ff`.

## refresh-docs-workflow 41: Archive integrity gate

Head: `5428b044176f95248e6916dc00dd89c0df154078`. GNU Make 4.3. Exit: 0.

Working directory: `$LANES/682-pp-pin3`.

```sh
python3 scripts/check_archive.py
python3 scripts/check_archive.py --selftest
```

Log: `$VALIDATION_STORAGE/682-a554/round2/refresh/docs-workflow/41.log`; 128 bytes; SHA-256 `1a15e66a07892f544c4b9bee75201ff9acaf3edd2c37963a780f8473466d50cb`.

## refresh-docs-workflow 42: Per-page contents gate

Head: `5428b044176f95248e6916dc00dd89c0df154078`. GNU Make 4.3. Exit: 0.

Working directory: `$LANES/682-pp-pin3`.

```sh
python3 scripts/gen_toc.py --selftest
python3 scripts/gen_toc.py --verify-anchors
python3 scripts/gen_toc.py --check
```

Log: `$VALIDATION_STORAGE/682-a554/round2/refresh/docs-workflow/42.log`; 196 bytes; SHA-256 `36c8da18e4e51f6b3aec96cfb64f354aa3ed5a316faf8c7d2b9d4be36d11fe91`.

## refresh-docs-workflow 43: AEM store generator self-test

Head: `5428b044176f95248e6916dc00dd89c0df154078`. GNU Make 4.3. Exit: 0.

Working directory: `$LANES/682-pp-pin3`.

```sh
python3 avdecc/gen_aem_store.py --self-test
```

Log: `$VALIDATION_STORAGE/682-a554/round2/refresh/docs-workflow/43.log`; 3,596 bytes; SHA-256 `9f126bf9dfc7cb552a2414b98d2792449dc4ae126395997750d5039cb896f022`.

## refresh-docs-workflow 44: Sweep/build shape gate

Head: `5428b044176f95248e6916dc00dd89c0df154078`. GNU Make 4.3. Exit: 0.

Working directory: `$LANES/682-pp-pin3`.

```sh
python3 scripts/check_sweep_shape.py --self-test
```

Log: `$VALIDATION_STORAGE/682-a554/round2/refresh/docs-workflow/44.log`; 19,682 bytes; SHA-256 `2962726b80aba6c16ad55a00fdbd9b4907af69342b6b111405e89b7f4b98c349`.

## refresh-docs-workflow 45: Deploy shape gate

Head: `5428b044176f95248e6916dc00dd89c0df154078`. GNU Make 4.3. Exit: 0.

Working directory: `$LANES/682-pp-pin3`.

```sh
python3 scripts/check_deploy_shape.py --self-test
```

Log: `$VALIDATION_STORAGE/682-a554/round2/refresh/docs-workflow/45.log`; 9,270 bytes; SHA-256 `6e4bb815d4a015fc437da1e1584f8755b4feba5ab5272421126ca193b0a58610`.

## refresh-docs-workflow 46: Entity shape gate

Head: `5428b044176f95248e6916dc00dd89c0df154078`. GNU Make 4.3. Exit: 0.

Working directory: `$LANES/682-pp-pin3`.

```sh
python3 scripts/check_entity_shape.py --self-test
```

Log: `$VALIDATION_STORAGE/682-a554/round2/refresh/docs-workflow/46.log`; 25,694 bytes; SHA-256 `7c1cc4d5ce778537bd27790e075eb0d8159cf6c1281870eb96142e9465eff19c`.

## refresh-docs-workflow 47: Fetch the engine authority the builder derives from

Head: `5428b044176f95248e6916dc00dd89c0df154078`. GNU Make 4.3. Exit: 0.

Working directory: `$LANES/682-pp-pin3`.

```sh
git submodule update --init gptp-processor
```

Log: `$VALIDATION_STORAGE/682-a554/round2/refresh/docs-workflow/47.log`; 0 bytes; SHA-256 `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`.

## refresh-docs-workflow 48: Advertised-vs-emitted gate (green since 2026-07-28, item 00)

Head: `5428b044176f95248e6916dc00dd89c0df154078`. GNU Make 4.3. Exit: 0.

Working directory: `$LANES/682-pp-pin3`.

```sh
python3 -m pip install --quiet pyyaml
python3 scripts/check_wire_accountability.py --self-test
```

Log: `$VALIDATION_STORAGE/682-a554/round2/refresh/docs-workflow/48.log`; 4,965 bytes; SHA-256 `bd97b8b53304baf2b912ac2e4ec507e3b8f9ae4c5c2511b5dc69a41d2cbdd3d4`.

## refresh-docs-workflow 49: Strip git metadata, then run the docs gate

Head: `5428b044176f95248e6916dc00dd89c0df154078`. GNU Make 4.3. Exit: 0.

Working directory: `$VALIDATION_STORAGE/682-a554/round2/refresh/docs-no-git`.

```sh
rm -rf .git
python3 scripts/docs_check.py
python3 scripts/check_feature_status.py
```

Log: `$VALIDATION_STORAGE/682-a554/round2/refresh/docs-workflow/49.log`; 225 bytes; SHA-256 `61b434a5b050726a78dd7f6a13e73571394c8107723278946e505e7c5b71c713`.

