[A560]

Historical round-1 evidence; Round 2 evidence is in HANDOFF.md and ROUND2-GATES.md.


# Gate evidence

Relates to #665. Logs are retained in the assigned disk scratch directory. Names below are relative to that directory; hashes identify the full raw artifacts without copying builds or packages into this packet. Commands ran in the foreground and were not piped. `${SCRATCH}`, `${SDK}`, `${LWSRP}` and `${CGREEN}` denote caller-selected disk locations.

The final parent firmware sources were tested before committing them as `50d492c12789e1d80bf11f547e7fe53e02b4bdb9`. Earlier evidence remains applicable only where the corresponding inputs are unchanged. Hosted contexts, the exhaustive repository-wide RTL/synthesis merge bar, independent review and candidate-merge validation remain publication/integration obligations; this packet does not claim them.

## Primary commands

| Command | rc | Result and log |
|---|---:|---|
| `python3 sw/firmware/ctrl/test/test_ctrl_firmware.py --require-rv32 --self-test --jobs 4 --build-dir "${SCRATCH}/firmware-guard-final"` | 0 | All host, debug, timing, differential, entity and RV32 arms; 97 existing and 43 SRP mutants; two pin controls. `firmware-guard-final.log` |
| `python3 sw/firmware/gtest/fw_coverage.py --write --jobs 4` | 0 | Generator records 15 files, 100% after existing exclusions. `coverage-guard-write.log` |
| `python3 sw/firmware/gtest/fw_coverage.py --check --jobs 4` | 0 | Ratchet passes; SRP 359 lines / 342 arcs, no exclusions. `coverage-guard-check.log` |
| `python3 sw/firmware/gtest/fw_rv32_selftest.py --require-rv32` | 0 | 17 negative controls pass. `rv32-nvm-final-0.log` |
| `python3 sw/firmware/ctrl_nvm/test/test_ctrl_nvm.py --require-rv32 --jobs 4` | 0 | 434 saved-state cases and required RV32 builds pass. `nvm-normal-final.log` |
| `make -C "${SCRATCH}/mailbox-gate/tb/verilator/mbx" -j1 VERILATOR="${SCRATCH}/verilator-j8"` | 0 | Both RTL bus adapters, model differential, IF=2 and five mutations pass. `mailbox-gate.log` |
| `make -C "${SCRATCH}/processor-gates/tb/srp_stream_fsms" -j1 VERILATOR="${SCRATCH}/verilator-j8"` | 0 | 1,219 checks and shape walks pass. `processor-srp_stream_fsms.log` |
| `make -C "${SCRATCH}/processor-gates/tb/srp_top" -j1 VERILATOR="${SCRATCH}/verilator-j8"` | 0 | 2,200 checks and storage-shape runs pass. `processor-srp_top.log` |
| `python3 scripts/ci_events.py --selftest` | 0 | Final firmware workflow: 2,358 self-test arms pass. `ci-events-final.log` |

## Documentation, quality and gate controls

The following commands each returned zero. Later successful duplicates supersede their earlier run. The CI self-test in the primary table supersedes the earlier workflow version.

