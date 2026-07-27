/*
 * SPDX-FileCopyrightText: 2025 Oguz Kahraman <oguz.kahraman@kebag-logic.com>
 *
 * SPDX-License-Identifier: CERN-OHL-W-2.0
 */

//! Signal-bundle AXI4-Stream interface.
//!
//! TDATA_WIDTH_P DEFAULTS TO 64 BECAUSE 64 IS THE ONLY WIDTH THIS TREE HAS.
//! `common/parameters.svh` defines `AXIS_DATA_WIDTH 64` and every one of the
//! 53 instantiations in hdl/ and tb/ passes `.TDATA_WIDTH_P(...)` explicitly,
//! resolving to 64 in all of them - so the default is never used by an
//! elaboration and changing it cannot move one. It was 32, and that was not
//! free: a module whose only port is `axi_stream_if.slave` is elaborated at
//! the INTERFACE default when linted (or elaborated) as its own top, so the
//! 32 made 20 of the tree's 21 SELRANGE findings - constant bit selects above
//! bit 31 in KL_adp_parser (14), ptp_ts_core (5) and KL_avtp_common_parser (1)
//! - out of range in a narrow elaboration nothing instantiates, and cost two
//! `lint_off SELRANGE` pragmas in hdl/ieee17221/aecp/ to paper over.  A
//! default that no caller uses should name the tree it lives in.
interface axi_stream_if #(
  parameter TDATA_WIDTH_P = 64,
  parameter TID_WIDTH_P = 1,
  parameter TDEST_WIDTH_P = 1,
  parameter TUSER_WIDTH_P = 1
  )
  (
    input bit clk,
    input bit rst_n
  );

  logic tready;
  logic tvalid;
  logic tlast;
  logic [TDATA_WIDTH_P - 1 : 0] tdata;
  logic [TDATA_WIDTH_P/8 - 1 : 0] tkeep;
  logic [TDATA_WIDTH_P/8 - 1 : 0] tstrb;
  logic [TID_WIDTH_P - 1 : 0] tid;
  logic [TDEST_WIDTH_P - 1 : 0] tdest;
  logic [TUSER_WIDTH_P - 1 : 0] tuser;

  modport master (input tready, output tvalid, tlast, tdata, tid, tstrb, tdest, tuser, tkeep);
  modport slave (input tvalid, tlast, tdata, tid, tstrb, tdest, tuser, tkeep, output tready);

endinterface : axi_stream_if