// Verilated -*- C++ -*-
// DESCRIPTION: Verilator output: Model implementation (design independent parts)

#include "Vmedia_grid_align_wrap__pch.h"

//============================================================
// Constructors

Vmedia_grid_align_wrap::Vmedia_grid_align_wrap(VerilatedContext* _vcontextp__, const char* _vcname__)
    : VerilatedModel{*_vcontextp__}
    , vlSymsp{new Vmedia_grid_align_wrap__Syms(contextp(), _vcname__, this)}
    , clk{vlSymsp->TOP.clk}
    , rst_n{vlSymsp->TOP.rst_n}
    , sel_i{vlSymsp->TOP.sel_i}
    , frame_ev_i{vlSymsp->TOP.frame_ev_i}
    , tick_o{vlSymsp->TOP.tick_o}
    , engaged_o{vlSymsp->TOP.engaged_o}
    , u_o{vlSymsp->TOP.u_o}
    , err_cyc_o{vlSymsp->TOP.err_cyc_o}
    , phase_o{vlSymsp->TOP.phase_o}
    , tdm_dup_cnt_o{vlSymsp->TOP.tdm_dup_cnt_o}
    , tdm_skip_cnt_o{vlSymsp->TOP.tdm_skip_cnt_o}
    , rootp{&(vlSymsp->TOP)}
{
    // Register model with the context
    contextp()->addModel(this);
}

Vmedia_grid_align_wrap::Vmedia_grid_align_wrap(const char* _vcname__)
    : Vmedia_grid_align_wrap(Verilated::threadContextp(), _vcname__)
{
}

//============================================================
// Destructor

Vmedia_grid_align_wrap::~Vmedia_grid_align_wrap() {
    delete vlSymsp;
}

//============================================================
// Evaluation function

#ifdef VL_DEBUG
void Vmedia_grid_align_wrap___024root___eval_debug_assertions(Vmedia_grid_align_wrap___024root* vlSelf);
#endif  // VL_DEBUG
void Vmedia_grid_align_wrap___024root___eval_static(Vmedia_grid_align_wrap___024root* vlSelf);
void Vmedia_grid_align_wrap___024root___eval_initial(Vmedia_grid_align_wrap___024root* vlSelf);
void Vmedia_grid_align_wrap___024root___eval_settle(Vmedia_grid_align_wrap___024root* vlSelf);
void Vmedia_grid_align_wrap___024root___eval(Vmedia_grid_align_wrap___024root* vlSelf);

void Vmedia_grid_align_wrap::eval_step() {
    VL_DEBUG_IF(VL_DBG_MSGF("+++++TOP Evaluate Vmedia_grid_align_wrap::eval_step\n"); );
#ifdef VL_DEBUG
    // Debug assertions
    Vmedia_grid_align_wrap___024root___eval_debug_assertions(&(vlSymsp->TOP));
#endif  // VL_DEBUG
    vlSymsp->__Vm_deleter.deleteAll();
    if (VL_UNLIKELY(!vlSymsp->__Vm_didInit)) {
        VL_DEBUG_IF(VL_DBG_MSGF("+ Initial\n"););
        Vmedia_grid_align_wrap___024root___eval_static(&(vlSymsp->TOP));
        Vmedia_grid_align_wrap___024root___eval_initial(&(vlSymsp->TOP));
        Vmedia_grid_align_wrap___024root___eval_settle(&(vlSymsp->TOP));
        vlSymsp->__Vm_didInit = true;
    }
    VL_DEBUG_IF(VL_DBG_MSGF("+ Eval\n"););
    Vmedia_grid_align_wrap___024root___eval(&(vlSymsp->TOP));
    // Evaluate cleanup
    Verilated::endOfEval(vlSymsp->__Vm_evalMsgQp);
}

//============================================================
// Events and timing
bool Vmedia_grid_align_wrap::eventsPending() { return false; }

uint64_t Vmedia_grid_align_wrap::nextTimeSlot() {
    VL_FATAL_MT(__FILE__, __LINE__, "", "No delays in the design");
    return 0;
}

//============================================================
// Utilities

const char* Vmedia_grid_align_wrap::name() const {
    return vlSymsp->name();
}

//============================================================
// Invoke final blocks

void Vmedia_grid_align_wrap___024root___eval_final(Vmedia_grid_align_wrap___024root* vlSelf);

VL_ATTR_COLD void Vmedia_grid_align_wrap::final() {
    contextp()->executingFinal(true);
    Vmedia_grid_align_wrap___024root___eval_final(&(vlSymsp->TOP));
    contextp()->executingFinal(false);
}

//============================================================
// Implementations of abstract methods from VerilatedModel

const char* Vmedia_grid_align_wrap::hierName() const { return vlSymsp->name(); }
const char* Vmedia_grid_align_wrap::modelName() const { return "Vmedia_grid_align_wrap"; }
unsigned Vmedia_grid_align_wrap::threads() const { return 1; }
void Vmedia_grid_align_wrap::prepareClone() const { contextp()->prepareClone(); }
void Vmedia_grid_align_wrap::atClone() const {
    contextp()->threadPoolpOnClone();
}
