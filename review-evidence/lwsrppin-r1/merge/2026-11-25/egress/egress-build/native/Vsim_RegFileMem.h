// Verilated -*- C++ -*-
// DESCRIPTION: Verilator output: Design internal header
// See Vsim.h for the primary calling header

#ifndef VERILATED_VSIM_REGFILEMEM_H_
#define VERILATED_VSIM_REGFILEMEM_H_  // guard

#include "verilated.h"


class Vsim__Syms;

class alignas(VL_CACHE_LINE_BYTES) Vsim_RegFileMem final {
  public:

    // DESIGN SPECIFIC STATE
    CData/*0:0*/ __PVT__io_writes_0_valid;
    CData/*4:0*/ __PVT__io_writes_0_address;
    CData/*0:0*/ __PVT__io_reads_0_valid;
    CData/*4:0*/ __PVT__io_reads_0_address;
    CData/*0:0*/ __PVT__io_reads_1_valid;
    CData/*4:0*/ __PVT__io_reads_1_address;
    CData/*0:0*/ __PVT__litex_clk;
    CData/*0:0*/ __PVT__cpuResetCtrl_reset;
    SData/*15:0*/ __PVT__io_writes_0_uopId;
    IData/*31:0*/ __PVT__io_writes_0_data;
    IData/*31:0*/ __PVT__io_reads_0_data;
    IData/*31:0*/ __PVT__io_reads_1_data;
    IData/*31:0*/ __PVT__asMem_ram_spinal_port1;
    IData/*31:0*/ __PVT__asMem_ram_spinal_port2;
    VlUnpacked<IData/*31:0*/, 32> asMem_ram;

    // INTERNAL VARIABLES
    Vsim__Syms* vlSymsp;
    const char* vlNamep;

    // CONSTRUCTORS
    Vsim_RegFileMem();
    ~Vsim_RegFileMem();
    void ctor(Vsim__Syms* symsp, const char* namep);
    void dtor();
    VL_UNCOPYABLE(Vsim_RegFileMem);

    // INTERNAL METHODS
    void __Vconfigure(bool first);
};


#endif  // guard
