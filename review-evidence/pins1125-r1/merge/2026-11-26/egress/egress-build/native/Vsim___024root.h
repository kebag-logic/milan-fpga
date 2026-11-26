// Verilated -*- C++ -*-
// DESCRIPTION: Verilator output: Design internal header
// See Vsim.h for the primary calling header

#ifndef VERILATED_VSIM___024ROOT_H_
#define VERILATED_VSIM___024ROOT_H_  // guard

#include "verilated.h"
class Vsim_KL_mbx_pkg;
class Vsim_sim;


class Vsim__Syms;

class alignas(VL_CACHE_LINE_BYTES) Vsim___024root final {
  public:
    // CELLS
    Vsim_sim* sim;
    Vsim_KL_mbx_pkg* __PVT__KL_mbx_pkg;

    // DESIGN SPECIFIC STATE
    // Anonymous structures to workaround compiler member-count bugs
    struct {
        VL_IN8(sys_clk,0,0);
        VL_IN8(sys_reset,0,0);
        VL_IN8(audio_clk,0,0);
        VL_IN8(audio_tdm_clk,0,0);
        VL_OUT8(flash_cs,0,0);
        VL_OUT8(flash_rx_ready,0,0);
        VL_IN8(flash_rx_valid,0,0);
        VL_OUT8(flash_tx_len,5,0);
        VL_IN8(flash_tx_ready,0,0);
        VL_OUT8(flash_tx_valid,0,0);
        VL_OUT8(flash_tx_width,3,0);
        VL_IN8(mbx_amap_wr,0,0);
        VL_IN8(mbx_asp_chg,0,0);
        VL_IN8(mbx_avb_chg,0,0);
        VL_IN8(mbx_domain,7,0);
        VL_IN8(mbx_gm_change,0,0);
        VL_OUT8(mbx_host_ack,0,0);
        VL_OUT8(mbx_host_req,0,0);
        VL_OUT8(mbx_host_we,0,0);
        VL_IN8(mbx_link_up,0,0);
        VL_OUT8(mbx_ms_tick,0,0);
        VL_IN8(mbx_rx_data,7,0);
        VL_IN8(mbx_rx_if,0,0);
        VL_IN8(mbx_rx_last,0,0);
        VL_OUT8(mbx_rx_ready,0,0);
        VL_IN8(mbx_rx_valid,0,0);
        VL_OUT8(mbx_tx_ch,2,0);
        VL_OUT8(mbx_tx_data,7,0);
        VL_OUT8(mbx_tx_if,0,0);
        VL_OUT8(mbx_tx_last,0,0);
        VL_IN8(mbx_tx_ready,0,0);
        VL_OUT8(mbx_tx_valid,0,0);
        VL_IN8(milan_clk,0,0);
        VL_IN8(serial_sink_data,7,0);
        VL_OUT8(serial_sink_ready,0,0);
        VL_IN8(serial_sink_valid,0,0);
        VL_OUT8(serial_source_data,7,0);
        VL_IN8(serial_source_ready,0,0);
        VL_OUT8(serial_source_valid,0,0);
        VL_IN8(sim_trace,0,0);
        CData/*0:0*/ __VstlFirstIteration;
        CData/*0:0*/ __VstlPhaseResult;
        CData/*0:0*/ __Vtrigprevexpr___TOP__audio_clk__0;
        CData/*0:0*/ __Vtrigprevexpr___TOP__audio_tdm_clk__0;
        CData/*0:0*/ __Vtrigprevexpr___TOP__flash_rx_valid__0;
        CData/*0:0*/ __Vtrigprevexpr___TOP__flash_tx_ready__0;
        CData/*0:0*/ __Vtrigprevexpr___TOP__mbx_amap_wr__0;
        CData/*0:0*/ __Vtrigprevexpr___TOP__mbx_asp_chg__0;
        CData/*0:0*/ __Vtrigprevexpr___TOP__mbx_avb_chg__0;
        CData/*7:0*/ __Vtrigprevexpr___TOP__mbx_domain__0;
        CData/*0:0*/ __Vtrigprevexpr___TOP__mbx_gm_change__0;
        CData/*0:0*/ __Vtrigprevexpr___TOP__mbx_link_up__0;
        CData/*7:0*/ __Vtrigprevexpr___TOP__mbx_rx_data__0;
        CData/*0:0*/ __Vtrigprevexpr___TOP__mbx_rx_if__0;
        CData/*0:0*/ __Vtrigprevexpr___TOP__mbx_rx_last__0;
        CData/*0:0*/ __Vtrigprevexpr___TOP__mbx_rx_valid__0;
        CData/*0:0*/ __Vtrigprevexpr___TOP__mbx_tx_ready__0;
        CData/*0:0*/ __Vtrigprevexpr___TOP__milan_clk__0;
        CData/*7:0*/ __Vtrigprevexpr___TOP__serial_sink_data__0;
        CData/*0:0*/ __Vtrigprevexpr___TOP__serial_sink_valid__0;
        CData/*0:0*/ __Vtrigprevexpr___TOP__serial_source_ready__0;
        CData/*0:0*/ __Vtrigprevexpr___TOP__sim_trace__0;
        CData/*0:0*/ __Vtrigprevexpr___TOP__sys_clk__0;
        CData/*0:0*/ __Vtrigprevexpr___TOP__sys_reset__0;
    };
    struct {
        CData/*0:0*/ __VicoDidInit;
        CData/*0:0*/ __VicoPhaseResult;
        CData/*0:0*/ __Vtrigprevexpr___TOP__sys_clk__1;
        CData/*0:0*/ __Vtrigprevexpr___TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952____PVT__litex_reset__0;
        CData/*0:0*/ __Vtrigprevexpr___TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952____PVT__cpuResetCtrl_fiber_aggregator_asyncBuffers_0__DOT__buffers_1__0;
        CData/*0:0*/ __Vtrigprevexpr___TOP__sim__VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952____PVT__cpuResetCtrl_fiber_buffer__DOT__buffers_1__0;
        CData/*0:0*/ __Vtrigprevexpr_h8ac6c1f5__1;
        CData/*0:0*/ __VactPhaseResult;
        CData/*0:0*/ __VnbaPhaseResult;
        VL_OUT16(mbx_host_addr,12,0);
        VL_IN(flash_rx_data,31,0);
        VL_OUT(flash_tx_data,31,0);
        VL_OUT(mbx_host_rdata,31,0);
        VL_OUT(mbx_host_wdata,31,0);
        IData/*31:0*/ __Vtrigprevexpr___TOP__flash_rx_data__0;
        IData/*31:0*/ __VactIterCount;
        VL_IN64(mbx_gm_id,63,0);
        QData/*63:0*/ __Vtrigprevexpr___TOP__mbx_gm_id__0;
        VlUnpacked<QData/*63:0*/, 1> __VstlTriggered;
        VlUnpacked<QData/*63:0*/, 2> __VicoTriggered;
        VlUnpacked<QData/*63:0*/, 1> __VactTriggered;
        VlUnpacked<QData/*63:0*/, 1> __VnbaTriggered;
    };

    // INTERNAL VARIABLES
    Vsim__Syms* vlSymsp;
    const char* vlNamep;

    // CONSTRUCTORS
    Vsim___024root(Vsim__Syms* symsp, const char* namep);
    ~Vsim___024root();
    VL_UNCOPYABLE(Vsim___024root);

    // INTERNAL METHODS
    void __Vconfigure(bool first);
};


#endif  // guard
