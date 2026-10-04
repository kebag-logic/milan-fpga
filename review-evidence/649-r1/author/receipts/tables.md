<!-- table: map-image -->
| Scope | LUT | Logic | LUTRAM | SRL | FF | IOB FF | RAMB36 | RAMB18 | DSP | CARRY4 | Slices | LUT % of image |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| `milan_datapath` | 42,200 | 40,388 | 1,812 | 0 | 48,433 | 3 | 30 | 12 | 14 | 3,107 | 13,083.0 | 83.12 |
| `@own` | 4,847 | 4,551 | 294 | 2 | 6,072 | 18 | 47 | 10 | 0 | 274 | 1,535.7 | 9.55 |
| `VexiiRiscvLitex_f5f08b170311db53220574624f819159` | 3,524 | 3,400 | 122 | 2 | 4,734 | 0 | 2 | 5 | 0 | 114 | 1,128.8 | 6.94 |
| `KL_gptp_gmii_launch` | 186 | 186 | 0 | 0 | 317 | 0 | 0 | 0 | 0 | 3 | 68.1 | 0.37 |
| `KL_mac_rmon_events` | 49 | 49 | 0 | 0 | 78 | 0 | 0 | 0 | 0 | 8 | 16.5 | 0.10 |
| sharing adjustment | -39 | -39 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0.0 | - |
| **alinx_ax7101** | 50,767 | 48,535 | 2,228 | 4 | 59,634 | 21 | 79 | 27 | 14 | 3,506 | 15,832.0 | 100.00 |
<!-- end table: map-image -->

<!-- table: map-datapath -->
| Scope | LUT | Logic | LUTRAM | SRL | FF | IOB FF | RAMB36 | RAMB18 | DSP | CARRY4 | Slices | LUT % of image |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| `milan_datapath/pp_shadow` | 23,904 | 22,796 | 1,108 | 0 | 24,265 | 0 | 21 | 3 | 8 | 1,576 | 7,121.8 | 47.09 |
| `milan_datapath/g_gptp_plane.u_gptp_shadow` | 5,004 | 4,496 | 508 | 0 | 5,899 | 0 | 3 | 3 | 4 | 339 | 1,571.4 | 9.86 |
| `milan_datapath/csr` | 3,073 | 3,073 | 0 | 0 | 2,141 | 0 | 0 | 2 | 0 | 37 | 703.5 | 6.05 |
| `milan_datapath/chan_map_capture` | 1,079 | 1,079 | 0 | 0 | 1,321 | 0 | 1 | 0 | 0 | 20 | 326.1 | 2.13 |
| `milan_datapath/g_mmcm_servo.mmcm_servo` | 899 | 899 | 0 | 0 | 814 | 0 | 0 | 0 | 0 | 156 | 236.9 | 1.77 |
| `milan_datapath/avtp_rx_monitor` | 889 | 889 | 0 | 0 | 1,353 | 0 | 0 | 1 | 0 | 71 | 304.9 | 1.75 |
| `milan_datapath/aaf_latency_tap_bank` | 674 | 674 | 0 | 0 | 621 | 0 | 0 | 0 | 0 | 72 | 190.9 | 1.33 |
| `milan_datapath/aaf_packetizer` | 622 | 622 | 0 | 0 | 1,331 | 0 | 1 | 1 | 0 | 9 | 251.3 | 1.23 |
| `milan_datapath/@own` | 563 | 563 | 0 | 0 | 2,805 | 0 | 0 | 0 | 0 | 65 | 456.6 | 1.11 |
| `milan_datapath/g_rx_filter.rx_filter` | 512 | 512 | 0 | 0 | 1,570 | 0 | 0 | 0 | 0 | 0 | 247.4 | 1.01 |
| `milan_datapath/avtp_rx_parser` | 501 | 501 | 0 | 0 | 706 | 0 | 0 | 0 | 0 | 83 | 161.0 | 0.99 |
| `milan_datapath/g_tdm_render_live.g_master.chan_tdm_render` | 499 | 499 | 0 | 0 | 623 | 1 | 3 | 0 | 0 | 0 | 141.7 | 0.98 |
| `milan_datapath/g_aaf_meter.aaf_clock_meter` | 483 | 451 | 32 | 0 | 630 | 0 | 0 | 0 | 0 | 91 | 153.3 | 0.95 |
| `milan_datapath/g_maap.maap_engine` | 479 | 479 | 0 | 0 | 267 | 0 | 0 | 0 | 0 | 65 | 110.3 | 0.94 |
| `milan_datapath/render_setpoint` | 381 | 253 | 128 | 0 | 137 | 0 | 0 | 0 | 0 | 14 | 88.9 | 0.75 |
| `milan_datapath/media_grid_align` | 373 | 373 | 0 | 0 | 107 | 0 | 0 | 0 | 0 | 77 | 81.8 | 0.73 |
| `milan_datapath/crf_tx` | 317 | 317 | 0 | 0 | 311 | 0 | 0 | 0 | 1 | 19 | 90.1 | 0.62 |
| `milan_datapath/ptp_sync` | 297 | 297 | 0 | 0 | 405 | 0 | 0 | 0 | 0 | 36 | 97.5 | 0.59 |
| `milan_datapath/aaf_rx_depkt` | 273 | 271 | 2 | 0 | 144 | 0 | 1 | 1 | 0 | 17 | 62.9 | 0.54 |
| `milan_datapath/crf_rx` | 267 | 267 | 0 | 0 | 542 | 0 | 0 | 1 | 0 | 101 | 147.8 | 0.53 |
| `milan_datapath/talker_diag` | 225 | 225 | 0 | 0 | 359 | 0 | 0 | 0 | 0 | 87 | 113.2 | 0.44 |
| `milan_datapath/media_nco` | 130 | 130 | 0 | 0 | 46 | 0 | 0 | 0 | 1 | 30 | 27.3 | 0.26 |
| `milan_datapath/chan_map_render` | 112 | 112 | 0 | 0 | 676 | 0 | 0 | 0 | 0 | 0 | 89.0 | 0.22 |
| `milan_datapath/adp_tx_mux` | 109 | 109 | 0 | 0 | 24 | 0 | 0 | 0 | 0 | 5 | 17.1 | 0.21 |
| `milan_datapath/ts_counter` | 97 | 97 | 0 | 0 | 153 | 0 | 0 | 0 | 0 | 16 | 29.3 | 0.19 |
| `milan_datapath/ctl_tx_mux` | 85 | 85 | 0 | 0 | 22 | 0 | 0 | 0 | 0 | 4 | 13.9 | 0.17 |
| `milan_datapath/g_aif_tdm_master.g_solo.aaf_capture` | 75 | 41 | 34 | 0 | 243 | 2 | 0 | 0 | 0 | 8 | 47.1 | 0.15 |
| `milan_datapath/link_guard` | 72 | 72 | 0 | 0 | 114 | 0 | 0 | 0 | 0 | 25 | 31.0 | 0.14 |
| `milan_datapath/stream_table` | 58 | 58 | 0 | 0 | 69 | 0 | 0 | 0 | 0 | 6 | 17.0 | 0.11 |
| `milan_datapath/g_gptp_plane.gptp_ctl_mux` | 55 | 55 | 0 | 0 | 23 | 0 | 0 | 0 | 0 | 5 | 10.3 | 0.11 |
| `milan_datapath/ptp_clock_validity` | 51 | 51 | 0 | 0 | 125 | 0 | 0 | 0 | 0 | 20 | 31.2 | 0.10 |
| `milan_datapath/ethernet_counters` | 40 | 40 | 0 | 0 | 449 | 0 | 0 | 0 | 0 | 40 | 78.1 | 0.08 |
| `milan_datapath/tone_gen_media` | 38 | 38 | 0 | 0 | 30 | 0 | 0 | 0 | 0 | 0 | 7.3 | 0.07 |
| `milan_datapath/crf_dp_mux` | 34 | 34 | 0 | 0 | 23 | 0 | 0 | 0 | 0 | 5 | 7.8 | 0.07 |
| `milan_datapath/media_clock_restart` | 20 | 20 | 0 | 0 | 28 | 0 | 0 | 0 | 0 | 4 | 7.4 | 0.04 |
| `milan_datapath/pp_maap_shim` | 9 | 9 | 0 | 0 | 46 | 0 | 0 | 0 | 0 | 4 | 7.1 | 0.02 |
| `milan_datapath/ctl_ifg` | 8 | 8 | 0 | 0 | 10 | 0 | 0 | 0 | 0 | 0 | 2.2 | 0.02 |
| `milan_datapath/pcm_route` | 2 | 2 | 0 | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 0.3 | 0.00 |
| sharing adjustment | -109 | -109 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0.0 | - |
| **milan_datapath** | 42,200 | 40,388 | 1,812 | 0 | 48,433 | 3 | 30 | 12 | 14 | 3,107 | 13,083.0 | 83.12 |
<!-- end table: map-datapath -->

<!-- table: map-soc-names -->
| Name class | FF | IOB FF | LUT cells | LUT-RAM cells | RAMB36 | RAMB18 | DSP |
|---|---:|---:|---:|---:|---:|---:|---:|
| DDR3 controller | 1,334 | 0 | 823 | 0 | 0 | 0 | 0 |
| DDR3 PHY | 1,265 | 0 | 873 | 1 | 0 | 0 | 0 |
| Other named cells | 1,185 | 9 | 271 | 1 | 0 | 0 | 0 |
| CSR banks and bus | 714 | 0 | 123 | 0 | 0 | 0 | 0 |
| Clock-domain crossings | 420 | 0 | 0 | 0 | 0 | 0 | 0 |
| Ethernet MAC and PHY | 368 | 9 | 123 | 0 | 0 | 0 | 0 |
| Milan NIC bridge | 272 | 0 | 77 | 0 | 0 | 0 | 0 |
| Generated FIFO storage | 199 | 0 | 34 | 582 | 29 | 9 | 0 |
| SPI flash | 194 | 0 | 57 | 0 | 0 | 0 | 0 |
| SPI master | 121 | 0 | 1 | 0 | 0 | 0 | 0 |
| Anonymous LUT | 0 | 0 | 3,231 | 0 | 0 | 0 | 0 |
| BIOS ROM and SRAM | 0 | 0 | 0 | 0 | 18 | 1 | 0 |
<!-- end table: map-soc-names -->

