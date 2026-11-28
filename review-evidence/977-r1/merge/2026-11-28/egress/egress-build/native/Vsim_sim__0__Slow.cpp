// Verilated -*- C++ -*-
// DESCRIPTION: Verilator output: Design implementation internals
// See Vsim.h for the primary calling header

#include "Vsim__pch.h"

VL_ATTR_COLD void Vsim_sim___eval_static__TOP__sim__0(Vsim_sim* vlSelf);

VL_ATTR_COLD void Vsim_sim___eval_static__TOP__sim(Vsim_sim* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+      Vsim_sim___eval_static__TOP__sim\n"); );
    Vsim__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Body
    Vsim_sim___eval_static__TOP__sim__0(vlSelf);
    {
        // Inlined CFunc: _eval_static__TOP__sim__1
        vlSelfRef.__PVT__en_storage = 0U;
    }
    vlSelfRef.__PVT__enable_storage = 0U;
    vlSelfRef.__PVT__flashboundary_clk_divisor_storage = 8U;
    vlSelfRef.__PVT__flashboundary_cs = 0U;
    vlSelfRef.__PVT__flashboundary_mode_storage = 0U;
    vlSelfRef.__PVT__load_storage = 0U;
    vlSelfRef.__PVT__pending_wr_data = 0U;
    vlSelfRef.__PVT__pending_wr_stb = 0U;
    vlSelfRef.__PVT__reload_storage = 0U;
    vlSelfRef.__PVT__soc_adapted_interface_adr = 0U;
    vlSelfRef.__PVT__soc_adapted_interface_cyc = 0U;
    vlSelfRef.__PVT__soc_adapted_interface_dat_w = 0U;
    vlSelfRef.__PVT__soc_adapted_interface_sel = 0U;
    vlSelfRef.__PVT__soc_adapted_interface_stb = 0U;
    vlSelfRef.__PVT__soc_adapted_interface_we = 0U;
    vlSelfRef.__PVT__soc_bus_errors = 0U;
    vlSelfRef.__PVT__soc_data = 0U;
    vlSelfRef.__PVT__soc_data_socbushandler_next_value1 = 0U;
    vlSelfRef.__PVT__soc_data_socbushandler_next_value_ce1 = 0U;
    vlSelfRef.__PVT__soc_enable_storage = 0U;
    vlSelfRef.__PVT__soc_last_ar_aw_n = 0U;
    vlSelfRef.__PVT__soc_last_ar_aw_n_socbushandler_next_value0 = 0U;
    vlSelfRef.__PVT__soc_last_ar_aw_n_socbushandler_next_value_ce0 = 0U;
    vlSelfRef.__PVT__soc_pending_status = 0U;
    vlSelfRef.__PVT__soc_pending_wr_data = 0U;
    vlSelfRef.__PVT__soc_pending_wr_stb = 0U;
    vlSelfRef.__PVT__soc_reset_storage = 0U;
    vlSelfRef.__PVT__soc_reset_wr_stb = 0U;
    vlSelfRef.__PVT__soc_rx_clear = 0U;
    vlSelfRef.__PVT__soc_rx_fifo_consume = 0U;
    vlSelfRef.__PVT__soc_rx_fifo_level0 = 0U;
    vlSelfRef.__PVT__soc_rx_fifo_produce = 0U;
    vlSelfRef.__PVT__soc_rx_fifo_readable = 0U;
    vlSelfRef.__PVT__soc_rx_fifo_wrport_adr = 0U;
    vlSelfRef.__PVT__soc_rxtx_re = 0U;
    vlSelfRef.__PVT__soc_scratch_storage = 0x12345678U;
    vlSelfRef.__PVT__soc_soc_rst = 0U;
    vlSelfRef.__PVT__soc_status_status = 0U;
    vlSelfRef.__PVT__soc_tx_fifo_consume = 0U;
    vlSelfRef.__PVT__soc_tx_fifo_level0 = 0U;
    vlSelfRef.__PVT__soc_tx_fifo_produce = 0U;
    vlSelfRef.__PVT__soc_tx_fifo_readable = 0U;
    vlSelfRef.__PVT__soc_tx_fifo_wrport_adr = 0U;
    vlSelfRef.__PVT__soc_vexiiriscv_interrupt = 0U;
    vlSelfRef.__PVT__soc_vexiiriscv_pbus_ar_ready = 0U;
    vlSelfRef.__PVT__soc_vexiiriscv_pbus_aw_ready = 0U;
    vlSelfRef.__PVT__soc_vexiiriscv_pbus_b_payload_resp = 0U;
    vlSelfRef.__PVT__soc_vexiiriscv_pbus_b_valid = 0U;
    vlSelfRef.__PVT__soc_vexiiriscv_pbus_r_payload_data = 0U;
    vlSelfRef.__PVT__soc_vexiiriscv_pbus_r_payload_resp = 0U;
    vlSelfRef.__PVT__soc_vexiiriscv_pbus_r_valid = 0U;
    vlSelfRef.__PVT__soc_vexiiriscv_pbus_w_ready = 0U;
    vlSelfRef.__PVT__storage = 0U;
    vlSelfRef.__PVT__update_value_storage = 0U;
    vlSelfRef.__PVT__update_value_wr_stb = 0U;
    vlSelfRef.__PVT__value = 0U;
    vlSelfRef.__PVT__value_status = 0U;
    vlSelfRef.__PVT__zero_clear = 0U;
    vlSelfRef.__PVT__zero_pending = 0U;
    vlSelfRef.__PVT__zero_trigger_d = 0U;
    const uint64_t __VscopeHash = VL_MURMUR64_HASH(vlSelf->vlNamep);
    vlSelfRef.__PVT__KL_mbx__DOT__bound_decode__DOT__rel = VL_SCOPED_RAND_RESET_I(15, __VscopeHash, 9779507245596684639ull);
    vlSelfRef.__PVT__KL_mbx__DOT__bound_decode__DOT__in_entry = VL_SCOPED_RAND_RESET_I(15, __VscopeHash, 5830245705883143219ull);
    vlSelfRef.__PVT__KL_mbx__DOT__bound_decode__DOT__entry = VL_SCOPED_RAND_RESET_I(15, __VscopeHash, 10797740573648280643ull);
    vlSelfRef.__PVT__KL_mbx__DOT__pub_decode__DOT__rel = VL_SCOPED_RAND_RESET_I(15, __VscopeHash, 12003309689186330138ull);
    vlSelfRef.__PVT__KL_mbx__DOT__pub_decode__DOT__in_if = VL_SCOPED_RAND_RESET_I(15, __VscopeHash, 11029882707264093778ull);
    vlSelfRef.__PVT__KL_mbx__DOT__pub_decode__DOT__in_srcs = VL_SCOPED_RAND_RESET_I(15, __VscopeHash, 12941024145939380109ull);
    vlSelfRef.__PVT__KL_mbx__DOT__pub_decode__DOT__in_sinks = VL_SCOPED_RAND_RESET_I(15, __VscopeHash, 6731189035122970561ull);
    vlSelfRef.__PVT__KL_mbx__DOT__pub_decode__DOT__src_entry = VL_SCOPED_RAND_RESET_I(15, __VscopeHash, 3705923088255420907ull);
    vlSelfRef.__PVT__KL_mbx__DOT__pub_decode__DOT__entry = VL_SCOPED_RAND_RESET_I(15, __VscopeHash, 420992429133451889ull);
    vlSelfRef.__PVT__KL_mbx__DOT__face_decode__DOT__rel = VL_SCOPED_RAND_RESET_I(15, __VscopeHash, 11884552812589247293ull);
    vlSelfRef.__PVT__KL_mbx__DOT__face_decode__DOT__in_if = VL_SCOPED_RAND_RESET_I(15, __VscopeHash, 17769256767622576682ull);
    vlSelfRef.__PVT__KL_mbx__DOT__face_decode__DOT__entry = VL_SCOPED_RAND_RESET_I(15, __VscopeHash, 3174193372368264168ull);
    vlSelfRef.__PVT__KL_mbx__DOT__rd_bound_decode__DOT__rel = VL_SCOPED_RAND_RESET_I(15, __VscopeHash, 16129726988558544071ull);
    vlSelfRef.__PVT__KL_mbx__DOT__rd_bound_decode__DOT__in_entry = VL_SCOPED_RAND_RESET_I(15, __VscopeHash, 1640194640169513276ull);
    vlSelfRef.__PVT__KL_mbx__DOT__rd_bound_decode__DOT__entry = VL_SCOPED_RAND_RESET_I(15, __VscopeHash, 12653013347498452607ull);
    vlSelfRef.__PVT__KL_mbx__DOT__rd_pub_decode__DOT__rel = VL_SCOPED_RAND_RESET_I(15, __VscopeHash, 2915326696662940611ull);
    vlSelfRef.__PVT__KL_mbx__DOT__rd_pub_decode__DOT__in_if = VL_SCOPED_RAND_RESET_I(15, __VscopeHash, 11665841022475341103ull);
    vlSelfRef.__PVT__KL_mbx__DOT__rd_pub_decode__DOT__in_srcs = VL_SCOPED_RAND_RESET_I(15, __VscopeHash, 11828151302302321535ull);
    vlSelfRef.__PVT__KL_mbx__DOT__rd_pub_decode__DOT__in_sinks = VL_SCOPED_RAND_RESET_I(15, __VscopeHash, 10057561734615678413ull);
    vlSelfRef.__PVT__KL_mbx__DOT__rd_pub_decode__DOT__src_entry = VL_SCOPED_RAND_RESET_I(15, __VscopeHash, 13777305547532255716ull);
    vlSelfRef.__PVT__KL_mbx__DOT__rd_pub_decode__DOT__entry = VL_SCOPED_RAND_RESET_I(15, __VscopeHash, 14563479524329869757ull);
    vlSelfRef.__PVT__KL_mbx__DOT__rd_face_decode__DOT__rel = VL_SCOPED_RAND_RESET_I(15, __VscopeHash, 7551284265455218903ull);
    vlSelfRef.__PVT__KL_mbx__DOT__rd_face_decode__DOT__in_if = VL_SCOPED_RAND_RESET_I(15, __VscopeHash, 12937379452287314517ull);
    vlSelfRef.__PVT__KL_mbx__DOT__rd_face_decode__DOT__entry = VL_SCOPED_RAND_RESET_I(15, __VscopeHash, 14231573912042566512ull);
    vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__record__DOT__etype = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 14186063595612124074ull);
    vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__record__DOT__dtype = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 12828626821491374166ull);
    vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__record__DOT__dindex = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 15126456156289249281ull);
    vlSelfRef.__PVT__KL_mbx__DOT__u_tx__DOT__arbiter__DOT__sum = 0U;
    vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__classify__DOT__ethertype = VL_SCOPED_RAND_RESET_I(16, __VscopeHash, 7569752261615686868ull);
    vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__classify__DOT__subtype = VL_SCOPED_RAND_RESET_I(8, __VscopeHash, 11191324917327500978ull);
    vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__classify__DOT__msg = VL_SCOPED_RAND_RESET_I(4, __VscopeHash, 977889498099267306ull);
    vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__classify__DOT__unnamedblk9__DOT__unnamedblk10__DOT__dst_ok = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 11750040470615124499ull);
    vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__verdict__DOT__unnamedblk11__DOT__unnamedblk12__DOT__j = VL_SCOPED_RAND_RESET_I(4, __VscopeHash, 16040826773648550988ull);
    vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__verdict__DOT__unnamedblk11__DOT__unnamedblk12__DOT__field_ok = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 3870344137798646536ull);
    vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__verdict__DOT__unnamedblk11__DOT__unnamedblk12__DOT__overlap = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 4714941261533501634ull);
    vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__verdict__DOT__unnamedblk11__DOT__unnamedblk12__DOT__own_end = VL_SCOPED_RAND_RESET_Q(49, __VscopeHash, 9942660010000161158ull);
    vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__verdict__DOT__unnamedblk11__DOT__unnamedblk12__DOT__req_end = VL_SCOPED_RAND_RESET_Q(49, __VscopeHash, 2929320996611472553ull);
    vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__buckets__DOT__unnamedblk18__DOT__unnamedblk19__DOT__tokens = VL_SCOPED_RAND_RESET_I(9, __VscopeHash, 8710991650452521175ull);
}

