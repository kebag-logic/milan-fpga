// Verilated -*- C++ -*-
// DESCRIPTION: Verilator output: Primary model header
//
// This header should be included by all source files instantiating the design.
// The class here is then constructed to instantiate the design.
// See the Verilator manual for examples.

#ifndef VERILATED_VMILAN_DATAPATH_H_
#define VERILATED_VMILAN_DATAPATH_H_  // guard

#include "verilated.h"
#include "svdpi.h"

class Vmilan_datapath__Syms;
class Vmilan_datapath___024root;
class Vmilan_datapath_axi_stream_if;
class Vmilan_datapath_axi_stream_if__TC3;


// This class is the main interface to the Verilated model
class alignas(VL_CACHE_LINE_BYTES) Vmilan_datapath VL_NOT_FINAL : public VerilatedModel {
  private:
    // Symbol table holding complete model state (owned by this class)
    Vmilan_datapath__Syms* const vlSymsp;

  public:

    // CONSTEXPR CAPABILITIES
    // Verilated with --trace?
    static constexpr bool traceCapable = false;

    // PORTS
    // The application code writes and reads these signals to
    // propagate new values into/out from the Verilated model.
    VL_IN8(&axis_clk,0,0);
    VL_IN8(&clk_audio_i,0,0);
    VL_IN8(&clk_tdm_i,0,0);
    VL_IN8(&axis_resetn,0,0);
    VL_IN8(&gtx_clk,0,0);
    VL_IN8(&tdm_bclk_i,0,0);
    VL_IN8(&i_ps_clk,0,0);
    VL_IN8(&gtx_resetn,0,0);
    VL_IN8(&s_axi_awvalid,0,0);
    VL_OUT8(&s_axi_awready,0,0);
    VL_IN8(&s_axi_wstrb,3,0);
    VL_IN8(&s_axi_wvalid,0,0);
    VL_OUT8(&s_axi_wready,0,0);
    VL_OUT8(&s_axi_bresp,1,0);
    VL_OUT8(&s_axi_bvalid,0,0);
    VL_IN8(&s_axi_bready,0,0);
    VL_IN8(&s_axi_arvalid,0,0);
    VL_OUT8(&s_axi_arready,0,0);
    VL_OUT8(&s_axi_rresp,1,0);
    VL_OUT8(&s_axi_rvalid,0,0);
    VL_IN8(&s_axi_rready,0,0);
    VL_OUT8(&i2s_mclk_o,0,0);
    VL_OUT8(&i2s_sclk_o,0,0);
    VL_OUT8(&i2s_lrck_o,0,0);
    VL_IN8(&i2s_sdout_i,0,0);
    VL_IN8(&tdm_fsync_i,0,0);
    VL_OUT8(&tdm_bclk_o,0,0);
    VL_OUT8(&tdm_fsync_o,0,0);
    VL_OUT8(&tdm_dout_o,0,0);
    VL_IN8(&tdm_data_i,0,0);
    VL_OUT8(&i2s_dac_mclk_o,0,0);
    VL_OUT8(&i2s_dac_sclk_o,0,0);
    VL_OUT8(&i2s_dac_lrck_o,0,0);
    VL_OUT8(&i2s_dac_sdin_o,0,0);
    VL_IN8(&s_axis_tx_tkeep,7,0);
    VL_IN8(&s_axis_tx_tvalid,0,0);
    VL_IN8(&s_axis_tx_tlast,0,0);
    VL_OUT8(&s_axis_tx_tready,0,0);
    VL_OUT8(&m_axis_rx_tkeep,7,0);
    VL_OUT8(&m_axis_rx_tvalid,0,0);
    VL_OUT8(&m_axis_rx_tlast,0,0);
    VL_IN8(&m_axis_rx_tready,0,0);
    VL_OUT8(&m_axis_ts_tkeep,7,0);
    VL_OUT8(&m_axis_ts_tvalid,0,0);
    VL_OUT8(&m_axis_ts_tlast,0,0);
    VL_IN8(&m_axis_ts_tready,0,0);
    VL_OUT8(&m_axis_pcm_tkeep,7,0);
    VL_OUT8(&m_axis_pcm_tvalid,0,0);
    VL_OUT8(&m_axis_pcm_tlast,0,0);
    VL_OUT8(&m_axis_pcm_tuser,3,0);
    VL_IN8(&m_axis_pcm_tready,0,0);
    VL_OUT8(&m_axis_mac_tx_tkeep,7,0);
    VL_OUT8(&m_axis_mac_tx_tvalid,0,0);
    VL_OUT8(&m_axis_mac_tx_tlast,0,0);
    VL_IN8(&m_axis_mac_tx_tready,0,0);
    VL_IN8(&s_axis_mac_rx_tkeep,7,0);
    VL_IN8(&s_axis_mac_rx_tvalid,0,0);
    VL_IN8(&s_axis_mac_rx_tlast,0,0);
    VL_OUT8(&s_axis_mac_rx_tready,0,0);
    VL_OUT8(&o_mac_tx_en,0,0);
    VL_OUT8(&o_mac_rx_en,0,0);
    VL_OUT8(&o_mac_promisc,0,0);
    VL_OUT8(&o_mac_allmulti,0,0);
    VL_OUT8(&o_mac_is_1g,0,0);
    VL_OUT8(&o_mac_ifg,7,0);
    VL_OUT8(&o_phy_reset_n,0,0);
    VL_IN8(&i_mac_speed,1,0);
    VL_IN8(&i_link_up,0,0);
    VL_OUT8(&o_mac_reinit,0,0);
    VL_OUT8(&o_eth_rst,0,0);
    VL_IN8(&i_full_duplex,0,0);
    VL_IN8(&i_ethrx_tgl,0,0);
    VL_IN8(&i_ethtx_tgl,0,0);
    VL_IN8(&i_ethact_tgl,0,0);
    VL_OUT8(&o_irq_csr,0,0);
    VL_OUT8(&o_identify,0,0);
    VL_OUT8(&o_mmcm_drp_addr,6,0);
    VL_OUT8(&o_mmcm_drp_en,0,0);
    VL_OUT8(&o_mmcm_drp_we,0,0);
    VL_IN8(&i_mmcm_drp_rdy,0,0);
    VL_OUT8(&o_mmcm_rst,0,0);
    VL_IN8(&i_mmcm_locked,0,0);
    VL_OUT8(&o_mmcm_ps_en,0,0);
    VL_OUT8(&o_mmcm_ps_incdec,0,0);
    VL_IN8(&i_mmcm_ps_done,0,0);
    VL_IN8(&pb_enable_i,0,0);
    VL_IN8(&pb_underrun_silence_i,0,0);
    VL_IN8(&pb_stream_en_i,7,0);
    VL_OUT8(&pb_mem_rd_o,0,0);
    VL_IN8(&pb_mem_valid_i,0,0);
    VL_OUT8(&pb_playing_o,0,0);
    VL_IN16(&s_axi_awaddr,15,0);
    VL_IN16(&s_axi_araddr,15,0);
    VL_IN16(&i_mac_events,8,0);
    VL_IN16(&i_mac_events_cap,8,0);
    VL_OUT16(&o_mmcm_drp_di,15,0);
    VL_IN16(&i_mmcm_drp_do,15,0);
    VL_IN(&s_axi_wdata,31,0);
    VL_OUT(&s_axi_rdata,31,0);
    VL_IN(&pb_ring_len_i,31,0);
    VL_IN(&pb_ring_stride_i,31,0);
    VL_INW(&pb_wr_ptr_i,255,0,8);
    VL_OUT(&pb_mem_addr_o,31,0);
    VL_OUTW(&pb_rd_ptr_o,255,0,8);
    VL_OUTW(&pb_underrun_o,127,0,4);
    VL_OUTW(&pb_overrun_o,127,0,4);
    VL_IN64(&s_axis_tx_tdata,63,0);
    VL_OUT64(&m_axis_rx_tdata,63,0);
    VL_OUT64(&m_axis_ts_tdata,63,0);
    VL_OUT64(&m_axis_pcm_tdata,63,0);
    VL_OUT64(&m_axis_mac_tx_tdata,63,0);
    VL_IN64(&s_axis_mac_rx_tdata,63,0);
    VL_OUT64(&o_mac_addr,47,0);
    VL_OUT64(&o_mc_hash,63,0);
    VL_IN64(&pb_ring_base_i,63,0);
    VL_IN64(&pb_mem_data_i,63,0);