| Command | rc | Raw log |
|---|---:|---|
| `python3 -B scripts/docs_check.py` | 0 | `guard-quality-0.log` |
| `python3 -B scripts/check_doc_paths.py` | 0 | `guard-quality-1.log` |
| `python3 -B scripts/check_doc_style.py` | 0 | `docs-final-02.log` |
| `python3 -B scripts/check_doc_style.py --selftest` | 0 | `docs-final-03.log` |
| `python3 -B scripts/check_feature_status.py` | 0 | `docs-final-04.log` |
| `python3 -B scripts/check_baremetal_only.py --check` | 0 | `docs-final-05.log` |
| `python3 -B scripts/check_baremetal_only.py --selftest` | 0 | `docs-final-06.log` |
| `python3 -B scripts/ci_events.py --check` | 0 | `guard-quality-6.log` |
| `python3 -B scripts/ci_events.py --selftest` | 0 | `docs-final-08.log` |
| `python3 -B scripts/ci_scope.py --selftest` | 0 | `docs-final-09.log` |
| `python3 -B scripts/gen_toc.py --selftest` | 0 | `docs-final-10.log` |
| `python3 -B scripts/gen_toc.py --verify-anchors` | 0 | `docs-final-11.log` |
| `python3 -B scripts/gen_toc.py --check` | 0 | `guard-quality-5.log` |
| `python3 -B scripts/check_em_dash.py --base db9aa8c9b135b34ff3d070a979dee70440b37cc6` | 0 | `guard-quality-7.log` |
| `python3 -B docs/DOC_MAP.gen.py --check` | 0 | `docs-final-14.log` |
| `python3 -B docs/DOC_MAP.gen.py --selftest` | 0 | `docs-final-15.log` |
| `python3 -B scripts/check_archive.py` | 0 | `docs-final-16.log` |
| `python3 -B scripts/check_archive.py --selftest` | 0 | `docs-final-17.log` |
| `python3 -B scripts/check_cpp_idiom.py` | 0 | `guard-quality-2.log` |
| `python3 -B scripts/check_cpp_idiom.py --selftest` | 0 | `docs-final-19.log` |
| `python3 -B scripts/check_py_idiom.py` | 0 | `guard-quality-3.log` |
| `python3 -B scripts/check_py_idiom.py --selftest` | 0 | `docs-final-21.log` |
| `python3 -B scripts/check_hygiene.py --check` | 0 | `guard-quality-4.log` |
| `python3 -B scripts/check_hygiene.py --selftest` | 0 | `docs-final-23.log` |
| `python3 -B scripts/check_todo_ownership.py` | 0 | `docs-final-24.log` |
| `python3 -B scripts/check_todo_ownership.py --selftest` | 0 | `docs-final-25.log` |
| `python3 -B sw/firmware/gtest/fw_coverage.py --selftest` | 0 | `docs-final-27.log` |
| `python3 -B sw/firmware/gtest/tally_selftest.py --mutants` | 0 | `docs-final-28.log` |
| `python3 -B sw/mailbox/gen_mailbox.py --check` | 0 | `docs-final-29.log` |
| `python3 -B scripts/measure_control_flow.py --selftest` | 0 | `docs-extra-00.log` |
| `python3 -B scripts/measure_cohesion.py --selftest` | 0 | `docs-extra-01.log` |
| `python3 -B scripts/measure_naming.py --check` | 0 | `docs-extra-02.log` |
| `python3 -B scripts/measure_naming.py --selftest` | 0 | `docs-extra-03.log` |
| `python3 -B scripts/check_port_contracts.py` | 0 | `docs-extra-04.log` |
| `python3 -B scripts/check_port_contracts.py --selftest` | 0 | `docs-extra-05.log` |
| `python3 -B scripts/measure_fail_fast.py --check` | 0 | `guard-quality-9.log` |
| `python3 -B scripts/measure_fail_fast.py --selftest` | 0 | `docs-extra-07.log` |
| `python3 -B scripts/measure_test_evidence.py --check` | 0 | `guard-quality-8.log` |
| `python3 -B scripts/measure_test_evidence.py --selftest` | 0 | `docs-extra-09.log` |
| `python3 -B scripts/check_sv_idiom.py` | 0 | `docs-extra-10.log` |
| `python3 -B scripts/check_sh_idiom.py` | 0 | `docs-extra-11.log` |
| `python3 -B scripts/check_gptp_docs.py --with-submodule` | 0 | `docs-extra-12.log` |
| `python3 -B scripts/check_gptp_docs.py --selftest` | 0 | `docs-extra-13.log` |
| `python3 -B scripts/check_soc_sources.py` | 0 | `docs-extra-14.log` |
| `python3 -B scripts/check_soc_sources.py --selftest` | 0 | `docs-extra-15.log` |
| `python3 -B scripts/check_rtl_source_lists.py` | 0 | `docs-extra-16.log` |
| `python3 -B scripts/check_rtl_source_lists.py --selftest` | 0 | `docs-extra-17.log` |
| `python3 -B scripts/check_entity_shape.py --self-test` | 0 | `docs-extra-18.log` |
| `python3 -B scripts/check_sweep_shape.py --self-test` | 0 | `docs-extra-19.log` |
| `python3 -B scripts/check_deploy_shape.py --self-test` | 0 | `docs-extra-20.log` |
| `python3 -B scripts/gen_hdl_reference.py --selftest` | 0 | `docs-extra-21.log` |
| `python3 -B scripts/gen_hdl_reference.py --output ${SCRATCH}/hdl-reference` | 0 | `docs-extra-22.log` |
| `python3 -B scripts/lint_rtl.py --check` | 0 | `docs-extra-23.log` |

## Builder bank

All 100 functions in the original main-loop list returned zero, in their original order across foreground batches. `BUILDER-RESULTS.json` records each function and duration. Every original assertion ran. The driver imported the original functions, kept `--require-rv32`, relocated the generated output and resumed only after the last completed function. One indivisible bare-metal contract function ran beyond the intended ten-minute command window; it completed successfully in the foreground.

**One existing optional arm did not run:** gate 11 resource calibration needs the external mf48 place-utilization report, which is absent. This is explicitly a skip, not calibration evidence; no bench access was attempted. No other SKIP appears in the completed batches. This limitation does not affect the SRP firmware build, entity declarations or mailbox gates.

Successful functions came from batches 1, 2, 3 and 5. Batches 1 and 3 did not complete as invocations; only their individually completed functions are banked. Batches 2 and 5 returned zero. Batch 4 repeated the output-path setup failure and supplies no passing function. The final ledger is an aggregate of actual function results, not a claim that every attempted invocation passed.

## Upstream branches

Every Part B branch listed in UPSTREAM.md ran these four commands at its exact head, each rc 0:

```sh
cmake -S "${LWSRP}" -B "${SCRATCH}/final-BRANCH/build" -DCMAKE_BUILD_TYPE=Debug -DCMAKE_PREFIX_PATH="${CGREEN}"
cmake --build "${SCRATCH}/final-BRANCH/build" -j4
ctest --test-dir "${SCRATCH}/final-BRANCH/build" -V
SHLAN_LIBRARY="${SCRATCH}/final-BRANCH/build/libshlan.so" python3 -m behave
```