VL_ATTR_COLD void Vsim_sim___eval_static__TOP__sim__0(Vsim_sim* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+      Vsim_sim___eval_static__TOP__sim__0\n"); );
    Vsim__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Locals
    CData/*0:0*/ __PVT__add_devices_rx_pipe_ready_source_first;
    __PVT__add_devices_rx_pipe_ready_source_first = 0;
    CData/*0:0*/ __PVT__add_devices_rx_pipe_ready_source_last;
    __PVT__add_devices_rx_pipe_ready_source_last = 0;
    CData/*0:0*/ __PVT__builder_litespi_tx_mux_source_first;
    __PVT__builder_litespi_tx_mux_source_first = 0;
    CData/*0:0*/ __PVT__builder_litespi_tx_mux_source_last;
    __PVT__builder_litespi_tx_mux_source_last = 0;
    SData/*9:0*/ __PVT__builder_litespi_tx_mux_source_payload_clk_div;
    __PVT__builder_litespi_tx_mux_source_payload_clk_div = 0;
    CData/*7:0*/ __PVT__builder_litespi_tx_mux_source_payload_mask;
    __PVT__builder_litespi_tx_mux_source_payload_mask = 0;
    // Body
    vlSelfRef.__PVT__add_devices_crossbar_cs = 0U;
    vlSelfRef.__PVT__add_devices_ctrlmailboxdma16 = 0U;
    vlSelfRef.__PVT__add_devices_ctrlmailboxdma_cfg_storage = 0U;
    vlSelfRef.__PVT__add_devices_ctrlmailboxdma_cmd_storage = 0U;
    vlSelfRef.__PVT__add_devices_ctrlmailboxdma_cmd_wr_stb = 0U;
    vlSelfRef.__PVT__add_devices_ctrlmailboxdma_mem_storage = 0U;
    vlSelfRef.__PVT__add_devices_master_clk_divisor_storage = 0U;
    vlSelfRef.__PVT__add_devices_master_cs_storage = 0U;
    vlSelfRef.__PVT__add_devices_master_phyconfig_storage = 0U;
    vlSelfRef.__PVT__add_devices_master_rx_fifo_pipe_valid_source_payload_data = 0U;
    vlSelfRef.__PVT__add_devices_master_rx_fifo_pipe_valid_source_valid = 0U;
    vlSelfRef.__PVT__add_devices_master_rxtx_re = 0U;
    vlSelfRef.__PVT__add_devices_master_rxtx_we = 0U;
    vlSelfRef.__PVT__add_devices_master_status_status = 0U;
    vlSelfRef.__PVT__add_devices_master_tx_fifo_pipe_valid_source_first = 0U;
    vlSelfRef.__PVT__add_devices_master_tx_fifo_pipe_valid_source_last = 0U;
    vlSelfRef.__PVT__add_devices_master_tx_fifo_pipe_valid_source_payload_clk_div = 0U;
    vlSelfRef.__PVT__add_devices_master_tx_fifo_pipe_valid_source_payload_data = 0U;
    vlSelfRef.__PVT__add_devices_master_tx_fifo_pipe_valid_source_payload_len = 0U;
    vlSelfRef.__PVT__add_devices_master_tx_fifo_pipe_valid_source_payload_mask = 0U;
    vlSelfRef.__PVT__add_devices_master_tx_fifo_pipe_valid_source_payload_width = 0U;
    vlSelfRef.__PVT__add_devices_master_tx_fifo_pipe_valid_source_valid = 0U;
    vlSelfRef.__PVT__add_devices_mmap_burst_adr = 0U;
    vlSelfRef.__PVT__add_devices_mmap_burst_adr_subfragments_next_value3 = 0U;
    vlSelfRef.__PVT__add_devices_mmap_burst_adr_subfragments_next_value_ce3 = 0U;
    vlSelfRef.__PVT__add_devices_mmap_burst_cs = 0U;
    vlSelfRef.__PVT__add_devices_mmap_burst_cs_subfragments_next_value1 = 0U;
    vlSelfRef.__PVT__add_devices_mmap_burst_cs_subfragments_next_value_ce1 = 0U;
    vlSelfRef.__PVT__add_devices_mmap_bus_ack = 0U;
    vlSelfRef.__PVT__add_devices_mmap_bus_adr = 0U;
    vlSelfRef.__PVT__add_devices_mmap_bus_dat_r = 0U;
    vlSelfRef.__PVT__add_devices_mmap_byte_count = 0U;
    vlSelfRef.__PVT__add_devices_mmap_byte_count_subfragments_next_value2 = 0U;
    vlSelfRef.__PVT__add_devices_mmap_byte_count_subfragments_next_value_ce2 = 0U;
    vlSelfRef.__PVT__add_devices_mmap_clk_divisor_storage = 0U;
    vlSelfRef.__PVT__add_devices_mmap_count = 0x0100U;
    vlSelfRef.__PVT__add_devices_mmap_cs = 0U;
    vlSelfRef.__PVT__add_devices_mmap_dummy_bits_storage = 8U;
    vlSelfRef.__PVT__add_devices_mmap_request = 0U;
    vlSelfRef.__PVT__add_devices_mmap_sink_ready = 0U;
    vlSelfRef.__PVT__add_devices_mmap_source_payload_clk_div = 0U;
    vlSelfRef.__PVT__add_devices_mmap_source_payload_clk_div_subfragments_next_value0 = 0U;
    vlSelfRef.__PVT__add_devices_mmap_source_payload_clk_div_subfragments_next_value_ce0 = 0U;
    vlSelfRef.__PVT__add_devices_mmap_source_payload_data = 0U;
    vlSelfRef.__PVT__add_devices_mmap_source_payload_len = 0U;
    vlSelfRef.__PVT__add_devices_mmap_source_payload_mask = 0U;
    vlSelfRef.__PVT__add_devices_mmap_source_payload_width = 0U;
    vlSelfRef.__PVT__add_devices_mmap_source_valid = 0U;
    vlSelfRef.__PVT__add_devices_mmap_wait = 0U;
    vlSelfRef.__PVT__add_devices_rx_pipe_ready_sink_d_first = 0U;
    vlSelfRef.__PVT__add_devices_rx_pipe_ready_sink_d_last = 0U;
    vlSelfRef.__PVT__add_devices_rx_pipe_ready_sink_d_payload_data = 0U;
    vlSelfRef.__PVT__add_devices_rx_pipe_ready_sink_d_valid = 0U;
    __PVT__add_devices_rx_pipe_ready_source_first = 0U;
    __PVT__add_devices_rx_pipe_ready_source_last = 0U;
    vlSelfRef.__PVT__add_devices_rx_pipe_ready_source_payload_data = 0U;
    vlSelfRef.__PVT__add_devices_rx_pipe_ready_source_valid = 0U;
    vlSelfRef.__PVT__add_devices_rx_pipe_ready_valid = 0U;
    vlSelfRef.__PVT__add_devices_rx_pipe_valid_source_first = 0U;
    vlSelfRef.__PVT__add_devices_rx_pipe_valid_source_last = 0U;
    vlSelfRef.__PVT__add_devices_rx_pipe_valid_source_payload_data = 0U;
    vlSelfRef.__PVT__add_devices_rx_pipe_valid_source_valid = 0U;
    vlSelfRef.__PVT__add_devices_stimulusmailbox_ms_cnt = 0U;
    vlSelfRef.__PVT__add_devices_stimulusmailbox_ms_tick = 0U;
    vlSelfRef.__PVT__add_devices_stimulusmailbox_waited0 = 0U;
    vlSelfRef.__PVT__add_devices_stimulusmailbox_waited1 = 0U;
    vlSelfRef.__PVT__add_devices_tx_pipe_ready_sink_d_payload_data = 0U;
    vlSelfRef.__PVT__add_devices_tx_pipe_ready_sink_d_payload_len = 0U;
    vlSelfRef.__PVT__add_devices_tx_pipe_ready_sink_d_payload_width = 0U;
    vlSelfRef.__PVT__add_devices_tx_pipe_ready_sink_d_valid = 0U;
    vlSelfRef.__PVT__add_devices_tx_pipe_ready_source_payload_data = 0U;
    vlSelfRef.__PVT__add_devices_tx_pipe_ready_source_payload_len = 0U;
    vlSelfRef.__PVT__add_devices_tx_pipe_ready_source_payload_width = 0U;
    vlSelfRef.__PVT__add_devices_tx_pipe_ready_source_valid = 0U;
    vlSelfRef.__PVT__add_devices_tx_pipe_ready_valid = 0U;
    vlSelfRef.__PVT__add_devices_tx_pipe_valid_source_payload_data = 0U;
    vlSelfRef.__PVT__add_devices_tx_pipe_valid_source_payload_len = 0U;
    vlSelfRef.__PVT__add_devices_tx_pipe_valid_source_payload_width = 0U;
    vlSelfRef.__PVT__add_devices_tx_pipe_valid_source_valid = 0U;
    vlSelfRef.__PVT__builder_basiclowerer_self = 0U;
    vlSelfRef.__PVT__builder_count = 0x000f4240U;
    vlSelfRef.__PVT__builder_csr_bankarray_csrbank0_reset_re = 0U;
    vlSelfRef.__PVT__builder_csr_bankarray_csrbank0_scratch_re = 0U;
    vlSelfRef.__PVT__builder_csr_bankarray_csrbank1_cfg_re = 0U;
    vlSelfRef.__PVT__builder_csr_bankarray_csrbank1_cmd_re = 0U;
    vlSelfRef.__PVT__builder_csr_bankarray_csrbank1_mem_re = 0U;
    vlSelfRef.__PVT__builder_csr_bankarray_csrbank2_req_re = 0U;
    vlSelfRef.__PVT__builder_csr_bankarray_csrbank3_master_clk_divisor_re = 0U;
    vlSelfRef.__PVT__builder_csr_bankarray_csrbank3_master_cs_re = 0U;
    vlSelfRef.__PVT__builder_csr_bankarray_csrbank3_master_phyconfig_re = 0U;
    vlSelfRef.__PVT__builder_csr_bankarray_csrbank3_mmap_clk_divisor_re = 0U;
    vlSelfRef.__PVT__builder_csr_bankarray_csrbank3_mmap_dummy_bits_re = 0U;
    vlSelfRef.__PVT__builder_csr_bankarray_csrbank3_phy_clk_divisor_re = 0U;
    vlSelfRef.__PVT__builder_csr_bankarray_csrbank3_phy_mode_re = 0U;
    vlSelfRef.__PVT__builder_csr_bankarray_csrbank4_en_re = 0U;
    vlSelfRef.__PVT__builder_csr_bankarray_csrbank4_ev_enable_re = 0U;
    vlSelfRef.__PVT__builder_csr_bankarray_csrbank4_ev_pending_re = 0U;
    vlSelfRef.__PVT__builder_csr_bankarray_csrbank4_load_re = 0U;
    vlSelfRef.__PVT__builder_csr_bankarray_csrbank4_reload_re = 0U;
    vlSelfRef.__PVT__builder_csr_bankarray_csrbank4_update_value_re = 0U;
    vlSelfRef.__PVT__builder_csr_bankarray_csrbank5_ev_enable_re = 0U;
    vlSelfRef.__PVT__builder_csr_bankarray_csrbank5_ev_pending_re = 0U;
    vlSelfRef.__PVT__builder_csr_bankarray_interface0_bank_bus_dat_r = 0U;
    vlSelfRef.__PVT__builder_csr_bankarray_interface1_bank_bus_dat_r = 0U;
    vlSelfRef.__PVT__builder_csr_bankarray_interface2_bank_bus_dat_r = 0U;
    vlSelfRef.__PVT__builder_csr_bankarray_interface3_bank_bus_dat_r = 0U;
    vlSelfRef.__PVT__builder_csr_bankarray_interface4_bank_bus_dat_r = 0U;
    vlSelfRef.__PVT__builder_csr_bankarray_interface5_bank_bus_dat_r = 0U;
    vlSelfRef.__PVT__builder_csr_bankarray_sel_r = 0U;
    vlSelfRef.__PVT__builder_csr_bankarray_sram_bus_dat_r = 0U;
    vlSelfRef.__PVT__builder_csr_data_width = 0U;
    vlSelfRef.__PVT__builder_error = 0U;
    vlSelfRef.__PVT__builder_interface0_ack = 0U;
    vlSelfRef.__PVT__builder_interface0_dat_r = 0U;
    vlSelfRef.__PVT__builder_interface1_adr = 0U;
    vlSelfRef.__PVT__builder_interface1_dat_w = 0U;
    vlSelfRef.__PVT__builder_interface1_re = 0U;
    vlSelfRef.__PVT__builder_interface1_we = 0U;
    vlSelfRef.__PVT__builder_litespi_grant = 0U;
    vlSelfRef.__PVT__builder_litespi_next_state = 0U;
    vlSelfRef.__PVT__builder_litespi_rx_demux_endpoint0_source_payload_data = 0U;
    vlSelfRef.__PVT__builder_litespi_rx_demux_endpoint0_source_valid = 0U;
    vlSelfRef.__PVT__builder_litespi_rx_demux_endpoint1_source_payload_data = 0U;
    vlSelfRef.__PVT__builder_litespi_rx_demux_endpoint1_source_valid = 0U;
    vlSelfRef.__PVT__builder_litespi_rx_demux_sink_ready = 0U;
    vlSelfRef.__PVT__builder_litespi_state = 0U;
    vlSelfRef.__PVT__builder_litespi_tx_mux_endpoint0_sink_ready = 0U;
    vlSelfRef.__PVT__builder_litespi_tx_mux_endpoint1_sink_ready = 0U;
    __PVT__builder_litespi_tx_mux_source_first = 0U;
    __PVT__builder_litespi_tx_mux_source_last = 0U;
    __PVT__builder_litespi_tx_mux_source_payload_clk_div = 0U;
    vlSelfRef.__PVT__builder_litespi_tx_mux_source_payload_data = 0U;
    vlSelfRef.__PVT__builder_litespi_tx_mux_source_payload_len = 0U;
    __PVT__builder_litespi_tx_mux_source_payload_mask = 0U;
    vlSelfRef.__PVT__builder_litespi_tx_mux_source_payload_width = 0U;
    vlSelfRef.__PVT__builder_litespi_tx_mux_source_valid = 0U;
    vlSelfRef.__PVT__builder_next_state = 0U;
    vlSelfRef.__PVT__builder_rhs_self0 = 0U;
    vlSelfRef.__PVT__builder_rhs_self1 = 0U;
    vlSelfRef.__PVT__builder_rhs_self2 = 0U;
    vlSelfRef.__PVT__builder_rhs_self3 = 0U;
    vlSelfRef.__PVT__builder_rhs_self4 = 0U;
    vlSelfRef.__PVT__builder_rhs_self5 = 0U;
    vlSelfRef.__PVT__builder_shared_ack = 0U;
    vlSelfRef.__PVT__builder_shared_dat_r = 0U;
    vlSelfRef.__PVT__builder_slave_sel = 0U;
    vlSelfRef.__PVT__builder_slave_sel_r = 0U;
    vlSelfRef.__PVT__builder_state = 0U;
    vlSelfRef.__PVT__builder_wishbone2csr_next_state = 0U;
    vlSelfRef.__PVT__builder_wishbone2csr_state = 0U;
    vlSelfRef.__PVT__ctrlmemory0_slave_sel = 0U;
    vlSelfRef.__PVT__ctrlmemory0_sram0_bus_ack = 0U;
    vlSelfRef.__PVT__ctrlmemory0_sram1_bus_ack = 0U;
    vlSelfRef.__PVT__ctrlmemory1_slave_sel = 0U;
    vlSelfRef.__PVT__ctrlmemory1_sram2_bus_ack = 0U;
    vlSelfRef.__PVT__ctrlmemory1_sram2_we = 0U;
    vlSelfRef.__PVT__ctrlmemory1_sram3_bus_ack = 0U;
    vlSelfRef.__PVT__ctrlmemory1_sram3_we = 0U;
    vlSelfRef.__PVT__ctrlmemory1_sram4_bus_ack = 0U;
    vlSelfRef.__PVT__ctrlmemory1_sram4_we = 0U;
}

VL_ATTR_COLD void Vsim_sim___eval_initial__TOP__sim(Vsim_sim* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+      Vsim_sim___eval_initial__TOP__sim\n"); );
    Vsim__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Body
    VL_READMEM_N(true, 8, 49, 0, "sim_mem.init"s,  &(vlSelfRef.__PVT__mem)
                 , 0, ~0ULL);
    VL_READMEM_N(true, 32, 32768, 0, "sim_rom_bank0.init"s
                 ,  &(vlSelfRef.__PVT__rom_bank0), 0
                 , ~0ULL);
    VL_READMEM_N(true, 32, 2048, 0, "sim_rom_bank1.init"s
                 ,  &(vlSelfRef.__PVT__rom_bank1), 0
                 , ~0ULL);
}

