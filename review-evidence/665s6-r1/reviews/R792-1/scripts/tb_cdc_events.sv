// Reviewer probe (not a repository file): KL_mbx_cdc's event crossing, which the
// split leg does not drive. Each check prints PASS/FAIL; the last line is a tally.
// Build: verilator --binary --timing -Wno-fatal --top-module tb_cdc_events \
//   KL_mbx_pkg.sv cdc_handshake.sv cdc_pulse.sv KL_mbx_cdc_window.sv KL_mbx_cdc.sv tb_cdc_events.sv
`timescale 1ns/1ps
`default_nettype none
module tb_cdc_events;
  import KL_mbx_pkg::*;
  localparam int S = MBX_N_PUB_SOURCES_C, K = MBX_N_PUB_SINKS_C;
  logic sys_clk = 0, dp_clk = 0, sys_rst_n = 0, dp_rst_n = 0;
  always #5  sys_clk = ~sys_clk;   // the mailbox at 100 MHz
  always #10 dp_clk  = ~dp_clk;    // the datapath at 50 MHz

  logic        d_ctr_chg_valid = 0, d_avb = 0, d_asp = 0, d_amap = 0, d_link = 0, d_gm_p = 0;
  logic [15:0] d_ctr_type = 0, d_ctr_index = 0;
  logic [63:0] d_gm_id = 0;
  logic [7:0]  d_dom = 0;
  wire         m_ctr_p, m_avb_p, m_asp_p, m_amap_p, m_link, m_gm_p;
  wire [15:0]  m_ctr_type, m_ctr_index;
  wire [63:0]  m_gm_id;
  wire [7:0]   m_dom;

  KL_mbx_cdc dut (
    .sys_clk_i(sys_clk), .sys_rst_n(sys_rst_n), .dp_clk_i(dp_clk), .dp_rst_n(dp_rst_n),
    .m_pub_da_gate_i('0), .m_pub_licence_i('0), .m_pub_talker_decl_i('0), .m_pub_src_sid_i('0),
    .m_pub_idle_slope_i('0), .m_pub_dom_vid_i('0), .m_pub_dom_prio_i('0), .m_pub_dom_adopted_i(1'b0),
    .m_pub_bound_i('0), .m_pub_sid_valid_i('0), .m_pub_started_i('0), .m_pub_sid_i('0),
    .m_fw_send_i(1'b0), .m_fw_ack_p_o(), .m_fw_cur_config_i('0), .m_fw_identify_i('0),
    .m_fw_clk_src_index_i('0), .m_fw_lock_held_i(1'b0), .m_fw_dyn_dirty_i(1'b0), .m_fw_pt_offset_i('0),
    .m_fw_pt_offset_v_i('0), .m_fw_fmt_out_i('0), .m_fw_fmt_out_v_i('0), .m_fw_fmt_in_i('0),
    .m_fw_fmt_in_v_i('0), .m_fw_restore_i('0), .m_fw_rs_cause_i('0), .m_fw_restore_cause_i('0),
    .m_fw_nvm_i('0), .m_fw_nvm_verdict_i('0),
    .m_ctr_req_i(1'b0), .m_ctr_tag_i('0), .m_ctr_type_i('0), .m_ctr_index_i('0), .m_ctr_word_i('0),
    .m_ctr_ans_p_o(), .m_ctr_ans_tag_o(), .m_ctr_ans_data_o(),
    .m_amap_req_i(1'b0), .m_amap_tag_i('0), .m_amap_type_i('0), .m_amap_index_i('0),
    .m_amap_map_index_i('0), .m_amap_sel_i('0), .m_amap_rec_i('0),
    .m_amap_ans_p_o(), .m_amap_ans_tag_o(), .m_amap_ans_data_o(),
    .m_edit_req_i(1'b0), .m_edit_tag_i('0), .m_edit_type_i('0), .m_edit_index_i('0), .m_edit_phase_i('0),
    .m_edit_remove_i(1'b0), .m_edit_rec_i('0), .m_edit_count_i('0), .m_edit_record_i('0),
    .m_edit_value_i('0), .m_edit_ans_p_o(), .m_edit_ans_tag_o(), .m_edit_ans_data_o(),
    .m_gsi_req_i(1'b0), .m_gsi_tag_i('0), .m_gsi_type_i('0), .m_gsi_index_i('0), .m_gsi_kind_i('0),
    .m_gsi_sel_i('0), .m_gsi_ord_i('0), .m_gsi_prop_i('0), .m_gsi_ans_p_o(), .m_gsi_ans_tag_o(),
    .m_gsi_ans_data_o(),
    .m_ctr_chg_p_o(m_ctr_p), .m_ctr_chg_type_o(m_ctr_type), .m_ctr_chg_index_o(m_ctr_index),
    .m_avb_chg_p_o(m_avb_p), .m_asp_chg_p_o(m_asp_p), .m_amap_wr_p_o(m_amap_p), .m_link_up_o(m_link),
    .m_gm_change_p_o(m_gm_p), .m_gm_id_o(m_gm_id), .m_gptp_domain_o(m_dom),
    .d_pub_da_gate_o(), .d_pub_licence_o(), .d_pub_talker_decl_o(), .d_pub_src_sid_o(),
    .d_pub_idle_slope_o(), .d_pub_dom_vid_o(), .d_pub_dom_prio_o(), .d_pub_dom_adopted_o(),
    .d_pub_bound_o(), .d_pub_sid_valid_o(), .d_pub_started_o(), .d_pub_sid_o(),
    .d_cur_config_o(), .d_identify_o(), .d_clk_src_index_o(), .d_lock_held_o(), .d_dyn_dirty_o(),
    .d_pt_offset_o(), .d_pt_offset_v_o(), .d_fmt_out_o(), .d_fmt_out_v_o(), .d_fmt_in_o(), .d_fmt_in_v_o(),
    .d_restore_o(), .d_rs_cause_o(), .d_restore_cause_o(), .d_nvm_o(), .d_nvm_verdict_o(),
    .d_ctr_req_o(), .d_ctr_type_o(), .d_ctr_index_o(), .d_ctr_word_o(), .d_ctr_data_i('0), .d_ctr_wait_i(1'b0),
    .d_amap_req_o(), .d_amap_type_o(), .d_amap_index_o(), .d_amap_map_index_o(), .d_amap_sel_o(),
    .d_amap_rec_o(), .d_amap_data_i('0), .d_amap_wait_i(1'b0),
    .d_edit_req_o(), .d_edit_phase_o(), .d_edit_remove_o(), .d_edit_type_o(), .d_edit_index_o(),
    .d_edit_count_o(), .d_edit_rec_o(), .d_edit_record_o(), .d_edit_value_o(), .d_edit_data_i('0),
    .d_edit_wait_i(1'b0),
    .d_gsi_req_o(), .d_gsi_kind_o(), .d_gsi_type_o(), .d_gsi_index_o(), .d_gsi_sel_o(), .d_gsi_ord_o(),
    .d_gsi_prop_o(), .d_gsi_data_i('0), .d_gsi_wait_i(1'b0),
    .d_ctr_chg_valid_i(d_ctr_chg_valid), .d_ctr_chg_type_i(d_ctr_type), .d_ctr_chg_index_i(d_ctr_index),
    .d_avb_chg_p_i(d_avb), .d_asp_chg_p_i(d_asp), .d_amap_wr_p_i(d_amap), .d_link_up_i(d_link),
    .d_gm_change_p_i(d_gm_p), .d_gm_id_i(d_gm_id), .d_gptp_domain_i(d_dom));

  // the mailbox side's record of every pulse
  int n_ctr = 0, n_avb = 0, n_asp = 0, n_amap = 0, n_gm = 0;
  logic [15:0] seen_type [$];
  logic [15:0] seen_index [$];
  logic [63:0] gm_id_at_pulse = 0;
  logic [7:0]  dom_at_pulse = 0;
  always @(posedge sys_clk) if (sys_rst_n) begin
    if (m_ctr_p) begin n_ctr++; seen_type.push_back(m_ctr_type); seen_index.push_back(m_ctr_index); end
    if (m_avb_p) n_avb++;
    if (m_asp_p) n_asp++;
    if (m_amap_p) n_amap++;
    if (m_gm_p) begin n_gm++; gm_id_at_pulse = m_gm_id; dom_at_pulse = m_dom; end
  end

  int checks = 0, fails = 0;
  task automatic check(input string what, input bit ok);
    checks++;
    if (!ok) fails++;
    $display("%s %s", ok ? "PASS" : "FAIL", what);
  endtask
  task automatic dp_pulse_ctr(input logic [15:0] t, input logic [15:0] i);
    @(posedge dp_clk); d_ctr_chg_valid <= 1; d_ctr_type <= t; d_ctr_index <= i;
    @(posedge dp_clk); d_ctr_chg_valid <= 0;
  endtask
  task automatic settle(); repeat (200) @(posedge sys_clk); endtask
  task automatic clear(); n_ctr = 0; n_avb = 0; n_asp = 0; n_amap = 0; n_gm = 0;
    seen_type.delete(); seen_index.delete(); endtask

  initial begin
    repeat (5) @(posedge sys_clk); sys_rst_n = 1;
    repeat (5) @(posedge dp_clk);  dp_rst_n = 1;
    settle();
    check("no event posts after reset", n_ctr == 0 && n_avb == 0 && n_asp == 0 && n_amap == 0 && n_gm == 0);

    // 1. one counter change of STREAM_INPUT 1 posts once, with its descriptor
    clear(); dp_pulse_ctr(16'(MBX_CTRCHG_STREAM_INPUT_TYPE_C), 16'd1); settle();
    check("STREAM_INPUT 1 posts one pulse", n_ctr == 1);
    check("...with type STREAM_INPUT and index 1",
          n_ctr == 1 && seen_type[0] == 16'(MBX_CTRCHG_STREAM_INPUT_TYPE_C) && seen_index[0] == 16'd1);

    // 2. STREAM_OUTPUT 15, the AVB_INTERFACE and the CLOCK_DOMAIN on three consecutive dp cycles
    clear();
    @(posedge dp_clk); d_ctr_chg_valid <= 1; d_ctr_type <= 16'(MBX_CTRCHG_STREAM_OUTPUT_TYPE_C); d_ctr_index <= 16'd15;
    @(posedge dp_clk); d_ctr_type <= 16'(MBX_CTRCHG_AVB_INTERFACE_TYPE_C); d_ctr_index <= 16'd0;
    @(posedge dp_clk); d_ctr_type <= 16'(MBX_CTRCHG_CLOCK_DOMAIN_TYPE_C); d_ctr_index <= 16'd0;
    @(posedge dp_clk); d_ctr_chg_valid <= 0;
    settle();
    check("three consecutive descriptors post three pulses", n_ctr == 3);
    begin
      bit so = 0, avb = 0, ckd = 0;
      foreach (seen_type[k]) begin
        so  |= (seen_type[k] == 16'(MBX_CTRCHG_STREAM_OUTPUT_TYPE_C)) && (seen_index[k] == 16'd15);
        avb |= (seen_type[k] == 16'(MBX_CTRCHG_AVB_INTERFACE_TYPE_C)) && (seen_index[k] == 16'd0);
        ckd |= (seen_type[k] == 16'(MBX_CTRCHG_CLOCK_DOMAIN_TYPE_C)) && (seen_index[k] == 16'd0);
      end
      check("...each with its own descriptor", so && avb && ckd);
    end

    // 3. a descriptor out of the contract's table (STREAM_INPUT 16) posts the ALL record
    clear(); dp_pulse_ctr(16'(MBX_CTRCHG_STREAM_INPUT_TYPE_C), 16'd16); settle();
    check("an index past the table posts one ALL record (type 0xFFFF)", n_ctr == 1 && seen_type[0] == 16'hFFFF);

    // 4. one change held over two cycles of the same descriptor posts at most twice, at least once
    clear();
    @(posedge dp_clk); d_ctr_chg_valid <= 1; d_ctr_type <= 16'(MBX_CTRCHG_STREAM_INPUT_TYPE_C); d_ctr_index <= 16'd2;
    @(posedge dp_clk); @(posedge dp_clk); d_ctr_chg_valid <= 0; settle();
    check("a repeated descriptor posts at least once and at most twice", n_ctr >= 1 && n_ctr <= 2);

    // 5. the three face events, each once
    clear();
    @(posedge dp_clk); d_avb <= 1; @(posedge dp_clk); d_avb <= 0;
    @(posedge dp_clk); d_asp <= 1; @(posedge dp_clk); d_asp <= 0;
    @(posedge dp_clk); d_amap <= 1; @(posedge dp_clk); d_amap <= 0;
    settle();
    check("AVB_INFO_CHANGED posts once", n_avb == 1);
    check("AS_PATH_CHANGED posts once", n_asp == 1);
    check("AMAP_LIVE_WRITE posts once", n_amap == 1);

    // 6. a grandmaster change: the pulse reports the identity and the domain it came with
    clear();
    @(posedge dp_clk); d_gm_id <= 64'h0011_2233_4455_6677; d_dom <= 8'd3; d_gm_p <= 1;
    @(posedge dp_clk); d_gm_p <= 0;
    settle();
    check("a GM change posts one pulse", n_gm == 1);
    check("...with the new identity held", gm_id_at_pulse == 64'h0011_2233_4455_6677);
    check("...and its domain", dom_at_pulse == 8'd3);

    // 7. two GM changes far apart, each posted, the second identity reported
    clear();
    @(posedge dp_clk); d_gm_id <= 64'hAAAA_0000_0000_0001; d_gm_p <= 1; @(posedge dp_clk); d_gm_p <= 0;
    settle();
    @(posedge dp_clk); d_gm_id <= 64'hBBBB_0000_0000_0002; d_gm_p <= 1; @(posedge dp_clk); d_gm_p <= 0;
    settle();
    check("two separate GM changes post two pulses", n_gm == 2);
    check("...the last with the last identity", gm_id_at_pulse == 64'hBBBB_0000_0000_0002);

    // 8. LINK follows the level both ways
    d_link <= 1; settle(); check("LINK up crosses", m_link == 1);
    d_link <= 0; settle(); check("LINK down crosses", m_link == 0);

    // 9. a burst: a different STREAM_INPUT every dp cycle for 16 cycles, none lost
    clear();
    for (int k = 0; k < 16; k++) begin
      @(posedge dp_clk); d_ctr_chg_valid <= 1; d_ctr_type <= 16'(MBX_CTRCHG_STREAM_INPUT_TYPE_C); d_ctr_index <= 16'(k);
    end
    @(posedge dp_clk); d_ctr_chg_valid <= 0; settle();
    begin
      bit [15:0] got = '0;
      foreach (seen_type[k]) if (seen_type[k] == 16'(MBX_CTRCHG_STREAM_INPUT_TYPE_C)) got[seen_index[k][3:0]] = 1;
      check("a 16-descriptor burst loses none", got == 16'hFFFF);
      check("...and posts each once", n_ctr == 16);
    end

    $display("checks: %0d   failures: %0d", checks, fails);
    $finish;
  end
endmodule
`default_nettype wire
