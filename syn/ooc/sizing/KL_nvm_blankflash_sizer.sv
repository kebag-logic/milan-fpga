/*
 * SPDX-FileCopyrightText: 2026 Kebag Logic
 * SPDX-License-Identifier: CERN-OHL-W-2.0
 */
//---------------------------------------------------------------------------//
//  File        : KL_nvm_blankflash_sizer.sv
//  Project     : Milan FPGA -- saved state and fast connect
//                (docs/design/SAVED_STATE_FASTCONNECT.md section 8.3)
//
//  Description : AREA SIZING SKETCH, the BEFORE half of a before/after pair.
//                The blank-flash responder hdl/milan/KL_pp_shadow.sv carried
//                until the saved-state backing store landed, lifted verbatim
//                so that the two numbers in section 8.3 are measured on the
//                same face. The AFTER half is the shipping module itself,
//                hdl/milan/KL_nvm_backend.sv, which replaced this responder
//                inside the shadow; the sizing sketch that stood in for it
//                while the decision was taken is retired.
//
//  WHY ITS OWN FILE. Both tops used to live in one sizing file, and the lint
//  command the PR published then exited 1 under Verilator 5.050 on
//  DECLFILENAME -- a file may declare one top-level module named after it.
//  One module per file makes the advertised lint command reproduce.
//
//  THIS IS NOT SHIPPING RTL, and it is deliberately NOT under `hdl/`.
//  Nothing instantiates it and `scripts/lint_rtl.py` (which sweeps `hdl/`)
//  does not see it. tb/verilator/nvm_backend lints it with `-Wall` and no
//  `-Wno-fatal`, so the lint claim is executable rather than recorded.
//
//  Measure with (see syn/yosys/README.md for the toolchain):
//    syn/yosys/ooc.sh KL_nvm_blankflash_sizer
//  It takes no OOC_CHPARAM: it has no parameters, and passing any makes yosys
//  refuse with `Can't find object for defparam`.
//---------------------------------------------------------------------------//
`default_nettype none

module KL_nvm_blankflash_sizer (
    input  wire        clk_i,          //! core clock
    input  wire        rst_n,          //! synchronous active-low reset

    //! ---- device face: target of KL_pp_nvm_port's initiator ----
    input  wire        dev_req_i,      //! command request
    output logic       dev_gnt_o,      //! command accepted (one cycle)
    input  wire [1:0]  dev_op_i,       //! READ / WRITE / ERASE_REGION
    input  wire [15:0] dev_len_i,      //! byte count
    input  wire        dev_wvalid_i,   //! write byte present
    output logic       dev_wready_o,   //! responder accepts the write byte
    output logic       dev_rvalid_o,   //! read byte present
    output logic [7:0] dev_rdata_o,    //! read byte -- blank flash is 0xFF
    input  wire        dev_rready_i,   //! initiator accepts the read byte
    output logic       dev_busy_o,     //! command in flight
    output logic       dev_done_o,     //! one-cycle pulse: complete
    output logic       dev_err_o,      //! one-cycle pulse: failed (never)
    output logic       nvm_backed_o    //! CONSTANT 0: no media behind the face
);

  localparam logic [1:0] NVMP_OP_READ_C  = 2'd0;
  localparam logic [1:0] NVMP_OP_WRITE_C = 2'd1;
  //! Deliberately a localparam, not a parameter: the fact is a property of
  //! the logic in this file, and a parameter would let an integrator assert
  //! persistence the fabric does not have.
  localparam logic       NVM_BACKED_C    = 1'b0;

  logic        nvm_gnt_r, nvm_done_r, nvm_rvalid_r, nvm_wready_r;
  logic [15:0] nvm_cnt_r;
  logic        nvm_busy_r;

  always_ff @(posedge clk_i) begin
    if (!rst_n) begin
      nvm_busy_r   <= 1'b0;
      nvm_gnt_r    <= 1'b0;
      nvm_done_r   <= 1'b0;
      nvm_rvalid_r <= 1'b0;
      nvm_wready_r <= 1'b0;
      nvm_cnt_r    <= 16'd0;
    end else begin
      nvm_gnt_r  <= 1'b0;
      nvm_done_r <= 1'b0;
      if (!nvm_busy_r) begin
        nvm_rvalid_r <= 1'b0;
        nvm_wready_r <= 1'b0;
        if (dev_req_i) begin
          nvm_gnt_r  <= 1'b1;
          nvm_cnt_r  <= dev_len_i;
          nvm_busy_r <= 1'b1;
          // ERASE (and any zero-length command) completes with no data phase
          if ((dev_op_i != NVMP_OP_READ_C && dev_op_i != NVMP_OP_WRITE_C)
              || (dev_len_i == 16'd0)) begin
            nvm_busy_r <= 1'b0;
            nvm_done_r <= 1'b1;
          end else begin
            nvm_rvalid_r <= (dev_op_i == NVMP_OP_READ_C);
            nvm_wready_r <= (dev_op_i == NVMP_OP_WRITE_C);
          end
        end
      end else begin
        // one byte per accepted handshake, blank flash reads as 0xFF
        if ((nvm_rvalid_r & dev_rready_i) | (nvm_wready_r & dev_wvalid_i)) begin
          if (nvm_cnt_r <= 16'd1) begin
            nvm_busy_r   <= 1'b0;
            nvm_rvalid_r <= 1'b0;
            nvm_wready_r <= 1'b0;
            nvm_done_r   <= 1'b1;
          end else begin
            nvm_cnt_r <= nvm_cnt_r - 16'd1;
          end
        end
      end
    end
  end

  assign dev_gnt_o    = nvm_gnt_r;
  assign dev_wready_o = nvm_wready_r;
  assign dev_rvalid_o = nvm_rvalid_r;
  assign dev_rdata_o  = 8'hFF;
  assign dev_busy_o   = nvm_busy_r;
  assign dev_done_o   = nvm_done_r;
  assign dev_err_o    = 1'b0;
  assign nvm_backed_o = NVM_BACKED_C;

endmodule

`default_nettype wire
