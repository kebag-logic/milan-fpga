
# Create Project

create_project -force -name alinx_ax7101 -part xc7a100t-fgg484-2
set_msg_config -id {Common 17-55} -new_severity {Warning}
set_param general.maxThreads 32

# Add project commands


# Add Sources

read_verilog -v {$PACKET/scratch/repo/protocol-processor/hdl/acmp/pp_acmp_pkg.sv}
set_property file_type SystemVerilog [get_files {$PACKET/scratch/repo/protocol-processor/hdl/acmp/pp_acmp_pkg.sv}]
read_verilog -v {$PACKET/scratch/repo/protocol-processor/hdl/adp/pp_adp_pkg.sv}
set_property file_type SystemVerilog [get_files {$PACKET/scratch/repo/protocol-processor/hdl/adp/pp_adp_pkg.sv}]
read_verilog -v {$PACKET/scratch/repo/protocol-processor/hdl/aecp/ucpu_pkg.sv}
set_property file_type SystemVerilog [get_files {$PACKET/scratch/repo/protocol-processor/hdl/aecp/ucpu_pkg.sv}]
read_verilog -v {$PACKET/scratch/repo/protocol-processor/hdl/common/pp_pkg.sv}
set_property file_type SystemVerilog [get_files {$PACKET/scratch/repo/protocol-processor/hdl/common/pp_pkg.sv}]
read_verilog -v {$PACKET/scratch/repo/protocol-processor/hdl/srp/srp_pkg.sv}
set_property file_type SystemVerilog [get_files {$PACKET/scratch/repo/protocol-processor/hdl/srp/srp_pkg.sv}]
read_verilog -v {$PACKET/scratch/repo/protocol-processor/hdl/acmp/KL_acmp_nvm_shadow.sv}
set_property file_type SystemVerilog [get_files {$PACKET/scratch/repo/protocol-processor/hdl/acmp/KL_acmp_nvm_shadow.sv}]
read_verilog -v {$PACKET/scratch/repo/protocol-processor/hdl/acmp/KL_acmp_talker.sv}
set_property file_type SystemVerilog [get_files {$PACKET/scratch/repo/protocol-processor/hdl/acmp/KL_acmp_talker.sv}]
read_verilog -v {$PACKET/scratch/repo/protocol-processor/hdl/acmp/KL_pp_acmp_listener.sv}
set_property file_type SystemVerilog [get_files {$PACKET/scratch/repo/protocol-processor/hdl/acmp/KL_pp_acmp_listener.sv}]
read_verilog -v {$PACKET/scratch/repo/protocol-processor/hdl/acmp/KL_pp_acmp_lsn_admit.sv}
set_property file_type SystemVerilog [get_files {$PACKET/scratch/repo/protocol-processor/hdl/acmp/KL_pp_acmp_lsn_admit.sv}]
read_verilog -v {$PACKET/scratch/repo/protocol-processor/hdl/adp/KL_adp_engine.sv}
set_property file_type SystemVerilog [get_files {$PACKET/scratch/repo/protocol-processor/hdl/adp/KL_adp_engine.sv}]
read_verilog -v {$PACKET/scratch/repo/protocol-processor/hdl/aecp/KL_aecp_ca_originator.sv}
set_property file_type SystemVerilog [get_files {$PACKET/scratch/repo/protocol-processor/hdl/aecp/KL_aecp_ca_originator.sv}]
read_verilog -v {$PACKET/scratch/repo/protocol-processor/hdl/aecp/KL_aecp_desc_mem_guard.sv}
set_property file_type SystemVerilog [get_files {$PACKET/scratch/repo/protocol-processor/hdl/aecp/KL_aecp_desc_mem_guard.sv}]
read_verilog -v {$PACKET/scratch/repo/protocol-processor/hdl/aecp/KL_aecp_desc_store.sv}
set_property file_type SystemVerilog [get_files {$PACKET/scratch/repo/protocol-processor/hdl/aecp/KL_aecp_desc_store.sv}]
read_verilog -v {$PACKET/scratch/repo/protocol-processor/hdl/aecp/KL_aecp_dyn_state.sv}
set_property file_type SystemVerilog [get_files {$PACKET/scratch/repo/protocol-processor/hdl/aecp/KL_aecp_dyn_state.sv}]
read_verilog -v {$PACKET/scratch/repo/protocol-processor/hdl/aecp/KL_aecp_engine.sv}
set_property file_type SystemVerilog [get_files {$PACKET/scratch/repo/protocol-processor/hdl/aecp/KL_aecp_engine.sv}]
read_verilog -v {$PACKET/scratch/repo/protocol-processor/hdl/aecp/KL_aecp_notify.sv}
set_property file_type SystemVerilog [get_files {$PACKET/scratch/repo/protocol-processor/hdl/aecp/KL_aecp_notify.sv}]
read_verilog -v {$PACKET/scratch/repo/protocol-processor/hdl/aecp/KL_aecp_resp_buf.sv}
set_property file_type SystemVerilog [get_files {$PACKET/scratch/repo/protocol-processor/hdl/aecp/KL_aecp_resp_buf.sv}]
read_verilog -v {$PACKET/scratch/repo/protocol-processor/hdl/aecp/KL_aecp_ucpu.sv}
set_property file_type SystemVerilog [get_files {$PACKET/scratch/repo/protocol-processor/hdl/aecp/KL_aecp_ucpu.sv}]
read_verilog -v {$PACKET/scratch/repo/protocol-processor/hdl/common/KL_pp_prng.sv}
set_property file_type SystemVerilog [get_files {$PACKET/scratch/repo/protocol-processor/hdl/common/KL_pp_prng.sv}]
read_verilog -v {$PACKET/scratch/repo/protocol-processor/hdl/common/KL_pp_timer_service.sv}
set_property file_type SystemVerilog [get_files {$PACKET/scratch/repo/protocol-processor/hdl/common/KL_pp_timer_service.sv}]
read_verilog -v {$PACKET/scratch/repo/protocol-processor/hdl/maap/KL_pp_maap.sv}
set_property file_type SystemVerilog [get_files {$PACKET/scratch/repo/protocol-processor/hdl/maap/KL_pp_maap.sv}]
read_verilog -v {$PACKET/scratch/repo/protocol-processor/hdl/packet_engine/KL_pp_dispatch.sv}
set_property file_type SystemVerilog [get_files {$PACKET/scratch/repo/protocol-processor/hdl/packet_engine/KL_pp_dispatch.sv}]
read_verilog -v {$PACKET/scratch/repo/protocol-processor/hdl/packet_engine/KL_pp_event_router.sv}
set_property file_type SystemVerilog [get_files {$PACKET/scratch/repo/protocol-processor/hdl/packet_engine/KL_pp_event_router.sv}]
read_verilog -v {$PACKET/scratch/repo/protocol-processor/hdl/packet_engine/KL_pp_normalizer.sv}
set_property file_type SystemVerilog [get_files {$PACKET/scratch/repo/protocol-processor/hdl/packet_engine/KL_pp_normalizer.sv}]
read_verilog -v {$PACKET/scratch/repo/protocol-processor/hdl/packet_engine/KL_pp_nvm_mgr_arb.sv}
set_property file_type SystemVerilog [get_files {$PACKET/scratch/repo/protocol-processor/hdl/packet_engine/KL_pp_nvm_mgr_arb.sv}]
read_verilog -v {$PACKET/scratch/repo/protocol-processor/hdl/packet_engine/KL_pp_nvm_port.sv}
set_property file_type SystemVerilog [get_files {$PACKET/scratch/repo/protocol-processor/hdl/packet_engine/KL_pp_nvm_port.sv}]
read_verilog -v {$PACKET/scratch/repo/protocol-processor/hdl/packet_engine/KL_pp_originator.sv}
set_property file_type SystemVerilog [get_files {$PACKET/scratch/repo/protocol-processor/hdl/packet_engine/KL_pp_originator.sv}]
read_verilog -v {$PACKET/scratch/repo/protocol-processor/hdl/packet_engine/KL_pp_release_merge.sv}
set_property file_type SystemVerilog [get_files {$PACKET/scratch/repo/protocol-processor/hdl/packet_engine/KL_pp_release_merge.sv}]
read_verilog -v {$PACKET/scratch/repo/protocol-processor/hdl/packet_engine/KL_pp_rx_slots.sv}
set_property file_type SystemVerilog [get_files {$PACKET/scratch/repo/protocol-processor/hdl/packet_engine/KL_pp_rx_slots.sv}]
read_verilog -v {$PACKET/scratch/repo/protocol-processor/hdl/packet_engine/KL_pp_rx_validator.sv}
set_property file_type SystemVerilog [get_files {$PACKET/scratch/repo/protocol-processor/hdl/packet_engine/KL_pp_rx_validator.sv}]
read_verilog -v {$PACKET/scratch/repo/protocol-processor/hdl/packet_engine/KL_pp_scoreboard.sv}
set_property file_type SystemVerilog [get_files {$PACKET/scratch/repo/protocol-processor/hdl/packet_engine/KL_pp_scoreboard.sv}]
read_verilog -v {$PACKET/scratch/repo/protocol-processor/hdl/packet_engine/KL_pp_side_port.sv}
set_property file_type SystemVerilog [get_files {$PACKET/scratch/repo/protocol-processor/hdl/packet_engine/KL_pp_side_port.sv}]
read_verilog -v {$PACKET/scratch/repo/protocol-processor/hdl/packet_engine/KL_pp_trace_ring.sv}
set_property file_type SystemVerilog [get_files {$PACKET/scratch/repo/protocol-processor/hdl/packet_engine/KL_pp_trace_ring.sv}]
read_verilog -v {$PACKET/scratch/repo/protocol-processor/hdl/packet_engine/KL_pp_tx_arbiter.sv}
set_property file_type SystemVerilog [get_files {$PACKET/scratch/repo/protocol-processor/hdl/packet_engine/KL_pp_tx_arbiter.sv}]
read_verilog -v {$PACKET/scratch/repo/protocol-processor/hdl/packet_engine/KL_pp_tx_slots.sv}
set_property file_type SystemVerilog [get_files {$PACKET/scratch/repo/protocol-processor/hdl/packet_engine/KL_pp_tx_slots.sv}]
read_verilog -v {$PACKET/scratch/repo/protocol-processor/hdl/srp/KL_srp_admission.sv}
set_property file_type SystemVerilog [get_files {$PACKET/scratch/repo/protocol-processor/hdl/srp/KL_srp_admission.sv}]
read_verilog -v {$PACKET/scratch/repo/protocol-processor/hdl/srp/KL_srp_decoder.sv}
set_property file_type SystemVerilog [get_files {$PACKET/scratch/repo/protocol-processor/hdl/srp/KL_srp_decoder.sv}]
read_verilog -v {$PACKET/scratch/repo/protocol-processor/hdl/srp/KL_srp_domain.sv}
set_property file_type SystemVerilog [get_files {$PACKET/scratch/repo/protocol-processor/hdl/srp/KL_srp_domain.sv}]
read_verilog -v {$PACKET/scratch/repo/protocol-processor/hdl/srp/KL_srp_encoder.sv}
set_property file_type SystemVerilog [get_files {$PACKET/scratch/repo/protocol-processor/hdl/srp/KL_srp_encoder.sv}]
read_verilog -v {$PACKET/scratch/repo/protocol-processor/hdl/srp/KL_srp_listener_fsm.sv}
set_property file_type SystemVerilog [get_files {$PACKET/scratch/repo/protocol-processor/hdl/srp/KL_srp_listener_fsm.sv}]
read_verilog -v {$PACKET/scratch/repo/protocol-processor/hdl/srp/KL_srp_talker_fsm.sv}
set_property file_type SystemVerilog [get_files {$PACKET/scratch/repo/protocol-processor/hdl/srp/KL_srp_talker_fsm.sv}]
read_verilog -v {$PACKET/scratch/repo/protocol-processor/hdl/srp/KL_srp_top.sv}
set_property file_type SystemVerilog [get_files {$PACKET/scratch/repo/protocol-processor/hdl/srp/KL_srp_top.sv}]
read_verilog -v {$PACKET/scratch/repo/protocol-processor/hdl/srp/KL_srp_vlan.sv}
set_property file_type SystemVerilog [get_files {$PACKET/scratch/repo/protocol-processor/hdl/srp/KL_srp_vlan.sv}]
read_verilog -v {$PACKET/scratch/repo/protocol-processor/hdl/top/KL_mrp_strip.sv}
set_property file_type SystemVerilog [get_files {$PACKET/scratch/repo/protocol-processor/hdl/top/KL_mrp_strip.sv}]
read_verilog -v {$PACKET/scratch/repo/protocol-processor/hdl/top/protocol_processor_top.sv}
set_property file_type SystemVerilog [get_files {$PACKET/scratch/repo/protocol-processor/hdl/top/protocol_processor_top.sv}]
read_verilog -v {$PACKET/scratch/repo/hdl/milan/KL_pp_shadow.sv}
set_property file_type SystemVerilog [get_files {$PACKET/scratch/repo/hdl/milan/KL_pp_shadow.sv}]
read_verilog -v {$PACKET/scratch/repo/hdl/milan/KL_pp_maap_shim.sv}
set_property file_type SystemVerilog [get_files {$PACKET/scratch/repo/hdl/milan/KL_pp_maap_shim.sv}]
read_verilog -v {$PACKET/scratch/repo/hdl/milan/KL_nvm_backend.sv}
set_property file_type SystemVerilog [get_files {$PACKET/scratch/repo/hdl/milan/KL_nvm_backend.sv}]
read_verilog -v {$PACKET/scratch/repo/gptp-processor/hdl/ucpu/gptp_ucpu_pkg.sv}
set_property file_type SystemVerilog [get_files {$PACKET/scratch/repo/gptp-processor/hdl/ucpu/gptp_ucpu_pkg.sv}]
read_verilog -v {$PACKET/scratch/repo/gptp-processor/hdl/ucpu/KL_gptp_ucpu.sv}
set_property file_type SystemVerilog [get_files {$PACKET/scratch/repo/gptp-processor/hdl/ucpu/KL_gptp_ucpu.sv}]
read_verilog -v {$PACKET/scratch/repo/gptp-processor/hdl/wire/KL_gptp_rx_parser.sv}
set_property file_type SystemVerilog [get_files {$PACKET/scratch/repo/gptp-processor/hdl/wire/KL_gptp_rx_parser.sv}]
read_verilog -v {$PACKET/scratch/repo/gptp-processor/hdl/wire/KL_gptp_tx_slot.sv}
set_property file_type SystemVerilog [get_files {$PACKET/scratch/repo/gptp-processor/hdl/wire/KL_gptp_tx_slot.sv}]
read_verilog -v {$PACKET/scratch/repo/gptp-processor/hdl/common/KL_gptp_timer.sv}
set_property file_type SystemVerilog [get_files {$PACKET/scratch/repo/gptp-processor/hdl/common/KL_gptp_timer.sv}]
read_verilog -v {$PACKET/scratch/repo/gptp-processor/hdl/top/KL_gptp_engine.sv}
set_property file_type SystemVerilog [get_files {$PACKET/scratch/repo/gptp-processor/hdl/top/KL_gptp_engine.sv}]
read_verilog -v {$PACKET/scratch/repo/hdl/ieee8021as/gptp_plane/KL_gptp_txticket.sv}
set_property file_type SystemVerilog [get_files {$PACKET/scratch/repo/hdl/ieee8021as/gptp_plane/KL_gptp_txticket.sv}]
read_verilog -v {$PACKET/scratch/repo/hdl/ieee8021as/gptp_plane/KL_gptp_txret.sv}
set_property file_type SystemVerilog [get_files {$PACKET/scratch/repo/hdl/ieee8021as/gptp_plane/KL_gptp_txret.sv}]
read_verilog -v {$PACKET/scratch/repo/hdl/ieee8021as/gptp_plane/KL_gptp_gmii_launch.sv}
set_property file_type SystemVerilog [get_files {$PACKET/scratch/repo/hdl/ieee8021as/gptp_plane/KL_gptp_gmii_launch.sv}]
read_verilog -v {$PACKET/scratch/repo/hdl/ieee8021as/gptp_plane/KL_gptp_shadow.sv}
set_property file_type SystemVerilog [get_files {$PACKET/scratch/repo/hdl/ieee8021as/gptp_plane/KL_gptp_shadow.sv}]
read_verilog -v {$PACKET/scratch/repo/hdl/common/ethernet_packet_pkg.sv}
set_property file_type SystemVerilog [get_files {$PACKET/scratch/repo/hdl/common/ethernet_packet_pkg.sv}]
read_verilog -v {$PACKET/scratch/repo/hdl/common/axi_stream_if.sv}
set_property file_type SystemVerilog [get_files {$PACKET/scratch/repo/hdl/common/axi_stream_if.sv}]
read_verilog {$PACKET/scratch/repo/third_party/verilog-axis/rtl/axis_fifo.v}
read_verilog {$PACKET/scratch/repo/third_party/verilog-axis/rtl/axis_arb_mux.v}
read_verilog {$PACKET/scratch/repo/third_party/verilog-axis/rtl/arbiter.v}
read_verilog {$PACKET/scratch/repo/third_party/verilog-axis/rtl/priority_encoder.v}
read_verilog -v {$PACKET/scratch/repo/hdl/ieee8021as/ptp_timestamp/timestamp_counter.sv}
set_property file_type SystemVerilog [get_files {$PACKET/scratch/repo/hdl/ieee8021as/ptp_timestamp/timestamp_counter.sv}]
read_verilog -v {$PACKET/scratch/repo/hdl/ieee8021as/ptp_timestamp/ptp_csr_sync.sv}
set_property file_type SystemVerilog [get_files {$PACKET/scratch/repo/hdl/ieee8021as/ptp_timestamp/ptp_csr_sync.sv}]
read_verilog -v {$PACKET/scratch/repo/hdl/common/cdc_pulse.sv}
set_property file_type SystemVerilog [get_files {$PACKET/scratch/repo/hdl/common/cdc_pulse.sv}]
read_verilog -v {$PACKET/scratch/repo/hdl/common/cdc_handshake.sv}
set_property file_type SystemVerilog [get_files {$PACKET/scratch/repo/hdl/common/cdc_handshake.sv}]
read_verilog -v {$PACKET/scratch/repo/hdl/ieee8021as/ptp_timestamp/KL_ptp_clock_validity.sv}
set_property file_type SystemVerilog [get_files {$PACKET/scratch/repo/hdl/ieee8021as/ptp_timestamp/KL_ptp_clock_validity.sv}]
read_verilog -v {$PACKET/scratch/repo/hdl/ieee8021q/filtering/tcam.sv}
set_property file_type SystemVerilog [get_files {$PACKET/scratch/repo/hdl/ieee8021q/filtering/tcam.sv}]
read_verilog -v {$PACKET/scratch/repo/hdl/ieee8021q/filtering/rx_mac_filter.sv}
set_property file_type SystemVerilog [get_files {$PACKET/scratch/repo/hdl/ieee8021q/filtering/rx_mac_filter.sv}]
read_verilog -v {$PACKET/scratch/repo/hdl/common/tx_ifg_gasket.sv}
set_property file_type SystemVerilog [get_files {$PACKET/scratch/repo/hdl/common/tx_ifg_gasket.sv}]
read_verilog -v {$PACKET/scratch/repo/hdl/ieee1722/aaf/KL_pcm_lpf.sv}
set_property file_type SystemVerilog [get_files {$PACKET/scratch/repo/hdl/ieee1722/aaf/KL_pcm_lpf.sv}]
read_verilog -v {$PACKET/scratch/repo/hdl/common/KL_link_guard.sv}
set_property file_type SystemVerilog [get_files {$PACKET/scratch/repo/hdl/common/KL_link_guard.sv}]
read_verilog -v {$PACKET/scratch/repo/hdl/ieee17221/adp/adp_tx_arbiter.sv}
set_property file_type SystemVerilog [get_files {$PACKET/scratch/repo/hdl/ieee17221/adp/adp_tx_arbiter.sv}]
read_verilog -v {$PACKET/scratch/repo/hdl/ieee1722/aaf/aaf_talker_i2s.sv}
set_property file_type SystemVerilog [get_files {$PACKET/scratch/repo/hdl/ieee1722/aaf/aaf_talker_i2s.sv}]
read_verilog -v {$PACKET/scratch/repo/hdl/ieee1722/aaf/KL_aaf_rx_depacketizer.sv}
set_property file_type SystemVerilog [get_files {$PACKET/scratch/repo/hdl/ieee1722/aaf/KL_aaf_rx_depacketizer.sv}]
read_verilog -v {$PACKET/scratch/repo/hdl/ieee1722/aaf/KL_i2s_playback.sv}
set_property file_type SystemVerilog [get_files {$PACKET/scratch/repo/hdl/ieee1722/aaf/KL_i2s_playback.sv}]
read_verilog -v {$PACKET/scratch/repo/hdl/ieee1722/aaf/KL_tone_gen.sv}
set_property file_type SystemVerilog [get_files {$PACKET/scratch/repo/hdl/ieee1722/aaf/KL_tone_gen.sv}]
read_verilog -v {$PACKET/scratch/repo/hdl/ieee1722/aaf/KL_i2s_feed_mux.sv}
set_property file_type SystemVerilog [get_files {$PACKET/scratch/repo/hdl/ieee1722/aaf/KL_i2s_feed_mux.sv}]
read_verilog -v {$PACKET/scratch/repo/hdl/ieee1722/aaf/KL_aaf_latency_taps.sv}
set_property file_type SystemVerilog [get_files {$PACKET/scratch/repo/hdl/ieee1722/aaf/KL_aaf_latency_taps.sv}]
read_verilog -v {$PACKET/scratch/repo/hdl/ieee1722/aaf/KL_aaf_latency_tap_bank.sv}
set_property file_type SystemVerilog [get_files {$PACKET/scratch/repo/hdl/ieee1722/aaf/KL_aaf_latency_tap_bank.sv}]
read_verilog -v {$PACKET/scratch/repo/hdl/ieee1722/aaf/KL_media_adv.sv}
set_property file_type SystemVerilog [get_files {$PACKET/scratch/repo/hdl/ieee1722/aaf/KL_media_adv.sv}]
read_verilog -v {$PACKET/scratch/repo/hdl/common/cdc_pair_fifo.sv}
set_property file_type SystemVerilog [get_files {$PACKET/scratch/repo/hdl/common/cdc_pair_fifo.sv}]
read_verilog -v {$PACKET/scratch/repo/hdl/ieee1722/avtp/avtp_subtype_pkg.sv}
set_property file_type SystemVerilog [get_files {$PACKET/scratch/repo/hdl/ieee1722/avtp/avtp_subtype_pkg.sv}]
read_verilog -v {$PACKET/scratch/repo/hdl/ieee1722/avtp/avtp_stream_parser.sv}
set_property file_type SystemVerilog [get_files {$PACKET/scratch/repo/hdl/ieee1722/avtp/avtp_stream_parser.sv}]
read_verilog -v {$PACKET/scratch/repo/hdl/ieee1722/avtp/KL_stream_table.sv}
set_property file_type SystemVerilog [get_files {$PACKET/scratch/repo/hdl/ieee1722/avtp/KL_stream_table.sv}]
read_verilog -v {$PACKET/scratch/repo/hdl/ieee1722/avtp/KL_avtp_rx_monitor.sv}
set_property file_type SystemVerilog [get_files {$PACKET/scratch/repo/hdl/ieee1722/avtp/KL_avtp_rx_monitor.sv}]
read_verilog -v {$PACKET/scratch/repo/hdl/ieee1722/avtp/KL_avtp_rx_monitor_ctx.sv}
set_property file_type SystemVerilog [get_files {$PACKET/scratch/repo/hdl/ieee1722/avtp/KL_avtp_rx_monitor_ctx.sv}]
read_verilog -v {$PACKET/scratch/repo/hdl/ieee1722/avtp/KL_talker_diag_ctx.sv}
set_property file_type SystemVerilog [get_files {$PACKET/scratch/repo/hdl/ieee1722/avtp/KL_talker_diag_ctx.sv}]
read_verilog -v {$PACKET/scratch/repo/hdl/ieee1722/avtp/KL_media_clock_restart.sv}
set_property file_type SystemVerilog [get_files {$PACKET/scratch/repo/hdl/ieee1722/avtp/KL_media_clock_restart.sv}]
read_verilog -v {$PACKET/scratch/repo/hdl/ieee1722/aaf/KL_pcm_route.sv}
set_property file_type SystemVerilog [get_files {$PACKET/scratch/repo/hdl/ieee1722/aaf/KL_pcm_route.sv}]
read_verilog -v {$PACKET/scratch/repo/hdl/ieee1722/aaf/KL_aaf_capture_i2s.sv}
set_property file_type SystemVerilog [get_files {$PACKET/scratch/repo/hdl/ieee1722/aaf/KL_aaf_capture_i2s.sv}]
read_verilog -v {$PACKET/scratch/repo/hdl/ieee1722/aaf/KL_tdm_capture.sv}
set_property file_type SystemVerilog [get_files {$PACKET/scratch/repo/hdl/ieee1722/aaf/KL_tdm_capture.sv}]
read_verilog -v {$PACKET/scratch/repo/hdl/ieee1722/aaf/KL_tdm_capture_master.sv}
set_property file_type SystemVerilog [get_files {$PACKET/scratch/repo/hdl/ieee1722/aaf/KL_tdm_capture_master.sv}]
read_verilog -v {$PACKET/scratch/repo/hdl/ieee1722/aaf/KL_pair_blend.sv}
set_property file_type SystemVerilog [get_files {$PACKET/scratch/repo/hdl/ieee1722/aaf/KL_pair_blend.sv}]
read_verilog -v {$PACKET/scratch/repo/hdl/ieee1722/aaf/KL_pair_zero_fill.sv}
set_property file_type SystemVerilog [get_files {$PACKET/scratch/repo/hdl/ieee1722/aaf/KL_pair_zero_fill.sv}]
read_verilog -v {$PACKET/scratch/repo/hdl/ieee1722/aaf/KL_tdm_render.sv}
set_property file_type SystemVerilog [get_files {$PACKET/scratch/repo/hdl/ieee1722/aaf/KL_tdm_render.sv}]
read_verilog -v {$PACKET/scratch/repo/hdl/ieee1722/aaf/KL_tdm_render_master.sv}
set_property file_type SystemVerilog [get_files {$PACKET/scratch/repo/hdl/ieee1722/aaf/KL_tdm_render_master.sv}]
read_verilog -v {$PACKET/scratch/repo/hdl/ieee1722/aaf/KL_render_setpoint.sv}
set_property file_type SystemVerilog [get_files {$PACKET/scratch/repo/hdl/ieee1722/aaf/KL_render_setpoint.sv}]
read_verilog -v {$PACKET/scratch/repo/hdl/ieee1722/aaf/KL_chan_map_render.sv}
set_property file_type SystemVerilog [get_files {$PACKET/scratch/repo/hdl/ieee1722/aaf/KL_chan_map_render.sv}]
read_verilog -v {$PACKET/scratch/repo/hdl/ieee1722/aaf/KL_chan_map_capture.sv}
set_property file_type SystemVerilog [get_files {$PACKET/scratch/repo/hdl/ieee1722/aaf/KL_chan_map_capture.sv}]
read_verilog -v {$PACKET/scratch/repo/hdl/ieee1722/aaf/KL_aaf_packetizer.sv}
set_property file_type SystemVerilog [get_files {$PACKET/scratch/repo/hdl/ieee1722/aaf/KL_aaf_packetizer.sv}]
read_verilog -v {$PACKET/scratch/repo/hdl/ieee1722/crf/KL_crf_rx.sv}
set_property file_type SystemVerilog [get_files {$PACKET/scratch/repo/hdl/ieee1722/crf/KL_crf_rx.sv}]
read_verilog -v {$PACKET/scratch/repo/hdl/ieee1722/crf/KL_crf_tx.sv}
set_property file_type SystemVerilog [get_files {$PACKET/scratch/repo/hdl/ieee1722/crf/KL_crf_tx.sv}]
read_verilog -v {$PACKET/scratch/repo/hdl/ieee1722/maap/KL_maap.sv}
set_property file_type SystemVerilog [get_files {$PACKET/scratch/repo/hdl/ieee1722/maap/KL_maap.sv}]
read_verilog -v {$PACKET/scratch/repo/hdl/ieee1722/crf/KL_mmcm_drp_servo.sv}
set_property file_type SystemVerilog [get_files {$PACKET/scratch/repo/hdl/ieee1722/crf/KL_mmcm_drp_servo.sv}]
read_verilog -v {$PACKET/scratch/repo/hdl/ieee1722/crf/KL_media_nco.sv}
set_property file_type SystemVerilog [get_files {$PACKET/scratch/repo/hdl/ieee1722/crf/KL_media_nco.sv}]
read_verilog -v {$PACKET/scratch/repo/hdl/ieee1722/crf/KL_media_grid_align.sv}
set_property file_type SystemVerilog [get_files {$PACKET/scratch/repo/hdl/ieee1722/crf/KL_media_grid_align.sv}]
read_verilog -v {$PACKET/scratch/repo/hdl/common/eth_event_counter/ethernet_events.sv}
set_property file_type SystemVerilog [get_files {$PACKET/scratch/repo/hdl/common/eth_event_counter/ethernet_events.sv}]
read_verilog -v {$PACKET/scratch/repo/hdl/common/eth_event_counter/event_counter.sv}
set_property file_type SystemVerilog [get_files {$PACKET/scratch/repo/hdl/common/eth_event_counter/event_counter.sv}]
read_verilog -v {$PACKET/scratch/repo/hdl/common/eth_event_counter/KL_mac_rmon_events.sv}
set_property file_type SystemVerilog [get_files {$PACKET/scratch/repo/hdl/common/eth_event_counter/KL_mac_rmon_events.sv}]
read_verilog -v {$PACKET/scratch/repo/hdl/common/csr/milan_csr.sv}
set_property file_type SystemVerilog [get_files {$PACKET/scratch/repo/hdl/common/csr/milan_csr.sv}]
read_verilog -v {$PACKET/scratch/repo/hdl/milan/milan_datapath.sv}
set_property file_type SystemVerilog [get_files {$PACKET/scratch/repo/hdl/milan/milan_datapath.sv}]
read_verilog {$HOME/litex-milan/pythondata-cpu-vexiiriscv/pythondata_cpu_vexiiriscv/verilog/Ram_1w_1rs_Generic.v}
read_verilog {$HOME/litex-milan/pythondata-cpu-vexiiriscv/pythondata_cpu_vexiiriscv/verilog/Ram_1w_1ra_Generic.v}
read_verilog {$HOME/litex-milan/pythondata-cpu-vexiiriscv/pythondata_cpu_vexiiriscv/verilog/VexiiRiscvLitex_f5f08b170311db53220574624f819159.v}
read_verilog {$PACKET/scratch/work/ax7101/gateware/alinx_ax7101.v}

