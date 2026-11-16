# INDEX (generated from the files present, after sanitizing)

318 files.

| File | Bytes | sha256 (16) | First line |
|---|---:|---|---|
| `HANDOFF-r1.md` | 28,184 | `679f435b0ee45622` | # [A786] #920 round 1: the split's saved-state store saves a burst of acknowledged name changes in time |
| `PR-BODY.md` | 10,068 | `811513c57ff0fc64` | [A786] |
| `STOP-r1.md` | 4,672 | `20f20ebcf28a4b83` | [A786] STOP: the 8x8/1if split platform image misses the timing floor at all three directives |
| `receipts/bench/persist-1.console.txt` | 8,975 | `78a1aa2e409eb3ad` | 2026-11-15T20:35:08.474Z PP_STAT=5b000444 backed=1 dirty=0 stale=0 img_valid=1 pend=0 verdict=0 alarm=0 |
| `receipts/bench/persist-1.pcap.sha256` | 141 | `01b4ced93a54eb40` | f838c487d13759c898cbaa06663760beda52e705215800010c0d44c504bf5c45  112602 bytes  the harness capture of the persistenc... |
| `receipts/bench/persist-1.setname-pacing.txt` | 15,182 | `e8270d068f2a2953` | 0.000 ms  +   0.000  CMD seq=  103 desc=0x0000/0   name_index=0 status=0 'ENTITY_NEW_NAME' |
| `receipts/bench/persist-1.summary.txt` | 1,778 | `77b2c819130e147a` | The in-house persistence scenario on the board's current image (no reflash), 2026-11-15, under the bench lock: the ru... |
| `receipts/cause/harness-replay-1x1/large-files.sha256` | 270 | `03501bf0a44f0903` | 2a5187278f6319625d3dd53f07320b4e8199841b69ed0aa1ad02471b78de558c 82787377 save-burst.log |
| `receipts/cause/harness-replay-1x1/run-tail.txt` | 804 | `a2e51340970ff8a7` | HEAD 255458aa9df052c19ee0a8e843885dced328767d DIRTY 0 point 1x1 jobs 2 args --groups save-burst,save-flight start 22:... |
| `receipts/cause/harness-replay-1x1/save-burst.json` | 16,379 | `b7bb58d14a615d07` | { |
| `receipts/cause/harness-replay-1x1/save-flight.json` | 12,053 | `05fef550a43ba077` | { |
| `receipts/cause/harness-replay-1x1/table.md` | 5,113 | `adc3cec264acb7ee` | ### 1x1 |
| `receipts/cause/harness-replay-8x8-1if/large-files.sha256` | 179 | `9f7e3a065700462b` | 5f14628e3d0c1e09bcad4c8038618adee8ebd3d94c1d044aae1ef8d91c064ee1 75280133 save-burst.log |
| `receipts/cause/harness-replay-8x8-1if/run-tail.txt` | 789 | `122069ee43356b65` | HEAD 255458aa9df052c19ee0a8e843885dced328767d DIRTY 0 point 8x8-1if jobs 2 args --groups save-burst,save-flight start... |
| `receipts/cause/harness-replay-8x8-1if/save-flight.json` | 13,801 | `573cf04b85640254` | { |
| `receipts/cause/harness-replay-8x8-1if/table.md` | 3,912 | `c2a75b7c0d4126ee` | ### 8x8-1if |
| `receipts/cause/harness-replay-8x8-1if/trap.txt` | 1,042 | `d775edeff6bafbac` | save-burst at 8x8/1if on the base firmware (659d7687 with only the harness): the CPU traps during the burst. |
| `receipts/cause/names-table-1x1.txt` | 1,679 | `248d7f8d74e60e08` | AECP_ENTITY_NAMES_INIT of the 1x1/1if split image built at the base 659d7687 (the budget harness's build): ordinal, {... |
| `receipts/cause/rehearsal-setname-pacing.txt` | 15,182 | `0875fc15a07064a7` | 0.000 ms  +   0.000  CMD seq=  103 desc=0x0000/0   name_index=0 status=0 'ENTITY_NEW_NAME' |
| `receipts/cause/unit-burst-before-fix.txt` | 5,914 | `c12e77ed581b3b4e` | tsn-c-stack at 715589c1db7cf67e2f3259fd7083ebc7f0923376 |
| `receipts/cause/unit-nvm-after-fix.txt` | 1,692 | `b213c00c92bc8811` | tsn-c-stack at 715589c1db7cf67e2f3259fd7083ebc7f0923376 |
| `receipts/fix/8x8-1if-stated-triage.txt` | 5,515 | `66f9b8399ba1f497` | # The 8x8/1if stated-cost lines (STATED), the base (replay2: 659d7687's image) against the fix (fix2: 9e28059b's image), |
| `receipts/fix/burst-8x8-1if/large-files.sha256` | 270 | `6bbfd2543cfe6d53` | 25212e8d0dbea148d1e7210b3d56e6f2e60b5ca49f59483d4f3c1b0510d7ba07 64338310 save-burst.log |
| `receipts/fix/burst-8x8-1if/run-tail.txt` | 961 | `65076ca20fb2be6d` | HEAD 3d9cd3e00491c139cd38add163bb17065cd149b2 DIRTY 0 point 8x8-1if jobs 2 args --groups save-burst,save-flight start... |
| `receipts/fix/burst-8x8-1if/save-burst.json` | 31,131 | `c87d2a4a8b777f75` | { |
| `receipts/fix/burst-8x8-1if/save-flight.json` | 14,771 | `0bae272140766966` | { |
| `receipts/fix/burst-8x8-1if/table.md` | 5,246 | `98f84e15e6bc4328` | ### 8x8-1if |
| `receipts/gates/scripts_check_doc_paths.py.txt` | 106 | `c1c9809bb1d07b7c` | doc path gate: OK (1166 cited paths all resolve, 2 allowlisted; 10 line anchor(s) within their file) |
| `receipts/gates/scripts_check_doc_style.py.txt` | 52 | `3f9b32359d6419ee` | documentation style: OK (23 current documents) |
| `receipts/gates/scripts_check_py_idiom.py.txt` | 466 | `1c2a6808ee490dea` | py idiom: 631 first-party modules, 310729 lines |
| `receipts/gates/scripts_check_py_idiom.py_--selftest.txt` | 2,536 | `68a882038dd04b97` | [PASS] a bare except is a finding |
| `receipts/gates/scripts_docs_check.py.txt` | 133 | `14bfe5e1c26d98de` | docs_check: 0 finding(s) across 219 md files + 1600 scrubbed text files, scrub self-test 23/23, routing arms 4/4 [git... |
| `receipts/gates/sw_litex_test_ctrl_memory.py.txt` | 44,840 | `87ea7bdaa71cd7e7` | test_ctrl_memory: the split placement's firmware memory (#640 M8a) |
| `receipts/gates/tb_verilator_ctrl_service_budget_load_grade.py_--check.txt` | 1,417 | `2398127446f39f5e` | \| Point \| Load at the pin \| Load with tsn-c-stack#32 (owed to the pin move) \| Ceiling \| Compute for 0.70 (with t... |
| `receipts/harness/8x8-1if-stated-against-914.txt` | 1,420 | `562bd54cc29ae336` | # 8x8/1if: every STATED line of the combined regrade (97 groups), by kind, its most measured against this base's |
| `receipts/harness/regrade-1x1.txt` | 18,635 | `6edbc9d2f772b708` | HEAD 11860de216d2c211b02c6ddcc33e99bdf20e8594 DIRTY 0 point 1x1 jobs 1 args --regrade --out <scratch>/build/comb-1x1/... |
| `receipts/harness/regrade-8x8-1if.txt` | 113,601 | `024bd2d858c5b253` | HEAD 11860de216d2c211b02c6ddcc33e99bdf20e8594 DIRTY 0 point 8x8-1if jobs 1 args --regrade --out <scratch>/build/comb-... |
| `receipts/harness/results-json.sha256.txt` | 284 | `8b2248d50d7cbc0d` | # sha256 and size of each combined regrade's results.json (not kept: over 200 KB) |
| `receipts/harness/run-full1-1x1.txt` | 27,411 | `824bd3822bd5ea95` | HEAD 11860de216d2c211b02c6ddcc33e99bdf20e8594 DIRTY 0 point 1x1 jobs 8 args  start 23:29:36 |
| `receipts/harness/run-full1-8x8-1if.txt` | 27,320 | `d8959a3648cbfb8f` | HEAD 11860de216d2c211b02c6ddcc33e99bdf20e8594 DIRTY 0 point 8x8-1if jobs 8 args  start 23:23:22 |
| `receipts/harness/run-full1b-1x1.txt` | 33,911 | `73f916057a6f9ff9` | HEAD 11860de216d2c211b02c6ddcc33e99bdf20e8594 DIRTY 0 point 1x1 jobs 8 args --groups backlog-adp@program-aged1-4,back... |
| `receipts/harness/run-full1b-8x8-1if.txt` | 68,194 | `4b1d9b6d261e77a1` | HEAD 11860de216d2c211b02c6ddcc33e99bdf20e8594 DIRTY 0 point 8x8-1if jobs 6 args --groups backlog-adp@program-aged2-7,... |
| `receipts/harness/run-full1c-1x1.txt` | 2,519 | `1d2babd5d953d982` | HEAD 11860de216d2c211b02c6ddcc33e99bdf20e8594 DIRTY 0 point 1x1 jobs 8 args --reuse-build --out <scratch>/build/full1... |
| `receipts/harness/run-full1c-8x8-1if.txt` | 7,090 | `44c6e10399f4b924` | HEAD 11860de216d2c211b02c6ddcc33e99bdf20e8594 DIRTY 0 point 8x8-1if jobs 8 args --reuse-build --out <scratch>/build/f... |
| `receipts/harness/run-full1d-8x8-1if.txt` | 7,410 | `e84d5f279d190362` | HEAD 11860de216d2c211b02c6ddcc33e99bdf20e8594 DIRTY 0 point 8x8-1if jobs 6 args --reuse-build --out <scratch>/build/f... |
| `receipts/harness/sources-1x1.json` | 3,786 | `0ab6bed279946417` | { |
| `receipts/harness/sources-8x8-1if.json` | 4,141 | `9133812abeac0e54` | { |
| `receipts/harness/table-1x1.md` | 191,344 | `aaf410f3d24b2940` | ### 1x1 |
| `receipts/harness/table-8x8-1if.md` | 190,265 | `f2c1f8b01e59e748` | ### 8x8-1if |
| `receipts/image/1x1-AltSpreadLogic_high.txt` | 1,833 | `a61316c5dda76b86` | image endstation_ax7101_1x1_tdm8, placement directive AltSpreadLogic_high |
| `receipts/image/1x1-ExtraPostPlacementOpt.txt` | 1,790 | `480e73a5da79efa3` | image endstation_ax7101_1x1_tdm8, placement directive ExtraPostPlacementOpt |
| `receipts/image/1x1-ExtraTimingOpt.txt` | 1,822 | `49daef94600324ab` | image endstation_ax7101_1x1_tdm8, placement directive ExtraTimingOpt |
| `receipts/image/8x8-AltSpreadLogic_high.txt` | 1,694 | `7128dcaead072f98` | image endstation_ax7101_8x8, placement directive AltSpreadLogic_high |
| `receipts/image/8x8-ExtraPostPlacementOpt.txt` | 1,650 | `43c95602d39338d5` | image endstation_ax7101_8x8, placement directive ExtraPostPlacementOpt |
| `receipts/image/8x8-ExtraTimingOpt.txt` | 1,725 | `a6cfcf77bdebee4b` | image endstation_ax7101_8x8, placement directive ExtraTimingOpt |
| `receipts/image/base-659d7687-8x8-ExtraPostPlacementOpt.txt` | 1,655 | `0a04cbad306dcfbc` | image endstation_ax7101_8x8, placement directive ExtraPostPlacementOpt |
| `receipts/image/rom-per-image-base-659d7687.txt` | 2,157 | `187a2fc64f64f41a` | fixture-1x1-1if: rc 0 rom 111024 in 112640, sram 55152 in 55296, tiles 41.0, ledgered None None, ctrl_app.elf sha256 ... |
| `receipts/image/rom-per-image-f1f7c3e8.txt` | 2,157 | `dcc819c1d27c4378` | fixture-1x1-1if: rc 0 rom 111320 in 112640, sram 55216 in 55296, tiles 41.0, ledgered None None, ctrl_app.elf sha256 ... |
| `receipts/large-files.sha256` | 778 | `7debb0301536b222` | # files over 200 KB, kept as sha256 and size only |
| `receipts/sweep/gptp_shadow.txt` | 10,080 | `6da102a53a7cb238` | python3 test_mutant_lifecycle.py |
| `receipts/sweep/media_phase.txt` | 68,532 | `d4bdb3774d8a4668` | <tools>/pinned-verilator-5.050/verilator --cc --exe --build -j 0 --public-flat-rw -Wall -Wno-fatal -Werror-UNDRIVEN -... |
| `receipts/sweep/milan_dp.excerpt.txt` | 22,214 | `dd7770a4a8c4eab9` | # excerpt of milan_dp.txt (3,035,638 B, 24,228 lines, sha256 in large-files.sha256): its first 30 and last 80 lines |
| `receipts/sweep/spec-serial.json` | 623 | `242c41f2019df6d8` | { |
| `receipts/sweep/spec.json` | 587 | `6409d01c23a5aa18` | { |
| `receipts/sweep/summary-so-far.txt` | 1,087 | `9fbf2daffc5e1f71` | shard: 0/1   selected suites: 65 |
| `receipts/tests/budget-selftest-54280c94.results.txt` | 71,315 | `ad03687afb9fcdac` | # result lines of budget-selftest-54280c94.txt (815,974 B, sha256 in large-files.sha256): 875 PASS lines, 0 FAIL lines |
| `receipts/tests/budget-selftest-9646113b.results.txt` | 71,234 | `88cf67f103c54377` | # result lines of budget-selftest-9646113b.txt (815,864 B, sha256 in large-files.sha256): 875 PASS lines, 0 FAIL lines |
| `receipts/tests/controls/ctl-store-join-dropped-8x8-1if.txt` | 493 | `7b4638a4d909be49` | BURST save-burst: 107 name(s), the latest durable 1366.653 ms after its response (name 0; target 5,000 ms), 7 save(s)... |
| `receipts/tests/controls/ctl-store-names-past-256-lost-1x1.txt` | 606 | `8c561318a2089465` | BURST save-burst: 39 name(s), the latest durable never after its response (name 38; target 5,000 ms), 1 save(s), the ... |
| `receipts/tests/controls/ctl-store-next-save-waits-1x1.txt` | 494 | `959df006bd36bab1` | BURST save-flight: 1 name(s), the latest durable 1082.204 ms after its response (name 0; target 5,000 ms), 2 save(s),... |
| `receipts/tests/controls/ctl-store-step-only-owed-8x8-1if.txt` | 1,292 | `511e5852c5913d8d` | BURST save-burst: 107 name(s), the latest durable 8021.164 ms after its response (name 48; target 5,000 ms), 2 save(s... |
| `receipts/tests/nvm-split-target-1x1-104f85cc.txt` | 659 | `0952727c4a0561b4` | CONTROL step-over-t-svc caught: every phase's longest step at T_svc (2,000,000 cycles) passes and one cycle past it i... |
| `receipts/tests/nvm-split-target-8x8-104f85cc.txt` | 664 | `6f0fd3b8d15b34be` | CONTROL step-over-t-svc caught: every phase's longest step at T_svc (2,000,000 cycles) passes and one cycle past it i... |
| `receipts/tests/store-suite-selftest-54280c94.txt` | 32,883 | `1438db5c78d1d931` | HEAD 54280c9408ba06a16fa925f85e0398a16f33777d DIRTY 0 start 05:24:33 |
| `receipts/workflows/54280c94/batch-b.txt` | 4,240 | `719f3b9782e22946` | 05:00:21 start docs.yml wire-accountability |
| `receipts/workflows/54280c94/batch-c.txt` | 295 | `0e269c0248ace531` | 05:39:08 start rtl-fast.yml firmware-boundary |
| `receipts/workflows/54280c94/batch-d.txt` | 431 | `9d223f44da83482e` | 06:42:59 start elaborate.yml elaborate-gates-1 |
| `receipts/workflows/54280c94/docs__docs-check-no-git__ci_step_1.log` | 285 | `9fd90e3e0b2015e0` | # head 54280c9408ba06a16fa925f85e0398a16f33777d workflow docs.yml job docs-check-no-git step ci_step_1: Retain checko... |
| `receipts/workflows/54280c94/docs__docs-check-no-git__ci_step_1.rc` | 2 | `9a271f2a916b0b6e` | 0 |
| `receipts/workflows/54280c94/docs__docs-check-no-git__ci_step_2.log` | 263 | `90e64561c9976479` | # head 54280c9408ba06a16fa925f85e0398a16f33777d workflow docs.yml job docs-check-no-git step ci_step_2: Set CPU-deriv... |
| `receipts/workflows/54280c94/docs__docs-check-no-git__ci_step_2.rc` | 2 | `9a271f2a916b0b6e` | 0 |
| `receipts/workflows/54280c94/docs__docs-check-no-git__ci_step_3.log` | 503 | `96ce1ed25d970787` | # head 54280c9408ba06a16fa925f85e0398a16f33777d workflow docs.yml job docs-check-no-git step ci_step_3: Strip git met... |
| `receipts/workflows/54280c94/docs__docs-check-no-git__ci_step_3.rc` | 2 | `9a271f2a916b0b6e` | 0 |
| `receipts/workflows/54280c94/docs__docs-gates-0__DONE` | 9 | `fab506c9d858683b` | failed 0 |
| `receipts/workflows/54280c94/docs__docs-gates-0__ci_step_1.log` | 403 | `ec647c65e7870758` | # head 54280c9408ba06a16fa925f85e0398a16f33777d workflow docs.yml job docs-gates-0 step ci_step_1: Set CPU-derived jo... |
| `receipts/workflows/54280c94/docs__docs-gates-0__ci_step_1.rc` | 2 | `9a271f2a916b0b6e` | 0 |
| `receipts/workflows/54280c94/docs__docs-gates-0__ci_step_21.log` | 1,063 | `bfaa46d4cfeba831` | # head 54280c9408ba06a16fa925f85e0398a16f33777d workflow docs.yml job docs-gates-0 step ci_step_21: Fetch the builder... |
| `receipts/workflows/54280c94/docs__docs-gates-0__ci_step_21.rc` | 2 | `9a271f2a916b0b6e` | 0 |
| `receipts/workflows/54280c94/docs__docs-gates-0__ci_step_5.log` | 523 | `23b8978473af5a26` | # head 54280c9408ba06a16fa925f85e0398a16f33777d workflow docs.yml job docs-gates-0 step ci_step_5: Install the python... |
| `receipts/workflows/54280c94/docs__docs-gates-0__ci_step_5.rc` | 2 | `9a271f2a916b0b6e` | 0 |
| `receipts/workflows/54280c94/docs__docs-gates-0__ci_step_52.log` | 630 | `bc2e0ef1e791aee5` | # head 54280c9408ba06a16fa925f85e0398a16f33777d workflow docs.yml job docs-gates-0 step ci_step_52: Fetch inventory d... |
| `receipts/workflows/54280c94/docs__docs-gates-0__ci_step_52.rc` | 2 | `9a271f2a916b0b6e` | 0 |
| `receipts/workflows/54280c94/docs__docs-gates-0__ci_step_7.log` | 523 | `3dac50a23291e16e` | # head 54280c9408ba06a16fa925f85e0398a16f33777d workflow docs.yml job docs-gates-0 step ci_step_7: Install the pinned... |
| `receipts/workflows/54280c94/docs__docs-gates-0__ci_step_7.rc` | 2 | `9a271f2a916b0b6e` | 0 |
| `receipts/workflows/54280c94/docs__docs-gates-0__gate_1.log` | 1,446 | `163265b61a6f7f16` | # head 54280c9408ba06a16fa925f85e0398a16f33777d workflow docs.yml job docs-gates-0 step gate_1: Build the validated H... |
| `receipts/workflows/54280c94/docs__docs-gates-0__gate_1.rc` | 2 | `9a271f2a916b0b6e` | 0 |
| `receipts/workflows/54280c94/docs__docs-gates-0__gate_10.log` | 646 | `76b47d5158789281` | # head 54280c9408ba06a16fa925f85e0398a16f33777d workflow docs.yml job docs-gates-0 step gate_10: Audience diagram no-... |
| `receipts/workflows/54280c94/docs__docs-gates-0__gate_10.rc` | 2 | `9a271f2a916b0b6e` | 0 |
| `receipts/workflows/54280c94/docs__docs-gates-0__gate_11.log` | 553 | `e289821b7f977b5b` | # head 54280c9408ba06a16fa925f85e0398a16f33777d workflow docs.yml job docs-gates-0 step gate_11: Product solution sou... |
| `receipts/workflows/54280c94/docs__docs-gates-0__gate_11.rc` | 2 | `9a271f2a916b0b6e` | 0 |
| `receipts/workflows/54280c94/docs__docs-gates-0__gate_12.log` | 638 | `e1ba5b2b05518d94` | # head 54280c9408ba06a16fa925f85e0398a16f33777d workflow docs.yml job docs-gates-0 step gate_12: Verified submodule d... |
| `receipts/workflows/54280c94/docs__docs-gates-0__gate_12.rc` | 2 | `9a271f2a916b0b6e` | 0 |
| `receipts/workflows/54280c94/docs__docs-gates-0__gate_13.log` | 647 | `3cdab89e05186f0d` | # head 54280c9408ba06a16fa925f85e0398a16f33777d workflow docs.yml job docs-gates-0 step gate_13: HDL timing diagram n... |
| `receipts/workflows/54280c94/docs__docs-gates-0__gate_13.rc` | 2 | `9a271f2a916b0b6e` | 0 |
| `receipts/workflows/54280c94/docs__docs-gates-0__gate_14.log` | 525 | `31a1955f6cf36f28` | # head 54280c9408ba06a16fa925f85e0398a16f33777d workflow docs.yml job docs-gates-0 step gate_14: Published diagram PN... |
| `receipts/workflows/54280c94/docs__docs-gates-0__gate_14.rc` | 2 | `9a271f2a916b0b6e` | 0 |
| `receipts/workflows/54280c94/docs__docs-gates-0__gate_15.log` | 1,911 | `fc9d5fa82e2f0bc0` | # head 54280c9408ba06a16fa925f85e0398a16f33777d workflow docs.yml job docs-gates-0 step gate_15: Milan feature-status... |
| `receipts/workflows/54280c94/docs__docs-gates-0__gate_15.rc` | 2 | `9a271f2a916b0b6e` | 0 |
| `receipts/workflows/54280c94/docs__docs-gates-0__gate_16.log` | 525 | `c7643c661b896794` | # head 54280c9408ba06a16fa925f85e0398a16f33777d workflow docs.yml job docs-gates-0 step gate_16: Traceability matrix ... |
| `receipts/workflows/54280c94/docs__docs-gates-0__gate_16.rc` | 2 | `9a271f2a916b0b6e` | 0 |
| `receipts/workflows/54280c94/docs__docs-gates-0__gate_18.log` | 3,017 | `38fb346748bac1bb` | # head 54280c9408ba06a16fa925f85e0398a16f33777d workflow docs.yml job docs-gates-0 step gate_18: Imported gPTP docume... |
| `receipts/workflows/54280c94/docs__docs-gates-0__gate_18.rc` | 2 | `9a271f2a916b0b6e` | 0 |
| `receipts/workflows/54280c94/docs__docs-gates-0__gate_19.log` | 3,702 | `0eab865d01954150` | # head 54280c9408ba06a16fa925f85e0398a16f33777d workflow docs.yml job docs-gates-0 step gate_19: Code-quality measure... |
| `receipts/workflows/54280c94/docs__docs-gates-0__gate_19.rc` | 2 | `9a271f2a916b0b6e` | 0 |
| `receipts/workflows/54280c94/docs__docs-gates-0__gate_21.log` | 510 | `5f9ea609fb69846b` | # head 54280c9408ba06a16fa925f85e0398a16f33777d workflow docs.yml job docs-gates-0 step gate_21: Bare-metal scope gate |
| `receipts/workflows/54280c94/docs__docs-gates-0__gate_21.rc` | 2 | `9a271f2a916b0b6e` | 0 |
| `receipts/workflows/54280c94/docs__docs-gates-0__gate_24.log` | 51,919 | `801ceaf6653b46d8` | # head 54280c9408ba06a16fa925f85e0398a16f33777d workflow docs.yml job docs-gates-0 step gate_24: Compiler-absent firm... |
| `receipts/workflows/54280c94/docs__docs-gates-0__gate_24.rc` | 2 | `9a271f2a916b0b6e` | 0 |
| `receipts/workflows/54280c94/docs__docs-gates-0__gate_26.log` | 12,701 | `3d944960304d33a6` | # head 54280c9408ba06a16fa925f85e0398a16f33777d workflow docs.yml job docs-gates-0 step gate_26: NVM record-space gate |
| `receipts/workflows/54280c94/docs__docs-gates-0__gate_26.rc` | 2 | `9a271f2a916b0b6e` | 0 |
| `receipts/workflows/54280c94/docs__docs-gates-0__gate_27.log` | 813 | `0545a9f2e3bab419` | # head 54280c9408ba06a16fa925f85e0398a16f33777d workflow docs.yml job docs-gates-0 step gate_27: Capture measurement ... |
| `receipts/workflows/54280c94/docs__docs-gates-0__gate_27.rc` | 2 | `9a271f2a916b0b6e` | 0 |
| `receipts/workflows/54280c94/docs__docs-gates-0__gate_28.log` | 26,548 | `095e1d18944eb362` | # head 54280c9408ba06a16fa925f85e0398a16f33777d workflow docs.yml job docs-gates-0 step gate_28: Saved-state writer gate |
| `receipts/workflows/54280c94/docs__docs-gates-0__gate_28.rc` | 2 | `9a271f2a916b0b6e` | 0 |
| `receipts/workflows/54280c94/docs__docs-gates-0__gate_29.log` | 5,231 | `27a15fb892a83a1b` | # head 54280c9408ba06a16fa925f85e0398a16f33777d workflow docs.yml job docs-gates-0 step gate_29: SoC source-list gate... |
| `receipts/workflows/54280c94/docs__docs-gates-0__gate_29.rc` | 2 | `9a271f2a916b0b6e` | 0 |
| `receipts/workflows/54280c94/docs__docs-gates-0__gate_30.log` | 3,853 | `153f950f4394422f` | # head 54280c9408ba06a16fa925f85e0398a16f33777d workflow docs.yml job docs-gates-0 step gate_30: RTL source-list drif... |
| `receipts/workflows/54280c94/docs__docs-gates-0__gate_30.rc` | 2 | `9a271f2a916b0b6e` | 0 |
| `receipts/workflows/54280c94/docs__docs-gates-0__gate_31.log` | 41,001 | `abba937014ffdbf8` | # head 54280c9408ba06a16fa925f85e0398a16f33777d workflow docs.yml job docs-gates-0 step gate_31: Boundary-unit naming... |
| `receipts/workflows/54280c94/docs__docs-gates-0__gate_31.rc` | 2 | `9a271f2a916b0b6e` | 0 |
| `receipts/workflows/54280c94/docs__docs-gates-0__gate_32.log` | 5,432 | `8c07a3ab1b29a87b` | # head 54280c9408ba06a16fa925f85e0398a16f33777d workflow docs.yml job docs-gates-0 step gate_32: Port contract gate |
| `receipts/workflows/54280c94/docs__docs-gates-0__gate_32.rc` | 2 | `9a271f2a916b0b6e` | 0 |
| `receipts/workflows/54280c94/docs__docs-gates-0__gate_33.log` | 12,977 | `56beabe82cc6654e` | # head 54280c9408ba06a16fa925f85e0398a16f33777d workflow docs.yml job docs-gates-0 step gate_33: Fail-fast ratchet |
| `receipts/workflows/54280c94/docs__docs-gates-0__gate_33.rc` | 2 | `9a271f2a916b0b6e` | 0 |
| `receipts/workflows/54280c94/docs__docs-gates-0__gate_34.log` | 3,138 | `75173e5f239b57e8` | # head 54280c9408ba06a16fa925f85e0398a16f33777d workflow docs.yml job docs-gates-0 step gate_34: TODO ownership gate |
| `receipts/workflows/54280c94/docs__docs-gates-0__gate_34.rc` | 2 | `9a271f2a916b0b6e` | 0 |
| `receipts/workflows/54280c94/docs__docs-gates-0__gate_35.log` | 29,179 | `48226fcd2117e649` | # head 54280c9408ba06a16fa925f85e0398a16f33777d workflow docs.yml job docs-gates-0 step gate_35: Test-evidence ratchet |
| `receipts/workflows/54280c94/docs__docs-gates-0__gate_35.rc` | 2 | `9a271f2a916b0b6e` | 0 |
| `receipts/workflows/54280c94/docs__docs-gates-0__gate_36.log` | 4,372 | `30ae23f2788dc282` | # head 54280c9408ba06a16fa925f85e0398a16f33777d workflow docs.yml job docs-gates-0 step gate_36: Mechanical hygiene r... |
| `receipts/workflows/54280c94/docs__docs-gates-0__gate_36.rc` | 2 | `9a271f2a916b0b6e` | 0 |
| `receipts/workflows/54280c94/docs__docs-gates-0__gate_37.log` | 3,571 | `24b90573a090141c` | # head 54280c9408ba06a16fa925f85e0398a16f33777d workflow docs.yml job docs-gates-0 step gate_37: SystemVerilog idiom ... |
| `receipts/workflows/54280c94/docs__docs-gates-0__gate_37.rc` | 2 | `9a271f2a916b0b6e` | 0 |
| `receipts/workflows/54280c94/docs__docs-gates-0__gate_38.log` | 4,303 | `ecda18976035d876` | # head 54280c9408ba06a16fa925f85e0398a16f33777d workflow docs.yml job docs-gates-0 step gate_38: C and C++ idiom gate |
| `receipts/workflows/54280c94/docs__docs-gates-0__gate_38.rc` | 2 | `9a271f2a916b0b6e` | 0 |
| `receipts/workflows/54280c94/docs__docs-gates-0__gate_39.log` | 3,383 | `c85c406c766aea39` | # head 54280c9408ba06a16fa925f85e0398a16f33777d workflow docs.yml job docs-gates-0 step gate_39: Python idiom gate |
| `receipts/workflows/54280c94/docs__docs-gates-0__gate_39.rc` | 2 | `9a271f2a916b0b6e` | 0 |
| `receipts/workflows/54280c94/docs__docs-gates-0__gate_40.log` | 3,086 | `db8215c5a7d2c278` | # head 54280c9408ba06a16fa925f85e0398a16f33777d workflow docs.yml job docs-gates-0 step gate_40: Shell idiom gate |
| `receipts/workflows/54280c94/docs__docs-gates-0__gate_40.rc` | 2 | `9a271f2a916b0b6e` | 0 |
| `receipts/workflows/54280c94/docs__docs-gates-0__gate_43.log` | 494 | `4e382ec6c950eceb` | # head 54280c9408ba06a16fa925f85e0398a16f33777d workflow docs.yml job docs-gates-0 step gate_43: Doc cited-path gate |
| `receipts/workflows/54280c94/docs__docs-gates-0__gate_43.rc` | 2 | `9a271f2a916b0b6e` | 0 |
| `receipts/workflows/54280c94/docs__docs-gates-0__gate_44.log` | 524 | `30c26532e60d4011` | # head 54280c9408ba06a16fa925f85e0398a16f33777d workflow docs.yml job docs-gates-0 step gate_44: Archive integrity gate |
| `receipts/workflows/54280c94/docs__docs-gates-0__gate_44.rc` | 2 | `9a271f2a916b0b6e` | 0 |
| `receipts/workflows/54280c94/docs__docs-gates-0__gate_45.log` | 592 | `6faf0e6666f7570a` | # head 54280c9408ba06a16fa925f85e0398a16f33777d workflow docs.yml job docs-gates-0 step gate_45: Per-page contents gate |
| `receipts/workflows/54280c94/docs__docs-gates-0__gate_45.rc` | 2 | `9a271f2a916b0b6e` | 0 |
| `receipts/workflows/54280c94/docs__docs-gates-0__gate_46.log` | 3,999 | `9f077ec59e27aed7` | # head 54280c9408ba06a16fa925f85e0398a16f33777d workflow docs.yml job docs-gates-0 step gate_46: AEM store generator ... |
| `receipts/workflows/54280c94/docs__docs-gates-0__gate_46.rc` | 2 | `9a271f2a916b0b6e` | 0 |
| `receipts/workflows/54280c94/docs__docs-gates-0__gate_47.log` | 20,278 | `c5789dc234c281b3` | # head 54280c9408ba06a16fa925f85e0398a16f33777d workflow docs.yml job docs-gates-0 step gate_47: Sweep/build shape gate |
| `receipts/workflows/54280c94/docs__docs-gates-0__gate_47.rc` | 2 | `9a271f2a916b0b6e` | 0 |
| `receipts/workflows/54280c94/docs__docs-gates-0__gate_48.log` | 9,761 | `bfc5837c3b915349` | # head 54280c9408ba06a16fa925f85e0398a16f33777d workflow docs.yml job docs-gates-0 step gate_48: Deploy shape gate |
| `receipts/workflows/54280c94/docs__docs-gates-0__gate_48.rc` | 2 | `9a271f2a916b0b6e` | 0 |
| `receipts/workflows/54280c94/docs__docs-gates-0__gate_49.log` | 28,163 | `27b5a0ca1dd5100d` | # head 54280c9408ba06a16fa925f85e0398a16f33777d workflow docs.yml job docs-gates-0 step gate_49: Entity shape gate |
| `receipts/workflows/54280c94/docs__docs-gates-0__gate_49.rc` | 2 | `9a271f2a916b0b6e` | 0 |
| `receipts/workflows/54280c94/docs__docs-gates-0__gate_50.log` | 136,196 | `93f3030abc93a4b6` | # head 54280c9408ba06a16fa925f85e0398a16f33777d workflow docs.yml job docs-gates-0 step gate_50: CI scheduling and ev... |
| `receipts/workflows/54280c94/docs__docs-gates-0__gate_50.rc` | 2 | `9a271f2a916b0b6e` | 0 |
| `receipts/workflows/54280c94/docs__docs-gates-0__gate_7.log` | 557 | `ae0af2e238e89b6b` | # head 54280c9408ba06a16fa925f85e0398a16f33777d workflow docs.yml job docs-gates-0 step gate_7: Link health, wording,... |
| `receipts/workflows/54280c94/docs__docs-gates-0__gate_7.rc` | 2 | `9a271f2a916b0b6e` | 0 |
| `receipts/workflows/54280c94/docs__docs-gates-0__gate_8.log` | 536 | `684bfaebc9021566` | # head 54280c9408ba06a16fa925f85e0398a16f33777d workflow docs.yml job docs-gates-0 step gate_8: Added-line em-dash gate |
| `receipts/workflows/54280c94/docs__docs-gates-0__gate_8.rc` | 2 | `9a271f2a916b0b6e` | 0 |
| `receipts/workflows/54280c94/docs__docs-gates-0__gate_9.log` | 575 | `6ac4f1e659d2ecec` | # head 54280c9408ba06a16fa925f85e0398a16f33777d workflow docs.yml job docs-gates-0 step gate_9: Concise audience docu... |
| `receipts/workflows/54280c94/docs__docs-gates-0__gate_9.rc` | 2 | `9a271f2a916b0b6e` | 0 |
| `receipts/workflows/54280c94/docs__docs-gates-0__tree-after.txt` | 55 | `3207e94684ec1a27` | head 54280c9408ba06a16fa925f85e0398a16f33777d |
| `receipts/workflows/54280c94/docs__docs-gates-1__DONE` | 9 | `fab506c9d858683b` | failed 0 |
| `receipts/workflows/54280c94/docs__docs-gates-1__ci_step_1.log` | 403 | `ba68e49947f73b66` | # head 54280c9408ba06a16fa925f85e0398a16f33777d workflow docs.yml job docs-gates-1 step ci_step_1: Set CPU-derived jo... |
| `receipts/workflows/54280c94/docs__docs-gates-1__ci_step_1.rc` | 2 | `9a271f2a916b0b6e` | 0 |
| `receipts/workflows/54280c94/docs__docs-gates-1__ci_step_3.log` | 523 | `013f34c9526a0713` | # head 54280c9408ba06a16fa925f85e0398a16f33777d workflow docs.yml job docs-gates-1 step ci_step_3: Install the python... |
| `receipts/workflows/54280c94/docs__docs-gates-1__ci_step_3.rc` | 2 | `9a271f2a916b0b6e` | 0 |
| `receipts/workflows/54280c94/docs__docs-gates-1__ci_step_5.log` | 523 | `aa7231ebe27ca3bc` | # head 54280c9408ba06a16fa925f85e0398a16f33777d workflow docs.yml job docs-gates-1 step ci_step_5: Install the pinned... |
| `receipts/workflows/54280c94/docs__docs-gates-1__ci_step_5.rc` | 2 | `9a271f2a916b0b6e` | 0 |
| `receipts/workflows/54280c94/docs__docs-gates-1__ci_step_9.log` | 1,062 | `6449a45353441b3b` | # head 54280c9408ba06a16fa925f85e0398a16f33777d workflow docs.yml job docs-gates-1 step ci_step_9: Fetch the builder ... |
| `receipts/workflows/54280c94/docs__docs-gates-1__ci_step_9.rc` | 2 | `9a271f2a916b0b6e` | 0 |
| `receipts/workflows/54280c94/docs__docs-gates-1__gate_25_0.log` | 50,941 | `a6b28b5e5f3c10fe` | # head 54280c9408ba06a16fa925f85e0398a16f33777d workflow docs.yml job docs-gates-1 step gate_25_0: End-station builde... |
| `receipts/workflows/54280c94/docs__docs-gates-1__gate_25_0.rc` | 2 | `9a271f2a916b0b6e` | 0 |
| `receipts/workflows/54280c94/docs__docs-gates-1__tree-after.txt` | 55 | `3207e94684ec1a27` | head 54280c9408ba06a16fa925f85e0398a16f33777d |
| `receipts/workflows/54280c94/docs__docs-gates-2__DONE` | 9 | `fab506c9d858683b` | failed 0 |
| `receipts/workflows/54280c94/docs__docs-gates-2__ci_step_1.log` | 403 | `12fa8d9275b23390` | # head 54280c9408ba06a16fa925f85e0398a16f33777d workflow docs.yml job docs-gates-2 step ci_step_1: Set CPU-derived jo... |
| `receipts/workflows/54280c94/docs__docs-gates-2__ci_step_1.rc` | 2 | `9a271f2a916b0b6e` | 0 |
| `receipts/workflows/54280c94/docs__docs-gates-2__ci_step_3.log` | 523 | `f70f945779ec3d85` | # head 54280c9408ba06a16fa925f85e0398a16f33777d workflow docs.yml job docs-gates-2 step ci_step_3: Install the python... |
| `receipts/workflows/54280c94/docs__docs-gates-2__ci_step_3.rc` | 2 | `9a271f2a916b0b6e` | 0 |
| `receipts/workflows/54280c94/docs__docs-gates-2__ci_step_5.log` | 523 | `d8eb45bcb4fe39ff` | # head 54280c9408ba06a16fa925f85e0398a16f33777d workflow docs.yml job docs-gates-2 step ci_step_5: Install the pinned... |
| `receipts/workflows/54280c94/docs__docs-gates-2__ci_step_5.rc` | 2 | `9a271f2a916b0b6e` | 0 |
| `receipts/workflows/54280c94/docs__docs-gates-2__ci_step_9.log` | 1,062 | `e531779c730eef53` | # head 54280c9408ba06a16fa925f85e0398a16f33777d workflow docs.yml job docs-gates-2 step ci_step_9: Fetch the builder ... |
| `receipts/workflows/54280c94/docs__docs-gates-2__ci_step_9.rc` | 2 | `9a271f2a916b0b6e` | 0 |
| `receipts/workflows/54280c94/docs__docs-gates-2__gate_25_1.log` | 76,638 | `3958b885361537c9` | # head 54280c9408ba06a16fa925f85e0398a16f33777d workflow docs.yml job docs-gates-2 step gate_25_1: End-station builde... |
| `receipts/workflows/54280c94/docs__docs-gates-2__gate_25_1.rc` | 2 | `9a271f2a916b0b6e` | 0 |
| `receipts/workflows/54280c94/docs__docs-gates-2__gate_41.excerpt.txt` | 7,465 | `7106d10823ad84d9` | # excerpt of docs__docs-gates-2__gate_41.log (350,407 B, 5,475 lines, sha256 in large-files.sha256): its first 30 and... |
| `receipts/workflows/54280c94/docs__docs-gates-2__gate_41.rc` | 2 | `9a271f2a916b0b6e` | 0 |
| `receipts/workflows/54280c94/docs__docs-gates-2__gate_42.log` | 124,011 | `ee4ab94faf7c2aa5` | # head 54280c9408ba06a16fa925f85e0398a16f33777d workflow docs.yml job docs-gates-2 step gate_42: Local act runner con... |
| `receipts/workflows/54280c94/docs__docs-gates-2__gate_42.rc` | 2 | `9a271f2a916b0b6e` | 0 |
| `receipts/workflows/54280c94/docs__docs-gates-2__tree-after.txt` | 55 | `3207e94684ec1a27` | head 54280c9408ba06a16fa925f85e0398a16f33777d |
| `receipts/workflows/54280c94/docs__wire-accountability__DONE` | 9 | `fab506c9d858683b` | failed 0 |
| `receipts/workflows/54280c94/docs__wire-accountability__ci_step_1.log` | 417 | `7468488f48136b14` | # head 54280c9408ba06a16fa925f85e0398a16f33777d workflow docs.yml job wire-accountability step ci_step_1: Set CPU-der... |
| `receipts/workflows/54280c94/docs__wire-accountability__ci_step_1.rc` | 2 | `9a271f2a916b0b6e` | 0 |
| `receipts/workflows/54280c94/docs__wire-accountability__ci_step_3.log` | 655 | `f05dfbff7a72a58b` | # head 54280c9408ba06a16fa925f85e0398a16f33777d workflow docs.yml job wire-accountability step ci_step_3: Fetch the e... |
| `receipts/workflows/54280c94/docs__wire-accountability__ci_step_3.rc` | 2 | `9a271f2a916b0b6e` | 0 |
| `receipts/workflows/54280c94/docs__wire-accountability__ci_step_4.log` | 5,526 | `3d5ddbff71a9d2e0` | # head 54280c9408ba06a16fa925f85e0398a16f33777d workflow docs.yml job wire-accountability step ci_step_4: Advertised-... |
| `receipts/workflows/54280c94/docs__wire-accountability__ci_step_4.rc` | 2 | `9a271f2a916b0b6e` | 0 |
| `receipts/workflows/54280c94/docs__wire-accountability__tree-after.txt` | 55 | `3207e94684ec1a27` | head 54280c9408ba06a16fa925f85e0398a16f33777d |
| `receipts/workflows/54280c94/elaborate-gates-1-without-the-litex-venv/elaborate__elaborate-gates-1__DONE` | 9 | `4329c55ea796458a` | failed 2 |
| `receipts/workflows/54280c94/elaborate-gates-1-without-the-litex-venv/elaborate__elaborate-gates-1__ci_step_1.log` | 423 | `d26bb76974f10639` | # head 54280c9408ba06a16fa925f85e0398a16f33777d workflow elaborate.yml job elaborate-gates-1 step ci_step_1: Set CPU-... |
| `receipts/workflows/54280c94/elaborate-gates-1-without-the-litex-venv/elaborate__elaborate-gates-1__ci_step_1.rc` | 2 | `9a271f2a916b0b6e` | 0 |
| `receipts/workflows/54280c94/elaborate-gates-1-without-the-litex-venv/elaborate__elaborate-gates-1__ci_step_23.log` | 587 | `1b3eb526ec1af6d7` | # head 54280c9408ba06a16fa925f85e0398a16f33777d workflow elaborate.yml job elaborate-gates-1 step ci_step_23: Put Ver... |
| `receipts/workflows/54280c94/elaborate-gates-1-without-the-litex-venv/elaborate__elaborate-gates-1__ci_step_23.rc` | 2 | `9a271f2a916b0b6e` | 0 |
| `receipts/workflows/54280c94/elaborate-gates-1-without-the-litex-venv/elaborate__elaborate-gates-1__ci_step_4.log` | 1,126 | `524efaaed880ba58` | # head 54280c9408ba06a16fa925f85e0398a16f33777d workflow elaborate.yml job elaborate-gates-1 step ci_step_4: Fetch th... |
| `receipts/workflows/54280c94/elaborate-gates-1-without-the-litex-venv/elaborate__elaborate-gates-1__ci_step_4.rc` | 2 | `9a271f2a916b0b6e` | 0 |
| `receipts/workflows/54280c94/elaborate-gates-1-without-the-litex-venv/elaborate__elaborate-gates-1__gate_15_1.log` | 81,646 | `3342276ecde461c0` | # head 54280c9408ba06a16fa925f85e0398a16f33777d workflow elaborate.yml job elaborate-gates-1 step gate_15_1: Elaborat... |
| `receipts/workflows/54280c94/elaborate-gates-1-without-the-litex-venv/elaborate__elaborate-gates-1__gate_15_1.rc` | 2 | `4355a46b19d348dc` | 1 |
| `receipts/workflows/54280c94/elaborate-gates-1-without-the-litex-venv/elaborate__elaborate-gates-1__gate_19.log` | 3,145 | `0e44bda0ecc58f52` | # head 54280c9408ba06a16fa925f85e0398a16f33777d workflow elaborate.yml job elaborate-gates-1 step gate_19: Standalone... |
| `receipts/workflows/54280c94/elaborate-gates-1-without-the-litex-venv/elaborate__elaborate-gates-1__gate_19.rc` | 3 | `4393447bd3c1d55e` | 90 |
| `receipts/workflows/54280c94/elaborate-gates-1-without-the-litex-venv/elaborate__elaborate-gates-1__scope.log` | 18,320 | `bf3c33e5001b8210` | # head 54280c9408ba06a16fa925f85e0398a16f33777d workflow elaborate.yml job elaborate-gates-1 step scope: Decide wheth... |
| `receipts/workflows/54280c94/elaborate-gates-1-without-the-litex-venv/elaborate__elaborate-gates-1__scope.rc` | 2 | `9a271f2a916b0b6e` | 0 |
| `receipts/workflows/54280c94/elaborate-gates-1-without-the-litex-venv/elaborate__elaborate-gates-1__tree-after.txt` | 55 | `3207e94684ec1a27` | head 54280c9408ba06a16fa925f85e0398a16f33777d |
| `receipts/workflows/54280c94/elaborate__elaborate-gates-0__DONE` | 9 | `fab506c9d858683b` | failed 0 |
| `receipts/workflows/54280c94/elaborate__elaborate-gates-0__ci_step_1.log` | 423 | `d89e2f851d2dcccc` | # head 54280c9408ba06a16fa925f85e0398a16f33777d workflow elaborate.yml job elaborate-gates-0 step ci_step_1: Set CPU-... |
| `receipts/workflows/54280c94/elaborate__elaborate-gates-0__ci_step_1.rc` | 2 | `9a271f2a916b0b6e` | 0 |
| `receipts/workflows/54280c94/elaborate__elaborate-gates-0__ci_step_4.log` | 1,126 | `a9158be5a3f2a44b` | # head 54280c9408ba06a16fa925f85e0398a16f33777d workflow elaborate.yml job elaborate-gates-0 step ci_step_4: Fetch th... |
| `receipts/workflows/54280c94/elaborate__elaborate-gates-0__ci_step_4.rc` | 2 | `9a271f2a916b0b6e` | 0 |
| `receipts/workflows/54280c94/elaborate__elaborate-gates-0__gate_15_0.log` | 51,069 | `655e8a19b6ddf530` | # head 54280c9408ba06a16fa925f85e0398a16f33777d workflow elaborate.yml job elaborate-gates-0 step gate_15_0: Elaborat... |
| `receipts/workflows/54280c94/elaborate__elaborate-gates-0__gate_15_0.rc` | 2 | `9a271f2a916b0b6e` | 0 |
| `receipts/workflows/54280c94/elaborate__elaborate-gates-0__scope.log` | 18,320 | `b99289c6a7b3b2ba` | # head 54280c9408ba06a16fa925f85e0398a16f33777d workflow elaborate.yml job elaborate-gates-0 step scope: Decide wheth... |
| `receipts/workflows/54280c94/elaborate__elaborate-gates-0__scope.rc` | 2 | `9a271f2a916b0b6e` | 0 |
| `receipts/workflows/54280c94/elaborate__elaborate-gates-0__tree-after.txt` | 55 | `3207e94684ec1a27` | head 54280c9408ba06a16fa925f85e0398a16f33777d |
| `receipts/workflows/54280c94/elaborate__elaborate-gates-1__DONE` | 9 | `fab506c9d858683b` | failed 0 |
| `receipts/workflows/54280c94/elaborate__elaborate-gates-1__ci_step_1.log` | 420 | `e046d5ac479e11a5` | # head 54280c9408ba06a16fa925f85e0398a16f33777d workflow elaborate.yml job elaborate-gates-1 step ci_step_1: Set CPU-... |
| `receipts/workflows/54280c94/elaborate__elaborate-gates-1__ci_step_1.rc` | 2 | `9a271f2a916b0b6e` | 0 |
| `receipts/workflows/54280c94/elaborate__elaborate-gates-1__ci_step_23.log` | 584 | `7962ae488579f64a` | # head 54280c9408ba06a16fa925f85e0398a16f33777d workflow elaborate.yml job elaborate-gates-1 step ci_step_23: Put Ver... |
| `receipts/workflows/54280c94/elaborate__elaborate-gates-1__ci_step_23.rc` | 2 | `9a271f2a916b0b6e` | 0 |
| `receipts/workflows/54280c94/elaborate__elaborate-gates-1__ci_step_4.log` | 1,123 | `acfaacddac8a286e` | # head 54280c9408ba06a16fa925f85e0398a16f33777d workflow elaborate.yml job elaborate-gates-1 step ci_step_4: Fetch th... |
| `receipts/workflows/54280c94/elaborate__elaborate-gates-1__ci_step_4.rc` | 2 | `9a271f2a916b0b6e` | 0 |
| `receipts/workflows/54280c94/elaborate__elaborate-gates-1__gate_15_1.log` | 84,556 | `56f376acf77e68b8` | # head 54280c9408ba06a16fa925f85e0398a16f33777d workflow elaborate.yml job elaborate-gates-1 step gate_15_1: Elaborat... |
| `receipts/workflows/54280c94/elaborate__elaborate-gates-1__gate_15_1.rc` | 2 | `9a271f2a916b0b6e` | 0 |
| `receipts/workflows/54280c94/elaborate__elaborate-gates-1__gate_19.log` | 1,671 | `355bebd5435ed339` | # head 54280c9408ba06a16fa925f85e0398a16f33777d workflow elaborate.yml job elaborate-gates-1 step gate_19: Standalone... |
| `receipts/workflows/54280c94/elaborate__elaborate-gates-1__gate_19.rc` | 2 | `9a271f2a916b0b6e` | 0 |
| `receipts/workflows/54280c94/elaborate__elaborate-gates-1__scope.log` | 18,317 | `f3e531a313edb337` | # head 54280c9408ba06a16fa925f85e0398a16f33777d workflow elaborate.yml job elaborate-gates-1 step scope: Decide wheth... |
| `receipts/workflows/54280c94/elaborate__elaborate-gates-1__scope.rc` | 2 | `9a271f2a916b0b6e` | 0 |
| `receipts/workflows/54280c94/elaborate__elaborate-gates-1__tree-after.txt` | 55 | `3207e94684ec1a27` | head 54280c9408ba06a16fa925f85e0398a16f33777d |
| `receipts/workflows/54280c94/elaborate__elaborate__DONE` | 9 | `fab506c9d858683b` | failed 0 |
| `receipts/workflows/54280c94/elaborate__elaborate__tree-after.txt` | 55 | `3207e94684ec1a27` | head 54280c9408ba06a16fa925f85e0398a16f33777d |
| `receipts/workflows/54280c94/rtl-fast__firmware-boundary__DONE` | 9 | `fab506c9d858683b` | failed 0 |
| `receipts/workflows/54280c94/rtl-fast__firmware-boundary__ci_step_1.log` | 418 | `97f4bbf5b537a9dc` | # head 54280c9408ba06a16fa925f85e0398a16f33777d workflow rtl-fast.yml job firmware-boundary step ci_step_1: Set CPU-d... |
| `receipts/workflows/54280c94/rtl-fast__firmware-boundary__ci_step_1.rc` | 2 | `9a271f2a916b0b6e` | 0 |
| `receipts/workflows/54280c94/rtl-fast__firmware-boundary__ci_step_3.log` | 1,545 | `3c89e47290a77a23` | # head 54280c9408ba06a16fa925f85e0398a16f33777d workflow rtl-fast.yml job firmware-boundary step ci_step_3: Fetch RTL... |
| `receipts/workflows/54280c94/rtl-fast__firmware-boundary__ci_step_3.rc` | 2 | `9a271f2a916b0b6e` | 0 |
| `receipts/workflows/54280c94/rtl-fast__firmware-boundary__ci_step_9.log` | 71,171 | `aa2e55d76202b5af` | # head 54280c9408ba06a16fa925f85e0398a16f33777d workflow rtl-fast.yml job firmware-boundary step ci_step_9: Hold the ... |
| `receipts/workflows/54280c94/rtl-fast__firmware-boundary__ci_step_9.rc` | 2 | `9a271f2a916b0b6e` | 0 |
| `receipts/workflows/54280c94/rtl-fast__firmware-boundary__tree-after.txt` | 55 | `3207e94684ec1a27` | head 54280c9408ba06a16fa925f85e0398a16f33777d |
| `receipts/workflows/f1f7c3e8/batch-a.txt` | 1,631 | `08d5b8d68aaa53c9` | 03:48:52 start rtl-fast.yml firmware-unit |
| `receipts/workflows/f1f7c3e8/rtl-fast__changes__DONE` | 9 | `fab506c9d858683b` | failed 0 |
| `receipts/workflows/f1f7c3e8/rtl-fast__changes__ci_step_1.log` | 251 | `c7f45a4ce9de0d46` | # head f1f7c3e8fae905b7cf9cb0524063719ab2f331a7 workflow rtl-fast.yml job changes step ci_step_1: Set CPU-derived job... |
| `receipts/workflows/f1f7c3e8/rtl-fast__changes__ci_step_1.rc` | 2 | `9a271f2a916b0b6e` | 0 |
| `receipts/workflows/f1f7c3e8/rtl-fast__changes__scope.log` | 18,228 | `ecb35a77c6d9e3f3` | # head f1f7c3e8fae905b7cf9cb0524063719ab2f331a7 workflow rtl-fast.yml job changes step scope: Classify the change con... |
| `receipts/workflows/f1f7c3e8/rtl-fast__changes__scope.rc` | 2 | `9a271f2a916b0b6e` | 0 |
| `receipts/workflows/f1f7c3e8/rtl-fast__changes__tree-after.txt` | 55 | `911700cdc8884560` | head f1f7c3e8fae905b7cf9cb0524063719ab2f331a7 |
| `receipts/workflows/f1f7c3e8/rtl-fast__firmware-aecp-mutants__DONE` | 9 | `fab506c9d858683b` | failed 0 |
| `receipts/workflows/f1f7c3e8/rtl-fast__firmware-aecp-mutants__ci_step_1.log` | 429 | `fed6e4fe803e47dc` | # head f1f7c3e8fae905b7cf9cb0524063719ab2f331a7 workflow rtl-fast.yml job firmware-aecp-mutants step ci_step_1: Set C... |
| `receipts/workflows/f1f7c3e8/rtl-fast__firmware-aecp-mutants__ci_step_1.rc` | 2 | `9a271f2a916b0b6e` | 0 |
| `receipts/workflows/f1f7c3e8/rtl-fast__firmware-aecp-mutants__ci_step_3.log` | 1,576 | `22d92b71decaf38b` | # head f1f7c3e8fae905b7cf9cb0524063719ab2f331a7 workflow rtl-fast.yml job firmware-aecp-mutants step ci_step_3: Fetch... |
| `receipts/workflows/f1f7c3e8/rtl-fast__firmware-aecp-mutants__ci_step_3.rc` | 2 | `9a271f2a916b0b6e` | 0 |
| `receipts/workflows/f1f7c3e8/rtl-fast__firmware-aecp-mutants__ci_step_9.excerpt.txt` | 19,775 | `098115e12cc3b21d` | # excerpt of rtl-fast__firmware-aecp-mutants__ci_step_9.log (237,320 B, 1,190 lines, sha256 in large-files.sha256): i... |
| `receipts/workflows/f1f7c3e8/rtl-fast__firmware-aecp-mutants__ci_step_9.rc` | 2 | `9a271f2a916b0b6e` | 0 |
| `receipts/workflows/f1f7c3e8/rtl-fast__firmware-aecp-mutants__tree-after.txt` | 73 | `be479795a3022a03` | head f1f7c3e8fae905b7cf9cb0524063719ab2f331a7 |
| `receipts/workflows/f1f7c3e8/rtl-fast__firmware-control-mutants__DONE` | 9 | `fab506c9d858683b` | failed 0 |
| `receipts/workflows/f1f7c3e8/rtl-fast__firmware-control-mutants__ci_step_1.log` | 435 | `0093e6f16124ca4a` | # head f1f7c3e8fae905b7cf9cb0524063719ab2f331a7 workflow rtl-fast.yml job firmware-control-mutants step ci_step_1: Se... |
| `receipts/workflows/f1f7c3e8/rtl-fast__firmware-control-mutants__ci_step_1.rc` | 2 | `9a271f2a916b0b6e` | 0 |
| `receipts/workflows/f1f7c3e8/rtl-fast__firmware-control-mutants__ci_step_3.log` | 1,597 | `a0e28dd73cdb7ec2` | # head f1f7c3e8fae905b7cf9cb0524063719ab2f331a7 workflow rtl-fast.yml job firmware-control-mutants step ci_step_3: Fe... |
| `receipts/workflows/f1f7c3e8/rtl-fast__firmware-control-mutants__ci_step_3.rc` | 2 | `9a271f2a916b0b6e` | 0 |
| `receipts/workflows/f1f7c3e8/rtl-fast__firmware-control-mutants__ci_step_9.log` | 136,420 | `41ad44eedc627b3a` | # head f1f7c3e8fae905b7cf9cb0524063719ab2f331a7 workflow rtl-fast.yml job firmware-control-mutants step ci_step_9: Ru... |
| `receipts/workflows/f1f7c3e8/rtl-fast__firmware-control-mutants__ci_step_9.rc` | 2 | `9a271f2a916b0b6e` | 0 |
| `receipts/workflows/f1f7c3e8/rtl-fast__firmware-control-mutants__tree-after.txt` | 73 | `be479795a3022a03` | head f1f7c3e8fae905b7cf9cb0524063719ab2f331a7 |
| `receipts/workflows/f1f7c3e8/rtl-fast__firmware-srp-mutants__DONE` | 9 | `fab506c9d858683b` | failed 0 |
| `receipts/workflows/f1f7c3e8/rtl-fast__firmware-srp-mutants__ci_step_1.log` | 427 | `5fc94906e999fbe2` | # head f1f7c3e8fae905b7cf9cb0524063719ab2f331a7 workflow rtl-fast.yml job firmware-srp-mutants step ci_step_1: Set CP... |
| `receipts/workflows/f1f7c3e8/rtl-fast__firmware-srp-mutants__ci_step_1.rc` | 2 | `9a271f2a916b0b6e` | 0 |
| `receipts/workflows/f1f7c3e8/rtl-fast__firmware-srp-mutants__ci_step_3.log` | 1,569 | `21d3dbda2ee3e0ea` | # head f1f7c3e8fae905b7cf9cb0524063719ab2f331a7 workflow rtl-fast.yml job firmware-srp-mutants step ci_step_3: Fetch ... |
| `receipts/workflows/f1f7c3e8/rtl-fast__firmware-srp-mutants__ci_step_3.rc` | 2 | `9a271f2a916b0b6e` | 0 |
| `receipts/workflows/f1f7c3e8/rtl-fast__firmware-srp-mutants__ci_step_9.excerpt.txt` | 15,182 | `2a139a3689c4441c` | # excerpt of rtl-fast__firmware-srp-mutants__ci_step_9.log (232,405 B, 1,152 lines, sha256 in large-files.sha256): it... |
| `receipts/workflows/f1f7c3e8/rtl-fast__firmware-srp-mutants__ci_step_9.rc` | 2 | `9a271f2a916b0b6e` | 0 |
| `receipts/workflows/f1f7c3e8/rtl-fast__firmware-srp-mutants__tree-after.txt` | 73 | `be479795a3022a03` | head f1f7c3e8fae905b7cf9cb0524063719ab2f331a7 |
| `receipts/workflows/f1f7c3e8/rtl-fast__firmware-unit__DONE` | 9 | `fab506c9d858683b` | failed 0 |
| `receipts/workflows/f1f7c3e8/rtl-fast__firmware-unit__ci_step_1.log` | 413 | `7fd5492f4b946d21` | # head f1f7c3e8fae905b7cf9cb0524063719ab2f331a7 workflow rtl-fast.yml job firmware-unit step ci_step_1: Set CPU-deriv... |
| `receipts/workflows/f1f7c3e8/rtl-fast__firmware-unit__ci_step_1.rc` | 2 | `9a271f2a916b0b6e` | 0 |
| `receipts/workflows/f1f7c3e8/rtl-fast__firmware-unit__ci_step_10.log` | 96,331 | `e8232c45e6f5bd99` | # head f1f7c3e8fae905b7cf9cb0524063719ab2f331a7 workflow rtl-fast.yml job firmware-unit step ci_step_10: Run the cont... |
| `receipts/workflows/f1f7c3e8/rtl-fast__firmware-unit__ci_step_10.rc` | 2 | `9a271f2a916b0b6e` | 0 |
| `receipts/workflows/f1f7c3e8/rtl-fast__firmware-unit__ci_step_11.log` | 5,260 | `082eef29f9a03e43` | # head f1f7c3e8fae905b7cf9cb0524063719ab2f331a7 workflow rtl-fast.yml job firmware-unit step ci_step_11: Run the save... |
| `receipts/workflows/f1f7c3e8/rtl-fast__firmware-unit__ci_step_11.rc` | 2 | `9a271f2a916b0b6e` | 0 |
| `receipts/workflows/f1f7c3e8/rtl-fast__firmware-unit__ci_step_12.log` | 9,548 | `8da1cef4a73568db` | # head f1f7c3e8fae905b7cf9cb0524063719ab2f331a7 workflow rtl-fast.yml job firmware-unit step ci_step_12: Hold the fir... |
| `receipts/workflows/f1f7c3e8/rtl-fast__firmware-unit__ci_step_12.rc` | 2 | `9a271f2a916b0b6e` | 0 |
| `receipts/workflows/f1f7c3e8/rtl-fast__firmware-unit__ci_step_3.log` | 1,520 | `6c8bbf8995190c4d` | # head f1f7c3e8fae905b7cf9cb0524063719ab2f331a7 workflow rtl-fast.yml job firmware-unit step ci_step_3: Fetch RTL dep... |
| `receipts/workflows/f1f7c3e8/rtl-fast__firmware-unit__ci_step_3.rc` | 2 | `9a271f2a916b0b6e` | 0 |
| `receipts/workflows/f1f7c3e8/rtl-fast__firmware-unit__ci_step_7.log` | 2,421 | `466f00bc9a4f53c5` | # head f1f7c3e8fae905b7cf9cb0524063719ab2f331a7 workflow rtl-fast.yml job firmware-unit step ci_step_7: Prove the tal... |
| `receipts/workflows/f1f7c3e8/rtl-fast__firmware-unit__ci_step_7.rc` | 2 | `9a271f2a916b0b6e` | 0 |
| `receipts/workflows/f1f7c3e8/rtl-fast__firmware-unit__tree-after.txt` | 73 | `be479795a3022a03` | head f1f7c3e8fae905b7cf9cb0524063719ab2f331a7 |
| `receipts/workflows/f1f7c3e8/rtl-fast__firmware-verilator__DONE` | 9 | `fab506c9d858683b` | failed 0 |
| `receipts/workflows/f1f7c3e8/rtl-fast__firmware-verilator__ci_step_1.log` | 423 | `445735c5d2e1fe42` | # head f1f7c3e8fae905b7cf9cb0524063719ab2f331a7 workflow rtl-fast.yml job firmware-verilator step ci_step_1: Set CPU-... |
| `receipts/workflows/f1f7c3e8/rtl-fast__firmware-verilator__ci_step_1.rc` | 2 | `9a271f2a916b0b6e` | 0 |
| `receipts/workflows/f1f7c3e8/rtl-fast__firmware-verilator__ci_step_11.log` | 587 | `74a6e7c4db250c3c` | # head f1f7c3e8fae905b7cf9cb0524063719ab2f331a7 workflow rtl-fast.yml job firmware-verilator step ci_step_11: Put Ver... |
| `receipts/workflows/f1f7c3e8/rtl-fast__firmware-verilator__ci_step_11.rc` | 2 | `9a271f2a916b0b6e` | 0 |
| `receipts/workflows/f1f7c3e8/rtl-fast__firmware-verilator__ci_step_14.log` | 60,839 | `4499a2e3feeadc67` | # head f1f7c3e8fae905b7cf9cb0524063719ab2f331a7 workflow rtl-fast.yml job firmware-verilator step ci_step_14: Hold th... |
| `receipts/workflows/f1f7c3e8/rtl-fast__firmware-verilator__ci_step_14.rc` | 2 | `9a271f2a916b0b6e` | 0 |
| `receipts/workflows/f1f7c3e8/rtl-fast__firmware-verilator__ci_step_3.log` | 1,555 | `476e93861380a8bd` | # head f1f7c3e8fae905b7cf9cb0524063719ab2f331a7 workflow rtl-fast.yml job firmware-verilator step ci_step_3: Fetch RT... |
| `receipts/workflows/f1f7c3e8/rtl-fast__firmware-verilator__ci_step_3.rc` | 2 | `9a271f2a916b0b6e` | 0 |
| `receipts/workflows/f1f7c3e8/rtl-fast__firmware-verilator__tree-after.txt` | 55 | `911700cdc8884560` | head f1f7c3e8fae905b7cf9cb0524063719ab2f331a7 |
| `receipts/workflows/not_run.json` | 32,455 | `921191ef4a187d52` | { |
| `receipts/workflows/not_run_920.json` | 1,267 | `b02c56a11ea26bfc` | { |
| `receipts/workflows/not_run_920_5428.json` | 1,958 | `94f90fc2d4aad08d` | { |
| `receipts/workflows/not_run_920_f1f7.json` | 1,379 | `9f9f7bf2646b8ad0` | { |
| `receipts/workflows/verify-docs-54280c94.md` | 12,355 | `a76f368242088d10` | \| Workflow \| Job \| Step \| Name \| rc \| Log or reason \| |
| `receipts/workflows/verify-elaborate-54280c94.md` | 8,428 | `85009e5008dc1061` | \| Workflow \| Job \| Step \| Name \| rc \| Log or reason \| |
| `receipts/workflows/verify-rtl-fast-54280c94.md` | 22,093 | `0b14c6cfaefe35f8` | \| Workflow \| Job \| Step \| Name \| rc \| Log or reason \| |
| `receipts/workflows/verify-rtl-fast-f1f7c3e8.md` | 21,403 | `b1805f47bdac647d` | \| Workflow \| Job \| Step \| Name \| rc \| Log or reason \| |