<!-- table: map-ranking -->
| Rank | Block | LUT | Logic | LUTRAM | SRL | FF | IOB FF | RAMB36 | RAMB18 | DSP | CARRY4 | Slices | LUT % of image |
|---:|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 1 | `@own` | 4,847 | 4,551 | 294 | 2 | 6,072 | 18 | 47 | 10 | 0 | 274 | 1,535.7 | 9.55 |
| 2 | `milan_datapath/pp_shadow/u_pp/u_notify` | 3,149 | 3,053 | 96 | 0 | 3,301 | 0 | 0 | 0 | 0 | 188 | 955.9 | 6.20 |
| 3 | `milan_datapath/csr` | 3,073 | 3,073 | 0 | 0 | 2,141 | 0 | 0 | 2 | 0 | 37 | 703.5 | 6.05 |
| 4 | `milan_datapath/g_gptp_plane.u_gptp_shadow/u_engine/u_ucpu` | 2,088 | 1,956 | 132 | 0 | 728 | 0 | 1 | 1 | 4 | 105 | 393.9 | 4.11 |
| 5 | `milan_datapath/pp_shadow/u_pp/u_aecp/@own` | 1,791 | 1,791 | 0 | 0 | 1,099 | 0 | 1 | 0 | 0 | 106 | 452.1 | 3.53 |
| 6 | `milan_datapath/pp_shadow/u_pp/u_aecp/u_ucpu` | 1,716 | 1,584 | 132 | 0 | 496 | 0 | 3 | 0 | 0 | 72 | 342.7 | 3.38 |
| 7 | `milan_datapath/pp_shadow/u_pp/u_listener` | 1,407 | 1,407 | 0 | 0 | 1,110 | 0 | 5 | 0 | 0 | 28 | 345.7 | 2.77 |
| 8 | `milan_datapath/pp_shadow/u_pp/u_srp/u_encoder` | 1,317 | 1,149 | 168 | 0 | 1,062 | 0 | 0 | 0 | 0 | 99 | 365.7 | 2.59 |
| 9 | `milan_datapath/pp_shadow/u_pp/u_aecp/u_d3` | 1,317 | 1,317 | 0 | 0 | 485 | 0 | 0 | 0 | 0 | 112 | 285.9 | 2.59 |
| 10 | `milan_datapath/pp_shadow/u_pp/u_aecp/u_dyn` | 1,142 | 1,142 | 0 | 0 | 467 | 0 | 0 | 0 | 0 | 44 | 240.4 | 2.25 |
| 11 | `milan_datapath/chan_map_capture` | 1,079 | 1,079 | 0 | 0 | 1,321 | 0 | 1 | 0 | 0 | 20 | 326.1 | 2.12 |
| 12 | `milan_datapath/pp_shadow/u_pp/u_aecp/u_store` | 979 | 893 | 86 | 0 | 694 | 0 | 2 | 0 | 1 | 107 | 270.4 | 1.93 |
| 13 | `milan_datapath/avtp_rx_monitor` | 889 | 889 | 0 | 0 | 1,353 | 0 | 0 | 1 | 0 | 71 | 304.9 | 1.75 |
| 14 | `milan_datapath/pp_shadow/u_pp/u_timer` | 884 | 884 | 0 | 0 | 179 | 0 | 1 | 0 | 0 | 229 | 187.3 | 1.74 |
| 15 | `milan_datapath/pp_shadow/u_pp/u_srp/@own` | 862 | 862 | 0 | 0 | 2,792 | 0 | 0 | 0 | 0 | 0 | 626.7 | 1.70 |
| 16 | `milan_datapath/g_gptp_plane.u_gptp_shadow/u_engine/@own` | 852 | 544 | 308 | 0 | 2,158 | 0 | 0 | 0 | 0 | 54 | 432.3 | 1.68 |
| 17 | `VexiiRiscvLitex_f5f08b170311db53220574624f819159/vexiis_0_logic_core/@own` | 798 | 774 | 22 | 2 | 1,041 | 0 | 0 | 0 | 0 | 35 | 233.5 | 1.57 |
| 18 | `milan_datapath/pp_shadow/u_pp/u_nvm_shadow` | 793 | 695 | 98 | 0 | 1,118 | 0 | 0 | 0 | 0 | 51 | 231.9 | 1.56 |
| 19 | `milan_datapath/g_mmcm_servo.mmcm_servo/@own` | 791 | 791 | 0 | 0 | 770 | 0 | 0 | 0 | 0 | 148 | 213.1 | 1.56 |
| 20 | `milan_datapath/pp_shadow/u_pp/u_originator` | 726 | 706 | 20 | 0 | 885 | 0 | 0 | 0 | 0 | 53 | 250.8 | 1.43 |
| 21 | `milan_datapath/pp_shadow/u_pp/u_talker` | 710 | 654 | 56 | 0 | 517 | 0 | 0 | 0 | 0 | 17 | 170.5 | 1.40 |
| 22 | `VexiiRiscvLitex_f5f08b170311db53220574624f819159/@own` | 700 | 700 | 0 | 0 | 1,807 | 0 | 0 | 0 | 0 | 17 | 285.9 | 1.38 |
| 23 | `milan_datapath/aaf_packetizer` | 622 | 622 | 0 | 0 | 1,331 | 0 | 1 | 1 | 0 | 9 | 251.3 | 1.23 |
| 24 | `milan_datapath/g_gptp_plane.u_gptp_shadow/@own` | 615 | 571 | 44 | 0 | 985 | 0 | 0 | 0 | 0 | 64 | 243.6 | 1.21 |
| 25 | `milan_datapath/pp_shadow/u_pp/u_srp/u_talker` | 608 | 608 | 0 | 0 | 671 | 0 | 0 | 0 | 0 | 20 | 184.3 | 1.20 |
| 26 | `milan_datapath/pp_shadow/u_pp/u_srp/u_decoder` | 584 | 584 | 0 | 0 | 630 | 0 | 0 | 1 | 0 | 61 | 171.5 | 1.15 |
| 27 | `milan_datapath/@own` | 563 | 563 | 0 | 0 | 2,805 | 0 | 0 | 0 | 0 | 65 | 456.6 | 1.11 |
| 28 | `milan_datapath/pp_shadow/u_pp/u_rx_validator` | 548 | 548 | 0 | 0 | 751 | 0 | 0 | 1 | 0 | 45 | 191.1 | 1.08 |
| 29 | `milan_datapath/g_rx_filter.rx_filter/mac_cam` | 511 | 511 | 0 | 0 | 1,568 | 0 | 0 | 0 | 0 | 0 | 247.0 | 1.01 |
| 30 | `milan_datapath/pp_shadow/u_nvm` | 505 | 505 | 0 | 0 | 476 | 0 | 0 | 0 | 4 | 45 | 147.7 | 0.99 |
| 31 | `milan_datapath/avtp_rx_parser` | 501 | 501 | 0 | 0 | 706 | 0 | 0 | 0 | 0 | 83 | 161.0 | 0.99 |
| 32 | `milan_datapath/g_gptp_plane.u_gptp_shadow/u_engine/u_parser` | 485 | 485 | 0 | 0 | 370 | 0 | 0 | 0 | 0 | 52 | 127.8 | 0.95 |
| 33 | `milan_datapath/g_aaf_meter.aaf_clock_meter` | 483 | 451 | 32 | 0 | 630 | 0 | 0 | 0 | 0 | 91 | 153.3 | 0.95 |
| 34 | `milan_datapath/g_tdm_render_live.g_master.chan_tdm_render/u_fcdc` | 482 | 482 | 0 | 0 | 24 | 0 | 3 | 0 | 0 | 0 | 77.1 | 0.95 |
| 35 | `milan_datapath/g_maap.maap_engine` | 479 | 479 | 0 | 0 | 267 | 0 | 0 | 0 | 0 | 65 | 110.3 | 0.94 |
| 36 | `milan_datapath/pp_shadow/u_pp/u_srp/u_listener` | 474 | 474 | 0 | 0 | 667 | 0 | 0 | 0 | 0 | 29 | 154.7 | 0.93 |
| 37 | `milan_datapath/pp_shadow/u_pp/u_adp` | 443 | 395 | 48 | 0 | 471 | 0 | 0 | 0 | 1 | 32 | 130.6 | 0.87 |
| 38 | `milan_datapath/g_gptp_plane.u_gptp_shadow/u_txret` | 442 | 442 | 0 | 0 | 1,159 | 0 | 0 | 0 | 0 | 26 | 226.0 | 0.87 |
| 39 | `milan_datapath/pp_shadow/u_pp/u_nvm_port` | 439 | 439 | 0 | 0 | 127 | 0 | 0 | 0 | 0 | 58 | 96.7 | 0.86 |
| 40 | `VexiiRiscvLitex_f5f08b170311db53220574624f819159/peripheral_toAxiLite4_logic_bridge/@own` | 406 | 406 | 0 | 0 | 103 | 0 | 0 | 0 | 0 | 14 | 78.7 | 0.80 |
| 41 | `milan_datapath/pp_shadow/u_pp/@own` | 382 | 382 | 0 | 0 | 3,084 | 0 | 0 | 0 | 0 | 20 | 418.3 | 0.75 |
| 42 | `milan_datapath/pp_shadow/u_pp/u_dispatch/u_aecp_q` | 382 | 190 | 192 | 0 | 287 | 0 | 0 | 0 | 0 | 6 | 80.7 | 0.75 |
| 43 | `milan_datapath/render_setpoint` | 381 | 253 | 128 | 0 | 137 | 0 | 0 | 0 | 0 | 14 | 88.9 | 0.75 |
| 44 | `milan_datapath/media_grid_align` | 373 | 373 | 0 | 0 | 107 | 0 | 0 | 0 | 0 | 77 | 81.8 | 0.73 |
| 45 | `milan_datapath/aaf_latency_tap_bank/g_ltap.aaf_latency_taps/rx_chain` | 343 | 343 | 0 | 0 | 290 | 0 | 0 | 0 | 0 | 32 | 93.8 | 0.68 |
| 46 | `milan_datapath/pp_shadow/u_pp/u_tx_slots` | 341 | 341 | 0 | 0 | 135 | 0 | 1 | 0 | 0 | 5 | 75.6 | 0.67 |
| 47 | `milan_datapath/pp_shadow/u_pp/u_aecp/u_resp` | 332 | 332 | 0 | 0 | 260 | 0 | 0 | 0 | 0 | 16 | 86.0 | 0.65 |
| 48 | `milan_datapath/aaf_latency_tap_bank/g_ltap.aaf_latency_taps/tx_chain` | 326 | 326 | 0 | 0 | 290 | 0 | 0 | 0 | 0 | 32 | 90.6 | 0.64 |
| 49 | `milan_datapath/crf_tx/@own` | 314 | 314 | 0 | 0 | 307 | 0 | 0 | 0 | 1 | 19 | 89.2 | 0.62 |
| 50 | `milan_datapath/ptp_sync` | 297 | 297 | 0 | 0 | 405 | 0 | 0 | 0 | 0 | 36 | 97.5 | 0.58 |
| 51 | `milan_datapath/pp_shadow/u_pp/u_dispatch/u_acmp_q` | 285 | 149 | 136 | 0 | 204 | 0 | 0 | 0 | 0 | 0 | 56.0 | 0.56 |
| 52 | `milan_datapath/crf_rx` | 267 | 267 | 0 | 0 | 542 | 0 | 0 | 1 | 0 | 101 | 147.8 | 0.53 |
| 53 | `milan_datapath/g_gptp_plane.u_gptp_shadow/u_engine/u_timer` | 245 | 245 | 0 | 0 | 320 | 0 | 0 | 0 | 0 | 28 | 77.9 | 0.48 |
| 54 | `milan_datapath/talker_diag` | 225 | 225 | 0 | 0 | 359 | 0 | 0 | 0 | 0 | 87 | 113.2 | 0.44 |
| 55 | `VexiiRiscvLitex_f5f08b170311db53220574624f819159/vexiis_0_logic_core/integer_RegFilePlugin_logic_regfile_fpga` | 225 | 225 | 0 | 0 | 0 | 0 | 0 | 2 | 0 | 8 | 29.9 | 0.44 |
| 56 | `milan_datapath/pp_shadow/u_pp/u_srp/u_admission` | 224 | 224 | 0 | 0 | 207 | 0 | 0 | 0 | 2 | 16 | 53.6 | 0.44 |
| 57 | `milan_datapath/aaf_rx_depkt/frame_fifo` | 223 | 223 | 0 | 0 | 32 | 0 | 1 | 1 | 0 | 5 | 38.4 | 0.44 |
| 58 | `milan_datapath/pp_shadow/u_pp/u_event_router` | 221 | 221 | 0 | 0 | 51 | 0 | 0 | 0 | 0 | 0 | 45.8 | 0.43 |
| 59 | `milan_datapath/pp_shadow/u_pp/u_tx_arbiter` | 204 | 204 | 0 | 0 | 182 | 0 | 0 | 0 | 0 | 4 | 51.1 | 0.40 |
| 60 | `VexiiRiscvLitex_f5f08b170311db53220574624f819159/mem_toAxi4_logic_bridge/@own` | 192 | 192 | 0 | 0 | 338 | 0 | 0 | 0 | 0 | 0 | 78.1 | 0.38 |
| 61 | `KL_gptp_gmii_launch/@own` | 178 | 178 | 0 | 0 | 201 | 0 | 0 | 0 | 0 | 3 | 49.2 | 0.35 |
| 62 | `milan_datapath/g_gptp_plane.u_gptp_shadow/u_engine/u_txslot` | 150 | 126 | 24 | 0 | 62 | 0 | 0 | 0 | 0 | 0 | 31.3 | 0.29 |
| 63 | `VexiiRiscvLitex_f5f08b170311db53220574624f819159/dma_bridge_write_bridge/aligner` | 146 | 144 | 2 | 0 | 143 | 0 | 0 | 0 | 0 | 8 | 38.4 | 0.29 |
| 64 | `milan_datapath/pp_shadow/u_pp/u_srp/u_vlan` | 140 | 128 | 12 | 0 | 126 | 0 | 0 | 0 | 0 | 9 | 38.4 | 0.28 |
| 65 | `milan_datapath/pp_shadow/u_pp/u_scoreboard` | 138 | 138 | 0 | 0 | 169 | 0 | 0 | 0 | 0 | 16 | 44.1 | 0.27 |
| 66 | `milan_datapath/pp_shadow/u_pp/u_prng` | 133 | 133 | 0 | 0 | 150 | 0 | 0 | 0 | 0 | 22 | 46.1 | 0.26 |
| 67 | `milan_datapath/media_nco` | 130 | 130 | 0 | 0 | 46 | 0 | 0 | 0 | 1 | 30 | 27.3 | 0.26 |
| 68 | `VexiiRiscvLitex_f5f08b170311db53220574624f819159/vexiis_0_logic_core/FetchCachelessPlugin_logic_buffer_words` | 128 | 104 | 24 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 19.9 | 0.25 |
| 69 | `milan_datapath/pp_shadow/u_pp/u_ca_builder` | 127 | 127 | 0 | 0 | 152 | 0 | 0 | 0 | 0 | 0 | 39.8 | 0.25 |
| 70 | `VexiiRiscvLitex_f5f08b170311db53220574624f819159/ioBus_to_peripheral_bus_cc/a_1/@own` | 120 | 120 | 0 | 0 | 16 | 0 | 1 | 1 | 0 | 0 | 21.5 | 0.24 |
| 71 | `VexiiRiscvLitex_f5f08b170311db53220574624f819159/unified_mBus_to_mem_toAxi4_up_widthAdapter/upsize_d_ctx/contexts` | 119 | 115 | 4 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 18.5 | 0.23 |
| 72 | `milan_datapath/chan_map_render` | 112 | 112 | 0 | 0 | 676 | 0 | 0 | 0 | 0 | 0 | 89.0 | 0.22 |
| 73 | `milan_datapath/adp_tx_mux` | 109 | 109 | 0 | 0 | 24 | 0 | 0 | 0 | 0 | 5 | 17.1 | 0.21 |
| 74 | `milan_datapath/g_mmcm_servo.mmcm_servo/u_tick_cdc` | 103 | 103 | 0 | 0 | 4 | 0 | 0 | 0 | 0 | 8 | 18.5 | 0.20 |
| 75 | `VexiiRiscvLitex_f5f08b170311db53220574624f819159/dma_bridge_read_bridge/aligner` | 99 | 91 | 8 | 0 | 122 | 0 | 0 | 1 | 0 | 8 | 32.4 | 0.20 |
| 76 | `milan_datapath/ts_counter` | 97 | 97 | 0 | 0 | 153 | 0 | 0 | 0 | 0 | 16 | 29.3 | 0.19 |
| 77 | `VexiiRiscvLitex_f5f08b170311db53220574624f819159/unified_mBus_arbiter_core/a_arbiter` | 96 | 96 | 0 | 0 | 8 | 0 | 0 | 0 | 0 | 0 | 19.7 | 0.19 |
| 78 | `milan_datapath/pp_shadow/u_pp/g_rx_pool[5].u_rx_slots` | 89 | 89 | 0 | 0 | 62 | 0 | 1 | 0 | 0 | 3 | 21.6 | 0.17 |
| 79 | `milan_datapath/ctl_tx_mux` | 85 | 85 | 0 | 0 | 22 | 0 | 0 | 0 | 0 | 4 | 13.9 | 0.17 |
| 80 | `milan_datapath/pp_shadow/u_pp/u_srp/u_domain` | 77 | 77 | 0 | 0 | 108 | 0 | 0 | 0 | 0 | 0 | 26.9 | 0.15 |
| 81 | `milan_datapath/pp_shadow/u_pp/u_normalizer` | 72 | 72 | 0 | 0 | 307 | 0 | 0 | 0 | 0 | 6 | 48.7 | 0.14 |
| 82 | `milan_datapath/link_guard` | 72 | 72 | 0 | 0 | 114 | 0 | 0 | 0 | 0 | 25 | 31.0 | 0.14 |
| 83 | `milan_datapath/pp_shadow/ctl_fifo` | 72 | 72 | 0 | 0 | 33 | 0 | 1 | 1 | 0 | 3 | 14.2 | 0.14 |
| 84 | `VexiiRiscvLitex_f5f08b170311db53220574624f819159/peripheral_toAxiLite4_logic_bridge/a_buffered_fork2` | 71 | 71 | 0 | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 12.3 | 0.14 |
| 85 | `milan_datapath/pp_shadow/u_pp/u_mrp_strip` | 70 | 70 | 0 | 0 | 107 | 0 | 1 | 0 | 0 | 17 | 30.6 | 0.14 |
| 86 | `milan_datapath/pp_shadow/u_pp/u_dispatch/u_adp_q` | 70 | 10 | 60 | 0 | 88 | 0 | 0 | 0 | 0 | 0 | 18.0 | 0.14 |
| 87 | `milan_datapath/g_gptp_plane.u_gptp_shadow/rx_fifo` | 69 | 69 | 0 | 0 | 33 | 0 | 1 | 1 | 0 | 7 | 15.6 | 0.14 |
| 88 | `milan_datapath/stream_table` | 58 | 58 | 0 | 0 | 69 | 0 | 0 | 0 | 0 | 6 | 17.0 | 0.11 |
| 89 | `VexiiRiscvLitex_f5f08b170311db53220574624f819159/peripheral_bus_decoder_core/d_arbiter` | 58 | 58 | 0 | 0 | 8 | 0 | 0 | 0 | 0 | 0 | 9.2 | 0.11 |
| 90 | `VexiiRiscvLitex_f5f08b170311db53220574624f819159/dma_filter_down_to_unified_mBus_cc/a_1/@own` | 57 | 57 | 0 | 0 | 16 | 0 | 1 | 1 | 0 | 0 | 10.6 | 0.11 |
| 91 | `VexiiRiscvLitex_f5f08b170311db53220574624f819159/peripheral_clint_thread_core` | 55 | 55 | 0 | 0 | 208 | 0 | 0 | 0 | 0 | 24 | 41.3 | 0.11 |
| 92 | `milan_datapath/g_gptp_plane.u_gptp_shadow/tx_fifo` | 55 | 55 | 0 | 0 | 30 | 0 | 1 | 1 | 0 | 3 | 13.6 | 0.11 |
| 93 | `milan_datapath/g_gptp_plane.gptp_ctl_mux` | 55 | 55 | 0 | 0 | 23 | 0 | 0 | 0 | 0 | 5 | 10.3 | 0.11 |
| 94 | `milan_datapath/g_aif_tdm_master.g_solo.aaf_capture/u_tcdc` | 54 | 20 | 34 | 0 | 82 | 0 | 0 | 0 | 0 | 0 | 21.2 | 0.11 |
| 95 | `milan_datapath/pp_shadow/u_pp/u_side_port` | 53 | 53 | 0 | 0 | 6 | 0 | 0 | 0 | 0 | 0 | 8.0 | 0.10 |
| 96 | `milan_datapath/ptp_clock_validity` | 51 | 51 | 0 | 0 | 125 | 0 | 0 | 0 | 0 | 20 | 31.2 | 0.10 |
| 97 | `milan_datapath/aaf_rx_depkt/@own` | 51 | 49 | 2 | 0 | 112 | 0 | 0 | 0 | 0 | 12 | 24.4 | 0.10 |
| 98 | `milan_datapath/pp_shadow/u_pp/g_rx_pool[2].u_rx_slots` | 50 | 50 | 0 | 0 | 62 | 0 | 1 | 0 | 0 | 2 | 14.9 | 0.10 |
| 99 | `VexiiRiscvLitex_f5f08b170311db53220574624f819159/dma_filter_down_to_unified_mBus_cc/d_1/@own` | 46 | 18 | 28 | 0 | 57 | 0 | 0 | 0 | 0 | 0 | 15.9 | 0.09 |
| 100 | `VexiiRiscvLitex_f5f08b170311db53220574624f819159/ioBus_to_peripheral_bus_cc/d_1/@own` | 45 | 15 | 30 | 0 | 60 | 0 | 0 | 0 | 0 | 0 | 19.7 | 0.09 |
| 101 | `milan_datapath/pp_shadow/u_pp/g_rx_pool[0].u_rx_slots` | 38 | 38 | 0 | 0 | 38 | 0 | 1 | 0 | 0 | 7 | 12.8 | 0.07 |
| 102 | `milan_datapath/tone_gen_media` | 38 | 38 | 0 | 0 | 30 | 0 | 0 | 0 | 0 | 0 | 7.3 | 0.07 |
| 103 | `milan_datapath/pp_shadow/u_pp/u_trace` | 37 | 37 | 0 | 0 | 18 | 0 | 1 | 0 | 0 | 4 | 9.2 | 0.07 |
| 104 | `milan_datapath/pp_shadow/u_pp/g_rx_pool[4].u_rx_slots` | 36 | 36 | 0 | 0 | 22 | 0 | 1 | 0 | 0 | 3 | 8.2 | 0.07 |
| 105 | `VexiiRiscvLitex_f5f08b170311db53220574624f819159/dma_filter_logic_core` | 36 | 36 | 0 | 0 | 21 | 0 | 0 | 0 | 0 | 0 | 9.2 | 0.07 |
| 106 | `VexiiRiscvLitex_f5f08b170311db53220574624f819159/peripheral_plic_intc_thread_logic` | 34 | 34 | 0 | 0 | 145 | 0 | 0 | 0 | 0 | 0 | 32.4 | 0.07 |
| 107 | `milan_datapath/crf_dp_mux` | 34 | 34 | 0 | 0 | 23 | 0 | 0 | 0 | 0 | 5 | 7.8 | 0.07 |
| 108 | `KL_mac_rmon_events/@own` | 32 | 32 | 0 | 0 | 66 | 0 | 0 | 0 | 0 | 8 | 12.9 | 0.06 |
| 109 | `milan_datapath/pp_shadow/u_pp/g_rx_pool[1].u_rx_slots` | 30 | 30 | 0 | 0 | 22 | 0 | 1 | 0 | 0 | 3 | 7.6 | 0.06 |
| 110 | `milan_datapath/pp_shadow/u_pp/u_dispatch/@own` | 28 | 28 | 0 | 0 | 48 | 0 | 0 | 0 | 0 | 12 | 14.9 | 0.06 |
| 111 | `VexiiRiscvLitex_f5f08b170311db53220574624f819159/dma_bridge_write_bridge/compactor/@own` | 27 | 27 | 0 | 0 | 40 | 0 | 0 | 0 | 0 | 0 | 9.7 | 0.05 |
| 112 | `milan_datapath/g_aif_tdm_master.g_solo.aaf_capture/@own` | 21 | 21 | 0 | 0 | 161 | 2 | 0 | 0 | 0 | 8 | 25.9 | 0.04 |
| 113 | `milan_datapath/media_clock_restart` | 20 | 20 | 0 | 0 | 28 | 0 | 0 | 0 | 0 | 4 | 7.4 | 0.04 |
| 114 | `milan_datapath/g_gptp_plane.u_gptp_shadow/u_txticket` | 19 | 19 | 0 | 0 | 54 | 0 | 0 | 0 | 0 | 0 | 9.4 | 0.04 |
| 115 | `milan_datapath/g_tdm_render_live.g_master.chan_tdm_render/@own` | 18 | 18 | 0 | 0 | 599 | 1 | 0 | 0 | 0 | 0 | 64.6 | 0.04 |
| 116 | `VexiiRiscvLitex_f5f08b170311db53220574624f819159/unified_mBus_to_mem_toAxi4_up_widthAdapter/@own` | 17 | 17 | 0 | 0 | 346 | 0 | 0 | 0 | 0 | 0 | 60.5 | 0.03 |
| 117 | `VexiiRiscvLitex_f5f08b170311db53220574624f819159/unified_mBus_decoder_core/d_arbiter` | 13 | 13 | 0 | 0 | 7 | 0 | 0 | 0 | 0 | 0 | 3.5 | 0.03 |
| 118 | `milan_datapath/pp_shadow/u_pp/u_nvm_arb` | 13 | 13 | 0 | 0 | 4 | 0 | 0 | 0 | 0 | 0 | 2.5 | 0.03 |
| 119 | `VexiiRiscvLitex_f5f08b170311db53220574624f819159/mem_toAxi4_logic_bridge/d_arbiter` | 13 | 13 | 0 | 0 | 3 | 0 | 0 | 0 | 0 | 0 | 2.4 | 0.03 |
| 120 | `VexiiRiscvLitex_f5f08b170311db53220574624f819159/mem_toAxi4_logic_bridge/a_ctx/contexts` | 13 | 9 | 4 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 2.4 | 0.03 |
| 121 | `milan_datapath/pp_shadow/u_pp/u_dispatch/u_maap_q` | 11 | 7 | 4 | 0 | 8 | 0 | 0 | 0 | 0 | 0 | 2.9 | 0.02 |
| 122 | `VexiiRiscvLitex_f5f08b170311db53220574624f819159/dma_bridge_down_arbiter_core/a_arbiter` | 11 | 11 | 0 | 0 | 7 | 0 | 0 | 0 | 0 | 0 | 2.6 | 0.02 |
| 123 | `milan_datapath/pp_shadow/@own` | 9 | 9 | 0 | 0 | 321 | 0 | 0 | 0 | 0 | 6 | 42.1 | 0.02 |
| 124 | `milan_datapath/pp_maap_shim` | 9 | 9 | 0 | 0 | 46 | 0 | 0 | 0 | 0 | 4 | 7.1 | 0.02 |
| 125 | `milan_datapath/ethernet_counters/event_counter_gen[3].counter_inst` | 8 | 8 | 0 | 0 | 32 | 0 | 0 | 0 | 0 | 8 | 8.8 | 0.02 |
| 126 | `milan_datapath/ethernet_counters/event_counter_gen[4].counter_inst` | 8 | 8 | 0 | 0 | 32 | 0 | 0 | 0 | 0 | 8 | 8.8 | 0.02 |
| 127 | `milan_datapath/ethernet_counters/event_counter_gen[5].counter_inst` | 8 | 8 | 0 | 0 | 32 | 0 | 0 | 0 | 0 | 8 | 8.8 | 0.02 |
| 128 | `milan_datapath/ethernet_counters/event_counter_gen[7].counter_inst` | 8 | 8 | 0 | 0 | 32 | 0 | 0 | 0 | 0 | 8 | 8.8 | 0.02 |
| 129 | `milan_datapath/ethernet_counters/event_counter_gen[8].counter_inst` | 8 | 8 | 0 | 0 | 32 | 0 | 0 | 0 | 0 | 8 | 9.0 | 0.02 |
| 130 | `milan_datapath/ctl_ifg` | 8 | 8 | 0 | 0 | 10 | 0 | 0 | 0 | 0 | 0 | 2.2 | 0.02 |
| 131 | `VexiiRiscvLitex_f5f08b170311db53220574624f819159/dma_bridge_write_bridge/onPerId_bridge/onAw_halted_fork2` | 8 | 8 | 0 | 0 | 2 | 0 | 0 | 0 | 0 | 0 | 1.2 | 0.02 |
| 132 | `KL_mac_rmon_events/gen_evt_cdc[8].gen_live_lane.evt_cdc` | 8 | 8 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 1.1 | 0.02 |
| 133 | `milan_datapath/g_mmcm_servo.mmcm_servo/u_batch_hs` | 7 | 7 | 0 | 0 | 40 | 0 | 0 | 0 | 0 | 0 | 5.3 | 0.01 |
| 134 | `VexiiRiscvLitex_f5f08b170311db53220574624f819159/mem_toAxi4_logic_bridge/a_halted_fork2` | 6 | 6 | 0 | 0 | 2 | 0 | 0 | 0 | 0 | 0 | 1.4 | 0.01 |
| 135 | `KL_gptp_gmii_launch/u_rec_cdc` | 5 | 5 | 0 | 0 | 102 | 0 | 0 | 0 | 0 | 0 | 16.0 | 0.01 |
| 136 | `milan_datapath/aaf_latency_tap_bank/@own` | 5 | 5 | 0 | 0 | 9 | 0 | 0 | 0 | 0 | 0 | 1.5 | 0.01 |
| 137 | `KL_gptp_gmii_launch/u_seal_cdc` | 4 | 4 | 0 | 0 | 14 | 0 | 0 | 0 | 0 | 0 | 2.9 | 0.01 |
| 138 | `VexiiRiscvLitex_f5f08b170311db53220574624f819159/dma_bridge_read_bridge/compactor` | 4 | 4 | 0 | 0 | 4 | 0 | 0 | 0 | 0 | 0 | 1.5 | 0.01 |
| 139 | `VexiiRiscvLitex_f5f08b170311db53220574624f819159/peripheral_clint_time_cc_driver/@own` | 3 | 3 | 0 | 0 | 130 | 0 | 0 | 0 | 0 | 0 | 17.4 | 0.01 |
| 140 | `VexiiRiscvLitex_f5f08b170311db53220574624f819159/dma_bridge_read_bridge/toTileink` | 3 | 3 | 0 | 0 | 4 | 0 | 0 | 0 | 0 | 0 | 1.0 | 0.01 |
| 141 | `milan_datapath/crf_tx/u_evt_cdc` | 3 | 3 | 0 | 0 | 4 | 0 | 0 | 0 | 0 | 0 | 0.9 | 0.01 |
| 142 | `VexiiRiscvLitex_f5f08b170311db53220574624f819159/vexiis_0_priv_stoptime_regNext_cc_driver/@own` | 3 | 3 | 0 | 0 | 3 | 0 | 0 | 0 | 0 | 0 | 1.2 | 0.01 |
| 143 | `KL_mac_rmon_events/gen_evt_cdc[3].gen_live_lane.evt_cdc` | 3 | 3 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0.3 | 0.01 |
| 144 | `KL_mac_rmon_events/gen_evt_cdc[4].gen_live_lane.evt_cdc` | 2 | 2 | 0 | 0 | 4 | 0 | 0 | 0 | 0 | 0 | 0.8 | 0.00 |
| 145 | `KL_mac_rmon_events/gen_evt_cdc[5].gen_live_lane.evt_cdc` | 2 | 2 | 0 | 0 | 4 | 0 | 0 | 0 | 0 | 0 | 0.8 | 0.00 |
| 146 | `KL_mac_rmon_events/gen_evt_cdc[7].gen_live_lane.evt_cdc` | 2 | 2 | 0 | 0 | 4 | 0 | 0 | 0 | 0 | 0 | 0.6 | 0.00 |
| 147 | `VexiiRiscvLitex_f5f08b170311db53220574624f819159/dma_bridge_write_bridge/compactor/io_up_aw_fork2` | 2 | 2 | 0 | 0 | 2 | 0 | 0 | 0 | 0 | 0 | 0.6 | 0.00 |
| 148 | `milan_datapath/pcm_route` | 2 | 2 | 0 | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 0.3 | 0.00 |
| 149 | `milan_datapath/aaf_latency_tap_bank/g_ltap.aaf_latency_taps/@own` | 1 | 1 | 0 | 0 | 32 | 0 | 0 | 0 | 0 | 8 | 5.0 | 0.00 |
| 150 | `milan_datapath/g_rx_filter.rx_filter/@own` | 1 | 1 | 0 | 0 | 2 | 0 | 0 | 0 | 0 | 0 | 0.4 | 0.00 |
| 151 | `milan_datapath/pp_shadow/u_pp/u_desc_mem_guard` | 1 | 1 | 0 | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 0.2 | 0.00 |
| 152 | `milan_datapath/pp_shadow/u_pp/u_lsn_admit` | 1 | 1 | 0 | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 0.2 | 0.00 |
| 153 | `milan_datapath/ethernet_counters/@own` | 0 | 0 | 0 | 0 | 289 | 0 | 0 | 0 | 0 | 0 | 34.0 | 0.00 |
| 154 | `VexiiRiscvLitex_f5f08b170311db53220574624f819159/dma_filter_down_to_unified_mBus_cc/a_1/popToPushGray_buffercc` | 0 | 0 | 0 | 0 | 8 | 0 | 0 | 0 | 0 | 0 | 1.5 | 0.00 |
| 155 | `VexiiRiscvLitex_f5f08b170311db53220574624f819159/dma_filter_down_to_unified_mBus_cc/a_1/pushToPopGray_buffercc` | 0 | 0 | 0 | 0 | 8 | 0 | 0 | 0 | 0 | 0 | 1.5 | 0.00 |
| 156 | `VexiiRiscvLitex_f5f08b170311db53220574624f819159/dma_filter_down_to_unified_mBus_cc/d_1/popToPushGray_buffercc` | 0 | 0 | 0 | 0 | 8 | 0 | 0 | 0 | 0 | 0 | 0.8 | 0.00 |
| 157 | `VexiiRiscvLitex_f5f08b170311db53220574624f819159/dma_filter_down_to_unified_mBus_cc/d_1/pushToPopGray_buffercc` | 0 | 0 | 0 | 0 | 8 | 0 | 0 | 0 | 0 | 0 | 1.1 | 0.00 |
| 158 | `VexiiRiscvLitex_f5f08b170311db53220574624f819159/ioBus_to_peripheral_bus_cc/a_1/popToPushGray_buffercc` | 0 | 0 | 0 | 0 | 8 | 0 | 0 | 0 | 0 | 0 | 1.1 | 0.00 |
| 159 | `VexiiRiscvLitex_f5f08b170311db53220574624f819159/ioBus_to_peripheral_bus_cc/a_1/pushToPopGray_buffercc` | 0 | 0 | 0 | 0 | 8 | 0 | 0 | 0 | 0 | 0 | 1.0 | 0.00 |
| 160 | `VexiiRiscvLitex_f5f08b170311db53220574624f819159/ioBus_to_peripheral_bus_cc/d_1/popToPushGray_buffercc` | 0 | 0 | 0 | 0 | 8 | 0 | 0 | 0 | 0 | 0 | 1.8 | 0.00 |
| 161 | `VexiiRiscvLitex_f5f08b170311db53220574624f819159/ioBus_to_peripheral_bus_cc/d_1/pushToPopGray_buffercc` | 0 | 0 | 0 | 0 | 8 | 0 | 0 | 0 | 0 | 0 | 1.8 | 0.00 |
| 162 | `milan_datapath/pp_shadow/u_pp/u_release_merge` | 0 | 0 | 0 | 0 | 4 | 0 | 0 | 0 | 0 | 0 | 0.4 | 0.00 |
| 163 | `VexiiRiscvLitex_f5f08b170311db53220574624f819159/dma_bridge_write_bridge/onPerId_bridge/@own` | 0 | 0 | 0 | 0 | 3 | 0 | 0 | 0 | 0 | 0 | 0.4 | 0.00 |
| 164 | `VexiiRiscvLitex_f5f08b170311db53220574624f819159/bufferCC_19` | 0 | 0 | 0 | 0 | 2 | 0 | 0 | 0 | 0 | 0 | 0.2 | 0.00 |
| 165 | `VexiiRiscvLitex_f5f08b170311db53220574624f819159/bufferCC_20` | 0 | 0 | 0 | 0 | 2 | 0 | 0 | 0 | 0 | 0 | 0.2 | 0.00 |
| 166 | `VexiiRiscvLitex_f5f08b170311db53220574624f819159/cpuResetCtrl_fiber_aggregator_asyncBuffers_0` | 0 | 0 | 0 | 0 | 2 | 0 | 0 | 0 | 0 | 0 | 0.5 | 0.00 |
| 167 | `VexiiRiscvLitex_f5f08b170311db53220574624f819159/cpuResetCtrl_fiber_buffer` | 0 | 0 | 0 | 0 | 2 | 0 | 0 | 0 | 0 | 0 | 1.0 | 0.00 |
| 168 | `VexiiRiscvLitex_f5f08b170311db53220574624f819159/peripheral_clint_time_cc_driver/litex_reset_asyncAssertSyncDeassert_buffercc` | 0 | 0 | 0 | 0 | 2 | 0 | 0 | 0 | 0 | 0 | 0.4 | 0.00 |
| 169 | `VexiiRiscvLitex_f5f08b170311db53220574624f819159/peripheral_clint_time_cc_driver/outHitSignal_buffercc` | 0 | 0 | 0 | 0 | 2 | 0 | 0 | 0 | 0 | 0 | 0.2 | 0.00 |
| 170 | `VexiiRiscvLitex_f5f08b170311db53220574624f819159/peripheral_clint_time_cc_driver/pushArea_target_buffercc` | 0 | 0 | 0 | 0 | 2 | 0 | 0 | 0 | 0 | 0 | 1.0 | 0.00 |
| 171 | `VexiiRiscvLitex_f5f08b170311db53220574624f819159/peripheral_plic_intc_to_vexiis_0_priv_mei_flag_buffercc` | 0 | 0 | 0 | 0 | 2 | 0 | 0 | 0 | 0 | 0 | 0.2 | 0.00 |
| 172 | `VexiiRiscvLitex_f5f08b170311db53220574624f819159/vexiis_0_priv_stoptime_regNext_cc_driver/outHitSignal_buffercc` | 0 | 0 | 0 | 0 | 2 | 0 | 0 | 0 | 0 | 0 | 0.2 | 0.00 |
| 173 | `VexiiRiscvLitex_f5f08b170311db53220574624f819159/vexiis_0_priv_stoptime_regNext_cc_driver/pushArea_target_buffercc` | 0 | 0 | 0 | 0 | 2 | 0 | 0 | 0 | 0 | 0 | 1.0 | 0.00 |
| 174 | `VexiiRiscvLitex_f5f08b170311db53220574624f819159/vexiis_0_priv_stoptime_regNext_cc_driver/toplevel_cpuResetCtrl_reset_asyncAssertSyncDeassert_buffercc` | 0 | 0 | 0 | 0 | 2 | 0 | 0 | 0 | 0 | 0 | 0.4 | 0.00 |
| 175 | `VexiiRiscvLitex_f5f08b170311db53220574624f819159/dma_bridge_read_bridge/onPerId_bridge` | 0 | 0 | 0 | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 0.1 | 0.00 |
<!-- end table: map-ranking -->

