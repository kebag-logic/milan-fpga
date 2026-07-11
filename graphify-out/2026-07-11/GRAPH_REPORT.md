# Graph Report - milan-fpga  (2026-07-11)

## Corpus Check
- 382 files · ~446,594 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 2850 nodes · 3563 edges · 393 communities (209 shown, 184 thin omitted)
- Extraction: 96% EXTRACTED · 4% INFERRED · 0% AMBIGUOUS · INFERRED: 140 edges (avg confidence: 0.53)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `06d6c7b7`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- [[_COMMUNITY_milan_soc.py|milan_soc.py]]
- [[_COMMUNITY_H|H]]
- [[_COMMUNITY_Milan v1.2 endpoint — Functional & Non-Functional Requirements (FRNFR)|Milan v1.2 endpoint — Functional & Non-Functional Requirements (FR/NFR)]]
- [[_COMMUNITY_Troubleshooting — every problem hit bringing up the full-FPGA solution, and its fix|Troubleshooting — every problem hit bringing up the full-FPGA solution, and its fix]]
- [[_COMMUNITY_README|README.md]]
- [[_COMMUNITY_Latency & memory investigation — why single-port TCP caps at 30 Mbits (2026-07-05)|Latency & memory investigation — why single-port TCP caps at 30 Mbit/s (2026-07-05)]]
- [[_COMMUNITY_MilanDebug|MilanDebug]]
- [[_COMMUNITY_Direction from the 1-NIC endpoint to a 4-port AVB switch (MTU fixed at 1500)|Direction: from the 1-NIC endpoint to a 4-port AVB switch (MTU fixed at 1500)]]
- [[_COMMUNITY_TX RingDMAReader prefetch — design plan (roadmap step 1, primary TX lever)|TX RingDMAReader prefetch — design plan (roadmap step 1, primary TX lever)]]
- [[_COMMUNITY_2. Functional Requirements (FR)|2. Functional Requirements (FR)]]
- [[_COMMUNITY_MilanDebug|MilanDebug]]
- [[_COMMUNITY_PART B — ADP  AVDECC (the complete AVB solution)|PART B — ADP / AVDECC (the complete AVB solution)]]
- [[_COMMUNITY_Protocol validation matrix — every protocol, and every test that validates it|Protocol validation matrix — every protocol, and every test that validates it]]
- [[_COMMUNITY_H|H]]
- [[_COMMUNITY_Documentation index|Documentation index]]
- [[_COMMUNITY_PART A — Fully-FPGA RISC-V Linux platform|PART A — Fully-FPGA RISC-V Linux platform]]
- [[_COMMUNITY_BDHarness|BDHarness]]
- [[_COMMUNITY_Glossary|Glossary]]
- [[_COMMUNITY_MilanSimSoC|MilanSimSoC]]
- [[_COMMUNITY_drain|drain]]
- [[_COMMUNITY_Throughput goal — ≥200 Mbits RX and TX, reach for 1 Gbits|Throughput goal — ≥200 Mbit/s RX *and* TX, reach for 1 Gbit/s]]
- [[_COMMUNITY_HW-GRORSC — receive-side coalescing in the RX BD engine (design, 2026-07-07)|HW-GRO/RSC — receive-side coalescing in the RX BD engine (design, 2026-07-07)]]
- [[_COMMUNITY_sim_main.cpp|sim_main.cpp]]
- [[_COMMUNITY_milan_csr.sv|milan_csr.sv]]
- [[_COMMUNITY_Register groups|Register groups]]
- [[_COMMUNITY_RX overload wedge — completion-order inversion under RSC + ACK-merge FIXED in sim|RX overload wedge — completion-order inversion under RSC + ACK-merge [FIXED in sim]]]
- [[_COMMUNITY_RX memory-hierarchy plan — cold vs capacity, and the dedicated-network-cache decision|RX memory-hierarchy plan — cold vs capacity, and the dedicated-network-cache decision]]
- [[_COMMUNITY_tools_lat_mem_rd.c|tools_lat_mem_rd.c]]
- [[_COMMUNITY_milan_soc.py|milan_soc.py]]
- [[_COMMUNITY_perf_campaign_chart.py|perf_campaign_chart.py]]
- [[_COMMUNITY_SVG|SVG]]
- [[_COMMUNITY_Throughput goal — 500 Mbits RX and TX, reach for 1 Gbits|Throughput goal — >500 Mbit/s RX *and* TX, reach for 1 Gbit/s]]
- [[_COMMUNITY_Documentation index|Documentation index]]
- [[_COMMUNITY_Running the tests — the complete guide|Running the tests — the complete guide]]
- [[_COMMUNITY_Getting the maximum out of the gigabit link — headroom analysis at 100 MHz|Getting the maximum out of the gigabit link — headroom analysis at 100 MHz]]
- [[_COMMUNITY_test_rsc_ack_merge|test_rsc_ack_merge]]
- [[_COMMUNITY_RX  TX performance — what we improved, how, and what's next|RX / TX performance — what we improved, how, and what's next]]
- [[_COMMUNITY_StormModel|StormModel]]
- [[_COMMUNITY_tools_wakebench.c|tools_wakebench.c]]
- [[_COMMUNITY_Milan v1.2 → FRNFR dependency matrix|Milan v1.2 → FR/NFR dependency matrix]]
- [[_COMMUNITY_Profiling on the Milan board — method, and the misaligned-usercopy case study|Profiling on the Milan board — method, and the misaligned-usercopy case study]]
- [[_COMMUNITY_BDHarness|BDHarness]]
- [[_COMMUNITY_hsplit14  hsq12 — per-page (cut-through) hs delivery|hsplit14 / hsq12 — per-page (cut-through) hs delivery]]
- [[_COMMUNITY_De-Xilinx plan  -  replace XPMvendor IP with Alex Forencich open cores|De-Xilinx plan  -  replace XPM/vendor IP with Alex Forencich open cores]]
- [[_COMMUNITY_CPPI-style DMA redesign  -  on-chip descriptors, cut-through, zero-copy (plan)|CPPI-style DMA redesign  -  on-chip descriptors, cut-through, zero-copy (plan)]]
- [[_COMMUNITY_Simulation  -  how the Milan design is simulated and verified|Simulation  -  how the Milan design is simulated and verified]]
- [[_COMMUNITY_deploy.sh|deploy.sh]]
- [[_COMMUNITY_Attaching AXI-Stream FPGA cores to the NaxRiscv SoC|Attaching AXI-Stream FPGA cores to the NaxRiscv SoC]]
- [[_COMMUNITY_RX stages|RX stages]]
- [[_COMMUNITY_Second bug  -  TX-to-wire the 2026-07-04 investigation log (OPEN, bisection running)|Second bug  -  TX-to-wire: the 2026-07-04 investigation log (OPEN, bisection running)]]
- [[_COMMUNITY_Register groups|Register groups]]
- [[_COMMUNITY_TB|TB]]
- [[_COMMUNITY_CBS datapath bug  -  classifier `tdest` mis-timing under back-to-back frames FIXED|CBS datapath bug  -  classifier `tdest` mis-timing under back-to-back frames [FIXED]]]
- [[_COMMUNITY_Frame|Frame]]
- [[_COMMUNITY_RX ring DMA  -  root cause of the large-frame RX loss + the AXI-burst fix|RX ring DMA  -  root cause of the large-frame RX loss + the AXI-burst fix]]
- [[_COMMUNITY_RX fan-out & the TX throughput ceiling (2026-07-07)|RX fan-out & the TX throughput ceiling (2026-07-07)]]
- [[_COMMUNITY_TB|TB]]
- [[_COMMUNITY_Board porting  -  Alinx AX7101 (XC7A100T-2FGG484I)|Board porting  -  Alinx AX7101 (XC7A100T-2FGG484I)]]
- [[_COMMUNITY_TB|TB]]
- [[_COMMUNITY_Harness|Harness]]
- [[_COMMUNITY_test_rsc_ack_merge|test_rsc_ack_merge]]
- [[_COMMUNITY_IdealRef|IdealRef]]
- [[_COMMUNITY_Harness|Harness]]
- [[_COMMUNITY_FixedPointRef|FixedPointRef]]
- [[_COMMUNITY_LiteXModule|LiteXModule]]
- [[_COMMUNITY_SlopeEngineRef|SlopeEngineRef]]
- [[_COMMUNITY_Harness|Harness]]
- [[_COMMUNITY_Protocol validation matrix  -  every protocol, and every test that validates it|Protocol validation matrix  -  every protocol, and every test that validates it]]
- [[_COMMUNITY_CbsInputs|CbsInputs]]
- [[_COMMUNITY_Harness|Harness]]
- [[_COMMUNITY_Documentation index|Documentation index]]
- [[_COMMUNITY_TSN on FPGA — Requirements|TSN on FPGA — Requirements]]
- [[_COMMUNITY_CbsConfig|CbsConfig]]
- [[_COMMUNITY_CBS verification harness (IEEE 802.1Qav credit-based shaper)|CBS verification harness (IEEE 802.1Qav credit-based shaper)]]
- [[_COMMUNITY_build.sh|build.sh]]
- [[_COMMUNITY_cbs_ver_wrap|cbs_ver_wrap]]
- [[_COMMUNITY_credit_based_shaper.sv|credit_based_shaper.sv]]
- [[_COMMUNITY_M-A3 (partial) — DMA + AXIS-CDC data path on silicon (100 MHz, all-blocks)|M-A3 (partial) — DMA + AXIS-CDC data path on silicon (100 MHz, all-blocks)]]
- [[_COMMUNITY_test_axis_cobs_encode.py|test_axis_cobs_encode.py]]
- [[_COMMUNITY_test_axis_fifo_adapter.py|test_axis_fifo_adapter.py]]
- [[_COMMUNITY_REGISTER_MAP|REGISTER_MAP.md]]
- [[_COMMUNITY_sim_main.cpp|sim_main.cpp]]
- [[_COMMUNITY_test_axis_cobs_decode.py|test_axis_cobs_decode.py]]
- [[_COMMUNITY_TB|TB]]
- [[_COMMUNITY_tb_ptp_ts_core|tb_ptp_ts_core]]
- [[_COMMUNITY_sim_main.cpp|sim_main.cpp]]
- [[_COMMUNITY_properties|properties]]
- [[_COMMUNITY_sim_main.cpp|sim_main.cpp]]
- [[_COMMUNITY_test_axis_frame_length_adjust_fifo.py|test_axis_frame_length_adjust_fifo.py]]
- [[_COMMUNITY_tb_ptp_ts_top|tb_ptp_ts_top]]
- [[_COMMUNITY_sim_main.cpp|sim_main.cpp]]
- [[_COMMUNITY_test_axis_arb_mux.py|test_axis_arb_mux.py]]
- [[_COMMUNITY_AXIStreamSource|AXIStreamSource]]
- [[_COMMUNITY_test_axis_ram_switch.py|test_axis_ram_switch.py]]
- [[_COMMUNITY_test_axis_switch.py|test_axis_switch.py]]
- [[_COMMUNITY_sim_main.cpp|sim_main.cpp]]
- [[_COMMUNITY_object|object]]
- [[_COMMUNITY_reg|reg]]
- [[_COMMUNITY_test_axis_pipeline_register.py|test_axis_pipeline_register.py]]
- [[_COMMUNITY_TODO — TSN on FPGA|TODO — TSN on FPGA]]
- [[_COMMUNITY_FULL_FPGA_SOLUTION|FULL_FPGA_SOLUTION.md]]
- [[_COMMUNITY_milan_top|milan_top]]
- [[_COMMUNITY_milan_dt.py|milan_dt.py]]
- [[_COMMUNITY_RxSteer|RxSteer]]
- [[_COMMUNITY_TB|TB]]
- [[_COMMUNITY_TB|TB]]
- [[_COMMUNITY_TB|TB]]
- [[_COMMUNITY_LiteXModule|LiteXModule]]
- [[_COMMUNITY_window|window]]
- [[_COMMUNITY_avtp_adp_packet_gen|avtp_adp_packet_gen]]
- [[_COMMUNITY_avtp_random_subtype|avtp_random_subtype]]
- [[_COMMUNITY_TB|TB]]
- [[_COMMUNITY_TB|TB]]
- [[_COMMUNITY_TB|TB]]
- [[_COMMUNITY_AVDECC entity model (IEEE 1722.1-2021  Milan v1.2)|AVDECC entity model (IEEE 1722.1-2021 / Milan v1.2)]]
- [[_COMMUNITY_tb_top|tb_top]]
- [[_COMMUNITY_tb_traffic_classifier|tb_traffic_classifier]]
- [[_COMMUNITY_milan_datapath|milan_datapath]]
- [[_COMMUNITY_Entity ptp_ts_core|Entity: ptp_ts_core]]
- [[_COMMUNITY_MilanSimSoC|MilanSimSoC]]
- [[_COMMUNITY_avtp_alter_subtype|avtp_alter_subtype]]
- [[_COMMUNITY_avtp_stream_subtype|avtp_stream_subtype]]
- [[_COMMUNITY_sim_main.cpp|sim_main.cpp]]
- [[_COMMUNITY_TB|TB]]
- [[_COMMUNITY_TB|TB]]
- [[_COMMUNITY_OPEN_SOURCE_MIGRATION|OPEN_SOURCE_MIGRATION.md]]
- [[_COMMUNITY_Entity KL_avtp_common_parser|Entity: KL_avtp_common_parser]]
- [[_COMMUNITY_Entity traffic_classifier|Entity: traffic_classifier]]
- [[_COMMUNITY_`adp_advertiser` — ADP transmit engine (design doc)|`adp_advertiser` — ADP transmit engine (design doc)]]
- [[_COMMUNITY_ptp|ptp]]
- [[_COMMUNITY_properties|properties]]
- [[_COMMUNITY_avtp_control_subtype|avtp_control_subtype]]
- [[_COMMUNITY_tb_traffic_controller_802_1q|tb_traffic_controller_802_1q]]
- [[_COMMUNITY_sim_main.cpp|sim_main.cpp]]
- [[_COMMUNITY_AXIStreamSink|AXIStreamSink]]
- [[_COMMUNITY_Milan TSN FPGA  -  architecture & developer guide|Milan TSN FPGA  -  architecture & developer guide]]
- [[_COMMUNITY_Glossary|Glossary]]
- [[_COMMUNITY_Pipeline telemetry (`milan_tlm_`)  -  in-fabric observability for the TXRX path|Pipeline telemetry (`milan_tlm_*`)  -  in-fabric observability for the TX/RX path]]
- [[_COMMUNITY_cells|cells]]
- [[_COMMUNITY_items|items]]
- [[_COMMUNITY_ptp_ts_top|ptp_ts_top]]
- [[_COMMUNITY_Appendix A  -  Phase-0 counter spec (detailed, buildable)|Appendix A  -  Phase-0 counter spec (detailed, buildable)]]
- [[_COMMUNITY_Entity traffic_controller_802_1q|Entity: traffic_controller_802_1q]]
- [[_COMMUNITY_Entity traffic_queues|Entity: traffic_queues]]
- [[_COMMUNITY_Entity KL_adp_parser|Entity: KL_adp_parser]]
- [[_COMMUNITY_`tcam` — ternary CAM destination-MAC database (design doc)|`tcam` — ternary CAM destination-MAC database (design doc)]]
- [[_COMMUNITY_Entity ethernet_events|Entity: ethernet_events]]
- [[_COMMUNITY_milan-dt.schema.json|milan-dt.schema.json]]
- [[_COMMUNITY_properties|properties]]
- [[_COMMUNITY_queues|queues]]
- [[_COMMUNITY_avtp_base_packet_gen|avtp_base_packet_gen]]
- [[_COMMUNITY_axis_ep.py|axis_ep.py]]
- [[_COMMUNITY_ll_ep.py|ll_ep.py]]
- [[_COMMUNITY_find_vivado_settings|find_vivado_settings]]
- [[_COMMUNITY_AVB_SWITCH_DIRECTION.gen.py|AVB_SWITCH_DIRECTION.gen.py]]
- [[_COMMUNITY_RX_RING_OPERATION.gen.py|RX_RING_OPERATION.gen.py]]
- [[_COMMUNITY_Entity credit_based_shaper|Entity: credit_based_shaper]]
- [[_COMMUNITY_Entity traffic_shaping_core|Entity: traffic_shaping_core]]
- [[_COMMUNITY_traffic_controller_802_1q|traffic_controller_802_1q]]
- [[_COMMUNITY_Entity milan_csr|Entity: milan_csr]]
- [[_COMMUNITY_Entity event_counter|Entity: event_counter]]
- [[_COMMUNITY_Entity ptp_ts_top|Entity: ptp_ts_top]]
- [[_COMMUNITY_Entity timestamp_counter|Entity: timestamp_counter]]
- [[_COMMUNITY_tb_traffic_queues|tb_traffic_queues]]
- [[_COMMUNITY_Platform|Platform]]
- [[_COMMUNITY_`sw` — boot one RISC-V core with the Milan NIC + driver|`sw/` — boot one RISC-V core with the Milan NIC + driver]]
- [[_COMMUNITY_CBS default-shaping bug  -  reset config paced ALL best-effort TX at 300 Mbs FIXED|CBS default-shaping bug  -  reset config paced ALL best-effort TX at 300 Mb/s [FIXED]]]
- [[_COMMUNITY_RX_RING_DMA.gen.py|RX_RING_DMA.gen.py]]
- [[_COMMUNITY_TX_STARVATION_FIX.gen.py|TX_STARVATION_FIX.gen.py]]
- [[_COMMUNITY_traffic_classifier|traffic_classifier]]
- [[_COMMUNITY_milan-fpga documentation overhaul — how to apply & what changed|milan-fpga documentation overhaul — how to apply & what changed]]
- [[_COMMUNITY_`kl-eth` — Milan TSN NIC Linux driver|`kl-eth` — Milan TSN NIC Linux driver]]
- [[_COMMUNITY_`swdts` — platform-convergent device tree for the Milan NIC|`sw/dts/` — platform-convergent device tree for the Milan NIC]]
- [[_COMMUNITY_sim_main.cpp|sim_main.cpp]]
- [[_COMMUNITY_test_axis_cobs_decode.py|test_axis_cobs_decode.py]]
- [[_COMMUNITY_test_axis_cobs_encode.py|test_axis_cobs_encode.py]]
- [[_COMMUNITY_test_axis_cobs_encode_zero_frame.py|test_axis_cobs_encode_zero_frame.py]]
- [[_COMMUNITY_avtp_packet_gen_pkg.svh|avtp_packet_gen_pkg.svh]]
- [[_COMMUNITY_avtp_stream_parser.sv|avtp_stream_parser.sv]]
- [[_COMMUNITY_ptp_ts_core|ptp_ts_core]]
- [[_COMMUNITY_LiteX-ecosystem patches|LiteX-ecosystem patches]]
- [[_COMMUNITY_README|README.md]]
- [[_COMMUNITY_tb_traffic_shaping_core|tb_traffic_shaping_core]]
- [[_COMMUNITY_controller_rate_wrap|controller_rate_wrap]]
- [[_COMMUNITY_shaper_core_wrap|shaper_core_wrap]]
- [[_COMMUNITY_KL_avtp_common_parser.sv|KL_avtp_common_parser.sv]]
- [[_COMMUNITY_milan-fpga — IEEE 1722  1722.1  Milan v1.2 on FPGA|milan-fpga — IEEE 1722 / 1722.1 / Milan v1.2 on FPGA]]
- [[_COMMUNITY_tb_top.sv|tb_top.sv]]
- [[_COMMUNITY_cdc_tb_top|cdc_tb_top]]
- [[_COMMUNITY_sim_main.cpp|sim_main.cpp]]
- [[_COMMUNITY_classifier_wrap|classifier_wrap]]
- [[_COMMUNITY_CSR verification harness (`milan_csr` AXI4-Lite control plane)|CSR verification harness (`milan_csr` AXI4-Lite control plane)]]
- [[_COMMUNITY_datapath_wrap|datapath_wrap]]
- [[_COMMUNITY_sim_main.cpp|sim_main.cpp]]
- [[_COMMUNITY_queues_wrap|queues_wrap]]
- [[_COMMUNITY_axis_frame_length_adjust_fifo|axis_frame_length_adjust_fifo]]
- [[_COMMUNITY_test_axis_broadcast_4|test_axis_broadcast_4]]
- [[_COMMUNITY_test_axis_cobs_decode|test_axis_cobs_decode]]
- [[_COMMUNITY_test_axis_frame_join_4|test_axis_frame_join_4]]
- [[_COMMUNITY_test_axis_ll_bridge|test_axis_ll_bridge]]
- [[_COMMUNITY_test_axis_stat_counter|test_axis_stat_counter]]
- [[_COMMUNITY_traffic_class_map.sv|traffic_class_map.sv]]
- [[_COMMUNITY_traffic_queues|traffic_queues]]
- [[_COMMUNITY_traffic_shaping_core.sv|traffic_shaping_core.sv]]
- [[_COMMUNITY_adp_advertiser.sv|adp_advertiser.sv]]
- [[_COMMUNITY_KL_adp_parser.sv|KL_adp_parser.sv]]
- [[_COMMUNITY_milan_dma_wrapper|milan_dma_wrapper]]
- [[_COMMUNITY_rx_mac_filter|rx_mac_filter]]
- [[_COMMUNITY_test_ll_axis_bridge|test_ll_axis_bridge]]
- [[_COMMUNITY_apply.sh|apply.sh]]
- [[_COMMUNITY__hs_init|_hs_init]]
- [[_COMMUNITY_run.sh|run.sh]]
- [[_COMMUNITY_tb_ethernet_events|tb_ethernet_events]]
- [[_COMMUNITY_tb_timestamp_counter|tb_timestamp_counter]]
- [[_COMMUNITY_arbiter|arbiter]]
- [[_COMMUNITY_axis_arb_mux|axis_arb_mux]]
- [[_COMMUNITY_axis_arb_mux_wrap.py|axis_arb_mux_wrap.py]]
- [[_COMMUNITY_axis_broadcast_wrap.py|axis_broadcast_wrap.py]]
- [[_COMMUNITY_axis_cobs_encode|axis_cobs_encode]]
- [[_COMMUNITY_axis_crosspoint_wrap.py|axis_crosspoint_wrap.py]]
- [[_COMMUNITY_axis_demux_wrap.py|axis_demux_wrap.py]]
- [[_COMMUNITY_axis_frame_join_wrap.py|axis_frame_join_wrap.py]]
- [[_COMMUNITY_axis_mux_wrap.py|axis_mux_wrap.py]]
- [[_COMMUNITY_axis_ram_switch_wrap.py|axis_ram_switch_wrap.py]]
- [[_COMMUNITY_axis_switch_wrap.py|axis_switch_wrap.py]]
- [[_COMMUNITY_bench|bench]]
- [[_COMMUNITY_bench|bench]]
- [[_COMMUNITY_test_arbiter_rr|test_arbiter_rr]]
- [[_COMMUNITY_test_arbiter|test_arbiter]]
- [[_COMMUNITY_test_axis_adapter_64_8.py|test_axis_adapter_64_8.py]]
- [[_COMMUNITY_test_axis_adapter_64_8|test_axis_adapter_64_8]]
- [[_COMMUNITY_test_axis_adapter_8_64.py|test_axis_adapter_8_64.py]]
- [[_COMMUNITY_test_axis_adapter_8_64|test_axis_adapter_8_64]]
- [[_COMMUNITY_test_axis_arb_mux_4_64.py|test_axis_arb_mux_4_64.py]]
- [[_COMMUNITY_test_axis_arb_mux_4_64|test_axis_arb_mux_4_64]]
- [[_COMMUNITY_test_axis_arb_mux_4.py|test_axis_arb_mux_4.py]]
- [[_COMMUNITY_test_axis_arb_mux_4|test_axis_arb_mux_4]]
- [[_COMMUNITY_test_axis_async_fifo_64.py|test_axis_async_fifo_64.py]]
- [[_COMMUNITY_test_axis_async_fifo_64|test_axis_async_fifo_64]]
- [[_COMMUNITY_test_axis_async_fifo_adapter_64_8.py|test_axis_async_fifo_adapter_64_8.py]]
- [[_COMMUNITY_test_axis_async_fifo_adapter_64_8|test_axis_async_fifo_adapter_64_8]]
- [[_COMMUNITY_test_axis_async_fifo_adapter_8_64.py|test_axis_async_fifo_adapter_8_64.py]]
- [[_COMMUNITY_test_axis_async_fifo_adapter_8_64|test_axis_async_fifo_adapter_8_64]]
- [[_COMMUNITY_test_axis_async_fifo.py|test_axis_async_fifo.py]]
- [[_COMMUNITY_test_axis_async_fifo|test_axis_async_fifo]]
- [[_COMMUNITY_test_axis_async_frame_fifo_64.py|test_axis_async_frame_fifo_64.py]]
- [[_COMMUNITY_test_axis_async_frame_fifo_64|test_axis_async_frame_fifo_64]]
- [[_COMMUNITY_test_axis_async_frame_fifo.py|test_axis_async_frame_fifo.py]]
- [[_COMMUNITY_test_axis_async_frame_fifo|test_axis_async_frame_fifo]]
- [[_COMMUNITY_test_axis_broadcast_4.py|test_axis_broadcast_4.py]]
- [[_COMMUNITY_test_axis_cobs_encode|test_axis_cobs_encode]]
- [[_COMMUNITY_test_axis_cobs_encode_zero_frame|test_axis_cobs_encode_zero_frame]]
- [[_COMMUNITY_test_axis_crosspoint_4x4_64.py|test_axis_crosspoint_4x4_64.py]]
- [[_COMMUNITY_test_axis_crosspoint_4x4_64|test_axis_crosspoint_4x4_64]]
- [[_COMMUNITY_test_axis_crosspoint_4x4.py|test_axis_crosspoint_4x4.py]]
- [[_COMMUNITY_test_axis_crosspoint_4x4|test_axis_crosspoint_4x4]]
- [[_COMMUNITY_test_axis_demux_4_64.py|test_axis_demux_4_64.py]]
- [[_COMMUNITY_test_axis_demux_4_64|test_axis_demux_4_64]]
- [[_COMMUNITY_test_axis_demux_4.py|test_axis_demux_4.py]]
- [[_COMMUNITY_test_axis_demux_4|test_axis_demux_4]]
- [[_COMMUNITY_test_axis_fifo_64.py|test_axis_fifo_64.py]]
- [[_COMMUNITY_test_axis_fifo_64|test_axis_fifo_64]]
- [[_COMMUNITY_test_axis_fifo_adapter_64_8.py|test_axis_fifo_adapter_64_8.py]]
- [[_COMMUNITY_test_axis_fifo_adapter_64_8|test_axis_fifo_adapter_64_8]]
- [[_COMMUNITY_test_axis_fifo_adapter_8_64.py|test_axis_fifo_adapter_8_64.py]]
- [[_COMMUNITY_test_axis_fifo_adapter_8_64|test_axis_fifo_adapter_8_64]]
- [[_COMMUNITY_test_axis_fifo.py|test_axis_fifo.py]]
- [[_COMMUNITY_test_axis_fifo|test_axis_fifo]]
- [[_COMMUNITY_test_axis_frame_fifo_64.py|test_axis_frame_fifo_64.py]]
- [[_COMMUNITY_test_axis_frame_fifo_64|test_axis_frame_fifo_64]]
- [[_COMMUNITY_test_axis_frame_fifo.py|test_axis_frame_fifo.py]]
- [[_COMMUNITY_test_axis_frame_fifo|test_axis_frame_fifo]]
- [[_COMMUNITY_test_axis_frame_len_64.py|test_axis_frame_len_64.py]]
- [[_COMMUNITY_test_axis_frame_len_64|test_axis_frame_len_64]]
- [[_COMMUNITY_test_axis_frame_len_8.py|test_axis_frame_len_8.py]]
- [[_COMMUNITY_test_axis_frame_len_8|test_axis_frame_len_8]]
- [[_COMMUNITY_test_axis_frame_length_adjust_64.py|test_axis_frame_length_adjust_64.py]]
- [[_COMMUNITY_test_axis_frame_length_adjust_64|test_axis_frame_length_adjust_64]]
- [[_COMMUNITY_test_axis_frame_length_adjust_8.py|test_axis_frame_length_adjust_8.py]]
- [[_COMMUNITY_test_axis_frame_length_adjust_8|test_axis_frame_length_adjust_8]]
- [[_COMMUNITY_test_axis_frame_length_adjust_fifo_64.py|test_axis_frame_length_adjust_fifo_64.py]]
- [[_COMMUNITY_test_axis_frame_length_adjust_fifo_64|test_axis_frame_length_adjust_fifo_64]]
- [[_COMMUNITY_test_axis_frame_length_adjust_fifo.py|test_axis_frame_length_adjust_fifo.py]]
- [[_COMMUNITY_test_axis_frame_length_adjust_fifo|test_axis_frame_length_adjust_fifo]]
- [[_COMMUNITY_test_axis_mux_4_64.py|test_axis_mux_4_64.py]]
- [[_COMMUNITY_test_axis_mux_4_64|test_axis_mux_4_64]]
- [[_COMMUNITY_test_axis_mux_4|test_axis_mux_4]]
- [[_COMMUNITY_test_axis_ram_switch_1x4_256_64.py|test_axis_ram_switch_1x4_256_64.py]]
- [[_COMMUNITY_test_axis_ram_switch_1x4_256_64|test_axis_ram_switch_1x4_256_64]]
- [[_COMMUNITY_test_axis_ram_switch_4x1_64_256.py|test_axis_ram_switch_4x1_64_256.py]]
- [[_COMMUNITY_test_axis_ram_switch_4x1_64_256|test_axis_ram_switch_4x1_64_256]]
- [[_COMMUNITY_test_axis_ram_switch_4x4_64_64.py|test_axis_ram_switch_4x4_64_64.py]]
- [[_COMMUNITY_test_axis_ram_switch_4x4_64_64|test_axis_ram_switch_4x4_64_64]]
- [[_COMMUNITY_test_axis_rate_limit_64.py|test_axis_rate_limit_64.py]]
- [[_COMMUNITY_test_axis_rate_limit_64|test_axis_rate_limit_64]]
- [[_COMMUNITY_test_axis_rate_limit.py|test_axis_rate_limit.py]]
- [[_COMMUNITY_test_axis_rate_limit|test_axis_rate_limit]]
- [[_COMMUNITY_test_axis_register_64.py|test_axis_register_64.py]]
- [[_COMMUNITY_test_axis_register_64|test_axis_register_64]]
- [[_COMMUNITY_test_axis_register.py|test_axis_register.py]]
- [[_COMMUNITY_test_axis_register|test_axis_register]]
- [[_COMMUNITY_test_axis_srl_fifo_64.py|test_axis_srl_fifo_64.py]]
- [[_COMMUNITY_test_axis_srl_fifo_64|test_axis_srl_fifo_64]]
- [[_COMMUNITY_test_axis_srl_fifo.py|test_axis_srl_fifo.py]]
- [[_COMMUNITY_test_axis_srl_fifo|test_axis_srl_fifo]]
- [[_COMMUNITY_test_axis_srl_register_64.py|test_axis_srl_register_64.py]]
- [[_COMMUNITY_test_axis_srl_register_64|test_axis_srl_register_64]]
- [[_COMMUNITY_test_axis_srl_register.py|test_axis_srl_register.py]]
- [[_COMMUNITY_test_axis_srl_register|test_axis_srl_register]]
- [[_COMMUNITY_test_axis_stat_counter.py|test_axis_stat_counter.py]]
- [[_COMMUNITY_test_axis_switch_4x4_64.py|test_axis_switch_4x4_64.py]]
- [[_COMMUNITY_test_axis_switch_4x4_64|test_axis_switch_4x4_64]]
- [[_COMMUNITY_test_axis_switch_4x4.py|test_axis_switch_4x4.py]]
- [[_COMMUNITY_test_axis_switch_4x4|test_axis_switch_4x4]]
- [[_COMMUNITY_test_axis_tap_64.py|test_axis_tap_64.py]]
- [[_COMMUNITY_test_axis_tap_64|test_axis_tap_64]]
- [[_COMMUNITY_test_axis_tap.py|test_axis_tap.py]]
- [[_COMMUNITY_test_axis_tap|test_axis_tap]]
- [[_COMMUNITY_bench|bench]]
- [[_COMMUNITY_test_priority_encoder|test_priority_encoder]]
- [[_COMMUNITY_adp_tx_arbiter.sv|adp_tx_arbiter.sv]]
- [[_COMMUNITY_axis_mux_rr_2in_1out.sv|axis_mux_rr_2in_1out.sv]]
- [[_COMMUNITY_cdc_handshake.sv|cdc_handshake.sv]]
- [[_COMMUNITY_cdc_pulse.sv|cdc_pulse.sv]]
- [[_COMMUNITY_tcam.sv|tcam.sv]]
- [[_COMMUNITY_ethernet_events|ethernet_events]]
- [[_COMMUNITY_event_counter.sv|event_counter.sv]]
- [[_COMMUNITY_ptp_csr_sync.sv|ptp_csr_sync.sv]]
- [[_COMMUNITY_timestamp_counter.sv|timestamp_counter.sv]]
- [[_COMMUNITY_.rd_sync|.rd_sync]]
- [[_COMMUNITY_tcp_tagged|tcp_tagged]]
- [[_COMMUNITY_test_bd_ring_full_gate|test_bd_ring_full_gate]]
- [[_COMMUNITY_top.sv|top.sv]]
- [[_COMMUNITY_avtp_alter_pkg.sv|avtp_alter_pkg.sv]]
- [[_COMMUNITY_avtp_control_pkg.sv|avtp_control_pkg.sv]]
- [[_COMMUNITY_avtp_stream_pkg.sv|avtp_stream_pkg.sv]]
- [[_COMMUNITY_axi_stream_driver.svh|axi_stream_driver.svh]]
- [[_COMMUNITY_README|README.md]]
- [[_COMMUNITY_axis_adapter.v|axis_adapter.v]]
- [[_COMMUNITY_axis_async_fifo_adapter|axis_async_fifo_adapter]]
- [[_COMMUNITY_axis_broadcast.v|axis_broadcast.v]]
- [[_COMMUNITY_axis_cobs_decode.v|axis_cobs_decode.v]]
- [[_COMMUNITY_axis_crosspoint.v|axis_crosspoint.v]]
- [[_COMMUNITY_axis_demux.v|axis_demux.v]]
- [[_COMMUNITY_axis_fifo.v|axis_fifo.v]]
- [[_COMMUNITY_axis_fifo_adapter|axis_fifo_adapter]]
- [[_COMMUNITY_axis_frame_join.v|axis_frame_join.v]]
- [[_COMMUNITY_axis_frame_len.v|axis_frame_len.v]]
- [[_COMMUNITY_axis_frame_length_adjust.v|axis_frame_length_adjust.v]]
- [[_COMMUNITY_axis_ll_bridge.v|axis_ll_bridge.v]]
- [[_COMMUNITY_axis_mux.v|axis_mux.v]]
- [[_COMMUNITY_axis_pipeline_fifo.v|axis_pipeline_fifo.v]]
- [[_COMMUNITY_axis_pipeline_register|axis_pipeline_register]]
- [[_COMMUNITY_axis_ram_switch|axis_ram_switch]]
- [[_COMMUNITY_axis_rate_limit.v|axis_rate_limit.v]]
- [[_COMMUNITY_axis_register.v|axis_register.v]]
- [[_COMMUNITY_axis_srl_fifo.v|axis_srl_fifo.v]]
- [[_COMMUNITY_axis_srl_register.v|axis_srl_register.v]]
- [[_COMMUNITY_axis_stat_counter.v|axis_stat_counter.v]]
- [[_COMMUNITY_axis_switch|axis_switch]]
- [[_COMMUNITY_axis_tap.v|axis_tap.v]]
- [[_COMMUNITY_ll_axis_bridge.v|ll_axis_bridge.v]]
- [[_COMMUNITY_sync_reset.v|sync_reset.v]]
- [[_COMMUNITY_vector|vector]]
- [[_COMMUNITY_Verilator verification harnesses|Verilator verification harnesses]]

