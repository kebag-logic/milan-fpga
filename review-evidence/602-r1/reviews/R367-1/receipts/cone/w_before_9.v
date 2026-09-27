`default_nettype none
module KL_media_clock_restart (
	clk_i,
	rst_n,
	restart_p_i,
	clk_src_i,
	streaming_i,
	frame_p_i,
	frame_idx_i,
	frame_mr_i,
	mr_o
);
	parameter [31:0] N_TALKERS_P = 1;
	parameter [31:0] HOLD_PDU_P = 8;
	input wire clk_i;
	input wire rst_n;
	input wire restart_p_i;
	input wire [15:0] clk_src_i;
	input wire [N_TALKERS_P - 1:0] streaming_i;
	input wire frame_p_i;
	input wire [3:0] frame_idx_i;
	input wire frame_mr_i;
	output reg [N_TALKERS_P - 1:0] mr_o;
	generate
		if ((N_TALKERS_P < 1) || (N_TALKERS_P > 16)) begin : genblk1
			initial $display("Error [elaboration] $REVIEWS/602-r367-1-packet/scratch/tree/hdl/ieee1722/avtp/KL_media_clock_restart.sv:197:5 - KL_media_clock_restart.genblk1\n msg: ", "KL_media_clock_restart: N_TALKERS_P=%0d outside 1..16 (4-bit idx).", N_TALKERS_P);
		end
		if (HOLD_PDU_P < 8) begin : genblk2
			initial $display("Error [elaboration] $REVIEWS/602-r367-1-packet/scratch/tree/hdl/ieee1722/avtp/KL_media_clock_restart.sv:200:5 - KL_media_clock_restart.genblk2\n msg: ", "KL_media_clock_restart: HOLD_PDU_P=%0d below the 1722-2016 4.4.4.3 floor of 8.", HOLD_PDU_P);
		end
	endgenerate
	localparam [31:0] IXW_C = $clog2((N_TALKERS_P == 1 ? 2 : N_TALKERS_P));
	localparam [31:0] HOLDW_C = $clog2(HOLD_PDU_P + 1);
	reg [N_TALKERS_P - 1:0] tgt_r;
	reg [15:0] clk_src_q_r;
	wire src_change_w = clk_src_q_r != clk_src_i;
	reg [HOLDW_C - 1:0] hold_r [0:N_TALKERS_P - 1];
	function automatic [31:0] sv2v_cast_32;
		input reg [31:0] inp;
		sv2v_cast_32 = inp;
	endfunction
	wire idx_ok_w = sv2v_cast_32(frame_idx_i) < N_TALKERS_P;
	wire [IXW_C - 1:0] fidx_w = frame_idx_i[IXW_C - 1:0];
	function automatic [HOLDW_C - 1:0] sv2v_cast_06EC6;
		input reg [HOLDW_C - 1:0] inp;
		sv2v_cast_06EC6 = inp;
	endfunction
	always @(posedge clk_i) begin : mcr_track
		if (!rst_n) begin
			tgt_r <= 1'sb0;
			mr_o <= 1'sb0;
			clk_src_q_r <= 16'd0;
			begin : sv2v_autoblock_1
				reg signed [31:0] t;
				for (t = 0; t < N_TALKERS_P; t = t + 1)
					hold_r[t] <= sv2v_cast_06EC6(HOLD_PDU_P);
			end
		end
		else begin
			clk_src_q_r <= clk_src_i;
			if (restart_p_i | src_change_w)
				tgt_r <= ~mr_o;
			begin : sv2v_autoblock_2
				reg signed [31:0] t;
				for (t = 0; t < N_TALKERS_P; t = t + 1)
					if (((restart_p_i | src_change_w) && streaming_i[t]) && (hold_r[t] == {HOLDW_C {1'sb0}}))
						tgt_r[t] <= mr_o[t];
			end
			if (((frame_p_i && idx_ok_w) && (frame_mr_i == mr_o[fidx_w])) && (hold_r[fidx_w] != sv2v_cast_06EC6(HOLD_PDU_P)))
				hold_r[fidx_w] <= hold_r[fidx_w] + 1'b1;
			begin : sv2v_autoblock_3
				reg signed [31:0] t;
				for (t = 0; t < N_TALKERS_P; t = t + 1)
					if (!streaming_i[t]) begin
						mr_o[t] <= tgt_r[t];
						hold_r[t] <= sv2v_cast_06EC6(HOLD_PDU_P);
					end
					else if ((mr_o[t] != tgt_r[t]) && (hold_r[t] == sv2v_cast_06EC6(HOLD_PDU_P))) begin : g_adopt
						mr_o[t] <= tgt_r[t];
						hold_r[t] <= 1'sb0;
					end
			end
		end
	end
endmodule
`default_nettype wire
`default_nettype none
module cone_w (
	clk,
	rst_n,
	sel,
	lk_q,
	locked,
	mr_tog,
	adj,
	load,
	src,
	strm,
	fp,
	fidx,
	fmr,
	mr
);
	input wire clk;
	input wire rst_n;
	input wire sel;
	input wire lk_q;
	input wire locked;
	input wire mr_tog;
	input wire adj;
	input wire load;
	input wire [15:0] src;
	input wire [8:0] strm;
	input wire fp;
	input wire [3:0] fidx;
	input wire fmr;
	output wire [8:0] mr;
	wire rq = (sel & ((lk_q & ~locked) | mr_tog)) | (adj | load);
	KL_media_clock_restart #(.N_TALKERS_P(9)) u(
		.clk_i(clk),
		.rst_n(rst_n),
		.restart_p_i(rq),
		.clk_src_i(src),
		.streaming_i(strm),
		.frame_p_i(fp),
		.frame_idx_i(fidx),
		.frame_mr_i(fmr),
		.mr_o(mr)
	);
endmodule
