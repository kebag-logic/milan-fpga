/*
 * SPDX-FileCopyrightText: 2025 Cemal Dogan <cemal.dogan@kebag-logic.com>
 *
 * SPDX-License-Identifier: CERN-OHL-W-2.0
 */

module tb_top();

  `include "avtp_packet_gen_pkg.svh"
  `include "axi_stream_driver.svh"

  avtp_control_subtype avtp_control_pkt;
  avtp_stream_subtype avtp_stream_pkt;
  avtp_alter_subtype avtp_alter_pkt;
  avtp_random_subtype avtp_random_pkt;

  avtp_common_hdr_t avtp_common_hdr;
  logic [7:0] pkt[$];

  parameter TDATA_WIDTH_P = 64;
  parameter TDEST_WIDTH_P = 2;
  parameter TUSER_WIDTH_P = 8;
  parameter T = 10;
  parameter PIPELINE_DELAY = 1;
  bit clk;
  bit rst_n;

  // DUT counters
  int number_of_supported_control = 0;
  int number_of_supported_stream = 0;
  int number_of_supported_alter = 0;
  int number_of_not_supported = 0;

  axi_stream_if #(.TDATA_WIDTH_P(TDATA_WIDTH_P), .TDEST_WIDTH_P(TDEST_WIDTH_P), .TUSER_WIDTH_P(TUSER_WIDTH_P))
                  m_axis_top(clk, rst_n);
  axi_stream_if #(.TDATA_WIDTH_P(TDATA_WIDTH_P)) s_axis_top(clk, rst_n);

  axi_stream_driver #(.CLK_PERIOD_P(T), .TDATA_WIDTH_P(TDATA_WIDTH_P)) axis_driver;

  KL_avtp_common_parser
  #(
    .PIPELINE_DELAY(PIPELINE_DELAY),
    .TDATA_WIDTH(TDATA_WIDTH_P)
  ) DUT (
    .clk_i(clk),
    .rst_n(rst_n),
    .s_axis(s_axis_top),
    .m_axis(m_axis_top)
  );

  always #(T/2) clk = ~clk;

  task reset_dut;
    #100;
    $display("[INFO][TOP] : Reseting the DUT");
    rst_n = 1'd1;
  endtask

  task drive_random_pkt;
    avtp_common_hdr = avtp_random_pkt.subtype_header_gen();
    avtp_random_pkt.avtp_packet_gen(pkt);
    // For now fill the rest with random data
    for (int i = 0; i < 18; i++) begin
      pkt.push_back($urandom_range(0,255));
    end
    #150ns;
    axis_driver.drive_axi_stream(pkt);
  endtask

  task report_summary;
    $display("[INFO][TOP] : Reporting Summary from the AVTP Random Generator Class");
    $display("---------------------------------------------------------------------");
    $display("[INFO][TOP] : Total # of AVTP Packet Generated is %d", avtp_random_pkt.total_count);
    $display("[INFO][TOP] : # of Control Packet Generated %d", avtp_random_pkt.control_count);
    $display("[INFO][TOP] : # of Stream Packet Generated %d", avtp_random_pkt.stream_count);
    $display("[INFO][TOP] : # of Alternative Packet Generated %d", avtp_random_pkt.alter_count);
    $display("[INFO][TOP] : # of Non-AVTP Packet Generated %d", (avtp_random_pkt.total_count - (avtp_random_pkt.control_count + avtp_random_pkt.stream_count + avtp_random_pkt.alter_count)));
    $display("");
    $display("[INFO][TOP] : Reporting Summary from the DUT");
    $display("---------------------------------------------------------------------");
    $display("[INFO][TOP] : # of Control Packet Parsed %d ",number_of_supported_control);
    $display("[INFO][TOP] : # of Stream Packet Parsed %d ", number_of_supported_stream);
    $display("[INFO][TOP] : # of Alternative Packet Parsed %d ", number_of_supported_alter);
    $display("[INFO][TOP] : # of Total Not supported Packet Parsed %d ", number_of_not_supported);
  endtask

  task check_total_parse_pkt;
    if (avtp_random_pkt.total_count == (number_of_not_supported + number_of_supported_control + number_of_supported_stream + number_of_supported_alter))
      $display("[INFO][TOP] : All Generated Pkts Parsed Correctly. ");
    else 
      $fatal(1, "[FATAL][TOP] : # number of total generated pkts is not equal to # of total parsed");
  endtask


  initial begin
    m_axis_top.tready = 1;
    axis_driver = new();
    avtp_random_pkt = new();
    axis_driver.axis_if = s_axis_top; // Bind the interfaces
    $display("[INFO][TOP] : ---------------------TEST CASE-I-------------------------------");
    $display("[INFO][TOP] : Randomly Generating the AVTP Packets");
    reset_dut();
    for (int i = 0; i < 300; i++) begin
      drive_random_pkt();
    end
    report_summary();
    #100ns;
    check_total_parse_pkt();
    $finish;
  end

  // Check whether the received packet control|stream|alter|not supported
  always @(posedge clk) begin
    // Check the tdest w.r.t to tkeep since we do not drive the tvalid and tlast
    // if the packet is not supported
    if (m_axis_top.tkeep == 'hF8) begin
        if (m_axis_top.tdest == 'h0) number_of_supported_control++;
        if (m_axis_top.tdest == 'h1) number_of_supported_stream++;
        if (m_axis_top.tdest == 'h2) number_of_supported_alter++;
        if (m_axis_top.tdest == 'h3) number_of_not_supported++;
    end
  end
endmodule