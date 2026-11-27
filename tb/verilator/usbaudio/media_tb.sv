// SPDX-FileCopyrightText: 2026 Kebag Logic
// SPDX-License-Identifier: CERN-OHL-W-2.0
`timescale 1ns/1ps
module media_tb;
  logic clk=0;
  always #5 clk=!clk;
  logic rst_n=0,tick=0,state_valid=0,ack_ready=1,play_valid=0;
  logic [66:0] state_data=0;
  logic [287:0] play_data=0;
  logic [6:0] level=0;
  wire state_ready,ack_valid,play_ready,pair_valid,capture_tick,capture_valid,error_value;
  wire [31:0] ack_epoch,left_value,right_value,frame_ns,gaps,drops,frames;
  wire [3:0] pair_slot;
  wire [287:0] capture_data;
  logic [63:0] render_data=0;
  logic render_valid=0,render_last=0,render_tick=0,capture_ready=1;
  wire [1:0] running;
  wire [13:0] extremes;
  int score_frame=-1,pair_count=0,tick_count=0;
  KL_usbaudio_media dut (
    .clk_i(clk),.rst_n(rst_n),.media_tick_i(tick),.media_ns_i(32'd1234),
    .state_valid_i(state_valid),.state_ready_o(state_ready),.state_i(state_data),
    .ack_valid_o(ack_valid),.ack_ready_i(ack_ready),.ack_epoch_o(ack_epoch),
    .playback_valid_i(play_valid),.playback_ready_o(play_ready),.playback_i(play_data),
    .playback_level_i(level),.pair_valid_o(pair_valid),.pair_slot_o(pair_slot),
    .pair_l_o(left_value),.pair_r_o(right_value),.frame_ns_o(frame_ns),.capture_tick_o(capture_tick),
    .render_data_i(render_data),.render_valid_i(render_valid),.render_last_i(render_last),
    .render_stream_i(4'd0),.render_tick_i(render_tick),.capture_valid_o(capture_valid),
    .capture_ready_i(capture_ready),.capture_o(capture_data),.gaps_o(gaps),.drops_o(drops),
    .frames_o(frames),.running_o(running),.playback_extremes_o(extremes),.error_o(error_value)
  );
  function automatic logic [31:0] value(input int frame,input int channel);
    return 32'h12345678+32'(frame)*32'h01020305+32'(channel)*32'h87654321;
  endfunction
  function automatic logic [31:0] swap(input logic [31:0] sample_value);
    return {sample_value[7:0],sample_value[15:8],sample_value[23:16],sample_value[31:24]};
  endfunction
  task automatic check(input bit condition,input string name);
    if(!condition) $fatal(1,"CHECK %s",name);
  endtask
  task automatic step(input int n=1);
    repeat(n) begin @(posedge clk);#1;@(negedge clk);#1;end
  endtask
  always @(posedge clk) if(rst_n) begin
    if(pair_valid) begin
      check(pair_slot==pair_count%4,"MEDIA_CHANNEL_ORDER");
      check(left_value==(score_frame<0?0:value(score_frame,pair_count%4*2)),"MEDIA_PLAYBACK_BITS");
      check(right_value==(score_frame<0?0:value(score_frame,pair_count%4*2+1)),"MEDIA_PLAYBACK_BITS");
      check(frame_ns==1234,"MEDIA_FRAME_TIMESTAMP");pair_count++;
    end
    if(capture_tick) begin check(pair_count%4==0,"MEDIA_ATOMIC_PUBLICATION");tick_count++;end
  end
  task automatic apply(input int play_epoch,input int cap_epoch,input int flags=7);
    state_data={32'(cap_epoch),32'(play_epoch),3'(flags)};state_valid=1;#1;
    check(state_ready && ack_valid && ack_epoch==32'(cap_epoch),"MEDIA_ACK_STATE");
    step();state_valid=0;step(3);
  endtask
  task automatic playback(input int id,input int epoch_value,input int queued);
    play_data[287:256]=32'(epoch_value);
    for(int ch=0;ch<8;ch++) play_data[ch*32+:32]=value(id,ch);
    play_valid=1;level=7'(queued);step(3);
  endtask
  task automatic grid(input int expected_frame);
    score_frame=expected_frame;tick=1;step();tick=0;play_valid=0;step(10);
    check(pair_count==tick_count*4,"MEDIA_GRID_ONCE");
  endtask
  task automatic render(input int id,input int pairs=4);
    for(int p=0;p<pairs;p++) begin
      render_valid=1;render_last=p==3;
      render_data={swap(value(id,p*2+1)),swap(value(id,p*2))};step();
      render_valid=0;render_last=0;step();
    end
  endtask
  task automatic capture_check(input int id,input int epoch_value);
    render_tick=1;#1;
    check(capture_valid && capture_data[287:256]==32'(epoch_value),"MEDIA_CAPTURE_EPOCH");
    for(int ch=0;ch<8;ch++) check(capture_data[ch*32+:32]==value(id,ch),"MEDIA_CAPTURE_BITS");
    step();render_tick=0;step();
  endtask
  // Model the next epoch's FIFO head throughout a deferred transition.
  // Handshakes, exact samples and frame counts independently prove retention.
  task automatic deferred_playback(input int offset);
    int deferred_cycles=0,acknowledgements=0;
    bit applied;
    rst_n=0;step(3);rst_n=1;step(3);
    pair_count=0;tick_count=0;apply(1,1);playback(200+offset,1,12);
    score_frame=offset==0 ? -1 : 200+offset;
    for(int cycle=0;cycle<12;cycle++) begin
      tick=cycle==0;
      if(cycle==offset) begin
        state_data={32'd2,32'd2,3'd7};state_valid=1;
        play_data[287:256]=2;
        for(int ch=0;ch<8;ch++) play_data[ch*32+:32]=value(300+offset,ch);
        play_valid=1;level=11;
      end
      #1;
      applied=state_valid && state_ready;
      if(state_valid && !state_ready) begin
        deferred_cycles++;
        check(!ack_valid,"MEDIA_DEFERRED_ACK_AFTER_APPLY");
      end
      if(cycle>=offset)
        check(play_valid && !play_ready,"MEDIA_DEFERRED_FRAME_RETAINED");
      if(ack_valid && ack_ready) begin
        check(applied && ack_epoch==2,"MEDIA_DEFERRED_ACK_AFTER_APPLY");
        acknowledgements++;
      end
      step();
      if(applied) state_valid=0;
      if(cycle==0 && offset!=0) play_valid=0;
    end
    tick=0;
    check(deferred_cycles>0 && acknowledgements==1,"MEDIA_DEFERRED_WINDOW_EXERCISED");
    check(pair_count==4 && tick_count==1 && frames==1,"MEDIA_DEFERRED_OLD_FRAME_COMPLETE");
    // Eleven frames cannot prime the new epoch or consume its first frame.
    score_frame=-1;tick=1;#1;
    check(!play_ready,"MEDIA_DEFERRED_FRAME_RETAINED");
    step();tick=0;step(10);
    check(play_valid && !play_ready && !running[1],"MEDIA_DEFERRED_REPREFILL");
    level=12;step(3);score_frame=300+offset;tick=1;#1;
    check(play_ready,"MEDIA_DEFERRED_FRAME_RELEASED");
    step();tick=0;play_valid=0;step(10);
    check(pair_count==12 && tick_count==3 && frames==3,"MEDIA_DEFERRED_FRAME_PLAYED_ONCE");
    check(gaps==0 && !error_value,"MEDIA_DEFERRED_NO_GAP");
  endtask
  initial begin
    step(4);rst_n=1;step(4);
    ack_ready=0;state_data={32'd1,32'd1,3'd7};state_valid=1;step(4);
    check(!state_ready && running==0,"MEDIA_ACK_BACKPRESSURE");
    ack_ready=1;step();state_valid=0;step(4);
    playback(0,1,11);grid(-1);check(gaps==0,"MEDIA_PREFILL_NO_GAP");
    playback(0,1,12);grid(0);
    apply(1,2);playback(1,1,1);grid(1);
    check(gaps==0 && running[1],"MEDIA_CAPTURE_EPOCH_PRESERVES_PLAYBACK");
    apply(2,2);playback(99,1,12);check(play_ready,"MEDIA_STALE_EPOCH_DRAIN");grid(-1);
    playback(2,2,11);grid(-1);playback(2,2,12);grid(2);
    render(0);capture_check(0,2);
    // Change capture epoch at every boundary, including on every pair
    // edge and on completion. Old trailing beats must not become errors.
    for(int cut=0;cut<6;cut++) begin
      for(int p=0;p<4;p++) begin
        render_valid=1;render_last=p==3;
        render_data={swap(value(10+cut,p*2+1)),swap(value(10+cut,p*2))};
        if(p==cut) begin state_data={32'(3+cut),32'd2,3'd7};state_valid=1;end
        step();state_valid=0;render_valid=0;render_last=0;step();
      end
      if(cut>=4) begin
        state_data={32'(3+cut),32'd2,3'd7};state_valid=1;
        if(cut==5) begin step();state_valid=0;step();end
      end
      render_tick=1;#1;check(!capture_valid,"MEDIA_EPOCH_PARTIAL_HIDDEN");
      step();render_tick=0;state_valid=0;step();
      check(!error_value && drops==0,"MEDIA_EPOCH_TRAILING_BEATS_CLEAN");
      render(20+cut);capture_check(20+cut,3+cut);
    end
    render(1,2);render_tick=1;#1;check(!capture_valid,"MEDIA_PARTIAL_HIDDEN");
    step();render_tick=0;step();
    // A malformed frame requires a session boundary; verify the error count
    // before resetting, then exercise a clean full-frame overflow separately.
    check(drops==1 && error_value,"MEDIA_INCOMPLETE_COUNT");
    rst_n=0;step(2);rst_n=1;step(2);apply(2,7);pair_count=0;tick_count=0;
    playback(3,2,12);grid(3);
    render(3);capture_ready=0;capture_check(3,7);capture_ready=1;
    check(drops==1 && error_value,"MEDIA_OVERFLOW_FRAME_COUNT");
    render(4);capture_check(4,7);
    grid(-1);check(gaps==1,"MEDIA_UNDERFLOW_FRAME_COUNT");
    check(extremes[13:7]>=12 && frames==2,"MEDIA_DIAGNOSTICS");
    rst_n=0;step();check(!capture_valid && gaps==0 && drops==0 && !error_value,"MEDIA_RESET");
    // A state change can arrive on the grid, any pair, or the snapshot.
    // Count actual output pairs and snapshots; an aborted walk cannot pass.
    for(int offset=0;offset<8;offset++) begin
      rst_n=0;step(3);rst_n=1;step(3);
      pair_count=0;tick_count=0;apply(1,1);playback(50+offset,1,12);
      score_frame=offset==0 ? -1 : 50+offset;
      for(int cycle=0;cycle<12;cycle++) begin
        tick=cycle==0;
        if(cycle==offset) begin state_data={32'd1,32'd2,3'd7};state_valid=1;end
        #1;
        if(state_valid && state_ready) begin step();state_valid=0;end
        else step();
        if(cycle==0) play_valid=0;
      end
      tick=0;
      check(pair_count==4 && tick_count==1 && frames==1,"MEDIA_EVERY_GRID_SNAPSHOT");
      check(gaps==0 && !error_value,"MEDIA_TRANSITION_NO_GAP");
      check(!running[1],"MEDIA_TRANSITION_REPRIMES");
      playback(70+offset,2,11);grid(-1);
      playback(70+offset,2,12);grid(70+offset);
    end
    for(int offset=0;offset<7;offset++) deferred_playback(offset);
    $display("PASS media endpoint: prefill, atomic frames, independent epochs, acknowledgement, all bits and loss counts");
    $finish;
  end
endmodule
