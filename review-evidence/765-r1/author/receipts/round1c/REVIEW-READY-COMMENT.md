[A657] REVIEW READY
Commit: 75db4b57cff47bb614d14dead084649a4c2aa2a3 (branch 765-unsupported-format, local, not pushed)
Changed:
- 7f84892a merges dev 78ca9bdf, which carries PR #767 (rounds 3 and 4) and PR #766. It is a merge commit: first parent 4605409b, second 78ca9bdf. git reported no conflict, and nothing earlier is rewritten. The merge changes the RTL by two #767 comment lines only. The #765 compare (KL_avtp_rx_monitor_ctx.sv:501,508,512-528; KL_crf_rx.sv:323-335) and #762's stopped-input wiring (milan_datapath.sv:6308) are unchanged.
- 75db4b57 gives [762-DP] the current-format stimulus (tb/verilator/milan_dp/sim_nxn.cpp:6764-6772). It reads STREAM_INPUT 0's channel count with GET_STREAM_FORMAT (rx_chans(0), as the 5.3.8.7 discard section before it does), logs it, and builds every PDU with it. The length is max(400, the AAF size), so #767's 400-octet frames are kept wherever they were long enough. The milan_dp README's [762-DP] paragraph says so (README.md:1199-1201). No [762-DP] check or expectation changed. rx_chans adds its own readability check, +1 per leg.
- The risk was real. At the merge commit, [762-DP] fails 4 checks on obj_dynmap (input 0 at 8 ch, 200/4) and on obj_nxn4c (4 ch, 1982/4): stopped-gap SEQ_NUM_MISMATCH +1, and after START MEDIA_LOCKED, SEQ_NUM_MISMATCH and STREAM_INTERRUPTED +1. The fixed 2-channel PDU was a format reject, so no gap reached the counters.
Validation (all rc 0 at 75db4b57, clean clones):
- scripts/run_all_suites.sh, shards 0/2 and 1/2: 63/63 suites, 2,187,823 checks, 0 failures, 0 timeouts
  - milan_dp: every leg, obj_dynmap included, and render_mutants 6/6
  - avtp_rxmon: lockstep N=1 116 and N=8 119, lockstep_mutants.py 14/14, format_mutants.py 6/6
  - crf_rx: mutants.py 21/21
- [762-DP] on all five legs that run it (obj_dynmap 8 ch, obj_nxn 4, obj_nxndv 4, obj_nxn8 8, obj_nxn4c 4): while stopped, SEQ_NUM_MISMATCH +1 and MEDIA_UNLOCKED +1 with STREAM_INTERRUPTED +0; after START, MEDIA_LOCKED +1, SEQ_NUM_MISMATCH +1 and STREAM_INTERRUPTED +1
- [762-DP] wiring plants at milan_datapath.sv:6308, on obj_dynmap and obj_nxn4c: 8/8 (clean control 201/0 and 1983/0)
  - '0 and acmpl_stopped_v_w[N_STREAMS:1] each fail exactly "[762-DP] 2 stopped gap: STREAM_INTERRUPTED +0" and "[762-DP] 3 stopped silence: STREAM_INTERRUPTED +0"
  - acmpl_bound_v_w[N_STREAMS-1:0] fails exactly "[762-DP] 4 started gap: STREAM_INTERRUPTED +1"
  - on obj_dynmap the elaborated-parameter digest is d2094321fbb6f594 in all four runs, the same as #767's review recorded
- make -C tb/verilator/milan_dp unb-mutants: 6/6
- make -C tb/verilator/tsn_fuzz with TSN_GEN_ROOT at the CI pin deca300c: AAF/AVTP 164/0, gPTP 677/0, freshness PASS
- syn/yosys/run.sh 58/58, tied-input and tap-purity PASS, cell counts identical to 2f33a9ce; scripts/xvlog_gate.py --check 0 findings
- 32 static and docs gates (lint_rtl, measure_test_evidence, idiom, hygiene, port contracts, em dash, docs_check, module matrix, resource-gate selftest and check-baseline, ...): all rc 0
- builder bank: scripts/ci_builder_legs.py run 0 and run 1 with test_builder.py --require-elaboration --require-rv32, then union --workflow elaborate; 103 gates exactly once. One arm did not run, for a recorded reason: gate 11 reads a historic Arty build tree that is not on this host
- route-1x1 (export from a clean clone at 75db4b57, same recipe as round 1b): fully routed, WNS +0.137 ns, WHS +0.024 ns. syn/ooc/pp_resource_gate.py check --endpoint route-1x1: RESULT PASS, LUT 49,857 (+244 over the record, tolerance 500). The timing and utilization report bodies are identical to round 1b's route at 2f33a9ce, so round 1b's per-block attribution stands
Acceptance criteria: met. A PDU whose subtype or channel count differs from the input's current format counts UNSUPPORTED_FORMAT and is discarded (4.4.2.2, Table 5.6/5.16/6.2). There are cases for another channel count, an AAF PDU on a CRF input and a matching PDU, each with a planted mutant: [UF1a-5a] with format_mutants.py, and [FMT] with crf_rx mutants.py. FR-STR-03 and the compliance matrix row are updated. The suites pass.
Open risks/questions:
- The round-1b open risk (#767's [762-DP] stimulus) is resolved by 75db4b57.
- make dynmap-mutants was not re-run. The change touches only the case that follows [DYNMAP] on a fresh boot.
- Round 1's limitations stand: the pruned 1x1 short-frame depacketizer window; inputs above 0 read their format only from LCTX words 2/3; samples_per_frame has no PDU field; the flat test-instrument monitor keeps no channel compare. New issues are recommended; none filed.
