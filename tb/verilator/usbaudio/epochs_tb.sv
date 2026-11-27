// SPDX-FileCopyrightText: 2026 Kebag Logic
// SPDX-License-Identifier: CERN-OHL-W-2.0
// Drive real socket records across drifting clocks through the epoch fence.
`timescale 1ns/1ps
module epochs_tb;
  logic bus_clk=0,media_clk=0,oscillator_clk=0,media_run=1,reset=1;
  always #10 bus_clk=!bus_clk;
  always #13 if(media_run) media_clk=!media_clk;
  always #20.345 oscillator_clk=!oscillator_clk;
  logic rx_valid=0,rx_accepted=0,status_ready=0,capture_ready=0;
  logic [15:0] rx_data=0;
  wire rx_ready,capture_valid,capture_last,capture_abort,status_valid,status_last,locked;
  wire [15:0] capture_data,status_data;
  logic tick=0,render_valid=0,render_last=0,render_tick=0;
  logic [63:0] render_data=0;
  wire pair_valid,mapper_tick;
  wire [3:0] pair_slot;
  wire [31:0] pair_l,pair_r,play_gaps,cap_drops;
  logic [15:0] incoming[$];
  logic [15:0] status_words[10];
  int bus_cycles=0,sequence_value=0,status_word=0,status_count=0,aborts=0;
  logic [31:0] latest_status=0,applied_epoch=0,published_epoch=32'hffffffff;
  int capture_words=0,packets=0,expected_capture=100,packet_words=0;
  int playback_pairs=0,playback_snapshots=0,expected_playback=-1;
  bit score_capture=0,score_playback=0;
  KL_usbaudio_bridge #(.WINDOW_LOG2_P(4)) dut (
    .bus_clk_i(bus_clk),.media_clk_i(media_clk),.oscillator_clk_i(oscillator_clk),
    .reset_i(reset),.media_locked_i(1'b1),.latency_qualified_i(1'b1),
    .rx_valid_i(rx_valid),.rx_ready_o(rx_ready),.rx_data_i(rx_data),
    .capture_valid_o(capture_valid),.capture_ready_i(capture_ready),.capture_data_o(capture_data),
    .capture_last_o(capture_last),.capture_abort_o(capture_abort),
    .status_valid_o(status_valid),.status_ready_i(status_ready),.status_data_o(status_data),
    .status_last_o(status_last),.media_tick_i(tick),.media_ns_i(32'd1234),
    .render_data_i(render_data),.render_valid_i(render_valid),.render_last_i(render_last),
    .render_stream_i(4'd0),.render_tick_i(render_tick),.pair_valid_o(pair_valid),
    .pair_slot_o(pair_slot),.pair_l_o(pair_l),.pair_r_o(pair_r),.frame_ns_o(),
    .capture_tick_o(mapper_tick),.locked_o(locked),.feedback_q16_o(),.error_o(),
    .playback_drops_o(),.playback_gaps_o(play_gaps),.capture_drops_o(cap_drops),
    .reference_losses_o(),.rejected_records_o(),.digest_errors_o(),.media_frames_o(),
    .playback_extremes_o(),.capture_extremes_o()
  );
  task automatic check(input bit condition,input string name);
    if(!condition) $fatal(1,"CHECK %s",name);
  endtask
  function automatic logic [31:0] sample_value(input int frame,input int channel);
    return (32'(frame)*32'h01020305) ^ (32'h89abcdef+32'(channel)*32'h31415927);
  endfunction
  function automatic logic [31:0] swap(input logic [31:0] value);
    return {value[7:0],value[15:8],value[23:16],value[31:24]};
  endfunction
  task automatic push32(input logic [31:0] value);
    incoming.push_back(value[15:0]);incoming.push_back(value[31:16]);
  endtask
  task automatic state_record(input int play_epoch,input int cap_epoch,
                             input int frames=0,input int first_frame=0);
    @(negedge bus_clk);#2;
    incoming.push_back(16'h554f);incoming.push_back(16'(frames*32));
    push32(32'(play_epoch));push32(32'(cap_epoch));
    incoming.push_back(7);incoming.push_back(16'h84ff);
    for(int f=0;f<frames;f++)
      for(int ch=0;ch<8;ch++) push32(sample_value(first_frame+f,ch));
  endtask
  task automatic bus_wait(input int cycles);
    repeat(cycles) begin @(negedge bus_clk);#2;end
  endtask
  task automatic media_wait(input int cycles=1);
    repeat(cycles) begin @(negedge media_clk);#2;end
  endtask
  // One producer serializes whole state/PCM/reference records. Reference
  // timing remains independent of the state and capture test sequence.
  always @(posedge bus_clk) if(!reset) begin
    rx_accepted=rx_valid && rx_ready;
    if(capture_abort) begin aborts++;capture_words=0;packet_words=0;end
    check(!dut.capture_packet.enabled_i || applied_epoch==dut.bus_capture_epoch_r,
          "BRIDGE_MEDIA_APPLIED_GATE");
    check(!dut.capture_packet.enabled_i || published_epoch==dut.bus_capture_epoch_r,
          "BRIDGE_PUBLISHED_ACK_GATE");
    if(status_valid && status_ready) begin
      status_words[status_word]=status_data;status_word++;
      check(status_last==(status_word==10),"BRIDGE_STATUS_LENGTH");
      if(status_last) begin
        latest_status={status_words[9],status_words[8]};
        // A new epoch cannot have been applied while its source clock was
        // stopped. Older immutable snapshots remain legal during a change.
        check(latest_status==0 || latest_status==applied_epoch ||
              latest_status==published_epoch,"BRIDGE_ACK_AFTER_MEDIA_APPLY");
        published_epoch=latest_status;status_count++;status_word=0;
      end
    end
    if(capture_valid && capture_ready && score_capture) begin
      logic [31:0] expected;
      expected=sample_value(expected_capture+capture_words/16,(capture_words%16)/2);
      check(capture_data==(capture_words%2==0?expected[15:0]:expected[31:16]),
            "BRIDGE_CAPTURE_CHANNEL_ZERO_RESTART");
      capture_words++;packet_words++;
      if(capture_last) begin
        check(packet_words>0 && packet_words<=112 && packet_words%16==0,
              "BRIDGE_CAPTURE_WHOLE_INTERVAL");
        packets++;packet_words=0;
      end
    end
  end
  always @(negedge bus_clk) if(!reset) begin
    if(rx_accepted) rx_valid=0;
    bus_cycles++;
    if(bus_cycles%50000==1000) begin
      logic [13:0] count_value;
      count_value=14'(sequence_value*8);sequence_value++;
      incoming.push_back(16'h5549);incoming.push_back(20);incoming.push_back(16'h0801);
      incoming.push_back({2'b00,count_value});push32(32'(sequence_value));push32({18'd0,count_value});
      incoming.push_back(sequence_value==1?1:0);incoming.push_back(16'h84ff);
    end
    if(!rx_valid && incoming.size()!=0) begin rx_data=incoming.pop_front();rx_valid=1;end
  end
  always @(posedge media_clk) if(!reset) begin
    if(dut.media_state_valid_w && dut.media_state_ready_w)
      applied_epoch=dut.media_state_w[66:35];
    if(pair_valid && score_playback) begin
      check(pair_slot==4'(playback_pairs%4),"BRIDGE_PLAYBACK_CHANNEL_ORDER");
      if(pair_l!=(expected_playback<0?0:sample_value(expected_playback,playback_pairs%4*2)))
        $display("playback frame=%0d pair=%0d actual=%h expected=%h",expected_playback,
                 playback_pairs,pair_l,sample_value(expected_playback,playback_pairs%4*2));
      check(pair_l==(expected_playback<0?0:sample_value(expected_playback,playback_pairs%4*2)) &&
            pair_r==(expected_playback<0?0:sample_value(expected_playback,playback_pairs%4*2+1)),
            "BRIDGE_INDEPENDENT_PLAYBACK_EPOCH");
      playback_pairs++;
    end
    if(mapper_tick && score_playback) playback_snapshots++;
  end
  task automatic grid(input int expected_frame);
    media_wait();expected_playback=expected_frame;playback_pairs=0;playback_snapshots=0;
    score_playback=1;tick=1;media_wait();tick=0;media_wait(10);score_playback=0;
    check(playback_pairs==4 && playback_snapshots==1,"BRIDGE_GRID_SNAPSHOT");
  endtask
  task automatic render_pairs(input int frame,input int first_pair=0,input int pair_limit=4);
    for(int pair_index=first_pair;pair_index<pair_limit;pair_index++) begin
      media_wait();render_valid=1;render_last=pair_index==3;
      render_data={swap(sample_value(frame,pair_index*2+1)),swap(sample_value(frame,pair_index*2))};
      media_wait();render_valid=0;render_last=0;
    end
  endtask
  task automatic close_render;
    media_wait();render_tick=1;media_wait();render_tick=0;
  endtask
  task automatic render_frames(input int first_frame,input int frames=24);
    for(int frame=first_frame;frame<first_frame+frames;frame++) begin
      render_pairs(frame);close_render();
    end
  endtask
  task automatic await_status(input logic [31:0] epoch_value);
    for(int wait_count=0;wait_count<60000;wait_count++) begin
      if(latest_status==epoch_value) return;
      bus_wait(1);
    end
    check(0,"BRIDGE_STATUS_TIMEOUT");
  endtask
  initial begin : campaign
    int before_abort,before_packets;
    logic [15:0] held_word;
    bus_wait(10);reset=0;
    // Keep the initial status uncommitted, so its sentinel matches the
    // first selected capture epoch. The applied gate must work independently.
    bus_wait(260000);check(locked,"BRIDGE_REFERENCE_QUALIFIED");
    media_wait();media_run=0;
    state_record(1,-1);bus_wait(100);
    check(dut.bus_capture_epoch_r==32'hffffffff && applied_epoch==0,
          "BRIDGE_UNAPPLIED_STATE_REACHED");
    check(aborts==1,"BRIDGE_CAPTURE_ABORT");
    status_ready=1;bus_wait(30000);
    check(latest_status==0 && status_count>0,"BRIDGE_ACK_AFTER_MEDIA_APPLY");
    media_run=1;await_status(32'hffffffff);
    state_record(1,-1,6,0);state_record(1,-1,6,6);state_record(1,-1,6,12);bus_wait(700);grid(0);
    render_frames(100);score_capture=1;capture_ready=1;
    wait(capture_words==3);@(negedge bus_clk);#2;capture_ready=0;held_word=capture_data;
    bus_wait(8);check(capture_data==held_word,"BRIDGE_ORDINARY_STALL_RETAINS_WORD");
    // Change capture only while both a bus interval and a render frame
    // are partial. The old render tail must be drained, never republished.
    render_pairs(200,0,2);before_abort=aborts;status_ready=0;
    state_record(1,0);bus_wait(100);
    check(aborts==before_abort+1 && capture_words==0,"BRIDGE_CAPTURE_ABORT");
    check(applied_epoch==0,"BRIDGE_CAPTURE_STATE_APPLIED");
    render_pairs(200,2,4);close_render();
    grid(1);check(play_gaps==0 && cap_drops==0,"BRIDGE_CAPTURE_ONLY_PRESERVES_PLAYBACK");
    render_frames(250,16);bus_wait(10000);
    check(!capture_valid,"BRIDGE_DATA_WAITS_FOR_STATUS");
    status_ready=1;await_status(0);bus_wait(50);
    expected_capture=300;render_frames(300);capture_ready=1;
    wait(capture_words==3);@(negedge bus_clk);#2;capture_ready=0;held_word=capture_data;
    // A playback-only transition must preserve this exact partial capture
    // word and every following channel, while reprime applies to playback.
    before_abort=aborts;before_packets=packets;
    state_record(2,0);bus_wait(100);
    check(aborts==before_abort && capture_data==held_word,"BRIDGE_PLAYBACK_ONLY_PRESERVES_CAPTURE");
    grid(-1);state_record(2,0,6,1000);state_record(2,0,6,1006);
    state_record(2,0,6,1012);bus_wait(700);grid(1000);
    capture_ready=1;wait(packets>before_packets);bus_wait(10);
    check(capture_words>=112 && play_gaps==0 && cap_drops==0,"BRIDGE_EPOCH_RECOVERY_CLEAN");
    $display("PASS bridge epochs: partial interval abandonment, channel-zero restart, applied and published acknowledgement gates, independent direction changes");
    $finish;
  end
  initial begin #20000000;$fatal(1,"CHECK BRIDGE_CAMPAIGN_TIMEOUT");end
endmodule