<!-- table: yosys-stream-total -->
| Measure | Fixed | Per stream | Per channel | Per stream-channel | Points | Residual RMS | Largest residual |
|---|---:|---:|---:|---:|---:|---:|---:|
| LUT | 82,767.4 | 13,881.0 | 401.2 | -99.0 | 6 | 1,227.5 | 2,431.8 |
| FF | 50,785.2 | 3,202.0 | 22.6 | -3.4 | 6 | 81.4 | 161.4 |
| BRAM | 26.1 | 0.8 | 0.0 | -0.0 | 6 | 0.1 | 0.1 |
| DSP | 21.5 | 0.4 | 0.1 | -0.0 | 6 | 0.2 | 0.4 |
<!-- end table: yosys-stream-total -->

<!-- table: yosys-stream-data -->
| Point | N | C | LUT | FF | BRAM | DSP | LUT residual |
|---|---:|---:|---:|---:|---:|---:|---:|
| ship | 1 | 8 | 97,607 | 54,041 | 27.0 | 22 | -1,459 |
| streams-2 | 2 | 8 | 114,587 | 57,477 | 28.0 | 23 | 2,432 |
| streams-4 | 4 | 8 | 137,523 | 63,611 | 29.5 | 23 | -811 |
| chans-2 | 1 | 2 | 97,577 | 54,041 | 27.0 | 22 | 324 |
| chans-4 | 1 | 4 | 97,371 | 54,041 | 27.0 | 22 | -486 |
| streams-4-chans-2 | 4 | 2 | 138,302 | 63,611 | 29.5 | 23 | 0 |
<!-- end table: yosys-stream-data -->

