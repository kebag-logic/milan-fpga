// Verilated -*- C++ -*-
// DESCRIPTION: Verilator output: Model implementation (design independent parts)

#include "Vptp_ts_top__pch.h"

//============================================================
// Constructors

Vptp_ts_top::Vptp_ts_top(VerilatedContext* _vcontextp__, const char* _vcname__)
    : VerilatedModel{*_vcontextp__}
    , vlSymsp{new Vptp_ts_top__Syms(contextp(), _vcname__, this)}
    , gtx_clk{vlSymsp->TOP.gtx_clk}
    , axis_clk{vlSymsp->TOP.axis_clk}
    , gtx_resetn{vlSymsp->TOP.gtx_resetn}
    , axis_resetn{vlSymsp->TOP.axis_resetn}
    , i_ptp_enable{vlSymsp->TOP.i_ptp_enable}
    , i_ptp_cmd_load{vlSymsp->TOP.i_ptp_cmd_load}
    , i_ptp_cmd_adjust{vlSymsp->TOP.i_ptp_cmd_adjust}
    , i_ptp_cmd_snapshot{vlSymsp->TOP.i_ptp_cmd_snapshot}
    , o_ptp_tod_rd_valid{vlSymsp->TOP.o_ptp_tod_rd_valid}
    , o_tx_ts_ready{vlSymsp->TOP.o_tx_ts_ready}
    , s_axis_tx_tvalid{vlSymsp->TOP.s_axis_tx_tvalid}
    , s_axis_tx_tready{vlSymsp->TOP.s_axis_tx_tready}
    , s_axis_tx_tlast{vlSymsp->TOP.s_axis_tx_tlast}
    , s_axis_tx_tkeep{vlSymsp->TOP.s_axis_tx_tkeep}
    , m_axis_tx_tvalid{vlSymsp->TOP.m_axis_tx_tvalid}
    , m_axis_tx_tready{vlSymsp->TOP.m_axis_tx_tready}
    , m_axis_tx_tlast{vlSymsp->TOP.m_axis_tx_tlast}
    , m_axis_tx_tkeep{vlSymsp->TOP.m_axis_tx_tkeep}
    , s_axis_rx_tvalid{vlSymsp->TOP.s_axis_rx_tvalid}
    , s_axis_rx_tready{vlSymsp->TOP.s_axis_rx_tready}
    , s_axis_rx_tlast{vlSymsp->TOP.s_axis_rx_tlast}
    , s_axis_rx_tkeep{vlSymsp->TOP.s_axis_rx_tkeep}
    , m_axis_rx_tvalid{vlSymsp->TOP.m_axis_rx_tvalid}
    , m_axis_rx_tready{vlSymsp->TOP.m_axis_rx_tready}
    , m_axis_rx_tlast{vlSymsp->TOP.m_axis_rx_tlast}
    , m_axis_rx_tkeep{vlSymsp->TOP.m_axis_rx_tkeep}
    , ts_m_axis_tvalid{vlSymsp->TOP.ts_m_axis_tvalid}
    , ts_m_axis_tready{vlSymsp->TOP.ts_m_axis_tready}
    , ts_m_axis_tlast{vlSymsp->TOP.ts_m_axis_tlast}
    , ts_m_axis_tkeep{vlSymsp->TOP.ts_m_axis_tkeep}
    , i_ptp_incr{vlSymsp->TOP.i_ptp_incr}
    , i_ptp_adj{vlSymsp->TOP.i_ptp_adj}
    , i_ptp_ingress_lat{vlSymsp->TOP.i_ptp_ingress_lat}
    , i_ptp_egress_lat{vlSymsp->TOP.i_ptp_egress_lat}
    , i_ptp_tod_wr{vlSymsp->TOP.i_ptp_tod_wr}
    , i_ptp_offset{vlSymsp->TOP.i_ptp_offset}
    , o_ptp_tod_rd{vlSymsp->TOP.o_ptp_tod_rd}
    , o_ptp_now{vlSymsp->TOP.o_ptp_now}
    , s_axis_tx_tdata{vlSymsp->TOP.s_axis_tx_tdata}
    , m_axis_tx_tdata{vlSymsp->TOP.m_axis_tx_tdata}
    , s_axis_rx_tdata{vlSymsp->TOP.s_axis_rx_tdata}
    , m_axis_rx_tdata{vlSymsp->TOP.m_axis_rx_tdata}
    , ts_m_axis_tdata{vlSymsp->TOP.ts_m_axis_tdata}
    , __PVT__ptp_ts_top__DOT__s_axis_tx{vlSymsp->TOP.__PVT__ptp_ts_top__DOT__s_axis_tx}
    , __PVT__ptp_ts_top__DOT__s_axis_rx{vlSymsp->TOP.__PVT__ptp_ts_top__DOT__s_axis_rx}
    , __PVT__ptp_ts_top__DOT__m_axis_tx{vlSymsp->TOP.__PVT__ptp_ts_top__DOT__m_axis_tx}
    , __PVT__ptp_ts_top__DOT__m_axis_rx{vlSymsp->TOP.__PVT__ptp_ts_top__DOT__m_axis_rx}
    , __PVT__ptp_ts_top__DOT__ts_m_axis_tx{vlSymsp->TOP.__PVT__ptp_ts_top__DOT__ts_m_axis_tx}
    , __PVT__ptp_ts_top__DOT__ts_m_axis_rx{vlSymsp->TOP.__PVT__ptp_ts_top__DOT__ts_m_axis_rx}
    , __PVT__ptp_ts_top__DOT__ts_tx_buffered{vlSymsp->TOP.__PVT__ptp_ts_top__DOT__ts_tx_buffered}
    , __PVT__ptp_ts_top__DOT__ts_rx_buffered{vlSymsp->TOP.__PVT__ptp_ts_top__DOT__ts_rx_buffered}
    , __PVT__ptp_ts_top__DOT__ts_switch_to_fifo{vlSymsp->TOP.__PVT__ptp_ts_top__DOT__ts_switch_to_fifo}
    , rootp{&(vlSymsp->TOP)}
{
    // Register model with the context
    contextp()->addModel(this);
}

