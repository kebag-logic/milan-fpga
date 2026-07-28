// Verilated -*- C++ -*-
// DESCRIPTION: Verilator output: Model implementation (design independent parts)

#include "Vmilan_datapath__pch.h"

//============================================================
// Constructors

Vmilan_datapath::Vmilan_datapath(VerilatedContext* _vcontextp__, const char* _vcname__)
    : VerilatedModel{*_vcontextp__}
    , vlSymsp{new Vmilan_datapath__Syms(contextp(), _vcname__, this)}
    , axis_clk{vlSymsp->TOP.axis_clk}
    , clk_audio_i{vlSymsp->TOP.clk_audio_i}
    , clk_tdm_i{vlSymsp->TOP.clk_tdm_i}
    , axis_resetn{vlSymsp->TOP.axis_resetn}
    , gtx_clk{vlSymsp->TOP.gtx_clk}
    , tdm_bclk_i{vlSymsp->TOP.tdm_bclk_i}
    , i_ps_clk{vlSymsp->TOP.i_ps_clk}
    , gtx_resetn{vlSymsp->TOP.gtx_resetn}
    , s_axi_awvalid{vlSymsp->TOP.s_axi_awvalid}
    , s_axi_awready{vlSymsp->TOP.s_axi_awready}
    , s_axi_wstrb{vlSymsp->TOP.s_axi_wstrb}
    , s_axi_wvalid{vlSymsp->TOP.s_axi_wvalid}
    , s_axi_wready{vlSymsp->TOP.s_axi_wready}
    , s_axi_bresp{vlSymsp->TOP.s_axi_bresp}
    , s_axi_bvalid{vlSymsp->TOP.s_axi_bvalid}
    , s_axi_bready{vlSymsp->TOP.s_axi_bready}
    , s_axi_arvalid{vlSymsp->TOP.s_axi_arvalid}
    , s_axi_arready{vlSymsp->TOP.s_axi_arready}
    , s_axi_rresp{vlSymsp->TOP.s_axi_rresp}
    , s_axi_rvalid{vlSymsp->TOP.s_axi_rvalid}
    , s_axi_rready{vlSymsp->TOP.s_axi_rready}
    , i2s_mclk_o{vlSymsp->TOP.i2s_mclk_o}
    , i2s_sclk_o{vlSymsp->TOP.i2s_sclk_o}
    , i2s_lrck_o{vlSymsp->TOP.i2s_lrck_o}
    , i2s_sdout_i{vlSymsp->TOP.i2s_sdout_i}
    , tdm_fsync_i{vlSymsp->TOP.tdm_fsync_i}
    , tdm_bclk_o{vlSymsp->TOP.tdm_bclk_o}
    , tdm_fsync_o{vlSymsp->TOP.tdm_fsync_o}
    , tdm_dout_o{vlSymsp->TOP.tdm_dout_o}
    , tdm_data_i{vlSymsp->TOP.tdm_data_i}
    , i2s_dac_mclk_o{vlSymsp->TOP.i2s_dac_mclk_o}
    , i2s_dac_sclk_o{vlSymsp->TOP.i2s_dac_sclk_o}
    , i2s_dac_lrck_o{vlSymsp->TOP.i2s_dac_lrck_o}
    , i2s_dac_sdin_o{vlSymsp->TOP.i2s_dac_sdin_o}
    , s_axis_tx_tkeep{vlSymsp->TOP.s_axis_tx_tkeep}
    , s_axis_tx_tvalid{vlSymsp->TOP.s_axis_tx_tvalid}
    , s_axis_tx_tlast{vlSymsp->TOP.s_axis_tx_tlast}
    , s_axis_tx_tready{vlSymsp->TOP.s_axis_tx_tready}
    , m_axis_rx_tkeep{vlSymsp->TOP.m_axis_rx_tkeep}
    , m_axis_rx_tvalid{vlSymsp->TOP.m_axis_rx_tvalid}
    , m_axis_rx_tlast{vlSymsp->TOP.m_axis_rx_tlast}
    , m_axis_rx_tready{vlSymsp->TOP.m_axis_rx_tready}
    , m_axis_ts_tkeep{vlSymsp->TOP.m_axis_ts_tkeep}
    , m_axis_ts_tvalid{vlSymsp->TOP.m_axis_ts_tvalid}
    , m_axis_ts_tlast{vlSymsp->TOP.m_axis_ts_tlast}
    , m_axis_ts_tready{vlSymsp->TOP.m_axis_ts_tready}
    , m_axis_pcm_tkeep{vlSymsp->TOP.m_axis_pcm_tkeep}
    , m_axis_pcm_tvalid{vlSymsp->TOP.m_axis_pcm_tvalid}
    , m_axis_pcm_tlast{vlSymsp->TOP.m_axis_pcm_tlast}
    , m_axis_pcm_tuser{vlSymsp->TOP.m_axis_pcm_tuser}
    , m_axis_pcm_tready{vlSymsp->TOP.m_axis_pcm_tready}
    , m_axis_mac_tx_tkeep{vlSymsp->TOP.m_axis_mac_tx_tkeep}
    , m_axis_mac_tx_tvalid{vlSymsp->TOP.m_axis_mac_tx_tvalid}
    , m_axis_mac_tx_tlast{vlSymsp->TOP.m_axis_mac_tx_tlast}
    , m_axis_mac_tx_tready{vlSymsp->TOP.m_axis_mac_tx_tready}
    , s_axis_mac_rx_tkeep{vlSymsp->TOP.s_axis_mac_rx_tkeep}
    , s_axis_mac_rx_tvalid{vlSymsp->TOP.s_axis_mac_rx_tvalid}
    , s_axis_mac_rx_tlast{vlSymsp->TOP.s_axis_mac_rx_tlast}
    , s_axis_mac_rx_tready{vlSymsp->TOP.s_axis_mac_rx_tready}
    , o_mac_tx_en{vlSymsp->TOP.o_mac_tx_en}
    , o_mac_rx_en{vlSymsp->TOP.o_mac_rx_en}
    , o_mac_promisc{vlSymsp->TOP.o_mac_promisc}
    , o_mac_allmulti{vlSymsp->TOP.o_mac_allmulti}
    , o_mac_is_1g{vlSymsp->TOP.o_mac_is_1g}
    , o_mac_ifg{vlSymsp->TOP.o_mac_ifg}
    , o_phy_reset_n{vlSymsp->TOP.o_phy_reset_n}
    , i_mac_speed{vlSymsp->TOP.i_mac_speed}
    , i_link_up{vlSymsp->TOP.i_link_up}
    , o_mac_reinit{vlSymsp->TOP.o_mac_reinit}
    , o_eth_rst{vlSymsp->TOP.o_eth_rst}
    , i_full_duplex{vlSymsp->TOP.i_full_duplex}
    , i_ethrx_tgl{vlSymsp->TOP.i_ethrx_tgl}
    , i_ethtx_tgl{vlSymsp->TOP.i_ethtx_tgl}
    , i_ethact_tgl{vlSymsp->TOP.i_ethact_tgl}
    , o_irq_csr{vlSymsp->TOP.o_irq_csr}
    , o_identify{vlSymsp->TOP.o_identify}
    , o_mmcm_drp_addr{vlSymsp->TOP.o_mmcm_drp_addr}
    , o_mmcm_drp_en{vlSymsp->TOP.o_mmcm_drp_en}
    , o_mmcm_drp_we{vlSymsp->TOP.o_mmcm_drp_we}
    , i_mmcm_drp_rdy{vlSymsp->TOP.i_mmcm_drp_rdy}
    , o_mmcm_rst{vlSymsp->TOP.o_mmcm_rst}
    , i_mmcm_locked{vlSymsp->TOP.i_mmcm_locked}
    , o_mmcm_ps_en{vlSymsp->TOP.o_mmcm_ps_en}
    , o_mmcm_ps_incdec{vlSymsp->TOP.o_mmcm_ps_incdec}
    , i_mmcm_ps_done{vlSymsp->TOP.i_mmcm_ps_done}
    , pb_enable_i{vlSymsp->TOP.pb_enable_i}
    , pb_underrun_silence_i{vlSymsp->TOP.pb_underrun_silence_i}
    , pb_stream_en_i{vlSymsp->TOP.pb_stream_en_i}
    , pb_mem_rd_o{vlSymsp->TOP.pb_mem_rd_o}
    , pb_mem_valid_i{vlSymsp->TOP.pb_mem_valid_i}
    , pb_playing_o{vlSymsp->TOP.pb_playing_o}
    , s_axi_awaddr{vlSymsp->TOP.s_axi_awaddr}
    , s_axi_araddr{vlSymsp->TOP.s_axi_araddr}
    , i_mac_events{vlSymsp->TOP.i_mac_events}
    , i_mac_events_cap{vlSymsp->TOP.i_mac_events_cap}
    , o_mmcm_drp_di{vlSymsp->TOP.o_mmcm_drp_di}
    , i_mmcm_drp_do{vlSymsp->TOP.i_mmcm_drp_do}
    , s_axi_wdata{vlSymsp->TOP.s_axi_wdata}
    , s_axi_rdata{vlSymsp->TOP.s_axi_rdata}
    , pb_ring_len_i{vlSymsp->TOP.pb_ring_len_i}
    , pb_ring_stride_i{vlSymsp->TOP.pb_ring_stride_i}
    , pb_wr_ptr_i{vlSymsp->TOP.pb_wr_ptr_i}
    , pb_mem_addr_o{vlSymsp->TOP.pb_mem_addr_o}
    , pb_rd_ptr_o{vlSymsp->TOP.pb_rd_ptr_o}
    , pb_underrun_o{vlSymsp->TOP.pb_underrun_o}
    , pb_overrun_o{vlSymsp->TOP.pb_overrun_o}
    , s_axis_tx_tdata{vlSymsp->TOP.s_axis_tx_tdata}
    , m_axis_rx_tdata{vlSymsp->TOP.m_axis_rx_tdata}
    , m_axis_ts_tdata{vlSymsp->TOP.m_axis_ts_tdata}
    , m_axis_pcm_tdata{vlSymsp->TOP.m_axis_pcm_tdata}
    , m_axis_mac_tx_tdata{vlSymsp->TOP.m_axis_mac_tx_tdata}
    , s_axis_mac_rx_tdata{vlSymsp->TOP.s_axis_mac_rx_tdata}
    , o_mac_addr{vlSymsp->TOP.o_mac_addr}
    , o_mc_hash{vlSymsp->TOP.o_mc_hash}
    , pb_ring_base_i{vlSymsp->TOP.pb_ring_base_i}
    , pb_mem_data_i{vlSymsp->TOP.pb_mem_data_i}
    , __PVT__milan_datapath__DOT__tx_axis_to_shaper{vlSymsp->TOP.__PVT__milan_datapath__DOT__tx_axis_to_shaper}
    , __PVT__milan_datapath__DOT__tx_axis_shaper_to_ts{vlSymsp->TOP.__PVT__milan_datapath__DOT__tx_axis_shaper_to_ts}
    , __PVT__milan_datapath__DOT__tx_axis_dp_to_arb{vlSymsp->TOP.__PVT__milan_datapath__DOT__tx_axis_dp_to_arb}
    , __PVT__milan_datapath__DOT__tx_axis_to_mac{vlSymsp->TOP.__PVT__milan_datapath__DOT__tx_axis_to_mac}
    , __PVT__milan_datapath__DOT__rx_axis_to_ts{vlSymsp->TOP.__PVT__milan_datapath__DOT__rx_axis_to_ts}
    , __PVT__milan_datapath__DOT__rx_axis_ptp_to_filt{vlSymsp->TOP.__PVT__milan_datapath__DOT__rx_axis_ptp_to_filt}
    , __PVT__milan_datapath__DOT__rx_axis_to_dma{vlSymsp->TOP.__PVT__milan_datapath__DOT__rx_axis_to_dma}
    , __PVT__milan_datapath__DOT__ts_metadata_axis{vlSymsp->TOP.__PVT__milan_datapath__DOT__ts_metadata_axis}
    , __PVT__milan_datapath__DOT__ptp_timestamp__DOT__s_axis_tx{vlSymsp->TOP.__PVT__milan_datapath__DOT__ptp_timestamp__DOT__s_axis_tx}
    , __PVT__milan_datapath__DOT__ptp_timestamp__DOT__s_axis_rx{vlSymsp->TOP.__PVT__milan_datapath__DOT__ptp_timestamp__DOT__s_axis_rx}
    , __PVT__milan_datapath__DOT__ptp_timestamp__DOT__m_axis_tx{vlSymsp->TOP.__PVT__milan_datapath__DOT__ptp_timestamp__DOT__m_axis_tx}
    , __PVT__milan_datapath__DOT__ptp_timestamp__DOT__m_axis_rx{vlSymsp->TOP.__PVT__milan_datapath__DOT__ptp_timestamp__DOT__m_axis_rx}
    , __PVT__milan_datapath__DOT__ptp_timestamp__DOT__ts_m_axis_tx{vlSymsp->TOP.__PVT__milan_datapath__DOT__ptp_timestamp__DOT__ts_m_axis_tx}
    , __PVT__milan_datapath__DOT__ptp_timestamp__DOT__ts_m_axis_rx{vlSymsp->TOP.__PVT__milan_datapath__DOT__ptp_timestamp__DOT__ts_m_axis_rx}
    , __PVT__milan_datapath__DOT__ptp_timestamp__DOT__ts_tx_buffered{vlSymsp->TOP.__PVT__milan_datapath__DOT__ptp_timestamp__DOT__ts_tx_buffered}
    , __PVT__milan_datapath__DOT__ptp_timestamp__DOT__ts_rx_buffered{vlSymsp->TOP.__PVT__milan_datapath__DOT__ptp_timestamp__DOT__ts_rx_buffered}
    , __PVT__milan_datapath__DOT__ptp_timestamp__DOT__ts_switch_to_fifo{vlSymsp->TOP.__PVT__milan_datapath__DOT__ptp_timestamp__DOT__ts_switch_to_fifo}
    , __PVT__milan_datapath__DOT__traffic_controller__DOT__classifier_to_queue{vlSymsp->TOP.__PVT__milan_datapath__DOT__traffic_controller__DOT__classifier_to_queue}
    , __PVT__milan_datapath__DOT__traffic_controller__DOT__queue_to_shaper{vlSymsp->TOP.__PVT__milan_datapath__DOT__traffic_controller__DOT__queue_to_shaper}
    , __PVT__milan_datapath__DOT__traffic_controller__DOT__classifier__DOT__m_axis_fifo{vlSymsp->TOP.__PVT__milan_datapath__DOT__traffic_controller__DOT__classifier__DOT__m_axis_fifo}
    , rootp{&(vlSymsp->TOP)}
{
    // Register model with the context
    contextp()->addModel(this);
}