<!-- table: yosys-stream-blocks -->
| Block | LUT fixed | LUT per stream | LUT per channel | LUT per N*C | LUT RMS | FF per stream | FF RMS |
|---|---:|---:|---:|---:|---:|---:|---:|
| `KL_pp_shadow` | 48,964 | 7,693.2 | 355.9 | -52.0 | 1,275.5 | 1,428.2 | 53.8 |
| `@own` | 4,311 | 4,849.7 | 123.7 | -58.9 | 240.2 | 824.7 | 0.4 |
| `KL_chan_map_capture` | 828 | 471.2 | -0.2 | 0.0 | 0.8 | 335.6 | 6.4 |
| `KL_avtp_rx_monitor_ctx` | 1,069 | 228.9 | 19.9 | -3.0 | 71.7 | 105.1 | 3.1 |
| `KL_talker_diag_ctx` | 25 | 217.9 | -19.8 | 3.0 | 71.2 | 166.0 | 0.0 |
| `KL_render_setpoint` | 213 | 193.1 | 0.2 | -0.0 | 0.7 | 28.0 | 0.0 |
| `KL_stream_table` | -4 | 93.4 | -1.8 | 0.3 | 6.4 | 69.0 | 0.0 |
| `avtp_stream_parser` | 1,905 | 80.4 | 2.6 | -0.4 | 9.3 | 0.7 | 0.1 |
| `KL_chan_map_render` | 2,454 | -15.0 | -84.6 | 12.8 | 304.1 | 192.0 | 0.0 |
| `milan_csr` | 4,585 | 26.5 | 0.2 | -0.0 | 0.9 | 0.4 | 0.2 |
| `KL_media_clock_restart` | 19 | 17.9 | -0.2 | 0.0 | 0.7 | 10.0 | 0.0 |
| `KL_aaf_packetizer` | 1,379 | 14.2 | 5.7 | -0.8 | 27.7 | 39.9 | 17.4 |
| `KL_pp_maap_shim` | 108 | 4.9 | 0.4 | -0.1 | 1.4 | 1.0 | 0.0 |
| `KL_aaf_clock_meter` | 568 | 3.4 | -0.5 | 0.1 | 1.9 | 0.3 | 0.1 |
<!-- end table: yosys-stream-blocks -->