VL_ATTR_COLD void Vsim_sim___stl_sequent__TOP__sim__0(Vsim_sim* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+      Vsim_sim___stl_sequent__TOP__sim__0\n"); );
    Vsim__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Locals
    CData/*0:0*/ __PVT__builder_litespi_tx_mux_source_first;
    __PVT__builder_litespi_tx_mux_source_first = 0;
    CData/*0:0*/ __PVT__builder_litespi_tx_mux_source_last;
    __PVT__builder_litespi_tx_mux_source_last = 0;
    SData/*9:0*/ __PVT__builder_litespi_tx_mux_source_payload_clk_div;
    __PVT__builder_litespi_tx_mux_source_payload_clk_div = 0;
    // Body
    vlSelfRef.__PVT__builder_error = 0U;
    if ((0U == vlSelfRef.__PVT__builder_count)) {
        vlSelfRef.__PVT__builder_error = 1U;
    }
    vlSelfRef.__PVT__add_devices_mmap_wait = 0U;
    vlSelfRef.__PVT__add_devices_mmap_burst_cs_subfragments_next_value_ce1 = 0U;
    vlSelfRef.__PVT__add_devices_mmap_source_payload_clk_div_subfragments_next_value_ce0 = 0U;
    vlSelfRef.__PVT__soc_tx_fifo_wrport_adr = vlSelfRef.__PVT__soc_tx_fifo_produce;
    vlSelfRef.__PVT__soc_rx_fifo_wrport_adr = vlSelfRef.__PVT__soc_rx_fifo_produce;
    vlSelfRef.KL_mbx__DOT__u_evt__DOT__wr_en_o = vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__busy_r;
    __PVT__builder_litespi_tx_mux_source_first = ((IData)(vlSelfRef.__PVT__builder_litespi_grant) 
                                                  && (IData)(vlSelfRef.__PVT__add_devices_master_tx_fifo_pipe_valid_source_first));
    __PVT__builder_litespi_tx_mux_source_last = ((IData)(vlSelfRef.__PVT__builder_litespi_grant) 
                                                 && (IData)(vlSelfRef.__PVT__add_devices_master_tx_fifo_pipe_valid_source_last));
    vlSelfRef.__PVT__add_devices_mmap_source_payload_clk_div_subfragments_next_value0 = 0U;
    vlSelfRef.__PVT__zero_clear = 0U;
    if (((IData)(vlSelfRef.__PVT__pending_wr_stb) & (IData)(vlSelfRef.__PVT__pending_wr_data))) {
        vlSelfRef.__PVT__zero_clear = 1U;
    }
    vlSelfRef.__PVT__KL_mbx_dma__DOT__left_next_w = 
        (0x000007ffU & ((IData)(vlSelfRef.__PVT__KL_mbx_dma__DOT__left_r) 
                        - (IData)(vlSelfRef.__PVT__KL_mbx_dma__DOT__chunk_r)));
    vlSelfRef.__PVT__KL_mbx_dma__DOT__word_addr_next_w 
        = (0x3fffffffU & (vlSelfRef.__PVT__KL_mbx_dma__DOT__word_addr_r 
                          + (IData)(vlSelfRef.__PVT__KL_mbx_dma__DOT__chunk_r)));
    vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__cls_at_w 
        = ((0x000fU == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__cnt_r)) 
           | ((IData)(vlSymsp->TOP.mbx_rx_last) & (0x000eU 
                                                   == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__cnt_r))));
    vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__drop_w 
        = ((IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__vd_drop_r) 
           & (2U == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__st_r)));
    vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__rate_w 
        = ((IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__vd_rate_r) 
           & (2U == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__st_r)));
    vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__accept_w 
        = ((IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__vd_acc_r) 
           & (2U == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__st_r)));
    vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__mis_w 
        = ((IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__vd_mis_r) 
           & (2U == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__st_r)));
    vlSelfRef.KL_mbx__DOT__u_evt__DOT__wr_addr_o = 
        (0x0000003fU & ((IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__head_r) 
                        + (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__k_r)));
    vlSelfRef.KL_mbx__DOT__u_evt__DOT__wr_data_o = vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__rec_r
        [vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__k_r];
    vlSelfRef.KL_mbx__DOT____Vcellinp__u_rx__own_eid_i 
        = (((QData)((IData)(vlSelfRef.__PVT__KL_mbx__DOT__own_eid_hi_r)) 
            << 0x00000020U) | (QData)((IData)(vlSelfRef.__PVT__KL_mbx__DOT__own_eid_lo_r)));
    __PVT__builder_litespi_tx_mux_source_payload_clk_div 
        = ((IData)(vlSelfRef.__PVT__builder_litespi_grant)
            ? (IData)(vlSelfRef.__PVT__add_devices_master_tx_fifo_pipe_valid_source_payload_clk_div)
            : (IData)(vlSelfRef.__PVT__add_devices_mmap_source_payload_clk_div));
    vlSelfRef.__PVT__add_devices_mmap_burst_cs_subfragments_next_value1 = 0U;
    if ((8U & (IData)(vlSelfRef.__PVT__builder_litespi_state))) {
        if ((4U & (IData)(vlSelfRef.__PVT__builder_litespi_state))) {
            vlSelfRef.__PVT__add_devices_mmap_wait = 1U;
            vlSelfRef.__PVT__add_devices_mmap_burst_cs_subfragments_next_value_ce1 = 1U;
            vlSelfRef.__PVT__add_devices_mmap_source_payload_clk_div_subfragments_next_value_ce0 = 1U;
            vlSelfRef.__PVT__add_devices_mmap_source_payload_clk_div_subfragments_next_value0 
                = vlSelfRef.__PVT__add_devices_mmap_clk_divisor_storage;
            vlSelfRef.__PVT__add_devices_mmap_burst_cs_subfragments_next_value1 
                = ((IData)(vlSelfRef.__PVT__add_devices_mmap_burst_cs) 
                   & (0U != (IData)(vlSelfRef.__PVT__add_devices_mmap_count)));
        } else if ((2U & (IData)(vlSelfRef.__PVT__builder_litespi_state))) {
            vlSelfRef.__PVT__add_devices_mmap_wait = 1U;
            vlSelfRef.__PVT__add_devices_mmap_burst_cs_subfragments_next_value_ce1 = 1U;
            vlSelfRef.__PVT__add_devices_mmap_source_payload_clk_div_subfragments_next_value_ce0 = 1U;
            vlSelfRef.__PVT__add_devices_mmap_source_payload_clk_div_subfragments_next_value0 
                = vlSelfRef.__PVT__add_devices_mmap_clk_divisor_storage;
            vlSelfRef.__PVT__add_devices_mmap_burst_cs_subfragments_next_value1 
                = ((IData)(vlSelfRef.__PVT__add_devices_mmap_burst_cs) 
                   & (0U != (IData)(vlSelfRef.__PVT__add_devices_mmap_count)));
        } else if ((1U & (IData)(vlSelfRef.__PVT__builder_litespi_state))) {
            vlSelfRef.__PVT__add_devices_mmap_wait = 1U;
            vlSelfRef.__PVT__add_devices_mmap_burst_cs_subfragments_next_value_ce1 = 1U;
            vlSelfRef.__PVT__add_devices_mmap_source_payload_clk_div_subfragments_next_value_ce0 = 1U;
            vlSelfRef.__PVT__add_devices_mmap_source_payload_clk_div_subfragments_next_value0 
                = vlSelfRef.__PVT__add_devices_mmap_clk_divisor_storage;
            vlSelfRef.__PVT__add_devices_mmap_burst_cs_subfragments_next_value1 
                = ((IData)(vlSelfRef.__PVT__add_devices_mmap_burst_cs) 
                   & (0U != (IData)(vlSelfRef.__PVT__add_devices_mmap_count)));
        }
    } else if ((1U & (~ ((IData)(vlSelfRef.__PVT__builder_litespi_state) 
                         >> 2U)))) {
        if ((1U & (~ ((IData)(vlSelfRef.__PVT__builder_litespi_state) 
                      >> 1U)))) {
            if ((1U & (~ (IData)(vlSelfRef.__PVT__builder_litespi_state)))) {
                vlSelfRef.__PVT__add_devices_mmap_wait = 1U;
                vlSelfRef.__PVT__add_devices_mmap_source_payload_clk_div_subfragments_next_value_ce0 = 1U;
                vlSelfRef.__PVT__add_devices_mmap_source_payload_clk_div_subfragments_next_value0 
                    = vlSelfRef.__PVT__add_devices_mmap_clk_divisor_storage;
            }
        }
        if ((2U & (IData)(vlSelfRef.__PVT__builder_litespi_state))) {
            if ((1U & (IData)(vlSelfRef.__PVT__builder_litespi_state))) {
                vlSelfRef.__PVT__add_devices_mmap_burst_cs_subfragments_next_value_ce1 = 1U;
                vlSelfRef.__PVT__add_devices_mmap_burst_cs_subfragments_next_value1 = 1U;
            }
        } else if ((1U & (~ (IData)(vlSelfRef.__PVT__builder_litespi_state)))) {
            vlSelfRef.__PVT__add_devices_mmap_burst_cs_subfragments_next_value_ce1 = 1U;
            vlSelfRef.__PVT__add_devices_mmap_burst_cs_subfragments_next_value1 
                = ((IData)(vlSelfRef.__PVT__add_devices_mmap_burst_cs) 
                   & (0U != (IData)(vlSelfRef.__PVT__add_devices_mmap_count)));
        }
    }
    vlSelfRef.__PVT__soc_tx_fifo_do_read = (((~ (IData)(vlSelfRef.__PVT__soc_tx_fifo_readable)) 
                                             | (IData)(vlSymsp->TOP.serial_source_ready)) 
                                            & (0U != (IData)(vlSelfRef.__PVT__soc_tx_fifo_level0)));
    vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__drain_w 
        = ((IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__cls_done_r) 
           & ((0U != (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__q_cnt_r)) 
              & ((0U == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__st_r)) 
                 | (1U == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__st_r)))));
    vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__fin_ready_w 
        = ((1U == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__st_r)) 
           & ((IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__cls_done_r) 
              & (0U == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__q_cnt_r))));
    vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__word_w 
        = (vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__wacc_r 
           | ((IData)(vlSymsp->TOP.mbx_rx_data) << 
              ((IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__lane_r) 
               << 3U)));
    vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__tick_p_w 
        = (vlSelfRef.__PVT__KL_mbx__DOT__tick_ctl_r 
           & ((IData)(vlSelfRef.__PVT__add_devices_stimulusmailbox_ms_tick) 
              & (0x0000000aU <= ((IData)(1U) + (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__tick_div_r)))));
    vlSelfRef.__PVT__KL_mbx_dma__DOT__ring_addr_next_w 
        = (0x00001fffU & ((IData)(vlSelfRef.__PVT__KL_mbx_dma__DOT__base_r) 
                          + ((IData)(vlSelfRef.__PVT__KL_mbx_dma__DOT__mask_r) 
                             & ((IData)(1U) + (IData)(vlSelfRef.__PVT__KL_mbx_dma__DOT__index_r)))));
    vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__bad_w 
        = (((IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__overflow_r) 
            | (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__oversize_r)) 
           | ((IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__cnt_r) 
              > ((4U >= (IData)(vlSelfRef.KL_mbx__DOT__u_rx__DOT__ch_r))
                  ? vlSymsp->TOP__KL_mbx_pkg.__PVT__MBX_CH_MAX_FRAME_BYTES_TBL_C
                 [vlSelfRef.KL_mbx__DOT__u_rx__DOT__ch_r]
                  : 0U)));
    vlSelfRef.__PVT__add_devices_mmap_source_valid = 0U;
    vlSelfRef.__PVT__add_devices_mmap_source_payload_width = 0U;
    if ((1U & (~ ((IData)(vlSelfRef.__PVT__builder_litespi_state) 
                  >> 3U)))) {
        if ((1U & (IData)(vlSelfRef.__PVT__builder_litespi_state))) {
            vlSelfRef.__PVT__add_devices_mmap_source_valid = 1U;
            vlSelfRef.__PVT__add_devices_mmap_source_payload_width = 1U;
        }
    }
}

