[A657] STOP
Commit: cc71db3a557bb6160c81e69a52fd3ceed6622dc5 (branch 765-unsupported-format: 31903ec1 RTL+tests, 91aaa6bd docs, cc71db3a milan_dp stimulus; on PR #767 head 4191b098)
Blocker: the route-1x1 resource gate exits 1. Assignment item 4 asks for rc 0 on every gate. AREA_BUDGET.md makes accepting this growth a reviewed re-record, which is not this lane's decision. Everything else is done and green.

Gate: `pp_resource_gate.py check --endpoint route-1x1` -> MATERIAL REGRESSION, LUT only. LUT 50,158 against the record's 49,613 (+545, tolerance 500); the base route of 4191b098 is 49,411 (+747). FF +15, SLICE -142, BRAM/DSP unchanged. WNS +0.363 ns (base +0.161), WHS +0.015 ns (floor 0), fully routed, no routing error.
Attribution: same recipe, Vivado build, pins and Tcl as the base route; memory init files identical; only the RTL differs. The changed blocks net -1 LUT (avtp_rx_monitor 778 -> 749, crf_rx 253 -> 281). After synthesis alone the design is already +621, of which the SoC CPU is +369 and top-level glue +248, neither reached by this RTL. After place: gptp_shadow +281, CPU +239, top +201, chan_map_render +89, milan_csr -118. Per AREA_BUDGET.md (combination B) that movement is still this change's cost.
Decision needed: accept the route and re-record route-1x1 (`record --write`, reviewed), or another disposition.

Changed:
- `KL_avtp_rx_monitor_ctx.sv:492-523`: the format compare adds the 10-bit channels_per_frame against the current format's [31:22]. A mismatch counts UNSUPPORTED_FORMAT and has no accept verdict, so the depacketizer drops it (Milan v1.2 4.4.2.2, Table 5.6, Table 6.2; IEEE 1722-2016 7.3, I.2.4, I.2.4.1). The BAF v1.1 comment is replaced.
- `KL_crf_rx.sv:321-333`: a Stream Data AVTPDU on the CRF input's stream_id is matched whatever its subtype. A non-CRF subtype is a format reject: UNSUPPORTED_FORMAT, not accepted, lock kept, sequence unmoved.
- Tests:
  - avtp_rxmon `[UF]` (`sim_main_nx.cpp:902`) and `format_mutants.py`: 5 mutants, each caught by its named check.
  - crf_rx `[FMT]` (`sim_main.cpp:1508`): 3 mutants in `mutants.py`.
  - The lockstep reference applies the same compare (the #762 precedent).
- milan_dp: 11 cases (36 checks) fed STREAM_INPUT 0 a channel count other than its current format. They now carry that format: GET_STREAM_FORMAT in sim_nxn.cpp, the declared format from the shape header in sim_main.cpp/sim_prune.cpp. No check removed.
- Docs:
  - FR-STR-03 and its status row.
  - A live 4.4.2.2 row in MILAN_COMPLIANCE_MATRIX.md, which closes the v1 family-compare record. That record is the archived docs/history/v1 page, left as evidence.
  - CRF_STATUS[15:8], MEDIA_CLOCK_FOLLOWING.md, TESTING.md.
- No register-map layout, port or parameter change.

Validation (Verilator 5.050, sv2v 0.0.12):
- scripts/run_all_suites.sh at cc71db3a: rc 0, 63/63 suites, 2,186,679 checks, 0 failures, 0 timeouts. tsn_fuzz with tsn-gen at the CI pin deca300c: AAF/AVTP 164/0, gPTP 677/0, freshness PASS.
- avtp_rxmon: NX 147/147, lockstep 53/53 at N=1 and N=8, lockstep_mutants 8/8, format_mutants 6/6. crf_rx mutants 18/18.
- milan_dp: every case rc 0 in a clean clone, including counters-1/-8 (and -frames), notify, nxn/nxn8/nxn4c/nxndv, ax1x1, prune, aclk and dynmap. unb-mutants 6/6.
- syn/yosys/run.sh: 58/58, tied-input and tap-purity PASS. xvlog_gate --check: 0 findings. 29 static gates rc 0 (lint_rtl, measure_test_evidence, idiom, hygiene, port contracts, docs, em dash, module matrix, resource-gate selftest/check-baseline).
- Interpreters: the Python gates ran on CPython 3.12.3. The sweep ran on the host CPython 3.14.8 because the provided 3.12.3 build lacks os.pidfd_open, which scripts/owned_process.py requires.

Acceptance criteria:
- Count and discard on a subtype or channel-count mismatch: met (`[UF2]`, `[UF3]`, `[UF5a]`, `[FMT-b]`).
- Simulation cases with planted mutants: met. Another channel count `[UF2a]`, AAF on CRF `[FMT-b1]`/`[FMT-b3]`, matching AAF `[UF1a]`, matching CRF `[FMT-a1]`.
- FR-STR-03 and traceability updated: met (as above).
- Suites pass: met (63/63).

Open risks/questions (new issues recommended; none filed):
1. On the pruned 1x1 leg, a bare 86-octet 2-channel frame is accepted by the monitor but not emitted by the depacketizer: 16 accepted, 0 emitted. The base 4191b098 shows the same. Padded to 120 octets, 15 emitted; to 230, all 16. The depacketizer commits only if the verdict lands before the frame's last beat. A real 2-channel stream uses 86-octet frames. sim_prune.cpp pads to 230 to keep its subject.
2. Inputs above 0 read their current format only from LCTX words 2/3 (the CSR window). SET_STREAM_FORMAT reaches input 0 only (milan_datapath.sv:3379), and no firmware writes those words. The channel compare now depends on them. The shipping 1x1 shape has one input.
3. samples_per_frame has no PDU field (1722-2016 I.2.4.1), so it is not compared.
4. The flat KL_avtp_rx_monitor test instrument keeps no channel compare; the delta is recorded in the engine's banner.
