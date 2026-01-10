/*
 * SPDX-FileCopyrightText: 2025 Cemal Dogan <cemal.dogan@kebag-logic.com>
 *
 * SPDX-License-Identifier: CERN-OHL-W-2.0
 */

package avtp_pkt_common_pkg;

  typedef bit [7:0] bit8;
  typedef bit [15:0] bit16;
  typedef bit [31:0] bit32;
  typedef bit [63:0] bit64;

  typedef enum bit [1:0] {
    CONTROL_HDR, 
    STREAM_HDR, 
    ALTER_HDR
  } subtype_t;

  typedef struct {
    bit8 subtype;
    bit h;
    bit [2:0] ver;
    string name;
  } avtp_common_hdr_t;

endpackage