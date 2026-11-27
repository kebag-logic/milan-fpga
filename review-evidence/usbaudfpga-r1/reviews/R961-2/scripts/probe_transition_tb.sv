// Reviewer probe: a playback epoch change deferred by an active pair walk,
// with the new epoch's first frame already at the playback FIFO head.
// Ordering oracle: while the state change is deferred, (1) no playback
// frame may be consumed and (2) no acknowledgement may be issued; after
// the change applies, the held new-epoch frame must still be there.
`timescale 1ns/1ps
module probe_transition_tb;
  logic clk=0; always #5 clk=!clk;
  logic rst_n=0,tick=0,state_valid=0,ack_ready=1,play_valid=0;
  logic [66:0] state_data=0; logic [287:0] play_data=0; logic [6:0] level=0;
  wire state_ready,ack_valid,play_ready,pair_valid,capture_tick,capture_valid,error_value;
  wire [31:0] ack_epoch,left_value,right_value,frame_ns,gaps,drops,frames;
  wire [3:0] pair_slot; wire [287:0] capture_data; wire [1:0] running; wire [13:0] extremes;
  int consumed_while_deferred=0, acked_while_deferred=0, deferred_cycles=0, new_frames_consumed=0;
  KL_usbaudio_media dut (
    .clk_i(clk),.rst_n(rst_n),.media_tick_i(tick),.media_ns_i(32'd1),
    .state_valid_i(state_valid),.state_ready_o(state_ready),.state_i(state_data),
    .ack_valid_o(ack_valid),.ack_ready_i(ack_ready),.ack_epoch_o(ack_epoch),
    .playback_valid_i(play_valid),.playback_ready_o(play_ready),.playback_i(play_data),
    .playback_level_i(level),.pair_valid_o(pair_valid),.pair_slot_o(pair_slot),
    .pair_l_o(left_value),.pair_r_o(right_value),.frame_ns_o(frame_ns),.capture_tick_o(capture_tick),
    .render_data_i(64'd0),.render_valid_i(1'b0),.render_last_i(1'b0),
    .render_stream_i(4'd0),.render_tick_i(1'b0),.capture_valid_o(capture_valid),
    .capture_ready_i(1'b1),.capture_o(capture_data),.gaps_o(gaps),.drops_o(drops),
    .frames_o(frames),.running_o(running),.playback_extremes_o(extremes),.error_o(error_value));
  task automatic step(input int n=1); repeat(n) begin @(posedge clk);#1; end endtask
  always @(posedge clk) if(rst_n) begin
    if(state_valid && !state_ready) begin
      deferred_cycles++;
      if(play_valid && play_ready) consumed_while_deferred++;
      if(ack_valid && ack_ready) acked_while_deferred++;
    end
    if(play_valid && play_ready && play_data[287:256]==2) new_frames_consumed++;
  end
  initial begin
    step(3); rst_n=1; step(3);
    // playback epoch 1 running and primed
    state_data={32'd1,32'd1,3'd7}; state_valid=1; step(); state_valid=0; step(3);
    play_data[287:256]=1; play_valid=1; level=12; step(3);
    tick=1; step(); tick=0; play_valid=0; step(10);
    // start the next grid walk, then while it walks present the new state
    // together with the new epoch's first frame at the FIFO head
    play_data[287:256]=1; play_valid=1; level=12;
    tick=1; step(); tick=0;
    play_data[287:256]=2; play_valid=1; level=1;
    state_data={32'd2,32'd2,3'd7}; state_valid=1; #1;
    for(int c=0;c<20 && !(state_valid && state_ready);c++) begin step(); #1; end
    step(); state_valid=0;
    // the held frame must be the new epoch's first and still unconsumed now
    if(new_frames_consumed!=0) $fatal(1,"CHECK PROBE_NEW_EPOCH_FRAME_LOST");
    step(5);
    $display("deferred_cycles=%0d consumed_while_deferred=%0d acked_while_deferred=%0d new_frame_still_present_after_apply=%0d",
             deferred_cycles, consumed_while_deferred, acked_while_deferred, new_frames_consumed==0);
    if(deferred_cycles==0) $fatal(1,"CHECK PROBE_NOT_DEFERRED");
    if(consumed_while_deferred!=0) $fatal(1,"CHECK PROBE_FRAME_CONSUMED_WHILE_DEFERRED");
    if(acked_while_deferred!=0) $fatal(1,"CHECK PROBE_ACK_WHILE_DEFERRED");
    $display("PASS probe transition ordering");
    $finish;
  end
endmodule