The behavior command runs from the upstream clone. Its logs are `final-BRANCH/gate-0.log` through `gate-3.log`. Part A retains the original behavior-harness loading failure; Part B's first topic fixes it. Final upstream totals: 24 cgreen tests / 1,914 assertions; three behavior scenarios / ten steps. Fifteen additional source-defect probes each compiled and returned rc 1 with the intended named failed test, then the restored source returned rc 0. `UPSTREAM-MUTANTS.json` in this packet records the exact source replacements. For each row, apply its single replacement in the separate clone, run `cmake --build "${SCRATCH}/final-zephyr-api-docs/build" -j4`, then run `"${SCRATCH}/final-zephyr-api-docs/build/unit_tests"`; require rc 1 and the row’s named failure. Restore the file before the next row, rebuild, and require the normal CTest run to return zero. No test assertion was modified.

## Build placement and limits

The mailbox and processor makefiles ran in scratch replicas of their test directories, with unchanged source inputs linked back to the verified worktree. The wrapper selects Verilator 5.050, replaces the unbounded make worker request with eight, and uses two build slots. It does not alter RTL or test expectations. Python campaign jobs were at most four. No hardware or shipping-image operation was performed.

## Prior attempts and red evidence

Initial long builder and mutation invocations hit command time limits and provide no passing verdict. The first builder attempt also selected the host Verilator and was discarded. Bounded final builder batches select 5.050. The initial shared RV32 negative-control failure exposed the old NVM harness consumer; importing the matching existing #679 consumer fixed it, and the 17-control gate and normal saved-state gate pass. An optional full saved-state mutation attempt timed out; it is not claimed as evidence.

The guard regression deliberately failed before correction: the release case counted seven rather than nine callbacks and changed malformed-input statistics; two debug probes failed to assert. These are preserved as red evidence. Builder recipe attempts 3 and 4 failed because a subprocess used the default generated-output path while the batch driver used scratch. A temporary output-path link made both paths resolve to the same scratch artifacts; assertions were unchanged.

## Artifact hashes

