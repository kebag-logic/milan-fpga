# Receipts index

Generated from the files present in this directory (after sanitizing host paths to `<scratch>`,
`<lane>`, `<tools>`, `<management>`, `<home>`). sha256 is truncated to 16 hex digits.

| File | Bytes | sha256 | First line |
|---|---:|---|---|
| `boot/README.md` | 964 | `880a493581541e5e` | The split boot simulation, the platform ledger and the memory test at 1a1e6665, on a clean clone. |
| `boot/boot-1x1-1a1e6665.log` | 10,504 | `dc7a0b70d4e4eef5` | head 1a1e6665fcfd57943f2721cd3bd024eb16b0aa84 dirty 0 |
| `boot/boot-8x8-1a1e6665.log` | 10,458 | `7d1814a575e8624f` | head 1a1e6665fcfd57943f2721cd3bd024eb16b0aa84 dirty 0 |
| `boot/boot-self-test-1a1e6665.log` | 54,300 | `630cb4cb76709614` | head 1a1e6665fcfd57943f2721cd3bd024eb16b0aa84 dirty 0 |
| `boot/plat-ledger-self-test-1a1e6665.log` | 14,894 | `c91317eb4a6b5680` | head 1a1e6665fcfd57943f2721cd3bd024eb16b0aa84 dirty 0 |
| `boot/test-ctrl-memory-1a1e6665.log` | 52,394 | `4a0843444d903b5b` | test_ctrl_memory: the split placement's firmware memory (#640 M8a) |
| `budget/README.md` | 1,075 | `cb4deaaa93e716ce` | The CPU budget's PHY figures at 1a1e6665, 1x1/1if and 8x8/1if. |
| `budget/harness-image-identity-1a1e6665.txt` | 493 | `0741cab639820deb` | tree 1a1e6665fcfd57943f2721cd3bd024eb16b0aa84 porcelain 0 |
| `head/files-changed.txt` | 3,195 | `33bde2e3f6f0fc5f` | Rounds 3 and 4: the commits and files, afa3ea19 (round 2's head) -> 1a1e6665, round 4's own da8a8b84 -> 1a1e66 |
| `measure/README.md` | 1,125 | `ff106ee32c117792` | The measurements behind 1a1e6665's restated figures, on clean clones of the code heads. |
| `measure/boot-1x1-8beada76.log` | 10,504 | `5764bc012044fd83` | head 8beada7683ab081c029317835893296f9ee547ef dirty 0 |
| `measure/boot-8x8-8beada76.log` | 10,458 | `f8c58dcd9175a214` | head 8beada7683ab081c029317835893296f9ee547ef dirty 0 |
| `measure/fw-coverage-check-33041d64.log` | 5,435 | `d8f97a922b0abb62` | toolchain: {'cc': 'gcc (GCC) 16.2.1 20260810', 'cxx': 'g++ (GCC) 16.2.1 20260810', 'gcov': 'gcov (GCC) 16.2.1  |
| `measure/fw-coverage-check-8beada76-refused.log` | 5,532 | `aac5d796e2c7ce45` | toolchain: {'cc': 'gcc (GCC) 16.2.1 20260810', 'cxx': 'g++ (GCC) 16.2.1 20260810', 'gcov': 'gcov (GCC) 16.2.1  |
| `measure/phy-plant-subset-33041d64-tree.log` | 16,604 | `486747e5ae01965b` | 54 mutants |
| `measure/plat-ledger-self-test-8beada76.log` | 14,894 | `1e142478b0e2e7c6` | head 8beada7683ab081c029317835893296f9ee547ef dirty 0 |
| `measure/rom-banking.txt` | 1,575 | `b53fc81222a277d2` | The platform image at each point as plat_ledger.py --self-test plans it (each point's JSON record): rom and sr |
| `measure/rom-per-file.txt` | 2,020 | `876308eeae8ab978` | rom bytes per object, base 70f4056f (dev-soft-core) -> 8beada76, and round 4's own share, da8a8b84 -> 8beada76 |
| `probes/README.md` | 947 | `39e6cd1a614fac61` | Both reviews' own probes, at 1a1e6665 on a clean clone, from copies of the reviewers' scripts under this round |
| `probes/r851-mutants-1a1e6665.txt` | 3,091 | `0a64d7bc09328a09` | R851-1's mutants.sh and an executor's copy with renamed anchors, at 1a1e6665 (round 4) |
| `probes/r851-retry-probe-1a1e6665.log` | 2,222 | `59a35bc165dcf730` | --- <scratch>/c-r4f/sw/firmware/ctrl/test/phy_peer.hpp	2026-11-17 01:03:54.989474409 +0100 |
| `probes/r852-retry-control-1a1e6665.log` | 4,721 | `6f08a6ef2e8324a5` | [==========] Running 37 tests from 3 test suites. |
| `probes/r852-retry-probe-1a1e6665.log` | 4,721 | `14db8bc5249c9a76` | [==========] Running 37 tests from 3 test suites. |
| `workflows/README.md` | 1,992 | `c30d283249696522` | Workflow jobs at 1a1e6665, step by step, each job on its own fresh clean clone of the head (run_wf.py, as in r |
| `workflows/batch-a.log` | 3,494 | `2f825e5e03ad97c1` | 01:04:09 start docs.yml wire-accountability |
| `workflows/batch-b.log` | 1,194 | `4c5aea1deb0e7959` | 01:04:09 start rtl-fast.yml changes |
| `workflows/batch-c.log` | 337 | `c01fad003df37c57` | 01:04:09 start rtl-fast.yml firmware-control-mutants |
| `workflows/batch-d.log` | 342 | `25086f595b3d847f` | 01:04:10 start elaborate.yml elaborate-gates-0 |
| `workflows/batch-e.log` | 553 | `63d2fc85ba53d63c` | 01:05:57 start elaborate.yml elaborate-gates-1 |
| `workflows/large-logs.sha256` | 393 | `3db8f06c3e793a2e` | Workflow step logs over 200 KB, kept in scratch and recorded here by size and sha256 (the log as written, befo |
| `workflows/logs/docs__docs-check-no-git__ci_step_1.log` | 252 | `192d0afbbf0933e9` | # head 1a1e6665fcfd57943f2721cd3bd024eb16b0aa84 workflow docs.yml job docs-check-no-git step ci_step_1: Retain |
| `workflows/logs/docs__docs-check-no-git__ci_step_1.rc` | 2 | `9a271f2a916b0b6e` | 0 |
| `workflows/logs/docs__docs-check-no-git__ci_step_2.log` | 230 | `18b386cd26d03565` | # head 1a1e6665fcfd57943f2721cd3bd024eb16b0aa84 workflow docs.yml job docs-check-no-git step ci_step_2: Set CP |
| `workflows/logs/docs__docs-check-no-git__ci_step_2.rc` | 2 | `9a271f2a916b0b6e` | 0 |
| `workflows/logs/docs__docs-check-no-git__ci_step_3.log` | 470 | `adbcd958fc29ba2d` | # head 1a1e6665fcfd57943f2721cd3bd024eb16b0aa84 workflow docs.yml job docs-check-no-git step ci_step_3: Strip  |
| `workflows/logs/docs__docs-check-no-git__ci_step_3.rc` | 2 | `9a271f2a916b0b6e` | 0 |
| `workflows/logs/docs__docs-check__DONE` | 9 | `fab506c9d858683b` | failed 0 |
| `workflows/logs/docs__docs-check__tree-after.txt` | 55 | `2d7cbc9d1a022490` | head 1a1e6665fcfd57943f2721cd3bd024eb16b0aa84 |
| `workflows/logs/docs__docs-gates-0__DONE` | 9 | `fab506c9d858683b` | failed 0 |
| `workflows/logs/docs__docs-gates-0__ci_step_1.log` | 370 | `fbdf6613f4378638` | # head 1a1e6665fcfd57943f2721cd3bd024eb16b0aa84 workflow docs.yml job docs-gates-0 step ci_step_1: Set CPU-der |
| `workflows/logs/docs__docs-gates-0__ci_step_1.rc` | 2 | `9a271f2a916b0b6e` | 0 |
| `workflows/logs/docs__docs-gates-0__ci_step_21.log` | 934 | `1926f06c0ff8a6de` | # head 1a1e6665fcfd57943f2721cd3bd024eb16b0aa84 workflow docs.yml job docs-gates-0 step ci_step_21: Fetch the  |
| `workflows/logs/docs__docs-gates-0__ci_step_21.rc` | 2 | `9a271f2a916b0b6e` | 0 |
| `workflows/logs/docs__docs-gates-0__ci_step_5.log` | 490 | `4ee014447c889e03` | # head 1a1e6665fcfd57943f2721cd3bd024eb16b0aa84 workflow docs.yml job docs-gates-0 step ci_step_5: Install the |
| `workflows/logs/docs__docs-gates-0__ci_step_5.rc` | 2 | `9a271f2a916b0b6e` | 0 |
| `workflows/logs/docs__docs-gates-0__ci_step_52.log` | 565 | `d3ddd4c6f994e658` | # head 1a1e6665fcfd57943f2721cd3bd024eb16b0aa84 workflow docs.yml job docs-gates-0 step ci_step_52: Fetch inve |
| `workflows/logs/docs__docs-gates-0__ci_step_52.rc` | 2 | `9a271f2a916b0b6e` | 0 |
| `workflows/logs/docs__docs-gates-0__ci_step_7.log` | 490 | `a7fca693742a598c` | # head 1a1e6665fcfd57943f2721cd3bd024eb16b0aa84 workflow docs.yml job docs-gates-0 step ci_step_7: Install the |
| `workflows/logs/docs__docs-gates-0__ci_step_7.rc` | 2 | `9a271f2a916b0b6e` | 0 |
| `workflows/logs/docs__docs-gates-0__gate_1.log` | 1,349 | `768e494fa869efaa` | # head 1a1e6665fcfd57943f2721cd3bd024eb16b0aa84 workflow docs.yml job docs-gates-0 step gate_1: Build the vali |
| `workflows/logs/docs__docs-gates-0__gate_1.rc` | 2 | `9a271f2a916b0b6e` | 0 |
| `workflows/logs/docs__docs-gates-0__gate_10.log` | 613 | `e8812ed8cb77d3dc` | # head 1a1e6665fcfd57943f2721cd3bd024eb16b0aa84 workflow docs.yml job docs-gates-0 step gate_10: Audience diag |
| `workflows/logs/docs__docs-gates-0__gate_10.rc` | 2 | `9a271f2a916b0b6e` | 0 |
| `workflows/logs/docs__docs-gates-0__gate_11.log` | 520 | `297c8eba7df18d95` | # head 1a1e6665fcfd57943f2721cd3bd024eb16b0aa84 workflow docs.yml job docs-gates-0 step gate_11: Product solut |
| `workflows/logs/docs__docs-gates-0__gate_11.rc` | 2 | `9a271f2a916b0b6e` | 0 |
| `workflows/logs/docs__docs-gates-0__gate_12.log` | 605 | `d49ab209be5c43f3` | # head 1a1e6665fcfd57943f2721cd3bd024eb16b0aa84 workflow docs.yml job docs-gates-0 step gate_12: Verified subm |
| `workflows/logs/docs__docs-gates-0__gate_12.rc` | 2 | `9a271f2a916b0b6e` | 0 |
| `workflows/logs/docs__docs-gates-0__gate_13.log` | 614 | `33a071608a3acb4d` | # head 1a1e6665fcfd57943f2721cd3bd024eb16b0aa84 workflow docs.yml job docs-gates-0 step gate_13: HDL timing di |
| `workflows/logs/docs__docs-gates-0__gate_13.rc` | 2 | `9a271f2a916b0b6e` | 0 |
| `workflows/logs/docs__docs-gates-0__gate_14.log` | 492 | `a098290e7336f853` | # head 1a1e6665fcfd57943f2721cd3bd024eb16b0aa84 workflow docs.yml job docs-gates-0 step gate_14: Published dia |
| `workflows/logs/docs__docs-gates-0__gate_14.rc` | 2 | `9a271f2a916b0b6e` | 0 |
| `workflows/logs/docs__docs-gates-0__gate_15.log` | 1,878 | `cffec42bbf442422` | # head 1a1e6665fcfd57943f2721cd3bd024eb16b0aa84 workflow docs.yml job docs-gates-0 step gate_15: Milan feature |
| `workflows/logs/docs__docs-gates-0__gate_15.rc` | 2 | `9a271f2a916b0b6e` | 0 |
| `workflows/logs/docs__docs-gates-0__gate_16.log` | 492 | `4c7585a330590050` | # head 1a1e6665fcfd57943f2721cd3bd024eb16b0aa84 workflow docs.yml job docs-gates-0 step gate_16: Traceability  |
| `workflows/logs/docs__docs-gates-0__gate_16.rc` | 2 | `9a271f2a916b0b6e` | 0 |
| `workflows/logs/docs__docs-gates-0__gate_18.log` | 2,984 | `0497c683b640a9ab` | # head 1a1e6665fcfd57943f2721cd3bd024eb16b0aa84 workflow docs.yml job docs-gates-0 step gate_18: Imported gPTP |
| `workflows/logs/docs__docs-gates-0__gate_18.rc` | 2 | `9a271f2a916b0b6e` | 0 |
| `workflows/logs/docs__docs-gates-0__gate_19.log` | 3,669 | `1f6b62e38e000f59` | # head 1a1e6665fcfd57943f2721cd3bd024eb16b0aa84 workflow docs.yml job docs-gates-0 step gate_19: Code-quality  |
| `workflows/logs/docs__docs-gates-0__gate_19.rc` | 2 | `9a271f2a916b0b6e` | 0 |
| `workflows/logs/docs__docs-gates-0__gate_21.log` | 477 | `4e1809b07c065a51` | # head 1a1e6665fcfd57943f2721cd3bd024eb16b0aa84 workflow docs.yml job docs-gates-0 step gate_21: Bare-metal sc |
| `workflows/logs/docs__docs-gates-0__gate_21.rc` | 2 | `9a271f2a916b0b6e` | 0 |
| `workflows/logs/docs__docs-gates-0__gate_24.log` | 51,854 | `3e26c26b38849228` | # head 1a1e6665fcfd57943f2721cd3bd024eb16b0aa84 workflow docs.yml job docs-gates-0 step gate_24: Compiler-abse |
| `workflows/logs/docs__docs-gates-0__gate_24.rc` | 2 | `9a271f2a916b0b6e` | 0 |
| `workflows/logs/docs__docs-gates-0__gate_26.log` | 12,668 | `e81e08d8772460bc` | # head 1a1e6665fcfd57943f2721cd3bd024eb16b0aa84 workflow docs.yml job docs-gates-0 step gate_26: NVM record-sp |
| `workflows/logs/docs__docs-gates-0__gate_26.rc` | 2 | `9a271f2a916b0b6e` | 0 |
| `workflows/logs/docs__docs-gates-0__gate_27.log` | 780 | `7a6d537cadcb8b35` | # head 1a1e6665fcfd57943f2721cd3bd024eb16b0aa84 workflow docs.yml job docs-gates-0 step gate_27: Capture measu |
| `workflows/logs/docs__docs-gates-0__gate_27.rc` | 2 | `9a271f2a916b0b6e` | 0 |
| `workflows/logs/docs__docs-gates-0__gate_28.log` | 26,514 | `1e54232e20a3082e` | # head 1a1e6665fcfd57943f2721cd3bd024eb16b0aa84 workflow docs.yml job docs-gates-0 step gate_28: Saved-state w |
| `workflows/logs/docs__docs-gates-0__gate_28.rc` | 2 | `9a271f2a916b0b6e` | 0 |
| `workflows/logs/docs__docs-gates-0__gate_29.log` | 5,198 | `11f8e763712c3d9a` | # head 1a1e6665fcfd57943f2721cd3bd024eb16b0aa84 workflow docs.yml job docs-gates-0 step gate_29: SoC source-li |
| `workflows/logs/docs__docs-gates-0__gate_29.rc` | 2 | `9a271f2a916b0b6e` | 0 |
| `workflows/logs/docs__docs-gates-0__gate_30.log` | 3,820 | `c7031ba26cd1470f` | # head 1a1e6665fcfd57943f2721cd3bd024eb16b0aa84 workflow docs.yml job docs-gates-0 step gate_30: RTL source-li |
| `workflows/logs/docs__docs-gates-0__gate_30.rc` | 2 | `9a271f2a916b0b6e` | 0 |
| `workflows/logs/docs__docs-gates-0__gate_31.log` | 40,968 | `8d542cb265885b5f` | # head 1a1e6665fcfd57943f2721cd3bd024eb16b0aa84 workflow docs.yml job docs-gates-0 step gate_31: Boundary-unit |
| `workflows/logs/docs__docs-gates-0__gate_31.rc` | 2 | `9a271f2a916b0b6e` | 0 |
| `workflows/logs/docs__docs-gates-0__gate_32.log` | 5,399 | `b7f03e792d861401` | # head 1a1e6665fcfd57943f2721cd3bd024eb16b0aa84 workflow docs.yml job docs-gates-0 step gate_32: Port contract |
| `workflows/logs/docs__docs-gates-0__gate_32.rc` | 2 | `9a271f2a916b0b6e` | 0 |
| `workflows/logs/docs__docs-gates-0__gate_33.log` | 12,944 | `06fd8ff7dd88b2e2` | # head 1a1e6665fcfd57943f2721cd3bd024eb16b0aa84 workflow docs.yml job docs-gates-0 step gate_33: Fail-fast rat |
| `workflows/logs/docs__docs-gates-0__gate_33.rc` | 2 | `9a271f2a916b0b6e` | 0 |
| `workflows/logs/docs__docs-gates-0__gate_34.log` | 3,105 | `530bda3433eb724b` | # head 1a1e6665fcfd57943f2721cd3bd024eb16b0aa84 workflow docs.yml job docs-gates-0 step gate_34: TODO ownershi |
| `workflows/logs/docs__docs-gates-0__gate_34.rc` | 2 | `9a271f2a916b0b6e` | 0 |
| `workflows/logs/docs__docs-gates-0__gate_35.log` | 29,146 | `4f72d0fa8048c8a0` | # head 1a1e6665fcfd57943f2721cd3bd024eb16b0aa84 workflow docs.yml job docs-gates-0 step gate_35: Test-evidence |
| `workflows/logs/docs__docs-gates-0__gate_35.rc` | 2 | `9a271f2a916b0b6e` | 0 |
| `workflows/logs/docs__docs-gates-0__gate_36.log` | 4,339 | `ec0f2aeda1683374` | # head 1a1e6665fcfd57943f2721cd3bd024eb16b0aa84 workflow docs.yml job docs-gates-0 step gate_36: Mechanical hy |
| `workflows/logs/docs__docs-gates-0__gate_36.rc` | 2 | `9a271f2a916b0b6e` | 0 |
| `workflows/logs/docs__docs-gates-0__gate_37.log` | 3,538 | `5526105884edd511` | # head 1a1e6665fcfd57943f2721cd3bd024eb16b0aa84 workflow docs.yml job docs-gates-0 step gate_37: SystemVerilog |
| `workflows/logs/docs__docs-gates-0__gate_37.rc` | 2 | `9a271f2a916b0b6e` | 0 |
| `workflows/logs/docs__docs-gates-0__gate_38.log` | 4,270 | `5e019aed350ff531` | # head 1a1e6665fcfd57943f2721cd3bd024eb16b0aa84 workflow docs.yml job docs-gates-0 step gate_38: C and C++ idi |
| `workflows/logs/docs__docs-gates-0__gate_38.rc` | 2 | `9a271f2a916b0b6e` | 0 |
| `workflows/logs/docs__docs-gates-0__gate_39.log` | 3,350 | `b6e6753c5fba1eae` | # head 1a1e6665fcfd57943f2721cd3bd024eb16b0aa84 workflow docs.yml job docs-gates-0 step gate_39: Python idiom  |
| `workflows/logs/docs__docs-gates-0__gate_39.rc` | 2 | `9a271f2a916b0b6e` | 0 |
| `workflows/logs/docs__docs-gates-0__gate_40.log` | 3,053 | `a8359d922b58f0e6` | # head 1a1e6665fcfd57943f2721cd3bd024eb16b0aa84 workflow docs.yml job docs-gates-0 step gate_40: Shell idiom g |
| `workflows/logs/docs__docs-gates-0__gate_40.rc` | 2 | `9a271f2a916b0b6e` | 0 |
| `workflows/logs/docs__docs-gates-0__gate_43.log` | 461 | `419c5ad3254a6c83` | # head 1a1e6665fcfd57943f2721cd3bd024eb16b0aa84 workflow docs.yml job docs-gates-0 step gate_43: Doc cited-pat |
| `workflows/logs/docs__docs-gates-0__gate_43.rc` | 2 | `9a271f2a916b0b6e` | 0 |
| `workflows/logs/docs__docs-gates-0__gate_44.log` | 491 | `c180da22b4d237f3` | # head 1a1e6665fcfd57943f2721cd3bd024eb16b0aa84 workflow docs.yml job docs-gates-0 step gate_44: Archive integ |
| `workflows/logs/docs__docs-gates-0__gate_44.rc` | 2 | `9a271f2a916b0b6e` | 0 |
| `workflows/logs/docs__docs-gates-0__gate_45.log` | 559 | `d80618e487e9328e` | # head 1a1e6665fcfd57943f2721cd3bd024eb16b0aa84 workflow docs.yml job docs-gates-0 step gate_45: Per-page cont |
| `workflows/logs/docs__docs-gates-0__gate_45.rc` | 2 | `9a271f2a916b0b6e` | 0 |
| `workflows/logs/docs__docs-gates-0__gate_46.log` | 3,966 | `92e36b50f3a533ce` | # head 1a1e6665fcfd57943f2721cd3bd024eb16b0aa84 workflow docs.yml job docs-gates-0 step gate_46: AEM store gen |
| `workflows/logs/docs__docs-gates-0__gate_46.rc` | 2 | `9a271f2a916b0b6e` | 0 |
| `workflows/logs/docs__docs-gates-0__gate_47.log` | 20,117 | `a51643f168e4b1bd` | # head 1a1e6665fcfd57943f2721cd3bd024eb16b0aa84 workflow docs.yml job docs-gates-0 step gate_47: Sweep/build s |
| `workflows/logs/docs__docs-gates-0__gate_47.rc` | 2 | `9a271f2a916b0b6e` | 0 |
| `workflows/logs/docs__docs-gates-0__gate_48.log` | 9,664 | `067393c56a6c54e7` | # head 1a1e6665fcfd57943f2721cd3bd024eb16b0aa84 workflow docs.yml job docs-gates-0 step gate_48: Deploy shape  |
| `workflows/logs/docs__docs-gates-0__gate_48.rc` | 2 | `9a271f2a916b0b6e` | 0 |
| `workflows/logs/docs__docs-gates-0__gate_49.log` | 28,098 | `c28394fdb253e47c` | # head 1a1e6665fcfd57943f2721cd3bd024eb16b0aa84 workflow docs.yml job docs-gates-0 step gate_49: Entity shape  |
| `workflows/logs/docs__docs-gates-0__gate_49.rc` | 2 | `9a271f2a916b0b6e` | 0 |
| `workflows/logs/docs__docs-gates-0__gate_50.log` | 135,971 | `4fc972f951087428` | # head 1a1e6665fcfd57943f2721cd3bd024eb16b0aa84 workflow docs.yml job docs-gates-0 step gate_50: CI scheduling |
| `workflows/logs/docs__docs-gates-0__gate_50.rc` | 2 | `9a271f2a916b0b6e` | 0 |
| `workflows/logs/docs__docs-gates-0__gate_7.log` | 524 | `6038dc0d87b95328` | # head 1a1e6665fcfd57943f2721cd3bd024eb16b0aa84 workflow docs.yml job docs-gates-0 step gate_7: Link health, w |
| `workflows/logs/docs__docs-gates-0__gate_7.rc` | 2 | `9a271f2a916b0b6e` | 0 |
| `workflows/logs/docs__docs-gates-0__gate_8.log` | 502 | `7a5df19f61891dfd` | # head 1a1e6665fcfd57943f2721cd3bd024eb16b0aa84 workflow docs.yml job docs-gates-0 step gate_8: Added-line em- |
| `workflows/logs/docs__docs-gates-0__gate_8.rc` | 2 | `9a271f2a916b0b6e` | 0 |
| `workflows/logs/docs__docs-gates-0__gate_9.log` | 542 | `f9f5b9d2bcef585c` | # head 1a1e6665fcfd57943f2721cd3bd024eb16b0aa84 workflow docs.yml job docs-gates-0 step gate_9: Concise audien |
| `workflows/logs/docs__docs-gates-0__gate_9.rc` | 2 | `9a271f2a916b0b6e` | 0 |
| `workflows/logs/docs__docs-gates-0__tree-after.txt` | 55 | `2d7cbc9d1a022490` | head 1a1e6665fcfd57943f2721cd3bd024eb16b0aa84 |
| `workflows/logs/docs__docs-gates-1__DONE` | 9 | `fab506c9d858683b` | failed 0 |
| `workflows/logs/docs__docs-gates-1__ci_step_1.log` | 370 | `7f7e8d72b66a9302` | # head 1a1e6665fcfd57943f2721cd3bd024eb16b0aa84 workflow docs.yml job docs-gates-1 step ci_step_1: Set CPU-der |
| `workflows/logs/docs__docs-gates-1__ci_step_1.rc` | 2 | `9a271f2a916b0b6e` | 0 |
| `workflows/logs/docs__docs-gates-1__ci_step_3.log` | 490 | `c0bd2c512dc18add` | # head 1a1e6665fcfd57943f2721cd3bd024eb16b0aa84 workflow docs.yml job docs-gates-1 step ci_step_3: Install the |
| `workflows/logs/docs__docs-gates-1__ci_step_3.rc` | 2 | `9a271f2a916b0b6e` | 0 |
| `workflows/logs/docs__docs-gates-1__ci_step_5.log` | 490 | `c844ac59d4d48beb` | # head 1a1e6665fcfd57943f2721cd3bd024eb16b0aa84 workflow docs.yml job docs-gates-1 step ci_step_5: Install the |
| `workflows/logs/docs__docs-gates-1__ci_step_5.rc` | 2 | `9a271f2a916b0b6e` | 0 |
| `workflows/logs/docs__docs-gates-1__ci_step_9.log` | 933 | `2b351a089e2bd908` | # head 1a1e6665fcfd57943f2721cd3bd024eb16b0aa84 workflow docs.yml job docs-gates-1 step ci_step_9: Fetch the b |
| `workflows/logs/docs__docs-gates-1__ci_step_9.rc` | 2 | `9a271f2a916b0b6e` | 0 |
| `workflows/logs/docs__docs-gates-1__gate_25_0.log` | 50,908 | `d7c334b631506c9b` | # head 1a1e6665fcfd57943f2721cd3bd024eb16b0aa84 workflow docs.yml job docs-gates-1 step gate_25_0: End-station |
| `workflows/logs/docs__docs-gates-1__gate_25_0.rc` | 2 | `9a271f2a916b0b6e` | 0 |
| `workflows/logs/docs__docs-gates-1__tree-after.txt` | 55 | `2d7cbc9d1a022490` | head 1a1e6665fcfd57943f2721cd3bd024eb16b0aa84 |
| `workflows/logs/docs__docs-gates-2__DONE` | 9 | `fab506c9d858683b` | failed 0 |
| `workflows/logs/docs__docs-gates-2__ci_step_1.log` | 370 | `d31aff178c7110fd` | # head 1a1e6665fcfd57943f2721cd3bd024eb16b0aa84 workflow docs.yml job docs-gates-2 step ci_step_1: Set CPU-der |
| `workflows/logs/docs__docs-gates-2__ci_step_1.rc` | 2 | `9a271f2a916b0b6e` | 0 |
| `workflows/logs/docs__docs-gates-2__ci_step_3.log` | 490 | `aa0a793d231b2862` | # head 1a1e6665fcfd57943f2721cd3bd024eb16b0aa84 workflow docs.yml job docs-gates-2 step ci_step_3: Install the |
| `workflows/logs/docs__docs-gates-2__ci_step_3.rc` | 2 | `9a271f2a916b0b6e` | 0 |
| `workflows/logs/docs__docs-gates-2__ci_step_5.log` | 490 | `c8213a185f52f423` | # head 1a1e6665fcfd57943f2721cd3bd024eb16b0aa84 workflow docs.yml job docs-gates-2 step ci_step_5: Install the |
| `workflows/logs/docs__docs-gates-2__ci_step_5.rc` | 2 | `9a271f2a916b0b6e` | 0 |
| `workflows/logs/docs__docs-gates-2__ci_step_9.log` | 933 | `3a62e81e626f811a` | # head 1a1e6665fcfd57943f2721cd3bd024eb16b0aa84 workflow docs.yml job docs-gates-2 step ci_step_9: Fetch the b |
| `workflows/logs/docs__docs-gates-2__ci_step_9.rc` | 2 | `9a271f2a916b0b6e` | 0 |
| `workflows/logs/docs__docs-gates-2__gate_25_1.log` | 76,632 | `b588cf4876d365a2` | # head 1a1e6665fcfd57943f2721cd3bd024eb16b0aa84 workflow docs.yml job docs-gates-2 step gate_25_1: End-station |
| `workflows/logs/docs__docs-gates-2__gate_25_1.rc` | 2 | `9a271f2a916b0b6e` | 0 |
| `workflows/logs/docs__docs-gates-2__gate_41.rc` | 2 | `9a271f2a916b0b6e` | 0 |
| `workflows/logs/docs__docs-gates-2__gate_42.log` | 123,978 | `4153969a4619b62c` | # head 1a1e6665fcfd57943f2721cd3bd024eb16b0aa84 workflow docs.yml job docs-gates-2 step gate_42: Local act run |
| `workflows/logs/docs__docs-gates-2__gate_42.rc` | 2 | `9a271f2a916b0b6e` | 0 |
| `workflows/logs/docs__docs-gates-2__tree-after.txt` | 55 | `2d7cbc9d1a022490` | head 1a1e6665fcfd57943f2721cd3bd024eb16b0aa84 |
| `workflows/logs/docs__wire-accountability__DONE` | 9 | `fab506c9d858683b` | failed 0 |
| `workflows/logs/docs__wire-accountability__ci_step_1.log` | 384 | `64747cc9573db7a3` | # head 1a1e6665fcfd57943f2721cd3bd024eb16b0aa84 workflow docs.yml job wire-accountability step ci_step_1: Set  |
| `workflows/logs/docs__wire-accountability__ci_step_1.rc` | 2 | `9a271f2a916b0b6e` | 0 |
| `workflows/logs/docs__wire-accountability__ci_step_3.log` | 590 | `28ef4b1bf1cb2cf9` | # head 1a1e6665fcfd57943f2721cd3bd024eb16b0aa84 workflow docs.yml job wire-accountability step ci_step_3: Fetc |
| `workflows/logs/docs__wire-accountability__ci_step_3.rc` | 2 | `9a271f2a916b0b6e` | 0 |
| `workflows/logs/docs__wire-accountability__ci_step_4.log` | 5,493 | `ce407ad183fe598e` | # head 1a1e6665fcfd57943f2721cd3bd024eb16b0aa84 workflow docs.yml job wire-accountability step ci_step_4: Adve |
| `workflows/logs/docs__wire-accountability__ci_step_4.rc` | 2 | `9a271f2a916b0b6e` | 0 |
| `workflows/logs/docs__wire-accountability__tree-after.txt` | 55 | `2d7cbc9d1a022490` | head 1a1e6665fcfd57943f2721cd3bd024eb16b0aa84 |
| `workflows/logs/elaborate__elaborate-gates-0__DONE` | 9 | `fab506c9d858683b` | failed 0 |
| `workflows/logs/elaborate__elaborate-gates-0__ci_step_1.log` | 383 | `fa33a8dcc498cfe2` | # head 1a1e6665fcfd57943f2721cd3bd024eb16b0aa84 workflow elaborate.yml job elaborate-gates-0 step ci_step_1: S |
| `workflows/logs/elaborate__elaborate-gates-0__ci_step_1.rc` | 2 | `9a271f2a916b0b6e` | 0 |
| `workflows/logs/elaborate__elaborate-gates-0__ci_step_4.log` | 990 | `a1ff2b6f40b8d5d4` | # head 1a1e6665fcfd57943f2721cd3bd024eb16b0aa84 workflow elaborate.yml job elaborate-gates-0 step ci_step_4: F |
| `workflows/logs/elaborate__elaborate-gates-0__ci_step_4.rc` | 2 | `9a271f2a916b0b6e` | 0 |
| `workflows/logs/elaborate__elaborate-gates-0__gate_15_0.log` | 51,029 | `2ad04f4c2e391040` | # head 1a1e6665fcfd57943f2721cd3bd024eb16b0aa84 workflow elaborate.yml job elaborate-gates-0 step gate_15_0: E |
| `workflows/logs/elaborate__elaborate-gates-0__gate_15_0.rc` | 2 | `9a271f2a916b0b6e` | 0 |
| `workflows/logs/elaborate__elaborate-gates-0__scope.log` | 18,280 | `c992a921143ebeee` | # head 1a1e6665fcfd57943f2721cd3bd024eb16b0aa84 workflow elaborate.yml job elaborate-gates-0 step scope: Decid |
| `workflows/logs/elaborate__elaborate-gates-0__scope.rc` | 2 | `9a271f2a916b0b6e` | 0 |
| `workflows/logs/elaborate__elaborate-gates-0__tree-after.txt` | 55 | `2d7cbc9d1a022490` | head 1a1e6665fcfd57943f2721cd3bd024eb16b0aa84 |
| `workflows/logs/elaborate__elaborate-gates-1__DONE` | 9 | `fab506c9d858683b` | failed 0 |
| `workflows/logs/elaborate__elaborate-gates-1__ci_step_1.log` | 383 | `bb2a7d230ab4230c` | # head 1a1e6665fcfd57943f2721cd3bd024eb16b0aa84 workflow elaborate.yml job elaborate-gates-1 step ci_step_1: S |
| `workflows/logs/elaborate__elaborate-gates-1__ci_step_1.rc` | 2 | `9a271f2a916b0b6e` | 0 |
| `workflows/logs/elaborate__elaborate-gates-1__ci_step_23.log` | 547 | `4f74dac732cfec4a` | # head 1a1e6665fcfd57943f2721cd3bd024eb16b0aa84 workflow elaborate.yml job elaborate-gates-1 step ci_step_23:  |
| `workflows/logs/elaborate__elaborate-gates-1__ci_step_23.rc` | 2 | `9a271f2a916b0b6e` | 0 |
| `workflows/logs/elaborate__elaborate-gates-1__ci_step_4.log` | 990 | `4296fd2692ba4ede` | # head 1a1e6665fcfd57943f2721cd3bd024eb16b0aa84 workflow elaborate.yml job elaborate-gates-1 step ci_step_4: F |
| `workflows/logs/elaborate__elaborate-gates-1__ci_step_4.rc` | 2 | `9a271f2a916b0b6e` | 0 |
| `workflows/logs/elaborate__elaborate-gates-1__gate_15_1.log` | 83,075 | `6f6ddc1e04a713be` | # head 1a1e6665fcfd57943f2721cd3bd024eb16b0aa84 workflow elaborate.yml job elaborate-gates-1 step gate_15_1: E |
| `workflows/logs/elaborate__elaborate-gates-1__gate_15_1.rc` | 2 | `9a271f2a916b0b6e` | 0 |
| `workflows/logs/elaborate__elaborate-gates-1__gate_19.log` | 1,602 | `c27f493548e679a4` | # head 1a1e6665fcfd57943f2721cd3bd024eb16b0aa84 workflow elaborate.yml job elaborate-gates-1 step gate_19: Sta |
| `workflows/logs/elaborate__elaborate-gates-1__gate_19.rc` | 2 | `9a271f2a916b0b6e` | 0 |
| `workflows/logs/elaborate__elaborate-gates-1__scope.log` | 18,280 | `367a65e63beca297` | # head 1a1e6665fcfd57943f2721cd3bd024eb16b0aa84 workflow elaborate.yml job elaborate-gates-1 step scope: Decid |
| `workflows/logs/elaborate__elaborate-gates-1__scope.rc` | 2 | `9a271f2a916b0b6e` | 0 |
| `workflows/logs/elaborate__elaborate-gates-1__tree-after.txt` | 55 | `2d7cbc9d1a022490` | head 1a1e6665fcfd57943f2721cd3bd024eb16b0aa84 |
| `workflows/logs/elaborate__elaborate__DONE` | 9 | `fab506c9d858683b` | failed 0 |
| `workflows/logs/elaborate__elaborate__tree-after.txt` | 55 | `2d7cbc9d1a022490` | head 1a1e6665fcfd57943f2721cd3bd024eb16b0aa84 |
| `workflows/logs/rtl-fast__changes__DONE` | 9 | `fab506c9d858683b` | failed 0 |
| `workflows/logs/rtl-fast__changes__ci_step_1.log` | 218 | `f6be698bc80863c8` | # head 1a1e6665fcfd57943f2721cd3bd024eb16b0aa84 workflow rtl-fast.yml job changes step ci_step_1: Set CPU-deri |
| `workflows/logs/rtl-fast__changes__ci_step_1.rc` | 2 | `9a271f2a916b0b6e` | 0 |
| `workflows/logs/rtl-fast__changes__scope.log` | 18,322 | `8b9bb98af3cd3f62` | # head 1a1e6665fcfd57943f2721cd3bd024eb16b0aa84 workflow rtl-fast.yml job changes step scope: Classify the cha |
| `workflows/logs/rtl-fast__changes__scope.rc` | 2 | `9a271f2a916b0b6e` | 0 |
| `workflows/logs/rtl-fast__changes__tree-after.txt` | 55 | `2d7cbc9d1a022490` | head 1a1e6665fcfd57943f2721cd3bd024eb16b0aa84 |
| `workflows/logs/rtl-fast__firmware-boundary__DONE` | 9 | `fab506c9d858683b` | failed 0 |
| `workflows/logs/rtl-fast__firmware-boundary__ci_step_1.log` | 381 | `6e6b9e0ddf66d496` | # head 1a1e6665fcfd57943f2721cd3bd024eb16b0aa84 workflow rtl-fast.yml job firmware-boundary step ci_step_1: Se |
| `workflows/logs/rtl-fast__firmware-boundary__ci_step_1.rc` | 2 | `9a271f2a916b0b6e` | 0 |
| `workflows/logs/rtl-fast__firmware-boundary__ci_step_3.log` | 1,348 | `2614b706f43f7029` | # head 1a1e6665fcfd57943f2721cd3bd024eb16b0aa84 workflow rtl-fast.yml job firmware-boundary step ci_step_3: Fe |
| `workflows/logs/rtl-fast__firmware-boundary__ci_step_3.rc` | 2 | `9a271f2a916b0b6e` | 0 |
| `workflows/logs/rtl-fast__firmware-boundary__ci_step_9.log` | 70,861 | `89a773491dacc670` | # head 1a1e6665fcfd57943f2721cd3bd024eb16b0aa84 workflow rtl-fast.yml job firmware-boundary step ci_step_9: Ho |
| `workflows/logs/rtl-fast__firmware-boundary__ci_step_9.rc` | 2 | `9a271f2a916b0b6e` | 0 |
| `workflows/logs/rtl-fast__firmware-boundary__tree-after.txt` | 55 | `2d7cbc9d1a022490` | head 1a1e6665fcfd57943f2721cd3bd024eb16b0aa84 |
| `workflows/logs/rtl-fast__firmware-control-mutants__DONE` | 9 | `fab506c9d858683b` | failed 0 |
| `workflows/logs/rtl-fast__firmware-control-mutants__ci_step_1.log` | 402 | `0388a0b9c1594ccb` | # head 1a1e6665fcfd57943f2721cd3bd024eb16b0aa84 workflow rtl-fast.yml job firmware-control-mutants step ci_ste |
| `workflows/logs/rtl-fast__firmware-control-mutants__ci_step_1.rc` | 2 | `9a271f2a916b0b6e` | 0 |
| `workflows/logs/rtl-fast__firmware-control-mutants__ci_step_3.log` | 1,404 | `f09d87fc9b05180f` | # head 1a1e6665fcfd57943f2721cd3bd024eb16b0aa84 workflow rtl-fast.yml job firmware-control-mutants step ci_ste |
| `workflows/logs/rtl-fast__firmware-control-mutants__ci_step_3.rc` | 2 | `9a271f2a916b0b6e` | 0 |
| `workflows/logs/rtl-fast__firmware-control-mutants__ci_step_9.log` | 146,350 | `921bda00799b9073` | # head 1a1e6665fcfd57943f2721cd3bd024eb16b0aa84 workflow rtl-fast.yml job firmware-control-mutants step ci_ste |
| `workflows/logs/rtl-fast__firmware-control-mutants__ci_step_9.rc` | 2 | `9a271f2a916b0b6e` | 0 |
| `workflows/logs/rtl-fast__firmware-control-mutants__tree-after.txt` | 73 | `932b4f96f8ca68f0` | head 1a1e6665fcfd57943f2721cd3bd024eb16b0aa84 |
| `workflows/logs/rtl-fast__firmware-unit__DONE` | 9 | `fab506c9d858683b` | failed 0 |
| `workflows/logs/rtl-fast__firmware-unit__ci_step_1.log` | 380 | `749bdef15f536a27` | # head 1a1e6665fcfd57943f2721cd3bd024eb16b0aa84 workflow rtl-fast.yml job firmware-unit step ci_step_1: Set CP |
| `workflows/logs/rtl-fast__firmware-unit__ci_step_1.rc` | 2 | `9a271f2a916b0b6e` | 0 |
| `workflows/logs/rtl-fast__firmware-unit__ci_step_10.log` | 90,306 | `d7e530b87eaf67b4` | # head 1a1e6665fcfd57943f2721cd3bd024eb16b0aa84 workflow rtl-fast.yml job firmware-unit step ci_step_10: Run t |
| `workflows/logs/rtl-fast__firmware-unit__ci_step_10.rc` | 2 | `9a271f2a916b0b6e` | 0 |
| `workflows/logs/rtl-fast__firmware-unit__ci_step_11.log` | 5,227 | `d024e277103e8702` | # head 1a1e6665fcfd57943f2721cd3bd024eb16b0aa84 workflow rtl-fast.yml job firmware-unit step ci_step_11: Run t |
| `workflows/logs/rtl-fast__firmware-unit__ci_step_11.rc` | 2 | `9a271f2a916b0b6e` | 0 |
| `workflows/logs/rtl-fast__firmware-unit__ci_step_12.log` | 9,622 | `8108b1cc2d99f3e4` | # head 1a1e6665fcfd57943f2721cd3bd024eb16b0aa84 workflow rtl-fast.yml job firmware-unit step ci_step_12: Hold  |
| `workflows/logs/rtl-fast__firmware-unit__ci_step_12.rc` | 2 | `9a271f2a916b0b6e` | 0 |
| `workflows/logs/rtl-fast__firmware-unit__ci_step_3.log` | 1,327 | `d75d1ddcc085fbb9` | # head 1a1e6665fcfd57943f2721cd3bd024eb16b0aa84 workflow rtl-fast.yml job firmware-unit step ci_step_3: Fetch  |
| `workflows/logs/rtl-fast__firmware-unit__ci_step_3.rc` | 2 | `9a271f2a916b0b6e` | 0 |
| `workflows/logs/rtl-fast__firmware-unit__ci_step_7.log` | 2,388 | `9e2a2a18c32a40f7` | # head 1a1e6665fcfd57943f2721cd3bd024eb16b0aa84 workflow rtl-fast.yml job firmware-unit step ci_step_7: Prove  |
| `workflows/logs/rtl-fast__firmware-unit__ci_step_7.rc` | 2 | `9a271f2a916b0b6e` | 0 |
| `workflows/logs/rtl-fast__firmware-unit__tree-after.txt` | 73 | `932b4f96f8ca68f0` | head 1a1e6665fcfd57943f2721cd3bd024eb16b0aa84 |
| `workflows/logs/rtl-fast__firmware-verilator__DONE` | 9 | `fab506c9d858683b` | failed 0 |
| `workflows/logs/rtl-fast__firmware-verilator__ci_step_1.log` | 390 | `d33f4de7b0bc6993` | # head 1a1e6665fcfd57943f2721cd3bd024eb16b0aa84 workflow rtl-fast.yml job firmware-verilator step ci_step_1: S |
| `workflows/logs/rtl-fast__firmware-verilator__ci_step_1.rc` | 2 | `9a271f2a916b0b6e` | 0 |
| `workflows/logs/rtl-fast__firmware-verilator__ci_step_11.log` | 554 | `b0a84ee9f9a94756` | # head 1a1e6665fcfd57943f2721cd3bd024eb16b0aa84 workflow rtl-fast.yml job firmware-verilator step ci_step_11:  |
| `workflows/logs/rtl-fast__firmware-verilator__ci_step_11.rc` | 2 | `9a271f2a916b0b6e` | 0 |
| `workflows/logs/rtl-fast__firmware-verilator__ci_step_14.log` | 60,774 | `b14da285109f5a32` | # head 1a1e6665fcfd57943f2721cd3bd024eb16b0aa84 workflow rtl-fast.yml job firmware-verilator step ci_step_14:  |
| `workflows/logs/rtl-fast__firmware-verilator__ci_step_14.rc` | 2 | `9a271f2a916b0b6e` | 0 |
| `workflows/logs/rtl-fast__firmware-verilator__ci_step_3.log` | 1,362 | `51ba6f6275c89607` | # head 1a1e6665fcfd57943f2721cd3bd024eb16b0aa84 workflow rtl-fast.yml job firmware-verilator step ci_step_3: F |
| `workflows/logs/rtl-fast__firmware-verilator__ci_step_3.rc` | 2 | `9a271f2a916b0b6e` | 0 |
| `workflows/logs/rtl-fast__firmware-verilator__tree-after.txt` | 55 | `2d7cbc9d1a022490` | head 1a1e6665fcfd57943f2721cd3bd024eb16b0aa84 |
| `workflows/not_run-rounds3-4.json.txt` | 34,485 | `9ca30ce95f05911d` | { |
| `workflows/verify-1a1e6665.md` | 43,860 | `1a6b080f399a9e06` | \| Workflow \| Job \| Step \| Name \| rc \| Log or reason \| |
