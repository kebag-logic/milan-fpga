/*
 * SPDX-FileCopyrightText: 2025 Oguz Kahraman <oguz.kahraman@kebag-logic.com>
 *
 * SPDX-License-Identifier: CERN-OHL-W-2.0
 */

/*
------------------------------------------------------------------------------
  File        : tb_ptp_ts_top.sv
  Author      : Oguz Kahraman

                oguz.kahraman@kebag-logic.com

  Date        : 2025-07-19
  Description : Comprehensive integration test for ptp_ts_top module.
                
                Key Test Scenarios:
                - Concurrent TX/RX PTP packet processing
                - Timestamp metadata preservation
                - Back-to-back packet handling
                - Mixed PTP/non-PTP traffic
                - Clock domain crossing validation
                - FIFO overflow protection

  Company     : Kebag Logic
  Project     : PTP Timestamping for Custom RGMII MAC
------------------------------------------------------------------------------
*/

`timescale 1ns/1ps

module tb_ptp_ts_top;

  //! Test Parameters
  localparam int TDATA_WIDTH = 64;
  localparam int TS_WIDTH = 64;
  localparam int STEP_SIZE = 8;
  localparam int METADATA_TDATA_WIDTH = 64;
  localparam bit BIG_ENDIAN = 0;
  localparam bit [15:0] ETH_TYPE = 16'hF788;
  localparam int CDC_PIPELINE_DELAY = 3;
  localparam int BEAT_BYTES = TDATA_WIDTH / 8;

  //! Clock Generation
  logic gtx_clk = 0;
  logic axis_clk = 0;
  always #4.0 gtx_clk = ~gtx_clk;    // 125MHz
  always #5.0 axis_clk = ~axis_clk;   // 100MHz

  //! Reset Signals
  logic gtx_resetn = 0;
  logic axis_resetn = 0;

  //! TX AXI-Stream Interface
  logic [TDATA_WIDTH-1:0] s_axis_tx_tdata;
  logic s_axis_tx_tvalid;
  wire s_axis_tx_tready;
  logic s_axis_tx_tlast;
  logic [(TDATA_WIDTH/8)-1:0] s_axis_tx_tkeep;

  wire [TDATA_WIDTH-1:0] m_axis_tx_tdata;
  wire m_axis_tx_tvalid;
  logic m_axis_tx_tready;
  wire m_axis_tx_tlast;
  wire [(TDATA_WIDTH/8)-1:0] m_axis_tx_tkeep;

  //! RX AXI-Stream Interface
  logic [TDATA_WIDTH-1:0] s_axis_rx_tdata;
  logic s_axis_rx_tvalid;
  wire s_axis_rx_tready;
  logic s_axis_rx_tlast;
  logic [(TDATA_WIDTH/8)-1:0] s_axis_rx_tkeep;

  wire [TDATA_WIDTH-1:0] m_axis_rx_tdata;
  wire m_axis_rx_tvalid;
  logic m_axis_rx_tready;
  wire m_axis_rx_tlast;
  wire [(TDATA_WIDTH/8)-1:0] m_axis_rx_tkeep;

  //! Timestamp Metadata Interface
  wire [TDATA_WIDTH-1:0] ts_m_axis_rx_tdata;
  wire ts_m_axis_rx_tvalid;
  logic ts_m_axis_rx_tready;
  wire ts_m_axis_rx_tlast;
  wire [(TDATA_WIDTH/8)-1:0] ts_m_axis_rx_tkeep;

  //! Test Control Signals
  logic test_active = 0;
  logic tx_packet_active = 0;
  logic rx_packet_active = 0;
  
  //! Statistics and Monitoring
  int tx_packets_sent = 0;
  int rx_packets_sent = 0;
  int tx_ptp_packets = 0;
  int rx_ptp_packets = 0;
  int metadata_packets_received = 1;
  
  // Packet Database
  typedef struct {
    string name;
    bit is_ptp;
    bit [15:0] seq_id;
    int packet_length;  //! in beats
    bit is_tx;         //! 1=TX, 0=RX
  } test_packet_t;

  test_packet_t test_packets[] = {
    '{"TX_PTP_1", 1, 16'h1001, 10, 1},
    '{"RX_PTP_1", 1, 16'h2001, 10, 0},
    '{"TX_PTP_2", 1, 16'h1002, 12, 1},
    '{"RX_PTP_2", 1, 16'h2002, 8, 0},
    '{"TX_NonPTP_1", 0, 16'h1003, 9, 1},
    '{"RX_NonPTP_1", 0, 16'h2003, 11, 0},
    '{"TX_PTP_3", 1, 16'h1004, 15, 1},
    '{"RX_PTP_3", 1, 16'h2004, 8, 0},
    '{"TX_PTP_Short", 1, 16'h1005, 8, 1},
    '{"RX_PTP_Long", 1, 16'h2005, 20, 0}
  };

  //! DUT Instantiation
  ptp_ts_top #(
    .TDATA_WIDTH(TDATA_WIDTH),
    .TS_WIDTH(TS_WIDTH),
    .STEP_SIZE(STEP_SIZE),
    .METADATA_TDATA_WIDTH(METADATA_TDATA_WIDTH),
    .BIG_ENDIAN(BIG_ENDIAN),
    .ETH_TYPE(ETH_TYPE),
    .CDC_PIPELINE_DELAY(CDC_PIPELINE_DELAY)
  ) dut (
    .gtx_clk(gtx_clk),
    .gtx_resetn(gtx_resetn),
    .axis_clk(axis_clk),
    .axis_resetn(axis_resetn),
    
    .s_axis_tx_tdata(s_axis_tx_tdata),
    .s_axis_tx_tvalid(s_axis_tx_tvalid),
    .s_axis_tx_tready(s_axis_tx_tready),
    .s_axis_tx_tlast(s_axis_tx_tlast),
    .s_axis_tx_tkeep(s_axis_tx_tkeep),
    
    .m_axis_tx_tdata(m_axis_tx_tdata),
    .m_axis_tx_tvalid(m_axis_tx_tvalid),
    .m_axis_tx_tready(m_axis_tx_tready),
    .m_axis_tx_tlast(m_axis_tx_tlast),
    .m_axis_tx_tkeep(m_axis_tx_tkeep),
    
    .s_axis_rx_tdata(s_axis_rx_tdata),
    .s_axis_rx_tvalid(s_axis_rx_tvalid),
    .s_axis_rx_tready(s_axis_rx_tready),
    .s_axis_rx_tlast(s_axis_rx_tlast),
    .s_axis_rx_tkeep(s_axis_rx_tkeep),
    
    .m_axis_rx_tdata(m_axis_rx_tdata),
    .m_axis_rx_tvalid(m_axis_rx_tvalid),
    .m_axis_rx_tready(m_axis_rx_tready),
    .m_axis_rx_tlast(m_axis_rx_tlast),
    .m_axis_rx_tkeep(m_axis_rx_tkeep),
    
    .ts_m_axis_tdata(ts_m_axis_rx_tdata),
    .ts_m_axis_tvalid(ts_m_axis_rx_tvalid),
    .ts_m_axis_tready(ts_m_axis_rx_tready),
    .ts_m_axis_tlast(ts_m_axis_rx_tlast),
    .ts_m_axis_tkeep(ts_m_axis_rx_tkeep)
  );

  //! Initialize all signals
  initial begin
    s_axis_tx_tdata = 0;
    s_axis_tx_tvalid = 0;
    s_axis_tx_tlast = 0;
    s_axis_tx_tkeep = 8'hFF;
    
    s_axis_rx_tdata = 0;
    s_axis_rx_tvalid = 0;
    s_axis_rx_tlast = 0;
    s_axis_rx_tkeep = 8'hFF;
    
    m_axis_tx_tready = 1;
    m_axis_rx_tready = 1;
    ts_m_axis_rx_tready = 1;
  end

  //! Reset Sequence
  initial begin
    gtx_resetn = 0;
    axis_resetn = 0;
    repeat (20) @(posedge axis_clk);
    gtx_resetn = 1;
    axis_resetn = 1;
    repeat (20) @(posedge axis_clk);
    $display("=== Reset sequence completed ===");
  end

  //! Task to send a TX packet
  task send_tx_packet(test_packet_t packet);
    logic [TDATA_WIDTH-1:0] tdata;
    int beat_count;
    
    $display("[%0t] Starting TX packet: %s (PTP=%0b, seq_id=0x%04x, length=%0d)", 
             $time, packet.name, packet.is_ptp, packet.seq_id, packet.packet_length);
    
    tx_packet_active = 1;
    
    //! Wait for ready
    while (!s_axis_tx_tready) @(posedge axis_clk);
    
    // Beat 0: MAC destination and source start
    @(posedge axis_clk);
    s_axis_tx_tdata <= 64'h00112233445566aa;
    s_axis_tx_tvalid <= 1;
    s_axis_tx_tlast <= 0;
    s_axis_tx_tkeep <= 8'hFF;
    
    //! Beat 1: MAC source end + EtherType
    @(posedge axis_clk);
    tdata = 64'habcdeffeabcd0000;
    if (packet.is_ptp) begin
      //! Little endian EtherType for PTP
      tdata[47:40] = ETH_TYPE[15:8];   // byte 12
      tdata[39:32] = ETH_TYPE[7:0];   // byte 13
    end else begin
      //! Non-PTP EtherType (IPv4)
      tdata[47:40] = 8'h00;
      tdata[39:32] = 8'h08;
    end
    s_axis_tx_tdata <= tdata;
    
    //! Filler beats until PTP sequence ID location (beat 4, bytes 30-31)
    beat_count = 2;
    while (beat_count < 5) begin
      @(posedge axis_clk);
      s_axis_tx_tdata <= 64'hDEADBEEFCAFEBABE + beat_count;
      s_axis_tx_tlast <= 0;
      beat_count++;
    end
    
    //! Beat containing PTP sequence ID (bytes 30-31)
    @(posedge axis_clk);
    tdata = 64'hFEEDFACE00000000;
    if (packet.is_ptp) begin
      // Little endian seq_id at bytes 30-31
      tdata[47:40] = packet.seq_id[7:0];   // byte 30 (LSB)
      tdata[39:32] = packet.seq_id[15:8];  // byte 31 (MSB)
    end
    s_axis_tx_tdata <= tdata;
    
    //! Remaining beats
    beat_count = 6;
    while (beat_count < packet.packet_length) begin
      @(posedge axis_clk);
      s_axis_tx_tdata <= {beat_count[7:0], 56'h123456789ABCDEF0};
      s_axis_tx_tlast <= (beat_count == packet.packet_length - 1);
      beat_count++;
    end
    
    //! End transaction
    @(posedge axis_clk);
    s_axis_tx_tvalid <= 0;
    s_axis_tx_tlast <= 0;
    
    tx_packet_active = 0;
    tx_packets_sent++;
    if (packet.is_ptp) tx_ptp_packets++;
    
    $display("[%0t] TX packet %s completed", $time, packet.name);
  endtask

  //! Task to send an RX packet
  task send_rx_packet(test_packet_t packet);
    logic [TDATA_WIDTH-1:0] tdata;
    int beat_count;
    
    $display("[%0t] Starting RX packet: %s (PTP=%0b, seq_id=0x%04x, length=%0d)", 
             $time, packet.name, packet.is_ptp, packet.seq_id, packet.packet_length);
    
    rx_packet_active = 1;
    
    //! Wait for ready
    while (!s_axis_rx_tready) @(posedge axis_clk);
    
    //! Beat 0: MAC destination and source start  
    @(posedge axis_clk);
    s_axis_rx_tdata <= 64'h00998877665544aa;
    s_axis_rx_tvalid <= 1;
    s_axis_rx_tlast <= 0;
    s_axis_rx_tkeep <= 8'hFF;
    
    //! Beat 1: MAC source end + EtherType
    @(posedge axis_clk);
    tdata = 64'hbbccddee00000000;
    if (packet.is_ptp) begin
      // Little endian EtherType for PTP
      tdata[47:40] = ETH_TYPE[15:8];   // byte 12
      tdata[39:32] = ETH_TYPE[7:0];   // byte 13
    end else begin
      // Non-PTP EtherType (IPv4)
      tdata[47:40] = 8'h00;
      tdata[39:32] = 8'h08;
    end
    s_axis_rx_tdata <= tdata;
    
    //! Filler beats until PTP sequence ID location
    beat_count = 2;
    while (beat_count < 5) begin
      @(posedge axis_clk);
      s_axis_rx_tdata <= 64'hCAFEBABEDEADBEEF + beat_count;
      s_axis_rx_tlast <= 0;
      beat_count++;
    end
    
    //! Beat containing PTP sequence ID 
    @(posedge axis_clk);
    tdata = 64'hBABEFACE00000000;
    if (packet.is_ptp) begin
      //! Little endian seq_id at bytes 44-45
      tdata[47:40] = packet.seq_id[7:0];   // byte 44 (LSB) 
      tdata[39:32] = packet.seq_id[15:8];  // byte 45 (MSB)
    end
    s_axis_rx_tdata <= tdata;
    
    //! Remaining beats
    beat_count = 6;
    while (beat_count < packet.packet_length) begin
      @(posedge axis_clk);
      s_axis_rx_tdata <= {beat_count[7:0], 56'h987654321FEDCBA0};
      s_axis_rx_tlast <= (beat_count == packet.packet_length - 1);
      beat_count++;
    end
    
    //! End transaction
    @(posedge axis_clk);
    s_axis_rx_tvalid <= 0;
    s_axis_rx_tlast <= 0;
    
    rx_packet_active = 0;
    rx_packets_sent++;
    if (packet.is_ptp) rx_ptp_packets++;
    
    $display("[%0t] RX packet %s completed", $time, packet.name);
  endtask

  //! Task to send concurrent TX and RX packets  
  task send_concurrent_packets(test_packet_t tx_pkt, test_packet_t rx_pkt);
    $display("\n=== CONCURRENT TRANSMISSION TEST ===");
    $display("[%0t] Starting concurrent TX: %s and RX: %s", $time, tx_pkt.name, rx_pkt.name);
    
    fork
      send_tx_packet(tx_pkt);
      send_rx_packet(rx_pkt);
    join
    
    $display("[%0t] Concurrent transmission completed", $time);
  endtask

  int tx_idx = 0;
  int rx_idx = 1;
  //! Task for stess_test
  task stress_test();

    $display("\n=== STRESS TEST: ===");
    
    repeat (10) begin
      fork
        begin
          if (test_packets[tx_idx].is_tx) send_tx_packet(test_packets[tx_idx]);
          tx_idx = (tx_idx + 2) % $size(test_packets);
        end
        begin  
          if (!test_packets[rx_idx].is_tx) begin
            test_packets[rx_idx].is_tx = 0; // Ensure it's RX
            send_rx_packet(test_packets[rx_idx]);
          end
          rx_idx = (rx_idx + 2) % $size(test_packets);
        end
      join
      
      //! Minimal delay between packet pairs
      repeat (1) @(posedge axis_clk);
    end
    
    $display("Stress test completed");
  endtask

  //! Task to create backpressure on metadata output
  task metadata_backpressure_test();
    $display("\n=== METADATA BACKPRESSURE TEST ===");
    
    //! Apply backpressure to metadata interface
    ts_m_axis_rx_tready = 0;
    
    //! Send multiple PTP packets while metadata is blocked
    fork
      send_tx_packet(test_packets[0]);  //! TX PTP packet
      send_rx_packet(test_packets[1]);  //! RX PTP packet
    join
    
    repeat (20) @(posedge axis_clk);
    
    //! Release backpressure intermittently
    repeat (5) begin
      @(posedge axis_clk);
      ts_m_axis_rx_tready = 1;
      @(posedge axis_clk);
      ts_m_axis_rx_tready = 0;
      @(posedge axis_clk);
    end
    
    //! Fully release backpressure
    ts_m_axis_rx_tready = 1;
    repeat (50) @(posedge axis_clk);
    
    $display("Metadata backpressure test completed");
  endtask


  logic [15:0] seq_id_out;
  logic direction;
  logic [63:0] timestamp_out;
  logic expecting_timestamp = 0;
  //! Monitor task for metadata output
  task monitor_metadata_output();
    forever begin
      @(posedge axis_clk);
      
      if (ts_m_axis_rx_tvalid && ts_m_axis_rx_tready) begin
        if (!expecting_timestamp) begin
          //! First beat: timestamp
          timestamp_out = ts_m_axis_rx_tdata;
          expecting_timestamp = 1;
          $display("[%0t] Metadata timestamp: %0d", $time, timestamp_out);
        end else begin
          //! Second beat: seq_id and direction
          seq_id_out = ts_m_axis_rx_tdata[63:48];
          direction = ts_m_axis_rx_tdata[40];
          expecting_timestamp = 0;
          metadata_packets_received++;
          
          $display("[%0t] Metadata complete: seq_id=0x%04x, direction=%s, timestamp=%0d (total=%0d)", 
                   $time, seq_id_out, direction ? "TX" : "RX", timestamp_out, metadata_packets_received);
        end
      end
    end
  endtask

  //! Performance monitoring task
  task performance_monitor();
    forever begin
      #1000; //! Report every 1us if the test is active
      
      if (test_active) begin
        $display("\n--- Performance Report [%0t] ---", $time);
        $display("TX Packets: %0d (PTP: %0d)", tx_packets_sent, tx_ptp_packets);
        $display("RX Packets: %0d (PTP: %0d)", rx_packets_sent, rx_ptp_packets);
        $display("Metadata Received: %0d", metadata_packets_received);
        $display("Active: TX=%0b, RX=%0b", tx_packet_active, rx_packet_active);
        $display("--------------------------------");
      end
    end
  endtask

  //! Main test sequence
  initial begin
    $display("=== PTP Timestamping Top Module Integration Test ===");
    $display("Configuration: TDATA_WIDTH=%0d, BIG_ENDIAN=%0b, ETH_TYPE=0x%04x", 
             TDATA_WIDTH, BIG_ENDIAN, ETH_TYPE);
    
    //! Wait for reset completion
    wait(axis_resetn);
    repeat (10) @(posedge axis_clk);
    
    test_active = 1;
    
    //! Start monitoring tasks
    fork
      monitor_metadata_output(); 
      performance_monitor();
    join_none
    
    //! Test 1: Sequential packet transmission
    $display("\n=== TEST 1: Sequential Transmission ===");
    foreach (test_packets[i]) begin
      if (test_packets[i].is_tx) begin
        send_tx_packet(test_packets[i]);
      end else begin
        test_packets[i].is_tx = 0; // Ensure RX
        send_rx_packet(test_packets[i]);
      end
      repeat (2) @(posedge axis_clk);
    end
    
    //! Test 2: Concurrent transmission
    $display("\n=== TEST 2: Concurrent Transmission ===");
    send_concurrent_packets(test_packets[0], test_packets[1]);
    repeat (5) @(posedge axis_clk);
    send_concurrent_packets(test_packets[2], test_packets[3]);
    repeat (5) @(posedge axis_clk);
    
    //! Test 3: Rapid-fire stress test
    stress_test();
    repeat (5) @(posedge axis_clk);
    
    //! Test 4: Metadata backpressure
    metadata_backpressure_test();
    repeat (5) @(posedge axis_clk);
    
    //! Test 5: Mixed PTP/Non-PTP concurrent traffic
    $display("\n=== TEST 5: Mixed PTP/Non-PTP Concurrent Traffic ===");
    fork
      send_tx_packet(test_packets[0]);  // TX PTP
      send_rx_packet(test_packets[4]);  // RX Non-PTP
    join
    @(posedge axis_clk);
    fork
      send_tx_packet(test_packets[4]);  // TX Non-PTP
      send_rx_packet(test_packets[1]);  // RX PTP
    join
    
    //! Allow time for all metadata to be processed
    repeat (150) @(posedge axis_clk);

    test_active = 0;
    //! Final report
    $display("\n");
    $display("=======================================================================");
    $display("FINAL INTEGRATION TEST RESULTS");
    $display("=======================================================================");
    $display("TX Packets Sent: %0d (PTP: %0d)", tx_packets_sent, tx_ptp_packets);
    $display("RX Packets Sent: %0d (PTP: %0d)", rx_packets_sent, rx_ptp_packets);
    $display("Total PTP Packets: %0d", tx_ptp_packets + rx_ptp_packets);
    $display("Metadata Packets Received: %0d", metadata_packets_received);
    
    //! Validate results
    if (metadata_packets_received == (tx_ptp_packets + rx_ptp_packets)) begin
      $display("SUCCESS: All PTP packets generated metadata");
    end else begin
      $error("FAILED: Expected %0d metadata packets, got %0d", 
             tx_ptp_packets + rx_ptp_packets, metadata_packets_received);
    end

    $display("=======================================================================");
    $display("INTEGRATION TEST COMPLETED");
    $display("=======================================================================");
    
  end

  //! Simulation timeout
  initial begin
  #200000;
    $error("Simulation timeout!");
    $finish;
  end

endmodule
