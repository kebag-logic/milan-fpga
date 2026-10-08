[A560]

# Round 2 gate evidence

Parent head `42a0371affceb2a07a734449d706be01fa5abc9a`. STOP: the mandatory builder contract remains incomplete. All other listed final commands pass.

Commands ran in foreground windows with disk scratch and bounded workers. Logs stay in the assigned scratch directory; the artifact table records hashes and sizes. No package, toolchain or build export is copied into this packet.

| Command | rc | Result | Evidence |
|---|---:|---|---|
| `python3 sw/firmware/ctrl/test/test_ctrl_firmware.py --require-rv32 --self-test --jobs 4 --build-dir "$SCRATCH/firmware-final"` | 0 | Host, debug, shape, wire differential and RV32 arms; 100 control plants, 54 SRP plants and two dependency controls. | `firmware-selftest.log` |
| `srp_mutants.campaign($SCRATCH/srp-mutants-final, $LWSRP, 4)` | 0 | Final 57-plant campaign; every named observable fails. | `srp-head.log` |
| `srp_mutants.campaign with only downlink-receive-accepted selected` | 0 | Final added plant caught, for 58 SRP plants total; exact code below. | `downlink-control.log` |
| `python3 sw/firmware/gtest/fw_coverage.py --write --jobs 4 --keep "$SCRATCH/coverage-final-2"` | 0 | Regenerated 15-file ratchet; no exclusion added. | `coverage-write-final.log` |
| `python3 sw/firmware/gtest/fw_coverage.py --check --jobs 4 --keep "$SCRATCH/coverage-closed"` | 0 | Current source and tests: 100% in all 15 files after existing exclusions. | `coverage-closed.log` |
| `python3 sw/firmware/gtest/fw_rv32_selftest.py --require-rv32` | 0 | 17 shared runtime and header controls. | `docs-53.log` |
| `python3 sw/firmware/ctrl_nvm/test/test_ctrl_nvm.py --require-rv32 --jobs 4` | 0 | 435 tests across five shapes; RV32 builds required. | `nvm-final.log` |
| `make -C "$SCRATCH/mailbox-gate/tb/verilator/mbx" -j1` | 0 | Both bus adapters, co-simulation, IF=2 and five required mutations. | `mailbox-final.log` |
| `make -C "$SCRATCH/processor-gates/tb/srp_stream_fsms" -j1` | 0 | 1219 checks, including shape walks. | `processor-fsms.log` |
| `make -C "$SCRATCH/processor-gates/tb/srp_top" -j1` | 0 | 2200 checks, including storage shapes. | `processor-top.log` |
| `python3 scripts/ci_events.py --selftest` | 0 | 1741 contract items, 2362 arms. | `ci-events-final.log` |
| `python3 sw/mailbox/gen_mailbox.py --check` | 0 | Generated contract is current. | `docs-28.log` |
| `Original builder main-list functions, foreground batches` | 0 for 99 functions | One function remains incomplete; optional gate 11 calibration is NOT RUN. | `builder-4.log` |
| `timeout 550s python3 builder_bank.py, contract function` | 124 twice | Mandatory contract function incomplete. This is the STOP reason. | `builder-2.log; builder-3.log` |
| `ctrl_image_runtime.py, then ctrl_image.py for each shape/interface/base` | 0 | Four F4 images and eight base comparisons, closed RV32I/ILP32 link. | `image-results-final.json` |
| `cmake configure/build; ctest; unit_tests; behave` | 0 | Both profiles; 46 unit cases, 2675 default / 2663 Milan assertions; 3 scenarios / 10 steps. | `lwsrp-reversals.log` |
| `python3 tests/check_reversals.py --work-dir "$SCRATCH/lwsrp-reversals" --prefix "$CGREEN"` | 0 | All 40 compiled upstream reversals detected and restored source green. | `lwsrp-reversals.log` |

## Campaign reproduction

The complete public firmware command now runs all 58 SRP plants. The full command above passed before the final four controls were added. A subsequent complete 57-plant campaign and the last single-plant delta pass against unchanged production code. The final coverage command reruns every positive host test, including the last added down-link receive observation.

To reproduce the last delta independently:

