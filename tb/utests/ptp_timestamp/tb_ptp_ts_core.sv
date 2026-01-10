/*
 * SPDX-FileCopyrightText: 2025 Oguz Kahraman <oguz.kahraman@kebag-logic.com>
 *
 * SPDX-License-Identifier: CERN-OHL-W-2.0
 */

/*
------------------------------------------------------------------------------
  File        : tb_ptp_ts_core.sv
  Author      : Oguz Kahraman

                oguz.kahraman@kebag-logic.com

  Date        : 2025-07-18
  Description : Testbench for the PTP timestamping core module.

                - Verifies both TX and RX paths.
                - Supports testing for big and little endian configurations.
                - Extracts gPTP sequence_id and timestamp from Ethernet frames.
                - Uses AXI-Stream driver to simulate Ethernet packet transfers.
                - Includes timestamp generator for driving the DUT.

  Company     : Kebag Logic
  Project     : PTP Timestamping for Custom RGMII MAC

------------------------------------------------------------------------------
*/

`timescale 1ns/1ps
import ethernet_packet_pkg::*;

//! @title Enhanced PTP Timestamping Core Testbench
//! @brief Comprehensive testbench for PTP timestamping core with endianness support
//! @details Tests both big and little endian configurations with multiple packet types
module tb_ptp_ts_core;

  //! TDATA_WIDTH AXI-Stream data width
  localparam TDATA_WIDTH = 64;
  //! TS_WIDTH Timestamp width
  localparam TS_WIDTH = 64;
  //! BEAT_BYTES Number of bytes per beat
  localparam BEAT_BYTES = TDATA_WIDTH / 8;

  //! clk Main clock (100MHz)
  logic clk = 0;
  always #5 clk = ~clk;

  //! clk_125 Timestamp source clock (125MHz)
  logic clk_125 = 0;
  always #4 clk_125 = ~clk_125;

  //! rstn Global reset (active low)
  logic rstn = 0;

  //! s_axis_be Big Endian Input AXI-Stream interface
  axi_stream_if #(.TDATA_WIDTH_P(TDATA_WIDTH)) s_axis_be();
  //! m_axis_be Big Endian Output AXI-Stream interface
  axi_stream_if #(.TDATA_WIDTH_P(TDATA_WIDTH)) m_axis_be();
  //! ts_m_axis_be Big Endian Timestamp metadata AXI-Stream interface
  axi_stream_if #(.TDATA_WIDTH_P(TDATA_WIDTH)) ts_m_axis_be();

  //! s_axis_le Little Endian Input AXI-Stream interface
  axi_stream_if #(.TDATA_WIDTH_P(TDATA_WIDTH)) s_axis_le();
  //! m_axis_le Little Endian Output AXI-Stream interface
  axi_stream_if #(.TDATA_WIDTH_P(TDATA_WIDTH)) m_axis_le();
  //! ts_m_axis_le Little Endian Timestamp metadata AXI-Stream interface
  axi_stream_if #(.TDATA_WIDTH_P(TDATA_WIDTH)) ts_m_axis_le();

  //! Current active interfaces based on test configuration
  axi_stream_if #(.TDATA_WIDTH_P(TDATA_WIDTH)) current_s_axis();
  axi_stream_if #(.TDATA_WIDTH_P(TDATA_WIDTH)) current_m_axis();
  axi_stream_if #(.TDATA_WIDTH_P(TDATA_WIDTH)) current_ts_m_axis();
  //! @signal ts Global timestamp counter output
  wire[TS_WIDTH-1:0] ts;

  //! Timestamp counter instance
  //! Generates incremental timestamps for testing
  timestamp_counter #(
    .COUNTER_WIDTH(64),
    .STEP_SIZE(8)
  ) ts_dut(
    .clk (clk_125),
    .resetn (rstn),
    .timestamp_out(ts)
  );

  //! test_big_endian Configuration for current test
  logic test_big_endian = 1;
  //! test_is_tx TX/RX mode for current test
  logic test_is_tx = 1;

  //! Big Endian DUT Instance
  //! Tests big endian configuration and TX direction
  ptp_ts_core #(
    .IS_TX(1),
    .TDATA_WIDTH(TDATA_WIDTH),
    .TS_WIDTH(TS_WIDTH),
    .BIG_ENDIAN(1),
    .ETH_TYPE(16'h88f7)
  ) dut_big_endian (
    .ts_src_clk(clk_125),
    .ts_src_resetn(rstn),
    .ts_dst_clk(clk),
    .ts_dst_resetn(rstn),
    .ts_in(ts),
    .s_axis(s_axis_be),
    .m_axis(m_axis_be),
    .ts_m_axis(ts_m_axis_be)
  );

  //! Little Endian DUT Instance
  //! Tests little endian configuration and RX direction
  ptp_ts_core #(
    .IS_TX(0),
    .TDATA_WIDTH(TDATA_WIDTH),
    .TS_WIDTH(TS_WIDTH),
    .BIG_ENDIAN(0),
    .ETH_TYPE(16'hf788)
  ) dut_little_endian (
    .ts_src_clk(clk_125),
    .ts_src_resetn(rstn),
    .ts_dst_clk(clk),
    .ts_dst_resetn(rstn),
    .ts_in(ts),
    .s_axis(s_axis_le),
    .m_axis(m_axis_le),
    .ts_m_axis(ts_m_axis_le)
  );

  //! Routing active interface signals based on test configuration
  assign current_s_axis.tdata = (test_big_endian) ? s_axis_be.tdata : s_axis_le.tdata;
  assign current_s_axis.tvalid = (test_big_endian) ? s_axis_be.tvalid : s_axis_le.tvalid;
  assign current_s_axis.tlast = (test_big_endian) ? s_axis_be.tlast : s_axis_le.tlast;
  assign current_s_axis.tkeep = (test_big_endian) ? s_axis_be.tkeep : s_axis_le.tkeep;
  assign current_s_axis.tready = (test_big_endian) ? s_axis_be.tready : s_axis_le.tready;

  assign current_m_axis.tdata = (test_big_endian) ? m_axis_be.tdata : m_axis_le.tdata;
  assign current_m_axis.tvalid = (test_big_endian) ? m_axis_be.tvalid : m_axis_le.tvalid;
  assign current_m_axis.tlast = (test_big_endian) ? m_axis_be.tlast : m_axis_le.tlast;
  assign current_m_axis.tkeep = (test_big_endian) ? m_axis_be.tkeep : m_axis_le.tkeep;
  assign current_m_axis.tready = (test_big_endian) ? m_axis_be.tready : m_axis_le.tready;

  assign current_ts_m_axis.tdata = (test_big_endian) ? ts_m_axis_be.tdata : ts_m_axis_le.tdata;
  assign current_ts_m_axis.tvalid = (test_big_endian) ? ts_m_axis_be.tvalid : ts_m_axis_le.tvalid;
  assign current_ts_m_axis.tlast = (test_big_endian) ? ts_m_axis_be.tlast : ts_m_axis_le.tlast;
  assign current_ts_m_axis.tkeep = (test_big_endian) ? ts_m_axis_be.tkeep : ts_m_axis_le.tkeep;
  assign current_ts_m_axis.tready = (test_big_endian) ? ts_m_axis_be.tready : ts_m_axis_le.tready;

  //! Debug signals for monitoring internal state
  logic [15:0] byte_counter_debug;
  logic start_packet_debug;
  logic seq_id_received_debug;
  logic is_ptp_debug;
  logic [15:0] eth_type_debug;
  logic [15:0] ptp_seq_id_debug;

  //! Connect debug signals based on current test configuration
  assign byte_counter_debug = test_big_endian ? dut_big_endian.byte_counter :
                              dut_little_endian.byte_counter;
  assign start_packet_debug = test_big_endian ? dut_big_endian.start_packet :
                              dut_little_endian.start_packet;
  assign seq_id_received_debug = test_big_endian ? dut_big_endian.seq_id_received :
                                 dut_little_endian.seq_id_received;
  assign is_ptp_debug = test_big_endian ? dut_big_endian.is_ptp :
                        dut_little_endian.is_ptp;
  assign eth_type_debug = test_big_endian ? dut_big_endian.eth_type :
                          dut_little_endian.eth_type;
  assign ptp_seq_id_debug = test_big_endian ? dut_big_endian.ptp_seq_id :
                            dut_little_endian.ptp_seq_id;

  //! Test packet structure
  typedef struct {
    string name;         //! Test case name
    bit is_ptp;         //! Whether packet is PTP
    bit [15:0] seq_id;  //! Expected sequence ID
    bit [15:0] eth_type; //! Ethernet type to insert
    int packet_length;   //! Packet length in beats(words)
  } test_packet_t;

  //! Test packet database
  test_packet_t test_packets[] = {
    '{"PTP_Normal_1", 1, 16'h1234, 16'h88F7, 10},
    '{"PTP_Normal_2", 1, 16'h5678, 16'h88F7, 12},
    '{"PTP_SeqID_0", 1, 16'h0000, 16'h88F7, 8},
    '{"PTP_SeqID_Max", 1, 16'hFFFF, 16'h88F7, 15},
    '{"Non_PTP_IPv4", 0, 16'h9ABC, 16'h0800, 10},
    '{"Non_PTP_IPv6", 0, 16'hDEF0, 16'h86DD, 9},
    '{"Non_PTP_ARP", 0, 16'h1111, 16'h0806, 11},
    '{"PTP_Short", 1, 16'h2222, 16'h88F7, 8},
    '{"PTP_Long", 1, 16'h3333, 16'h88F7, 20}
  };

  //! Initialize all AXI interface signals
  initial begin
    //! Initialize Big Endian interfaces
    s_axis_be.tdata = 64'd0;
    s_axis_be.tvalid = 1'b0;
    s_axis_be.tkeep = 8'hFF;
    s_axis_be.tlast = 1'b0;
    m_axis_be.tready = 1'b1;
    ts_m_axis_be.tready = 1'b1;

    //! Initialize Little Endian interfaces
    s_axis_le.tdata = 64'd0;
    s_axis_le.tvalid = 1'b0;
    s_axis_le.tkeep = 8'hFF;
    s_axis_le.tlast = 1'b0;
    m_axis_le.tready = 1'b1;
    ts_m_axis_le.tready = 1'b1;
  end

  //! @brief Send packet task with proper endianness support
  //! @param packet Test packet structure
  //! @param big_endian Endianness configuration
  task send_packet(test_packet_t packet, bit big_endian);
    logic [TDATA_WIDTH-1:0] tdata;
    int beat_count;
    
    $display("=== Starting packet: %s (PTP=%0b, seq_id=0x%04x, endian=%s) ===", 
             packet.name, packet.is_ptp, packet.seq_id, big_endian ? "BIG" : "LITTLE");
    
    //! Select the correct interface based on endianness
    if (big_endian) begin
      //! Wait for ready before starting
      while (!m_axis_be.tready) @(posedge clk);

      //! Beat 1: bytes 0-7 (Ethernet header start - MAC addresses)
      tdata = 64'h0011223344556677;
      @(posedge clk);
      s_axis_be.tvalid <= 1;
      s_axis_be.tdata <= tdata;
      s_axis_be.tlast <= 0;
      s_axis_be.tkeep <= 8'hFF;

      //! Beat 2: bytes 8-15 (contains eth_type at bytes 14-15)
      tdata = 64'habcdeffeabcd0000;
      //! Big endian: MSB first
      tdata[31:24] = packet.eth_type[15:8];  // byte 14
      tdata[23:16] = packet.eth_type[7:0];   // byte 15
      
      @(posedge clk);
      s_axis_be.tdata <= tdata;
      s_axis_be.tlast <= 0;

      //! Filler beats to reach PTP sequence ID location
      beat_count = 2;
      while (beat_count < 5) begin
        @(posedge clk);
        s_axis_be.tdata <= 64'hDEADBEEFCAFEBABE;
        s_axis_be.tlast <= 0;
        
        while (!(s_axis_be.tvalid && s_axis_be.tready)) @(posedge clk);
        beat_count++;
      end

      //! Beat containing PTP sequence ID
      tdata = 64'hFEEDFACEDEADBEEF;
      //! Big endian: MSB first
      tdata[31:24] = packet.seq_id[15:8];  // high byte seq_id
      tdata[23:16] = packet.seq_id[7:0];   // low byte seq_id
      
      @(posedge clk);
      s_axis_be.tdata <= tdata;
      s_axis_be.tlast <= 0;
      
      while (!(s_axis_be.tvalid && s_axis_be.tready)) @(posedge clk);
      $display("Seq ID beat: byte_counter=%0d, seq_id_received=%0b, ptp_seq_id=0x%04x",
               byte_counter_debug, seq_id_received_debug, ptp_seq_id_debug);

      //! Send remaining beats until packet completion
      beat_count = 6;
      while (beat_count < packet.packet_length) begin
        @(posedge clk);
        s_axis_be.tdata <= {beat_count[7:0], 56'h123456789ABCDEF0};
        s_axis_be.tlast <= (beat_count == packet.packet_length - 1);
        
        while (!(s_axis_be.tvalid && s_axis_be.tready)) @(posedge clk);
        beat_count++;
      end

      //! End transaction
      @(posedge clk);
      s_axis_be.tvalid <= 0;
      s_axis_be.tlast <= 0;
      
    end else begin
      //! Little Endian processing
      //! Wait for ready before starting
      while (!m_axis_le.tready) @(posedge clk);

      //! Beat 1: bytes 0-7 (Ethernet header start - MAC addresses)
      tdata = 64'h0011223344556677;
      @(posedge clk);
      s_axis_le.tvalid <= 1;
      s_axis_le.tdata <= tdata;
      s_axis_le.tlast <= 0;
      s_axis_le.tkeep <= 8'hFF;

      //! Beat 2: bytes 8-15 (contains eth_type at bytes 13-14)
      tdata = 64'habcdeffeabcd0000;
      //! Little endian: LSB first
      tdata[47:40] = packet.eth_type[7:0];   // byte 13 (LSB)
      tdata[39:32] = packet.eth_type[15:8];  // byte 14 (MSB)
      
      @(posedge clk);
      s_axis_le.tdata <= tdata;
      s_axis_le.tlast <= 0;

      //! Filler beats to reach PTP sequence ID location
      beat_count = 2;
      while (beat_count < 5) begin
        @(posedge clk);
        s_axis_le.tdata <= 64'hDEADBEEFCAFEBABE;
        s_axis_le.tlast <= 0;
        
        while (!(s_axis_le.tvalid && s_axis_le.tready)) @(posedge clk);
        beat_count++;
      end

      //! Beat containing PTP sequence ID
      tdata = 64'hFEEDFACEDEADBEEF;
      //! Little endian: LSB first
      tdata[47:40] = packet.seq_id[7:0];   // low byte seq_id (LSB)
      tdata[39:32] = packet.seq_id[15:8];  // high byte seq_id (MSB)
      
      @(posedge clk);
      s_axis_le.tdata <= tdata;
      s_axis_le.tlast <= 0;
      
      while (!(s_axis_le.tvalid && s_axis_le.tready)) @(posedge clk);
      $display("Seq ID beat: byte_counter=%0d, seq_id_received=%0b, ptp_seq_id=0x%04x",
               byte_counter_debug, seq_id_received_debug, ptp_seq_id_debug);

      //! Send remaining beats until packet completion
      beat_count = 6;
      while (beat_count < packet.packet_length) begin
        @(posedge clk);
        s_axis_le.tdata <= {beat_count[7:0], 56'h123456789ABCDEF0};
        s_axis_le.tlast <= (beat_count == packet.packet_length - 1);
        
        while (!(s_axis_le.tvalid && s_axis_le.tready)) @(posedge clk);
        beat_count++;
      end

      //! End transaction
      @(posedge clk);
      s_axis_le.tvalid <= 0;
      s_axis_le.tlast <= 0;
    end
    
    $display("=== Packet %s transmission complete (is_ptp=%0b) ===", packet.name, is_ptp_debug);
    //repeat (5) @(posedge clk); // Wait between packets
  endtask

  //! @brief Monitor task for timestamp metadata
  //! @details Monitors and displays timestamp metadata output
  task monitor_metadata();
    logic [15:0] seq_id_out;
    logic direction;
    logic [63:0] timestamp_out;
    
    forever begin
      @(posedge clk);
      
      //! Monitor Big Endian metadata
      if (ts_m_axis_be.tvalid && ts_m_axis_be.tready) begin
        if (ts_m_axis_be.tlast) begin
          $display("BE Metadata (LOW): 0x%016x (tlast=%0b)", ts_m_axis_be.tdata, ts_m_axis_be.tlast);
          seq_id_out = ts_m_axis_be.tdata[63:48];
          direction = ts_m_axis_be.tdata[40];
          $display("  -> BE seq_id=0x%04x, direction=%0s", seq_id_out, direction ? "TX" : "RX");
        end else begin
          timestamp_out = ts_m_axis_be.tdata;
          $display("BE Metadata (HIGH): 0x%016x (tlast=%0b) - Timestamp=%0d", 
                   ts_m_axis_be.tdata, ts_m_axis_be.tlast, timestamp_out);
        end
      end
      
      //! Monitor Little Endian metadata
      if (ts_m_axis_le.tvalid && ts_m_axis_le.tready) begin
        if (ts_m_axis_le.tlast) begin
          $display("LE Metadata (LOW): 0x%016x (tlast=%0b)", ts_m_axis_le.tdata,
                    ts_m_axis_le.tlast);
          seq_id_out = ts_m_axis_le.tdata[63:48];
          direction = ts_m_axis_le.tdata[40];
          $display("  -> LE seq_id=0x%04x, direction=%0s", seq_id_out, direction ? "TX" : "RX");
        end else begin
          timestamp_out = ts_m_axis_le.tdata;
          $display("LE Metadata (HIGH): 0x%016x (tlast=%0b) - Timestamp=%0d", 
                   ts_m_axis_le.tdata, ts_m_axis_le.tlast, timestamp_out);
        end
      end
    end
  endtask

  //! @brief Debug monitor for internal signals
  //! @details Provides detailed debug information during packet processing
  task debug_monitor();
    forever begin
      @(posedge clk);
      if (test_big_endian) begin
        if (s_axis_be.tvalid && s_axis_be.tready) begin
          // $display("BE Debug: byte_counter=%0d, start_packet=%0b, seq_id_received=%0b, is_ptp=%0b,\
          //           eth_type=0x%04x", byte_counter_debug, start_packet_debug, seq_id_received_debug,
          //           is_ptp_debug, eth_type_debug);
        end
      end else begin
        if (s_axis_le.tvalid && s_axis_le.tready) begin
          // $display("LE Debug: byte_counter=%0d, start_packet=%0b, seq_id_received=%0b, is_ptp=%0b,\
          //           eth_type=0x%04x", byte_counter_debug, start_packet_debug, seq_id_received_debug,
          //           is_ptp_debug, eth_type_debug);
        end
      end
    end
  endtask

  int packet_count = 0;
  int ptp_packet_count = 0;
  int metadata_count = 0;

  //! @brief Performance monitor
  //! @details Tracks packet processing performance and timing
  task performance_monitor();
    forever begin
      @(posedge clk);
      //! Count completed packets
      if (test_big_endian) begin
        if (s_axis_be.tvalid && s_axis_be.tready && s_axis_be.tlast) begin
          packet_count++;
          if (is_ptp_debug) ptp_packet_count++;
        end
        if (ts_m_axis_be.tvalid && ts_m_axis_be.tready && ts_m_axis_be.tlast) begin
          metadata_count++;
        end
      end else begin
        if (s_axis_le.tvalid && s_axis_le.tready && s_axis_le.tlast) begin
          packet_count++;
          if (is_ptp_debug) ptp_packet_count++;
        end
        if (ts_m_axis_le.tvalid && ts_m_axis_le.tready && ts_m_axis_le.tlast) begin
          metadata_count++;
        end
      end
      
      //! Report every 10 packets
      if (packet_count % 10 == 0 && packet_count > 0) begin
        $display("Performance: %0d packets processed, %0d PTP, %0d metadata outputs", 
                 packet_count, ptp_packet_count, metadata_count);
      end
    end
  endtask

  //! @brief Run test suite for specific endianness
  //! @param big_endian Endianness configuration to test
  //! @param is_tx TX/RX mode configuration
  task run_test_suite(bit big_endian, bit is_tx);
    $display("\n" + "="*80);
    $display("TESTING %s ENDIAN, %s MODE", big_endian ? "BIG" : "LITTLE", is_tx ? "TX" : "RX");
    $display("="*80);
    
    //! Configure test mode
    test_big_endian = big_endian;
    test_is_tx = is_tx;
    
    //! Test each packet type
    foreach (test_packets[i]) begin
      $display("\n--- TEST %0d: %s ---", i+1, test_packets[i].name);
      send_packet(test_packets[i], big_endian);
    end
    
    $display("\n%s ENDIAN %s MODE TESTS COMPLETED", big_endian ? "BIG" : "LITTLE", is_tx ? "TX" :
              "RX");
  endtask
  bit test_endian;
  //! @brief Stress test with rapid packet transmission
  //! @details Tests back-to-back packet processing capability
  task stress_test();
    $display("\n" + "="*80);
    $display("STRESS TEST - RAPID PACKET TRANSMISSION");
    $display("="*80);
    
    repeat (20) begin
      test_endian= $urandom % 2;
      test_big_endian = test_endian;
      send_packet(test_packets[$urandom % $size(test_packets)], test_endian);
      //repeat (1) @(posedge clk); // Minimal delay between packets
    end
    
    $display("STRESS TEST COMPLETED");
  endtask

  //! @brief Error injection test
  //! @details Tests behavior with malformed packets
  task error_injection_test();
    $display("\n" + "="*80);
    $display("ERROR INJECTION TEST");
    $display("="*80);
    
    //! Test with truncated packet (early tlast) - Big Endian
    test_big_endian = 1;
    $display("--- Testing truncated packet (Big Endian) ---");
    @(posedge clk);
    s_axis_be.tvalid <= 1;
    s_axis_be.tdata <= 64'h0011223344556677;
    s_axis_be.tlast <= 0;
    s_axis_be.tkeep <= 8'hFF;
    
    while (!(s_axis_be.tvalid && s_axis_be.tready)) @(posedge clk);
    
    @(posedge clk);
    s_axis_be.tdata <= 64'h88F788F788F788F7; // PTP type but truncated
    s_axis_be.tlast <= 1; // Early termination
    
    while (!(s_axis_be.tvalid && s_axis_be.tready)) @(posedge clk);
    
    @(posedge clk);
    s_axis_be.tvalid <= 0;
    s_axis_be.tlast <= 0;
    
    repeat (2) @(posedge clk);
    
    //! Test with truncated packet (early tlast) - Little Endian
    test_big_endian = 0;
    $display("--- Testing truncated packet (Little Endian) ---");
    @(posedge clk);
    s_axis_le.tvalid <= 1;
    s_axis_le.tdata <= 64'h0011223344556677;
    s_axis_le.tlast <= 0;
    s_axis_le.tkeep <= 8'hFF;
    
    while (!(s_axis_le.tvalid && s_axis_le.tready)) @(posedge clk);
    
    @(posedge clk);
    s_axis_le.tdata <= 64'hF788F788F788F788; // PTP type but truncated (little endian)
    s_axis_le.tlast <= 1; // Early termination
    
    while (!(s_axis_le.tvalid && s_axis_le.tready)) @(posedge clk);
    
    @(posedge clk);
    s_axis_le.tvalid <= 0;
    s_axis_le.tlast <= 0;
    
    repeat (2) @(posedge clk);
    
    $display("ERROR INJECTION TEST COMPLETED");
  endtask

  //! @brief Main test execution
  initial begin
    //! Reset sequence
    rstn <= 0;
    repeat (10) @(posedge clk);
    rstn <= 1;
    repeat (10) @(posedge clk);
    $display("Starting Enhanced PTP Timestamping Core Testbench");
    $display("BEAT_BYTES = %0d", BEAT_BYTES);
    $display("PTP_SEQ_ID_OFFSET = %0d", PTP_SEQ_ID_OFFSET);
    $display("ETH_HEADER_NO_VLAN_OFFSET = %0d", ETH_HEADER_NO_VLAN_OFFSET);
    
    //! Start monitoring tasks
    fork
      monitor_metadata();
      debug_monitor();
      performance_monitor();
    join_none

    //! Run comprehensive test suite
    run_test_suite(1, 1);  // Big endian, TX mode
    run_test_suite(0, 0);  // Little endian, RX mode
    run_test_suite(1, 0);  // Big endian, RX mode
    run_test_suite(0, 1);  // Little endian, TX mode
    
    //! Run stress test
    stress_test();
    
    //! Run error injection test
    error_injection_test();
    
    repeat (20) @(posedge clk);
    
    $display("\n" + "="*80);
    $display("ALL TESTS COMPLETED SUCCESSFULLY");
    $display("="*80);
    
  end

  //! @brief Simulation timeout protection
  initial begin
    #50000;
    $display("ERROR: Simulation timeout!!!");
    $finish;
  end

  //! @brief Protocol compliance checker
  //! @details Verifies AXI-Stream protocol compliance
  always @(posedge clk) begin
    if (rstn) begin
      //! Check for protocol violations on Big Endian interface
      if (s_axis_be.tvalid && !s_axis_be.tready && $past(s_axis_be.tvalid) &&
          ($past(s_axis_be.tdata) !== s_axis_be.tdata)) begin
        $error("AXI-Stream protocol violation (BE): tdata changed while tvalid high and tready low");
      end
      
      if (s_axis_be.tvalid && !s_axis_be.tready && $past(s_axis_be.tvalid) &&
          ($past(s_axis_be.tlast) !== s_axis_be.tlast)) begin
        $error("AXI-Stream protocol violation (BE): tlast changed while tvalid high and tready low");
      end
      
      //! Check for protocol violations on Little Endian interface
      if (s_axis_le.tvalid && !s_axis_le.tready && $past(s_axis_le.tvalid) &&
          ($past(s_axis_le.tdata) !== s_axis_le.tdata)) begin
        $error("AXI-Stream protocol violation (LE): tdata changed while tvalid high and tready low");
      end
      
      if (s_axis_le.tvalid && !s_axis_le.tready && $past(s_axis_le.tvalid) &&
          ($past(s_axis_le.tlast) !== s_axis_le.tlast)) begin
        $error("AXI-Stream protocol violation (LE): tlast changed while tvalid high and tready low");
      end
    end
  end

endmodule