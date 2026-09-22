// Verilated -*- C++ -*-
// DESCRIPTION: Verilator output: Primary model header
//
// This header should be included by all source files instantiating the design.
// The class here is then constructed to instantiate the design.
// See the Verilator manual for examples.

#ifndef VERILATED_VPTP_TS_TOP_H_
#define VERILATED_VPTP_TS_TOP_H_  // guard

#include "verilated.h"

class Vptp_ts_top__Syms;
class Vptp_ts_top___024root;
class Vptp_ts_top_axi_stream_if;


// This class is the main interface to the Verilated model
class alignas(VL_CACHE_LINE_BYTES) Vptp_ts_top VL_NOT_FINAL : public VerilatedModel {
  private:
    // Symbol table holding complete model state (owned by this class)
    Vptp_ts_top__Syms* const vlSymsp;

  public:

    // CONSTEXPR CAPABILITIES
    // Verilated with --trace?
    static constexpr bool traceCapable = false;

    // PORTS
    // The application code writes and reads these signals to
    // propagate new values into/out from the Verilated model.
    VL_IN8(&gtx_clk,0,0);
    VL_IN8(&axis_clk,0,0);
    VL_IN8(&gtx_resetn,0,0);
    VL_IN8(&axis_resetn,0,0);
    VL_IN8(&i_ptp_enable,0,0);
    VL_IN8(&i_ptp_cmd_load,0,0);
    VL_IN8(&i_ptp_cmd_adjust,0,0);
    VL_IN8(&i_ptp_cmd_snapshot,0,0);
    VL_OUT8(&o_ptp_tod_rd_valid,0,0);
    VL_OUT8(&o_tx_ts_ready,0,0);
    VL_IN8(&s_axis_tx_tvalid,0,0);
    VL_OUT8(&s_axis_tx_tready,0,0);
    VL_IN8(&s_axis_tx_tlast,0,0);
    VL_IN8(&s_axis_tx_tkeep,7,0);
    VL_OUT8(&m_axis_tx_tvalid,0,0);
    VL_IN8(&m_axis_tx_tready,0,0);
    VL_OUT8(&m_axis_tx_tlast,0,0);
    VL_OUT8(&m_axis_tx_tkeep,7,0);
    VL_IN8(&s_axis_rx_tvalid,0,0);
    VL_OUT8(&s_axis_rx_tready,0,0);
    VL_IN8(&s_axis_rx_tlast,0,0);
    VL_IN8(&s_axis_rx_tkeep,7,0);
    VL_OUT8(&m_axis_rx_tvalid,0,0);
    VL_IN8(&m_axis_rx_tready,0,0);
    VL_OUT8(&m_axis_rx_tlast,0,0);
    VL_OUT8(&m_axis_rx_tkeep,7,0);
    VL_OUT8(&ts_m_axis_tvalid,0,0);
    VL_IN8(&ts_m_axis_tready,0,0);
    VL_OUT8(&ts_m_axis_tlast,0,0);
    VL_OUT8(&ts_m_axis_tkeep,7,0);
    VL_IN(&i_ptp_incr,31,0);
    VL_IN(&i_ptp_adj,31,0);
    VL_IN(&i_ptp_ingress_lat,31,0);
    VL_IN(&i_ptp_egress_lat,31,0);
    VL_IN64(&i_ptp_tod_wr,63,0);
    VL_IN64(&i_ptp_offset,63,0);
    VL_OUT64(&o_ptp_tod_rd,63,0);
    VL_OUT64(&o_ptp_now,63,0);
    VL_IN64(&s_axis_tx_tdata,63,0);
    VL_OUT64(&m_axis_tx_tdata,63,0);
    VL_IN64(&s_axis_rx_tdata,63,0);
    VL_OUT64(&m_axis_rx_tdata,63,0);
    VL_OUT64(&ts_m_axis_tdata,63,0);

    // CELLS
    // Public to allow access to /* verilator public */ items.
    // Otherwise the application code can consider these internals.
    Vptp_ts_top_axi_stream_if* const __PVT__ptp_ts_top__DOT__s_axis_tx;
    Vptp_ts_top_axi_stream_if* const __PVT__ptp_ts_top__DOT__s_axis_rx;
    Vptp_ts_top_axi_stream_if* const __PVT__ptp_ts_top__DOT__m_axis_tx;
    Vptp_ts_top_axi_stream_if* const __PVT__ptp_ts_top__DOT__m_axis_rx;
    Vptp_ts_top_axi_stream_if* const __PVT__ptp_ts_top__DOT__ts_m_axis_tx;
    Vptp_ts_top_axi_stream_if* const __PVT__ptp_ts_top__DOT__ts_m_axis_rx;
    Vptp_ts_top_axi_stream_if* const __PVT__ptp_ts_top__DOT__ts_tx_buffered;
    Vptp_ts_top_axi_stream_if* const __PVT__ptp_ts_top__DOT__ts_rx_buffered;
    Vptp_ts_top_axi_stream_if* const __PVT__ptp_ts_top__DOT__ts_switch_to_fifo;

    // Root instance pointer to allow access to model internals,
    // including inlined /* verilator public_flat_* */ items.
    Vptp_ts_top___024root* const rootp;

    // CONSTRUCTORS
    /// Construct the model; called by application code
    /// If contextp is null, then the model will use the default global context
    /// If name is "", then makes a wrapper with a
    /// single model invisible with respect to DPI scope names.
    explicit Vptp_ts_top(VerilatedContext* contextp, const char* name = "TOP");
    explicit Vptp_ts_top(const char* name = "TOP");
    /// Destroy the model; called (often implicitly) by application code
    virtual ~Vptp_ts_top();
  private:
    VL_UNCOPYABLE(Vptp_ts_top);  ///< Copying not allowed

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
