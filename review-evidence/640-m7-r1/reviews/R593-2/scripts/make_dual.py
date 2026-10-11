#!/usr/bin/env python3
"""Build the dual-instance differential probe (reviewer probe, R593-2).

Usage: python3 -I make_dual.py <exact-head tree copy> <dual dir>

<dual dir>/dev must already hold the dev-base (e8454e27 / donor 5dce647a)
copies of KL_gptp_shadow, KL_gptp_txret, KL_gptp_engine, KL_gptp_timer and
gptp_shadow_wrap with every one of those module names suffixed `_dev`.

The probe takes the exact-head gptp_tables wrapper and harness unchanged
and adds, beside the head plane `u_bench`, a dev-base plane `u_dev` driven
by the same inputs (the same test-only result-face force is applied to
both). Every cycle outside reset and outside the decode check it compares
the planes' module outputs and their internal plane-visible faces (engine
byte faces, tap FIFO strobes, result face while offered, departure take,
credit hold) and counts mismatching cycles. The harness grades that count
at zero and the compared-cycle count as coverage.
"""
import sys
from pathlib import Path

head = Path(sys.argv[1])
dual = Path(sys.argv[2])
src = head / "tb/verilator/gptp_tables"

wrap = (src / "gptp_tables_wrap.sv").read_text()
cpp = (src / "sim_main.cpp").read_text()

def once(text, old, new):
    assert text.count(old) == 1, old
    return text.replace(old, new, 1)

# ---- new outputs -----------------------------------------------------------
wrap = once(wrap, "    output logic  [7:0] tmr_slots_o     //! slots compared, as a set\n);",
            "    output logic  [7:0] tmr_slots_o,    //! slots compared, as a set\n"
            "    output logic [31:0] dual_mm_o,\n"
            "    output logic [31:0] dual_cmp_o,\n"
            "    output logic [31:0] dual_txbeats_o,\n"
            "    output logic [31:0] dual_res_o,\n"
            "    output logic [31:0] dual_first_o,\n"
            "    output logic [31:0] dual_raw_o\n);")

# ---- the dev-base plane ----------------------------------------------------
dev_inst = """
  wire [63:0] d_tx_tdata; wire [7:0] d_tx_tkeep; wire d_tx_tvalid, d_tx_tlast;
  wire [31:0] d_pub_flags; wire [63:0] d_phc_ns;
  wire d_txts_v; wire [63:0] d_txts_ns; wire [15:0] d_txts_seq; wire [3:0] d_txts_type; wire d_txts_ok;
  wire [15:0] d_tap_drop, d_rx_drop, d_ev_drop, d_prog_run, d_txts_lost, d_txts_barr;
  gptp_shadow_wrap_dev #(
      .UCODE_HEX_P   (UCODE_HEX_P),
      .CLK_HZ_P      (CLK_HZ_P),
      .PHC_TICK_NS_P (8)
  ) u_dev (
      .clk_i (clk_i), .rst_n (rst_n),
      .rx_tdata_i (rx_tdata_i), .rx_tkeep_i (rx_tkeep_i), .rx_tvalid_i (rx_tvalid_i),
      .rx_tready_i (rx_tready_i), .rx_tlast_i (rx_tlast_i),
      .tx_tdata_o (d_tx_tdata), .tx_tkeep_o (d_tx_tkeep), .tx_tvalid_o (d_tx_tvalid),
      .tx_tlast_o (d_tx_tlast), .tx_tready_i (tx_tready_i),
      .rechold_en_i (rechold_en_i), .rechold_type_i (rechold_type_i),
      .rechold_release_i (rechold_release_i),
      .recfault_en_i (1'b0), .recfault_mode_i (2'd0), .linkg_dis_i (1'b0),
      .linkg_freeze_i (1'b0), .cfg_mac_reinit_i (1'b0), .eth_alive_i (1'b1),
      .obs_rst_i (1'b0), .phc_en_i (1'b1), .phc_incr_i (32'h0800_0000),
      .phc_adj_ovr_en_i (1'b0), .phc_adj_ovr_i (32'sd0), .phc_load_i (1'b0),
      .phc_tod_wr_i (64'd0),
      .pub_flags_o (d_pub_flags), .phc_ns_o (d_phc_ns),
      .dbg_eng_txts_v_o (d_txts_v), .dbg_eng_txts_ns_o (d_txts_ns),
      .dbg_eng_txts_seq_o (d_txts_seq), .dbg_eng_txts_type_o (d_txts_type),
      .dbg_eng_txts_ok_o (d_txts_ok),
      .dbg_tap_drop_o (d_tap_drop), .dbg_rx_drop_o (d_rx_drop), .dbg_ev_drop_o (d_ev_drop),
      .dbg_prog_run_o (d_prog_run), .dbg_txts_lost_o (d_txts_lost), .dbg_txts_barr_o (d_txts_barr)
  );
"""
wrap = once(wrap, "  //! the plane's reset: the slice bench resets the plane with its own rst_n\n",
            dev_inst + "\n  //! the plane's reset: the slice bench resets the plane with its own rst_n\n")