# Add EDIFs


# Add IPs


set_msg_config -id {Synth 8-4445} -new_severity ERROR
read_xdc baseline_boundary.xdc
# Add constraints

read_xdc alinx_ax7101.xdc
set_property PROCESSING_ORDER EARLY [get_files alinx_ax7101.xdc]

# Add pre-synthesis commands


# Synthesis

synth_design -directive AreaOptimized_high -top alinx_ax7101 -part xc7a100t-fgg484-2 -include_dirs {$PACKET/scratch/repo/configs/generated/endstation_ax7101_1x1_tdm8 $PACKET/scratch/repo/configs/generated/endstation_ax7101_1x1_tdm8/gen $PACKET/scratch/repo/hdl/common $PACKET/scratch/repo/hdl/ieee8021q/ts $PACKET/scratch/repo/hdl/ieee8021as/ptp_timestamp $PACKET/scratch/repo/hdl/ieee17221/adp $PACKET/scratch/repo/hdl/common/csr $PACKET/scratch/repo/hdl/common/eth_event_counter $PACKET/scratch/repo/hdl/ieee1722/avtp}

# Synthesis report

report_timing_summary -file alinx_ax7101_timing_synth.rpt
report_utilization -hierarchical -file alinx_ax7101_utilization_hierarchical_synth.rpt
report_utilization -file alinx_ax7101_utilization_synth.rpt
write_checkpoint -force alinx_ax7101_synth.dcp