<!-- table: vivado-opt-data -->
| Anchor | N | LUT | FF | BRAM | DSP | LUT residual |
|---|---:|---:|---:|---:|---:|---:|
| ship | 1 | 43,622 | 48,697 | 36.0 | 14 | -364 |
| streams-2 | 2 | 48,361 | 51,521 | 39.5 | 14 | 547 |
| streams-4 | 4 | 55,288 | 57,413 | 41.0 | 14 | -182 |
<!-- end table: vivado-opt-data -->

<!-- table: vivado-opt-fit -->
| Measure after optimization | Fixed | Per stream | Points | Residual RMS | Largest residual |
|---|---:|---:|---:|---:|---:|
| LUT | 40,158.5 | 3,827.9 | 3 | 393.6 | 546.6 |
| FF | 45,751.0 | 2,911.1 | 3 | 37.6 | 52.3 |
| BRAM | 35.2 | 1.5 | 3 | 0.8 | 1.2 |
| DSP | 14.0 | 0.0 | 3 | 0.0 | 0.0 |
<!-- end table: vivado-opt-fit -->

<!-- table: vivado-opt-blocks -->
| Block | LUT at N=1 | LUT per stream | LUT RMS | FF per stream | BRAM per stream |
|---|---:|---:|---:|---:|---:|
| `KL_pp_shadow` | 25,094 | 2,478.1 | 61.7 | 1,155.3 | 1.54 |
| `KL_chan_map_capture` | 1,080 | 316.9 | 14.7 | 350.9 | 0.00 |
| `milan_csr` | 2,893 | 210.6 | 119.4 | 27.9 | 0.00 |
| `KL_avtp_rx_monitor_ctx` | 1,011 | 208.5 | 81.0 | 24.8 | 0.00 |
| `KL_render_setpoint` | 380 | 205.1 | 0.9 | 28.0 | 0.00 |
| `@own` | 230 | 137.1 | 0.5 | 878.6 | 0.00 |
| `KL_aaf_packetizer` | 655 | 95.4 | 98.8 | 33.5 | -0.00 |
| `KL_chan_map_render` | 119 | 87.1 | 8.2 | 192.0 | 0.00 |
| `KL_talker_diag_ctx` | 281 | 65.6 | 17.9 | 166.0 | 0.00 |
| `KL_stream_table` | 58 | 55.1 | 3.9 | 69.0 | 0.00 |
| `KL_crf_rx` | 300 | -23.6 | 14.5 | 0.0 | 0.00 |
| `timestamp_counter` | 97 | 15.4 | 21.4 | 0.0 | 0.00 |
| `KL_maap` | 507 | -9.4 | 2.8 | 0.0 | 0.00 |
| `KL_aaf_latency_tap_bank` | 675 | -9.1 | 9.9 | 0.1 | 0.00 |
<!-- end table: vivado-opt-blocks -->

