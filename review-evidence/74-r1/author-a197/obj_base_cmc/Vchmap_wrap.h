// Verilated -*- C++ -*-
// DESCRIPTION: Verilator output: Primary model header
//
// This header should be included by all source files instantiating the design.
// The class here is then constructed to instantiate the design.
// See the Verilator manual for examples.

#ifndef VERILATED_VCHMAP_WRAP_H_
#define VERILATED_VCHMAP_WRAP_H_  // guard

#include "verilated.h"
#include "svdpi.h"

class Vchmap_wrap__Syms;
class Vchmap_wrap___024root;
class Vchmap_wrap_KL_chan_map_capture;


// This class is the main interface to the Verilated model
class alignas(VL_CACHE_LINE_BYTES) Vchmap_wrap VL_NOT_FINAL : public VerilatedModel {
  private:
    // Symbol table holding complete model state (owned by this class)
    Vchmap_wrap__Syms* const vlSymsp;

  public:

    // CONSTEXPR CAPABILITIES
    // Verilated with --trace?
    static constexpr bool traceCapable = false;

    // PORTS
    // The application code writes and reads these signals to
    // propagate new values into/out from the Verilated model.
    VL_IN8(&clk,0,0);
    VL_IN8(&clk_audio,0,0);
    VL_IN8(&rst_n,0,0);
    VL_IN8(&tg_en_i,0,0);
    VL_IN8(&tg_tick_i,0,0);
    VL_IN8(&i2s_pair_valid_i,0,0);
    VL_IN8(&tdm_pair_valid_i,0,0);
    VL_IN8(&tdm_pair_slot_i,3,0);
    VL_IN8(&lb_tvalid_i,0,0);
    VL_IN8(&lb_tlast_i,0,0);
    VL_IN8(&lb_tuser_i,3,0);
    VL_IN8(&a_lb_flush_i,7,0);
    VL_IN8(&b_lb_flush_i,7,0);
    VL_IN8(&a_map_wr_en_i,0,0);
    VL_IN8(&a_map_wr_addr_i,5,0);
    VL_IN8(&a_map_rd_en_i,0,0);
    VL_IN8(&a_map_rd_addr_i,5,0);
    VL_OUT8(&a_map_rd_valid_o,0,0);
    VL_IN8(&a_tick_i,0,0);
    VL_OUT8(&a_pv_o,0,0);
    VL_IN8(&a_en_i,1,0);
    VL_IN8(&a_tctx_wr_en_i,0,0);
    VL_IN8(&a_tctx_wr_addr_i,6,0);
    VL_OUT8(&a_tctx_wr_rdy_o,0,0);
    VL_IN8(&a_tctx_rd_en_i,0,0);
    VL_IN8(&a_tctx_rd_addr_i,6,0);
    VL_OUT8(&a_tctx_rd_valid_o,0,0);
    VL_OUT8(&a_tkeep_o,7,0);
    VL_OUT8(&a_tvalid_o,0,0);
    VL_OUT8(&a_tlast_o,0,0);
    VL_IN8(&a_tready_i,0,0);
    VL_IN8(&b_map_wr_en_i,0,0);
    VL_IN8(&b_map_wr_addr_i,5,0);
    VL_IN8(&b_map_rd_en_i,0,0);
    VL_IN8(&b_map_rd_addr_i,5,0);
    VL_OUT8(&b_map_rd_valid_o,0,0);
    VL_IN8(&b_tick_i,0,0);
    VL_IN8(&b_en_i,7,0);
    VL_IN8(&b_tctx_wr_en_i,0,0);
    VL_IN8(&b_tctx_wr_addr_i,6,0);
    VL_OUT8(&b_tctx_wr_rdy_o,0,0);
    VL_IN8(&b_tctx_rd_en_i,0,0);
    VL_IN8(&b_tctx_rd_addr_i,6,0);
    VL_OUT8(&b_tctx_rd_valid_o,0,0);
    VL_OUT8(&b_tkeep_o,7,0);
    VL_OUT8(&b_tvalid_o,0,0);
    VL_OUT8(&b_tlast_o,0,0);
    VL_IN8(&b_tready_i,0,0);
    VL_IN16(&vlan_vid_i,11,0);
    VL_OUT16(&a_dup_cnt_o,15,0);
    VL_OUT16(&a_skip_cnt_o,15,0);
    VL_OUT16(&a_tdm_dup_cnt_o,15,0);
    VL_OUT16(&a_tdm_skip_cnt_o,15,0);
    VL_OUT16(&b_dup_cnt_o,15,0);
    VL_OUT16(&b_skip_cnt_o,15,0);
    VL_IN16(&a_map_wr_data_i,12,0);
    VL_OUT16(&a_map_rd_data_o,14,0);
    VL_IN16(&b_map_wr_data_i,12,0);
    VL_OUT16(&b_map_rd_data_o,14,0);
    VL_OUT(&tone_legacy_o,23,0);
    VL_OUT(&tone_media_o,23,0);
    VL_IN(&transit_ns_i,31,0);
    VL_IN(&i2s_l_i,23,0);
    VL_IN(&i2s_r_i,23,0);
    VL_IN(&tdm_l_i,23,0);
    VL_IN(&tdm_r_i,23,0);
    VL_IN(&tone_smp_i,23,0);
    VL_IN(&lb_wire_chans_i,31,0);
    VL_IN(&a_tctx_wr_data_i,31,0);
    VL_OUT(&a_tctx_rd_data_o,31,0);
    VL_IN(&b_tctx_wr_data_i,31,0);
    VL_OUT(&b_tctx_rd_data_o,31,0);
    VL_IN64(&dest_mac_i,47,0);
    VL_IN64(&station_mac_i,47,0);
    VL_IN64(&ptp_ns_i,63,0);
    VL_IN64(&lb_tdata_i,63,0);
    VL_OUT64(&a_tdata_o,63,0);
    VL_OUT64(&b_tdata_o,63,0);

    // CELLS
    // Public to allow access to /* verilator public */ items.
    // Otherwise the application code can consider these internals.
    Vchmap_wrap_KL_chan_map_capture* const __PVT__chmap_wrap__DOT__u_chmap_a;
    Vchmap_wrap_KL_chan_map_capture* const __PVT__chmap_wrap__DOT__u_chmap_b;

    // Root instance pointer to allow access to model internals,
    // including inlined /* verilator public_flat_* */ items.
    Vchmap_wrap___024root* const rootp;

    // CONSTRUCTORS
    /// Construct the model; called by application code
    /// If contextp is null, then the model will use the default global context
    /// If name is "", then makes a wrapper with a
    /// single model invisible with respect to DPI scope names.
    explicit Vchmap_wrap(VerilatedContext* contextp, const char* name = "TOP");
    explicit Vchmap_wrap(const char* name = "TOP");
    /// Destroy the model; called (often implicitly) by application code
    virtual ~Vchmap_wrap();
  private:
    VL_UNCOPYABLE(Vchmap_wrap);  ///< Copying not allowed

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
