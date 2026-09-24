`default_nettype none
module cdc_pulse (
	src_clk,
	src_rst_n,
	src_pulse,
	dest_clk,
	dest_rst_n,
	dest_pulse
);
	parameter signed [31:0] DEST_SYNC_FF = 2;
	input wire src_clk;
	input wire src_rst_n;
	input wire src_pulse;
	input wire dest_clk;
	input wire dest_rst_n;
	output wire dest_pulse;
	reg src_level;
	always @(posedge src_clk)
		if (!src_rst_n)
			src_level <= 1'b0;
		else if (src_pulse)
			src_level <= ~src_level;
	(* ASYNC_REG = "TRUE" *) reg [DEST_SYNC_FF:0] sync;
	always @(posedge dest_clk)
		if (!dest_rst_n)
			sync <= 1'sb0;
		else
			sync <= {sync[DEST_SYNC_FF - 1:0], src_level};
	assign dest_pulse = sync[DEST_SYNC_FF] ^ sync[DEST_SYNC_FF - 1];
endmodule
`default_nettype wire
`default_nettype none
module cdc_handshake (
	src_clk,
	src_rst_n,
	src_in,
	src_send,
	src_rcv,
	dest_clk,
	dest_rst_n,
	dest_out,
	dest_req
);
	parameter signed [31:0] WIDTH = 64;
	parameter signed [31:0] DEST_SYNC_FF = 2;
	parameter signed [31:0] SRC_SYNC_FF = 2;
	input wire src_clk;
	input wire src_rst_n;
	input wire [WIDTH - 1:0] src_in;
	input wire src_send;
	output wire src_rcv;
	input wire dest_clk;
	input wire dest_rst_n;
	output wire [WIDTH - 1:0] dest_out;
	output wire dest_req;
	reg src_send_d;
	reg req_tog;
	reg [WIDTH - 1:0] data_hold;
	(* ASYNC_REG = "TRUE" *) reg [SRC_SYNC_FF:0] ack_sync;
	(* ASYNC_REG = "TRUE" *) reg [DEST_SYNC_FF:0] req_sync;
	reg [WIDTH - 1:0] dest_out_r;
	reg dest_req_r;
	reg ack_tog;
	always @(posedge src_clk)
		if (!src_rst_n) begin
			src_send_d <= 1'b0;
			req_tog <= 1'b0;
			data_hold <= 1'sb0;
		end
		else begin
			src_send_d <= src_send;
			if (src_send && !src_send_d) begin
				data_hold <= src_in;
				req_tog <= ~req_tog;
			end
		end
	always @(posedge src_clk)
		if (!src_rst_n)
			ack_sync <= 1'sb0;
		else
			ack_sync <= {ack_sync[SRC_SYNC_FF - 1:0], ack_tog};
	assign src_rcv = ack_sync[SRC_SYNC_FF] ^ ack_sync[SRC_SYNC_FF - 1];
	always @(posedge dest_clk)
		if (!dest_rst_n)
			req_sync <= 1'sb0;
		else
			req_sync <= {req_sync[DEST_SYNC_FF - 1:0], req_tog};
	wire req_edge = req_sync[DEST_SYNC_FF] ^ req_sync[DEST_SYNC_FF - 1];
	always @(posedge dest_clk)
		if (!dest_rst_n) begin
			dest_out_r <= 1'sb0;
			dest_req_r <= 1'b0;
			ack_tog <= 1'b0;
		end
		else begin
			dest_req_r <= req_edge;
			if (req_edge) begin
				dest_out_r <= data_hold;
				ack_tog <= ~ack_tog;
			end
		end
	assign dest_out = dest_out_r;
	assign dest_req = dest_req_r;
endmodule
`default_nettype wire
`default_nettype none
module KL_mmcm_drp_servo (
	clk_i,
	rst_n,
	clk_audio_i,
	ps_clk_i,
	ptp_now_i,
	clk_src_i,
	crf_src_idx_i,
	crf_locked_i,
	crf_rate_i,
	auto_repair_i,
	ps_invert_i,
	drp_addr_o,
	drp_en_o,
	drp_we_o,
	drp_di_o,
	drp_do_i,
	drp_rdy_i,
	mmcm_rst_o,
	mmcm_locked_i,
	ps_en_o,
	ps_incdec_o,
	ps_done_i,
	status_o
);
	parameter [31:0] CLK_FREQ_HZ_P = 50000000;
	parameter [31:0] TICK_CYC_P = 24576;
	parameter [31:0] WIN_LOG2_P = 9;
	parameter [63:0] NOM_WIN_NS_P = 64'd512000000;
	parameter [31:0] NORM_SHIFT_P = 0;
	parameter [31:0] KI_SHIFT_P = 1;
	parameter [31:0] KP_SHIFT_P = 2;
	parameter signed [31:0] U_MAX_P = 102400;
	parameter signed [31:0] SLEW_MAX_P = 51200;
	parameter signed [31:0] LOCK_THR_P = 1024;
	parameter [31:0] LOCK_WIN_P = 4;
	parameter [31:0] GAIN_NUM_P = 59;
	parameter [31:0] PS_TOUT_CYC_P = 255;
	parameter [31:0] RELOCK_TOUT_P = 131072;
	parameter [15:0] CFG_C0R1_P = 16'h0595;
	parameter [15:0] CFG_C0R1_MASK_P = 16'hefff;
	parameter [15:0] CFG_C0R2_P = 16'h0080;
	parameter [15:0] CFG_C0R2_MASK_P = 16'h7fff;
	input wire clk_i;
	input wire rst_n;
	input wire clk_audio_i;
	input wire ps_clk_i;
	input wire [63:0] ptp_now_i;
	input wire [15:0] clk_src_i;
	input wire [15:0] crf_src_idx_i;
	input wire crf_locked_i;
	input wire signed [31:0] crf_rate_i;
	input wire auto_repair_i;
	input wire ps_invert_i;
	output reg [6:0] drp_addr_o;
	output reg drp_en_o;
	output reg drp_we_o;
	output reg [15:0] drp_di_o;
	input wire [15:0] drp_do_i;
	input wire drp_rdy_i;
	output reg mmcm_rst_o;
	input wire mmcm_locked_i;
	output reg ps_en_o;
	output reg ps_incdec_o;
	input wire ps_done_i;
	output wire [31:0] status_o;
	localparam [6:0] DADDR_C0R1_C = 7'h08;
	localparam [6:0] DADDR_C0R2_C = 7'h09;
	localparam [6:0] DADDR_POWER_C = 7'h28;
	localparam [15:0] POWER_ALL_C = 16'hffff;
	localparam [31:0] WIN_TICKS_C = 1 << WIN_LOG2_P;
	localparam signed [31:0] ECLAMP_C = 32'sd1 << 20;
	localparam signed [31:0] GUARD_THR_C = 32'sd1 << 19;
	localparam [31:0] DISC_MAX_C = 4;
	reg [1:0] arst_sync_r;
	wire arst_n_w = arst_sync_r[1];
	always @(posedge clk_audio_i) begin : audio_rst_sync
		arst_sync_r <= {arst_sync_r[0], rst_n};
	end
	reg [$clog2(TICK_CYC_P) - 1:0] tick_div_r;
	reg tick_a_r;
	function automatic [$clog2(TICK_CYC_P) - 1:0] sv2v_cast_66F09;
		input reg [$clog2(TICK_CYC_P) - 1:0] inp;
		sv2v_cast_66F09 = inp;
	endfunction
	always @(posedge clk_audio_i) begin : tick_div
		if (!arst_n_w) begin
			tick_div_r <= 1'sb0;
			tick_a_r <= 1'b0;
		end
		else if (tick_div_r == sv2v_cast_66F09(TICK_CYC_P - 1)) begin
			tick_div_r <= 1'sb0;
			tick_a_r <= 1'b1;
		end
		else begin
			tick_div_r <= tick_div_r + 1'b1;
			tick_a_r <= 1'b0;
		end
	end
	wire tick_p_w;
	cdc_pulse u_tick_cdc(
		.src_clk(clk_audio_i),
		.src_rst_n(arst_n_w),
		.src_pulse(tick_a_r),
		.dest_clk(clk_i),
		.dest_rst_n(rst_n),
		.dest_pulse(tick_p_w)
	);
	(* ASYNC_REG = "TRUE" *) reg [1:0] locked_sync_r;
	(* ASYNC_REG = "TRUE" *) reg [1:0] psbusy_sync_r;
	(* ASYNC_REG = "TRUE" *) reg [1:0] psfault_sync_r;
	reg ps_busy_ps_r;
	reg ps_fault_ps_r;
	always @(posedge clk_i) begin : in_syncs
		if (!rst_n) begin
			locked_sync_r <= 1'sb0;
			psbusy_sync_r <= 1'sb0;
			psfault_sync_r <= 1'sb0;
		end
		else begin
			locked_sync_r <= {locked_sync_r[0], mmcm_locked_i};
			psbusy_sync_r <= {psbusy_sync_r[0], ps_busy_ps_r};
			psfault_sync_r <= {psfault_sync_r[0], ps_fault_ps_r};
		end
	end
	wire mmcm_locked_s_w = locked_sync_r[1];
	wire ps_busy_s_w = psbusy_sync_r[1];
	wire ps_fault_s_w = psfault_sync_r[1];
	reg [2:0] state_r;
	reg [3:0] dstate_r;
	wire servo_sel_w = clk_src_i == crf_src_idx_i;
	reg [WIN_LOG2_P:0] tick_cnt_r;
	reg [63:0] win_start_r;
	reg win_valid_r;
	reg [1:0] win_skip_r;
	reg signed [31:0] ew_r;
	reg [1:0] disc_run_r;
	reg [5:0] disc_cnt_r;
	reg signed [23:0] integ_r;
	reg signed [23:0] u_cmd_r;
	reg [$clog2(LOCK_WIN_P + 1) - 1:0] lock_cnt_r;
	reg [2:0] pp_seq_r;
	reg pp_run_r;
	reg signed [63:0] pp_d_r;
	reg signed [63:0] pp_spann_r;
	reg signed [31:0] pp_locerr_r;
	reg signed [31:0] pp_rate_r;
	reg signed [31:0] pp_isum_r;
	reg pp_thr_r;
	reg signed [23:0] pp_ig_r;
	reg signed [31:0] pp_un_r;
	reg signed [23:0] pp_ut_r;
	reg signed [31:0] pp_du_r;
	reg signed [31:0] u_gain_r;
	reg signed [31:0] acc_r;
	reg hs_send_r;
	reg [14:0] hs_data_r;
	wire hs_rcv_w;
	reg ps_hold_r;
	reg drp_pass_r;
	reg rd_second_r;
	reg repairing_r;
	reg [15:0] rd_val_r;
	reg verified_r;
	reg mismatch_r;
	reg drp_fault_r;
	reg [$clog2(RELOCK_TOUT_P + 1) - 1:0] relock_r;
	reg [3:0] rst_settle_r;
	wire [15:0] exp_val_w = (rd_second_r ? CFG_C0R2_P : CFG_C0R1_P);
	wire [15:0] exp_mask_w = (rd_second_r ? CFG_C0R2_MASK_P : CFG_C0R1_MASK_P);
	reg [63:0] ptp_q_r;
	always @(posedge clk_i) begin : ptp_stage_S
		ptp_q_r <= ptp_now_i;
	end
	function automatic signed [23:0] sv2v_cast_24_signed;
		input reg signed [23:0] inp;
		sv2v_cast_24_signed = inp;
	endfunction
	function automatic signed [23:0] clamp_u;
		input reg signed [31:0] v;
		if (v > U_MAX_P)
			clamp_u = sv2v_cast_24_signed(U_MAX_P);
		else if (v < -U_MAX_P)
			clamp_u = sv2v_cast_24_signed(-U_MAX_P);
		else
			clamp_u = sv2v_cast_24_signed(v);
	endfunction
	function automatic signed [31:0] sv2v_cast_32_signed;
		input reg signed [31:0] inp;
		sv2v_cast_32_signed = inp;
	endfunction
	function automatic [$clog2(LOCK_WIN_P + 1) - 1:0] sv2v_cast_CAE88;
		input reg [$clog2(LOCK_WIN_P + 1) - 1:0] inp;
		sv2v_cast_CAE88 = inp;
	endfunction
	function automatic [((WIN_LOG2_P + 0) >= 0 ? WIN_LOG2_P + 1 : 1 - (WIN_LOG2_P + 0)) - 1:0] sv2v_cast_22A9D;
		input reg [((WIN_LOG2_P + 0) >= 0 ? WIN_LOG2_P + 1 : 1 - (WIN_LOG2_P + 0)) - 1:0] inp;
		sv2v_cast_22A9D = inp;
	endfunction
	function automatic signed [63:0] sv2v_cast_64_signed;
		input reg signed [63:0] inp;
		sv2v_cast_64_signed = inp;
	endfunction
	function automatic [1:0] sv2v_cast_2;
		input reg [1:0] inp;
		sv2v_cast_2 = inp;
	endfunction
	function automatic signed [13:0] sv2v_cast_14_signed;
		input reg signed [13:0] inp;
		sv2v_cast_14_signed = inp;
	endfunction
	function automatic [$clog2(RELOCK_TOUT_P + 1) - 1:0] sv2v_cast_89450;
		input reg [$clog2(RELOCK_TOUT_P + 1) - 1:0] inp;
		sv2v_cast_89450 = inp;
	endfunction
	always @(posedge clk_i) begin : servo_engine
		if (!rst_n) begin
			state_r <= 3'd0;
			dstate_r <= 4'd0;
			tick_cnt_r <= 1'sb0;
			win_start_r <= 1'sb0;
			win_valid_r <= 1'b0;
			win_skip_r <= 1'sb0;
			disc_run_r <= 1'sb0;
			disc_cnt_r <= 1'sb0;
			ew_r <= 1'sb0;
			integ_r <= 1'sb0;
			u_cmd_r <= 1'sb0;
			lock_cnt_r <= 1'sb0;
			acc_r <= 1'sb0;
			hs_send_r <= 1'b0;
			hs_data_r <= 1'sb0;
			ps_hold_r <= 1'b0;
			drp_addr_o <= 1'sb0;
			drp_en_o <= 1'b0;
			drp_we_o <= 1'b0;
			drp_di_o <= 1'sb0;
			mmcm_rst_o <= 1'b0;
			drp_pass_r <= 1'b0;
			rd_second_r <= 1'b0;
			repairing_r <= 1'b0;
			rd_val_r <= 1'sb0;
			verified_r <= 1'b0;
			mismatch_r <= 1'b0;
			drp_fault_r <= 1'b0;
			relock_r <= 1'sb0;
			rst_settle_r <= 1'sb0;
			pp_seq_r <= 1'sb0;
			pp_run_r <= 1'b0;
			pp_d_r <= 1'sb0;
			pp_spann_r <= 1'sb0;
			pp_locerr_r <= 1'sb0;
			pp_rate_r <= 1'sb0;
			pp_isum_r <= 1'sb0;
			pp_thr_r <= 1'b0;
			pp_ig_r <= 1'sb0;
			pp_un_r <= 1'sb0;
			pp_ut_r <= 1'sb0;
			pp_du_r <= 1'sb0;
			u_gain_r <= 1'sb0;
		end
		else begin
			drp_en_o <= 1'b0;
			drp_we_o <= 1'b0;
			if (hs_send_r && hs_rcv_w)
				hs_send_r <= 1'b0;
			u_gain_r <= sv2v_cast_32_signed(u_cmd_r) * GAIN_NUM_P;
			(* full_case, parallel_case *)
			case (state_r)
				3'd0: begin
					u_cmd_r <= 1'sb0;
					integ_r <= 1'sb0;
					acc_r <= 1'sb0;
					win_valid_r <= 1'b0;
					lock_cnt_r <= 1'sb0;
					disc_run_r <= 1'sb0;
					disc_cnt_r <= 1'sb0;
					verified_r <= 1'b0;
					mismatch_r <= 1'b0;
					drp_fault_r <= 1'b0;
					mmcm_rst_o <= 1'b0;
					ps_hold_r <= 1'b0;
					if (servo_sel_w && crf_locked_i) begin
						state_r <= 3'd1;
						dstate_r <= 4'd1;
						rd_second_r <= 1'b0;
						drp_pass_r <= 1'b1;
						repairing_r <= 1'b0;
					end
				end
				3'd1, 3'd2:
					if (!servo_sel_w) begin
						mmcm_rst_o <= 1'b0;
						dstate_r <= 4'd0;
						state_r <= 3'd0;
					end
				3'd3, 3'd4:
					if (!servo_sel_w)
						state_r <= 3'd0;
					else if (!crf_locked_i)
						state_r <= 3'd5;
					else if ((state_r == 3'd3) && (lock_cnt_r >= sv2v_cast_CAE88(LOCK_WIN_P)))
						state_r <= 3'd4;
					else if ((state_r == 3'd4) && (lock_cnt_r == {$clog2(LOCK_WIN_P + 1) {1'sb0}}))
						state_r <= 3'd3;
				3'd5:
					if (!servo_sel_w)
						state_r <= 3'd0;
					else if (crf_locked_i) begin
						state_r <= 3'd3;
						win_skip_r <= 2'd2;
						lock_cnt_r <= 1'sb0;
					end
				3'd6: begin
					mmcm_rst_o <= 1'b0;
					if (!servo_sel_w)
						state_r <= 3'd0;
				end
				default: state_r <= 3'd0;
			endcase
			if (|{state_r == 3'd3, state_r == 3'd4, state_r == 3'd5}) begin
				if (tick_p_w) begin
					if (!win_valid_r) begin
						win_start_r <= ptp_q_r;
						win_valid_r <= 1'b1;
						tick_cnt_r <= 1'sb0;
					end
					else if (tick_cnt_r == sv2v_cast_22A9D(WIN_TICKS_C - 1)) begin
						tick_cnt_r <= 1'sb0;
						win_start_r <= ptp_q_r;
						pp_d_r <= $signed(ptp_q_r - win_start_r);
						pp_rate_r <= crf_rate_i;
						pp_run_r <= (win_skip_r == {2 {1'sb0}}) && (state_r != 3'd5);
						pp_seq_r <= 3'd1;
						if (win_skip_r != {2 {1'sb0}})
							win_skip_r <= win_skip_r - 2'd1;
					end
					else
						tick_cnt_r <= tick_cnt_r + 1'b1;
				end
				(* full_case, parallel_case *)
				case (pp_seq_r)
					3'd0:
						;
					3'd1: begin : pi_norm_S
						pp_spann_r <= (pp_d_r - $signed(NOM_WIN_NS_P)) <<< NORM_SHIFT_P;
						pp_seq_r <= 3'd2;
					end
					3'd2: begin : pi_eclamp_S
						pp_locerr_r <= (pp_spann_r > sv2v_cast_64_signed(ECLAMP_C) ? ECLAMP_C : (pp_spann_r < -sv2v_cast_64_signed(ECLAMP_C) ? -ECLAMP_C : sv2v_cast_32_signed(pp_spann_r)));
						pp_seq_r <= 3'd3;
					end
					3'd3: begin : pi_err_S
						ew_r <= pp_locerr_r - pp_rate_r;
						pp_seq_r <= 3'd4;
					end
					3'd4: begin : pi_isum_S
						pp_isum_r <= sv2v_cast_32_signed(integ_r) + (ew_r >>> KI_SHIFT_P);
						pp_thr_r <= (ew_r < LOCK_THR_P) && (ew_r > -LOCK_THR_P);
						if (pp_run_r && ((ew_r > GUARD_THR_C) || (ew_r < -GUARD_THR_C))) begin
							pp_run_r <= 1'b0;
							if (disc_cnt_r != 6'h3f)
								disc_cnt_r <= disc_cnt_r + 6'd1;
							if (disc_run_r == sv2v_cast_2(3)) begin
								win_valid_r <= 1'b0;
								disc_run_r <= 1'sb0;
							end
							else
								disc_run_r <= disc_run_r + 2'd1;
						end
						pp_seq_r <= 3'd5;
					end
					3'd5: begin : pi_pterm_S
						pp_ig_r <= clamp_u(pp_isum_r);
						pp_un_r <= sv2v_cast_32_signed(clamp_u(pp_isum_r)) + (ew_r >>> KP_SHIFT_P);
						pp_seq_r <= 3'd6;
					end
					3'd6: begin : pi_uclamp_S
						pp_ut_r <= clamp_u(pp_un_r);
						pp_du_r <= sv2v_cast_32_signed(clamp_u(pp_un_r)) - sv2v_cast_32_signed(u_cmd_r);
						pp_seq_r <= 3'd7;
					end
					3'd7: begin : pi_wb_S
						if (pp_run_r) begin
							disc_run_r <= 1'sb0;
							if (pp_du_r > SLEW_MAX_P)
								u_cmd_r <= u_cmd_r + sv2v_cast_24_signed(SLEW_MAX_P);
							else if (pp_du_r < -SLEW_MAX_P)
								u_cmd_r <= u_cmd_r - sv2v_cast_24_signed(SLEW_MAX_P);
							else
								u_cmd_r <= pp_ut_r;
							integ_r <= pp_ig_r;
							if (pp_thr_r) begin
								if (lock_cnt_r != sv2v_cast_CAE88(LOCK_WIN_P))
									lock_cnt_r <= lock_cnt_r + 1'b1;
							end
							else
								lock_cnt_r <= 1'sb0;
						end
						pp_seq_r <= 1'sb0;
					end
					default: pp_seq_r <= 1'sb0;
				endcase
				begin : dispatch
					reg signed [31:0] a_v;
					reg signed [31:0] b_v;
					a_v = acc_r;
					if (tick_p_w && !ps_hold_r)
						a_v = a_v + u_gain_r;
					if ((!hs_send_r && !ps_busy_s_w) && !ps_hold_r) begin
						b_v = acc_r >>> 9;
						if (b_v > 32'sd16383)
							b_v = 32'sd16383;
						if (b_v < -32'sd16383)
							b_v = -32'sd16383;
						if (b_v != 0) begin
							hs_data_r <= (b_v > 0 ? {ps_invert_i, sv2v_cast_14_signed(b_v)} : {~ps_invert_i, sv2v_cast_14_signed(-b_v)});
							hs_send_r <= 1'b1;
							a_v = a_v - (b_v <<< 9);
						end
					end
					acc_r <= a_v;
				end
			end
			else
				pp_seq_r <= 1'sb0;
			(* full_case, parallel_case *)
			case (dstate_r)
				4'd0:
					;
				4'd1: begin
					drp_addr_o <= (rd_second_r ? DADDR_C0R2_C : DADDR_C0R1_C);
					drp_en_o <= 1'b1;
					dstate_r <= 4'd2;
				end
				4'd2:
					if (drp_rdy_i) begin
						rd_val_r <= drp_do_i;
						if ((drp_do_i & exp_mask_w) != (exp_val_w & exp_mask_w))
							drp_pass_r <= 1'b0;
						if (repairing_r)
							dstate_r <= 4'd3;
						else if (!rd_second_r) begin
							rd_second_r <= 1'b1;
							dstate_r <= 4'd1;
						end
						else if (drp_pass_r && ((drp_do_i & exp_mask_w) == (exp_val_w & exp_mask_w))) begin
							verified_r <= 1'b1;
							dstate_r <= 4'd0;
							state_r <= 3'd3;
							win_valid_r <= 1'b0;
							win_skip_r <= 2'd1;
						end
						else begin
							mismatch_r <= 1'b1;
							if (auto_repair_i) begin
								state_r <= 3'd2;
								ps_hold_r <= 1'b1;
								dstate_r <= 4'd5;
							end
							else begin
								dstate_r <= 4'd0;
								state_r <= 3'd3;
								win_valid_r <= 1'b0;
								win_skip_r <= 2'd1;
							end
						end
					end
				4'd5:
					if (!ps_busy_s_w && !hs_send_r) begin
						mmcm_rst_o <= 1'b1;
						rst_settle_r <= 4'd15;
						dstate_r <= 4'd6;
					end
				4'd6:
					if (rst_settle_r == {4 {1'sb0}})
						dstate_r <= 4'd7;
					else
						rst_settle_r <= rst_settle_r - 4'd1;
				4'd7: begin
					drp_addr_o <= DADDR_POWER_C;
					drp_di_o <= POWER_ALL_C;
					drp_en_o <= 1'b1;
					drp_we_o <= 1'b1;
					dstate_r <= 4'd8;
				end
				4'd8:
					if (drp_rdy_i) begin
						rd_second_r <= 1'b0;
						dstate_r <= 4'd1;
					end
				4'd3: begin
					drp_addr_o <= (rd_second_r ? DADDR_C0R2_C : DADDR_C0R1_C);
					drp_di_o <= (rd_val_r & ~exp_mask_w) | (exp_val_w & exp_mask_w);
					drp_en_o <= 1'b1;
					drp_we_o <= 1'b1;
					dstate_r <= 4'd4;
				end
				4'd4:
					if (drp_rdy_i) begin
						if (!rd_second_r) begin
							rd_second_r <= 1'b1;
							dstate_r <= 4'd1;
						end
						else begin
							mmcm_rst_o <= 1'b0;
							relock_r <= sv2v_cast_89450(RELOCK_TOUT_P);
							dstate_r <= 4'd9;
						end
					end
				4'd9:
					if (mmcm_locked_s_w) begin
						verified_r <= 1'b1;
						ps_hold_r <= 1'b0;
						dstate_r <= 4'd0;
						state_r <= 3'd3;
						win_valid_r <= 1'b0;
						win_skip_r <= 2'd1;
					end
					else if (relock_r == {$clog2(RELOCK_TOUT_P + 1) {1'sb0}}) begin
						drp_fault_r <= 1'b1;
						ps_hold_r <= 1'b0;
						dstate_r <= 4'd0;
						state_r <= 3'd6;
					end
					else
						relock_r <= relock_r - 1'b1;
				default: dstate_r <= 4'd0;
			endcase
			if ((state_r == 3'd2) && (dstate_r == 4'd5))
				repairing_r <= 1'b1;
			if (|{state_r == 3'd0, state_r == 3'd3})
				repairing_r <= 1'b0;
		end
	end
	reg [1:0] psrst_sync_r;
	wire psrst_n_w = psrst_sync_r[1];
	always @(posedge ps_clk_i) begin : ps_rst_sync
		psrst_sync_r <= {psrst_sync_r[0], rst_n};
	end
	wire [14:0] ps_cmd_w;
	wire ps_req_w;
	cdc_handshake #(.WIDTH(15)) u_batch_hs(
		.src_clk(clk_i),
		.src_rst_n(rst_n),
		.src_in(hs_data_r),
		.src_send(hs_send_r),
		.src_rcv(hs_rcv_w),
		.dest_clk(ps_clk_i),
		.dest_rst_n(psrst_n_w),
		.dest_out(ps_cmd_w),
		.dest_req(ps_req_w)
	);
	reg [1:0] pstate_r;
	reg [13:0] ps_cnt_r;
	reg ps_dir_r;
	reg pend_v_r;
	reg [14:0] pend_r;
	reg [$clog2(PS_TOUT_CYC_P + 1) - 1:0] ps_wd_r;
	function automatic [$clog2(PS_TOUT_CYC_P + 1) - 1:0] sv2v_cast_4B089;
		input reg [$clog2(PS_TOUT_CYC_P + 1) - 1:0] inp;
		sv2v_cast_4B089 = inp;
	endfunction
	always @(posedge ps_clk_i) begin : ps_runner
		if (!psrst_n_w) begin
			pstate_r <= 2'd0;
			ps_en_o <= 1'b0;
			ps_incdec_o <= 1'b0;
			ps_cnt_r <= 1'sb0;
			ps_dir_r <= 1'b0;
			pend_v_r <= 1'b0;
			pend_r <= 1'sb0;
			ps_busy_ps_r <= 1'b0;
			ps_fault_ps_r <= 1'b0;
			ps_wd_r <= 1'sb0;
		end
		else begin
			ps_en_o <= 1'b0;
			if (ps_req_w) begin
				pend_v_r <= 1'b1;
				pend_r <= ps_cmd_w;
			end
			(* full_case, parallel_case *)
			case (pstate_r)
				2'd0: begin
					ps_busy_ps_r <= pend_v_r || ps_req_w;
					if (pend_v_r) begin
						ps_dir_r <= pend_r[14];
						ps_cnt_r <= pend_r[13:0];
						pend_v_r <= ps_req_w;
						pstate_r <= 2'd1;
					end
				end
				2'd1: begin
					ps_busy_ps_r <= 1'b1;
					ps_en_o <= 1'b1;
					ps_incdec_o <= ps_dir_r;
					ps_wd_r <= sv2v_cast_4B089(PS_TOUT_CYC_P);
					pstate_r <= 2'd2;
				end
				2'd2:
					if (ps_done_i) begin
						if (ps_cnt_r <= 14'd1)
							pstate_r <= 2'd0;
						else begin
							ps_cnt_r <= ps_cnt_r - 14'd1;
							pstate_r <= 2'd1;
						end
					end
					else if (ps_wd_r == {$clog2(PS_TOUT_CYC_P + 1) {1'sb0}}) begin
						ps_fault_ps_r <= 1'b1;
						pstate_r <= 2'd0;
					end
					else
						ps_wd_r <= ps_wd_r - 1'b1;
				default: pstate_r <= 2'd0;
			endcase
		end
	end
	function automatic signed [15:0] sv2v_cast_16_signed;
		input reg signed [15:0] inp;
		sv2v_cast_16_signed = inp;
	endfunction
	wire signed [15:0] trim_w = sv2v_cast_16_signed(u_cmd_r >>> 5);
	assign status_o = {trim_w, disc_cnt_r, 1'b0, drp_fault_r, ps_fault_s_w, ps_busy_s_w | hs_send_r, mmcm_locked_s_w, mismatch_r, verified_r, state_r};
endmodule
`default_nettype wire
