// Verilated -*- C++ -*-
// DESCRIPTION: Verilator output: Primary model header
//
// This header should be included by all source files instantiating the design.
// The class here is then constructed to instantiate the design.
// See the Verilator manual for examples.

#ifndef VERILATED_VSIM_H_
#define VERILATED_VSIM_H_  // guard

#include "verilated.h"
#include "svdpi.h"

class Vsim__Syms;
class Vsim___024root;
class Vsim_KL_mbx_pkg;
class Vsim_sim;


// This class is the main interface to the Verilated model
class alignas(VL_CACHE_LINE_BYTES) Vsim VL_NOT_FINAL : public VerilatedModel {
  private:
    // Symbol table holding complete model state (owned by this class)
    Vsim__Syms* const vlSymsp;

  public:

    // CONSTEXPR CAPABILITIES
    // Verilated with --trace?
    static constexpr bool traceCapable = false;

    // PORTS
    // The application code writes and reads these signals to
    // propagate new values into/out from the Verilated model.
    VL_IN8(&sys_clk,0,0);
    VL_IN8(&sys_reset,0,0);
    VL_IN8(&audio_clk,0,0);
    VL_IN8(&audio_tdm_clk,0,0);
    VL_OUT8(&flash_cs,0,0);
    VL_OUT8(&flash_rx_ready,0,0);
    VL_IN8(&flash_rx_valid,0,0);
    VL_OUT8(&flash_tx_len,5,0);
    VL_IN8(&flash_tx_ready,0,0);
    VL_OUT8(&flash_tx_valid,0,0);
    VL_OUT8(&flash_tx_width,3,0);
    VL_IN8(&mbx_amap_wr,0,0);
    VL_IN8(&mbx_asp_chg,0,0);
    VL_IN8(&mbx_avb_chg,0,0);
    VL_IN8(&mbx_domain,7,0);
    VL_IN8(&mbx_gm_change,0,0);
    VL_OUT8(&mbx_host_ack,0,0);
    VL_OUT8(&mbx_host_req,0,0);
    VL_OUT8(&mbx_host_we,0,0);
    VL_IN8(&mbx_link_up,0,0);
    VL_OUT8(&mbx_ms_tick,0,0);
    VL_IN8(&mbx_rx_data,7,0);
    VL_IN8(&mbx_rx_if,0,0);
    VL_IN8(&mbx_rx_last,0,0);
    VL_OUT8(&mbx_rx_ready,0,0);
    VL_IN8(&mbx_rx_valid,0,0);
    VL_OUT8(&mbx_tx_ch,2,0);
    VL_OUT8(&mbx_tx_data,7,0);
    VL_OUT8(&mbx_tx_if,0,0);
    VL_OUT8(&mbx_tx_last,0,0);
    VL_IN8(&mbx_tx_ready,0,0);
    VL_OUT8(&mbx_tx_valid,0,0);
    VL_IN8(&milan_clk,0,0);
    VL_IN8(&serial_sink_data,7,0);
    VL_OUT8(&serial_sink_ready,0,0);
    VL_IN8(&serial_sink_valid,0,0);
    VL_OUT8(&serial_source_data,7,0);
    VL_IN8(&serial_source_ready,0,0);
    VL_OUT8(&serial_source_valid,0,0);
    VL_IN8(&sim_trace,0,0);
    VL_OUT16(&mbx_host_addr,12,0);
    VL_IN(&flash_rx_data,31,0);
    VL_OUT(&flash_tx_data,31,0);
    VL_OUT(&mbx_host_rdata,31,0);
    VL_OUT(&mbx_host_wdata,31,0);
    VL_IN64(&mbx_gm_id,63,0);

    // CELLS
    // Public to allow access to /* verilator public */ items.
    // Otherwise the application code can consider these internals.
    Vsim_sim* const sim;
    Vsim_KL_mbx_pkg* const __PVT__KL_mbx_pkg;

    // Root instance pointer to allow access to model internals,
    // including inlined /* verilator public_flat_* */ items.
    Vsim___024root* const rootp;

    // CONSTRUCTORS
    /// Construct the model; called by application code
    /// If contextp is null, then the model will use the default global context
    /// If name is "", then makes a wrapper with a
    /// single model invisible with respect to DPI scope names.
    explicit Vsim(VerilatedContext* contextp, const char* name = "TOP");
    explicit Vsim(const char* name = "TOP");
    /// Destroy the model; called (often implicitly) by application code
    virtual ~Vsim();
  private:
    VL_UNCOPYABLE(Vsim);  ///< Copying not allowed

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