<!-- table: vivado-synth-data -->
| Anchor | N | LUT | FF | BRAM | DSP | LUT residual |
|---|---:|---:|---:|---:|---:|---:|
| ship | 1 | 44,305 | 48,821 | 36.0 | 14 | -387 |
| streams-2 | 2 | 49,185 | 51,622 | 39.5 | 14 | 580 |
| streams-4 | 4 | 56,238 | 57,533 | 41.0 | 14 | -193 |
<!-- end table: vivado-synth-data -->

<!-- table: vivado-synth-fit -->
| Measure after synthesis | Fixed | Per stream | Points | Residual RMS | Largest residual |
|---|---:|---:|---:|---:|---:|
| LUT | 40,778.5 | 3,913.2 | 3 | 417.7 | 580.1 |
| FF | 45,865.5 | 2,911.4 | 3 | 47.7 | 66.2 |
| BRAM | 35.2 | 1.5 | 3 | 0.8 | 1.2 |
| DSP | 14.0 | 0.0 | 3 | 0.0 | 0.0 |
<!-- end table: vivado-synth-fit -->

<!-- table: vivado-synth-blocks -->
| Block | LUT at N=1 | LUT per stream | LUT RMS | FF per stream | BRAM per stream |
|---|---:|---:|---:|---:|---:|
| `KL_pp_shadow` | 25,294 | 2,511.8 | 61.9 | 1,152.8 | 1.54 |
| `KL_chan_map_capture` | 1,081 | 317.9 | 14.7 | 350.9 | 0.00 |
| `milan_csr` | 2,935 | 231.6 | 123.8 | 27.9 | 0.00 |
| `KL_avtp_rx_monitor_ctx` | 1,008 | 214.8 | 100.8 | 24.8 | 0.00 |
| `KL_render_setpoint` | 380 | 212.8 | 2.9 | 28.0 | 0.00 |
| `@own` | 243 | 136.1 | 2.6 | 878.6 | 0.00 |
| `KL_chan_map_render` | 127 | 85.9 | 7.4 | 192.0 | 0.00 |
| `KL_aaf_packetizer` | 804 | 81.0 | 56.2 | 33.5 | -0.00 |
| `KL_talker_diag_ctx` | 283 | 64.8 | 18.7 | 166.0 | 0.00 |
| `KL_stream_table` | 58 | 55.1 | 3.9 | 69.0 | 0.00 |
| `avtp_stream_parser` | 605 | 37.6 | 11.4 | 1.8 | 0.00 |
| `KL_crf_rx` | 315 | -27.6 | 10.2 | 0.0 | 0.00 |
| `timestamp_counter` | 97 | 15.4 | 21.4 | 0.0 | 0.00 |
| `KL_aaf_latency_tap_bank` | 681 | -10.1 | 10.3 | 0.1 | 0.00 |
<!-- end table: vivado-synth-blocks -->

<!-- table: datapath-marginals -->
| Point | Change | LUT | FF | BRAM | DSP | LUT x calibration | Routed block LUT / FF | Blocks that moved most (LUT) |
|---|---|---:|---:|---:|---:|---:|---:|---|
| all-tier1-off | `DPROBES_P`=0, `LTAP_P`=0, `MAAP_P`=0, `MCSERVO_P`=0, `RXFILT_P`=0 | -3,456 | -3,453 | 0 | -1 | -1,545 | - | `KL_aaf_latency_tap_bank/KL_aaf_latency_taps/KL_aaf_latency_chain` -930; `KL_mmcm_drp_servo/@own` -858; `rx_mac_filter/tcam` -678 |
| chans-2 | `TALKER_WIRE_CHANS_P`=2 | -30 | 0 | 0 | 0 | -13 | - | `KL_pp_shadow/protocol_processor_top/KL_aecp_engine` -28; `@own` -15; `KL_aaf_packetizer` +8 |
| chans-4 | `TALKER_WIRE_CHANS_P`=4 | -236 | 0 | 0 | 0 | -105 | - | `@own` -268; `KL_pp_shadow/protocol_processor_top/KL_adp_engine` +18; `KL_aaf_packetizer` +14 |
| i2s | `AUDIO_IF_MASTER_P`=0, `AUDIO_IF_RENDER_SLOTS_P`=0, `AUDIO_IF_SLOTS_P`=0, `TALKER_WIRE_CHANS_P`=2 | -759 | -1,044 | 0 | +1 | -339 | - | `KL_tdm_render_master/@own` -858; `KL_tone_gen` +169; `KL_tdm_render_master/cdc_pair_fifo` -139 |
| no-aaf-meter | rm_ax7101_1x1_tdm8_noaafclk | -685 | -640 | 0 | 0 | -306 | 483 / 630 | `KL_aaf_clock_meter` -570; `@own` -238; `KL_pp_shadow/protocol_processor_top/KL_pp_acmp_listener` +80 |
| no-crf | rm_ax7101_1x1_tdm8_nocrf | -6,552 | -739 | 0 | 0 | -2,928 | - | `KL_pp_shadow/protocol_processor_top/KL_srp_top` -3,232; `KL_pp_shadow/protocol_processor_top/@own` -969; `@own` -928 |
| no-dprobes | `DPROBES_P`=0 | -26 | -74 | 0 | 0 | -12 | - | `@own` -26 |
| no-gptp-plane | `GPTP_PLANE_EN_P`=0 | -11,354 | -7,893 | -4.5 | -4 | -5,074 | 5,004 / 5,899 | `KL_gptp_shadow/KL_gptp_engine/@own` -3,838; `KL_gptp_shadow/KL_gptp_engine/KL_gptp_ucpu` -1,732; `@own` -1,566 |
| no-loopback | `LOOPBACK_P`=0 | -50 | -190 | 0 | 0 | -22 | - | `KL_chan_map_capture` -87; `@own` +38; `KL_mmcm_drp_servo/@own` -1 |
| no-ltap | `LTAP_P`=0 | -943 | -622 | 0 | 0 | -421 | 674 / 621 | `KL_aaf_latency_tap_bank/KL_aaf_latency_taps/KL_aaf_latency_chain` -930; `@own` -53; `KL_pp_shadow/protocol_processor_top/@own` +49 |
| no-maap | `MAAP_P`=0 | -782 | -268 | 0 | 0 | -349 | 479 / 267 | `KL_maap` -595; `@own` -235; `KL_pp_shadow/protocol_processor_top/@own` +49 |
| no-mcservo | `MCSERVO_P`=0 | -858 | -798 | 0 | -1 | -383 | 899 / 814 | `KL_mmcm_drp_servo/@own` -858; `KL_pp_shadow/protocol_processor_top/KL_adp_engine` -72; `KL_crf_rx` +67 |
| no-rxfilt | `RXFILT_P`=0 | -786 | -1,691 | 0 | 0 | -351 | 512 / 1,570 | `rx_mac_filter/tcam` -678; `rx_mac_filter/@own` -123; `KL_pp_shadow/protocol_processor_top/@own` +49 |
| render-0 | `AUDIO_IF_RENDER_SLOTS_P`=0 | -1,060 | -1,113 | 0 | 0 | -474 | 499 / 623 | `KL_tdm_render_master/@own` -858; `KL_tdm_render_master/cdc_pair_fifo` -139; `@own` -110 |
| ship-8x8 | `AUDIO_IF_CLK_HZ_P`=98304000, `AUDIO_IF_RENDER_SLOTS_P`=0, `AUDIO_IF_SLOTS_P`=32, `DPROBES_P`=0, `LOOPBACK_P`=0, `LTAP_P`=0, `N_STREAMS`=8 | +72,659 | +16,774 | +2.5 | 0 | 32,472 | - | `@own` +22,847; `KL_pp_shadow/protocol_processor_top/KL_acmp_talker` +20,212; `KL_pp_shadow/protocol_processor_top/KL_srp_top` +14,271 |
| streams-2 | `N_STREAMS`=2 | +16,980 | +3,436 | +1.0 | +1 | 7,589 | - | `KL_pp_shadow/protocol_processor_top/KL_acmp_talker` +6,390; `@own` +5,046; `KL_pp_shadow/protocol_processor_top/KL_srp_top` +2,210 |
| streams-4 | `N_STREAMS`=4 | +39,916 | +9,570 | +2.5 | +1 | 17,839 | - | `@own` +13,209; `KL_pp_shadow/protocol_processor_top/KL_acmp_talker` +10,722; `KL_pp_shadow/protocol_processor_top/KL_srp_top` +7,773 |
| streams-4-chans-2 | `N_STREAMS`=4, `TALKER_WIRE_CHANS_P`=2 | +40,695 | +9,570 | +2.5 | +1 | 18,187 | - | `@own` +14,028; `KL_pp_shadow/protocol_processor_top/KL_acmp_talker` +10,722; `KL_pp_shadow/protocol_processor_top/KL_srp_top` +7,772 |
| streams-8 (refused by a guard) | `N_STREAMS`=8 | +86,176 | +22,063 | +5.5 | +1 | 38,513 | - | `@own` +30,406; `KL_pp_shadow/protocol_processor_top/KL_acmp_talker` +20,139; `KL_pp_shadow/protocol_processor_top/KL_srp_top` +14,271 |
| streams-8-chans-2 (refused by a guard) | `N_STREAMS`=8, `TALKER_WIRE_CHANS_P`=2 | +87,432 | +22,063 | +5.5 | +1 | 39,075 | - | `@own` +31,950; `KL_pp_shadow/protocol_processor_top/KL_acmp_talker` +19,865; `KL_pp_shadow/protocol_processor_top/KL_srp_top` +14,271 |
| tdm16 | `AUDIO_IF_CLK_HZ_P`=49152000, `AUDIO_IF_RENDER_SLOTS_P`=0, `AUDIO_IF_SLOTS_P`=16 | -1,054 | -1,110 | 0 | 0 | -471 | - | `KL_tdm_render_master/@own` -858; `KL_tdm_render_master/cdc_pair_fifo` -139; `@own` -110 |
| tdm32 | `AUDIO_IF_CLK_HZ_P`=98304000, `AUDIO_IF_RENDER_SLOTS_P`=0, `AUDIO_IF_SLOTS_P`=32 | -1,053 | -1,107 | 0 | 0 | -471 | - | `KL_tdm_render_master/@own` -858; `KL_tdm_render_master/cdc_pair_fifo` -139; `@own` -110 |
| with-i2spb | `I2SPB_P`=1 | +673 | +678 | +1.0 | 0 | 301 | - | `KL_i2s_playback/@own` +440; `@own` +106; `KL_i2s_feed_mux` +83 |
| with-lpf | `LPF_P`=1 | -69 | 0 | 0 | 0 | -31 | - | `@own` -96; `KL_pp_shadow/protocol_processor_top/KL_aecp_engine` +32; `KL_mmcm_drp_servo/@own` -5 |
| with-pps | `PPS_P`=1 | +156 | +294 | 0 | 0 | 70 | - | `timestamp_counter` +117; `@own` +50; `KL_pp_shadow/protocol_processor_top/KL_aecp_engine` -28 |
<!-- end table: datapath-marginals -->