    // CELLS
    // Public to allow access to /* verilator public */ items.
    // Otherwise the application code can consider these internals.
    Vmilan_datapath_axi_stream_if* const __PVT__milan_datapath__DOT__tx_axis_to_shaper;
    Vmilan_datapath_axi_stream_if* const __PVT__milan_datapath__DOT__tx_axis_shaper_to_ts;
    Vmilan_datapath_axi_stream_if* const __PVT__milan_datapath__DOT__tx_axis_dp_to_arb;
    Vmilan_datapath_axi_stream_if* const __PVT__milan_datapath__DOT__tx_axis_to_mac;
    Vmilan_datapath_axi_stream_if* const __PVT__milan_datapath__DOT__rx_axis_to_ts;
    Vmilan_datapath_axi_stream_if* const __PVT__milan_datapath__DOT__rx_axis_ptp_to_filt;
    Vmilan_datapath_axi_stream_if* const __PVT__milan_datapath__DOT__rx_axis_to_dma;
    Vmilan_datapath_axi_stream_if* const __PVT__milan_datapath__DOT__ts_metadata_axis;
    Vmilan_datapath_axi_stream_if* const __PVT__milan_datapath__DOT__ptp_timestamp__DOT__s_axis_tx;
    Vmilan_datapath_axi_stream_if* const __PVT__milan_datapath__DOT__ptp_timestamp__DOT__s_axis_rx;
    Vmilan_datapath_axi_stream_if* const __PVT__milan_datapath__DOT__ptp_timestamp__DOT__m_axis_tx;
    Vmilan_datapath_axi_stream_if* const __PVT__milan_datapath__DOT__ptp_timestamp__DOT__m_axis_rx;
    Vmilan_datapath_axi_stream_if* const __PVT__milan_datapath__DOT__ptp_timestamp__DOT__ts_m_axis_tx;
    Vmilan_datapath_axi_stream_if* const __PVT__milan_datapath__DOT__ptp_timestamp__DOT__ts_m_axis_rx;
    Vmilan_datapath_axi_stream_if* const __PVT__milan_datapath__DOT__ptp_timestamp__DOT__ts_tx_buffered;
    Vmilan_datapath_axi_stream_if* const __PVT__milan_datapath__DOT__ptp_timestamp__DOT__ts_rx_buffered;
    Vmilan_datapath_axi_stream_if* const __PVT__milan_datapath__DOT__ptp_timestamp__DOT__ts_switch_to_fifo;
    Vmilan_datapath_axi_stream_if__TC3* const __PVT__milan_datapath__DOT__traffic_controller__DOT__classifier_to_queue;
    Vmilan_datapath_axi_stream_if__TC3* const __PVT__milan_datapath__DOT__traffic_controller__DOT__queue_to_shaper;
    Vmilan_datapath_axi_stream_if* const __PVT__milan_datapath__DOT__traffic_controller__DOT__classifier__DOT__m_axis_fifo;

