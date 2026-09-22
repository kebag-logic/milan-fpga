/*
 * SPDX-FileCopyrightText: 2026 Kebag Logic
 * SPDX-License-Identifier: CERN-OHL-W-2.0
 */
//---------------------------------------------------------------------------//
//  File        : ucpu_pkg.sv
//  Project     : IEEE 1722.1 protocol processor (docs/architecture/06 §8)
//
//  Description : µISA encoding for the AECP micro-coded engine — the concrete
//                proposal for the width 06 §8 leaves unstated. One µop is
//                48 bits (P-UCODE-ROM-DEPTH × 48 = 2048 × 48 = 98,304 bits
//                = 3 RAMB36 on the reference part):
//
//                  [47:43] op     one of the 29 operations of 06 §8
//                  [42:39] rd     destination operand register
//                  [38:35] ra     source operand register A
//                  [34:31] rb     source operand register B / mask
//                  [30:28] fmt    field width: 0=byte 1=word16 2=dword32
//                                 3=qword64 (moves, fields, compares)
//                  [27:24] cnd    condition / check / gather selector
//                  [23:0]  imm24  branch target [10:0], state offset [19:0],
//                                 literal, or status code [4:0] by op
//
//                The register file is 16 × 64 bits. r13..r15 are preloaded at
//                dispatch with the normalized-transaction operands (03 §4):
//                r15 = {controller_eid}, r14 = {opd0: descriptor_type|index|
//                arg}, r13 = {opd1}. r0 reads as zero by convention of the
//                generated µcode, not of the hardware.
//---------------------------------------------------------------------------//
`default_nettype none

package ucpu_pkg;

  // ---- µop field extraction --------------------------------------------
  localparam int unsigned UCODE_W_C  = 48;
  localparam int unsigned UPC_W_C    = 11;   // P-UCODE-ROM-DEPTH = 2048

  typedef struct packed {
    logic [4:0]  op;
    logic [3:0]  rd;
    logic [3:0]  ra;
    logic [3:0]  rb;
    logic [2:0]  fmt;
    logic [3:0]  cnd;
    logic [23:0] imm;
  } uop_t;

  // ---- the 29 operations of 06 §8, group order --------------------------
  typedef enum logic [4:0] {
    // Flow
    OP_NOP        = 5'd0,
    OP_BRANCH     = 5'd1,
    OP_BR_STATUS  = 5'd2,   // BRANCH_IF_STATUS
    OP_END        = 5'd3,
    // Data
    OP_MOVE       = 5'd4,
    OP_COMPARE    = 5'd5,
    OP_SET_MASKED = 5'd6,
    // Model (image + overlay via 07 §3)
    OP_DESC_ADDR  = 5'd7,
    OP_READ_ST    = 5'd8,   // READ_STATE
    OP_WRITE_ST   = 5'd9,   // WRITE_STATE
    OP_NAME_RD    = 5'd10,
    OP_NAME_WR    = 5'd11,
    OP_COPY_BUF   = 5'd12,  // COPY_BUFFER
    // Checks
    OP_CHECK_LOCK = 5'd13,
    OP_CHECK_ARG  = 5'd14,
    OP_MAP_VALID  = 5'd15,  // MAP_VALIDATE
    // Gather
    OP_GATHER_EXT = 5'd16,
    OP_READ_CTRS  = 5'd17,  // READ_COUNTERS
    // Iterate
    OP_ITER_OPEN  = 5'd18,
    OP_ITER_NEXT  = 5'd19,
    OP_APPEND     = 5'd20,  // APPEND_RESP (skip-on-overflow, 06 §8)
    // Effects
    OP_COMMIT     = 5'd21,
    OP_NVM_MARK   = 5'd22,
    OP_NOTIFY_ENQ = 5'd23,
    // Respond
    OP_SET_STATUS = 5'd24,
    OP_SET_LENGTH = 5'd25,
    OP_BUILD_HDR  = 5'd26,  // BUILD_HEADER
    OP_BUILD_FLD  = 5'd27,  // BUILD_FIELD
    OP_SEND_RESP  = 5'd28,  // SEND_RESPONSE
    OP_SHIFT_R    = 5'd29   // logical right shift by imm[5:0]
  } ucpu_op_e;

  // ---- fmt codes ---------------------------------------------------------
  localparam logic [2:0] FMT_B_C = 3'd0;
  localparam logic [2:0] FMT_W_C = 3'd1;
  localparam logic [2:0] FMT_D_C = 3'd2;
  localparam logic [2:0] FMT_Q_C = 3'd3;

  // ---- CHECK_ARG / COMPARE relations (cnd field) -------------------------
  localparam logic [3:0] REL_EQ_C = 4'd0;
  localparam logic [3:0] REL_NE_C = 4'd1;
  localparam logic [3:0] REL_LT_C = 4'd2;
  localparam logic [3:0] REL_GE_C = 4'd3;
  localparam logic [3:0] REL_IN_C = 4'd4;  // set-membership via gather-side rom

  // ---- AECP status codes carried by the 5-bit status register ------------
  // (values = IEEE 1722.1-2021 Table 7-141 low codes; the full 8-bit wire
  //  status is formed by the response builder header stage)
  localparam logic [4:0] ST_SUCCESS_C        = 5'd0;
  localparam logic [4:0] ST_NOT_IMPLEMENTED_C = 5'd1;
  localparam logic [4:0] ST_NO_SUCH_DESC_C   = 5'd2;
  localparam logic [4:0] ST_LOCKED_C         = 5'd3;
  localparam logic [4:0] ST_BAD_ARGUMENTS_C  = 5'd7;
  //! Table 7-141 status 8: Milan §5.4.2.21's refusal when the registered-
  //! controller list is full (E_REGUN's failure arm)
  localparam logic [4:0] ST_NO_RESOURCES_C   = 5'd8;
  //! IEEE 1722.1-2021 §7.4 status 10: the entity detected an internal error.
  //! KL_aecp_engine answers with it when the response memory fails under a
  //! frame it has already started building — never a SUCCESS carrying bytes
  //! nobody read.
  localparam logic [4:0] ST_ENTITY_MISBEHAVING_C = 5'd10;
  localparam logic [4:0] ST_NOT_SUPPORTED_C  = 5'd11;

  // ---- response buffer geometry (Milan §5.4.2.5: 524-byte payload cap) ---
  localparam int unsigned RESP_BYTES_C = 576;   // one TX slot, 03 §2
  localparam int unsigned RESP_CAP_C   = 524;   // APPEND_RESP overflow line

endpackage : ucpu_pkg
`default_nettype wire
