# Independent statement checks

Exact head: 18a4dc1fcf91528a52737d5ea830b5acd5d543c4. These are source checks, not an assertion that all external clauses were available. `source-excerpts.log`, `construction.log` and the suite logs preserve the corresponding evidence. “01” through “08” mean `docs/architecture/NN_*.md`.

| # | Current-page statement | Independent source / executable evidence | Result |
|---|---|---|---|
| 1 | 01 F01.5: one AVB interface by default | top:107 N_AVB_IF_P=1 | match |
| 2 | 01 F01.5: 16 registry controllers per interface | common/pp_pkg.sv PP_N_CTRL_C=16 | match |
| 3 | 01 F01.5: one Audio Unit | top N_AUDIO_UNIT_P=1 | match |
| 4 | 01 F01.5: one clock domain | top N_CLK_DOMAIN_P=1 | match |
| 5 | 01 F01.5: four RX slots | top:115 RX_SLOTS_P=4 | match |
| 6 | 01 F01.5: 576 bytes per RX slot | top:116 RX_SLOT_BYTES_P=576 | match |
| 7 | 01 F01.5: four standard TX slots | top:118 TX_STD_SLOTS_P=4 | match |
| 8 | 01 F01.5: 1600-byte oversize TX slot | top:119 TX_OVERSIZE_BYTES_P=1600 | match |
| 9 | 01 F01.5: 100 MHz core default | top:121 CLK_HZ_P=100000000 | match |
| 10 | 01 F01.5: 2048-word microcode ROM | ucpu_pkg UPC_W_C=11; generator produces 2048 words | match |
| 11 | 01 F01.5: 48-bit microinstructions | ucpu_pkg UCODE_W_C=48; generated words are 12 hex digits | match |
| 12 | 01 F01.5: 32-bit listener ROM entries, 112 active cells | listener trom_r; generator 112 event/state cells plus padding to 128 | match |
| 13 | 01 F01.5: trace ring 256 by 128 bits | KL_pp_trace_ring RECORDS_P=256, RECORD_W_P=128 | match |
| 14 | 01 F01.5: MAAP acceptance timeout 1024 clocks | KL_acmp_talker:208 MAAP_ACCEPT_CYC_P=1024 | match |
| 15 | 01 F01.5: MAAP reply timeout 10000 ms | KL_acmp_talker:248 MAAP_RSP_MS_P=10000 | match |
| 16 | 01 F01.5: restore timeout ceil(clock/50) | top:169-170 quotient plus nonzero remainder | match |
| 17 | 01 F01.5: aggregate restore timeout one clock-rate count | top:179 NVM_RS_AGG_CYC_P=CLK_HZ_P | match |
| 18 | 01 F01.5: retry backoff ceil(clock/2) | top:184 quotient plus remainder | match |
| 19 | 01 F01.5: memory deadline one clock-rate count | top:197 NVM_MEM_TMO_CYC_P=CLK_HZ_P | match |
| 20 | 01 F01.5: both persistence producers debounce 500 ms ticks | KL_acmp_nvm_shadow:139 and KL_aecp_nvm_writer:193 | match |
| 21 | 01 F01.5: two additional retries | same producer parameter declarations RETRY_MAX_P=2 | match |
| 22 | 08 F08.4: five singleton timer slots | pp_pkg:181 PP_SINGLETON_SLOTS_C=5 | match |
| 23 | 08 F08.4: two MAAP slots appended after singletons | pp_pkg:186, 205-206 | match |
| 24 | 08 F08.4: baseline 68, with SRP 91 | pp_timer_map recurrence, 1+8+8+8+32+4+5+2=68 and +7+8+8=91; timer_map suite passes | match |
| 25 | 07 F07.1: shipped ROM kinds are microcode and listener transitions; no dispatch/response-size ROM | complete hdl readmem search has only KL_aecp_ucpu:150 and KL_pp_acmp_listener:423; both generators independently regenerated | match |
| 26 | 01 §5: effective-enable fall implements shutdown, no separate shutdown port | top:2027 requested enable AND restore_done AND !rbt_adp_off | match |
| 27 | 06 §6.11: REBOOT below cdl 16 routes BAD_ARGUMENTS | engine:3655 UPC_RBOOTBAD; gen_ucode:2366 ST_BADARG | match to source; external §7.4.43 text not yet independently available |
| 28 | 06 §6.11: non-ENTITY REBOOT routes NOT_SUPPORTED | engine:3656 UPC_RBOOTNS; gen_ucode:2365 ST_NSUPP | match to source |
| 29 | 06 §6.11: descriptor locate precedes lock test | gen_ucode:2353-2355 DESC_ADDR, BR_STATUS then CHECK_LOCK | match to source |
| 30 | 06 §6.11: successful REBOOT enqueues notification class 9 | gen_ucode:2356-2357 SET_STATUS then NOTIFY_ENQ 9 | match to source |
| 31 | 06 §6.11: successful response TX grant stops command service | engine:3962-3970 A_TXW, !uns, rboot, SUCCESS; txn_ready_o:2682 and A_IDLE:2860 both gate rbt_hold | match to source |
| 32 | 06 §6.11: unsolicited path remains available during hold | engine A_IDLE tests unsolicited work independently; hold is on command take | match to source |
| 33 | 06 §6.11: new RX frames discarded after acceptance | top:1357-1364 frame-level admission latch | match to source |
| 34 | 06 §6.11: request waits for notifications, ADP queue and arbiter idle | top:4943-4950 RB_NTF and RB_DEP guards | match to source |
| 35 | 06 §6.11: reboot request held until reset | top:4951 absorbing RB_REQ and :4957 level decode | match to source |
| 36 | 06 §6.11: persistence is not a request condition | complete sequence top:4936-4957 has no persistence wait; pending handling belongs to integrator | match to source |
| 37 | 06 §8: 29 µISA operations, table lacks SHIFT_R | ucpu_pkg:50-90 enumerates 0..29; KL_aecp_ucpu:681 implements SHIFT_R; generated ROM has 13 words with opcode 29 | FAIL: F2 |
| 38 | 02 §4.1: §34.6.1.1 defines per-stream idleSlope | public PR body identifies this clause as nonexistent while page:284 retains it | inconsistent: F1, direct edition recheck pending |
| 39 | tb/prng headline: 76 checks | reviewer execution: 76 PASS, 0 FAIL | match |
| 40 | tb/dispatch headline: 211 checks | reviewer execution: 211 PASS, 0 FAIL | match |
| 41 | tb/desc_store headline: 586 checks | reviewer execution: 586 PASS, 0 FAIL | match |
| 42 | tb/timer_map headline: 1360 checks | reviewer execution: 1360 PASS, 0 FAIL | match |
| 43 | tb/dyn_state: two shapes, 62 + 56 = 118 checks | reviewer execution: 118 PASS, 0 FAIL | match |
