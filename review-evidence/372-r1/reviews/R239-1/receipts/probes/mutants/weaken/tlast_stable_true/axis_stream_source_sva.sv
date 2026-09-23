/*
 * SPDX-FileCopyrightText: 2026 Kebag Logic
 * SPDX-License-Identifier: CERN-OHL-W-2.0
 */
//---------------------------------------------------------------------------//
//  File        : axis_stream_source_sva.sv
//  Project     : Milan TSN NIC -- assertion-based verification (#372)
//
//  Description : The source obligations of ONE AXI4-Stream interface, as a
//                simulation-only checker (Arm IHI0051A section 2.2). Once a
//                source raises TVALID it holds TVALID, TDATA, TKEEP and TLAST
//                unchanged until the rising edge at which TREADY takes the
//                beat. Each signal is its own labelled property, so a failure
//                names the one signal that moved.
//
//                The one design decision that matters is WHOSE obligation a
//                failure is. The properties are the same on every interface,
//                so the owner is carried by the instance name: a bound checker
//                instantiates this module as `u_<port>_stimulus` where the
//                testbench or an upstream block drives TVALID, and as
//                `u_<port>_dut` where the design under test does. A stimulus
//                failure is a testbench defect, a DUT failure a design defect.
//
//                Reset: every property samples the rising edge and is
//                disabled while rst_n is low, so an attempt that overlaps a
//                reset is abandoned, not failed. A stalled beat that a reset
//                discards is legal.
//
//                Witness: each property's pass action reports, through the
//                `axis_sva_witness` DPI call, whether the attempt it completed
//                was non-vacuous (the beat really was stalled at the previous
//                edge). Pinned Verilator 5.050 runs a pass action at EVERY
//                passing edge, vacuous or not, so the flag is the witness and
//                the call is not: a harness counts flagged calls only, and
//                compares them with its own port-level count of the same
//                stalls. See docs/testing/ASSERTIONS.md.
//---------------------------------------------------------------------------//

`default_nettype none

module axis_stream_source_sva #(
  parameter int unsigned TDATA_WIDTH_P = 64 //! TDATA width in bits; a whole, non-zero number of bytes
) (
  input wire                       clk_i,    //! the interface clock; every property samples its rising edge
  input wire                       rst_n,    //! synchronous, active-low; every property is disabled while it is low
  input wire                       tvalid_i, //! TVALID, as the source drives it
  input wire                       tready_i, //! TREADY, as the sink drives it
  input wire [TDATA_WIDTH_P-1:0]   tdata_i,  //! TDATA, as the source drives it
  input wire [TDATA_WIDTH_P/8-1:0] tkeep_i,  //! TKEEP, as the source drives it
  input wire                       tlast_i   //! TLAST, as the source drives it
);

  if (TDATA_WIDTH_P == 0 || TDATA_WIDTH_P % 8 != 0) begin : gen_guard_tdata_width
    $error("axis_stream_source_sva: TDATA_WIDTH_P=%0d is not a whole, non-zero number of bytes",
           TDATA_WIDTH_P);
  end

  //! Reports one completed attempt of the property named `rule_name`;
  //! `nonvacuous` is set when the antecedent really held one edge earlier.
  import "DPI-C" context function void axis_sva_witness(input string rule_name,
                                                        input bit nonvacuous);

  //! the source offers a beat that the sink does not take at this edge
  logic stalled_w;
  assign stalled_w = tvalid_i && !tready_i;

  ap_tvalid_held_until_handshake: assert property (
      @(posedge clk_i) disable iff (!rst_n) stalled_w |=> tvalid_i)
    axis_sva_witness("ap_tvalid_held_until_handshake", $past(rst_n && stalled_w));
  else
    $error("TVALID fell before TREADY took the beat (IHI0051A 2.2)");

  ap_tdata_stable_until_handshake: assert property (
      @(posedge clk_i) disable iff (!rst_n) stalled_w |=> $stable(tdata_i))
    axis_sva_witness("ap_tdata_stable_until_handshake", $past(rst_n && stalled_w));
  else
    $error("TDATA changed while the beat was stalled (IHI0051A 2.2)");

  ap_tkeep_stable_until_handshake: assert property (
      @(posedge clk_i) disable iff (!rst_n) stalled_w |=> $stable(tkeep_i))
    axis_sva_witness("ap_tkeep_stable_until_handshake", $past(rst_n && stalled_w));
  else
    $error("TKEEP changed while the beat was stalled (IHI0051A 2.2)");

  ap_tlast_stable_until_handshake: assert property (
      @(posedge clk_i) disable iff (!rst_n) stalled_w |=> 1'b1)
    axis_sva_witness("ap_tlast_stable_until_handshake", $past(rst_n && stalled_w));
  else
    $error("TLAST changed while the beat was stalled (IHI0051A 2.2)");

endmodule

`default_nettype wire