<!-- table: processor-marginals -->
| Point | Change | LUT | FF | BRAM | DSP | LUT x calibration | Routed block LUT / FF | Blocks that moved most (LUT) |
|---|---|---:|---:|---:|---:|---:|---:|---|
| pp-controls-2 | `N_CONTROL_P`=2 | -326 | +9 | 0 | 0 | - | - | `protocol_processor_top/KL_srp_top/KL_srp_talker_fsm` -125; `protocol_processor_top/KL_pp_rx_validator` -113; `protocol_processor_top/KL_adp_engine` -43 |
| pp-controls-4 | `N_CONTROL_P`=4 | -189 | +27 | 0 | 0 | - | - | `protocol_processor_top/KL_srp_top/KL_srp_talker_fsm` -125; `protocol_processor_top/KL_pp_rx_validator` -113; `protocol_processor_top/KL_aecp_engine/KL_aecp_dyn_state` -55 |
| pp-ctrl-12 | `PP_N_CTRL_C`=12 | +728 | -32 | 0 | 0 | - | - | `protocol_processor_top/KL_aecp_notify` +1,170; `protocol_processor_top/KL_srp_top/KL_srp_listener_fsm` -204; `protocol_processor_top/@own` -91 |
| pp-ctrl-32 (refused by a guard) | `PP_N_CTRL_C`=32 | +11,922 | +241 | 0 | 0 | - | - | `protocol_processor_top/KL_aecp_notify` +11,607; `protocol_processor_top/KL_pp_timer_service` +363; `protocol_processor_top/KL_srp_top/KL_srp_talker_fsm` -271 |
| pp-ctrl-4 | `PP_N_CTRL_C`=4 | -6,818 | -111 | 0 | 0 | - | - | `protocol_processor_top/KL_aecp_notify` -7,092; `protocol_processor_top/KL_pp_originator` +219; `protocol_processor_top/KL_acmp_nvm_shadow` +167 |
| pp-ctrl-8 | `PP_N_CTRL_C`=8 | -4,228 | -72 | 0 | 0 | - | - | `protocol_processor_top/KL_aecp_notify` -3,826; `protocol_processor_top/KL_srp_top/KL_srp_listener_fsm` -204; `protocol_processor_top/KL_acmp_talker` -105 |
| pp-idx-16 | `DESC_IDX_ENTRIES_P`=16 | -53 | -1 | 0 | 0 | - | - | `protocol_processor_top/KL_pp_rx_validator` -76; `protocol_processor_top/KL_aecp_engine/@own` -55; `protocol_processor_top/KL_acmp_nvm_shadow` +51 |
| pp-idx-64 | `DESC_IDX_ENTRIES_P`=64 | +112 | +1 | 0 | 0 | - | - | `protocol_processor_top/KL_aecp_engine/KL_aecp_desc_store` +80; `protocol_processor_top/KL_acmp_nvm_shadow` +51; `protocol_processor_top/KL_pp_rx_validator` -48 |
| pp-line-1008 | `DESC_LINE_BYTES_P`=1008 | -23 | 0 | 0 | 0 | - | - | `protocol_processor_top/KL_pp_rx_validator` -58; `protocol_processor_top/KL_aecp_engine/@own` -41; `protocol_processor_top/KL_adp_engine` +24 |
| pp-line-1152 (refused by a guard) | `DESC_LINE_BYTES_P`=1152 | +837 | +1 | 0 | 0 | - | - | `protocol_processor_top/KL_aecp_notify` +915; `protocol_processor_top/KL_pp_rx_validator` -76; `protocol_processor_top/KL_adp_engine` -33 |
| pp-line-288 (refused by a guard) | `DESC_LINE_BYTES_P`=288 | -20 | +63 | -1.0 | 0 | - | - | `protocol_processor_top/@own` -143; `protocol_processor_top/KL_aecp_engine/KL_aecp_desc_store` +88; `protocol_processor_top/KL_adp_engine` +88 |
| pp-line-512 (refused by a guard) | `DESC_LINE_BYTES_P`=512 | -433 | +64 | -1.0 | 0 | - | - | `protocol_processor_top/KL_aecp_notify` -276; `protocol_processor_top/@own` -143; `protocol_processor_top/KL_pp_rx_validator` -76 |
| pp-line-768 | `DESC_LINE_BYTES_P`=768 | +146 | 0 | 0 | 0 | - | - | `protocol_processor_top/KL_adp_engine` +88; `protocol_processor_top/@own` +49; `protocol_processor_top/KL_aecp_engine/KL_aecp_ucpu` +24 |
| pp-names-128 | `DESC_NAME_ENTRIES_P`=128 | +116 | +89 | +1.0 | 0 | - | - | `KL_nvm_backend` +248; `protocol_processor_top/@own` -143; `protocol_processor_top/KL_srp_top/KL_srp_admission` +70 |
| pp-names-235 (refused by a guard) | `DESC_NAME_ENTRIES_P`=235 | +78 | +89 | +3.0 | 0 | - | - | `KL_nvm_backend` +234; `protocol_processor_top/@own` -143; `protocol_processor_top/KL_srp_top/KL_srp_admission` +70 |
| pp-names-64 | `DESC_NAME_ENTRIES_P`=64 | -103 | +25 | 0 | 0 | - | - | `protocol_processor_top/@own` -143; `KL_nvm_backend` +89; `protocol_processor_top/KL_pp_rx_validator` -64 |
| pp-rxbytes-1152 | `RX_SLOT_BYTES_P`=1152 | +834 | +43 | +3.0 | 0 | - | - | `protocol_processor_top/KL_aecp_notify` +745; `protocol_processor_top/KL_pp_rx_slots` +84; `protocol_processor_top/KL_adp_engine` +67 |
| pp-rxbytes-288 | `RX_SLOT_BYTES_P`=288 | -129 | -31 | -3.0 | 0 | - | - | `protocol_processor_top/KL_adp_engine` -93; `protocol_processor_top/KL_acmp_talker` +80; `protocol_processor_top/KL_aecp_engine/@own` -31 |
| pp-rxfifo-2048 | `RX_FIFO_BYTES_P`=2048 | -4 | -5 | 0 | 0 | - | - | `axis_fifo` -4 |
| pp-rxfifo-8192 | `RX_FIFO_BYTES_P`=8192 | -40 | +5 | +1.0 | 0 | - | - | `protocol_processor_top/KL_pp_rx_validator` -46; `axis_fifo` +6 |
| pp-rxslots-2 | `RX_SLOTS_P`=2 | -850 | -161 | -3.0 | 0 | - | - | `protocol_processor_top/KL_aecp_notify` -602; `protocol_processor_top/KL_pp_rx_slots` -216; `protocol_processor_top/KL_pp_rx_validator` -69 |
| pp-rxslots-8 | `RX_SLOTS_P`=8 | +525 | +316 | +3.0 | 0 | - | - | `protocol_processor_top/KL_pp_rx_slots` +528; `protocol_processor_top/KL_acmp_talker` -51; `protocol_processor_top/KL_pp_rx_validator` -50 |
| pp-si3 | `N_SPORT_IN_P`=2, `N_SPORT_OUT_P`=2, `N_STREAM_IN_P`=3, `N_STREAM_OUT_P`=3 | +10,780 | +1,555 | 0 | 0 | - | - | `protocol_processor_top/KL_acmp_talker` +6,443; `protocol_processor_top/KL_srp_top/KL_srp_talker_fsm` +948; `protocol_processor_top/KL_srp_top/KL_srp_listener_fsm` +881 |
| pp-si5 | `N_SPORT_IN_P`=4, `N_SPORT_OUT_P`=4, `N_STREAM_IN_P`=5, `N_STREAM_OUT_P`=5 | +22,044 | +4,177 | 0 | 0 | - | - | `protocol_processor_top/KL_acmp_talker` +10,572; `protocol_processor_top/KL_srp_top/KL_srp_talker_fsm` +3,258; `protocol_processor_top/KL_srp_top/KL_srp_listener_fsm` +2,604 |
| pp-si9 | `N_SPORT_IN_P`=8, `N_SPORT_OUT_P`=8, `N_STREAM_IN_P`=9, `N_STREAM_OUT_P`=9 | +42,959 | +9,645 | 0 | 0 | - | - | `protocol_processor_top/KL_acmp_talker` +20,248; `protocol_processor_top/KL_srp_top/KL_srp_talker_fsm` +6,957; `protocol_processor_top/KL_srp_top/KL_srp_listener_fsm` +5,642 |
| pp-txslots-2 | `TX_STD_SLOTS_P`=2 | +586 | -97 | 0 | 0 | - | - | `protocol_processor_top/KL_aecp_notify` +856; `protocol_processor_top/KL_pp_tx_slots` -163; `protocol_processor_top/KL_pp_rx_validator` -113 |
| pp-txslots-8 | `TX_STD_SLOTS_P`=8 | +797 | +159 | +1.0 | 0 | - | - | `protocol_processor_top/@own` +499; `protocol_processor_top/KL_pp_tx_slots` +317; `protocol_processor_top/KL_pp_rx_validator` -121 |
| pp-units-2 | `N_AUDIO_UNIT_P`=2, `N_CLK_DOM_P`=2 | -249 | +57 | 0 | 0 | - | - | `protocol_processor_top/KL_srp_top/KL_srp_talker_fsm` -125; `protocol_processor_top/KL_pp_rx_validator` -113; `protocol_processor_top/KL_adp_engine` -43 |
| pp-units-4 | `N_AUDIO_UNIT_P`=4, `N_CLK_DOM_P`=4 | +251 | +171 | 0 | 0 | - | - | `protocol_processor_top/KL_adp_engine` +152; `protocol_processor_top/KL_pp_rx_validator` -113; `protocol_processor_top/@own` -96 |
<!-- end table: processor-marginals -->

<!-- table: processor-parameters -->
| Parameter | Values | LUT per unit | FF per unit | BRAM per unit | LUT residual RMS | Largest LUT residual |
|---|---|---:|---:|---:|---:|---:|
| `DESC_IDX_ENTRIES_P` | 16, 32, 64 | 3.45 | 0.04 | 0.000 | 0.9 | 1.3 |
| `DESC_LINE_BYTES_P` | 576, 768, 1,008 | -0.08 | 0.00 | 0.000 | 73.5 | 103.7 |
| `DESC_NAME_ENTRIES_P` | 39, 64, 128 | 1.72 | 1.00 | 0.010 | 62.0 | 85.0 |
| `N_AUDIO_UNIT_P+N_CLK_DOM_P` | 1, 2, 4 | 107.43 | 57.00 | 0.000 | 154.0 | 213.9 |
| `N_CONTROL_P` | 1, 2, 4 | -44.21 | 9.00 | 0.000 | 121.8 | 169.1 |
| `N_SPORT_IN_P+N_SPORT_OUT_P+N_STREAM_IN_P+N_STREAM_OUT_P` | 1, 2, 4, 8 | 5,885.97 | 1,367.45 | -0.000 | 1,988.8 | 2,759.3 |
| `PP_N_CTRL_C` | 4, 8, 12, 16 | 635.25 | 9.33 | 0.000 | 1,224.0 | 2,037.0 |
| `RX_FIFO_BYTES_P` | 2,048, 4,096, 8,192 | -0.01 | 0.00 | 0.000 | 7.4 | 10.3 |
| `RX_SLOTS_P` | 2, 4, 8 | 215.18 | 79.43 | 0.960 | 181.3 | 251.8 |
| `RX_SLOT_BYTES_P` | 288, 576, 1,152 | 1.16 | 0.08 | 0.010 | 88.9 | 123.4 |
| `TX_STD_SLOTS_P` | 2, 4, 8 | 58.61 | 42.25 | 0.180 | 303.8 | 421.9 |
<!-- end table: processor-parameters -->

