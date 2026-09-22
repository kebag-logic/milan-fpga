// Verilated -*- C++ -*-
// DESCRIPTION: Verilator output: Design internal header
// See Vptp_ts_top.h for the primary calling header

#ifndef VERILATED_VPTP_TS_TOP___024ROOT_H_
#define VERILATED_VPTP_TS_TOP___024ROOT_H_  // guard

#include "verilated.h"
class Vptp_ts_top_axi_stream_if;


class Vptp_ts_top__Syms;

class alignas(VL_CACHE_LINE_BYTES) Vptp_ts_top___024root final {
  public:
    // CELLS
    Vptp_ts_top_axi_stream_if* __PVT__ptp_ts_top__DOT__s_axis_tx;
    Vptp_ts_top_axi_stream_if* __PVT__ptp_ts_top__DOT__s_axis_rx;
    Vptp_ts_top_axi_stream_if* __PVT__ptp_ts_top__DOT__m_axis_tx;
    Vptp_ts_top_axi_stream_if* __PVT__ptp_ts_top__DOT__m_axis_rx;
    Vptp_ts_top_axi_stream_if* __PVT__ptp_ts_top__DOT__ts_m_axis_tx;
    Vptp_ts_top_axi_stream_if* __PVT__ptp_ts_top__DOT__ts_m_axis_rx;
    Vptp_ts_top_axi_stream_if* __PVT__ptp_ts_top__DOT__ts_tx_buffered;
    Vptp_ts_top_axi_stream_if* __PVT__ptp_ts_top__DOT__ts_rx_buffered;
    Vptp_ts_top_axi_stream_if* __PVT__ptp_ts_top__DOT__ts_switch_to_fifo;

