// Verilated -*- C++ -*-
// DESCRIPTION: Verilator output: Model implementation (design independent parts)

#include "Vaxis_mux_rr_2in_1out__pch.h"

//============================================================
// Constructors

Vaxis_mux_rr_2in_1out::Vaxis_mux_rr_2in_1out(VerilatedContext* _vcontextp__, const char* _vcname__)
    : VerilatedModel{*_vcontextp__}
    , vlSymsp{new Vaxis_mux_rr_2in_1out__Syms(contextp(), _vcname__, this)}
    , clk{vlSymsp->TOP.clk}
    , rst_n{vlSymsp->TOP.rst_n}
    , s0_tdata{vlSymsp->TOP.s0_tdata}
    , s0_tvalid{vlSymsp->TOP.s0_tvalid}
    , s0_tready{vlSymsp->TOP.s0_tready}
    , s0_tlast{vlSymsp->TOP.s0_tlast}
    , s0_tkeep{vlSymsp->TOP.s0_tkeep}
    , s1_tdata{vlSymsp->TOP.s1_tdata}
    , s1_tvalid{vlSymsp->TOP.s1_tvalid}
    , s1_tready{vlSymsp->TOP.s1_tready}
    , s1_tlast{vlSymsp->TOP.s1_tlast}
    , s1_tkeep{vlSymsp->TOP.s1_tkeep}
    , m_tdata{vlSymsp->TOP.m_tdata}
    , m_tvalid{vlSymsp->TOP.m_tvalid}
    , m_tready{vlSymsp->TOP.m_tready}
    , m_tlast{vlSymsp->TOP.m_tlast}
    , m_tkeep{vlSymsp->TOP.m_tkeep}
    , rootp{&(vlSymsp->TOP)}
{
    // Register model with the context
    contextp()->addModel(this);
}

Vaxis_mux_rr_2in_1out::Vaxis_mux_rr_2in_1out(const char* _vcname__)
    : Vaxis_mux_rr_2in_1out(Verilated::threadContextp(), _vcname__)
{
}

//============================================================
// Destructor

Vaxis_mux_rr_2in_1out::~Vaxis_mux_rr_2in_1out() {
    delete vlSymsp;
}

//============================================================
// Evaluation function

#ifdef VL_DEBUG
void Vaxis_mux_rr_2in_1out___024root___eval_debug_assertions(Vaxis_mux_rr_2in_1out___024root* vlSelf);
#endif  // VL_DEBUG
void Vaxis_mux_rr_2in_1out___024root___eval_static(Vaxis_mux_rr_2in_1out___024root* vlSelf);
void Vaxis_mux_rr_2in_1out___024root___eval_initial(Vaxis_mux_rr_2in_1out___024root* vlSelf);
void Vaxis_mux_rr_2in_1out___024root___eval_settle(Vaxis_mux_rr_2in_1out___024root* vlSelf);
void Vaxis_mux_rr_2in_1out___024root___eval(Vaxis_mux_rr_2in_1out___024root* vlSelf);

void Vaxis_mux_rr_2in_1out::eval_step() {
    VL_DEBUG_IF(VL_DBG_MSGF("+++++TOP Evaluate Vaxis_mux_rr_2in_1out::eval_step\n"); );
#ifdef VL_DEBUG
    // Debug assertions
    Vaxis_mux_rr_2in_1out___024root___eval_debug_assertions(&(vlSymsp->TOP));
#endif  // VL_DEBUG
    vlSymsp->__Vm_deleter.deleteAll();
    if (VL_UNLIKELY(!vlSymsp->__Vm_didInit)) {
        VL_DEBUG_IF(VL_DBG_MSGF("+ Initial\n"););
        Vaxis_mux_rr_2in_1out___024root___eval_static(&(vlSymsp->TOP));
        Vaxis_mux_rr_2in_1out___024root___eval_initial(&(vlSymsp->TOP));
        Vaxis_mux_rr_2in_1out___024root___eval_settle(&(vlSymsp->TOP));
        vlSymsp->__Vm_didInit = true;
    }
    VL_DEBUG_IF(VL_DBG_MSGF("+ Eval\n"););
    Vaxis_mux_rr_2in_1out___024root___eval(&(vlSymsp->TOP));
    // Evaluate cleanup
    Verilated::endOfEval(vlSymsp->__Vm_evalMsgQp);
}

//============================================================
// Events and timing
bool Vaxis_mux_rr_2in_1out::eventsPending() { return false; }

uint64_t Vaxis_mux_rr_2in_1out::nextTimeSlot() {
    VL_FATAL_MT(__FILE__, __LINE__, "", "No delays in the design");
    return 0;
}

//============================================================
// Utilities

const char* Vaxis_mux_rr_2in_1out::name() const {
    return vlSymsp->name();
}

//============================================================
// Invoke final blocks

void Vaxis_mux_rr_2in_1out___024root___eval_final(Vaxis_mux_rr_2in_1out___024root* vlSelf);

VL_ATTR_COLD void Vaxis_mux_rr_2in_1out::final() {
    contextp()->executingFinal(true);
    Vaxis_mux_rr_2in_1out___024root___eval_final(&(vlSymsp->TOP));
    contextp()->executingFinal(false);
}

//============================================================
// Implementations of abstract methods from VerilatedModel

const char* Vaxis_mux_rr_2in_1out::hierName() const { return vlSymsp->name(); }
const char* Vaxis_mux_rr_2in_1out::modelName() const { return "Vaxis_mux_rr_2in_1out"; }
unsigned Vaxis_mux_rr_2in_1out::threads() const { return 1; }
void Vaxis_mux_rr_2in_1out::prepareClone() const { contextp()->prepareClone(); }
void Vaxis_mux_rr_2in_1out::atClone() const {
    contextp()->threadPoolpOnClone();
}
