/*
 * SPDX-FileCopyrightText: 2026 Kebag Logic
 * SPDX-License-Identifier: CERN-OHL-W-2.0
 */
//---------------------------------------------------------------------------//
//  File        : timer_map_wrap.sv
//  Project     : IEEE 1722.1 protocol processor
//                (docs/architecture/08 §5 F08.4 timer-slot map;
//                 02 §5 event-router source map)
//
//  Description : Elaborates pp_pkg's two index maps at a fixed table of
//                SHAPES and publishes every base as a port, so a C++ model
//                that re-derives F08.4 from the document can grade them.
//
//                The maps are pure elaboration arithmetic — there is no
//                state and no clock — so the DUT here is the FUNCTION, not a
//                datapath. That is exactly the level the defect lived at: a
//                literal map is right at one shape and silently aliases at
//                every other, and no simulation of the 8x8 shape can ever
//                see it.
//
//                Shapes are elaborated as separate instances rather than
//                looped in C++ because a parameter is an elaboration-time
//                value: only a real instance proves what the tool computes.
//---------------------------------------------------------------------------//
`default_nettype none

//! one shape: SI x SO through both maps, flattened onto 32-bit ports
module timer_map_probe
  import pp_pkg::*;
#(
    parameter int unsigned SI_P = 8,
    parameter int unsigned SO_P = 8
) (
    //! F08.4 slot map (08 §5)
    output logic [31:0] adp_adv_o,
    output logic [31:0] adp_noadp_o,
    output logic [31:0] lstn_o,
    output logic [31:0] tkr_o,
    output logic [31:0] regmon_o,
    output logic [31:0] capool_o,
    output logic [31:0] single_o,
    output logic [31:0] maap_o,
    output logic [31:0] base_end_o,
    output logic [31:0] srp_cad_o,
    output logic [31:0] srp_tk_o,
    output logic [31:0] srp_ls_o,
    output logic [31:0] srp_end_o,
    //! the width the top derives for the slot index
    output logic [31:0] slot_aw_o,
    //! 02 §5 event-router source map
    output logic [31:0] evr_tk_reg_o,
    output logic [31:0] evr_tk_unreg_o,
    output logic [31:0] evr_adp_disc_o,
    output logic [31:0] evr_adp_dep_o,
    output logic [31:0] evr_domain_o,
    output logic [31:0] evr_lsn_chg_o,
    output logic [31:0] evr_gm_chg_o,
    output logic [31:0] evr_link_o,
    output logic [31:0] evr_n_src_o,
    output logic [31:0] evr_src_w_o
);
  localparam pp_timer_map_t M_C =
      pp_timer_map(PP_N_IF_C, SI_P, SO_P, PP_N_CTRL_C, PP_CA_POOL_C);
  localparam pp_evr_map_t   E_C = pp_evr_map(SI_P, SO_P);

  assign adp_adv_o   = 32'(M_C.adp_adv);
  assign adp_noadp_o = 32'(M_C.adp_noadp);
  assign lstn_o      = 32'(M_C.lstn);
  assign tkr_o       = 32'(M_C.tkr);
  assign regmon_o    = 32'(M_C.regmon);
  assign capool_o    = 32'(M_C.capool);
  assign single_o    = 32'(M_C.single);
  assign maap_o      = 32'(M_C.maap);
  assign base_end_o  = 32'(M_C.base_end);
  assign srp_cad_o   = 32'(M_C.srp_cad);
  assign srp_tk_o    = 32'(M_C.srp_tk);
  assign srp_ls_o    = 32'(M_C.srp_ls);
  assign srp_end_o   = 32'(M_C.srp_end);
  assign slot_aw_o   = 32'($clog2(M_C.srp_end));

  assign evr_tk_reg_o   = 32'(E_C.tk_reg);
  assign evr_tk_unreg_o = 32'(E_C.tk_unreg);
  assign evr_adp_disc_o = 32'(E_C.adp_disc);
  assign evr_adp_dep_o  = 32'(E_C.adp_dep);
  assign evr_domain_o   = 32'(E_C.domain);
  assign evr_lsn_chg_o  = 32'(E_C.lsn_chg);
  assign evr_gm_chg_o   = 32'(E_C.gm_chg);
  assign evr_link_o     = 32'(E_C.link);
  assign evr_n_src_o    = 32'(E_C.n_src);
  assign evr_src_w_o    = 32'((E_C.n_src > 1) ? $clog2(E_C.n_src) : 1);
endmodule

//! the shape table. Row 5 is the F01.5 default (the historical literal map);
//! row 6 is the 9x9 shape the reference platform's generated header asks for
//! (ADP_TALKER_SRC_C = ADP_LISTENER_SINK_C = 9: the CRF Media Clock Output
//! is itself a source and a sink), where every literal map aliased.
module timer_map_wrap
  import pp_pkg::*;
(
    output logic [31:0] si_o    [0:9],
    output logic [31:0] so_o    [0:9],
    output logic [31:0] map_o   [0:9][0:13],
    output logic [31:0] evr_o   [0:9][0:9]
);
  localparam int unsigned N_SHAPE_C = 10;
  localparam int unsigned SI_TBL_C [0:9] = '{1, 1, 8, 2, 4, 8, 9, 9,  3, 16};
  localparam int unsigned SO_TBL_C [0:9] = '{1, 8, 1, 2, 4, 8, 9, 2, 12, 16};

  for (genvar g = 0; g < int'(N_SHAPE_C); g++) begin : gen_shape
    timer_map_probe #(
        .SI_P (SI_TBL_C[g]),
        .SO_P (SO_TBL_C[g])
    ) u_probe (
        .adp_adv_o      (map_o[g][0]),
        .adp_noadp_o    (map_o[g][1]),
        .lstn_o         (map_o[g][2]),
        .tkr_o          (map_o[g][3]),
        .regmon_o       (map_o[g][4]),
        .capool_o       (map_o[g][5]),
        .single_o       (map_o[g][6]),
        .maap_o         (map_o[g][7]),
        .base_end_o     (map_o[g][8]),
        .srp_cad_o      (map_o[g][9]),
        .srp_tk_o       (map_o[g][10]),
        .srp_ls_o       (map_o[g][11]),
        .srp_end_o      (map_o[g][12]),
        .slot_aw_o      (map_o[g][13]),
        .evr_tk_reg_o   (evr_o[g][0]),
        .evr_tk_unreg_o (evr_o[g][1]),
        .evr_adp_disc_o (evr_o[g][2]),
        .evr_adp_dep_o  (evr_o[g][3]),
        .evr_domain_o   (evr_o[g][4]),
        .evr_lsn_chg_o  (evr_o[g][5]),
        .evr_gm_chg_o   (evr_o[g][6]),
        .evr_link_o     (evr_o[g][7]),
        .evr_n_src_o    (evr_o[g][8]),
        .evr_src_w_o    (evr_o[g][9])
    );
    assign si_o[g] = 32'(SI_TBL_C[g]);
    assign so_o[g] = 32'(SO_TBL_C[g]);
  end

  //! the owner-tag allocation the top bounds its shape against (pp_pkg)
  // verilator lint_off UNUSEDPARAM
  localparam logic [7:0] OWN_LSTN_C    = PP_OWN_LSTN_C;
  localparam logic [7:0] OWN_SRP_TK_C  = PP_OWN_SRP_TK_C;
  localparam logic [7:0] OWN_TKR_C     = PP_OWN_TKR_C;
  localparam logic [7:0] OWN_SRP_LS_C  = PP_OWN_SRP_LS_C;
  localparam logic [7:0] OWN_SRP_CAD_C = PP_OWN_SRP_CAD_C;
  localparam logic [7:0] OWN_MAAP_C    = PP_OWN_MAAP_C;
  // verilator lint_on UNUSEDPARAM
endmodule

`default_nettype wire
