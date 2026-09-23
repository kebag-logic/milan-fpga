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
    , i_ps_clk{vlSymsp->TOP.i_ps_clk}
    , o_desc_mem_req_valid{vlSymsp->TOP.o_desc_mem_req_valid}
    , i_desc_mem_req_ready{vlSymsp->TOP.i_desc_mem_req_ready}
    , i_desc_mem_rsp_valid{vlSymsp->TOP.i_desc_mem_rsp_valid}
    , o_desc_mem_rsp_ready{vlSymsp->TOP.o_desc_mem_rsp_ready}
    , i_desc_mem_rsp_last{vlSymsp->TOP.i_desc_mem_rsp_last}
    , i_desc_mem_rsp_err{vlSymsp->TOP.i_desc_mem_rsp_err}
    , o_resp_mem_req_valid{vlSymsp->TOP.o_resp_mem_req_valid}
    , i_resp_mem_req_ready{vlSymsp->TOP.i_resp_mem_req_ready}
    , i_resp_mem_rsp_valid{vlSymsp->TOP.i_resp_mem_rsp_valid}
    , o_resp_mem_rsp_ready{vlSymsp->TOP.o_resp_mem_rsp_ready}
    , i_resp_mem_rsp_last{vlSymsp->TOP.i_resp_mem_rsp_last}
    , i_resp_mem_rsp_err{vlSymsp->TOP.i_resp_mem_rsp_err}
    , o_resp_mem_wr_valid{vlSymsp->TOP.o_resp_mem_wr_valid}
    , i_resp_mem_wr_ready{vlSymsp->TOP.i_resp_mem_wr_ready}
    , o_resp_mem_wr_strb{vlSymsp->TOP.o_resp_mem_wr_strb}
    , i_resp_mem_wr_done{vlSymsp->TOP.i_resp_mem_wr_done}
    , i_resp_mem_wr_err{vlSymsp->TOP.i_resp_mem_wr_err}
    , o_nvm_mem_req_valid{vlSymsp->TOP.o_nvm_mem_req_valid}
    , i_nvm_mem_req_ready{vlSymsp->TOP.i_nvm_mem_req_ready}
    , i_nvm_mem_rsp_valid{vlSymsp->TOP.i_nvm_mem_rsp_valid}
    , o_nvm_mem_rsp_ready{vlSymsp->TOP.o_nvm_mem_rsp_ready}
    , i_nvm_mem_rsp_last{vlSymsp->TOP.i_nvm_mem_rsp_last}
    , i_nvm_mem_rsp_err{vlSymsp->TOP.i_nvm_mem_rsp_err}
    , o_nvm_mem_wr_valid{vlSymsp->TOP.o_nvm_mem_wr_valid}
    , i_nvm_mem_wr_ready{vlSymsp->TOP.i_nvm_mem_wr_ready}
    , o_nvm_mem_wr_strb{vlSymsp->TOP.o_nvm_mem_wr_strb}
    , i_nvm_mem_wr_done{vlSymsp->TOP.i_nvm_mem_wr_done}
    , i_nvm_mem_wr_err{vlSymsp->TOP.i_nvm_mem_wr_err}
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
    , tdm_bclk_i{vlSymsp->TOP.tdm_bclk_i}
    , tdm_fsync_i{vlSymsp->TOP.tdm_fsync_i}
    , tdm_bclk_o{vlSymsp->TOP.tdm_bclk_o}
    , tdm_fsync_o{vlSymsp->TOP.tdm_fsync_o}
    , media_lrclk_o{vlSymsp->TOP.media_lrclk_o}
    , pps_o{vlSymsp->TOP.pps_o}
    , tdm_mclk_o{vlSymsp->TOP.tdm_mclk_o}
    , tdm_dout_o{vlSymsp->TOP.tdm_dout_o}
    , tdm_data_i{vlSymsp->TOP.tdm_data_i}
    , i2s_dac_mclk_o{vlSymsp->TOP.i2s_dac_mclk_o}
    , i2s_dac_sclk_o{vlSymsp->TOP.i2s_dac_sclk_o}
    , i2s_dac_lrck_o{vlSymsp->TOP.i2s_dac_lrck_o}
    , i2s_dac_sdin_o{vlSymsp->TOP.i2s_dac_sdin_o}
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
    , o_eth_guard{vlSymsp->TOP.o_eth_guard}
    , i_full_duplex{vlSymsp->TOP.i_full_duplex}
    , i_ethrx_tgl{vlSymsp->TOP.i_ethrx_tgl}
    , i_ethtx_tgl{vlSymsp->TOP.i_ethtx_tgl}
    , i_ethact_tgl{vlSymsp->TOP.i_ethact_tgl}
    , i_gptp_txrec_valid{vlSymsp->TOP.i_gptp_txrec_valid}
    , i_gptp_txrec_kind{vlSymsp->TOP.i_gptp_txrec_kind}
    , i_gptp_txrec_gen{vlSymsp->TOP.i_gptp_txrec_gen}
    , i_gptp_txrec_type{vlSymsp->TOP.i_gptp_txrec_type}
    , i_gptp_txrec_delta{vlSymsp->TOP.i_gptp_txrec_delta}
    , i_gptp_txrec_abort{vlSymsp->TOP.i_gptp_txrec_abort}
    , o_gptp_txseal_req{vlSymsp->TOP.o_gptp_txseal_req}
    , o_gptp_txseal_gen{vlSymsp->TOP.o_gptp_txseal_gen}
    , i_gptp_txseal_ack{vlSymsp->TOP.i_gptp_txseal_ack}
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
    , o_desc_mem_req_beats{vlSymsp->TOP.o_desc_mem_req_beats}
    , o_resp_mem_req_beats{vlSymsp->TOP.o_resp_mem_req_beats}
    , o_nvm_mem_req_beats{vlSymsp->TOP.o_nvm_mem_req_beats}
    , s_axi_awaddr{vlSymsp->TOP.s_axi_awaddr}
    , s_axi_araddr{vlSymsp->TOP.s_axi_araddr}
    , i_gptp_txrec_oidx{vlSymsp->TOP.i_gptp_txrec_oidx}
    , i_gptp_txrec_seq{vlSymsp->TOP.i_gptp_txrec_seq}
    , i_mac_events{vlSymsp->TOP.i_mac_events}
    , i_mac_events_cap{vlSymsp->TOP.i_mac_events_cap}
    , o_mmcm_drp_di{vlSymsp->TOP.o_mmcm_drp_di}
    , i_mmcm_drp_do{vlSymsp->TOP.i_mmcm_drp_do}
    , o_desc_mem_req_addr{vlSymsp->TOP.o_desc_mem_req_addr}
    , o_resp_mem_req_addr{vlSymsp->TOP.o_resp_mem_req_addr}
    , o_resp_mem_wr_addr{vlSymsp->TOP.o_resp_mem_wr_addr}
    , o_nvm_mem_req_addr{vlSymsp->TOP.o_nvm_mem_req_addr}
    , o_nvm_mem_wr_addr{vlSymsp->TOP.o_nvm_mem_wr_addr}
    , s_axi_wdata{vlSymsp->TOP.s_axi_wdata}
    , s_axi_rdata{vlSymsp->TOP.s_axi_rdata}
    , i_desc_mem_rsp_data{vlSymsp->TOP.i_desc_mem_rsp_data}
    , i_resp_mem_rsp_data{vlSymsp->TOP.i_resp_mem_rsp_data}
    , o_resp_mem_wr_data{vlSymsp->TOP.o_resp_mem_wr_data}
    , i_nvm_mem_rsp_data{vlSymsp->TOP.i_nvm_mem_rsp_data}
    , o_nvm_mem_wr_data{vlSymsp->TOP.o_nvm_mem_wr_data}
    , m_axis_mac_tx_tdata{vlSymsp->TOP.m_axis_mac_tx_tdata}
    , s_axis_mac_rx_tdata{vlSymsp->TOP.s_axis_mac_rx_tdata}
    , o_mac_addr{vlSymsp->TOP.o_mac_addr}
    , o_mc_hash{vlSymsp->TOP.o_mc_hash}
    , __PVT__milan_datapath__DOT__tx_axis_to_mac{vlSymsp->TOP.__PVT__milan_datapath__DOT__tx_axis_to_mac}
    , __PVT__milan_datapath__DOT__rx_axis_from_mac{vlSymsp->TOP.__PVT__milan_datapath__DOT__rx_axis_from_mac}
    , __PVT__milan_datapath__DOT__rx_axis_fabric{vlSymsp->TOP.__PVT__milan_datapath__DOT__rx_axis_fabric}
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
