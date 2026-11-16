# INDEX (generated from the files present, after sanitizing)

227 files.

| File | Bytes | sha256 (16) | First line |
|---|---:|---|---|
| `HANDOFF-r3.md` | 8759 | `5dd36499749ad9b8` | # HANDOFF round 3, [A784], lane 917 (#917, PR #918, part of #665) |
| `PR-BODY.md` | 34676 | `617cc2df9727c631` | [A784] |
| `comments/REVIEW-READY.md` | 4543 | `c61d36cf786510fb` | [A784] REVIEW READY |
| `receipts/budget/attribution/probe_attribution.log` | 3017 | `01e4abf6f3d73397` | # the review's probe_attribution.py (R846-2), unmodified, against a clean clone at 394612c5 (porcelain 0) |
| `receipts/budget/attribution/probe_attribution.py.txt` | 2625 | `c423fc43b515b946` | """Run against a checkout: python3 -B probe_attribution.py CHECKOUT. |
| `receipts/budget/budget.sh.txt` | 1319 | `7e4f069d5d8f2cae` | #!/usr/bin/env bash |
| `receipts/budget/held-8x8/aecp-held.json` | 5237 | `4802db0fc1eaa4ef` | { |
| `receipts/budget/held-8x8/aecp-held.txt` | 2758 | `214b4ab68f2d5d28` | wait ready |
| `receipts/budget/held-8x8/attribution-evidence.txt` | 620 | `65e80035c3e9e9b6` | held records (last byte, hold, commit, channel, interface, tag, bytes): |
| `receipts/budget/held-8x8/hold-and-commit-lines.txt` | 44 | `95a78c177c26dbe1` | 67363:RXH 100001427 2 |
| `receipts/budget/held-8x8/large-logs.sha256` | 87 | `513762806be2936d` | 538123cc85e7544e0a70f9abe8feaad0a0a8b5c558df1c61d797e4be791d3171 3417402 aecp-held.log |
| `receipts/budget/held-8x8/results.json` | 7728 | `9833cfa973e80769` | { |
| `receipts/budget/held-8x8/run.log` | 20974 | `72f020adf9d53b85` | HEAD 394612c55148b43354359daeab2aa88d4f019ec2 DIRTY 0 point 8x8 jobs 4 start 00:56:13 |
| `receipts/budget/held-8x8/run.rc` | 2 | `9a271f2a916b0b6e` | 0 |
| `receipts/budget/held-8x8/table.md` | 1801 | `8b791acb39cf4fa7` | ### 8x8 |
| `receipts/budget/held_evidence.py.txt` | 1727 | `d3adc0e2b858fe89` | """held_evidence.py <checkout> <build-dir>: the aecp-held log's held records, refused frames and probe row und |
| `receipts/budget/regrade/regrade.log` | 1144 | `5409034c775d0e68` | grader at 394612c55148b43354359daeab2aa88d4f019ec2 porcelain 0 |
| `receipts/budget/regrade/regrade.py.txt` | 1843 | `61c22f40248a2dd6` | """regrade.py <checkout> <build-dir> <point> <out> [<results-dir name>, default results]: grade a recorded run |
| `receipts/budget/regrade/regrade.rc` | 2 | `9a271f2a916b0b6e` | 0 |
| `receipts/budget/regrade/regrade_r3.sh.txt` | 780 | `462338878eccf8cf` | #!/usr/bin/env bash |
| `receipts/budget/selftest/large-logs.sha256` | 101 | `481133b3299491ed` | e100322832b35467da96db1c4e2123cfb06bba5cf92530798bab44558cc3a7ba 666365 budget-selftest-394612c5.log |
| `receipts/budget/selftest/selftest-excerpt.txt` | 37760 | `02502fd465480225` | # run.py --self-test on a clean clone at 394612c5 (rc 0): its held lines, its mutant verdicts and its end |
| `receipts/firmware/README.md` | 824 | `60a3f5de1bf94948` | # The firmware gate at 394612c5 |
| `receipts/firmware/first-attempt-without-pyyaml.log` | 1089 | `ae453bc1c2c68846` | HEAD 394612c55148b43354359daeab2aa88d4f019ec2 porcelain 0 |
| `receipts/firmware/test_ctrl_firmware-394612c5.log` | 73269 | `1cded401d476169f` | HEAD 394612c55148b43354359daeab2aa88d4f019ec2 porcelain 0 python <other-scratch>/gates/venv/bin/python3 |
| `receipts/generator/P1-refill-probe.txt` | 3655 | `a41b58fe435aacb7` | # probe P1 (R845-2 F1) on a disposable clone of 394612c5: aecp refill_ms 5 -> 10, then the gates before and af |
| `receipts/generator/gen_mailbox-selftest.log` | 13807 | `87aabc0db019dcdc` | # gen_mailbox.py --selftest, full output, clean clone at 394612c5 |
| `receipts/images/fixture-compare.txt` | 193 | `d24780abdb68870b` | fixture images: 46 at the base, 46 at 394612c5 |
| `receipts/images/fixture-images-394612c5.sha256` | 6236 | `4075bc562e8f12d8` | 039f7ea0b35ece75616df75ba8865ea8091bb86e3889c8018a122c2309adfe35  ./ctrl_image/head/endstation_ax7101_1x1_tdm8 |
| `receipts/images/fixture-images-base.sha256` | 6236 | `4075bc562e8f12d8` | 039f7ea0b35ece75616df75ba8865ea8091bb86e3889c8018a122c2309adfe35  ./ctrl_image/head/endstation_ax7101_1x1_tdm8 |
| `receipts/images/fixture-run-394612c5.txt` | 938 | `660aa9a368c710ec` | head 394612c55148b43354359daeab2aa88d4f019ec2 porcelain 0 |
| `receipts/images/images.sh.txt` | 1369 | `ba456e2ecf30c5a1` | #!/usr/bin/env bash |
| `receipts/images/images_r3.sh.txt` | 747 | `56201bd7ef889864` | #!/usr/bin/env bash |
| `receipts/images/split-1x1-394612c5.log` | 956 | `3ea9f569789a31cc` | head 394612c55148b43354359daeab2aa88d4f019ec2 porcelain 0 |
| `receipts/images/split-8x8-1if-394612c5.log` | 1238 | `1ce594ba0505ca3d` | head 394612c55148b43354359daeab2aa88d4f019ec2 porcelain 0 |
| `receipts/images/split-images-round1-and-base.txt` | 1602 | `0e7e5ab3c9a58d54` | head 84d8a214 split exports (route recipe), against the base route of the tree-identical 084cf7a8 |
| `receipts/images/split_image_r2.sh.txt` | 2340 | `754d56a265df4fc7` | #!/usr/bin/env bash |
| `receipts/local/local-gates-394612c5.txt` | 3402 | `97c4d25b6f98852c` | # local gates on a clean clone at 394612c5 (porcelain 0) |
| `receipts/mbx/make-and-mutants-394612c5.log` | 123647 | `0fbec5f69285f422` | HEAD 394612c55148b43354359daeab2aa88d4f019ec2 porcelain 0 |
| `receipts/rtl/trees.txt` | 2792 | `398dfba0be65ce36` | # git trees and blobs at 3926c271, 8f73ade5 and 394612c5 (equal hashes are equal content) |
| `receipts/tools/bgunit.sh.txt` | 1104 | `e179ace8f37ba1a3` | #!/usr/bin/env bash |
| `receipts/tools/clone.sh.txt` | 1009 | `3a11560baca80bfa` | #!/usr/bin/env bash |
| `receipts/tools/index.py.txt` | 1117 | `b2fccf980815e445` | """index.py <round-dir>: INDEX.md listing every file present under <round-dir> (but INDEX.md): path, bytes, sh |
| `receipts/tools/sanitize.py.sha256` | 199 | `9a5b3e52d0e52e13` | 3d1681bc50240a252c57424f65d65aafb3fcdd2aef9db485dd2ce045241f3ec1 1663 sanitize.py (not copied: its substitutio |
| `receipts/tools/unit.sh.txt` | 1017 | `c94397e685015eac` | #!/usr/bin/env bash |
| `receipts/tools/waitrc.sh.txt` | 365 | `ee226397e07ae9f1` | #!/usr/bin/env bash |
| `receipts/workflows/README.md` | 1463 | `1a1d0d48da1b5da2` | # Workflow jobs at 394612c5, step by step |
| `receipts/workflows/batch-d.log` | 3917 | `1d2bef21cadf14b9` | 00:59:36 start docs.yml wire-accountability |
| `receipts/workflows/batch-e.log` | 758 | `a8b49d5436b8dff6` | 00:59:37 start elaborate.yml elaborate-gates-0 |
| `receipts/workflows/large-logs.sha256` | 104 | `e2d2b8eb6ee2d208` | 23e564a1dc91b2068828ccc83d63941a4b38bb769a4a8f25add5b7a2a2083174 350375 docs__docs-gates-2__gate_41.log |
| `receipts/workflows/logs/docs__docs-check-no-git__ci_step_1.log` | 253 | `ab2a9f4ce01a5f9f` | # head 394612c55148b43354359daeab2aa88d4f019ec2 workflow docs.yml job docs-check-no-git step ci_step_1: Retain |
| `receipts/workflows/logs/docs__docs-check-no-git__ci_step_1.rc` | 2 | `9a271f2a916b0b6e` | 0 |
| `receipts/workflows/logs/docs__docs-check-no-git__ci_step_2.log` | 231 | `5471fd9f78b69d13` | # head 394612c55148b43354359daeab2aa88d4f019ec2 workflow docs.yml job docs-check-no-git step ci_step_2: Set CP |
| `receipts/workflows/logs/docs__docs-check-no-git__ci_step_2.rc` | 2 | `9a271f2a916b0b6e` | 0 |
| `receipts/workflows/logs/docs__docs-check-no-git__ci_step_3.log` | 471 | `2028e861fdbd53c6` | # head 394612c55148b43354359daeab2aa88d4f019ec2 workflow docs.yml job docs-check-no-git step ci_step_3: Strip  |
| `receipts/workflows/logs/docs__docs-check-no-git__ci_step_3.rc` | 2 | `9a271f2a916b0b6e` | 0 |
| `receipts/workflows/logs/docs__docs-check__DONE` | 9 | `fab506c9d858683b` | failed 0 |
| `receipts/workflows/logs/docs__docs-check__tree-after.txt` | 55 | `fd4dded7e314dfb5` | head 394612c55148b43354359daeab2aa88d4f019ec2 |
| `receipts/workflows/logs/docs__docs-gates-0__DONE` | 9 | `fab506c9d858683b` | failed 0 |
| `receipts/workflows/logs/docs__docs-gates-0__ci_step_1.log` | 371 | `5dbc526663c481cb` | # head 394612c55148b43354359daeab2aa88d4f019ec2 workflow docs.yml job docs-gates-0 step ci_step_1: Set CPU-der |
| `receipts/workflows/logs/docs__docs-gates-0__ci_step_1.rc` | 2 | `9a271f2a916b0b6e` | 0 |
| `receipts/workflows/logs/docs__docs-gates-0__ci_step_21.log` | 935 | `7819320fa41e408b` | # head 394612c55148b43354359daeab2aa88d4f019ec2 workflow docs.yml job docs-gates-0 step ci_step_21: Fetch the  |
| `receipts/workflows/logs/docs__docs-gates-0__ci_step_21.rc` | 2 | `9a271f2a916b0b6e` | 0 |
| `receipts/workflows/logs/docs__docs-gates-0__ci_step_5.log` | 491 | `04efeeada982ae25` | # head 394612c55148b43354359daeab2aa88d4f019ec2 workflow docs.yml job docs-gates-0 step ci_step_5: Install the |
| `receipts/workflows/logs/docs__docs-gates-0__ci_step_5.rc` | 2 | `9a271f2a916b0b6e` | 0 |
| `receipts/workflows/logs/docs__docs-gates-0__ci_step_52.log` | 566 | `6c76c323b2a403e2` | # head 394612c55148b43354359daeab2aa88d4f019ec2 workflow docs.yml job docs-gates-0 step ci_step_52: Fetch inve |
| `receipts/workflows/logs/docs__docs-gates-0__ci_step_52.rc` | 2 | `9a271f2a916b0b6e` | 0 |
| `receipts/workflows/logs/docs__docs-gates-0__ci_step_7.log` | 491 | `b75232a08ab4e4c9` | # head 394612c55148b43354359daeab2aa88d4f019ec2 workflow docs.yml job docs-gates-0 step ci_step_7: Install the |
| `receipts/workflows/logs/docs__docs-gates-0__ci_step_7.rc` | 2 | `9a271f2a916b0b6e` | 0 |
| `receipts/workflows/logs/docs__docs-gates-0__gate_1.log` | 1350 | `ce7d23f2f70f44b8` | # head 394612c55148b43354359daeab2aa88d4f019ec2 workflow docs.yml job docs-gates-0 step gate_1: Build the vali |
| `receipts/workflows/logs/docs__docs-gates-0__gate_1.rc` | 2 | `9a271f2a916b0b6e` | 0 |
| `receipts/workflows/logs/docs__docs-gates-0__gate_10.log` | 614 | `aaced1cf2f43a28e` | # head 394612c55148b43354359daeab2aa88d4f019ec2 workflow docs.yml job docs-gates-0 step gate_10: Audience diag |
| `receipts/workflows/logs/docs__docs-gates-0__gate_10.rc` | 2 | `9a271f2a916b0b6e` | 0 |
| `receipts/workflows/logs/docs__docs-gates-0__gate_11.log` | 521 | `ba9816c9b080ddf1` | # head 394612c55148b43354359daeab2aa88d4f019ec2 workflow docs.yml job docs-gates-0 step gate_11: Product solut |
| `receipts/workflows/logs/docs__docs-gates-0__gate_11.rc` | 2 | `9a271f2a916b0b6e` | 0 |
| `receipts/workflows/logs/docs__docs-gates-0__gate_12.log` | 606 | `e76bc9897111034a` | # head 394612c55148b43354359daeab2aa88d4f019ec2 workflow docs.yml job docs-gates-0 step gate_12: Verified subm |
| `receipts/workflows/logs/docs__docs-gates-0__gate_12.rc` | 2 | `9a271f2a916b0b6e` | 0 |
| `receipts/workflows/logs/docs__docs-gates-0__gate_13.log` | 615 | `5a38823019fef2b6` | # head 394612c55148b43354359daeab2aa88d4f019ec2 workflow docs.yml job docs-gates-0 step gate_13: HDL timing di |
| `receipts/workflows/logs/docs__docs-gates-0__gate_13.rc` | 2 | `9a271f2a916b0b6e` | 0 |
| `receipts/workflows/logs/docs__docs-gates-0__gate_14.log` | 493 | `22480ad368c54e7e` | # head 394612c55148b43354359daeab2aa88d4f019ec2 workflow docs.yml job docs-gates-0 step gate_14: Published dia |
| `receipts/workflows/logs/docs__docs-gates-0__gate_14.rc` | 2 | `9a271f2a916b0b6e` | 0 |
| `receipts/workflows/logs/docs__docs-gates-0__gate_15.log` | 1879 | `5c3244426373f621` | # head 394612c55148b43354359daeab2aa88d4f019ec2 workflow docs.yml job docs-gates-0 step gate_15: Milan feature |
| `receipts/workflows/logs/docs__docs-gates-0__gate_15.rc` | 2 | `9a271f2a916b0b6e` | 0 |
| `receipts/workflows/logs/docs__docs-gates-0__gate_16.log` | 493 | `f3105c80405ef08a` | # head 394612c55148b43354359daeab2aa88d4f019ec2 workflow docs.yml job docs-gates-0 step gate_16: Traceability  |
| `receipts/workflows/logs/docs__docs-gates-0__gate_16.rc` | 2 | `9a271f2a916b0b6e` | 0 |
| `receipts/workflows/logs/docs__docs-gates-0__gate_18.log` | 2985 | `2d0a0d0e24d89b36` | # head 394612c55148b43354359daeab2aa88d4f019ec2 workflow docs.yml job docs-gates-0 step gate_18: Imported gPTP |
| `receipts/workflows/logs/docs__docs-gates-0__gate_18.rc` | 2 | `9a271f2a916b0b6e` | 0 |
| `receipts/workflows/logs/docs__docs-gates-0__gate_19.log` | 3670 | `96e434dab5830230` | # head 394612c55148b43354359daeab2aa88d4f019ec2 workflow docs.yml job docs-gates-0 step gate_19: Code-quality  |
| `receipts/workflows/logs/docs__docs-gates-0__gate_19.rc` | 2 | `9a271f2a916b0b6e` | 0 |
| `receipts/workflows/logs/docs__docs-gates-0__gate_21.log` | 478 | `4540a2a9a9339f59` | # head 394612c55148b43354359daeab2aa88d4f019ec2 workflow docs.yml job docs-gates-0 step gate_21: Bare-metal sc |
| `receipts/workflows/logs/docs__docs-gates-0__gate_21.rc` | 2 | `9a271f2a916b0b6e` | 0 |
| `receipts/workflows/logs/docs__docs-gates-0__gate_24.log` | 51855 | `1560ecd89499d774` | # head 394612c55148b43354359daeab2aa88d4f019ec2 workflow docs.yml job docs-gates-0 step gate_24: Compiler-abse |
| `receipts/workflows/logs/docs__docs-gates-0__gate_24.rc` | 2 | `9a271f2a916b0b6e` | 0 |
| `receipts/workflows/logs/docs__docs-gates-0__gate_26.log` | 12669 | `3f566f7fc187f33b` | # head 394612c55148b43354359daeab2aa88d4f019ec2 workflow docs.yml job docs-gates-0 step gate_26: NVM record-sp |
| `receipts/workflows/logs/docs__docs-gates-0__gate_26.rc` | 2 | `9a271f2a916b0b6e` | 0 |
| `receipts/workflows/logs/docs__docs-gates-0__gate_27.log` | 781 | `9b63a9c818522633` | # head 394612c55148b43354359daeab2aa88d4f019ec2 workflow docs.yml job docs-gates-0 step gate_27: Capture measu |
| `receipts/workflows/logs/docs__docs-gates-0__gate_27.rc` | 2 | `9a271f2a916b0b6e` | 0 |
| `receipts/workflows/logs/docs__docs-gates-0__gate_28.log` | 26518 | `b70469131f6fc0fb` | # head 394612c55148b43354359daeab2aa88d4f019ec2 workflow docs.yml job docs-gates-0 step gate_28: Saved-state w |
| `receipts/workflows/logs/docs__docs-gates-0__gate_28.rc` | 2 | `9a271f2a916b0b6e` | 0 |
| `receipts/workflows/logs/docs__docs-gates-0__gate_29.log` | 5199 | `84db29dd560fd7f6` | # head 394612c55148b43354359daeab2aa88d4f019ec2 workflow docs.yml job docs-gates-0 step gate_29: SoC source-li |
| `receipts/workflows/logs/docs__docs-gates-0__gate_29.rc` | 2 | `9a271f2a916b0b6e` | 0 |
| `receipts/workflows/logs/docs__docs-gates-0__gate_30.log` | 3821 | `555c2b14a4aa72cc` | # head 394612c55148b43354359daeab2aa88d4f019ec2 workflow docs.yml job docs-gates-0 step gate_30: RTL source-li |
| `receipts/workflows/logs/docs__docs-gates-0__gate_30.rc` | 2 | `9a271f2a916b0b6e` | 0 |
| `receipts/workflows/logs/docs__docs-gates-0__gate_31.log` | 40969 | `759643a480b235c8` | # head 394612c55148b43354359daeab2aa88d4f019ec2 workflow docs.yml job docs-gates-0 step gate_31: Boundary-unit |
| `receipts/workflows/logs/docs__docs-gates-0__gate_31.rc` | 2 | `9a271f2a916b0b6e` | 0 |
| `receipts/workflows/logs/docs__docs-gates-0__gate_32.log` | 5400 | `0ccefc6ff1c7b5f3` | # head 394612c55148b43354359daeab2aa88d4f019ec2 workflow docs.yml job docs-gates-0 step gate_32: Port contract |
| `receipts/workflows/logs/docs__docs-gates-0__gate_32.rc` | 2 | `9a271f2a916b0b6e` | 0 |
| `receipts/workflows/logs/docs__docs-gates-0__gate_33.log` | 12945 | `9dfff0f475a0bd5c` | # head 394612c55148b43354359daeab2aa88d4f019ec2 workflow docs.yml job docs-gates-0 step gate_33: Fail-fast rat |
| `receipts/workflows/logs/docs__docs-gates-0__gate_33.rc` | 2 | `9a271f2a916b0b6e` | 0 |
| `receipts/workflows/logs/docs__docs-gates-0__gate_34.log` | 3106 | `3965ac3f19b21f08` | # head 394612c55148b43354359daeab2aa88d4f019ec2 workflow docs.yml job docs-gates-0 step gate_34: TODO ownershi |
| `receipts/workflows/logs/docs__docs-gates-0__gate_34.rc` | 2 | `9a271f2a916b0b6e` | 0 |
| `receipts/workflows/logs/docs__docs-gates-0__gate_35.log` | 29147 | `186dad825e2fee61` | # head 394612c55148b43354359daeab2aa88d4f019ec2 workflow docs.yml job docs-gates-0 step gate_35: Test-evidence |
| `receipts/workflows/logs/docs__docs-gates-0__gate_35.rc` | 2 | `9a271f2a916b0b6e` | 0 |
| `receipts/workflows/logs/docs__docs-gates-0__gate_36.log` | 4340 | `7bb39ffe84004faa` | # head 394612c55148b43354359daeab2aa88d4f019ec2 workflow docs.yml job docs-gates-0 step gate_36: Mechanical hy |
| `receipts/workflows/logs/docs__docs-gates-0__gate_36.rc` | 2 | `9a271f2a916b0b6e` | 0 |
| `receipts/workflows/logs/docs__docs-gates-0__gate_37.log` | 3539 | `a0b5a754e7f0fa1f` | # head 394612c55148b43354359daeab2aa88d4f019ec2 workflow docs.yml job docs-gates-0 step gate_37: SystemVerilog |
| `receipts/workflows/logs/docs__docs-gates-0__gate_37.rc` | 2 | `9a271f2a916b0b6e` | 0 |
| `receipts/workflows/logs/docs__docs-gates-0__gate_38.log` | 4271 | `25152b7a54ef0576` | # head 394612c55148b43354359daeab2aa88d4f019ec2 workflow docs.yml job docs-gates-0 step gate_38: C and C++ idi |
| `receipts/workflows/logs/docs__docs-gates-0__gate_38.rc` | 2 | `9a271f2a916b0b6e` | 0 |
| `receipts/workflows/logs/docs__docs-gates-0__gate_39.log` | 3351 | `9088ef0161080c91` | # head 394612c55148b43354359daeab2aa88d4f019ec2 workflow docs.yml job docs-gates-0 step gate_39: Python idiom  |
| `receipts/workflows/logs/docs__docs-gates-0__gate_39.rc` | 2 | `9a271f2a916b0b6e` | 0 |
| `receipts/workflows/logs/docs__docs-gates-0__gate_40.log` | 3054 | `179274a2903fd17e` | # head 394612c55148b43354359daeab2aa88d4f019ec2 workflow docs.yml job docs-gates-0 step gate_40: Shell idiom g |
| `receipts/workflows/logs/docs__docs-gates-0__gate_40.rc` | 2 | `9a271f2a916b0b6e` | 0 |
| `receipts/workflows/logs/docs__docs-gates-0__gate_43.log` | 462 | `1556029390a3aa4a` | # head 394612c55148b43354359daeab2aa88d4f019ec2 workflow docs.yml job docs-gates-0 step gate_43: Doc cited-pat |
| `receipts/workflows/logs/docs__docs-gates-0__gate_43.rc` | 2 | `9a271f2a916b0b6e` | 0 |
| `receipts/workflows/logs/docs__docs-gates-0__gate_44.log` | 492 | `2c51d5c091fb5a03` | # head 394612c55148b43354359daeab2aa88d4f019ec2 workflow docs.yml job docs-gates-0 step gate_44: Archive integ |
| `receipts/workflows/logs/docs__docs-gates-0__gate_44.rc` | 2 | `9a271f2a916b0b6e` | 0 |
| `receipts/workflows/logs/docs__docs-gates-0__gate_45.log` | 560 | `d410ab2fe7383207` | # head 394612c55148b43354359daeab2aa88d4f019ec2 workflow docs.yml job docs-gates-0 step gate_45: Per-page cont |
| `receipts/workflows/logs/docs__docs-gates-0__gate_45.rc` | 2 | `9a271f2a916b0b6e` | 0 |
| `receipts/workflows/logs/docs__docs-gates-0__gate_46.log` | 3967 | `97db9113d757b25a` | # head 394612c55148b43354359daeab2aa88d4f019ec2 workflow docs.yml job docs-gates-0 step gate_46: AEM store gen |
| `receipts/workflows/logs/docs__docs-gates-0__gate_46.rc` | 2 | `9a271f2a916b0b6e` | 0 |
| `receipts/workflows/logs/docs__docs-gates-0__gate_47.log` | 20118 | `2a06afabc8ea7406` | # head 394612c55148b43354359daeab2aa88d4f019ec2 workflow docs.yml job docs-gates-0 step gate_47: Sweep/build s |
| `receipts/workflows/logs/docs__docs-gates-0__gate_47.rc` | 2 | `9a271f2a916b0b6e` | 0 |
| `receipts/workflows/logs/docs__docs-gates-0__gate_48.log` | 9665 | `68fc9b7124aec093` | # head 394612c55148b43354359daeab2aa88d4f019ec2 workflow docs.yml job docs-gates-0 step gate_48: Deploy shape  |
| `receipts/workflows/logs/docs__docs-gates-0__gate_48.rc` | 2 | `9a271f2a916b0b6e` | 0 |
| `receipts/workflows/logs/docs__docs-gates-0__gate_49.log` | 28099 | `586b3487d5e7c602` | # head 394612c55148b43354359daeab2aa88d4f019ec2 workflow docs.yml job docs-gates-0 step gate_49: Entity shape  |
| `receipts/workflows/logs/docs__docs-gates-0__gate_49.rc` | 2 | `9a271f2a916b0b6e` | 0 |
| `receipts/workflows/logs/docs__docs-gates-0__gate_50.log` | 135972 | `7585fb8d78818c9e` | # head 394612c55148b43354359daeab2aa88d4f019ec2 workflow docs.yml job docs-gates-0 step gate_50: CI scheduling |
| `receipts/workflows/logs/docs__docs-gates-0__gate_50.rc` | 2 | `9a271f2a916b0b6e` | 0 |
| `receipts/workflows/logs/docs__docs-gates-0__gate_7.log` | 525 | `e2b938d3033701dd` | # head 394612c55148b43354359daeab2aa88d4f019ec2 workflow docs.yml job docs-gates-0 step gate_7: Link health, w |
| `receipts/workflows/logs/docs__docs-gates-0__gate_7.rc` | 2 | `9a271f2a916b0b6e` | 0 |
| `receipts/workflows/logs/docs__docs-gates-0__gate_8.log` | 504 | `7043a3fe27eab2d4` | # head 394612c55148b43354359daeab2aa88d4f019ec2 workflow docs.yml job docs-gates-0 step gate_8: Added-line em- |
| `receipts/workflows/logs/docs__docs-gates-0__gate_8.rc` | 2 | `9a271f2a916b0b6e` | 0 |
| `receipts/workflows/logs/docs__docs-gates-0__gate_9.log` | 543 | `fea40fb33a93978c` | # head 394612c55148b43354359daeab2aa88d4f019ec2 workflow docs.yml job docs-gates-0 step gate_9: Concise audien |
| `receipts/workflows/logs/docs__docs-gates-0__gate_9.rc` | 2 | `9a271f2a916b0b6e` | 0 |
| `receipts/workflows/logs/docs__docs-gates-0__tree-after.txt` | 55 | `fd4dded7e314dfb5` | head 394612c55148b43354359daeab2aa88d4f019ec2 |
| `receipts/workflows/logs/docs__docs-gates-1__DONE` | 9 | `fab506c9d858683b` | failed 0 |
| `receipts/workflows/logs/docs__docs-gates-1__ci_step_1.log` | 371 | `36b4756366825d8d` | # head 394612c55148b43354359daeab2aa88d4f019ec2 workflow docs.yml job docs-gates-1 step ci_step_1: Set CPU-der |
| `receipts/workflows/logs/docs__docs-gates-1__ci_step_1.rc` | 2 | `9a271f2a916b0b6e` | 0 |
| `receipts/workflows/logs/docs__docs-gates-1__ci_step_3.log` | 491 | `ecbd55d02f42fdae` | # head 394612c55148b43354359daeab2aa88d4f019ec2 workflow docs.yml job docs-gates-1 step ci_step_3: Install the |
| `receipts/workflows/logs/docs__docs-gates-1__ci_step_3.rc` | 2 | `9a271f2a916b0b6e` | 0 |
| `receipts/workflows/logs/docs__docs-gates-1__ci_step_5.log` | 491 | `ae68d3878eda99f2` | # head 394612c55148b43354359daeab2aa88d4f019ec2 workflow docs.yml job docs-gates-1 step ci_step_5: Install the |
| `receipts/workflows/logs/docs__docs-gates-1__ci_step_5.rc` | 2 | `9a271f2a916b0b6e` | 0 |
| `receipts/workflows/logs/docs__docs-gates-1__ci_step_9.log` | 934 | `28a9caff90eb7a8a` | # head 394612c55148b43354359daeab2aa88d4f019ec2 workflow docs.yml job docs-gates-1 step ci_step_9: Fetch the b |
| `receipts/workflows/logs/docs__docs-gates-1__ci_step_9.rc` | 2 | `9a271f2a916b0b6e` | 0 |
| `receipts/workflows/logs/docs__docs-gates-1__gate_25_0.log` | 50909 | `c62e277f64034b66` | # head 394612c55148b43354359daeab2aa88d4f019ec2 workflow docs.yml job docs-gates-1 step gate_25_0: End-station |
| `receipts/workflows/logs/docs__docs-gates-1__gate_25_0.rc` | 2 | `9a271f2a916b0b6e` | 0 |
| `receipts/workflows/logs/docs__docs-gates-1__tree-after.txt` | 55 | `fd4dded7e314dfb5` | head 394612c55148b43354359daeab2aa88d4f019ec2 |
| `receipts/workflows/logs/docs__docs-gates-2__DONE` | 9 | `fab506c9d858683b` | failed 0 |
| `receipts/workflows/logs/docs__docs-gates-2__ci_step_1.log` | 371 | `bb879be8f771957d` | # head 394612c55148b43354359daeab2aa88d4f019ec2 workflow docs.yml job docs-gates-2 step ci_step_1: Set CPU-der |
| `receipts/workflows/logs/docs__docs-gates-2__ci_step_1.rc` | 2 | `9a271f2a916b0b6e` | 0 |
| `receipts/workflows/logs/docs__docs-gates-2__ci_step_3.log` | 491 | `1b3fd27e75494acd` | # head 394612c55148b43354359daeab2aa88d4f019ec2 workflow docs.yml job docs-gates-2 step ci_step_3: Install the |
| `receipts/workflows/logs/docs__docs-gates-2__ci_step_3.rc` | 2 | `9a271f2a916b0b6e` | 0 |
| `receipts/workflows/logs/docs__docs-gates-2__ci_step_5.log` | 491 | `f6f6f332268f8374` | # head 394612c55148b43354359daeab2aa88d4f019ec2 workflow docs.yml job docs-gates-2 step ci_step_5: Install the |
| `receipts/workflows/logs/docs__docs-gates-2__ci_step_5.rc` | 2 | `9a271f2a916b0b6e` | 0 |
| `receipts/workflows/logs/docs__docs-gates-2__ci_step_9.log` | 934 | `27a823a7b0af1b03` | # head 394612c55148b43354359daeab2aa88d4f019ec2 workflow docs.yml job docs-gates-2 step ci_step_9: Fetch the b |
| `receipts/workflows/logs/docs__docs-gates-2__ci_step_9.rc` | 2 | `9a271f2a916b0b6e` | 0 |
| `receipts/workflows/logs/docs__docs-gates-2__gate_25_1.log` | 76633 | `c95ada5ca236c9ed` | # head 394612c55148b43354359daeab2aa88d4f019ec2 workflow docs.yml job docs-gates-2 step gate_25_1: End-station |
| `receipts/workflows/logs/docs__docs-gates-2__gate_25_1.rc` | 2 | `9a271f2a916b0b6e` | 0 |
| `receipts/workflows/logs/docs__docs-gates-2__gate_41.rc` | 2 | `9a271f2a916b0b6e` | 0 |
| `receipts/workflows/logs/docs__docs-gates-2__gate_42.log` | 123979 | `72992a20bdc8cc7a` | # head 394612c55148b43354359daeab2aa88d4f019ec2 workflow docs.yml job docs-gates-2 step gate_42: Local act run |
| `receipts/workflows/logs/docs__docs-gates-2__gate_42.rc` | 2 | `9a271f2a916b0b6e` | 0 |
| `receipts/workflows/logs/docs__docs-gates-2__tree-after.txt` | 55 | `fd4dded7e314dfb5` | head 394612c55148b43354359daeab2aa88d4f019ec2 |
| `receipts/workflows/logs/docs__wire-accountability__DONE` | 9 | `fab506c9d858683b` | failed 0 |
| `receipts/workflows/logs/docs__wire-accountability__ci_step_1.log` | 385 | `8bc9971cae1b3cd4` | # head 394612c55148b43354359daeab2aa88d4f019ec2 workflow docs.yml job wire-accountability step ci_step_1: Set  |
| `receipts/workflows/logs/docs__wire-accountability__ci_step_1.rc` | 2 | `9a271f2a916b0b6e` | 0 |
| `receipts/workflows/logs/docs__wire-accountability__ci_step_3.log` | 591 | `a828b9e644955e67` | # head 394612c55148b43354359daeab2aa88d4f019ec2 workflow docs.yml job wire-accountability step ci_step_3: Fetc |
| `receipts/workflows/logs/docs__wire-accountability__ci_step_3.rc` | 2 | `9a271f2a916b0b6e` | 0 |
| `receipts/workflows/logs/docs__wire-accountability__ci_step_4.log` | 5494 | `d97ae0733592751a` | # head 394612c55148b43354359daeab2aa88d4f019ec2 workflow docs.yml job wire-accountability step ci_step_4: Adve |
| `receipts/workflows/logs/docs__wire-accountability__ci_step_4.rc` | 2 | `9a271f2a916b0b6e` | 0 |
| `receipts/workflows/logs/docs__wire-accountability__tree-after.txt` | 55 | `fd4dded7e314dfb5` | head 394612c55148b43354359daeab2aa88d4f019ec2 |
| `receipts/workflows/logs/elaborate__elaborate-gates-0__DONE` | 9 | `fab506c9d858683b` | failed 0 |
| `receipts/workflows/logs/elaborate__elaborate-gates-0__ci_step_1.log` | 388 | `f291c378648edeb0` | # head 394612c55148b43354359daeab2aa88d4f019ec2 workflow elaborate.yml job elaborate-gates-0 step ci_step_1: S |
| `receipts/workflows/logs/elaborate__elaborate-gates-0__ci_step_1.rc` | 2 | `9a271f2a916b0b6e` | 0 |
| `receipts/workflows/logs/elaborate__elaborate-gates-0__ci_step_4.log` | 995 | `27fa5e315c952ed3` | # head 394612c55148b43354359daeab2aa88d4f019ec2 workflow elaborate.yml job elaborate-gates-0 step ci_step_4: F |
| `receipts/workflows/logs/elaborate__elaborate-gates-0__ci_step_4.rc` | 2 | `9a271f2a916b0b6e` | 0 |
| `receipts/workflows/logs/elaborate__elaborate-gates-0__gate_15_0.log` | 51034 | `50dc3295e1ab13b5` | # head 394612c55148b43354359daeab2aa88d4f019ec2 workflow elaborate.yml job elaborate-gates-0 step gate_15_0: E |
| `receipts/workflows/logs/elaborate__elaborate-gates-0__gate_15_0.rc` | 2 | `9a271f2a916b0b6e` | 0 |
| `receipts/workflows/logs/elaborate__elaborate-gates-0__scope.log` | 18604 | `21647160ca29c321` | # head 394612c55148b43354359daeab2aa88d4f019ec2 workflow elaborate.yml job elaborate-gates-0 step scope: Decid |
| `receipts/workflows/logs/elaborate__elaborate-gates-0__scope.rc` | 2 | `9a271f2a916b0b6e` | 0 |
| `receipts/workflows/logs/elaborate__elaborate-gates-0__tree-after.txt` | 55 | `fd4dded7e314dfb5` | head 394612c55148b43354359daeab2aa88d4f019ec2 |
| `receipts/workflows/logs/elaborate__elaborate-gates-1__DONE` | 9 | `fab506c9d858683b` | failed 0 |
| `receipts/workflows/logs/elaborate__elaborate-gates-1__ci_step_1.log` | 388 | `feecd589bad79d34` | # head 394612c55148b43354359daeab2aa88d4f019ec2 workflow elaborate.yml job elaborate-gates-1 step ci_step_1: S |
| `receipts/workflows/logs/elaborate__elaborate-gates-1__ci_step_1.rc` | 2 | `9a271f2a916b0b6e` | 0 |
| `receipts/workflows/logs/elaborate__elaborate-gates-1__ci_step_23.log` | 552 | `12a112bc5cc80bff` | # head 394612c55148b43354359daeab2aa88d4f019ec2 workflow elaborate.yml job elaborate-gates-1 step ci_step_23:  |
| `receipts/workflows/logs/elaborate__elaborate-gates-1__ci_step_23.rc` | 2 | `9a271f2a916b0b6e` | 0 |
| `receipts/workflows/logs/elaborate__elaborate-gates-1__ci_step_4.log` | 995 | `71c24084279db711` | # head 394612c55148b43354359daeab2aa88d4f019ec2 workflow elaborate.yml job elaborate-gates-1 step ci_step_4: F |
| `receipts/workflows/logs/elaborate__elaborate-gates-1__ci_step_4.rc` | 2 | `9a271f2a916b0b6e` | 0 |
| `receipts/workflows/logs/elaborate__elaborate-gates-1__gate_15_1.log` | 83081 | `59439423658582cc` | # head 394612c55148b43354359daeab2aa88d4f019ec2 workflow elaborate.yml job elaborate-gates-1 step gate_15_1: E |
| `receipts/workflows/logs/elaborate__elaborate-gates-1__gate_15_1.rc` | 2 | `9a271f2a916b0b6e` | 0 |
| `receipts/workflows/logs/elaborate__elaborate-gates-1__gate_19.log` | 1607 | `29582acf9d2700a5` | # head 394612c55148b43354359daeab2aa88d4f019ec2 workflow elaborate.yml job elaborate-gates-1 step gate_19: Sta |
| `receipts/workflows/logs/elaborate__elaborate-gates-1__gate_19.rc` | 2 | `9a271f2a916b0b6e` | 0 |
| `receipts/workflows/logs/elaborate__elaborate-gates-1__scope.log` | 18604 | `4037a9a19e6a0951` | # head 394612c55148b43354359daeab2aa88d4f019ec2 workflow elaborate.yml job elaborate-gates-1 step scope: Decid |
| `receipts/workflows/logs/elaborate__elaborate-gates-1__scope.rc` | 2 | `9a271f2a916b0b6e` | 0 |
| `receipts/workflows/logs/elaborate__elaborate-gates-1__tree-after.txt` | 55 | `fd4dded7e314dfb5` | head 394612c55148b43354359daeab2aa88d4f019ec2 |
| `receipts/workflows/logs/rtl-fast__changes__DONE` | 9 | `fab506c9d858683b` | failed 0 |
| `receipts/workflows/logs/rtl-fast__changes__ci_step_1.log` | 219 | `4baa77f722b68328` | # head 394612c55148b43354359daeab2aa88d4f019ec2 workflow rtl-fast.yml job changes step ci_step_1: Set CPU-deri |
| `receipts/workflows/logs/rtl-fast__changes__ci_step_1.rc` | 2 | `9a271f2a916b0b6e` | 0 |
| `receipts/workflows/logs/rtl-fast__changes__scope.log` | 18519 | `a392f16bd3e2aefd` | # head 394612c55148b43354359daeab2aa88d4f019ec2 workflow rtl-fast.yml job changes step scope: Classify the cha |
| `receipts/workflows/logs/rtl-fast__changes__scope.rc` | 2 | `9a271f2a916b0b6e` | 0 |
| `receipts/workflows/logs/rtl-fast__changes__tree-after.txt` | 55 | `fd4dded7e314dfb5` | head 394612c55148b43354359daeab2aa88d4f019ec2 |
| `receipts/workflows/logs/rtl__full-ci-gate__DONE` | 9 | `fab506c9d858683b` | failed 0 |
| `receipts/workflows/logs/rtl__full-ci-gate__ci_step_1.log` | 369 | `56dffb2d66990b23` | # head 394612c55148b43354359daeab2aa88d4f019ec2 workflow rtl.yml job full-ci-gate step ci_step_1: Set CPU-deri |
| `receipts/workflows/logs/rtl__full-ci-gate__ci_step_1.rc` | 2 | `9a271f2a916b0b6e` | 0 |
| `receipts/workflows/logs/rtl__full-ci-gate__ci_step_5.log` | 660 | `c31a99760affa5e8` | # head 394612c55148b43354359daeab2aa88d4f019ec2 workflow rtl.yml job full-ci-gate step ci_step_5: Hold every w |
| `receipts/workflows/logs/rtl__full-ci-gate__ci_step_5.rc` | 2 | `9a271f2a916b0b6e` | 0 |
| `receipts/workflows/logs/rtl__full-ci-gate__gate.log` | 18699 | `0edb292cec900420` | # head 394612c55148b43354359daeab2aa88d4f019ec2 workflow rtl.yml job full-ci-gate step gate: Decide whether th |
| `receipts/workflows/logs/rtl__full-ci-gate__gate.rc` | 2 | `9a271f2a916b0b6e` | 0 |
| `receipts/workflows/logs/rtl__full-ci-gate__target.log` | 486 | `9c48792f418e9523` | # head 394612c55148b43354359daeab2aa88d4f019ec2 workflow rtl.yml job full-ci-gate step target: Print the event |
| `receipts/workflows/logs/rtl__full-ci-gate__target.rc` | 2 | `9a271f2a916b0b6e` | 0 |
| `receipts/workflows/logs/rtl__full-ci-gate__tree-after.txt` | 55 | `fd4dded7e314dfb5` | head 394612c55148b43354359daeab2aa88d4f019ec2 |
| `receipts/workflows/not_run.json` | 32455 | `921191ef4a187d52` | { |
| `receipts/workflows/run_wf.py.txt` | 7332 | `2f15d0f355f7a1d8` | #!/usr/bin/env python3 |
| `receipts/workflows/verify-394612c5.md` | 18184 | `69ce94da0597f598` | / Workflow / Job / Step / Name / rc / Log or reason / |
| `receipts/workflows/verify_wf.py.txt` | 2759 | `b75276bff129be16` | #!/usr/bin/env python3 |
| `receipts/workflows/verify_wf_jobs.py.txt` | 3067 | `48c500beda2d8e8c` | #!/usr/bin/env python3 |
| `receipts/workflows/wf_batch.sh.txt` | 626 | `8300a62666cdec13` | #!/usr/bin/env bash |