    // Root instance pointer to allow access to model internals,
    // including inlined /* verilator public_flat_* */ items.
    Vmilan_datapath___024root* const rootp;

    // CONSTRUCTORS
    /// Construct the model; called by application code
    /// If contextp is null, then the model will use the default global context
    /// If name is "", then makes a wrapper with a
    /// single model invisible with respect to DPI scope names.
    explicit Vmilan_datapath(VerilatedContext* contextp, const char* name = "TOP");
    explicit Vmilan_datapath(const char* name = "TOP");
    /// Destroy the model; called (often implicitly) by application code
    virtual ~Vmilan_datapath();
  private:
    VL_UNCOPYABLE(Vmilan_datapath);  ///< Copying not allowed

  public:
    // API METHODS
    /// Evaluate the model.  Application must call when inputs change.
    void eval() { eval_step(); }
    /// Evaluate when calling multiple units/models per time step.
    void eval_step();
    /// Evaluate at end of a timestep for tracing, when using eval_step().
    /// Application must call after all eval() and before time changes.
    void eval_end_step() {}
    /// Simulation complete, run final blocks.  Application must call on completion.
    void final();
    /// Are there scheduled events to handle?
    bool eventsPending();
    /// Returns time at next time slot. Aborts if !eventsPending()
    uint64_t nextTimeSlot();
    /// Trace signals in the model; called by application code
    void trace(VerilatedTraceBaseC* tfp, int levels, int options = 0) { contextp()->trace(tfp, levels, options); }
    /// Retrieve name of this model instance (as passed to constructor).
    const char* name() const;

    // Abstract methods from VerilatedModel
    const char* hierName() const override final;
    const char* modelName() const override final;
    unsigned threads() const override final;
    /// Prepare for cloning the model at the process level (e.g. fork in Linux)
    /// Release necessary resources. Called before cloning.
    void prepareClone() const;
    /// Re-init after cloning the model at the process level (e.g. fork in Linux)
    /// Re-allocate necessary resources. Called after cloning.
    void atClone() const;
  private:
    // Internal functions - trace registration
    void traceBaseModel(VerilatedTraceBaseC* tfp, int levels, int options);
};

#endif  // guard
