`default_nettype none
module cone_w (input wire clk, input wire rst_n, input wire sel, input wire lk_q,
  input wire locked, input wire mr_tog, input wire adj, input wire load,
  input wire [15:0] src, input wire [9-1:0] strm, input wire fp,
  input wire [3:0] fidx, input wire fmr, output logic [9-1:0] mr);
  wire rq = (sel & ((lk_q & ~locked) | mr_tog)) | (adj | load);
  KL_media_clock_restart #(.N_TALKERS_P(9)) u (.clk_i(clk), .rst_n(rst_n),
    .restart_p_i(rq), .clk_src_i(src), .streaming_i(strm), .frame_p_i(fp),
    .frame_idx_i(fidx), .frame_mr_i(fmr), .mr_o(mr));
endmodule
