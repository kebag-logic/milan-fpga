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

  parameter TDATA_WIDTH_P = 128;
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
  int error_supported_control = 0;
  int error_supported_stream = 0;
  int error_supported_alter = 0;
  int error_not_supported = 0;

  int sent_supported_control = 0;
  int sent_supported_stream = 0;
  int sent_supported_alter = 0;
  int sent_not_supported = 0;

  localparam int NUM_TESTED_M_AXIS = 4;
  localparam int TESTED_PORT_VALUES[NUM_TESTED_M_AXIS] = '{0, 1, 2, 3}; 

  axi_stream_if #(.TDATA_WIDTH_P(TDATA_WIDTH_P), .TDEST_WIDTH_P(TDEST_WIDTH_P),.TUSER_WIDTH_P(TUSER_WIDTH_P)) m_axis_top [NUM_TESTED_M_AXIS-1:0] (clk, rst_n);
  
  axi_stream_if #(.TDATA_WIDTH_P(TDATA_WIDTH_P), .TDEST_WIDTH_P(TDEST_WIDTH_P),.TUSER_WIDTH_P(TUSER_WIDTH_P)) s_axis_top(clk, rst_n);

  axi_stream_driver #(.CLK_PERIOD_P(T), .TDATA_WIDTH_P(TDATA_WIDTH_P), .TDEST_WIDTH_P(TDEST_WIDTH_P),.TUSER_WIDTH_P(TUSER_WIDTH_P)) axis_driver;

  KL_avtp_packet_switch
  #(
    .IN_REG(1),
    .OUT_REG(1),
    .NUM_M_AXIS_IF(NUM_TESTED_M_AXIS),
    .PORT_VALUES(TESTED_PORT_VALUES),
    .FIFO_DEPTH(128)
  ) DUT (
    .clk_i(clk),
    .resetn_i(rst_n),
    .s_axis(s_axis_top),
    .m_axis({m_axis_top[0],m_axis_top[1],m_axis_top[2],m_axis_top[3]})
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
    $display("[INFO][TOP] : Total # of AVTP Packet Generated is              %d", avtp_random_pkt.total_count);
    //$display("[INFO][TOP] : # of Control Packet Generated %d", avtp_random_pkt.control_count);
    //$display("[INFO][TOP] : # of Stream Packet Generated %d", avtp_random_pkt.stream_count);
    //$display("[INFO][TOP] : # of Alternative Packet Generated %d", avtp_random_pkt.alter_count);
    //$display("[INFO][TOP] : # of Non-AVTP Packet Generated %d", (avtp_random_pkt.total_count - (avtp_random_pkt.control_count + avtp_random_pkt.stream_count + avtp_random_pkt.alter_count)));
    $display("");
    $display("[INFO][TOP] : # of Control Packet Generated                    %d", sent_supported_control);
    $display("[INFO][TOP] : # of Stream Packet Generated                     %d", sent_supported_stream);
    $display("[INFO][TOP] : # of Alternative Packet Generated                %d", sent_supported_alter);
    $display("[INFO][TOP] : # of Non-AVTP Packet Generated                   %d", sent_not_supported);
    $display("");
    $display("[INFO][TOP] : Reporting Summary from the DUT");
    $display("---------------------------------------------------------------------");
    $display("[INFO][TOP] : # of Control Packet Parsed                       %d ", number_of_supported_control);
    $display("[INFO][TOP] : # of Stream Packet Parsed                        %d ", number_of_supported_stream);
    $display("[INFO][TOP] : # of Alternative Packet Parsed                   %d ", number_of_supported_alter);
    $display("[INFO][TOP] : # of Total Not supported Packet Parsed           %d ", number_of_not_supported);
    $display("[INFO][TOP] : # of Errors on Control Packet Parsed             %d ", error_supported_control);
    $display("[INFO][TOP] : # of Errors on Stream Packet Parsed              %d ", error_supported_stream);
    $display("[INFO][TOP] : # of Errors on Alternative Packet Parsed         %d ", error_supported_alter);
    $display("[INFO][TOP] : # of Errors on Total Not supported Packet Parsed %d ", error_not_supported);
  endtask

  task check_total_parse_pkt;
    if (avtp_random_pkt.total_count == (number_of_not_supported + number_of_supported_control + number_of_supported_stream + number_of_supported_alter))
      $display("[INFO][TOP] : All Generated Pkts Parsed Correctly. ");
    else 
      $fatal(1, "[FATAL][TOP] : # number of total generated pkts is not equal to # of total parsed");
  endtask


  initial begin
    m_axis_top[0].tready = 1'b1;
    m_axis_top[1].tready = 1'b1;
    m_axis_top[2].tready = 1'b1;
    m_axis_top[3].tready = 1'b1;

    axis_driver = new();
    avtp_random_pkt = new();
    axis_driver.axis_if = s_axis_top; // Bind the interfaces
    $display("[INFO][TOP] : ---------------------TEST CASE-I-------------------------------");
    $display("[INFO][TOP] : Randomly Generating the AVTP Packets");
    reset_dut();
    for (int i = 0; i < 10000; i++) begin
      //s_axis_top.tdest = $urandom_range(1,3);
      drive_random_pkt();
    end
    #100ns;
    report_summary();
    #100ns;
    check_total_parse_pkt();
    $finish;
  end
  
  always@(posedge clk)
  begin
    m_axis_top[0].tready <= $urandom_range(0,1);
    m_axis_top[1].tready <= $urandom_range(0,1);
    m_axis_top[2].tready <= $urandom_range(0,1);
    m_axis_top[3].tready <= $urandom_range(0,1);
  end

  logic r_parser_state,parser_state;
  localparam IDLE_S = 0;
  localparam WAIT_S = 1;

  always_comb begin : subtype_save_logic
      parser_state <= r_parser_state;
      case (r_parser_state)
        IDLE_S : begin
          if (s_axis_top.tvalid) begin
            s_axis_top.tuser <= s_axis_top.tdata[47:40];
            parser_state     <= WAIT_S;
          end
        end

        WAIT_S : begin
          if (s_axis_top.tready & s_axis_top.tvalid & s_axis_top.tlast) parser_state <= IDLE_S;
        end

        default : begin
          parser_state <= IDLE_S;
        end
      endcase
  end : subtype_save_logic

  always@(posedge clk)
  begin
      if(~rst_n)
      begin
         r_parser_state <= IDLE_S;
      end
      else
      begin
         r_parser_state <= parser_state;
      end
  end

  always_comb begin : tdest_assign
   case (s_axis_top.tuser)
      ADP, AECP, ACMP, MAAP: s_axis_top.tdest = 'h0;
      IIDC, MMA_STREAM, AAF: s_axis_top.tdest = 'h1;
      CRF : s_axis_top.tdest                  = 'h2;
      default : s_axis_top.tdest              = 'h3;
    endcase
  end : tdest_assign

  // Check whether the received packet control|stream|alter|not supported
  logic packet_valid[NUM_TESTED_M_AXIS-1:0];
  generate 
    for(genvar i = 0; i < NUM_TESTED_M_AXIS; i++) begin
      assign packet_valid[i] =  m_axis_top[i].tlast && m_axis_top[i].tvalid && m_axis_top[i].tready;
    end
  endgenerate
  // Checking for valid packet on master axi stream interface of dut or else
  // count errors
  always @(posedge clk) begin
    // Check the tdest w.r.t to tkeep since we do not drive the tvalid and tlast
    // if the packet is not supported
    if (packet_valid[0] && m_axis_top[0].tdest == 0) number_of_supported_control++;
    else if (packet_valid[0]) error_supported_control++;
    if (packet_valid[1] && m_axis_top[1].tdest == 1) number_of_supported_stream++;
    else if (packet_valid[1]) error_supported_stream++;
    if (packet_valid[2] && m_axis_top[2].tdest == 2) number_of_supported_alter++;
    else if (packet_valid[2]) error_supported_alter++;
    if (packet_valid[3] && m_axis_top[3].tdest == 3) number_of_not_supported++;
    else if (packet_valid[3]) error_not_supported++;
  end
  
  logic send_packet_valid;
  assign send_packet_valid =  s_axis_top.tlast && s_axis_top.tvalid && s_axis_top.tready;

  always @(posedge clk) begin
    // Check the tdest w.r.t to tkeep since we do not drive the tvalid and tlast
    // if the packet is not supported
    if(send_packet_valid) begin
      if (s_axis_top.tdest == 0) sent_supported_control++;
      if (s_axis_top.tdest == 1) sent_supported_stream++;
      if (s_axis_top.tdest == 2) sent_supported_alter++;
      if (s_axis_top.tdest == 3) sent_not_supported++;
    end
  end

endmodule
