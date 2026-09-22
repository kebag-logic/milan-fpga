/*
 * SPDX-FileCopyrightText: 2026 Kebag Logic
 * SPDX-License-Identifier: CERN-OHL-W-2.0
 */

/*
------------------------------------------------------------------------------
  File        : ptp_csr_sync.sv
  Author      : Kebag Logic

  Date        : 2026-07-01
  Description : Clock-domain crossing between the milan_csr register plane
                (aclk / axis_clk) and the PTP hardware clock (ts_clk / gtx_clk).
                Satisfies REQ-CSR-03: the CSR emits value + apply-strobe; this
                block synchronises them at the consumer.

                Forward (aclk -> ts_clk):
                  * Quasi-static rate config (enable, incr, adj) is carried with
                    a plain 2-flop vector synchroniser. These change rarely and a
                    one-tick mixed sample only perturbs the integrated rate by a
                    negligible amount, which the servo corrects — standard PHC
                    practice.
                  * settime/adjtime payloads (tod_wr, offset) are held stable by
                    software before the command; the command pulse is carried by
                    a toggle synchroniser and, when it lands, the (stable) payload
                    is sampled in the ts_clk domain.
                  * The snapshot command is a pure toggle-synchronised pulse.

                Return (ts_clk -> aclk):
                  * The gettime snapshot value is captured in ts_clk on the
                    counter's snapshot-valid pulse, then its validity is toggle-
                    synchronised to aclk where the (now stable) value is sampled
                    and a 1-cycle valid pulse is produced for milan_csr.

                Plain-FF synchronisers are used (no XPM) so the block is portable
                and lint-clean; apply the usual ASYNC_REG/false-path constraints
                on the *_meta/*_sync flops.

                PPS ALARM CROSSING (PPS_P, default OFF - issue #260). The same
                three shapes, once more: the runtime enable is quasi-static and
                takes the plain 2-flop vector synchroniser; the 64-bit armed
                target is held stable by software and sampled when its toggle-
                synchronised arm strobe lands; the live target returns on a
                PERIODIC PUBLISH rather than on the pulse that changes it. The
                publish beat is what makes the return coherent: the target can
                change every ts_clk tick while a target armed in the past
                catches up, and a value that moves every tick cannot be sampled
                safely by a toggle protocol. Capturing it once every 2^PUB_LOG2
                ticks holds each published word still for far longer than the
                three aclk edges the toggle needs, so the reading software gets
                a whole 64-bit target and never a torn one.

  Company     : Kebag Logic
  Project     : PTP Timestamping for Custom RGMII MAC
------------------------------------------------------------------------------
*/

