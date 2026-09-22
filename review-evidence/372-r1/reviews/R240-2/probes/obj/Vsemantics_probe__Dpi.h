// Verilated -*- C++ -*-
// DESCRIPTION: Verilator output: Prototypes for DPI import and export functions.
//
// Verilator includes this file in all generated .cpp files that use DPI functions.
// Manually include this file where DPI .c import functions are declared to ensure
// the C functions match the expectations of the DPI imports.

#ifndef VERILATED_VSEMANTICS_PROBE__DPI_H_
#define VERILATED_VSEMANTICS_PROBE__DPI_H_  // guard

#include "svdpi.h"

#ifdef __cplusplus
extern "C" {
#endif


    // DPI IMPORTS
    // DPI import at $VALIDATION_STORAGE/reviews/r240-372-r2/tb/common/sva/axis_stream_source_sva.sv:60:40
    extern void axis_sva_witness(const char* rule_name, svBit nonvacuous);
    // DPI import at $WORKSPACE_HOME/milan-fpga-management/2026-09-22/372-r2-r240/probes/semantics_probe.sv:9:40
    extern void probe_result(const char* rule_name, svBit passed);

#ifdef __cplusplus
}
#endif

#endif  // guard