# the same test-only force on the dev plane's result face
wrap = once(wrap,
            "      force u_bench.u_shadow.eng_txts_ready_w = 1'b0;\n",
            "      force u_bench.u_shadow.eng_txts_ready_w = 1'b0;\n"
            "      force u_dev.u_shadow.eng_txts_valid_w = 1'b0;\n"
            "      force u_dev.u_shadow.eng_txts_ready_w = 1'b0;\n")
wrap = once(wrap,
            "      release u_bench.u_shadow.eng_txts_ready_w;\n",
            "      release u_bench.u_shadow.eng_txts_ready_w;\n"
            "      release u_dev.u_shadow.eng_txts_valid_w;\n"
            "      release u_dev.u_shadow.eng_txts_ready_w;\n")

compare = """
  // ======================================================================= //
  //  reviewer probe: head plane against the dev-base plane                  //
  // ======================================================================= //
  `define H u_bench.u_shadow
  `define D u_dev.u_shadow
  logic dual_on_w, dual_bad_w;
  assign dual_on_w = rst_n && !kdec_en_i;
  assign dual_bad_w = dual_on_w && (
      (tx_tdata_o  != d_tx_tdata)  || (tx_tkeep_o  != d_tx_tkeep) ||
      (tx_tvalid_o != d_tx_tvalid) || (tx_tlast_o  != d_tx_tlast) ||
      (pub_flags_o != d_pub_flags) || (phc_ns_o    != d_phc_ns)   ||
      (dbg_eng_txts_v_o    != d_txts_v)    ||
      //! the bench's dbg_eng_txts_{ns,seq,type,ok} are the raw result-face
      //! nets; the engine samples them only on an accepted beat (v_o)
      (dbg_eng_txts_v_o && ((dbg_eng_txts_ns_o != d_txts_ns) ||
                            (dbg_eng_txts_seq_o  != d_txts_seq)  ||
                            (dbg_eng_txts_type_o != d_txts_type) ||
                            (dbg_eng_txts_ok_o   != d_txts_ok))) ||
      (dbg_tap_drop_o  != d_tap_drop)  || (dbg_rx_drop_o   != d_rx_drop) ||
      (dbg_ev_drop_o   != d_ev_drop)   || (dbg_prog_run_o  != d_prog_run) ||
      (dbg_txts_lost_o != d_txts_lost) || (dbg_txts_barr_o != d_txts_barr) ||
      (`H.fw_ready_w != `D.fw_ready_w) || (`H.ff_valid_w != `D.ff_valid_w) ||
      (`H.ff_ovf_w != `D.ff_ovf_w) || (`H.ff_bad_w != `D.ff_bad_w) ||
      (`H.ff_good_w != `D.ff_good_w) ||
      (`H.eng_rx_valid_w != `D.eng_rx_valid_w) ||
      (`H.eng_rx_valid_w && ((`H.eng_rx_data_w != `D.eng_rx_data_w) ||
                             (`H.eng_rx_sof_w  != `D.eng_rx_sof_w)  ||
                             (`H.eng_rx_eof_w  != `D.eng_rx_eof_w))) ||
      (`H.tx_byte_w != `D.tx_byte_w) ||
      (`H.tx_byte_w && ((`H.eng_tx_data_w != `D.eng_tx_data_w) ||
                        (`H.eng_tx_eof_w  != `D.eng_tx_eof_w))) ||
      (`H.gbo_valid_w != `D.gbo_valid_w) || (`H.gbo_ready_w != `D.gbo_ready_w) ||
      (`H.txf_out_valid_w != `D.txf_out_valid_w) ||
      (`H.u_txret.txts_valid_o != `D.u_txret.txts_valid_o) ||
      (`H.u_txret.txts_valid_o &&
         ((`H.u_txret.txts_ns_o   != `D.u_txret.txts_ns_o)   ||
          (`H.u_txret.txts_seq_o  != `D.u_txret.txts_seq_o)  ||
          (`H.u_txret.txts_type_o != `D.u_txret.txts_type_o) ||
          (`H.u_txret.txts_ok_o   != `D.u_txret.txts_ok_o)   ||
          (`H.u_txret.txts_gen_o  != `D.u_txret.txts_gen_o))) ||
      (`H.eng_txts_ready_w != `D.eng_txts_ready_w) ||
      (`H.u_txret.dep_take_o != `D.u_txret.dep_take_o) ||
      (`H.u_txret.credit_hold_o != `D.u_txret.credit_hold_o) ||
      (`H.u_txret.n_led_r != `D.u_txret.n_led_r) ||
      (`H.u_engine.u_timer.ev_valid_o != `D.u_engine.u_timer.ev_valid_o) ||
      (`H.u_engine.u_timer.ev_valid_o &&
         (`H.u_engine.u_timer.ev_slot_o != `D.u_engine.u_timer.ev_slot_o)));
  logic raw_face_diff_w;
  assign raw_face_diff_w = dual_on_w && !dbg_eng_txts_v_o &&
      ((dbg_eng_txts_ns_o != d_txts_ns) || (dbg_eng_txts_seq_o != d_txts_seq) ||
       (dbg_eng_txts_type_o != d_txts_type) || (dbg_eng_txts_ok_o != d_txts_ok));
  logic [31:0] dual_cyc_r;
  always_ff @(posedge clk_i) begin : dual_counters
    if (cnt_clr_i) begin
      dual_mm_o <= '0; dual_cmp_o <= '0; dual_txbeats_o <= '0; dual_res_o <= '0;
      dual_first_o <= '1; dual_cyc_r <= '0; dual_raw_o <= '0;
    end else begin
      dual_cyc_r <= dual_cyc_r + 32'd1;
      if (dual_on_w) dual_cmp_o <= dual_cmp_o + 32'd1;
      if (dual_bad_w) begin
        dual_mm_o <= dual_mm_o + 32'd1;
        if (dual_first_o == '1) dual_first_o <= dual_cyc_r;
      end
      if (raw_face_diff_w) dual_raw_o <= dual_raw_o + 32'd1;
      if (dual_on_w && tx_tvalid_o && tx_tready_i) dual_txbeats_o <= dual_txbeats_o + 32'd1;
      if (dual_on_w && `H.u_txret.txts_valid_o && `H.u_txret.txts_ready_i)
        dual_res_o <= dual_res_o + 32'd1;
    end
  end : dual_counters
  `undef H
  `undef D

endmodule : gptp_tables_wrap"""
wrap = once(wrap, "\nendmodule : gptp_tables_wrap", compare)

cpp = once(cpp, "    // the five lockstep verdicts: the names the mutation driver requires\n",
           "    std::printf(\"dual: %u compared, %u mismatching, first at %u, %u tx beats, %u results taken, %u idle raw-face cycles differ\\n\",\n"
           "                dut->dual_cmp_o, dut->dual_mm_o, dut->dual_first_o, dut->dual_txbeats_o, dut->dual_res_o, dut->dual_raw_o);\n"
           "    check.dec(\"dual: head plane against dev-base plane, mismatching cycles\", dut->dual_mm_o, 0);\n"
           "    check.that(\"dual coverage: compared cycles\", dut->dual_cmp_o >= 30000000u);\n"
           "    check.that(\"dual coverage: tx beats\", dut->dual_txbeats_o >= 10000u);\n"
           "    check.that(\"dual coverage: results taken\", dut->dual_res_o >= 1000u);\n"
           "    // the five lockstep verdicts: the names the mutation driver requires\n")

(dual / "gptp_tables_wrap.sv").write_text(wrap)
(dual / "sim_main.cpp").write_text(cpp)
print("wrote", dual / "gptp_tables_wrap.sv", dual / "sim_main.cpp")