`default_nettype none

module ptp_csr_sync #(
  parameter int TS_WIDTH   = 64, //! Integer-ns time width
  parameter int INCR_WIDTH = 32, //! Increment/addend width
  parameter bit PPS_P      = 1'b0 //! 1 = carry the PPS alarm controls/readback; 0 = prune them
)(
  // ---- source domain: aclk (milan_csr) ----
  input  wire                    aclk,
  input  wire                    aresetn,
  input  wire                    a_enable,     //! PTP enable (quasi-static)
  input  wire [INCR_WIDTH-1:0]   a_incr,       //! Nominal increment (quasi-static)
  input  wire [INCR_WIDTH-1:0]   a_adj,        //! adjfine addend (quasi-static)
  input  wire [TS_WIDTH-1:0]     a_tod_wr,     //! settime payload (held stable at cmd)
  input  wire [TS_WIDTH-1:0]     a_offset,     //! adjtime payload (held stable at cmd)
  input  wire                    a_cmd_load,   //! settime strobe (1 aclk cycle)
  input  wire                    a_cmd_adjust, //! adjtime strobe (1 aclk cycle)
  input  wire                    a_cmd_snapshot,//! gettime strobe (1 aclk cycle)
  output wire [TS_WIDTH-1:0]     a_tod_rd,     //! gettime result (aclk)
  output wire                    a_tod_rd_valid,//! gettime result valid (1 aclk pulse)
  input  wire                    a_pps_enable, //! PPS runtime enable (quasi-static, PPS_P only)
  input  wire [TS_WIDTH-1:0]     a_pps_target_ns, //! PPS armed target, ns (held stable at the arm strobe)
  input  wire                    a_pps_arm,    //! PPS arm strobe (1 aclk cycle)
  output wire [TS_WIDTH-1:0]     a_pps_target_rd_ns,//! Live PPS target published back (aclk). 0 when PPS_P = 0

  // ---- destination domain: ts_clk (timestamp_counter) ----
  input  wire                    ts_clk,
  input  wire                    ts_resetn,
  output wire                    t_enable,     //! Synchronised enable
  output wire [INCR_WIDTH-1:0]   t_incr,       //! Synchronised increment
  output wire [INCR_WIDTH-1:0]   t_adj,        //! Synchronised adjfine addend
  output wire [TS_WIDTH-1:0]     t_tod_wr,     //! Sampled settime payload
  output wire                    t_cmd_load,   //! Synchronised settime pulse
  output wire [TS_WIDTH-1:0]     t_offset,     //! Sampled adjtime payload
  output wire                    t_cmd_adjust, //! Synchronised adjtime pulse
  output wire                    t_cmd_snapshot,//! Synchronised gettime pulse
  input  wire [TS_WIDTH-1:0]     t_tod_snapshot,      //! Snapshot value (ts_clk)
  input  wire                    t_tod_snapshot_valid,//! Snapshot valid pulse (ts_clk)
  output wire                    t_pps_enable,        //! Synchronised PPS enable (ts_clk). 0 when PPS_P = 0
  output wire [TS_WIDTH-1:0]     t_pps_target_ns,        //! Sampled PPS target (ts_clk). 0 when PPS_P = 0
  output wire                    t_pps_arm,           //! Synchronised PPS arm pulse (ts_clk). 0 when PPS_P = 0
  input  wire [TS_WIDTH-1:0]     t_pps_target_live_ns    //! Live PPS target from the counter (ts_clk)
);

  //! Publish beat for the PPS target return path: one capture every 2^PUB_LOG2
  //! ts_clk ticks (2.05 us at 125 MHz), which is what bounds how fast the
  //! published word can move while an aclk toggle is in flight.
  localparam int PPS_PUB_LOG2 = 8;

  // --------------------------------------------------------------------------
  //  Quasi-static rate config: 2-flop vector synchronisers into ts_clk.
  // --------------------------------------------------------------------------
  (* ASYNC_REG = "TRUE" *) logic                  en_meta,   en_sync;
  (* ASYNC_REG = "TRUE" *) logic [INCR_WIDTH-1:0] incr_meta, incr_sync;
  (* ASYNC_REG = "TRUE" *) logic [INCR_WIDTH-1:0] adj_meta,  adj_sync;
  always_ff @(posedge ts_clk) begin : rate_cfg_sync
    if (!ts_resetn) begin
      en_meta <= 1'b0; en_sync <= 1'b0;
      incr_meta <= '0; incr_sync <= '0;
      adj_meta <= '0;  adj_sync <= '0;
    end else begin
      en_meta   <= a_enable;   en_sync   <= en_meta;
      incr_meta <= a_incr;     incr_sync <= incr_meta;
      adj_meta  <= a_adj;      adj_sync  <= adj_meta;
    end
  end
  assign t_enable = en_sync;
  assign t_incr   = incr_sync;
  assign t_adj    = adj_sync;

  // --------------------------------------------------------------------------
  //  Command pulse crossings via toggle synchronisers.
  //  Source toggles a level on each pulse; destination edge-detects it.
  // --------------------------------------------------------------------------
  logic load_tgl, adj_tgl, snap_tgl;
  always_ff @(posedge aclk) begin : src_toggles
    if (!aresetn) begin
      load_tgl <= 1'b0; adj_tgl <= 1'b0; snap_tgl <= 1'b0;
    end else begin
      if (a_cmd_load)     load_tgl <= ~load_tgl;
      if (a_cmd_adjust)   adj_tgl  <= ~adj_tgl;
      if (a_cmd_snapshot) snap_tgl <= ~snap_tgl;
    end
  end

  (* ASYNC_REG = "TRUE" *) logic [2:0] load_s, adj_s, snap_s;
  always_ff @(posedge ts_clk) begin : dst_toggle_sync
    if (!ts_resetn) begin
      load_s <= '0; adj_s <= '0; snap_s <= '0;
    end else begin
      load_s <= {load_s[1:0], load_tgl};
      adj_s  <= {adj_s[1:0],  adj_tgl};
      snap_s <= {snap_s[1:0], snap_tgl};
    end
  end
  wire load_pulse = load_s[2] ^ load_s[1];
  wire adj_pulse  = adj_s[2]  ^ adj_s[1];
  wire snap_pulse = snap_s[2] ^ snap_s[1];

  // Sample the (stable) payloads when the synchronised command lands, and delay
  // the settime/adjtime command pulse by one cycle so the counter sees the pulse
  // *after* the captured payload is stable on t_tod_wr/t_offset (the capture
  // register updates on the same edge the raw pulse asserts). The snapshot
  // command carries no payload, so it is forwarded without delay.
  logic [TS_WIDTH-1:0] tod_wr_cap, offset_cap;
  logic                load_pulse_q, adj_pulse_q;
  always_ff @(posedge ts_clk) begin : payload_capture
    if (!ts_resetn) begin
      tod_wr_cap <= '0; offset_cap <= '0;
      load_pulse_q <= 1'b0; adj_pulse_q <= 1'b0;
    end else begin
      if (load_pulse) tod_wr_cap <= a_tod_wr;
      if (adj_pulse)  offset_cap <= a_offset;
      load_pulse_q <= load_pulse;
      adj_pulse_q  <= adj_pulse;
    end
  end
  assign t_tod_wr      = tod_wr_cap;
  assign t_offset      = offset_cap;
  assign t_cmd_load    = load_pulse_q;
  assign t_cmd_adjust  = adj_pulse_q;
  assign t_cmd_snapshot= snap_pulse;

  // --------------------------------------------------------------------------
  //  Snapshot return path (ts_clk -> aclk): capture value, toggle-sync valid.
  // --------------------------------------------------------------------------
  logic [TS_WIDTH-1:0] snap_val_ts;
  logic                snap_tgl_ts;
  always_ff @(posedge ts_clk) begin : snap_capture
    if (!ts_resetn) begin
      snap_val_ts <= '0; snap_tgl_ts <= 1'b0;
    end else if (t_tod_snapshot_valid) begin
      snap_val_ts <= t_tod_snapshot;
      snap_tgl_ts <= ~snap_tgl_ts;
    end
  end

  (* ASYNC_REG = "TRUE" *) logic [2:0] snap_ret_s;
  logic [TS_WIDTH-1:0] tod_rd_reg;
  logic                tod_rd_valid_reg;
  always_ff @(posedge aclk) begin : snap_return_sync
    if (!aresetn) begin
      snap_ret_s <= '0; tod_rd_reg <= '0; tod_rd_valid_reg <= 1'b0;
    end else begin
      snap_ret_s <= {snap_ret_s[1:0], snap_tgl_ts};
      tod_rd_valid_reg <= snap_ret_s[2] ^ snap_ret_s[1];
      if (snap_ret_s[2] ^ snap_ret_s[1])
        tod_rd_reg <= snap_val_ts;  // stable by the time the toggle propagates
    end
  end
  assign a_tod_rd       = tod_rd_reg;
  assign a_tod_rd_valid = tod_rd_valid_reg;

  // --------------------------------------------------------------------------
  //  PPS alarm crossing (#260). Same three shapes as above, PPS_P gated.
  // --------------------------------------------------------------------------
  generate
    if (PPS_P) begin : g_pps_sync
      //! Quasi-static enable: plain 2-flop vector synchroniser.
      (* ASYNC_REG = "TRUE" *) logic pps_en_meta, pps_en_sync;
      always_ff @(posedge ts_clk) begin : pps_en_cdc
        if (!ts_resetn) begin
          pps_en_meta <= 1'b0; pps_en_sync <= 1'b0;
        end else begin
          pps_en_meta <= a_pps_enable; pps_en_sync <= pps_en_meta;
        end
      end : pps_en_cdc

      //! Arm strobe: source toggle, destination edge-detect, payload sampled
      //! when the toggle lands and the pulse delayed one tick behind it.
      logic pps_arm_tgl;
      always_ff @(posedge aclk) begin : pps_arm_src
        if (!aresetn)          pps_arm_tgl <= 1'b0;
        else if (a_pps_arm)    pps_arm_tgl <= ~pps_arm_tgl;
      end : pps_arm_src

      (* ASYNC_REG = "TRUE" *) logic [2:0] pps_arm_s;
      logic [TS_WIDTH-1:0] pps_target_cap;
      logic                pps_arm_pulse_q;
      always_ff @(posedge ts_clk) begin : pps_arm_dst
        if (!ts_resetn) begin
          pps_arm_s <= '0; pps_target_cap <= '0; pps_arm_pulse_q <= 1'b0;
        end else begin
          pps_arm_s <= {pps_arm_s[1:0], pps_arm_tgl};
          if (pps_arm_s[2] ^ pps_arm_s[1]) pps_target_cap <= a_pps_target_ns;
          pps_arm_pulse_q <= pps_arm_s[2] ^ pps_arm_s[1];
        end
      end : pps_arm_dst

      //! Return path: periodic publish, then the same toggle protocol. The
      //! beat is free-running, so the published word is still for 2^PUB_LOG2
      //! ts_clk ticks no matter how fast the live target is moving.
      logic [PPS_PUB_LOG2-1:0] pub_cnt_ts;
      logic [TS_WIDTH-1:0]     pub_val_ts;
      logic                    pub_tgl_ts;
      always_ff @(posedge ts_clk) begin : pps_publish
        if (!ts_resetn) begin
          pub_cnt_ts <= '0; pub_val_ts <= '0; pub_tgl_ts <= 1'b0;
        end else begin
          pub_cnt_ts <= pub_cnt_ts + 1'b1;
          if (pub_cnt_ts == '0) begin
            pub_val_ts <= t_pps_target_live_ns;
            pub_tgl_ts <= ~pub_tgl_ts;
          end
        end
      end : pps_publish

      (* ASYNC_REG = "TRUE" *) logic [2:0] pub_ret_s;
      logic [TS_WIDTH-1:0] pps_target_rd_ns_reg;
      always_ff @(posedge aclk) begin : pps_return_sync
        if (!aresetn) begin
          pub_ret_s <= '0; pps_target_rd_ns_reg <= '0;
        end else begin
          pub_ret_s <= {pub_ret_s[1:0], pub_tgl_ts};
          if (pub_ret_s[2] ^ pub_ret_s[1])
            pps_target_rd_ns_reg <= pub_val_ts;  // stable for the whole publish beat
        end
      end : pps_return_sync

      assign t_pps_enable    = pps_en_sync;
      assign t_pps_target_ns    = pps_target_cap;
      assign t_pps_arm       = pps_arm_pulse_q;
      assign a_pps_target_rd_ns = pps_target_rd_ns_reg;
    end : g_pps_sync
    else begin : g_pps_sync_parked
      //! Option OFF: no synchroniser, no publish beat, no readback register.
      assign t_pps_enable    = 1'b0;
      assign t_pps_target_ns    = '0;
      assign t_pps_arm       = 1'b0;
      assign a_pps_target_rd_ns = '0;
      wire _unused_pps_sync = &{1'b0, a_pps_enable, a_pps_target_ns, a_pps_arm,
                                t_pps_target_live_ns, 1'b0};
    end : g_pps_sync_parked
  endgenerate

endmodule

`default_nettype wire