VL_ATTR_COLD void Vsim_sim___stl_sequent__TOP__sim__1(Vsim_sim* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+      Vsim_sim___stl_sequent__TOP__sim__1\n"); );
    Vsim__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Locals
    CData/*0:0*/ __PVT__add_devices_rx_pipe_ready_source_first;
    __PVT__add_devices_rx_pipe_ready_source_first = 0;
    CData/*0:0*/ __PVT__add_devices_rx_pipe_ready_source_last;
    __PVT__add_devices_rx_pipe_ready_source_last = 0;
    // Body
    vlSelfRef.__PVT__add_devices_mmap_source_payload_mask = 0U;
    if (vlSelfRef.__PVT__add_devices_tx_pipe_ready_valid) {
        vlSelfRef.__PVT__add_devices_tx_pipe_ready_source_valid 
            = vlSelfRef.__PVT__add_devices_tx_pipe_ready_sink_d_valid;
        vlSelfRef.__PVT__add_devices_tx_pipe_ready_source_payload_data 
            = vlSelfRef.__PVT__add_devices_tx_pipe_ready_sink_d_payload_data;
        vlSelfRef.__PVT__add_devices_tx_pipe_ready_source_payload_len 
            = vlSelfRef.__PVT__add_devices_tx_pipe_ready_sink_d_payload_len;
        vlSelfRef.__PVT__add_devices_tx_pipe_ready_source_payload_width 
            = vlSelfRef.__PVT__add_devices_tx_pipe_ready_sink_d_payload_width;
    } else {
        vlSelfRef.__PVT__add_devices_tx_pipe_ready_source_valid 
            = vlSelfRef.__PVT__add_devices_tx_pipe_valid_source_valid;
        vlSelfRef.__PVT__add_devices_tx_pipe_ready_source_payload_data 
            = vlSelfRef.__PVT__add_devices_tx_pipe_valid_source_payload_data;
        vlSelfRef.__PVT__add_devices_tx_pipe_ready_source_payload_len 
            = vlSelfRef.__PVT__add_devices_tx_pipe_valid_source_payload_len;
        vlSelfRef.__PVT__add_devices_tx_pipe_ready_source_payload_width 
            = vlSelfRef.__PVT__add_devices_tx_pipe_valid_source_payload_width;
    }
    vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__wdata_w 
        = ((3U == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__st_r))
            ? (0x10000000U | ((IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__cnt_r) 
                              | ((IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__if_r) 
                                 << 0x00000010U))) : 
           ((4U == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__st_r))
             ? vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__arrival_ms_r
             : vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__q_data_r
            [vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__q_rd_r]));
    vlSelfRef.__PVT__KL_mbx__DOT__txr_data_w = ((4U 
                                                 & (IData)(vlSelfRef.__PVT__KL_mbx__DOT__txr_ch_r))
                                                 ? 
                                                ((- (IData)(
                                                            (1U 
                                                             & (~ (IData)(vlSelfRef.__PVT__KL_mbx__DOT__txr_ch_r))))) 
                                                 & (vlSelfRef.__PVT__KL_mbx__DOT__srp_tx_rdata_w 
                                                    & (- (IData)(
                                                                 (1U 
                                                                  & (~ 
                                                                     ((IData)(vlSelfRef.__PVT__KL_mbx__DOT__txr_ch_r) 
                                                                      >> 1U)))))))
                                                 : 
                                                ((2U 
                                                  & (IData)(vlSelfRef.__PVT__KL_mbx__DOT__txr_ch_r))
                                                  ? 
                                                 ((1U 
                                                   & (IData)(vlSelfRef.__PVT__KL_mbx__DOT__txr_ch_r))
                                                   ? vlSelfRef.__PVT__KL_mbx__DOT__maap_tx_rdata_w
                                                   : vlSelfRef.__PVT__KL_mbx__DOT__aecp_tx_rdata_w)
                                                  : 
                                                 ((1U 
                                                   & (IData)(vlSelfRef.__PVT__KL_mbx__DOT__txr_ch_r))
                                                   ? vlSelfRef.__PVT__KL_mbx__DOT__acmp_tx_rdata_w
                                                   : vlSelfRef.__PVT__KL_mbx__DOT__adp_tx_rdata_w)));
    vlSelfRef.__PVT__soc_rx_clear = 0U;
    if (((IData)(vlSelfRef.__PVT__soc_pending_wr_stb) 
         & ((IData)(vlSelfRef.__PVT__soc_pending_wr_data) 
            >> 1U))) {
        vlSelfRef.__PVT__soc_rx_clear = 1U;
    }
    vlSelfRef.__PVT__add_devices_mmap_source_payload_len = 0U;
    if ((1U & (~ ((IData)(vlSelfRef.__PVT__builder_litespi_state) 
                  >> 3U)))) {
        if ((4U & (IData)(vlSelfRef.__PVT__builder_litespi_state))) {
            if ((1U & (IData)(vlSelfRef.__PVT__builder_litespi_state))) {
                vlSelfRef.__PVT__add_devices_mmap_source_payload_mask = 0U;
            }
            if ((2U & (IData)(vlSelfRef.__PVT__builder_litespi_state))) {
                if ((1U & (IData)(vlSelfRef.__PVT__builder_litespi_state))) {
                    vlSelfRef.__PVT__add_devices_mmap_source_payload_len = 0x20U;
                }
            } else if ((1U & (IData)(vlSelfRef.__PVT__builder_litespi_state))) {
                vlSelfRef.__PVT__add_devices_mmap_source_payload_len 
                    = (0x0000003fU & (IData)(vlSelfRef.__PVT__add_devices_mmap_dummy_bits_storage));
            }
        } else {
            if ((1U & (IData)(vlSelfRef.__PVT__builder_litespi_state))) {
                vlSelfRef.__PVT__add_devices_mmap_source_payload_mask = 1U;
            }
            if ((2U & (IData)(vlSelfRef.__PVT__builder_litespi_state))) {
                if ((1U & (IData)(vlSelfRef.__PVT__builder_litespi_state))) {
                    vlSelfRef.__PVT__add_devices_mmap_source_payload_len = 0x18U;
                }
            } else if ((1U & (IData)(vlSelfRef.__PVT__builder_litespi_state))) {
                vlSelfRef.__PVT__add_devices_mmap_source_payload_len = 8U;
            }
        }
    }
    vlSelfRef.__PVT__add_devices_mmap_sink_ready = 0U;
    if ((8U & (IData)(vlSelfRef.__PVT__builder_litespi_state))) {
        if ((1U & (~ ((IData)(vlSelfRef.__PVT__builder_litespi_state) 
                      >> 2U)))) {
            if ((1U & (~ ((IData)(vlSelfRef.__PVT__builder_litespi_state) 
                          >> 1U)))) {
                if ((1U & (~ (IData)(vlSelfRef.__PVT__builder_litespi_state)))) {
                    vlSelfRef.__PVT__add_devices_mmap_sink_ready = 1U;
                }
            }
        }
    } else if ((4U & (IData)(vlSelfRef.__PVT__builder_litespi_state))) {
        if ((1U & (~ (IData)(vlSelfRef.__PVT__builder_litespi_state)))) {
            vlSelfRef.__PVT__add_devices_mmap_sink_ready = 1U;
        }
    } else if ((2U & (IData)(vlSelfRef.__PVT__builder_litespi_state))) {
        if ((1U & (~ (IData)(vlSelfRef.__PVT__builder_litespi_state)))) {
            vlSelfRef.__PVT__add_devices_mmap_sink_ready = 1U;
        }
    }
    if (vlSelfRef.__PVT__add_devices_rx_pipe_ready_valid) {
        __PVT__add_devices_rx_pipe_ready_source_first 
            = vlSelfRef.__PVT__add_devices_rx_pipe_ready_sink_d_first;
        __PVT__add_devices_rx_pipe_ready_source_last 
            = vlSelfRef.__PVT__add_devices_rx_pipe_ready_sink_d_last;
    } else {
        __PVT__add_devices_rx_pipe_ready_source_first 
            = vlSelfRef.__PVT__add_devices_rx_pipe_valid_source_first;
        __PVT__add_devices_rx_pipe_ready_source_last 
            = vlSelfRef.__PVT__add_devices_rx_pipe_valid_source_last;
    }
    vlSelfRef.__PVT__soc_vexiiriscv_pbus_r_payload_data = 0U;
    vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__max_words_w 
        = (0x000003ffU & (((IData)(3U) + ((4U >= (IData)(vlSelfRef.KL_mbx__DOT__u_rx__DOT__ch_r))
                                           ? vlSymsp->TOP__KL_mbx_pkg.__PVT__MBX_CH_MAX_FRAME_BYTES_TBL_C
                                          [vlSelfRef.KL_mbx__DOT__u_rx__DOT__ch_r]
                                           : 0U)) >> 2U));
    vlSelfRef.__PVT__soc_vexiiriscv_pbus_r_payload_resp = 0U;
    if ((1U & (~ ((IData)(vlSelfRef.__PVT__builder_state) 
                  >> 2U)))) {
        if ((2U & (IData)(vlSelfRef.__PVT__builder_state))) {
            if ((1U & (~ (IData)(vlSelfRef.__PVT__builder_state)))) {
                vlSelfRef.__PVT__soc_vexiiriscv_pbus_r_payload_data 
                    = vlSelfRef.__PVT__soc_data;
                vlSelfRef.__PVT__soc_vexiiriscv_pbus_r_payload_resp = 0U;
            }
        }
    }
    vlSelfRef.__PVT__soc_vexiiriscv_pbus_b_payload_resp = 0U;
    if ((4U & (IData)(vlSelfRef.__PVT__builder_state))) {
        if ((1U & (~ ((IData)(vlSelfRef.__PVT__builder_state) 
                      >> 1U)))) {
            if ((1U & (~ (IData)(vlSelfRef.__PVT__builder_state)))) {
                vlSelfRef.__PVT__soc_vexiiriscv_pbus_b_payload_resp = 0U;
            }
        }
    }
    vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__ctr_roll_w 
        = ((IData)(vlSelfRef.__PVT__add_devices_stimulusmailbox_ms_tick) 
           & (0x000003e8U <= ((IData)(1U) + (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__ctr_epoch_r))));
    vlSelfRef.__VdfgRegularize_h6e95ff9d_0_107 = (((IData)(vlSelfRef.__PVT__soc_rx_fifo_readable) 
                                                   << 1U) 
                                                  | (0x10U 
                                                     != (IData)(vlSelfRef.__PVT__soc_tx_fifo_level0)));
    vlSelfRef.__PVT__soc_soc_rst = 0U;
    if (vlSelfRef.__PVT__soc_reset_wr_stb) {
        vlSelfRef.__PVT__soc_soc_rst = (1U & (IData)(vlSelfRef.__PVT__soc_reset_storage));
    }
    vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__c_tap_w[0U] 
        = vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__g_cmp__BRA__0__KET____DOT__sr_r
        [(7U & ((IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__cnt_r) 
                - (IData)(2U)))];
    vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__c_tap_w[1U] 
        = vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__g_cmp__BRA__1__KET____DOT__sr_r
        [(7U & ((IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__cnt_r) 
                - (IData)(2U)))];
    vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__c_tap_w[2U] 
        = vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__g_cmp__BRA__2__KET____DOT__sr_r
        [(7U & ((IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__cnt_r) 
                - (IData)(2U)))];
    vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__c_tap_w[3U] 
        = vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__g_cmp__BRA__3__KET____DOT__sr_r
        [(7U & ((IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__cnt_r) 
                - (IData)(2U)))];
    vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__c_tap_w[4U] 
        = vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__g_cmp__BRA__4__KET____DOT__sr_r
        [(7U & ((IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__cnt_r) 
                - (IData)(2U)))];
    vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__c_tap_w[5U] 
        = vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__g_cmp__BRA__5__KET____DOT__sr_r
        [(7U & ((IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__cnt_r) 
                - (IData)(2U)))];
    vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__c_tap_w[6U] 
        = vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__g_cmp__BRA__6__KET____DOT__sr_r
        [(7U & ((IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__cnt_r) 
                - (IData)(2U)))];
    vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__c_tap_w[7U] 
        = vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__g_cmp__BRA__7__KET____DOT__sr_r
        [(7U & ((IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__cnt_r) 
                - (IData)(2U)))];
    vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__c_tap_w[8U] 
        = vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__g_cmp__BRA__8__KET____DOT__sr_r
        [(7U & ((IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__cnt_r) 
                - (IData)(2U)))];
    vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__c_tap_w[9U] 
        = vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__g_cmp__BRA__9__KET____DOT__sr_r
        [(7U & ((IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__cnt_r) 
                - (IData)(2U)))];
    vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__c_tap_w[10U] 
        = vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__g_cmp__BRA__10__KET____DOT__sr_r
        [(7U & ((IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__cnt_r) 
                - (IData)(2U)))];
    vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__c_tap_w[11U] 
        = vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__g_cmp__BRA__11__KET____DOT__sr_r
        [(7U & ((IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__cnt_r) 
                - (IData)(2U)))];
    vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__c_tap_w[12U] 
        = vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__g_cmp__BRA__12__KET____DOT__sr_r
        [(7U & ((IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__cnt_r) 
                - (IData)(2U)))];
    vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__c_tap_w[13U] 
        = vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__g_cmp__BRA__13__KET____DOT__sr_r
        [(7U & ((IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__cnt_r) 
                - (IData)(2U)))];
    vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__c_tap_w[14U] 
        = vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__g_cmp__BRA__14__KET____DOT__sr_r
        [(7U & ((IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__cnt_r) 
                - (IData)(2U)))];
}

extern const VlUnpacked<CData/*0:0*/, 2> Vsim__ConstPool__TABLE_h1b85385a_0;