report_utilization -hierarchical -hierarchical_depth 10 -hierarchical_min_primitive_count 0 -file baseline_hierarchy.rpt
report_utilization -file baseline_utilization.rpt
report_timing_summary -max_paths 10 -file baseline_timing.rpt
set pf [open baseline_cells.tsv w]
puts $pf "cell\tprimitive"
foreach c [get_cells -hier -filter {IS_PRIMITIVE == 1}] {
  puts $pf "$c\t[get_property REF_NAME $c]"
}
close $pf

set pp [get_cells -hier -filter {ORIG_REF_NAME == KL_pp_shadow || REF_NAME == KL_pp_shadow}]
if {[llength $pp] != 1} { error "Expected exactly one protocol wrapper" }
report_utilization -cells $pp -file baseline_pp_utilization.rpt
report_timing -through [get_pins -of_objects $pp] -max_paths 10 -file baseline_pp_boundary_timing.rpt

set scope_root ""
set pp [get_cells -quiet -hier -filter {ORIG_REF_NAME == KL_pp_shadow || REF_NAME == KL_pp_shadow}]
if {[llength $pp] == 1} {
  set scope_root "$pp/"
} elseif {[llength $pp] == 0} {
  set core [get_cells -quiet u_pp]
  if {[llength $core] != 1 || [get_property ORIG_REF_NAME $core] ne "protocol_processor_top"} {
    error "Expected the standalone wrapper's processor instance"
  }
} else {
  error "Expected exactly one protocol wrapper"
}
set tf [open baseline_scope_timing.tsv w]
puts $tf "instance\tsequential_cells\tinternal_WNS_ns"
foreach relative {wrapper u_pp u_pp/u_aecp u_pp/u_srp u_pp/u_notify u_pp/u_listener u_pp/u_talker u_nvm} {
  set path "$scope_root$relative"
  if {$relative eq "wrapper"} {
    set path [string trimright $scope_root /]
  }
  if {$path eq ""} {
    set path KL_pp_shadow
    set regs [get_cells -hier -filter {IS_SEQUENTIAL == 1}]
  } else {
    set regs [get_cells -hier -filter [format {NAME =~ "%s/*" && IS_SEQUENTIAL == 1} $path]]
  }
  set worst [get_timing_paths -from $regs -to $regs -max_paths 1]
  if {[llength $worst] != 1} { error "No internal timing path for $path" }
  puts $tf "$path\t[llength $regs]\t[get_property SLACK $worst]"
  flush $tf
}
close $tf

quit
