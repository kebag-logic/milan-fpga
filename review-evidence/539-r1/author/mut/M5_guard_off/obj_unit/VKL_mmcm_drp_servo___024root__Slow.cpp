// Verilated -*- C++ -*-
// DESCRIPTION: Verilator output: Design implementation internals
// See VKL_mmcm_drp_servo.h for the primary calling header

#include "VKL_mmcm_drp_servo__pch.h"

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