## God Nodes (most connected - your core abstractions)
1. `BDHarness` - 42 edges
2. `Documentation` - 34 edges
3. `FixedPointRef` - 24 edges
4. `IdealRef` - 24 edges
5. `TB` - 22 edges
6. `TB` - 22 edges
7. `Troubleshooting  -  every problem hit bringing up the full-FPGA solution, and its fix` - 20 edges
8. `Harness` - 18 edges
9. `Harness` - 18 edges
10. `MilanDebug` - 17 edges

## Surprising Connections (you probably didn't know these)
- `test_bd_zero_copy()` --calls--> `frame()`  [INFERRED]
  sw/litex/test_ring_bd.py → sw/litex/test_ring_dma.py
- `test_bd_no_buffer_drop()` --calls--> `frame()`  [INFERRED]
  sw/litex/test_ring_bd.py → sw/litex/test_ring_dma.py
- `test_bd_ring_wrap()` --calls--> `frame()`  [INFERRED]
  sw/litex/test_ring_bd.py → sw/litex/test_ring_dma.py
- `test_bd_ring_full_gate()` --calls--> `frame()`  [INFERRED]
  sw/litex/test_ring_bd.py → sw/litex/test_ring_dma.py
- `test_bd_large_frame_content()` --calls--> `frame()`  [INFERRED]
  sw/litex/test_ring_bd.py → sw/litex/test_ring_dma.py

