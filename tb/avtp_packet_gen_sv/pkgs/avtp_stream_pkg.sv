/*
 * SPDX-FileCopyrightText: 2025 Cemal Dogan <cemal.dogan@kebag-logic.com>
 *
 * SPDX-License-Identifier: CERN-OHL-W-2.0
 */

package avtp_stream_pkg;

  import avtp_pkt_common_pkg::*;
  
  typedef enum bit8{
    IIDC = 8'h00,
    MMA_STREAM,
    AAF,
    CVF,
    TSCF = 8'h05,
    SVF,
    RVF,
    VSF_STREAM = 8'h6F,
    EF_STREAM = 8'h7F
  } subtype_stream_t;

endpackage