Vmilan_datapath::Vmilan_datapath(const char* _vcname__)
    : Vmilan_datapath(Verilated::threadContextp(), _vcname__)
{
}

//============================================================
// Destructor

Vmilan_datapath::~Vmilan_datapath() {
    delete vlSymsp;
}

//============================================================
// Evaluation function

#ifdef VL_DEBUG
void Vmilan_datapath___024root___eval_debug_assertions(Vmilan_datapath___024root* vlSelf);
#endif  // VL_DEBUG
void Vmilan_datapath___024root___eval_static(Vmilan_datapath___024root* vlSelf);
void Vmilan_datapath___024root___eval_initial(Vmilan_datapath___024root* vlSelf);
void Vmilan_datapath___024root___eval_settle(Vmilan_datapath___024root* vlSelf);
void Vmilan_datapath___024root___eval(Vmilan_datapath___024root* vlSelf);

void Vmilan_datapath::eval_step() {
    VL_DEBUG_IF(VL_DBG_MSGF("+++++TOP Evaluate Vmilan_datapath::eval_step\n"); );
#ifdef VL_DEBUG
    // Debug assertions
    Vmilan_datapath___024root___eval_debug_assertions(&(vlSymsp->TOP));
#endif  // VL_DEBUG
    vlSymsp->__Vm_deleter.deleteAll();
    if (VL_UNLIKELY(!vlSymsp->__Vm_didInit)) {
        VL_DEBUG_IF(VL_DBG_MSGF("+ Initial\n"););
        Vmilan_datapath___024root___eval_static(&(vlSymsp->TOP));
        Vmilan_datapath___024root___eval_initial(&(vlSymsp->TOP));
        Vmilan_datapath___024root___eval_settle(&(vlSymsp->TOP));
        vlSymsp->__Vm_didInit = true;
    }
    VL_DEBUG_IF(VL_DBG_MSGF("+ Eval\n"););
    Vmilan_datapath___024root___eval(&(vlSymsp->TOP));
    // Evaluate cleanup
    Verilated::endOfEval(vlSymsp->__Vm_evalMsgQp);
}

//============================================================
// Events and timing
bool Vmilan_datapath::eventsPending() { return false; }

uint64_t Vmilan_datapath::nextTimeSlot() {
    VL_FATAL_MT(__FILE__, __LINE__, "", "No delays in the design");
    return 0;
}

//============================================================
// Utilities

const char* Vmilan_datapath::name() const {
    return vlSymsp->name();
}

//============================================================
// Invoke final blocks

void Vmilan_datapath___024root___eval_final(Vmilan_datapath___024root* vlSelf);

VL_ATTR_COLD void Vmilan_datapath::final() {
    contextp()->executingFinal(true);
    Vmilan_datapath___024root___eval_final(&(vlSymsp->TOP));
    contextp()->executingFinal(false);
}

//============================================================
// Implementations of abstract methods from VerilatedModel

const char* Vmilan_datapath::hierName() const { return vlSymsp->name(); }
const char* Vmilan_datapath::modelName() const { return "Vmilan_datapath"; }
unsigned Vmilan_datapath::threads() const { return 1; }
void Vmilan_datapath::prepareClone() const { contextp()->prepareClone(); }
void Vmilan_datapath::atClone() const {
    contextp()->threadPoolpOnClone();
}