## Import Cycles
- 1-file cycle: `hdl/common/milan_datapath.sv -> hdl/common/milan_datapath.sv`
- 1-file cycle: `hdl/common/milan_top.sv -> hdl/common/milan_top.sv`
- 1-file cycle: `hdl/1722/KL_avtp_common_parser.sv -> hdl/1722/KL_avtp_common_parser.sv`
- 1-file cycle: `hdl/1722/avtp_stream_parser.sv -> hdl/1722/avtp_stream_parser.sv`
- 1-file cycle: `hdl/802_1q_traffic_shaper/credit_based_shaper.sv -> hdl/802_1q_traffic_shaper/credit_based_shaper.sv`
- 1-file cycle: `hdl/802_1q_traffic_shaper/traffic_class_map.sv -> hdl/802_1q_traffic_shaper/traffic_class_map.sv`
- 1-file cycle: `hdl/802_1q_traffic_shaper/traffic_classifier.sv -> hdl/802_1q_traffic_shaper/traffic_classifier.sv`
- 1-file cycle: `hdl/802_1q_traffic_shaper/traffic_controller_802_1q.sv -> hdl/802_1q_traffic_shaper/traffic_controller_802_1q.sv`
- 1-file cycle: `hdl/802_1q_traffic_shaper/traffic_shaping_core.sv -> hdl/802_1q_traffic_shaper/traffic_shaping_core.sv`
- 1-file cycle: `hdl/adp/KL_adp_parser.sv -> hdl/adp/KL_adp_parser.sv`
- 1-file cycle: `hdl/adp/adp_advertiser.sv -> hdl/adp/adp_advertiser.sv`
- 1-file cycle: `hdl/ptp_timestamp/ptp_ts_core.sv -> hdl/ptp_timestamp/ptp_ts_core.sv`
- 1-file cycle: `tb/avtp_packet_gen_sv/pkgs/avtp_alter_pkg.sv -> tb/avtp_packet_gen_sv/pkgs/avtp_alter_pkg.sv`
- 1-file cycle: `tb/avtp_packet_gen_sv/pkgs/avtp_control_pkg.sv -> tb/avtp_packet_gen_sv/pkgs/avtp_control_pkg.sv`
- 1-file cycle: `tb/avtp_packet_gen_sv/pkgs/avtp_stream_pkg.sv -> tb/avtp_packet_gen_sv/pkgs/avtp_stream_pkg.sv`
- 1-file cycle: `tb/avtp_packet_gen_sv/tb_classes/avtp_packet_gen_pkg.svh -> tb/avtp_packet_gen_sv/tb_classes/avtp_packet_gen_pkg.svh`
- 1-file cycle: `tb/itests/802_1q_traffic_shaper/tb_traffic_controller_802_1q.sv -> tb/itests/802_1q_traffic_shaper/tb_traffic_controller_802_1q.sv`
- 1-file cycle: `tb/utests/802_1q_traffic_shaper/tb_traffic_classifier.sv -> tb/utests/802_1q_traffic_shaper/tb_traffic_classifier.sv`
- 1-file cycle: `tb/utests/802_1q_traffic_shaper/tb_traffic_queues.sv -> tb/utests/802_1q_traffic_shaper/tb_traffic_queues.sv`
- 1-file cycle: `tb/utests/802_1q_traffic_shaper/tb_traffic_shaping_core.sv -> tb/utests/802_1q_traffic_shaper/tb_traffic_shaping_core.sv`

