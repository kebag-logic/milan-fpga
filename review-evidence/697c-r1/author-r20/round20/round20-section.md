## Round 20

**REVIEW READY locally at `d40e4e9827be2516f8f34b9d65f0a483fff2194c`**, on `697-consume`. The clean resumed head was `97e713168470bfae2685521fa557dc462b782b32`. Origin was verified as the assigned public repository. `git fetch origin dev` yielded `e81ce82f9aa3e4dcaffa5bcdf7e60f0c7cffd80c`; its no-fast-forward merge is `a71b0e4149c26576499d05cacf2fa6fbfe27fb15`. There were no textual conflicts. The implementation is the single following commit, `d40e4e982`. Both subjects are one line with no body or trailers. No push, PR edit, rebase, amend, merge to dev or hardware operation was performed.

Authority: [Round 20 assignment](https://github.com/kebag-logic/milan-fpga/issues/697#issuecomment-6140933191), [composition review R584-18](https://github.com/kebag-logic/milan-fpga/pull/705#issuecomment-6139118335), #726 / PR #729, and #697 acceptance items 1–5 with its recorded pin rulings. This is implementation evidence; a new independent verdict and protected hosted contexts are still required.

### Changed files and classification

| File:line | Change and purpose |
|---|---|
| `tb/verilator/milan_dp/stream_counter_f5.py:40` | Adds --stack and build-only; shared pin verification runs before any staging or compilation. Build-only retains the same compile/link path and runs no tests or plants. |
| `sw/firmware/ctrl/test/ctrl_configs.py:122` | Registers both F5 shapes as the sixth mandatory independent capture. The Makefile classification states precisely that its firmware recipes delegate to that separately captured program. |
| `sw/firmware/ctrl/test/ctrl_plants.py:193` | Removing the F5 entry or its own capture is refused by name; neither can be covered accidentally by another builder. |
| `tb/verilator/milan_dp/Makefile:545` | Pins the aggregate run before compilation; counters, counters-f5 and counters-mutants each require stack-pin. F5 recipes forward STACK_DIR. |
| `sw/firmware/ctrl/test/ctrl_pin.py:695` | Census requires all three counter prerequisites, including the RTL-only counters entry. Four F5 dirty/off-pin arms cover direct execution and build-only. |
| `sw/firmware/ctrl/test/ctrl_pin_bench.py:11` | Moves the existing bench-control helper intact, then adds prerequisite-removal plants for the three counter entries; preserves the Python size ratchet. |
| `sw/firmware/ctrl/README.md:126` | Documents six captures, 103 boundary defects and 120 pin controls, including F5 and counter entry points. |
| `docs/testing/CI_WORKFLOWS.md:80` | Documents the mandatory two-shape F5 build-only capture in the existing firmware-boundary job; no workflow step is dropped or duplicated. |

F5 compiles the AECP core, mailbox adapter, mailbox/loop support and its test fixture against public stack headers. Its two independent runs recorded 30 compiler invocations containing 28 compiled sources, all rc 0. Both shape runs are attributed to F5 itself. The full boundary judges them along with the other five captures. The classification does not claim the Makefile compiles nothing: its own direct compiler recipes build RTL harnesses and its firmware build delegates to F5.

The assignment names `counters` and `counters-f5`; the actual Makefile also invokes F5 from `counters-mutants`. All three are pinned. `counters` is RTL-only, so an explicit census rule and a prerequisite-removal plant prevent its promised pin check becoming accidental. `run` is also pinned first so aggregate entry controls refuse before compiling. All these negative checks name the modified stack file rather than relying on a compiler failure.

R584-18-F1: the held-text probe reports zero program refusals; removing either F5 classification or its independent capture is caught. R584-18-F2: direct F5 and all counter entries reject a modified/off-pin stack before builds; poisoned-header controls never reach compilation; each prerequisite-removal plant fails the census. Four direct F5 arms plus the additional Makefile arms raise the shared pin population from 106 to 120. No production firmware, image input or pin changed after the merge.

### Dev changes inherited by the merge

Each row comes unchanged from fetched dev `e81ce82f`; the first changed line in the merge delta is named. The counter contract, RTL, fixture and behavior changes are PR #729's. The following implementation commit modifies only the eight files in the change table above.

| File:line | Source |
|---|---|
| `docs/README.md:93` | Inherited from dev `e81ce82f` |
| `docs/findings/117_GPTP_SILICON_EVIDENCE.md:4` | Inherited from dev `e81ce82f` |
| `docs/findings/394_387_E1_SWITCH_CYCLES.md:4` | Inherited from dev `e81ce82f` |
| `docs/findings/629_MEDIA_CLOCK_FOLLOWING_BENCH.md:4` | Inherited from dev `e81ce82f` |
| `docs/findings/667_TALKER_START_BENCH.md:4` | Inherited from dev `e81ce82f` |
| `docs/findings/B14_BENCH_5603C353.md:4` | Inherited from dev `e81ce82f` |
| `docs/history/v1/reference/PROTOCOL_TRACEABILITY.md:320` | Inherited from dev `e81ce82f` |
| `docs/reference/REGISTER_MAP.md:148` | Inherited from dev `e81ce82f` |
| `docs/testing/726_STREAM_COUNTERS.md:1` | Inherited from dev `e81ce82f` |
| `docs/testing/CI_WORKFLOWS.md:286` | Inherited from dev `e81ce82f` |
| `docs/testing/MILAN_V12_AUDIT_2026-08-16.md:218` | Inherited from dev `e81ce82f` |
| `docs/testing/TESTING.md:513` | Inherited from dev `e81ce82f` |
| `hdl/ieee1722/aaf/KL_aaf_packetizer.sv:182` | Inherited from dev `e81ce82f` |
| `hdl/ieee1722/avtp/KL_avtp_rx_monitor.sv:18` | Inherited from dev `e81ce82f` |
| `hdl/ieee1722/avtp/KL_avtp_rx_monitor_ctx.sv:27` | Inherited from dev `e81ce82f` |
| `hdl/ieee1722/avtp/KL_talker_diag_ctx.sv:32` | Inherited from dev `e81ce82f` |
| `hdl/ieee1722/crf/KL_crf_rx.sv:58` | Inherited from dev `e81ce82f` |
| `scripts/measure_test_evidence_readers.py:127` | Inherited from dev `e81ce82f` |
| `scripts/suite_shards.py:2` | Inherited from dev `e81ce82f` |
| `sw/firmware/ctrl/aecp/README.md:55` | Inherited from dev `e81ce82f` |
| `tb/tools/torture_campaign.py:68` | Inherited from dev `e81ce82f` |
| `tb/verilator/avtp_rxmon/sim_lockstep.cpp:9` | Inherited from dev `e81ce82f` |
| `tb/verilator/avtp_rxmon/sim_main_nx.cpp:16` | Inherited from dev `e81ce82f` |
| `tb/verilator/crf_rx/sim_main.cpp:98` | Inherited from dev `e81ce82f` |
| `tb/verilator/milan_dp/Makefile:27` | Inherited from dev `e81ce82f` |
| `tb/verilator/milan_dp/README.md:24` | Inherited from dev `e81ce82f` |
| `tb/verilator/milan_dp/sim_crf_licence.cpp:55` | Inherited from dev `e81ce82f` |
| `tb/verilator/milan_dp/sim_nxn.cpp:93` | Inherited from dev `e81ce82f` |
| `tb/verilator/milan_dp/stream_counter_f5.cpp:1` | Inherited from dev `e81ce82f` |
| `tb/verilator/milan_dp/stream_counter_f5.py:1` | Inherited from dev `e81ce82f` |
| `tb/verilator/milan_dp/stream_counters.hpp:1` | Inherited from dev `e81ce82f` |
| `tb/verilator/milan_dp/stream_counters.py:1` | Inherited from dev `e81ce82f` |
| `tb/verilator/tkdiag/sim_main.cpp:17` | Inherited from dev `e81ce82f` |
| `tests/features/counters_contract_milan.feature:42` | Inherited from dev `e81ce82f` |
| `tests/steps/counters_contract_steps.py:344` | Inherited from dev `e81ce82f` |
| `tests/steps/torture_plan_steps.py:298` | Inherited from dev `e81ce82f` |

### Images and pin proof

The chosen pin remains `405dc68310a18f669049ffc10cc23eef7300dcff`; lwSRP remains `08ee86e812a0eb5e1dc6cd61b494d8baf3491348`. The stack directory/top-level and its own public origin were checked before operations. No stack branch was modified or pushed.

`round20/pin-text-diff.txt` is the fresh complete seven-file diff against dev `e81ce82f`; `pin-tokens.log` proves identical non-comment tokens at identical line positions. `pin-continuity.txt` proves the seven dev inputs are unchanged since `c20c85bd`, so the retained six debug/release RV32 object equalities in `pin-proof.txt` still apply. The source files differ in comments and licence text under ruling 6092176555; source-text byte identity is not claimed. Linked-image byte identity is independently measured below.

All 65 fresh linked ELFs are equal by direct byte comparison, size and SHA-256: five standalone, 30 flat runtime and 30 split runtime variants, covering all five shipped shapes, both interface counts and all three compositions. Both complete manifests hash to `96f55deba3b69b224fb838b746f559b3c944b552c694cef3211470d8b11db584`. The standalone image comparison also reports +0 for every section at both default shapes. The 33 linked-image self-test controls pass.

| Image / shape / layout / composition | Dev bytes / head bytes | Dev SHA-256 | Head SHA-256 |
|---|---:|---|---|
| `ctrl_image/head/endstation_arty_4x4/ctrl_app.elf` | 50752 / 50752 | `8c27ee19b7a4f0a6266834c43c50d8a397469c612fe86860ecc2296ae44ebb5e` | `8c27ee19b7a4f0a6266834c43c50d8a397469c612fe86860ecc2296ae44ebb5e` |
| `ctrl_image/head/endstation_arty_8ch/ctrl_app.elf` | 50752 / 50752 | `b7976d5cc2e0bc8889bbe471472e4817a6368df9a31d48ec8c2e8a1d63c23af7` | `b7976d5cc2e0bc8889bbe471472e4817a6368df9a31d48ec8c2e8a1d63c23af7` |
| `ctrl_image/head/endstation_arty_current/ctrl_app.elf` | 50744 / 50744 | `b119b2b56911120eeb424276525ca53d2e34340bf169bbb4a788efe65cb8a092` | `b119b2b56911120eeb424276525ca53d2e34340bf169bbb4a788efe65cb8a092` |
| `ctrl_image/head/endstation_ax7101_1x1_tdm8/ctrl_app.elf` | 50768 / 50768 | `5a4086ce0245a5e2ad198aa0db56e62b982b7c4c6d177fe4929dca4da6b2dfff` | `5a4086ce0245a5e2ad198aa0db56e62b982b7c4c6d177fe4929dca4da6b2dfff` |
| `ctrl_image/head/endstation_ax7101_8x8/ctrl_app.elf` | 50776 / 50776 | `acb380ee815698bcd99f31920c09e55c3e93d44d7d09b4d1ae8f2d6a2a03c1bd` | `acb380ee815698bcd99f31920c09e55c3e93d44d7d09b4d1ae8f2d6a2a03c1bd` |
| `flat-endstation_arty_4x4-if1-srp/ctrl_app.elf` | 68836 / 68836 | `228c4d2d4da86158199c99b08a0b895661fec07eb56c9554fc2ad32ee0f276c4` | `228c4d2d4da86158199c99b08a0b895661fec07eb56c9554fc2ad32ee0f276c4` |
| `flat-endstation_arty_4x4-if1-nosrp/ctrl_app.elf` | 35312 / 35312 | `b25d258237bf6aa4005ce6a72ce0b36640c08a046e8e522c56e9759ead85d7a7` | `b25d258237bf6aa4005ce6a72ce0b36640c08a046e8e522c56e9759ead85d7a7` |
| `flat-endstation_arty_4x4-if1-aecp/ctrl_app.elf` | 127148 / 127148 | `82e5ce706c7736fa6778c6477a5d43233415fac26efc851aaeb2776146ce34cf` | `82e5ce706c7736fa6778c6477a5d43233415fac26efc851aaeb2776146ce34cf` |
| `flat-endstation_arty_4x4-if2-srp/ctrl_app.elf` | 70364 / 70364 | `d11e73701465dc12654b1871f72a7b10f1ea2c6a2f69157f2b8ea9d5cd3d2d89` | `d11e73701465dc12654b1871f72a7b10f1ea2c6a2f69157f2b8ea9d5cd3d2d89` |
| `flat-endstation_arty_4x4-if2-nosrp/ctrl_app.elf` | 36184 / 36184 | `77419321adfeed9057dbd7b67461dd807c78222422526ca822ea56b9ab39df03` | `77419321adfeed9057dbd7b67461dd807c78222422526ca822ea56b9ab39df03` |
| `flat-endstation_arty_4x4-if2-aecp/ctrl_app.elf` | 128676 / 128676 | `a2dd25cfe83a2469fe03b63ab6804f44fa7c3f91134d338f4ddc642890c76288` | `a2dd25cfe83a2469fe03b63ab6804f44fa7c3f91134d338f4ddc642890c76288` |
| `flat-endstation_arty_8ch-if1-srp/ctrl_app.elf` | 68836 / 68836 | `fed8b54f96ec1c60797841de476947215550b234b3785442e88e96e1b8ed4be8` | `fed8b54f96ec1c60797841de476947215550b234b3785442e88e96e1b8ed4be8` |
| `flat-endstation_arty_8ch-if1-nosrp/ctrl_app.elf` | 35312 / 35312 | `b23e71ad89fe5f7d3e7d059ff8a4f9d48f6a69a71d6060ff166f088e8f7b0ca4` | `b23e71ad89fe5f7d3e7d059ff8a4f9d48f6a69a71d6060ff166f088e8f7b0ca4` |
| `flat-endstation_arty_8ch-if1-aecp/ctrl_app.elf` | 132900 / 132900 | `c2799ea46a854c45e54992800c3cdc93175a364193d41d37f2eefacb966d2118` | `c2799ea46a854c45e54992800c3cdc93175a364193d41d37f2eefacb966d2118` |
| `flat-endstation_arty_8ch-if2-srp/ctrl_app.elf` | 70364 / 70364 | `8da5b37b2527b7b6bf097126ac2c6f3ec39a705c7bdcb3095812d1417388bb0c` | `8da5b37b2527b7b6bf097126ac2c6f3ec39a705c7bdcb3095812d1417388bb0c` |
| `flat-endstation_arty_8ch-if2-nosrp/ctrl_app.elf` | 36184 / 36184 | `f47dc12d5a6bbf98aabb6874b778d3867fbd0310998243b5f65046da42ced74c` | `f47dc12d5a6bbf98aabb6874b778d3867fbd0310998243b5f65046da42ced74c` |
| `flat-endstation_arty_8ch-if2-aecp/ctrl_app.elf` | 134428 / 134428 | `57ad658eff2ddd7570fe64ef08afe51ccdacf23e1fcc98c2dfcf5893aed168c2` | `57ad658eff2ddd7570fe64ef08afe51ccdacf23e1fcc98c2dfcf5893aed168c2` |
| `flat-endstation_arty_current-if1-srp/ctrl_app.elf` | 68412 / 68412 | `7c8ecec43b7a6f829490d84ba46ef485265965188329ee4f412b8eae86d8d245` | `7c8ecec43b7a6f829490d84ba46ef485265965188329ee4f412b8eae86d8d245` |
| `flat-endstation_arty_current-if1-nosrp/ctrl_app.elf` | 35312 / 35312 | `f0f462ae82deb1f9613987c36f965fc05a94e3e727f49eb5c70d0a20becf45ae` | `f0f462ae82deb1f9613987c36f965fc05a94e3e727f49eb5c70d0a20becf45ae` |
| `flat-endstation_arty_current-if1-aecp/ctrl_app.elf` | 121416 / 121416 | `7f2bac9275054548497234c7d8c5042c1525c822775f1391a394d7abb65ff4dc` | `7f2bac9275054548497234c7d8c5042c1525c822775f1391a394d7abb65ff4dc` |
| `flat-endstation_arty_current-if2-srp/ctrl_app.elf` | 69900 / 69900 | `0ca8e6a97eafb7f628960c8fd7d6bf047887ecd16d4aa2728939793f8cc1aa0e` | `0ca8e6a97eafb7f628960c8fd7d6bf047887ecd16d4aa2728939793f8cc1aa0e` |
| `flat-endstation_arty_current-if2-nosrp/ctrl_app.elf` | 36184 / 36184 | `3f40b9150068f56b9118493f9d7d21e1452137c504e826a8d10d86dc3c1d14df` | `3f40b9150068f56b9118493f9d7d21e1452137c504e826a8d10d86dc3c1d14df` |
| `flat-endstation_arty_current-if2-aecp/ctrl_app.elf` | 122912 / 122912 | `31dd11a7820b681d494632ff41ec235bf563a9c5efa3d6cabc89821ae8389bba` | `31dd11a7820b681d494632ff41ec235bf563a9c5efa3d6cabc89821ae8389bba` |
| `flat-endstation_ax7101_1x1_tdm8-if1-srp/ctrl_app.elf` | 68764 / 68764 | `db0fb58e7ebfec18465210871c83e560c8f71f4149932775bf8423f5b7becb19` | `db0fb58e7ebfec18465210871c83e560c8f71f4149932775bf8423f5b7becb19` |
| `flat-endstation_ax7101_1x1_tdm8-if1-nosrp/ctrl_app.elf` | 35312 / 35312 | `a2bea49e78da57f9642592d753e71b7b67d928e0f3482f3fc5ea650694b69bba` | `a2bea49e78da57f9642592d753e71b7b67d928e0f3482f3fc5ea650694b69bba` |
| `flat-endstation_ax7101_1x1_tdm8-if1-aecp/ctrl_app.elf` | 123612 / 123612 | `74a12209e0301a9a7313861e6e944f972a3ba84374a147e476cf2f12814fdcda` | `74a12209e0301a9a7313861e6e944f972a3ba84374a147e476cf2f12814fdcda` |
| `flat-endstation_ax7101_1x1_tdm8-if2-srp/ctrl_app.elf` | 70188 / 70188 | `e052ed2b10e1ae3a65d0b4a0ab31b0d92e7bcd5379c525a4223c1a71f336ad47` | `e052ed2b10e1ae3a65d0b4a0ab31b0d92e7bcd5379c525a4223c1a71f336ad47` |
| `flat-endstation_ax7101_1x1_tdm8-if2-nosrp/ctrl_app.elf` | 36184 / 36184 | `bf7e37a793f2a5cc12c171c4568359ac57464009da4931b6d00d8bb56d420ab3` | `bf7e37a793f2a5cc12c171c4568359ac57464009da4931b6d00d8bb56d420ab3` |
| `flat-endstation_ax7101_1x1_tdm8-if2-aecp/ctrl_app.elf` | 125044 / 125044 | `d3fc02d6916278dc6f43cc27e96920d68657dabe6f4cae7c3cfb26ee43e2ce14` | `d3fc02d6916278dc6f43cc27e96920d68657dabe6f4cae7c3cfb26ee43e2ce14` |
| `flat-endstation_ax7101_8x8-if1-srp/ctrl_app.elf` | 68868 / 68868 | `b9bf08715abcd58e7b7a66781e1e27e9a6762d9560366f68df5c9b2b42487af4` | `b9bf08715abcd58e7b7a66781e1e27e9a6762d9560366f68df5c9b2b42487af4` |
| `flat-endstation_ax7101_8x8-if1-nosrp/ctrl_app.elf` | 35312 / 35312 | `7dd3d0843ef5f97f2f0c58af62fb937561d9c4bb20c0defb33221c2412087f2f` | `7dd3d0843ef5f97f2f0c58af62fb937561d9c4bb20c0defb33221c2412087f2f` |
| `flat-endstation_ax7101_8x8-if1-aecp/ctrl_app.elf` | 137332 / 137332 | `1721078bbde9510b60ba82f4c4cf7cc0639709bc3b419c0aad1260eb407d5d99` | `1721078bbde9510b60ba82f4c4cf7cc0639709bc3b419c0aad1260eb407d5d99` |
| `flat-endstation_ax7101_8x8-if2-srp/ctrl_app.elf` | 70372 / 70372 | `3fc8b8ab4ba24e7d89e0b932ddafa0cffc2f1b9762a17b4cbe0808165f0640aa` | `3fc8b8ab4ba24e7d89e0b932ddafa0cffc2f1b9762a17b4cbe0808165f0640aa` |
| `flat-endstation_ax7101_8x8-if2-nosrp/ctrl_app.elf` | 36184 / 36184 | `104552602a5e5fb901f2a03058f8f0d498d3e6782c9b1ed2e79aeefb6359c04d` | `104552602a5e5fb901f2a03058f8f0d498d3e6782c9b1ed2e79aeefb6359c04d` |
| `flat-endstation_ax7101_8x8-if2-aecp/ctrl_app.elf` | 138836 / 138836 | `fbcf4230d2a5087f28659de75907f60a1f92304e747d3587eb1d40546c6e5e81` | `fbcf4230d2a5087f28659de75907f60a1f92304e747d3587eb1d40546c6e5e81` |
| `split-endstation_arty_4x4-if1-srp/ctrl_app.elf` | 69144 / 69144 | `b63e6e61df8b020539f5676c824a9653c53422e534586372934bf06036d8072b` | `b63e6e61df8b020539f5676c824a9653c53422e534586372934bf06036d8072b` |
| `split-endstation_arty_4x4-if1-nosrp/ctrl_app.elf` | 35624 / 35624 | `1463ecabbae6d29453e7beaa48d5d87a2683df70bcf30b6ca196bb51093f4dc0` | `1463ecabbae6d29453e7beaa48d5d87a2683df70bcf30b6ca196bb51093f4dc0` |
| `split-endstation_arty_4x4-if1-aecp/ctrl_app.elf` | 129740 / 129740 | `bf536d4fca826822cc402bae4b6676ecb5ccb3087b2399c23b1bcbdcd1c96c09` | `bf536d4fca826822cc402bae4b6676ecb5ccb3087b2399c23b1bcbdcd1c96c09` |
| `split-endstation_arty_4x4-if2-srp/ctrl_app.elf` | 70672 / 70672 | `78dcd5b43530f79482de5a860794f345a1e9b3284bf7d813cfe2441cda43c924` | `78dcd5b43530f79482de5a860794f345a1e9b3284bf7d813cfe2441cda43c924` |
| `split-endstation_arty_4x4-if2-nosrp/ctrl_app.elf` | 36496 / 36496 | `05cc67f98e6a3b116e31758796b006d0d3359faef4d10988cce3a4ce80e6f6f1` | `05cc67f98e6a3b116e31758796b006d0d3359faef4d10988cce3a4ce80e6f6f1` |
| `split-endstation_arty_4x4-if2-aecp/ctrl_app.elf` | 129740 / 129740 | `5b0fca5b8ba2780dec30679fb2d3e23f76ffccce2d9372d58f610c78787368b5` | `5b0fca5b8ba2780dec30679fb2d3e23f76ffccce2d9372d58f610c78787368b5` |
| `split-endstation_arty_8ch-if1-srp/ctrl_app.elf` | 69144 / 69144 | `c3c00cb451fea423a03c6e3db549ef56d9ea2653b881567e65bdc71b2db267c3` | `c3c00cb451fea423a03c6e3db549ef56d9ea2653b881567e65bdc71b2db267c3` |
| `split-endstation_arty_8ch-if1-nosrp/ctrl_app.elf` | 35624 / 35624 | `922a5273abcf495c9eb7738d6e189600056e05d74f944714aebe4d70b9f3e6ed` | `922a5273abcf495c9eb7738d6e189600056e05d74f944714aebe4d70b9f3e6ed` |
| `split-endstation_arty_8ch-if1-aecp/ctrl_app.elf` | 133836 / 133836 | `4f7cb03c125fa28a46d2b0bd3543c71c769dee0c01bff4fd88d113cc65df02c0` | `4f7cb03c125fa28a46d2b0bd3543c71c769dee0c01bff4fd88d113cc65df02c0` |
| `split-endstation_arty_8ch-if2-srp/ctrl_app.elf` | 70672 / 70672 | `cb658c5cc7e56ebf45bf868bf3a4e1b7a30bcd68946340af8051b9f44ec8017e` | `cb658c5cc7e56ebf45bf868bf3a4e1b7a30bcd68946340af8051b9f44ec8017e` |
| `split-endstation_arty_8ch-if2-nosrp/ctrl_app.elf` | 36496 / 36496 | `9d0707575b07b5a28274601c0b8a67836e9b07b3f1da73640a477fd68c921c0d` | `9d0707575b07b5a28274601c0b8a67836e9b07b3f1da73640a477fd68c921c0d` |
| `split-endstation_arty_8ch-if2-aecp/ctrl_app.elf` | 137932 / 137932 | `5e2f217ecae327bd2080066807017904485d9bfda4fa06085f8e7f24a44dd081` | `5e2f217ecae327bd2080066807017904485d9bfda4fa06085f8e7f24a44dd081` |
| `split-endstation_arty_current-if1-srp/ctrl_app.elf` | 68720 / 68720 | `3e0bbb97b4d8cbe46f6e47d2a25997ddd081a014be4424399f46409c2a36667b` | `3e0bbb97b4d8cbe46f6e47d2a25997ddd081a014be4424399f46409c2a36667b` |
| `split-endstation_arty_current-if1-nosrp/ctrl_app.elf` | 35624 / 35624 | `6e2058af7af81fa722792273811f0ce0112090968663798322ae082dd7480b8a` | `6e2058af7af81fa722792273811f0ce0112090968663798322ae082dd7480b8a` |
| `split-endstation_arty_current-if1-aecp/ctrl_app.elf` | 125560 / 125560 | `2ea3cfe7d7855ba6b0af93b9d01511f219f5ae6d72ccd367d165f93adb521b82` | `2ea3cfe7d7855ba6b0af93b9d01511f219f5ae6d72ccd367d165f93adb521b82` |
| `split-endstation_arty_current-if2-srp/ctrl_app.elf` | 70208 / 70208 | `5126df88e5ca3ec3045dfef82d1627c41d21f707c6301d9da9011fe6be550171` | `5126df88e5ca3ec3045dfef82d1627c41d21f707c6301d9da9011fe6be550171` |
| `split-endstation_arty_current-if2-nosrp/ctrl_app.elf` | 36496 / 36496 | `039953b2c8ba10f8b149d29a7e119e28f44859e52ba261d1991de0adcc93e574` | `039953b2c8ba10f8b149d29a7e119e28f44859e52ba261d1991de0adcc93e574` |
| `split-endstation_arty_current-if2-aecp/ctrl_app.elf` | 125560 / 125560 | `2b21101556ea642a82a2abf709d5f1060ff96101bcacfdba8cbe9de0e2ab7ad5` | `2b21101556ea642a82a2abf709d5f1060ff96101bcacfdba8cbe9de0e2ab7ad5` |
| `split-endstation_ax7101_1x1_tdm8-if1-srp/ctrl_app.elf` | 69072 / 69072 | `98a4d3efbb0a736348536497e971a5d1de2c5ecfb3b36eedf1cba40d7cfe73af` | `98a4d3efbb0a736348536497e971a5d1de2c5ecfb3b36eedf1cba40d7cfe73af` |
| `split-endstation_ax7101_1x1_tdm8-if1-nosrp/ctrl_app.elf` | 35624 / 35624 | `699bfb5e60dd2c1c2eb75a0261c50a4148957541cd8d9de44e12d1684e9d8aeb` | `699bfb5e60dd2c1c2eb75a0261c50a4148957541cd8d9de44e12d1684e9d8aeb` |
| `split-endstation_ax7101_1x1_tdm8-if1-aecp/ctrl_app.elf` | 125588 / 125588 | `7b9abdfa85028610c96e38e07ea5159875bb92ada730e16dca7c8b1671866715` | `7b9abdfa85028610c96e38e07ea5159875bb92ada730e16dca7c8b1671866715` |
| `split-endstation_ax7101_1x1_tdm8-if2-srp/ctrl_app.elf` | 70496 / 70496 | `b2f0a89354e41dcb4098915a3beab592ca3be1283a7467f9058f1829f5b8832e` | `b2f0a89354e41dcb4098915a3beab592ca3be1283a7467f9058f1829f5b8832e` |
| `split-endstation_ax7101_1x1_tdm8-if2-nosrp/ctrl_app.elf` | 36496 / 36496 | `cf66960c3ff7dc948dcea77455c30eb42bbccc7e6f1b7dbc60a7a04e2bf053aa` | `cf66960c3ff7dc948dcea77455c30eb42bbccc7e6f1b7dbc60a7a04e2bf053aa` |
| `split-endstation_ax7101_1x1_tdm8-if2-aecp/ctrl_app.elf` | 125588 / 125588 | `27dc78da865f00feed7f60f7e4fd56c55a75dfb518bb999e1c22200cc81201d2` | `27dc78da865f00feed7f60f7e4fd56c55a75dfb518bb999e1c22200cc81201d2` |
| `split-endstation_ax7101_8x8-if1-srp/ctrl_app.elf` | 69176 / 69176 | `894962e6880e272e6e6c4aaf19501ae1829a4023110d57c6b5f518b5f8b6ec17` | `894962e6880e272e6e6c4aaf19501ae1829a4023110d57c6b5f518b5f8b6ec17` |
| `split-endstation_ax7101_8x8-if1-nosrp/ctrl_app.elf` | 35624 / 35624 | `9f3cd2b5abd3aa48e5874235baedb63577f5fa26f12e718ef9127033f540cea0` | `9f3cd2b5abd3aa48e5874235baedb63577f5fa26f12e718ef9127033f540cea0` |
| `split-endstation_ax7101_8x8-if1-aecp/ctrl_app.elf` | 138268 / 138268 | `dcd58b96a87d53d42b60c73031e3dd8db4927b7b76b409656aaa3173d09c16d7` | `dcd58b96a87d53d42b60c73031e3dd8db4927b7b76b409656aaa3173d09c16d7` |
| `split-endstation_ax7101_8x8-if2-srp/ctrl_app.elf` | 70680 / 70680 | `27d72c579ac3e444993db59119237cc6992c8ce6d1a2e5f73cee2b3ab7b1bfe9` | `27d72c579ac3e444993db59119237cc6992c8ce6d1a2e5f73cee2b3ab7b1bfe9` |
| `split-endstation_ax7101_8x8-if2-nosrp/ctrl_app.elf` | 36496 / 36496 | `2a5f6bfe67506d516270656e2444dae12d302bd57e42e36da513fbbb5057bbac` | `2a5f6bfe67506d516270656e2444dae12d302bd57e42e36da513fbbb5057bbac` |
| `split-endstation_ax7101_8x8-if2-aecp/ctrl_app.elf` | 142364 / 142364 | `60190c0fa70a22c9c5d2ac93c4d906b38b9aff65358c708ee90d16f5fc85a464` | `60190c0fa70a22c9c5d2ac93c4d906b38b9aff65358c708ee90d16f5fc85a464` |

### Gates and planted controls

Every final required command has rc 0. Negative plants intentionally return nonzero inside their enclosing self-checking command. `round20/receipts.json` records every exact argument vector and elapsed time; `logs/docs-head.log` lists all 54 documentation commands individually. Raw files too large for this packet are represented by size/SHA-256 in `raw-artifacts.json`, with verdict extracts where useful. No binary, toolchain, package or tree export is in the packet.

| Gate / population | Result | Planted control or independent comparison |
|---|---|---|
| Six compiler captures and firmware boundary | 2852 sources / 3082 invocations; no findings | 103 defects + 8 admitted controls + 1 baseline = 112; all expected, including F5 registry/capture deletion |
| Verilator boundary | 829 sources / 926 invocations; no findings | Five defects + baseline = 6; mailbox co-simulation, MAAP differential and both AECP wire shapes pass |
| Shared pin / census / figures | 120 / 4 controls, none misbehaved | Both Git 2.43/2.56 and CPython 3.12.3/3.14.7; dirty bytes, off-pin, object-store/configuration attacks and prerequisite removal |
| Entry points | 27 × 12 = 324 named refusals | Original 21 plus F5 shapes/build-only and all three counter targets; replacement/forged objects, attributes, transport configuration and mode changes |
| Hook rules | H0 clean; H1–H24 caught on both Python versions | Each audit-hook rule removed independently |
| Configuration variants | 21 per Git version, expected table below | Clean baseline; individual configuration checks weakened; no new escape or lost detection |
| Four shard entry forms | Four refuse edited header; four escape when pin line removed | Standalone driver pin-removal control |
| Earlier unchanged review probes | All eight scripts rc 0 on each Git | Spelling, sparse index, promisor transport and object-store probes; detailed retained logs |
| Firmware execution/mutations | All 915 verdicts pass | 60 arms, 506 control, 76 AECP, 198/73 SRP, two lwSRP pin controls |
| Store execution | 435 tests across five shapes | Existing failure/reset/order/boundary cases; coverage reader controls below; no 109-mutant campaign claimed |
| Memory | Full suite passes; 44 mutants caught | Existing reset, split-memory and initialization plants |
| Coverage | 30 files; identical normalized head/dev table | Same compiler; unchanged exclusions; 29/29 reader controls |
| Listener / SDK / RV32 / image readers | All pass | 18 listener mutants, 25 SDK tests, RV32 diagnostic plants and 33 image controls |
| CI event contract / firmware census | 2169 checks; 3064 self-test arms; preserved census | 16 additional workflow plants caught; shard proof 916 invocations in exactly one shard |
| Disposable runner | 446 self-test arms pass | Network disabled, read-only candidate, no socket or credential forwarding; never candidate host-side orchestration |
| Documentation/source-list/evidence/idioms | 54/54 commands pass at committed head | Their standing self-tests, missing-input and evidence-reader plants; no ratchet increased |
| #726 baselines and original defect controls | Both shapes, frames-only, MAKEFLAGS=-w pass | Both before variants fail only the required original TX/RX/CADENCE groups |
| #726 counter mutations | All 12 RTL shape/variant cases pass | Eleven named variants; egress-stall also at 8×8; every detection has a passing check-omission run |
| F5 | Both baselines and direct make target pass | late/rate/fixed-grid each detected, then passes with its named check omitted; build-only runs no tests |
| #726 behavior / campaign / scheduling | 406 scenarios, 1977 steps; self-tests pass | Counter laws and phase/cadence cases; torture campaign self-test and suite shard controls |

The six capture phases plus judgement total 836.79 seconds locally (46.5% of the existing 30-minute timeout, below its 1080-second 60% ceiling). This excludes dependency installation and is a sum of bounded foreground commands, not a new hosted timing. Verilator boundary took 511.49 seconds (21.3% of its 40-minute timeout). Prior hosted budget evidence remains historical; this head has no new hosted acceptance.

### Coverage table

Same GCC/gcov 16.2.1 and GoogleTest 1.18.0 on candidate and dev. Counts below are raw covered/total; percentages are after the unchanged documented exclusions. Every normalized row is identical on both sides.

| File | Dev/head lines | Dev/head branches | After exclusions |
|---|---:|---:|---|
| `sw/firmware/ctrl/acmp/acmp_mbx.c` | 79/79 | 28/28 | 100.00% lines / 100.00% branches |
| `sw/firmware/ctrl/acmp/acmp_nvm.c` | 38/38 | 10/10 | 100.00% lines / 100.00% branches |
| `sw/firmware/ctrl/adp/adp_mbx.c` | 83/83 | 38/40 | 100.00% lines / 100.00% branches |
| `sw/firmware/ctrl/aecp/aecp.c` | 357/357 | 308/308 | 100.00% lines / 100.00% branches |
| `sw/firmware/ctrl/aecp/aecp_commands.c` | 424/424 | 362/362 | 100.00% lines / 100.00% branches |
| `sw/firmware/ctrl/aecp/aecp_image.c` | 77/77 | 80/80 | 100.00% lines / 100.00% branches |
| `sw/firmware/ctrl/aecp/aecp_maps.c` | 222/222 | 290/290 | 100.00% lines / 100.00% branches |
| `sw/firmware/ctrl/aecp/aecp_mbx.c` | 101/101 | 40/40 | 100.00% lines / 100.00% branches |
| `sw/firmware/ctrl/aecp/aecp_nvm.c` | 102/102 | 86/86 | 100.00% lines / 100.00% branches |
| `sw/firmware/ctrl/aecp/aecp_state.c` | 63/63 | 69/69 | 100.00% lines / 100.00% branches |
| `sw/firmware/ctrl/app/ctrl_app.c` | 42/43 | 40/44 | 100.00% lines / 100.00% branches |
| `sw/firmware/ctrl/app/ctrl_app_aecp.c` | 107/107 | 64/64 | 100.00% lines / 100.00% branches |
| `sw/firmware/ctrl/app/ctrl_app_srp.c` | 82/82 | 62/62 | 100.00% lines / 100.00% branches |
| `sw/firmware/ctrl/loop/ctrl_loop.c` | 101/101 | 62/62 | 100.00% lines / 100.00% branches |
| `sw/firmware/ctrl/maap/maap_csr.c` | 39/39 | 18/18 | 100.00% lines / 100.00% branches |
| `sw/firmware/ctrl/maap/maap_mbx.c` | 99/99 | 64/64 | 100.00% lines / 100.00% branches |
| `sw/firmware/ctrl/mbx/mbx.c` | 243/243 | 102/102 | 100.00% lines / 100.00% branches |
| `sw/firmware/ctrl/mbx/mbx_wire.h` | 15/15 | 12/12 | 100.00% lines / 100.00% branches |
| `sw/firmware/ctrl/plat/mbx_plat_mmio.c` | 10/10 | 0/0 | 100.00% lines / 100.00% branches |
| `sw/firmware/ctrl/port/ctrl_debug.c` | 19/19 | 6/6 | 100.00% lines / 100.00% branches |
| `sw/firmware/ctrl/port/ctrl_pool.c` | 99/99 | 60/60 | 100.00% lines / 100.00% branches |
| `sw/firmware/ctrl/port/shlan_port.c` | 22/22 | 6/6 | 100.00% lines / 100.00% branches |
| `sw/firmware/ctrl/srp/srp_mbx.c` | 540/540 | 486/486 | 100.00% lines / 100.00% branches |
| `sw/firmware/ctrl_nvm/nvm_klj2.c` | 198/199 | 106/110 | 100.00% lines / 100.00% branches |
| `sw/firmware/ctrl_nvm/nvm_store.c` | 434/434 | 259/266 | 100.00% lines / 100.00% branches |
| `sw/firmware/ctrl_nvm/plat/nvm_flash_litespi.c` | 100/100 | 63/64 | 100.00% lines / 100.00% branches |
| `third_party/tsn-c-stack/include/wire.h` | 10/10 | 2/2 | 100.00% lines / 100.00% branches |
| `third_party/tsn-c-stack/src/acmp.c` | 767/767 | 362/362 | 100.00% lines / 100.00% branches |
| `third_party/tsn-c-stack/src/adp.c` | 204/206 | 95/102 | 100.00% lines / 100.00% branches |
| `third_party/tsn-c-stack/src/maap.c` | 209/209 | 140/140 | 100.00% lines / 100.00% branches |

### Mutation tables

The full 915 named results are in `round20/firmware-verdicts.txt`. Disjoint campaign populations are retained as JSON; no item is dropped or counted twice.

| Population | Count | Result |
|---|---:|---|
| Control slices | 127 / 127 / 127 / 125 | 506 caught |
| AECP | 76 | 76 caught |
| SRP two interfaces | 99 / 99 | 198 caught |
| SRP one interface | 37 / 36 | 73 caught |
| lwSRP pin | 2 | 2 caught |
| Memory | 44 | 44 caught |
| Listener | 18 | 18 caught |
| Boundary defects / admitted / baseline | 103 / 8 / 1 | All expected |
| Verilator boundary defects / baseline | 5 / 1 | All expected |
| Pin / figure | 120 / 4 | All expected in four environments |
| CI workflow plants | 16 | 16 caught |
| RTL counter mutants | 11 + egress-stall at second shape | 12 detected and 12 omission escapes |
| F5 counter mutants | 3 | 3 detected and 3 omission escapes |

| Configuration variant | Git 2.43 | Git 2.56 |
|---|---|---|
| N0 none | rc 0; 0 escaped | rc 0; 0 escaped |
| N1 the superproject check not called | rc 1; 7 escaped | rc 1; 7 escaped |
| N2 the superproject check after the index is read | rc 1; 5 escaped | rc 0; 0 escaped |
| N3 the superproject's local scope only | rc 1; 1 escaped | rc 1; 1 escaped |
| N4 extensions.partialclone not refused | rc 1; 2 escaped | rc 1; 2 escaped |
| N4 remote.promisor not refused | rc 1; 4 escaped | rc 1; 4 escaped |
| N4 remote.partialclonefilter not refused | rc 1; 2 escaped | rc 1; 2 escaped |
| N4 remote.uploadpack not refused | rc 1; 1 escaped | rc 1; 1 escaped |
| N4 core.sshcommand not refused | rc 1; 1 escaped | rc 1; 1 escaped |
| N4 core.fsmonitor not refused | rc 1; 2 escaped | rc 1; 2 escaped |
| N5 the helper's own command-line setting refused in the superproject | rc 1; 0 escaped; clean proof refused | rc 1; 0 escaped; clean proof refused |
| N6 no HELPER_CONFIG | rc 0; 0 escaped | rc 0; 0 escaped |
| N7 no GIT_NO_LAZY_FETCH | rc 0; 0 escaped | rc 0; 0 escaped |
| N8 neither the superproject check nor GIT_NO_LAZY_FETCH | rc 1; 7 escaped | rc 1; 7 escaped |
| N9 neither the superproject check nor HELPER_CONFIG | rc 1; 7 escaped | rc 1; 7 escaped |
| P1 round 16's match: a remote key with a named subsection only | rc 1; 3 escaped | rc 1; 3 escaped |
| P2 a remote key with a subsection, named or empty, only | rc 1; 2 escaped | rc 1; 2 escaped |
| P3 a remote key with a named subsection or none only | rc 1; 1 escaped | rc 1; 1 escaped |
| P4 the stack's `*` family holding an empty subsection too | rc 1; 1 escaped | rc 1; 1 escaped |
| P5 parsed_key reading an empty subsection as none | rc 1; 1 escaped | rc 1; 1 escaped |
| P6 parsed_key reading no subsection as an empty one | rc 1; 51 escaped; clean proof refused | rc 1; 51 escaped; clean proof refused |

N6/N7 remove isolated defense-in-depth settings while the primary check remains; their zero escapes are expected and are not kills. N2 retains its known Git-version difference. N5/P6 over-refuse the clean proof. P6 retains its 51 affected controls before its expected setup refusal; its original detections remain. H0–H24 and each #726 named group/omission result are retained in the gate logs.

### Reproduction, corrections and limits

Use CPython 3.12.3, the pinned RV32 SDK and Verilator 5.050, `VERILATOR_JOBS=2`, campaign `--jobs 4`, disk `TMPDIR` and the pinned Python requirements. `WORK`, `CAP`, `CANDIDATE`, `DEV`, `EVIDENCE` and `RUNTIME_ROOT` are caller-selected paths; the runtime root supplies the same `runtime` and `runtime-freestanding` archives. The retained Round 19 reproduction block applies with the sixth capture added and the dev reference changed to e81ce82f. Exact command receipts cover every additional campaign.

```sh
python3 sw/firmware/ctrl/test/ctrl_capture.py --out "$CAP/f5" -- python3 tb/verilator/milan_dp/stream_counter_f5.py --build-only --shape 1 --work "$WORK/f5-1"
python3 sw/firmware/ctrl/test/ctrl_capture.py --out "$CAP/f5" -- python3 tb/verilator/milan_dp/stream_counter_f5.py --build-only --shape 8 --work "$WORK/f5-8"
python3 sw/firmware/ctrl/test/ctrl_boundary.py --require-rv32 --selftest --without verilator --capture "$CAP/rv32" --capture "$CAP/control" --capture "$CAP/store" --capture "$CAP/coverage" --capture "$CAP/memory" --capture "$CAP/f5"
python3 sw/firmware/ctrl/test/ctrl_boundary.py --require-rv32 --selftest --only verilator
python3 "$EVIDENCE/round20/scripts/held_text_probe.py" "$CANDIDATE"
python3 "$EVIDENCE/round20/scripts/images.py" "$CANDIDATE" "$WORK/images-head"
python3 "$EVIDENCE/round20/scripts/images.py" "$DEV" "$WORK/images-dev"
python3 sw/firmware/ctrl/test/ctrl_image.py --base e81ce82f9aa3e4dcaffa5bcdf7e60f0c7cffd80c --out "$WORK/image-delta"
make -C tb/verilator/milan_dp counters-f5
python3 "$EVIDENCE/round20/scripts/stream_group.py" "$WORK" tx-interval rx-interval tx-reset aaf-reset
python3 "$EVIDENCE/round20/scripts/stream_group.py" "$WORK" crf-reset rx-saturation late rate
python3 "$EVIDENCE/round20/scripts/stream_group.py" "$WORK" tx-nodirty fixed-grid egress-stall egress-stall@8
```

Corrected attempts remain visible. The first documentation run caught the expanded pin module's size; extracting the existing bench helper fixed it without changing the ratchet. A clone-verification path typo was corrected before use. The first configuration run reused a disposable stack store previously unpacked for forged-object entry controls; cleanup raced automatic maintenance. Those setup failures are excluded, and both complete configuration tables come from fresh independent stores. No failing plant is counted as a successful mutation kill merely because its setup failed.

The service briefly exceeded the requested 9 GB working target: recorded peak 11,070,345,216 bytes, with no OOM event. Overlap was reduced and only this task's file cache was reclaimed. Subsequent monitored samples remained below the target. At most two simulation builds ran at once; no campaign used more than four workers. All runs were foreground commands below the ten-minute command limit; no hardware or Vivado run occurred.

R584-17-RES-1 and R585-18's corresponding pushed-head residue are applied to the prepared PR body's historical Round 19 statements. R584-17-RES-2's historical README citation is corrected to line 193, with the current line 196 called out. The earlier R585-16 prose residue remains explicitly quoted and carried as assigned. No existing issue/PR comment was edited, and the PR itself was not edited.

No coverage row, required mutation kill or #726 regression was lost. The historical supplementary 109-mutant store campaign is not claimed; the required store execution command passes. The full exhaustive repository sweep, Yosys/Vivado gates, protected hosted contexts and PR-head local replica are not claimed for this unpushed round. Independent review, publication and the later merge-validation bar remain the manager's work. The issue remains open. The prepared new issue comment reports this exact head and bounded local evidence; after posting REVIEW READY, work stops.


### Final inherited unit-suite supplement

The merge audit checked the changed unit fixtures directly in disposable checkouts, in addition to the parent-MAC counter campaign. All four command groups return rc 0:

| Command | Result / standing control |
|---|---|
| `make -C tb/verilator/tkdiag` | 99 checks, zero failures; five mutation checks pass |
| `make -C tb/verilator/avtp_rxmon` | Single/multiple-context tests pass; lockstep 36 checks at each shape; five mutation checks pass |
| `make -C tb/verilator/crf_rx run` | Counter, 2201-check discontinuity and connected-talker simulations pass |
| `make -C tb/verilator/crf_rx mutants` | Ten positive/negative checks pass; six receiver and two servo defects detected |

These legacy Makefiles spell build concurrency literally. A scratch launcher changes only `-j`'s value to 2 and forwards every remaining argument to the supplied pinned 5.050 executable. Its portable source is `round20/scripts/verilator-two.py`; set `PINNED_VERILATOR` to that executable and `VERILATOR` to the launcher. No source/expectation/timing flag changed. At most two builds ran together.

`round20/population-continuity.json` confirms every control/SRP population equals Round 19's, including each disjoint slice. `round20/verdict-continuity.json` confirms all 915 sorted verdict lines are identical, not just their count. The final packet contains 66 passing main command groups plus the seven separately recorded quick checks and the 54-command documentation list. The working tree remains clean at `d40e4e9827be2516f8f34b9d65f0a483fff2194c`.