| Artifact | Bytes | SHA-256 |
|---|---:|---|
| `ci-events-final.log` | 151340 | `de0dee2a7be48105906876757461b6081dbfe1b3d5910479f09f836aa6e82393` |
| `coverage-guard-check.log` | 2706 | `f9c67deccd6e83d3605da7774fd6d4a42c79691000a2d1100c7ac86715140a25` |
| `coverage-guard-write.log` | 2727 | `061f0d10f542a0f370c577892bcf67c5f63bff74148c127d02789759f651e24f` |
| `docs-extra-00.log` | 2565 | `34d85283c432e38af30c33dcc6de6b85208e1ec98a538b78e68061d27421972b` |
| `docs-extra-01.log` | 728 | `10f526cea8560a3a39135260553e767b316076d7598559fb5f07e8cfab2c5363` |
| `docs-extra-02.log` | 36608 | `1cf945250501b5b0267ea1d21f976938536502d765b18d75110bfb3bffbc4508` |
| `docs-extra-03.log` | 4026 | `20635e2ee5994ddc3555ad8acef6af506885fef1ccec25b9c4efb88ab4984c02` |
| `docs-extra-04.log` | 421 | `3c1a34d3169cf6f071f2cbb62a8ddca7591338e9f45ee665e1c66758f22c5524` |
| `docs-extra-05.log` | 4619 | `8cbdbe06b994bf0db6efd8d9289a0a237bb965d3a771a9d536aa23e8ae0ae75e` |
| `docs-extra-07.log` | 6597 | `ef92c9eb4e29bf495c938a2ebe16cb2ec7896671a4e7a63ae465c76f5ca8373a` |
| `docs-extra-09.log` | 5659 | `3c818777e9f41c6d64a15fa699cd238a94b030f0ce19981df099f855b97416ba` |
| `docs-extra-10.log` | 218 | `aed2873a1909e4a41b3e6dee6dc5aaab993bbf1ef41f556062a5b377a6a8b167` |
| `docs-extra-11.log` | 235 | `7ace602f03fa0e411862de119cff9d337583f1f2170d920dff65a0e0f39ee6d9` |
| `docs-extra-12.log` | 66 | `7ca87a8501c54854805f1cf90d49b2a8ff6353a1049fd21cf0631569f5024e41` |
| `docs-extra-13.log` | 46 | `200332e4eddfd8a6338d8a4dbe27d2f513de92f951a1aa1f6b25882182bc290e` |
| `docs-extra-14.log` | 85 | `7ea77f321df0437a49feae4436006813f0653a8151945dbf7601fe0e5e289033` |
| `docs-extra-15.log` | 1501 | `d877c9fa9a5d1db2854c5ed3486ca7d2d135944cf3953143bdf63b554f8c3dc0` |
| `docs-extra-16.log` | 153 | `ed979d7e26c3cd7a6f14364c11994089b77632424d04252613eeed458ebc8a95` |
| `docs-extra-17.log` | 3300 | `418b0ce0f1f8a55805a4c0e75385ae0f3c18b83b3af16598f5cfc45b40591f1d` |
| `docs-extra-18.log` | 25693 | `016d0ddb5406a250386877b6de32a63744377f51b3c0ed4249a855b6c681ddb2` |
| `docs-extra-19.log` | 19678 | `a6ad2c6e560c8f06ea5f73a60207e7944a8003b36f44c642f7bac2a1fbb8410d` |
| `docs-extra-20.log` | 9268 | `923dcefaad4562e30213c30f848d642a16a04942e66bf0aeb004f75c6930de9c` |
| `docs-extra-21.log` | 407 | `3bf8423ff446fe9f033a1cc49f434237e2ca7cf0351ccb0d4f3c8195f67a586c` |
| `docs-extra-22.log` | 400 | `51b0be929fa55487b2abfba94235ab22760513e763c02991600d0af499087cc2` |
| `docs-extra-23.log` | 14186 | `65cf027e20af8ebe4174cc753a5a88ea9f25e42a1365b6125c0a8e63dd337b28` |
| `docs-final-02.log` | 47 | `1491d3f6bec03b920cf58f5fb28e6abff4a9d433a758bc0fe5d2db77bf4f53cd` |
| `docs-final-03.log` | 33 | `0acc8195c60dd145a8f17d24b7b07c29074ac131d71893f9cef5f880239dd909` |
| `docs-final-04.log` | 29 | `802f5eeb2f0aa147169f3ddb9c64d4369ca92ab380455195403f2e8ae02490d0` |
| `docs-final-05.log` | 72 | `391631d37280466fe626c5d19a04bb249a9042f6a37b05eb3b48423a432c0537` |
| `docs-final-06.log` | 43 | `09b491b87735efaef68eafe7f45f4fe4ba1f8ad036c0d252d2a93a00906d51f8` |
| `docs-final-08.log` | 150848 | `c711afb09bc9ac7ae1a3202547083356a0c40605868c879174eb28c6b3a52c28` |
| `docs-final-09.log` | 6877 | `cda2e3e13229332d91d0863932d724a7fdeef280c924f262aa43f5d5448c62da` |
| `docs-final-10.log` | 38 | `d7fd5f6ebcdd25e6cf93b623b0fba00cfa32d19c812ce34eb6b8d8b352ac9b32` |
| `docs-final-11.log` | 64 | `069e1ba57535293a64ff4abc42bf720e9f41249f905882f6beab60c118c2348f` |
| `docs-final-14.log` | 61 | `74408f0fbcdfc1c7e22f6eccd3eb299da61cabe9bb4526eed416b31a8bf61e16` |
| `docs-final-15.log` | 60 | `85ddf25d9a99974b71a9c165cbfbbf390be3d7bf74f081b4cc669622a0a562b9` |
| `docs-final-16.log` | 93 | `69d45782911c2958be2fef681f849e9b3915293c938de331bb6885dab21fd46c` |
| `docs-final-17.log` | 35 | `83aa5efe967935657a1678bf63262a7c435d29d571cc08dd2ae8cf6f8569d34a` |
| `docs-final-19.log` | 3593 | `7fd74c4ebf8b2f0a9812a20518981f63c8350a34c535bcde2c7fa6c58fbec2b9` |
| `docs-final-21.log` | 2531 | `d7413b83955948950d15e364a901be97cf05148dad38e97be07b2d63eb46406d` |
| `docs-final-23.log` | 1847 | `2c7b5cb25dc4cc0407fc27441f4bba2291c74fa2aa2b22f1276e129651f615a8` |
| `docs-final-24.log` | 161 | `bc4af51f5ff8f32c90e3cce3b819efa6df182203c56707eef30607ab9bf9bff0` |
| `docs-final-25.log` | 2584 | `696cea82f33dcda09f3d8b1047ee2682f9ca7c6da9348a07813eaf3d3d6f978b` |
| `docs-final-27.log` | 3710 | `3788b02a1c5d91d7ff2c8581f2ed09040261511d92565dd669103fee911dca0b` |
| `docs-final-28.log` | 3982 | `02268c336448885863d0308d88968cde7fe44eedb9743f0589fc01020f7eca11` |
| `docs-final-29.log` | 26 | `9bb7d3a8faff1627f39a3bb7c9462a0b15ec8dd6c94a44c48d2fc7ac515a982f` |
| `final-bare-metal-api-docs/gate-0.log` | 395 | `93e5b92ed5b003f5d8ac6a27a8cc4dd6d27381ae88c7f4affc3791545cde3b5d` |
| `final-bare-metal-api-docs/gate-1.log` | 1223 | `78ff9e586f296504a1ce11366ce1e5626d1c39a892b56292ee4d835b718733d9` |
| `final-bare-metal-api-docs/gate-2.log` | 1043 | `4743bdaff8c46650b316f693d331262fc0edbfefe5db089ddfe626dbbf513cfa` |
| `final-bare-metal-api-docs/gate-3.log` | 1303 | `5028e77862e79ead5f2f66f4789515f311e881e79db25d4c5207b58d1ff51428` |
| `final-freestanding-headers/gate-0.log` | 396 | `a00449c492b04164148619c256aea6518d933460a2631e3a1e28a03a81af5d5c` |
| `final-freestanding-headers/gate-1.log` | 1223 | `edf64f4cff9b759c98ece5b37e6fb2638b22756efec364ba46da48de1711b492` |
| `final-freestanding-headers/gate-2.log` | 1044 | `740cccc99b791f9e6a3df5d4b7a3a5bbf7baeae22b33d0809b909bf77a278369` |
| `final-freestanding-headers/gate-3.log` | 1303 | `5028e77862e79ead5f2f66f4789515f311e881e79db25d4c5207b58d1ff51428` |
| `final-mrp-bounded-storage/gate-0.log` | 395 | `e96c7b9a0e894f62c59de008e0317fdd88ab4b5d6553e439b2b1ca29eda7eebc` |
| `final-mrp-bounded-storage/gate-1.log` | 1223 | `47e05f939d430b0c58a9205793f8dd34ac0badd33c84fabfea56529c75d2c4d9` |
| `final-mrp-bounded-storage/gate-2.log` | 1041 | `769b0e95a44cbdc5d157e4711c1c6b34ba2d0ffe7512e781765d14899f04d8a8` |
| `final-mrp-bounded-storage/gate-3.log` | 1303 | `5028e77862e79ead5f2f66f4789515f311e881e79db25d4c5207b58d1ff51428` |
| `final-mrp-pdu-segmentation/gate-0.log` | 396 | `66761798fcaf0ece9af46c883f080f9309fe6ee43e1269358c16d8b3e090b350` |
| `final-mrp-pdu-segmentation/gate-1.log` | 1223 | `313dd63e790c23439b42a4ad97ed926f7f58064c4fec5415aa7538c468d53954` |
| `final-mrp-pdu-segmentation/gate-2.log` | 1046 | `6773ba9d10c402f977932b69e4c5912a484fcc3da869c5fc3d9b1f69deb995c2` |
| `final-mrp-pdu-segmentation/gate-3.log` | 1303 | `5028e77862e79ead5f2f66f4789515f311e881e79db25d4c5207b58d1ff51428` |
| `final-mrp-receive-validation/gate-0.log` | 398 | `1921762100f835f5d536f85dd9c77015e63975d5604965061b098f4a6e3d11e8` |
| `final-mrp-receive-validation/gate-1.log` | 1143 | `b0feb58d97b24a4c49d6e500b1860b181b35b70da657ba56ba59008685cd3185` |
| `final-mrp-receive-validation/gate-2.log` | 1012 | `36f6b1ac614a5812727ca87a93feb00c63b0fbff729c832ebd8a00188a1bdc01` |
| `final-mrp-receive-validation/gate-3.log` | 1303 | `5028e77862e79ead5f2f66f4789515f311e881e79db25d4c5207b58d1ff51428` |
| `final-mrp-registration-updates/gate-0.log` | 400 | `931765006c5a98cc5f66ad37acc097a977a90f4d86f20b9c40dec1fcd8ceb719` |
| `final-mrp-registration-updates/gate-1.log` | 1223 | `6c851ddd2f7e95bdc95d7105c995ce0f84a04df8a953cf88ce72366d13b9cbe7` |
| `final-mrp-registration-updates/gate-2.log` | 1061 | `71fbd5193708cd00151947a3fac432bb89ec28565337b6dccf9f916a4d66c296` |
| `final-mrp-registration-updates/gate-3.log` | 1303 | `5028e77862e79ead5f2f66f4789515f311e881e79db25d4c5207b58d1ff51428` |
| `final-mrp-transmit-opportunities/gate-0.log` | 402 | `86115b7ed6a6f55a63d04c97e86378e47467d6c7571ba923cc035aa820b9095d` |
| `final-mrp-transmit-opportunities/gate-1.log` | 1223 | `742040272633370a0f128d42c5a0cd456e2d5c352803172398127f3a438e4990` |
| `final-mrp-transmit-opportunities/gate-2.log` | 1078 | `ceb001fea976a82a447a368bfdfccfcb51bac3cde609e107299da85bd4a5c69f` |
| `final-mrp-transmit-opportunities/gate-3.log` | 1303 | `5028e77862e79ead5f2f66f4789515f311e881e79db25d4c5207b58d1ff51428` |
| `final-mrp-transmit-retry/gate-0.log` | 394 | `faa484d9f6e969b203dbd2ab9e7385cc02dd6410feff8fda21b5c1e18e056a07` |
| `final-mrp-transmit-retry/gate-1.log` | 1223 | `2a93fff0dd8eb55241c0768a2f01cdf54ef8c761ee9a2cc6de107249fdd81cc8` |
| `final-mrp-transmit-retry/gate-2.log` | 1037 | `24f361c9990359d1c1fed87deb11d774164beae20943ebd38d298eb73102322f` |
| `final-mrp-transmit-retry/gate-3.log` | 1303 | `5028e77862e79ead5f2f66f4789515f311e881e79db25d4c5207b58d1ff51428` |
| `final-mrp-transmit/gate-0.log` | 388 | `6882a09ada1306fb492f696f5e2b37ac2f4fadcf3c39863594dcb78e9cea3285` |
| `final-mrp-transmit/gate-1.log` | 1223 | `58f93ee72a65a040c560fe063a77ec936fde0668c3a3f893d0ae6359c6430d53` |
| `final-mrp-transmit/gate-2.log` | 1013 | `01e42b30b2ada83271725bc73e50b674ff4893aec5d7a68f704fdfda1e2872c1` |
| `final-mrp-transmit/gate-3.log` | 1303 | `5028e77862e79ead5f2f66f4789515f311e881e79db25d4c5207b58d1ff51428` |
| `final-mrp-withdrawal-value/gate-0.log` | 396 | `583d575c80bd19dbba410f69cf12d78bcf9d4a131f17e340c879176cbf2f1b64` |
| `final-mrp-withdrawal-value/gate-1.log` | 1223 | `702725114228a799b93994f4a882cd7bc79b096cd36cbd1274bca99b9900077e` |
| `final-mrp-withdrawal-value/gate-2.log` | 1053 | `02fe6e3b7606574a45920ead7d97fbe06012dde551ad2ad7ab0aaf3babf88bf7` |
| `final-mrp-withdrawal-value/gate-3.log` | 1303 | `a2c7718d0b1083f856bbebabd2788497d044b18cfb70e7dbfd6f693c07e8894b` |
| `final-msrp-context-compatibility/gate-0.log` | 402 | `052ff92145fcf88cf96b35fd33057bf2cd22cf10fc0690c5b1a7cddd0922240d` |
| `final-msrp-context-compatibility/gate-1.log` | 1223 | `8e3f85c45256e5a97a97faff5d73c63b3b418685d4817eac77ecfedd1b5c805f` |
| `final-msrp-context-compatibility/gate-2.log` | 1069 | `dcc739bcbe0dc8f0c79b647fd3f7e64975834e66da86f52f5abd36ef690d2364` |
| `final-msrp-context-compatibility/gate-3.log` | 1303 | `5028e77862e79ead5f2f66f4789515f311e881e79db25d4c5207b58d1ff51428` |
| `final-msrp-listener-new/gate-0.log` | 393 | `a88a76b483728abc74e577f3192df54b462ce854a70e726405371bce883c14ed` |
| `final-msrp-listener-new/gate-1.log` | 1223 | `c06545a8f94e54b80f4ddad0cd8d1f40147a17f7b5774fa14b70436f3059c538` |
| `final-msrp-listener-new/gate-2.log` | 1034 | `c160371343cee628178bca5ed9c44cb5545814e3aade8e82859a566e0e74d057` |
| `final-msrp-listener-new/gate-3.log` | 1303 | `5028e77862e79ead5f2f66f4789515f311e881e79db25d4c5207b58d1ff51428` |
| `final-msrp-talker-replacement/gate-0.log` | 399 | `6722783fb1b554043054a933e35bef43f0609e567195fb21cb2d24e299724b8f` |
| `final-msrp-talker-replacement/gate-1.log` | 1223 | `da667f1298b3307bd341d4b1e2bc633c0e70d2262be4c343705a63b57b4bef4b` |
| `final-msrp-talker-replacement/gate-2.log` | 1059 | `77a50857a381f8192ace7adbf390bbd12149a8d1ddcb58604dcb4b2d687fe883` |
| `final-msrp-talker-replacement/gate-3.log` | 1303 | `5028e77862e79ead5f2f66f4789515f311e881e79db25d4c5207b58d1ff51428` |
| `final-msrp-wire-values/gate-0.log` | 392 | `4533fdcc35b204df715d56a16a7ced1363f4788e49ce7b98f6b41e01c93a4c3a` |
| `final-msrp-wire-values/gate-1.log` | 1064 | `845687d758ebbec3702b295d44fc223f403ace94ecdb28f6f54ecefacd813ff7` |
| `final-msrp-wire-values/gate-2.log` | 947 | `0d754edb959d1fda1c2281f027c124a6d0d2ef9c2ac5c603888424fb334dda14` |
| `final-msrp-wire-values/gate-3.log` | 1303 | `5028e77862e79ead5f2f66f4789515f311e881e79db25d4c5207b58d1ff51428` |
| `final-parser-vector-reads/gate-0.log` | 395 | `7f2a1c7e1a223a976536fa62cccd2bad8654a4f05ebaca3b94ff54e7b1cc203f` |
| `final-parser-vector-reads/gate-1.log` | 1223 | `ce49f2f8bc04627305ec1ba807b64e8040de0ed34b98a28f745b78c34bcf3fea` |
| `final-parser-vector-reads/gate-2.log` | 1040 | `ddbf876195258f39cd100488605b1df30c3a2fdb2bc78976df7d5d668af5709a` |
| `final-parser-vector-reads/gate-3.log` | 1303 | `5028e77862e79ead5f2f66f4789515f311e881e79db25d4c5207b58d1ff51428` |
| `final-test-entrypoints/gate-0.log` | 392 | `473431f47af8f1d1d64dc7b02dd8fedee7bdf760ed0e843f22c9b5838d6a7839` |
| `final-test-entrypoints/gate-1.log` | 904 | `ad3f2ddeeba4c6e48c6c17ab302cb9f3088cb3149d1a288e5a83131b8967c929` |
| `final-test-entrypoints/gate-2.log` | 883 | `b3eefaa300ead3bcea33fede81d9f46ad068aaaa715ac738432b9fcd5e3dc928` |
| `final-test-entrypoints/gate-3.log` | 1303 | `5028e77862e79ead5f2f66f4789515f311e881e79db25d4c5207b58d1ff51428` |
| `final-timer-lifetime/gate-0.log` | 390 | `b9aae31510be61929cc89b82222536ab3d6775b261a89eec3c2f99bea7840c0d` |
| `final-timer-lifetime/gate-1.log` | 981 | `04c699373a233812a5e2949313cd1fec762ee759f6d74057a445df52e3648d1a` |
| `final-timer-lifetime/gate-2.log` | 896 | `d2b6cea6ff384fe358cc623914f97a5010908c2e5bedc45c54960d6277d5caa8` |
| `final-timer-lifetime/gate-3.log` | 1303 | `5028e77862e79ead5f2f66f4789515f311e881e79db25d4c5207b58d1ff51428` |
| `final-zephyr-api-docs/gate-0.log` | 391 | `f7cce71f525923e6451ec1de7eb478afb61e9380b4df336c6cc081bb9ae90319` |
| `final-zephyr-api-docs/gate-1.log` | 1223 | `a27100ef15815a700f915adb93acc1bad4e8ab9955bb123053c03ee0d905f656` |
| `final-zephyr-api-docs/gate-2.log` | 1026 | `ff28bb70ac760855b6d301453d7d0936673a0a3e2134a2af6feef901a381e1ac` |
| `final-zephyr-api-docs/gate-3.log` | 1303 | `5028e77862e79ead5f2f66f4789515f311e881e79db25d4c5207b58d1ff51428` |
| `firmware-guard-final.log` | 78071 | `bd7da5b9906464ae39fddd1db0e832287e3ec149057f8ad30d5bcd44a58a31d7` |
| `guard-quality-0.log` | 128 | `357dbb92cd36745bc8193b6687a71125bb2399806f1413bac53cfd5e82c96755` |
| `guard-quality-1.log` | 100 | `f6b4bf0ee623dc3c0e2d45e1b24678a931ceece007f4eeaf3e06fa47af34c3b4` |
| `guard-quality-2.log` | 316 | `ed373b026aa9b1148dfe2cb2a937a25535eeb5447113fd3320a85a96f0b3777b` |
| `guard-quality-3.log` | 461 | `cb5732359af8d77bf9ca4da41cb88a4ba44c74d8ea7b365b3de84d910142c999` |
| `guard-quality-4.log` | 2000 | `20619e1b8aaff2e03c73203566bd5f0bb0afe6ac18466382a893e744de6a6f28` |
| `guard-quality-5.log` | 94 | `35e7e86e67b2d3d3968be2ae5107b946549d31bc8426a393fdae86c12f341b47` |
| `guard-quality-6.log` | 167 | `617e44ed66b13896b9bf7fa2c76c7242990622e9ced9ba79a693484ad4bd4a77` |
| `guard-quality-7.log` | 140 | `4de3d330cd712651df65cef02083d091865f34639f1a89278db4ee5222626d31` |
| `guard-quality-8.log` | 14635 | `4322b73a4b194c5aedc7a75ca57b7e20bbecce56a56032963eb515d2e1892a2a` |
| `guard-quality-9.log` | 6085 | `bbf0264b3cc1beedf3b725b71c379498d33eceeff22f734695af87a77240563e` |
| `mailbox-gate.log` | 35483 | `c6c78529502f78a7e9fda918816b937a3d7c1a136bbae243ab5eea234b557cce` |
| `nvm-normal-final.log` | 3549 | `ae5c029ad90250ff6a00b2f9e62bd930a6aeaf2f289bb2de349e862a830a5afc` |
| `processor-srp_stream_fsms.log` | 42444 | `1dbbd1a52868d5b60266338b9a46a992572f1e2dc2262b1ccdd30aa75b29903f` |
| `processor-srp_top.log` | 82489 | `688d4f5dd205bcd25b941c2b5c0e6bdc3814a4b48306a3e96c9038fffa2d1491` |
| `reentry-debug-red.log` | 2134 | `71c1a58192f6f64a87ab47cf6f42bc2ab54094ee4329d614671373f1ec5b7e90` |
| `reentry-red.log` | 4976 | `0ee1a86678e5bc832a753362eda6522a45a0bc6421db22d7b7499db7826658af` |
| `rv32-nvm-final-0.log` | 793 | `9cd3b019b88560e4f902812b20cbb7d859405f50f0e686d6d71b6474287e7c94` |
| `upstream-final-results.json` | 2059 | `bd2b765c3af0f6c467fa959dc000d9e14ed93ce4da4668806b5eb751ffadcf24` |
| `upstream-final.diff` | 101728 | `4731eb07c80c290d232a39892b047c372a205bece3e319255aae5baf5beb25a9` |
| `upstream-mutant-0-build.log` | 206 | `66b3a2648ca3ed37bc412c8bcb41e4c86908dbbd093ca2ecccf03268f1e14eb5` |
| `upstream-mutant-0.log` | 694 | `1d951b5479193e119a9962b29012a6c1ae88e6dc04026a5f19ee49460303e72d` |
| `upstream-mutant-1-build.log` | 273 | `fce3a27c1187a8f1c8cca5962e512e283f297ded46c7facb108f283bdfb43958` |
| `upstream-mutant-1.log` | 468 | `01e3f9e1b05a57207f48652358e73a6b7686251a822edc02e3c4ff2609ef24b7` |
| `upstream-mutant-10-build.log` | 207 | `4a63a211209195d3f481c8217a9c40e7415190347d39f8d9d325a192882fcc48` |
| `upstream-mutant-10.log` | 733 | `039d92f19df178231ce2458b0fbb388e582d5febe36c928d3842b0a2e6ae09bf` |
| `upstream-mutant-11-build.log` | 207 | `4a63a211209195d3f481c8217a9c40e7415190347d39f8d9d325a192882fcc48` |
| `upstream-mutant-11.log` | 1841 | `b3dd46dca364f6122c3e30e41eb948f6d08f01a9b7dd4049f2a10a6953f6bb3c` |
| `upstream-mutant-12-build.log` | 207 | `4a63a211209195d3f481c8217a9c40e7415190347d39f8d9d325a192882fcc48` |
| `upstream-mutant-12.log` | 840 | `03f0775f28e02eda73a1e961ef271a0a43377d27d0830dae20aef68a9c1910eb` |
| `upstream-mutant-13-build.log` | 207 | `4a63a211209195d3f481c8217a9c40e7415190347d39f8d9d325a192882fcc48` |
| `upstream-mutant-13.log` | 2545 | `30e79de7d2f2dd2e829a3c87be48db00c263ec760388d387c6d894796637c25e` |
| `upstream-mutant-14-build.log` | 274 | `358945008dd0166202d1a531e86d4b95687162f565dc95c53201c88d1af6786c` |
| `upstream-mutant-14.log` | 796 | `c897eb50289269316435800515fa8c39195a3bb1b6b6391fff3fc01228056054` |
| `upstream-mutant-2-build.log` | 274 | `358945008dd0166202d1a531e86d4b95687162f565dc95c53201c88d1af6786c` |
| `upstream-mutant-2.log` | 735 | `ee9a046dbc4d10f5c86b32bb8eef620f967c51da2d4bb090bcfcdf4f3b5212e7` |
| `upstream-mutant-3-build.log` | 449 | `f1800730018e4af0c7f14cede7ff693c0fc5aca4e4b87cf93607f14c1720f9e9` |
| `upstream-mutant-3.log` | 558 | `18522a7bf41408523918cecaf21d6fe31e4867c57965ac37446fa403cca9742b` |
| `upstream-mutant-4-build.log` | 516 | `eddd604dde710184e13d0683655238e41ddb4a1c042ff080d3bf28b096fc45f5` |
| `upstream-mutant-4.log` | 752 | `cad7e5e325e649473fd18e669bd5dadf4cf519201b21affee5a3ef31db7669de` |
| `upstream-mutant-5-build.log` | 274 | `be670950117d2f3602419346732247f86be4a7d507fa3f64a49bfcfe3996a1ae` |
| `upstream-mutant-5.log` | 1273 | `7cfdfe399ada6223c590de2b18ede816812fd64382900bf029a8e630c06cb5e8` |
| `upstream-mutant-6-build.log` | 207 | `4a63a211209195d3f481c8217a9c40e7415190347d39f8d9d325a192882fcc48` |
| `upstream-mutant-6.log` | 534 | `86bbb9770088ed8d2f0ce62aa2e5d91caf6440307927569189f4b63ba40f1df6` |
| `upstream-mutant-7-build.log` | 207 | `4a63a211209195d3f481c8217a9c40e7415190347d39f8d9d325a192882fcc48` |
| `upstream-mutant-7.log` | 512 | `b53862d7d4fcba729f9fce09c80170893f48bc8ae128695d900dd051b593056a` |
| `upstream-mutant-8-build.log` | 207 | `4a63a211209195d3f481c8217a9c40e7415190347d39f8d9d325a192882fcc48` |
| `upstream-mutant-8.log` | 751 | `9146829aa96ed799624839547809abfad196ca95f4db7a36500202a1ea564887` |
| `upstream-mutant-9-build.log` | 207 | `4a63a211209195d3f481c8217a9c40e7415190347d39f8d9d325a192882fcc48` |
| `upstream-mutant-9.log` | 3248 | `8d52b139b9fbe9dd98d37c96e9b64e5715475af1e60c12516d29e3e1d3de4267` |
| `upstream-mutant-results.json` | 2168 | `bc9e5b73be76a82ba6fe37b990ee21ca32978c4c8ce2a0d09f3bb4ac4d8db757` |
| `upstream-mutants-restored-build.log` | 207 | `cb3ac8dd2786a1df257c01ada0d5c59861df8ed5f619cceb4f01a446c735a0f9` |
| `upstream-mutants-restored.log` | 1026 | `cca5da393ffbc2e9ef955890e628ea8e7b71c4fd385c3ad73368ca75290aafc5` |
| `upstream-mutants.json` | 3505 | `cd152abfab9d0210cda5a8febb68aaf52cf2971ebc27816f47454a09a285cb53` |
| `builder-bank-1.log` | 10483 | `47ec38624c9d556081dc43a8a780deaf0c27cb7208c201d1bfb6a1c1a5ee8ccc` |
| `builder-bank-2.log` | 49500 | `2ee1ef86f10a76118d536b7da71c7da0b72ea3aaaeab9a61e33bed9319dabcb9` |
| `builder-bank-3.log` | 19062 | `e1494e5f6a7497a5ae4aa85c33a56632f046c4e2dfe67b26c5eb509355f55099` |
| `builder-bank-4.log` | 2111 | `69e625b45abed692b9a9f33f7c03de9b4dcd130acd219ef80b0761d306e8ae05` |
| `builder-bank-5.log` | 29389 | `d7fcf61bc66f431547e92ef969ac8ab2a2a2a74e7deb2122c75a4a5f30b3c740` |
| `builder-bank-results.json` | 8990 | `d54b73edc5d275598f3ecd4ca2ef257640e49a0e3a8c3440507ec4f64183b373` |
| `builder_bank.py` | 1543 | `7b8256c9a6ef8fcc7b79cd9e3e41cc936036a0c9bf60b58ce51f73ffad6b48fe` |
| `verilator-j8` | 525 | `931fe933529f8168b9cb26ff335e368a12b15180af1f9cc28578d099cd5d70b6` |