```python
import sys
from pathlib import Path
sys.path.insert(0, "sw/firmware/ctrl/test")
import srp_mutants
srp_mutants.DEFECTS = tuple(d for d in srp_mutants.DEFECTS
                           if d.name == "downlink-receive-accepted")
raise SystemExit(int(srp_mutants.campaign(Path("$SCRATCH/downlink"),
                                         Path("third_party/lwSRP").resolve(), 4)))
```

Substitute the scratch path before running. Removing the selection runs all 58 plants. No assertion or failed-observable matcher is changed.

## Documentation and source-quality gates

The recorded interpreter uses the provisioned Markdown dependencies for renderer-dependent commands and the system interpreter for the CI contract.

| Command | rc | Log |
|---|---:|---|
| `python3 -B scripts/docs_check.py` | 0 | `docs-00.log` |
| `python3 -B scripts/check_doc_paths.py` | 0 | `docs-01.log` |
| `python3 -B scripts/check_doc_style.py` | 0 | `docs-02.log` |
| `python3 -B scripts/check_doc_style.py --selftest` | 0 | `docs-03.log` |
| `python3 -B scripts/check_feature_status.py` | 0 | `docs-04.log` |
| `python3 -B scripts/check_baremetal_only.py --check` | 0 | `docs-05.log` |
| `python3 -B scripts/check_baremetal_only.py --selftest` | 0 | `docs-06.log` |
| `python3 -B scripts/ci_events.py --check` | 0 | `docs-07.log` |
| `python3 -B scripts/ci_scope.py --selftest` | 0 | `docs-09.log` |
| `python3 -B docs/DOC_MAP.gen.py --check` | 0 | `docs-14.log` |
| `python3 -B docs/DOC_MAP.gen.py --selftest` | 0 | `docs-15.log` |
| `python3 -B scripts/check_archive.py` | 0 | `docs-16.log` |
| `python3 -B scripts/check_archive.py --selftest` | 0 | `docs-17.log` |
| `python3 -B scripts/check_cpp_idiom.py --selftest` | 0 | `docs-19.log` |
| `python3 -B scripts/check_py_idiom.py --selftest` | 0 | `docs-21.log` |
| `python3 -B scripts/check_hygiene.py --check` | 0 | `docs-22.log` |
| `python3 -B scripts/check_hygiene.py --selftest` | 0 | `docs-23.log` |
| `python3 -B scripts/check_todo_ownership.py` | 0 | `docs-24.log` |
| `python3 -B scripts/check_todo_ownership.py --selftest` | 0 | `docs-25.log` |
| `python3 -B sw/firmware/gtest/fw_coverage.py --selftest` | 0 | `docs-26.log` |
| `python3 -B sw/firmware/gtest/tally_selftest.py --mutants` | 0 | `docs-27.log` |
| `python3 -B sw/mailbox/gen_mailbox.py --check` | 0 | `docs-28.log` |
| `python3 -B scripts/measure_control_flow.py --selftest` | 0 | `docs-29.log` |
| `python3 -B scripts/measure_cohesion.py --selftest` | 0 | `docs-30.log` |
| `python3 -B scripts/measure_naming.py --check` | 0 | `docs-31.log` |
| `python3 -B scripts/measure_naming.py --selftest` | 0 | `docs-32.log` |
| `python3 -B scripts/check_port_contracts.py` | 0 | `docs-33.log` |
| `python3 -B scripts/check_port_contracts.py --selftest` | 0 | `docs-34.log` |
| `python3 -B scripts/measure_fail_fast.py --check` | 0 | `docs-35.log` |
| `python3 -B scripts/measure_fail_fast.py --selftest` | 0 | `docs-36.log` |
| `python3 -B scripts/measure_test_evidence.py --check` | 0 | `docs-37.log` |
| `python3 -B scripts/measure_test_evidence.py --selftest` | 0 | `docs-38.log` |
| `python3 -B scripts/check_sv_idiom.py` | 0 | `docs-39.log` |
| `python3 -B scripts/check_sh_idiom.py` | 0 | `docs-40.log` |
| `python3 -B scripts/check_gptp_docs.py --with-submodule` | 0 | `docs-41.log` |
| `python3 -B scripts/check_gptp_docs.py --selftest` | 0 | `docs-42.log` |
| `python3 -B scripts/check_soc_sources.py` | 0 | `docs-43.log` |
| `python3 -B scripts/check_soc_sources.py --selftest` | 0 | `docs-44.log` |
| `python3 -B scripts/check_rtl_source_lists.py` | 0 | `docs-45.log` |
| `python3 -B scripts/check_rtl_source_lists.py --selftest` | 0 | `docs-46.log` |
| `python3 -B scripts/check_entity_shape.py --self-test` | 0 | `docs-47.log` |
| `python3 -B scripts/check_sweep_shape.py --self-test` | 0 | `docs-48.log` |
| `python3 -B scripts/check_deploy_shape.py --self-test` | 0 | `docs-49.log` |
| `python3 -B scripts/lint_rtl.py --check` | 0 | `docs-52.log` |
| `python3 -B sw/firmware/gtest/fw_rv32_selftest.py --require-rv32` | 0 | `docs-53.log` |
| `python3 -B scripts/ci_events.py --selftest` | 0 | `ci-events-final.log` |
| `python3 -B scripts/gen_toc.py --selftest` | 0 | `docs-10.log` |
| `python3 -B scripts/gen_toc.py --verify-anchors` | 0 | `docs-11.log` |
| `python3 -B scripts/gen_toc.py --check` | 0 | `docs-12.log` |
| `python3 -B scripts/check_em_dash.py --base d51b373ad7e8e8381af2797be3ebb8ee45c62e3c` | 0 | `docs-13.log` |
| `python3 -B scripts/check_cpp_idiom.py` | 0 | `docs-18.log` |
| `python3 -B scripts/check_py_idiom.py` | 0 | `docs-20.log` |
| `python3 -B scripts/gen_hdl_reference.py --selftest` | 0 | `docs-50.log` |
| `python3 -B scripts/gen_hdl_reference.py --output $SCRATCH/hdl-reference` | 0 | `docs-51.log` |
| `python3 -B scripts/check_cpp_idiom.py` | 0 | `final-check_cpp_idiom.py.log` |
| `python3 -B scripts/check_py_idiom.py` | 0 | `final-check_py_idiom.py.log` |
| `python3 -B scripts/docs_check.py` | 0 | `final-docs_check.py.log` |
| `python3 -B scripts/check_hygiene.py --check` | 0 | `final-check_hygiene.py.log` |
| Upstream: `python3 doc/tools/check_sentences.py` | 0 | `upstream-doc-0.log` |
| Upstream: `python3 doc/tools/check_references.py` | 0 | `upstream-doc-1.log` |
| Upstream: `python3 doc/tools/check_references.py --self-test` | 0 | `upstream-doc-2.log` |
| Upstream: `python3 doc/tools/check_links.py --github-auth` | 0 | `upstream-doc-3.log` |

