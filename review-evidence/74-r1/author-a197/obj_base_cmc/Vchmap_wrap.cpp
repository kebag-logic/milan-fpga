// Verilated -*- C++ -*-
// DESCRIPTION: Verilator output: Model implementation (design independent parts)

#include "Vchmap_wrap__pch.h"

//============================================================
// Constructors

Vchmap_wrap::Vchmap_wrap(VerilatedContext* _vcontextp__, const char* _vcname__)
    : VerilatedModel{*_vcontextp__}
    , vlSymsp{new Vchmap_wrap__Syms(contextp(), _vcname__, this)}
    , clk{vlSymsp->TOP.clk}
    , clk_audio{vlSymsp->TOP.clk_audio}
    , rst_n{vlSymsp->TOP.rst_n}
    , tg_en_i{vlSymsp->TOP.tg_en_i}
    , tg_tick_i{vlSymsp->TOP.tg_tick_i}
    , i2s_pair_valid_i{vlSymsp->TOP.i2s_pair_valid_i}
    , tdm_pair_valid_i{vlSymsp->TOP.tdm_pair_valid_i}
    , tdm_pair_slot_i{vlSymsp->TOP.tdm_pair_slot_i}
    , lb_tvalid_i{vlSymsp->TOP.lb_tvalid_i}
    , lb_tlast_i{vlSymsp->TOP.lb_tlast_i}
    , lb_tuser_i{vlSymsp->TOP.lb_tuser_i}
    , a_lb_flush_i{vlSymsp->TOP.a_lb_flush_i}
    , b_lb_flush_i{vlSymsp->TOP.b_lb_flush_i}
    , a_map_wr_en_i{vlSymsp->TOP.a_map_wr_en_i}
    , a_map_wr_addr_i{vlSymsp->TOP.a_map_wr_addr_i}
    , a_map_rd_en_i{vlSymsp->TOP.a_map_rd_en_i}
    , a_map_rd_addr_i{vlSymsp->TOP.a_map_rd_addr_i}
    , a_map_rd_valid_o{vlSymsp->TOP.a_map_rd_valid_o}
    , a_tick_i{vlSymsp->TOP.a_tick_i}
    , a_pv_o{vlSymsp->TOP.a_pv_o}
    , a_en_i{vlSymsp->TOP.a_en_i}
    , a_tctx_wr_en_i{vlSymsp->TOP.a_tctx_wr_en_i}
    , a_tctx_wr_addr_i{vlSymsp->TOP.a_tctx_wr_addr_i}
    , a_tctx_wr_rdy_o{vlSymsp->TOP.a_tctx_wr_rdy_o}
    , a_tctx_rd_en_i{vlSymsp->TOP.a_tctx_rd_en_i}
    , a_tctx_rd_addr_i{vlSymsp->TOP.a_tctx_rd_addr_i}
    , a_tctx_rd_valid_o{vlSymsp->TOP.a_tctx_rd_valid_o}
    , a_tkeep_o{vlSymsp->TOP.a_tkeep_o}
    , a_tvalid_o{vlSymsp->TOP.a_tvalid_o}
    , a_tlast_o{vlSymsp->TOP.a_tlast_o}
    , a_tready_i{vlSymsp->TOP.a_tready_i}
    , b_map_wr_en_i{vlSymsp->TOP.b_map_wr_en_i}
    , b_map_wr_addr_i{vlSymsp->TOP.b_map_wr_addr_i}
    , b_map_rd_en_i{vlSymsp->TOP.b_map_rd_en_i}
    , b_map_rd_addr_i{vlSymsp->TOP.b_map_rd_addr_i}
    , b_map_rd_valid_o{vlSymsp->TOP.b_map_rd_valid_o}
    , b_tick_i{vlSymsp->TOP.b_tick_i}
    , b_en_i{vlSymsp->TOP.b_en_i}
    , b_tctx_wr_en_i{vlSymsp->TOP.b_tctx_wr_en_i}
    , b_tctx_wr_addr_i{vlSymsp->TOP.b_tctx_wr_addr_i}
    , b_tctx_wr_rdy_o{vlSymsp->TOP.b_tctx_wr_rdy_o}
    , b_tctx_rd_en_i{vlSymsp->TOP.b_tctx_rd_en_i}
    , b_tctx_rd_addr_i{vlSymsp->TOP.b_tctx_rd_addr_i}
    , b_tctx_rd_valid_o{vlSymsp->TOP.b_tctx_rd_valid_o}
    , b_tkeep_o{vlSymsp->TOP.b_tkeep_o}
    , b_tvalid_o{vlSymsp->TOP.b_tvalid_o}
    , b_tlast_o{vlSymsp->TOP.b_tlast_o}
    , b_tready_i{vlSymsp->TOP.b_tready_i}
    , vlan_vid_i{vlSymsp->TOP.vlan_vid_i}
    , a_dup_cnt_o{vlSymsp->TOP.a_dup_cnt_o}
    , a_skip_cnt_o{vlSymsp->TOP.a_skip_cnt_o}
    , a_tdm_dup_cnt_o{vlSymsp->TOP.a_tdm_dup_cnt_o}
    , a_tdm_skip_cnt_o{vlSymsp->TOP.a_tdm_skip_cnt_o}
    , b_dup_cnt_o{vlSymsp->TOP.b_dup_cnt_o}
    , b_skip_cnt_o{vlSymsp->TOP.b_skip_cnt_o}
    , a_map_wr_data_i{vlSymsp->TOP.a_map_wr_data_i}
    , a_map_rd_data_o{vlSymsp->TOP.a_map_rd_data_o}
    , b_map_wr_data_i{vlSymsp->TOP.b_map_wr_data_i}
    , b_map_rd_data_o{vlSymsp->TOP.b_map_rd_data_o}
    , tone_legacy_o{vlSymsp->TOP.tone_legacy_o}
    , tone_media_o{vlSymsp->TOP.tone_media_o}
    , transit_ns_i{vlSymsp->TOP.transit_ns_i}
    , i2s_l_i{vlSymsp->TOP.i2s_l_i}
    , i2s_r_i{vlSymsp->TOP.i2s_r_i}
    , tdm_l_i{vlSymsp->TOP.tdm_l_i}
    , tdm_r_i{vlSymsp->TOP.tdm_r_i}
    , tone_smp_i{vlSymsp->TOP.tone_smp_i}
    , lb_wire_chans_i{vlSymsp->TOP.lb_wire_chans_i}
    , a_tctx_wr_data_i{vlSymsp->TOP.a_tctx_wr_data_i}
    , a_tctx_rd_data_o{vlSymsp->TOP.a_tctx_rd_data_o}
    , b_tctx_wr_data_i{vlSymsp->TOP.b_tctx_wr_data_i}
    , b_tctx_rd_data_o{vlSymsp->TOP.b_tctx_rd_data_o}
    , dest_mac_i{vlSymsp->TOP.dest_mac_i}
    , station_mac_i{vlSymsp->TOP.station_mac_i}
    , ptp_ns_i{vlSymsp->TOP.ptp_ns_i}
    , lb_tdata_i{vlSymsp->TOP.lb_tdata_i}
    , a_tdata_o{vlSymsp->TOP.a_tdata_o}
    , b_tdata_o{vlSymsp->TOP.b_tdata_o}
    , __PVT__chmap_wrap__DOT__u_chmap_a{vlSymsp->TOP.__PVT__chmap_wrap__DOT__u_chmap_a}
    , __PVT__chmap_wrap__DOT__u_chmap_b{vlSymsp->TOP.__PVT__chmap_wrap__DOT__u_chmap_b}
    , rootp{&(vlSymsp->TOP)}
{
    // Register model with the context
    contextp()->addModel(this);
}

