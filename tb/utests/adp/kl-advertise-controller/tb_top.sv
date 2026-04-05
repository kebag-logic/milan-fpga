module tb_top();

  parameter T = 10;
  bit clk;
  bit rst_n;
  adp_advertise_event_t advertise_event;
  
  logic [63:0] rcv_entity_id;
  logic [63:0] entity_id;
  logic [63:0] grandmaster_id;

  bit rcv_adp_discover;
  bit link_down;
  bit link_up;
  bit shutdown;
  link_status_t link_status;
  tmr_events_t tmr_events;
  bit start_tmr_delay;
  bit stop_tmr_delay;
  bit start_tmr_advertise;
  bit stop_tmr_advertise;

  bit timeout;
  bit tmr_delay;
  bit tmr_advertise;

  KL_advertise_controller DUT
  (
    .clk_i(clk),
    .rst_n(rst_n),
    .rcv_entity_id_i(rcv_entity_id),
    .entity_id_i(entity_id),
    .grandmaster_id_i(grandmaster_id),
    .rcv_adp_discover_i(rcv_adp_discover),
    .link_status(link_status),
    .tmr_events(tmr_events),
    .advertise_event_o(advertise_event)
  );


  always #(T/2) clk = ~clk;

  task reset_dut;
    rcv_entity_id = 64'h0;
    entity_id = 64'hFFFF_CCCC_EEEE_DDDD; // PAAD entity_id
    grandmaster_id = {1'd1};
    #100;
    $display("[INFO][TOP] : Reseting the DUT");
    rst_n = 1'd1;
  endtask

  task monitor_event;
    $monitor(" Event LINK_UP triggered %d", advertise_event.LINK_UP);
    $monitor(" Event LINK_DOWN triggered %d", advertise_event.LINK_DOWN);
    $monitor(" Event RCV_ADP_DISCOVER triggered %d", advertise_event.RCV_ADP_DISCOVER);
    $monitor(" Event TMR_ADVERTISE triggered %d", advertise_event.TMR_ADVERTISE);
    $monitor(" Event TMR_DELAY triggered %d", advertise_event.TMR_DELAY);
    $monitor(" Event GM_CHANGE triggered %d", advertise_event.GM_CHANGE);
    $monitor(" Event SHUTDOWN triggered %d", advertise_event.SHUTDOWN);
  endtask

  initial begin
    reset_dut();

    $display("[INFO][TOP] : ----------- TP.UT.ADVERTISE_CNTRL_0000 -----------");
    $display("[INFO][TOP] : Giving link_up, link_down and shutdown signals and observing the advertise event");
    link_status.link_up = 1'd1;
    link_status.link_down = 1'd1;
    link_status.shutdown = 1'd1;
    @(posedge clk);
    if (advertise_event.LINK_UP & advertise_event.LINK_DOWN & advertise_event.SHUTDOWN)
      $display("[INFO][TOP] : TP.UT.ADVERTISE_CNTRL_0000 Successful");
    else $fatal("TP.UT.ADVERTISE_CNTRL_0000 Failed");

    link_status.link_up = 1'd0;
    link_status.link_down = 1'd0;
    link_status.shutdown = 1'd0;

    $display("[INFO][TOP] : ------------------------------------");
    $display("[INFO][TOP] : ------------------------------------");
    $display("[INFO][TOP] : ----------- TP.UT.ADVERTISE_CNTRL_0001 -----------");
    $display("[INFO][TOP] : Provide rcv_adp_discover with rcv_entity_id zero");
    @(posedge clk);
    rcv_adp_discover = 1'd1;
    @(posedge clk);
    rcv_adp_discover = 1'd0;
    if (advertise_event.RCV_ADP_DISCOVER) 
      $display("[INFO][TOP] : TP.UT.ADVERTISE_CNTRL_0001 Successful");
    else $fatal("TP.UT.ADVERTISE_CNTRL_0001 Failed");

    #50;
    $display("[INFO][TOP] : ------------------------------------");
    $display("[INFO][TOP] : ------------------------------------");
    $display("[INFO][TOP] : ----------- TP.UT.ADVERTISE_CNTRL_0002 -----------");
    $display("[INFO][TOP] : Provide rcv_adp_discover with rcv_entity_id that is equal to the entity_id");
    rcv_entity_id = entity_id;
    @(posedge clk);
    rcv_adp_discover = 1'd1;
    @(posedge clk);
    rcv_adp_discover = 1'd0;
    if (advertise_event.RCV_ADP_DISCOVER) 
      $display("[INFO][TOP] : TP.UT.ADVERTISE_CNTRL_0002 Successful");
    else $fatal("TP.UT.ADVERTISE_CNTRL_0002 Failed");

    #50;
    $display("[INFO][TOP] : ------------------------------------");
    $display("[INFO][TOP] : ------------------------------------");
    $display("[INFO][TOP] : ----------- TP.UT.ADVERTISE_CNTRL_0003 -----------");
    $display("[INFO][TOP] : Provide rcv_adp_discover with rcv_entity_id that is NOT equal to the entity_id");
    rcv_entity_id = 64'h1234_1234_1234_1234;
    @(posedge clk);
    rcv_adp_discover = 1'd1;
    @(posedge clk);
    rcv_adp_discover = 1'd0;
    if (!advertise_event.RCV_ADP_DISCOVER) 
      $display("[INFO][TOP] : TP.UT.ADVERTISE_CNTRL_0003 Successful");
    else $fatal("TP.UT.ADVERTISE_CNTRL_0003 Failed");


    $display("[INFO][TOP] : ------------------------------------");
    $display("[INFO][TOP] : ------------------------------------");
    $display("[INFO][TOP] : ----------- TP.UT.ADVERTISE_CNTRL_0004 -----------");
    $display("[INFO][TOP] : Give different grandmaster_id and observe the GM_CHANGE event");
    #1ns
    grandmaster_id = 64'hCDCD_CDCD_CDCD_CDCD;
    @(posedge clk);
    if (advertise_event.GM_CHANGE)
      $display("[INFO][TOP] : TP.UT.ADVERTISE_CNTRL_0004 Successful");
    else $fatal("TP.UT.ADVERTISE_CNTRL_0004 Failed");


    $display("[INFO][TOP] : ----------- TP.UT.ADVERTISE_CNTRL_0005 -----------");
    $display("[INFO][TOP] : Start both counters and wait for EVENT");
    @(posedge clk);
    tmr_events.start_tmr_advertise = 1'd1;
    tmr_events.start_tmr_delay = 1'd1;
    @(posedge clk);
    tmr_events.start_tmr_advertise = 1'd0;
    tmr_events.start_tmr_delay = 1'd0;


    fork
      // Event TMR_DELAY
      begin
        @(advertise_event.TMR_DELAY);
        tmr_delay = 1'd1;
      end
      // Event TMR_ADVERTISE
      begin
        @(advertise_event.TMR_ADVERTISE);
        tmr_advertise = 1'd1;
      end
      // Timeout
      begin
        #6s;
        $fatal("TP.UT.ADVERTISE_CNTRL_0005 Failed");
      end
    join_none

    wait(tmr_delay && tmr_advertise);
    $display("[INFO][TOP] : TP.UT.ADVERTISE_CNTRL_0005 Successful");
    disable fork;
    $finish;

  end
endmodule