VL_ATTR_COLD void Vsim_sim___stl_sequent__TOP__sim__2(Vsim_sim* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+      Vsim_sim___stl_sequent__TOP__sim__2\n"); );
    Vsim__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Locals
    SData/*15:0*/ __PVT__KL_mbx__DOT__u_rx__DOT__used_w;
    __PVT__KL_mbx__DOT__u_rx__DOT__used_w = 0;
    SData/*15:0*/ __PVT__KL_mbx__DOT__u_rx__DOT__cused_w;
    __PVT__KL_mbx__DOT__u_rx__DOT__cused_w = 0;
    SData/*15:0*/ __PVT__KL_mbx__DOT__u_rx__DOT__tail_w;
    __PVT__KL_mbx__DOT__u_rx__DOT__tail_w = 0;
    VlWide<3>/*95:0*/ __Vtemp_1;
    // Body
    vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__c_tap_w[15U] 
        = vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__g_cmp__BRA__15__KET____DOT__sr_r
        [(7U & ((IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__cnt_r) 
                - (IData)(2U)))];
    vlSelfRef.__VdfgRegularize_h6e95ff9d_0_109 = (0x0000ffffU 
                                                  & ((IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__head_r) 
                                                     - vlSelfRef.__PVT__KL_mbx__DOT__evt_tail_r));
    vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__own_mac_w 
        = ((((QData)((IData)(vlSelfRef.__PVT__KL_mbx__DOT__own_mac_hi_r[0U])) 
             << 0x00000020U) | (QData)((IData)(vlSelfRef.__PVT__KL_mbx__DOT__own_mac_lo_r[0U]))) 
           & (- (QData)((IData)((1U & (~ (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__if_r)))))));
    vlSelfRef.KL_mbx__DOT____Vcellinp__u_rx__maap_base_i 
        = (((QData)((IData)((0x0000ffffU & vlSelfRef.__PVT__KL_mbx__DOT__maap_base_hi_r))) 
            << 0x00000020U) | (QData)((IData)(vlSelfRef.__PVT__KL_mbx__DOT__maap_base_lo_r)));
    vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__ring_words_w 
        = ((4U >= (IData)(vlSelfRef.KL_mbx__DOT__u_rx__DOT__ch_r))
            ? (0x0000ffffU & vlSymsp->TOP__KL_mbx_pkg.__PVT__MBX_CH_RX_WORDS_TBL_C
               [vlSelfRef.KL_mbx__DOT__u_rx__DOT__ch_r])
            : 0U);
    __Vtemp_1[0U] = (IData)((((QData)((IData)((((IData)(vlSelfRef.__PVT__KL_mbx__DOT__rx_tail_r[3U]) 
                                                << 0x00000010U) 
                                               | vlSelfRef.__PVT__KL_mbx__DOT__rx_tail_r[2U]))) 
                              << 0x00000020U) | (QData)((IData)(
                                                                (((IData)(vlSelfRef.__PVT__KL_mbx__DOT__rx_tail_r[1U]) 
                                                                  << 0x00000010U) 
                                                                 | vlSelfRef.__PVT__KL_mbx__DOT__rx_tail_r[0U])))));
    __Vtemp_1[1U] = (IData)(((((QData)((IData)((((IData)(vlSelfRef.__PVT__KL_mbx__DOT__rx_tail_r[3U]) 
                                                 << 0x00000010U) 
                                                | vlSelfRef.__PVT__KL_mbx__DOT__rx_tail_r[2U]))) 
                               << 0x00000020U) | (QData)((IData)(
                                                                 (((IData)(vlSelfRef.__PVT__KL_mbx__DOT__rx_tail_r[1U]) 
                                                                   << 0x00000010U) 
                                                                  | vlSelfRef.__PVT__KL_mbx__DOT__rx_tail_r[0U])))) 
                             >> 0x00000020U));
    __Vtemp_1[2U] = vlSelfRef.__PVT__KL_mbx__DOT__rx_tail_r[4U];
    __PVT__KL_mbx__DOT__u_rx__DOT__tail_w = ((0x4fU 
                                              >= (0x0000007fU 
                                                  & ((IData)(vlSelfRef.KL_mbx__DOT__u_rx__DOT__ch_r) 
                                                     << 4U)))
                                              ? (0x0000ffffU 
                                                 & (((0U 
                                                      == 
                                                      (0x0000001fU 
                                                       & ((IData)(vlSelfRef.KL_mbx__DOT__u_rx__DOT__ch_r) 
                                                          << 4U)))
                                                      ? 0U
                                                      : 
                                                     (__Vtemp_1
                                                      [
                                                      (((IData)(0x0000000fU) 
                                                        + 
                                                        (0x0000007fU 
                                                         & ((IData)(vlSelfRef.KL_mbx__DOT__u_rx__DOT__ch_r) 
                                                            << 4U))) 
                                                       >> 5U)] 
                                                      << 
                                                      ((IData)(0x00000020U) 
                                                       - 
                                                       (0x0000001fU 
                                                        & ((IData)(vlSelfRef.KL_mbx__DOT__u_rx__DOT__ch_r) 
                                                           << 4U))))) 
                                                    | (__Vtemp_1
                                                       [
                                                       (3U 
                                                        & ((IData)(vlSelfRef.KL_mbx__DOT__u_rx__DOT__ch_r) 
                                                           >> 1U))] 
                                                       >> 
                                                       (0x0000001fU 
                                                        & ((IData)(vlSelfRef.KL_mbx__DOT__u_rx__DOT__ch_r) 
                                                           << 4U)))))
                                              : 0U);
    __PVT__KL_mbx__DOT__u_rx__DOT__used_w = (0x0000ffffU 
                                             & (((4U 
                                                  >= (IData)(vlSelfRef.KL_mbx__DOT__u_rx__DOT__ch_r))
                                                  ? vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__wr_head_r
                                                 [vlSelfRef.KL_mbx__DOT__u_rx__DOT__ch_r]
                                                  : 0U) 
                                                - (IData)(__PVT__KL_mbx__DOT__u_rx__DOT__tail_w)));
    __PVT__KL_mbx__DOT__u_rx__DOT__cused_w = (0x0000ffffU 
                                              & (((4U 
                                                   >= (IData)(vlSelfRef.KL_mbx__DOT__u_rx__DOT__ch_r))
                                                   ? vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__head_r
                                                  [vlSelfRef.KL_mbx__DOT__u_rx__DOT__ch_r]
                                                   : 0U) 
                                                 - (IData)(__PVT__KL_mbx__DOT__u_rx__DOT__tail_w)));
    vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__free_w 
        = ((((IData)(__PVT__KL_mbx__DOT__u_rx__DOT__used_w) 
             > (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__ring_words_w)) 
            | ((IData)(__PVT__KL_mbx__DOT__u_rx__DOT__cused_w) 
               > (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__ring_words_w)))
            ? 0U : (0x0000ffffU & ((IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__ring_words_w) 
                                   - (IData)(__PVT__KL_mbx__DOT__u_rx__DOT__used_w))));
    vlSelfRef.__PVT__add_devices_crossbar_source_ready 
        = (1U & (~ ((IData)(vlSelfRef.__PVT__add_devices_tx_pipe_valid_source_valid) 
                    & (IData)(vlSelfRef.__PVT__add_devices_tx_pipe_ready_valid))));
    vlSelfRef.__PVT__soc_adapted_interface_dat_w = 0U;
    vlSelfRef.__PVT__builder_csr_bankarray_sram_bus_dat_r = 0U;
    if (vlSelfRef.__PVT__builder_csr_bankarray_sel_r) {
        vlSelfRef.__PVT__builder_csr_bankarray_sram_bus_dat_r 
            = vlSelfRef.__PVT__mem_dat0;
    }
    if (vlSelfRef.__PVT__add_devices_rx_pipe_ready_valid) {
        vlSelfRef.__PVT__add_devices_rx_pipe_ready_source_payload_data 
            = vlSelfRef.__PVT__add_devices_rx_pipe_ready_sink_d_payload_data;
        vlSelfRef.__PVT__add_devices_rx_pipe_ready_source_valid 
            = vlSelfRef.__PVT__add_devices_rx_pipe_ready_sink_d_valid;
    } else {
        vlSelfRef.__PVT__add_devices_rx_pipe_ready_source_payload_data 
            = vlSelfRef.__PVT__add_devices_rx_pipe_valid_source_payload_data;
        vlSelfRef.__PVT__add_devices_rx_pipe_ready_source_valid 
            = vlSelfRef.__PVT__add_devices_rx_pipe_valid_source_valid;
    }
    vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__refill_w[0U] 
        = ((IData)(vlSelfRef.__PVT__add_devices_stimulusmailbox_ms_tick) 
           & (0x0000000aU <= ((IData)(1U) + vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__refill_r[0U])));
    vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__refill_w[1U] 
        = ((IData)(vlSelfRef.__PVT__add_devices_stimulusmailbox_ms_tick) 
           & (5U <= ((IData)(1U) + vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__refill_r[1U])));
    vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__refill_w[2U] 
        = ((IData)(vlSelfRef.__PVT__add_devices_stimulusmailbox_ms_tick) 
           & (5U <= ((IData)(1U) + vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__refill_r[2U])));
    vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__refill_w[3U] 
        = ((IData)(vlSelfRef.__PVT__add_devices_stimulusmailbox_ms_tick) 
           & (0x00000014U <= ((IData)(1U) + vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__refill_r[3U])));
    vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__refill_w[4U] 
        = ((IData)(vlSelfRef.__PVT__add_devices_stimulusmailbox_ms_tick) 
           & (2U <= ((IData)(1U) + vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__refill_r[4U])));
    vlSelfRef.__PVT__KL_mbx_dma__DOT__last_chunk_w 
        = ((IData)(vlSelfRef.__PVT__KL_mbx_dma__DOT__left_r) 
           == (IData)(vlSelfRef.__PVT__KL_mbx_dma__DOT__chunk_r));
    vlSelfRef.__VdfgRegularize_h6e95ff9d_0_0 = (0x0000000fU 
                                                & VL_MULS_III(32, (IData)(0x00000010U), Vsim__ConstPool__TABLE_h1b85385a_0
                                                              [vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__if_r]));
    vlSelfRef.__PVT__KL_mbx__DOT__tx_head_w[0U] = (IData)(
                                                          (((QData)((IData)(
                                                                            (((IData)(vlSelfRef.__PVT__KL_mbx__DOT__tx_head_r[3U]) 
                                                                              << 0x00000010U) 
                                                                             | vlSelfRef.__PVT__KL_mbx__DOT__tx_head_r[2U]))) 
                                                            << 0x00000020U) 
                                                           | (QData)((IData)(
                                                                             (((IData)(vlSelfRef.__PVT__KL_mbx__DOT__tx_head_r[1U]) 
                                                                               << 0x00000010U) 
                                                                              | vlSelfRef.__PVT__KL_mbx__DOT__tx_head_r[0U])))));
    vlSelfRef.__PVT__KL_mbx__DOT__tx_head_w[1U] = (IData)(
                                                          ((((QData)((IData)(
                                                                             (((IData)(vlSelfRef.__PVT__KL_mbx__DOT__tx_head_r[3U]) 
                                                                               << 0x00000010U) 
                                                                              | vlSelfRef.__PVT__KL_mbx__DOT__tx_head_r[2U]))) 
                                                             << 0x00000020U) 
                                                            | (QData)((IData)(
                                                                              (((IData)(vlSelfRef.__PVT__KL_mbx__DOT__tx_head_r[1U]) 
                                                                                << 0x00000010U) 
                                                                               | vlSelfRef.__PVT__KL_mbx__DOT__tx_head_r[0U])))) 
                                                           >> 0x00000020U));
    vlSelfRef.__PVT__KL_mbx__DOT__tx_head_w[2U] = (0x0000ffffU 
                                                   & vlSelfRef.__PVT__KL_mbx__DOT__tx_head_r[4U]);
    vlSelfRef.__PVT__builder_interface0_ack = 0U;
    if (vlSelfRef.__PVT__builder_wishbone2csr_state) {
        vlSelfRef.__PVT__builder_interface0_ack = 1U;
    }
    vlSelfRef.__PVT__add_devices_ctrlmailboxdma5 = 
        ((IData)(vlSelfRef.__PVT__KL_mbx__DOT__ack_r) 
         & (IData)(vlSelfRef.__PVT__KL_mbx_dma__DOT__cpu_wait_r));
    vlSelfRef.__PVT__soc_adapted_interface_sel = 0U;
    if ((1U & (~ ((IData)(vlSelfRef.__PVT__builder_state) 
                  >> 2U)))) {
        if ((2U & (IData)(vlSelfRef.__PVT__builder_state))) {
            if ((1U & (IData)(vlSelfRef.__PVT__builder_state))) {
                vlSelfRef.__PVT__soc_adapted_interface_dat_w 
                    = vlSymsp->TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952.__PVT__peripheral_toAxiLite4_logic_bridge__DOT__a_halted_rData_data;
                vlSelfRef.__PVT__soc_adapted_interface_sel 
                    = vlSymsp->TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952.__PVT__peripheral_toAxiLite4_logic_bridge__DOT__a_halted_rData_mask;
            }
        } else if ((1U & (IData)(vlSelfRef.__PVT__builder_state))) {
            vlSelfRef.__PVT__soc_adapted_interface_sel = 0x0fU;
        }
    }
    vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__any_w = 0U;
    vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__src_w = 0U;
    vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__src_if_w = 0U;
    vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__src_slot_w = 0U;
    if (((IData)(vlSymsp->TOP.mbx_link_up) != (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__posted_up_r))) {
        vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__any_w = 1U;
        vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__src_w = 0U;
        vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__src_if_w = 0U;
    }
    if (((~ (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__any_w)) 
         & (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__gm_pend_r))) {
        vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__any_w = 1U;
        vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__src_w = 1U;
        vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__src_if_w = 0U;
    }
    if ((1U & ((~ (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__any_w)) 
               & (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__pend_r)))) {
        vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__any_w = 1U;
        vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__src_w = 2U;
        vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__src_slot_w = 0U;
    }
    if ((1U & ((~ (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__any_w)) 
               & ((IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__pend_r) 
                  >> 1U)))) {
        vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__any_w = 1U;
        vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__src_w = 2U;
        vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__src_slot_w = 1U;
    }
    if ((1U & ((~ (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__any_w)) 
               & ((IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__pend_r) 
                  >> 2U)))) {
        vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__any_w = 1U;
        vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__src_w = 2U;
        vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__src_slot_w = 2U;
    }
    if ((1U & ((~ (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__any_w)) 
               & ((IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__pend_r) 
                  >> 3U)))) {
        vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__any_w = 1U;
        vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__src_w = 2U;
        vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__src_slot_w = 3U;
    }
    if ((1U & ((~ (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__any_w)) 
               & ((IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__pend_r) 
                  >> 4U)))) {
        vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__any_w = 1U;
        vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__src_w = 2U;
        vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__src_slot_w = 4U;
    }
    if ((1U & ((~ (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__any_w)) 
               & ((IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__pend_r) 
                  >> 5U)))) {
        vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__any_w = 1U;
        vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__src_w = 2U;
        vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__src_slot_w = 5U;
    }
    if ((1U & ((~ (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__any_w)) 
               & ((IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__pend_r) 
                  >> 6U)))) {
        vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__any_w = 1U;
        vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__src_w = 2U;
        vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__src_slot_w = 6U;
    }
    if ((1U & ((~ (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__any_w)) 
               & ((IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__pend_r) 
                  >> 7U)))) {
        vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__any_w = 1U;
        vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__src_w = 2U;
        vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__src_slot_w = 7U;
    }
    if ((1U & ((~ (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__any_w)) 
               & ((IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__pend_r) 
                  >> 8U)))) {
        vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__any_w = 1U;
        vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__src_w = 2U;
        vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__src_slot_w = 8U;
    }
}