## Communities (393 total, 184 thin omitted)

### Community 0 - "milan_soc.py"
Cohesion: 0.05
Nodes (38): `arbiter` module, AXI Stream Interface Example, `axis_adapter` module, `axis_arb_mux` module, `axis_async_fifo_adapter` module, `axis_async_fifo` module, `axis_broadcast` module, `axis_cobs_decode` (+30 more)

### Community 1 - "H"
Cohesion: 0.20
Nodes (9): 1. Usage, 2. The named configurations, 3. The launch discipline (why the script is not just a for-loop), 4. After the build: load + console, per board, 5. Gates before a build is "good", Adding a configuration, `arty`  -  Digilent Arty A7-100, the second Milan node, `ax7101`  -  Alinx AX7101, the perf/ship platform (+1 more)

### Community 2 - "Milan v1.2 endpoint — Functional & Non-Functional Requirements (FR/NFR)"
Cohesion: 0.06
Nodes (32): 1.1 Baseline (the "small" endpoint), 1.2 Scaling parameters (referenced throughout), 1.3 Actors, 1. Scope, actors, and the baseline system, 2.10 Host Linux driver  *(Phase 7 / `REQ-DRV-*`; needs a kernel tree  -  not buildable in this repo)*, 2.11 Device tree  *(Phase 8 / `REQ-DT-*`; the DT contract the driver binds to)*, 2.1 Discovery  -  ADP  *(1722.1-2021 §6; Milan v1.2 §5.2)*, 2.2 Enumeration & control  -  AECP/AEM  *(1722.1-2021 §7,§9; Milan v1.2 §5.3–5.4)* (+24 more)

### Community 3 - "Troubleshooting — every problem hit bringing up the full-FPGA solution, and its fix"
Cohesion: 0.14
Nodes (14): 1. What the full-FPGA solution is (high level), 2. The protocol stack (high level), 3. Status at a glance, 4. Repository map (medium level), 5.1 Control  -  `milan_csr` (AXI4-Lite), 5.2 Data  -  `MilanDMA` (§A.6, `--with-dma`), 5.3 MAC  -  `MilanMAC` (§A.7, `--with-mac`), 5.4 Events  -  IRQ → PLIC (+6 more)

