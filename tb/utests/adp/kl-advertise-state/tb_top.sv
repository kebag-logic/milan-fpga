module tb_top();

  parameter TDATA_WIDTH_P = 64;
  parameter T = 10;
  bit clk;
  bit rst_n;

  entity_info_t mmap_entity_info;
  adp_advertise_event_t advertise_event;
  bit [63:0] grandmaster_id;
  bit [7:0] gptp_domain_number;

  tmr_events_t tmr_events;

  logic [63:0] dut_pkt[$];
  logic [63:0] ref_available_pkt[$];
  logic [63:0] ref_departing_pkt[$];
  bit status = 1;

  axi_stream_if #(.TDATA_WIDTH_P(TDATA_WIDTH_P)) m_axis(clk, rst_n);

  KL_advertise_state DUT
  (
    .clk_i(clk),
    .rst_n(rst_n),
    .mmap_entity_info_i(mmap_entity_info),
    .advertise_event_i(advertise_event),
    .grandmaster_id_i(grandmaster_id),
    .gptp_domain_number_i(gptp_domain_number),
    .tmr_events_o(tmr_events),
    .m_axis(m_axis)
  );

  always #(T/2) clk = ~clk;

  task reset_dut;
    #100;
    $display("[INFO][TOP] : Reseting the DUT");
    grandmaster_id = 64'hABCD_1234_FEFE_5678;
    gptp_domain_number = 8'hCD;
    advertise_event.LINK_DOWN = 0;
    advertise_event.LINK_UP = 0;
    advertise_event.SHUTDOWN = 0;
    advertise_event.RCV_ADP_DISCOVER = 0;
    advertise_event.TMR_ADVERTISE = 0;
    advertise_event.TMR_DELAY = 0;
    advertise_event.GM_CHANGE = 0;
    m_axis.tready = 1'd1;
    rst_n = 1'd1;
  endtask

  task mmap_assignments;
    mmap_entity_info.valid_time = 5'd10;
    mmap_entity_info.entity_id = {$urandom, $urandom};
    mmap_entity_info.entity_model_id = {$urandom, $urandom};
    mmap_entity_info.entity_capabilities = $urandom;
    {mmap_entity_info.talker_stream_sources,mmap_entity_info.talker_capabilities} = $urandom;
    {mmap_entity_info.listener_stream_sinks,mmap_entity_info.listener_capabilities} = $urandom;
    mmap_entity_info.controller_capabilities = $urandom;
    mmap_entity_info.available_index = $urandom;
    {mmap_entity_info.current_configuration_index,mmap_entity_info.identify_control_index} = $urandom;
    mmap_entity_info.interface_index = $urandom_range(0,65535);
    mmap_entity_info.association_id = {$urandom, $urandom};
    give_strobe(mmap_entity_info.entity_info_valid);
  endtask

  task generate_ref_packet;
    ref logic [63:0] ref_pkt[$];
    ref_pkt.push_back({16'h22F0, 8'hFA, 8'h00, mmap_entity_info.valid_time, 11'h38, mmap_entity_info.entity_id[63:48]});
    ref_pkt.push_back({mmap_entity_info.entity_id[47:0], mmap_entity_info.entity_model_id[63:48]});
    ref_pkt.push_back({mmap_entity_info.entity_model_id[47:0], mmap_entity_info.entity_capabilities[31:16]});
    ref_pkt.push_back({mmap_entity_info.entity_capabilities, mmap_entity_info.talker_stream_sources, mmap_entity_info.talker_capabilities, mmap_entity_info.listener_stream_sinks});
    ref_pkt.push_back({mmap_entity_info.listener_capabilities, mmap_entity_info.controller_capabilities, mmap_entity_info.available_index[31:16]});
    ref_pkt.push_back({mmap_entity_info.available_index[15:0], grandmaster_id[63:16]});
    ref_pkt.push_back({grandmaster_id[15:0], gptp_domain_number, 8'd0, mmap_entity_info.current_configuration_index, mmap_entity_info.identify_control_index});
    ref_pkt.push_back({mmap_entity_info.interface_index, mmap_entity_info.association_id[63:16]});
    ref_pkt.push_back({mmap_entity_info.association_id[15:0], 48'd0});
  endtask

  // Give events with one clock cycle
  task automatic give_strobe;
    ref logic strobe;
    begin
      @(posedge clk);
      strobe = 1'd1;
      @(posedge clk);
      strobe = 1'd0;
    end
  endtask

  // Save the m_axis transactions into unbounded queue
  task automatic save_m_axis;
    ref logic [63:0] pkt[$];
    begin
      while(!m_axis.tlast) begin
        @(posedge clk);
        if (m_axis.tvalid && m_axis.tready)
          pkt.push_back(m_axis.tdata);
      end
    end
  endtask

  // Compare what dut generated vs reference packet
  task compare_pkts;
    ref logic [63:0] ref_pkt[$];
    ref logic [63:0] dut_pkt[$];
    ref bit status;
    $display("[INFO][TOP][COMPARE-PACKETS]- Comparing the TX packet with Reference Packet");
    foreach (dut_pkt[i])
      status &= (ref_pkt[i] == dut_pkt[i]);
    dut_pkt.delete();
  endtask

  // --------------------------------------------------------------------- //
  // ---------------------------- TEST CASES ----------------------------- //
  // --------------------------------------------------------------------- //
  task TP_UT_ADVERTISE_STATE_0000;
    $display("-----------------------------------------------------------------------------");
    $display("[INFO][TOP][TP_UT_ADVERTISE_STATE_0000]- Test Case TP_UT_ADVERTISE_STATE_0000");
    give_strobe(advertise_event.LINK_UP);
    wait (tmr_events.start_tmr_delay);
    $display("[INFO][TOP][TP_UT_ADVERTISE_STATE_0000]- START_TMR_DELAY detected");
    $display("[INFO][TOP][TP_UT_ADVERTISE_STATE_0000]- Successful");
  endtask;

  task TP_UT_ADVERTISE_STATE_0001;
    $display("-----------------------------------------------------------------------------");
    $display("[INFO][TOP][TP_UT_ADVERTISE_STATE_0001]- Test Case TP_UT_ADVERTISE_STATE_0001");
    #100;
    give_strobe(advertise_event.TMR_DELAY);
    wait (tmr_events.start_tmr_advertise);
    $display("[INFO][TOP][TP_UT_ADVERTISE_STATE_0001]- START_TMR_ADVERTISE detected");
    save_m_axis(dut_pkt);
    compare_pkts(ref_available_pkt, dut_pkt, status);
    if (!status)
      $fatal("[INFO][TOP][TP_UT_ADVERTISE_STATE_0001] - FAILED");
    else
      $display("[INFO][TOP][TP_UT_ADVERTISE_STATE_0001]- Successful");
  endtask;

  task TP_UT_ADVERTISE_STATE_0002;
    $display("-----------------------------------------------------------------------------");
    $display("[INFO][TOP][TP_UT_ADVERTISE_STATE_0002]- Test Case TP_UT_ADVERTISE_STATE_0002");
    #100;

    give_strobe(advertise_event.LINK_UP);
    wait (tmr_events.start_tmr_delay);
    $display("[INFO][TOP][TP_UT_ADVERTISE_STATE_0002]- START_TMR_DELAY detected");
    #50;
    give_strobe(advertise_event.LINK_DOWN);
    wait (tmr_events.stop_tmr_delay);
    $display("[INFO][TOP][TP_UT_ADVERTISE_STATE_0002]- STOP_TMR_DELAY detected");
    $display("[INFO][TOP][TP_UT_ADVERTISE_STATE_0002]- Successful");
  endtask;

  task TP_UT_ADVERTISE_STATE_0003;
    $display("-----------------------------------------------------------------------------");
    $display("[INFO][TOP][TP_UT_ADVERTISE_STATE_0003]- Test Case TP_UT_ADVERTISE_STATE_0003");
    #100;

    give_strobe(advertise_event.LINK_UP);
    wait (tmr_events.start_tmr_delay);
    $display("[INFO][TOP][TP_UT_ADVERTISE_STATE_0003]- START_TMR_DELAY detected");
    #50;
    give_strobe(advertise_event.SHUTDOWN);
    wait (tmr_events.stop_tmr_delay);
    $display("[INFO][TOP][TP_UT_ADVERTISE_STATE_0003]- STOP_TMR_DELAY detected");
    save_m_axis(dut_pkt);
    compare_pkts(ref_departing_pkt, dut_pkt, status);
    if (!status)
      $fatal("[INFO][TOP][TP_UT_ADVERTISE_STATE_0003] - FAILED");
    else
      $display("[INFO][TOP][TP_UT_ADVERTISE_STATE_0003]- Successful");
  endtask;

  task TP_UT_ADVERTISE_STATE_0004;
    $display("-----------------------------------------------------------------------------");
    $display("[INFO][TOP][TP_UT_ADVERTISE_STATE_0004]- Test Case TP_UT_ADVERTISE_STATE_0004");
    #100;

    give_strobe(advertise_event.LINK_UP);
    #50;
    give_strobe(advertise_event.TMR_DELAY);
    #50;
    give_strobe(advertise_event.RCV_ADP_DISCOVER);
    wait (tmr_events.stop_tmr_advertise && tmr_events.start_tmr_delay);
    $display("[INFO][TOP][TP_UT_ADVERTISE_STATE_0004]- START_TMR_DELAY and STOP_TMR_ADVERTISE detected");
    $display("[INFO][TOP][TP_UT_ADVERTISE_STATE_0004]- Successful");
  endtask;

  task TP_UT_ADVERTISE_STATE_0005;
    $display("-----------------------------------------------------------------------------");
    $display("[INFO][TOP][TP_UT_ADVERTISE_STATE_0005]- Test Case TP_UT_ADVERTISE_STATE_0005");
    #100;

    give_strobe(advertise_event.TMR_DELAY);
    #50;
    give_strobe(advertise_event.TMR_ADVERTISE);
    wait (tmr_events.start_tmr_delay);
    $display("[INFO][TOP][TP_UT_ADVERTISE_STATE_0005]- START_TMR_DELAY detected");
    $display("[INFO][TOP][TP_UT_ADVERTISE_STATE_0005]- Successful");
  endtask;

  task TP_UT_ADVERTISE_STATE_0006;
    $display("-----------------------------------------------------------------------------");
    $display("[INFO][TOP][TP_UT_ADVERTISE_STATE_0006]- Test Case TP_UT_ADVERTISE_STATE_0006");
    #100;

    give_strobe(advertise_event.TMR_DELAY);
    #50;
    give_strobe(advertise_event.LINK_DOWN);
    wait (tmr_events.stop_tmr_advertise);
    $display("[INFO][TOP][TP_UT_ADVERTISE_STATE_0006]- STOP_TMR_ADVERTISE detected");
    $display("[INFO][TOP][TP_UT_ADVERTISE_STATE_0006]- Successful");
  endtask;

  task TP_UT_ADVERTISE_STATE_0007;
    $display("-----------------------------------------------------------------------------");
    $display("[INFO][TOP][TP_UT_ADVERTISE_STATE_0007]- Test Case TP_UT_ADVERTISE_STATE_0007");
    #100;
    give_strobe(advertise_event.LINK_UP);
    #50;
    give_strobe(advertise_event.TMR_DELAY);
    #50;
    give_strobe(advertise_event.GM_CHANGE);
    wait (tmr_events.start_tmr_delay);
    $display("[INFO][TOP][TP_UT_ADVERTISE_STATE_0007]- START_TMR_DELAY detected");
    $display("[INFO][TOP][TP_UT_ADVERTISE_STATE_0007]- Successful");
  endtask;

  task TP_UT_ADVERTISE_STATE_0008;
    $display("-----------------------------------------------------------------------------");
    $display("[INFO][TOP][TP_UT_ADVERTISE_STATE_0008]- Test Case TP_UT_ADVERTISE_STATE_0008");
    #100;
    give_strobe(advertise_event.SHUTDOWN);
    wait (tmr_events.stop_tmr_advertise);
    $display("[INFO][TOP][TP_UT_ADVERTISE_STATE_0008]- STOP_TMR_ADVERTISE detected");
    save_m_axis(dut_pkt);
    compare_pkts(ref_departing_pkt, dut_pkt, status);
    if (!status)
      $fatal("[INFO][TOP][TP_UT_ADVERTISE_STATE_0008] - FAILED");
    else
      $display("[INFO][TOP][TP_UT_ADVERTISE_STATE_0008]- Successful");
  endtask

  initial begin
    reset_dut();
    #50;
    $display("[INFO][TOP] : Assigning the memory map input");
    mmap_assignments();
    #10;
    $display("[INFO][TOP] : Generating the reference packets");
    generate_ref_packet(ref_available_pkt);
    generate_ref_packet(ref_departing_pkt);
    ref_departing_pkt[0][39:32] = 8'h01;
    TP_UT_ADVERTISE_STATE_0000();
    TP_UT_ADVERTISE_STATE_0001();
    TP_UT_ADVERTISE_STATE_0008();
    TP_UT_ADVERTISE_STATE_0002();
    TP_UT_ADVERTISE_STATE_0003();
    TP_UT_ADVERTISE_STATE_0004();
    TP_UT_ADVERTISE_STATE_0005();
    TP_UT_ADVERTISE_STATE_0006();
    TP_UT_ADVERTISE_STATE_0007();
    $finish;
  end

endmodule