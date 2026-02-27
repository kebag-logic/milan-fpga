/*
 * SPDX-FileCopyrightText: 2025 Oguz Kahraman <oguz.kahraman@kebag-logic.com>
 *
 * SPDX-License-Identifier: CERN-OHL-W-2.0
 */

/*
------------------------------------------------------------------------------
  File        : credit_based_shaper.sv
  Author      : Oguz Kahraman

                oguz.kahraman@kebag-logic.com

  Date        : 2025-07-05
  Description : Credit-Based Shaper (CBS) module implementing IEEE 802.1Qav
                traffic shaping for time-sensitive networking (TSN). The
                module maintains a credit counter per queue to control
                transmission eligibility based on configured idle and send
                slopes.

                - Increases credit during idle time (idle slope)
                - Decreases credit when transmitting (send slope)
                - Transmission is allowed only when credit >= 0

  Company     : Kebag Logic
  Project     : 802.1Q Traffic Shaper

------------------------------------------------------------------------------
*/

`include "ethernet_packet_pkg.sv"
import ethernet_packet_pkg::*;

`default_nettype none

module credit_based_shaper #(
  parameter int IDLE_SLOPE_1G = 750_000_000,  //! Idle slope in bits per second for 1G(bps)
  parameter int IDLE_SLOPE_100M = 75_000_000, //! Idle slope in bits per second for 100M(bps)
  parameter int HI_CREDIT = 1536,          //! Maximum credit (bytes), scaled internally
  parameter int LO_CREDIT = -1536,         //! Minimum credit (bytes), scaled internally
  parameter int CLK_FREQ_HZ = 125_000_000  //! Clock frequency in Hz (system uses 100_000_000 from
  //! ethernet_packet_pkg)
)(
  input wire clk,                          //! clock signal
  input wire resetn,                       //! Synhronous active low reset

  input wire queue_has_data_i,             //! Queue has data ready to send
  input wire is_transmitting_i,            //! High when the queue is actively transmitting
  input wire is_1g_i,                      //! High when the link rate is 1GBps
  input wire is_granted_i,                 //! High when the queue is granted
  input wire [15:0] bytes_sent_i,          //! Number of bytes sent in current cycle

  output wire allow_transmit_o             //! High when credit allows transmission
);

  //! Credit counter in Q31.16 fixed-point format (48-bit signed)
  (* use_dsp = "yes" *) logic signed [47:0] credit;

  //! Active idle slope (bps): IDLE_SLOPE_1G or IDLE_SLOPE_100M
  logic signed [47:0] idle_slope;
  //! Active send slope (bps): idle_slope - link_rate (always negative)
  logic signed [47:0] send_slope;
  //! Active link rate (bps): 1_000_000_000 or 100_000_000
  logic signed [47:0] link_rate;
  //! Q.16 fixed point slope computed for each cycle. It will be changed with SRP in the future
  //! Credit bytes earned per clock cycle during idle
  logic signed [47:0] idle_slope_per_cycle;
  //! Credit bytes lost per data byte transmitted
  logic signed [47:0] send_slope_per_byte;

  //! registered allow_transmit signal
  logic allow_transmit_reg;

  logic signed [47:0] send_delta;
  logic signed [47:0] credit_add_idle;
  logic is_transmitting;
  logic queue_has_data;
  logic is_granted;

  //! Dynamic slope calculation
  always_comb begin
    link_rate = is_1g_i ? 1_000_000_000 : 100_000_000;
    idle_slope = is_1g_i ? IDLE_SLOPE_1G : IDLE_SLOPE_100M;
    send_slope = idle_slope - link_rate;

    idle_slope_per_cycle = (idle_slope <<< FP_DECIMAL_POINT) / CLK_FREQ_HZ / BYTE_TO_BIT;
    send_slope_per_byte  = (send_slope <<< FP_DECIMAL_POINT) / link_rate;
  end

  //! Allow transmit if credit is non-negative
  assign allow_transmit_o = allow_transmit_reg;

  //! allow_transmit registered 
  always_ff @(posedge clk) begin : allow_transmit
    if(!resetn)begin
      allow_transmit_reg <= '0;
    end else begin
      allow_transmit_reg <= (credit >= 0);
    end
  end

  //! Register every signal for better timing
  always_ff @(posedge clk) begin : stage1_pipe
    if(!resetn)begin
      send_delta <= 'd0;
      credit_add_idle <= 'd0;
      is_transmitting <= 'd0;
      queue_has_data <= 'd0;
      is_granted <= 'd0;
    end
    else begin
      send_delta      <= send_slope_per_byte * $signed(bytes_sent_i);
      credit_add_idle <= idle_slope_per_cycle;
      is_transmitting <= is_transmitting_i;
      queue_has_data  <= queue_has_data_i;
      is_granted <= is_granted_i;
    end
  end

  //! Credit update logic
  always_ff @(posedge clk) begin : credit_update_logic
    if(!resetn)begin
      credit <= '0;
    end
    else begin
      if(is_transmitting) begin
        //! Apply send slope during transmission (bounded by LO_CREDIT)
        if(credit + send_delta < (LO_CREDIT <<< FP_DECIMAL_POINT))
          credit <= (LO_CREDIT <<< FP_DECIMAL_POINT);
        else
          credit <= credit + send_delta;
      end
      else if(is_granted && !is_transmitting)begin
        //! If downstream is not ready dont change credit value
      end
      //! If queue does not have data and not tranmitting and credit above zero then credit must
      //! be zero
      else if (!queue_has_data && !is_transmitting && credit >= 0) begin
        credit <= '0;
      end
      else if (!queue_has_data)begin
        //! If queue is empty and credit is negative, increment credit till 0
        if(credit < 0)begin
          credit <= (credit + credit_add_idle >= 0) ? 'd0 : credit + credit_add_idle;
        end
        else begin
          credit <= 'd0;
        end
      end
      //! Accumulate credit during idle (bounded by HI_CREDIT)
      else if(credit < (HI_CREDIT <<< FP_DECIMAL_POINT))begin
        credit <= (credit + credit_add_idle > (HI_CREDIT <<< FP_DECIMAL_POINT)) ?
                  (HI_CREDIT <<< FP_DECIMAL_POINT) : credit + credit_add_idle;
      end
    end
  end

endmodule

`default_nettype wire
