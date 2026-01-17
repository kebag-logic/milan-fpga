module tb_top();

  parameter T = 10;
  bit clk;
  bit rst_n;

  // Inputs
  logic [31:0] rcv_available_index;
  logic [15:0] rcv_interface_index;
  logic [4:0] rcv_valid_time;
  logic [63:0] rcv_gptp_grandmaster_id;
  logic [7:0] rcv_gptp_domain_number;
  logic active_talker;
  logic RCV_ADP_AVAILABLE;
  logic RCV_ADP_DEPARTING;
  logic TMR_NO_ADP;
  logic [63:0] gptp_grandmaster_id;
  logic [7:0] gptp_domain_number;
  // Outputs
  wire EVT_TK_DISCOVERED;
  wire EVT_TK_DEPARTED;

  bit status = 1;

  typedef enum logic [2:0] {
    SINK_NOT_CONNECTED_S,
    TK_NOT_DISCOVERED_S,
    TK_NOT_DISCOVERED_2_S,
    TK_DISCOVERED_S,
    TK_DISCOVERED_AVA_S,
    TK_DISCOVERED_AVA_2_S,
    TK_DISCOVERED_DEP_S
  } state_discovery_s;

  KL_discovery_state DUT
  (
    .clk_i(clk),
    .rst_n(rst_n),
    .rcv_available_index_i(rcv_available_index),
    .rcv_interface_index_i(rcv_interface_index),
    .rcv_valid_time_i(rcv_valid_time),
    .rcv_gptp_grandmaster_id_i(rcv_gptp_grandmaster_id),
    .rcv_gptp_domain_number_i(rcv_gptp_domain_number),
    .active_talker(active_talker),
    .RCV_ADP_AVAILABLE(RCV_ADP_AVAILABLE),
    .RCV_ADP_DEPARTING(RCV_ADP_DEPARTING),
    .TMR_NO_ADP(TMR_NO_ADP),
    .gptp_grandmaster_id_i(gptp_grandmaster_id),
    .gptp_domain_number_i(gptp_domain_number),
    .EVT_TK_DISCOVERED(EVT_TK_DISCOVERED),
    .EVT_TK_DEPARTED(EVT_TK_DEPARTED)
  );

  always #(T/2) clk = ~clk;

  task reset_dut;
    #100;
    $display("[INFO][TOP] : Reseting the DUT");
    rcv_available_index = '0;
    rcv_interface_index = '0;
    rcv_valid_time = '0;
    rcv_gptp_grandmaster_id = '0;
    rcv_gptp_domain_number = '0;
    active_talker = '0;
    RCV_ADP_AVAILABLE = '0;
    RCV_ADP_DEPARTING = '0;
    TMR_NO_ADP = '0;
    gptp_grandmaster_id = {$random, $random};
    gptp_domain_number = $urandom_range(0,255);
    rst_n = 1'd1;
  endtask

  task automatic give_strobe;
    ref logic strobe;
    @(posedge clk);
    strobe = 1'd1;
    @(posedge clk);
    strobe = 1'd0;
  endtask

  task automatic TP_UT_DISCOVERY_STATE_0000;
    ref bit status;
    begin
      $display("-------------------------------------------");    
      $display("[INFO][TOP] : TP.UT.DISCOVERY_STATE_0000 ");
      $display("[INFO][TOP] : Checking the active_talker input reactions ");
      @(posedge clk);
      // Give active_talker to enable the state machine
      active_talker = 1'd1;
      repeat ($urandom_range(1,30)) @(posedge clk);
      // Check the DISCOVERY STATE MACHINE
      status &= (DUT.state_discovery_r == TK_NOT_DISCOVERED_S);
      @(posedge clk);
      // Disable the active_talker
      active_talker = 1'd0;
      repeat ($urandom_range(1,30)) @(posedge clk);
      // Check the DISCOVERY STATE MACHINE
      status &= (DUT.state_discovery_r == SINK_NOT_CONNECTED_S);
      if (!status) $fatal(1, "[FATAL][TOP] : TP.UT.DISCOVERY_STATE_0000 Failed");
      else $display("[INFO][TOP] : TP.UT.DISCOVERY_STATE_0000 Succesfull");
      // Leave the State machine active to proceed with other test cases
      active_talker = 1'd1;
    end
  endtask

  task automatic TP_UT_DISCOVERY_STATE_0001;
    ref bit status;
    ref logic RCV_ADP_AVAILABLE;
    ref logic [31:0] rcv_available_index;
    ref logic [15:0] rcv_interface_index;
    ref logic [4:0] rcv_valid_time;
    ref logic [63:0] rcv_gptp_grandmaster_id;
    ref logic [7:0] rcv_gptp_domain_number;
    begin
      $display("-------------------------------------------");    
      $display("[INFO][TOP] : TP.UT.DISCOVERY_STATE_0001 ");
      $display("[INFO][TOP] : POSITIVE - 5.6.4.5.1");
      // Random numbers for indexes
      rcv_available_index = $random;
      rcv_interface_index = $urandom_range(0,65535);
      rcv_valid_time = 5'd10; // Constant from Specs
      // Test case 2.1
      rcv_gptp_grandmaster_id = gptp_grandmaster_id;
      rcv_gptp_domain_number = gptp_domain_number;
      give_strobe(RCV_ADP_AVAILABLE);
      @(posedge clk);
      status &= (DUT.tk_not_available_index_r == rcv_available_index);
      status &= (DUT.tk_not_interface_index_r == rcv_interface_index);
      status &= (DUT.tk_not_valid_time_r == rcv_valid_time);
      fork
        begin
          @(DUT.start_tmr_no_adp_r);
          $display("[INFO][TOP] : The Counter has started");
        end
        begin
          @(EVT_TK_DISCOVERED);
          $display("[INFO][TOP] : EVT_TK_DISCOVERED Received");
        end
      join
      @(posedge clk);
      status &= (DUT.state_discovery_r == TK_DISCOVERED_S);
      if (!status) $fatal(1, "[FATAL][TOP] : TP.UT.DISCOVERY_STATE_0001 Failed");
      else $display("[INFO][TOP] : TP.UT.DISCOVERY_STATE_0001 Succesfull");
    end
  endtask

  task automatic TP_UT_DISCOVERY_STATE_0002;
    ref bit status;
    ref logic RCV_ADP_AVAILABLE;
    ref logic [31:0] rcv_available_index;
    ref logic [15:0] rcv_interface_index;
    ref logic [63:0] rcv_gptp_grandmaster_id;
    ref logic [7:0] rcv_gptp_domain_number;
    begin
      $display("-------------------------------------------");    
      $display("[INFO][TOP] : TP.UT.DISCOVERY_STATE_0002");
      $display("[INFO][TOP] : POSITIVE - Clause 5.6.4.5.2");
      rcv_available_index++; // Increment available_index
      give_strobe(RCV_ADP_AVAILABLE);
      @(posedge clk);
      // Check whether the save is correct
      status &= (DUT.tk_available_index_r == rcv_available_index);
      fork
        begin
          @(DUT.stop_tmr_no_adp_r); // Reseting the counter
          $display("[INFO][TOP] : The Counter has started");
        end
        begin
          @(DUT.start_tmr_no_adp_r);
          $display("[INFO][TOP] : EVT_TK_DISCOVERED Received");
        end
      join
      status &= (DUT.state_discovery_r == TK_DISCOVERED_S);
      if (!status) $fatal(1, "[FATAL][TOP] : TP.UT.DISCOVERY_STATE_0002 Failed");
      else $display("[INFO][TOP] : TP.UT.DISCOVERY_STATE_0002 Succesfull");
    end
  endtask

  task automatic TP_UT_DISCOVERY_STATE_0003;
    ref bit status;
    ref logic RCV_ADP_DEPARTING;
    ref logic [15:0] rcv_interface_index;
    begin
      $display("-------------------------------------------");    
      $display("[INFO][TOP] : TP.UT.DISCOVERY_STATE_0003");
      $display("[INFO][TOP] : POSITIVE - Clause 5.6.4.5.3");
      give_strobe(RCV_ADP_DEPARTING);
      @(posedge clk);
      fork
        begin
          @(DUT.stop_tmr_no_adp_r); // Check whether the counter stopped
          $display("[INFO][TOP] : The Counter has stopped");
        end
        begin
          @(DUT.EVT_TK_DEPARTED); // Check whether departed is given
          $display("[INFO][TOP] : EVT_TK_DEPARTED Received");
        end
      join
      status &= (DUT.state_discovery_r == TK_NOT_DISCOVERED_S);
      if (!status) $fatal(1, "[FATAL][TOP] : TP.UT.DISCOVERY_STATE_0003 Failed");
      else $display("[INFO][TOP] : TP.UT.DISCOVERY_STATE_0003 Succesfull");
    end
  endtask

  task automatic TP_UT_DISCOVERY_STATE_0004;
    ref bit status;
    begin
      $display("-------------------------------------------");    
      $display("[INFO][TOP] : TP.UT.DISCOVERY_STATE_0004");
      $display("[INFO][TOP] : POSITIVE - Clause 5.6.4.5.4");
      $display("[INFO][TOP] : Giving TMR_NO_ADP event");
      @(posedge clk);
      DUT.TMR_NO_ADP_COUNTER_0.completed_r = 1'd1;
      @(posedge clk);
      DUT.TMR_NO_ADP_COUNTER_0.completed_r = 1'd0;
      @(DUT.EVT_TK_DEPARTED); // Check whether departed is given
      $display("[INFO][TOP] : EVT_TK_DEPARTED Received");
      status &= (DUT.state_discovery_r == TK_NOT_DISCOVERED_S);
      if (!status) $fatal(1, "[FATAL][TOP] : TP.UT.DISCOVERY_STATE_0004 Failed");
      else $display("[INFO][TOP] : TP.UT.DISCOVERY_STATE_0004 Succesfull");
    end
  endtask

  initial begin
    reset_dut();
    #100ns;
    TP_UT_DISCOVERY_STATE_0000(status);
    #50ns;
    TP_UT_DISCOVERY_STATE_0001(status,RCV_ADP_AVAILABLE, rcv_available_index, rcv_interface_index,rcv_valid_time,rcv_gptp_grandmaster_id, rcv_gptp_domain_number);
    #50ns;
    TP_UT_DISCOVERY_STATE_0002(status,RCV_ADP_AVAILABLE, rcv_available_index, rcv_interface_index,rcv_gptp_grandmaster_id, rcv_gptp_domain_number);
    #50ns;
    TP_UT_DISCOVERY_STATE_0003(status,RCV_ADP_DEPARTING, rcv_interface_index);
    $display("[INFO][TOP] : Re-do the Test case 2 to make the DUT on TK_DISCOVERED state");
    TP_UT_DISCOVERY_STATE_0001(status,RCV_ADP_AVAILABLE, rcv_available_index, rcv_interface_index,rcv_valid_time,rcv_gptp_grandmaster_id, rcv_gptp_domain_number);
    #50ns;
    TP_UT_DISCOVERY_STATE_0004(status);
    $finish;
  end

  /* Test Scenarios
      1. Assert active_talker and observe the state as TK_NOT_DISCOVERED_S.
      Re-assert active talker and observe the state as SINK_NOT_CONNECTED_S.

      2. Clause 5.6.4.5.1 - Active_talker HIGH
        ------------------------------ POSITIVE ---------------------------------
        2.1 Give RCV_ADP_AVAILABLE event, provide gptp_domain|grandmaster id equal to the inputs from PTP module
        2.2 Check whether rcv_available_index and rcv_interface_indexes are matched with
        internal registers
        2.3 Check whether timer has started.
        2.4 Observe the EVT_TK_DISCOVERED and check whether state is TK_DISCOVERED

      3. Clause 5.6.4.5.2 
      ------------------------------ POSITIVE ---------------------------------
      3.1 
        3.1.1 Give RCV_ADP_AVAILABLE event with interface_index equal to the previous value.
        3.1.2 Give available_index bigger than previous value
        3.1.3 Check whether TMR_NO_ADP counter reset and state is TK_DISCOVERED
      3.2
        3.2.1 Give RCV_ADP_DEPARING with the same interface_index.
        3.2.2 Check whether timer stopped by the DUT and check EVT_TK_DEPARTED is given
        3.2.3 Check whether the state is TK_NOT_DISCOVERED
      3.3 
        3.3.1 Re-do the test case 2 to make the DUT in TK_DISCOVERED state
        3.3.2 Give timer_completed to DUT (TMR_NO_ADP event)
        3.3.3 Check whether the state is TK_NOT_DISCOVERED and EVT_TK_DEPARTED is given

  */
endmodule