// SPDX-FileCopyrightText: 2026 Kebag Logic
// SPDX-License-Identifier: CERN-OHL-W-2.0
// Whole-frame capture mapper into the real AAF serializer, both storage widths.
`timescale 1ns/1ps
module storage_tb #(
  parameter int WIDTH_P = 32
);
  logic clk = 0;
  always #5 clk = !clk;
  logic rst_n = 0, map_write = 0, source_valid = 0, tick = 0;
  logic [2:0] map_address = 0;
  logic [12:0] map_data = 0;
  logic [3:0] source_slot = 0;
  logic [WIDTH_P-1:0] source_l = 0, source_r = 0;
  wire pair_valid;
  wire [4:0] pair_slot;
  wire [WIDTH_P-1:0] pair_l, pair_r;
  wire [63:0] data;
  wire [7:0] keep;
  wire valid, last;
  logic ready = 0;
  int cycles = 0, frame_bytes = 0, packets = 0, samples = 0, mapped = 0;
  logic [31:0] assembled = 0;
  function automatic logic [31:0] pattern(input int frame, input int channel);
    return (32'(frame)*32'h01020305) ^ (32'h89abcdef+32'(channel)*32'h31415927);
  endfunction
  function automatic logic [31:0] expected(input int frame, input int channel);
    return WIDTH_P == 32 ? pattern(frame, channel) : pattern(frame, channel) & 32'hffffff00;
  endfunction
  KL_chan_map_capture #(.SAMPLE_BITS_P(WIDTH_P), .N_SLOTS_P(4), .N_TDM_P(8),
      .N_LB_STREAMS_P(1), .N_LB_CH_P(8)) mapper (
    .clk_i(clk), .rst_n(rst_n), .map_wr_en_i(map_write), .map_wr_addr_i(map_address),
    .map_wr_data_i(map_data), .map_rd_en_i(1'b0), .map_rd_addr_i(3'd0),
    .map_rd_data_o(), .map_rd_valid_o(), .map_flat_o(),
    .i2s_pair_valid_i(1'b0), .i2s_l_i(24'd0), .i2s_r_i(24'd0),
    .tdm_pair_valid_i(source_valid), .tdm_pair_slot_i(source_slot),
    .tdm_l_i(source_l), .tdm_r_i(source_r), .tdm_close_ns_i(32'd0),
    .tone_smp_i(24'd0), .tick_i(tick), .pair_valid_o(pair_valid),
    .pair_slot_o(pair_slot), .pair_l_o(pair_l), .pair_r_o(pair_r),
    .lb_dup_cnt_o(), .lb_skip_cnt_o(), .tdm_dup_cnt_o(), .tdm_skip_cnt_o(),
    .tdm_walk_ns_o()
  );
  KL_aaf_packetizer #(.SAMPLE_BITS_P(WIDTH_P), .N_TALKERS_P(1), .WIRE_CHANS_P(8)) packetizer (
    .clk_i(clk), .rst_n(rst_n), .pair_valid_i(pair_valid), .pair_slot_i(pair_slot),
    .pair_l_i(pair_l), .pair_r_i(pair_r), .stream_en_i(1'b1),
    .dest_mac_i(48'h91e0f0000001), .station_mac_i(48'h001122334455),
    .vlan_vid_i(12'd2), .vlan_pcp_i(3'd3), .dom_ovr_i(1'b0), .stream_id_i(64'd0),
    .transit_ns_i(32'd2000000), .ptp_ns_i(64'd1000000000), .ts_uncertain_i(1'b0), .mr_i(1'b0),
    .tctx_wr_en_i(1'b0), .tctx_wr_addr_i(7'd0), .tctx_wr_data_i(32'd0), .tctx_wr_rdy_o(),
    .tctx_rd_en_i(1'b0), .tctx_rd_addr_i(7'd0), .tctx_rd_data_o(), .tctx_rd_valid_o(),
    .m_axis_tdata(data), .m_axis_tkeep(keep), .m_axis_tvalid(valid), .m_axis_tlast(last),
    .m_axis_tready(ready), .frames_sent_o(), .frame_p_o(), .frame_idx_o(),
    .frame_tu_o(), .frame_mr_o()
  );
  always @(negedge clk) begin
    cycles = cycles+1;
    ready = cycles%7 != 0 && cycles%13 != 0;
  end
  always @(posedge clk) if (rst_n) begin
    if (pair_valid) begin
      if (pair_slot != 5'(mapped%4)
          || pair_l != WIDTH_P'(pattern(mapped/4, (mapped%4)*2) >> (32-WIDTH_P))
          || pair_r != WIDTH_P'(pattern(mapped/4, (mapped%4)*2+1) >> (32-WIDTH_P)))
        $fatal(1, "CHECK CAPTURE_STORAGE_ALL_BITS");
      mapped = mapped+1;
    end
    if (valid && ready) begin
      for (int b = 0; b < 8; b++) if (keep[b]) begin
        if (frame_bytes >= 42) begin
          assembled = (assembled << 8) | 32'(data[b*8 +: 8]);
          if ((frame_bytes-42)%4 == 3) begin
            if (assembled != expected(samples/8, samples%8))
              $fatal(1, "CHECK AAF_STORAGE_ALL_BITS sample=%0d got=%08x expected=%08x",
                     samples, assembled, expected(samples/8, samples%8));
            samples = samples+1;
          end
        end
        frame_bytes = frame_bytes+1;
      end
      if (last) begin
        if (frame_bytes != 234) $fatal(1, "CHECK AAF_EIGHT_CHANNEL_LENGTH");
        frame_bytes = 0;
        packets = packets+1;
      end
    end
  end
  task automatic step(input int n);
    repeat (n) @(negedge clk);
  endtask
  initial begin
    step(10); rst_n = 1; step(20);
    for (int ch = 0; ch < 8; ch++) begin
      map_write = 1; map_address = 3'(ch); map_data = 13'h1200 | 13'((ch%2)<<11) | 13'(ch/2);
      step(1);
    end
    map_write = 0; step(20);
    for (int frame = 0; frame < 6000; frame++) begin
      for (int p = 0; p < 4; p++) begin
        source_valid = 1; source_slot = 4'(p);
        source_l = WIDTH_P'(pattern(frame,p*2) >> (32-WIDTH_P));
        source_r = WIDTH_P'(pattern(frame,p*2+1) >> (32-WIDTH_P));
        step(1);
      end
      source_valid = 0; step(2); tick = 1; step(1); tick = 0; step(1035);
    end
    step(2000);
    if (packets != 1000 || samples != 48000 || mapped != 24000)
      $fatal(1, "CHECK CAPTURE_STORAGE_COUNTS packets=%0d samples=%0d mapped=%0d", packets,samples,mapped);
    $display("PASS capture storage %0d: 6000 frames, 1000 AAF packets, every channel and subslot bit", WIDTH_P);
    $finish;
  end
endmodule
