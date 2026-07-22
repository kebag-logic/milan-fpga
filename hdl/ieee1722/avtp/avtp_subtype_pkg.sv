/*
 * SPDX-FileCopyrightText: 2025 Cemal Dogan <cemal.dogan@kebag-logic.com>
 *
 * SPDX-License-Identifier: CERN-OHL-W-2.0
*/

/*
------------------------------------------------------------------------------
  File        : avtp_subtype_pkg.sv
  Author      : Cemal Dogan 

                cemal.dogan@kebag-logic.com

  Date        : 2025-12-28
  Description : AVTP Subtype package

  Company     : Kebag Logic
  Project     : AVTP Parsing 

------------------------------------------------------------------------------
*/


package avtp_subtype_pkg;

  //! AVTP possible subtype-field from
  //! IEEE 1722-2016 Table 6. AVTP Stream data subtype values
  typedef enum bit [7:0] {
    IIDC,
    MMA_STREAM,
    AAF,
    CVF,
    CRF,
    TSCF,
    SVF,
    RVF,
    AEF_CONTINUOUS = 8'h6E,
    VSF_STREAM,
    EF_STREAM      = 8'h7F,
    NTSCF          = 8'h82,
    ESCF           = 8'hEC,
    EECF,
    AEF_DISCRETE,
    ADP            = 8'hFA,
    AECP,
    ACMP,
    MAAP           = 8'hFE,
    EF_CONTROL
  } subtype_enum_t;

endpackage : avtp_subtype_pkg