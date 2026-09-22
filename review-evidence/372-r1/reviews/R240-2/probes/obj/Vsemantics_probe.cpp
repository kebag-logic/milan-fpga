// Verilated -*- C++ -*-
// DESCRIPTION: Verilator output: Model implementation (design independent parts)

#include "Vsemantics_probe__pch.h"

//============================================================
// Constructors

Vsemantics_probe::Vsemantics_probe(VerilatedContext* _vcontextp__, const char* _vcname__)
    : VerilatedModel{*_vcontextp__}
    , vlSymsp{new Vsemantics_probe__Syms(contextp(), _vcname__, this)}
    , clk{vlSymsp->TOP.clk}
    , rst_n{vlSymsp->TOP.rst_n}
    , valid{vlSymsp->TOP.valid}
    , ready{vlSymsp->TOP.ready}
    , data{vlSymsp->TOP.data}
    , keep{vlSymsp->TOP.keep}
    , last{vlSymsp->TOP.last}
    , rootp{&(vlSymsp->TOP)}
{
    // Register model with the context
    contextp()->addModel(this);
}

Vsemantics_probe::Vsemantics_probe(const char* _vcname__)
    : Vsemantics_probe(Verilated::threadContextp(), _vcname__)
{
}

//============================================================
// Destructor

Vsemantics_probe::~Vsemantics_probe() {
    delete vlSymsp;
}

//============================================================
// Evaluation function

#ifdef VL_DEBUG
void Vsemantics_probe___024root___eval_debug_assertions(Vsemantics_probe___024root* vlSelf);
#endif  // VL_DEBUG
void Vsemantics_probe___024root___eval_static(Vsemantics_probe___024root* vlSelf);
void Vsemantics_probe___024root___eval_initial(Vsemantics_probe___024root* vlSelf);
void Vsemantics_probe___024root___eval_settle(Vsemantics_probe___024root* vlSelf);
void Vsemantics_probe___024root___eval(Vsemantics_probe___024root* vlSelf);

void Vsemantics_probe::eval_step() {
    VL_DEBUG_IF(VL_DBG_MSGF("+++++TOP Evaluate Vsemantics_probe::eval_step\n"); );
#ifdef VL_DEBUG
    // Debug assertions
    Vsemantics_probe___024root___eval_debug_assertions(&(vlSymsp->TOP));
#endif  // VL_DEBUG
    vlSymsp->__Vm_deleter.deleteAll();
    if (VL_UNLIKELY(!vlSymsp->__Vm_didInit)) {
        VL_DEBUG_IF(VL_DBG_MSGF("+ Initial\n"););
        Vsemantics_probe___024root___eval_static(&(vlSymsp->TOP));
        Vsemantics_probe___024root___eval_initial(&(vlSymsp->TOP));
        Vsemantics_probe___024root___eval_settle(&(vlSymsp->TOP));
        vlSymsp->__Vm_didInit = true;
    }
    VL_DEBUG_IF(VL_DBG_MSGF("+ Eval\n"););
    Vsemantics_probe___024root___eval(&(vlSymsp->TOP));
    // Evaluate cleanup
    Verilated::endOfEval(vlSymsp->__Vm_evalMsgQp);
}

//============================================================
// Events and timing
bool Vsemantics_probe::eventsPending() { return false; }

uint64_t Vsemantics_probe::nextTimeSlot() {
    VL_FATAL_MT(__FILE__, __LINE__, "", "No delays in the design");
    return 0;
}

//============================================================
// Utilities

const char* Vsemantics_probe::name() const {
    return vlSymsp->name();
}

//============================================================
// Invoke final blocks

void Vsemantics_probe___024root___eval_final(Vsemantics_probe___024root* vlSelf);

VL_ATTR_COLD void Vsemantics_probe::final() {
    contextp()->executingFinal(true);
    Vsemantics_probe___024root___eval_final(&(vlSymsp->TOP));
    contextp()->executingFinal(false);
}

//============================================================
// Implementations of abstract methods from VerilatedModel

const char* Vsemantics_probe::hierName() const { return vlSymsp->name(); }
const char* Vsemantics_probe::modelName() const { return "Vsemantics_probe"; }
unsigned Vsemantics_probe::threads() const { return 1; }
void Vsemantics_probe::prepareClone() const { contextp()->prepareClone(); }
void Vsemantics_probe::atClone() const {
    contextp()->threadPoolpOnClone();
}