<!-- table: adp-marginals -->
| Point | Change | LUT | FF | BRAM | DSP | LUT x calibration | Routed block LUT / FF | Blocks that moved most (LUT) |
|---|---|---:|---:|---:|---:|---:|---:|---|
| adp-if-2 | `N_IF_P`=2 | +239 | +76 | 0 | 0 | - | - | `KL_adp_engine` +239 |
| adp-if-4 | `N_IF_P`=4 | +493 | +226 | 0 | 0 | - | - | `KL_adp_engine` +493 |
<!-- end table: adp-marginals -->

<!-- table: tdm-model -->
| Point | Capture slots | LUT | FF | BRAM | DSP |
|---|---:|---:|---:|---:|---:|
| render-0 | 8 | 96,547 | 52,928 | 27.0 | 22 |
| tdm16 | 16 | 96,553 | 52,931 | 27.0 | 22 |
| tdm32 | 32 | 96,554 | 52,934 | 27.0 | 22 |
<!-- end table: tdm-model -->

<!-- table: calibration-totals -->
| Anchor | Measure | Yosys hierarchical | Yosys flattened | Vivado synth | Vivado opt | Opt / hierarchical | Opt / flattened |
|---|---|---:|---:|---:|---:|---:|---:|
| ship | LUT | 97,607 | 108,067 | 44,305 | 43,622 | 0.447 | 0.404 |
| ship | FF | 54,041 | 47,718 | 48,821 | 48,697 | 0.901 | 1.021 |
| ship-8x8 | LUT | 170,266 | 173,181 | 61,439 | 60,454 | 0.355 | 0.349 |
| ship-8x8 | FF | 70,815 | 61,823 | 61,436 | 61,383 | 0.867 | 0.993 |
| streams-2 | LUT | 114,587 | 123,111 | 49,185 | 48,361 | 0.422 | 0.393 |
| streams-2 | FF | 57,477 | 51,127 | 51,622 | 51,521 | 0.896 | 1.008 |
| streams-4 | LUT | 137,523 | 146,016 | 56,238 | 55,288 | 0.402 | 0.379 |
| streams-4 | FF | 63,611 | 57,321 | 57,533 | 57,413 | 0.903 | 1.002 |
<!-- end table: calibration-totals -->

<!-- table: calibration-blocks -->
| Block | Yosys LUT | Vivado opt LUT | Opt / Yosys LUT | Opt / Yosys FF | Routed LUT | Routed / opt |
|---|---:|---:|---:|---:|---:|---:|
| `KL_pp_shadow` | 57,515 | 25,094 | 0.436 | 0.904 | 23,904 | 0.953 |
| `KL_gptp_shadow` | 9,414 | 5,204 | 0.553 | 0.920 | 5,004 | 0.962 |
| `milan_csr` | 4,612 | 2,893 | 0.627 | 0.616 | 3,073 | 1.062 |
| `KL_chan_map_capture` | 1,299 | 1,080 | 0.831 | 0.954 | 1,079 | 0.999 |
| `KL_avtp_rx_monitor_ctx` | 1,345 | 1,011 | 0.752 | 1.240 | 889 | 0.879 |
| `KL_mmcm_drp_servo` | 865 | 912 | 1.054 | 1.028 | 899 | 0.986 |
| `KL_aaf_latency_tap_bank` | 938 | 675 | 0.720 | 1.000 | 674 | 0.999 |
| `KL_aaf_packetizer` | 1,396 | 655 | 0.469 | 0.974 | 622 | 0.950 |
| `KL_aaf_clock_meter` | 570 | 534 | 0.937 | 0.992 | 483 | 0.904 |
| `avtp_stream_parser` | 1,991 | 519 | 0.261 | 0.844 | 501 | 0.965 |
| `rx_mac_filter` | 801 | 513 | 0.640 | 0.928 | 512 | 0.998 |
| `KL_maap` | 595 | 507 | 0.852 | 0.996 | 479 | 0.945 |
| `KL_tdm_render_master` | 997 | 507 | 0.509 | 0.576 | 499 | 0.984 |
| `KL_media_grid_align` | 310 | 383 | 1.235 | 1.000 | 373 | 0.974 |
| `KL_render_setpoint` | 407 | 380 | 0.934 | 0.851 | 381 | 1.003 |
| `KL_crf_tx` | 443 | 322 | 0.727 | 1.000 | 317 | 0.984 |
| `ptp_csr_sync` | 8 | 307 | 38.375 | 1.000 | 297 | 0.967 |
| `KL_crf_rx` | 370 | 300 | 0.811 | 0.996 | 267 | 0.890 |
| `KL_aaf_rx_depacketizer` | 268 | 297 | 1.108 | 0.548 | 273 | 0.919 |
| `adp_tx_arbiter` | 356 | 283 | 0.795 | 1.000 | 283 | 1.000 |
| `KL_talker_diag_ctx` | 196 | 281 | 1.434 | 1.000 | 225 | 0.801 |
| `@own` | 9,458 | 230 | 0.024 | 0.906 | 563 | 2.448 |
| `KL_media_nco` | 107 | 131 | 1.224 | 1.000 | 130 | 0.992 |
| `KL_chan_map_render` | 2,238 | 119 | 0.053 | 0.893 | 112 | 0.941 |
| `timestamp_counter` | 368 | 97 | 0.264 | 1.000 | 97 | 1.000 |
| `KL_tdm_capture_master` | 91 | 78 | 0.857 | 0.988 | 75 | 0.962 |
| `ethernet_events` | 94 | 73 | 0.777 | 1.997 | 40 | 0.548 |
| `KL_link_guard` | 101 | 68 | 0.673 | 1.018 | 72 | 1.059 |
| `KL_tone_gen` | 150 | 62 | 0.413 | 1.000 | 38 | 0.613 |
| `KL_stream_table` | 85 | 58 | 0.682 | 1.000 | 58 | 1.000 |
| `KL_ptp_clock_validity` | 52 | 32 | 0.615 | 1.000 | 51 | 1.594 |
| `KL_media_clock_restart` | 36 | 23 | 0.639 | 1.000 | 20 | 0.870 |
| `KL_pp_maap_shim` | 114 | 9 | 0.079 | 0.422 | 9 | 1.000 |
| `tx_ifg_gasket` | 15 | 8 | 0.533 | 1.000 | 8 | 1.000 |
| `KL_pcm_route` | 2 | 2 | 1.000 | 1.000 | 2 | 1.000 |
<!-- end table: calibration-blocks -->

<!-- table: redundancy-blocks -->
| Routed block | LUT | FF | RAMB36 | RAMB18 | DSP |
|---|---:|---:|---:|---:|---:|
| `KL_gptp_gmii_launch` | 186 | 317 | 0 | 0 | 0 |
| `KL_mac_rmon_events` | 49 | 78 | 0 | 0 | 0 |
| `milan_datapath/g_gptp_plane.u_gptp_shadow` | 5,004 | 5,899 | 3 | 3 | 4 |
| `milan_datapath/g_gptp_plane.gptp_ctl_mux` | 55 | 23 | 0 | 0 | 0 |
| `milan_datapath/g_rx_filter.rx_filter` | 512 | 1,570 | 0 | 0 | 0 |
| `milan_datapath/ts_counter` | 97 | 153 | 0 | 0 | 0 |
| `milan_datapath/ptp_sync` | 297 | 405 | 0 | 0 | 0 |
| `milan_datapath/ptp_clock_validity` | 51 | 125 | 0 | 0 | 0 |
| `milan_datapath/link_guard` | 72 | 114 | 0 | 0 | 0 |
| `milan_datapath/ethernet_counters` | 40 | 449 | 0 | 0 | 0 |
| `milan_datapath/ctl_tx_mux` | 85 | 22 | 0 | 0 | 0 |
| `milan_datapath/ctl_ifg` | 8 | 10 | 0 | 0 | 0 |
| `milan_datapath/adp_tx_mux` | 109 | 24 | 0 | 0 | 0 |
| `milan_datapath/crf_dp_mux` | 34 | 23 | 0 | 0 | 0 |
| `milan_datapath/avtp_rx_parser` | 501 | 706 | 0 | 0 | 0 |
| **sum** | **7,100** | **9,918** | **3** | **3** | **4** |
<!-- end table: redundancy-blocks -->

<!-- table: guard-refusals -->
| Point | Guard that fires |
|---|---|
| pp-ctrl-32 | `F08.4: owner tags OVERLAP at SI=2 SO=2 (8-bit expiry bus)` |
| pp-line-1152 | `DESC_LINE_BYTES_P=1152 is above 1008: 16 + line passes the 1024-byte cursor`; `RESP_D8_CAP_BYTES_P=1168 outside 524..1024 (the 10-bit cursor)` |
| pp-line-288 | `response buffer (304 B) is smaller than GET_DYNAMIC_INFO limit (524 B)`; `DESC_LINE_BYTES_P=288 is below 576: no room for a 71-record GET_AUDIO_MAP page`; `RESP_D8_CAP_BYTES_P=304 outside 524..1024 (the 10-bit cursor)` |
| pp-line-512 | `DESC_LINE_BYTES_P=512 is below 576: no room for a 71-record GET_AUDIO_MAP page` |
| pp-names-235 | `KL_nvm_backend: N_NAME_P=235 outside 1..128: the NAME block is 0x80..0xFF.` |
| streams-8 | `KL_nvm_backend: N_NAME_P=235 outside 1..128: the NAME block is 0x80..0xFF.` |
| streams-8-chans-2 | `KL_nvm_backend: N_NAME_P=235 outside 1..128: the NAME block is 0x80..0xFF.` |
<!-- end table: guard-refusals -->

<!-- table: soc-outcomes -->
| Variant | Changed flags | Outcome | Refusal |
|---|---|---|---|
| axilite | `--bus-standard axi-lite` | accepted | - |
| cpu2 | `--cpu-count 2` | refused | `--software-profile baremetal requires --cpu vexiiriscv --xlen 32 --cpu-count 1` |
| l1-caches | `--scala-args=--with-fetch-l1 --with-lsu-l1` | refused | `--software-profile baremetal requires no FPU, --l2-bytes 0, and no --scala-args overrides` |
| l2-8k | `--l2-bytes 8192` | refused | `--software-profile baremetal requires no FPU, --l2-bytes 0, and no --scala-args overrides` |
| naxriscv | `--cpu naxriscv` | refused | `--software-profile baremetal requires --cpu vexiiriscv --xlen 32 --cpu-count 1` |
| rv64 | `--xlen 64` | refused | `--software-profile baremetal requires --cpu vexiiriscv --xlen 32 --cpu-count 1` |
| rv64-fpu | `--xlen 64`, `--with-fpu` | refused | `--software-profile baremetal requires --cpu vexiiriscv --xlen 32 --cpu-count 1` |
| ship | as shipped | accepted | - |
<!-- end table: soc-outcomes -->

<!-- table: soc-prices -->
| Variant | Part | LUT | FF | RAMB36 | RAMB18 | DSP |
|---|---|---:|---:|---:|---:|---:|
| axilite | cpu | 4,574 | 5,337 | 0 | 0 | 0 |
| axilite | top | 10,100 | 8,805 | 14 | 3 | 0 |
| ship | cpu | 4,574 | 5,337 | 0 | 0 | 0 |
| ship | top | 9,778 | 8,690 | 14 | 3 | 0 |
<!-- end table: soc-prices -->