VL_ATTR_COLD void Vsim_sim___stl_sequent__TOP__sim__3(Vsim_sim* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+      Vsim_sim___stl_sequent__TOP__sim__3\n"); );
    Vsim__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Body
    if ((1U & ((~ (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__any_w)) 
               & ((IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__pend_r) 
                  >> 9U)))) {
        vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__any_w = 1U;
        vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__src_w = 2U;
        vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__src_slot_w = 9U;
    }
    if ((1U & ((~ (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__any_w)) 
               & ((IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__pend_r) 
                  >> 0x0aU)))) {
        vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__any_w = 1U;
        vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__src_w = 2U;
        vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__src_slot_w = 0x0aU;
    }
    if ((1U & ((~ (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__any_w)) 
               & ((IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__pend_r) 
                  >> 0x0bU)))) {
        vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__any_w = 1U;
        vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__src_w = 2U;
        vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__src_slot_w = 0x0bU;
    }
    if ((1U & ((~ (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__any_w)) 
               & ((IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__pend_r) 
                  >> 0x0cU)))) {
        vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__any_w = 1U;
        vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__src_w = 2U;
        vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__src_slot_w = 0x0cU;
    }
    if ((1U & ((~ (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__any_w)) 
               & ((IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__pend_r) 
                  >> 0x0dU)))) {
        vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__any_w = 1U;
        vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__src_w = 2U;
        vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__src_slot_w = 0x0dU;
    }
    if ((1U & ((~ (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__any_w)) 
               & ((IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__pend_r) 
                  >> 0x0eU)))) {
        vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__any_w = 1U;
        vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__src_w = 2U;
        vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__src_slot_w = 0x0eU;
    }
    if (((~ (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__any_w)) 
         & ((IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__pend_r) 
            >> 0x0000000fU))) {
        vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__any_w = 1U;
        vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__src_w = 2U;
        vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__src_slot_w = 0x0fU;
    }
    if (((~ (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__any_w)) 
         & (0U != (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__tick_cnt_r)))) {
        vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__any_w = 1U;
        vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__src_w = 3U;
    }
    vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__src_bit_w = 0U;
    if (((~ (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__any_w)) 
         & (0U != vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__amap_cnt_r[0U]))) {
        vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__any_w = 1U;
        vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__src_w = 4U;
        vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__src_if_w = 0U;
    }
    if (((~ (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__any_w)) 
         & (0U != vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__avb_cnt_r[0U]))) {
        vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__any_w = 1U;
        vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__src_w = 5U;
        vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__src_if_w = 0U;
    }
    if (((~ (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__any_w)) 
         & (0U != vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__asp_cnt_r[0U]))) {
        vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__any_w = 1U;
        vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__src_w = 6U;
        vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__src_if_w = 0U;
    }
    if ((1U & (((~ (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__any_w)) 
                & (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__ctr_pend_r[0U])) 
               & (~ (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__ctr_seen_r[0U]))))) {
        vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__any_w = 1U;
        vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__src_w = 7U;
        vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__src_if_w = 0U;
        vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__src_bit_w = 0U;
    }
    if ((1U & (((~ (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__any_w)) 
                & (IData)((vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__ctr_pend_r[0U] 
                           >> 1U))) & (~ (IData)((vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__ctr_seen_r[0U] 
                                                  >> 1U)))))) {
        vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__any_w = 1U;
        vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__src_w = 7U;
        vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__src_if_w = 0U;
        vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__src_bit_w = 1U;
    }
    if ((1U & (((~ (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__any_w)) 
                & (IData)((vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__ctr_pend_r[0U] 
                           >> 2U))) & (~ (IData)((vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__ctr_seen_r[0U] 
                                                  >> 2U)))))) {
        vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__any_w = 1U;
        vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__src_w = 7U;
        vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__src_if_w = 0U;
        vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__src_bit_w = 2U;
    }
    if ((1U & (((~ (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__any_w)) 
                & (IData)((vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__ctr_pend_r[0U] 
                           >> 3U))) & (~ (IData)((vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__ctr_seen_r[0U] 
                                                  >> 3U)))))) {
        vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__any_w = 1U;
        vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__src_w = 7U;
        vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__src_if_w = 0U;
        vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__src_bit_w = 3U;
    }
    if ((1U & (((~ (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__any_w)) 
                & (IData)((vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__ctr_pend_r[0U] 
                           >> 4U))) & (~ (IData)((vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__ctr_seen_r[0U] 
                                                  >> 4U)))))) {
        vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__any_w = 1U;
        vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__src_w = 7U;
        vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__src_if_w = 0U;
        vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__src_bit_w = 4U;
    }
    if ((1U & (((~ (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__any_w)) 
                & (IData)((vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__ctr_pend_r[0U] 
                           >> 5U))) & (~ (IData)((vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__ctr_seen_r[0U] 
                                                  >> 5U)))))) {
        vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__any_w = 1U;
        vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__src_w = 7U;
        vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__src_if_w = 0U;
        vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__src_bit_w = 5U;
    }
    if ((1U & (((~ (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__any_w)) 
                & (IData)((vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__ctr_pend_r[0U] 
                           >> 6U))) & (~ (IData)((vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__ctr_seen_r[0U] 
                                                  >> 6U)))))) {
        vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__any_w = 1U;
        vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__src_w = 7U;
        vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__src_if_w = 0U;
        vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__src_bit_w = 6U;
    }
    if ((1U & (((~ (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__any_w)) 
                & (IData)((vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__ctr_pend_r[0U] 
                           >> 7U))) & (~ (IData)((vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__ctr_seen_r[0U] 
                                                  >> 7U)))))) {
        vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__any_w = 1U;
        vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__src_w = 7U;
        vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__src_if_w = 0U;
        vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__src_bit_w = 7U;
    }
    if ((1U & (((~ (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__any_w)) 
                & (IData)((vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__ctr_pend_r[0U] 
                           >> 8U))) & (~ (IData)((vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__ctr_seen_r[0U] 
                                                  >> 8U)))))) {
        vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__any_w = 1U;
        vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__src_w = 7U;
        vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__src_if_w = 0U;
        vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__src_bit_w = 8U;
    }
    if ((1U & (((~ (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__any_w)) 
                & (IData)((vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__ctr_pend_r[0U] 
                           >> 9U))) & (~ (IData)((vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__ctr_seen_r[0U] 
                                                  >> 9U)))))) {
        vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__any_w = 1U;
        vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__src_w = 7U;
        vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__src_if_w = 0U;
        vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__src_bit_w = 9U;
    }
    if ((1U & (((~ (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__any_w)) 
                & (IData)((vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__ctr_pend_r[0U] 
                           >> 0x0aU))) & (~ (IData)(
                                                    (vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__ctr_seen_r[0U] 
                                                     >> 0x0aU)))))) {
        vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__any_w = 1U;
        vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__src_w = 7U;
        vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__src_if_w = 0U;
        vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__src_bit_w = 0x0aU;
    }
    if ((1U & (((~ (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__any_w)) 
                & (IData)((vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__ctr_pend_r[0U] 
                           >> 0x0bU))) & (~ (IData)(
                                                    (vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__ctr_seen_r[0U] 
                                                     >> 0x0bU)))))) {
        vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__any_w = 1U;
        vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__src_w = 7U;
        vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__src_if_w = 0U;
        vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__src_bit_w = 0x0bU;
    }
}

VL_ATTR_COLD void Vsim_sim___stl_sequent__TOP__sim__4(Vsim_sim* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+      Vsim_sim___stl_sequent__TOP__sim__4\n"); );
    Vsim__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Body
    if ((1U & (((~ (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__any_w)) 
                & (IData)((vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__ctr_pend_r[0U] 
                           >> 0x0cU))) & (~ (IData)(
                                                    (vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__ctr_seen_r[0U] 
                                                     >> 0x0cU)))))) {
        vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__any_w = 1U;
        vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__src_w = 7U;
        vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__src_if_w = 0U;
        vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__src_bit_w = 0x0cU;
    }
    if ((1U & (((~ (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__any_w)) 
                & (IData)((vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__ctr_pend_r[0U] 
                           >> 0x0dU))) & (~ (IData)(
                                                    (vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__ctr_seen_r[0U] 
                                                     >> 0x0dU)))))) {
        vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__any_w = 1U;
        vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__src_w = 7U;
        vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__src_if_w = 0U;
        vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__src_bit_w = 0x0dU;
    }
    if ((1U & (((~ (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__any_w)) 
                & (IData)((vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__ctr_pend_r[0U] 
                           >> 0x0eU))) & (~ (IData)(
                                                    (vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__ctr_seen_r[0U] 
                                                     >> 0x0eU)))))) {
        vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__any_w = 1U;
        vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__src_w = 7U;
        vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__src_if_w = 0U;
        vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__src_bit_w = 0x0eU;
    }
    if ((1U & (((~ (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__any_w)) 
                & (IData)((vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__ctr_pend_r[0U] 
                           >> 0x0fU))) & (~ (IData)(
                                                    (vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__ctr_seen_r[0U] 
                                                     >> 0x0fU)))))) {
        vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__any_w = 1U;
        vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__src_w = 7U;
        vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__src_if_w = 0U;
        vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__src_bit_w = 0x0fU;
    }
    if ((1U & (((~ (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__any_w)) 
                & (IData)((vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__ctr_pend_r[0U] 
                           >> 0x10U))) & (~ (IData)(
                                                    (vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__ctr_seen_r[0U] 
                                                     >> 0x10U)))))) {
        vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__any_w = 1U;
        vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__src_w = 7U;
        vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__src_if_w = 0U;
        vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__src_bit_w = 0x10U;
    }
    if ((1U & (((~ (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__any_w)) 
                & (IData)((vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__ctr_pend_r[0U] 
                           >> 0x11U))) & (~ (IData)(
                                                    (vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__ctr_seen_r[0U] 
                                                     >> 0x11U)))))) {
        vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__any_w = 1U;
        vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__src_w = 7U;
        vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__src_if_w = 0U;
        vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__src_bit_w = 0x11U;
    }
    if ((1U & (((~ (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__any_w)) 
                & (IData)((vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__ctr_pend_r[0U] 
                           >> 0x12U))) & (~ (IData)(
                                                    (vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__ctr_seen_r[0U] 
                                                     >> 0x12U)))))) {
        vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__any_w = 1U;
        vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__src_w = 7U;
        vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__src_if_w = 0U;
        vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__src_bit_w = 0x12U;
    }
    if ((1U & (((~ (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__any_w)) 
                & (IData)((vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__ctr_pend_r[0U] 
                           >> 0x13U))) & (~ (IData)(
                                                    (vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__ctr_seen_r[0U] 
                                                     >> 0x13U)))))) {
        vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__any_w = 1U;
        vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__src_w = 7U;
        vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__src_if_w = 0U;
        vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__src_bit_w = 0x13U;
    }
    if ((1U & (((~ (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__any_w)) 
                & (IData)((vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__ctr_pend_r[0U] 
                           >> 0x14U))) & (~ (IData)(
                                                    (vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__ctr_seen_r[0U] 
                                                     >> 0x14U)))))) {
        vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__any_w = 1U;
        vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__src_w = 7U;
        vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__src_if_w = 0U;
        vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__src_bit_w = 0x14U;
    }
    if ((1U & (((~ (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__any_w)) 
                & (IData)((vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__ctr_pend_r[0U] 
                           >> 0x15U))) & (~ (IData)(
                                                    (vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__ctr_seen_r[0U] 
                                                     >> 0x15U)))))) {
        vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__any_w = 1U;
        vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__src_w = 7U;
        vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__src_if_w = 0U;
        vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__src_bit_w = 0x15U;
    }
    if ((1U & (((~ (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__any_w)) 
                & (IData)((vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__ctr_pend_r[0U] 
                           >> 0x16U))) & (~ (IData)(
                                                    (vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__ctr_seen_r[0U] 
                                                     >> 0x16U)))))) {
        vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__any_w = 1U;
        vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__src_w = 7U;
        vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__src_if_w = 0U;
        vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__src_bit_w = 0x16U;
    }
    if ((1U & (((~ (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__any_w)) 
                & (IData)((vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__ctr_pend_r[0U] 
                           >> 0x17U))) & (~ (IData)(
                                                    (vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__ctr_seen_r[0U] 
                                                     >> 0x17U)))))) {
        vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__any_w = 1U;
        vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__src_w = 7U;
        vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__src_if_w = 0U;
        vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__src_bit_w = 0x17U;
    }
    if ((1U & (((~ (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__any_w)) 
                & (IData)((vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__ctr_pend_r[0U] 
                           >> 0x18U))) & (~ (IData)(
                                                    (vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__ctr_seen_r[0U] 
                                                     >> 0x18U)))))) {
        vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__any_w = 1U;
        vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__src_w = 7U;
        vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__src_if_w = 0U;
        vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__src_bit_w = 0x18U;
    }
    if ((1U & (((~ (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__any_w)) 
                & (IData)((vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__ctr_pend_r[0U] 
                           >> 0x19U))) & (~ (IData)(
                                                    (vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__ctr_seen_r[0U] 
                                                     >> 0x19U)))))) {
        vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__any_w = 1U;
        vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__src_w = 7U;
        vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__src_if_w = 0U;
        vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__src_bit_w = 0x19U;
    }
    if ((1U & (((~ (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__any_w)) 
                & (IData)((vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__ctr_pend_r[0U] 
                           >> 0x1aU))) & (~ (IData)(
                                                    (vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__ctr_seen_r[0U] 
                                                     >> 0x1aU)))))) {
        vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__any_w = 1U;
        vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__src_w = 7U;
        vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__src_if_w = 0U;
        vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__src_bit_w = 0x1aU;
    }
    if ((1U & (((~ (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__any_w)) 
                & (IData)((vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__ctr_pend_r[0U] 
                           >> 0x1bU))) & (~ (IData)(
                                                    (vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__ctr_seen_r[0U] 
                                                     >> 0x1bU)))))) {
        vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__any_w = 1U;
        vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__src_w = 7U;
        vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__src_if_w = 0U;
        vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__src_bit_w = 0x1bU;
    }
    if ((1U & (((~ (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__any_w)) 
                & (IData)((vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__ctr_pend_r[0U] 
                           >> 0x1cU))) & (~ (IData)(
                                                    (vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__ctr_seen_r[0U] 
                                                     >> 0x1cU)))))) {
        vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__any_w = 1U;
        vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__src_w = 7U;
        vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__src_if_w = 0U;
        vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__src_bit_w = 0x1cU;
    }
    if ((1U & (((~ (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__any_w)) 
                & (IData)((vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__ctr_pend_r[0U] 
                           >> 0x1dU))) & (~ (IData)(
                                                    (vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__ctr_seen_r[0U] 
                                                     >> 0x1dU)))))) {
        vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__any_w = 1U;
        vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__src_w = 7U;
        vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__src_if_w = 0U;
        vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__src_bit_w = 0x1dU;
    }
}

