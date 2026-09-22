// Verilated -*- C++ -*-
// DESCRIPTION: Verilator output: Prototypes for DPI import and export functions.
//
// Verilator includes this file in all generated .cpp files that use DPI functions.
// Manually include this file where DPI .c import functions are declared to ensure
// the C functions match the expectations of the DPI imports.

#ifndef VERILATED_VAXIS_MUX_RR_2IN_1OUT__DPI_H_
#define VERILATED_VAXIS_MUX_RR_2IN_1OUT__DPI_H_  // guard

#include "svdpi.h"

#ifdef __cplusplus
extern "C" {
#endif


    // DPI IMPORTS
    // DPI import at ../../common/sva/axis_mux_rr_2in_1out_sva.sv:75:40
    extern void axis_sva_witness(const char* rule_name, svBit nonvacuous);

#ifdef __cplusplus
}
#endif

#endif  // guard
