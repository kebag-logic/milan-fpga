/*
 * SPDX-FileCopyrightText: 2025 Cemal Dogan <cemal.dogan@kebag-logic.com>
 *
 * SPDX-License-Identifier: CERN-OHL-W-2.0
 */

package avtp_alter_pkg;

  import avtp_pkt_common_pkg::*;

  typedef enum bit8 {
    CRF = 8'h04,
    AEF_CONTINUOUS = 8'h6E,
    NTSCF = 8'h82,
    ESCF = 8'hEC,
    EECF,
    AEF_DISCRETE
  } subtype_alter_t;

endpackage