## Execution details and prior attempts

The mailbox recipe ran from a scratch test-directory copy, with the unchanged HDL, firmware and common harness referenced from the candidate worktree. The processor makefiles reused their scratch test directories and unchanged pinned sources. The compiler wrapper selects version 5.050, limits each build to eight make workers and holds one of two process locks. Campaign drivers use at most four workers.

The builder driver invokes the original 100 functions in original order, saving only completed zero-exit functions. Two attempts at `test_baremetal_profile_contract` each hit the 550-second window. The remaining independent functions then ran; the pending function is explicitly omitted from the passing ledger. ROUND2-BUILDER.json contains all 99 results and both timeouts. Gate 11 needs an absent external place-utilization report; its calibration is not claimed. No test or acceptance criterion was weakened to remove either limitation.

Earlier red attempts are retained. They include expected pre-fix behavior failures, stale mutation planting sites, a crash-only retry plant rejected as insufficient evidence, a missing scratch harness link, missing Markdown dependencies, the pre-merge CI step name, source-style findings, and a direct campaign invocation given a missing/wrong reuse include directory. The canonical full firmware command passes all 100 merged controls. The final receive test first lost one coverage arc when it replaced stable link-down input with adjacent edges; it now covers both, with a new discriminating plant. Only the final passing logs are banked; incomplete attempts are not passing evidence.