Vptp_ts_top::Vptp_ts_top(const char* _vcname__)
    : Vptp_ts_top(Verilated::threadContextp(), _vcname__)
{
}

//============================================================
// Destructor

Vptp_ts_top::~Vptp_ts_top() {
    delete vlSymsp;
}

//============================================================
// Evaluation function

#ifdef VL_DEBUG
void Vptp_ts_top___024root___eval_debug_assertions(Vptp_ts_top___024root* vlSelf);
#endif  // VL_DEBUG
void Vptp_ts_top___024root___eval_static(Vptp_ts_top___024root* vlSelf);
void Vptp_ts_top___024root___eval_initial(Vptp_ts_top___024root* vlSelf);
void Vptp_ts_top___024root___eval_settle(Vptp_ts_top___024root* vlSelf);
void Vptp_ts_top___024root___eval(Vptp_ts_top___024root* vlSelf);

void Vptp_ts_top::eval_step() {
    VL_DEBUG_IF(VL_DBG_MSGF("+++++TOP Evaluate Vptp_ts_top::eval_step\n"); );
#ifdef VL_DEBUG
    // Debug assertions
    Vptp_ts_top___024root___eval_debug_assertions(&(vlSymsp->TOP));
#endif  // VL_DEBUG
    vlSymsp->__Vm_deleter.deleteAll();
    if (VL_UNLIKELY(!vlSymsp->__Vm_didInit)) {
        VL_DEBUG_IF(VL_DBG_MSGF("+ Initial\n"););
        Vptp_ts_top___024root___eval_static(&(vlSymsp->TOP));
        Vptp_ts_top___024root___eval_initial(&(vlSymsp->TOP));
        Vptp_ts_top___024root___eval_settle(&(vlSymsp->TOP));
        vlSymsp->__Vm_didInit = true;
    }
    VL_DEBUG_IF(VL_DBG_MSGF("+ Eval\n"););
    Vptp_ts_top___024root___eval(&(vlSymsp->TOP));
    // Evaluate cleanup
    Verilated::endOfEval(vlSymsp->__Vm_evalMsgQp);
}

//============================================================
// Events and timing
bool Vptp_ts_top::eventsPending() { return false; }

uint64_t Vptp_ts_top::nextTimeSlot() {
    VL_FATAL_MT(__FILE__, __LINE__, "", "No delays in the design");
    return 0;
}

//============================================================
// Utilities

const char* Vptp_ts_top::name() const {
    return vlSymsp->name();
}

//============================================================
// Invoke final blocks

void Vptp_ts_top___024root___eval_final(Vptp_ts_top___024root* vlSelf);

VL_ATTR_COLD void Vptp_ts_top::final() {
    contextp()->executingFinal(true);
    Vptp_ts_top___024root___eval_final(&(vlSymsp->TOP));
    contextp()->executingFinal(false);
}

//============================================================
// Implementations of abstract methods from VerilatedModel

const char* Vptp_ts_top::hierName() const { return vlSymsp->name(); }
const char* Vptp_ts_top::modelName() const { return "Vptp_ts_top"; }
unsigned Vptp_ts_top::threads() const { return 1; }
void Vptp_ts_top::prepareClone() const { contextp()->prepareClone(); }
void Vptp_ts_top::atClone() const {
    contextp()->threadPoolpOnClone();
}