### Community 4 - "README.md"
Cohesion: 0.09
Nodes (24): DriverModel, _mk_overload_harness(), DriverModel + content/conservation accounting (invariants I1/I2)., reap() plus content verification of every completion., Seeded silicon-realistic RSC storm vs invariants I1/I2/I3., Storm at REAL silicon geometry: 1448-byte MSS segs (183 beats — deep multi-burst, M1 telemetry (CAMPAIGN_500_PLAN): the close-reason counters + coalesce ratio, tcp_frame variant with a settable source port (multi-flow) at doff=5 (so     pay (+16 more)

### Community 5 - "Latency & memory investigation — why single-port TCP caps at 30 Mbit/s (2026-07-05)"
Cohesion: 0.13
Nodes (15): 10. What changed this session, 11. Status & next steps, 1. The contradiction that drove everything, 2. What it is NOT (each ruled out by measurement), 3. The two regimes  -  flood localises the ceiling, 4.1 Decomposing the 1424 ns  -  TLB vs DRAM (hugepage A/B), 4. Root cause  -  memory latency (the 14k-pps ceiling), 5. The poll-CSR cost (why backing off the poll helps +32 %) (+7 more)

### Community 6 - "MilanDebug"
Cohesion: 0.12
Nodes (27): Harness, BDHarness, _csum_ref(), _fold_nc(), _ip_check(), _lanes(), _mk_template(), v2 realign: segment addresses at every offset 0..7 (Ethernet's skb->data is (+19 more)

### Community 7 - "Direction: from the 1-NIC endpoint to a 4-port AVB switch (MTU fixed at 1500)"
Cohesion: 0.14
Nodes (14): CPU budget vs the 4-port switch (measured 2026-07-05, xc7a100t = 63,400 LUTs), Decision matrix (2026-07-05, scope: **4× GMII/RGMII copper ports**, MTU fixed 1500), Direction: from the 1-NIC endpoint to a 4-port AVB switch (MTU fixed at 1500), Execution order, Hardware reality, Memory: "would a wider bus help?" (panel ④), Step plan for the executed session (C1/C2/I1), The constraint set (+6 more)

### Community 8 - "TX RingDMAReader prefetch — design plan (roadmap step 1, primary TX lever)"
Cohesion: 0.17
Nodes (11): 1. Results  -  where everything stands, 2. Topology  -  what plugs into what, 3. How to connect, 4. How to harness, AREA-70 campaign: CLOSED (silicon keeper = build_cbsf_epo), Arty A7-100 (second Milan node)  -  port done, bring-up in progress, Hardening shipped, Milan product plane (the AVB-switch era, started 2026-07-11) (+3 more)

### Community 9 - "2. Functional Requirements (FR)"
Cohesion: 0.10
Nodes (20): Section 10: Yosys / sv2v cannot find axis_mux_rr_2in_1out, Section 11: milan_dp AXI-write BFM did not commit writes, Section 12: Benign Verilator warnings (PINMISSING and SELRANGE), Section 13: traffic_queues silently dropped a frame, Section 14: datapath harness "≥2 queues" assertion failed, Section 15: `--full` fails 100 MHz timing in the CBS credit-shaper, Section 16: clean 100 MHz  -  run the dense datapath in its own clock domain, Section 17: on-hardware NIC bring-up  -  DMA works, but no packet on the wire (it's GMII, not RGMII) (+12 more)

### Community 10 - "MilanDebug"
Cohesion: 0.12
Nodes (14): MilanDebug, Memory-mapped observability for the whole TX+RX AXIS pipeline  -  the numbers a, Latch `live` into a shadow on `capture` and expose it as a CSR., frames / beats / stalls at a sys-domain AXIS endpoint. Returns the frame counter, busy/stall/starve/cyc at a datapath-input endpoint in domain `cd`, to sys., Frame count at an endpoint in clock domain `cd`, brought to sys and captured., Count only frames for which `match` (held over the frame) is asserted at `last`., Count frames whose (untagged) EtherType == `etype`. `ep` must carry `.data` (+6 more)

### Community 11 - "PART B — ADP / AVDECC (the complete AVB solution)"
Cohesion: 0.06
Nodes (36): 0. Decisions & assumptions (confirm before starting), 1.1 What the PL already owns (reuse as-is), 1.2 What the Zynq PS provides today (must be re-created in fabric), 1.3 The one hard consequence of removing the PS, 1. Why this is a "port the host, keep the datapath" job, 3. Effort, risk, and ordering, 4. What changes in the repo (file-level), 5. Open items to confirm (+28 more)

### Community 12 - "Protocol validation matrix — every protocol, and every test that validates it"
Cohesion: 0.06
Nodes (35): A generic Getter/Setter, AECP Command Specific Extract, AECP Common Data Parser, AECP L0 Current Selected Configuration, AECP Memory Mapped module, AECP Packet response, AECP Packet Validation, AECP Specific Data Parser (+27 more)

### Community 13 - "H"
Cohesion: 0.35
Nodes (7): arp_frame(), H, reassemble queue qi's beats into frames (bytes)., ref_hash(), tcp_frame(), test_nonip_and_bypass(), test_route_and_consistency()

### Community 14 - "Documentation index"
Cohesion: 0.18
Nodes (11): Bottom line for the switch, Levers that *would* move single-flow throughput  -  and why they're out, Matrix 1  -  baseline single flow, Matrix 2  -  RX-coalesce (poll-cadence) sweep, Matrix 3  -  parallel streams (does the ceiling aggregate?), Reproduce, Root cause  -  a per-frame *latency* ceiling, not a *throughput* one, Single-port throughput on VexiiRiscv  -  what a second core would (not) buy (+3 more)

### Community 15 - "PART A — Fully-FPGA RISC-V Linux platform"
Cohesion: 0.38
Nodes (3): capture(), reset_ctrs(), phase0_measure.sh script

### Community 16 - "BDHarness"
Cohesion: 0.07
Nodes (27): Campaign plan: >500 Mbit/s TX *and* RX  -  every step gated by a gateware measurement, DECISION (2026-07-08): stay at 100 MHz; next lever = L2/memory, Existing gateware measurement surface (validated this campaign), Gate summary (the plan on one line each), Phase M1  -  instrumentation build (FIRST: the probes the plan needs), Phase R0  -  full re-baseline on the instrumented, storm-proof gateware, Phase R1  -  RX 2-queue fan-out at 100 MHz (the mandatory RX lever), Phase R2  -  RX per-aggregate cost: RSC geometry + delivery tuning (+19 more)

### Community 17 - "Glossary"
Cohesion: 0.17
Nodes (14): THE parallel-storm delivery death (silicon 2026-07-08, decoded off the dead, test_bd_drops_overflow_v2_alias(), frame(), Harness, Wait until nothing is buffered AND wr_ptr has been stable for `settle` cycles, Ones-complement sum of 16-bit LE lanes — what the ingress must deliver., Walk `count` committed frames from ring offset rd; return (frames, seqs, rd)., One DUT + AXI-slave memory model + always-ready monitor, driven per scenario. (+6 more)

### Community 18 - "MilanSimSoC"
Cohesion: 0.13
Nodes (15): 2026-07-06: zero-upload ACHIEVED  -  the sizes that made "full" fit, Build a flash-boot bitstream, Caveats, Field notes (2026-07-10 silicon session), Flash layout (`FLASHBOOT_LAYOUT` in `milan_soc.py`), Flash the kernel once (partial mode), Getting to zero-upload, How the boot works (+7 more)

### Community 19 - "drain"
Cohesion: 0.60
Nodes (4): drain(), Feed n_frames back-to-back; return (cycles_to_drain, wr, drops, shadow_word)., test_writeback_bandwidth(), test_writeback_correctness()

### Community 21 - "Throughput goal — ≥200 Mbit/s RX *and* TX, reach for 1 Gbit/s"
Cohesion: 0.14
Nodes (14): 0. Phase 0  -  measure the assumptions first (this gates everything below), 1. The problem, from the measurement, 2. Root cause, from the RTL, 3. Why it is viable (no blockers at the bus level), 4. Expected win (depth → duty)  -  a **model**, to be set by Phase-0 measurement, 5. Design, 6. What does **not** change, 7. Sim strategy (must land before any build) (+6 more)

### Community 22 - "HW-GRO/RSC — receive-side coalescing in the RX BD engine (design, 2026-07-07)"
Cohesion: 0.10
Nodes (20): ACK-run merging  -  LIVE on silicon (2026-07-07): TX 109 → 121, As-built rules  -  where the implementation pins down (or diverges from) the spec text, BD format v2 (16 B, LE)  -  merged aggregates, Buffer/write path, Driver contract, Driver robustness (the-private-test-repo `85122fa`), HW-GRO/RSC  -  receive-side coalescing in the RX BD engine (design, 2026-07-07), Implementation status (2026-07-07)  -  phases A+B DONE, sim-verified (+12 more)

### Community 23 - "sim_main.cpp"
Cohesion: 0.73
Nodes (5): axi_read(), axi_write(), ck(), main(), posedge()

### Community 26 - "RX overload wedge — completion-order inversion under RSC + ACK-merge [FIXED in sim]"
Cohesion: 0.18
Nodes (11): Defense in depth (driver, kl-eth `83aa7ec`), Lessons, RX overload wedge  -  TWO bugs: BD-order inversion + drops/v2-marker alias [FIXED, silicon-validated], Silicon forensics  -  "delivery dead, hardware healthy", Status  -  silicon results (2026-07-08, `build_dp100_wfix`, WNS +0.092), Symptom (silicon), The contract, stated, The fix (`09e3a09`)  -  BD order == pop order by construction (+3 more)

### Community 28 - "RX memory-hierarchy plan — cold vs capacity, and the dedicated-network-cache decision"
Cohesion: 0.14
Nodes (14): Architecture finding (2026-07-08)  -  why a network *scratchpad* is the wrong lever HERE, BRAM budget (the shared constraint  -  L2 and network-SRAM compete), Branch A  -  capacity-bound: grow / partition the L2, Branch B  -  cold / bandwidth-bound: the dedicated network cache, Ceiling test (`recv(MSG_TRUNC)` drains without `copy_to_user`  -  `tcp.c:2866`), Decision tree (one glance), Gates & rule, PERF VERDICT (2026-07-09)  -  the RX wall is the recv payload copy, measured (+6 more)

### Community 30 - "milan_soc.py"
Cohesion: 0.15
Nodes (13): 0. Why this exists, 1. The LSU and its L1 D-cache at a glance, 2. The load pipeline and what "miss" means, 3. The refill engine  -  the "8 refills", 4. The L1↔L2 bus: where the parallelism is spent, 5. The honest part: how MLP actually arises on an *in-order* core, 6. Timeline picture, 7. What we built and MEASURED on silicon (2026-07-08) (+5 more)

### Community 34 - "perf_campaign_chart.py"
Cohesion: 0.83
Nodes (3): bar(), bx(), y()

### Community 35 - "SVG"
Cohesion: 0.15
Nodes (3): esc(), Tiny SVG builder for the Milan perf docs — consistent styling, no deps., SVG

### Community 36 - "Throughput goal — >500 Mbit/s RX *and* TX, reach for 1 Gbit/s"
Cohesion: 0.12
Nodes (16): Detailed investigations (read these for the evidence), ⚡ FORCED-MARCH RESULTS (2026-07-09 evening  -  R1 refuted, R2 LANDED, R3 in flight), Ground rules for this campaign, (original T1 notes below), Phase X MEASURED (2026-07-08)  -  clock uplift REFUTES the linear projection, Phase X status + T2 latency decomposition (2026-07-08), R0 baseline (signed, 2026-07-08, `build_dp100_m1` WNS +0.056  -  CAMPAIGN_500_PLAN), R1 result (2026-07-08, `build_dp100_m1`, hash_sel=0  -  2-queue fan-out LIVE) (+8 more)

### Community 37 - "Documentation index"
Cohesion: 0.29
Nodes (7): Copy-removal endgame (measured 2026-07-09) — 481 unreachable via the socket API, DDIO / zero-copy RX levers (measured 2026-07-09, toward the 481 ceiling), Lever log — goal · change · **measured effect**, Memory-depth loop end (measured 2026-07-09) — the knee is L2 downPending=8, Performance CHANGELOG — Milan FPGA TSN NIC, Rejected / refuted levers (measured, not assumed), Where the goal stands

### Community 39 - "Running the tests — the complete guide"
Cohesion: 0.17
Nodes (11): 1. Elaboration smoke test (ALWAYS before committing RTL to P&R), 2.1 Harness architecture (what a test looks like), 2.2 Timing budgets and geometry traps, 2.3 Cycle-exact introspection (the livelock toolkit), 2. The LiteX/Migen behavioral suites (sw/litex/test_*.py), 3. Verilator harnesses (tb/verilator/*, 18 of them), 4. Yosys device-portability check (syn/yosys), 5. P&R (Vivado)  -  see the build scripts (+3 more)

### Community 40 - "Getting the maximum out of the gigabit link — headroom analysis at 100 MHz"
Cohesion: 0.22
Nodes (8): 1. Where the link stands, 2. The budget model (anchor for every lever), 3. RX levers, ranked, 4. TX levers, ranked, 5. What actually reaches the wire (recommendation), 6. Evidence index (tonight), App profile (2026-07-10, keeper @ steady −P8 334 Mbit, per-hart, symbolized), Getting the maximum out of the gigabit link  -  headroom analysis at 100 MHz

### Community 41 - "test_rsc_ack_merge"
Cohesion: 0.13
Nodes (14): BD encodings (hs mode only; hs_en=0 ⇒ bit-exact legacy), build_hsq4 (2026-07-10 evening)  -  the CQ-depth fix VALIDATED; hs takes the single-flow record, build_hsq5 (2026-07-10 late)  -  THE MULTI-FLOW LIVELOCK: ROOT-CAUSED, FIXED, SILICON-DEAD, build_hsq6 (2026-07-10)  -  MULTI-FLOW NEGATIVE SCALING ROOT-CAUSED: the un-gated BD ring, build_hsq7 / hsq7t (2026-07-10)  -  CQ LUTRAM diet; the 2-queue slice wall FALLS, build_hsq8/9/10 (2026-07-10 overnight)  -  2-QUEUE HS ON SILICON; 16K PAGES BREAK THE FAMINE, CSRs (appended after rsc_agemax  -  all existing offsets preserved), Driver (kl-eth `hsplit` mode, module param; legacy default intact) (+6 more)

### Community 42 - "RX / TX performance — what we improved, how, and what's next"
Cohesion: 0.25
Nodes (8): Part 1  -  how we explained the RX improvements (the short version), Part 2  -  TX (and why our RX change didn't touch it), Part 3  -  what's next: DDIO (the vindicated "network cache"), RX / TX performance  -  what we improved, how, and what's next, The goal, in one line, The levers at a glance (measured), Then `perf` told us the truth, Where we are (after R2  -  `build_r2slots` + kl-eth `mslot60d`)

### Community 43 - "StormModel"
Cohesion: 0.40
Nodes (4): How to change behavior safely (the loop), Regression net, RX performance tuning map  -  maintainer's guide, The ranked extraction list (as of 2026-07-11)

### Community 44 - "tools_wakebench.c"
Cohesion: 0.60
Nodes (3): main(), now_ns(), pin()

### Community 45 - "Milan v1.2 → FR/NFR dependency matrix"
Cohesion: 0.12
Nodes (17): A. Discovery  -  ADP  *(Milan v1.2 Discovery; IEEE 1722.1-2021 §6)*, B. AEM descriptor model  *(Milan v1.2 §5.3.3.1–5.3.3.11)*, C. Enumeration & control  -  AECP/AEM  *(Milan v1.2 §5.4)*, Coverage & test summary, D. Milan Vendor Unique  -  MVU  *(Milan v1.2 §5.4.3.2)*, E. Connection management  -  ACMP  *(Milan v1.2 §5.5)*, F. Streaming & stream formats  -  AVTP AAF  *(Milan v1.2 §5.4 format match; §6 Base Audio Formats)*, G. Reservation & addressing  -  MAAP, SRP  *(Milan v1.2 §5.6; 802.1Qat/Qak)* (+9 more)

### Community 47 - "Profiling on the Milan board — method, and the misaligned-usercopy case study"
Cohesion: 0.22
Nodes (8): 1. What profiling this board can and cannot do, 2. Measurement protocol (what was actually run), 3. Symbolizing without kallsyms, 4. Reading the raw histogram *before* symbols: address-cluster shape, 5. From symbol to *which loop*: disassemble the exact PCs, 6. Drawing the conclusions (each with its check), 7. Pitfalls log (things that bit, so they're written down), Profiling on the Milan board  -  method, and the misaligned-usercopy case study

### Community 48 - "BDHarness"
Cohesion: 0.07
Nodes (57): BDHarness, csum_ref(), A,B,A,B interleave: both flows aggregate concurrently (no park closes); B     cl, Open aggregate A, then a v1 single and a PSH-closed flow B: ready BDs stay     i, n_slots+1 concurrent flows: the 5th park-closes the round-robin victim     exact, An open aggregate holds the CQ head while v1 singles pile behind it: at     leve, A flow appending forever (every append inside rsc_tout) closes on the     lifeti, One 2-seg aggregate: header lands in ring slot 0, payload at page offset 0     b (+49 more)

### Community 49 - "hsplit14 / hsq12 — per-page (cut-through) hs delivery"
Cohesion: 0.29
Nodes (6): Expected effect + follow-ups, hsplit14 / hsq12  -  per-page (cut-through) hs delivery, hsq12 RTL changes (RingDMAWriter), kl-eth hsplit14 changes, Sim updates (test_ring_bd.py), Why the current RTL holds everything to close

### Community 50 - "De-Xilinx plan  -  replace XPM/vendor IP with Alex Forencich open cores"
Cohesion: 0.12
Nodes (16): 1. Inventory  -  what is Xilinx today, 2. Forencich core catalog (the list you asked for), 3. Replacement mapping, 4. Migration plan (phased, each phase Verilator-verified), 5. Licensing & vendoring, 6. Open-toolchain synthesis check (device portability), 7. Definition of done, corundum  -  full open NIC  (`github.com/corundum/corundum`)  *(optional, for scale-out)* (+8 more)

### Community 51 - "CPPI-style DMA redesign  -  on-chip descriptors, cut-through, zero-copy (plan)"
Cohesion: 0.13
Nodes (15): 2026-07-06 addendum  -  batching + a false-parity retraction, 2026-07-07 campaign  -  SMP, the three-copies profile, copybreak RX, stall verdict, Bring-up log & current state (2026-07-05, end of session), CPPI-style DMA redesign  -  on-chip descriptors, cut-through, zero-copy (plan), Current RX path (silicon-proven `RingDMAWriter`), Layer-per-layer debug method (use `lview.sh`), Net effect on MAC RAM, P5 v1 TX-BD  -  silicon results (2026-07-06) (+7 more)

### Community 52 - "Simulation  -  how the Milan design is simulated and verified"
Cohesion: 0.13
Nodes (15): Section 0: Prerequisites, Section 1.1: Anatomy of a harness, Section 1.2: What milan_dp proves  -  the integration harness, Section 1.3: Running them, Section 1.4: Warning suppressions and why they are safe, Section 1: Verilator RTL harnesses, Section 2: Softcore boot with litex_sim, Section 3.1: How it is wired (+7 more)

### Community 53 - "deploy.sh"
Cohesion: 0.52
Nodes (6): do_build(), do_console(), do_flash(), do_flash_images(), do_load(), deploy.sh script

### Community 54 - "Attaching AXI-Stream FPGA cores to the NaxRiscv SoC"
Cohesion: 0.15
Nodes (13): 1. The mental model: AXI-Stream is not memory-mapped, 2. What NaxRiscv exposes in LiteX, 3. Plane ①  -  control (AXI-Lite / CSR slave), 4. Plane ②  -  data (AXI-Stream ↔ memory via DMA), 4a. Coherent DMA (recommended)  -  no cache flushes in the driver, 4b. Non-coherent DMA  -  simpler fabric, driver must flush, 5. Plane ③  -  events (IRQ → PLIC), 6. Clock-domain crossing (+5 more)

### Community 55 - "RX stages"
Cohesion: 0.14
Nodes (13): Build and driver lineage (what "hsqN" and "hsplitN" mean), Obsolete and staged-for-removal code, RX stages, Stage R1: wire, RGMII PHY, MAC, Stage R2: flow steering (RxSteer, 2-queue builds), Stage R3: RSC aggregation (RingDMAWriter slots), Stage R4: page placement (header split), Stage R5: completion queue and BD publication (+5 more)

### Community 56 - "Second bug  -  TX-to-wire: the 2026-07-04 investigation log (OPEN, bisection running)"
Cohesion: 0.15
Nodes (13): FINAL LAYERS + VERDICT  -  IT PINGS (2026-07-04 evening), kl-eth TX debug  -  "link up, RX works, but the peer never sees our frames", Reusable takeaways, ROOT CAUSE FOUND (2026-07-04 evening)  -  cut-through core + bubbly source, Second bug  -  TX-to-wire: the 2026-07-04 investigation log (OPEN, bisection running), Test rig (generic), The diagnostic chain (each step ruled something in or out), The fix (gateware  -  `milan-fpga`, `sw/litex/milan_soc.py`, `MilanMAC`) (+5 more)

### Community 57 - "Register groups"
Cohesion: 0.17
Nodes (12): 0x000  -  Identification / IRQ, 0x100  -  MAC control / status  `(REQ-MAC-01..03)`, 0x200  -  Statistics (RMON)  `(REQ-MAC-04)`, 0x300  -  802.1Q classifier  `(REQ-CLS-01..04)`, 0x400  -  802.1Qav CBS (per queue)  `(REQ-CBS-01..03)`, 0x500  -  PTP hardware clock  `(REQ-PTP-01..04, 06)`, 0x600  -  ADP advertiser  `(IEEE 1722.1-2021 / Milan v1.2, FR-DISC-01..04)`, 0x700  -  RX destination-MAC TCAM filter  `(REQ-MAC-02)` (+4 more)

### Community 58 - "TB"
Cohesion: 0.26
Nodes (7): run_stress_test(), run_test(), run_test_init_sink_pause(), run_test_init_sink_pause_reset(), run_test_overflow(), run_test_tuser_assert(), TB

### Community 59 - "CBS datapath bug  -  classifier `tdest` mis-timing under back-to-back frames [FIXED]"
Cohesion: 0.22
Nodes (9): CBS datapath bug  -  classifier `tdest` mis-timing under back-to-back frames [FIXED], Root cause (sim-confirmed, `tb/verilator/controller_rate`), Second defect: arbiter cross-lock in `traffic_queues` (the actual TX wedger), Silicon re-test with the cross-lock fix (ring10, 2026-07-05), Silicon verification (ring9 = classifier fix only, 2026-07-05), Status, Symptom (silicon), The fix (shipped) (+1 more)

### Community 60 - "Frame"
Cohesion: 0.10
Nodes (24): Beat, data, keep, last, ck(), main(), make_frame(), Frame (+16 more)

### Community 61 - "RX ring DMA  -  root cause of the large-frame RX loss + the AXI-burst fix"
Cohesion: 0.22
Nodes (9): How it works (v2 mechanism, end to end), Measured ladder (silicon, night of 2026-07-04/05  -  each step verified end-to-end), Related, RX ring DMA  -  root cause of the large-frame RX loss + the AXI-burst fix, The fix  -  `RingDMAWriter` v2 (`sw/litex/milan_soc.py`), The measurement chain (how to pin this class of bug fast), The TX mirror  -  `RingDMAReader` (same night, same disease, same cure), TL;DR (+1 more)

### Community 63 - "TB"
Cohesion: 0.19
Nodes (17): process_f_files(), run_stress_test(), run_test(), run_test_init_sink_pause(), run_test_init_sink_pause_reset(), run_test_init_sink_pause_sink_reset(), run_test_init_sink_pause_source_reset(), run_test_overflow() (+9 more)

### Community 64 - "Board porting  -  Alinx AX7101 (XC7A100T-2FGG484I)"
Cohesion: 0.29
Nodes (7): 1. Board facts (from the official Alinx repo), 2. Porting method (reproducible), 3. What changed, 4. Verification (open toolchain, no Vivado), 5. Board-gated (needs the schematic / Vivado / the board), Board porting  -  Alinx AX7101 (XC7A100T-2FGG484I), PHY mapping (per port)  -  GMII, not RGMII

### Community 65 - "TB"
Cohesion: 0.19
Nodes (15): run_stress_test(), run_test(), run_test_init_sink_pause(), run_test_init_sink_pause_reset(), run_test_init_sink_pause_sink_reset(), run_test_init_sink_pause_source_reset(), run_test_overflow(), run_test_oversize() (+7 more)

### Community 66 - "Harness"
Cohesion: 0.13
Nodes (16): Cfg, hi, idle, lo, shaped, Harness, active, checks (+8 more)

### Community 67 - "test_rsc_ack_merge"
Cohesion: 0.33
Nodes (6): pure-ACK builder: doff=5, or doff=8 with the given 12 option bytes., ACK-run merging: N same-flow pure ACKs collapse to ONE v1 BD holding the     LAT, Merge eligibility: timestamp-only options (01 01 08 0A) merge; any other     opt, tcp_ack(), test_rsc_ack_merge(), test_rsc_ack_passthrough_and_ts()

### Community 68 - "IdealRef"
Cohesion: 0.10
Nodes (15): IdealRef, allow, cfg, cnt, credit, credit_add_idle, isc_r, isg (+7 more)

### Community 69 - "Harness"
Cohesion: 0.17
Nodes (12): Harness, cfg, checks, dut, fails, fref, iref, max_ideal_err (+4 more)

### Community 70 - "FixedPointRef"
Cohesion: 0.11
Nodes (11): FixedPointRef, allow, cfg, credit, credit_add_idle, eng, isg, istx (+3 more)

### Community 71 - "LiteXModule"
Cohesion: 0.17
Nodes (11): SoCCore, _CRG, main(), MilanDMA, MilanMAC, MilanSoC, Clock/reset: PLL the 200 MHz board clock down to the system clock.      With `wi, # NOTE: the frame is FULLY inside hdr_reg (beats <= 9), so absorbing (+3 more)

### Community 72 - "SlopeEngineRef"
Cohesion: 0.13
Nodes (13): SlopeEngineRef, cnt, den, idle_s, is1g_s, isc, M48, num (+5 more)

### Community 73 - "Harness"
Cohesion: 0.16
Nodes (12): __int128, Harness, checks, dut, fails, m, main(), Model (+4 more)

### Community 74 - "Protocol validation matrix  -  every protocol, and every test that validates it"
Cohesion: 0.26
Nodes (7): run_stress_test(), run_test(), run_test_init_sink_pause(), run_test_init_sink_pause_reset(), run_test_overflow(), run_test_tuser_assert(), TB

### Community 75 - "CbsInputs"
Cohesion: 0.18
Nodes (11): CbsInputs, bytes_sent, hi_credit, idle_slope, is_1g, is_granted, is_transmitting, lo_credit (+3 more)

### Community 76 - "Harness"
Cohesion: 0.21
Nodes (11): Harness, pack_frame(), payload(), Reassemble collected beats into frames of exact byte lists., payload: list of byte values -> (header_word, [payload words], padded_len), Write one frame slot into the ring image at byte offset `off`; return new off., test_4k(), test_backpressure() (+3 more)

### Community 77 - "Documentation index"
Cohesion: 0.22
Nodes (9): 1  -  System overview & architecture, 2  -  Design direction & plans, 3  -  Contracts: ABI, requirements, validation, 4  -  Build, boot & operate, 5  -  Findings: bugs cornered and measured on silicon, 6  -  Module & verification docs, Conventions, Documentation index (+1 more)

### Community 78 - "TSN on FPGA — Requirements"
Cohesion: 0.11
Nodes (19): 1. Goal and scope, 2. Reference standards, 3. Missing elements to comply with the 802.1 configuration standards (gap analysis), 4.A Control plane — memory-mapped CSR (foundation), 4.B gPTP / IEEE 1588 hardware clock (PHC), 4.C IEEE 802.1Qav credit-based shaper, 4.D IEEE 802.1Q classification and queuing, 4.E IEEE 802.3 MAC configuration and management (+11 more)

### Community 79 - "CbsConfig"
Cohesion: 0.29
Nodes (4): CbsConfig, BYTE_TO_BIT, clk_freq_hz, FP

### Community 80 - "CBS verification harness (IEEE 802.1Qav credit-based shaper)"
Cohesion: 0.25
Nodes (7): CBS verification harness (IEEE 802.1Qav credit-based shaper), Configuration, Notes surfaced by this harness, Run it, Scenarios, The slope engine mirror (STRICT pairing), What it checks

### Community 84 - "M-A3 (partial) — DMA + AXIS-CDC data path on silicon (100 MHz, all-blocks)"
Cohesion: 0.11
Nodes (18): (a) Cache-coherent DMA — the DMA read stale DRAM, (b) Internal MAC loopback CSR — self-contained verification, Breakthrough — the RGMII RX is ALIVE, just mis-sampled (delay tuning), (c) DMA endianness — on-wire bytes were reversed, Coherent DMA + internal loopback + endianness (2026-07-03, `build_gmii_coh`/`_final`), CONFIRMED ON SILICON — full TX/RX correct, both directions (`build_gmii_final`, 2026-07-03), CONFIRMED ON SILICON — the `last_be` fix makes frames egress (2026-07-03), M-A3 (partial) — DMA + AXIS-CDC data path on silicon (100 MHz, all-blocks) (+10 more)

### Community 85 - "test_axis_cobs_encode.py"
Cohesion: 0.15
Nodes (8): cobs_decode(), cobs_encode(), prbs31(), prbs_payload(), process_f_files(), run_test(), TB, test_axis_cobs_encode()

### Community 86 - "test_axis_fifo_adapter.py"
Cohesion: 0.23
Nodes (11): process_f_files(), run_stress_test(), run_test(), run_test_init_sink_pause(), run_test_init_sink_pause_reset(), run_test_overflow(), run_test_oversize(), run_test_pause() (+3 more)

### Community 87 - "REGISTER_MAP.md"
Cohesion: 0.17
Nodes (3): System domain map, The domains, controller_rate — CBS end-to-end shaping/interference reproduction (OPEN BUG)

### Community 88 - "sim_main.cpp"
Cohesion: 0.29
Nodes (17): axi_read(), axi_write(), ck(), do_reset(), eval(), frames_equal(), hi(), lo() (+9 more)

### Community 89 - "test_axis_cobs_decode.py"
Cohesion: 0.15
Nodes (5): cobs_encode(), prbs31(), prbs_payload(), run_test(), TB

### Community 90 - "TB"
Cohesion: 0.24
Nodes (9): run_stress_test(), run_test(), run_test_init_sink_pause(), run_test_init_sink_pause_reset(), run_test_overflow(), run_test_oversize(), run_test_pause(), run_test_tuser_assert() (+1 more)

### Community 91 - "tb_ptp_ts_core"
Cohesion: 0.12
Nodes (16): error_injection_test, run_test_suite, send_packet, axi_stream_if, ethernet_packet_pkg, ptp_ts_core, stress_test, timestamp_counter (+8 more)

### Community 92 - "sim_main.cpp"
Cohesion: 0.24
Nodes (16): ck(), config_classifier(), vector, do_reset(), hi(), lo(), main(), Res (+8 more)

### Community 93 - "properties"
Cohesion: 0.12
Nodes (16): default, description, enum, type, description, type, description, pattern (+8 more)

### Community 94 - "sim_main.cpp"
Cohesion: 0.22
Nodes (15): ck(), ckx(), vector, feed(), hi(), lo(), main(), mkavtp() (+7 more)

### Community 95 - "test_axis_frame_length_adjust_fifo.py"
Cohesion: 0.23
Nodes (8): process_f_files(), run_test(), run_test_init_sink_pause(), run_test_init_sink_pause_reset(), run_test_overflow(), run_test_tuser_assert(), TB, test_axis_frame_length_adjust_fifo()

### Community 96 - "tb_ptp_ts_top"
Cohesion: 0.13
Nodes (14): metadata_backpressure_test, send_concurrent_packets, send_rx_packet, send_tx_packet, ptp_ts_top, stress_test, tb_ptp_ts_top, metadata_backpressure_test (+6 more)

### Community 97 - "sim_main.cpp"
Cohesion: 0.36
Nodes (14): Beat, data, keep, last, ck(), vector, drain(), eq() (+6 more)

### Community 98 - "test_axis_arb_mux.py"
Cohesion: 0.26
Nodes (7): process_f_files(), run_arb_test(), run_stress_test(), run_test(), run_test_tuser_assert(), TB, test_axis_arb_mux()

### Community 100 - "test_axis_ram_switch.py"
Cohesion: 0.26
Nodes (7): process_f_files(), run_arb_test(), run_stress_test(), run_test(), run_test_tuser_assert(), TB, test_axis_ram_switch()

### Community 101 - "test_axis_switch.py"
Cohesion: 0.26
Nodes (7): process_f_files(), run_arb_test(), run_stress_test(), run_test(), run_test_tuser_assert(), TB, test_axis_switch()

### Community 102 - "sim_main.cpp"
Cohesion: 0.35
Nodes (13): CData, apply_static_fields(), be(), capture_frame(), check_common(), ck(), clear_events(), vector (+5 more)

### Community 103 - "object"
Cohesion: 0.15
Nodes (3): object, LocalLinkSink, LocalLinkSource

### Community 104 - "reg"
Cohesion: 0.14
Nodes (14): $ref, $ref, $ref, $ref, csr, dma-rx, dma-ts, dma-tx (+6 more)

### Community 105 - "test_axis_pipeline_register.py"
Cohesion: 0.26
Nodes (6): process_f_files(), run_stress_test(), run_test(), run_test_tuser_assert(), TB, test_axis_pipeline_register()

### Community 106 - "TODO — TSN on FPGA"
Cohesion: 0.14
Nodes (14): Dependency summary, Phase 0 — Verification & docs (start here; partly done), Phase 1 — Memory-mapped CSR plane (critical path) `(REQ-CSR-*)`, Phase 2 — PTP hardware clock (PHC) `(REQ-PTP-*)`, Phase 3 — 802.1Qav CBS fixes + runtime config `(REQ-CBS-*)`, Phase 4 — 802.1Q classification `(REQ-CLS-*)`, Phase 5 — 802.3 MAC configuration & management `(REQ-MAC-*)`, Phase 6 — Multi-channel DMA (enables N queues) (+6 more)

### Community 107 - "FULL_FPGA_SOLUTION.md"
Cohesion: 0.33
Nodes (5): Caveat — the `dma-*` reg window has a different layout (LiteX build), CBS offload policy, DT match & resources, Feature surface → CSR (see `docs/FR_NFR.md` §2.10 `FR-DRV-*`), `kl-eth` — Milan TSN NIC Linux driver

### Community 108 - "milan_top"
Cohesion: 0.17
Nodes (11): eth_mac_1g_rgmii_fifo, milan_top, adp_tx_arbiter, axi_stream_if, ethernet_events, ethernet_packet_pkg, milan_csr, ptp_ts_top (+3 more)

### Community 109 - "milan_dt.py"
Cohesion: 0.24
Nodes (12): _cells(), extract_litex(), gen_dtsi(), _int(), main(), Coerce an IR numeric field to int — accepts a plain int or a string like     '0x, Render a base/size as n address/size cells (1 => 32-bit, 2 => 64-bit hi/lo)., Wrap the overlay in a synthetic base tree (providing the referenced labels) and (+4 more)

### Community 110 - "RxSteer"
Cohesion: 0.15
Nodes (8): _axis_dp_cdc(), _AxisDP, Circular-DRAM-ring -> AXIS-frame **AXI burst** DMA reader (TX upgrade, 2026-07-0, 2-way RX flow-steering front-end (parallel ACK/recv processing, TX>=200 step)., Pair of stream endpoints for one AXIS lane crossing the datapath boundary:     `, Cross one AXIS lane between the sys domain (DMA engine / MAC core) and the     d, RingDMAReader, RxSteer

### Community 111 - "TB"
Cohesion: 0.28
Nodes (4): run_stress_test(), run_test(), run_test_tuser_assert(), TB

### Community 112 - "TB"
Cohesion: 0.28
Nodes (4): run_stress_test(), run_test(), run_test_tuser_assert(), TB

### Community 113 - "TB"
Cohesion: 0.28
Nodes (4): run_stress_test(), run_test(), run_test_tuser_assert(), TB

### Community 114 - "LiteXModule"
Cohesion: 0.23
Nodes (7): LiteXModule, _MilanRGMIICRG, MilanRGMIIPHY, MilanRGMIIRX, RGMII RX matching the Alinx AX7101 vendor design: raw IBUF data straight into an, Pipeline reference: docs/PIPELINE_STAGES.md (stages R3-R5: slots, pages,     CQ/, RingDMAWriter

### Community 115 - "window"
Cohesion: 0.17
Nodes (12): description, type, $defs, window, base, size, description, type (+4 more)

### Community 116 - "avtp_adp_packet_gen"
Cohesion: 0.20
Nodes (11): adp_message_type_t, avtp_adp_packet_gen, adp_packet_gen, avtp_packet_gen, subtype_gen, subtype_header_gen, avtp_adp_t, avtp_common_hdr_t (+3 more)

### Community 117 - "avtp_random_subtype"
Cohesion: 0.17
Nodes (11): avtp_base_packet_gen, avtp_common_hdr_t, avtp_random_subtype, avtp_packet_gen, subtype_gen, subtype_header_gen, ref, subtype_alter_t (+3 more)

### Community 118 - "TB"
Cohesion: 0.26
Nodes (3): run_test(), run_test_tuser_assert(), TB

### Community 119 - "TB"
Cohesion: 0.26
Nodes (3): run_test(), run_test_tuser_assert(), TB

### Community 120 - "TB"
Cohesion: 0.26
Nodes (3): run_test(), run_test_tuser_assert(), TB

### Community 121 - "AVDECC entity model (IEEE 1722.1-2021 / Milan v1.2)"
Cohesion: 0.18
Nodes (11): A. Generate the FPGA AEM memory image, AVDECC entity model (IEEE 1722.1-2021 / Milan v1.2), B. Cross-check the software entity, C. Drive READ_DESCRIPTOR tests, Field classes (the important convention), How to use it, Milan v1.2 conformance notes (what makes this a *Milan* entity, not just AVDECC), Open items to confirm against the Milan v1.2 PDF (+3 more)

### Community 122 - "tb_top"
Cohesion: 0.18
Nodes (10): check_total_parse_pkt, KL_avtp_common_parser, report_summary, reset_dut, axi_stream_if, tb_top, check_total_parse_pkt, drive_random_pkt (+2 more)

### Community 123 - "tb_traffic_classifier"
Cohesion: 0.18
Nodes (8): expect_tdest, axi_stream_if, create_vlan_packet, drive_packet, ethernet_packet_pkg, traffic_classifier, tb_traffic_classifier, drive_packet

### Community 124 - "milan_datapath"
Cohesion: 0.20
Nodes (9): milan_datapath, adp_tx_arbiter, axi_stream_if, ethernet_events, ethernet_packet_pkg, milan_csr, ptp_ts_top, rx_mac_filter (+1 more)

### Community 125 - "Entity: ptp_ts_core"
Cohesion: 0.18
Nodes (10): Constants, Diagram, Entity: ptp_ts_core, Generics, Instantiations, Ports, Processes, Signals (+2 more)

### Community 126 - "MilanSimSoC"
Cohesion: 0.20
Nodes (8): SimSoC, main(), MilanSimSoC, SimSoC + the Milan TSN datapath as an AXI4-Lite CSR slave at 0x9000_0000., add_milan_datapath(), MilanNIC, The Milan TSN datapath (`milan_datapath.sv`) wired into the SoC.      `milan_dat, Instantiate `milan_datapath` and add its RTL sources  -  the single place the

### Community 127 - "avtp_alter_subtype"
Cohesion: 0.18
Nodes (10): avtp_alter_subtype, avtp_packet_gen, subtype_gen, subtype_header_gen, avtp_base_packet_gen, avtp_common_hdr_t, bit8, ref (+2 more)

### Community 128 - "avtp_stream_subtype"
Cohesion: 0.18
Nodes (10): avtp_base_packet_gen, avtp_common_hdr_t, avtp_stream_subtype, avtp_packet_gen, subtype_gen, subtype_header_gen, bit8, ref (+2 more)

### Community 129 - "sim_main.cpp"
Cohesion: 0.33
Nodes (10): Beat, data, keep, last, ck(), vector, hi(), lo() (+2 more)

### Community 132 - "OPEN_SOURCE_MIGRATION.md"
Cohesion: 0.33
Nodes (5): Coverage, How it works, Notes, Open-toolchain synthesis check (Yosys) — device portability, Tooling

### Community 133 - "Entity: KL_avtp_common_parser"
Cohesion: 0.20
Nodes (9): Description, Diagram, Entity: KL_avtp_common_parser, Generics, Ports, Processes, Signals, State machines (+1 more)

### Community 134 - "Entity: traffic_classifier"
Cohesion: 0.20
Nodes (9): Constants, Description, Diagram, Entity: traffic_classifier, Generics, Instantiations, Ports, Processes (+1 more)

### Community 135 - "`adp_advertiser` — ADP transmit engine (design doc)"
Cohesion: 0.20
Nodes (10): 1. Purpose, 2. Emitted frame — byte-exact layout, 3.1 Events → message, 3.2 Timing, 3.3 FSM, 3. Behaviour, 4. Interface → CSR mapping, 5. Verification (what the harness proves) (+2 more)

### Community 136 - "ptp"
Cohesion: 0.20
Nodes (10): description, type, description, type, clock_hz, present, ptp, additionalProperties (+2 more)

### Community 137 - "properties"
Cohesion: 0.20
Nodes (10): description, type, additionalProperties, properties, type, mode, phy, reset_gpio (+2 more)

### Community 138 - "avtp_control_subtype"
Cohesion: 0.20
Nodes (9): avtp_base_packet_gen, avtp_common_hdr_t, avtp_control_subtype, avtp_packet_gen, subtype_gen, subtype_header_gen, ref, subtype_control_t (+1 more)

### Community 139 - "tb_traffic_controller_802_1q"
Cohesion: 0.20
Nodes (8): axi_stream_if, create_vlan_packet, drive_packet, ethernet_packet_pkg, traffic_controller_802_1q, tb_traffic_controller_802_1q, drive_packet, send_packet_of_class

### Community 140 - "sim_main.cpp"
Cohesion: 0.49
Nodes (9): beat0(), ck(), vector, hi(), lo(), main(), send_frame(), step() (+1 more)

### Community 142 - "Milan TSN FPGA  -  architecture & developer guide"
Cohesion: 0.22
Nodes (9): 1. Repository layout, 2. System block diagram, 3. Datapath (exists today, see `hdl/common/milan_top.sv`), 4. Control plane (the new `milan_csr`), 5. Clock domains & CDC, 6. HDL ↔ software mapping, 7. Verification, 8. Where to change things (maintainability) (+1 more)

### Community 143 - "Glossary"
Cohesion: 0.22
Nodes (9): AVB / TSN / Milan, CPU / cache / memory (the >500 RX campaign), Ethernet / PHY / wire, FPGA / tooling, Glossary, Linux networking / performance, LiteX / SoC / boot, Project shorthand (+1 more)

### Community 144 - "Pipeline telemetry (`milan_tlm_*`)  -  in-fabric observability for the TX/RX path"
Cohesion: 0.29
Nodes (7): Addressing note, Coherent capture, Cross-platform (LiteX vs Zynq), Extending it, Pipeline telemetry (`milan_tlm_*`)  -  in-fabric observability for the TX/RX path, Reading it from Linux, What it measures

### Community 145 - "cells"
Cohesion: 0.22
Nodes (9): description, items, type, type, cells, shaped, description, items (+1 more)

### Community 146 - "items"
Cohesion: 0.22
Nodes (9): description, items, maxItems, minItems, type, additionalProperties, oneOf, required (+1 more)

### Community 147 - "ptp_ts_top"
Cohesion: 0.25
Nodes (7): axis_mux_rr_2in_1out, ptp_ts_top, axi_stream_if, axis_fifo, ptp_ts_core, timestamp_counter, ptp_csr_sync

### Community 148 - "Appendix A  -  Phase-0 counter spec (detailed, buildable)"
Cohesion: 0.25
Nodes (8): A.0  -  Exposures (small read-only taps on existing modules; zero functional effect), A.1  -  Read round-trip latency L  (`rd_latency_probe`), A.2  -  Starve decomposition  (`rd_produce_probe`)  -  the decision-maker, A.3  -  Interconnect outstanding-depth proxy  (`outstanding_hi_probe`), A.4  -  Integration (one closure, revert = delete it), A.5  -  Measurement protocol (on `build_dp100_p0`, the instrumented 100 MHz gateware), A.6  -  What the numbers decide (before writing any prefetch RTL), Appendix A  -  Phase-0 counter spec (detailed, buildable)

### Community 149 - "Entity: traffic_controller_802_1q"
Cohesion: 0.25
Nodes (7): Constants, Diagram, Entity: traffic_controller_802_1q, Generics, Instantiations, Ports, Signals

### Community 150 - "Entity: traffic_queues"
Cohesion: 0.25
Nodes (7): Constants, Diagram, Entity: traffic_queues, Generics, Instantiations, Ports, Signals

### Community 151 - "Entity: KL_adp_parser"
Cohesion: 0.25
Nodes (7): Constants, Diagram, Entity: KL_adp_parser, Ports, Processes, Signals, State machines

### Community 152 - "`tcam` — ternary CAM destination-MAC database (design doc)"
Cohesion: 0.25
Nodes (7): 1. What it is, 2. Why ternary (vs an exact-match CAM), 3. Interface, 4. How it fits the datapath, 5. Verification, 6. Notes / extensions, `tcam` — ternary CAM destination-MAC database (design doc)

### Community 153 - "Entity: ethernet_events"
Cohesion: 0.25
Nodes (7): Description, Diagram, Entity: ethernet_events, Generics, Ports, Processes, Signals

### Community 154 - "milan-dt.schema.json"
Cohesion: 0.25
Nodes (7): additionalProperties, description, $id, required, $schema, title, type

### Community 155 - "properties"
Cohesion: 0.25
Nodes (8): properties, enum, type, description, minimum, type, name, num

### Community 156 - "queues"
Cohesion: 0.25
Nodes (8): queues, rxq, txq, additionalProperties, properties, type, type, type

### Community 157 - "avtp_base_packet_gen"
Cohesion: 0.32
Nodes (7): avtp_base_packet_gen, avtp_packet_gen, subtype_gen, subtype_header_gen, avtp_common_hdr_t, ref, subtype_t

### Community 158 - "axis_ep.py"
Cohesion: 0.32
Nodes (5): Copyright (c) 2014-2018 Alex Forencich  Permission is hereby granted, free of ch, bench(), test_bench(), bench(), test_bench()

### Community 159 - "ll_ep.py"
Cohesion: 0.32
Nodes (5): Copyright (c) 2014-2018 Alex Forencich  Permission is hereby granted, free of ch, bench(), test_bench(), bench(), test_bench()

### Community 160 - "find_vivado_settings"
Cohesion: 0.38
Nodes (6): find_vivado_settings(), main(), Minimal shell-quote (paths here are simple, but be safe)., Locate a Vivado settings64.sh (sourced to put `vivado` on PATH)., shq(), Path

### Community 161 - "AVB_SWITCH_DIRECTION.gen.py"
Cohesion: 0.48
Nodes (5): arrow(), badge(), box(), esc(), text()

### Community 162 - "RX_RING_OPERATION.gen.py"
Cohesion: 0.48
Nodes (5): arrow(), box(), esc(), seg(), text()

### Community 163 - "Entity: credit_based_shaper"
Cohesion: 0.29
Nodes (6): Diagram, Entity: credit_based_shaper, Generics, Ports, Processes, Signals

### Community 164 - "Entity: traffic_shaping_core"
Cohesion: 0.29
Nodes (6): Diagram, Entity: traffic_shaping_core, Generics, Ports, Processes, Signals

### Community 165 - "traffic_controller_802_1q"
Cohesion: 0.29
Nodes (6): axi_stream_if, ethernet_packet_pkg, traffic_classifier, traffic_queues, traffic_shaping_core, traffic_controller_802_1q

### Community 166 - "Entity: milan_csr"
Cohesion: 0.29
Nodes (7): Description, Diagram, Entity: milan_csr, Generics, Ports, Processes, Signals

### Community 167 - "Entity: event_counter"
Cohesion: 0.29
Nodes (6): Description, Diagram, Entity: event_counter, Generics, Ports, Processes

### Community 168 - "Entity: ptp_ts_top"
Cohesion: 0.29
Nodes (6): Diagram, Entity: ptp_ts_top, Generics, Instantiations, Ports, Signals

### Community 169 - "Entity: timestamp_counter"
Cohesion: 0.29
Nodes (6): Diagram, Entity: timestamp_counter, Generics, Ports, Processes, Signals

### Community 170 - "tb_traffic_queues"
Cohesion: 0.29
Nodes (6): send_packet_to_queue, axi_stream_if, ethernet_packet_pkg, traffic_queues, tb_traffic_queues, send_packet_to_queue

### Community 171 - "Platform"
Cohesion: 0.29
Nodes (3): Platform, # NOTE: the GMII TX IOB-packing constraint lives in MilanMAC (milan_soc.py), whi, Xilinx7SeriesPlatform

### Community 172 - "`sw/` — boot one RISC-V core with the Milan NIC + driver"
Cohesion: 0.29
Nodes (7): Boot Linux (needs the board / a bitstream), Boot the core in simulation (no Vivado, self-contained) ✅ verified, Build the board SoC, Configurability, Status (what actually runs on this box), `sw/` — boot one RISC-V core with the Milan NIC + driver, Toolchain install (once)

### Community 173 - "CBS default-shaping bug  -  reset config paced ALL best-effort TX at 300 Mb/s [FIXED]"
Cohesion: 0.33
Nodes (6): CBS default-shaping bug  -  reset config paced ALL best-effort TX at 300 Mb/s [FIXED], Lessons, Root cause  -  two defaults contradicting each other, Symptom, The fix, Verification on silicon (before fixing)

### Community 174 - "RX_RING_DMA.gen.py"
Cohesion: 0.53
Nodes (4): arrow(), box(), esc(), text()

### Community 175 - "TX_STARVATION_FIX.gen.py"
Cohesion: 0.53
Nodes (4): arrow(), box(), esc(), text()

### Community 176 - "traffic_classifier"
Cohesion: 0.33
Nodes (5): axi_stream_if, axis_fifo, ethernet_packet_pkg, traffic_classifier, traffic_class_map

### Community 178 - "`kl-eth` — Milan TSN NIC Linux driver"
Cohesion: 0.18
Nodes (11): 1. L1 / L2  -  Ethernet, filtering, stats, 2. Shaping / QoS  -  802.1Qav CBS, 3. Timing  -  gPTP / 802.1AS + PHC, 4. Discovery / control  -  AVDECC (IEEE 1722.1-2021 + Milan v1.2), 5. Reservation + address allocation, 6. Media transport  -  AVTP (IEEE 1722), 7. Host / SoC / driver, 8. Test inventory (how to run every automated test today) (+3 more)

### Community 179 - "`sw/dts/` — platform-convergent device tree for the Milan NIC"
Cohesion: 0.33
Nodes (5): Adding a new platform (the convergence contract), Files, Fully-FPGA flow (FR-DT-08), Notes, `sw/dts/` — platform-convergent device tree for the Milan NIC

### Community 180 - "sim_main.cpp"
Cohesion: 0.67
Nodes (5): ck(), look(), main(), tick(), wr()

### Community 184 - "avtp_packet_gen_pkg.svh"
Cohesion: 0.40
Nodes (4): avtp_alter_pkg, avtp_control_pkg, avtp_stream_pkg, avtp_pkt_common_pkg

### Community 186 - "avtp_stream_parser.sv"
Cohesion: 0.40
Nodes (3): avtp_stream_parser, avtp_subtype_pkg, ethernet_packet_pkg

### Community 188 - "ptp_ts_core"
Cohesion: 0.40
Nodes (4): ptp_ts_core, cdc_handshake, cdc_pulse, ethernet_packet_pkg

### Community 189 - "LiteX-ecosystem patches"
Cohesion: 0.40
Nodes (4): `0001-milan-linux-flashboot.patch` — QSPI Linux flash-boot, `0002-liteeth-gmii-tx-clk-invert.patch` — GMII TX clock phase option, LiteX-ecosystem patches, Usage

### Community 190 - "README.md"
Cohesion: 0.40
Nodes (4): Docs, Notes, Objective, Usage for Modelsim/Questa

### Community 191 - "tb_traffic_shaping_core"
Cohesion: 0.40
Nodes (4): axi_stream_if, ethernet_packet_pkg, traffic_shaping_core, tb_traffic_shaping_core

### Community 192 - "controller_rate_wrap"
Cohesion: 0.40
Nodes (4): controller_rate_wrap, axi_stream_if, ethernet_packet_pkg, traffic_controller_802_1q

### Community 193 - "shaper_core_wrap"
Cohesion: 0.40
Nodes (4): shaper_core_wrap, axi_stream_if, ethernet_packet_pkg, traffic_shaping_core

### Community 194 - "KL_avtp_common_parser.sv"
Cohesion: 0.50
Nodes (3): KL_avtp_common_parser, avtp_subtype_pkg, tdest_assign

### Community 195 - "milan-fpga — IEEE 1722 / 1722.1 / Milan v1.2 on FPGA"
Cohesion: 0.50
Nodes (4): Developers, Maintainers, milan-fpga — IEEE 1722 / 1722.1 / Milan v1.2 on FPGA, Running the testbenches

### Community 197 - "cdc_tb_top"
Cohesion: 0.50
Nodes (3): cdc_tb_top, cdc_handshake, cdc_pulse

### Community 198 - "sim_main.cpp"
Cohesion: 0.83
Nodes (3): ck(), main(), step()

### Community 199 - "classifier_wrap"
Cohesion: 0.50
Nodes (3): classifier_wrap, axi_stream_if, traffic_classifier

### Community 200 - "CSR verification harness (`milan_csr` AXI4-Lite control plane)"
Cohesion: 0.50
Nodes (4): CSR verification harness (`milan_csr` AXI4-Lite control plane), Extending, Run it, What it checks

### Community 201 - "datapath_wrap"
Cohesion: 0.50
Nodes (3): datapath_wrap, axi_stream_if, traffic_controller_802_1q

### Community 202 - "sim_main.cpp"
Cohesion: 0.83
Nodes (3): ck(), main(), step()

### Community 203 - "queues_wrap"
Cohesion: 0.50
Nodes (3): queues_wrap, axi_stream_if, traffic_queues

### Community 204 - "axis_frame_length_adjust_fifo"
Cohesion: 0.50
Nodes (3): axis_frame_length_adjust_fifo, axis_fifo, axis_frame_length_adjust

### Community 400 - "Verilator verification harnesses"
Cohesion: 0.67
Nodes (3): Conventions, Notes, Verilator verification harnesses

## Knowledge Gaps
- **1150 isolated node(s):** `How to change behavior safely (the loop)`, `The ranked extraction list (as of 2026-07-11)`, `Regression net`, `Performance (socket TCP, MTU 1500, measured on silicon)`, `AREA-70 campaign: CLOSED (silicon keeper = build_cbsf_epo)` (+1145 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **184 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `Milan on a fully-FPGA RISC-V platform  -  detailed migration & implementation plan` connect `PART B — ADP / AVDECC (the complete AVB solution)` to `REGISTER_MAP.md`?**
  _High betweenness centrality (0.007) - this node is a cross-community bridge._
- **Why does `AXIStreamSource` connect `AXIStreamSource` to `AXIStreamSink`, `axis_ep.py`, `object`?**
  _High betweenness centrality (0.005) - this node is a cross-community bridge._
- **Why does `TB` connect `Protocol validation matrix  -  every protocol, and every test that validates it` to `object`?**
  _High betweenness centrality (0.004) - this node is a cross-community bridge._
- **What connects `How to change behavior safely (the loop)`, `The ranked extraction list (as of 2026-07-11)`, `Regression net` to the rest of the system?**
  _1253 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `milan_soc.py` be split into smaller, more focused modules?**
  _Cohesion score 0.05128205128205128 - nodes in this community are weakly interconnected._
- **Should `Milan v1.2 endpoint — Functional & Non-Functional Requirements (FR/NFR)` be split into smaller, more focused modules?**
  _Cohesion score 0.0625 - nodes in this community are weakly interconnected._
- **Should `Troubleshooting — every problem hit bringing up the full-FPGA solution, and its fix` be split into smaller, more focused modules?**
  _Cohesion score 0.14285714285714285 - nodes in this community are weakly interconnected._