Linked size was measured at `181e3e1ac62cf768532087ee647c94c554338c8c`. All production source, runtime and size-fixture bytes are unchanged at the final head; subsequent commits only strengthen tests and restore the inherited executable bit. ROUND2-SIZE.json retains that measured head rather than relabeling the artifact.

## Artifact hashes

All names below are relative to the assigned round-2 scratch directory.

| Artifact | Bytes | SHA-256 |
|---|---:|---|
| `adapter-closed.log` | 12036 | `8b8a08e2b506bdbb0a0e9f3d2d83a2329a585285ce4e2f9b77322506ac177df7` |
| `adapter-final-2.log` | 12036 | `a1833afba7f8b2a09d6e3569332d5922f84fe388c62341306ebd581b8a34adf0` |
| `adapter-final.log` | 686671 | `680c4b4b4282273f215808aaa6f19f876ac37af467834aefc931c89445a32253` |
| `adapter-guards.log` | 12034 | `2aebd494ab2f4e2cdb945266ddc69b05d2a36e95783f727e9252043a1aebb63a` |
| `adapter.log` | 11002 | `3d4b82155fb01616ba8c54a8f1da8bceb345cb96d20fb9d277b930ce9d751d4a` |
| `before-fixes.log` | 8834 | `b25a5a560084c1179fa108bd22b4c512dd94e0c428d784b4a1e50176e243121c` |
| `builder-1.log` | 11021 | `099b9729995538e849118e0409dc2792f6f7c85bc858a291e9c6c20414fab196` |
| `builder-2.log` | 506 | `3cb98679c178f670e5b4ce0c4d718dfe448bda0b023b2f1e1d3ac3b2ed7f516c` |
| `builder-3.log` | 535 | `6fa9264834ffcb637bfa67cf71db014bb23117e8bb544686577afeba1f07a93c` |
| `builder-4.log` | 46427 | `0734d3e1cd56e91f394ec184311f98e948ba1c2a03388e9c494400d28cff1597` |
| `ci-events-final.log` | 151471 | `db420a4b83a96d53cefdd88cc69322ed20d7ac02ec28012258d3175fdb7eea37` |
| `coverage-check.log` | 2706 | `e4bc4d5c14199ea781e5a06b287d375873c0a971dfebdfc43a7029b9ac156c65` |
| `coverage-closed.log` | 2706 | `e4bc4d5c14199ea781e5a06b287d375873c0a971dfebdfc43a7029b9ac156c65` |
| `coverage-ctrl-2.log` | 6136 | `39f12122fb8ee87af2b5afaa73e9e1dd72c0dc7784ccf8b58133c0387b6e81dc` |
| `coverage-head.log` | 2796 | `b4e9f866b1f3d33995315c5823664bd04582d546f4ec40e9ee9405133499b77b` |
| `coverage-write-final.log` | 2727 | `43dbb9f8b1122396fada6728a02da4675e609015ce729051a126b877cf67e459` |
| `coverage-write.log` | 2727 | `5a968c22339cc94269fc75bc449b7c15684552e423af759d77ba8a7e66de7709` |
| `coverage.log` | 2965 | `e10238140ddfdc5cc57ff9ae340b6bf1913a4c3210637e169f3a663e088ccb6f` |
| `ctrl-mutants-final.log` | 18840 | `c185db1c83c859c1131c074923f7bca59eb90dc14219b8707830a41172a0d2c0` |
| `ctrl-mutants.log` | 18840 | `c185db1c83c859c1131c074923f7bca59eb90dc14219b8707830a41172a0d2c0` |
| `docs-00.log` | 128 | `54907fa47d23a984cae9e36189e2aa0e111eb7f78280948ab3d9eb57b34acb4b` |
| `docs-01.log` | 85 | `a34a22b91783fd13cff50a728b782a4260336456542731b5a8f777c17d5c7f87` |
| `docs-02.log` | 47 | `1491d3f6bec03b920cf58f5fb28e6abff4a9d433a758bc0fe5d2db77bf4f53cd` |
| `docs-03.log` | 33 | `0acc8195c60dd145a8f17d24b7b07c29074ac131d71893f9cef5f880239dd909` |
| `docs-04.log` | 29 | `802f5eeb2f0aa147169f3ddb9c64d4369ca92ab380455195403f2e8ae02490d0` |
| `docs-05.log` | 72 | `da751982198d0f5e2f596da261edef69e5551787ae29236553989575e0b88a6d` |
| `docs-06.log` | 43 | `09b491b87735efaef68eafe7f45f4fe4ba1f8ad036c0d252d2a93a00906d51f8` |
| `docs-07.log` | 167 | `617e44ed66b13896b9bf7fa2c76c7242990622e9ced9ba79a693484ad4bd4a77` |
| `docs-08.log` | 112 | `66ff829cdfd77c5b5c714c54610e3918d9a542b9f6c0840266c46fa44e8892cb` |
| `docs-09.log` | 6877 | `cda2e3e13229332d91d0863932d724a7fdeef280c924f262aa43f5d5448c62da` |
| `docs-10.log` | 38 | `d7fd5f6ebcdd25e6cf93b623b0fba00cfa32d19c812ce34eb6b8d8b352ac9b32` |
| `docs-11.log` | 64 | `fbcdbabe0c602923ea3d082f57a2fa2c96fc0020677277a7064bb7b4b9a4085b` |
| `docs-12.log` | 94 | `327a49b965f12e7f77c6ab1ae5812d3fed54f2dd64786e400f71111120c97fbd` |
| `docs-13.log` | 140 | `9936bf7a108524b565b824b75815fc15581ef2e205a99bfa3bc9212b1889522e` |
| `docs-14.log` | 61 | `74408f0fbcdfc1c7e22f6eccd3eb299da61cabe9bb4526eed416b31a8bf61e16` |
| `docs-15.log` | 60 | `85ddf25d9a99974b71a9c165cbfbbf390be3d7bf74f081b4cc669622a0a562b9` |
| `docs-16.log` | 93 | `69d45782911c2958be2fef681f849e9b3915293c938de331bb6885dab21fd46c` |
| `docs-17.log` | 35 | `83aa5efe967935657a1678bf63262a7c435d29d571cc08dd2ae8cf6f8569d34a` |
| `docs-18.log` | 316 | `4f37b0cf782484c207b3ab78799290797a61c8aa342b598baa2500226183f384` |
| `docs-19.log` | 3593 | `7fd74c4ebf8b2f0a9812a20518981f63c8350a34c535bcde2c7fa6c58fbec2b9` |
| `docs-20.log` | 461 | `81c6db80d8cd5eb7922df87a0b1d4235e0023de2dc877e2837ff5d1194e39f4b` |
| `docs-21.log` | 2531 | `d7413b83955948950d15e364a901be97cf05148dad38e97be07b2d63eb46406d` |
| `docs-22.log` | 2000 | `30d803ec0c6f62e13a0fa664d995c164c5492e0ca88f55e226a2287948dc391f` |
| `docs-23.log` | 1847 | `2c7b5cb25dc4cc0407fc27441f4bba2291c74fa2aa2b22f1276e129651f615a8` |
| `docs-24.log` | 161 | `2583a791e02823f48fd87fb2c77bd0fcca1641edd540f1ddc0bae5256115c984` |
| `docs-25.log` | 2584 | `696cea82f33dcda09f3d8b1047ee2682f9ca7c6da9348a07813eaf3d3d6f978b` |
| `docs-26.log` | 3710 | `3788b02a1c5d91d7ff2c8581f2ed09040261511d92565dd669103fee911dca0b` |
| `docs-27.log` | 3982 | `02268c336448885863d0308d88968cde7fe44eedb9743f0589fc01020f7eca11` |
| `docs-28.log` | 26 | `9bb7d3a8faff1627f39a3bb7c9462a0b15ec8dd6c94a44c48d2fc7ac515a982f` |
| `docs-29.log` | 2565 | `34d85283c432e38af30c33dcc6de6b85208e1ec98a538b78e68061d27421972b` |
| `docs-30.log` | 728 | `10f526cea8560a3a39135260553e767b316076d7598559fb5f07e8cfab2c5363` |
| `docs-31.log` | 36608 | `1cf945250501b5b0267ea1d21f976938536502d765b18d75110bfb3bffbc4508` |
| `docs-32.log` | 4026 | `20635e2ee5994ddc3555ad8acef6af506885fef1ccec25b9c4efb88ab4984c02` |
| `docs-33.log` | 421 | `3c1a34d3169cf6f071f2cbb62a8ddca7591338e9f45ee665e1c66758f22c5524` |
| `docs-34.log` | 4619 | `8cbdbe06b994bf0db6efd8d9289a0a237bb965d3a771a9d536aa23e8ae0ae75e` |
| `docs-35.log` | 6085 | `bbf0264b3cc1beedf3b725b71c379498d33eceeff22f734695af87a77240563e` |
| `docs-36.log` | 6597 | `ef92c9eb4e29bf495c938a2ebe16cb2ec7896671a4e7a63ae465c76f5ca8373a` |
| `docs-37.log` | 14871 | `30d8fb61edeb6851416d834317922c33ff8744eccd8c133a10e72e49282400bf` |
| `docs-38.log` | 5895 | `9665bb06c04a7169e36eb253ae73089a4786ac51c2db1b5c8f5a67e8e090f9b2` |
| `docs-39.log` | 218 | `aed2873a1909e4a41b3e6dee6dc5aaab993bbf1ef41f556062a5b377a6a8b167` |
| `docs-40.log` | 235 | `7ace602f03fa0e411862de119cff9d337583f1f2170d920dff65a0e0f39ee6d9` |
| `docs-41.log` | 66 | `7ca87a8501c54854805f1cf90d49b2a8ff6353a1049fd21cf0631569f5024e41` |
| `docs-42.log` | 46 | `200332e4eddfd8a6338d8a4dbe27d2f513de92f951a1aa1f6b25882182bc290e` |
| `docs-43.log` | 85 | `7ea77f321df0437a49feae4436006813f0653a8151945dbf7601fe0e5e289033` |
| `docs-44.log` | 1501 | `d877c9fa9a5d1db2854c5ed3486ca7d2d135944cf3953143bdf63b554f8c3dc0` |
| `docs-45.log` | 153 | `ed979d7e26c3cd7a6f14364c11994089b77632424d04252613eeed458ebc8a95` |
| `docs-46.log` | 3300 | `418b0ce0f1f8a55805a4c0e75385ae0f3c18b83b3af16598f5cfc45b40591f1d` |
| `docs-47.log` | 25693 | `016d0ddb5406a250386877b6de32a63744377f51b3c0ed4249a855b6c681ddb2` |
| `docs-48.log` | 19678 | `7b8a50c9d048a3c866a551fd45f747ffc38f3fd3a241fbed468e1a4425c37526` |
| `docs-49.log` | 9268 | `923dcefaad4562e30213c30f848d642a16a04942e66bf0aeb004f75c6930de9c` |
| `docs-50.log` | 414 | `625d99900c3c0d12dbc101e649287a5315fbd5ab4b5c22f66b47ab9e4a36939c` |
| `docs-51.log` | 407 | `207013a7316f1205834b6db0af20885fdc5c7ee977064d52c31c3736921910be` |
| `docs-52.log` | 14186 | `dfbecc1b77d0e5b6f59fbe7d1bd7df35529343118be7e3e7239059ab18d82d32` |
| `docs-53.log` | 793 | `9cd3b019b88560e4f902812b20cbb7d859405f50f0e686d6d71b6474287e7c94` |
| `docs-batch-2.log` | 395 | `7461fa00ef1172527e03a09f6341017a0ac22fea55825cf81384235ae79f87e9` |
| `docs-batch.log` | 2115 | `4f51d360643fc0532e1fdd2e2a634e279528bfe7c754aae200b1f6369a2789df` |
| `downlink-control.log` | 556 | `546f6d215fb245bd81f66e94bc411a60a41cfc49f3b70a4b948fecda175f5761` |
| `final-check_cpp_idiom.py.log` | 316 | `4f37b0cf782484c207b3ab78799290797a61c8aa342b598baa2500226183f384` |
| `final-check_hygiene.py.log` | 2000 | `30d803ec0c6f62e13a0fa664d995c164c5492e0ca88f55e226a2287948dc391f` |
| `final-check_py_idiom.py.log` | 461 | `7a5bedb4da671f58fa46b7f91806a2d44ec33b07640e3ee45ea31f9290be5803` |
| `final-docs_check.py.log` | 128 | `54907fa47d23a984cae9e36189e2aa0e111eb7f78280948ab3d9eb57b34acb4b` |
| `firmware-closed.log` | 35875 | `439eef0726a230bb83d90e3a60e72bca143d922d9d7cd437d458d4814a56386b` |
| `firmware-final.log` | 35875 | `439eef0726a230bb83d90e3a60e72bca143d922d9d7cd437d458d4814a56386b` |
| `firmware-selftest.log` | 85424 | `18489ea59a9738392e06f2073ebc286ef11ea0b89f88d1bb51c3c548238b2dd0` |
| `firmware.log` | 34903 | `522470d7c22e171e9352e4f89424f67855c5e4487682391704d65fdbfd54d269` |
| `image-dev-1x1_tdm8-if1.log` | 979 | `49dc6bdcecf2e66776aa39fff5fa65107bcffe9d1346485037e4988a9d1e3053` |
| `image-dev-1x1_tdm8-if2.log` | 1279 | `3b4a855591cec00869ed4ba3fa19286938c96c234e0efbf0328204d318d64698` |
| `image-dev-8x8-if1.log` | 974 | `8921c3f96811d5b2025421ee75745fe87b45b945fcc4f494a6623c7f8fa25bca` |
| `image-dev-8x8-if2.log` | 1259 | `06e4e60d4699dcd59819a7cd5753da1f3ece588f3f78b70a05277312a4640b07` |
| `image-fc-1x1_tdm8-if1.log` | 979 | `9d0bd0a3ebe846bc8ae017bec6fb29f7a1121cfb561bbabc395a75e6511950f3` |
| `image-fc-1x1_tdm8-if2.log` | 1276 | `21a6d4c0d9b3c43e1ca409b37d62d60e734c9b6d111a0110f9de00be7071b5c5` |
| `image-fc-8x8-if1.log` | 974 | `fcbd9a39cd0c7612167f49c03bd20d4806dcc832e11f385c154f6e7b468bc225` |
| `image-fc-8x8-if2.log` | 1256 | `56639a6ebe9552bab7fa614c502fdc9963bbe27800b558fe583e86617b4c7318` |
| `image-final-endstation_ax7101_1x1_tdm8-if1.log` | 1030 | `5289ccd3be72e4017872272a231cbfeee48cdc91988bf028a708f85b83db90bf` |
| `image-final-endstation_ax7101_1x1_tdm8-if2.log` | 1392 | `aa1b720df86b6270b9ca9e98257cb658a2db40abcc1bfbe1797049bb1744cba0` |
| `image-final-endstation_ax7101_8x8-if1.log` | 1027 | `57d15490c3d1ae813dfb443501c18aa4a04dad7189ef669865d06f430c662c1d` |
| `image-final-endstation_ax7101_8x8-if2.log` | 1373 | `743b2989d7444a16fd48beb0e72ea463a4e2720cded418d9c01f0c0321d79e00` |
| `image-head-1x1_tdm8-if1.log` | 1030 | `b90430919bbebd871d4f2c8720ede98fa4e25e1ad2a3e04a638db8798a68ced5` |
| `image-head-1x1_tdm8-if2.log` | 1335 | `4e1ddbed2f8f46015e3d4b68b4b1e947614b0883fa10927a99f7ea81b44303d0` |
| `image-head-8x8-if1.log` | 1027 | `297a2fbecbb54de8727eb93f87cde4b899b4d6e4bd5a46c4f8b7eacf53437d38` |
| `image-head-8x8-if2.log` | 1316 | `fa94fb27da5e83d201b2e154ed8dbdaa4e88c58d92f331f3f76db3fc9d000796` |
| `lwsrp-reversals.log` | 3386 | `6f754147d2982dbf78beed2c7e0dcdedba8fd5e46f203dc76713450cc67883dd` |
| `mailbox-final.log` | 33838 | `813e87785b234b496a51ac1683520babefa19cd47fea1f6be87f9217a4562f94` |
| `mailbox.log` | 5865 | `aaf37a39c99f203f5e9c14d3dcfb0fbcbd146e329d8ca7852d1cd045925df6fd` |
| `new-controls-final.log` | 1606 | `9963eeae179c312431dae050608ad4a23ffe160247140df78e9d59b0638fe650` |
| `new-controls.log` | 1916 | `a51ff18c342c9f7b333350718088c42530bb74e7730da63a2d923312b1e6efb5` |
| `nvm-final.log` | 3981 | `aca49c80a6f07d0deff6a0d261526709c396b3c5cafa419c3e8bbf360a0f1175` |
| `processor-fsms.log` | 5393 | `b9a6e365bcc714a8431af810f88484cc17a9e9381a4fe986849aabb5a6fc9828` |
| `processor-top.log` | 31582 | `a733e38686ca5f09ffafd4a8a2994b9f99f4e6d96b0dbf154fe7b8caf75f4aa6` |
| `runtime-final.log` | 0 | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |
| `srp-head.log` | 30721 | `4f339438028f11c38716414938218addda321b8bc75b0d25cb4a3191e0739814` |
| `srp-mutants-closed.log` | 29070 | `06d60e09c3f7a244164d69ac4eee7ba9c780bf476708a7bd4a554b7142a6ade0` |
| `srp-mutants-final.log` | 29070 | `06d60e09c3f7a244164d69ac4eee7ba9c780bf476708a7bd4a554b7142a6ade0` |
| `srp-mutants.log` | 28057 | `46038eae4ed165a8f2a2ce1582d9e3f196b6b4922ae2ccd2c03c788fd8abcf54` |
| `upstream-doc-0.log` | 3487 | `9c41f57b2003d039e079af2fc4d75a5020851090402c8659add278e88fd410eb` |
| `upstream-doc-1.log` | 3470 | `9e9fdb53e50d5cee8f6b3bf90290533bb4027fe4980ac4e115dc22947ae35b8c` |
| `upstream-doc-2.log` | 43 | `7e68a151a2a780cf539294ed60b0be326c24af9329a53af527c0acdfa479b6f6` |
| `upstream-doc-3.log` | 1372 | `6ad9f081ab91f0cea227650f401067bea089a78fa1371d71ae58ca9eace5840f` |
| `builder-bank-results.json` | 8901 | `1ddaee53433cf1b84d2d4121dfe8071ea3e89c9a13a09a92f4bbd0c8a43828dd` |
| `builder_bank.py` | 1692 | `49c1990ba45877761fd47cc636d3996e1f81186f028ab321bef3c1f47fba19e5` |
| `runtime-final/provenance.json` | 37170 | `c19324362c265f2c2c745502703e49072ca57d35ce03c6f203b5039cf7e8ef22` |
| `image-results-final.json` | 13420 | `894b74e940a516db34689be670067875104811cc535f5fd23d2be0defe7fca7e` |

