// SPDX-FileCopyrightText: 2026 Kebag Logic
// SPDX-License-Identifier: CERN-OHL-W-2.0
// Single-beat GPIF master for sockets 0, 1 and 3 on A1:A0.
// Address/flag settling and turnaround follow the public harness budget.
`default_nettype none
module KL_usbaudio_gpif #(
  parameter int unsigned BUS_HZ_P = 50_000_000 //! status service deadline
)(
  input wire clk_i, //! output-launch clock
  input wire capture_clk_i, //! phased DQ input-capture clock
  input wire reset_i, //! asynchronous session/pad shutdown
  input wire [15:0] dq_i, //! external data bus
  (* IOB = "TRUE" *) output logic [15:0] dq_o, //! registered output data
  (* IOB = "TRUE", dont_touch = "TRUE" *) output logic [15:0] dq_t_o, //! one tristate register per pin, one releases
  (* IOB = "TRUE", dont_touch = "TRUE" *) output logic [1:0] address_o, //! only sockets 0, 1 and 3
  (* IOB = "TRUE" *) output logic slwr_n_o, //! active-low write pulse
  (* IOB = "TRUE" *) output logic slrd_n_o, //! active-low read pulse
  (* IOB = "TRUE" *) output logic sloe_n_o, //! active-low external output enable
  (* IOB = "TRUE" *) output logic pktend_n_o, //! final word commits a capture/status record
  input wire flaga_i, //! selected socket ready level
  output wire rx_valid_o, //! one received word, held through backpressure
  input wire rx_ready_i, //! parser accepts word
  output wire [15:0] rx_data_o, //! received little-endian word
  input wire capture_valid_i, //! capture word available
  output wire capture_ready_o, //! capture word transferred
  input wire [15:0] capture_data_i, //! capture word
  input wire capture_last_i, //! last whole-frame word of interval
  input wire capture_abort_i, //! epoch fence, only after a completed read
  input wire status_valid_i, //! status word available
  output wire status_ready_o, //! status word transferred
  input wire [15:0] status_data_i, //! status word
  input wire status_last_i //! tenth status word
);
  typedef enum logic [3:0] {
    TURN_S, SELECT_S, SETTLE_S, CHECK_S, WRITE_S, QUIET_S,
    READ_S, READ_WAIT_S, CAPTURE_S, PUSH_S
  } state_t;
  state_t state_r, next_w;
  logic [3:0] delay_r;
  logic read_turn_r;
  logic [15:0] rx_r;
  logic [31:0] status_age_r;
  (* IOB = "TRUE" *) logic [15:0] captured_r;
  (* ASYNC_REG = "TRUE" *) logic flag_meta_r, flag_sync_r;
  wire rst_n_w, cap_rst_n_w;
  KL_usbaudio_reset capture_reset (.clk_i(capture_clk_i), .reset_i(reset_i), .rst_n(cap_rst_n_w));
  KL_usbaudio_reset release_reset (.clk_i(clk_i), .reset_i(reset_i), .rst_n(rst_n_w));
  wire selected_status_w = address_o == 1;
  wire selected_read_w = address_o == 3;
  wire tx_valid_w = selected_status_w ? status_valid_i : capture_valid_i && !capture_abort_i;
  wire take_read_w = selected_read_w && flag_sync_r && rx_ready_i;
  wire take_write_w = !selected_read_w && flag_sync_r && tx_valid_w;
  assign rx_valid_o = state_r == PUSH_S;
  assign rx_data_o = rx_r;
  assign capture_ready_o = state_r == WRITE_S && !selected_status_w;
  assign status_ready_o = state_r == WRITE_S && selected_status_w;
  always_ff @(posedge capture_clk_i) begin : input_capture
    if (!cap_rst_n_w) captured_r <= 0;
    else captured_r <= dq_i;
  end : input_capture
  always_ff @(posedge clk_i or negedge rst_n_w) begin : flag_crossing
    if (!rst_n_w) begin
      flag_meta_r <= 0;
      flag_sync_r <= 0;
    end else begin
      flag_meta_r <= flaga_i;
      flag_sync_r <= flag_meta_r;
    end
  end : flag_crossing
  always_comb begin : next_state
    next_w = state_r;
    case (state_r)
      TURN_S: if (delay_r == 0) next_w = SELECT_S;
      SELECT_S: next_w = SETTLE_S;
      SETTLE_S: if (delay_r == 0) next_w = CHECK_S;
      CHECK_S: next_w = take_read_w ? READ_S : take_write_w ? WRITE_S : TURN_S;
      WRITE_S: next_w = QUIET_S;
      QUIET_S: if (delay_r == 0) next_w = TURN_S;
      READ_S: next_w = READ_WAIT_S;
      READ_WAIT_S: if (delay_r == 0) next_w = CAPTURE_S;
      CAPTURE_S: next_w = PUSH_S;
      PUSH_S: if (rx_ready_i) next_w = TURN_S;
      default: next_w = TURN_S;
    endcase
  end : next_state
  always_ff @(posedge clk_i or negedge rst_n_w) begin : bus_schedule
    if (!rst_n_w) begin
      state_r <= TURN_S;
      delay_r <= 2;
      read_turn_r <= 1;
      rx_r <= 0;
      status_age_r <= 0;
      dq_o <= 0;
      dq_t_o <= '1;
      address_o <= 0;
      slwr_n_o <= 1;
      slrd_n_o <= 1;
      sloe_n_o <= 1;
      pktend_n_o <= 1;
    end else begin
      state_r <= next_w;
      dq_t_o <= {16{next_w != WRITE_S}};
      slwr_n_o <= next_w != WRITE_S;
      slrd_n_o <= next_w != READ_S;
      sloe_n_o <= !(next_w == READ_S || next_w == READ_WAIT_S || next_w == CAPTURE_S);
      pktend_n_o <= 1;
      if (status_age_r < BUS_HZ_P/2000) status_age_r <= status_age_r+1'b1;
      case (state_r)
        TURN_S, SETTLE_S, QUIET_S, READ_WAIT_S:
          if (delay_r != 0) delay_r <= delay_r-1'b1;
        SELECT_S: begin
          // Audio owns ordinary arbitration. A due status gets a bounded
          // ten-word turn; this avoids starvation under saturated PCM.
          if (status_valid_i && status_age_r >= BUS_HZ_P/2000) address_o <= 1;
          else if (read_turn_r) address_o <= 3;
          else if (capture_valid_i) address_o <= 0;
          else if (status_valid_i) address_o <= 1;
          else address_o <= 3;
          delay_r <= 6;
        end
        CHECK_S: begin
          if (take_write_w) begin
            dq_o <= selected_status_w ? status_data_i : capture_data_i;
            pktend_n_o <= !(selected_status_w ? status_last_i : capture_last_i);
          end else if (!take_read_w) begin
            read_turn_r <= !read_turn_r;
            delay_r <= 2;
          end
        end
        WRITE_S: begin
          delay_r <= 5;
          read_turn_r <= 1;
          if (selected_status_w && status_last_i) status_age_r <= 0;
        end
        READ_S: delay_r <= 1;
        CAPTURE_S: rx_r <= captured_r;
        PUSH_S: if (rx_ready_i) begin
          delay_r <= 2;
          read_turn_r <= 0;
        end
        default: ;
      endcase
    end
  end : bus_schedule
endmodule
`default_nettype wire
