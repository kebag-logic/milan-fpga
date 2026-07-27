// Verilated -*- C++ -*-
// DESCRIPTION: Verilator output: Model implementation (design independent parts)

#include "VKL_ptp_clock_validity__pch.h"

//============================================================
// Constructors

VKL_ptp_clock_validity::VKL_ptp_clock_validity(VerilatedContext* _vcontextp__, const char* _vcname__)
    : VerilatedModel{*_vcontextp__}
    , vlSymsp{new VKL_ptp_clock_validity__Syms(contextp(), _vcname__, this)}
    , clk_i{vlSymsp->TOP.clk_i}
    , rst_n{vlSymsp->TOP.rst_n}
    , sw_wr_p_i{vlSymsp->TOP.sw_wr_p_i}
    , sw_sync_ok_i{vlSymsp->TOP.sw_sync_ok_i}
    , sw_disc_p_i{vlSymsp->TOP.sw_disc_p_i}
    , phc_load_p_i{vlSymsp->TOP.phc_load_p_i}
    , phc_adj_p_i{vlSymsp->TOP.phc_adj_p_i}
    , ts_uncertain_o{vlSymsp->TOP.ts_uncertain_o}
    , sw_wdog_q_i{vlSymsp->TOP.sw_wdog_q_i}
    , stat_o{vlSymsp->TOP.stat_o}
    , tu_ivals_o{vlSymsp->TOP.tu_ivals_o}
    , gm_id_i{vlSymsp->TOP.gm_id_i}
    , rootp{&(vlSymsp->TOP)}
{
    // Register model with the context
    contextp()->addModel(this);
}

VKL_ptp_clock_validity::VKL_ptp_clock_validity(const char* _vcname__)
    : VKL_ptp_clock_validity(Verilated::threadContextp(), _vcname__)
{
}

//============================================================
// Destructor

VKL_ptp_clock_validity::~VKL_ptp_clock_validity() {
    delete vlSymsp;
}

//============================================================
// Evaluation function

#ifdef VL_DEBUG
void VKL_ptp_clock_validity___024root___eval_debug_assertions(VKL_ptp_clock_validity___024root* vlSelf);
#endif  // VL_DEBUG
void VKL_ptp_clock_validity___024root___eval_static(VKL_ptp_clock_validity___024root* vlSelf);
void VKL_ptp_clock_validity___024root___eval_initial(VKL_ptp_clock_validity___024root* vlSelf);
void VKL_ptp_clock_validity___024root___eval_settle(VKL_ptp_clock_validity___024root* vlSelf);
void VKL_ptp_clock_validity___024root___eval(VKL_ptp_clock_validity___024root* vlSelf);

void VKL_ptp_clock_validity::eval_step() {
    VL_DEBUG_IF(VL_DBG_MSGF("+++++TOP Evaluate VKL_ptp_clock_validity::eval_step\n"); );
#ifdef VL_DEBUG
    // Debug assertions
    VKL_ptp_clock_validity___024root___eval_debug_assertions(&(vlSymsp->TOP));
#endif  // VL_DEBUG
    vlSymsp->__Vm_deleter.deleteAll();
    if (VL_UNLIKELY(!vlSymsp->__Vm_didInit)) {
        VL_DEBUG_IF(VL_DBG_MSGF("+ Initial\n"););
        VKL_ptp_clock_validity___024root___eval_static(&(vlSymsp->TOP));
        VKL_ptp_clock_validity___024root___eval_initial(&(vlSymsp->TOP));
        VKL_ptp_clock_validity___024root___eval_settle(&(vlSymsp->TOP));
        vlSymsp->__Vm_didInit = true;
    }
    VL_DEBUG_IF(VL_DBG_MSGF("+ Eval\n"););
    VKL_ptp_clock_validity___024root___eval(&(vlSymsp->TOP));
    // Evaluate cleanup
    Verilated::endOfEval(vlSymsp->__Vm_evalMsgQp);
}

//============================================================
// Events and timing
bool VKL_ptp_clock_validity::eventsPending() { return false; }

uint64_t VKL_ptp_clock_validity::nextTimeSlot() {
    VL_FATAL_MT(__FILE__, __LINE__, "", "No delays in the design");
    return 0;
}

//============================================================
// Utilities

const char* VKL_ptp_clock_validity::name() const {
    return vlSymsp->name();
}

//============================================================
// Invoke final blocks

void VKL_ptp_clock_validity___024root___eval_final(VKL_ptp_clock_validity___024root* vlSelf);

VL_ATTR_COLD void VKL_ptp_clock_validity::final() {
    contextp()->executingFinal(true);
    VKL_ptp_clock_validity___024root___eval_final(&(vlSymsp->TOP));
    contextp()->executingFinal(false);
}

//============================================================
// Implementations of abstract methods from VerilatedModel

const char* VKL_ptp_clock_validity::hierName() const { return vlSymsp->name(); }
const char* VKL_ptp_clock_validity::modelName() const { return "VKL_ptp_clock_validity"; }
unsigned VKL_ptp_clock_validity::threads() const { return 1; }
void VKL_ptp_clock_validity::prepareClone() const { contextp()->prepareClone(); }
void VKL_ptp_clock_validity::atClone() const {
    contextp()->threadPoolpOnClone();
}
