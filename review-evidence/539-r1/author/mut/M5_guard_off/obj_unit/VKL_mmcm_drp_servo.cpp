// Verilated -*- C++ -*-
// DESCRIPTION: Verilator output: Model implementation (design independent parts)

#include "VKL_mmcm_drp_servo__pch.h"

//============================================================
// Constructors

VKL_mmcm_drp_servo::VKL_mmcm_drp_servo(VerilatedContext* _vcontextp__, const char* _vcname__)
    : VerilatedModel{*_vcontextp__}
    , vlSymsp{new VKL_mmcm_drp_servo__Syms(contextp(), _vcname__, this)}
    , clk_i{vlSymsp->TOP.clk_i}
    , clk_audio_i{vlSymsp->TOP.clk_audio_i}
    , ps_clk_i{vlSymsp->TOP.ps_clk_i}
    , rst_n{vlSymsp->TOP.rst_n}
    , crf_locked_i{vlSymsp->TOP.crf_locked_i}
    , auto_repair_i{vlSymsp->TOP.auto_repair_i}
    , ps_invert_i{vlSymsp->TOP.ps_invert_i}
    , drp_addr_o{vlSymsp->TOP.drp_addr_o}
    , drp_en_o{vlSymsp->TOP.drp_en_o}
    , drp_we_o{vlSymsp->TOP.drp_we_o}
    , drp_rdy_i{vlSymsp->TOP.drp_rdy_i}
    , mmcm_rst_o{vlSymsp->TOP.mmcm_rst_o}
    , mmcm_locked_i{vlSymsp->TOP.mmcm_locked_i}
    , ps_en_o{vlSymsp->TOP.ps_en_o}
    , ps_incdec_o{vlSymsp->TOP.ps_incdec_o}
    , ps_done_i{vlSymsp->TOP.ps_done_i}
    , clk_src_i{vlSymsp->TOP.clk_src_i}
    , crf_src_idx_i{vlSymsp->TOP.crf_src_idx_i}
    , drp_di_o{vlSymsp->TOP.drp_di_o}
    , drp_do_i{vlSymsp->TOP.drp_do_i}
    , crf_rate_i{vlSymsp->TOP.crf_rate_i}
    , status_o{vlSymsp->TOP.status_o}
    , ptp_now_i{vlSymsp->TOP.ptp_now_i}
    , rootp{&(vlSymsp->TOP)}
{
    // Register model with the context
    contextp()->addModel(this);
}

VKL_mmcm_drp_servo::VKL_mmcm_drp_servo(const char* _vcname__)
    : VKL_mmcm_drp_servo(Verilated::threadContextp(), _vcname__)
{
}

//============================================================
// Destructor

VKL_mmcm_drp_servo::~VKL_mmcm_drp_servo() {
    delete vlSymsp;
}

//============================================================
// Evaluation function

#ifdef VL_DEBUG
void VKL_mmcm_drp_servo___024root___eval_debug_assertions(VKL_mmcm_drp_servo___024root* vlSelf);
#endif  // VL_DEBUG
void VKL_mmcm_drp_servo___024root___eval_static(VKL_mmcm_drp_servo___024root* vlSelf);
void VKL_mmcm_drp_servo___024root___eval_initial(VKL_mmcm_drp_servo___024root* vlSelf);
void VKL_mmcm_drp_servo___024root___eval_settle(VKL_mmcm_drp_servo___024root* vlSelf);
void VKL_mmcm_drp_servo___024root___eval(VKL_mmcm_drp_servo___024root* vlSelf);

void VKL_mmcm_drp_servo::eval_step() {
    VL_DEBUG_IF(VL_DBG_MSGF("+++++TOP Evaluate VKL_mmcm_drp_servo::eval_step\n"); );
#ifdef VL_DEBUG
    // Debug assertions
    VKL_mmcm_drp_servo___024root___eval_debug_assertions(&(vlSymsp->TOP));
#endif  // VL_DEBUG
    vlSymsp->__Vm_deleter.deleteAll();
    if (VL_UNLIKELY(!vlSymsp->__Vm_didInit)) {
        VL_DEBUG_IF(VL_DBG_MSGF("+ Initial\n"););
        VKL_mmcm_drp_servo___024root___eval_static(&(vlSymsp->TOP));
        VKL_mmcm_drp_servo___024root___eval_initial(&(vlSymsp->TOP));
        VKL_mmcm_drp_servo___024root___eval_settle(&(vlSymsp->TOP));
        vlSymsp->__Vm_didInit = true;
    }
    VL_DEBUG_IF(VL_DBG_MSGF("+ Eval\n"););
    VKL_mmcm_drp_servo___024root___eval(&(vlSymsp->TOP));
    // Evaluate cleanup
    Verilated::endOfEval(vlSymsp->__Vm_evalMsgQp);
}

//============================================================
// Events and timing
bool VKL_mmcm_drp_servo::eventsPending() { return false; }

uint64_t VKL_mmcm_drp_servo::nextTimeSlot() {
    VL_FATAL_MT(__FILE__, __LINE__, "", "No delays in the design");
    return 0;
}

//============================================================
// Utilities

const char* VKL_mmcm_drp_servo::name() const {
    return vlSymsp->name();
}

//============================================================
// Invoke final blocks

void VKL_mmcm_drp_servo___024root___eval_final(VKL_mmcm_drp_servo___024root* vlSelf);

VL_ATTR_COLD void VKL_mmcm_drp_servo::final() {
    contextp()->executingFinal(true);
    VKL_mmcm_drp_servo___024root___eval_final(&(vlSymsp->TOP));
    contextp()->executingFinal(false);
}

//============================================================
// Implementations of abstract methods from VerilatedModel

const char* VKL_mmcm_drp_servo::hierName() const { return vlSymsp->name(); }
const char* VKL_mmcm_drp_servo::modelName() const { return "VKL_mmcm_drp_servo"; }
unsigned VKL_mmcm_drp_servo::threads() const { return 1; }
void VKL_mmcm_drp_servo::prepareClone() const { contextp()->prepareClone(); }
void VKL_mmcm_drp_servo::atClone() const {
    contextp()->threadPoolpOnClone();
}
