# Receipts index

Generated from the files present in this directory (after sanitizing host paths to `<scratch>`,
`<lane>`, `<tools>`, `<management>`, `<home>`). sha256 is truncated to 16 hex digits.

| File | Bytes | sha256 | First line |
|---|---:|---|---|
| `boot/README.md` | 802 | `44b5a89ee727616b` | The split boot simulation, the platform ledger and the memory test at da8a8b84, on a clean clone. |
| `boot/boot-1x1-da8a8b84.log` | 10,504 | `06399b4e1c7ea072` | head da8a8b84e63623e124363eabfe1d1e62844c1453 dirty 0 |
| `boot/boot-8x8-da8a8b84.log` | 10,458 | `83974e17a951923a` | head da8a8b84e63623e124363eabfe1d1e62844c1453 dirty 0 |
| `boot/boot-self-test-da8a8b84.log` | 54,300 | `a261bf55e4112aea` | head da8a8b84e63623e124363eabfe1d1e62844c1453 dirty 0 |
| `boot/plat-ledger-self-test-da8a8b84.log` | 14,894 | `6fe5291bd19d942f` | head da8a8b84e63623e124363eabfe1d1e62844c1453 dirty 0 |
| `boot/test-ctrl-memory-da8a8b84.log` | 52,394 | `69de05d1e10764aa` | test_ctrl_memory: the split placement's firmware memory (#640 M8a) |
| `budget/README.md` | 1,674 | `4a77805685211a64` | The CPU budget's PHY figures at da8a8b84, 1x1/1if and 8x8/1if. |
| `budget/harness-image-identity-da8a8b84.txt` | 493 | `8d2b6f283d1ac9ab` | tree da8a8b84e63623e124363eabfe1d1e62844c1453 porcelain 0 |
| `head/files-changed.txt` | 2,088 | `79f673aad0f8a2c2` | Round 3's commits and files, afa3ea19 (round 2's head) -> da8a8b84 |
| `measure/README.md` | 1,054 | `e2849e054f320770` | The measurements behind da8a8b84's restated figures, taken on a clean clone of c79f1c76 (the code head; da8a8b |
| `measure/boot-1x1-c79f1c76.log` | 10,473 | `3c6a369473e52229` | head c79f1c76c263b0dcec29927b9719e9de4b3c626b dirty 0 |
| `measure/boot-8x8-c79f1c76.log` | 10,427 | `fcae768a858aa26a` | head c79f1c76c263b0dcec29927b9719e9de4b3c626b dirty 0 |
| `measure/fw-coverage-check-c79f1c76.log` | 5,435 | `fff9c3ec690c0f4d` | toolchain: {'cc': 'gcc (GCC) 16.2.1 20260810', 'cxx': 'g++ (GCC) 16.2.1 20260810', 'gcov': 'gcov (GCC) 16.2.1  |
| `measure/plat-ledger-self-test-c79f1c76.log` | 14,861 | `11894fcdce8e57d2` | head c79f1c76c263b0dcec29927b9719e9de4b3c626b dirty 0 |
| `measure/rom-banking.txt` | 1,884 | `83633a1555a87557` | The platform image at each point, as plat_ledger.py --self-test plans it (each point's JSON record): rom and |
| `measure/rom-per-file.txt` | 2,025 | `e6c18f6aa35ed2a0` | rom bytes (.text, .rodata, .srodata, .data load) per object, base 70f4056f (dev-soft-core) -> c79f1c76 (the pl |
| `probes/README.md` | 1,287 | `04f72a2a84704118` | The two reviews' own probes, run at da8a8b84 on a clean clone, from copies of the reviewers' scripts under thi |
| `probes/r851-m3-m3b-words-da8a8b84.txt` | 1,248 | `57dc9efa54f0d392` | R851's m3 and m3b at da8a8b84: each mutant's suite run (scripts/mutants.sh's phy_probe.sh), its failing test a |
| `probes/r851-mutants-da8a8b84.txt` | 451 | `969764aca212fb92` | m1 rc=1 FAILED  ] PlatPhy.P14AResetPhyIsAdvertisedAgain |
| `probes/r851-retry-probe-da8a8b84.log` | 2,226 | `3e8c2764b4ad1c49` | --- <scratch>/c-r3f/sw/firmware/ctrl/test/phy_peer.hpp	2026-11-16 23:10:29.033306718 +0100 |
| `probes/r852-retry-control-da8a8b84.log` | 4,360 | `87dd9829230c8edb` | [==========] Running 34 tests from 3 test suites. |
| `probes/r852-retry-probe-da8a8b84.log` | 4,360 | `203752e90f938bbe` | [==========] Running 34 tests from 3 test suites. |
| `workflows/README.md` | 2,121 | `6410a4fbdc3bb4eb` | Workflow jobs at da8a8b84, step by step, each job on its own fresh clean clone of the head (run_wf.py, as in |
| `workflows/batch-a.log` | 3,494 | `672415e9c218c534` | 23:10:39 start docs.yml wire-accountability |
| `workflows/batch-b.log` | 1,194 | `a81651995e4034b1` | 23:10:39 start rtl-fast.yml changes |
| `workflows/batch-c.log` | 337 | `402ff1d4392128ef` | 23:10:39 start rtl-fast.yml firmware-control-mutants |
| `workflows/batch-d.log` | 342 | `5a73d11d5438a2d3` | 23:46:37 start elaborate.yml elaborate-gates-0 |
| `workflows/batch-e.log` | 553 | `4c23cd75f92b3edd` | 23:46:37 start elaborate.yml elaborate-gates-1 |
| `workflows/large-logs.sha256` | 397 | `a06ddeface77bcbe` | Workflow step logs over 200 KB, kept in scratch and recorded here by size and sha256 (the log as written, befo |
| `workflows/logs/docs__docs-check-no-git__ci_step_1.log` | 252 | `329972051deb7fce` | # head da8a8b84e63623e124363eabfe1d1e62844c1453 workflow docs.yml job docs-check-no-git step ci_step_1: Retain |
| `workflows/logs/docs__docs-check-no-git__ci_step_1.rc` | 2 | `9a271f2a916b0b6e` | 0 |
| `workflows/logs/docs__docs-check-no-git__ci_step_2.log` | 230 | `0c2d2d72804dad9c` | # head da8a8b84e63623e124363eabfe1d1e62844c1453 workflow docs.yml job docs-check-no-git step ci_step_2: Set CP |
| `workflows/logs/docs__docs-check-no-git__ci_step_2.rc` | 2 | `9a271f2a916b0b6e` | 0 |
| `workflows/logs/docs__docs-check-no-git__ci_step_3.log` | 470 | `f174431623ad1bc2` | # head da8a8b84e63623e124363eabfe1d1e62844c1453 workflow docs.yml job docs-check-no-git step ci_step_3: Strip  |
| `workflows/logs/docs__docs-check-no-git__ci_step_3.rc` | 2 | `9a271f2a916b0b6e` | 0 |
| `workflows/logs/docs__docs-check__DONE` | 9 | `fab506c9d858683b` | failed 0 |
| `workflows/logs/docs__docs-check__tree-after.txt` | 55 | `3661c2cd6e799acc` | head da8a8b84e63623e124363eabfe1d1e62844c1453 |
| `workflows/logs/docs__docs-gates-0__DONE` | 9 | `fab506c9d858683b` | failed 0 |
| `workflows/logs/docs__docs-gates-0__ci_step_1.log` | 370 | `f23c71b8ca0b0629` | # head da8a8b84e63623e124363eabfe1d1e62844c1453 workflow docs.yml job docs-gates-0 step ci_step_1: Set CPU-der |
| `workflows/logs/docs__docs-gates-0__ci_step_1.rc` | 2 | `9a271f2a916b0b6e` | 0 |
| `workflows/logs/docs__docs-gates-0__ci_step_21.log` | 934 | `1308e7d74f18fb40` | # head da8a8b84e63623e124363eabfe1d1e62844c1453 workflow docs.yml job docs-gates-0 step ci_step_21: Fetch the  |
| `workflows/logs/docs__docs-gates-0__ci_step_21.rc` | 2 | `9a271f2a916b0b6e` | 0 |
| `workflows/logs/docs__docs-gates-0__ci_step_5.log` | 490 | `a33459ae0d29c9c3` | # head da8a8b84e63623e124363eabfe1d1e62844c1453 workflow docs.yml job docs-gates-0 step ci_step_5: Install the |
| `workflows/logs/docs__docs-gates-0__ci_step_5.rc` | 2 | `9a271f2a916b0b6e` | 0 |
| `workflows/logs/docs__docs-gates-0__ci_step_52.log` | 565 | `55467bfbc2b6fc0a` | # head da8a8b84e63623e124363eabfe1d1e62844c1453 workflow docs.yml job docs-gates-0 step ci_step_52: Fetch inve |
| `workflows/logs/docs__docs-gates-0__ci_step_52.rc` | 2 | `9a271f2a916b0b6e` | 0 |
| `workflows/logs/docs__docs-gates-0__ci_step_7.log` | 490 | `0ec8643ddf048ff2` | # head da8a8b84e63623e124363eabfe1d1e62844c1453 workflow docs.yml job docs-gates-0 step ci_step_7: Install the |
| `workflows/logs/docs__docs-gates-0__ci_step_7.rc` | 2 | `9a271f2a916b0b6e` | 0 |
| `workflows/logs/docs__docs-gates-0__gate_1.log` | 1,349 | `13b55b995feecb1a` | # head da8a8b84e63623e124363eabfe1d1e62844c1453 workflow docs.yml job docs-gates-0 step gate_1: Build the vali |
| `workflows/logs/docs__docs-gates-0__gate_1.rc` | 2 | `9a271f2a916b0b6e` | 0 |
| `workflows/logs/docs__docs-gates-0__gate_10.log` | 613 | `5af9c272567c3752` | # head da8a8b84e63623e124363eabfe1d1e62844c1453 workflow docs.yml job docs-gates-0 step gate_10: Audience diag |
| `workflows/logs/docs__docs-gates-0__gate_10.rc` | 2 | `9a271f2a916b0b6e` | 0 |
| `workflows/logs/docs__docs-gates-0__gate_11.log` | 520 | `68fa999441bfaf58` | # head da8a8b84e63623e124363eabfe1d1e62844c1453 workflow docs.yml job docs-gates-0 step gate_11: Product solut |
| `workflows/logs/docs__docs-gates-0__gate_11.rc` | 2 | `9a271f2a916b0b6e` | 0 |
| `workflows/logs/docs__docs-gates-0__gate_12.log` | 605 | `36159da599bbf5e1` | # head da8a8b84e63623e124363eabfe1d1e62844c1453 workflow docs.yml job docs-gates-0 step gate_12: Verified subm |
| `workflows/logs/docs__docs-gates-0__gate_12.rc` | 2 | `9a271f2a916b0b6e` | 0 |
| `workflows/logs/docs__docs-gates-0__gate_13.log` | 614 | `a65b29f10f444b54` | # head da8a8b84e63623e124363eabfe1d1e62844c1453 workflow docs.yml job docs-gates-0 step gate_13: HDL timing di |
| `workflows/logs/docs__docs-gates-0__gate_13.rc` | 2 | `9a271f2a916b0b6e` | 0 |
| `workflows/logs/docs__docs-gates-0__gate_14.log` | 492 | `5e83aefd89a1e567` | # head da8a8b84e63623e124363eabfe1d1e62844c1453 workflow docs.yml job docs-gates-0 step gate_14: Published dia |
| `workflows/logs/docs__docs-gates-0__gate_14.rc` | 2 | `9a271f2a916b0b6e` | 0 |
| `workflows/logs/docs__docs-gates-0__gate_15.log` | 1,878 | `1a66f7a17fa65ff2` | # head da8a8b84e63623e124363eabfe1d1e62844c1453 workflow docs.yml job docs-gates-0 step gate_15: Milan feature |
| `workflows/logs/docs__docs-gates-0__gate_15.rc` | 2 | `9a271f2a916b0b6e` | 0 |
| `workflows/logs/docs__docs-gates-0__gate_16.log` | 492 | `39c3ee9ceec1a74e` | # head da8a8b84e63623e124363eabfe1d1e62844c1453 workflow docs.yml job docs-gates-0 step gate_16: Traceability  |
| `workflows/logs/docs__docs-gates-0__gate_16.rc` | 2 | `9a271f2a916b0b6e` | 0 |
| `workflows/logs/docs__docs-gates-0__gate_18.log` | 2,984 | `747c039a7ca0e4cb` | # head da8a8b84e63623e124363eabfe1d1e62844c1453 workflow docs.yml job docs-gates-0 step gate_18: Imported gPTP |
| `workflows/logs/docs__docs-gates-0__gate_18.rc` | 2 | `9a271f2a916b0b6e` | 0 |
| `workflows/logs/docs__docs-gates-0__gate_19.log` | 3,669 | `dd88bbab58c82c0f` | # head da8a8b84e63623e124363eabfe1d1e62844c1453 workflow docs.yml job docs-gates-0 step gate_19: Code-quality  |
| `workflows/logs/docs__docs-gates-0__gate_19.rc` | 2 | `9a271f2a916b0b6e` | 0 |
| `workflows/logs/docs__docs-gates-0__gate_21.log` | 477 | `4bc6f5b421326013` | # head da8a8b84e63623e124363eabfe1d1e62844c1453 workflow docs.yml job docs-gates-0 step gate_21: Bare-metal sc |
| `workflows/logs/docs__docs-gates-0__gate_21.rc` | 2 | `9a271f2a916b0b6e` | 0 |
| `workflows/logs/docs__docs-gates-0__gate_24.log` | 51,854 | `a3b8e2577ec81307` | # head da8a8b84e63623e124363eabfe1d1e62844c1453 workflow docs.yml job docs-gates-0 step gate_24: Compiler-abse |
| `workflows/logs/docs__docs-gates-0__gate_24.rc` | 2 | `9a271f2a916b0b6e` | 0 |
| `workflows/logs/docs__docs-gates-0__gate_26.log` | 12,668 | `48618dfb1cef5ef4` | # head da8a8b84e63623e124363eabfe1d1e62844c1453 workflow docs.yml job docs-gates-0 step gate_26: NVM record-sp |
| `workflows/logs/docs__docs-gates-0__gate_26.rc` | 2 | `9a271f2a916b0b6e` | 0 |
| `workflows/logs/docs__docs-gates-0__gate_27.log` | 780 | `41df8f4d749d77ee` | # head da8a8b84e63623e124363eabfe1d1e62844c1453 workflow docs.yml job docs-gates-0 step gate_27: Capture measu |
| `workflows/logs/docs__docs-gates-0__gate_27.rc` | 2 | `9a271f2a916b0b6e` | 0 |
| `workflows/logs/docs__docs-gates-0__gate_28.log` | 26,481 | `03a2f101b544f31b` | # head da8a8b84e63623e124363eabfe1d1e62844c1453 workflow docs.yml job docs-gates-0 step gate_28: Saved-state w |
| `workflows/logs/docs__docs-gates-0__gate_28.rc` | 2 | `9a271f2a916b0b6e` | 0 |
| `workflows/logs/docs__docs-gates-0__gate_29.log` | 5,198 | `08722490ff50dc5e` | # head da8a8b84e63623e124363eabfe1d1e62844c1453 workflow docs.yml job docs-gates-0 step gate_29: SoC source-li |
| `workflows/logs/docs__docs-gates-0__gate_29.rc` | 2 | `9a271f2a916b0b6e` | 0 |
| `workflows/logs/docs__docs-gates-0__gate_30.log` | 3,820 | `83d74fee93f63d94` | # head da8a8b84e63623e124363eabfe1d1e62844c1453 workflow docs.yml job docs-gates-0 step gate_30: RTL source-li |
| `workflows/logs/docs__docs-gates-0__gate_30.rc` | 2 | `9a271f2a916b0b6e` | 0 |
| `workflows/logs/docs__docs-gates-0__gate_31.log` | 40,968 | `d7319b285e64d82a` | # head da8a8b84e63623e124363eabfe1d1e62844c1453 workflow docs.yml job docs-gates-0 step gate_31: Boundary-unit |
| `workflows/logs/docs__docs-gates-0__gate_31.rc` | 2 | `9a271f2a916b0b6e` | 0 |
| `workflows/logs/docs__docs-gates-0__gate_32.log` | 5,399 | `837cf873347cfcfc` | # head da8a8b84e63623e124363eabfe1d1e62844c1453 workflow docs.yml job docs-gates-0 step gate_32: Port contract |
| `workflows/logs/docs__docs-gates-0__gate_32.rc` | 2 | `9a271f2a916b0b6e` | 0 |
| `workflows/logs/docs__docs-gates-0__gate_33.log` | 12,944 | `389bfb5800398d6e` | # head da8a8b84e63623e124363eabfe1d1e62844c1453 workflow docs.yml job docs-gates-0 step gate_33: Fail-fast rat |
| `workflows/logs/docs__docs-gates-0__gate_33.rc` | 2 | `9a271f2a916b0b6e` | 0 |
| `workflows/logs/docs__docs-gates-0__gate_34.log` | 3,105 | `184a67a431f661a0` | # head da8a8b84e63623e124363eabfe1d1e62844c1453 workflow docs.yml job docs-gates-0 step gate_34: TODO ownershi |
| `workflows/logs/docs__docs-gates-0__gate_34.rc` | 2 | `9a271f2a916b0b6e` | 0 |
| `workflows/logs/docs__docs-gates-0__gate_35.log` | 29,146 | `eb3ae105e8468af0` | # head da8a8b84e63623e124363eabfe1d1e62844c1453 workflow docs.yml job docs-gates-0 step gate_35: Test-evidence |
| `workflows/logs/docs__docs-gates-0__gate_35.rc` | 2 | `9a271f2a916b0b6e` | 0 |
| `workflows/logs/docs__docs-gates-0__gate_36.log` | 4,339 | `dbf7ee512e2b4b3e` | # head da8a8b84e63623e124363eabfe1d1e62844c1453 workflow docs.yml job docs-gates-0 step gate_36: Mechanical hy |
| `workflows/logs/docs__docs-gates-0__gate_36.rc` | 2 | `9a271f2a916b0b6e` | 0 |
| `workflows/logs/docs__docs-gates-0__gate_37.log` | 3,538 | `42d562d88c1ac9ed` | # head da8a8b84e63623e124363eabfe1d1e62844c1453 workflow docs.yml job docs-gates-0 step gate_37: SystemVerilog |
| `workflows/logs/docs__docs-gates-0__gate_37.rc` | 2 | `9a271f2a916b0b6e` | 0 |
| `workflows/logs/docs__docs-gates-0__gate_38.log` | 4,270 | `17cec395994344e0` | # head da8a8b84e63623e124363eabfe1d1e62844c1453 workflow docs.yml job docs-gates-0 step gate_38: C and C++ idi |
| `workflows/logs/docs__docs-gates-0__gate_38.rc` | 2 | `9a271f2a916b0b6e` | 0 |
| `workflows/logs/docs__docs-gates-0__gate_39.log` | 3,350 | `ce7b51ce875e0a43` | # head da8a8b84e63623e124363eabfe1d1e62844c1453 workflow docs.yml job docs-gates-0 step gate_39: Python idiom  |
| `workflows/logs/docs__docs-gates-0__gate_39.rc` | 2 | `9a271f2a916b0b6e` | 0 |
| `workflows/logs/docs__docs-gates-0__gate_40.log` | 3,053 | `2af82db42b372c2c` | # head da8a8b84e63623e124363eabfe1d1e62844c1453 workflow docs.yml job docs-gates-0 step gate_40: Shell idiom g |
| `workflows/logs/docs__docs-gates-0__gate_40.rc` | 2 | `9a271f2a916b0b6e` | 0 |
| `workflows/logs/docs__docs-gates-0__gate_43.log` | 461 | `70ae83bfabd90fdb` | # head da8a8b84e63623e124363eabfe1d1e62844c1453 workflow docs.yml job docs-gates-0 step gate_43: Doc cited-pat |
| `workflows/logs/docs__docs-gates-0__gate_43.rc` | 2 | `9a271f2a916b0b6e` | 0 |
| `workflows/logs/docs__docs-gates-0__gate_44.log` | 491 | `82a0403b1affa90f` | # head da8a8b84e63623e124363eabfe1d1e62844c1453 workflow docs.yml job docs-gates-0 step gate_44: Archive integ |
| `workflows/logs/docs__docs-gates-0__gate_44.rc` | 2 | `9a271f2a916b0b6e` | 0 |
| `workflows/logs/docs__docs-gates-0__gate_45.log` | 559 | `2ac4be1d030d01e0` | # head da8a8b84e63623e124363eabfe1d1e62844c1453 workflow docs.yml job docs-gates-0 step gate_45: Per-page cont |
| `workflows/logs/docs__docs-gates-0__gate_45.rc` | 2 | `9a271f2a916b0b6e` | 0 |
| `workflows/logs/docs__docs-gates-0__gate_46.log` | 3,966 | `91bf131d75031707` | # head da8a8b84e63623e124363eabfe1d1e62844c1453 workflow docs.yml job docs-gates-0 step gate_46: AEM store gen |
| `workflows/logs/docs__docs-gates-0__gate_46.rc` | 2 | `9a271f2a916b0b6e` | 0 |
| `workflows/logs/docs__docs-gates-0__gate_47.log` | 20,117 | `27a9caff5e9652ff` | # head da8a8b84e63623e124363eabfe1d1e62844c1453 workflow docs.yml job docs-gates-0 step gate_47: Sweep/build s |
| `workflows/logs/docs__docs-gates-0__gate_47.rc` | 2 | `9a271f2a916b0b6e` | 0 |
| `workflows/logs/docs__docs-gates-0__gate_48.log` | 9,664 | `0535194cdd874314` | # head da8a8b84e63623e124363eabfe1d1e62844c1453 workflow docs.yml job docs-gates-0 step gate_48: Deploy shape  |
| `workflows/logs/docs__docs-gates-0__gate_48.rc` | 2 | `9a271f2a916b0b6e` | 0 |
| `workflows/logs/docs__docs-gates-0__gate_49.log` | 28,098 | `d755d1e9d604ed6e` | # head da8a8b84e63623e124363eabfe1d1e62844c1453 workflow docs.yml job docs-gates-0 step gate_49: Entity shape  |
| `workflows/logs/docs__docs-gates-0__gate_49.rc` | 2 | `9a271f2a916b0b6e` | 0 |
| `workflows/logs/docs__docs-gates-0__gate_50.log` | 135,971 | `95962100683eedf4` | # head da8a8b84e63623e124363eabfe1d1e62844c1453 workflow docs.yml job docs-gates-0 step gate_50: CI scheduling |
| `workflows/logs/docs__docs-gates-0__gate_50.rc` | 2 | `9a271f2a916b0b6e` | 0 |
| `workflows/logs/docs__docs-gates-0__gate_7.log` | 524 | `8eebc542e6a70ffd` | # head da8a8b84e63623e124363eabfe1d1e62844c1453 workflow docs.yml job docs-gates-0 step gate_7: Link health, w |
| `workflows/logs/docs__docs-gates-0__gate_7.rc` | 2 | `9a271f2a916b0b6e` | 0 |
| `workflows/logs/docs__docs-gates-0__gate_8.log` | 502 | `4965591c0a6f348d` | # head da8a8b84e63623e124363eabfe1d1e62844c1453 workflow docs.yml job docs-gates-0 step gate_8: Added-line em- |
| `workflows/logs/docs__docs-gates-0__gate_8.rc` | 2 | `9a271f2a916b0b6e` | 0 |
| `workflows/logs/docs__docs-gates-0__gate_9.log` | 542 | `509d7d9ec3aa4a9b` | # head da8a8b84e63623e124363eabfe1d1e62844c1453 workflow docs.yml job docs-gates-0 step gate_9: Concise audien |
| `workflows/logs/docs__docs-gates-0__gate_9.rc` | 2 | `9a271f2a916b0b6e` | 0 |
| `workflows/logs/docs__docs-gates-0__tree-after.txt` | 55 | `3661c2cd6e799acc` | head da8a8b84e63623e124363eabfe1d1e62844c1453 |
| `workflows/logs/docs__docs-gates-1__DONE` | 9 | `fab506c9d858683b` | failed 0 |
| `workflows/logs/docs__docs-gates-1__ci_step_1.log` | 370 | `6c8ccec206852d13` | # head da8a8b84e63623e124363eabfe1d1e62844c1453 workflow docs.yml job docs-gates-1 step ci_step_1: Set CPU-der |
| `workflows/logs/docs__docs-gates-1__ci_step_1.rc` | 2 | `9a271f2a916b0b6e` | 0 |
| `workflows/logs/docs__docs-gates-1__ci_step_3.log` | 490 | `8a254caf7430b483` | # head da8a8b84e63623e124363eabfe1d1e62844c1453 workflow docs.yml job docs-gates-1 step ci_step_3: Install the |
| `workflows/logs/docs__docs-gates-1__ci_step_3.rc` | 2 | `9a271f2a916b0b6e` | 0 |
| `workflows/logs/docs__docs-gates-1__ci_step_5.log` | 490 | `52ab786bb84965a8` | # head da8a8b84e63623e124363eabfe1d1e62844c1453 workflow docs.yml job docs-gates-1 step ci_step_5: Install the |
| `workflows/logs/docs__docs-gates-1__ci_step_5.rc` | 2 | `9a271f2a916b0b6e` | 0 |
| `workflows/logs/docs__docs-gates-1__ci_step_9.log` | 933 | `9d3d1177fa8e9bf6` | # head da8a8b84e63623e124363eabfe1d1e62844c1453 workflow docs.yml job docs-gates-1 step ci_step_9: Fetch the b |
| `workflows/logs/docs__docs-gates-1__ci_step_9.rc` | 2 | `9a271f2a916b0b6e` | 0 |
| `workflows/logs/docs__docs-gates-1__gate_25_0.log` | 50,908 | `a7c8a8bc2712a929` | # head da8a8b84e63623e124363eabfe1d1e62844c1453 workflow docs.yml job docs-gates-1 step gate_25_0: End-station |
| `workflows/logs/docs__docs-gates-1__gate_25_0.rc` | 2 | `9a271f2a916b0b6e` | 0 |
| `workflows/logs/docs__docs-gates-1__tree-after.txt` | 55 | `3661c2cd6e799acc` | head da8a8b84e63623e124363eabfe1d1e62844c1453 |
| `workflows/logs/docs__docs-gates-2__DONE` | 9 | `fab506c9d858683b` | failed 0 |
| `workflows/logs/docs__docs-gates-2__ci_step_1.log` | 370 | `bc7ad75f2d07ae84` | # head da8a8b84e63623e124363eabfe1d1e62844c1453 workflow docs.yml job docs-gates-2 step ci_step_1: Set CPU-der |
| `workflows/logs/docs__docs-gates-2__ci_step_1.rc` | 2 | `9a271f2a916b0b6e` | 0 |
| `workflows/logs/docs__docs-gates-2__ci_step_3.log` | 490 | `78215a1718f9c0ae` | # head da8a8b84e63623e124363eabfe1d1e62844c1453 workflow docs.yml job docs-gates-2 step ci_step_3: Install the |
| `workflows/logs/docs__docs-gates-2__ci_step_3.rc` | 2 | `9a271f2a916b0b6e` | 0 |
| `workflows/logs/docs__docs-gates-2__ci_step_5.log` | 490 | `5e1b20a215b685c3` | # head da8a8b84e63623e124363eabfe1d1e62844c1453 workflow docs.yml job docs-gates-2 step ci_step_5: Install the |
| `workflows/logs/docs__docs-gates-2__ci_step_5.rc` | 2 | `9a271f2a916b0b6e` | 0 |
| `workflows/logs/docs__docs-gates-2__ci_step_9.log` | 933 | `0b4326e79dadead2` | # head da8a8b84e63623e124363eabfe1d1e62844c1453 workflow docs.yml job docs-gates-2 step ci_step_9: Fetch the b |
| `workflows/logs/docs__docs-gates-2__ci_step_9.rc` | 2 | `9a271f2a916b0b6e` | 0 |
| `workflows/logs/docs__docs-gates-2__gate_25_1.log` | 76,638 | `8d64087e769a675d` | # head da8a8b84e63623e124363eabfe1d1e62844c1453 workflow docs.yml job docs-gates-2 step gate_25_1: End-station |
| `workflows/logs/docs__docs-gates-2__gate_25_1.rc` | 2 | `9a271f2a916b0b6e` | 0 |
| `workflows/logs/docs__docs-gates-2__gate_41.rc` | 2 | `9a271f2a916b0b6e` | 0 |
| `workflows/logs/docs__docs-gates-2__gate_42.log` | 123,978 | `868449788b22bc54` | # head da8a8b84e63623e124363eabfe1d1e62844c1453 workflow docs.yml job docs-gates-2 step gate_42: Local act run |
| `workflows/logs/docs__docs-gates-2__gate_42.rc` | 2 | `9a271f2a916b0b6e` | 0 |
| `workflows/logs/docs__docs-gates-2__tree-after.txt` | 55 | `3661c2cd6e799acc` | head da8a8b84e63623e124363eabfe1d1e62844c1453 |
| `workflows/logs/docs__wire-accountability__DONE` | 9 | `fab506c9d858683b` | failed 0 |
| `workflows/logs/docs__wire-accountability__ci_step_1.log` | 384 | `6393747ddc173fe5` | # head da8a8b84e63623e124363eabfe1d1e62844c1453 workflow docs.yml job wire-accountability step ci_step_1: Set  |
| `workflows/logs/docs__wire-accountability__ci_step_1.rc` | 2 | `9a271f2a916b0b6e` | 0 |
| `workflows/logs/docs__wire-accountability__ci_step_3.log` | 590 | `ff5f26bc7a21052b` | # head da8a8b84e63623e124363eabfe1d1e62844c1453 workflow docs.yml job wire-accountability step ci_step_3: Fetc |
| `workflows/logs/docs__wire-accountability__ci_step_3.rc` | 2 | `9a271f2a916b0b6e` | 0 |
| `workflows/logs/docs__wire-accountability__ci_step_4.log` | 5,493 | `fa45ebff2fe6c4ef` | # head da8a8b84e63623e124363eabfe1d1e62844c1453 workflow docs.yml job wire-accountability step ci_step_4: Adve |
| `workflows/logs/docs__wire-accountability__ci_step_4.rc` | 2 | `9a271f2a916b0b6e` | 0 |
| `workflows/logs/docs__wire-accountability__tree-after.txt` | 55 | `3661c2cd6e799acc` | head da8a8b84e63623e124363eabfe1d1e62844c1453 |
| `workflows/logs/elaborate__elaborate-gates-0__DONE` | 9 | `fab506c9d858683b` | failed 0 |
| `workflows/logs/elaborate__elaborate-gates-0__ci_step_1.log` | 383 | `392936598c32af7b` | # head da8a8b84e63623e124363eabfe1d1e62844c1453 workflow elaborate.yml job elaborate-gates-0 step ci_step_1: S |
| `workflows/logs/elaborate__elaborate-gates-0__ci_step_1.rc` | 2 | `9a271f2a916b0b6e` | 0 |
| `workflows/logs/elaborate__elaborate-gates-0__ci_step_4.log` | 990 | `0a358e1ffd5c406f` | # head da8a8b84e63623e124363eabfe1d1e62844c1453 workflow elaborate.yml job elaborate-gates-0 step ci_step_4: F |
| `workflows/logs/elaborate__elaborate-gates-0__ci_step_4.rc` | 2 | `9a271f2a916b0b6e` | 0 |
| `workflows/logs/elaborate__elaborate-gates-0__gate_15_0.log` | 51,029 | `18fef231c07af087` | # head da8a8b84e63623e124363eabfe1d1e62844c1453 workflow elaborate.yml job elaborate-gates-0 step gate_15_0: E |
| `workflows/logs/elaborate__elaborate-gates-0__gate_15_0.rc` | 2 | `9a271f2a916b0b6e` | 0 |
| `workflows/logs/elaborate__elaborate-gates-0__scope.log` | 18,280 | `816e0dfae6c0a9cd` | # head da8a8b84e63623e124363eabfe1d1e62844c1453 workflow elaborate.yml job elaborate-gates-0 step scope: Decid |
| `workflows/logs/elaborate__elaborate-gates-0__scope.rc` | 2 | `9a271f2a916b0b6e` | 0 |
| `workflows/logs/elaborate__elaborate-gates-0__tree-after.txt` | 55 | `3661c2cd6e799acc` | head da8a8b84e63623e124363eabfe1d1e62844c1453 |
| `workflows/logs/elaborate__elaborate-gates-1__DONE` | 9 | `fab506c9d858683b` | failed 0 |
| `workflows/logs/elaborate__elaborate-gates-1__ci_step_1.log` | 383 | `ce6df90ef0d70fb1` | # head da8a8b84e63623e124363eabfe1d1e62844c1453 workflow elaborate.yml job elaborate-gates-1 step ci_step_1: S |
| `workflows/logs/elaborate__elaborate-gates-1__ci_step_1.rc` | 2 | `9a271f2a916b0b6e` | 0 |
| `workflows/logs/elaborate__elaborate-gates-1__ci_step_23.log` | 547 | `e93ea2e9b59dffd6` | # head da8a8b84e63623e124363eabfe1d1e62844c1453 workflow elaborate.yml job elaborate-gates-1 step ci_step_23:  |
| `workflows/logs/elaborate__elaborate-gates-1__ci_step_23.rc` | 2 | `9a271f2a916b0b6e` | 0 |
| `workflows/logs/elaborate__elaborate-gates-1__ci_step_4.log` | 990 | `a11fb92186fd51e8` | # head da8a8b84e63623e124363eabfe1d1e62844c1453 workflow elaborate.yml job elaborate-gates-1 step ci_step_4: F |
| `workflows/logs/elaborate__elaborate-gates-1__ci_step_4.rc` | 2 | `9a271f2a916b0b6e` | 0 |
| `workflows/logs/elaborate__elaborate-gates-1__gate_15_1.log` | 83,077 | `7d6d3f0e4d38ffa0` | # head da8a8b84e63623e124363eabfe1d1e62844c1453 workflow elaborate.yml job elaborate-gates-1 step gate_15_1: E |
| `workflows/logs/elaborate__elaborate-gates-1__gate_15_1.rc` | 2 | `9a271f2a916b0b6e` | 0 |
| `workflows/logs/elaborate__elaborate-gates-1__gate_19.log` | 1,602 | `a108bf39c4d9191f` | # head da8a8b84e63623e124363eabfe1d1e62844c1453 workflow elaborate.yml job elaborate-gates-1 step gate_19: Sta |
| `workflows/logs/elaborate__elaborate-gates-1__gate_19.rc` | 2 | `9a271f2a916b0b6e` | 0 |
| `workflows/logs/elaborate__elaborate-gates-1__scope.log` | 18,280 | `612652d91e0d1959` | # head da8a8b84e63623e124363eabfe1d1e62844c1453 workflow elaborate.yml job elaborate-gates-1 step scope: Decid |
| `workflows/logs/elaborate__elaborate-gates-1__scope.rc` | 2 | `9a271f2a916b0b6e` | 0 |
| `workflows/logs/elaborate__elaborate-gates-1__tree-after.txt` | 55 | `3661c2cd6e799acc` | head da8a8b84e63623e124363eabfe1d1e62844c1453 |
| `workflows/logs/elaborate__elaborate__DONE` | 9 | `fab506c9d858683b` | failed 0 |
| `workflows/logs/elaborate__elaborate__tree-after.txt` | 55 | `3661c2cd6e799acc` | head da8a8b84e63623e124363eabfe1d1e62844c1453 |
| `workflows/logs/rtl-fast__changes__DONE` | 9 | `fab506c9d858683b` | failed 0 |
| `workflows/logs/rtl-fast__changes__ci_step_1.log` | 218 | `8e9c64d9e4166595` | # head da8a8b84e63623e124363eabfe1d1e62844c1453 workflow rtl-fast.yml job changes step ci_step_1: Set CPU-deri |
| `workflows/logs/rtl-fast__changes__ci_step_1.rc` | 2 | `9a271f2a916b0b6e` | 0 |
| `workflows/logs/rtl-fast__changes__scope.log` | 18,325 | `276a5674a8ebacb4` | # head da8a8b84e63623e124363eabfe1d1e62844c1453 workflow rtl-fast.yml job changes step scope: Classify the cha |
| `workflows/logs/rtl-fast__changes__scope.rc` | 2 | `9a271f2a916b0b6e` | 0 |
| `workflows/logs/rtl-fast__changes__tree-after.txt` | 55 | `3661c2cd6e799acc` | head da8a8b84e63623e124363eabfe1d1e62844c1453 |
| `workflows/logs/rtl-fast__firmware-boundary__DONE` | 9 | `fab506c9d858683b` | failed 0 |
| `workflows/logs/rtl-fast__firmware-boundary__ci_step_1.log` | 381 | `cc14c4596767b5d9` | # head da8a8b84e63623e124363eabfe1d1e62844c1453 workflow rtl-fast.yml job firmware-boundary step ci_step_1: Se |
| `workflows/logs/rtl-fast__firmware-boundary__ci_step_1.rc` | 2 | `9a271f2a916b0b6e` | 0 |
| `workflows/logs/rtl-fast__firmware-boundary__ci_step_3.log` | 1,348 | `a8008297573db067` | # head da8a8b84e63623e124363eabfe1d1e62844c1453 workflow rtl-fast.yml job firmware-boundary step ci_step_3: Fe |
| `workflows/logs/rtl-fast__firmware-boundary__ci_step_3.rc` | 2 | `9a271f2a916b0b6e` | 0 |
| `workflows/logs/rtl-fast__firmware-boundary__ci_step_9.log` | 70,861 | `13a997fe709acefa` | # head da8a8b84e63623e124363eabfe1d1e62844c1453 workflow rtl-fast.yml job firmware-boundary step ci_step_9: Ho |
| `workflows/logs/rtl-fast__firmware-boundary__ci_step_9.rc` | 2 | `9a271f2a916b0b6e` | 0 |
| `workflows/logs/rtl-fast__firmware-boundary__tree-after.txt` | 55 | `3661c2cd6e799acc` | head da8a8b84e63623e124363eabfe1d1e62844c1453 |
| `workflows/logs/rtl-fast__firmware-control-mutants__DONE` | 9 | `fab506c9d858683b` | failed 0 |
| `workflows/logs/rtl-fast__firmware-control-mutants__ci_step_1.log` | 402 | `d9d488f886141bc9` | # head da8a8b84e63623e124363eabfe1d1e62844c1453 workflow rtl-fast.yml job firmware-control-mutants step ci_ste |
| `workflows/logs/rtl-fast__firmware-control-mutants__ci_step_1.rc` | 2 | `9a271f2a916b0b6e` | 0 |
| `workflows/logs/rtl-fast__firmware-control-mutants__ci_step_3.log` | 1,404 | `8d2836d3e53eb8d3` | # head da8a8b84e63623e124363eabfe1d1e62844c1453 workflow rtl-fast.yml job firmware-control-mutants step ci_ste |
| `workflows/logs/rtl-fast__firmware-control-mutants__ci_step_3.rc` | 2 | `9a271f2a916b0b6e` | 0 |
| `workflows/logs/rtl-fast__firmware-control-mutants__ci_step_9.log` | 145,081 | `6e0e34325e43a228` | # head da8a8b84e63623e124363eabfe1d1e62844c1453 workflow rtl-fast.yml job firmware-control-mutants step ci_ste |
| `workflows/logs/rtl-fast__firmware-control-mutants__ci_step_9.rc` | 2 | `9a271f2a916b0b6e` | 0 |
| `workflows/logs/rtl-fast__firmware-control-mutants__tree-after.txt` | 73 | `282194ef9247d8b8` | head da8a8b84e63623e124363eabfe1d1e62844c1453 |
| `workflows/logs/rtl-fast__firmware-unit__DONE` | 9 | `fab506c9d858683b` | failed 0 |
| `workflows/logs/rtl-fast__firmware-unit__ci_step_1.log` | 380 | `2b456dda0626d450` | # head da8a8b84e63623e124363eabfe1d1e62844c1453 workflow rtl-fast.yml job firmware-unit step ci_step_1: Set CP |
| `workflows/logs/rtl-fast__firmware-unit__ci_step_1.rc` | 2 | `9a271f2a916b0b6e` | 0 |
| `workflows/logs/rtl-fast__firmware-unit__ci_step_10.log` | 90,306 | `3c1c4e0a4623e31f` | # head da8a8b84e63623e124363eabfe1d1e62844c1453 workflow rtl-fast.yml job firmware-unit step ci_step_10: Run t |
| `workflows/logs/rtl-fast__firmware-unit__ci_step_10.rc` | 2 | `9a271f2a916b0b6e` | 0 |
| `workflows/logs/rtl-fast__firmware-unit__ci_step_11.log` | 5,227 | `2810a9718c2fab68` | # head da8a8b84e63623e124363eabfe1d1e62844c1453 workflow rtl-fast.yml job firmware-unit step ci_step_11: Run t |
| `workflows/logs/rtl-fast__firmware-unit__ci_step_11.rc` | 2 | `9a271f2a916b0b6e` | 0 |
| `workflows/logs/rtl-fast__firmware-unit__ci_step_12.log` | 9,622 | `36e3760483fc82c0` | # head da8a8b84e63623e124363eabfe1d1e62844c1453 workflow rtl-fast.yml job firmware-unit step ci_step_12: Hold  |
| `workflows/logs/rtl-fast__firmware-unit__ci_step_12.rc` | 2 | `9a271f2a916b0b6e` | 0 |
| `workflows/logs/rtl-fast__firmware-unit__ci_step_3.log` | 1,327 | `708f8ea474de5af9` | # head da8a8b84e63623e124363eabfe1d1e62844c1453 workflow rtl-fast.yml job firmware-unit step ci_step_3: Fetch  |
| `workflows/logs/rtl-fast__firmware-unit__ci_step_3.rc` | 2 | `9a271f2a916b0b6e` | 0 |
| `workflows/logs/rtl-fast__firmware-unit__ci_step_7.log` | 2,388 | `6371d3798701434d` | # head da8a8b84e63623e124363eabfe1d1e62844c1453 workflow rtl-fast.yml job firmware-unit step ci_step_7: Prove  |
| `workflows/logs/rtl-fast__firmware-unit__ci_step_7.rc` | 2 | `9a271f2a916b0b6e` | 0 |
| `workflows/logs/rtl-fast__firmware-unit__tree-after.txt` | 73 | `282194ef9247d8b8` | head da8a8b84e63623e124363eabfe1d1e62844c1453 |
| `workflows/logs/rtl-fast__firmware-verilator__DONE` | 9 | `fab506c9d858683b` | failed 0 |
| `workflows/logs/rtl-fast__firmware-verilator__ci_step_1.log` | 390 | `0dee3a34eda2baef` | # head da8a8b84e63623e124363eabfe1d1e62844c1453 workflow rtl-fast.yml job firmware-verilator step ci_step_1: S |
| `workflows/logs/rtl-fast__firmware-verilator__ci_step_1.rc` | 2 | `9a271f2a916b0b6e` | 0 |
| `workflows/logs/rtl-fast__firmware-verilator__ci_step_11.log` | 554 | `40d0e1fb072e0554` | # head da8a8b84e63623e124363eabfe1d1e62844c1453 workflow rtl-fast.yml job firmware-verilator step ci_step_11:  |
| `workflows/logs/rtl-fast__firmware-verilator__ci_step_11.rc` | 2 | `9a271f2a916b0b6e` | 0 |
| `workflows/logs/rtl-fast__firmware-verilator__ci_step_14.log` | 60,774 | `48627b5c7871f8b4` | # head da8a8b84e63623e124363eabfe1d1e62844c1453 workflow rtl-fast.yml job firmware-verilator step ci_step_14:  |
| `workflows/logs/rtl-fast__firmware-verilator__ci_step_14.rc` | 2 | `9a271f2a916b0b6e` | 0 |
| `workflows/logs/rtl-fast__firmware-verilator__ci_step_3.log` | 1,362 | `0b1724d733d74a98` | # head da8a8b84e63623e124363eabfe1d1e62844c1453 workflow rtl-fast.yml job firmware-verilator step ci_step_3: F |
| `workflows/logs/rtl-fast__firmware-verilator__ci_step_3.rc` | 2 | `9a271f2a916b0b6e` | 0 |
| `workflows/logs/rtl-fast__firmware-verilator__tree-after.txt` | 55 | `3661c2cd6e799acc` | head da8a8b84e63623e124363eabfe1d1e62844c1453 |
| `workflows/not_run-round3.json.txt` | 34,485 | `9ca30ce95f05911d` | { |
| `workflows/verify-da8a8b84.md` | 43,860 | `1a6b080f399a9e06` | \| Workflow \| Job \| Step \| Name \| rc \| Log or reason \| |
