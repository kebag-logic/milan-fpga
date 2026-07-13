/*
 * SPDX-FileCopyrightText: 2025 Oguz Kahraman <oguz.kahraman@kebag-logic.com>
 *
 * SPDX-License-Identifier: CERN-OHL-W-2.0
 */

`timescale 1ns/1ps
`default_nettype none

module axis_mux_rr_2in_1out #(
  parameter int TDATA_WIDTH = 64
)(
  input  wire clk,
  input  wire rst_n,

  //! Slave 0 axis interface
  input  wire [TDATA_WIDTH-1:0] s0_tdata,
  input  wire s0_tvalid,
  output wire s0_tready,
  input  wire s0_tlast,
  input  wire [TDATA_WIDTH/8-1:0] s0_tkeep,

  //! Slave 1 axis interface
  input  wire [TDATA_WIDTH-1:0] s1_tdata,
  input  wire s1_tvalid,
  output wire s1_tready,
  input  wire s1_tlast,
  input  wire [TDATA_WIDTH/8-1:0] s1_tkeep,

  //! Master axis interface
  output reg  [TDATA_WIDTH-1:0]  m_tdata,
  output reg                     m_tvalid,
  input  wire                    m_tready,
  output reg                     m_tlast,
  output reg  [TDATA_WIDTH/8-1:0] m_tkeep
);

  //! typedef for state enumeration
  typedef enum logic [1:0] {
    IDLE,     //! wait state for stream valid signal priority depends on previous served packet
    STREAM_0, //! consume and serve stream0
    STREAM_1  //! consume and serve stream1
  } state_t;

  //! state declerations
  state_t state, next_state;

  //! flag indicates which slave has been used to give a chance to another one
  logic last_served;

  //! tready assignment to not have packet interleave
  assign s0_tready = (state == STREAM_0) && m_tready;
  assign s1_tready = (state == STREAM_1) && m_tready;

  //! FSM transaction
  always_ff @(posedge clk) begin : fsm_transaction
    if (!rst_n)
      state <= IDLE;
    else
      state <= next_state;
  end

  //! last served stream transaction it will be affect on next served prioirity
  always_ff @(posedge clk) begin : last_served_track
    if (!rst_n)
      last_served <= 1'b0;
    else if ((s0_tready && s0_tvalid && s0_tlast) || (s1_tready && s1_tvalid && s1_tlast))
      last_served <= (state == STREAM_0) ? 1'b0 : 1'b1;
  end

  //! Next state logic with round-robin
  always_comb begin : round_robin_slave_selection
    next_state = state;
    case (state)
      IDLE: begin
        if (!last_served) begin
          if (s1_tvalid)
            next_state = STREAM_1;
          else if (s0_tvalid)
            next_state = STREAM_0;
        end else begin
          if (s0_tvalid)
            next_state = STREAM_0;
          else if (s1_tvalid)
            next_state = STREAM_1;
        end
      end

      STREAM_0: begin
        if (s0_tvalid && s0_tlast && m_tready)
          next_state = IDLE;
      end

      STREAM_1: begin
        if (s1_tvalid && s1_tlast && m_tready)
          next_state = IDLE;
      end
      default : next_state = IDLE;
    endcase
  end

  //! Muxing logic
  always_comb begin : mux_logic
    m_tvalid = 1'b0;
    m_tdata  = '0;
    m_tkeep  = '0;
    m_tlast  = 1'b0;

    case (state)
      STREAM_0: begin
        // tvalid must NOT depend on tready (AXI-Stream rule; the old
        // `s0_tvalid && s0_tready` term folded m_tready into m_tvalid and
        // deadlocks against a sink that waits for valid before ready)
        m_tvalid = s0_tvalid;
        m_tdata  = s0_tdata;
        m_tkeep  = s0_tkeep;
        m_tlast  = s0_tlast;
      end
      STREAM_1: begin
        m_tvalid = s1_tvalid;
        m_tdata  = s1_tdata;
        m_tkeep  = s1_tkeep;
        m_tlast  = s1_tlast;
      end
    endcase
  end

endmodule

`default_nettype wire
