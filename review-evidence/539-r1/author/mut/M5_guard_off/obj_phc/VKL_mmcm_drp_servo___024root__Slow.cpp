// Verilated -*- C++ -*-
// DESCRIPTION: Verilator output: Design implementation internals
// See VKL_mmcm_drp_servo.h for the primary calling header

#include "VKL_mmcm_drp_servo__pch.h"

// Parameter definitions for VKL_mmcm_drp_servo___024root
constexpr CData/*6:0*/ VKL_mmcm_drp_servo___024root::KL_mmcm_drp_servo__DOT__DADDR_C0R1_C;
constexpr CData/*6:0*/ VKL_mmcm_drp_servo___024root::KL_mmcm_drp_servo__DOT__DADDR_C0R2_C;
constexpr CData/*6:0*/ VKL_mmcm_drp_servo___024root::KL_mmcm_drp_servo__DOT__DADDR_POWER_C;
constexpr SData/*15:0*/ VKL_mmcm_drp_servo___024root::KL_mmcm_drp_servo__DOT__CFG_C0R1_P;
constexpr SData/*15:0*/ VKL_mmcm_drp_servo___024root::KL_mmcm_drp_servo__DOT__CFG_C0R1_MASK_P;
constexpr SData/*15:0*/ VKL_mmcm_drp_servo___024root::KL_mmcm_drp_servo__DOT__CFG_C0R2_P;
constexpr SData/*15:0*/ VKL_mmcm_drp_servo___024root::KL_mmcm_drp_servo__DOT__CFG_C0R2_MASK_P;
constexpr SData/*15:0*/ VKL_mmcm_drp_servo___024root::KL_mmcm_drp_servo__DOT__POWER_ALL_C;
constexpr IData/*31:0*/ VKL_mmcm_drp_servo___024root::KL_mmcm_drp_servo__DOT__CLK_FREQ_HZ_P;
constexpr IData/*31:0*/ VKL_mmcm_drp_servo___024root::KL_mmcm_drp_servo__DOT__TICK_CYC_P;
constexpr IData/*31:0*/ VKL_mmcm_drp_servo___024root::KL_mmcm_drp_servo__DOT__WIN_LOG2_P;
constexpr IData/*31:0*/ VKL_mmcm_drp_servo___024root::KL_mmcm_drp_servo__DOT__NORM_SHIFT_P;
constexpr IData/*31:0*/ VKL_mmcm_drp_servo___024root::KL_mmcm_drp_servo__DOT__KI_SHIFT_P;
constexpr IData/*31:0*/ VKL_mmcm_drp_servo___024root::KL_mmcm_drp_servo__DOT__KP_SHIFT_P;
constexpr IData/*31:0*/ VKL_mmcm_drp_servo___024root::KL_mmcm_drp_servo__DOT__U_MAX_P;
constexpr IData/*31:0*/ VKL_mmcm_drp_servo___024root::KL_mmcm_drp_servo__DOT__SLEW_MAX_P;
constexpr IData/*31:0*/ VKL_mmcm_drp_servo___024root::KL_mmcm_drp_servo__DOT__LOCK_THR_P;
constexpr IData/*31:0*/ VKL_mmcm_drp_servo___024root::KL_mmcm_drp_servo__DOT__LOCK_WIN_P;
constexpr IData/*31:0*/ VKL_mmcm_drp_servo___024root::KL_mmcm_drp_servo__DOT__GAIN_NUM_P;
constexpr IData/*31:0*/ VKL_mmcm_drp_servo___024root::KL_mmcm_drp_servo__DOT__PS_TOUT_CYC_P;
constexpr IData/*31:0*/ VKL_mmcm_drp_servo___024root::KL_mmcm_drp_servo__DOT__RELOCK_TOUT_P;
constexpr IData/*31:0*/ VKL_mmcm_drp_servo___024root::KL_mmcm_drp_servo__DOT__WIN_TICKS_C;
constexpr IData/*31:0*/ VKL_mmcm_drp_servo___024root::KL_mmcm_drp_servo__DOT__ECLAMP_C;
constexpr IData/*31:0*/ VKL_mmcm_drp_servo___024root::KL_mmcm_drp_servo__DOT__GUARD_THR_C;
constexpr IData/*31:0*/ VKL_mmcm_drp_servo___024root::KL_mmcm_drp_servo__DOT__DISC_MAX_C;
constexpr IData/*31:0*/ VKL_mmcm_drp_servo___024root::KL_mmcm_drp_servo__DOT__STEP_DET_NS_C;
constexpr IData/*31:0*/ VKL_mmcm_drp_servo___024root::KL_mmcm_drp_servo__DOT__u_batch_hs__DOT__WIDTH;
constexpr IData/*31:0*/ VKL_mmcm_drp_servo___024root::KL_mmcm_drp_servo__DOT__u_batch_hs__DOT__DEST_SYNC_FF;
constexpr IData/*31:0*/ VKL_mmcm_drp_servo___024root::KL_mmcm_drp_servo__DOT__u_batch_hs__DOT__SRC_SYNC_FF;
constexpr IData/*31:0*/ VKL_mmcm_drp_servo___024root::KL_mmcm_drp_servo__DOT__u_tick_cdc__DOT__DEST_SYNC_FF;
constexpr QData/*63:0*/ VKL_mmcm_drp_servo___024root::KL_mmcm_drp_servo__DOT__NOM_WIN_NS_P;


void VKL_mmcm_drp_servo___024root___ctor_var_reset(VKL_mmcm_drp_servo___024root* vlSelf);

VKL_mmcm_drp_servo___024root::VKL_mmcm_drp_servo___024root(VKL_mmcm_drp_servo__Syms* symsp, const char* namep)
 {
    vlSymsp = symsp;
    vlNamep = strdup(namep);
    // Reset structure values
    VKL_mmcm_drp_servo___024root___ctor_var_reset(this);
}

void VKL_mmcm_drp_servo___024root::__Vconfigure(bool first) {
    (void)first;  // Prevent unused variable warning
}

VKL_mmcm_drp_servo___024root::~VKL_mmcm_drp_servo___024root() {
    VL_DO_DANGLING(std::free(const_cast<char*>(vlNamep)), vlNamep);
}