VL_ATTR_COLD void Vsim_sim___stl_sequent__TOP__sim__5(Vsim_sim* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+      Vsim_sim___stl_sequent__TOP__sim__5\n"); );
    Vsim__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Body
    if ((1U & (((~ (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__any_w)) 
                & (IData)((vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__ctr_pend_r[0U] 
                           >> 0x1eU))) & (~ (IData)(
                                                    (vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__ctr_seen_r[0U] 
                                                     >> 0x1eU)))))) {
        vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__any_w = 1U;
        vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__src_w = 7U;
        vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__src_if_w = 0U;
        vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__src_bit_w = 0x1eU;
    }
    if ((1U & (((~ (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__any_w)) 
                & (IData)((vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__ctr_pend_r[0U] 
                           >> 0x1fU))) & (~ (IData)(
                                                    (vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__ctr_seen_r[0U] 
                                                     >> 0x1fU)))))) {
        vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__any_w = 1U;
        vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__src_w = 7U;
        vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__src_if_w = 0U;
        vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__src_bit_w = 0x1fU;
    }
    if ((1U & (((~ (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__any_w)) 
                & (IData)((vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__ctr_pend_r[0U] 
                           >> 0x20U))) & (~ (IData)(
                                                    (vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__ctr_seen_r[0U] 
                                                     >> 0x20U)))))) {
        vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__any_w = 1U;
        vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__src_w = 7U;
        vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__src_if_w = 0U;
        vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__src_bit_w = 0x20U;
    }
    if ((1U & (((~ (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__any_w)) 
                & (IData)((vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__ctr_pend_r[0U] 
                           >> 0x21U))) & (~ (IData)(
                                                    (vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__ctr_seen_r[0U] 
                                                     >> 0x21U)))))) {
        vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__any_w = 1U;
        vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__src_w = 7U;
        vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__src_if_w = 0U;
        vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__src_bit_w = 0x21U;
    }
    if ((1U & (((~ (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__any_w)) 
                & (IData)((vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__ctr_pend_r[0U] 
                           >> 0x22U))) & (~ (IData)(
                                                    (vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__ctr_seen_r[0U] 
                                                     >> 0x22U)))))) {
        vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__any_w = 1U;
        vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__src_w = 7U;
        vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__src_if_w = 0U;
        vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__src_bit_w = 0x22U;
    }
    vlSelfRef.__PVT__soc_adapted_interface_we = 0U;
    vlSelfRef.__VdfgRegularize_h6e95ff9d_0_101 = (1U 
                                                  & (~ 
                                                     ((IData)(vlSelfRef.__PVT__KL_mbx_dma__DOT__hold_r) 
                                                      | (IData)(vlSelfRef.__PVT__KL_mbx_dma__DOT__cpu_wait_r))));
    vlSelfRef.__PVT__KL_mbx__DOT__tx_tail_w[0U] = (IData)(
                                                          (((QData)((IData)(
                                                                            (((IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_tx__DOT__tail_r[3U]) 
                                                                              << 0x00000010U) 
                                                                             | vlSelfRef.__PVT__KL_mbx__DOT__u_tx__DOT__tail_r[2U]))) 
                                                            << 0x00000020U) 
                                                           | (QData)((IData)(
                                                                             (((IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_tx__DOT__tail_r[1U]) 
                                                                               << 0x00000010U) 
                                                                              | vlSelfRef.__PVT__KL_mbx__DOT__u_tx__DOT__tail_r[0U])))));
    vlSelfRef.__PVT__KL_mbx__DOT__tx_tail_w[1U] = (IData)(
                                                          ((((QData)((IData)(
                                                                             (((IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_tx__DOT__tail_r[3U]) 
                                                                               << 0x00000010U) 
                                                                              | vlSelfRef.__PVT__KL_mbx__DOT__u_tx__DOT__tail_r[2U]))) 
                                                             << 0x00000020U) 
                                                            | (QData)((IData)(
                                                                              (((IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_tx__DOT__tail_r[1U]) 
                                                                                << 0x00000010U) 
                                                                               | vlSelfRef.__PVT__KL_mbx__DOT__u_tx__DOT__tail_r[0U])))) 
                                                           >> 0x00000020U));
    vlSelfRef.__PVT__KL_mbx__DOT__tx_tail_w[2U] = (0x0000ffffU 
                                                   & vlSelfRef.__PVT__KL_mbx__DOT__u_tx__DOT__tail_r[4U]);
    vlSelfRef.__PVT__KL_mbx__DOT__tx_err_w[0U] = (IData)(
                                                         (((QData)((IData)(
                                                                           (((IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_tx__DOT__err_r[3U]) 
                                                                             << 0x00000010U) 
                                                                            | vlSelfRef.__PVT__KL_mbx__DOT__u_tx__DOT__err_r[2U]))) 
                                                           << 0x00000020U) 
                                                          | (QData)((IData)(
                                                                            (((IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_tx__DOT__err_r[1U]) 
                                                                              << 0x00000010U) 
                                                                             | vlSelfRef.__PVT__KL_mbx__DOT__u_tx__DOT__err_r[0U])))));
    vlSelfRef.__PVT__KL_mbx__DOT__tx_err_w[1U] = (IData)(
                                                         ((((QData)((IData)(
                                                                            (((IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_tx__DOT__err_r[3U]) 
                                                                              << 0x00000010U) 
                                                                             | vlSelfRef.__PVT__KL_mbx__DOT__u_tx__DOT__err_r[2U]))) 
                                                            << 0x00000020U) 
                                                           | (QData)((IData)(
                                                                             (((IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_tx__DOT__err_r[1U]) 
                                                                               << 0x00000010U) 
                                                                              | vlSelfRef.__PVT__KL_mbx__DOT__u_tx__DOT__err_r[0U])))) 
                                                          >> 0x00000020U));
    vlSelfRef.__PVT__KL_mbx__DOT__tx_err_w[2U] = (0x0000ffffU 
                                                  & vlSelfRef.__PVT__KL_mbx__DOT__u_tx__DOT__err_r[4U]);
    vlSelfRef.__PVT__KL_mbx__DOT__rx_head_w[0U] = (IData)(
                                                          (((QData)((IData)(
                                                                            (((IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__head_pub_r[3U]) 
                                                                              << 0x00000010U) 
                                                                             | vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__head_pub_r[2U]))) 
                                                            << 0x00000020U) 
                                                           | (QData)((IData)(
                                                                             (((IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__head_pub_r[1U]) 
                                                                               << 0x00000010U) 
                                                                              | vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__head_pub_r[0U])))));
    vlSelfRef.__PVT__KL_mbx__DOT__rx_head_w[1U] = (IData)(
                                                          ((((QData)((IData)(
                                                                             (((IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__head_pub_r[3U]) 
                                                                               << 0x00000010U) 
                                                                              | vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__head_pub_r[2U]))) 
                                                             << 0x00000020U) 
                                                            | (QData)((IData)(
                                                                              (((IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__head_pub_r[1U]) 
                                                                                << 0x00000010U) 
                                                                               | vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__head_pub_r[0U])))) 
                                                           >> 0x00000020U));
    vlSelfRef.__PVT__KL_mbx__DOT__rx_head_w[2U] = (0x0000ffffU 
                                                   & vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__head_pub_r[4U]);
    vlSelfRef.__PVT__KL_mbx__DOT__rx_drop_w[0U] = (IData)(
                                                          (((QData)((IData)(
                                                                            (((IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__drop_r[3U]) 
                                                                              << 0x00000010U) 
                                                                             | vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__drop_r[2U]))) 
                                                            << 0x00000020U) 
                                                           | (QData)((IData)(
                                                                             (((IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__drop_r[1U]) 
                                                                               << 0x00000010U) 
                                                                              | vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__drop_r[0U])))));
    vlSelfRef.__PVT__KL_mbx__DOT__rx_drop_w[1U] = (IData)(
                                                          ((((QData)((IData)(
                                                                             (((IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__drop_r[3U]) 
                                                                               << 0x00000010U) 
                                                                              | vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__drop_r[2U]))) 
                                                             << 0x00000020U) 
                                                            | (QData)((IData)(
                                                                              (((IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__drop_r[1U]) 
                                                                                << 0x00000010U) 
                                                                               | vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__drop_r[0U])))) 
                                                           >> 0x00000020U));
    vlSelfRef.__PVT__KL_mbx__DOT__rx_drop_w[2U] = (0x0000ffffU 
                                                   & vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__drop_r[4U]);
    vlSelfRef.__PVT__KL_mbx__DOT__rate_drop_w[0U] = (IData)(
                                                            (((QData)((IData)(
                                                                              (((IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__rate_drop_r[3U]) 
                                                                                << 0x00000010U) 
                                                                               | vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__rate_drop_r[2U]))) 
                                                              << 0x00000020U) 
                                                             | (QData)((IData)(
                                                                               (((IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__rate_drop_r[1U]) 
                                                                                << 0x00000010U) 
                                                                                | vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__rate_drop_r[0U])))));
    vlSelfRef.__PVT__KL_mbx__DOT__rate_drop_w[1U] = (IData)(
                                                            ((((QData)((IData)(
                                                                               (((IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__rate_drop_r[3U]) 
                                                                                << 0x00000010U) 
                                                                                | vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__rate_drop_r[2U]))) 
                                                               << 0x00000020U) 
                                                              | (QData)((IData)(
                                                                                (((IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__rate_drop_r[1U]) 
                                                                                << 0x00000010U) 
                                                                                | vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__rate_drop_r[0U])))) 
                                                             >> 0x00000020U));
    vlSelfRef.__PVT__KL_mbx__DOT__rate_drop_w[2U] = 
        (0x0000ffffU & vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__rate_drop_r[4U]);
    vlSelfRef.__PVT__KL_mbx__DOT__rx_pass_w[0U] = (IData)(
                                                          (((QData)((IData)(
                                                                            (((IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__pass_r[3U]) 
                                                                              << 0x00000010U) 
                                                                             | vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__pass_r[2U]))) 
                                                            << 0x00000020U) 
                                                           | (QData)((IData)(
                                                                             (((IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__pass_r[1U]) 
                                                                               << 0x00000010U) 
                                                                              | vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__pass_r[0U])))));
    vlSelfRef.__PVT__KL_mbx__DOT__rx_pass_w[1U] = (IData)(
                                                          ((((QData)((IData)(
                                                                             (((IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__pass_r[3U]) 
                                                                               << 0x00000010U) 
                                                                              | vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__pass_r[2U]))) 
                                                             << 0x00000020U) 
                                                            | (QData)((IData)(
                                                                              (((IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__pass_r[1U]) 
                                                                                << 0x00000010U) 
                                                                               | vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__pass_r[0U])))) 
                                                           >> 0x00000020U));
    vlSelfRef.__PVT__KL_mbx__DOT__rx_pass_w[2U] = (0x0000ffffU 
                                                   & vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__pass_r[4U]);
    vlSelfRef.__PVT__KL_mbx_dma__DOT__mover_w = (1U 
                                                 & (~ 
                                                    ((IData)(vlSelfRef.__PVT__KL_mbx_dma__DOT__cpu_wait_r) 
                                                     | (0U 
                                                        == (IData)(vlSelfRef.__PVT__KL_mbx_dma__DOT__state_r)))));
    vlSelfRef.__PVT__KL_mbx__DOT__rd_bound_decode__DOT__rel 
        = (0x00007fffU & ((IData)(vlSelfRef.__PVT__KL_mbx__DOT__rd_off_r) 
                          - (IData)(0x0200U)));
    vlSelfRef.__PVT__KL_mbx__DOT__rd_bound_decode__DOT__in_entry 
        = (0x000fU & (IData)(vlSelfRef.__PVT__KL_mbx__DOT__rd_bound_decode__DOT__rel));
    vlSelfRef.__PVT__KL_mbx__DOT__rd_bound_decode__DOT__entry 
        = (0x000fU & ((IData)(vlSelfRef.__PVT__KL_mbx__DOT__rd_bound_decode__DOT__rel) 
                      >> 4U));
    vlSelfRef.__PVT__KL_mbx__DOT__rd_bnd_reg_w = 0U;
    if ((4U == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__rd_bound_decode__DOT__in_entry))) {
        vlSelfRef.__PVT__KL_mbx__DOT__rd_bnd_reg_w = 1U;
    }
    if ((8U == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__rd_bound_decode__DOT__in_entry))) {
        vlSelfRef.__PVT__KL_mbx__DOT__rd_bnd_reg_w = 2U;
    }
    vlSelfRef.__PVT__KL_mbx__DOT__rd_bnd_at_w = (((
                                                   (0x0200U 
                                                    <= (IData)(vlSelfRef.__PVT__KL_mbx__DOT__rd_off_r)) 
                                                   & (1U 
                                                      > 
                                                      ((IData)(vlSelfRef.__PVT__KL_mbx__DOT__rd_bound_decode__DOT__rel) 
                                                       >> 8U))) 
                                                  & (0x0010U 
                                                     > (IData)(vlSelfRef.__PVT__KL_mbx__DOT__rd_bound_decode__DOT__entry))) 
                                                 & (((0U 
                                                      == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__rd_bound_decode__DOT__in_entry)) 
                                                     | (4U 
                                                        == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__rd_bound_decode__DOT__in_entry))) 
                                                    | (8U 
                                                       == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__rd_bound_decode__DOT__in_entry))));
    vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__rb_a_w 
        = (0x0000001fU & ((IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__hrd_r)
                           ? (VL_MULS_III(32, (IData)(2U), (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__hrk_r)) 
                              + (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__hrhi_r))
                           : (VL_MULS_III(32, (IData)(2U), (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__cp_k_r)) 
                              + (1U & ((IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__cp_b_r) 
                                       >> 2U)))));
    vlSelfRef.__PVT__soc_vexiiriscv_pbus_r_valid = 0U;
    if ((1U & (~ ((IData)(vlSelfRef.__PVT__builder_state) 
                  >> 2U)))) {
        if ((2U & (IData)(vlSelfRef.__PVT__builder_state))) {
            if ((1U & (IData)(vlSelfRef.__PVT__builder_state))) {
                vlSelfRef.__PVT__soc_adapted_interface_we = 1U;
            }
            if ((1U & (~ (IData)(vlSelfRef.__PVT__builder_state)))) {
                vlSelfRef.__PVT__soc_vexiiriscv_pbus_r_valid = 1U;
            }
        }
    }
    vlSelfRef.__PVT__soc_vexiiriscv_pbus_b_valid = 0U;
    if ((4U & (IData)(vlSelfRef.__PVT__builder_state))) {
        if ((1U & (~ ((IData)(vlSelfRef.__PVT__builder_state) 
                      >> 1U)))) {
            if ((1U & (~ (IData)(vlSelfRef.__PVT__builder_state)))) {
                vlSelfRef.__PVT__soc_vexiiriscv_pbus_b_valid = 1U;
            }
        }
    }
    vlSelfRef.__PVT__KL_mbx__DOT__rd_face_decode__DOT__rel 
        = (0x00007fffU & ((IData)(vlSelfRef.__PVT__KL_mbx__DOT__rd_off_r) 
                          - (IData)(0x6000U)));
    vlSelfRef.__PVT__KL_mbx__DOT__rd_face_decode__DOT__in_if 
        = (0x03ffU & (IData)(vlSelfRef.__PVT__KL_mbx__DOT__rd_face_decode__DOT__rel));
    vlSelfRef.__PVT__KL_mbx__DOT__rd_face_if_w = (1U 
                                                  & ((IData)(vlSelfRef.__PVT__KL_mbx__DOT__rd_face_decode__DOT__rel) 
                                                     >> 0x0000000aU));
    vlSelfRef.__PVT__KL_mbx__DOT__rd_face_area_w = 
        ((0x0200U <= (IData)(vlSelfRef.__PVT__KL_mbx__DOT__rd_face_decode__DOT__in_if))
          ? 2U : ((0x0100U <= (IData)(vlSelfRef.__PVT__KL_mbx__DOT__rd_face_decode__DOT__in_if))
                   ? 1U : 0U));
    if ((2U == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__rd_face_area_w))) {
        vlSelfRef.__PVT__KL_mbx__DOT__rd_face_decode__DOT__entry 
            = (0x000007ffU & (((IData)(vlSelfRef.__PVT__KL_mbx__DOT__rd_face_decode__DOT__in_if) 
                               - (IData)(0x0200U)) 
                              >> 4U));
        vlSelfRef.__PVT__KL_mbx__DOT__rd_face_reg_w 
            = (0x000fU & ((IData)(vlSelfRef.__PVT__KL_mbx__DOT__rd_face_decode__DOT__in_if) 
                          - (IData)(0x0200U)));
    } else {
        vlSelfRef.__PVT__KL_mbx__DOT__rd_face_decode__DOT__entry 
            = (0x000007ffU & (((IData)(vlSelfRef.__PVT__KL_mbx__DOT__rd_face_decode__DOT__in_if) 
                               - (IData)(0x0100U)) 
                              >> 4U));
        vlSelfRef.__PVT__KL_mbx__DOT__rd_face_reg_w 
            = ((1U == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__rd_face_area_w))
                ? (0x000fU & ((IData)(vlSelfRef.__PVT__KL_mbx__DOT__rd_face_decode__DOT__in_if) 
                              - (IData)(0x0100U))) : (IData)(vlSelfRef.__PVT__KL_mbx__DOT__rd_face_decode__DOT__in_if));
    }
    vlSelfRef.__PVT__KL_mbx__DOT__rd_face_s_w = (0x0000000fU 
                                                 & (IData)(vlSelfRef.__PVT__KL_mbx__DOT__rd_face_decode__DOT__entry));
    vlSelfRef.__PVT__KL_mbx__DOT__rd_face_k_w = (0x0000000fU 
                                                 & (IData)(vlSelfRef.__PVT__KL_mbx__DOT__rd_face_decode__DOT__entry));
}

