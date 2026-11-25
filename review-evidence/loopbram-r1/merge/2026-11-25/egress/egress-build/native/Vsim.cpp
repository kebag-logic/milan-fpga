// Verilated -*- C++ -*-
// DESCRIPTION: Verilator output: Model implementation (design independent parts)

#include "Vsim__pch.h"

//============================================================
// Constructors

Vsim::Vsim(VerilatedContext* _vcontextp__, const char* _vcname__)
    : VerilatedModel{*_vcontextp__}
    , vlSymsp{new Vsim__Syms(contextp(), _vcname__, this)}
    , sys_clk{vlSymsp->TOP.sys_clk}
    , sys_reset{vlSymsp->TOP.sys_reset}
    , audio_clk{vlSymsp->TOP.audio_clk}
    , audio_tdm_clk{vlSymsp->TOP.audio_tdm_clk}
    , flash_cs{vlSymsp->TOP.flash_cs}
    , flash_rx_ready{vlSymsp->TOP.flash_rx_ready}
    , flash_rx_valid{vlSymsp->TOP.flash_rx_valid}
    , flash_tx_len{vlSymsp->TOP.flash_tx_len}
    , flash_tx_ready{vlSymsp->TOP.flash_tx_ready}
    , flash_tx_valid{vlSymsp->TOP.flash_tx_valid}
    , flash_tx_width{vlSymsp->TOP.flash_tx_width}
    , mbx_amap_wr{vlSymsp->TOP.mbx_amap_wr}
    , mbx_asp_chg{vlSymsp->TOP.mbx_asp_chg}
    , mbx_avb_chg{vlSymsp->TOP.mbx_avb_chg}
    , mbx_domain{vlSymsp->TOP.mbx_domain}
    , mbx_gm_change{vlSymsp->TOP.mbx_gm_change}
    , mbx_host_ack{vlSymsp->TOP.mbx_host_ack}
    , mbx_host_req{vlSymsp->TOP.mbx_host_req}
    , mbx_host_we{vlSymsp->TOP.mbx_host_we}
    , mbx_link_up{vlSymsp->TOP.mbx_link_up}
    , mbx_ms_tick{vlSymsp->TOP.mbx_ms_tick}
    , mbx_rx_data{vlSymsp->TOP.mbx_rx_data}
    , mbx_rx_if{vlSymsp->TOP.mbx_rx_if}
    , mbx_rx_last{vlSymsp->TOP.mbx_rx_last}
    , mbx_rx_ready{vlSymsp->TOP.mbx_rx_ready}
    , mbx_rx_valid{vlSymsp->TOP.mbx_rx_valid}
    , mbx_tx_ch{vlSymsp->TOP.mbx_tx_ch}
    , mbx_tx_data{vlSymsp->TOP.mbx_tx_data}
    , mbx_tx_if{vlSymsp->TOP.mbx_tx_if}
    , mbx_tx_last{vlSymsp->TOP.mbx_tx_last}
    , mbx_tx_ready{vlSymsp->TOP.mbx_tx_ready}
    , mbx_tx_valid{vlSymsp->TOP.mbx_tx_valid}
    , milan_clk{vlSymsp->TOP.milan_clk}
    , serial_sink_data{vlSymsp->TOP.serial_sink_data}
    , serial_sink_ready{vlSymsp->TOP.serial_sink_ready}
    , serial_sink_valid{vlSymsp->TOP.serial_sink_valid}
    , serial_source_data{vlSymsp->TOP.serial_source_data}
    , serial_source_ready{vlSymsp->TOP.serial_source_ready}
    , serial_source_valid{vlSymsp->TOP.serial_source_valid}
    , sim_trace{vlSymsp->TOP.sim_trace}
    , mbx_host_addr{vlSymsp->TOP.mbx_host_addr}
    , flash_rx_data{vlSymsp->TOP.flash_rx_data}
    , flash_tx_data{vlSymsp->TOP.flash_tx_data}
    , mbx_host_rdata{vlSymsp->TOP.mbx_host_rdata}
    , mbx_host_wdata{vlSymsp->TOP.mbx_host_wdata}
    , mbx_gm_id{vlSymsp->TOP.mbx_gm_id}
    , sim{vlSymsp->TOP.sim}
    , __PVT__KL_mbx_pkg{vlSymsp->TOP.__PVT__KL_mbx_pkg}
    , rootp{&(vlSymsp->TOP)}
{
    // Register model with the context
    contextp()->addModel(this);
}

Vsim::Vsim(const char* _vcname__)
    : Vsim(Verilated::threadContextp(), _vcname__)
{
}

//============================================================
// Destructor

Vsim::~Vsim() {
    delete vlSymsp;
}

//============================================================
// Evaluation function

#ifdef VL_DEBUG
void Vsim___024root___eval_debug_assertions(Vsim___024root* vlSelf);
#endif  // VL_DEBUG
void Vsim___024root___eval_static(Vsim___024root* vlSelf);
void Vsim___024root___eval_initial(Vsim___024root* vlSelf);
void Vsim___024root___eval_settle(Vsim___024root* vlSelf);
void Vsim___024root___eval(Vsim___024root* vlSelf);

void Vsim::eval_step() {
    VL_DEBUG_IF(VL_DBG_MSGF("+++++TOP Evaluate Vsim::eval_step\n"); );
#ifdef VL_DEBUG
    // Debug assertions
    Vsim___024root___eval_debug_assertions(&(vlSymsp->TOP));
#endif  // VL_DEBUG
    vlSymsp->__Vm_deleter.deleteAll();
    if (VL_UNLIKELY(!vlSymsp->__Vm_didInit)) {
        VL_DEBUG_IF(VL_DBG_MSGF("+ Initial\n"););
        Vsim___024root___eval_static(&(vlSymsp->TOP));
        Vsim___024root___eval_initial(&(vlSymsp->TOP));
        Vsim___024root___eval_settle(&(vlSymsp->TOP));
        vlSymsp->__Vm_didInit = true;
    }
    VL_DEBUG_IF(VL_DBG_MSGF("+ Eval\n"););
    Vsim___024root___eval(&(vlSymsp->TOP));
    // Evaluate cleanup
    Verilated::endOfEval(vlSymsp->__Vm_evalMsgQp);
}

//============================================================
// Events and timing
bool Vsim::eventsPending() { return false; }

uint64_t Vsim::nextTimeSlot() {
    VL_FATAL_MT(__FILE__, __LINE__, "", "No delays in the design");
    return 0;
}

//============================================================
// Utilities

const char* Vsim::name() const {
    return vlSymsp->name();
}

//============================================================
// Invoke final blocks

void Vsim___024root___eval_final(Vsim___024root* vlSelf);

VL_ATTR_COLD void Vsim::final() {
    contextp()->executingFinal(true);
    Vsim___024root___eval_final(&(vlSymsp->TOP));
    contextp()->executingFinal(false);
}

//============================================================
// Implementations of abstract methods from VerilatedModel

const char* Vsim::hierName() const { return vlSymsp->name(); }
const char* Vsim::modelName() const { return "Vsim"; }
unsigned Vsim::threads() const { return 1; }
void Vsim::prepareClone() const { contextp()->prepareClone(); }
void Vsim::atClone() const {
    contextp()->threadPoolpOnClone();
}
