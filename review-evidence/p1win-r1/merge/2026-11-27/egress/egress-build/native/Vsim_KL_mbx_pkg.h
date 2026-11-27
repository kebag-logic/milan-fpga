// Verilated -*- C++ -*-
// DESCRIPTION: Verilator output: Design internal header
// See Vsim.h for the primary calling header

#ifndef VERILATED_VSIM_KL_MBX_PKG_H_
#define VERILATED_VSIM_KL_MBX_PKG_H_  // guard

#include "verilated.h"


class Vsim__Syms;

class alignas(VL_CACHE_LINE_BYTES) Vsim_KL_mbx_pkg final {
  public:

    // INTERNAL VARIABLES
    Vsim__Syms* vlSymsp;
    const char* vlNamep;

    // PARAMETERS
    static constexpr VlUnpacked<IData/*31:0*/, 5> __PVT__MBX_CH_RX_WORDS_TBL_C = {{
        0x00000100U, 0x00000100U, 0x00000200U, 0x00000080U,
        0x00000400U
    }};
    static constexpr VlUnpacked<IData/*31:0*/, 5> __PVT__MBX_CH_TX_WORDS_TBL_C = {{
        0x00000080U, 0x00000100U, 0x00000200U, 0x00000080U,
        0x00000200U
    }};
    static constexpr VlUnpacked<IData/*31:0*/, 5> __PVT__MBX_CH_MAX_FRAME_BYTES_TBL_C = {{
        0x00000080U, 0x00000080U, 0x000005eaU, 0x00000040U,
        0x000005eaU
    }};
    static constexpr VlUnpacked<IData/*31:0*/, 15> __PVT__MBX_TERM_TEST_TBL_C = {{
        3U, 2U, 5U, 2U,
        2U, 0U, 2U, 2U,
        0U, 4U, 0U, 0U,
        1U, 0U, 0U
    }};
    static constexpr VlUnpacked<IData/*31:0*/, 15> __PVT__MBX_TERM_OFFSET_TBL_C = {{
        0x00000012U, 0x00000012U, 0x00000012U, 0x00000022U,
        0x0000002aU, 0U, 0x00000012U, 0x0000001aU,
        0U, 0x0000001aU, 0U, 0U,
        0U, 0U, 0U
    }};
    static constexpr VlUnpacked<IData/*31:0*/, 15> __PVT__MBX_TERM_MASK_TBL_C = {{
        4U, 4U, 3U, 0x0000ffffU,
        0x0000ffffU, 0U, 0x00005555U, 0x0000aaaaU,
        0U, 0x0000000eU, 0U, 0U,
        0x0000ffffU, 0U, 0U
    }};

    // CONSTRUCTORS
    Vsim_KL_mbx_pkg();
    ~Vsim_KL_mbx_pkg();
    void ctor(Vsim__Syms* symsp, const char* namep);
    void dtor();
    VL_UNCOPYABLE(Vsim_KL_mbx_pkg);

    // INTERNAL METHODS
    void __Vconfigure(bool first);
};


#endif  // guard