VL_ATTR_COLD void Vsim_sim___stl_sequent__TOP__sim__6(Vsim_sim* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+      Vsim_sim___stl_sequent__TOP__sim__6\n"); );
    Vsim__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Locals
    CData/*7:0*/ __PVT__builder_litespi_tx_mux_source_payload_mask;
    __PVT__builder_litespi_tx_mux_source_payload_mask = 0;
    // Body
    vlSelfRef.__PVT__KL_mbx__DOT__rd_face_at_w = ((
                                                   (0x6000U 
                                                    <= (IData)(vlSelfRef.__PVT__KL_mbx__DOT__rd_off_r)) 
                                                   & (1U 
                                                      > 
                                                      ((IData)(vlSelfRef.__PVT__KL_mbx__DOT__rd_face_decode__DOT__rel) 
                                                       >> 0x0000000aU))) 
                                                  & ((((0U 
                                                        == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__rd_face_area_w)) 
                                                       & (((((((((((((((((((((((((((((((((((((0U 
                                                                                == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__rd_face_reg_w)) 
                                                                                | (4U 
                                                                                == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__rd_face_reg_w))) 
                                                                                | (8U 
                                                                                == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__rd_face_reg_w))) 
                                                                                | (0x000cU 
                                                                                == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__rd_face_reg_w))) 
                                                                                | (0x0010U 
                                                                                == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__rd_face_reg_w))) 
                                                                                | (0x0014U 
                                                                                == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__rd_face_reg_w))) 
                                                                                | (0x0018U 
                                                                                == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__rd_face_reg_w))) 
                                                                                | (0x001cU 
                                                                                == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__rd_face_reg_w))) 
                                                                                | (0x0040U 
                                                                                == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__rd_face_reg_w))) 
                                                                                | (0x0044U 
                                                                                == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__rd_face_reg_w))) 
                                                                                | (0x0048U 
                                                                                == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__rd_face_reg_w))) 
                                                                                | (0x004cU 
                                                                                == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__rd_face_reg_w))) 
                                                                                | (0x0050U 
                                                                                == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__rd_face_reg_w))) 
                                                                                | (0x0060U 
                                                                                == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__rd_face_reg_w))) 
                                                                                | (0x0064U 
                                                                                == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__rd_face_reg_w))) 
                                                                               | (0x0068U 
                                                                                == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__rd_face_reg_w))) 
                                                                              | (0x006cU 
                                                                                == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__rd_face_reg_w))) 
                                                                             | (0x0070U 
                                                                                == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__rd_face_reg_w))) 
                                                                            | (0x0074U 
                                                                               == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__rd_face_reg_w))) 
                                                                           | (0x0080U 
                                                                              == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__rd_face_reg_w))) 
                                                                          | (0x0084U 
                                                                             == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__rd_face_reg_w))) 
                                                                         | (0x0088U 
                                                                            == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__rd_face_reg_w))) 
                                                                        | (0x008cU 
                                                                           == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__rd_face_reg_w))) 
                                                                       | (0x0090U 
                                                                          == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__rd_face_reg_w))) 
                                                                      | (0x0094U 
                                                                         == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__rd_face_reg_w))) 
                                                                     | (0x0098U 
                                                                        == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__rd_face_reg_w))) 
                                                                    | (0x009cU 
                                                                       == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__rd_face_reg_w))) 
                                                                   | (0x00a0U 
                                                                      == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__rd_face_reg_w))) 
                                                                  | (0x00a4U 
                                                                     == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__rd_face_reg_w))) 
                                                                 | (0x00c0U 
                                                                    == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__rd_face_reg_w))) 
                                                                | (0x00c4U 
                                                                   == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__rd_face_reg_w))) 
                                                               | (0x00c8U 
                                                                  == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__rd_face_reg_w))) 
                                                              | (0x00ccU 
                                                                 == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__rd_face_reg_w))) 
                                                             | (0x00d0U 
                                                                == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__rd_face_reg_w))) 
                                                            | (0x00d4U 
                                                               == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__rd_face_reg_w))) 
                                                           | (0x00d8U 
                                                              == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__rd_face_reg_w))) 
                                                          | (0x00dcU 
                                                             == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__rd_face_reg_w)))) 
                                                      | (((1U 
                                                           == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__rd_face_area_w)) 
                                                          & (0x0010U 
                                                             > (IData)(vlSelfRef.__PVT__KL_mbx__DOT__rd_face_decode__DOT__entry))) 
                                                         & ((((0U 
                                                               == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__rd_face_reg_w)) 
                                                              | (4U 
                                                                 == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__rd_face_reg_w))) 
                                                             | (8U 
                                                                == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__rd_face_reg_w))) 
                                                            | (0x000cU 
                                                               == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__rd_face_reg_w))))) 
                                                     | (((2U 
                                                          == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__rd_face_area_w)) 
                                                         & (0x0010U 
                                                            > (IData)(vlSelfRef.__PVT__KL_mbx__DOT__rd_face_decode__DOT__entry))) 
                                                        & (((0U 
                                                             == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__rd_face_reg_w)) 
                                                            | (4U 
                                                               == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__rd_face_reg_w))) 
                                                           | (8U 
                                                              == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__rd_face_reg_w))))));
    vlSelfRef.__PVT__KL_mbx__DOT__rd_pub_decode__DOT__rel 
        = (0x00007fffU & ((IData)(vlSelfRef.__PVT__KL_mbx__DOT__rd_off_r) 
                          - (IData)(0x0800U)));
    vlSelfRef.__PVT__KL_mbx__DOT__rd_pub_decode__DOT__in_if 
        = (0x01ffU & (IData)(vlSelfRef.__PVT__KL_mbx__DOT__rd_pub_decode__DOT__rel));
    vlSelfRef.__PVT__KL_mbx__DOT__rd_pub_decode__DOT__in_srcs 
        = (0x00007fffU & ((IData)(vlSelfRef.__PVT__KL_mbx__DOT__rd_pub_decode__DOT__in_if) 
                          - (IData)(0x0080U)));
    vlSelfRef.__PVT__KL_mbx__DOT__rd_pub_decode__DOT__in_sinks 
        = (0x00007fffU & ((IData)(vlSelfRef.__PVT__KL_mbx__DOT__rd_pub_decode__DOT__in_if) 
                          - (IData)(0x0100U)));
    vlSelfRef.__PVT__KL_mbx__DOT__rd_pub_decode__DOT__src_entry 
        = ((IData)(vlSelfRef.__PVT__KL_mbx__DOT__rd_pub_decode__DOT__in_srcs) 
           >> 3U);
    vlSelfRef.__PVT__KL_mbx__DOT__rd_pub_decode__DOT__entry 
        = ((IData)(vlSelfRef.__PVT__KL_mbx__DOT__rd_pub_decode__DOT__in_sinks) 
           >> 4U);
    vlSelfRef.__PVT__KL_mbx__DOT__rd_pub_if_w = (1U 
                                                 & ((IData)(vlSelfRef.__PVT__KL_mbx__DOT__rd_pub_decode__DOT__rel) 
                                                    >> 9U));
    vlSelfRef.__PVT__KL_mbx__DOT__rd_pub_sink_w = (0x0100U 
                                                   <= (IData)(vlSelfRef.__PVT__KL_mbx__DOT__rd_pub_decode__DOT__in_if));
    vlSelfRef.__PVT__KL_mbx__DOT__rd_pub_src_w = ((~ (IData)(vlSelfRef.__PVT__KL_mbx__DOT__rd_pub_sink_w)) 
                                                  & (0x0080U 
                                                     <= (IData)(vlSelfRef.__PVT__KL_mbx__DOT__rd_pub_decode__DOT__in_if)));
    vlSelfRef.__PVT__KL_mbx__DOT__rd_pub_s_w = (0x0000000fU 
                                                & (IData)(vlSelfRef.__PVT__KL_mbx__DOT__rd_pub_decode__DOT__src_entry));
    vlSelfRef.__PVT__KL_mbx__DOT__rd_pub_k_w = (0x0000000fU 
                                                & (IData)(vlSelfRef.__PVT__KL_mbx__DOT__rd_pub_decode__DOT__entry));
    vlSelfRef.__PVT__KL_mbx__DOT__rd_pub_reg_w = ((IData)(vlSelfRef.__PVT__KL_mbx__DOT__rd_pub_sink_w)
                                                   ? 
                                                  (0x000fU 
                                                   & (IData)(vlSelfRef.__PVT__KL_mbx__DOT__rd_pub_decode__DOT__in_sinks))
                                                   : 
                                                  ((IData)(vlSelfRef.__PVT__KL_mbx__DOT__rd_pub_src_w)
                                                    ? 
                                                   (7U 
                                                    & (IData)(vlSelfRef.__PVT__KL_mbx__DOT__rd_pub_decode__DOT__in_srcs))
                                                    : (IData)(vlSelfRef.__PVT__KL_mbx__DOT__rd_pub_decode__DOT__in_if)));
    vlSelfRef.__PVT__KL_mbx__DOT__rd_pub_at_w = (((0x0800U 
                                                   <= (IData)(vlSelfRef.__PVT__KL_mbx__DOT__rd_off_r)) 
                                                  & (1U 
                                                     > 
                                                     ((IData)(vlSelfRef.__PVT__KL_mbx__DOT__rd_pub_decode__DOT__rel) 
                                                      >> 9U))) 
                                                 & ((IData)(vlSelfRef.__PVT__KL_mbx__DOT__rd_pub_sink_w)
                                                     ? 
                                                    ((0x0010U 
                                                      > (IData)(vlSelfRef.__PVT__KL_mbx__DOT__rd_pub_decode__DOT__entry)) 
                                                     & (((0U 
                                                          == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__rd_pub_reg_w)) 
                                                         | (4U 
                                                            == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__rd_pub_reg_w))) 
                                                        | (8U 
                                                           == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__rd_pub_reg_w))))
                                                     : 
                                                    ((IData)(vlSelfRef.__PVT__KL_mbx__DOT__rd_pub_src_w)
                                                      ? 
                                                     ((0x0010U 
                                                       > (IData)(vlSelfRef.__PVT__KL_mbx__DOT__rd_pub_decode__DOT__src_entry)) 
                                                      & ((0U 
                                                          == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__rd_pub_reg_w)) 
                                                         | (4U 
                                                            == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__rd_pub_reg_w))))
                                                      : 
                                                     (((((0U 
                                                          == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__rd_pub_reg_w)) 
                                                         | (4U 
                                                            == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__rd_pub_reg_w))) 
                                                        | (8U 
                                                           == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__rd_pub_reg_w))) 
                                                       | (0x000cU 
                                                          == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__rd_pub_reg_w))) 
                                                      | (0x0010U 
                                                         == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__rd_pub_reg_w))))));
    vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__take_w 
        = ((IData)(vlSymsp->TOP.mbx_rx_valid) & (IData)(vlSymsp->TOP.mbx_rx_ready));
    if (vlSelfRef.__PVT__builder_litespi_grant) {
        vlSelfRef.__PVT__builder_litespi_tx_mux_source_valid 
            = vlSelfRef.__PVT__add_devices_master_tx_fifo_pipe_valid_source_valid;
        vlSelfRef.__PVT__builder_litespi_tx_mux_source_payload_width 
            = vlSelfRef.__PVT__add_devices_master_tx_fifo_pipe_valid_source_payload_width;
        __PVT__builder_litespi_tx_mux_source_payload_mask 
            = vlSelfRef.__PVT__add_devices_master_tx_fifo_pipe_valid_source_payload_mask;
        vlSelfRef.__PVT__builder_litespi_tx_mux_source_payload_len 
            = vlSelfRef.__PVT__add_devices_master_tx_fifo_pipe_valid_source_payload_len;
    } else {
        vlSelfRef.__PVT__builder_litespi_tx_mux_source_valid 
            = vlSelfRef.__PVT__add_devices_mmap_source_valid;
        vlSelfRef.__PVT__builder_litespi_tx_mux_source_payload_width 
            = vlSelfRef.__PVT__add_devices_mmap_source_payload_width;
        __PVT__builder_litespi_tx_mux_source_payload_mask 
            = vlSelfRef.__PVT__add_devices_mmap_source_payload_mask;
        vlSelfRef.__PVT__builder_litespi_tx_mux_source_payload_len 
            = vlSelfRef.__PVT__add_devices_mmap_source_payload_len;
    }
    vlSelfRef.__PVT__soc_rx_fifo_do_read = (((~ (IData)(vlSelfRef.__PVT__soc_rx_fifo_readable)) 
                                             | (IData)(vlSelfRef.__PVT__soc_rx_clear)) 
                                            & (0U != (IData)(vlSelfRef.__PVT__soc_rx_fifo_level0)));
    vlSelfRef.__PVT__soc_status_status = vlSelfRef.__VdfgRegularize_h6e95ff9d_0_107;
    vlSelfRef.__PVT__soc_pending_status = vlSelfRef.__VdfgRegularize_h6e95ff9d_0_107;
    vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__classify__DOT__ethertype 
        = (((IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__b12_r) 
            << 8U) | (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__b13_r));
    vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__classify__DOT__subtype 
        = ((0x000eU == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__cnt_r))
            ? (IData)(vlSymsp->TOP.mbx_rx_data) : (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__sub_r));
    vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__classify__DOT__msg 
        = ((0x000fU == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__cnt_r))
            ? (0x0000000fU & (IData)(vlSymsp->TOP.mbx_rx_data))
            : 0U);
    vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__cls_hit_w = 0U;
    vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__cls_ch_w = 0U;
    vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__ctrl_et_w = 0U;
    vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__classify__DOT__unnamedblk9__DOT__unnamedblk10__DOT__dst_ok 
        = (0x000091e0f0010000ULL == vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__dst_r);
    if ((0x22f0U == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__classify__DOT__ethertype))) {
        vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__ctrl_et_w = 1U;
        vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__ctrl_et_w = 1U;
    }
    if (((((IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__classify__DOT__unnamedblk9__DOT__unnamedblk10__DOT__dst_ok) 
           & (0x22f0U == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__classify__DOT__ethertype))) 
          & (0xfaU == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__classify__DOT__subtype))) 
         & (0x0000ffffU >> (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__classify__DOT__msg)))) {
        vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__cls_hit_w = 1U;
        vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__cls_ch_w = 0U;
    }
    vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__classify__DOT__unnamedblk9__DOT__unnamedblk10__DOT__dst_ok 
        = (0x000091e0f0010000ULL == vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__dst_r);
    if ((((((~ (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__cls_hit_w)) 
            & (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__classify__DOT__unnamedblk9__DOT__unnamedblk10__DOT__dst_ok)) 
           & (0x22f0U == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__classify__DOT__ethertype))) 
          & (0xfcU == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__classify__DOT__subtype))) 
         & (0x0000ffffU >> (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__classify__DOT__msg)))) {
        vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__cls_hit_w = 1U;
        vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__cls_ch_w = 1U;
    }
}