    // DESIGN SPECIFIC STATE
    // Anonymous structures to workaround compiler member-count bugs
    struct {
        VL_IN8(gtx_clk,0,0);
        VL_IN8(axis_clk,0,0);
        VL_IN8(gtx_resetn,0,0);
        VL_IN8(axis_resetn,0,0);
        VL_IN8(i_ptp_enable,0,0);
        VL_IN8(i_ptp_cmd_load,0,0);
        VL_IN8(i_ptp_cmd_adjust,0,0);
        VL_IN8(i_ptp_cmd_snapshot,0,0);
        VL_OUT8(o_ptp_tod_rd_valid,0,0);
        VL_OUT8(o_tx_ts_ready,0,0);
        VL_IN8(s_axis_tx_tvalid,0,0);
        VL_OUT8(s_axis_tx_tready,0,0);
        VL_IN8(s_axis_tx_tlast,0,0);
        VL_IN8(s_axis_tx_tkeep,7,0);
        VL_OUT8(m_axis_tx_tvalid,0,0);
        VL_IN8(m_axis_tx_tready,0,0);
        VL_OUT8(m_axis_tx_tlast,0,0);
        VL_OUT8(m_axis_tx_tkeep,7,0);
        VL_IN8(s_axis_rx_tvalid,0,0);
        VL_OUT8(s_axis_rx_tready,0,0);
        VL_IN8(s_axis_rx_tlast,0,0);
        VL_IN8(s_axis_rx_tkeep,7,0);
        VL_OUT8(m_axis_rx_tvalid,0,0);
        VL_IN8(m_axis_rx_tready,0,0);
        VL_OUT8(m_axis_rx_tlast,0,0);
        VL_OUT8(m_axis_rx_tkeep,7,0);
        VL_OUT8(ts_m_axis_tvalid,0,0);
        VL_IN8(ts_m_axis_tready,0,0);
        VL_OUT8(ts_m_axis_tlast,0,0);
        VL_OUT8(ts_m_axis_tkeep,7,0);
        CData/*0:0*/ ptp_ts_top__DOT__tx_ts_ready_r;
        CData/*7:0*/ ptp_ts_top__DOT____Vcellout__axis_tx_rx_ts_switch_rr__m_tkeep;
        CData/*0:0*/ ptp_ts_top__DOT____Vcellout__axis_tx_rx_ts_switch_rr__m_tlast;
        CData/*0:0*/ ptp_ts_top__DOT____Vcellout__axis_tx_rx_ts_switch_rr__m_tvalid;
        CData/*1:0*/ ptp_ts_top__DOT__ts_metadata_drain_fifo__DOT__wr_ptr_reg;
        CData/*1:0*/ ptp_ts_top__DOT__ts_metadata_drain_fifo__DOT__wr_ptr_commit_reg;
        CData/*1:0*/ ptp_ts_top__DOT__ts_metadata_drain_fifo__DOT__rd_ptr_reg;
        CData/*1:0*/ ptp_ts_top__DOT__ts_metadata_drain_fifo__DOT__m_axis_tvalid_pipe_reg;
        CData/*0:0*/ ptp_ts_top__DOT__ts_metadata_drain_fifo__DOT__mark_frame_reg;
        CData/*1:0*/ ptp_ts_top__DOT__rx_ts_buffer__DOT__wr_ptr_reg;
        CData/*1:0*/ ptp_ts_top__DOT__rx_ts_buffer__DOT__wr_ptr_commit_reg;
        CData/*1:0*/ ptp_ts_top__DOT__rx_ts_buffer__DOT__rd_ptr_reg;
        CData/*1:0*/ ptp_ts_top__DOT__rx_ts_buffer__DOT__m_axis_tvalid_pipe_reg;
        CData/*0:0*/ ptp_ts_top__DOT__rx_ts_buffer__DOT__mark_frame_reg;
        CData/*1:0*/ ptp_ts_top__DOT__tx_ts_buffer__DOT__wr_ptr_reg;
        CData/*1:0*/ ptp_ts_top__DOT__tx_ts_buffer__DOT__wr_ptr_commit_reg;
        CData/*1:0*/ ptp_ts_top__DOT__tx_ts_buffer__DOT__rd_ptr_reg;
        CData/*1:0*/ ptp_ts_top__DOT__tx_ts_buffer__DOT__m_axis_tvalid_pipe_reg;
        CData/*0:0*/ ptp_ts_top__DOT__tx_ts_buffer__DOT__mark_frame_reg;
        CData/*1:0*/ ptp_ts_top__DOT__axis_tx_rx_ts_switch_rr__DOT__state;
        CData/*0:0*/ ptp_ts_top__DOT__axis_tx_rx_ts_switch_rr__DOT__last_served;
        CData/*0:0*/ ptp_ts_top__DOT__ptp_ts_rx__DOT__start_packet;
        CData/*6:0*/ ptp_ts_top__DOT__ptp_ts_rx__DOT__byte_counter;
        CData/*0:0*/ ptp_ts_top__DOT__ptp_ts_rx__DOT__eth_match;
        CData/*0:0*/ ptp_ts_top__DOT__ptp_ts_rx__DOT__eth_type_valid;
        CData/*3:0*/ ptp_ts_top__DOT__ptp_ts_rx__DOT__msg_type;
        CData/*0:0*/ ptp_ts_top__DOT__ptp_ts_rx__DOT__ptp_seq_id_valid;
        CData/*0:0*/ ptp_ts_top__DOT__ptp_ts_rx__DOT__vlan_tagged;
        CData/*0:0*/ ptp_ts_top__DOT__ptp_ts_rx__DOT__beat_acc;
        CData/*3:0*/ ptp_ts_top__DOT__ptp_ts_rx__DOT__q0_mt;
        CData/*3:0*/ ptp_ts_top__DOT__ptp_ts_rx__DOT__q1_mt;
        CData/*1:0*/ ptp_ts_top__DOT__ptp_ts_rx__DOT__rec_lvl;
        CData/*0:0*/ ptp_ts_top__DOT__ptp_ts_rx__DOT__rec_push;
        CData/*1:0*/ ptp_ts_top__DOT__ptp_ts_rx__DOT__ts_state;
    };
    struct {
        CData/*3:0*/ ptp_ts_top__DOT__ptp_ts_rx__DOT__cur_mt;
        CData/*0:0*/ ptp_ts_top__DOT__ptp_ts_rx__DOT__pop_r;
        CData/*0:0*/ ptp_ts_top__DOT__ptp_ts_tx__DOT__start_packet;
        CData/*6:0*/ ptp_ts_top__DOT__ptp_ts_tx__DOT__byte_counter;
        CData/*0:0*/ ptp_ts_top__DOT__ptp_ts_tx__DOT__eth_match;
        CData/*0:0*/ ptp_ts_top__DOT__ptp_ts_tx__DOT__eth_type_valid;
        CData/*3:0*/ ptp_ts_top__DOT__ptp_ts_tx__DOT__msg_type;
        CData/*0:0*/ ptp_ts_top__DOT__ptp_ts_tx__DOT__ptp_seq_id_valid;
        CData/*0:0*/ ptp_ts_top__DOT__ptp_ts_tx__DOT__vlan_tagged;
        CData/*0:0*/ ptp_ts_top__DOT__ptp_ts_tx__DOT__beat_acc;
        CData/*3:0*/ ptp_ts_top__DOT__ptp_ts_tx__DOT__q0_mt;
        CData/*3:0*/ ptp_ts_top__DOT__ptp_ts_tx__DOT__q1_mt;
        CData/*1:0*/ ptp_ts_top__DOT__ptp_ts_tx__DOT__rec_lvl;
        CData/*0:0*/ ptp_ts_top__DOT__ptp_ts_tx__DOT__rec_push;
        CData/*1:0*/ ptp_ts_top__DOT__ptp_ts_tx__DOT__ts_state;
        CData/*3:0*/ ptp_ts_top__DOT__ptp_ts_tx__DOT__cur_mt;
        CData/*0:0*/ ptp_ts_top__DOT__ptp_ts_tx__DOT__pop_r;
        CData/*0:0*/ ptp_ts_top__DOT__ts_counter__DOT__tod_snapshot_valid;
        CData/*0:0*/ ptp_ts_top__DOT__ptp_sync__DOT__en_meta;
        CData/*0:0*/ ptp_ts_top__DOT__ptp_sync__DOT__en_sync;
        CData/*0:0*/ ptp_ts_top__DOT__ptp_sync__DOT__load_tgl;
        CData/*0:0*/ ptp_ts_top__DOT__ptp_sync__DOT__adj_tgl;
        CData/*0:0*/ ptp_ts_top__DOT__ptp_sync__DOT__snap_tgl;
        CData/*2:0*/ ptp_ts_top__DOT__ptp_sync__DOT__load_s;
        CData/*2:0*/ ptp_ts_top__DOT__ptp_sync__DOT__adj_s;
        CData/*2:0*/ ptp_ts_top__DOT__ptp_sync__DOT__snap_s;
        CData/*0:0*/ ptp_ts_top__DOT__ptp_sync__DOT__load_pulse_q;
        CData/*0:0*/ ptp_ts_top__DOT__ptp_sync__DOT__adj_pulse_q;
        CData/*0:0*/ ptp_ts_top__DOT__ptp_sync__DOT__snap_tgl_ts;
        CData/*2:0*/ ptp_ts_top__DOT__ptp_sync__DOT__snap_ret_s;
        CData/*0:0*/ ptp_ts_top__DOT__ptp_sync__DOT__tod_rd_valid_reg;
        CData/*2:0*/ __Vdly__ptp_ts_top__DOT__ptp_sync__DOT__snap_s;
        CData/*0:0*/ __Vdly__ptp_ts_top__DOT__ptp_sync__DOT__snap_tgl_ts;
        CData/*0:0*/ __VstlFirstIteration;
        CData/*0:0*/ __VstlPhaseResult;
        CData/*0:0*/ __Vtrigprevexpr___TOP__gtx_clk__0;
        CData/*0:0*/ __Vtrigprevexpr___TOP__gtx_resetn__0;
        CData/*0:0*/ __Vtrigprevexpr___TOP__axis_clk__0;
        CData/*0:0*/ __Vtrigprevexpr___TOP__axis_resetn__0;
        CData/*0:0*/ __Vtrigprevexpr___TOP__i_ptp_enable__0;
        CData/*0:0*/ __Vtrigprevexpr___TOP__i_ptp_cmd_load__0;
        CData/*0:0*/ __Vtrigprevexpr___TOP__i_ptp_cmd_adjust__0;
        CData/*0:0*/ __Vtrigprevexpr___TOP__i_ptp_cmd_snapshot__0;
        CData/*0:0*/ __Vtrigprevexpr___TOP__s_axis_tx_tvalid__0;
        CData/*0:0*/ __Vtrigprevexpr___TOP__s_axis_tx_tlast__0;
        CData/*7:0*/ __Vtrigprevexpr___TOP__s_axis_tx_tkeep__0;
        CData/*0:0*/ __Vtrigprevexpr___TOP__m_axis_tx_tready__0;
        CData/*0:0*/ __Vtrigprevexpr___TOP__s_axis_rx_tvalid__0;
        CData/*0:0*/ __Vtrigprevexpr___TOP__s_axis_rx_tlast__0;
        CData/*7:0*/ __Vtrigprevexpr___TOP__s_axis_rx_tkeep__0;
        CData/*0:0*/ __Vtrigprevexpr___TOP__m_axis_rx_tready__0;
        CData/*0:0*/ __Vtrigprevexpr___TOP__ts_m_axis_tready__0;
        CData/*0:0*/ __VicoDidInit;
        CData/*0:0*/ __VicoPhaseResult;
        CData/*0:0*/ __Vtrigprevexpr___TOP__axis_clk__1;
        CData/*0:0*/ __Vtrigprevexpr___TOP__gtx_clk__1;
        CData/*0:0*/ __VactPhaseResult;
        CData/*0:0*/ __VnbaPhaseResult;
        SData/*15:0*/ ptp_ts_top__DOT__ptp_ts_rx__DOT__ptp_seq_id;
        SData/*15:0*/ ptp_ts_top__DOT__ptp_ts_rx__DOT__q0_seq;
        SData/*15:0*/ ptp_ts_top__DOT__ptp_ts_rx__DOT__q1_seq;
        SData/*15:0*/ ptp_ts_top__DOT__ptp_ts_rx__DOT__cur_seq;
        SData/*15:0*/ ptp_ts_top__DOT__ptp_ts_tx__DOT__ptp_seq_id;
        SData/*15:0*/ ptp_ts_top__DOT__ptp_ts_tx__DOT__q0_seq;
    };
    struct {
        SData/*15:0*/ ptp_ts_top__DOT__ptp_ts_tx__DOT__q1_seq;
        SData/*15:0*/ ptp_ts_top__DOT__ptp_ts_tx__DOT__cur_seq;
        VL_IN(i_ptp_incr,31,0);
        VL_IN(i_ptp_adj,31,0);
        VL_IN(i_ptp_ingress_lat,31,0);
        VL_IN(i_ptp_egress_lat,31,0);
        VlWide<3>/*87:0*/ ptp_ts_top__DOT__ts_counter__DOT__acc;
        VlWide<3>/*87:0*/ ptp_ts_top__DOT__ts_counter__DOT__tod_accumulator__DOT__unnamedblk1__DOT__next;
        IData/*31:0*/ ptp_ts_top__DOT__ptp_sync__DOT__incr_meta;
        IData/*31:0*/ ptp_ts_top__DOT__ptp_sync__DOT__incr_sync;
        IData/*31:0*/ ptp_ts_top__DOT__ptp_sync__DOT__adj_meta;
        IData/*31:0*/ ptp_ts_top__DOT__ptp_sync__DOT__adj_sync;
        VlWide<3>/*87:0*/ __Vdly__ptp_ts_top__DOT__ts_counter__DOT__acc;
        IData/*31:0*/ __Vtrigprevexpr___TOP__i_ptp_incr__0;
        IData/*31:0*/ __Vtrigprevexpr___TOP__i_ptp_adj__0;
        IData/*31:0*/ __Vtrigprevexpr___TOP__i_ptp_ingress_lat__0;
        IData/*31:0*/ __Vtrigprevexpr___TOP__i_ptp_egress_lat__0;
        IData/*31:0*/ __VactIterCount;
        VL_IN64(i_ptp_tod_wr,63,0);
        VL_IN64(i_ptp_offset,63,0);
        VL_OUT64(o_ptp_tod_rd,63,0);
        VL_OUT64(o_ptp_now,63,0);
        VL_IN64(s_axis_tx_tdata,63,0);
        VL_OUT64(m_axis_tx_tdata,63,0);
        VL_IN64(s_axis_rx_tdata,63,0);
        VL_OUT64(m_axis_rx_tdata,63,0);
        VL_OUT64(ts_m_axis_tdata,63,0);
        QData/*63:0*/ ptp_ts_top__DOT____Vcellout__axis_tx_rx_ts_switch_rr__m_tdata;
        QData/*63:0*/ ptp_ts_top__DOT__ptp_ts_rx__DOT__ts_sop;
        QData/*63:0*/ ptp_ts_top__DOT__ptp_ts_rx__DOT__q0_ts;
        QData/*63:0*/ ptp_ts_top__DOT__ptp_ts_rx__DOT__q1_ts;
        QData/*63:0*/ ptp_ts_top__DOT__ptp_ts_rx__DOT__cur_ts;
        QData/*63:0*/ ptp_ts_top__DOT__ptp_ts_tx__DOT__ts_sop;
        QData/*63:0*/ ptp_ts_top__DOT__ptp_ts_tx__DOT__q0_ts;
        QData/*63:0*/ ptp_ts_top__DOT__ptp_ts_tx__DOT__q1_ts;
        QData/*63:0*/ ptp_ts_top__DOT__ptp_ts_tx__DOT__cur_ts;
        QData/*63:0*/ ptp_ts_top__DOT__ts_counter__DOT__tod_snapshot;
        QData/*63:0*/ ptp_ts_top__DOT__ptp_sync__DOT__tod_wr_cap;
        QData/*63:0*/ ptp_ts_top__DOT__ptp_sync__DOT__offset_cap;
        QData/*63:0*/ ptp_ts_top__DOT__ptp_sync__DOT__snap_val_ts;
        QData/*63:0*/ ptp_ts_top__DOT__ptp_sync__DOT__tod_rd_reg;
        QData/*63:0*/ __Vtrigprevexpr___TOP__i_ptp_tod_wr__0;
        QData/*63:0*/ __Vtrigprevexpr___TOP__i_ptp_offset__0;
        QData/*63:0*/ __Vtrigprevexpr___TOP__s_axis_tx_tdata__0;
        QData/*63:0*/ __Vtrigprevexpr___TOP__s_axis_rx_tdata__0;
        VlUnpacked<VlWide<3>/*72:0*/, 2> ptp_ts_top__DOT__ts_metadata_drain_fifo__DOT__mem;
        VlUnpacked<VlWide<3>/*72:0*/, 2> ptp_ts_top__DOT__ts_metadata_drain_fifo__DOT__m_axis_pipe_reg;
        VlUnpacked<VlWide<3>/*72:0*/, 2> ptp_ts_top__DOT__rx_ts_buffer__DOT__mem;
        VlUnpacked<VlWide<3>/*72:0*/, 2> ptp_ts_top__DOT__rx_ts_buffer__DOT__m_axis_pipe_reg;
        VlUnpacked<VlWide<3>/*72:0*/, 2> ptp_ts_top__DOT__tx_ts_buffer__DOT__mem;
        VlUnpacked<VlWide<3>/*72:0*/, 2> ptp_ts_top__DOT__tx_ts_buffer__DOT__m_axis_pipe_reg;
        VlUnpacked<QData/*63:0*/, 1> __VstlTriggered;
        VlUnpacked<QData/*63:0*/, 2> __VicoTriggered;
        VlUnpacked<QData/*63:0*/, 1> __VactTriggered;
        VlUnpacked<QData/*63:0*/, 1> __VnbaTriggered;
    };

    // INTERNAL VARIABLES
    Vptp_ts_top__Syms* vlSymsp;
    const char* vlNamep;

    // CONSTRUCTORS
    Vptp_ts_top___024root(Vptp_ts_top__Syms* symsp, const char* namep);
    ~Vptp_ts_top___024root();
    VL_UNCOPYABLE(Vptp_ts_top___024root);

    // INTERNAL METHODS
    void __Vconfigure(bool first);
};


#endif  // guard