Vchmap_wrap::Vchmap_wrap(const char* _vcname__)
    : Vchmap_wrap(Verilated::threadContextp(), _vcname__)
{
}

//============================================================
// Destructor

Vchmap_wrap::~Vchmap_wrap() {
    delete vlSymsp;
}

//============================================================
// Evaluation function

#ifdef VL_DEBUG
void Vchmap_wrap___024root___eval_debug_assertions(Vchmap_wrap___024root* vlSelf);
#endif  // VL_DEBUG
void Vchmap_wrap___024root___eval_static(Vchmap_wrap___024root* vlSelf);
void Vchmap_wrap___024root___eval_initial(Vchmap_wrap___024root* vlSelf);
void Vchmap_wrap___024root___eval_settle(Vchmap_wrap___024root* vlSelf);
void Vchmap_wrap___024root___eval(Vchmap_wrap___024root* vlSelf);

void Vchmap_wrap::eval_step() {
    VL_DEBUG_IF(VL_DBG_MSGF("+++++TOP Evaluate Vchmap_wrap::eval_step\n"); );
#ifdef VL_DEBUG
    // Debug assertions
    Vchmap_wrap___024root___eval_debug_assertions(&(vlSymsp->TOP));
#endif  // VL_DEBUG
    vlSymsp->__Vm_deleter.deleteAll();
    if (VL_UNLIKELY(!vlSymsp->__Vm_didInit)) {
        VL_DEBUG_IF(VL_DBG_MSGF("+ Initial\n"););
        Vchmap_wrap___024root___eval_static(&(vlSymsp->TOP));
        Vchmap_wrap___024root___eval_initial(&(vlSymsp->TOP));
        Vchmap_wrap___024root___eval_settle(&(vlSymsp->TOP));
        vlSymsp->__Vm_didInit = true;
    }
    VL_DEBUG_IF(VL_DBG_MSGF("+ Eval\n"););
    Vchmap_wrap___024root___eval(&(vlSymsp->TOP));
    // Evaluate cleanup
    Verilated::endOfEval(vlSymsp->__Vm_evalMsgQp);
}

//============================================================
// Events and timing
bool Vchmap_wrap::eventsPending() { return false; }

uint64_t Vchmap_wrap::nextTimeSlot() {
    VL_FATAL_MT(__FILE__, __LINE__, "", "No delays in the design");
    return 0;
}

//============================================================
// Utilities

const char* Vchmap_wrap::name() const {
    return vlSymsp->name();
}

//============================================================
// Invoke final blocks

void Vchmap_wrap___024root___eval_final(Vchmap_wrap___024root* vlSelf);

VL_ATTR_COLD void Vchmap_wrap::final() {
    contextp()->executingFinal(true);
    Vchmap_wrap___024root___eval_final(&(vlSymsp->TOP));
    contextp()->executingFinal(false);
}

//============================================================
// Implementations of abstract methods from VerilatedModel

const char* Vchmap_wrap::hierName() const { return vlSymsp->name(); }
const char* Vchmap_wrap::modelName() const { return "Vchmap_wrap"; }
unsigned Vchmap_wrap::threads() const { return 1; }
void Vchmap_wrap::prepareClone() const { contextp()->prepareClone(); }
void Vchmap_wrap::atClone() const {
    contextp()->threadPoolpOnClone();
}