## Final upstream rerun

The local topic head was rebuilt and checked again after the documentation-only commit. Each command returned zero.

| Command | rc | Log |
|---|---:|---|
| `cmake --build $SCRATCH/lwsrp-build --parallel 4` | 0 | `upstream-final-0.log` |
| `ctest --test-dir $SCRATCH/lwsrp-build --output-on-failure` | 0 | `upstream-final-1.log` |
| `$SCRATCH/lwsrp-build/unit_tests` | 0 | `upstream-final-2.log` |
| `python3 -m behave` | 0 | `upstream-final-3.log` |

The behavior command runs in the separate upstream clone with `SHLAN_LIBRARY` selecting the rebuilt shared library and the test runtime library on its search path.

| Artifact | Bytes | SHA-256 |
|---|---:|---|
| `upstream-final-0.log` | 57 | `998f6e296b514c27dc8adc51a62d4bde81dcea6967285cc19d6639daa0e50c28` |
| `upstream-final-1.log` | 211 | `a88279ab900a9763dcd46db5e690946ea17edbf115ef323fc9a15844d408ba70` |
| `upstream-final-2.log` | 339 | `aa53f9a1f8f445eac3c72931df11f13a72bfb70dc4987cd1d4433b9e32270826` |
| `upstream-final-3.log` | 1303 | `5028e77862e79ead5f2f66f4789515f311e881e79db25d4c5207b58d1ff51428` |
